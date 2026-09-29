from __future__ import annotations

from collections import Counter, defaultdict
import json
import hashlib
from typing import Any

from .f1b_r2_paired_method_m2_sequential_resolution import (
    EXPECTED_METHODS_M2,
    REFIT_FAILURE,
    UNRESOLVED_AT_CAP,
    stable_shard,
)
from .f1b_r2_s4_broad_executor import (
    EVIDENCE_ORIGIN_NEW,
    PREFIX_EXECUTION_FAILURE,
)


EVIDENCE_ORIGIN_IMPORTED = "RETAINED_M2_IMPORT"
SHARD_STATUS = "NON_AUTHORITATIVE_S4_W0_SHARD_COMPLETE"


def canonical_json_sha256(value: Any) -> str:
    payload = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def method_row_id(scientific_run_id: str, method_id: str) -> str:
    return f"{scientific_run_id}|METHOD={method_id}"


def is_imported_prefix_row(scientific_row: dict) -> bool:
    replicate = int(scientific_row["evaluation_replicate"])
    identity_type = str(scientific_row["identity_type"])
    if identity_type == "DEPARTURE":
        return replicate in range(5)
    if identity_type == "NULL":
        return replicate in range(20)
    raise ValueError("unsupported W0 identity type")


def normalize_imported_m2_row(row: dict) -> dict:
    status = str(row["status"])
    if status not in {
        "SEQUENTIAL_RESOLVED_AT_PREFIX",
        "SEQUENTIAL_RESOLVED",
        "SEQUENTIAL_UNRESOLVED_AT_CAP",
    }:
        raise ValueError("unsupported imported M2 terminal status")
    if bool(row["m1_prefix_exact"]) is not True:
        raise ValueError("imported M2 row lost prefix exactness")
    if int(row["new_refit_failure_count"]) != 0:
        raise ValueError("imported M2 row contains refit failure")
    if str(row["retained_m1_attempt_sequence_sha256"]) != str(
        row["regenerated_m1_attempt_sequence_sha256"]
    ):
        raise ValueError("imported M2 prefix digest changed")

    return {
        "scientific_run_id": str(row["scientific_run_id"]),
        "dataset_id": str(row["dataset_id"]),
        "dataset_sha256": str(row["dataset_sha256"]),
        "identity": str(row["identity"]),
        "identity_type": str(row["identity_type"]),
        "restriction": str(row["restriction"]),
        "role": str(row["role"]),
        "anchor_id": row["anchor_id"],
        "axis": row["axis"],
        "sign": row["sign"],
        "target_mean_bernoulli_kl": row["target_mean_bernoulli_kl"],
        "evaluation_replicate": int(row["evaluation_replicate"]),
        "missingness_rate": float(row["missingness_rate"]),
        "inference_method": str(row["inference_method"]),
        "evidence_origin": EVIDENCE_ORIGIN_IMPORTED,
        "bootstrap_base_seed": int(row["bootstrap_base_seed"]),
        "prefix_attempt_sequence_sha256": str(
            row["regenerated_m1_attempt_sequence_sha256"]
        ),
        "prefix_attempt_count": 199,
        "prefix_successful_attempt_count": 199,
        "prefix_refit_failure_count": 0,
        "prefix_execution_failure": False,
        "observed_statistic": float(row["observed_statistic"]),
        "prefix_sum_199": int(row["prefix_sum_199"]),
        "prefix_decision": row["prefix_decision"],
        "prefix_boundary_hit": row["prefix_boundary_hit"],
        "continued_beyond_199": bool(row["continued_beyond_199"]),
        "first_new_draw_index": row["first_new_draw_index"],
        "new_attempt_count": int(row["new_attempt_count"]),
        "new_successful_attempt_count": int(
            row["new_successful_attempt_count"]
        ),
        "new_refit_failure_count": int(row["new_refit_failure_count"]),
        "new_attempt_sequence_sha256": row["new_attempt_sequence_sha256"],
        "status": status,
        "decision": row["decision"],
        "boundary_hit": row["boundary_hit"],
        "terminal_n": int(row["terminal_n"]),
        "terminal_sum": int(row["terminal_sum"]),
        "failure_n": row["failure_n"],
    }


def validate_shard_scientific_rows(
    scientific_rows: list[dict],
    *,
    shard_index: int,
) -> None:
    if not 0 <= int(shard_index) < 250:
        raise ValueError("S4 W0 shard index outside 0..249")
    if not scientific_rows:
        raise ValueError("S4 W0 shard cannot be empty")

    ids = [str(row["scientific_run_id"]) for row in scientific_rows]
    if len(ids) != len(set(ids)):
        raise ValueError("S4 W0 shard scientific IDs are not unique")

    for row in scientific_rows:
        replicate = int(row["evaluation_replicate"])
        if not 0 <= replicate <= 24:
            raise ValueError("S4 W0 shard contains non-W0 replicate")
        if stable_shard(str(row["scientific_run_id"]), 250) != int(
            shard_index
        ):
            raise ValueError("S4 W0 shard assignment changed")


