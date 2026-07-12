"""Reusable card components for the Streamlit UI.

Renders metric cards and suggestion cards as styled HTML blocks.
"""

from __future__ import annotations

import streamlit as st

from models.schemas import Priority, Suggestion


def render_metric_card(
    icon: str,
    value: str,
    label: str,
    delta: str | None = None,
) -> None:
    """Render a styled metric card.

    Args:
        icon: Emoji icon displayed above the value.
        value: Primary metric value (e.g., "78.5").
        label: Description label below the value.
        delta: Optional delta indicator (e.g., "+5%").
    """
    delta_html = f'<div style="color:#10B981;font-size:0.8rem;font-weight:600;">{delta}</div>' if delta else ""

    st.markdown(
        f"""
        <div class="metric-card animate-in">
            <div class="metric-icon">{icon}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-label">{label}</div>
            {delta_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_suggestion_card(suggestion: Suggestion) -> None:
    """Render a styled suggestion card with priority badge.

    Args:
        suggestion: The ``Suggestion`` dataclass to display.
    """
    priority_class = suggestion.priority.value

    st.markdown(
        f"""
        <div class="suggestion-card priority-{priority_class} animate-in">
            <span class="priority-badge {priority_class}">{priority_class}</span>
            <div class="suggestion-title">{suggestion.title}</div>
            <div class="suggestion-body">{suggestion.description}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_skill_tags(skills: list[str], tag_type: str = "matched") -> None:
    """Render a collection of skill tags.

    Args:
        skills: List of skill names.
        tag_type: Either ``"matched"`` (green) or ``"missing"`` (red).
    """
    if not skills:
        st.markdown(
            f'<p style="color:var(--text-secondary);font-style:italic;">No {tag_type} skills.</p>',
            unsafe_allow_html=True,
        )
        return

    tags_html = "".join(
        f'<span class="skill-tag {tag_type}">{skill}</span>' for skill in skills
    )
    st.markdown(f'<div style="margin:0.5rem 0;">{tags_html}</div>', unsafe_allow_html=True)


def render_section_header(text: str) -> None:
    """Render a styled section header.

    Args:
        text: Header text to display.
    """
    st.markdown(
        f'<div class="section-header">{text}</div>',
        unsafe_allow_html=True,
    )
