import pandas as pd

from src.data_loader import Workbook
from src.reporting import format_channel_fit, role_signal_trends


def workbook_with(**tabs) -> Workbook:
    return Workbook(tabs=tabs, source_label="demo", warnings=[])


def test_role_signal_trends_prefers_report_tab():
    report = pd.DataFrame({"role": ["Problem Framing"], "signal": ["ctr"]})
    model = pd.DataFrame({"role": ["Solution Education"], "signal": ["ctr"]})
    workbook = workbook_with(
        report_role_signal_trends=report,
        model_role_signal_trends=model,
    )

    assert role_signal_trends(workbook).equals(report)


def test_role_signal_trends_derives_from_creative_daily():
    creative_daily = pd.DataFrame(
        {
            "role": ["Problem Framing", "Problem Framing"],
            "signal": ["ctr", "ctr"],
            "current_value": [0.01, 0.012],
            "prior_value": [0.009, 0.01],
        }
    )
    result = role_signal_trends(workbook_with(model_creative_daily=creative_daily))

    assert result.iloc[0]["current_value"] == 0.011
    assert result.iloc[0]["signal_label"] == "Ctr"


def test_format_channel_fit_falls_back_to_format_analysis():
    fallback = pd.DataFrame({"format": ["Breaking Drop"]})
    result = format_channel_fit(workbook_with(report_format_analysis=fallback))

    assert result.equals(fallback)
