from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = (
    ROOT
    / "model"
    / "results"
    / "f1b_r2_bootstrap_calibration_screen_non_authoritative_2026-09-27.json"
)


def load() -> dict:
    return json.loads(RESULT.read_text(encoding="utf-8"))


def test_result_retains_full_frozen_screen_summary() -> None:
    result = load()
    assert result["authoritative"] is False
    assert result["design"]["bootstrap_draws"] == [49, 99, 199]
    assert result["design"]["evaluation_replicates_per_draw"] == 20
    assert result["design"]["restriction_tests"] == 300
    assert len(result["summary_rows"]) == 15
    assert len(result["execution"]["partitions"]) == 3


def test_result_has_no_execution_or_bootstrap_failures() -> None:
    for row in load()["summary_rows"]:
        assert row["fit_failures"] == 0
        assert row["bootstrap_calibration_failures"] == 0
        assert row["mean_bootstrap_fit_failures"] == 0


def test_predeclared_advancement_verdict_is_reproducible() -> None:
    advancement = load()["advancement"]
    verdicts = {
        row["bootstrap_draws"]: row for row in advancement["verdicts"]
    }

    assert verdicts[49]["pass"] is True
    assert verdicts[49]["add_specificity_rejections"] == 1
    assert verdicts[49]["cbd_departure_rejections"] == 16

    assert verdicts[99]["pass"] is False
    assert verdicts[99]["add_specificity_rejections"] == 3
    assert verdicts[99]["cbd_departure_rejections"] == 14

    assert verdicts[199]["pass"] is False
    assert verdicts[199]["add_specificity_rejections"] == 1
    assert verdicts[199]["cbd_departure_rejections"] == 13

    assert advancement["passing_draw_counts"] == [49]
    assert advancement["smallest_passing_for_next_non_authoritative_stage"] == 49


def test_screen_result_cannot_promote_authoritative_or_human_gates() -> None:
    result = load()
    advancement = result["advancement"]
    assert advancement["authoritative_draw_count_frozen"] is False
    assert advancement["next_stage"] == (
        "BROADER_NON_AUTHORITATIVE_DEPARTURE_CHARACTERIZATION_ONLY"
    )
    assert "does not validate exact alpha" in result["interpretation_boundary"]
    assert "human N" in result["interpretation_boundary"]


def test_execution_provenance_matches_frozen_source() -> None:
    result = load()
    assert result["provenance"]["source_commit"] == (
        "9206c8e96adc10818d20bff93a290daf0392fe92"
    )
    assert result["provenance"]["config_sha256"] == (
        "213173be9dbb2934fd3ec4201ed2aed509d7ad7712906ddcc7f0dc17c5202f4e"
    )
    assert result["execution"]["github_run_id"] == "36300108050"
    assert result["execution"]["temporary_pr"] == 156
