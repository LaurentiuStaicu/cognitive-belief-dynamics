from __future__ import annotations

from collections import Counter
import hashlib
import json
from typing import Any


BRIDGE_ID = "F1B.R2.S4.M2_PREFIX_BRIDGE.V1"
STATUS = "NON_AUTHORITATIVE_S4_M2_PREFIX_BRIDGE_DESIGN"
EXPECTED_METHODS = (
    "POPULATION",
    "HIERARCHICAL_0.5X",
    "HIERARCHICAL_1X",
    "HIERARCHICAL_2X",
)
ALLOWED_M2_STATUSES = {
    "SEQUENTIAL_RESOLVED_AT_PREFIX",
    "SEQUENTIAL_RESOLVED",
    "SEQUENTIAL_UNRESOLVED_AT_CAP",
}


def canonical_json_sha256(value: Any) -> str:
    payload = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def validate_prefix_bridge_config(config: dict) -> None:
    if config["bridge_id"] != BRIDGE_ID:
        raise ValueError("S4 M2 prefix-bridge identity changed")
    if config["status"] != STATUS:
        raise ValueError("unsupported S4 M2 prefix-bridge status")
    if int(config["issue"]) != 259:
        raise ValueError("S4 M2 prefix-bridge issue changed")

    m1 = config["m1_source"]
    m2 = config["m2_source"]
    s4 = config["s4_matrix_source"]
    overlap = config["overlap"]
    broad = config["broad_consequence"]

    if int(m1["scientific_run_count"]) != 840:
        raise ValueError("M1 prefix scientific-run count changed")
    if int(m1["method_row_count"]) != 3360:
        raise ValueError("M1 prefix method-row count changed")
    if int(m1["prefix_attempts"]) != 199:
        raise ValueError("M1 prefix length changed")

    if int(m2["scientific_run_count"]) != 840:
        raise ValueError("M2 prefix scientific-run count changed")
    if int(m2["method_row_count"]) != 3360:
        raise ValueError("M2 prefix method-row count changed")
    if tuple(str(x) for x in m2["eligible_methods"]) != EXPECTED_METHODS:
        raise ValueError("M2 eligible-method order/set changed")

    if int(s4["scientific_run_count"]) != 15000:
        raise ValueError("S4 scientific-run count changed")

    if int(overlap["expected_scientific_run_count"]) != 840:
        raise ValueError("prefix overlap scientific-run count changed")
    if int(overlap["expected_method_row_count"]) != 3360:
        raise ValueError("prefix overlap method-row count changed")
    if tuple(int(x) for x in overlap["departure_replicate_indices"]) != tuple(
        range(5)
    ):
        raise ValueError("departure prefix replicate identity changed")
    if tuple(int(x) for x in overlap["null_replicate_indices"]) != tuple(
        range(20)
    ):
        raise ValueError("null prefix replicate identity changed")
    if int(overlap["expected_departure_scientific_runs"]) != 720:
        raise ValueError("departure prefix run count changed")
    if int(overlap["expected_null_scientific_runs"]) != 120:
        raise ValueError("null prefix run count changed")
    if overlap["expected_status_counts"] != {
        "SEQUENTIAL_RESOLVED_AT_PREFIX": 2402,
        "SEQUENTIAL_RESOLVED": 834,
        "SEQUENTIAL_UNRESOLVED_AT_CAP": 124,
        "BOOTSTRAP_REFIT_FAILURE_UNRESOLVED": 0,
    }:
        raise ValueError("M2 prefix status-count contract changed")

    if int(broad["total_scientific_runs"]) != 15000:
        raise ValueError("broad scientific-run count changed")
    if int(broad["total_method_rows"]) != 60000:
        raise ValueError("broad method-row count changed")
    if int(broad["imported_scientific_runs_if_bridge_passes"]) != 840:
        raise ValueError("imported scientific-run count changed")
    if int(broad["imported_method_rows_if_bridge_passes"]) != 3360:
        raise ValueError("imported method-row count changed")
    if int(broad["new_scientific_runs_if_bridge_passes"]) != 14160:
        raise ValueError("new scientific-run count changed")
    if int(broad["new_method_executions_if_bridge_passes"]) != 56640:
        raise ValueError("new method-execution count changed")
    if (
        int(broad["wave0_new_method_executions"])
        + int(broad["wave1_new_method_executions"])
        + int(broad["wave2_new_method_executions"])
        + int(broad["wave3_new_method_executions"])
        != 56640
    ):
        raise ValueError("wave execution totals do not sum to broad remainder")

    for key, value in config["import_rules"].items():
        if key == "failed_bridge_row_recomputed_not_dropped":
            if value is not True:
                raise ValueError("failed bridge rows must be recomputed")
        elif value is not True:
            raise ValueError(f"prefix import rule weakened: {key}")

    if any(bool(value) for value in config["boundary"].values()):
        raise ValueError("S4 M2 prefix-bridge boundary was weakened")


