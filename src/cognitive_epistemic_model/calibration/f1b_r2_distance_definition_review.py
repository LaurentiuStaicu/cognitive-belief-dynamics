from __future__ import annotations

from itertools import combinations
from math import sqrt

import numpy as np
from scipy.optimize import minimize
from scipy.special import expit, xlogy

from .f1b_r2_controlled_departures import (
    cbd_utility,
    design_arrays,
    general_utility,
)
from .f1b_r2_projection_bound_sensitivity import (
    run_projection_bound_sensitivity,
)


def _rms(values: np.ndarray) -> float:
    array = np.asarray(values, dtype=float)
    return float(sqrt(float(np.mean(array**2))))


def _base_bounds(departure_config: dict) -> list[tuple[float, float]]:
    raw = departure_config["cbd_projection"]["parameter_bounds"]
    return [
        tuple(float(x) for x in raw["sharing_bias"]),
        tuple(float(x) for x in raw["baseline_logit"]),
        tuple(float(x) for x in raw["beta_accuracy"]),
        tuple(float(x) for x in raw["beta_reward"]),
    ]


def _scaled_bounds(
    departure_config: dict,
    multiplier: float,
) -> list[tuple[float, float]]:
    if multiplier <= 0.0:
        raise ValueError("domain multiplier must be positive")
    return [
        (float(low) * multiplier, float(high) * multiplier)
        for low, high in _base_bounds(departure_config)
    ]


def _active_bounds(
    parameters: np.ndarray,
    bounds: list[tuple[float, float]],
    *,
    tolerance: float,
) -> list[str]:
    names = (
        "sharing_bias",
        "baseline_logit",
        "beta_accuracy",
        "beta_reward",
    )
    active: list[str] = []
    for name, value, (low, high) in zip(
        names,
        np.asarray(parameters, dtype=float),
        bounds,
        strict=True,
    ):
        if abs(float(value) - float(low)) <= tolerance:
            active.append(f"{name}=LOW")
        if abs(float(value) - float(high)) <= tolerance:
            active.append(f"{name}=HIGH")
    return active


def _bernoulli_kl_from_probability_and_logit(
    p: np.ndarray,
    q_logit: np.ndarray,
) -> np.ndarray:
    p = np.asarray(p, dtype=float)
    eta = np.asarray(q_logit, dtype=float)
    if p.shape != eta.shape:
        raise ValueError("Bernoulli probability/logit shapes must match")
    log_q = -np.logaddexp(0.0, -eta)
    log_one_minus_q = -np.logaddexp(0.0, eta)
    entropy_term = xlogy(p, p) + xlogy(1.0 - p, 1.0 - p)
    return entropy_term - p * log_q - (1.0 - p) * log_one_minus_q


def _surface_metrics(
    *,
    eta_general: np.ndarray,
    eta_cbd: np.ndarray,
) -> dict:
    p_general = expit(eta_general)
    p_cbd = expit(eta_cbd)
    eta_delta = eta_general - eta_cbd
    p_delta = p_general - p_cbd
    kl = _bernoulli_kl_from_probability_and_logit(
        p_general,
        eta_cbd,
    )
    variance_cbd = p_cbd * (1.0 - p_cbd)
    mean_kl = float(np.mean(kl))
    return {
        "utility_rms_distance": _rms(eta_delta),
        "probability_rms_distance": _rms(p_delta),
        "mean_bernoulli_kl_general_to_cbd": mean_kl,
        "max_bernoulli_kl_general_to_cbd": float(np.max(kl)),
        "sqrt_2_mean_kl_diagnostic": float(
            sqrt(max(0.0, 2.0 * mean_kl))
        ),
        "information_weighted_logit_distance": _rms(
            np.sqrt(variance_cbd) * eta_delta
        ),
        "mean_absolute_probability_difference": float(
            np.mean(np.abs(p_delta))
        ),
        "max_absolute_probability_difference": float(
            np.max(np.abs(p_delta))
        ),
        "min_probability_general": float(np.min(p_general)),
        "max_probability_general": float(np.max(p_general)),
        "min_probability_cbd": float(np.min(p_cbd)),
        "max_probability_cbd": float(np.max(p_cbd)),
    }


