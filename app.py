import pandas as pd
import streamlit as st

from src.data_loader import load_workbook
from src.normalization import scorecard_dict
from src.spotify_config import APP_TITLE, CHANNEL_GUIDANCE, ROLE_DEFINITIONS
from src.spotify_recommendations import fatigue_flags, portfolio_insights, territory_signal
from src.ui_components import money, number, percent, safe_table, section_intro

st.set_page_config(page_title=APP_TITLE, page_icon="●", layout="wide")
st.markdown(
    """
    <style>
    .stApp { background: #f7f8f7; }
    .block-container { padding-top: 1.5rem; max-width: 1450px; }
    [data-testid="stMetric"] { background: white; border: 1px solid #e5e8e6; padding: 14px; border-radius: 12px; }
    div[data-testid="stSidebar"] { background: #111814; }
    div[data-testid="stSidebar"] * { color: #f5f7f5; }
    h1, h2, h3 { letter-spacing: -0.025em; }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data(ttl=600)
def get_data():
    return load_workbook(st.secrets)


workbook = get_data()
with st.sidebar:
    st.markdown("## Creative Intelligence")
    page = st.radio(
        "Navigate",
        [
            "Overview",
            "Portfolio Balance",
            "Message Territories",
            "Creative Roles",
            "Formats + Channels",
            "Fatigue Watchlist",
            "Next Tests / Decision Log",
            "Data Requirements / QA",
        ],
        label_visibility="collapsed",
    )
    st.divider()
    st.caption(workbook.source_label)
    st.caption("Pitch sample · Directional signals")

if page == "Overview":
    st.title("Spotify Advertising Paid Creative Intelligence")
    st.subheader("This system turns paid creative performance into production decisions.")
    st.caption("A sample creative diagnostics layer for translating paid media signals into creative planning decisions.")
    scorecard = scorecard_dict(workbook.get("report_scorecard"))
    metrics = [
        ("Total Spend", "total_spend", money),
        ("Impressions", "impressions", number),
        ("Clicks", "clicks", number),
        ("Engagements", "engagements", number),
        ("Conversions", "conversions", number),
        ("CTR", "ctr", percent),
        ("CPL", "cpl", money),
        ("Mapped Assets", "mapped_asset_count", number),
        ("Unmapped Assets", "unmapped_asset_count", number),
    ]
    for start in range(0, len(metrics), 5):
        columns = st.columns(min(5, len(metrics) - start))
        for column, (label, key, formatter) in zip(columns, metrics[start : start + 5]):
            column.metric(label, formatter(scorecard.get(key)))
    st.info(
        "**How to read this**\n\nMedia reporting tells us what happened in-platform. This dashboard translates those signals into creative implications: which message territories are working, which roles are missing, which formats need refresh, and what to make next."
    )

elif page == "Portfolio Balance":
    section_intro("Portfolio Balance", "See where investment is concentrated and where the production plan needs broader coverage.")
    role_mix = workbook.get("report_role_mix")
    territories = workbook.get("report_territory_analysis")
    left, right = st.columns(2)
    with left:
        st.subheader("Spend by creative role")
        if not role_mix.empty and {"role", "spend"}.issubset(role_mix):
            st.bar_chart(role_mix.set_index("role")["spend"], color="#1ed760")
        else:
            safe_table(role_mix, "report_role_mix")
    with right:
        st.subheader("Spend by message territory")
        if not territories.empty and {"territory", "spend"}.issubset(territories):
            st.bar_chart(territories.set_index("territory")["spend"], color="#6c5ce7")
        else:
            safe_table(territories, "report_territory_analysis")
    for insight in portfolio_insights(role_mix, territories):
        st.warning(insight)
    st.subheader("Balance readout")
    safe_table(workbook.get("report_portfolio_balance"), "report_portfolio_balance")
    st.caption("Planning cues: add underrepresented roles; build adjacent variants around winning territories; balance proof-heavy creative with problem framing and creative possibility.")

elif page == "Message Territories":
    section_intro("Message Territories", "Rank the narratives earning attention and identify where to scale, refresh, or improve the next step.")
    data = workbook.get("report_territory_analysis").copy()
    if not data.empty:
        median_ctr = data.get("ctr", pd.Series([0])).median()
        median_spend = data.get("spend", pd.Series([0])).median()
        data["creative_implication"] = data.apply(territory_signal, axis=1, args=(median_ctr, median_spend))
        st.bar_chart(data.set_index("territory")[["spend"]], color="#1ed760")
    safe_table(data, "report_territory_analysis", ["territory", "spend", "impressions", "clicks", "engagements", "conversions", "ctr", "cpl", "creative_implication"])

elif page == "Creative Roles":
    section_intro("Creative Roles", "Evaluate each asset by the job it is designed to do, not by a single universal KPI.")
    for role, definition in ROLE_DEFINITIONS.items():
        st.markdown(f"**{role}** — {definition}")
    safe_table(workbook.get("report_role_mix"), "report_role_mix")
    st.info("Problem Framing: attention, engagement, CTR · Solution Education: CTR and content engagement · Proof & Credibility: warm-audience response · Action / Conversion: conversion rate and CPL")

elif page == "Formats + Channels":
    section_intro("Formats + Channels", "Connect format performance to the role each channel can play in the creative system.")
    safe_table(workbook.get("report_format_analysis"), "report_format_analysis")
    st.subheader("Channel × role coverage")
    safe_table(workbook.get("report_channel_role_matrix"), "report_channel_role_matrix")
    with st.expander("Channel interpretation guide"):
        for channel, guidance in CHANNEL_GUIDANCE.items():
            st.markdown(f"**{channel}:** {guidance}")

elif page == "Fatigue Watchlist":
    section_intro("Fatigue Watchlist", "Spot assets that need a new hook, proof point, edit, audience version, CTA, or retirement decision.")
    data = fatigue_flags(workbook.get("report_fatigue_watchlist"))
    if not data.empty:
        flagged = int((data["fatigue_flag"] | data["spend_efficiency_flag"]).sum())
        st.metric("Assets requiring attention", flagged)
    safe_table(data, "report_fatigue_watchlist", ["asset_id", "channel", "territory", "role", "format", "spend", "avg_frequency", "clicks", "impressions", "ctr", "recommendation"])

elif page == "Next Tests / Decision Log":
    section_intro("Next Tests / Decision Log", "The goal is to decide what should be scaled, versioned, refreshed, reframed, replaced, or retired.")
    st.subheader("Recommended production tests")
    safe_table(workbook.get("report_next_tests"), "report_next_tests")
    st.subheader("Decision log")
    safe_table(workbook.get("creative_decision_log"), "creative_decision_log")

else:
    section_intro("Data Requirements / QA", "A reliable creative intelligence layer depends on consistent inputs and complete asset taxonomy.")
    safe_table(workbook.get("data_requirements"), "data_requirements")
    gaps = workbook.get("qa_mapping_gaps")
    st.subheader("Mapping quality")
    if gaps.empty:
        st.success("No unmapped assets are present in the current demo dataset.")
    else:
        st.warning(f"{len(gaps)} asset mapping gap(s) need attention before the next readout.")
        safe_table(gaps, "qa_mapping_gaps")
    st.info("In a live engagement, this depends on a clean handoff from the media agency and consistent creative asset naming.")

for warning in workbook.warnings:
    st.sidebar.caption(warning)

