from __future__ import annotations

from collections import Counter
import hashlib
import json
from typing import Any

from .f1b_r2_paired_method_m2_sequential_resolution import stable_shard


TOPOLOGY_ID = "F1B.R2.S4.BROAD_EXECUTION_TOPOLOGY.V1"
STATUS = "NON_AUTHORITATIVE_S4_BROAD_EXECUTION_TOPOLOGY_DESIGN"
EXPECTED_METHODS = (
    "POPULATION",
    "HIERARCHICAL_0.5X",
    "HIERARCHICAL_1X",
    "HIERARCHICAL_2X",
)


def canonical_json_sha256(value: Any) -> str:
    payload = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def validate_topology_config(config: dict) -> None:
    if config["topology_id"] != TOPOLOGY_ID:
        raise ValueError("S4 topology identity changed")
    if config["status"] != STATUS:
        raise ValueError("unsupported S4 topology status")
    if int(config["issue"]) != 259:
        raise ValueError("S4 topology issue changed")

    binding = config["retained_sources"]["method_binding_result"]
    if tuple(binding["eligible_methods"]) != EXPECTED_METHODS:
        raise ValueError("S4 topology method order/set changed")
    if int(binding["scientific_run_count"]) != 15000:
        raise ValueError("S4 topology scientific-run count changed")
    if int(binding["method_execution_count"]) != 60000:
        raise ValueError("S4 topology method-execution count changed")
    if float(binding["maximum_worst_case_component_mcse"]) != 0.05:
        raise ValueError("S4 topology MCSE target changed")

    prefix = config["retained_sources"]["prefix_bridge_result"]
    if int(prefix["imported_scientific_run_count"]) != 840:
        raise ValueError("S4 topology imported scientific-run count changed")
    if int(prefix["imported_method_row_count"]) != 3360:
        raise ValueError("S4 topology imported method-row count changed")

    wave_partition = config["wave_partition"]
    if tuple(int(x) for x in wave_partition["exhaustive_indices"]) != tuple(
        range(100)
    ):
        raise ValueError("S4 topology replicate identity changed")
    if int(wave_partition["wave_count"]) != 4:
        raise ValueError("S4 topology wave count changed")

    expected = (
        ("W0", 0, 24, 3750, 840, 3360, 2910, 11640),
        ("W1", 25, 49, 3750, 0, 0, 3750, 15000),
        ("W2", 50, 74, 3750, 0, 0, 3750, 15000),
        ("W3", 75, 99, 3750, 0, 0, 3750, 15000),
    )
    actual = tuple(
        (
            str(w["wave_id"]),
            int(w["replicate_start"]),
            int(w["replicate_end"]),
            int(w["expected_scientific_run_count"]),
            int(w["imported_scientific_run_count"]),
            int(w["imported_method_row_count"]),
            int(w["new_scientific_run_count"]),
            int(w["new_method_execution_count"]),
        )
        for w in wave_partition["waves"]
    )
    if actual != expected:
        raise ValueError("S4 topology wave definition changed")

    shard = config["shard_partition"]
    if int(shard["shard_count_per_wave"]) != 250:
        raise ValueError("S4 topology shard count changed")
    if shard["assignment_key"] != "scientific_run_id":
        raise ValueError("S4 topology shard key changed")
    if shard["hash_algorithm"] != "SHA256_FIRST_8_BYTES_BIG_ENDIAN_MODULO":
        raise ValueError("S4 topology shard hash changed")
    if shard["all_methods_for_scientific_run_same_shard"] is not True:
        raise ValueError("S4 topology method pairing weakened")
    if shard["imported_rows_remain_with_scientific_run_shard"] is not True:
        raise ValueError("S4 topology imported-row locality changed")
    if int(shard["expected_matrix_jobs_per_wave"]) != 250:
        raise ValueError("S4 topology matrix size changed")
    if int(shard["github_actions_matrix_max_jobs"]) != 256:
        raise ValueError("S4 topology GitHub matrix limit changed")
    if shard["wave_combine_job_is_not_matrix_member"] is not True:
        raise ValueError("S4 topology wave combine placement changed")
    if shard["expected_assignment_rows_sha256"] != (
        "7d37f2384c1003490a4b6e7a091f8648ed61e72241f964d3ce0336229f63dbce"
    ):
        raise ValueError("S4 topology assignment digest changed")
    expected_ranges = {
        "W0": [5, 29],
        "W1": [5, 27],
        "W2": [6, 27],
        "W3": [4, 27],
    }
    if shard["expected_scientific_runs_per_shard_range"] != expected_ranges:
        raise ValueError("S4 topology expected shard ranges changed")

    combine = config["final_combine"]
    if tuple(combine["required_wave_ids"]) != ("W0", "W1", "W2", "W3"):
        raise ValueError("S4 final wave set changed")
    if int(combine["total_scientific_run_count"]) != 15000:
        raise ValueError("S4 final scientific-run count changed")
    if int(combine["total_method_row_count"]) != 60000:
        raise ValueError("S4 final method-row count changed")
    if int(combine["imported_method_row_count"]) != 3360:
        raise ValueError("S4 final imported method-row count changed")
    if int(combine["newly_executed_method_row_count"]) != 56640:
        raise ValueError("S4 final new method-row count changed")
    if tuple(combine["exact_method_order"]) != EXPECTED_METHODS:
        raise ValueError("S4 final method order/set changed")
    if combine["retain_unresolved_in_denominators"] is not True:
        raise ValueError("S4 unresolved denominator rule changed")
    if combine["method_selection_by_combine"] is not False:
        raise ValueError("S4 combine cannot select a method")

    policy = config["execution_policy"]
    if policy["separate_workflow_run_per_wave"] is not True:
        raise ValueError("S4 waves must execute separately")
    if tuple(policy["execute_wave_order"]) != ("W0", "W1", "W2", "W3"):
        raise ValueError("S4 wave execution order changed")
    if policy["early_scientific_interpretation_forbidden"] is not True:
        raise ValueError("S4 early interpretation was enabled")
    if policy["final_scientific_interpretation_requires_all_waves"] is not True:
        raise ValueError("S4 final interpretation completeness weakened")
    if policy["failed_shard_recomputed_same_identity_only"] is not True:
        raise ValueError("S4 failed-shard identity rule weakened")

    if config["release"]["release_blocker_closed"] is not False:
        raise ValueError("S4 topology cannot close v0.2.0 blocker")
    if any(bool(value) for value in config["boundary"].values()):
        raise ValueError("S4 topology boundary was weakened")