def _objective_value(
    candidate_id: str,
    *,
    parameters: np.ndarray,
    eta_general: np.ndarray,
    p_general: np.ndarray,
    belief: np.ndarray,
    accuracy: np.ndarray,
    reward: np.ndarray,
) -> float:
    eta_cbd = cbd_utility(
        parameters,
        belief,
        accuracy,
        reward,
    )
    if candidate_id == "STABILIZED_UTILITY_RMS":
        delta = eta_general - eta_cbd
        return float(np.mean(delta**2))
    if candidate_id == "PROBABILITY_RMS":
        delta = p_general - expit(eta_cbd)
        return float(np.mean(delta**2))
    if candidate_id == "BERNOULLI_KL_GENERAL_TO_CBD":
        return float(
            np.mean(
                _bernoulli_kl_from_probability_and_logit(
                    p_general,
                    eta_cbd,
                )
            )
        )
    raise ValueError(f"unsupported distance candidate: {candidate_id}")


def _cbd_utility_surface_coordinates(
    parameters: np.ndarray | tuple[float, ...],
    belief: np.ndarray,
    accuracy: np.ndarray,
    reward: np.ndarray,
) -> np.ndarray:
    values = np.asarray(parameters, dtype=float)
    if values.shape != (4,):
        raise ValueError("CBD surface coordinates must have four parameters")
    bias, w0, w1, beta_reward = values
    if not 0.0 <= float(w0) <= 1.0:
        raise ValueError("W0 must lie in [0,1]")
    if not 0.0 <= float(w1) <= 1.0:
        raise ValueError("W1 must lie in [0,1]")
    if not np.all(np.isin(accuracy, (0.0, 1.0))):
        raise ValueError("surface-coordinate CBD requires binary accuracy cue")
    weight = np.where(accuracy == 0.0, w0, w1)
    return (
        float(bias)
        + weight * (2.0 * belief - 1.0)
        + float(beta_reward) * (1.0 - weight) * reward
    )


def _surface_coordinates_from_logit_parameters(
    parameters: tuple[float, ...] | np.ndarray,
) -> tuple[float, float, float, float]:
    values = np.asarray(parameters, dtype=float)
    if values.shape != (4,):
        raise ValueError("CBD logit parameters must have four coordinates")
    bias, baseline_logit, beta_accuracy, beta_reward = values
    return (
        float(bias),
        float(expit(baseline_logit)),
        float(expit(baseline_logit + beta_accuracy)),
        float(beta_reward),
    )


def _objective_value_surface_coordinates(
    candidate_id: str,
    *,
    parameters: np.ndarray,
    eta_general: np.ndarray,
    p_general: np.ndarray,
    belief: np.ndarray,
    accuracy: np.ndarray,
    reward: np.ndarray,
) -> float:
    eta_cbd = _cbd_utility_surface_coordinates(
        parameters,
        belief,
        accuracy,
        reward,
    )
    if candidate_id == "STABILIZED_UTILITY_RMS":
        delta = eta_general - eta_cbd
        return float(np.mean(delta**2))
    if candidate_id == "PROBABILITY_RMS":
        delta = p_general - expit(eta_cbd)
        return float(np.mean(delta**2))
    if candidate_id == "BERNOULLI_KL_GENERAL_TO_CBD":
        return float(
            np.mean(
                _bernoulli_kl_from_probability_and_logit(
                    p_general,
                    eta_cbd,
                )
            )
        )
    raise ValueError(f"unsupported distance candidate: {candidate_id}")


def _active_closure_bounds(
    parameters: np.ndarray,
    bounds: list[tuple[float, float]],
    *,
    tolerance: float,
) -> list[str]:
    names = ("sharing_bias", "W0", "W1", "beta_reward")
    active: list[str] = []
    for name, value, (low, high) in zip(
        names,
        np.asarray(parameters, dtype=float),
        bounds,
        strict=True,
    ):
        if abs(float(value) - float(low)) <= tolerance:
            active.append(f"{name}=LOW")
        if abs(float(value) - float(high)) <= tolerance:
            active.append(f"{name}=HIGH")
    return active


