from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

from cognitive_epistemic_model.calibration.f1b_r1_design_size_search import (
    run_r1_design_size_search,
)

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "model" / "benchmarks" / "f1b_r1_design_size_search.json"


def load_config() -> dict:
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def tiny_config() -> dict:
    config = deepcopy(load_config())
    config["replicates_per_cell"] = 1
    config["participant_counts"] = [12, 24]
    config["item_counts"] = [12, 24]
    config["missingness_rates"] = [0.0]
    config["hierarchical_scale_multipliers"] = [0.5, 1.0]
    return config


def test_design_size_config_freezes_axes_and_gates() -> None:
    config = load_config()
    assert config["participant_counts"] == [24, 48, 96]
    assert config["item_counts"] == [24, 48, 96]
    assert config["replicates_per_cell"] == 200
    assert config["separation_regimes"] == ["STRONG"]
    assert config["missingness_rates"] == [0.0, 0.15]
    assert config["hierarchical_scale_multipliers"] == [0.5, 1.0, 2.0]
    assert config["design_eligibility"] == {
        "scope": "ALL_STRONG_GENERATOR_X_MISSINGNESS_CELLS",
        "strong_point_recovery_minimum": 0.8,
        "strong_recovery_wilson_lower_minimum": 0.7,
        "wrong_probability_maximum": 0.05,
        "fit_failure_probability_maximum": 0.01,
        "status": "PROSPECTIVE_DESIGN_ELIGIBILITY_NOT_SCIENTIFIC_PROMOTION",
    }
    assert config["execution_boundary"]["human_n_frozen"] is False
    assert config["execution_boundary"]["participant_recruitment_allowed"] is False


def test_tiny_search_is_reproducible_and_reports_design_eligibility() -> None:
    config = tiny_config()
    first = run_r1_design_size_search(config)
    second = run_r1_design_size_search(config)
    assert first == second
    assert first["status"] == "NON_AUTHORITATIVE_R1_DESIGN_SIZE_SEARCH_RESULT"
    assert first["authoritative"] is False

    # 2 participant counts × 2 item counts × 3 generators ×
    # 1 missingness × (population + 2 hierarchical variants)
    assert len(first["grid_results"]) == 36

    # 2 × 2 size cells × 3 inference variants
    assert len(first["design_eligibility"]) == 12

    for row in first["grid_results"]:
        total = (
            row["recovery"]["probability"]
            + row["wrong"]["probability"]
            + row["inconclusive"]["probability"]
            + row["fit_failure"]["probability"]
        )
        assert abs(total - 1.0) < 1e-12


def test_item_counts_must_match_frozen_condition_structure() -> None:
    config = tiny_config()
    config["item_counts"] = [18]
    try:
        run_r1_design_size_search(config)
    except ValueError as exc:
        assert "multiples of the 12 frozen R1 condition cells" in str(exc)
    else:
        raise AssertionError("invalid item grid should be rejected")
