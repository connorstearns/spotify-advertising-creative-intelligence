from pathlib import Path

import pandas as pd


SAMPLE_DIR = Path(__file__).resolve().parents[1] / "data" / "sample_exports"

SELECTED_TERRITORIES = {
    "Drop Into The Moment",
    "Don’t Just Play — Perform",
}

EXPECTED_FORMATS = {
    "Breaking Drop",
    "Drop-ins of the Week",
    "Drop the Mic in 60 Seconds",
    "Industry Drops",
    "Play Hard, Perform Hard",
    "Star Performers",
    "Play with Creative. Perform with Numbers.",
    "Performance Proof Card",
    "CTA / Lead Gen Variant",
    "Case Study Card",
    "Stat Animation",
}


def test_visible_territory_reports_only_use_selected_territories():
    taxonomy = pd.read_csv(SAMPLE_DIR / "taxonomy_message_territories.csv")
    report = pd.read_csv(SAMPLE_DIR / "report_territory_analysis.csv")

    assert set(taxonomy["territory"]) == SELECTED_TERRITORIES
    assert set(report["territory"]) == SELECTED_TERRITORIES


def test_format_taxonomy_matches_selected_deck_formats():
    formats = pd.read_csv(SAMPLE_DIR / "taxonomy_formats.csv")

    assert set(formats["format"]) == EXPECTED_FORMATS
    assert set(formats["territory"]) == SELECTED_TERRITORIES | {"Both selected territories"}


def test_role_performance_has_current_prior_and_three_signals_per_role():
    performance = pd.read_csv(SAMPLE_DIR / "report_role_performance.csv")
    expected_roles = {
        "Problem Framing",
        "Solution Education",
        "Proof & Credibility",
        "Action / Conversion",
    }

    assert set(performance["role"]) == expected_roles
    assert performance.groupby("role").size().eq(3).all()
    assert performance[["current_value", "prior_value"]].notna().all().all()
