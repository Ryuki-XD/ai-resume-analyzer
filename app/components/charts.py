"""Interactive Plotly chart components for the Streamlit UI.

All charts use a consistent color palette and are configured for
seamless rendering inside Streamlit with transparent backgrounds.
"""

from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st

from models.schemas import SkillCategory


# Shared layout defaults for transparent, borderless charts
_TRANSPARENT_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, system-ui, sans-serif"),
    margin=dict(l=20, r=20, t=40, b=20),
)


def render_gauge_chart(score: float) -> None:
    """Render an ATS score gauge chart.

    The gauge transitions from red → amber → green as the score
    increases from 0 to 100.

    Args:
        score: ATS compatibility score (0–100).
    """
    if score >= 75:
        bar_color = "#10B981"
    elif score >= 50:
        bar_color = "#F59E0B"
    else:
        bar_color = "#EF4444"

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number+delta",
            value=score,
            number=dict(suffix="/100", font=dict(size=42, color=bar_color)),
            title=dict(text="ATS Compatibility Score", font=dict(size=16)),
            gauge=dict(
                axis=dict(range=[0, 100], tickwidth=2, tickcolor="#6B7280"),
                bar=dict(color=bar_color, thickness=0.75),
                bgcolor="rgba(0,0,0,0.03)",
                borderwidth=0,
                steps=[
                    dict(range=[0, 33], color="rgba(239,68,68,0.1)"),
                    dict(range=[33, 66], color="rgba(245,158,11,0.1)"),
                    dict(range=[66, 100], color="rgba(16,185,129,0.1)"),
                ],
                threshold=dict(
                    line=dict(color=bar_color, width=4),
                    thickness=0.85,
                    value=score,
                ),
            ),
        )
    )

    fig.update_layout(
        **_TRANSPARENT_LAYOUT,
        height=300,
    )

    st.plotly_chart(fig, use_container_width=True)


def render_keyword_chart(
    matched: list[str],
    missing: list[str],
) -> None:
    """Render a horizontal bar chart comparing matched vs. missing keywords.

    Args:
        matched: Keywords found in the resume.
        missing: Keywords missing from the resume.
    """
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=[len(matched)],
            y=["Keywords"],
            orientation="h",
            name="Matched",
            marker=dict(color="#10B981", cornerradius=6),
            text=[f"{len(matched)} matched"],
            textposition="inside",
            textfont=dict(color="white", size=13, family="Inter"),
        )
    )

    fig.add_trace(
        go.Bar(
            x=[len(missing)],
            y=["Keywords"],
            orientation="h",
            name="Missing",
            marker=dict(color="#EF4444", cornerradius=6),
            text=[f"{len(missing)} missing"],
            textposition="inside",
            textfont=dict(color="white", size=13, family="Inter"),
        )
    )

    fig.update_layout(
        **_TRANSPARENT_LAYOUT,
        barmode="stack",
        height=120,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=12),
        ),
        xaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
        yaxis=dict(showticklabels=False, showgrid=False),
    )

    st.plotly_chart(fig, use_container_width=True)


def render_skill_radar(categories: list[SkillCategory]) -> None:
    """Render a radar (spider) chart of skill category scores.

    Args:
        categories: List of ``SkillCategory`` results to plot.
    """
    if not categories:
        st.info("No skill categories to display.")
        return

    # Truncate long names for readability on the radar
    labels = [cat.name.split(" ", 1)[-1][:20] for cat in categories]
    scores = [cat.score for cat in categories]

    # Close the polygon
    labels_closed = labels + [labels[0]]
    scores_closed = scores + [scores[0]]

    fig = go.Figure()

    fig.add_trace(
        go.Scatterpolar(
            r=scores_closed,
            theta=labels_closed,
            fill="toself",
            fillcolor="rgba(79, 70, 229, 0.15)",
            line=dict(color="#4F46E5", width=2.5),
            marker=dict(size=6, color="#4F46E5"),
            name="Your Skills",
        )
    )

    fig.update_layout(
        **_TRANSPARENT_LAYOUT,
        height=400,
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                showticklabels=True,
                tickfont=dict(size=10, color="#9CA3AF"),
                gridcolor="rgba(107,114,128,0.2)",
            ),
            angularaxis=dict(
                tickfont=dict(size=11),
                gridcolor="rgba(107,114,128,0.15)",
            ),
        ),
        showlegend=False,
    )

    st.plotly_chart(fig, use_container_width=True)


def render_category_bars(categories: list[SkillCategory]) -> None:
    """Render horizontal bars for each skill category score.

    Args:
        categories: Skill categories sorted by score.
    """
    if not categories:
        return

    names = [cat.name for cat in categories]
    scores = [cat.score for cat in categories]
    colors = [
        "#EF4444" if s < 33 else "#F59E0B" if s < 66 else "#10B981"
        for s in scores
    ]

    fig = go.Figure(
        go.Bar(
            x=scores,
            y=names,
            orientation="h",
            marker=dict(color=colors, cornerradius=6),
            text=[f"{s:.0f}%" for s in scores],
            textposition="auto",
            textfont=dict(color="white", size=12, family="Inter"),
        )
    )

    fig.update_layout(
        **_TRANSPARENT_LAYOUT,
        height=max(200, len(categories) * 50),
        xaxis=dict(
            range=[0, 100],
            showgrid=True,
            gridcolor="rgba(107,114,128,0.1)",
            title="Match %",
        ),
        yaxis=dict(autorange="reversed"),
    )

    st.plotly_chart(fig, use_container_width=True)
