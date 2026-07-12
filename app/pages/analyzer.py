"""Resume analysis page.

Handles file upload, job description input, analysis execution, result
display (charts, cards, tags), and PDF report export.
"""

from __future__ import annotations

import streamlit as st

from app.components.cards import (
    render_metric_card,
    render_section_header,
    render_skill_tags,
    render_suggestion_card,
)
from app.components.charts import (
    render_category_bars,
    render_gauge_chart,
    render_keyword_chart,
    render_skill_radar,
)
from models.schemas import AnalysisResult
from services.analyzer import analyze_resume
from services.report_generator import generate_pdf_report
from services.resume_parser import parse_resume
from utils.constants import MAX_FILE_SIZE_MB
from utils.logger import get_logger

logger = get_logger(__name__)


def _render_upload_section() -> tuple[object | None, str]:
    """Render the file upload and job description input widgets.

    Returns:
        Tuple of (uploaded_file, job_description_text).
    """
    st.markdown(
        """
        <div class="hero-container" style="padding:2rem 2rem;">
            <h1 style="font-size:1.8rem !important;">🔬 Resume Analyzer</h1>
            <p>Upload your resume and paste the job description to get started.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_upload, col_jd = st.columns(2)

    with col_upload:
        render_section_header("📤 Upload Resume")
        uploaded_file = st.file_uploader(
            "Upload your resume",
            type=["pdf", "docx"],
            help=f"Maximum file size: {MAX_FILE_SIZE_MB} MB",
            label_visibility="collapsed",
        )

        if uploaded_file:
            size_mb = uploaded_file.size / (1024 * 1024)
            if size_mb > MAX_FILE_SIZE_MB:
                st.error(f"File too large ({size_mb:.1f} MB). Maximum is {MAX_FILE_SIZE_MB} MB.")
                uploaded_file = None
            else:
                st.success(f"✅ **{uploaded_file.name}** ({size_mb:.2f} MB)")

    with col_jd:
        render_section_header("📋 Job Description")
        job_description = st.text_area(
            "Paste the job description",
            height=200,
            placeholder="Paste the full job description here to compare against your resume…",
            label_visibility="collapsed",
        )

    return uploaded_file, job_description


def _render_results(result: AnalysisResult) -> None:
    """Render the full analysis results dashboard."""

    # --- Top Metrics Row ---------------------------------------------------
    col1, col2, col3, col4 = st.columns(4)

    score = result.ats_score
    if score >= 75:
        verdict = "Excellent ✨"
    elif score >= 50:
        verdict = "Good 👍"
    elif score >= 25:
        verdict = "Needs Work 🔧"
    else:
        verdict = "Low ⚠️"

    with col1:
        render_metric_card("🎯", f"{score:.1f}", "ATS Score")
    with col2:
        render_metric_card("📝", str(result.word_count), "Word Count")
    with col3:
        render_metric_card("✅", str(len(result.matched_keywords)), "Matched Keywords")
    with col4:
        render_metric_card("❌", str(len(result.missing_keywords)), "Missing Keywords")

    st.markdown("<br>", unsafe_allow_html=True)

    # --- ATS Gauge + Keyword Bar -------------------------------------------
    col_gauge, col_kw = st.columns([1, 1])

    with col_gauge:
        render_section_header("📊 ATS Score Breakdown")
        render_gauge_chart(result.ats_score)
        st.markdown(
            f'<p style="text-align:center;font-weight:600;font-size:1.1rem;">'
            f'Verdict: {verdict}</p>',
            unsafe_allow_html=True,
        )

    with col_kw:
        render_section_header("🔑 Keyword Match Overview")
        render_keyword_chart(result.matched_keywords, result.missing_keywords)

        st.markdown("<br>", unsafe_allow_html=True)

        # Section detection summary
        render_section_header("📑 Resume Sections")
        for section, present in result.section_feedback.items():
            icon = "✅" if present else "❌"
            st.markdown(f"&nbsp;&nbsp;{icon} &nbsp; **{section.title()}**")

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Skill Radar + Category Bars ---------------------------------------
    if result.skill_categories:
        col_radar, col_bars = st.columns([1, 1])

        with col_radar:
            render_section_header("🎯 Skill Radar")
            render_skill_radar(result.skill_categories)

        with col_bars:
            render_section_header("📈 Category Scores")
            render_category_bars(result.skill_categories)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Matched / Missing Keywords ----------------------------------------
    col_matched, col_missing = st.columns(2)

    with col_matched:
        render_section_header("✅ Matched Keywords")
        render_skill_tags(result.matched_keywords, "matched")

    with col_missing:
        render_section_header("❌ Missing Keywords")
        render_skill_tags(result.missing_keywords, "missing")

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Skill Category Details (Expandable) --------------------------------
    if result.skill_categories:
        render_section_header("🏷️ Skill Details by Category")
        for cat in result.skill_categories:
            with st.expander(f"{cat.name} — {cat.score:.0f}%", expanded=cat.score < 50):
                col_m, col_x = st.columns(2)
                with col_m:
                    st.markdown("**Matched:**")
                    render_skill_tags(cat.matched, "matched")
                with col_x:
                    st.markdown("**Missing:**")
                    render_skill_tags(cat.missing, "missing")

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Suggestions -------------------------------------------------------
    render_section_header("💡 Improvement Suggestions")

    if result.suggestions:
        for suggestion in result.suggestions:
            render_suggestion_card(suggestion)
    else:
        st.success("🎉 Your resume looks great! No critical improvements needed.")

    st.markdown("<br>", unsafe_allow_html=True)

    # --- PDF Export --------------------------------------------------------
    render_section_header("📥 Export Report")

    try:
        pdf_bytes = generate_pdf_report(result)
        st.download_button(
            label="📥  Download PDF Report",
            data=pdf_bytes,
            file_name="resume_analysis_report.pdf",
            mime="application/pdf",
            use_container_width=True,
        )
    except Exception as exc:
        logger.error("PDF generation failed: %s", exc)
        st.error(f"Failed to generate PDF report: {exc}")


def render_analyzer() -> None:
    """Render the full analyzer page with upload, analysis, and results."""

    uploaded_file, job_description = _render_upload_section()

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Analyze Button ----------------------------------------------------
    col_left, col_center, col_right = st.columns([1, 2, 1])
    with col_center:
        analyze_clicked = st.button(
            "🚀  Analyze Resume",
            use_container_width=True,
            type="primary",
            disabled=not (uploaded_file and job_description),
        )

    if analyze_clicked and uploaded_file and job_description:
        with st.spinner("🔬 Analyzing your resume…"):
            try:
                # Step 1: Parse
                resume_text = parse_resume(uploaded_file, uploaded_file.name)

                # Step 2: Analyze
                result = analyze_resume(resume_text, job_description)

                # Store in session for persistence across reruns
                st.session_state["analysis_result"] = result

            except ValueError as exc:
                st.error(f"⚠️ {exc}")
                logger.warning("Analysis failed (ValueError): %s", exc)
                return
            except Exception as exc:
                st.error(f"❌ An unexpected error occurred: {exc}")
                logger.error("Analysis failed: %s", exc, exc_info=True)
                return

    # --- Display results if available --------------------------------------
    if "analysis_result" in st.session_state:
        st.markdown("---")
        _render_results(st.session_state["analysis_result"])
