import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src.theme import (
    CARD_BG,
    CHART_COLORS,
    DANGER,
    MUTED_BLUE,
    MUTED_TEAL,
    PAGE_BG,
    PRIMARY_GREEN,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    WARNING,
)


def render_section_header(title: str, copy: str, kicker: str = "Creative diagnostics") -> None:
    st.markdown(
        f"""
        <div class="section-header">
          <div class="section-kicker">{kicker}</div>
          <div class="section-title">{title}</div>
          <div class="section-copy">{copy}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_kpi_card(label: str, value: str, accent: str = PRIMARY_GREEN) -> None:
    st.markdown(
        f"""
        <div class="kpi-card" style="--accent:{accent}">
          <div class="kpi-label">{label}</div>
          <div class="kpi-value">{value}</div>
          <div class="kpi-accent"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_insight_card(
    body: str,
    title: str = "Portfolio signal",
    tone: str = "warning",
) -> None:
    accent = {"positive": PRIMARY_GREEN, "warning": WARNING, "danger": DANGER, "info": MUTED_BLUE}.get(tone, MUTED_BLUE)
    st.markdown(
        f"""
        <div class="insight-card" style="--accent:{accent}">
          <div class="card-label">Insight</div>
          <div class="card-title">{title}</div>
          <div class="card-body">{body}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_status_chip(label: str, tone: str = "neutral") -> str:
    color = {
        "positive": PRIMARY_GREEN,
        "warning": WARNING,
        "danger": DANGER,
        "info": MUTED_BLUE,
        "neutral": TEXT_SECONDARY,
    }.get(tone, TEXT_SECONDARY)
    return f'<span class="status-chip" style="--chip:{color}">{label}</span>'


def render_recommendation_card(title: str, body: str, status: str = "Recommended") -> None:
    st.markdown(
        f"""
        <div class="recommendation-card" style="--accent:{PRIMARY_GREEN}">
          <div class="card-label">{render_status_chip(status, "positive")}</div>
          <div class="card-title">{title}</div>
          <div class="card-body">{body}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_definition_card(title: str, body: str, accent: str = MUTED_TEAL) -> None:
    st.markdown(
        f"""
        <div class="definition-card" style="--accent:{accent}">
          <div class="card-title">{title}</div>
          <div class="card-body">{body}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def format_signal_value(value: float, value_format: str) -> str:
    if pd.isna(value):
        return "-"
    if value_format == "percent":
        return f"{value:.1%}"
    if value_format == "currency":
        return f"${value:,.0f}"
    return f"{value:,.0f}"


def render_role_signal(
    label: str,
    current: float,
    prior: float,
    value_format: str,
    lower_is_better: bool = False,
    trend_values: str = "",
) -> None:
    if isinstance(lower_is_better, str):
        lower_is_better = lower_is_better.strip().lower() in {"true", "1", "yes"}
    if prior:
        raw_change = (current - prior) / abs(prior)
    else:
        raw_change = 0.0
    directional_change = -raw_change if lower_is_better else raw_change
    tone = "positive" if directional_change > 0.02 else "danger" if directional_change < -0.02 else "neutral"
    arrow = "↑" if directional_change > 0.02 else "↓" if directional_change < -0.02 else "→"
    color = PRIMARY_GREEN if tone == "positive" else DANGER if tone == "danger" else TEXT_SECONDARY
    values = []
    for item in str(trend_values).split("|"):
        try:
            values.append(float(item))
        except ValueError:
            continue
    if len(values) >= 2:
        minimum, maximum = min(values), max(values)
        spread = maximum - minimum or 1
        points = " ".join(
            f"{index * (100 / (len(values) - 1)):.1f},{30 - ((value - minimum) / spread * 24):.1f}"
            for index, value in enumerate(values)
        )
        sparkline = (
            f'<svg class="signal-sparkline" viewBox="0 0 100 32" preserveAspectRatio="none">'
            f'<polyline points="{points}" fill="none" stroke="{color}" stroke-width="2.5" '
            f'stroke-linecap="round" stroke-linejoin="round"/></svg>'
        )
    else:
        sparkline = ""
    st.markdown(
        f"""
        <div class="role-signal">
          <div class="signal-topline">
            <span class="signal-label">{label}</span>
            <span class="signal-change" style="color:{color}">{arrow} {abs(raw_change):.1%} vs prior</span>
          </div>
          <div class="signal-period">Current period</div>
          <div class="signal-value">{format_signal_value(current, value_format)}</div>
          <div class="signal-prior">Prior period {format_signal_value(prior, value_format)}</div>
          {sparkline}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_role_header(
    role: str,
    job: str,
    question: str,
    status: str,
    tone: str,
) -> None:
    st.markdown(
        f"""
        <div class="role-card-header">
          <div class="role-card-title-row">
            <div>
              <div class="role-card-title">{role}</div>
              <div class="role-card-job">{job}</div>
            </div>
            <div>{render_status_chip(status, tone)}</div>
          </div>
          <div class="role-question">{question}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_role_diagnosis(diagnosis: str, recommendation: str, tone: str) -> None:
    accent = {
        "positive": PRIMARY_GREEN,
        "warning": WARNING,
        "danger": DANGER,
        "neutral": MUTED_BLUE,
    }.get(tone, MUTED_BLUE)
    st.markdown(
        f"""
        <div class="role-diagnosis" style="--accent:{accent}">
          <div class="role-diagnosis-item">
            <span class="card-label">Diagnosis</span>
            <span class="role-diagnosis-copy">{diagnosis}</span>
          </div>
          <div class="role-diagnosis-item">
            <span class="card-label">Recommended action</span>
            <span class="role-diagnosis-copy">{recommendation}</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_diagnostic_card(
    title: str,
    eyebrow: str,
    fields: list[tuple[str, str]],
    recommendation: str,
    status: str = "Stable",
    tone: str = "neutral",
) -> None:
    field_html = "".join(
        f"""
        <div class="diagnostic-field">
          <div class="diagnostic-label">{label}</div>
          <div class="diagnostic-value">{value}</div>
        </div>
        """
        for label, value in fields
    )
    st.markdown(
        f"""
        <div class="diagnostic-card">
          <div class="diagnostic-card-top">
            <div>
              <div class="card-label">{eyebrow}</div>
              <div class="diagnostic-title">{title}</div>
            </div>
            <div>{render_status_chip(status, tone)}</div>
          </div>
          <div class="diagnostic-grid">{field_html}</div>
          <div class="diagnostic-action">
            <span class="card-label">Next move</span>
            <span>{recommendation}</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _chart_layout(fig: go.Figure, height: int = 390) -> go.Figure:
    fig.update_layout(
        height=height,
        margin=dict(l=20, r=20, t=45, b=20),
        paper_bgcolor=CARD_BG,
        plot_bgcolor=CARD_BG,
        font=dict(color=TEXT_SECONDARY, family="Arial, sans-serif", size=12),
        title_font=dict(color=TEXT_PRIMARY, size=15),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=TEXT_SECONDARY)),
        hoverlabel=dict(bgcolor="#202722", bordercolor="#344039", font_color=TEXT_PRIMARY),
    )
    fig.update_xaxes(gridcolor="#27302C", zerolinecolor="#27302C", linecolor="#27302C")
    fig.update_yaxes(gridcolor="#27302C", zerolinecolor="#27302C", linecolor="#27302C")
    return fig


def render_bar_chart(
    frame: pd.DataFrame,
    category: str,
    value: str,
    title: str,
    color_sequence: list[str] | None = None,
) -> None:
    if frame.empty or not {category, value}.issubset(frame.columns):
        empty_state(title)
        return
    chart = frame.sort_values(value, ascending=True)
    fig = px.bar(
        chart,
        x=value,
        y=category,
        orientation="h",
        color=category,
        color_discrete_sequence=color_sequence or CHART_COLORS,
        title=title,
        text_auto=".2s",
    )
    fig.update_traces(marker_line_width=0, textposition="outside", cliponaxis=False)
    fig.update_layout(showlegend=False, xaxis_title=None, yaxis_title=None)
    if value == "spend":
        fig.update_xaxes(tickprefix="$", separatethousands=True)
    st.plotly_chart(_chart_layout(fig), width="stretch", config={"displayModeBar": False})


def render_scatter_chart(
    frame: pd.DataFrame,
    x: str,
    y: str,
    label: str,
    size: str,
    title: str,
) -> None:
    if frame.empty or not {x, y, label, size}.issubset(frame.columns):
        empty_state(title)
        return
    fig = px.scatter(
        frame,
        x=x,
        y=y,
        text=label,
        size=size,
        color=label,
        color_discrete_sequence=CHART_COLORS,
        title=title,
    )
    fig.update_traces(textposition="top center", marker=dict(opacity=0.88, line=dict(width=1, color=PAGE_BG)))
    fig.update_layout(showlegend=False, xaxis_title=x.replace("_", " ").title(), yaxis_title=y.upper())
    if x == "spend":
        fig.update_xaxes(tickprefix="$", separatethousands=True)
    if y == "ctr":
        fig.update_yaxes(tickformat=".1%")
    st.plotly_chart(_chart_layout(fig), width="stretch", config={"displayModeBar": False})


def empty_state(tab_name: str) -> None:
    render_insight_card(
        f"No demo rows are currently available for {tab_name.replace('_', ' ')}.",
        title="Data not available",
        tone="info",
    )


def safe_table(frame: pd.DataFrame, tab_name: str, columns: list[str] | None = None) -> None:
    if frame.empty:
        empty_state(tab_name)
        return
    selected = [column for column in (columns or list(frame.columns)) if column in frame.columns]
    column_labels = {
        "territory": "Creative Territory",
        "creative_territory": "Creative Territory",
        "role": "Creative Role",
        "format": "Format",
        "asset_id": "Asset ID",
        "asset_name": "Asset Name",
        "avg_frequency": "Avg. Frequency",
        "creative_implication": "Creative Implication",
        "planning_action": "Planning Action",
        "coverage_status": "Coverage Status",
        "spend_share": "Spend Share",
        "suggested_action": "Suggested Action",
        "success_signal": "Success Signal",
        "source_signal": "Source / Signal",
        "next_review": "Next Review",
    }
    column_config = {
        column: st.column_config.Column(column_labels[column])
        for column in selected
        if column in column_labels
    }
    st.dataframe(
        frame[selected],
        width="stretch",
        hide_index=True,
        column_config=column_config,
    )


def money(value) -> str:
    return f"${value:,.0f}" if pd.notna(value) else "-"


def number(value) -> str:
    return f"{value:,.0f}" if pd.notna(value) else "-"


def percent(value) -> str:
    return f"{value:.1%}" if pd.notna(value) else "-"