def _method_map(rows: list[dict], label: str) -> dict[tuple[str, str], dict]:
    result = {
        (str(row["scientific_run_id"]), str(row["inference_method"])): row
        for row in rows
    }
    if len(result) != len(rows):
        raise ValueError(f"{label} method-row identities are not unique")
    return result


def build_prefix_bridge_manifest(
    *,
    m1_source: dict,
    m2_source: dict,
    s4_manifest: dict,
    config: dict,
    regenerated_dataset_sha256: dict[str, str],
    expected_bootstrap_seed: dict[str, int],
) -> dict:
    validate_prefix_bridge_config(config)

    if m1_source["status"] != "NON_AUTHORITATIVE_PAIRED_METHOD_M1_SCREEN_RESULT":
        raise ValueError("raw M1 source status changed")
    if m2_source["status"] != "NON_AUTHORITATIVE_PAIRED_METHOD_M2_COMBINED_RESULT":
        raise ValueError("raw M2 source status changed")
    if s4_manifest["status"] != (
        "NON_AUTHORITATIVE_S4_BROAD_SCIENTIFIC_MATRIX_MANIFEST"
    ):
        raise ValueError("raw S4 manifest status changed")
    if any(bool(x["authoritative"]) for x in (m1_source, m2_source, s4_manifest)):
        raise ValueError("prefix bridge source unexpectedly authoritative")

    if tuple(str(x) for x in m1_source["eligible_methods"]) != EXPECTED_METHODS:
        raise ValueError("raw M1 eligible-method order/set changed")
    if tuple(str(x) for x in m2_source["eligible_methods"]) != EXPECTED_METHODS:
        raise ValueError("raw M2 eligible-method order/set changed")
    if m2_source["overall_decision"] != "M2_HAS_ELIGIBLE_METHODS":
        raise ValueError("raw M2 overall decision changed")

    if int(m1_source["scientific_run_count"]) != 840:
        raise ValueError("raw M1 scientific-run count changed")
    if int(m1_source["method_execution_count"]) != 3360:
        raise ValueError("raw M1 method-row count changed")
    if int(m2_source["scientific_run_count"]) != 840:
        raise ValueError("raw M2 scientific-run count changed")
    if int(m2_source["method_execution_count"]) != 3360:
        raise ValueError("raw M2 method-row count changed")
    if int(s4_manifest["scientific_run_count"]) != 15000:
        raise ValueError("raw S4 scientific-run count changed")

    m1_map = _method_map(list(m1_source["rows"]), "M1")
    m2_map = _method_map(list(m2_source["rows"]), "M2")
    if set(m1_map) != set(m2_map):
        raise ValueError("M1 and M2 method-row identities differ")
    if len(m2_map) != 3360:
        raise ValueError("prefix bridge does not contain 3360 method rows")

    s4_map = {
        str(row["scientific_run_id"]): row
        for row in s4_manifest["rows"]
    }
    if len(s4_map) != 15000:
        raise ValueError("S4 scientific-run identities are not unique")

    m2_scientific_ids = sorted({key[0] for key in m2_map})
    if len(m2_scientific_ids) != 840:
        raise ValueError("M2 prefix scientific-run identity count changed")
    if not set(m2_scientific_ids).issubset(s4_map):
        raise ValueError("M2 prefix is not an exact subset of S4 matrix")
    if set(regenerated_dataset_sha256) != set(m2_scientific_ids):
        raise ValueError("regenerated dataset fingerprint coverage changed")
    if set(expected_bootstrap_seed) != set(m2_scientific_ids):
        raise ValueError("expected bootstrap-seed coverage changed")

    status_counts = Counter()
    departure_ids: set[str] = set()
    null_ids: set[str] = set()
    imported_method_ids: list[str] = []

    for scientific_run_id in m2_scientific_ids:
        s4_row = s4_map[scientific_run_id]
        method_rows = [
            m2_map[(scientific_run_id, method_id)]
            for method_id in EXPECTED_METHODS
        ]
        if len({str(row["dataset_sha256"]) for row in method_rows}) != 1:
            raise ValueError("paired M2 methods saw different dataset hashes")
        actual_dataset_sha = str(method_rows[0]["dataset_sha256"])
        if actual_dataset_sha != str(
            regenerated_dataset_sha256[scientific_run_id]
        ):
            raise ValueError("deterministic regenerated dataset SHA mismatch")

        for method_id, m2_row in zip(
            EXPECTED_METHODS,
            method_rows,
            strict=True,
        ):
            m1_row = m1_map[(scientific_run_id, method_id)]

            shared_fields = (
                "dataset_id",
                "dataset_sha256",
                "identity",
                "identity_type",
                "restriction",
                "role",
                "anchor_id",
                "axis",
                "sign",
                "target_mean_bernoulli_kl",
                "evaluation_replicate",
                "observed_statistic",
                "bootstrap_base_seed",
            )
            for field in shared_fields:
                if m2_row[field] != m1_row[field]:
                    raise ValueError(f"M1/M2 prefix field mismatch: {field}")

            if float(m2_row["missingness_rate"]) != float(
                m1_row["missingness_rate"]
            ):
                raise ValueError("M1/M2 missingness mismatch")
            if int(m2_row["bootstrap_base_seed"]) != int(
                expected_bootstrap_seed[scientific_run_id]
            ):
                raise ValueError("deterministic bootstrap base seed mismatch")
            if str(m2_row["retained_m1_attempt_sequence_sha256"]) != str(
                m1_row["bootstrap_attempt_sequence_sha256"]
            ):
                raise ValueError("M1/M2 attempt-sequence digest mismatch")
            if str(m2_row["regenerated_m1_attempt_sequence_sha256"]) != str(
                m1_row["bootstrap_attempt_sequence_sha256"]
            ):
                raise ValueError("M2 regenerated M1 prefix digest mismatch")
            if m2_row["m1_prefix_exact"] is not True:
                raise ValueError("M2 prefix exactness changed")
            if int(m2_row["new_refit_failure_count"]) != 0:
                raise ValueError("M2 prefix row contains new refit failure")

            status = str(m2_row["status"])
            if status not in ALLOWED_M2_STATUSES:
                raise ValueError(f"unsupported import terminal status: {status}")
            status_counts[status] += 1

            if status == "SEQUENTIAL_UNRESOLVED_AT_CAP":
                if m2_row["decision"] is not None:
                    raise ValueError("unresolved-at-cap row has a decision")
                if int(m2_row["terminal_n"]) != 10000:
                    raise ValueError("unresolved-at-cap row did not reach cap")
            else:
                if m2_row["decision"] not in (
                    "REJECT_P_LE_ALPHA",
                    "NOT_REJECT_P_GT_ALPHA",
                ):
                    raise ValueError("resolved M2 row lacks valid decision")
                if not 199 <= int(m2_row["terminal_n"]) <= 10000:
                    raise ValueError("resolved M2 terminal n outside controller")

            if str(s4_row["dataset_id"]) != str(m2_row["dataset_id"]):
                raise ValueError("S4/M2 dataset identity mismatch")
            compare_fields = (
                "identity",
                "identity_type",
                "restriction",
                "role",
                "anchor_id",
                "axis",
                "sign",
                "target_mean_bernoulli_kl",
                "evaluation_replicate",
            )
            for field in compare_fields:
                if s4_row[field] != m2_row[field]:
                    raise ValueError(f"S4/M2 field mismatch: {field}")
            if float(s4_row["missingness"]) != float(
                m2_row["missingness_rate"]
            ):
                raise ValueError("S4/M2 missingness mismatch")

            imported_method_ids.append(
                f"{scientific_run_id}|METHOD={method_id}"
            )

        if method_rows[0]["identity_type"] == "DEPARTURE":
            departure_ids.add(scientific_run_id)
        elif method_rows[0]["identity_type"] == "NULL":
            null_ids.add(scientific_run_id)
        else:
            raise ValueError("unsupported prefix identity type")

    expected_status = dict(config["overlap"]["expected_status_counts"])
    actual_status = {
        "SEQUENTIAL_RESOLVED_AT_PREFIX": status_counts[
            "SEQUENTIAL_RESOLVED_AT_PREFIX"
        ],
        "SEQUENTIAL_RESOLVED": status_counts["SEQUENTIAL_RESOLVED"],
        "SEQUENTIAL_UNRESOLVED_AT_CAP": status_counts[
            "SEQUENTIAL_UNRESOLVED_AT_CAP"
        ],
        "BOOTSTRAP_REFIT_FAILURE_UNRESOLVED": 0,
    }
    if actual_status != expected_status:
        raise ValueError("M2 import terminal status counts changed")

    if len(departure_ids) != 720:
        raise ValueError("departure prefix overlap count changed")
    if len(null_ids) != 120:
        raise ValueError("null prefix overlap count changed")

    departure_replicates = {
        int(m2_map[(run_id, EXPECTED_METHODS[0])]["evaluation_replicate"])
        for run_id in departure_ids
    }
    null_replicates = {
        int(m2_map[(run_id, EXPECTED_METHODS[0])]["evaluation_replicate"])
        for run_id in null_ids
    }
    if departure_replicates != set(range(5)):
        raise ValueError("departure prefix replicate set changed")
    if null_replicates != set(range(20)):
        raise ValueError("null prefix replicate set changed")

    return {
        "bridge_id": config["bridge_id"],
        "status": "NON_AUTHORITATIVE_S4_M2_PREFIX_BRIDGE_COMPLETE",
        "authoritative": False,
        "issue": int(config["issue"]),
        "imported_scientific_run_count": len(m2_scientific_ids),
        "imported_method_row_count": len(imported_method_ids),
        "imported_departure_scientific_run_count": len(departure_ids),
        "imported_null_scientific_run_count": len(null_ids),
        "imported_scientific_run_ids_sha256": canonical_json_sha256(
            m2_scientific_ids
        ),
        "imported_method_row_ids_sha256": canonical_json_sha256(
            sorted(imported_method_ids)
        ),
        "terminal_status_counts": actual_status,
        "new_scientific_run_count": int(
            config["broad_consequence"][
                "new_scientific_runs_if_bridge_passes"
            ]
        ),
        "new_method_execution_count": int(
            config["broad_consequence"][
                "new_method_executions_if_bridge_passes"
            ]
        ),
        "wave0_new_method_executions": int(
            config["broad_consequence"]["wave0_new_method_executions"]
        ),
        "wave1_new_method_executions": int(
            config["broad_consequence"]["wave1_new_method_executions"]
        ),
        "wave2_new_method_executions": int(
            config["broad_consequence"]["wave2_new_method_executions"]
        ),
        "wave3_new_method_executions": int(
            config["broad_consequence"]["wave3_new_method_executions"]
        ),
        "prefix_import_authorized": True,
        "broad_estimand_changed": False,
        "method_selected": False,
        "power_validated": False,
        "boundary": dict(config["boundary"]),
    }
