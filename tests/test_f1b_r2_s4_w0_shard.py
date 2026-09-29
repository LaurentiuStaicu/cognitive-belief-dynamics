from __future__ import annotations

from copy import deepcopy

import pytest

from cognitive_epistemic_model.calibration import f1b_r2_s4_w0_shard as shard
from cognitive_epistemic_model.calibration.f1b_r2_paired_method_m2_sequential_resolution import (
    EXPECTED_METHODS_M2,
    stable_shard,
)


def scientific_row(run_id: str, *, replicate: int, identity_type: str) -> dict:
    return {
        "scientific_run_id": run_id,
        "dataset_id": run_id.split("|RESTRICTION=")[0],
        "identity": "X",
        "identity_type": identity_type,
        "restriction": "ADD_RESTRICTION",
        "role": "ADD_DEPARTURE_DIAGNOSTIC" if identity_type == "DEPARTURE" else "ADD_NULL_FALSE_REJECTION",
        "anchor_id": None,
        "axis": "A" if identity_type == "DEPARTURE" else None,
        "sign": 1 if identity_type == "DEPARTURE" else None,
        "target_mean_bernoulli_kl": 0.002 if identity_type == "DEPARTURE" else None,
        "evaluation_replicate": replicate,
        "missingness": 0.0,
    }


def broad_method_row(run_id: str, method: str, *, origin: str) -> dict:
    return {
        "scientific_run_id": run_id,
        "dataset_id": run_id.split("|RESTRICTION=")[0],
        "dataset_sha256": "a" * 64,
        "identity": "X",
        "identity_type": "DEPARTURE",
        "restriction": "ADD_RESTRICTION",
        "role": "ADD_DEPARTURE_DIAGNOSTIC",
        "anchor_id": None,
        "axis": "A",
        "sign": 1,
        "target_mean_bernoulli_kl": 0.002,
        "evaluation_replicate": 5,
        "missingness_rate": 0.0,
        "inference_method": method,
        "evidence_origin": origin,
        "bootstrap_base_seed": 1,
        "prefix_attempt_sequence_sha256": "b" * 64,
        "prefix_attempt_count": 199,
        "prefix_successful_attempt_count": 199,
        "prefix_refit_failure_count": 0,
        "prefix_execution_failure": False,
        "observed_statistic": 1.0,
        "prefix_sum_199": 10,
        "prefix_decision": "REJECT_P_LE_ALPHA",
        "prefix_boundary_hit": "LOWER",
        "continued_beyond_199": False,
        "first_new_draw_index": None,
        "new_attempt_count": 0,
        "new_successful_attempt_count": 0,
        "new_refit_failure_count": 0,
        "new_attempt_sequence_sha256": None,
        "status": "SEQUENTIAL_RESOLVED_AT_PREFIX",
        "decision": "REJECT_P_LE_ALPHA",
        "boundary_hit": "LOWER",
        "terminal_n": 199,
        "terminal_sum": 10,
        "failure_n": None,
    }


def imported_m2_row() -> dict:
    return {
        "scientific_run_id": "DATA|RESTRICTION=ADD_RESTRICTION|MISSINGNESS=0.00",
        "dataset_id": "DATA",
        "dataset_sha256": "a" * 64,
        "identity": "X",
        "identity_type": "DEPARTURE",
        "restriction": "ADD_RESTRICTION",
        "role": "ADD_DEPARTURE_DIAGNOSTIC",
        "anchor_id": None,
        "axis": "A",
        "sign": 1,
        "target_mean_bernoulli_kl": 0.002,
        "evaluation_replicate": 4,
        "missingness_rate": 0.0,
        "inference_method": "POPULATION",
        "bootstrap_base_seed": 123,
        "observed_statistic": 1.0,
        "prefix_sum_199": 10,
        "prefix_decision": "REJECT_P_LE_ALPHA",
        "prefix_boundary_hit": "LOWER",
        "continued_beyond_199": False,
        "first_new_draw_index": None,
        "new_attempt_count": 0,
        "new_successful_attempt_count": 0,
        "new_refit_failure_count": 0,
        "new_attempt_sequence_sha256": None,
        "status": "SEQUENTIAL_RESOLVED_AT_PREFIX",
        "decision": "REJECT_P_LE_ALPHA",
        "boundary_hit": "LOWER",
        "terminal_n": 199,
        "terminal_sum": 10,
        "failure_n": None,
        "m1_prefix_exact": True,
        "retained_m1_attempt_sequence_sha256": "b" * 64,
        "regenerated_m1_attempt_sequence_sha256": "b" * 64,
    }


