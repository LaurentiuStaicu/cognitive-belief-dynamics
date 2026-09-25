from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

from cognitive_epistemic_model.calibration.f1b_recovery_characterization import (
    FIT_FAILURE,
    _scale_random_effects,
    run_characterization,
)

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "model" / "benchmarks" / "f1b_recovery_characterization.json"


def load_config() -> dict:
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def tiny_config() -> dict:
    config = deepcopy(load_config())
    config["replicates_per_cell"] = 1
    config["separation_regimes"] = ["MODERATE"]
    config["missingness_rates"] = [0.0]
    config["hierarchical_scale_multipliers"] = [0.5, 1.0, 2.0]
    config["R1"]["participants"] = 12
    config["R1"]["items"] = 12
    config["R2"]["participants"] = 12
    config["R2"]["items"] = 18
    return config


def test_characterization_config_keeps_all_scientific_gates_closed() -> None:
    config = load_config()
    assert config["status"] == "NON_AUTHORITATIVE_CHARACTERIZATION_DESIGN"
    assert config["separation_regimes"] == ["WEAK", "MODERATE", "STRONG"]
    assert config["missingness_rates"] == [0.0, 0.15]
    assert config["hierarchical_scale_multipliers"] == [0.5, 1.0, 2.0]
    assert config["execution_boundary"] == {
        "authoritative_run_allowed": False,
        "authoritative_core_grid_frozen": False,
        "human_n_frozen": False,
        "participant_recruitment_allowed": False,
        "runtime_f1b_change_allowed": False,
    }


def test_scale_multipliers_change_assumed_fit_scales_not_generator_scales() -> None:
    generator = {
        "participant_intercept_sd": 0.2,
        "item_intercept_sd": 0.2,
        "participant_slope_sd": 0.1,
        "item_slope_sd": 0.1,
    }
    half = _scale_random_effects(generator, 0.5, r2=False)
    matched = _scale_random_effects(generator, 1.0, r2=False)
    double = _scale_random_effects(generator, 2.0, r2=False)

    assert half.participant_intercept_sd == 0.1
    assert matched.participant_intercept_sd == 0.2
    assert double.participant_intercept_sd == 0.4
    assert generator["participant_intercept_sd"] == 0.2


def test_tiny_characterization_reuses_common_design_and_reports_all_outcomes() -> None:
    result = run_characterization(tiny_config())

    assert result["status"] == "NON_AUTHORITATIVE_CHARACTERIZATION_RESULT"
    assert result["authoritative"] is False
    assert result["replicates_per_cell"] == 1

    rows = result["grid_results"]
    # 2 problems × 3 generators × (1 population + 3 hierarchical scales)
    assert len(rows) == 24
    for row in rows:
        assert set(row["selected"]).issuperset({"INCONCLUSIVE", FIT_FAILURE})
        total = (
            row["recovery_probability"]
            + row["wrong_probability"]
            + row["inconclusive_probability"]
            + row["fit_failure_probability"]
        )
        assert abs(total - 1.0) < 1e-12

    comparisons = result["comparisons"]
    # 2 problems × 3 generators × 3 hierarchical scales
    assert len(comparisons) == 18


def test_tiny_characterization_is_seed_reproducible() -> None:
    config = tiny_config()
    first = run_characterization(config)
    second = run_characterization(config)
    assert first == second
