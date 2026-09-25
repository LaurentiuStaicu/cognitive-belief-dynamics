from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

from cognitive_epistemic_model.calibration.f1b_r1_high_replicate import (
    run_r1_high_replicate_characterization,
    wilson_interval,
)

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "model" / "benchmarks" / "f1b_r1_high_replicate_characterization.json"


def load_config() -> dict:
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def tiny_config() -> dict:
    config = deepcopy(load_config())
    config["replicates_per_cell"] = 2
    config["separation_regimes"] = ["STRONG"]
    config["missingness_rates"] = [0.0]
    config["hierarchical_scale_multipliers"] = [0.5, 1.0, 2.0]
    config["R1"]["participants"] = 12
    config["R1"]["items"] = 12
    return config


def test_wilson_interval_is_bounded_and_contains_point_estimate() -> None:
    low, high = wilson_interval(160, 200)
    assert 0.0 <= low <= 0.8 <= high <= 1.0

    zero_low, zero_high = wilson_interval(0, 200)
    assert zero_low == 0.0
    assert 0.0 < zero_high < 0.05


def test_config_freezes_high_replicate_design_before_run() -> None:
    config = load_config()

    assert config["replicates_per_cell"] == 200
    assert config["separation_regimes"] == ["WEAK", "MODERATE", "STRONG"]
    assert config["missingness_rates"] == [0.0, 0.15]
    assert config["hierarchical_scale_multipliers"] == [0.5, 1.0, 2.0]
    assert config["design_eligibility"] == {
        "scope": "STRONG_CELLS_ONLY",
        "strong_point_recovery_minimum": 0.8,
        "strong_recovery_wilson_lower_minimum": 0.7,
        "wrong_probability_maximum": 0.05,
        "fit_failure_probability_maximum": 0.01,
        "status": "PROSPECTIVE_DESIGN_ELIGIBILITY_NOT_SCIENTIFIC_PROMOTION",
    }
    assert config["execution_boundary"]["human_n_frozen"] is False
    assert config["execution_boundary"]["participant_recruitment_allowed"] is False
    assert config["execution_boundary"]["runtime_f1b_change_allowed"] is False


def test_tiny_run_is_reproducible_and_reports_uncertainty_and_eligibility() -> None:
    config = tiny_config()
    first = run_r1_high_replicate_characterization(config)
    second = run_r1_high_replicate_characterization(config)

    assert first == second
    assert first["status"] == "NON_AUTHORITATIVE_R1_HIGH_REPLICATE_RESULT"
    assert first["authoritative"] is False

    # 3 generators × (population + three hierarchical scales)
    assert len(first["grid_results"]) == 12
    assert len(first["design_eligibility"]) == 4

    for row in first["grid_results"]:
        for key in ("recovery", "wrong", "inconclusive", "fit_failure"):
            metric = row[key]
            assert 0.0 <= metric["wilson_95"][0] <= metric["probability"]
            assert metric["probability"] <= metric["wilson_95"][1] <= 1.0
