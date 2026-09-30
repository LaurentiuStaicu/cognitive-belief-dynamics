from __future__ import annotations

from collections import Counter
import hashlib
import json
from typing import Any

from .f1b_r2_paired_method_m2_sequential_resolution import (
    EXPECTED_METHODS_M2,
    stable_shard,
)


GATE_ID = "F1B.R2.S4.ALL_NEW_WAVE.EXECUTION_GATE.V1"
STATUS = "NON_AUTHORITATIVE_S4_ALL_NEW_WAVE_EXECUTION_DESIGN"

EXPECTED_WAVES = {
    "W1": {
        "predecessor_wave_id": "W0",
        "predecessor_status": "NON_AUTHORITATIVE_S4_W0_COMBINED_COMPLETE_RETAINED",
        "replicate_start": 25,
        "replicate_end": 49,
        "scientific_run_ids_sha256": (
            "42a1803705c0c4f7efbfae0983a7c57f20036c76cd933c99af3fcd4e3cd9087c"
        ),
        "method_row_ids_sha256": (
            "2191e0aceb072c20bca90dab1b6db3ed8bffef997bf2ead8ec2ace2ac4a81957"
        ),
        "shard_plan_sha256": (
            "36d294a165ec1e8a8baffac70516ce7fceab149998079b534998503f3f578175"
        ),
        "shard_range": (5, 27),
    },
    "W2": {
        "predecessor_wave_id": "W1",
        "predecessor_status": "NON_AUTHORITATIVE_S4_W1_COMBINED_COMPLETE_RETAINED",
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
        "shard_range": (6, 27),
    },
    "W3": {
        "predecessor_wave_id": "W2",
        "predecessor_status": "NON_AUTHORITATIVE_S4_W2_COMBINED_COMPLETE_RETAINED",
        "replicate_start": 75,
        "replicate_end": 99,
        "scientific_run_ids_sha256": (
            "e0b7126a2342a65427a03f1a45d42990093e89f2c3ab0eeb661544b5548ff3ce"
        ),
        "method_row_ids_sha256": (
            "81ed9d1c0ea527da9d1501c5652e529e87f50e73c7eb3a2b876fad0d02393998"
        ),
        "shard_plan_sha256": (
            "d27bce0c8c17022644bcaaa6f0bb4b2be19239cf8074ab54ae75c982feb058e2"
        ),
        "shard_range": (4, 27),
    },
}

EXPECTED_RETAINED_PREDECESSORS = {
    "W1": {
        "path": "model/results/f1b_r2_s4_w0_combined_2026-09-29.json",
        "git_blob_sha": "d8aa5b48a91b6242c3a0d4455c4d2278c30642e1",
    },
    "W2": {
        "path": "model/results/f1b_r2_s4_w1_combined_2026-09-30.json",
        "git_blob_sha": "7302806c2630b8d24a84f20885a543274badcd33",
    },
}


def canonical_json_sha256(value: Any) -> str:
    payload = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def method_row_id(scientific_run_id: str, method_id: str) -> str:
    return f"{scientific_run_id}|METHOD={method_id}"


def combined_status(wave_id: str) -> str:
    wave = str(wave_id)
    if wave not in EXPECTED_WAVES:
        raise ValueError("unsupported S4 all-new wave")
    return f"NON_AUTHORITATIVE_S4_{wave}_COMBINED_COMPLETE"


def shard_status(wave_id: str) -> str:
    wave = str(wave_id)
    if wave not in EXPECTED_WAVES:
        raise ValueError("unsupported S4 all-new wave")
    return f"NON_AUTHORITATIVE_S4_{wave}_SHARD_COMPLETE"


def plan_status(wave_id: str) -> str:
    wave = str(wave_id)
    if wave not in EXPECTED_WAVES:
        raise ValueError("unsupported S4 all-new wave")
    return f"NON_AUTHORITATIVE_S4_{wave}_EXECUTION_PLAN_COMPLETE"


