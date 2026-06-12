import pandas as pd
import streamlit as st

from src.access_control import require_demo_access
from src.data_loader import load_workbook
from src.normalization import scorecard_dict
from src.spotify_config import (
    APP_TITLE,
    CHANNEL_GUIDANCE,
    CREATIVE_TERRITORIES,
    ROLE_PERFORMANCE,
)
from src.spotify_recommendations import fatigue_flags, portfolio_insights, role_health, territory_signal
from src.theme import APP_CSS, CHART_COLORS, DANGER, MUTED_BLUE, MUTED_TEAL, PRIMARY_GREEN, WARNING
from src.ui_components import (
    money,
    number,
    percent,
    render_bar_chart,
    render_definition_card,
    render_insight_card,
    render_kpi_card,
    render_recommendation_card,
    render_role_diagnosis,
    render_role_header,
    render_role_signal,
    render_scatter_chart,
    render_section_header,
    render_status_chip,
    safe_table,
)

st.set_page_config(page_title=APP_TITLE, page_icon=":material/analytics:", layout="wide")
st.markdown(APP_CSS, unsafe_allow_html=True)

if not require_demo_access(st.secrets, st.session_state):
    st.stop()


@st.cache_data(ttl=600)
def get_data():
    return load_workbook(st.secrets)


