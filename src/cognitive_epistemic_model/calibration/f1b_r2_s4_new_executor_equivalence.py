from __future__ import annotations

import hashlib
import json
from typing import Any

from .f1b_r2_s4_broad_executor import (
    compare_new_row_to_retained_m2,
)


EQUIVALENCE_ID = "F1B.R2.S4.NEW_EXECUTOR_EQUIVALENCE.V1"
STATUS = "NON_AUTHORITATIVE_S4_NEW_EXECUTOR_EQUIVALENCE_DESIGN"
EXPECTED_METHODS = (
    "POPULATION",
    "HIERARCHICAL_0.5X",
    "HIERARCHICAL_1X",
    "HIERARCHICAL_2X",
)
EXPECTED_STATUSES = (
    "SEQUENTIAL_RESOLVED_AT_PREFIX",
    "SEQUENTIAL_RESOLVED",
    "SEQUENTIAL_UNRESOLVED_AT_CAP",
)
EXPECTED_SELECTION_SHA256 = (
    "41062e2bf501799a41b78d412b33551685045b98b9a67c9d50a9a26131c16b36"
)


def canonical_json_sha256(value: Any) -> str:
    payload = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def validate_equivalence_config(config: dict) -> None:
    if config["equivalence_id"] != EQUIVALENCE_ID:
        raise ValueError("S4 equivalence identity changed")
    if config["status"] != STATUS:
        raise ValueError("unsupported S4 equivalence status")
    if int(config["issue"]) != 259:
        raise ValueError("S4 equivalence issue changed")

    m2 = config["retained_sources"]["m2"]
    if int(m2["scientific_run_count"]) != 840:
        raise ValueError("S4 equivalence M2 scientific-run count changed")
    if int(m2["method_row_count"]) != 3360:
        raise ValueError("S4 equivalence M2 method-row count changed")

    selection = config["selection"]
    if tuple(selection["methods"]) != EXPECTED_METHODS:
        raise ValueError("S4 equivalence method set/order changed")
    if tuple(selection["statuses"]) != EXPECTED_STATUSES:
        raise ValueError("S4 equivalence status set/order changed")
    if selection["rule"] != (
        "LEXICOGRAPHICALLY_SMALLEST_SCIENTIFIC_RUN_ID_PER_METHOD_STATUS"
    ):
        raise ValueError("S4 equivalence selection rule changed")
    if int(selection["expected_row_count"]) != 12:
        raise ValueError("S4 equivalence row count changed")
    if int(selection["expected_unique_scientific_run_count"]) != 7:
        raise ValueError("S4 equivalence unique-run count changed")
    if selection["selected_row_identity_sha256"] != EXPECTED_SELECTION_SHA256:
        raise ValueError("S4 equivalence selection digest changed")

    lineage = config["numerical_lineage"]
    if lineage["environment_variable"] != "OPENBLAS_CORETYPE":
        raise ValueError("S4 equivalence environment variable changed")
    if lineage["required_value"] != "Haswell":
        raise ValueError("S4 equivalence OpenBLAS core changed")
    if lineage["must_be_set_before_python_start"] is not True:
        raise ValueError("S4 equivalence core must precede Python startup")
    if lineage["runtime_confirmation_required"] is not True:
        raise ValueError("S4 equivalence runtime confirmation weakened")
    if lineage["fallback_allowed"] is not False:
        raise ValueError("S4 equivalence environment fallback enabled")

    executor = config["executor_contract"]
    if int(executor["prefix_attempts"]) != 199:
        raise ValueError("S4 equivalence prefix length changed")
    if executor["stop_on_first_prefix_refit_failure"] is not True:
        raise ValueError("S4 equivalence prefix stop rule weakened")
    if executor["prefix_execution_failure_state"] != (
        "PREFIX_EXECUTION_FAILURE_UNRESOLVED"
    ):
        raise ValueError("S4 equivalence prefix execution state changed")
    if executor["prefix_refit_failure_state"] != (
        "BOOTSTRAP_REFIT_FAILURE_UNRESOLVED"
    ):
        raise ValueError("S4 equivalence prefix refit state changed")
    if executor["controller_id"] != "F1B.R2.RESAMPLING_RISK_CONTROLLER.V1":
        raise ValueError("S4 equivalence controller changed")
    if int(executor["first_new_draw_index"]) != 199:
        raise ValueError("S4 equivalence first new draw changed")
    if int(executor["maximum_total_attempts"]) != 10000:
        raise ValueError("S4 equivalence cap changed")
    if executor["exact_retained_m2_equality_required"] is not True:
        raise ValueError("S4 equivalence exact-equality requirement weakened")

    expected_fields = (
        "dataset_sha256",
        "inference_method",
        "bootstrap_base_seed",
        "prefix_attempt_sequence_sha256",
        "observed_statistic",
        "prefix_sum_199",
        "prefix_decision",
        "prefix_boundary_hit",
        "continued_beyond_199",
        "first_new_draw_index",
        "new_attempt_count",
        "new_successful_attempt_count",
        "new_refit_failure_count",
        "new_attempt_sequence_sha256",
        "status",
        "decision",
        "boundary_hit",
        "terminal_n",
        "terminal_sum",
        "failure_n",
    )
    if tuple(config["exact_equality_fields"]) != expected_fields:
        raise ValueError("S4 equivalence equality-field set changed")

    if config["release"]["release_blocker_closed"] is not False:
        raise ValueError("S4 equivalence cannot close v0.2.0 blocker")
    if any(bool(value) for value in config["boundary"].values()):
        raise ValueError("S4 equivalence boundary was weakened")


