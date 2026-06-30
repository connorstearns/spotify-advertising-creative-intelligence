import pandas as pd

from src.normalization import detect_header_row, normalize_copy_text, normalize_frame, scorecard_dict


def test_detects_title_row_and_normalizes_columns():
    raw = pd.DataFrame(
        [
            ["Creative performance report", "", ""],
            ["Asset ID", "Total Spend", "CTR"],
            ["A-1", "$1,200", "1.5%"],
        ]
    )
    result = normalize_frame(raw, headerless=True)
    assert detect_header_row(raw) == 1
    assert list(result.columns) == ["asset_id", "total_spend", "ctr"]
    assert result.iloc[0]["asset_id"] == "A-1"


def test_scorecard_kpi_value_shape():
    frame = pd.DataFrame({"kpi": ["Total Spend", "Clicks"], "value": ["$12,000", "350"]})
    assert scorecard_dict(frame) == {"total_spend": 12000, "clicks": 350}


def test_normalizes_old_creative_performance_territory_label():
    assert normalize_copy_text("DON'T JUST PLAY — PERFORM") == "Don't just perform. Play."
    assert (
        normalize_copy_text("Don’t Just Play — Perform is resonating unevenly")
        == "Don't just perform. Play. is resonating unevenly"
    )

    frame = normalize_frame(
        pd.DataFrame({"Creative Territory": ["DOn't Just Play. Perform."]})
    )
    assert frame.iloc[0]["creative_territory"] == "Don't just perform. Play."
