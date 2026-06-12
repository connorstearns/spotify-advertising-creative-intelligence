PAGE_BG = "#0B0F0E"
CARD_BG = "#151A18"
CARD_BG_ALT = "#1E2421"
BORDER = "#2A332F"
PRIMARY_GREEN = "#1DB954"
TEXT_PRIMARY = "#F4F7F5"
TEXT_SECONDARY = "#A8B3AD"
WARNING = "#F6C85F"
DANGER = "#F26D6D"
MUTED_BLUE = "#7BA7FF"
MUTED_TEAL = "#65D6C0"

CHART_COLORS = [
    MUTED_BLUE,
    MUTED_TEAL,
    PRIMARY_GREEN,
    WARNING,
    "#B79CFF",
    "#E58AAE",
    "#8C9A94",
]

APP_CSS = f"""
<style>
:root {{
  --page-bg: {PAGE_BG};
  --card-bg: {CARD_BG};
  --card-bg-alt: {CARD_BG_ALT};
  --border: {BORDER};
  --green: {PRIMARY_GREEN};
  --text-primary: {TEXT_PRIMARY};
  --text-secondary: {TEXT_SECONDARY};
}}

.stApp {{
  background:
    radial-gradient(circle at 78% -15%, rgba(29, 185, 84, 0.10), transparent 28rem),
    var(--page-bg);
  color: var(--text-primary);
}}

.block-container {{
  max-width: 1480px;
  padding: 2rem 2.25rem 4rem;
}}

[data-testid="stHeader"] {{ background: rgba(11, 15, 14, 0.88); }}
[data-testid="stSidebar"] {{
  background: #0E1311;
  border-right: 1px solid var(--border);
}}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stCaption {{ color: var(--text-secondary); }}
[data-testid="stSidebar"] div[role="radiogroup"] label {{
  border-radius: 8px;
  padding: 0.5rem 0.65rem;
  transition: background 120ms ease;
}}
[data-testid="stSidebar"] div[role="radiogroup"] label:hover {{
  background: var(--card-bg-alt);
}}
[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {{
  background: rgba(29, 185, 84, 0.12);
  color: var(--text-primary);
}}

h1, h2, h3 {{
  color: var(--text-primary);
  letter-spacing: -0.035em;
}}
p, li, label {{ color: var(--text-primary); }}
.stCaption, [data-testid="stCaptionContainer"] {{ color: var(--text-secondary) !important; }}
hr {{ border-color: var(--border) !important; }}

.hero-panel {{
  position: relative;
  overflow: hidden;
  padding: 2.25rem 2.4rem 2rem;
  margin-bottom: 1.25rem;
  border: 1px solid var(--border);
  border-radius: 18px;
  background: linear-gradient(135deg, #18201C 0%, #111614 68%, #152019 100%);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.22);
}}
.hero-panel::after {{
  content: "";
  position: absolute;
  width: 220px;
  height: 220px;
  right: -85px;
  top: -110px;
  border-radius: 50%;
  background: rgba(29, 185, 84, 0.14);
  filter: blur(2px);
}}
.eyebrow {{
  color: var(--green);
  font-size: 0.74rem;
  font-weight: 700;
  letter-spacing: 0.13em;
  text-transform: uppercase;
}}
.hero-title {{
  max-width: 900px;
  margin: 0.45rem 0 0.6rem;
  color: var(--text-primary);
  font-size: clamp(2rem, 4vw, 3.55rem);
  line-height: 1.02;
  font-weight: 750;
  letter-spacing: -0.055em;
}}
.hero-subtitle {{
  max-width: 810px;
  color: var(--text-secondary);
  font-size: 1.03rem;
  line-height: 1.55;
}}
.hero-flow {{
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.55rem;
  margin-top: 1.45rem;
}}
.flow-step {{
  padding: 0.42rem 0.7rem;
  border: 1px solid var(--border);
  border-radius: 999px;
  background: rgba(30, 36, 33, 0.8);
  color: var(--text-primary);
  font-size: 0.78rem;
  font-weight: 600;
}}
.flow-arrow {{ color: var(--green); font-size: 0.82rem; }}

.access-panel {{
  margin-top: 14vh;
  padding: 2rem 2rem 1.5rem;
  border: 1px solid var(--border);
  border-bottom: 0;
  border-radius: 18px 18px 0 0;
  background: linear-gradient(145deg, #18201C 0%, #111614 72%);
  box-shadow: 0 24px 70px rgba(0, 0, 0, 0.28);
}}
.access-title {{
  margin-top: 0.55rem;
  color: var(--text-primary);
  font-size: 2rem;
  font-weight: 740;
  line-height: 1.08;
  letter-spacing: -0.045em;
}}
.access-copy {{
  margin-top: 0.75rem;
  color: var(--text-secondary);
  line-height: 1.5;
}}
[data-testid="stForm"] {{
  padding: 0.25rem 2rem 2rem;
  border: 1px solid var(--border);
  border-top: 0;
  border-radius: 0 0 18px 18px;
  background: var(--card-bg);
}}
[data-testid="stTextInput"] input {{
  color: var(--text-primary);
  border-color: var(--border);
  background: var(--card-bg-alt);
}}
[data-testid="stFormSubmitButton"] button {{
  min-height: 2.8rem;
  border: 1px solid var(--green);
  background: var(--green);
  color: #07100A;
  font-weight: 720;
}}
[data-testid="stFormSubmitButton"] button:hover {{
  border-color: #36D36D;
  background: #36D36D;
  color: #07100A;
}}

.section-header {{ margin: 0.7rem 0 1rem; }}
.section-kicker {{
  color: var(--green);
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}}
.section-title {{
  margin: 0.25rem 0 0.25rem;
  color: var(--text-primary);
  font-size: 1.9rem;
  font-weight: 720;
  letter-spacing: -0.04em;
}}
.section-copy {{
  max-width: 820px;
  color: var(--text-secondary);
  line-height: 1.5;
}}

.kpi-card, .insight-card, .recommendation-card, .definition-card {{
  height: 100%;
  border: 1px solid var(--border);
  border-radius: 13px;
  background: var(--card-bg);
}}
.kpi-card {{ min-height: 112px; padding: 1rem 1.05rem; }}
.kpi-label {{
  color: var(--text-secondary);
  font-size: 0.72rem;
  font-weight: 650;
  letter-spacing: 0.07em;
  text-transform: uppercase;
}}
.kpi-value {{
  margin-top: 0.48rem;
  color: var(--text-primary);
  font-size: 1.7rem;
  font-weight: 720;
  letter-spacing: -0.035em;
}}
.kpi-accent {{
  width: 28px;
  height: 3px;
  margin-top: 0.7rem;
  border-radius: 10px;
  background: var(--accent, var(--green));
}}
.insight-card, .recommendation-card, .definition-card {{
  padding: 1rem 1.1rem;
  margin: 0.55rem 0;
  border-left: 3px solid var(--accent, var(--green));
}}
.card-label {{
  color: var(--text-secondary);
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}}
.card-title {{
  margin-top: 0.25rem;
  color: var(--text-primary);
  font-size: 1rem;
  font-weight: 680;
}}
.card-body {{
  margin-top: 0.35rem;
  color: var(--text-secondary);
  font-size: 0.88rem;
  line-height: 1.5;
}}
.status-chip {{
  display: inline-flex;
  align-items: center;
  padding: 0.26rem 0.55rem;
  border: 1px solid color-mix(in srgb, var(--chip) 45%, transparent);
  border-radius: 999px;
  background: color-mix(in srgb, var(--chip) 12%, transparent);
  color: var(--chip);
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.035em;
  text-transform: uppercase;
}}

.role-card-header {{
  margin-top: 0.8rem;
  padding: 1.25rem 1.3rem 0.9rem;
  border: 1px solid var(--border);
  border-bottom: 0;
  border-radius: 15px 15px 0 0;
  background: linear-gradient(135deg, #19201D, var(--card-bg));
}}
.role-card-title-row {{
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 1rem;
}}
.role-card-title {{
  color: var(--text-primary);
  font-size: 1.18rem;
  font-weight: 720;
  letter-spacing: -0.025em;
}}
.role-card-job {{
  margin-top: 0.25rem;
  color: var(--text-secondary);
  font-size: 0.84rem;
}}
.role-question {{
  margin-top: 0.8rem;
  color: var(--text-primary);
  font-size: 0.87rem;
  font-weight: 620;
}}
.role-signal {{
  min-height: 150px;
  padding: 0.9rem 0.95rem 0.7rem;
  border: 1px solid var(--border);
  background: var(--card-bg);
}}
.signal-topline {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
}}
.signal-label {{
  color: var(--text-secondary);
  font-size: 0.72rem;
  font-weight: 680;
  letter-spacing: 0.025em;
}}
.signal-change {{ font-size: 0.76rem; font-weight: 720; }}
.signal-period {{
  margin-top: 0.55rem;
  color: var(--text-secondary);
  font-size: 0.65rem;
  font-weight: 650;
  letter-spacing: 0.055em;
  text-transform: uppercase;
}}
.signal-value {{
  margin-top: 0.15rem;
  color: var(--text-primary);
  font-size: 1.5rem;
  font-weight: 730;
  letter-spacing: -0.035em;
}}
.signal-prior {{
  color: var(--text-secondary);
  font-size: 0.72rem;
}}
.signal-sparkline {{
  display: block;
  width: 100%;
  height: 32px;
  margin-top: 0.5rem;
  overflow: visible;
}}
.role-diagnosis {{
  display: grid;
  grid-template-columns: 1fr 1.35fr;
  gap: 1rem;
  padding: 0.85rem 1rem;
  margin-bottom: 0.8rem;
  border: 1px solid var(--border);
  border-top: 0;
  border-left: 3px solid var(--accent);
  border-radius: 0 0 15px 15px;
  background: var(--card-bg-alt);
}}
.role-diagnosis-item {{
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}}
.role-diagnosis-copy {{
  color: var(--text-primary);
  font-size: 0.84rem;
  line-height: 1.45;
}}

.diagnostic-card {{
  height: 100%;
  padding: 1.15rem 1.2rem;
  margin: 0.45rem 0;
  border: 1px solid var(--border);
  border-radius: 14px;
  background: var(--card-bg);
}}
.diagnostic-card-top {{
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
}}
.diagnostic-title {{
  margin-top: 0.25rem;
  color: var(--text-primary);
  font-size: 1.08rem;
  font-weight: 710;
  letter-spacing: -0.025em;
}}
.diagnostic-grid {{
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 0.75rem;
  margin-top: 1rem;
}}
.diagnostic-field {{
  padding: 0.7rem 0.75rem;
  border: 1px solid var(--border);
  border-radius: 9px;
  background: var(--card-bg-alt);
}}
.diagnostic-label {{
  color: var(--text-secondary);
  font-size: 0.66rem;
  font-weight: 680;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}}
.diagnostic-value {{
  margin-top: 0.25rem;
  color: var(--text-primary);
  font-size: 0.84rem;
  font-weight: 620;
  line-height: 1.35;
}}
.diagnostic-action {{
  display: flex;
  gap: 0.7rem;
  align-items: baseline;
  margin-top: 0.85rem;
  padding-top: 0.8rem;
  border-top: 1px solid var(--border);
  color: var(--text-primary);
  font-size: 0.84rem;
  line-height: 1.45;
}}

[data-testid="stDataFrame"] {{
  overflow: hidden;
  border: 1px solid var(--border);
  border-radius: 12px;
  background: var(--card-bg);
}}
[data-testid="stExpander"] {{
  border: 1px solid var(--border);
  border-radius: 12px;
  background: var(--card-bg);
}}
[data-testid="stAlert"] {{
  border-radius: 12px;
  border: 1px solid var(--border);
  background: var(--card-bg-alt);
}}
[data-testid="stPlotlyChart"] {{
  border: 1px solid var(--border);
  border-radius: 13px;
  background: var(--card-bg);
  padding: 0.35rem;
}}
</style>
"""
