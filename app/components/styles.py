"""Custom CSS theming for the Streamlit application.

Injects a single ``<style>`` block with CSS custom properties that
work across both light and dark Streamlit themes.
"""

from __future__ import annotations

import streamlit as st


def inject_custom_css() -> None:
    """Inject the application's custom CSS into the Streamlit page.

    Call this once at the top of ``main.py`` after ``st.set_page_config``.
    """
    st.markdown(_CSS, unsafe_allow_html=True)


_CSS = """
<style>
/* ================================================================
   CSS Custom Properties — Light / Dark adaptive
   ================================================================ */
:root {
    --primary: #4F46E5;
    --primary-light: #6366F1;
    --primary-dark: #3730A3;
    --success: #10B981;
    --warning: #F59E0B;
    --danger: #EF4444;
    --surface: #FFFFFF;
    --surface-hover: #F9FAFB;
    --text-primary: #111827;
    --text-secondary: #6B7280;
    --border: #E5E7EB;
    --gradient-start: #4F46E5;
    --gradient-end: #7C3AED;
    --card-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
    --card-shadow-hover: 0 8px 30px rgba(0, 0, 0, 0.10);
    --radius: 16px;
    --radius-sm: 10px;
}

/* Dark mode overrides (Streamlit uses data-theme or class) */
[data-testid="stAppViewContainer"][data-theme="dark"],
.stApp[data-theme="dark"],
[data-theme="dark"] {
    --surface: #1E1E2E;
    --surface-hover: #2A2A3C;
    --text-primary: #E5E7EB;
    --text-secondary: #9CA3AF;
    --border: #374151;
    --card-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
    --card-shadow-hover: 0 8px 30px rgba(0, 0, 0, 0.35);
}

/* ================================================================
   Global Resets
   ================================================================ */
.block-container {
    padding-top: 2rem !important;
    max-width: 1100px;
}

/* ================================================================
   Metric Cards
   ================================================================ */
.metric-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.5rem;
    box-shadow: var(--card-shadow);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    text-align: center;
}

.metric-card:hover {
    box-shadow: var(--card-shadow-hover);
    transform: translateY(-3px);
}

.metric-card .metric-icon {
    font-size: 2rem;
    margin-bottom: 0.5rem;
}

.metric-card .metric-value {
    font-size: 2rem;
    font-weight: 800;
    background: linear-gradient(135deg, var(--gradient-start), var(--gradient-end));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.metric-card .metric-label {
    font-size: 0.85rem;
    color: var(--text-secondary);
    margin-top: 0.25rem;
    font-weight: 500;
    letter-spacing: 0.02em;
}

/* ================================================================
   Suggestion Cards
   ================================================================ */
.suggestion-card {
    border-radius: var(--radius-sm);
    padding: 1.1rem 1.3rem;
    margin-bottom: 0.75rem;
    border-left: 4px solid var(--primary);
    background: var(--surface);
    box-shadow: var(--card-shadow);
    transition: all 0.25s ease;
}

.suggestion-card:hover {
    box-shadow: var(--card-shadow-hover);
    transform: translateX(4px);
}

.suggestion-card.priority-high   { border-left-color: var(--danger);  }
.suggestion-card.priority-medium { border-left-color: var(--warning); }
.suggestion-card.priority-low    { border-left-color: var(--success); }

.suggestion-card .suggestion-title {
    font-weight: 700;
    font-size: 0.95rem;
    margin-bottom: 0.3rem;
}

.suggestion-card .suggestion-body {
    font-size: 0.85rem;
    color: var(--text-secondary);
    line-height: 1.55;
}

.suggestion-card .priority-badge {
    display: inline-block;
    padding: 0.15rem 0.55rem;
    border-radius: 999px;
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 0.4rem;
}

.priority-badge.high   { background: #FEE2E2; color: #B91C1C; }
.priority-badge.medium { background: #FEF3C7; color: #92400E; }
.priority-badge.low    { background: #D1FAE5; color: #065F46; }

/* ================================================================
   Skill Tags
   ================================================================ */
.skill-tag {
    display: inline-block;
    padding: 0.3rem 0.75rem;
    margin: 0.2rem;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.01em;
    transition: transform 0.2s ease;
}

.skill-tag:hover {
    transform: scale(1.06);
}

.skill-tag.matched {
    background: #D1FAE5;
    color: #065F46;
    border: 1px solid #A7F3D0;
}

.skill-tag.missing {
    background: #FEE2E2;
    color: #B91C1C;
    border: 1px solid #FECACA;
}

/* ================================================================
   Hero Section
   ================================================================ */
.hero-container {
    background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 50%, #A855F7 100%);
    border-radius: var(--radius);
    padding: 3rem 2.5rem;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 10px 40px rgba(79, 70, 229, 0.25);
    position: relative;
    overflow: hidden;
}

.hero-container::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 60%);
    animation: heroShimmer 8s ease-in-out infinite;
}

@keyframes heroShimmer {
    0%, 100% { transform: translate(0, 0) rotate(0deg); }
    50% { transform: translate(10%, 10%) rotate(5deg); }
}

.hero-container h1 {
    color: white !important;
    font-size: 2.4rem !important;
    font-weight: 800 !important;
    margin-bottom: 0.6rem !important;
    position: relative;
}

.hero-container p {
    color: rgba(255, 255, 255, 0.9) !important;
    font-size: 1.1rem !important;
    position: relative;
}

/* ================================================================
   Feature Cards (Dashboard)
   ================================================================ */
.feature-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.8rem 1.5rem;
    text-align: center;
    box-shadow: var(--card-shadow);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    height: 100%;
}

.feature-card:hover {
    box-shadow: var(--card-shadow-hover);
    transform: translateY(-4px);
    border-color: var(--primary-light);
}

.feature-card .feature-icon {
    font-size: 2.5rem;
    margin-bottom: 1rem;
}

.feature-card .feature-title {
    font-weight: 700;
    font-size: 1rem;
    margin-bottom: 0.5rem;
}

.feature-card .feature-desc {
    font-size: 0.82rem;
    color: var(--text-secondary);
    line-height: 1.5;
}

/* ================================================================
   Section headers
   ================================================================ */
.section-header {
    font-size: 1.3rem;
    font-weight: 700;
    margin: 1.5rem 0 1rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid var(--primary);
    display: inline-block;
}

/* ================================================================
   Progress Bar Overrides
   ================================================================ */
.stProgress > div > div > div {
    background: linear-gradient(90deg, var(--gradient-start), var(--gradient-end)) !important;
    border-radius: 999px;
}

/* ================================================================
   Sidebar Styling
   ================================================================ */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1E1B4B 0%, #312E81 100%);
}

[data-testid="stSidebar"] .stMarkdown,
[data-testid="stSidebar"] .stRadio label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span {
    color: #E0E7FF !important;
}

[data-testid="stSidebar"] .stRadio > div {
    gap: 0.3rem;
}

/* ================================================================
   File Uploader
   ================================================================ */
[data-testid="stFileUploader"] {
    border: 2px dashed var(--primary-light) !important;
    border-radius: var(--radius) !important;
    padding: 1rem !important;
    transition: border-color 0.3s ease;
}

[data-testid="stFileUploader"]:hover {
    border-color: var(--primary) !important;
}

/* ================================================================
   Button Overrides
   ================================================================ */
.stButton > button {
    border-radius: var(--radius-sm) !important;
    font-weight: 600 !important;
    letter-spacing: 0.02em !important;
    transition: all 0.25s ease !important;
    padding: 0.55rem 1.5rem !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 15px rgba(79, 70, 229, 0.3) !important;
}

.stDownloadButton > button {
    background: linear-gradient(135deg, var(--gradient-start), var(--gradient-end)) !important;
    color: white !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    font-weight: 600 !important;
    padding: 0.6rem 1.5rem !important;
    transition: all 0.25s ease !important;
}

.stDownloadButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(79, 70, 229, 0.35) !important;
}

/* ================================================================
   Animations
   ================================================================ */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}

.animate-in {
    animation: fadeInUp 0.6s ease-out both;
}

/* Staggered animation delays */
.delay-1 { animation-delay: 0.1s; }
.delay-2 { animation-delay: 0.2s; }
.delay-3 { animation-delay: 0.3s; }
.delay-4 { animation-delay: 0.4s; }
</style>
"""
