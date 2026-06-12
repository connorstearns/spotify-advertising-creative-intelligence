import pandas as pd

from src.spotify_config import REQUIRED_ROLES, ROLE_PERFORMANCE


def _as_bool(value) -> bool:
    if isinstance(value, str):
        return value.strip().lower() in {"true", "1", "yes"}
    return bool(value)


def signal_change(current: float, prior: float, lower_is_better: bool = False) -> float:
    if pd.isna(current) or pd.isna(prior) or prior == 0:
        return 0.0
    raw_change = (current - prior) / abs(prior)
    return -raw_change if lower_is_better else raw_change


def role_health(role_frame: pd.DataFrame) -> dict[str, str | float]:
    if role_frame.empty:
        return {
            "status": "Stable",
            "tone": "neutral",
            "score": 0.0,
            "recommendation": "Continue monitoring role-specific signals.",
        }
    changes = [
        signal_change(
            row.get("current_value", 0),
            row.get("prior_value", 0),
            _as_bool(row.get("lower_is_better", False)),
        )
        for _, row in role_frame.iterrows()
    ]
    score = sum(changes) / len(changes)
    if score >= 0.05:
        status, tone = "Improving", "positive"
    elif score >= -0.02:
        status, tone = "Stable", "neutral"
    elif score >= -0.07:
        status, tone = "Watch", "warning"
    else:
        status, tone = "Needs Action", "danger"
    recommendation = (
        "Continue the current direction and build the next measured variant."
        if status == "Improving"
        else "Hold the role strategy steady and monitor the next period."
        if status == "Stable"
        else ROLE_PERFORMANCE.get(role_frame.iloc[0].get("role"), {}).get(
            "recommendation", "Refresh the creative approach."
        )
    )
    return {
        "status": status,
        "tone": tone,
        "score": score,
        "recommendation": recommendation,
    }


def portfolio_insights(role_mix: pd.DataFrame, territories: pd.DataFrame) -> list[str]:
    insights = []
    for frame, label, column in [
        (role_mix, "creative role", "role"),
        (territories, "creative territory", "territory"),
    ]:
        if frame.empty or "spend" not in frame or column not in frame:
            continue
        total = frame["spend"].sum()
        if total > 0:
            leader = frame.loc[frame["spend"].idxmax()]
            share = leader["spend"] / total
            if share > 0.5:
                action = (
                    "Rebalance production volume across the two selected territories."
                    if column == "territory"
                    else "Add underrepresented roles within the selected territories."
                )
                insights.append(f"{leader[column]} represents {share:.0%} of {label} spend. {action}")
    present = set(role_mix.get("role", pd.Series(dtype=str)).dropna())
    missing = [role for role in REQUIRED_ROLES if role not in present]
    if missing:
        insights.append(f"Missing role coverage: {', '.join(missing)}. Add underrepresented roles.")
    if not insights:
        insights.append("Coverage is balanced across the two selected creative territories. Continue testing variants within each.")
    return insights


def territory_signal(row: pd.Series, median_ctr: float, median_spend: float) -> str:
    ctr = row.get("ctr", 0) or 0
    spend = row.get("spend", 0) or 0
    conversions = row.get("conversions", 0) or 0
    territory = row.get("territory", "")
    if territory == "Drop Into The Moment" and ctr >= median_ctr:
        return "Build a new Breaking Drop variant for a timely fandom or industry moment."
    if territory == "Don’t Just Play — Perform" and ctr >= median_ctr:
        return "Version “Play with Creative. Perform with numbers.” by buyer segment."
    if ctr >= median_ctr and conversions <= 1:
        return "Interest is strong; strengthen the next step and conversion path."
    if spend >= median_spend and ctr < median_ctr:
        return "High investment with weak response; reframe or refresh."
    if spend < median_spend and ctr >= median_ctr:
        return "Promising early signal; consider scaling or producing more variants."
    return "Maintain coverage and continue learning."


def fatigue_flags(frame: pd.DataFrame) -> pd.DataFrame:
    if frame.empty:
        return frame
    result = frame.copy()
    ctr = result.get("ctr", pd.Series(0, index=result.index)).fillna(0)
    spend = result.get("spend", pd.Series(0, index=result.index)).fillna(0)
    frequency = result.get("avg_frequency", pd.Series(0, index=result.index)).fillna(0)
    median_ctr, median_spend = ctr.median(), spend.median()
    result["fatigue_flag"] = (frequency >= 3) & (ctr < median_ctr)
    result["spend_efficiency_flag"] = (spend >= median_spend) & (ctr < median_ctr)

    def recommendation(row: pd.Series) -> str:
        territory = row.get("territory", "")
        role = row.get("role", "")
        if row["fatigue_flag"] and territory == "Drop Into The Moment":
            return "Build a new Breaking Drop variant for a timely fandom or industry moment"
        if row["fatigue_flag"] and territory == "Don’t Just Play — Perform":
            return "Version the creative excellence hook by buyer segment"
        if row["spend_efficiency_flag"] and role == "Action / Conversion":
            return "Add a clearer next step to the selected territory"
        if row["fatigue_flag"]:
            return "Refresh the hook or proof point"
        if row["spend_efficiency_flag"]:
            return "Reframe the message before adding spend"
        return "Monitor"

    result["recommendation"] = result.apply(recommendation, axis=1)
    return result
