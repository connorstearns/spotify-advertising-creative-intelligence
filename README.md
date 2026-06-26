# Spotify Advertising Paid Creative Intelligence

A demo Streamlit dashboard for a Spotify Advertising paid creative intelligence pitch. It is a creative diagnostics and production-planning tool that translates paid media signals into decisions about creative roles, territories, formats, channels, trends, fatigue, and next tests.

This sample complements media agency reporting; it does not replace it. The app reads named tabs from a structured Google Sheet when credentials are configured and falls back to matching CSV files in `data/sample_exports/`. Source identifiers and connector details are never shown in the UI.

The illustrative taxonomy uses only the selected WIP creative territories **Drop Into The Moment** and **Don't just perform. Play.** Their language is used as planning metadata, sample asset naming, and next-test prompts rather than as an official campaign or creative gallery.

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

## Keeping the demo app awake

The `Keep Streamlit Dashboard Awake` GitHub Actions workflow opens the deployed Streamlit dashboard in a headless Chrome browser on a low-frequency schedule, and it can also be run manually before a pitch or demo. If Streamlit shows a `Wake up app` button, the workflow clicks it and waits briefly for the app to start. If the button is not present, the app is treated as already awake.

Configure the repository variable `STREAMLIT_APP_URLS` with one or more deployed app URLs, separated by commas:

```text
https://your-dashboard.streamlit.app
```

To run it manually, open the repository in GitHub, go to **Actions**, choose **Keep Streamlit Dashboard Awake**, and select **Run workflow**. The workflow is intentionally low-frequency, uses wake-only Python dependencies from `requirements-wake.txt`, and does not mutate dashboard data.

## What it covers

- Creative Role Performance with current-vs-prior role-specific KPI trends
- Compact diagnostics for the two selected creative territories
- Format and channel fit tied to territory, role, and primary signal
- Role-specific fatigue and recommended refresh type
- Production recommendations and an optional creative decision log
- Data requirements and asset-mapping QA

## Caveats

- Sample data is illustrative and pitch-safe.
- Low-volume signals are directional.
- The dashboard does not prove incrementality.
- Conversion quality depends on the available media and CRM data.
- Real production use requires approved data access, source governance, and appropriate authentication.

## Tests

```powershell
python -m pytest
```
