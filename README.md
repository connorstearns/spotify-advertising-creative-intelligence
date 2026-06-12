# Spotify Advertising Paid Creative Intelligence

A demo Streamlit dashboard for a Spotify Advertising paid creative intelligence pitch. It is a creative diagnostics and production-planning tool that translates paid media signals into decisions about creative territories, creative roles, formats, channels, fatigue, and next tests.

This sample complements media agency reporting; it does not replace it. The app reads from a structured Google Sheet when credentials are configured and falls back to matching CSV files in `data/sample_exports/`. Source identifiers and connector details are never shown in the UI.

The illustrative taxonomy uses only the selected WIP creative territories **Drop Into The Moment** and **Don’t Just Play — Perform**. Their language is used as planning metadata, sample asset naming, and next-test prompts rather than as an official campaign or creative gallery.

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

The bundled sample exports make the dashboard immediately demo-ready.

## Demo access

Set `app_password` in `.streamlit/secrets.toml` to require a password:

```toml
app_password = "set-this-outside-version-control"
```

The password is never stored in the repository. If `app_password` is omitted, local access is allowed and a warning is written only to the application logs.

## Google Sheets setup

Create `.streamlit/secrets.toml` with a `gcp_service_account` table containing the standard Google service-account fields. Share the source workbook with that service account. If credentials or a requested tab are unavailable, the app falls back to demo CSVs or displays a friendly empty state.

## What it covers

- Creative Role Performance with current-vs-prior role-specific KPI trends
- Secondary executive overview scorecard
- Portfolio balance by creative role and creative territory
- Creative territory, role, format, and channel diagnostics
- Fatigue watchlist
- Next-test recommendations and a creative decision log
- Data requirements and asset-mapping QA

## Caveats

- Sample data is illustrative and pitch-safe.
- Low-volume signals are directional.
- The dashboard does not prove incrementality.
- Conversion quality depends on the available media and CRM data.

## Tests

```powershell
python -m pytest
```
