from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from cognitive_epistemic_model.calibration import (
    f1b_r2_s4_all_new_wave_shard as shard,
)
from cognitive_epistemic_model.calibration.f1b_r2_paired_method_m2_sequential_resolution import (
    EXPECTED_METHODS_M2,
    stable_shard,
)
from cognitive_epistemic_model.calibration.f1b_r2_s4_broad_executor import (
    EVIDENCE_ORIGIN_NEW,
)


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "model" / "benchmarks" / "f1b_r2_s4_w1_execution_v1.json"


def load_config() -> dict:
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def scientific_row(run_id: str, *, replicate: int = 25) -> dict:
    return {
        "scientific_run_id": run_id,
        "evaluation_replicate": replicate,
    }


def broad_method_row(run_id: str, method: str, *, origin: str) -> dict:
    return {
        "scientific_run_id": run_id,
        "dataset_sha256": "a" * 64,
        "role": "ADD_DEPARTURE_DIAGNOSTIC",
        "missingness_rate": 0.0,
        "inference_method": method,
        "evidence_origin": origin,
        "status": "SEQUENTIAL_RESOLVED_AT_PREFIX",
        "decision": "REJECT_P_LE_ALPHA",
        "terminal_n": 199,
    }


def test_w1_shard_result_requires_all_four_methods() -> None:
    config = load_config()
    run_id = "W1|TEST|REPLICATE=25"
    index = stable_shard(run_id, 250)
    rows = [
        broad_method_row(run_id, method, origin=EVIDENCE_ORIGIN_NEW)
        for method in EXPECTED_METHODS_M2[:-1]
    ]
    with pytest.raises(ValueError, match="method-row count"):
        shard.build_all_new_shard_result(
            [scientific_row(run_id)],
            rows,
            shard_index=index,
            expected_scientific_run_count=1,
            config=config,
        )


def test_w1_shard_result_accepts_all_new_row() -> None:
    config = load_config()
    run_id = "W1|TEST|REPLICATE=25"
    index = stable_shard(run_id, 250)
    rows = [
        broad_method_row(run_id, method, origin=EVIDENCE_ORIGIN_NEW)
        for method in EXPECTED_METHODS_M2
    ]
    result = shard.build_all_new_shard_result(
        [scientific_row(run_id)],
        rows,
        shard_index=index,
        expected_scientific_run_count=1,
        config=config,
    )
    assert result["wave_id"] == "W1"
    assert result["imported_method_row_count"] == 0
    assert result["new_method_execution_count"] == 4
    assert result["scientific_interpretation_authorized"] is False


def test_w1_shard_rejects_imported_origin() -> None:
    config = load_config()
    run_id = "W1|TEST|REPLICATE=25"
    index = stable_shard(run_id, 250)
    rows = [
        broad_method_row(run_id, method, origin="RETAINED_M2_IMPORT")
        for method in EXPECTED_METHODS_M2
    ]
    with pytest.raises(ValueError, match="imported evidence"):
        shard.build_all_new_shard_result(
            [scientific_row(run_id)],
            rows,
            shard_index=index,
            expected_scientific_run_count=1,
            config=config,
        )


def test_w1_shard_rejects_dataset_pairing_change() -> None:
    config = load_config()
    run_id = "W1|TEST|REPLICATE=25"
    index = stable_shard(run_id, 250)
    rows = [
        broad_method_row(run_id, method, origin=EVIDENCE_ORIGIN_NEW)
        for method in EXPECTED_METHODS_M2
    ]
    rows[-1] = deepcopy(rows[-1])
    rows[-1]["dataset_sha256"] = "b" * 64
    with pytest.raises(ValueError, match="different datasets"):
        shard.build_all_new_shard_result(
            [scientific_row(run_id)],
            rows,
            shard_index=index,
            expected_scientific_run_count=1,
            config=config,
        )


def test_w1_shard_rejects_wrong_replicate() -> None:
    config = load_config()
    run_id = "W1|TEST|REPLICATE=24"
    index = stable_shard(run_id, 250)
    rows = [
        broad_method_row(run_id, method, origin=EVIDENCE_ORIGIN_NEW)
        for method in EXPECTED_METHODS_M2
    ]
    with pytest.raises(ValueError, match="wrong replicate"):
        shard.build_all_new_shard_result(
            [scientific_row(run_id, replicate=24)],
            rows,
            shard_index=index,
            expected_scientific_run_count=1,
            config=config,
        )
