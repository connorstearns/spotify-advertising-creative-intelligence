from pathlib import Path

APP_TITLE = "Spotify Advertising Paid Creative Intelligence"
SHEET_ID = "1XCLBJmHPR-ACqxwMgpqX9p23iw3vRiWnoLQJTnkO2AQ"
SAMPLE_DIR = Path(__file__).resolve().parents[1] / "data" / "sample_exports"

TABS = [
    "pitch_demo_summary",
    "controls",
    "taxonomy_message_territories",
    "taxonomy_creative_roles",
    "taxonomy_formats",
    "asset_taxonomy_map",
    "raw_paid_media_daily",
    "model_creative_daily",
    "report_scorecard",
    "report_role_mix",
    "report_territory_analysis",
    "report_format_analysis",
    "report_fatigue_watchlist",
    "report_next_tests",
    "qa_mapping_gaps",
    "report_portfolio_balance",
    "report_channel_role_matrix",
    "creative_decision_log",
    "data_requirements",
    "monthly_readout_template",
]

NUMERIC_COLUMNS = {
    "spend",
    "impressions",
    "clicks",
    "engagements",
    "conversions",
    "ctr",
    "cpl",
    "frequency",
    "avg_frequency",
    "mapped_asset_count",
    "unmapped_asset_count",
}

REQUIRED_ROLES = [
    "Problem Framing",
    "Solution Education",
    "Proof & Credibility",
    "Action / Conversion",
]

CREATIVE_TERRITORIES = {
    "Drop Into The Moment": (
        "Real-time culture, trending fandoms, and timely advertiser opportunities. "
        "Shows how brands can identify where fandom is building and act on cultural moments with measurable signals."
    ),
    "Don’t Just Play — Perform": (
        "Creative excellence plus measurable performance. Brings artistry and impact together in a category "
        "often dominated by functionality, metrics, and data."
    ),
}

ROLE_DEFINITIONS = {
    "Problem Framing": "Reframes the buyer's media challenge and creates a reason to care.",
    "Solution Education": "Explains how Spotify Advertising solves that challenge.",
    "Proof & Credibility": "Reduces skepticism with evidence, benchmarks, or case studies.",
    "Action / Conversion": "Creates a clear next step such as download, register, explore, or contact sales.",
}

CHANNEL_GUIDANCE = {
    "LinkedIn": "B2B education, proof, thought leadership, and lead-gen paths",
    "Meta": "Social-first hooks, motion, reach, retargeting, and creative variation",
    "YouTube": "Motion-led education, product storytelling, and cutdowns",
    "Reddit": "Native POVs, discussion prompts, and community-relevant problem framing",
    "Display": "Reinforcement, retargeting, proof points, and CTA support",
    "CTV / TikTok": "Future motion-first awareness and education adaptation",
}
