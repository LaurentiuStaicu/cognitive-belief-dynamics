from __future__ import annotations

from collections import Counter, defaultdict
import hashlib
import json
import statistics
from typing import Any

from .f1b_r2_paired_method_m2_sequential_resolution import (
    EXPECTED_METHODS_M2,
    REFIT_FAILURE,
    UNRESOLVED_AT_CAP,
)
from .f1b_r2_s4_broad_executor import PREFIX_EXECUTION_FAILURE
from .f1b_r2_s4_w0_shard import (
    EVIDENCE_ORIGIN_IMPORTED,
    EVIDENCE_ORIGIN_NEW,
    SHARD_STATUS,
    method_row_id,
)


COMBINED_STATUS = "NON_AUTHORITATIVE_S4_W0_COMBINED_COMPLETE"


def canonical_json_sha256(value: Any) -> str:
    payload = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _counter_dict(counter: Counter) -> dict:
    return dict(sorted(counter.items()))


def combine_w0_shards(
    shard_results: list[dict],
    *,
    plan: dict,
    config: dict,
) -> dict:
    if len(shard_results) != 250:
        raise ValueError("S4 W0 combine requires exactly 250 shards")

    by_index = {int(row["shard_index"]): row for row in shard_results}
    if len(by_index) != 250 or set(by_index) != set(range(250)):
        raise ValueError("S4 W0 shard-index coverage changed")

    expected_plan = {
        int(row["shard_index"]): row for row in plan["shard_plan"]
    }
    if set(expected_plan) != set(range(250)):
        raise ValueError("S4 W0 plan shard coverage changed")

    all_rows: list[dict] = []
    scientific_ids: set[str] = set()
    shard_identity_rows: list[str] = []
    for shard_index in range(250):
        shard = by_index[shard_index]
        expected = expected_plan[shard_index]
        if shard["status"] != SHARD_STATUS:
            raise ValueError("S4 W0 shard status changed")
        if shard["authoritative"] is not False:
            raise ValueError("S4 W0 shard became authoritative")
        for key in (
            "scientific_run_count",
            "imported_scientific_run_count",
            "new_scientific_run_count",
            "imported_method_row_count",
            "new_method_execution_count",
        ):
            if int(shard[key]) != int(expected[key]):
                raise ValueError(
                    f"S4 W0 shard count changed: shard={shard_index} key={key}"
                )
        if int(shard["method_row_count"]) != int(
            expected["scientific_run_count"]
        ) * 4:
            raise ValueError("S4 W0 shard method-row count changed")
        if shard["scientific_interpretation_authorized"] is not False:
            raise ValueError("S4 W0 shard interpretation unexpectedly enabled")
        if shard["method_selected"] is not False:
            raise ValueError("S4 W0 shard selected a method")
        if shard["power_validated"] is not False:
            raise ValueError("S4 W0 shard validated power")

        rows = list(shard["rows"])
        if len(rows) != int(shard["method_row_count"]):
            raise ValueError("S4 W0 shard embedded row count changed")

        local_scientific = sorted(
            {str(row["scientific_run_id"]) for row in rows}
        )
        if len(local_scientific) != int(shard["scientific_run_count"]):
            raise ValueError("S4 W0 shard scientific-row embedding changed")
        if canonical_json_sha256(local_scientific) != str(
            shard["scientific_run_ids_sha256"]
        ):
            raise ValueError("S4 W0 shard scientific digest changed")

        local_method_ids = sorted(
            method_row_id(
                str(row["scientific_run_id"]),
                str(row["inference_method"]),
            )
            for row in rows
        )
        if canonical_json_sha256(local_method_ids) != str(
            shard["method_row_ids_sha256"]
        ):
            raise ValueError("S4 W0 shard method digest changed")

        overlap = scientific_ids.intersection(local_scientific)
        if overlap:
            raise ValueError("S4 W0 scientific run appears in multiple shards")
        scientific_ids.update(local_scientific)
        all_rows.extend(rows)
        shard_identity_rows.append(
            f"{shard_index:03d}|"
            f"{shard['scientific_run_ids_sha256']}|"
            f"{shard['method_row_ids_sha256']}"
        )

    if len(scientific_ids) != 3750:
        raise ValueError("S4 W0 combined scientific-run count changed")
    if len(all_rows) != 15000:
        raise ValueError("S4 W0 combined method-row count changed")

    sorted_scientific_ids = sorted(scientific_ids)
    if canonical_json_sha256(sorted_scientific_ids) != str(
        config["wave"]["scientific_run_ids_sha256"]
    ):
        raise ValueError("S4 W0 combined scientific-run digest changed")

    method_ids = [
        method_row_id(
            str(row["scientific_run_id"]),
            str(row["inference_method"]),
        )
        for row in all_rows
    ]
    if len(set(method_ids)) != 15000:
        raise ValueError("S4 W0 combined method-row IDs are not unique")
    if canonical_json_sha256(sorted(method_ids)) != str(
        config["wave"]["method_row_ids_sha256"]
    ):
        raise ValueError("S4 W0 combined method-row digest changed")

    by_run: dict[str, list[dict]] = defaultdict(list)
    for row in all_rows:
        by_run[str(row["scientific_run_id"])].append(row)
    for run_id, rows in by_run.items():
        if {str(row["inference_method"]) for row in rows} != set(
            EXPECTED_METHODS_M2
        ):
            raise ValueError(f"S4 W0 combined method coverage changed: {run_id}")
        if len({str(row["dataset_sha256"]) for row in rows}) != 1:
            raise ValueError(f"S4 W0 combined dataset pairing changed: {run_id}")

    evidence_counts = Counter(str(row["evidence_origin"]) for row in all_rows)
    if evidence_counts != Counter(
        {EVIDENCE_ORIGIN_IMPORTED: 3360, EVIDENCE_ORIGIN_NEW: 11640}
    ):
        raise ValueError("S4 W0 evidence-origin counts changed")

    imported_ids = sorted(
        method_row_id(
            str(row["scientific_run_id"]),
            str(row["inference_method"]),
        )
        for row in all_rows
        if row["evidence_origin"] == EVIDENCE_ORIGIN_IMPORTED
    )
    new_ids = sorted(
        method_row_id(
            str(row["scientific_run_id"]),
            str(row["inference_method"]),
        )
        for row in all_rows
        if row["evidence_origin"] == EVIDENCE_ORIGIN_NEW
    )
    if canonical_json_sha256(imported_ids) != str(
        config["wave"]["imported_method_row_ids_sha256"]
    ):
        raise ValueError("S4 W0 imported combined digest changed")
    if canonical_json_sha256(new_ids) != str(
        config["wave"]["new_method_row_ids_sha256"]
    ):
        raise ValueError("S4 W0 new combined digest changed")

    status_counts = Counter(str(row["status"]) for row in all_rows)
    decision_counts = Counter(
        str(row["decision"])
        for row in all_rows
        if row["decision"] is not None
    )
    allowed_statuses = {
        "SEQUENTIAL_RESOLVED_AT_PREFIX",
        "SEQUENTIAL_RESOLVED",
        UNRESOLVED_AT_CAP,
        REFIT_FAILURE,
        PREFIX_EXECUTION_FAILURE,
    }
    if not set(status_counts).issubset(allowed_statuses):
        raise ValueError("S4 W0 combined unsupported terminal status")

    method_summaries = {}
    for method in EXPECTED_METHODS_M2:
        rows = [
            row for row in all_rows if str(row["inference_method"]) == method
        ]
        if len(rows) != 3750:
            raise ValueError("S4 W0 combined method row count changed")
        terminal_ns = [int(row["terminal_n"]) for row in rows]
        method_summaries[method] = {
            "row_count": len(rows),
            "status_counts": _counter_dict(
                Counter(str(row["status"]) for row in rows)
            ),
            "decision_counts": _counter_dict(
                Counter(
                    str(row["decision"])
                    for row in rows
                    if row["decision"] is not None
                )
            ),
            "evidence_origin_counts": _counter_dict(
                Counter(str(row["evidence_origin"]) for row in rows)
            ),
            "terminal_n_summary": {
                "minimum": min(terminal_ns),
                "median": statistics.median(terminal_ns),
                "maximum": max(terminal_ns),
            },
        }

    role_missingness = {}
    groups: dict[tuple[str, float], list[dict]] = defaultdict(list)
    for row in all_rows:
        groups[(str(row["role"]), float(row["missingness_rate"]))].append(row)
    for (role, missingness), rows in sorted(groups.items()):
        key = f"{role}|MISSINGNESS={missingness:.2f}"
        role_missingness[key] = {
            "method_row_count": len(rows),
            "status_counts": _counter_dict(
                Counter(str(row["status"]) for row in rows)
            ),
            "decision_counts": _counter_dict(
                Counter(
                    str(row["decision"])
                    for row in rows
                    if row["decision"] is not None
                )
            ),
        }

    ordered_rows = sorted(
        all_rows,
        key=lambda row: (
            str(row["scientific_run_id"]),
            EXPECTED_METHODS_M2.index(str(row["inference_method"])),
        ),
    )

    return {
        "status": COMBINED_STATUS,
        "authoritative": False,
        "issue": int(config["issue"]),
        "wave_id": "W0",
        "shard_count": 250,
        "scientific_run_count": 3750,
        "method_row_count": 15000,
        "imported_scientific_run_count": 840,
        "imported_method_row_count": 3360,
        "new_scientific_run_count": 2910,
        "new_method_execution_count": 11640,
        "scientific_run_ids_sha256": canonical_json_sha256(
            sorted_scientific_ids
        ),
        "method_row_ids_sha256": canonical_json_sha256(sorted(method_ids)),
        "imported_method_row_ids_sha256": canonical_json_sha256(imported_ids),
        "new_method_row_ids_sha256": canonical_json_sha256(new_ids),
        "shard_identity_digest_sha256": canonical_json_sha256(
            sorted(shard_identity_rows)
        ),
        "row_content_sha256": canonical_json_sha256(ordered_rows),
        "status_counts": _counter_dict(status_counts),
        "decision_counts": _counter_dict(decision_counts),
        "evidence_origin_counts": _counter_dict(evidence_counts),
        "method_summaries": method_summaries,
        "role_missingness_summaries": role_missingness,
        "rows": ordered_rows,
        "scientific_interpretation_authorized": False,
        "method_selected": False,
        "power_validated": False,
        "w1_authorized_after_retention": True,
        "release_0_2_0_blocker_closed": False,
    }
