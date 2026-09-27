from __future__ import annotations

from math import sqrt

import numpy as np
from scipy.optimize import minimize
from scipy.special import expit

from .f1b_r2_controlled_departures import (
    cbd_utility,
    design_arrays,
    general_utility,
)


def _rms(values: np.ndarray) -> float:
    array = np.asarray(values, dtype=float)
    return float(sqrt(float(np.mean(array**2))))


def _bernoulli_kl(
    p: np.ndarray,
    q: np.ndarray,
    *,
    epsilon: float,
) -> np.ndarray:
    p_safe = np.clip(np.asarray(p, dtype=float), epsilon, 1.0 - epsilon)
    q_safe = np.clip(np.asarray(q, dtype=float), epsilon, 1.0 - epsilon)
    return (
        p_safe * np.log(p_safe / q_safe)
        + (1.0 - p_safe)
        * np.log((1.0 - p_safe) / (1.0 - q_safe))
    )


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
        raise ValueError("bound multiplier must be positive")
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


def _projection_for_bounds(
    *,
    general_coefficients: tuple[float, ...],
    retained_current_parameters: tuple[float, ...],
    belief: np.ndarray,
    accuracy: np.ndarray,
    reward: np.ndarray,
    departure_config: dict,
    multiplier: float,
    optimization: dict,
    bound_activity_tolerance: float,
) -> dict:
    target = general_utility(
        general_coefficients,
        belief,
        accuracy,
        reward,
    )
    bounds = _scaled_bounds(departure_config, multiplier)
    starts = [
        tuple(float(x) for x in start)
        for start in departure_config["cbd_projection"]["deterministic_starts"]
    ]
    if optimization["include_retained_current_solution_as_common_start"]:
        starts.append(retained_current_parameters)

    records: list[dict] = []
    for index, start in enumerate(starts):
        x0 = np.asarray(start, dtype=float)
        if x0.shape != (4,):
            raise ValueError("projection starts must contain four parameters")
        for value, (low, high) in zip(x0, bounds, strict=True):
            if not float(low) <= float(value) <= float(high):
                raise ValueError("common projection start lies outside bounds")

        def objective(parameters: np.ndarray) -> float:
            delta = (
                cbd_utility(
                    parameters,
                    belief,
                    accuracy,
                    reward,
                )
                - target
            )
            return float(np.mean(delta**2))

        result = minimize(
            objective,
            x0=x0,
            method=str(optimization["method"]),
            bounds=bounds,
            options={
                "maxiter": int(optimization["maxiter"]),
                "ftol": float(optimization["ftol"]),
                "maxls": int(optimization["maxls"]),
            },
        )
        record = {
            "start_index": int(index),
            "initial_parameters": [float(x) for x in x0],
            "success": bool(result.success),
            "status": int(result.status),
            "message": str(result.message),
            "objective": (
                float(result.fun) if np.isfinite(result.fun) else None
            ),
            "rms_distance": (
                float(sqrt(max(0.0, float(result.fun))))
                if np.isfinite(result.fun)
                else None
            ),
            "parameters": (
                [float(x) for x in result.x]
                if np.all(np.isfinite(result.x))
                else None
            ),
        }
        records.append(record)

    successful = [
        record
        for record in records
        if record["success"]
        and record["objective"] is not None
        and record["parameters"] is not None
    ]
    if not successful:
        raise RuntimeError("all projection starts failed for a bound set")

    selected = min(successful, key=lambda row: float(row["objective"]))
    parameters = np.asarray(selected["parameters"], dtype=float)
    eta_general = target
    eta_cbd = cbd_utility(
        parameters,
        belief,
        accuracy,
        reward,
    )
    p_general = expit(eta_general)
    p_cbd = expit(eta_cbd)
    probability_delta = p_general - p_cbd
    utility_delta = eta_general - eta_cbd
    kl = _bernoulli_kl(
        p_general,
        p_cbd,
        epsilon=float(optimization["kl_clip_epsilon"]),
    )
    variance_cbd = p_cbd * (1.0 - p_cbd)

    return {
        "multiplier": float(multiplier),
        "bounds": [
            [float(low), float(high)] for low, high in bounds
        ],
        "selected_start_index": int(selected["start_index"]),
        "selected_parameters": [float(x) for x in parameters],
        "objective": float(selected["objective"]),
        "nearest_cbd_rms_distance": float(selected["rms_distance"]),
        "active_bounds": _active_bounds(
            parameters,
            bounds,
            tolerance=bound_activity_tolerance,
        ),
        "successful_start_count": len(successful),
        "failed_start_count": len(records) - len(successful),
        "start_records": records,
        "probability_rms_distance": _rms(probability_delta),
        "mean_absolute_probability_difference": float(
            np.mean(np.abs(probability_delta))
        ),
        "max_absolute_probability_difference": float(
            np.max(np.abs(probability_delta))
        ),
        "mean_bernoulli_kl_general_to_nearest_cbd": float(np.mean(kl)),
        "max_bernoulli_kl_general_to_nearest_cbd": float(np.max(kl)),
        "information_weighted_logit_distance": _rms(
            np.sqrt(variance_cbd) * utility_delta
        ),
        "min_probability_nearest_cbd": float(np.min(p_cbd)),
        "max_probability_nearest_cbd": float(np.max(p_cbd)),
        "mean_bernoulli_variance_nearest_cbd": float(
            np.mean(variance_cbd)
        ),
        "min_bernoulli_variance_nearest_cbd": float(np.min(variance_cbd)),
    }


