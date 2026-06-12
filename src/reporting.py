import pandas as pd

from src.data_loader import Workbook


def first_available(workbook: Workbook, *tab_names: str) -> pd.DataFrame:
    for tab_name in tab_names:
        frame = workbook.get(tab_name)
        if not frame.empty:
            return frame.copy()
    return pd.DataFrame()


def role_signal_trends(workbook: Workbook) -> pd.DataFrame:
    direct = first_available(
        workbook,
        "report_role_signal_trends",
        "model_role_signal_trends",
        "report_role_performance",
    )
    if not direct.empty:
        return direct
    return derive_role_signal_trends(workbook.get("model_creative_daily"))


def derive_role_signal_trends(frame: pd.DataFrame) -> pd.DataFrame:
    required = {"role", "signal", "current_value", "prior_value"}
    if frame.empty or not required.issubset(frame.columns):
        return pd.DataFrame()
    group_columns = [
        column
        for column in [
            "role",
            "signal",
            "signal_label",
            "value_format",
            "lower_is_better",
        ]
        if column in frame.columns
    ]
    result = (
        frame.groupby(group_columns, dropna=False)[["current_value", "prior_value"]]
        .mean()
        .reset_index()
    )
    if "signal_label" not in result:
        result["signal_label"] = result["signal"].str.replace("_", " ").str.title()
    if "value_format" not in result:
        result["value_format"] = "number"
    if "lower_is_better" not in result:
        result["lower_is_better"] = False
    result["trend_values"] = ""
    return result


def format_channel_fit(workbook: Workbook) -> pd.DataFrame:
    preferred = workbook.get("report_format_channel_fit")
    if not preferred.empty:
        return preferred.copy()
    formats = workbook.get("report_format_analysis")
    if not formats.empty:
        return formats.copy()
    return workbook.get("taxonomy_formats").copy()
