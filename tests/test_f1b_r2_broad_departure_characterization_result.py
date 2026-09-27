from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUMMARY = (
    ROOT
    / "model"
    / "results"
    / "f1b_r2_broad_departure_characterization_summary_non_authoritative_2026-09-27.json"
)
CELLS = (
    ROOT
    / "model"
    / "results"
    / "f1b_r2_broad_departure_characterization_non_authoritative_2026-09-27.tsv"
)


def load_summary() -> dict:
    return json.loads(SUMMARY.read_text(encoding="utf-8"))


def load_cells() -> list[dict[str, str]]:
    with CELLS.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def test_broad_result_is_complete_but_non_authoritative() -> None:
    result = load_summary()
    assert result["authoritative"] is False
    assert result["design"]["departure_cases"] == 36
    assert result["design"]["restriction_tests"] == 1500
    assert result["design"]["evaluation_replicates_per_cell"] == 20
    assert result["execution_integrity"]["aggregate_cells"] == 75
    assert result["execution_integrity"]["fit_failures_total"] == 0
    assert result["execution_integrity"]["bootstrap_calibration_failures_total"] == 0
    assert result["execution_integrity"]["bootstrap_fit_failures_total"] == 0


def test_aggregate_cell_table_retains_required_outputs() -> None:
    rows = load_cells()
    assert len(rows) == 75

    required = {
        "restriction",
        "role",
        "anchor_id",
        "axis",
        "sign",
        "requested_cbd_rms_distance",
        "achieved",
        "nearest_add",
        "rejections",
        "evaluation_replicates",
        "fit_failure_count",
        "bootstrap_calibration_failure_count",
        "mean_bootstrap_fit_failures",
        "mean_held_out_participant_delta",
        "mean_held_out_item_delta",
    }
    assert required.issubset(rows[0])

    for row in rows:
        assert int(row["evaluation_replicates"]) == 20
        assert int(row["fit_failure_count"]) == 0
        assert int(row["bootstrap_calibration_failure_count"]) == 0
        assert float(row["mean_bootstrap_fit_failures"]) == 0.0


def test_standalone_add_specificity_and_nulls_match_retained_result() -> None:
    rows = load_cells()
    specificity = [
        row
        for row in rows
        if row["role"] == "ADD_SPECIFICITY_NEGATIVE_CONTROL"
    ]
    assert len(specificity) == 12
    assert sum(int(row["rejections"]) for row in specificity) == 9
    assert all(float(row["nearest_add"]) < 1e-12 for row in specificity)

    nulls = {
        row["anchor_id"]: int(row["rejections"])
        for row in rows
        if row["role"] in {
            "ADD_NULL_FALSE_REJECTION",
            "CBD_NULL_FALSE_REJECTION",
        }
    }
    assert nulls == {
        "ADD_ANCHOR": 0,
        "CBD_ANCHOR_1": 1,
        "CBD_ANCHOR_2": 0,
    }


def test_complement_sign_asymmetry_remains_visible() -> None:
    rows = load_cells()

    def cbd_rejections(anchor: str, sign: str) -> list[int]:
        selected = [
            row
            for row in rows
            if row["restriction"] == "CBD_COMPLEMENT_RESTRICTION"
            and row["axis"] == "COMPLEMENT_RELATION_VIOLATION"
            and row["anchor_id"] == anchor
            and row["sign"] == sign
        ]
        selected.sort(key=lambda row: float(row["requested_cbd_rms_distance"]))
        return [int(row["rejections"]) for row in selected]

    assert cbd_rejections("CBD_ANCHOR_2", "1") == [5, 2, 10]
    assert cbd_rejections("CBD_ANCHOR_2", "-1") == [6, 14, 19]


def test_cross_shard_numerical_drift_stays_below_design_tolerance() -> None:
    drift = load_summary()["diagnostics"]["cross_shard_numeric_drift"]
    tolerance = drift["frozen_target_distance_tolerance"]
    assert drift["max_achieved_cbd_rms_range_within_identity"] < tolerance
    assert drift["max_nearest_add_rms_range_within_identity"] < tolerance


def test_result_does_not_promote_human_or_authoritative_gates() -> None:
    result = load_summary()
    assert result["next_gate"].startswith(
        "PREDECLARE_COMPLEMENT_RELATION_SIGN_ASYMMETRY"
    )
    boundary = result["interpretation_boundary"]
    assert "human N" in boundary
    assert "recruitment" in boundary
    assert result["design"]["bootstrap_draws"] == 49
