"""Dashboard landing page.

Displays a hero section, feature overview cards, and a quick-start
guide for new users.
"""

from __future__ import annotations

import streamlit as st


def render_dashboard() -> None:
    """Render the main dashboard landing page."""

    # --- Hero Section ------------------------------------------------------
    st.markdown(
        """
        <div class="hero-container">
            <h1>📄 AI Resume Analyzer</h1>
            <p>Optimize your resume with AI-powered ATS scoring, keyword analysis,
               and actionable improvement suggestions.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --- Stats Row ---------------------------------------------------------
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            """
            <div class="metric-card animate-in delay-1">
                <div class="metric-icon">📊</div>
                <div class="metric-value">ATS</div>
                <div class="metric-label">Compatibility Scoring</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="metric-card animate-in delay-2">
                <div class="metric-icon">🔍</div>
                <div class="metric-value">NLP</div>
                <div class="metric-label">Keyword Analysis</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
            <div class="metric-card animate-in delay-3">
                <div class="metric-icon">🎯</div>
                <div class="metric-value">Skills</div>
                <div class="metric-label">Gap Identification</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col4:
        st.markdown(
            """
            <div class="metric-card animate-in delay-4">
                <div class="metric-icon">📥</div>
                <div class="metric-value">PDF</div>
                <div class="metric-label">Report Export</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Feature Cards -----------------------------------------------------
    st.markdown('<div class="section-header">✨ Features</div>', unsafe_allow_html=True)

    features = [
        ("📤", "Upload Resume", "Support for PDF and DOCX formats. Simply drag and drop your resume file."),
        ("🤖", "AI Analysis", "TF-IDF powered keyword extraction and cosine similarity scoring."),
        ("📊", "Interactive Charts", "Visualize your results with gauge charts, radar plots, and category bars."),
        ("🏷️", "Keyword Matching", "See exactly which keywords match and which are missing from your resume."),
        ("🎯", "Skill Gap Analysis", "Categorized skill matching across 9 professional domains."),
        ("💡", "Smart Suggestions", "Prioritized, actionable improvement recommendations."),
    ]

    cols = st.columns(3)
    for idx, (icon, title, desc) in enumerate(features):
        with cols[idx % 3]:
            st.markdown(
                f"""
                <div class="feature-card animate-in delay-{idx % 4 + 1}">
                    <div class="feature-icon">{icon}</div>
                    <div class="feature-title">{title}</div>
                    <div class="feature-desc">{desc}</div>
                </div>
                <br>
                """,
                unsafe_allow_html=True,
            )

    # --- Quick Start Guide -------------------------------------------------
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">🚀 Quick Start</div>', unsafe_allow_html=True)

    steps = [
        ("1️⃣", "Navigate to **Analyze Resume** from the sidebar"),
        ("2️⃣", "Upload your resume (PDF or DOCX)"),
        ("3️⃣", "Paste the target job description"),
        ("4️⃣", "Click **Analyze** and review your results"),
        ("5️⃣", "Download the PDF report for your records"),
    ]

    for emoji, step in steps:
        st.markdown(f"{emoji} &nbsp; {step}")
