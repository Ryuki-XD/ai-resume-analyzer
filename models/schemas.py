"""Data models for the AI Resume Analyzer.

Defines dataclasses used across the application for type-safe data transfer
between services, UI components, and report generation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Priority(Enum):
    """Priority levels for improvement suggestions."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class Suggestion:
    """A single improvement suggestion for the resume.

    Attributes:
        title: Short heading for the suggestion.
        description: Detailed explanation and actionable advice.
        priority: Urgency level (HIGH, MEDIUM, LOW).
    """
    title: str
    description: str
    priority: Priority


@dataclass
class SkillCategory:
    """Skill analysis results for a single category.

    Attributes:
        name: Category display name (e.g., "Programming Languages").
        matched: Skills found in the resume.
        missing: Skills in the job description but absent from the resume.
        score: Match percentage (0–100) for this category.
    """
    name: str
    matched: list[str] = field(default_factory=list)
    missing: list[str] = field(default_factory=list)
    score: float = 0.0


@dataclass
class AnalysisResult:
    """Complete result of a resume analysis.

    Attributes:
        ats_score: Overall ATS compatibility score (0–100).
        matched_keywords: Keywords found in both resume and job description.
        missing_keywords: Keywords in job description but missing from resume.
        skill_categories: Per-category skill breakdown.
        suggestions: Prioritized improvement recommendations.
        resume_text: Raw text extracted from the resume.
        job_description: The job description used for comparison.
        word_count: Total word count of the resume.
        section_feedback: Feedback on resume sections detected.
    """
    ats_score: float = 0.0
    matched_keywords: list[str] = field(default_factory=list)
    missing_keywords: list[str] = field(default_factory=list)
    skill_categories: list[SkillCategory] = field(default_factory=list)
    suggestions: list[Suggestion] = field(default_factory=list)
    resume_text: str = ""
    job_description: str = ""
    word_count: int = 0
    section_feedback: dict[str, bool] = field(default_factory=dict)