def _project_candidate_closure(
    *,
    candidate_id: str,
    eta_general: np.ndarray,
    belief: np.ndarray,
    accuracy: np.ndarray,
    reward: np.ndarray,
    logit_starts: list[tuple[float, ...]],
    config: dict,
    departure_config: dict,
) -> dict:
    p_general = expit(eta_general)
    optimization = config["optimization"]
    tolerance = float(
        config["numerical_integrity"]["closure_boundary_tolerance"]
    )
    nested_tolerance = float(
        config["numerical_integrity"]["nested_objective_tolerance"]
    )

    starts = [
        _surface_coordinates_from_logit_parameters(start)
        for start in logit_starts
    ]
    domain_results: list[dict] = []
    for multiplier_raw in config["diagnostic_domain_multipliers"]:
        multiplier = float(multiplier_raw)
        scaled = _scaled_bounds(departure_config, multiplier)
        bounds = [
            scaled[0],
            (0.0, 1.0),
            (0.0, 1.0),
            scaled[3],
        ]
        records: list[dict] = []
        for start_index, start in enumerate(starts):
            x0 = np.asarray(start, dtype=float)
            result = minimize(
                lambda parameters: _objective_value_surface_coordinates(
                    candidate_id,
                    parameters=parameters,
                    eta_general=eta_general,
                    p_general=p_general,
                    belief=belief,
                    accuracy=accuracy,
                    reward=reward,
                ),
                x0=x0,
                method=str(optimization["method"]),
                bounds=bounds,
                options={
                    "maxiter": int(optimization["maxiter"]),
                    "ftol": float(optimization["ftol"]),
                    "maxls": int(optimization["maxls"]),
                },
            )
            objective = (
                float(result.fun) if np.isfinite(result.fun) else None
            )
            parameters = (
                [float(x) for x in result.x]
                if np.all(np.isfinite(result.x))
                else None
            )
            records.append(
                {
                    "start_index": int(start_index),
                    "initial_surface_coordinates": [float(x) for x in x0],
                    "success": bool(result.success),
                    "status": int(result.status),
                    "message": str(result.message),
                    "objective": objective,
                    "surface_coordinates": parameters,
                }
            )

        successful = [
            row
            for row in records
            if row["success"]
            and row["objective"] is not None
            and row["surface_coordinates"] is not None
        ]
        if not successful:
            raise RuntimeError(
                f"all closure starts failed for {candidate_id} at {multiplier}x"
            )
        selected = min(successful, key=lambda row: float(row["objective"]))
        parameters = np.asarray(
            selected["surface_coordinates"],
            dtype=float,
        )
        eta_cbd = _cbd_utility_surface_coordinates(
            parameters,
            belief,
            accuracy,
            reward,
        )
        active = _active_closure_bounds(
            parameters,
            bounds,
            tolerance=tolerance,
        )
        domain_results.append(
            {
                "domain_multiplier": multiplier,
                "bounds": [
                    [float(low), float(high)] for low, high in bounds
                ],
                "selected_start_index": int(selected["start_index"]),
                "selected_surface_coordinates": [
                    float(x) for x in parameters
                ],
                "objective": float(selected["objective"]),
                "primary_distance": _primary_distance(
                    candidate_id,
                    float(selected["objective"]),
                ),
                "active_bounds": active,
                "successful_start_count": len(successful),
                "failed_start_count": len(records) - len(successful),
                "start_records": records,
                "surface_metrics": _surface_metrics(
                    eta_general=eta_general,
                    eta_cbd=eta_cbd,
                ),
            }
        )

    for previous, current in zip(
        domain_results,
        domain_results[1:],
        strict=False,
    ):
        if (
            float(current["objective"])
            > float(previous["objective"]) + nested_tolerance
        ):
            raise ValueError(
                "nested closure objective increased under wider domain"
            )

    transitions = [
        {
            "from_multiplier": previous["domain_multiplier"],
            "to_multiplier": current["domain_multiplier"],
            "objective_change": (
                float(current["objective"])
                - float(previous["objective"])
            ),
            "primary_distance_change": (
                float(current["primary_distance"])
                - float(previous["primary_distance"])
            ),
        }
        for previous, current in zip(
            domain_results,
            domain_results[1:],
            strict=False,
        )
    ]
    widest = domain_results[-1]
    closure_components = [
        name
        for name in widest["active_bounds"]
        if name.startswith("W0=") or name.startswith("W1=")
    ]
    domain_components = [
        name
        for name in widest["active_bounds"]
        if name.startswith("sharing_bias=")
        or name.startswith("beta_reward=")
    ]
    if domain_components:
        status = "SCIENTIFIC_DOMAIN_UNRESOLVED"
    elif closure_components:
        status = "NON_ATTAINED_OR_CLOSURE_LIMIT"
    else:
        status = "FINITE_INTERIOR_ATTAINED"

    return {
        "coordinate_system": (
            "CBD_RESPONSE_SURFACE_(sharing_bias,W0,W1,beta_reward)"
        ),
        "finite_logit_family": "W0,W1 in (0,1)",
        "closed_surface_family": "W0,W1 in [0,1]",
        "attainment_status": status,
        "closure_boundary_components": closure_components,
        "scientific_domain_components": domain_components,
        "domain_results": domain_results,
        "domain_transitions": transitions,
        "selected_widest_domain": widest,
    }


