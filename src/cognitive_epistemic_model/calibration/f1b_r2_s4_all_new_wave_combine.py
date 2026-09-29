from __future__ import annotations

from collections import Counter, defaultdict
import statistics

from .f1b_r2_paired_method_m2_sequential_resolution import (
    EXPECTED_METHODS_M2,
    REFIT_FAILURE,
    UNRESOLVED_AT_CAP,
)
from .f1b_r2_s4_all_new_wave import (
    canonical_json_sha256,
    combined_status,
    method_row_id,
    validate_all_new_wave_config,
)
from .f1b_r2_s4_broad_executor import (
    EVIDENCE_ORIGIN_NEW,
    PREFIX_EXECUTION_FAILURE,
)


def _counter_dict(counter: Counter) -> dict:
    return dict(sorted(counter.items()))


def combine_all_new_wave_shards(
    shard_results: list[dict],
    *,
    plan: dict,
    config: dict,
) -> dict:
    validate_all_new_wave_config(config)
    wave_id = str(config["wave"]["wave_id"])

    if len(shard_results) != 250:
        raise ValueError("S4 all-new-wave combine requires exactly 250 shards")

    by_index = {int(row["shard_index"]): row for row in shard_results}
    if len(by_index) != 250 or set(by_index) != set(range(250)):
        raise ValueError("S4 all-new-wave shard-index coverage changed")

    expected_plan = {
        int(row["shard_index"]): row for row in plan["shard_plan"]
    }
    if set(expected_plan) != set(range(250)):
        raise ValueError("S4 all-new-wave plan shard coverage changed")
    if str(plan["wave_id"]) != wave_id:
        raise ValueError("S4 all-new-wave plan wave changed")

    all_rows: list[dict] = []
    scientific_ids: set[str] = set()
    shard_identity_rows: list[str] = []

    expected_shard_status = (
        f"NON_AUTHORITATIVE_S4_{wave_id}_SHARD_COMPLETE"
    )
    for shard_index in range(250):
        shard = by_index[shard_index]
        expected = expected_plan[shard_index]

        if shard["status"] != expected_shard_status:
            raise ValueError("S4 all-new-wave shard status changed")
        if shard["authoritative"] is not False:
            raise ValueError("S4 all-new-wave shard became authoritative")
        if str(shard["wave_id"]) != wave_id:
            raise ValueError("S4 all-new-wave shard wave changed")

        for key in (
            "scientific_run_count",
            "new_scientific_run_count",
            "new_method_execution_count",
        ):
            if int(shard[key]) != int(expected[key]):
                raise ValueError(
                    f"S4 all-new-wave shard count changed: "
                    f"shard={shard_index} key={key}"
                )
        if int(shard["imported_scientific_run_count"]) != 0:
            raise ValueError("S4 all-new-wave imported scientific row found")
        if int(shard["imported_method_row_count"]) != 0:
            raise ValueError("S4 all-new-wave imported method row found")
        if int(shard["method_row_count"]) != int(
            expected["scientific_run_count"]
        ) * 4:
            raise ValueError("S4 all-new-wave shard method-row count changed")
        if str(shard["scientific_run_ids_sha256"]) != str(
            expected["scientific_run_ids_sha256"]
        ):
            raise ValueError("S4 all-new-wave shard scientific digest changed")
        if str(shard["method_row_ids_sha256"]) != str(
            expected["method_row_ids_sha256"]
        ):
            raise ValueError("S4 all-new-wave shard method digest changed")
        if shard["scientific_interpretation_authorized"] is not False:
            raise ValueError(
                "S4 all-new-wave shard interpretation unexpectedly enabled"
            )
        if shard["method_selected"] is not False:
            raise ValueError("S4 all-new-wave shard selected a method")
        if shard["power_validated"] is not False:
            raise ValueError("S4 all-new-wave shard validated power")

        rows = list(shard["rows"])
        if len(rows) != int(shard["method_row_count"]):
            raise ValueError("S4 all-new-wave shard embedded row count changed")

        local_scientific = sorted(
            {str(row["scientific_run_id"]) for row in rows}
        )
        if len(local_scientific) != int(shard["scientific_run_count"]):
            raise ValueError(
                "S4 all-new-wave shard scientific-row embedding changed"
            )

        overlap = scientific_ids.intersection(local_scientific)
        if overlap:
            raise ValueError(
                "S4 all-new-wave scientific run appears in multiple shards"
            )
        scientific_ids.update(local_scientific)
        all_rows.extend(rows)
        shard_identity_rows.append(
            f"{shard_index:03d}|"
            f"{shard['scientific_run_ids_sha256']}|"
            f"{shard['method_row_ids_sha256']}"
        )

    if len(scientific_ids) != 3750:
        raise ValueError("S4 all-new-wave combined scientific count changed")
    if len(all_rows) != 15000:
        raise ValueError("S4 all-new-wave combined method count changed")

    sorted_scientific_ids = sorted(scientific_ids)
    if canonical_json_sha256(sorted_scientific_ids) != str(
        config["wave"]["scientific_run_ids_sha256"]
    ):
        raise ValueError("S4 all-new-wave combined scientific digest changed")

    method_ids = [
        method_row_id(
            str(row["scientific_run_id"]),
            str(row["inference_method"]),
        )
        for row in all_rows
    ]
    if len(set(method_ids)) != 15000:
        raise ValueError("S4 all-new-wave combined method IDs are not unique")
    if canonical_json_sha256(sorted(method_ids)) != str(
        config["wave"]["method_row_ids_sha256"]
    ):
        raise ValueError("S4 all-new-wave combined method digest changed")

    by_run: dict[str, list[dict]] = defaultdict(list)
    for row in all_rows:
        by_run[str(row["scientific_run_id"])].append(row)
    for run_id, rows in by_run.items():
        if {str(row["inference_method"]) for row in rows} != set(
            EXPECTED_METHODS_M2
        ):
            raise ValueError(
                f"S4 all-new-wave method coverage changed: {run_id}"
            )
        if len({str(row["dataset_sha256"]) for row in rows}) != 1:
            raise ValueError(
                f"S4 all-new-wave dataset pairing changed: {run_id}"
            )

    evidence_counts = Counter(str(row["evidence_origin"]) for row in all_rows)
    if evidence_counts != Counter({EVIDENCE_ORIGIN_NEW: 15000}):
        raise ValueError("S4 all-new-wave evidence origin changed")

    allowed_statuses = {
        "SEQUENTIAL_RESOLVED_AT_PREFIX",
        "SEQUENTIAL_RESOLVED",
        UNRESOLVED_AT_CAP,
        REFIT_FAILURE,
        PREFIX_EXECUTION_FAILURE,
    }
    status_counts = Counter(str(row["status"]) for row in all_rows)
    if not set(status_counts).issubset(allowed_statuses):
        raise ValueError("S4 all-new-wave unsupported terminal status")
    decision_counts = Counter(
        str(row["decision"])
        for row in all_rows
        if row["decision"] is not None
    )

    method_summaries = {}
    for method in EXPECTED_METHODS_M2:
        rows = [
            row for row in all_rows if str(row["inference_method"]) == method
        ]
        if len(rows) != 3750:
            raise ValueError("S4 all-new-wave method row count changed")
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
        "status": combined_status(wave_id),
        "authoritative": False,
        "issue": int(config["issue"]),
        "wave_id": wave_id,
        "shard_count": 250,
        "scientific_run_count": 3750,
        "method_row_count": 15000,
        "imported_scientific_run_count": 0,
        "imported_method_row_count": 0,
        "new_scientific_run_count": 3750,
        "new_method_execution_count": 15000,
        "scientific_run_ids_sha256": canonical_json_sha256(
            sorted_scientific_ids
        ),
        "method_row_ids_sha256": canonical_json_sha256(sorted(method_ids)),
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
        "next_wave_id": str(config["wave"]["next_wave_id"]),
        "next_wave_authorized_after_retention": True,
        "release_0_2_0_blocker_closed": False,
    }
