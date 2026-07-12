"""AI Resume Analyzer — Streamlit Application Entry Point.

Configures the page, injects custom CSS, sets up sidebar navigation,
and routes to the selected page module.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure the project root is on sys.path so all package imports resolve
_project_root = str(Path(__file__).resolve().parent.parent)
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

import streamlit as st

from app.components.styles import inject_custom_css
from app.pages.analyzer import render_analyzer
from app.pages.dashboard import render_dashboard
from utils.logger import get_logger

logger = get_logger(__name__)

# ---------------------------------------------------------------------------
# Page Configuration (must be the first Streamlit call)
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://github.com/Ryuki-XD/ai-resume-analyzer",
        "Report a Bug": "https://github.com/Ryuki-XD/ai-resume-analyzer/issues",
        "About": (
            "**AI Resume Analyzer** v1.0\n\n"
            "Built with Streamlit, scikit-learn, and Plotly.\n\n"
            "Analyze your resume against job descriptions with "
            "AI-powered ATS scoring and keyword analysis."
        ),
    },
)

# ---------------------------------------------------------------------------
# Inject Custom CSS
# ---------------------------------------------------------------------------
inject_custom_css()

# ---------------------------------------------------------------------------
# Sidebar Navigation
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown(
        """
        <div style="text-align:center; padding: 1.5rem 0 1rem 0;">
            <div style="font-size: 2.5rem; margin-bottom: 0.3rem;">📄</div>
            <div style="font-size: 1.1rem; font-weight: 700; color: #E0E7FF;">
                AI Resume Analyzer
            </div>
            <div style="font-size: 0.75rem; color: #A5B4FC; margin-top: 0.2rem;">
                v1.0 &nbsp;•&nbsp; Powered by ML
            </div>
        </div>
        <hr style="border-color: rgba(255,255,255,0.1); margin: 0.5rem 0 1rem 0;">
        """,
        unsafe_allow_html=True,
    )

    page = st.radio(
        "Navigation",
        options=["🏠 Dashboard", "🔬 Analyze Resume"],
        index=0,
        label_visibility="collapsed",
    )

    st.markdown("<br>" * 3, unsafe_allow_html=True)
    st.markdown(
        """
        <hr style="border-color: rgba(255,255,255,0.1); margin: 0.5rem 0;">
        <div style="text-align:center; padding: 0.8rem 0;">
            <div style="font-size: 0.72rem; color: #A5B4FC; line-height: 1.6;">
                Built with ❤️ using<br>
                Streamlit • scikit-learn • Plotly
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------------------
# Page Router
# ---------------------------------------------------------------------------
if page == "🏠 Dashboard":
    render_dashboard()
elif page == "🔬 Analyze Resume":
    render_analyzer()

logger.debug("Page rendered: %s", page.encode("ascii", "ignore").decode())