def test_normalize_imported_m2_row_preserves_terminal_evidence() -> None:
    row = shard.normalize_imported_m2_row(imported_m2_row())
    assert row["evidence_origin"] == shard.EVIDENCE_ORIGIN_IMPORTED
    assert row["prefix_attempt_sequence_sha256"] == "b" * 64
    assert row["prefix_attempt_count"] == 199
    assert row["status"] == "SEQUENTIAL_RESOLVED_AT_PREFIX"
    assert row["terminal_n"] == 199


def test_normalize_import_rejects_prefix_mismatch() -> None:
    row = imported_m2_row()
    row["regenerated_m1_attempt_sequence_sha256"] = "c" * 64
    with pytest.raises(ValueError, match="prefix digest"):
        shard.normalize_imported_m2_row(row)


def test_shard_result_requires_all_four_methods() -> None:
    run_id = "NEW|RESTRICTION=ADD_RESTRICTION|MISSINGNESS=0.00"
    srow = scientific_row(run_id, replicate=5, identity_type="DEPARTURE")
    index = stable_shard(run_id, 250)
    rows = [
        broad_method_row(run_id, method, origin=shard.EVIDENCE_ORIGIN_NEW)
        for method in EXPECTED_METHODS_M2[:-1]
    ]
    with pytest.raises(ValueError, match="method-row count"):
        shard.build_shard_result(
            [srow],
            rows,
            shard_index=index,
            expected_imported_scientific_run_count=0,
            expected_new_scientific_run_count=1,
        )


def test_shard_result_validates_new_row() -> None:
    run_id = "NEW|RESTRICTION=ADD_RESTRICTION|MISSINGNESS=0.00"
    srow = scientific_row(run_id, replicate=5, identity_type="DEPARTURE")
    index = stable_shard(run_id, 250)
    rows = [
        broad_method_row(run_id, method, origin=shard.EVIDENCE_ORIGIN_NEW)
        for method in EXPECTED_METHODS_M2
    ]
    result = shard.build_shard_result(
        [srow],
        rows,
        shard_index=index,
        expected_imported_scientific_run_count=0,
        expected_new_scientific_run_count=1,
    )
    assert result["scientific_run_count"] == 1
    assert result["method_row_count"] == 4
    assert result["new_method_execution_count"] == 4
    assert result["scientific_interpretation_authorized"] is False


def test_shard_result_rejects_wrong_evidence_origin() -> None:
    run_id = "NEW|RESTRICTION=ADD_RESTRICTION|MISSINGNESS=0.00"
    srow = scientific_row(run_id, replicate=5, identity_type="DEPARTURE")
    index = stable_shard(run_id, 250)
    rows = [
        broad_method_row(run_id, method, origin=shard.EVIDENCE_ORIGIN_IMPORTED)
        for method in EXPECTED_METHODS_M2
    ]
    with pytest.raises(ValueError, match="evidence origin"):
        shard.build_shard_result(
            [srow],
            rows,
            shard_index=index,
            expected_imported_scientific_run_count=0,
            expected_new_scientific_run_count=1,
        )


def test_shard_result_rejects_dataset_pairing_change() -> None:
    run_id = "NEW|RESTRICTION=ADD_RESTRICTION|MISSINGNESS=0.00"
    srow = scientific_row(run_id, replicate=5, identity_type="DEPARTURE")
    index = stable_shard(run_id, 250)
    rows = [
        broad_method_row(run_id, method, origin=shard.EVIDENCE_ORIGIN_NEW)
        for method in EXPECTED_METHODS_M2
    ]
    rows[-1] = deepcopy(rows[-1])
    rows[-1]["dataset_sha256"] = "c" * 64
    with pytest.raises(ValueError, match="different datasets"):
        shard.build_shard_result(
            [srow],
            rows,
            shard_index=index,
            expected_imported_scientific_run_count=0,
            expected_new_scientific_run_count=1,
        )