def validate_all_new_wave_config(config: dict) -> None:
    if config["gate_id"] != GATE_ID:
        raise ValueError("S4 all-new-wave gate identity changed")
    if config["status"] != STATUS:
        raise ValueError("unsupported S4 all-new-wave status")
    if int(config["issue"]) != 259:
        raise ValueError("S4 all-new-wave issue changed")

    wave = config["wave"]
    wave_id = str(wave["wave_id"])
    if wave_id not in EXPECTED_WAVES:
        raise ValueError("unsupported S4 all-new wave")
    expected = EXPECTED_WAVES[wave_id]

    if str(wave["predecessor_wave_id"]) != expected["predecessor_wave_id"]:
        raise ValueError("S4 all-new-wave predecessor changed")
    if int(wave["replicate_start"]) != expected["replicate_start"]:
        raise ValueError("S4 all-new-wave replicate_start changed")
    if int(wave["replicate_end"]) != expected["replicate_end"]:
        raise ValueError("S4 all-new-wave replicate_end changed")
    if int(wave["scientific_run_count"]) != 3750:
        raise ValueError("S4 all-new-wave scientific-run count changed")
    if int(wave["method_row_count"]) != 15000:
        raise ValueError("S4 all-new-wave method-row count changed")
    if int(wave["imported_scientific_run_count"]) != 0:
        raise ValueError("S4 all-new-wave cannot import scientific runs")
    if int(wave["imported_method_row_count"]) != 0:
        raise ValueError("S4 all-new-wave cannot import method rows")
    if int(wave["new_scientific_run_count"]) != 3750:
        raise ValueError("S4 all-new-wave new scientific count changed")
    if int(wave["new_method_execution_count"]) != 15000:
        raise ValueError("S4 all-new-wave new method count changed")
    if str(wave["scientific_run_ids_sha256"]) != expected[
        "scientific_run_ids_sha256"
    ]:
        raise ValueError("S4 all-new-wave scientific identity changed")
    if str(wave["method_row_ids_sha256"]) != expected[
        "method_row_ids_sha256"
    ]:
        raise ValueError("S4 all-new-wave method identity changed")
    if str(wave["shard_plan_sha256"]) != expected["shard_plan_sha256"]:
        raise ValueError("S4 all-new-wave shard-plan identity changed")

    if tuple(config["methods"]) != tuple(EXPECTED_METHODS_M2):
        raise ValueError("S4 all-new-wave method order/set changed")

    shards = config["shards"]
    if int(shards["shard_count"]) != 250:
        raise ValueError("S4 all-new-wave shard count changed")
    if shards["assignment_algorithm"] != (
        "SHA256_FIRST_8_BYTES_BIG_ENDIAN_MODULO"
    ):
        raise ValueError("S4 all-new-wave shard algorithm changed")
    if (
        int(shards["minimum_scientific_runs_per_shard"]),
        int(shards["maximum_scientific_runs_per_shard"]),
    ) != expected["shard_range"]:
        raise ValueError("S4 all-new-wave shard range changed")
    if shards["fail_fast"] is not False:
        raise ValueError("S4 all-new-wave fail-fast policy changed")
    if int(shards["max_parallel"]) != 20:
        raise ValueError("S4 all-new-wave max-parallel changed")
    if shards["all_four_methods_same_scientific_run_same_shard"] is not True:
        raise ValueError("S4 all-new-wave pairing weakened")

    execution = config["execution"]
    if execution["imports_forbidden"] is not True:
        raise ValueError("S4 all-new-wave imports must remain forbidden")
    if execution["evidence_origin"] != "S4_NEW_EXECUTION":
        raise ValueError("S4 all-new-wave evidence origin changed")
    if execution["new_rows_use_shared_broad_executor"] is not True:
        raise ValueError("S4 all-new-wave shared executor binding weakened")
    if execution["numerical_lineage"] != "Haswell":
        raise ValueError("S4 all-new-wave numerical lineage changed")
    if int(execution["sequential_prefix_attempts"]) != 199:
        raise ValueError("S4 all-new-wave prefix length changed")
    if int(execution["sequential_max_total_attempts"]) != 10000:
        raise ValueError("S4 all-new-wave sequential cap changed")
    if execution["stop_on_first_refit_failure"] is not True:
        raise ValueError("S4 all-new-wave refit rule changed")
    if execution["scientific_interpretation_after_wave"] is not False:
        raise ValueError("S4 all-new-wave cannot authorize interpretation")

    predecessor = config["retained_sources"]["predecessor_result"]
    if str(predecessor["wave_id"]) != expected["predecessor_wave_id"]:
        raise ValueError("S4 all-new-wave retained predecessor changed")
    if str(predecessor["required_status"]) != expected["predecessor_status"]:
        raise ValueError("S4 all-new-wave retained predecessor status changed")
    if wave_id == "W3":
        raise ValueError("S4 W3 execution requires a retained W2 predecessor config")
    expected_predecessor = EXPECTED_RETAINED_PREDECESSORS[wave_id]
    if str(predecessor.get("path")) != expected_predecessor["path"]:
        raise ValueError("S4 all-new-wave retained predecessor path changed")
    if str(predecessor.get("git_blob_sha")) != expected_predecessor["git_blob_sha"]:
        raise ValueError("S4 all-new-wave retained predecessor blob changed")
    if predecessor["next_wave_authorized_after_retention"] is not True:
        raise ValueError("S4 all-new-wave predecessor authorization changed")

    authorization = config["authorization"]
    if authorization["predecessor_retained"] is not True:
        raise ValueError("S4 all-new-wave predecessor is not retained")
    if authorization["wave_execution_authorized"] is not True:
        raise ValueError("S4 all-new-wave is not authorized")

    if wave_id == "W1":
        if authorization["full_wave_requires_preflight_retention"] is not True:
            raise ValueError("S4 W1 preflight gate weakened")
        preflight_retained = bool(authorization["preflight_retained"])
        full_wave_authorized = bool(
            authorization["full_wave_execution_authorized"]
        )
        if full_wave_authorized != preflight_retained:
            raise ValueError(
                "S4 W1 full-wave authorization must match retained preflight"
            )
        if authorization["w2_authorized"] is not False:
            raise ValueError("S4 W1 cannot authorize W2 before retention")
        if authorization["w3_authorized"] is not False:
            raise ValueError("S4 W1 cannot authorize W3")
    elif wave_id == "W2":
        if "preflight" in config:
            raise ValueError("S4 W2 must not depend on a W1-style preflight")
        if "preflight_result" in config["retained_sources"]:
            raise ValueError("S4 W2 must not retain a W1 preflight dependency")
        if authorization["full_wave_requires_preflight_retention"] is not False:
            raise ValueError("S4 W2 must not require a new preflight")
        if authorization["preflight_retained"] is not False:
            raise ValueError("S4 W2 preflight flag must remain false")
        if authorization["full_wave_execution_authorized"] is not True:
            raise ValueError("S4 W2 full-wave execution is not authorized")
        if authorization["w2_authorized"] is not True:
            raise ValueError("S4 W2 authorization flag is not retained")
        if authorization["w3_authorized"] is not False:
            raise ValueError("S4 W2 cannot authorize W3 before retention")

    combine = config["wave_combine"]
    if int(combine["exact_scientific_run_count"]) != 3750:
        raise ValueError("S4 all-new-wave combine scientific count changed")
    if int(combine["exact_method_row_count"]) != 15000:
        raise ValueError("S4 all-new-wave combine method count changed")
    if int(combine["exact_imported_method_row_count"]) != 0:
        raise ValueError("S4 all-new-wave combine imports changed")
    if int(combine["exact_new_method_row_count"]) != 15000:
        raise ValueError("S4 all-new-wave combine new-row count changed")
    if combine["retain_unresolved_in_denominators"] is not True:
        raise ValueError("S4 all-new-wave unresolved denominator weakened")
    if combine["retain_refit_failures_in_denominators"] is not True:
        raise ValueError("S4 all-new-wave failure denominator weakened")
    if combine["method_selection_forbidden"] is not True:
        raise ValueError("S4 all-new-wave cannot select a method")
    if combine["next_wave_authorization_after_retention"] is not True:
        raise ValueError("S4 all-new-wave sequencing weakened")

    if config["release"]["release_blocker_closed"] is not False:
        raise ValueError("S4 all-new-wave cannot close v0.2.0 blocker")

    boundary = config["boundary"]
    if wave_id == "W1":
        if any(bool(value) for value in boundary.values()):
            raise ValueError("S4 all-new-wave boundary was weakened")
    elif wave_id == "W2":
        if boundary["full_w1_executed"] is not True:
            raise ValueError("S4 W2 predecessor completion was not retained")
        if boundary["w2_authorized"] is not True:
            raise ValueError("S4 W2 boundary authorization is missing")
        forbidden = (
            "w2_executed",
            "w3_authorized",
            "w3_executed",
            "scientific_interpretation_authorized",
            "method_selected",
            "scale_selected",
            "power_validated",
            "human_n_frozen",
            "participant_recruitment_allowed",
            "runtime_f1b_change_allowed",
            "version_bumped",
        )
        if any(bool(boundary[key]) for key in forbidden):
            raise ValueError("S4 W2 boundary was weakened")


