from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from cognitive_epistemic_model.calibration import (
    f1b_r2_s4_broad_execution_topology as topology,
)
from cognitive_epistemic_model.calibration.f1b_r2_paired_method_m2_sequential_resolution import (
    stable_shard,
)


ROOT = Path(__file__).resolve().parents[1]
CONFIG = (
    ROOT
    / "model"
    / "benchmarks"
    / "f1b_r2_s4_broad_execution_topology_v1.json"
)


def load_config() -> dict:
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def test_repository_topology_contract_is_frozen() -> None:
    config = load_config()
    topology.validate_topology_config(config)
    assert config["wave_partition"]["wave_count"] == 4
    assert config["shard_partition"]["shard_count_per_wave"] == 250
    assert config["final_combine"]["total_scientific_run_count"] == 15000
    assert config["final_combine"]["total_method_row_count"] == 60000
    assert (
        config["final_combine"]["newly_executed_method_row_count"]
        == 56640
    )


@pytest.mark.parametrize(
    ("replicate", "wave_id"),
    [
        (0, "W0"),
        (24, "W0"),
        (25, "W1"),
        (49, "W1"),
        (50, "W2"),
        (74, "W2"),
        (75, "W3"),
        (99, "W3"),
    ],
)
def test_wave_boundaries_are_exact(replicate: int, wave_id: str) -> None:
    assert topology.wave_for_replicate(replicate) == wave_id


def test_wave_mapping_rejects_out_of_range_replicate() -> None:
    with pytest.raises(ValueError, match="outside"):
        topology.wave_for_replicate(100)


def test_topology_reuses_m2_stable_shard_exactly() -> None:
    run_id = (
        "SYNTHETIC|REPLICATE=42|RESTRICTION=ADD_RESTRICTION"
        "|MISSINGNESS=0.15"
    )
    assert stable_shard(run_id, 250) == 151


def test_prefix_membership_rules_are_frozen() -> None:
    assert topology.is_imported_prefix_row(
        {"identity_type": "DEPARTURE", "evaluation_replicate": 4}
    )
    assert not topology.is_imported_prefix_row(
        {"identity_type": "DEPARTURE", "evaluation_replicate": 5}
    )
    assert topology.is_imported_prefix_row(
        {"identity_type": "NULL", "evaluation_replicate": 19}
    )
    assert not topology.is_imported_prefix_row(
        {"identity_type": "NULL", "evaluation_replicate": 20}
    )


def test_topology_rejects_wave_boundary_change() -> None:
    config = deepcopy(load_config())
    config["wave_partition"]["waves"][0]["replicate_end"] = 23
    with pytest.raises(ValueError, match="wave definition"):
        topology.validate_topology_config(config)


def test_topology_rejects_shard_count_change() -> None:
    config = deepcopy(load_config())
    config["shard_partition"]["shard_count_per_wave"] = 249
    with pytest.raises(ValueError, match="shard count"):
        topology.validate_topology_config(config)


def test_topology_rejects_denominator_shrinkage() -> None:
    config = deepcopy(load_config())
    config["final_combine"]["total_method_row_count"] = 56640
    with pytest.raises(ValueError, match="method-row count"):
        topology.validate_topology_config(config)


def test_topology_rejects_early_interpretation() -> None:
    config = deepcopy(load_config())
    config["execution_policy"]["early_scientific_interpretation_forbidden"] = False
    with pytest.raises(ValueError, match="early interpretation"):
        topology.validate_topology_config(config)


def test_topology_cannot_close_release_blocker() -> None:
    config = deepcopy(load_config())
    config["release"]["release_blocker_closed"] = True
    with pytest.raises(ValueError, match="v0.2.0 blocker"):
        topology.validate_topology_config(config)


def test_topology_boundary_cannot_be_weakened() -> None:
    config = deepcopy(load_config())
    config["boundary"]["power_validated"] = True
    with pytest.raises(ValueError, match="boundary"):
        topology.validate_topology_config(config)