def wave_for_replicate(replicate: int) -> str:
    value = int(replicate)
    if not 0 <= value <= 99:
        raise ValueError("S4 replicate outside 0..99")
    return f"W{value // 25}"


def is_imported_prefix_row(row: dict) -> bool:
    replicate = int(row["evaluation_replicate"])
    identity_type = str(row["identity_type"])
    if identity_type == "DEPARTURE":
        return replicate in range(5)
    if identity_type == "NULL":
        return replicate in range(20)
    raise ValueError("unsupported S4 identity type")


def method_row_id(scientific_run_id: str, method_id: str) -> str:
    return f"{scientific_run_id}|METHOD={method_id}"


def build_topology_manifest(
    s4_manifest: dict,
    prefix_result: dict,
    config: dict,
) -> dict:
    validate_topology_config(config)

    if s4_manifest["status"] != (
        "NON_AUTHORITATIVE_S4_BROAD_SCIENTIFIC_MATRIX_MANIFEST"
    ):
        raise ValueError("S4 raw manifest status changed")
    if int(s4_manifest["scientific_run_count"]) != 15000:
        raise ValueError("S4 raw manifest run count changed")

    rows = list(s4_manifest["rows"])
    run_ids = [str(row["scientific_run_id"]) for row in rows]
    if len(run_ids) != 15000 or len(set(run_ids)) != 15000:
        raise ValueError("S4 topology requires 15,000 unique run IDs")
    if canonical_json_sha256(sorted(run_ids)) != str(
        config["retained_sources"]["s4_matrix_result"][
            "scientific_run_ids_sha256"
        ]
    ):
        raise ValueError("S4 topology raw manifest digest mismatch")

    imported_ids = sorted(
        str(row["scientific_run_id"])
        for row in rows
        if is_imported_prefix_row(row)
    )
    if len(imported_ids) != 840:
        raise ValueError("S4 topology imported run count is not 840")
    if canonical_json_sha256(imported_ids) != str(
        prefix_result["import_identity"]["imported_scientific_run_ids_sha256"]
    ):
        raise ValueError("S4 topology imported run digest mismatch")

    imported_method_ids = sorted(
        method_row_id(run_id, method)
        for run_id in imported_ids
        for method in EXPECTED_METHODS
    )
    if len(imported_method_ids) != 3360:
        raise ValueError("S4 topology imported method count is not 3,360")
    if canonical_json_sha256(imported_method_ids) != str(
        prefix_result["import_identity"]["imported_method_row_ids_sha256"]
    ):
        raise ValueError("S4 topology imported method digest mismatch")

    wave_counts: Counter[str] = Counter()
    wave_imported: Counter[str] = Counter()
    shard_counts: Counter[tuple[str, int]] = Counter()
    shard_imported: Counter[tuple[str, int]] = Counter()
    assignment_rows: list[str] = []

    for row in rows:
        run_id = str(row["scientific_run_id"])
        wave_id = wave_for_replicate(int(row["evaluation_replicate"]))
        shard_index = stable_shard(run_id, 250)
        imported = is_imported_prefix_row(row)

        wave_counts[wave_id] += 1
        shard_counts[(wave_id, shard_index)] += 1
        if imported:
            wave_imported[wave_id] += 1
            shard_imported[(wave_id, shard_index)] += 1

        assignment_rows.append(
            f"{run_id}|WAVE={wave_id}|SHARD={shard_index:03d}"
            f"|IMPORTED={int(imported)}"
        )

    assignment_digest = canonical_json_sha256(sorted(assignment_rows))
    if assignment_digest != str(
        config["shard_partition"]["expected_assignment_rows_sha256"]
    ):
        raise ValueError("S4 topology assignment digest mismatch")

    expected_wave_counts = {f"W{i}": 3750 for i in range(4)}
    if dict(wave_counts) != expected_wave_counts:
        raise ValueError("S4 topology wave coverage changed")
    if dict(wave_imported) != {"W0": 840}:
        raise ValueError("S4 imported prefix escaped W0")

    shard_plan: list[dict] = []
    for wave_index in range(4):
        wave_id = f"W{wave_index}"
        for shard_index in range(250):
            scientific = int(shard_counts[(wave_id, shard_index)])
            imported = int(shard_imported[(wave_id, shard_index)])
            new_scientific = scientific - imported
            shard_plan.append(
                {
                    "wave_id": wave_id,
                    "shard_index": shard_index,
                    "scientific_run_count": scientific,
                    "imported_scientific_run_count": imported,
                    "new_scientific_run_count": new_scientific,
                    "imported_method_row_count": imported * 4,
                    "new_method_execution_count": new_scientific * 4,
                }
            )

    if len(shard_plan) != 1000:
        raise ValueError("S4 topology shard-plan count changed")
    if any(row["scientific_run_count"] <= 0 for row in shard_plan):
        raise ValueError("S4 topology contains empty shard")
    if sum(row["scientific_run_count"] for row in shard_plan) != 15000:
        raise ValueError("S4 topology shard coverage is incomplete")
    if sum(row["imported_scientific_run_count"] for row in shard_plan) != 840:
        raise ValueError("S4 topology imported shard coverage changed")
    if sum(row["new_method_execution_count"] for row in shard_plan) != 56640:
        raise ValueError("S4 topology new execution count changed")

    per_wave_summary = []
    for wave_id in ("W0", "W1", "W2", "W3"):
        subset = [row for row in shard_plan if row["wave_id"] == wave_id]
        summary = {
                "wave_id": wave_id,
                "shard_count": len(subset),
                "scientific_run_count": sum(
                    row["scientific_run_count"] for row in subset
                ),
                "imported_scientific_run_count": sum(
                    row["imported_scientific_run_count"] for row in subset
                ),
                "new_scientific_run_count": sum(
                    row["new_scientific_run_count"] for row in subset
                ),
                "imported_method_row_count": sum(
                    row["imported_method_row_count"] for row in subset
                ),
                "new_method_execution_count": sum(
                    row["new_method_execution_count"] for row in subset
                ),
                "minimum_scientific_runs_per_shard": min(
                    row["scientific_run_count"] for row in subset
                ),
            "maximum_scientific_runs_per_shard": max(
                row["scientific_run_count"] for row in subset
            ),
        }
        expected_range = config["shard_partition"][
            "expected_scientific_runs_per_shard_range"
        ][wave_id]
        if [
            summary["minimum_scientific_runs_per_shard"],
            summary["maximum_scientific_runs_per_shard"],
        ] != expected_range:
            raise ValueError("S4 topology shard range mismatch")
        per_wave_summary.append(summary)

    return {
        "topology_id": config["topology_id"],
        "status": "NON_AUTHORITATIVE_S4_BROAD_EXECUTION_TOPOLOGY_COMPLETE",
        "authoritative": False,
        "issue": int(config["issue"]),
        "wave_count": 4,
        "shard_count_per_wave": 250,
        "total_shard_count": 1000,
        "scientific_run_count": 15000,
        "method_row_count": 60000,
        "imported_scientific_run_count": 840,
        "imported_method_row_count": 3360,
        "new_scientific_run_count": 14160,
        "new_method_execution_count": 56640,
        "scientific_run_ids_sha256": canonical_json_sha256(sorted(run_ids)),
        "assignment_rows_sha256": assignment_digest,
        "per_wave_summary": per_wave_summary,
        "shard_plan": shard_plan,
        "broad_execution_authorized_after_topology_retention": True,
        "scientific_interpretation_authorized": False,
        "release_0_2_0_blocker_closed": False,
        "boundary": dict(config["boundary"]),
    }
