from dataclasses import dataclass

import pandas as pd

from src.normalization import normalize_frame
from src.spotify_config import SAMPLE_DIR, SHEET_ID, TABS


@dataclass
class Workbook:
    tabs: dict[str, pd.DataFrame]
    source_label: str
    warnings: list[str]

    def get(self, name: str) -> pd.DataFrame:
        return self.tabs.get(name, pd.DataFrame())


def load_csv_tabs() -> Workbook:
    tabs, warnings = {}, []
    for tab in TABS:
        path = SAMPLE_DIR / f"{tab}.csv"
        if path.exists():
            try:
                tabs[tab] = normalize_frame(pd.read_csv(path))
            except Exception as exc:
                warnings.append(f"Could not load optional sample tab '{tab}': {exc}")
    return Workbook(tabs=tabs, source_label="Source: demo data", warnings=warnings)


def _credentials_from_secrets(secrets) -> dict | None:
    if "gcp_service_account" in secrets:
        return dict(secrets["gcp_service_account"])
    return None


def load_google_tabs(secrets) -> Workbook:
    import gspread
    from google.oauth2.service_account import Credentials

    info = _credentials_from_secrets(secrets)
    if not info:
        raise ValueError("Google Sheets credentials are not configured.")
    scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
    client = gspread.authorize(Credentials.from_service_account_info(info, scopes=scopes))
    spreadsheet = client.open_by_key(SHEET_ID)
    tabs, warnings = {}, []
    available = {sheet.title: sheet for sheet in spreadsheet.worksheets()}
    for tab in TABS:
        if tab not in available:
            warnings.append(f"Optional workbook tab '{tab}' is unavailable.")
            continue
        values = available[tab].get_all_values()
        if values:
            tabs[tab] = normalize_frame(pd.DataFrame(values), headerless=True)
    return Workbook(tabs=tabs, source_label="Source: sample creative intelligence workbook", warnings=warnings)


def load_workbook(secrets=None) -> Workbook:
    if secrets is not None:
        try:
            return load_google_tabs(secrets)
        except Exception:
            pass
    return load_csv_tabs()

