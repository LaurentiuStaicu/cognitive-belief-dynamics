from __future__ import annotations

import numpy as np

from .f1b_r2_paired_bootstrap_characterization import dataset_fingerprint
from .f1b_r2_paired_method_m1_screen import (
    M1ScientificSpec,
    bootstrap_seed_for,
    dataset_id_for,
    run_method_prefix,
    validate_m1_config,
)
from .f1b_r2_paired_method_m2_sequential_resolution import (
    EXPECTED_METHODS_M2,
    REFIT_FAILURE,
    UNRESOLVED_AT_CAP,
    _method_observed_fit,
    _new_draw_statistic,
    _prefix_state,
    validate_m2_config,
)
from .f1b_r2_resampling_risk import ResamplingRiskBoundaryTable
from .f1b_r2_resampling_risk_replay import (
    canonical_attempt_sequence_sha256,
)
from .f1b_r2_restriction_recovery import R2Restriction


PREFIX_EXECUTION_FAILURE = "PREFIX_EXECUTION_FAILURE_UNRESOLVED"
EVIDENCE_ORIGIN_NEW = "S4_NEW_EXECUTION"


def _scientific_identity(
    scientific_row: dict,
    *,
    spec: M1ScientificSpec,
    replicate: int,
) -> tuple[str, str]:
    dataset_id = dataset_id_for(spec, int(replicate))
    missingness = float(scientific_row["missingness"])
    scientific_run_id = (
        f"{dataset_id}|RESTRICTION={spec.restriction}"
        f"|MISSINGNESS={missingness:.2f}"
    )
    if str(scientific_row["scientific_run_id"]) != scientific_run_id:
        raise ValueError("S4 executor scientific-run identity mismatch")
    if str(scientific_row["dataset_id"]) != dataset_id:
        raise ValueError("S4 executor dataset identity mismatch")
    if int(scientific_row["evaluation_replicate"]) != int(replicate):
        raise ValueError("S4 executor replicate mismatch")
    compare = {
        "identity": spec.identity,
        "identity_type": spec.identity_type,
        "restriction": spec.restriction,
        "role": spec.role,
        "anchor_id": spec.anchor_id,
        "axis": spec.axis,
        "sign": spec.sign,
        "target_mean_bernoulli_kl": spec.target_mean_bernoulli_kl,
    }
    for key, expected in compare.items():
        if scientific_row[key] != expected:
            raise ValueError(f"S4 executor scientific field mismatch: {key}")
    return dataset_id, scientific_run_id


def _base_row(
    scientific_row: dict,
    *,
    dataset_sha256: str,
    method_id: str,
    base_seed: int,
) -> dict:
    return {
        "scientific_run_id": str(scientific_row["scientific_run_id"]),
        "dataset_id": str(scientific_row["dataset_id"]),
        "dataset_sha256": str(dataset_sha256),
        "identity": str(scientific_row["identity"]),
        "identity_type": str(scientific_row["identity_type"]),
        "restriction": str(scientific_row["restriction"]),
        "role": str(scientific_row["role"]),
        "anchor_id": scientific_row["anchor_id"],
        "axis": scientific_row["axis"],
        "sign": scientific_row["sign"],
        "target_mean_bernoulli_kl": scientific_row[
            "target_mean_bernoulli_kl"
        ],
        "evaluation_replicate": int(
            scientific_row["evaluation_replicate"]
        ),
        "missingness_rate": float(scientific_row["missingness"]),
        "inference_method": str(method_id),
        "evidence_origin": EVIDENCE_ORIGIN_NEW,
        "bootstrap_base_seed": int(base_seed),
    }


