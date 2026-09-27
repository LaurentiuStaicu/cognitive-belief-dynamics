from __future__ import annotations

import csv
import json
from functools import lru_cache
from pathlib import Path

import pytest

from cognitive_epistemic_model.calibration.f1b_r2_projection_bound_sensitivity import (
    run_projection_bound_sensitivity,
)

ROOT = Path(__file__).resolve().parents[1]
CONFIG = (
    ROOT
    / "model"
    / "benchmarks"
    / "f1b_r2_projection_bound_sensitivity.json"
)
DEPARTURES = (
    ROOT
    / "model"
    / "benchmarks"
    / "f1b_r2_controlled_departure_design.json"
)
CASES = (
    ROOT
    / "model"
    / "results"
    / "f1b_r2_complement_sign_geometry_case_summary_2026-09-27.tsv"
)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_cases() -> list[dict]:
    with CASES.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    return [
        {
            **row,
            "sign": int(row["sign"]),
            "requested_cbd_rms_distance": float(
                row["requested_cbd_rms_distance"]
            ),
            "achieved_cbd_rms_distance": float(
                row["achieved_cbd_rms_distance"]
            ),
            "general_coefficients": json.loads(row["general_coefficients"]),
            "nearest_cbd_parameters": json.loads(
                row["nearest_cbd_parameters"]
            ),
        }
        for row in rows
    ]


@lru_cache(maxsize=1)
def result() -> dict:
    return run_projection_bound_sensitivity(
        load_json(CONFIG),
        load_json(DEPARTURES),
        load_cases(),
    )


def test_bound_grid_and_boundary_are_frozen_non_authoritatively() -> None:
    config = load_json(CONFIG)
    assert [
        (row["id"], row["multiplier"])
        for row in config["bound_sets"]
    ] == [
        ("CURRENT_1X", 1),
        ("WIDE_2X", 2),
        ("WIDE_4X", 4),
        ("WIDE_8X", 8),
    ]
    boundary = config["execution_boundary"]
    assert boundary["stochastic_simulation_allowed"] is False
    assert boundary["model_fitting_allowed"] is False
    assert boundary["paired_bootstrap_stage_allowed"] is False
    assert boundary["operational_fitter_bounds_change_allowed"] is False
    assert boundary["departure_regeneration_allowed"] is False
    assert boundary["human_n_frozen"] is False
    assert boundary["participant_recruitment_allowed"] is False
    assert boundary["runtime_f1b_change_allowed"] is False


def test_full_deterministic_audit_is_complete() -> None:
    audit = result()
    assert audit["authoritative"] is False
    assert audit["case_count"] == 12
    assert audit["bound_set_count"] == 4
    assert audit["case_bound_result_count"] == 48
    assert len(audit["case_results"]) == 12
    assert len(audit["sign_comparisons"]) == 24

    for case in audit["case_results"]:
        assert len(case["bound_results"]) == 4
        assert len(case["bound_transitions"]) == 3
        assert {
            row["bound_set_id"] for row in case["bound_results"]
        } == {
            "CURRENT_1X",
            "WIDE_2X",
            "WIDE_4X",
            "WIDE_8X",
        }
        for projection in case["bound_results"]:
            assert len(projection["start_records"]) == 8
            assert projection["successful_start_count"] >= 1


def test_current_projection_reproduces_retained_stage_a_result() -> None:
    for case in result()["case_results"]:
        assert case["current_1x_reproduction_rms_delta"] == pytest.approx(
            0.0,
            abs=1e-8,
        )


def test_nested_bounds_never_worsen_best_projection_objective() -> None:
    for case in result()["case_results"]:
        objectives = [
            float(row["objective"])
            for row in case["bound_results"]
        ]
        assert objectives[1] <= objectives[0] + 1e-10
        assert objectives[2] <= objectives[1] + 1e-10
        assert objectives[3] <= objectives[2] + 1e-10


def test_fixed_general_surfaces_are_not_regenerated() -> None:
    retained = {row["case_id"]: row for row in load_cases()}
    for case in result()["case_results"]:
        assert case["general_coefficients"] == pytest.approx(
            retained[case["case_id"]]["general_coefficients"],
            abs=0.0,
        )
        assert case["requested_cbd_rms_distance"] == pytest.approx(
            retained[case["case_id"]]["requested_cbd_rms_distance"],
            abs=0.0,
        )


def test_each_bound_set_retains_both_signs_for_every_contrast() -> None:
    comparisons = result()["sign_comparisons"]
    assert len(comparisons) == 2 * 3 * 4
    for row in comparisons:
        metrics = row["metrics"]
        assert "nearest_cbd_rms_distance" in metrics
        assert "probability_rms_distance" in metrics
        assert "mean_bernoulli_kl_general_to_nearest_cbd" in metrics
        assert "information_weighted_logit_distance" in metrics


def test_result_cannot_promote_stochastic_or_human_gate() -> None:
    boundary = result()["interpretation_boundary"]
    assert "do not change the operational fitter" in boundary
    assert "do not authorize paired bootstrap" in boundary
    assert "human N" in boundary
    assert "recruitment" in boundary
    assert "runtime F1b" in boundary