def render_hero() -> None:
    st.markdown(
        """
        <div class="hero-panel">
          <div class="eyebrow">Independent pitch concept · Creative intelligence</div>
          <div class="hero-title">Spotify Advertising Paid Creative Intelligence</div>
          <div class="hero-subtitle">
            This sample shows how the selected creative territories can be measured, compared, refreshed,
            and translated into next-test recommendations.
          </div>
          <div class="hero-flow">
            <span class="flow-step">Tag Creative</span><span class="flow-arrow">→</span>
            <span class="flow-step">Read Performance</span><span class="flow-arrow">→</span>
            <span class="flow-step">Diagnose Signals</span><span class="flow-arrow">→</span>
            <span class="flow-step">Decide What To Make Next</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


workbook = get_data()
with st.sidebar:
    st.markdown(
        """
        <div class="eyebrow">Pitch sample</div>
        <h2 style="margin-top:.35rem">Creative Intelligence</h2>
        <p style="color:#A8B3AD;font-size:.82rem;margin-top:-.4rem">Paid creative diagnostics</p>
        """,
        unsafe_allow_html=True,
    )
    page = st.radio(
        "Navigate",
        [
            "Creative Role Performance",
            "Executive Overview",
            "Portfolio Balance",
            "Creative Territories",
            "Formats + Channels",
            "Fatigue Watchlist",
            "Next Tests / Decision Log",
            "Data Requirements / QA",
        ],
        label_visibility="collapsed",
    )
    st.divider()
    st.markdown(render_status_chip("Demo environment", "positive"), unsafe_allow_html=True)
    st.caption("Access-controlled demo · Sample data only")
    st.caption("Directional signals · Not an official product")

if page == "Creative Role Performance":
    render_section_header(
        "Creative Role Performance",
        "Each role is evaluated against the signals that show whether it is doing its job, with current-period performance compared directly to the prior period.",
        "Role-specific diagnostics",
    )
    st.markdown(
        """
        <div class="hero-flow" style="margin:0 0 1rem">
          <span class="flow-step">Creative Role</span><span class="flow-arrow">→</span>
          <span class="flow-step">Primary Signals</span><span class="flow-arrow">→</span>
          <span class="flow-step">Trend</span><span class="flow-arrow">→</span>
          <span class="flow-step">Diagnosis</span><span class="flow-arrow">→</span>
          <span class="flow-step">Recommended Action</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    performance = workbook.get("report_role_performance")
    if performance.empty:
        render_insight_card(
            "Role-specific trend data is not available yet.",
            title="Performance data unavailable",
            tone="info",
        )
    else:
        for role, definition in ROLE_PERFORMANCE.items():
            role_frame = performance[performance["role"] == role]
            health = role_health(role_frame)
            render_role_header(
                role,
                definition["job"],
                definition["question"],
                str(health["status"]),
                str(health["tone"]),
            )
            signal_columns = st.columns(3, gap="small")
            for column, (_, signal) in zip(signal_columns, role_frame.head(3).iterrows()):
                with column:
                    render_role_signal(
                        str(signal.get("signal_label", signal.get("signal", "Signal"))),
                        float(signal.get("current_value", 0)),
                        float(signal.get("prior_value", 0)),
                        str(signal.get("value_format", "number")),
                        signal.get("lower_is_better", False),
                        str(signal.get("trend_values", "")),
                    )
            render_role_diagnosis(str(health["recommendation"]), str(health["tone"]))

elif page == "Executive Overview":
    render_hero()
    scorecard = scorecard_dict(workbook.get("report_scorecard"))
    metrics = [
        ("Total Spend", "total_spend", money, MUTED_BLUE),
        ("Impressions", "impressions", number, MUTED_TEAL),
        ("Clicks", "clicks", number, PRIMARY_GREEN),
        ("Engagements", "engagements", number, "#B79CFF"),
        ("Conversions", "conversions", number, WARNING),
        ("CTR", "ctr", percent, MUTED_TEAL),
        ("CPL", "cpl", money, MUTED_BLUE),
        ("Mapped Assets", "mapped_asset_count", number, PRIMARY_GREEN),
        ("Unmapped Assets", "unmapped_asset_count", number, DANGER),
    ]
    for start in range(0, len(metrics), 5):
        columns = st.columns(min(5, len(metrics) - start))
        for column, (label, key, formatter, accent) in zip(columns, metrics[start : start + 5]):
            with column:
                render_kpi_card(label, formatter(scorecard.get(key)), accent)
    render_insight_card(
        "This sample shows how the selected creative territories can be measured, compared, refreshed, and translated into next-test recommendations.",
        title="How to read this",
        tone="info",
    )

elif page == "Portfolio Balance":
    render_section_header(
        "Portfolio Balance",
        "See where investment is concentrated and where the production plan needs broader coverage.",
        "Investment architecture",
    )
    role_mix = workbook.get("report_role_mix")
    territories = workbook.get("report_territory_analysis")
    left, right = st.columns(2)
    with left:
        render_bar_chart(role_mix, "role", "spend", "Spend by creative role")
    with right:
        render_bar_chart(territories, "territory", "spend", "Spend by creative territory")
    for insight in portfolio_insights(role_mix, territories):
        render_insight_card(insight, tone="warning")
    render_section_header("Balance Readout", "A planning view of concentrated and underrepresented portfolio segments.", "Production planning")
    safe_table(workbook.get("report_portfolio_balance"), "report_portfolio_balance")
    render_recommendation_card(
        "Develop the selected territories",
        "Build timely Drop Into The Moment variants and version Don’t Just Play — Perform by buyer segment, format, and funnel role.",
    )

elif page == "Creative Territories":
    render_section_header(
        "Creative Territories",
        "Compare the two selected creative territories and identify where to scale, refresh, or improve the next step.",
        "Territory performance",
    )
    territory_columns = st.columns(2)
    for index, (territory, definition) in enumerate(CREATIVE_TERRITORIES.items()):
        with territory_columns[index]:
            render_definition_card(territory, definition, CHART_COLORS[index])
    data = workbook.get("report_territory_analysis").copy()
    if not data.empty:
        median_ctr = data.get("ctr", pd.Series([0])).median()
        median_spend = data.get("spend", pd.Series([0])).median()
        data["creative_implication"] = data.apply(territory_signal, axis=1, args=(median_ctr, median_spend))
        render_scatter_chart(data, "spend", "ctr", "territory", "impressions", "Investment vs. response")
    safe_table(
        data,
        "report_territory_analysis",
        ["territory", "spend", "impressions", "clicks", "engagements", "conversions", "ctr", "cpl", "creative_implication"],
    )

elif page == "Formats + Channels":
    render_section_header(
        "Formats + Channels",
        "Compare territory-specific and shared formats, then connect performance to the role each channel can play.",
        "Activation coverage",
    )
    formats = workbook.get("report_format_analysis")
    render_bar_chart(formats, "format", "spend", "Format investment")
    safe_table(formats, "report_format_analysis")
    render_section_header("Channel × Role Coverage", "Where each channel currently contributes across the creative journey.", "Cross-channel system")
    safe_table(workbook.get("report_channel_role_matrix"), "report_channel_role_matrix")
    with st.expander("Channel interpretation guide"):
        cols = st.columns(2)
        for index, (channel, guidance) in enumerate(CHANNEL_GUIDANCE.items()):
            with cols[index % 2]:
                render_definition_card(channel, guidance, CHART_COLORS[index])

elif page == "Fatigue Watchlist":
    render_section_header(
        "Fatigue Watchlist",
        "Spot assets that need a new hook, proof point, edit, audience version, CTA, or retirement decision.",
        "Creative health",
    )
    data = fatigue_flags(workbook.get("report_fatigue_watchlist"))
    if not data.empty:
        flagged = int((data["fatigue_flag"] | data["spend_efficiency_flag"]).sum())
        cols = st.columns([1, 3])
        with cols[0]:
            render_kpi_card("Assets requiring attention", number(flagged), DANGER if flagged else PRIMARY_GREEN)
        with cols[1]:
            render_insight_card(
                "Priority combines frequency pressure with below-median response and inefficient high-spend assets.",
                title="Watchlist logic",
                tone="warning",
            )
    safe_table(
        data,
        "report_fatigue_watchlist",
        ["asset_id", "asset_name", "channel", "territory", "role", "format", "spend", "avg_frequency", "clicks", "impressions", "ctr", "recommendation"],
    )

elif page == "Next Tests / Decision Log":
    render_section_header(
        "Next Tests / Decision Log",
        "Decide what should be scaled, versioned, refreshed, reframed, replaced, or retired.",
        "Production decisions",
    )
    tests = workbook.get("report_next_tests")
    if not tests.empty:
        for _, row in tests.head(4).iterrows():
            render_recommendation_card(
                str(row.get("suggested_action", "Recommended test")),
                f"{row.get('trigger', '')} Success signal: {row.get('success_signal', '')}",
                status=f"Priority {row.get('priority', '')}",
            )
    render_section_header("Decision Log", "A durable record of signals, actions, ownership, and review timing.", "Operating cadence")
    safe_table(workbook.get("creative_decision_log"), "creative_decision_log")

else:
    render_section_header(
        "Data Requirements / QA",
        "A reliable creative intelligence layer depends on consistent inputs and complete asset taxonomy.",
        "Data foundation",
    )
    safe_table(workbook.get("data_requirements"), "data_requirements")
    gaps = workbook.get("qa_mapping_gaps")
    render_section_header("Mapping Quality", "Identify missing taxonomy before it weakens the next creative readout.", "Quality assurance")
    if gaps.empty:
        render_insight_card("No unmapped assets are present in the current demo dataset.", title="Mapping complete", tone="positive")
    else:
        render_insight_card(
            f"{len(gaps)} asset mapping gap(s) need attention before the next readout.",
            title="Taxonomy cleanup required",
            tone="danger",
        )
        safe_table(gaps, "qa_mapping_gaps")
    render_insight_card(
        "In a live engagement, this depends on a clean handoff from the media agency and consistent creative asset naming.",
        title="Operating requirement",
        tone="info",
    )

for warning in workbook.warnings:
    st.sidebar.caption(warning)