def run_new_stream(
    scientific_row: dict,
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
    validate_m1_config(m1_config)
    validate_m2_config(m2_config)
    if method_id not in EXPECTED_METHODS_M2:
        raise ValueError("unknown S4 inference method")

    _, _ = _scientific_identity(
        scientific_row,
        spec=spec,
        replicate=int(replicate),
    )
    fingerprint = dataset_fingerprint(dataset)
    base_seed = bootstrap_seed_for(
        spec,
        int(replicate),
        paired_config=paired_config,
    )
    base = _base_row(
        scientific_row,
        dataset_sha256=fingerprint,
        method_id=method_id,
        base_seed=base_seed,
    )

    regenerated = run_method_prefix(
        dataset,
        spec=spec,
        replicate=int(replicate),
        method_id=method_id,
        paired_config=paired_config,
        config=m1_config,
    )

    if regenerated["fit_failure"]:
        return {
            **base,
            "prefix_attempt_sequence_sha256": None,
            "prefix_attempt_count": 0,
            "prefix_successful_attempt_count": 0,
            "prefix_refit_failure_count": 0,
            "prefix_execution_failure": True,
            "observed_statistic": None,
            "prefix_sum_199": None,
            "prefix_decision": None,
            "prefix_boundary_hit": None,
            "continued_beyond_199": False,
            "first_new_draw_index": None,
            "new_attempt_count": 0,
            "new_successful_attempt_count": 0,
            "new_refit_failure_count": 0,
            "new_attempt_sequence_sha256": None,
            "status": PREFIX_EXECUTION_FAILURE,
            "decision": None,
            "boundary_hit": None,
            "terminal_n": None,
            "terminal_sum": None,
            "failure_n": None,
        }

    attempts = list(regenerated["bootstrap_attempt_statistics"])
    observed = regenerated["observed_statistic"]
    if observed is None:
        raise ValueError("S4 prefix lacks observed statistic")

    if len(attempts) != 199:
        return {
            **base,
            "prefix_attempt_sequence_sha256": (
                None
                if not attempts
                else canonical_attempt_sequence_sha256(attempts)
            ),
            "prefix_attempt_count": len(attempts),
            "prefix_successful_attempt_count": sum(
                value is not None for value in attempts
            ),
            "prefix_refit_failure_count": sum(
                value is None for value in attempts
            ),
            "prefix_execution_failure": True,
            "observed_statistic": float(observed),
            "prefix_sum_199": None,
            "prefix_decision": None,
            "prefix_boundary_hit": None,
            "continued_beyond_199": False,
            "first_new_draw_index": None,
            "new_attempt_count": 0,
            "new_successful_attempt_count": 0,
            "new_refit_failure_count": 0,
            "new_attempt_sequence_sha256": None,
            "status": PREFIX_EXECUTION_FAILURE,
            "decision": None,
            "boundary_hit": None,
            "terminal_n": None,
            "terminal_sum": None,
            "failure_n": None,
        }

    if any(value is None for value in attempts):
        first_failure_index = next(
            index for index, value in enumerate(attempts)
            if value is None
        )
        used = attempts[: first_failure_index + 1]
        terminal_sum = sum(
            int(float(value) >= float(observed))
            for value in used
            if value is not None
        )
        return {
            **base,
            "prefix_attempt_sequence_sha256": (
                canonical_attempt_sequence_sha256(used)
            ),
            "prefix_attempt_count": len(used),
            "prefix_successful_attempt_count": sum(
                value is not None for value in used
            ),
            "prefix_refit_failure_count": 1,
            "prefix_execution_failure": False,
            "observed_statistic": float(observed),
            "prefix_sum_199": None,
            "prefix_decision": None,
            "prefix_boundary_hit": None,
            "continued_beyond_199": False,
            "first_new_draw_index": None,
            "new_attempt_count": 0,
            "new_successful_attempt_count": 0,
            "new_refit_failure_count": 0,
            "new_attempt_sequence_sha256": None,
            "status": REFIT_FAILURE,
            "decision": None,
            "boundary_hit": None,
            "terminal_n": first_failure_index + 1,
            "terminal_sum": int(terminal_sum),
            "failure_n": first_failure_index + 1,
        }

    if regenerated["bootstrap_calibration_failure"]:
        return {
            **base,
            "prefix_attempt_sequence_sha256": (
                canonical_attempt_sequence_sha256(attempts)
            ),
            "prefix_attempt_count": 199,
            "prefix_successful_attempt_count": 199,
            "prefix_refit_failure_count": 0,
            "prefix_execution_failure": True,
            "observed_statistic": float(observed),
            "prefix_sum_199": None,
            "prefix_decision": None,
            "prefix_boundary_hit": None,
            "continued_beyond_199": False,
            "first_new_draw_index": None,
            "new_attempt_count": 0,
            "new_successful_attempt_count": 0,
            "new_refit_failure_count": 0,
            "new_attempt_sequence_sha256": None,
            "status": PREFIX_EXECUTION_FAILURE,
            "decision": None,
            "boundary_hit": None,
            "terminal_n": 199,
            "terminal_sum": None,
            "failure_n": None,
        }

    prefix_hash = canonical_attempt_sequence_sha256(attempts)
    prefix = _prefix_state(
        observed=float(observed),
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

    if decision is None:
        restriction = R2Restriction(str(spec.restriction))
        observed_pair, scales = _method_observed_fit(
            dataset,
            restriction=restriction,
            method_id=method_id,
            paired_config=paired_config,
        )
        if float(observed_pair.statistic) != float(observed):
            raise ValueError("S4 continuation observed fit mismatch")

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
            partial_sum += int(float(statistic) >= float(observed))
            boundary = boundaries.row(total_n)
            if partial_sum <= int(boundary.lower):
                decision = "REJECT_P_LE_ALPHA"
                boundary_hit = "LOWER"
                status = "SEQUENTIAL_RESOLVED"
                terminal_n = total_n
                break
            if partial_sum >= int(boundary.upper):
                decision = "NOT_REJECT_P_GT_ALPHA"
                boundary_hit = "UPPER"
                status = "SEQUENTIAL_RESOLVED"
                terminal_n = total_n
                break
        else:
            status = UNRESOLVED_AT_CAP
            terminal_n = int(
                m2_config["controller"]["maximum_total_attempts"]
            )

    if terminal_n is None:
        raise RuntimeError("S4 stream did not terminate")

    return {
        **base,
        "prefix_attempt_sequence_sha256": prefix_hash,
        "prefix_attempt_count": 199,
        "prefix_successful_attempt_count": 199,
        "prefix_refit_failure_count": 0,
        "prefix_execution_failure": False,
        "observed_statistic": float(observed),
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


def compare_new_row_to_retained_m2(
    new_row: dict,
    retained_row: dict,
) -> None:
    if new_row["evidence_origin"] != EVIDENCE_ORIGIN_NEW:
        raise ValueError("S4 equivalence row origin changed")
    mapping = {
        "scientific_run_id": "scientific_run_id",
        "dataset_id": "dataset_id",
        "dataset_sha256": "dataset_sha256",
        "identity": "identity",
        "identity_type": "identity_type",
        "restriction": "restriction",
        "role": "role",
        "anchor_id": "anchor_id",
        "axis": "axis",
        "sign": "sign",
        "target_mean_bernoulli_kl": "target_mean_bernoulli_kl",
        "evaluation_replicate": "evaluation_replicate",
        "missingness_rate": "missingness_rate",
        "inference_method": "inference_method",
        "bootstrap_base_seed": "bootstrap_base_seed",
        "observed_statistic": "observed_statistic",
        "prefix_sum_199": "prefix_sum_199",
        "prefix_decision": "prefix_decision",
        "prefix_boundary_hit": "prefix_boundary_hit",
        "continued_beyond_199": "continued_beyond_199",
        "first_new_draw_index": "first_new_draw_index",
        "new_attempt_count": "new_attempt_count",
        "new_successful_attempt_count": "new_successful_attempt_count",
        "new_refit_failure_count": "new_refit_failure_count",
        "new_attempt_sequence_sha256": "new_attempt_sequence_sha256",
        "status": "status",
        "decision": "decision",
        "boundary_hit": "boundary_hit",
        "terminal_n": "terminal_n",
        "terminal_sum": "terminal_sum",
        "failure_n": "failure_n",
    }
    for new_key, retained_key in mapping.items():
        if new_row[new_key] != retained_row[retained_key]:
            raise ValueError(
                f"S4/M2 equivalence mismatch: {new_key}"
            )
    if new_row["prefix_attempt_sequence_sha256"] != retained_row[
        "regenerated_m1_attempt_sequence_sha256"
    ]:
        raise ValueError("S4/M2 prefix digest mismatch")
    if new_row["prefix_attempt_count"] != 199:
        raise ValueError("S4 equivalence prefix attempt count changed")
    if new_row["prefix_successful_attempt_count"] != 199:
        raise ValueError("S4 equivalence prefix success count changed")
    if new_row["prefix_refit_failure_count"] != 0:
        raise ValueError("S4 equivalence prefix failure count changed")
    if new_row["prefix_execution_failure"] is not False:
        raise ValueError("S4 equivalence prefix unexpectedly failed")
