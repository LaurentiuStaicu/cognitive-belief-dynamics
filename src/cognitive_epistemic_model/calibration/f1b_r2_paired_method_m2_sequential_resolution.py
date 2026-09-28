from __future__ import annotations

from collections import defaultdict
import hashlib
import json
from statistics import median
from typing import Any, Mapping

import numpy as np

from .f1b_r2_homogeneous_paired_lineage import (
    validate_h1_runtime_cores,
)
from .f1b_r2_openblas_lineage import validate_candidate_environment
from .f1b_r2_paired_method_m1_screen import (
    EXPECTED_METHODS,
    M1ScientificSpec,
    bootstrap_seed_for,
    hierarchical_scales,
    run_method_prefix,
    validate_m1_config,
)
from .f1b_r2_population_restriction_recovery import (
    fit_population_restriction_pair,
    population_bootstrap_seed_sequence,
    simulate_exact_design_under_population_restriction,
)
from .f1b_r2_resampling_risk import (
    ResamplingRiskBoundaryTable,
    generate_resampling_risk_boundaries,
)
from .f1b_r2_resampling_risk_replay import (
    canonical_attempt_sequence_sha256,
)
from .f1b_r2_restriction_recovery import (
    R2Restriction,
    fit_restriction_pair,
    simulate_exact_design_under_restriction,
)