def select_equivalence_rows(
    m2_source: dict,
    config: dict,
) -> list[dict]:
    validate_equivalence_config(config)
    if m2_source["status"] != "NON_AUTHORITATIVE_PAIRED_METHOD_M2_COMBINED_RESULT":
        raise ValueError("S4 equivalence M2 source status changed")
    if m2_source["authoritative"] is not False:
        raise ValueError("S4 equivalence M2 source became authoritative")
    if int(m2_source["scientific_run_count"]) != 840:
        raise ValueError("S4 equivalence M2 source run count changed")
    if int(m2_source["method_execution_count"]) != 3360:
        raise ValueError("S4 equivalence M2 source row count changed")

    rows = list(m2_source["rows"])
    if len(rows) != 3360:
        raise ValueError("S4 equivalence M2 rows missing")
    keys = {
        (str(row["scientific_run_id"]), str(row["inference_method"]))
        for row in rows
    }
    if len(keys) != 3360:
        raise ValueError("S4 equivalence M2 row identities not unique")

    selected: list[dict] = []
    identity_strings: list[str] = []
    for method_id in EXPECTED_METHODS:
        for status in EXPECTED_STATUSES:
            candidates = [
                row
                for row in rows
                if str(row["inference_method"]) == method_id
                and str(row["status"]) == status
            ]
            if not candidates:
                raise ValueError(
                    f"S4 equivalence missing M2 status coverage: "
                    f"{method_id} / {status}"
                )
            row = min(
                candidates,
                key=lambda value: str(value["scientific_run_id"]),
            )
            selected.append(row)
            identity_strings.append(
                f"{method_id}|{status}|{row['scientific_run_id']}"
            )

    if len(selected) != 12:
        raise ValueError("S4 equivalence did not select exactly 12 rows")
    if len({str(row["scientific_run_id"]) for row in selected}) != 7:
        raise ValueError("S4 equivalence unique scientific-run count changed")
    digest = canonical_json_sha256(identity_strings)
    if digest != EXPECTED_SELECTION_SHA256:
        raise ValueError("S4 equivalence selected-row digest mismatch")
    return selected


def build_equivalence_result(
    *,
    selected_retained_rows: list[dict],
    reproduced_rows: list[dict],
    config: dict,
) -> dict:
    validate_equivalence_config(config)
    if len(selected_retained_rows) != 12 or len(reproduced_rows) != 12:
        raise ValueError("S4 equivalence requires exactly 12 row pairs")

    pairs = []
    for retained, reproduced in zip(
        selected_retained_rows,
        reproduced_rows,
        strict=True,
    ):
        compare_new_row_to_retained_m2(reproduced, retained)
        pairs.append(
            {
                "inference_method": str(retained["inference_method"]),
                "status": str(retained["status"]),
                "scientific_run_id": str(retained["scientific_run_id"]),
                "dataset_sha256": str(retained["dataset_sha256"]),
                "bootstrap_base_seed": int(retained["bootstrap_base_seed"]),
                "prefix_attempt_sequence_sha256": str(
                    retained["regenerated_m1_attempt_sequence_sha256"]
                ),
                "new_attempt_sequence_sha256": retained[
                    "new_attempt_sequence_sha256"
                ],
                "terminal_n": int(retained["terminal_n"]),
                "decision": retained["decision"],
                "boundary_hit": retained["boundary_hit"],
                "terminal_sum": int(retained["terminal_sum"]),
                "failure_n": retained["failure_n"],
                "exact_match": True,
            }
        )

    pair_identity_sha256 = canonical_json_sha256(
        [
            [
                row["inference_method"],
                row["status"],
                row["scientific_run_id"],
            ]
            for row in pairs
        ]
    )
    if pair_identity_sha256 != EXPECTED_SELECTION_SHA256:
        raise ValueError("S4 equivalence output selection digest changed")

    reproduced_evidence_sha256 = canonical_json_sha256(
        [
            {
                key: row[key]
                for key in (
                    "inference_method",
                    "status",
                    "scientific_run_id",
                    "dataset_sha256",
                    "bootstrap_base_seed",
                    "prefix_attempt_sequence_sha256",
                    "new_attempt_sequence_sha256",
                    "terminal_n",
                    "decision",
                    "boundary_hit",
                    "terminal_sum",
                    "failure_n",
                )
            }
            for row in pairs
        ]
    )

    return {
        "equivalence_id": config["equivalence_id"],
        "status": "NON_AUTHORITATIVE_S4_NEW_EXECUTOR_EQUIVALENCE_COMPLETE",
        "authoritative": False,
        "issue": int(config["issue"]),
        "selected_row_count": 12,
        "unique_scientific_run_count": 7,
        "selected_row_identity_sha256": pair_identity_sha256,
        "reproduced_evidence_sha256": reproduced_evidence_sha256,
        "exact_match_count": 12,
        "mismatch_count": 0,
        "pairs": pairs,
        "broad_executor_authorized_after_retention": True,
        "broad_execution_started": False,
        "scientific_interpretation_authorized": False,
        "release_0_2_0_blocker_closed": False,
        "boundary": dict(config["boundary"]),
    }
