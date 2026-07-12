"""Core analysis engine for resume evaluation.

Orchestrates TF-IDF scoring, keyword matching, skill gap analysis,
section detection, and improvement suggestion generation.
"""

from __future__ import annotations

import json
from pathlib import Path

from models.schemas import AnalysisResult, Priority, SkillCategory, Suggestion
from utils.constants import (
    CATEGORY_DISPLAY_NAMES,
    EXPECTED_SECTIONS,
    IDEAL_WORD_COUNT_MAX,
    IDEAL_WORD_COUNT_MIN,
    SCORE_WEIGHTS,
    SKILLS_JSON_PATH,
    SUGGESTION_TEMPLATES,
)
from utils.logger import get_logger
from utils.text_processing import (
    clean_text,
    compute_cosine_similarity,
    extract_keywords,
)

logger = get_logger(__name__)


def _load_skill_database() -> dict[str, list[str]]:
    """Load the skill database from the JSON file."""
    try:
        with open(SKILLS_JSON_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error("Skills database not found at %s", SKILLS_JSON_PATH)
        return {}
    except json.JSONDecodeError as exc:
        logger.error("Invalid JSON in skills database: %s", exc)
        return {}


def _match_skills(
    resume_text: str,
    job_text: str,
    skill_db: dict[str, list[str]],
) -> list[SkillCategory]:
    """Match resume skills against job description per category.

    Only considers skills that appear in the job description so
    the analysis stays relevant to the target role.
    """
    resume_clean = clean_text(resume_text)
    job_clean = clean_text(job_text)
    categories: list[SkillCategory] = []

    for category_key, skills in skill_db.items():
        display_name = CATEGORY_DISPLAY_NAMES.get(category_key, category_key)

        # Only evaluate skills that the job description mentions
        relevant_skills = [s for s in skills if s.lower() in job_clean]
        if not relevant_skills:
            continue

        matched = [s for s in relevant_skills if s.lower() in resume_clean]
        missing = [s for s in relevant_skills if s.lower() not in resume_clean]
        score = (len(matched) / len(relevant_skills) * 100) if relevant_skills else 0

        categories.append(
            SkillCategory(
                name=display_name,
                matched=matched,
                missing=missing,
                score=round(score, 1),
            )
        )

    # Sort by score ascending so weakest areas appear first
    categories.sort(key=lambda c: c.score)
    return categories


def _detect_sections(resume_text: str) -> dict[str, bool]:
    """Detect which expected resume sections are present."""
    text_lower = resume_text.lower()
    return {
        section: any(kw in text_lower for kw in keywords)
        for section, keywords in EXPECTED_SECTIONS.items()
    }


def _compute_word_count_score(word_count: int) -> float:
    """Score based on how close the word count is to the ideal range."""
    if IDEAL_WORD_COUNT_MIN <= word_count <= IDEAL_WORD_COUNT_MAX:
        return 100.0
    elif word_count < IDEAL_WORD_COUNT_MIN:
        return max(0, (word_count / IDEAL_WORD_COUNT_MIN) * 100)
    else:
        # Gradually penalise overly long resumes
        excess = word_count - IDEAL_WORD_COUNT_MAX
        return max(0, 100 - (excess / IDEAL_WORD_COUNT_MAX) * 50)


def _generate_suggestions(
    result: AnalysisResult,
    sections: dict[str, bool],
) -> list[Suggestion]:
    """Build a prioritised list of improvement suggestions."""
    suggestions: list[Suggestion] = []

    # Missing keywords
    if len(result.missing_keywords) > 5:
        suggestions.append(
            Suggestion(
                title="🔑 Add Missing Keywords",
                description=SUGGESTION_TEMPLATES["missing_keywords"].format(
                    count=len(result.missing_keywords)
                ),
                priority=Priority.HIGH,
            )
        )

    # Word count
    if result.word_count < IDEAL_WORD_COUNT_MIN:
        suggestions.append(
            Suggestion(
                title="📝 Expand Your Resume",
                description=SUGGESTION_TEMPLATES["short_resume"].format(
                    count=result.word_count
                ),
                priority=Priority.MEDIUM,
            )
        )
    elif result.word_count > IDEAL_WORD_COUNT_MAX:
        suggestions.append(
            Suggestion(
                title="✂️ Trim Your Resume",
                description=SUGGESTION_TEMPLATES["long_resume"].format(
                    count=result.word_count
                ),
                priority=Priority.LOW,
            )
        )

    # Missing sections
    for section, present in sections.items():
        if not present:
            suggestions.append(
                Suggestion(
                    title=f"📌 Add '{section.title()}' Section",
                    description=SUGGESTION_TEMPLATES["missing_section"].format(
                        section=section.title()
                    ),
                    priority=Priority.HIGH if section in ("experience", "skills") else Priority.MEDIUM,
                )
            )

    # Weak skill categories
    for cat in result.skill_categories:
        if cat.score < 50 and cat.missing:
            top_missing = ", ".join(cat.missing[:5])
            suggestions.append(
                Suggestion(
                    title=f"📊 Improve {cat.name}",
                    description=SUGGESTION_TEMPLATES["low_skill_match"].format(
                        score=cat.score,
                        category=cat.name,
                        skills=top_missing,
                    ),
                    priority=Priority.HIGH if cat.score < 25 else Priority.MEDIUM,
                )
            )

    # Quantifiable achievements
    resume_lower = result.resume_text.lower()
    has_numbers = any(char.isdigit() for char in result.resume_text)
    quantifiers = ["increased", "reduced", "improved", "saved", "generated", "achieved"]
    has_quantifiers = any(q in resume_lower for q in quantifiers)

    if not has_numbers or not has_quantifiers:
        suggestions.append(
            Suggestion(
                title="📈 Add Quantifiable Achievements",
                description=(
                    "Strengthen your experience bullets with measurable "
                    "results. Use numbers, percentages, and action verbs "
                    "like 'Increased revenue by 25%' or 'Reduced latency "
                    "by 40ms'."
                ),
                priority=Priority.MEDIUM,
            )
        )

    # Sort: HIGH → MEDIUM → LOW
    priority_order = {Priority.HIGH: 0, Priority.MEDIUM: 1, Priority.LOW: 2}
    suggestions.sort(key=lambda s: priority_order[s.priority])

    return suggestions


def analyze_resume(resume_text: str, job_description: str) -> AnalysisResult:
    """Run the full analysis pipeline on a resume against a job description.

    Pipeline:
        1. Keyword extraction and matching
        2. Skill category matching
        3. Section detection
        4. ATS score computation (weighted composite)
        5. Suggestion generation

    Args:
        resume_text: Plain text extracted from the resume.
        job_description: The job description to compare against.

    Returns:
        Populated ``AnalysisResult`` with all analysis outputs.
    """
    logger.info("Starting resume analysis…")

    skill_db = _load_skill_database()

    # --- 1. Keyword analysis ---
    job_keywords = extract_keywords(job_description, top_n=40)
    resume_clean = clean_text(resume_text)

    matched_keywords = [kw for kw in job_keywords if kw in resume_clean]
    missing_keywords = [kw for kw in job_keywords if kw not in resume_clean]

    keyword_score = (
        (len(matched_keywords) / len(job_keywords) * 100) if job_keywords else 0
    )

    # --- 2. Skill matching ---
    skill_categories = _match_skills(resume_text, job_description, skill_db)
    avg_skill_score = (
        sum(c.score for c in skill_categories) / len(skill_categories)
        if skill_categories
        else 0
    )

    # --- 3. Section detection ---
    sections = _detect_sections(resume_text)
    section_score = (sum(sections.values()) / len(sections)) * 100

    # --- 4. Word count score ---
    word_count = len(resume_text.split())
    wc_score = _compute_word_count_score(word_count)

    # --- 5. Weighted ATS score ---
    ats_score = (
        SCORE_WEIGHTS["keyword_match"] * keyword_score
        + SCORE_WEIGHTS["skill_match"] * avg_skill_score
        + SCORE_WEIGHTS["section_presence"] * section_score
        + SCORE_WEIGHTS["word_count"] * wc_score
    )

    # Boost with cosine similarity (adds up to 10 bonus points)
    cosine_sim = compute_cosine_similarity(resume_text, job_description)
    ats_score = min(100, ats_score + cosine_sim * 10)

    result = AnalysisResult(
        ats_score=round(ats_score, 1),
        matched_keywords=matched_keywords,
        missing_keywords=missing_keywords,
        skill_categories=skill_categories,
        resume_text=resume_text,
        job_description=job_description,
        word_count=word_count,
        section_feedback=sections,
    )

    # --- 6. Suggestions (needs partially populated result) ---
    result.suggestions = _generate_suggestions(result, sections)

    logger.info("Analysis complete — ATS score: %.1f", result.ats_score)
    return result
