from __future__ import annotations

from collections import Counter, defaultdict
import hashlib
import json
from typing import Any

from .f1b_r2_paired_method_m2_sequential_resolution import (
    EXPECTED_METHODS_M2,
    REFIT_FAILURE,
    UNRESOLVED_AT_CAP,
    stable_shard,
)
from .f1b_r2_s4_all_new_wave import (
    canonical_json_sha256,
    method_row_id,
    shard_status,
    validate_all_new_wave_config,
)
from .f1b_r2_s4_broad_executor import (
    EVIDENCE_ORIGIN_NEW,
    PREFIX_EXECUTION_FAILURE,
)


def validate_all_new_scientific_rows(
    scientific_rows: list[dict],
    *,
    shard_index: int,
    config: dict,
) -> None:
    validate_all_new_wave_config(config)
    if not 0 <= int(shard_index) < 250:
        raise ValueError("S4 all-new-wave shard index outside 0..249")
    if not scientific_rows:
        raise ValueError("S4 all-new-wave shard cannot be empty")

    ids = [str(row["scientific_run_id"]) for row in scientific_rows]
    if len(ids) != len(set(ids)):
        raise ValueError("S4 all-new-wave scientific IDs are not unique")

    start = int(config["wave"]["replicate_start"])
    end = int(config["wave"]["replicate_end"])
    for row in scientific_rows:
        replicate = int(row["evaluation_replicate"])
        if not start <= replicate <= end:
            raise ValueError("S4 all-new-wave shard contains wrong replicate")
        if stable_shard(str(row["scientific_run_id"]), 250) != int(
            shard_index
        ):
            raise ValueError("S4 all-new-wave shard assignment changed")


def build_all_new_shard_result(
    scientific_rows: list[dict],
    method_rows: list[dict],
    *,
    shard_index: int,
    expected_scientific_run_count: int,
    config: dict,
) -> dict:
    validate_all_new_scientific_rows(
        scientific_rows,
        shard_index=int(shard_index),
        config=config,
    )

    wave_id = str(config["wave"]["wave_id"])
    scientific_ids = sorted(
        str(row["scientific_run_id"]) for row in scientific_rows
    )
    if len(scientific_ids) != int(expected_scientific_run_count):
        raise ValueError("S4 all-new-wave shard scientific count changed")

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
        raise ValueError("S4 all-new-wave shard method-row count changed")
    if len(set(actual_method_ids)) != len(actual_method_ids):
        raise ValueError("S4 all-new-wave method-row IDs are not unique")
    if sorted(actual_method_ids) != expected_method_ids:
        raise ValueError("S4 all-new-wave method coverage changed")

    by_run: dict[str, list[dict]] = defaultdict(list)
    for row in method_rows:
        by_run[str(row["scientific_run_id"])].append(row)
    if set(by_run) != set(scientific_ids):
        raise ValueError("S4 all-new-wave scientific coverage changed")

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
            raise ValueError("S4 all-new-wave method set changed")
        if len({str(row["dataset_sha256"]) for row in rows}) != 1:
            raise ValueError("S4 all-new-wave paired methods saw different datasets")
        if any(
            str(row["evidence_origin"]) != EVIDENCE_ORIGIN_NEW for row in rows
        ):
            raise ValueError("S4 all-new-wave imported evidence is forbidden")

        for row in rows:
            status = str(row["status"])
            if status not in allowed_statuses:
                raise ValueError("S4 all-new-wave unsupported terminal status")
            status_counts[status] += 1
            evidence_counts[str(row["evidence_origin"])] += 1
            if row["decision"] is not None:
                decision_counts[str(row["decision"])] += 1
            if status == UNRESOLVED_AT_CAP:
                if row["decision"] is not None:
                    raise ValueError("S4 all-new-wave unresolved row has decision")
                if int(row["terminal_n"]) != 10000:
                    raise ValueError(
                        "S4 all-new-wave unresolved row did not reach cap"
                    )
            if status in {REFIT_FAILURE, PREFIX_EXECUTION_FAILURE}:
                if row["decision"] is not None:
                    raise ValueError("S4 all-new-wave failure row has decision")

    expected_new_method_rows = len(scientific_rows) * 4
    if evidence_counts != Counter(
        {EVIDENCE_ORIGIN_NEW: expected_new_method_rows}
    ):
        raise ValueError("S4 all-new-wave evidence-origin count changed")

    return {
        "status": shard_status(wave_id),
        "authoritative": False,
        "wave_id": wave_id,
        "shard_index": int(shard_index),
        "scientific_run_count": len(scientific_rows),
        "method_row_count": len(method_rows),
        "imported_scientific_run_count": 0,
        "new_scientific_run_count": len(scientific_rows),
        "imported_method_row_count": 0,
        "new_method_execution_count": len(method_rows),
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
