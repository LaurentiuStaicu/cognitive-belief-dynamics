from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = (
    ROOT
    / "model"
    / "benchmarks"
    / "f1b_r2_bootstrap_calibration_screen_49_99_199x20.json"
)


def load() -> dict:
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def test_screen_uses_prefrozen_draw_grid_and_twenty_replicates() -> None:
    config = load()
    assert config["bootstrap"]["draw_grid"] == [49, 99, 199]
    assert config["evaluation_replicate_grid"] == [20]
    assert config["expected_trial_count"] == 300
    assert config["bootstrap"]["draw_grid_status"] == (
        "STAGED_SCREEN_NOT_AUTHORITATIVE"
    )
    assert config["evaluation_replicate_grid_status"] == (
        "STAGED_SCREEN_NOT_AUTHORITATIVE"
    )


def test_screen_keeps_same_pilot_identity_set() -> None:
    config = load()
    assert set(config["null_generators"]) == {
        "CBD_ANCHOR_1",
        "CBD_ANCHOR_2",
        "ADD_ANCHOR",
    }
    assert config["departure_case_filter"] == {
        "anchor_id": ["CBD_ADD_INTERSECTION_ANCHOR_1"],
        "axis": ["STANDALONE_ACCURACY_MAIN_EFFECT"],
        "sign": [1],
        "requested_cbd_rms_distance": [0.25],
    }


def test_stage_advancement_rule_is_frozen_before_execution() -> None:
    screen = load()["stage_advancement_screen"]
    assert screen["require_zero_fit_failures"] is True
    assert screen["require_zero_bootstrap_calibration_failures"] is True
    assert screen["max_null_rejections_out_of_20"] == 2
    assert screen["max_add_specificity_rejections_out_of_20"] == 2
    assert screen["min_cbd_departure_rejections_out_of_20"] == 16
    assert screen["applies_independently_by_bootstrap_draw_count"] is True
    assert screen["authoritative_draw_count_freeze_allowed"] is False


def test_screen_cannot_promote_human_or_runtime_gate() -> None:
    config = load()
    assert config["execution_boundary"] == {
        "authoritative_bootstrap_draws_frozen": False,
        "authoritative_evaluation_replicates_frozen": False,
        "authoritative_run_allowed": False,
        "authoritative_core_grid_frozen": False,
        "human_n_frozen": False,
        "participant_recruitment_allowed": False,
        "runtime_f1b_change_allowed": False,
    }
