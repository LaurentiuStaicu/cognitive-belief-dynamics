from __future__ import annotations

import csv
import json
from pathlib import Path

import pytest

from cognitive_epistemic_model.calibration.f1b_r2_geometry_diagnostics import (
    run_complement_sign_geometry_diagnostic,
)

ROOT = Path(__file__).resolve().parents[1]
CONFIG = (
    ROOT
    / "model"
    / "benchmarks"
    / "f1b_r2_complement_sign_geometry_diagnostic.json"
)
DEPARTURES = (
    ROOT
    / "model"
    / "benchmarks"
    / "f1b_r2_controlled_departure_design.json"
)
SUMMARY = (
    ROOT
    / "model"
    / "results"
    / "f1b_r2_complement_sign_geometry_summary_non_authoritative_2026-09-27.json"
)
CASES = (
    ROOT
    / "model"
    / "results"
    / "f1b_r2_complement_sign_geometry_case_summary_2026-09-27.tsv"
)

# Cross-run optimizer/BLAS drift is expected below the frozen 1e-6
# departure-generation tolerance. A later clean CI rerun observed
# probability-RMS drift of about 1.37e-9 for a retained deterministic
# case, so keep this regression threshold at 1e-8: still 100x tighter
# than the scientific departure-generation tolerance while avoiding
# false failures from numerically equivalent optimizer solutions.
NUMERICAL_REPRODUCTION_ABS_TOL = 1e-8


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_cases() -> list[dict[str, str]]:
    with CASES.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def test_retained_geometry_result_is_non_authoritative_and_complete() -> None:
    summary = load_json(SUMMARY)
    assert summary["authoritative"] is False
    assert summary["execution"]["case_count"] == 12
    assert summary["execution"]["cell_row_count"] == 216
    assert summary["deterministic_finding"]["geometry_asymmetry_present"] is True
    assert summary["next_gate"] == (
        "DETERMINISTIC_NEAREST_CBD_PROJECTION_BOUND_SENSITIVITY_BEFORE_PAIRED_BOOTSTRAP"
    )


def test_case_summary_retains_all_twelve_frozen_cases() -> None:
    rows = load_cases()
    assert len(rows) == 12
    assert {row["anchor_id"] for row in rows} == {
        "CBD_ANCHOR_1",
        "CBD_ANCHOR_2",
    }
    assert {int(row["sign"]) for row in rows} == {-1, 1}
    assert {float(row["requested_cbd_rms_distance"]) for row in rows} == {
        0.1,
        0.25,
        0.5,
    }


def test_retained_case_summaries_reproduce_current_deterministic_engine() -> None:
    rerun = run_complement_sign_geometry_diagnostic(
        load_json(CONFIG),
        load_json(DEPARTURES),
    )
    by_id = {row["case_id"]: row for row in rerun["case_summaries"]}

    for retained in load_cases():
        current = by_id[retained["case_id"]]
        assert float(retained["achieved_cbd_rms_distance"]) == pytest.approx(
            current["achieved_cbd_rms_distance"],
            abs=NUMERICAL_REPRODUCTION_ABS_TOL,
        )
        assert float(retained["probability_rms_distance"]) == pytest.approx(
            current["probability_rms_distance"],
            abs=NUMERICAL_REPRODUCTION_ABS_TOL,
        )
        assert float(
            retained["mean_bernoulli_kl_general_to_nearest_cbd"]
        ) == pytest.approx(
            current["mean_bernoulli_kl_general_to_nearest_cbd"],
            abs=NUMERICAL_REPRODUCTION_ABS_TOL,
        )
        assert json.loads(retained["general_coefficients"]) == pytest.approx(
            current["general_coefficients"],
            abs=NUMERICAL_REPRODUCTION_ABS_TOL,
        )
        assert json.loads(retained["nearest_cbd_parameters"]) == pytest.approx(
            current["nearest_cbd_parameters"],
            abs=NUMERICAL_REPRODUCTION_ABS_TOL,
        )


def test_medium_and_large_plus_geometry_is_less_separated() -> None:
    comparisons = load_json(SUMMARY)["deterministic_finding"]["comparisons"]
    selected = [
        row
        for row in comparisons
        if row["distance"] in {0.25, 0.5}
    ]
    assert len(selected) == 4
    for row in selected:
        assert row["probability_rms_plus_over_minus"] < 0.8
        assert row["mean_kl_plus_over_minus"] < 0.65
        assert row["information_distance_plus_over_minus"] < 0.8


def test_projection_bound_activity_is_explicitly_retained() -> None:
    activity = load_json(SUMMARY)["saturation_and_bounds"][
        "nearest_cbd_projection_bound_activity"
    ]
    assert len(activity) == 12
    active = [
        row
        for row in activity
        if row["active_bounds"]
    ]
    assert len(active) == 9

    anchor2_plus_025 = next(
        row
        for row in activity
        if row["anchor_id"] == "CBD_ANCHOR_2"
        and row["distance"] == 0.25
        and row["sign"] == 1
    )
    assert anchor2_plus_025["active_bounds"] == ["beta_reward=HIGH"]


def test_result_cannot_promote_paired_bootstrap_or_human_gate() -> None:
    summary = load_json(SUMMARY)
    boundary = summary["interpretation_boundary"]
    assert "does not change the frozen departure definition" in boundary
    assert "human N" in boundary
    assert "recruitment" in boundary
    assert "runtime F1b" in boundary
