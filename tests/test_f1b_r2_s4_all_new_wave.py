from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from cognitive_epistemic_model.calibration import f1b_r2_s4_all_new_wave as wave


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "model" / "benchmarks" / "f1b_r2_s4_w1_execution_v1.json"


def load_config() -> dict:
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def test_repository_w1_contract_is_frozen() -> None:
    config = load_config()
    wave.validate_all_new_wave_config(config)
    assert config["wave"]["wave_id"] == "W1"
    assert config["wave"]["replicate_start"] == 25
    assert config["wave"]["replicate_end"] == 49
    assert config["wave"]["scientific_run_count"] == 3750
    assert config["wave"]["method_row_count"] == 15000
    assert config["wave"]["imported_method_row_count"] == 0
    assert config["wave"]["new_method_execution_count"] == 15000
    assert config["wave"]["shard_plan_sha256"] == (
        "36d294a165ec1e8a8baffac70516ce7fceab149998079b534998503f3f578175"
    )
    assert config["preflight"]["shard_index"] == 11


def test_w1_rejects_w0_membership() -> None:
    config = deepcopy(load_config())
    config["wave"]["wave_id"] = "W0"
    with pytest.raises(ValueError, match="unsupported"):
        wave.validate_all_new_wave_config(config)


def test_w1_rejects_premature_w2_relabel() -> None:
    config = deepcopy(load_config())
    config["wave"].update(
        {
            "wave_id": "W2",
            "predecessor_wave_id": "W1",
            "replicate_start": 50,
            "replicate_end": 74,
            "scientific_run_ids_sha256": (
                "a24dea39afdb03b91784248755d9ddad94466bbab8391044308eeeb8c9eff617"
            ),
            "method_row_ids_sha256": (
                "a338bd644ee62a474cf417aa0396a0ff2df4a310618e63ffb644c8f5f3cc8ba2"
            ),
            "shard_plan_sha256": (
                "399b4feecc51731f4691ca7168eb61625834cc1dc74e2fb66d3f6fe23ffe2475"
            ),
        }
    )
    config["shards"]["minimum_scientific_runs_per_shard"] = 6
    config["retained_sources"]["predecessor_result"]["wave_id"] = "W1"
    with pytest.raises(ValueError, match="predecessor status"):
        wave.validate_all_new_wave_config(config)


def test_w1_rejects_imported_rows() -> None:
    config = deepcopy(load_config())
    config["wave"]["imported_method_row_count"] = 4
    with pytest.raises(ValueError, match="cannot import"):
        wave.validate_all_new_wave_config(config)


def test_w1_rejects_method_change() -> None:
    config = deepcopy(load_config())
    config["methods"].pop()
    with pytest.raises(ValueError, match="method order/set"):
        wave.validate_all_new_wave_config(config)


def test_w1_rejects_parallelism_change() -> None:
    config = deepcopy(load_config())
    config["shards"]["max_parallel"] = 21
    with pytest.raises(ValueError, match="max-parallel"):
        wave.validate_all_new_wave_config(config)


def test_w1_rejects_early_interpretation() -> None:
    config = deepcopy(load_config())
    config["execution"]["scientific_interpretation_after_wave"] = True
    with pytest.raises(ValueError, match="interpretation"):
        wave.validate_all_new_wave_config(config)


def test_w1_rejects_preflight_shortcut() -> None:
    config = deepcopy(load_config())
    config["authorization"]["preflight_retained"] = True
    with pytest.raises(ValueError, match="authorization must match"):
        wave.validate_all_new_wave_config(config)


def test_w1_rejects_full_wave_before_preflight_retention() -> None:
    config = deepcopy(load_config())
    config["authorization"]["full_wave_execution_authorized"] = True
    with pytest.raises(ValueError, match="authorization must match"):
        wave.validate_all_new_wave_config(config)


def test_w1_boundary_cannot_be_weakened() -> None:
    config = deepcopy(load_config())
    config["boundary"]["power_validated"] = True
    with pytest.raises(ValueError, match="boundary"):
        wave.validate_all_new_wave_config(config)