def build_all_new_wave_plan(s4_manifest: dict, config: dict) -> dict:
    validate_all_new_wave_config(config)

    if s4_manifest["status"] != (
        "NON_AUTHORITATIVE_S4_BROAD_SCIENTIFIC_MATRIX_MANIFEST"
    ):
        raise ValueError("S4 all-new-wave raw manifest status changed")
    if int(s4_manifest["scientific_run_count"]) != 15000:
        raise ValueError("S4 all-new-wave raw manifest count changed")

    wave = config["wave"]
    wave_id = str(wave["wave_id"])
    start = int(wave["replicate_start"])
    end = int(wave["replicate_end"])

    rows = [
        row
        for row in s4_manifest["rows"]
        if start <= int(row["evaluation_replicate"]) <= end
    ]
    if len(rows) != 3750:
        raise ValueError("S4 all-new-wave selection is not 3,750 runs")

    run_ids = sorted(str(row["scientific_run_id"]) for row in rows)
    if len(set(run_ids)) != 3750:
        raise ValueError("S4 all-new-wave run identities are not unique")
    if canonical_json_sha256(run_ids) != str(
        wave["scientific_run_ids_sha256"]
    ):
        raise ValueError("S4 all-new-wave run-ID digest changed")

    method_ids = sorted(
        method_row_id(run_id, method)
        for run_id in run_ids
        for method in EXPECTED_METHODS_M2
    )
    if len(method_ids) != 15000:
        raise ValueError("S4 all-new-wave method identity count changed")
    if canonical_json_sha256(method_ids) != str(
        wave["method_row_ids_sha256"]
    ):
        raise ValueError("S4 all-new-wave method-row digest changed")

    shard_plan = []
    for shard_index in range(250):
        shard_rows = [
            row
            for row in rows
            if stable_shard(str(row["scientific_run_id"]), 250)
            == shard_index
        ]
        if not shard_rows:
            raise ValueError("S4 all-new-wave contains an empty shard")
        shard_run_ids = sorted(
            str(row["scientific_run_id"]) for row in shard_rows
        )
        shard_method_ids = sorted(
            method_row_id(run_id, method)
            for run_id in shard_run_ids
            for method in EXPECTED_METHODS_M2
        )
        shard_plan.append(
            {
                "shard_index": shard_index,
                "scientific_run_count": len(shard_rows),
                "imported_scientific_run_count": 0,
                "new_scientific_run_count": len(shard_rows),
                "imported_method_row_count": 0,
                "new_method_execution_count": len(shard_rows) * 4,
                "scientific_run_ids_sha256": canonical_json_sha256(
                    shard_run_ids
                ),
                "method_row_ids_sha256": canonical_json_sha256(
                    shard_method_ids
                ),
            }
        )

    counts = [row["scientific_run_count"] for row in shard_plan]
    expected_range = EXPECTED_WAVES[wave_id]["shard_range"]
    if (min(counts), max(counts)) != expected_range:
        raise ValueError("S4 all-new-wave shard load range changed")

    digest_plan = [
        {
            "shard_index": row["shard_index"],
            "scientific_run_count": row["scientific_run_count"],
            "imported_scientific_run_count": 0,
            "new_scientific_run_count": row["new_scientific_run_count"],
            "imported_method_row_count": 0,
            "new_method_execution_count": row[
                "new_method_execution_count"
            ],
        }
        for row in shard_plan
    ]
    if canonical_json_sha256(digest_plan) != str(
        wave["shard_plan_sha256"]
    ):
        raise ValueError("S4 all-new-wave shard-plan digest changed")

    preflight_output: dict[str, Any] = {}
    if wave_id == "W1":
        preflight = config["preflight"]
        selected = shard_plan[int(preflight["shard_index"])]
        for key in (
            "scientific_run_count",
            "new_scientific_run_count",
            "new_method_execution_count",
            "scientific_run_ids_sha256",
            "method_row_ids_sha256",
        ):
            if selected[key] != preflight[key]:
                raise ValueError(f"S4 W1 preflight identity changed: {key}")
        preflight_output = {
            "preflight_shard_index": int(preflight["shard_index"]),
            "preflight_retained": bool(
                config["authorization"]["preflight_retained"]
            ),
        }

    result = {
        "gate_id": config["gate_id"],
        "status": plan_status(wave_id),
        "authoritative": False,
        "issue": int(config["issue"]),
        "wave_id": wave_id,
        "replicate_start": start,
        "replicate_end": end,
        "scientific_run_count": 3750,
        "method_row_count": 15000,
        "imported_scientific_run_count": 0,
        "imported_method_row_count": 0,
        "new_scientific_run_count": 3750,
        "new_method_execution_count": 15000,
        "scientific_run_ids_sha256": canonical_json_sha256(run_ids),
        "method_row_ids_sha256": canonical_json_sha256(method_ids),
        "shard_count": 250,
        "shard_plan_sha256": canonical_json_sha256(digest_plan),
        "shard_plan": shard_plan,
        "full_wave_execution_authorized": bool(
            config["authorization"]["full_wave_execution_authorized"]
        ),
        "scientific_interpretation_authorized": False,
        "method_selected": False,
        "power_validated": False,
        "release_0_2_0_blocker_closed": False,
    }
    result.update(preflight_output)
    return result
