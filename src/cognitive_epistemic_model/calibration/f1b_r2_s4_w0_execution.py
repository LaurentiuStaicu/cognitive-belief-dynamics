from __future__ import annotations

from collections import Counter
import hashlib
import json
from typing import Any

from .f1b_r2_paired_method_m2_sequential_resolution import stable_shard


GATE_ID = "F1B.R2.S4.W0.EXECUTION_GATE.V1"
STATUS = "NON_AUTHORITATIVE_S4_W0_EXECUTION_DESIGN"
EXPECTED_RAW_M2_STATUS = "NON_AUTHORITATIVE_PAIRED_METHOD_M2_COMBINED_RESULT"
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


def method_row_id(scientific_run_id: str, method_id: str) -> str:
    return f"{scientific_run_id}|METHOD={method_id}"


def is_imported_prefix_row(row: dict) -> bool:
    replicate = int(row["evaluation_replicate"])
    identity_type = str(row["identity_type"])
    if identity_type == "DEPARTURE":
        return replicate in range(5)
    if identity_type == "NULL":
        return replicate in range(20)
    raise ValueError("unsupported W0 identity type")


def validate_w0_config(config: dict) -> None:
    if config["gate_id"] != GATE_ID:
        raise ValueError("S4 W0 gate identity changed")
    if config["status"] != STATUS:
        raise ValueError("unsupported S4 W0 gate status")
    if int(config["issue"]) != 259:
        raise ValueError("S4 W0 issue changed")

    preflight = config["retained_sources"]["fresh_preflight_result"]
    if preflight["structural_preflight_pass"] is not True:
        raise ValueError("S4 W0 requires passed fresh preflight")
    if preflight["w0_authorized_after_retention"] is not True:
        raise ValueError("S4 W0 fresh-preflight authorization changed")

    methods = tuple(
        config["retained_sources"]["method_binding_result"][
            "eligible_methods"
        ]
    )
    if methods != EXPECTED_METHODS:
        raise ValueError("S4 W0 method order/set changed")

    wave = config["wave"]
    expected_wave = {
        "wave_id": "W0",
        "replicate_start": 0,
        "replicate_end": 24,
        "scientific_run_count": 3750,
        "method_row_count": 15000,
        "imported_scientific_run_count": 840,
        "imported_method_row_count": 3360,
        "new_scientific_run_count": 2910,
        "new_method_execution_count": 11640,
    }
    for key, expected in expected_wave.items():
        if wave[key] != expected:
            raise ValueError(f"S4 W0 wave contract changed: {key}")

    shards = config["shards"]
    if int(shards["shard_count"]) != 250:
        raise ValueError("S4 W0 shard count changed")
    if tuple(int(x) for x in shards["matrix_indices"]) != tuple(range(250)):
        raise ValueError("S4 W0 shard matrix changed")
    if shards["fail_fast"] is not False:
        raise ValueError("S4 W0 fail-fast policy changed")
    if int(shards["max_parallel"]) != 20:
        raise ValueError("S4 W0 max-parallel changed")
    if shards["all_four_methods_same_scientific_run_same_shard"] is not True:
        raise ValueError("S4 W0 method pairing weakened")

    execution = config["execution"]
    if execution["imported_rows_recomputed"] is not False:
        raise ValueError("S4 W0 imported rows cannot be recomputed")
    if execution["new_rows_use_broad_executor"] is not True:
        raise ValueError("S4 W0 broad executor binding weakened")
    if execution["numerical_lineage"] != "Haswell":
        raise ValueError("S4 W0 numerical lineage changed")
    if int(execution["sequential_prefix_attempts"]) != 199:
        raise ValueError("S4 W0 prefix length changed")
    if int(execution["sequential_max_total_attempts"]) != 10000:
        raise ValueError("S4 W0 sequential cap changed")
    if execution["stop_on_first_refit_failure"] is not True:
        raise ValueError("S4 W0 refit-failure rule changed")
    if execution["wave_combine_requires_all_250_shards"] is not True:
        raise ValueError("S4 W0 combine completeness weakened")
    if execution["scientific_interpretation_after_wave"] is not False:
        raise ValueError("S4 W0 cannot authorize scientific interpretation")

    combine = config["wave_combine"]
    if int(combine["exact_scientific_run_count"]) != 3750:
        raise ValueError("S4 W0 combine scientific-run count changed")
    if int(combine["exact_method_row_count"]) != 15000:
        raise ValueError("S4 W0 combine method-row count changed")
    if int(combine["exact_imported_method_row_count"]) != 3360:
        raise ValueError("S4 W0 combine imported-row count changed")
    if int(combine["exact_new_method_row_count"]) != 11640:
        raise ValueError("S4 W0 combine new-row count changed")
    if combine["retain_unresolved_in_denominators"] is not True:
        raise ValueError("S4 W0 unresolved denominator rule changed")
    if combine["retain_refit_failures_in_denominators"] is not True:
        raise ValueError("S4 W0 refit-failure denominator rule changed")
    if combine["method_selection_forbidden"] is not True:
        raise ValueError("S4 W0 cannot select a method")
    if combine["w1_authorization_after_w0_retention"] is not True:
        raise ValueError("S4 W1 authorization rule changed")

    if config["release"]["release_blocker_closed"] is not False:
        raise ValueError("S4 W0 cannot close v0.2.0 blocker")
    if any(bool(value) for value in config["boundary"].values()):
        raise ValueError("S4 W0 boundary was weakened")