def build_shard_result(
    scientific_rows: list[dict],
    method_rows: list[dict],
    *,
    shard_index: int,
    expected_imported_scientific_run_count: int,
    expected_new_scientific_run_count: int,
) -> dict:
    validate_shard_scientific_rows(
        scientific_rows,
        shard_index=int(shard_index),
    )

    scientific_ids = sorted(
        str(row["scientific_run_id"]) for row in scientific_rows
    )
    expected_method_ids = sorted(
        method_row_id(run_id, method)
        for run_id in scientific_ids
        for method in EXPECTED_METHODS_M2
    )
    actual_method_ids = [
        method_row_id(
            str(row["scientific_run_id"]),
            str(row["inference_method"]),
        )
        for row in method_rows
    ]
    if len(actual_method_ids) != len(expected_method_ids):
        raise ValueError("S4 W0 shard method-row count changed")
    if len(set(actual_method_ids)) != len(actual_method_ids):
        raise ValueError("S4 W0 shard method-row IDs are not unique")
    if sorted(actual_method_ids) != expected_method_ids:
        raise ValueError("S4 W0 shard method coverage changed")

    by_run: dict[str, list[dict]] = defaultdict(list)
    for row in method_rows:
        by_run[str(row["scientific_run_id"])].append(row)
    if set(by_run) != set(scientific_ids):
        raise ValueError("S4 W0 shard scientific coverage changed")

    scientific_map = {
        str(row["scientific_run_id"]): row for row in scientific_rows
    }
    imported_scientific = 0
    new_scientific = 0
    imported_method_rows = 0
    new_method_rows = 0

    allowed_statuses = {
        "SEQUENTIAL_RESOLVED_AT_PREFIX",
        "SEQUENTIAL_RESOLVED",
        UNRESOLVED_AT_CAP,
        REFIT_FAILURE,
        PREFIX_EXECUTION_FAILURE,
    }
    status_counts: Counter[str] = Counter()
    decision_counts: Counter[str] = Counter()
    evidence_counts: Counter[str] = Counter()

    for run_id, rows in by_run.items():
        if {str(row["inference_method"]) for row in rows} != set(
            EXPECTED_METHODS_M2
        ):
            raise ValueError("S4 W0 shard method set changed")
        if len({str(row["dataset_sha256"]) for row in rows}) != 1:
            raise ValueError("S4 W0 paired methods saw different datasets")

        imported = is_imported_prefix_row(scientific_map[run_id])
        expected_origin = (
            EVIDENCE_ORIGIN_IMPORTED if imported else EVIDENCE_ORIGIN_NEW
        )
        if any(str(row["evidence_origin"]) != expected_origin for row in rows):
            raise ValueError("S4 W0 shard evidence origin changed")

        if imported:
            imported_scientific += 1
            imported_method_rows += 4
        else:
            new_scientific += 1
            new_method_rows += 4

        for row in rows:
            status = str(row["status"])
            if status not in allowed_statuses:
                raise ValueError("S4 W0 shard unsupported terminal status")
            status_counts[status] += 1
            evidence_counts[str(row["evidence_origin"])] += 1
            if row["decision"] is not None:
                decision_counts[str(row["decision"])] += 1
            if status == UNRESOLVED_AT_CAP:
                if row["decision"] is not None:
                    raise ValueError("S4 W0 unresolved row has decision")
                if int(row["terminal_n"]) != 10000:
                    raise ValueError("S4 W0 unresolved row did not reach cap")
            if status == REFIT_FAILURE and row["decision"] is not None:
                raise ValueError("S4 W0 refit failure has decision")

    if imported_scientific != int(expected_imported_scientific_run_count):
        raise ValueError("S4 W0 shard imported scientific count changed")
    if new_scientific != int(expected_new_scientific_run_count):
        raise ValueError("S4 W0 shard new scientific count changed")

    return {
        "status": SHARD_STATUS,
        "authoritative": False,
        "wave_id": "W0",
        "shard_index": int(shard_index),
        "scientific_run_count": len(scientific_rows),
        "method_row_count": len(method_rows),
        "imported_scientific_run_count": imported_scientific,
        "new_scientific_run_count": new_scientific,
        "imported_method_row_count": imported_method_rows,
        "new_method_execution_count": new_method_rows,
        "scientific_run_ids_sha256": canonical_json_sha256(scientific_ids),
        "method_row_ids_sha256": canonical_json_sha256(
            sorted(actual_method_ids)
        ),
        "status_counts": dict(sorted(status_counts.items())),
        "decision_counts": dict(sorted(decision_counts.items())),
        "evidence_origin_counts": dict(sorted(evidence_counts.items())),
        "rows": method_rows,
        "scientific_interpretation_authorized": False,
        "method_selected": False,
        "power_validated": False,
    }