def _relative_change(current: float, previous: float) -> float | None:
    if previous == 0.0:
        return None
    return float((current - previous) / abs(previous))


def _sign_comparisons(case_results: list[dict]) -> list[dict]:
    grouped: dict[tuple[str, float, str], dict[int, dict]] = {}
    for case in case_results:
        for projection in case["bound_results"]:
            key = (
                str(case["anchor_id"]),
                float(case["requested_cbd_rms_distance"]),
                str(projection["bound_set_id"]),
            )
            grouped.setdefault(key, {})[int(case["sign"])] = projection

    comparisons: list[dict] = []
    metrics = (
        "nearest_cbd_rms_distance",
        "probability_rms_distance",
        "mean_bernoulli_kl_general_to_nearest_cbd",
        "information_weighted_logit_distance",
    )
    for (anchor, distance, bound_set), signs in sorted(grouped.items()):
        if set(signs) != {-1, 1}:
            raise ValueError("each sign comparison requires plus and minus")
        minus = signs[-1]
        plus = signs[1]
        metric_rows: dict[str, dict] = {}
        for metric in metrics:
            minus_value = float(minus[metric])
            plus_value = float(plus[metric])
            metric_rows[metric] = {
                "minus": minus_value,
                "plus": plus_value,
                "plus_minus_difference": plus_value - minus_value,
                "plus_over_minus_ratio": (
                    plus_value / minus_value
                    if minus_value != 0.0
                    else None
                ),
            }
        comparisons.append(
            {
                "anchor_id": anchor,
                "requested_cbd_rms_distance": distance,
                "bound_set_id": bound_set,
                "metrics": metric_rows,
                "minus_active_bounds": minus["active_bounds"],
                "plus_active_bounds": plus["active_bounds"],
            }
        )
    return comparisons


