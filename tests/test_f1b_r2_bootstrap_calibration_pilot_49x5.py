from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PILOT = (
    ROOT
    / "model"
    / "benchmarks"
    / "f1b_r2_bootstrap_calibration_pilot_49x5.json"
)


def load() -> dict:
    return json.loads(PILOT.read_text(encoding="utf-8"))


def test_pilot_is_exactly_49_draws_by_5_replicates() -> None:
    config = load()
    assert config["characterization_id"] == (
        "F1B.R2.BOOTSTRAP_CALIBRATION.PILOT.49X5.2026-09-27"
    )
    assert config["pilot_role"] == "PREDECLARED_LOW_COST_CALIBRATION_PILOT"
    assert config["bootstrap"]["draw_grid"] == [49]
    assert config["bootstrap"]["minimum_successful_draws_by_draw_count"] == {
        "49": 45
    }
    assert config["evaluation_replicate_grid"] == [5]
    assert config["expected_trial_count"] == 25


def test_pilot_uses_full_24x36_design_and_one_prefrozen_departure() -> None:
    config = load()
    assert config["design"]["participants"] == 24
    assert config["design"]["items"] == 36
    assert config["design"]["missingness_rate"] == 0
    assert config["fit_scale_multiplier"] == 1

    selector = config["departure_case_filter"]
    assert selector == {
        "anchor_id": ["CBD_ADD_INTERSECTION_ANCHOR_1"],
        "axis": ["STANDALONE_ACCURACY_MAIN_EFFECT"],
        "sign": [1],
        "requested_cbd_rms_distance": [0.25],
    }


def test_pilot_retains_all_three_null_calibrations() -> None:
    config = load()
    assert set(config["null_generators"]) == {
        "CBD_ANCHOR_1",
        "CBD_ANCHOR_2",
        "ADD_ANCHOR",
    }


def test_pilot_cannot_promote_any_scientific_or_human_gate() -> None:
    config = load()
    assert config["bootstrap"]["draw_grid_status"] == (
        "PILOT_ONLY_NOT_AUTHORITATIVE"
    )
    assert config["evaluation_replicate_grid_status"] == (
        "PILOT_ONLY_NOT_AUTHORITATIVE"
    )
    assert config["execution_boundary"] == {
        "authoritative_bootstrap_draws_frozen": False,
        "authoritative_evaluation_replicates_frozen": False,
        "authoritative_run_allowed": False,
        "authoritative_core_grid_frozen": False,
        "human_n_frozen": False,
        "participant_recruitment_allowed": False,
        "runtime_f1b_change_allowed": False,
    }