DESIGN_ID = "F1B.R2.PAIRED_METHOD_M2_SEQUENTIAL_RESOLUTION.V1"
STATUS = "NON_AUTHORITATIVE_PAIRED_METHOD_M2_SEQUENTIAL_RESOLUTION_DESIGN"
EXPECTED_METHODS_M2 = (
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
REJECT = "REJECT_P_LE_ALPHA"
NOT_REJECT = "NOT_REJECT_P_GT_ALPHA"
REFIT_FAILURE = "BOOTSTRAP_REFIT_FAILURE_UNRESOLVED"
UNRESOLVED_AT_CAP = "SEQUENTIAL_UNRESOLVED_AT_CAP"
REPORTING_CHECKPOINTS = (199, 499, 999, 1999, 4999, 10000)


def canonical_json_sha256(value: Any) -> str:
    payload = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def stable_shard(value: str, count: int) -> int:
    digest = hashlib.sha256(value.encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big") % int(count)


def validate_m2_config(config: dict) -> None:
    if config["design_id"] != DESIGN_ID:
        raise ValueError("M2 design identity changed")
    if config["status"] != STATUS:
        raise ValueError("unsupported M2 design status")
    if int(config["issue"]) != 259:
        raise ValueError("M2 issue changed")

    candidate = config["candidate_environment"]
    if candidate["variable"] != "OPENBLAS_CORETYPE":
        raise ValueError("M2 environment variable changed")
    if candidate["value"] != "Haswell":
        raise ValueError("M2 OpenBLAS core changed")
    if candidate["must_be_set_before_python_start"] is not True:
        raise ValueError("M2 OpenBLAS core must be set before Python startup")
    if candidate["runtime_core_confirmation_required"] is not True:
        raise ValueError("M2 runtime core confirmation is required")
    if candidate["environment_fallback_allowed"] is not False:
        raise ValueError("M2 environment fallback is forbidden")

    m1 = config["retained_m1"]
    if int(m1["scientific_run_count"]) != 840:
        raise ValueError("M2 M1 scientific-run count changed")
    if int(m1["method_execution_count"]) != 3360:
        raise ValueError("M2 M1 method-execution count changed")
    if int(m1["prefix_attempts"]) != 199:
        raise ValueError("M2 M1 prefix length changed")
    if int(m1["required_prefix_fit_failures"]) != 0:
        raise ValueError("M2 requires failure-free M1 prefixes")
    if tuple(str(x) for x in m1["eligible_methods"]) != EXPECTED_METHODS_M2:
        raise ValueError("M2 method membership changed")
    if m1["hierarchical_scale_sensitive"] is not True:
        raise ValueError("M2 must retain M1 scale-sensitivity flag")

    design = config["scientific_design"]
    if tuple(float(x) for x in design["missingness_regimes"]) != (0.0, 0.15):
        raise ValueError("M2 missingness regimes changed")
    if int(design["expected_departure_cell_count"]) != 72:
        raise ValueError("M2 departure-cell count changed")
    if int(design["departure_replicates_per_cell"]) != 5:
        raise ValueError("M2 departure replicate count changed")
    if int(design["null_replicates_per_identity"]) != 20:
        raise ValueError("M2 null replicate count changed")
    if int(design["scientific_run_count"]) != 840:
        raise ValueError("M2 scientific-run count changed")
    if int(design["method_execution_count"]) != 3360:
        raise ValueError("M2 method-execution count changed")
    if design["same_scientific_matrix_as_m1"] is not True:
        raise ValueError("M2 must preserve the M1 scientific matrix")
    if design["same_dataset_and_mask_across_methods"] is not True:
        raise ValueError("M2 method pairing was weakened")
    if design["hierarchical_common_random_numbers_across_scales"] is not True:
        raise ValueError("M2 hierarchical common random numbers changed")
    if design["population_method_namespace_distinct"] is not True:
        raise ValueError("M2 population namespace must remain distinct")

    controller = config["controller"]
    expected_controller = {
        "controller_id": "F1B.R2.RESAMPLING_RISK_CONTROLLER.V1",
        "alpha": 0.05,
        "epsilon": 0.001,
        "halfspend": 1000,
        "probability_tolerance": 1e-12,
        "prior_total_attempts": 199,
        "first_new_draw_index": 199,
        "maximum_new_draw_index": 9999,
        "maximum_total_attempts": 10000,
    }
    for key, expected in expected_controller.items():
        actual = controller[key]
        if isinstance(expected, float):
            if float(actual) != expected:
                raise ValueError(f"M2 controller field changed: {key}")
        elif actual != expected:
            raise ValueError(f"M2 controller field changed: {key}")
    if controller["stop_on_boundary"] is not True:
        raise ValueError("M2 must stop on boundary")
    if controller["stop_on_first_new_refit_failure"] is not True:
        raise ValueError("M2 must stop on first new refit failure")
    if controller["refit_failure_status"] != REFIT_FAILURE:
        raise ValueError("M2 refit-failure status changed")
    if controller["unresolved_at_cap_status"] != UNRESOLVED_AT_CAP:
        raise ValueError("M2 cap status changed")

    eligibility = config["eligibility"]
    if float(eligibility["maximum_overall_refit_failure_proportion"]) != 0.02:
        raise ValueError("M2 overall refit threshold changed")
    if (
        float(
            eligibility[
                "maximum_role_missingness_refit_failure_proportion"
            ]
        )
        != 0.05
    ):
        raise ValueError("M2 stratum refit threshold changed")
    if float(eligibility["minimum_overall_resolution_proportion"]) != 0.80:
        raise ValueError("M2 overall resolution threshold changed")
    if (
        float(eligibility["minimum_role_missingness_resolution_proportion"])
        != 0.60
    ):
        raise ValueError("M2 stratum resolution threshold changed")
    if eligibility["m1_eligibility_inheritance_required"] is not True:
        raise ValueError("M2 must inherit M1 eligibility")

    execution = config["execution"]
    if int(execution["shard_count"]) != 80:
        raise ValueError("M2 shard count changed")
    if execution["shard_assignment"] != (
        "SHA256_SCIENTIFIC_RUN_ID_MODULO_SHARD_COUNT"
    ):
        raise ValueError("M2 shard assignment changed")
    if execution["keep_all_methods_for_scientific_run_in_same_shard"] is not True:
        raise ValueError("M2 within-run method pairing was weakened")
    if tuple(int(x) for x in execution["reporting_checkpoints_total_n"]) != (
        REPORTING_CHECKPOINTS
    ):
        raise ValueError("M2 reporting checkpoints changed")

    if tuple(config["decision_states"]) != (
        "M2_ELIGIBLE",
        "M2_INELIGIBLE_REFIT_STABILITY",
        "M2_INELIGIBLE_OVERALL_RESOLUTION",
        "M2_INELIGIBLE_STRATUM_RESOLUTION",
    ):
        raise ValueError("M2 decision states changed")
    if any(bool(value) for value in config["boundary"].values()):
        raise ValueError("M2 scientific boundary was weakened")


def validate_m2_environment(
    environment: Mapping[str, str | None] | None = None,
) -> None:
    validate_candidate_environment(
        environment,
        expected_core="Haswell",
    )


def validate_m2_runtime_cores(cores: tuple[str, ...]) -> None:
    validate_h1_runtime_cores(cores)


def validate_retained_m1_result(result: dict, config: dict) -> None:
    validate_m2_config(config)
    retained = config["retained_m1"]
    if result["result_id"] != (
        "F1B.R2.PAIRED_METHOD_M1_SCREEN.RESULT.2026-09-28"
    ):
        raise ValueError("retained M1 result identity changed")
    if result["status"] != (
        "NON_AUTHORITATIVE_PAIRED_METHOD_M1_SCREEN_COMPLETE_RETAINED"
    ):
        raise ValueError("M2 requires retained completed M1 result")
    if result["authoritative"] is not False:
        raise ValueError("retained M1 result became authoritative")
    if int(result["issue"]) != 259:
        raise ValueError("retained M1 issue changed")
    execution = result["execution"]
    if int(execution["artifact_id"]) != int(retained["artifact_id"]):
        raise ValueError("retained M1 artifact ID changed")
    if str(execution["combined_json_sha256"]) != str(
        retained["combined_json_sha256"]
    ):
        raise ValueError("retained M1 combined SHA-256 changed")
    if int(execution["combined_json_size_bytes"]) != int(
        retained["combined_json_size_bytes"]
    ):
        raise ValueError("retained M1 combined size changed")
    overall = result["overall"]
    if overall["decision"] != "M1_HAS_ELIGIBLE_METHODS":
        raise ValueError("M2 requires M1 eligible-method result")
    if tuple(overall["eligible_methods"]) != EXPECTED_METHODS_M2:
        raise ValueError("retained M1 eligible set changed")
    if overall["hierarchical_scale_sensitive"] is not True:
        raise ValueError("retained M1 scale sensitivity changed")
    if result["interpretation"]["m2_method_set_bound_to_m1_eligible_methods"] is not True:
        raise ValueError("retained M1 did not bind M2 membership")


def validate_m1_combined(m1: dict, config: dict) -> None:
    validate_m2_config(config)
    if m1["design_id"] != "F1B.R2.PAIRED_METHOD_M1_SCREEN.V1":
        raise ValueError("M2 M1 artifact identity changed")
    if m1["status"] != "NON_AUTHORITATIVE_PAIRED_METHOD_M1_COMBINED_RESULT":
        raise ValueError("M2 M1 artifact status changed")
    if m1["authoritative"] is not False:
        raise ValueError("M2 M1 artifact became authoritative")
    if int(m1["scientific_run_count"]) != 840:
        raise ValueError("M2 M1 scientific-run count mismatch")
    if int(m1["method_execution_count"]) != 3360:
        raise ValueError("M2 M1 method-execution count mismatch")
    if tuple(m1["eligible_methods"]) != EXPECTED_METHODS_M2:
        raise ValueError("M2 M1 artifact eligible set mismatch")
    if m1["hierarchical_scale_sensitive"] is not True:
        raise ValueError("M2 M1 scale-sensitivity flag mismatch")
    rows = list(m1["rows"])
    if len(rows) != 3360:
        raise ValueError("M2 M1 row count changed")
    keys = {
        (str(row["scientific_run_id"]), str(row["inference_method"]))
        for row in rows
    }
    if len(keys) != 3360:
        raise ValueError("M2 M1 row identities are not unique")
    if any(bool(row["fit_failure"]) for row in rows):
        raise ValueError("M2 M1 artifact contains observed fit failure")
    if any(bool(row["bootstrap_calibration_failure"]) for row in rows):
        raise ValueError("M2 M1 artifact contains prefix calibration failure")
    if any(int(row["bootstrap_fit_failures"]) != 0 for row in rows):
        raise ValueError("M2 M1 artifact contains prefix refit failure")
    if any(int(row["bootstrap_draws_successful"]) != 199 for row in rows):
        raise ValueError("M2 M1 artifact prefix success count changed")


def build_m2_boundaries(config: dict) -> ResamplingRiskBoundaryTable:
    validate_m2_config(config)
    controller = config["controller"]
    return generate_resampling_risk_boundaries(
        alpha=float(controller["alpha"]),
        epsilon=float(controller["epsilon"]),
        halfspend=float(controller["halfspend"]),
        max_n=int(controller["maximum_total_attempts"]),
        probability_tolerance=float(controller["probability_tolerance"]),
    )


def _restriction_index(restriction: R2Restriction) -> int:
    return 1 if restriction is R2Restriction.ADD else 2


def _prefix_state(
    *,
    observed: float,
    attempts: list[float | None],
    boundaries: ResamplingRiskBoundaryTable,
) -> dict:
    if len(attempts) != 199:
        raise ValueError("M2 prefix must contain exactly 199 attempts")
    if any(value is None for value in attempts):
        raise ValueError("M2 prefix contains refit failure")
    partial_sum = sum(
        int(float(value) >= float(observed))
        for value in attempts
    )
    boundary = boundaries.row(199)
    if partial_sum <= int(boundary.lower):
        return {
            "partial_sum": partial_sum,
            "decision": REJECT,
            "boundary_hit": "LOWER",
        }
    if partial_sum >= int(boundary.upper):
        return {
            "partial_sum": partial_sum,
            "decision": NOT_REJECT,
            "boundary_hit": "UPPER",
        }
    return {
        "partial_sum": partial_sum,
        "decision": None,
        "boundary_hit": None,
    }


def _method_observed_fit(
    dataset,
    *,
    restriction: R2Restriction,
    method_id: str,
    paired_config: dict,
):
    if method_id == "POPULATION":
        pair = fit_population_restriction_pair(dataset, restriction)
        return pair, None
    multiplier = {
        "HIERARCHICAL_0.5X": 0.5,
        "HIERARCHICAL_1X": 1.0,
        "HIERARCHICAL_2X": 2.0,
    }[method_id]
    scales = hierarchical_scales(paired_config, multiplier)
    pair = fit_restriction_pair(
        dataset,
        restriction,
        scales=scales,
    )
    return pair, scales


def _new_draw_statistic(
    dataset,
    *,
    restriction: R2Restriction,
    method_id: str,
    observed_pair,
    scales,
    base_seed: int,
    draw_index: int,
) -> float:
    if method_id == "POPULATION":
        rng = np.random.default_rng(
            population_bootstrap_seed_sequence(
                seed=int(base_seed),
                restriction=restriction,
                draw_index=int(draw_index),
            )
        )
        bootstrap_dataset = simulate_exact_design_under_population_restriction(
            dataset,
            observed_pair.restricted,
            rng=rng,
        )
        pair = fit_population_restriction_pair(
            bootstrap_dataset,
            restriction,
        )
        return float(pair.statistic)

    rng = np.random.default_rng(
        np.random.SeedSequence(
            [
                int(base_seed),
                int(_restriction_index(restriction)),
                int(draw_index),
            ]
        )
    )
    bootstrap_dataset = simulate_exact_design_under_restriction(
        dataset,
        observed_pair.restricted,
        scales=scales,
        rng=rng,
    )
    pair = fit_restriction_pair(
        bootstrap_dataset,
        restriction,
        scales=scales,
    )
    return float(pair.statistic)


def characterize_stream(
    retained_m1_row: dict,
    *,
    spec: M1ScientificSpec,
    replicate: int,
    dataset,
    method_id: str,
    paired_config: dict,
    m1_config: dict,
    m2_config: dict,
    boundaries: ResamplingRiskBoundaryTable,
) -> dict:
    validate_m2_config(m2_config)
    validate_m1_config(m1_config)
    if method_id not in EXPECTED_METHODS_M2:
        raise ValueError("unknown M2 method")
    if method_id != str(retained_m1_row["inference_method"]):
        raise ValueError("M2 method does not match retained M1 row")

    regenerated = run_method_prefix(
        dataset,
        spec=spec,
        replicate=int(replicate),
        method_id=method_id,
        paired_config=paired_config,
        config=m1_config,
    )
    if regenerated["fit_failure"]:
        raise ValueError("M2 exact M1 replay produced observed fit failure")
    if regenerated["bootstrap_calibration_failure"]:
        raise ValueError("M2 exact M1 replay produced calibration failure")
    attempts = list(regenerated["bootstrap_attempt_statistics"])
    if len(attempts) != 199 or any(value is None for value in attempts):
        raise ValueError("M2 exact M1 replay prefix is not failure-free 199")

    regenerated_hash = canonical_attempt_sequence_sha256(attempts)
    retained_hash = str(
        retained_m1_row["bootstrap_attempt_sequence_sha256"]
    )
    if regenerated_hash != retained_hash:
        raise ValueError("M2 exact M1 attempt-sequence hash mismatch")
    if float(regenerated["observed_statistic"]) != float(
        retained_m1_row["observed_statistic"]
    ):
        raise ValueError("M2 exact M1 observed statistic mismatch")

    base_seed = bootstrap_seed_for(
        spec,
        int(replicate),
        paired_config=paired_config,
    )
    if int(base_seed) != int(retained_m1_row["bootstrap_base_seed"]):
        raise ValueError("M2 exact M1 bootstrap base seed mismatch")

    prefix = _prefix_state(
        observed=float(regenerated["observed_statistic"]),
        attempts=attempts,
        boundaries=boundaries,
    )
    partial_sum = int(prefix["partial_sum"])
    decision = prefix["decision"]
    boundary_hit = prefix["boundary_hit"]
    status = (
        "SEQUENTIAL_RESOLVED_AT_PREFIX"
        if decision is not None
        else "SEQUENTIAL_ACTIVE_AFTER_PREFIX"
    )
    terminal_n = 199 if decision is not None else None
    failure_n = None
    new_attempts: list[float | None] = []

    observed_pair = None
    scales = None
    if decision is None:
        restriction = R2Restriction(str(spec.restriction))
        observed_pair, scales = _method_observed_fit(
            dataset,
            restriction=restriction,
            method_id=method_id,
            paired_config=paired_config,
        )
        if float(observed_pair.statistic) != float(
            regenerated["observed_statistic"]
        ):
            raise ValueError("M2 continuation observed fit mismatch")

        for draw_index in range(
            int(m2_config["controller"]["first_new_draw_index"]),
            int(m2_config["controller"]["maximum_new_draw_index"]) + 1,
        ):
            total_n = draw_index + 1
            try:
                statistic = _new_draw_statistic(
                    dataset,
                    restriction=restriction,
                    method_id=method_id,
                    observed_pair=observed_pair,
                    scales=scales,
                    base_seed=int(base_seed),
                    draw_index=draw_index,
                )
            except (RuntimeError, ValueError, np.linalg.LinAlgError):
                new_attempts.append(None)
                status = REFIT_FAILURE
                failure_n = total_n
                terminal_n = total_n
                break

            new_attempts.append(float(statistic))
            partial_sum += int(
                float(statistic) >= float(regenerated["observed_statistic"])
            )
            boundary = boundaries.row(total_n)
            if partial_sum <= int(boundary.lower):
                decision = REJECT
                boundary_hit = "LOWER"
                status = "SEQUENTIAL_RESOLVED"
                terminal_n = total_n
                break
            if partial_sum >= int(boundary.upper):
                decision = NOT_REJECT
                boundary_hit = "UPPER"
                status = "SEQUENTIAL_RESOLVED"
                terminal_n = total_n
                break
        else:
            status = UNRESOLVED_AT_CAP
            terminal_n = int(m2_config["controller"]["maximum_total_attempts"])

    if terminal_n is None:
        raise RuntimeError("M2 stream did not terminate")

    return {
        "scientific_run_id": str(retained_m1_row["scientific_run_id"]),
        "dataset_id": str(retained_m1_row["dataset_id"]),
        "dataset_sha256": str(retained_m1_row["dataset_sha256"]),
        "identity": str(retained_m1_row["identity"]),
        "identity_type": str(retained_m1_row["identity_type"]),
        "restriction": str(retained_m1_row["restriction"]),
        "role": str(retained_m1_row["role"]),
        "anchor_id": retained_m1_row["anchor_id"],
        "axis": retained_m1_row["axis"],
        "sign": retained_m1_row["sign"],
        "target_mean_bernoulli_kl": retained_m1_row[
            "target_mean_bernoulli_kl"
        ],
        "evaluation_replicate": int(retained_m1_row["evaluation_replicate"]),
        "missingness_rate": float(retained_m1_row["missingness_rate"]),
        "inference_method": method_id,
        "bootstrap_base_seed": int(base_seed),
        "retained_m1_attempt_sequence_sha256": retained_hash,
        "regenerated_m1_attempt_sequence_sha256": regenerated_hash,
        "m1_prefix_exact": True,
        "observed_statistic": float(regenerated["observed_statistic"]),
        "prefix_sum_199": int(prefix["partial_sum"]),
        "prefix_decision": prefix["decision"],
        "prefix_boundary_hit": prefix["boundary_hit"],
        "continued_beyond_199": prefix["decision"] is None,
        "first_new_draw_index": (
            199 if prefix["decision"] is None else None
        ),
        "new_attempt_count": len(new_attempts),
        "new_successful_attempt_count": sum(
            value is not None for value in new_attempts
        ),
        "new_refit_failure_count": sum(
            value is None for value in new_attempts
        ),
        "new_attempt_sequence_sha256": (
            None
            if not new_attempts
            else canonical_attempt_sequence_sha256(new_attempts)
        ),
        "status": status,
        "decision": decision,
        "boundary_hit": boundary_hit,
        "terminal_n": int(terminal_n),
        "terminal_sum": int(partial_sum),
        "failure_n": failure_n,
    }


def _method_rows(rows: list[dict], method_id: str) -> list[dict]:
    selected = [
        row for row in rows
        if str(row["inference_method"]) == method_id
    ]
    if len(selected) != 840:
        raise ValueError(f"M2 method {method_id} does not have 840 rows")
    return selected


def _resolved(row: dict) -> bool:
    return row["decision"] in (REJECT, NOT_REJECT)


def _refit_failure(row: dict) -> bool:
    return row["status"] == REFIT_FAILURE


def _expected_direction(row: dict) -> bool:
    decision = row["decision"]
    role = str(row["role"])
    if decision is None:
        return False
    if role in (
        "ADD_NULL_FALSE_REJECTION",
        "CBD_NULL_FALSE_REJECTION",
        "ADD_SPECIFICITY_NEGATIVE_CONTROL",
    ):
        return decision == NOT_REJECT
    if role in (
        "ADD_DEPARTURE_DIAGNOSTIC",
        "CBD_DEPARTURE_DETECTION",
    ):
        return decision == REJECT
    raise ValueError("unknown M2 role semantics")


def _checkpoint_state(row: dict, checkpoint_n: int) -> str:
    n = int(checkpoint_n)
    terminal_n = int(row["terminal_n"])
    if terminal_n > n:
        return "ACTIVE"
    if _resolved(row):
        return "RESOLVED"
    if row["status"] == REFIT_FAILURE:
        return REFIT_FAILURE
    if row["status"] == UNRESOLVED_AT_CAP:
        return UNRESOLVED_AT_CAP
    raise ValueError("unsupported M2 terminal state")


def evaluate_method(
    rows: list[dict],
    config: dict,
    method_id: str,
) -> dict:
    validate_m2_config(config)
    selected = _method_rows(rows, method_id)
    eligibility = config["eligibility"]

    failures = [row for row in selected if _refit_failure(row)]
    resolved = [row for row in selected if _resolved(row)]
    unresolved_cap = [
        row for row in selected if row["status"] == UNRESOLVED_AT_CAP
    ]
    overall_failure_rate = len(failures) / len(selected)
    overall_resolution_rate = len(resolved) / len(selected)

    strata = []
    refit_pass = (
        overall_failure_rate
        <= float(eligibility["maximum_overall_refit_failure_proportion"])
    )
    stratum_resolution_pass = True
    for role in EXPECTED_ROLES:
        for missingness in (0.0, 0.15):
            group = [
                row for row in selected
                if str(row["role"]) == role
                and float(row["missingness_rate"]) == missingness
            ]
            if not group:
                raise ValueError("empty M2 role/missingness stratum")
            failure_rate = sum(_refit_failure(row) for row in group) / len(group)
            resolution_rate = sum(_resolved(row) for row in group) / len(group)
            refit_pass = refit_pass and failure_rate <= float(
                eligibility[
                    "maximum_role_missingness_refit_failure_proportion"
                ]
            )
            stratum_resolution_pass = (
                stratum_resolution_pass
                and resolution_rate
                >= float(
                    eligibility[
                        "minimum_role_missingness_resolution_proportion"
                    ]
                )
            )
            strata.append(
                {
                    "role": role,
                    "missingness_rate": missingness,
                    "run_count": len(group),
                    "resolved_count": sum(_resolved(row) for row in group),
                    "refit_failure_count": sum(
                        _refit_failure(row) for row in group
                    ),
                    "unresolved_at_cap_count": sum(
                        row["status"] == UNRESOLVED_AT_CAP for row in group
                    ),
                    "resolution_rate": resolution_rate,
                    "refit_failure_rate": failure_rate,
                }
            )

    overall_resolution_pass = (
        overall_resolution_rate
        >= float(eligibility["minimum_overall_resolution_proportion"])
    )
    if not refit_pass:
        decision_state = "M2_INELIGIBLE_REFIT_STABILITY"
    elif not overall_resolution_pass:
        decision_state = "M2_INELIGIBLE_OVERALL_RESOLUTION"
    elif not stratum_resolution_pass:
        decision_state = "M2_INELIGIBLE_STRATUM_RESOLUTION"
    else:
        decision_state = "M2_ELIGIBLE"

    stopping = sorted(
        int(row["terminal_n"])
        for row in resolved
    )
    checkpoints = []
    for n in REPORTING_CHECKPOINTS:
        counts = defaultdict(int)
        for row in selected:
            counts[_checkpoint_state(row, n)] += 1
        checkpoints.append(
            {
                "total_n": n,
                "resolved_count": counts["RESOLVED"],
                "active_count": counts["ACTIVE"],
                "refit_failure_unresolved_count": counts[REFIT_FAILURE],
                "unresolved_at_cap_count": counts[UNRESOLVED_AT_CAP],
            }
        )

    reject_count = sum(row["decision"] == REJECT for row in selected)
    not_reject_count = sum(
        row["decision"] == NOT_REJECT for row in selected
    )
    unresolved_count = len(selected) - reject_count - not_reject_count
    expected_count = sum(_expected_direction(row) for row in selected)

    return {
        "inference_method": method_id,
        "decision_state": decision_state,
        "run_count": len(selected),
        "reject_count": reject_count,
        "not_reject_count": not_reject_count,
        "resolved_count": len(resolved),
        "refit_failure_count": len(failures),
        "unresolved_at_cap_count": len(unresolved_cap),
        "unresolved_total_count": unresolved_count,
        "overall_resolution_rate": overall_resolution_rate,
        "overall_refit_failure_rate": overall_failure_rate,
        "expected_direction_count": expected_count,
        "expected_direction_total_denominator_bounds": [
            expected_count / len(selected),
            (expected_count + unresolved_count) / len(selected),
        ],
        "stopping_n": {
            "minimum": None if not stopping else min(stopping),
            "median": None if not stopping else median(stopping),
            "maximum": None if not stopping else max(stopping),
        },
        "role_missingness": strata,
        "reporting_checkpoints": checkpoints,
        "checks": {
            "m1_eligibility_inherited": True,
            "refit_stability_pass": refit_pass,
            "overall_resolution_pass": overall_resolution_pass,
            "stratum_resolution_pass": stratum_resolution_pass,
        },
    }


def pairwise_method_concordance(rows: list[dict]) -> list[dict]:
    by_run: dict[str, dict[str, dict]] = defaultdict(dict)
    for row in rows:
        by_run[str(row["scientific_run_id"])][
            str(row["inference_method"])
        ] = row
    if len(by_run) != 840:
        raise ValueError("M2 scientific-run pairing count changed")
    results = []
    methods = list(EXPECTED_METHODS_M2)
    for i, left in enumerate(methods):
        for right in methods[i + 1 :]:
            both_resolved = 0
            same_decision = 0
            either_unresolved = 0
            for method_rows in by_run.values():
                if set(method_rows) != set(EXPECTED_METHODS_M2):
                    raise ValueError("M2 scientific run lacks paired methods")
                a = method_rows[left]
                b = method_rows[right]
                if _resolved(a) and _resolved(b):
                    both_resolved += 1
                    same_decision += int(a["decision"] == b["decision"])
                else:
                    either_unresolved += 1
            results.append(
                {
                    "left": left,
                    "right": right,
                    "both_resolved_count": both_resolved,
                    "same_decision_count": same_decision,
                    "decision_concordance_among_both_resolved": (
                        None
                        if both_resolved == 0
                        else same_decision / both_resolved
                    ),
                    "either_unresolved_count": either_unresolved,
                }
            )
    return results


def hierarchical_terminal_sensitivity(rows: list[dict]) -> list[dict]:
    methods = (
        "HIERARCHICAL_0.5X",
        "HIERARCHICAL_1X",
        "HIERARCHICAL_2X",
    )
    output = []
    for missingness in (0.0, 0.15):
        strata = (
            ("ADD_SPECIFICITY_NEGATIVE_CONTROL", None),
            ("CBD_DEPARTURE_DETECTION", 0.003),
            ("ADD_DEPARTURE_DIAGNOSTIC", 0.003),
        )
        for role, kl in strata:
            method_values = {}
            for method in methods:
                group = [
                    row for row in rows
                    if row["inference_method"] == method
                    and row["role"] == role
                    and float(row["missingness_rate"]) == missingness
                    and (
                        kl is None
                        or float(row["target_mean_bernoulli_kl"]) == kl
                    )
                ]
                if not group:
                    raise ValueError("empty M2 scale-sensitivity stratum")
                expected = sum(_expected_direction(row) for row in group)
                unresolved = sum(not _resolved(row) for row in group)
                method_values[method] = {
                    "run_count": len(group),
                    "expected_direction_count": expected,
                    "unresolved_count": unresolved,
                    "expected_direction_total_denominator_bounds": [
                        expected / len(group),
                        (expected + unresolved) / len(group),
                    ],
                }
            output.append(
                {
                    "role": role,
                    "target_mean_bernoulli_kl": kl,
                    "missingness_rate": missingness,
                    "methods": method_values,
                }
            )
    return output


def evaluate_all_methods(rows: list[dict], config: dict) -> dict:
    validate_m2_config(config)
    if len(rows) != 3360:
        raise ValueError("M2 combined row count changed")
    keys = {
        (str(row["scientific_run_id"]), str(row["inference_method"]))
        for row in rows
    }
    if len(keys) != 3360:
        raise ValueError("M2 combined row identities are not unique")

    method_results = [
        evaluate_method(rows, config, method)
        for method in EXPECTED_METHODS_M2
    ]
    eligible = [
        row["inference_method"]
        for row in method_results
        if row["decision_state"] == "M2_ELIGIBLE"
    ]
    overall_decision = (
        "M2_HAS_ELIGIBLE_METHODS"
        if eligible
        else "M2_NO_ELIGIBLE_METHOD_INFERENCE_REDESIGN_REQUIRED"
    )
    return {
        "method_results": method_results,
        "eligible_methods": eligible,
        "overall_decision": overall_decision,
        "pairwise_method_concordance": pairwise_method_concordance(rows),
        "hierarchical_terminal_sensitivity": hierarchical_terminal_sensitivity(
            rows
        ),
    }
