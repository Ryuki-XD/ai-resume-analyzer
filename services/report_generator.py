"""PDF report generator for analysis results.

Builds a styled, multi-section PDF report using fpdf2 and returns
the binary content for download via Streamlit.
"""

from __future__ import annotations

import re
from datetime import datetime

from fpdf import FPDF

from models.schemas import AnalysisResult, Priority
from utils.logger import get_logger

logger = get_logger(__name__)

# ---------------------------------------------------------------------------
# Color palette (R, G, B)
# ---------------------------------------------------------------------------
_CLR_PRIMARY = (79, 70, 229)       # Indigo
_CLR_SUCCESS = (16, 185, 129)      # Emerald
_CLR_WARNING = (245, 158, 11)      # Amber
_CLR_DANGER = (239, 68, 68)        # Red
_CLR_DARK = (30, 30, 46)           # Dark surface
_CLR_TEXT = (55, 65, 81)           # Gray-700
_CLR_LIGHT_BG = (243, 244, 246)   # Gray-100

# Unicode → Latin-1 fallbacks for fpdf2's built-in fonts
_CHAR_REPLACEMENTS = {
    "—": "-",    # em dash
    "–": "-",    # en dash
    "‘": "'",    # left single quote
    "’": "'",    # right single quote
    "“": '"',    # left double quote
    "”": '"',    # right double quote
    "…": "...",  # ellipsis
    "•": "-",    # bullet
    " ": " ",    # non-breaking space
}


def _sanitize(text: str) -> str:
    """Make text safe for fpdf2's built-in Latin-1 fonts.

    Replaces common typographic characters with ASCII equivalents and
    strips anything else outside Latin-1 (e.g. emoji).
    """
    for src, dst in _CHAR_REPLACEMENTS.items():
        text = text.replace(src, dst)
    text = text.encode("latin-1", errors="ignore").decode("latin-1")
    return re.sub(r" {2,}", " ", text).strip()


class _ReportPDF(FPDF):
    """Custom FPDF subclass with header/footer branding."""

    def header(self) -> None:
        self.set_font("Helvetica", "B", 18)
        self.set_text_color(*_CLR_PRIMARY)
        self.cell(0, 12, "AI Resume Analyzer Report", new_x="LMARGIN", new_y="NEXT", align="C")
        self.set_draw_color(*_CLR_PRIMARY)
        self.set_line_width(0.5)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(6)

    def footer(self) -> None:
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    # --- Helpers -----------------------------------------------------------

    def section_title(self, title: str) -> None:
        """Add a styled section heading."""
        self.ln(4)
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(*_CLR_PRIMARY)
        self.cell(0, 10, _sanitize(title), new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*_CLR_PRIMARY)
        self.set_line_width(0.3)
        self.line(10, self.get_y(), 80, self.get_y())
        self.ln(4)

    def body_text(self, text: str) -> None:
        """Add regular body text."""
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*_CLR_TEXT)
        self.multi_cell(0, 6, _sanitize(text))
        self.ln(2)

    def badge(self, text: str, color: tuple[int, int, int]) -> None:
        """Add a colored inline badge, wrapping to a new line if needed."""
        text = _sanitize(text)
        self.set_font("Helvetica", "B", 9)
        self.set_fill_color(*color)
        self.set_text_color(255, 255, 255)
        w = self.get_string_width(text) + 6
        if self.get_x() + w > self.w - self.r_margin:
            self.ln(8)
        self.cell(w, 6, text, fill=True, new_x="RIGHT", new_y="TOP")
        self.cell(2)  # spacer


def generate_pdf_report(result: AnalysisResult) -> bytes:
    """Generate a formatted PDF report from analysis results.

    Args:
        result: The completed ``AnalysisResult`` to render.

    Returns:
        Raw PDF bytes ready for download.
    """
    logger.info("Generating PDF report…")

    pdf = _ReportPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    # --- Meta info ---------------------------------------------------------
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(
        0, 6,
        f"Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}",
        new_x="LMARGIN", new_y="NEXT", align="R",
    )
    pdf.ln(2)

    # --- ATS Score ---------------------------------------------------------
    pdf.section_title("ATS Compatibility Score")

    score = result.ats_score
    if score >= 75:
        score_color = _CLR_SUCCESS
        verdict = "Excellent"
    elif score >= 50:
        score_color = _CLR_WARNING
        verdict = "Needs Improvement"
    else:
        score_color = _CLR_DANGER
        verdict = "Low Compatibility"

    pdf.set_font("Helvetica", "B", 28)
    pdf.set_text_color(*score_color)
    pdf.cell(0, 14, _sanitize(f"{score:.1f} / 100  —  {verdict}"), new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(4)

    pdf.body_text(f"Word Count: {result.word_count} words")

    # --- Matched Keywords --------------------------------------------------
    pdf.section_title("Matched Keywords")
    if result.matched_keywords:
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(*_CLR_TEXT)
        for kw in result.matched_keywords:
            pdf.badge(kw, _CLR_SUCCESS)
        pdf.ln(8)
    else:
        pdf.body_text("No matching keywords were found.")

    # --- Missing Keywords --------------------------------------------------
    pdf.section_title("Missing Keywords")
    if result.missing_keywords:
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(*_CLR_TEXT)
        for kw in result.missing_keywords:
            pdf.badge(kw, _CLR_DANGER)
        pdf.ln(8)
    else:
        pdf.body_text("Great — no critical keywords are missing!")

    # --- Skill Categories --------------------------------------------------
    pdf.section_title("Skill Analysis by Category")
    for cat in result.skill_categories:
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(*_CLR_DARK)
        pdf.cell(0, 8, _sanitize(f"{cat.name}  —  {cat.score:.0f}%"), new_x="LMARGIN", new_y="NEXT")

        if cat.matched:
            pdf.set_font("Helvetica", "", 9)
            pdf.set_text_color(*_CLR_SUCCESS)
            pdf.multi_cell(0, 6, _sanitize(f"  Matched: {', '.join(cat.matched)}"), new_x="LMARGIN", new_y="NEXT")
        if cat.missing:
            pdf.set_font("Helvetica", "", 9)
            pdf.set_text_color(*_CLR_DANGER)
            pdf.multi_cell(0, 6, _sanitize(f"  Missing: {', '.join(cat.missing)}"), new_x="LMARGIN", new_y="NEXT")
        pdf.ln(3)

    # --- Section Feedback --------------------------------------------------
    pdf.section_title("Resume Sections Detected")
    for section, present in result.section_feedback.items():
        icon = "YES" if present else "NO"
        color = _CLR_SUCCESS if present else _CLR_DANGER
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(*color)
        pdf.cell(0, 6, f"  [{icon}]  {section.title()}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    # --- Suggestions -------------------------------------------------------
    pdf.section_title("Improvement Suggestions")
    priority_colors = {
        Priority.HIGH: _CLR_DANGER,
        Priority.MEDIUM: _CLR_WARNING,
        Priority.LOW: _CLR_SUCCESS,
    }
    for suggestion in result.suggestions:
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(*priority_colors[suggestion.priority])
        pdf.cell(
            0, 7,
            _sanitize(f"[{suggestion.priority.value.upper()}]  {suggestion.title}"),
            new_x="LMARGIN", new_y="NEXT",
        )
        pdf.body_text(f"    {suggestion.description}")
        pdf.ln(1)

    # --- Output ------------------------------------------------------------
    pdf_bytes = pdf.output()
    logger.info("PDF report generated (%d bytes).", len(pdf_bytes))
    return bytes(pdf_bytes)
