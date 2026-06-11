import pandas as pd

from src.spotify_recommendations import fatigue_flags, portfolio_insights


def test_portfolio_concentration_and_missing_roles():
    roles = pd.DataFrame({"role": ["Proof & Credibility"], "spend": [100]})
    territories = pd.DataFrame({"territory": ["Proof & Performance", "Audience Reach"], "spend": [80, 20]})
    insights = " ".join(portfolio_insights(roles, territories))
    assert "Missing role coverage" in insights
    assert "Proof & Performance" in insights


def test_fatigue_flag():
    frame = pd.DataFrame(
        {
            "asset_id": ["A", "B"],
            "spend": [1000, 100],
            "ctr": [0.005, 0.02],
            "avg_frequency": [4.0, 1.2],
        }
    )
    result = fatigue_flags(frame)
    assert bool(result.loc[0, "fatigue_flag"])
    assert result.loc[0, "recommendation"] == "Refresh hook or proof point"