def _primary_distance(candidate_id: str, objective: float) -> float:
    if candidate_id in {
        "STABILIZED_UTILITY_RMS",
        "PROBABILITY_RMS",
    }:
        return float(sqrt(max(0.0, objective)))
    if candidate_id == "BERNOULLI_KL_GENERAL_TO_CBD":
        return float(objective)
    raise ValueError(f"unsupported distance candidate: {candidate_id}")


def _cell_rows(
    *,
    case: dict,
    candidate_id: str,
    eta_general: np.ndarray,
    eta_cbd: np.ndarray,
    belief: np.ndarray,
    accuracy: np.ndarray,
    reward: np.ndarray,
) -> list[dict]:
    p_general = expit(eta_general)
    p_cbd = expit(eta_cbd)
    kl = _bernoulli_kl_from_probability_and_logit(
        p_general,
        eta_cbd,
    )
    rows: list[dict] = []
    for index in range(len(belief)):
        rows.append(
            {
                "case_id": str(case["case_id"]),
                "candidate_id": candidate_id,
                "cell_index": int(index),
                "belief_B": float(belief[index]),
                "accuracy_cue_A": float(accuracy[index]),
                "reward_context_R": float(reward[index]),
                "eta_general": float(eta_general[index]),
                "eta_cbd": float(eta_cbd[index]),
                "utility_delta": float(
                    eta_general[index] - eta_cbd[index]
                ),
                "p_general": float(p_general[index]),
                "p_cbd": float(p_cbd[index]),
                "probability_delta": float(
                    p_general[index] - p_cbd[index]
                ),
                "bernoulli_kl_general_to_cbd": float(kl[index]),
            }
        )
    return rows