def build_w0_plan(
    s4_manifest: dict,
    m2_combined: dict,
    config: dict,
) -> dict:
    validate_w0_config(config)

    if s4_manifest["status"] != (
        "NON_AUTHORITATIVE_S4_BROAD_SCIENTIFIC_MATRIX_MANIFEST"
    ):
        raise ValueError("S4 W0 raw manifest status changed")
    if int(s4_manifest["scientific_run_count"]) != 15000:
        raise ValueError("S4 W0 raw manifest count changed")
    if m2_combined["status"] != EXPECTED_RAW_M2_STATUS:
        raise ValueError("S4 W0 M2 raw status changed")

    rows = [
        row
        for row in s4_manifest["rows"]
        if 0 <= int(row["evaluation_replicate"]) <= 24
    ]
    if len(rows) != 3750:
        raise ValueError("S4 W0 selection is not exactly 3,750 runs")

    run_ids = sorted(str(row["scientific_run_id"]) for row in rows)
    if len(set(run_ids)) != 3750:
        raise ValueError("S4 W0 run identities are not unique")
    if canonical_json_sha256(run_ids) != str(
        config["wave"]["scientific_run_ids_sha256"]
    ):
        raise ValueError("S4 W0 run-ID digest changed")

    all_method_ids = sorted(
        method_row_id(run_id, method)
        for run_id in run_ids
        for method in EXPECTED_METHODS
    )
    if canonical_json_sha256(all_method_ids) != str(
        config["wave"]["method_row_ids_sha256"]
    ):
        raise ValueError("S4 W0 method-row digest changed")

    imported_rows = [row for row in rows if is_imported_prefix_row(row)]
    new_rows = [row for row in rows if not is_imported_prefix_row(row)]
    imported_ids = sorted(
        str(row["scientific_run_id"]) for row in imported_rows
    )
    new_ids = sorted(str(row["scientific_run_id"]) for row in new_rows)
    if len(imported_ids) != 840 or len(new_ids) != 2910:
        raise ValueError("S4 W0 imported/new run counts changed")
    if canonical_json_sha256(imported_ids) != str(
        config["wave"]["imported_scientific_run_ids_sha256"]
    ):
        raise ValueError("S4 W0 imported run digest changed")
    if canonical_json_sha256(new_ids) != str(
        config["wave"]["new_scientific_run_ids_sha256"]
    ):
        raise ValueError("S4 W0 new run digest changed")

    m2_map = {
        (str(row["scientific_run_id"]), str(row["inference_method"])): row
        for row in m2_combined["rows"]
    }
    if len(m2_map) != 3360:
        raise ValueError("S4 W0 M2 retained row identity count changed")
    imported_method_ids = sorted(
        method_row_id(run_id, method)
        for run_id in imported_ids
        for method in EXPECTED_METHODS
    )
    if any(
        (run_id, method) not in m2_map
        for run_id in imported_ids
        for method in EXPECTED_METHODS
    ):
        raise ValueError("S4 W0 imported M2 row coverage changed")
    if canonical_json_sha256(imported_method_ids) != str(
        config["wave"]["imported_method_row_ids_sha256"]
    ):
        raise ValueError("S4 W0 imported method digest changed")

    new_method_ids = sorted(
        method_row_id(run_id, method)
        for run_id in new_ids
        for method in EXPECTED_METHODS
    )
    if canonical_json_sha256(new_method_ids) != str(
        config["wave"]["new_method_row_ids_sha256"]
    ):
        raise ValueError("S4 W0 new method digest changed")

    shard_plan = []
    for shard_index in range(250):
        shard_rows = [
            row
            for row in rows
            if stable_shard(str(row["scientific_run_id"]), 250)
            == shard_index
        ]
        imported = [
            row for row in shard_rows if is_imported_prefix_row(row)
        ]
        new = [
            row for row in shard_rows if not is_imported_prefix_row(row)
        ]
        if not shard_rows:
            raise ValueError("S4 W0 contains an empty shard")
        shard_plan.append(
            {
                "shard_index": shard_index,
                "scientific_run_count": len(shard_rows),
                "imported_scientific_run_count": len(imported),
                "new_scientific_run_count": len(new),
                "imported_method_row_count": len(imported) * 4,
                "new_method_execution_count": len(new) * 4,
                "scientific_run_ids_sha256": canonical_json_sha256(
                    sorted(str(row["scientific_run_id"]) for row in shard_rows)
                ),
            }
        )

    counts = [row["scientific_run_count"] for row in shard_plan]
    if min(counts) != int(
        config["shards"]["minimum_scientific_runs_per_shard"]
    ):
        raise ValueError("S4 W0 minimum shard load changed")
    if max(counts) != int(
        config["shards"]["maximum_scientific_runs_per_shard"]
    ):
        raise ValueError("S4 W0 maximum shard load changed")

    digest_plan = [
        {
            "shard_index": row["shard_index"],
            "scientific_run_count": row["scientific_run_count"],
            "imported_scientific_run_count": row[
                "imported_scientific_run_count"
            ],
            "new_scientific_run_count": row["new_scientific_run_count"],
            "imported_method_row_count": row["imported_method_row_count"],
            "new_method_execution_count": row[
                "new_method_execution_count"
            ],
        }
        for row in shard_plan
    ]
    if canonical_json_sha256(digest_plan) != str(
        config["shards"]["shard_plan_sha256"]
    ):
        raise ValueError("S4 W0 shard-plan digest changed")

    return {
        "gate_id": config["gate_id"],
        "status": "NON_AUTHORITATIVE_S4_W0_EXECUTION_PLAN_COMPLETE",
        "authoritative": False,
        "issue": int(config["issue"]),
        "wave_id": "W0",
        "scientific_run_count": 3750,
        "method_row_count": 15000,
        "imported_scientific_run_count": 840,
        "imported_method_row_count": 3360,
        "new_scientific_run_count": 2910,
        "new_method_execution_count": 11640,
        "scientific_run_ids_sha256": config["wave"][
            "scientific_run_ids_sha256"
        ],
        "method_row_ids_sha256": config["wave"][
            "method_row_ids_sha256"
        ],
        "imported_method_row_ids_sha256": config["wave"][
            "imported_method_row_ids_sha256"
        ],
        "new_method_row_ids_sha256": config["wave"][
            "new_method_row_ids_sha256"
        ],
        "shard_count": 250,
        "shard_plan_sha256": config["shards"]["shard_plan_sha256"],
        "shard_plan": shard_plan,
        "execution_authorized": True,
        "scientific_interpretation_authorized": False,
        "w1_authorized": False,
        "release_0_2_0_blocker_closed": False,
        "boundary": dict(config["boundary"]),
    }
