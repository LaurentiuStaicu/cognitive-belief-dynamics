from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from cognitive_epistemic_model.calibration import f1b_r2_s4_method_binding as binding


ROOT = Path(__file__).resolve().parents[1]
CONFIG = (
    ROOT
    / "model"
    / "benchmarks"
    / "f1b_r2_s4_method_binding_v1.json"
)
M2_RESULT = (
    ROOT
    / "model"
    / "results"
    / "f1b_r2_paired_method_m2_sequential_resolution_2026-09-28.json"
)
S4_RESULT = (
    ROOT
    / "model"
    / "results"
    / "f1b_r2_s4_broad_scientific_matrix_2026-09-28.json"
)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_repository_binding_contract_is_frozen() -> None:
    config = load(CONFIG)
    binding.validate_s4_method_binding_config(config)
    assert tuple(config["bound_execution"]["method_order"]) == binding.EXPECTED_METHODS
    assert config["bound_execution"]["scientific_run_count"] == 15000
    assert config["bound_execution"]["method_execution_count"] == 60000
    assert config["retained_s4_matrix"]["replicates_per_stratum"] == 100
    assert (
        config["retained_s4_matrix"]["maximum_worst_case_component_mcse"]
        == 0.05
    )


def test_retained_m2_and_s4_results_satisfy_binding() -> None:
    config = load(CONFIG)
    m2 = load(M2_RESULT)
    s4 = load(S4_RESULT)
    binding.validate_retained_results(m2, s4, config)
    manifest = binding.build_s4_bound_execution_manifest(m2, s4, config)
    assert manifest["eligible_methods"] == list(binding.EXPECTED_METHODS)
    assert manifest["method_count"] == 4
    assert manifest["scientific_run_count"] == 15000
    assert manifest["method_execution_count"] == 60000
    assert manifest["method_selected"] is False
    assert manifest["broad_characterization_authorized"] is True
    assert manifest["power_validated"] is False
    assert manifest["release_0_2_0_blocker_closed"] is False


def test_binding_rejects_method_removal() -> None:
    config = deepcopy(load(CONFIG))
    config["bound_execution"]["method_order"].pop()
    with pytest.raises(ValueError, match="method order/set"):
        binding.validate_s4_method_binding_config(config)


def test_binding_rejects_method_reordering() -> None:
    config = deepcopy(load(CONFIG))
    config["bound_execution"]["method_order"][0:2] = reversed(
        config["bound_execution"]["method_order"][0:2]
    )
    with pytest.raises(ValueError, match="method order/set"):
        binding.validate_s4_method_binding_config(config)


def test_binding_rejects_matrix_shrinkage() -> None:
    config = deepcopy(load(CONFIG))
    config["bound_execution"]["scientific_run_count"] = 14999
    with pytest.raises(ValueError, match="scientific-run count"):
        binding.validate_s4_method_binding_config(config)


def test_binding_rejects_replacement_of_failed_method_run_pairs() -> None:
    config = deepcopy(load(CONFIG))
    config["bound_execution"]["failed_method_run_pairs_replaced"] = True
    with pytest.raises(ValueError, match="cannot be replaced"):
        binding.validate_s4_method_binding_config(config)


def test_binding_rejects_posthoc_method_selection() -> None:
    config = deepcopy(load(CONFIG))
    config["interpretation"]["method_selection_authorized"] = True
    with pytest.raises(ValueError, match="cannot select"):
        binding.validate_s4_method_binding_config(config)


def test_binding_rejects_release_blocker_shortcut() -> None:
    config = deepcopy(load(CONFIG))
    config["interpretation"]["release_0_2_0_blocker_closed"] = True
    with pytest.raises(ValueError, match="v0.2.0 blocker"):
        binding.validate_s4_method_binding_config(config)


def test_binding_boundary_cannot_be_weakened() -> None:
    config = deepcopy(load(CONFIG))
    config["boundary"]["power_validated"] = True
    with pytest.raises(ValueError, match="boundary"):
        binding.validate_s4_method_binding_config(config)
