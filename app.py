import pandas as pd
import streamlit as st

from src.access_control import require_demo_access
from src.data_loader import load_workbook
from src.reporting import first_available, format_channel_fit, role_signal_trends
from src.spotify_config import APP_TITLE, CREATIVE_TERRITORIES, ROLE_PERFORMANCE
from src.spotify_recommendations import role_health, signal_status
from src.theme import APP_CSS
from src.ui_components import (
    format_signal_value,
    render_diagnostic_card,
    render_insight_card,
    render_role_diagnosis,
    render_role_header,
    render_role_signal,
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


def bool_value(value) -> bool:
    if isinstance(value, str):
        return value.strip().lower() in {"true", "1", "yes"}
    return bool(value)


def status_tone(status: str) -> str:
    return {
        "Improving": "positive",
        "Stable": "neutral",
        "Watch": "warning",
        "Needs Action": "danger",
    }.get(status, "neutral")


workbook = get_data()
with st.sidebar:
    st.markdown(
        """
        <div class="eyebrow">Pitch sample</div>
        <h2 style="margin-top:.35rem; color:#F4F7F5;">
            Creative <span style="color:#1DB954;">Intelligence</span>
        </h2>
        <p style="color:#1DB954;font-size:.82rem;margin-top:-.4rem">
            Creative diagnostics + production planning
        </p>
        """,
        unsafe_allow_html=True,
    )
    page = st.radio(
        "Navigate",
        [
            "Creative Role Performance",
            "Creative Territories",
            "Format + Channel Fit",
            "Fatigue + Refresh Needs",
            "What To Make Next",
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
        "Is each creative role doing its job? Current-period signals are compared with the prior period to diagnose health and direct the next production action.",
        "Role-specific KPI trends",
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
    performance = role_signal_trends(workbook)
    if performance.empty:
        render_insight_card(
            "Role-specific trend data is not available yet. Add report_role_signal_trends or model_role_signal_trends to enable this view.",
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
            diagnosis = (
                "Signals are strengthening and the role is doing its job."
                if health["status"] == "Improving"
                else "Signals are holding within a narrow range."
                if health["status"] == "Stable"
                else "At least one primary signal is weakening and needs a focused creative response."
            )
            render_role_diagnosis(
                diagnosis,
                str(health["recommendation"]),
                str(health["tone"]),
            )

elif page == "Creative Territories":
    render_section_header(
        "Creative Territories",
        "Compare how the two selected creative territories are performing by role, signal trend, and next move.",
        "Territory diagnostics",
    )
    territory_report = workbook.get("report_territory_analysis")
    cards = st.columns(2)
    for index, (territory, description) in enumerate(CREATIVE_TERRITORIES.items()):
        row = (
            territory_report[territory_report.get("creative_territory", pd.Series(dtype=str)) == territory]
            if not territory_report.empty
            else pd.DataFrame()
        )
        values = row.iloc[0].to_dict() if not row.empty else {}
        status = str(values.get("health_status", "Stable"))
        with cards[index]:
            render_diagnostic_card(
                territory,
                description,
                [
                    ("Strongest role", str(values.get("strongest_role", "Not available"))),
                    ("Weakest role", str(values.get("weakest_role", "Not available"))),
                    ("Improving signal", str(values.get("improving_signal", "Not available"))),
                    ("Watch signal", str(values.get("watch_signal", "Not available"))),
                    ("Role health", str(values.get("role_health_summary", "Awaiting signal data"))),
                ],
                str(values.get("next_recommended_move", "Continue monitoring role-specific signals.")),
                status,
                status_tone(status),
            )

elif page == "Format + Channel Fit":
    render_section_header(
        "Format + Channel Fit",
        "Tie each format to its creative territory, role, channel, and role-relevant primary signal.",
        "Activation diagnostics",
    )
    fit = format_channel_fit(workbook)
    if fit.empty:
        render_insight_card(
            "Format and channel fit data is not available yet.",
            title="Fit data unavailable",
            tone="info",
        )
    else:
        for start in range(0, len(fit), 2):
            columns = st.columns(2)
            for column, (_, row) in zip(columns, fit.iloc[start : start + 2].iterrows()):
                lower_is_better = bool_value(row.get("lower_is_better", False))
                status, tone, change = signal_status(
                    float(row.get("current_value", 0)),
                    float(row.get("prior_value", 0)),
                    lower_is_better,
                )
                value_format = str(row.get("value_format", "number"))
                with column:
                    render_diagnostic_card(
                        str(row.get("format", "Format")),
                        str(row.get("creative_territory", row.get("territory", "Selected territory"))),
                        [
                            ("Creative role", str(row.get("creative_role", row.get("role", "Not available")))),
                            ("Channel", str(row.get("channel", "Not available"))),
                            ("Primary signal", str(row.get("primary_signal", "Not available"))),
                            (
                                "Current / prior",
                                f"{format_signal_value(row.get('current_value', 0), value_format)} / "
                                f"{format_signal_value(row.get('prior_value', 0), value_format)}",
                            ),
                            ("Change", f"{change:+.1%} directional"),
                        ],
                        str(row.get("recommendation", "Continue monitoring role fit.")),
                        status,
                        tone,
                    )

elif page == "Fatigue + Refresh Needs":
    render_section_header(
        "Fatigue + Refresh Needs",
        "Which role-specific signals are weakening, and what type of creative refresh is needed?",
        "Creative health",
    )
    fatigue = workbook.get("report_fatigue_watchlist")
    if fatigue.empty:
        render_insight_card("No fatigue watchlist rows are available.", title="No current watchlist", tone="info")
    else:
        for start in range(0, len(fatigue), 2):
            columns = st.columns(2)
            for column, (_, row) in zip(columns, fatigue.iloc[start : start + 2].iterrows()):
                value_format = str(row.get("value_format", "number"))
                lower_is_better = bool_value(row.get("lower_is_better", False))
                status, tone, change = signal_status(
                    float(row.get("current_value", 0)),
                    float(row.get("prior_value", 0)),
                    lower_is_better,
                )
                with column:
                    render_diagnostic_card(
                        str(row.get("asset_name", row.get("asset_id", "Asset"))),
                        f"{row.get('creative_territory', '')} · {row.get('creative_role', '')}",
                        [
                            ("Asset ID", str(row.get("asset_id", "Not available"))),
                            ("Format / channel", f"{row.get('format', '')} · {row.get('channel', '')}"),
                            ("Declining signal", str(row.get("signal_declining", "Not available"))),
                            (
                                "Current / prior",
                                f"{format_signal_value(row.get('current_value', 0), value_format)} / "
                                f"{format_signal_value(row.get('prior_value', 0), value_format)}",
                            ),
                            ("Change / frequency", f"{change:+.1%} · {row.get('frequency', '-')}x"),
                            ("Refresh type", str(row.get("recommended_refresh_type", "Refresh"))),
                        ],
                        str(row.get("recommended_action", "Refresh the weakening creative signal.")),
                        status,
                        tone,
                    )

elif page == "What To Make Next":
    render_section_header(
        "What To Make Next",
        "The goal is not reporting for reporting’s sake. The goal is to decide what should be scaled, versioned, refreshed, reframed, replaced, or retired.",
        "Production planning",
    )
    recommendations = workbook.get("report_next_tests")
    if recommendations.empty:
        render_insight_card("No production recommendations are available.", title="No next tests", tone="info")
    else:
        for start in range(0, len(recommendations), 2):
            columns = st.columns(2)
            for column, (_, row) in zip(columns, recommendations.iloc[start : start + 2].iterrows()):
                with column:
                    render_diagnostic_card(
                        str(row.get("recommendation", "Recommended test")),
                        str(row.get("creative_territory", "Selected territory")),
                        [
                            ("Creative role", str(row.get("creative_role", "Not available"))),
                            ("Signal to improve", str(row.get("signal_to_improve", "Not available"))),
                            ("Production action", str(row.get("production_action", "Not available"))),
                            ("Owner", str(row.get("owner", "Not assigned"))),
                            ("Rationale", str(row.get("rationale", "Not available"))),
                        ],
                        f"Status: {row.get('status', 'Planned')}",
                        str(row.get("status", "Planned")),
                        "positive" if str(row.get("status", "")).lower() == "in production" else "info",
                    )
    decision_log = workbook.get("creative_decision_log")
    if not decision_log.empty:
        with st.expander("Decision log detail"):
            safe_table(decision_log, "creative_decision_log")

else:
    render_section_header(
        "Data Requirements / QA",
        "A reliable creative intelligence layer depends on approved source access, complete taxonomy, and consistent asset naming.",
        "Data foundation",
    )
    safe_table(workbook.get("data_requirements"), "data_requirements")
    gaps = workbook.get("qa_mapping_gaps")
    if gaps.empty:
        render_insight_card("No mapping gaps are present in the current demo data.", title="Mapping complete", tone="positive")
    else:
        render_insight_card(
            f"{len(gaps)} mapping gap(s) need attention before the next readout.",
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
