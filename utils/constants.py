"""Application-wide constants and configuration.

Centralizes magic numbers, thresholds, file constraints, and display
labels used throughout the analyzer.
"""

from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent
DATA_DIR: Path = PROJECT_ROOT / "data"
LOGS_DIR: Path = PROJECT_ROOT / "logs"
SKILLS_JSON_PATH: Path = DATA_DIR / "skills.json"

# ---------------------------------------------------------------------------
# File upload constraints
# ---------------------------------------------------------------------------
MAX_FILE_SIZE_MB: int = 10
SUPPORTED_EXTENSIONS: tuple[str, ...] = (".pdf", ".docx")

# ---------------------------------------------------------------------------
# ATS scoring weights (must sum to 1.0)
# ---------------------------------------------------------------------------
SCORE_WEIGHTS: dict[str, float] = {
    "keyword_match": 0.40,
    "skill_match": 0.30,
    "section_presence": 0.15,
    "word_count": 0.15,
}

# ---------------------------------------------------------------------------
# Resume section detection patterns
# ---------------------------------------------------------------------------
EXPECTED_SECTIONS: dict[str, list[str]] = {
    "contact": ["email", "phone", "linkedin", "github", "portfolio"],
    "summary": ["summary", "objective", "profile", "about"],
    "experience": ["experience", "work history", "employment", "work experience"],
    "education": ["education", "academic", "degree", "university", "college"],
    "skills": ["skills", "technical skills", "competencies", "proficiencies"],
    "projects": ["projects", "portfolio", "personal projects"],
    "certifications": ["certifications", "certificates", "licenses"],
}

# ---------------------------------------------------------------------------
# Word count thresholds for scoring
# ---------------------------------------------------------------------------
IDEAL_WORD_COUNT_MIN: int = 400
IDEAL_WORD_COUNT_MAX: int = 800

# ---------------------------------------------------------------------------
# Display labels for skill categories (maps JSON keys → UI labels)
# ---------------------------------------------------------------------------
CATEGORY_DISPLAY_NAMES: dict[str, str] = {
    "programming_languages": "💻 Programming Languages",
    "frameworks_and_libraries": "📦 Frameworks & Libraries",
    "databases": "🗄️ Databases",
    "cloud_and_devops": "☁️ Cloud & DevOps",
    "data_science_and_ml": "🤖 Data Science & ML",
    "tools_and_platforms": "🔧 Tools & Platforms",
    "soft_skills": "🤝 Soft Skills",
    "certifications": "📜 Certifications",
    "security": "🔒 Security",
}

# ---------------------------------------------------------------------------
# Suggestion templates
# ---------------------------------------------------------------------------
SUGGESTION_TEMPLATES: dict[str, str] = {
    "missing_keywords": (
        "Your resume is missing {count} important keywords from the job "
        "description. Incorporate these terms naturally into your experience "
        "bullets and skills section."
    ),
    "short_resume": (
        "Your resume has only {count} words. Most ATS-friendly resumes "
        "contain 400–800 words. Consider expanding your experience "
        "descriptions with quantified achievements."
    ),
    "long_resume": (
        "Your resume has {count} words, which exceeds the recommended "
        "400–800 word range. Consider trimming less relevant details "
        "to keep it concise and targeted."
    ),
    "missing_section": (
        "Your resume appears to be missing a '{section}' section. "
        "Most hiring managers and ATS systems expect to see this section."
    ),
    "low_skill_match": (
        "Only {score:.0f}% of the required {category} skills were found. "
        "Consider highlighting: {skills}."
    ),
}
