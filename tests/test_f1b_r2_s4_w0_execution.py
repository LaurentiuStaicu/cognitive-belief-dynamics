from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from cognitive_epistemic_model.calibration import f1b_r2_s4_w0_execution as w0


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "model" / "benchmarks" / "f1b_r2_s4_w0_execution_v1.json"


def load_config() -> dict:
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def test_repository_w0_contract_is_frozen() -> None:
    config = load_config()
    w0.validate_w0_config(config)
    assert config["wave"]["wave_id"] == "W0"
    assert config["wave"]["scientific_run_count"] == 3750
    assert config["wave"]["method_row_count"] == 15000
    assert config["wave"]["imported_method_row_count"] == 3360
    assert config["wave"]["new_method_execution_count"] == 11640
    assert config["shards"]["shard_count"] == 250
    assert config["shards"]["max_parallel"] == 20


def test_import_membership_is_exact() -> None:
    assert w0.is_imported_prefix_row(
        {"identity_type":"DEPARTURE","evaluation_replicate":4}
    )
    assert not w0.is_imported_prefix_row(
        {"identity_type":"DEPARTURE","evaluation_replicate":5}
    )
    assert w0.is_imported_prefix_row(
        {"identity_type":"NULL","evaluation_replicate":19}
    )
    assert not w0.is_imported_prefix_row(
        {"identity_type":"NULL","evaluation_replicate":20}
    )


def test_method_row_identity_is_stable() -> None:
    assert w0.method_row_id("RUN", "POPULATION") == "RUN|METHOD=POPULATION"


def test_w0_rejects_method_change() -> None:
    config = deepcopy(load_config())
    config["retained_sources"]["method_binding_result"]["eligible_methods"].pop()
    with pytest.raises(ValueError, match="method order/set"):
        w0.validate_w0_config(config)


def test_w0_rejects_wave_expansion() -> None:
    config = deepcopy(load_config())
    config["wave"]["replicate_end"] = 25
    with pytest.raises(ValueError, match="replicate_end"):
        w0.validate_w0_config(config)


def test_w0_rejects_parallelism_change() -> None:
    config = deepcopy(load_config())
    config["shards"]["max_parallel"] = 21
    with pytest.raises(ValueError, match="max-parallel"):
        w0.validate_w0_config(config)


def test_w0_rejects_import_recomputation() -> None:
    config = deepcopy(load_config())
    config["execution"]["imported_rows_recomputed"] = True
    with pytest.raises(ValueError, match="cannot be recomputed"):
        w0.validate_w0_config(config)


def test_w0_rejects_scientific_interpretation() -> None:
    config = deepcopy(load_config())
    config["execution"]["scientific_interpretation_after_wave"] = True
    with pytest.raises(ValueError, match="scientific interpretation"):
        w0.validate_w0_config(config)


def test_w0_rejects_release_shortcut() -> None:
    config = deepcopy(load_config())
    config["release"]["release_blocker_closed"] = True
    with pytest.raises(ValueError, match="v0.2.0 blocker"):
        w0.validate_w0_config(config)


def test_w0_boundary_cannot_be_weakened() -> None:
    config = deepcopy(load_config())
    config["boundary"]["power_validated"] = True
    with pytest.raises(ValueError, match="boundary"):
        w0.validate_w0_config(config)
