from __future__ import annotations

import hashlib
import json
from typing import Any


PREFLIGHT_ID = "F1B.R2.S4.FRESH_REPLICATE_PREFLIGHT.V1"
STATUS = "NON_AUTHORITATIVE_S4_FRESH_REPLICATE_PREFLIGHT_DESIGN"
EXPECTED_METHODS = (
    "POPULATION",
    "HIERARCHICAL_0.5X",
    "HIERARCHICAL_1X",
    "HIERARCHICAL_2X",
)
EXPECTED_ROLES = (
    "ADD_DEPARTURE_DIAGNOSTIC",
    "ADD_NULL_FALSE_REJECTION",
    "ADD_SPECIFICITY_NEGATIVE_CONTROL",
    "CBD_DEPARTURE_DETECTION",
    "CBD_NULL_FALSE_REJECTION",
)
EXPECTED_NULL_IDENTITIES = (
    "ADD_NULL",
    "CBD_NULL_ANCHOR_1",
    "CBD_NULL_ANCHOR_2",
)
EXPECTED_RUN_DIGEST = (
    "d55ce620877a7b64a8ce37312025756482ff287456b62811f6a5b8249197666e"
)
EXPECTED_METHOD_DIGEST = (
    "be00d6689e29d5af959baa747a72254f449ec4d4dd20cd070460dac71f7a0a21"
)
EXPECTED_TERMINAL_STATES = (
    "SEQUENTIAL_RESOLVED_AT_PREFIX",
    "SEQUENTIAL_RESOLVED",
    "SEQUENTIAL_UNRESOLVED_AT_CAP",
    "BOOTSTRAP_REFIT_FAILURE_UNRESOLVED",
    "PREFIX_EXECUTION_FAILURE_UNRESOLVED",
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


def validate_preflight_config(config: dict) -> None:
    if config["preflight_id"] != PREFLIGHT_ID:
        raise ValueError("S4 fresh-preflight identity changed")
    if config["status"] != STATUS:
        raise ValueError("unsupported S4 fresh-preflight status")
    if int(config["issue"]) != 259:
        raise ValueError("S4 fresh-preflight issue changed")

    prerequisite = config["prerequisite"]
    if prerequisite["retained_executor_equivalence_required_before_execution"] is not True:
        raise ValueError("S4 preflight equivalence prerequisite weakened")
    if int(prerequisite["exact_equivalence_row_count"]) != 12:
        raise ValueError("S4 preflight equivalence row count changed")
    if int(prerequisite["exact_equivalence_match_count"]) != 12:
        raise ValueError("S4 preflight equivalence match count changed")
    if prerequisite["broad_executor_authorized_required"] is not True:
        raise ValueError("S4 preflight executor authorization weakened")
    if prerequisite["preflight_execution_before_equivalence_retention"] is not False:
        raise ValueError("S4 preflight cannot run before equivalence retention")

    equivalence = config["retained_sources"]["executor_equivalence"]
    if int(equivalence["exact_match_count"]) != 12:
        raise ValueError("S4 retained equivalence match count changed")
    if int(equivalence["mismatch_count"]) != 0:
        raise ValueError("S4 retained equivalence mismatch count changed")
    if equivalence["broad_executor_authorized"] is not True:
        raise ValueError("S4 retained equivalence authorization changed")
    if equivalence["selected_row_identity_sha256"] != (
        "41062e2bf501799a41b78d412b33551685045b98b9a67c9d50a9a26131c16b36"
    ):
        raise ValueError("S4 retained equivalence selection digest changed")
    if equivalence["reproduced_evidence_sha256"] != (
        "8de59c440b348efe72f901bdbd36b85f1e7db485ede96ffc74d438b11159f24d"
    ):
        raise ValueError("S4 retained equivalence evidence digest changed")

    selection = config["selection"]
    if tuple(selection["methods"]) != EXPECTED_METHODS:
        raise ValueError("S4 fresh-preflight method order/set changed")

    null = selection["null"]
    if tuple(null["identities"]) != EXPECTED_NULL_IDENTITIES:
        raise ValueError("S4 fresh-preflight null identities changed")
    if int(null["evaluation_replicate"]) != 20:
        raise ValueError("S4 fresh-preflight null replicate changed")
    if tuple(float(x) for x in null["missingness"]) != (0.0, 0.15):
        raise ValueError("S4 fresh-preflight null missingness changed")

    departure = selection["departure"]
    if tuple(departure["roles"]) != (
        "ADD_SPECIFICITY_NEGATIVE_CONTROL",
        "ADD_DEPARTURE_DIAGNOSTIC",
        "CBD_DEPARTURE_DETECTION",
    ):
        raise ValueError("S4 fresh-preflight departure roles changed")
    if tuple(int(x) for x in departure["signs"]) != (-1, 1):
        raise ValueError("S4 fresh-preflight departure signs changed")
    if int(departure["evaluation_replicate"]) != 5:
        raise ValueError("S4 fresh-preflight departure replicate changed")
    if tuple(float(x) for x in departure["missingness"]) != (0.0, 0.15):
        raise ValueError("S4 fresh-preflight departure missingness changed")
    if departure["cell_choice"] != (
        "LEXICOGRAPHICALLY_SMALLEST_SCIENTIFIC_RUN_ID_"
        "PER_ROLE_SIGN_MISSINGNESS"
    ):
        raise ValueError("S4 fresh-preflight departure selection changed")

    if int(selection["expected_scientific_run_count"]) != 18:
        raise ValueError("S4 fresh-preflight scientific-run count changed")
    if int(selection["expected_method_row_count"]) != 72:
        raise ValueError("S4 fresh-preflight method-row count changed")
    if selection["expected_scientific_run_ids_sha256"] != EXPECTED_RUN_DIGEST:
        raise ValueError("S4 fresh-preflight run digest changed")
    if selection["expected_method_row_ids_sha256"] != EXPECTED_METHOD_DIGEST:
        raise ValueError("S4 fresh-preflight method digest changed")
    if selection["all_selected_runs_outside_m2_prefix"] is not True:
        raise ValueError("S4 fresh-preflight must stay outside M2 prefix")

    coverage = config["coverage"]
    if tuple(coverage["expected_roles"]) != EXPECTED_ROLES:
        raise ValueError("S4 fresh-preflight role coverage changed")
    if tuple(coverage["expected_null_identities"]) != EXPECTED_NULL_IDENTITIES:
        raise ValueError("S4 fresh-preflight null coverage changed")
    if tuple(coverage["expected_restrictions"]) != (
        "ADD_RESTRICTION",
        "CBD_COMPLEMENT_RESTRICTION",
    ):
        raise ValueError("S4 fresh-preflight restriction coverage changed")
    if tuple(float(x) for x in coverage["expected_missingness"]) != (0.0, 0.15):
        raise ValueError("S4 fresh-preflight missingness coverage changed")
    if tuple(int(x) for x in coverage["expected_departure_signs"]) != (-1, 1):
        raise ValueError("S4 fresh-preflight sign coverage changed")
    if tuple(coverage["expected_identity_types"]) != ("DEPARTURE", "NULL"):
        raise ValueError("S4 fresh-preflight identity-type coverage changed")
    if int(coverage["expected_method_count"]) != 4:
        raise ValueError("S4 fresh-preflight method count changed")

    execution = config["execution_contract"]
    if execution["numerical_lineage_variable"] != "OPENBLAS_CORETYPE":
        raise ValueError("S4 fresh-preflight lineage variable changed")
    if execution["numerical_lineage_value"] != "Haswell":
        raise ValueError("S4 fresh-preflight lineage value changed")
    if execution["runtime_core_confirmation_required"] is not True:
        raise ValueError("S4 fresh-preflight runtime confirmation weakened")
    if int(execution["prefix_attempts"]) != 199:
        raise ValueError("S4 fresh-preflight prefix length changed")
    if int(execution["first_new_draw_index"]) != 199:
        raise ValueError("S4 fresh-preflight continuation start changed")
    if int(execution["maximum_total_attempts"]) != 10000:
        raise ValueError("S4 fresh-preflight cap changed")
    if execution["stop_on_first_prefix_refit_failure"] is not True:
        raise ValueError("S4 fresh-preflight refit-failure rule weakened")
    if execution["no_replacement_replicates"] is not True:
        raise ValueError("S4 fresh-preflight replacement replicate enabled")
    if execution["all_methods_same_scientific_dataset"] is not True:
        raise ValueError("S4 fresh-preflight dataset pairing weakened")
    if execution["all_methods_same_missingness_mask"] is not True:
        raise ValueError("S4 fresh-preflight missingness pairing weakened")
    if tuple(execution["allowed_terminal_states"]) != EXPECTED_TERMINAL_STATES:
        raise ValueError("S4 fresh-preflight terminal-state set changed")
    if execution["scientific_outcome_is_not_acceptance_criterion"] is not True:
        raise ValueError("S4 fresh-preflight scientific outcome became gate")

    if config["release"]["release_blocker_closed"] is not False:
        raise ValueError("S4 fresh-preflight cannot close v0.2.0 blocker")
    if any(bool(value) for value in config["boundary"].values()):
        raise ValueError("S4 fresh-preflight boundary was weakened")


def validate_retained_equivalence(result: dict, config: dict) -> None:
    validate_preflight_config(config)
    if result["status"] != (
        "NON_AUTHORITATIVE_S4_NEW_EXECUTOR_EQUIVALENCE_COMPLETE_RETAINED"
    ):
        raise ValueError("S4 retained equivalence status changed")
    if result["authoritative"] is not False:
        raise ValueError("S4 retained equivalence became authoritative")
    eq = result["equivalence"]
    if int(eq["selected_row_count"]) != 12:
        raise ValueError("S4 retained equivalence selected-row count changed")
    if int(eq["exact_match_count"]) != 12:
        raise ValueError("S4 retained equivalence exact-match count changed")
    if int(eq["mismatch_count"]) != 0:
        raise ValueError("S4 retained equivalence mismatch count changed")
    if eq["selected_row_identity_sha256"] != config["retained_sources"][
        "executor_equivalence"
    ]["selected_row_identity_sha256"]:
        raise ValueError("S4 retained equivalence selection digest mismatch")
    if eq["reproduced_evidence_sha256"] != config["retained_sources"][
        "executor_equivalence"
    ]["reproduced_evidence_sha256"]:
        raise ValueError("S4 retained equivalence evidence digest mismatch")
    if eq["broad_executor_authorized_after_retention"] is not True:
        raise ValueError("S4 retained equivalence did not authorize executor")
    if result["interpretation"]["broad_executor_authorized"] is not True:
        raise ValueError("S4 retained equivalence interpretation changed")
    if result["release"]["release_blocker_closed"] is not False:
        raise ValueError("S4 retained equivalence closed v0.2.0 blocker")


def select_fresh_preflight_rows(
    s4_manifest: dict,
    config: dict,
) -> list[dict]:
    validate_preflight_config(config)
    if s4_manifest["status"] != (
        "NON_AUTHORITATIVE_S4_BROAD_SCIENTIFIC_MATRIX_MANIFEST"
    ):
        raise ValueError("S4 fresh-preflight raw manifest status changed")
    if int(s4_manifest["scientific_run_count"]) != 15000:
        raise ValueError("S4 fresh-preflight raw manifest count changed")

    rows = list(s4_manifest["rows"])
    selected: list[dict] = []

    null = config["selection"]["null"]
    for identity in null["identities"]:
        for missingness in null["missingness"]:
            candidates = [
                row
                for row in rows
                if row["identity_type"] == "NULL"
                and row["identity"] == identity
                and int(row["evaluation_replicate"])
                == int(null["evaluation_replicate"])
                and float(row["missingness"]) == float(missingness)
            ]
            if len(candidates) != 1:
                raise ValueError("S4 fresh-preflight null selection is not unique")
            selected.append(candidates[0])

    departure = config["selection"]["departure"]
    for role in departure["roles"]:
        for sign in departure["signs"]:
            for missingness in departure["missingness"]:
                candidates = [
                    row
                    for row in rows
                    if row["identity_type"] == "DEPARTURE"
                    and row["role"] == role
                    and int(row["sign"]) == int(sign)
                    and int(row["evaluation_replicate"])
                    == int(departure["evaluation_replicate"])
                    and float(row["missingness"]) == float(missingness)
                ]
                if not candidates:
                    raise ValueError("S4 fresh-preflight departure selection missing")
                selected.append(
                    min(candidates, key=lambda row: str(row["scientific_run_id"]))
                )

    if len(selected) != 18:
        raise ValueError("S4 fresh-preflight did not select 18 runs")
    run_ids = [str(row["scientific_run_id"]) for row in selected]
    if len(set(run_ids)) != 18:
        raise ValueError("S4 fresh-preflight selected duplicate run IDs")
    if canonical_json_sha256(run_ids) != str(
        config["selection"]["expected_scientific_run_ids_sha256"]
    ):
        raise ValueError("S4 fresh-preflight run-ID digest mismatch")

    method_ids = [
        method_row_id(run_id, method)
        for run_id in run_ids
        for method in EXPECTED_METHODS
    ]
    if len(method_ids) != 72 or len(set(method_ids)) != 72:
        raise ValueError("S4 fresh-preflight method IDs not unique")
    if canonical_json_sha256(method_ids) != str(
        config["selection"]["expected_method_row_ids_sha256"]
    ):
        raise ValueError("S4 fresh-preflight method-ID digest mismatch")

    roles = {str(row["role"]) for row in selected}
    if roles != set(EXPECTED_ROLES):
        raise ValueError("S4 fresh-preflight role coverage incomplete")
    null_identities = {
        str(row["identity"])
        for row in selected
        if row["identity_type"] == "NULL"
    }
    if null_identities != set(EXPECTED_NULL_IDENTITIES):
        raise ValueError("S4 fresh-preflight null identity coverage incomplete")
    restrictions = {str(row["restriction"]) for row in selected}
    if restrictions != {"ADD_RESTRICTION", "CBD_COMPLEMENT_RESTRICTION"}:
        raise ValueError("S4 fresh-preflight restriction coverage incomplete")
    missingness = {float(row["missingness"]) for row in selected}
    if missingness != {0.0, 0.15}:
        raise ValueError("S4 fresh-preflight missingness coverage incomplete")
    departure_signs = {
        int(row["sign"])
        for row in selected
        if row["identity_type"] == "DEPARTURE"
    }
    if departure_signs != {-1, 1}:
        raise ValueError("S4 fresh-preflight sign coverage incomplete")

    for row in selected:
        replicate = int(row["evaluation_replicate"])
        if row["identity_type"] == "DEPARTURE" and replicate < 5:
            raise ValueError("S4 fresh-preflight departure row is M2 prefix")
        if row["identity_type"] == "NULL" and replicate < 20:
            raise ValueError("S4 fresh-preflight null row is M2 prefix")

    return selected


def build_preflight_selection_manifest(
    s4_manifest: dict,
    equivalence_result: dict,
    config: dict,
) -> dict:
    validate_retained_equivalence(equivalence_result, config)
    rows = select_fresh_preflight_rows(s4_manifest, config)
    run_ids = [str(row["scientific_run_id"]) for row in rows]
    method_ids = [
        method_row_id(run_id, method)
        for run_id in run_ids
        for method in EXPECTED_METHODS
    ]
    return {
        "preflight_id": config["preflight_id"],
        "status": "NON_AUTHORITATIVE_S4_FRESH_REPLICATE_PREFLIGHT_SELECTION_COMPLETE",
        "authoritative": False,
        "issue": int(config["issue"]),
        "scientific_run_count": len(run_ids),
        "method_row_count": len(method_ids),
        "scientific_run_ids_sha256": canonical_json_sha256(run_ids),
        "method_row_ids_sha256": canonical_json_sha256(method_ids),
        "eligible_methods": list(EXPECTED_METHODS),
        "rows": rows,
        "execution_authorized": True,
        "executor_equivalence_retained_and_verified": True,
        "scientific_interpretation_authorized": False,
        "release_0_2_0_blocker_closed": False,
        "boundary": dict(config["boundary"]),
    }