def run_projection_bound_sensitivity(
    config: dict,
    departure_config: dict,
    retained_cases: list[dict],
) -> dict:
    if (
        config["status"]
        != "NON_AUTHORITATIVE_R2_PROJECTION_BOUND_SENSITIVITY_DESIGN"
    ):
        raise ValueError("unsupported projection-bound sensitivity status")

    boundary = config["execution_boundary"]
    forbidden = (
        "stochastic_simulation_allowed",
        "model_fitting_allowed",
        "paired_bootstrap_stage_allowed",
        "operational_fitter_bounds_change_allowed",
        "departure_regeneration_allowed",
    )
    if any(bool(boundary[key]) for key in forbidden):
        raise ValueError("deterministic sensitivity boundary is violated")

    if len(retained_cases) != int(config["expected_case_count"]):
        raise ValueError("unexpected retained complement-case count")

    design = departure_config["design_cells"]
    belief, accuracy, reward = design_arrays(
        tuple(float(x) for x in design["belief_B"]),
        tuple(float(x) for x in design["accuracy_cue_A"]),
        tuple(float(x) for x in design["reward_context_R"]),
    )
    if len(belief) != int(config["expected_cells_per_case"]):
        raise ValueError("unexpected design-cell count")

    bound_sets = config["bound_sets"]
    if [float(row["multiplier"]) for row in bound_sets] != [
        1.0,
        2.0,
        4.0,
        8.0,
    ]:
        raise ValueError("bound sensitivity grid must be 1x/2x/4x/8x")

    optimization = dict(config["optimization"])
    optimization["kl_clip_epsilon"] = float(config["kl_clip_epsilon"])
    tolerance = float(config["bound_activity_tolerance"])
    nested_tolerance = float(config["nested_objective_tolerance"])

    case_results: list[dict] = []
    for retained in retained_cases:
        if config["selected_axis"] not in str(retained["case_id"]):
            raise ValueError("retained case is outside the selected axis")
        coefficients = tuple(
            float(x) for x in retained["general_coefficients"]
        )
        current_parameters = tuple(
            float(x) for x in retained["nearest_cbd_parameters"]
        )
        eta_general = general_utility(
            coefficients,
            belief,
            accuracy,
            reward,
        )
        p_general = expit(eta_general)
        variance_general = p_general * (1.0 - p_general)

        results: list[dict] = []
        for bound_set in bound_sets:
            projection = _projection_for_bounds(
                general_coefficients=coefficients,
                retained_current_parameters=current_parameters,
                belief=belief,
                accuracy=accuracy,
                reward=reward,
                departure_config=departure_config,
                multiplier=float(bound_set["multiplier"]),
                optimization=optimization,
                bound_activity_tolerance=tolerance,
            )
            projection["bound_set_id"] = str(bound_set["id"])
            results.append(projection)

        for previous, current in zip(results, results[1:], strict=False):
            if (
                float(current["objective"])
                > float(previous["objective"]) + nested_tolerance
            ):
                raise ValueError(
                    "nested projection objective increased under wider bounds"
                )

        current_reference = np.asarray(
            results[0]["selected_parameters"],
            dtype=float,
        )
        for result in results:
            selected = np.asarray(
                result["selected_parameters"],
                dtype=float,
            )
            result["parameter_distance_from_current_1x"] = float(
                np.linalg.norm(selected - current_reference)
            )

        transitions: list[dict] = []
        for previous, current in zip(results, results[1:], strict=False):
            previous_rms = float(previous["nearest_cbd_rms_distance"])
            current_rms = float(current["nearest_cbd_rms_distance"])
            transitions.append(
                {
                    "from_bound_set": previous["bound_set_id"],
                    "to_bound_set": current["bound_set_id"],
                    "rms_absolute_change": current_rms - previous_rms,
                    "rms_relative_change": _relative_change(
                        current_rms,
                        previous_rms,
                    ),
                }
            )

        case_results.append(
            {
                "case_id": str(retained["case_id"]),
                "anchor_id": str(retained["anchor_id"]),
                "sign": int(retained["sign"]),
                "requested_cbd_rms_distance": float(
                    retained["requested_cbd_rms_distance"]
                ),
                "retained_current_achieved_cbd_rms_distance": float(
                    retained["achieved_cbd_rms_distance"]
                ),
                "general_coefficients": [float(x) for x in coefficients],
                "retained_current_nearest_cbd_parameters": [
                    float(x) for x in current_parameters
                ],
                "mean_probability_general": float(np.mean(p_general)),
                "min_probability_general": float(np.min(p_general)),
                "max_probability_general": float(np.max(p_general)),
                "mean_bernoulli_variance_general": float(
                    np.mean(variance_general)
                ),
                "min_bernoulli_variance_general": float(
                    np.min(variance_general)
                ),
                "bound_results": results,
                "bound_transitions": transitions,
                "current_1x_reproduction_rms_delta": (
                    float(results[0]["nearest_cbd_rms_distance"])
                    - float(retained["achieved_cbd_rms_distance"])
                ),
                "wide_8x_boundary_active": bool(
                    results[-1]["active_bounds"]
                ),
            }
        )

    return {
        "diagnostic_id": config["diagnostic_id"],
        "status": "NON_AUTHORITATIVE_R2_PROJECTION_BOUND_SENSITIVITY_RESULT",
        "authoritative": False,
        "case_count": len(case_results),
        "bound_set_count": len(bound_sets),
        "case_bound_result_count": len(case_results) * len(bound_sets),
        "case_results": case_results,
        "sign_comparisons": _sign_comparisons(case_results),
        "interpretation_boundary": (
            "Deterministic projection-bound sensitivity only. Fixed retained "
            "general surfaces are not regenerated. Diagnostic widened bounds "
            "do not change the operational fitter, do not authorize paired "
            "bootstrap, do not freeze bootstrap draws, evaluation replicates, "
            "the core grid or human N, and do not authorize recruitment or "
            "runtime F1b."
        ),
    }
