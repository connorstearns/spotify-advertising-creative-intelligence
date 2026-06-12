import pandas as pd

from src.spotify_recommendations import fatigue_flags, portfolio_insights, role_health, signal_change


def test_portfolio_concentration_and_missing_roles():
    roles = pd.DataFrame({"role": ["Proof & Credibility"], "spend": [100]})
    territories = pd.DataFrame(
        {"territory": ["Don’t Just Play — Perform", "Drop Into The Moment"], "spend": [80, 20]}
    )
    insights = " ".join(portfolio_insights(roles, territories))
    assert "Missing role coverage" in insights
    assert "two selected territories" in insights


def test_selected_territory_recommendation():
    from src.spotify_recommendations import territory_signal

    row = pd.Series(
        {"territory": "Drop Into The Moment", "spend": 100, "ctr": 0.02, "conversions": 10}
    )
    assert "Breaking Drop" in territory_signal(row, median_ctr=0.01, median_spend=200)


def test_fatigue_flag():
    frame = pd.DataFrame(
        {
            "asset_id": ["A", "B"],
            "spend": [1000, 100],
            "ctr": [0.005, 0.02],
            "avg_frequency": [4.0, 1.2],
            "territory": ["Drop Into The Moment", "Don’t Just Play — Perform"],
            "role": ["Problem Framing", "Solution Education"],
        }
    )
    result = fatigue_flags(frame)
    assert bool(result.loc[0, "fatigue_flag"])
    assert "Breaking Drop" in result.loc[0, "recommendation"]


def test_lower_cost_is_treated_as_improvement():
    assert signal_change(90, 100, lower_is_better=True) == 0.1


def test_role_health_returns_needs_action_for_weak_conversion_signals():
    frame = pd.DataFrame(
        {
            "role": ["Action / Conversion"] * 3,
            "current_value": [0.047, 142, 0.63],
            "prior_value": [0.051, 128, 0.68],
            "lower_is_better": [False, True, False],
        }
    )
    health = role_health(frame)
    assert health["status"] == "Needs Action"
    assert "CTA clarity" in health["recommendation"]
