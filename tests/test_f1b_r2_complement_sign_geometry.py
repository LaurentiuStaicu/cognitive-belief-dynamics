from __future__ import annotations

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


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def result() -> dict:
    return run_complement_sign_geometry_diagnostic(
        load(CONFIG),
        load(DEPARTURES),
    )


def test_geometry_stage_is_deterministic_only_by_contract() -> None:
    config = load(CONFIG)
    boundary = config["execution_boundary"]
    assert boundary["stochastic_simulation_allowed"] is False
    assert boundary["model_fitting_allowed"] is False
    assert boundary["paired_bootstrap_stage_allowed"] is False
    assert boundary["human_n_frozen"] is False
    assert boundary["participant_recruitment_allowed"] is False
    assert boundary["runtime_f1b_change_allowed"] is False


def test_geometry_result_covers_exact_complement_grid(result: dict) -> None:
    assert result["authoritative"] is False
    assert result["selected_axis"] == "COMPLEMENT_RELATION_VIOLATION"
    assert result["case_count"] == 12
    assert result["cells_per_case"] == 18
    assert result["cell_row_count"] == 216
    assert len(result["case_summaries"]) == 12
    assert len(result["sign_comparisons"]) == 6


def test_recomputed_utility_rms_matches_frozen_departure(result: dict) -> None:
    for row in result["case_summaries"]:
        assert row["recomputed_utility_rms_distance"] == pytest.approx(
            row["achieved_cbd_rms_distance"],
            abs=1e-10,
        )
        assert row["achieved_cbd_rms_distance"] == pytest.approx(
            row["requested_cbd_rms_distance"],
            abs=1e-6,
        )


def test_probability_and_kl_diagnostics_are_well_formed(result: dict) -> None:
    for row in result["case_summaries"]:
        assert 0.0 <= row["min_probability_general"] <= 1.0
        assert 0.0 <= row["max_probability_general"] <= 1.0
        assert 0.0 <= row["min_probability_nearest_cbd"] <= 1.0
        assert 0.0 <= row["max_probability_nearest_cbd"] <= 1.0
        assert row["probability_rms_distance"] >= 0.0
        assert row["mean_bernoulli_kl_general_to_nearest_cbd"] >= 0.0
        assert row["max_bernoulli_kl_general_to_nearest_cbd"] >= 0.0
        assert row["information_weighted_logit_distance"] >= 0.0
        assert 0 <= row["saturation_count_0.05"] <= 18
        assert 0 <= row["saturation_count_0.10"] <= 18

    for cell in result["cell_rows"]:
        assert 0.0 <= cell["general_probability"] <= 1.0
        assert 0.0 <= cell["nearest_cbd_probability"] <= 1.0
        assert cell["bernoulli_kl_general_to_nearest_cbd"] >= 0.0


def test_each_sign_comparison_contains_plus_and_minus_metrics(
    result: dict,
) -> None:
    expected_metrics = set(load(CONFIG)["comparisons"]["metrics"])
    for comparison in result["sign_comparisons"]:
        assert set(comparison["metrics"]) == expected_metrics
        for metric in comparison["metrics"].values():
            assert "minus" in metric
            assert "plus" in metric
            assert "plus_minus_difference" in metric
            assert "plus_over_minus_ratio" in metric
