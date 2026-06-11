import re

import pandas as pd

from src.spotify_config import NUMERIC_COLUMNS


def snake_case(value: object) -> str:
    text = str(value).strip().lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_")


def detect_header_row(raw: pd.DataFrame, max_rows: int = 8) -> int:
    """Find the most likely header row when a sheet contains title copy above data."""
    if raw.empty:
        return 0
    best_index, best_score = 0, -1
    for index in range(min(max_rows, len(raw))):
        values = raw.iloc[index].fillna("").astype(str).str.strip()
        non_empty = values[values.ne("")]
        unique = non_empty.nunique()
        score = len(non_empty) + unique * 0.25
        if len(non_empty) >= 2 and score > best_score:
            best_index, best_score = index, score
    return best_index


def normalize_frame(frame: pd.DataFrame, headerless: bool = False) -> pd.DataFrame:
    if frame is None or frame.empty:
        return pd.DataFrame()
    data = frame.copy()
    if headerless:
        header_index = detect_header_row(data)
        headers = [snake_case(value) for value in data.iloc[header_index]]
        data = data.iloc[header_index + 1 :].copy()
        data.columns = headers
    else:
        data.columns = [snake_case(column) for column in data.columns]
    data = data.loc[:, [column for column in data.columns if column and not column.startswith("unnamed")]]
    data = data.dropna(how="all").reset_index(drop=True)
    for column in set(data.columns) & NUMERIC_COLUMNS:
        cleaned = (
            data[column]
            .astype(str)
            .str.replace(r"[$,%]", "", regex=True)
            .str.replace(",", "", regex=False)
            .str.strip()
        )
        data[column] = pd.to_numeric(cleaned, errors="coerce")
        if column == "ctr":
            original = data[column].dropna()
            if not original.empty and original.median() > 1:
                data[column] = data[column] / 100
    return data


def scorecard_dict(frame: pd.DataFrame) -> dict[str, float]:
    if frame.empty:
        return {}
    if {"kpi", "value"}.issubset(frame.columns):
        return {
            snake_case(row["kpi"]): pd.to_numeric(
                str(row["value"]).replace("$", "").replace(",", "").replace("%", ""),
                errors="coerce",
            )
            for _, row in frame.iterrows()
        }
    return frame.iloc[0].to_dict()