def _project_candidate(
    *,
    candidate_id: str,
    eta_general: np.ndarray,
    belief: np.ndarray,
    accuracy: np.ndarray,
    reward: np.ndarray,
    starts: list[tuple[float, ...]],
    config: dict,
    departure_config: dict,
) -> dict:
    p_general = expit(eta_general)
    optimization = config["optimization"]
    tolerance = float(
        config["numerical_integrity"]["bound_activity_tolerance"]
    )
    nested_tolerance = float(
        config["numerical_integrity"]["nested_objective_tolerance"]
    )

    domain_results: list[dict] = []
    for multiplier_raw in config["diagnostic_domain_multipliers"]:
        multiplier = float(multiplier_raw)
        bounds = _scaled_bounds(departure_config, multiplier)
        records: list[dict] = []

        for start_index, start in enumerate(starts):
            x0 = np.asarray(start, dtype=float)
            if x0.shape != (4,):
                raise ValueError("all CBD starts must have four parameters")
            for value, (low, high) in zip(x0, bounds, strict=True):
                if not float(low) <= float(value) <= float(high):
                    raise ValueError(
                        "common projection start lies outside diagnostic domain"
                    )

            result = minimize(
                lambda parameters: _objective_value(
                    candidate_id,
                    parameters=parameters,
                    eta_general=eta_general,
                    p_general=p_general,
                    belief=belief,
                    accuracy=accuracy,
                    reward=reward,
                ),
                x0=x0,
                method=str(optimization["method"]),
                bounds=bounds,
                options={
                    "maxiter": int(optimization["maxiter"]),
                    "ftol": float(optimization["ftol"]),
                    "maxls": int(optimization["maxls"]),
                },
            )
            objective = (
                float(result.fun) if np.isfinite(result.fun) else None
            )
            parameters = (
                [float(x) for x in result.x]
                if np.all(np.isfinite(result.x))
                else None
            )
            records.append(
                {
                    "start_index": int(start_index),
                    "initial_parameters": [float(x) for x in x0],
                    "success": bool(result.success),
                    "status": int(result.status),
                    "message": str(result.message),
                    "objective": objective,
                    "parameters": parameters,
                }
            )

        successful = [
            row
            for row in records
            if row["success"]
            and row["objective"] is not None
            and row["parameters"] is not None
        ]
        if not successful:
            raise RuntimeError(
                f"all starts failed for {candidate_id} at {multiplier}x"
            )

        selected = min(
            successful,
            key=lambda row: float(row["objective"]),
        )
        parameters = np.asarray(selected["parameters"], dtype=float)
        eta_cbd = cbd_utility(
            parameters,
            belief,
            accuracy,
            reward,
        )
        metrics = _surface_metrics(
            eta_general=eta_general,
            eta_cbd=eta_cbd,
        )
        domain_results.append(
            {
                "domain_multiplier": multiplier,
                "bounds": [
                    [float(low), float(high)] for low, high in bounds
                ],
                "selected_start_index": int(
                    selected["start_index"]
                ),
                "selected_parameters": [
                    float(x) for x in parameters
                ],
                "objective": float(selected["objective"]),
                "primary_distance": _primary_distance(
                    candidate_id,
                    float(selected["objective"]),
                ),
                "active_bounds": _active_bounds(
                    parameters,
                    bounds,
                    tolerance=tolerance,
                ),
                "successful_start_count": len(successful),
                "failed_start_count": len(records) - len(successful),
                "start_records": records,
                "surface_metrics": metrics,
            }
        )

    for previous, current in zip(
        domain_results,
        domain_results[1:],
        strict=False,
    ):
        if (
            float(current["objective"])
            > float(previous["objective"]) + nested_tolerance
        ):
            raise ValueError(
                "nested candidate objective increased under wider domain"
            )

    transitions: list[dict] = []
    for previous, current in zip(
        domain_results,
        domain_results[1:],
        strict=False,
    ):
        transitions.append(
            {
                "from_multiplier": previous["domain_multiplier"],
                "to_multiplier": current["domain_multiplier"],
                "objective_change": (
                    float(current["objective"])
                    - float(previous["objective"])
                ),
                "primary_distance_change": (
                    float(current["primary_distance"])
                    - float(previous["primary_distance"])
                ),
            }
        )

    return {
        "candidate_id": candidate_id,
        "domain_results": domain_results,
        "domain_transitions": transitions,
        "selected_widest_domain": domain_results[-1],
    }


def _sign_comparisons(case_results: list[dict]) -> list[dict]:
    grouped: dict[tuple[str, float], dict[int, dict]] = {}
    for case in case_results:
        key = (
            str(case["anchor_id"]),
            float(case["historical_nominal_distance"]),
        )
        grouped.setdefault(key, {})[int(case["sign"])] = case

    comparisons: list[dict] = []
    for (anchor, distance), signs in sorted(grouped.items()):
        if set(signs) != {-1, 1}:
            raise ValueError("each sign comparison requires plus and minus")
        minus = signs[-1]
        plus = signs[1]
        candidate_rows: list[dict] = []
        minus_by_candidate = {
            row["candidate_id"]: row
            for row in minus["candidate_results"]
        }
        plus_by_candidate = {
            row["candidate_id"]: row
            for row in plus["candidate_results"]
        }
        for candidate_id in sorted(minus_by_candidate):
            minus_distance = float(
                minus_by_candidate[candidate_id][
                    "selected_widest_domain"
                ]["primary_distance"]
            )
            plus_distance = float(
                plus_by_candidate[candidate_id][
                    "selected_widest_domain"
                ]["primary_distance"]
            )
            candidate_rows.append(
                {
                    "candidate_id": candidate_id,
                    "minus": minus_distance,
                    "plus": plus_distance,
                    "plus_minus_difference": (
                        plus_distance - minus_distance
                    ),
                    "plus_over_minus_ratio": (
                        plus_distance / minus_distance
                        if minus_distance != 0.0
                        else None
                    ),
                }
            )
        comparisons.append(
            {
                "anchor_id": anchor,
                "historical_nominal_distance": distance,
                "candidates": candidate_rows,
            }
        )
    return comparisons


