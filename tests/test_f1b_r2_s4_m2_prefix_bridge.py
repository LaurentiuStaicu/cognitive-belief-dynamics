from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from cognitive_epistemic_model.calibration import f1b_r2_s4_m2_prefix_bridge as bridge


ROOT = Path(__file__).resolve().parents[1]
CONFIG = (
    ROOT
    / "model"
    / "benchmarks"
    / "f1b_r2_s4_m2_prefix_bridge_v1.json"
)


def load_config() -> dict:
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def test_repository_prefix_bridge_contract_is_frozen() -> None:
    config = load_config()
    bridge.validate_prefix_bridge_config(config)
    assert config["overlap"]["expected_scientific_run_count"] == 840
    assert config["overlap"]["expected_method_row_count"] == 3360
    assert config["overlap"]["expected_departure_scientific_runs"] == 720
    assert config["overlap"]["expected_null_scientific_runs"] == 120
    assert config["m2_source"]["eligible_methods"] == list(
        bridge.EXPECTED_METHODS
    )
    assert config["broad_consequence"]["total_scientific_runs"] == 15000
    assert config["broad_consequence"]["total_method_rows"] == 60000
    assert (
        config["broad_consequence"]["new_method_executions_if_bridge_passes"]
        == 56640
    )


def test_prefix_bridge_rejects_method_removal() -> None:
    config = deepcopy(load_config())
    config["m2_source"]["eligible_methods"].pop()
    with pytest.raises(ValueError, match="eligible-method"):
        bridge.validate_prefix_bridge_config(config)


def test_prefix_bridge_rejects_prefix_expansion() -> None:
    config = deepcopy(load_config())
    config["overlap"]["departure_replicate_indices"].append(5)
    with pytest.raises(ValueError, match="departure prefix replicate"):
        bridge.validate_prefix_bridge_config(config)


def test_prefix_bridge_rejects_status_reclassification() -> None:
    config = deepcopy(load_config())
    config["overlap"]["expected_status_counts"][
        "SEQUENTIAL_UNRESOLVED_AT_CAP"
    ] -= 1
    config["overlap"]["expected_status_counts"][
        "SEQUENTIAL_RESOLVED"
    ] += 1
    with pytest.raises(ValueError, match="status-count"):
        bridge.validate_prefix_bridge_config(config)


def test_prefix_bridge_rejects_denominator_shrinkage() -> None:
    config = deepcopy(load_config())
    config["broad_consequence"]["total_method_rows"] = 56640
    with pytest.raises(ValueError, match="broad method-row"):
        bridge.validate_prefix_bridge_config(config)


def test_prefix_bridge_rejects_drop_instead_of_recompute() -> None:
    config = deepcopy(load_config())
    config["import_rules"]["failed_bridge_row_recomputed_not_dropped"] = False
    with pytest.raises(ValueError, match="recomputed"):
        bridge.validate_prefix_bridge_config(config)


def test_prefix_bridge_boundary_cannot_be_weakened() -> None:
    config = deepcopy(load_config())
    config["boundary"]["method_selected"] = True
    with pytest.raises(ValueError, match="boundary"):
        bridge.validate_prefix_bridge_config(config)


def test_import_identity_digest_is_order_stable_when_sorted_by_caller() -> None:
    a = bridge.canonical_json_sha256(sorted(["b", "a"]))
    b = bridge.canonical_json_sha256(["a", "b"])
    assert a == b