def run_distance_definition_review(
    config: dict,
    departure_config: dict,
    bound_config: dict,
    retained_cases: list[dict],
) -> dict:
    if (
        config["status"]
        != "NON_AUTHORITATIVE_R2_DISTANCE_DEFINITION_REVIEW_DESIGN"
    ):
        raise ValueError("unsupported distance-definition review status")

    forbidden = (
        "stochastic_simulation_allowed",
        "model_fitting_allowed",
        "bootstrap_allowed",
        "operational_fitter_bounds_change_allowed",
        "historical_departure_regeneration_allowed",
        "metric_selection_authorized",
    )
    if any(
        bool(config["execution_boundary"][key])
        for key in forbidden
    ):
        raise ValueError("distance-definition review boundary is violated")

    if len(retained_cases) != int(config["expected_case_count"]):
        raise ValueError("unexpected retained complement-case count")

    design = departure_config["design_cells"]
    belief, accuracy, reward = design_arrays(
        tuple(float(x) for x in design["belief_B"]),
        tuple(float(x) for x in design["accuracy_cue_A"]),
        tuple(float(x) for x in design["reward_context_R"]),
    )
    if len(belief) != int(config["expected_cells_per_case"]):
        raise ValueError("unexpected frozen design-cell count")

    expected_weight = 1.0 / float(len(belief))
    declared_weight = float(
        config["design_weighting"]["weight_per_cell"]
    )
    if abs(declared_weight - expected_weight) > 1e-15:
        raise ValueError("uniform design weight does not match cell count")

    bound_audit = run_projection_bound_sensitivity(
        bound_config,
        departure_config,
        retained_cases,
    )
    wide8_by_case: dict[str, tuple[float, ...]] = {}
    for case in bound_audit["case_results"]:
        wide = next(
            row
            for row in case["bound_results"]
            if row["bound_set_id"] == "WIDE_8X"
        )
        wide8_by_case[str(case["case_id"])] = tuple(
            float(x) for x in wide["selected_parameters"]
        )

    original_starts = [
        tuple(float(x) for x in row)
        for row in departure_config["cbd_projection"][
            "deterministic_starts"
        ]
    ]
    if len(original_starts) != 7:
        raise ValueError("review requires the frozen seven original starts")

    candidate_ids = [
        str(row["id"]) for row in config["candidates"]
    ]
    if candidate_ids != [
        "STABILIZED_UTILITY_RMS",
        "PROBABILITY_RMS",
        "BERNOULLI_KL_GENERAL_TO_CBD",
    ]:
        raise ValueError("distance candidate set changed unexpectedly")

    case_results: list[dict] = []
    selected_cell_rows: list[dict] = []

    for retained in retained_cases:
        case_id = str(retained["case_id"])
        if config["selected_axis"] not in case_id:
            raise ValueError("retained case is outside selected axis")
        coefficients = tuple(
            float(x) for x in retained["general_coefficients"]
        )
        current_parameters = tuple(
            float(x) for x in retained["nearest_cbd_parameters"]
        )
        wide8_parameters = wide8_by_case[case_id]
        starts = [
            *original_starts,
            current_parameters,
            wide8_parameters,
        ]
        if len(starts) != 9:
            raise ValueError("review requires exactly nine common starts")

        eta_general = general_utility(
            coefficients,
            belief,
            accuracy,
            reward,
        )
        candidate_results: list[dict] = []
        selected_probability_surfaces: dict[str, np.ndarray] = {}

        for candidate_id in candidate_ids:
            candidate = _project_candidate(
                candidate_id=candidate_id,
                eta_general=eta_general,
                belief=belief,
                accuracy=accuracy,
                reward=reward,
                starts=starts,
                config=config,
                departure_config=departure_config,
            )
            widest = candidate["selected_widest_domain"]
            closure = _project_candidate_closure(
                candidate_id=candidate_id,
                eta_general=eta_general,
                belief=belief,
                accuracy=accuracy,
                reward=reward,
                logit_starts=starts,
                config=config,
                departure_config=departure_config,
            )
            closure_widest = closure["selected_widest_domain"]
            closure_eta_cbd = _cbd_utility_surface_coordinates(
                tuple(
                    float(x)
                    for x in closure_widest[
                        "selected_surface_coordinates"
                    ]
                ),
                belief,
                accuracy,
                reward,
            )
            logit_eta_cbd = cbd_utility(
                tuple(float(x) for x in widest["selected_parameters"]),
                belief,
                accuracy,
                reward,
            )
            objective_gap = (
                float(widest["objective"])
                - float(closure_widest["objective"])
            )
            equivalence_tolerance = float(
                config["numerical_integrity"][
                    "closure_objective_equivalence_tolerance"
                ]
            )
            if objective_gap < -equivalence_tolerance:
                raise ValueError(
                    "closed-surface projection is worse than finite-logit "
                    "projection beyond numerical tolerance"
                )
            closure["finite_logit_objective_minus_closure_objective"] = (
                objective_gap
            )
            closure[
                "selected_cbd_probability_rms_vs_finite_logit_widest"
            ] = _rms(expit(closure_eta_cbd) - expit(logit_eta_cbd))
            candidate["closure_attainment_diagnostic"] = closure
            candidate_results.append(candidate)
            eta_cbd = cbd_utility(
                tuple(
                    float(x)
                    for x in widest["selected_parameters"]
                ),
                belief,
                accuracy,
                reward,
            )
            selected_probability_surfaces[candidate_id] = expit(
                eta_cbd
            )
            selected_cell_rows.extend(
                _cell_rows(
                    case=retained,
                    candidate_id=candidate_id,
                    eta_general=eta_general,
                    eta_cbd=eta_cbd,
                    belief=belief,
                    accuracy=accuracy,
                    reward=reward,
                )
            )

        projection_comparisons: list[dict] = []
        for left_id, right_id in combinations(candidate_ids, 2):
            projection_comparisons.append(
                {
                    "left_candidate": left_id,
                    "right_candidate": right_id,
                    "selected_cbd_probability_rms": _rms(
                        selected_probability_surfaces[left_id]
                        - selected_probability_surfaces[right_id]
                    ),
                }
            )

        case_results.append(
            {
                "case_id": case_id,
                "anchor_id": str(retained["anchor_id"]),
                "sign": int(retained["sign"]),
                "historical_nominal_distance": float(
                    retained["requested_cbd_rms_distance"]
                ),
                "general_coefficients": [
                    float(x) for x in coefficients
                ],
                "retained_current_parameters": [
                    float(x) for x in current_parameters
                ],
                "reconstructed_wide8_parameters": [
                    float(x) for x in wide8_parameters
                ],
                "candidate_results": candidate_results,
                "candidate_projection_comparisons": (
                    projection_comparisons
                ),
            }
        )

    return {
        "review_id": config["review_id"],
        "status": "NON_AUTHORITATIVE_R2_DISTANCE_DEFINITION_REVIEW_RESULT",
        "authoritative": False,
        "case_count": len(case_results),
        "candidate_count": len(candidate_ids),
        "selected_cell_row_count": len(selected_cell_rows),
        "design_weighting": config["design_weighting"],
        "diagnostic_domain_multipliers": [
            float(x) for x in config["diagnostic_domain_multipliers"]
        ],
        "case_results": case_results,
        "selected_cell_rows": selected_cell_rows,
        "sign_comparisons": _sign_comparisons(case_results),
        "historical_results_rule": (
            "All retained #158/#163/#167 results keep their original bounded "
            "utility-RMS meaning. This deterministic review does not rewrite "
            "historical departure labels or results."
        ),
        "closure_attainment_rule": (
            "Finite CBD logit parameters imply W0,W1 in (0,1). The direct "
            "surface-coordinate diagnostic optimizes the same candidate "
            "objective over the closure W0,W1 in [0,1]. A selected W0/W1 "
            "boundary is reported as NON_ATTAINED_OR_CLOSURE_LIMIT; active "
            "sharing-bias/reward diagnostic bounds are reported separately "
            "as SCIENTIFIC_DOMAIN_UNRESOLVED."
        ),
        "interpretation_boundary": (
            "Deterministic scientific distance-definition comparison only. "
            "Candidate comparison does not select a metric, change operational "
            "fitter bounds, authorize paired bootstrap, freeze bootstrap draws, "
            "evaluation replicates, a core grid or human N, authorize "
            "recruitment, or authorize runtime F1b."
        ),
    }
