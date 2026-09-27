from __future__ import annotations

from math import sqrt

import numpy as np
from scipy.special import expit

from .f1b_r2_controlled_departures import (
    cbd_utility,
    design_arrays,
    generate_controlled_departure_design,
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
    if not 0.0 < epsilon < 0.5:
        raise ValueError("KL clipping epsilon must lie in (0,0.5)")
    p_safe = np.clip(np.asarray(p, dtype=float), epsilon, 1.0 - epsilon)
    q_safe = np.clip(np.asarray(q, dtype=float), epsilon, 1.0 - epsilon)
    return (
        p_safe * np.log(p_safe / q_safe)
        + (1.0 - p_safe)
        * np.log((1.0 - p_safe) / (1.0 - q_safe))
    )


def _saturation_count(probability: np.ndarray, threshold: float) -> int:
    if not 0.0 < threshold < 0.5:
        raise ValueError("saturation thresholds must lie in (0,0.5)")
    values = np.asarray(probability, dtype=float)
    return int(np.sum((values < threshold) | (values > 1.0 - threshold)))


def _metric_summary(
    *,
    case: dict,
    belief: np.ndarray,
    accuracy: np.ndarray,
    reward: np.ndarray,
    thresholds: tuple[float, ...],
    kl_epsilon: float,
) -> tuple[dict, list[dict]]:
    eta_general = general_utility(
        tuple(float(x) for x in case["general_coefficients"]),
        belief,
        accuracy,
        reward,
    )
    eta_cbd = cbd_utility(
        tuple(float(x) for x in case["nearest_cbd_parameters"]),
        belief,
        accuracy,
        reward,
    )
    utility_delta = eta_general - eta_cbd
    p_general = expit(eta_general)
    p_cbd = expit(eta_cbd)
    probability_delta = p_general - p_cbd
    kl = _bernoulli_kl(p_general, p_cbd, epsilon=kl_epsilon)
    variance_general = p_general * (1.0 - p_general)
    variance_cbd = p_cbd * (1.0 - p_cbd)

    summary = {
        "case_id": case["case_id"],
        "anchor_id": case["anchor_id"],
        "axis": case["axis"],
        "sign": int(case["sign"]),
        "requested_cbd_rms_distance": float(
            case["requested_cbd_rms_distance"]
        ),
        "achieved_cbd_rms_distance": float(
            case["achieved_cbd_rms_distance"]
        ),
        "scalar_step": float(case["scalar_step"]),
        "general_coefficients": [
            float(x) for x in case["general_coefficients"]
        ],
        "nearest_cbd_parameters": [
            float(x) for x in case["nearest_cbd_parameters"]
        ],
        "nearest_cbd_start_index": int(case["nearest_cbd_start_index"]),
        "nearest_add_rms_distance": float(
            case["nearest_add_rms_distance"]
        ),
        "recomputed_utility_rms_distance": _rms(utility_delta),
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
        "mean_probability_general": float(np.mean(p_general)),
        "min_probability_general": float(np.min(p_general)),
        "max_probability_general": float(np.max(p_general)),
        "mean_probability_nearest_cbd": float(np.mean(p_cbd)),
        "min_probability_nearest_cbd": float(np.min(p_cbd)),
        "max_probability_nearest_cbd": float(np.max(p_cbd)),
        "mean_bernoulli_variance_general": float(
            np.mean(variance_general)
        ),
        "min_bernoulli_variance_general": float(
            np.min(variance_general)
        ),
        "mean_bernoulli_variance_nearest_cbd": float(
            np.mean(variance_cbd)
        ),
        "min_bernoulli_variance_nearest_cbd": float(np.min(variance_cbd)),
    }
    for threshold in thresholds:
        key = f"saturation_count_{threshold:.2f}"
        summary[key] = _saturation_count(p_general, threshold)

    cells: list[dict] = []
    for index in range(len(belief)):
        cells.append(
            {
                "case_id": case["case_id"],
                "anchor_id": case["anchor_id"],
                "sign": int(case["sign"]),
                "requested_cbd_rms_distance": float(
                    case["requested_cbd_rms_distance"]
                ),
                "cell_index": int(index),
                "belief_B": float(belief[index]),
                "accuracy_cue_A": float(accuracy[index]),
                "reward_context_R": float(reward[index]),
                "general_utility": float(eta_general[index]),
                "nearest_cbd_utility": float(eta_cbd[index]),
                "signed_utility_difference": float(utility_delta[index]),
                "absolute_utility_difference": float(
                    abs(utility_delta[index])
                ),
                "general_probability": float(p_general[index]),
                "nearest_cbd_probability": float(p_cbd[index]),
                "signed_probability_difference": float(
                    probability_delta[index]
                ),
                "absolute_probability_difference": float(
                    abs(probability_delta[index])
                ),
                "bernoulli_kl_general_to_nearest_cbd": float(kl[index]),
                "bernoulli_variance_general": float(
                    variance_general[index]
                ),
                "bernoulli_variance_nearest_cbd": float(
                    variance_cbd[index]
                ),
            }
        )
    return summary, cells


def _sign_comparisons(
    summaries: list[dict],
    metric_names: tuple[str, ...],
) -> list[dict]:
    grouped: dict[tuple[str, float], dict[int, dict]] = {}
    for row in summaries:
        key = (
            str(row["anchor_id"]),
            float(row["requested_cbd_rms_distance"]),
        )
        grouped.setdefault(key, {})[int(row["sign"])] = row

    comparisons: list[dict] = []
    for (anchor_id, distance), signs in sorted(grouped.items()):
        if set(signs) != {-1, 1}:
            raise ValueError(
                "each geometry comparison requires both departure signs"
            )
        minus = signs[-1]
        plus = signs[1]
        metrics: dict[str, dict] = {}
        for name in metric_names:
            minus_value = float(minus[name])
            plus_value = float(plus[name])
            metrics[name] = {
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
                "anchor_id": anchor_id,
                "requested_cbd_rms_distance": distance,
                "metrics": metrics,
            }
        )
    return comparisons


def run_complement_sign_geometry_diagnostic(
    config: dict,
    departure_config: dict,
) -> dict:
    if (
        config["status"]
        != "NON_AUTHORITATIVE_R2_COMPLEMENT_SIGN_GEOMETRY_DESIGN"
    ):
        raise ValueError("unsupported complement sign geometry status")

    boundary = config["execution_boundary"]
    if boundary["stochastic_simulation_allowed"]:
        raise ValueError("geometry diagnostic must not authorize simulation")
    if boundary["model_fitting_allowed"]:
        raise ValueError("geometry diagnostic must not authorize fitting")

    design_result = generate_controlled_departure_design(departure_config)
    selected_axis = str(config["selected_axis"])
    cases = [
        case
        for case in design_result["cases"]
        if case["axis"] == selected_axis
    ]
    if len(cases) != int(config["expected_case_count"]):
        raise ValueError("unexpected selected complement case count")

    design = departure_config["design_cells"]
    belief, accuracy, reward = design_arrays(
        tuple(float(x) for x in design["belief_B"]),
        tuple(float(x) for x in design["accuracy_cue_A"]),
        tuple(float(x) for x in design["reward_context_R"]),
    )
    expected_cells = int(config["expected_cells_per_case"])
    if len(belief) != expected_cells:
        raise ValueError("unexpected frozen design-cell count")

    thresholds = tuple(
        float(x) for x in config["probability_saturation_thresholds"]
    )
    kl_epsilon = float(config["kl_clip_epsilon"])

    summaries: list[dict] = []
    cell_rows: list[dict] = []
    for case in cases:
        summary, cells = _metric_summary(
            case=case,
            belief=belief,
            accuracy=accuracy,
            reward=reward,
            thresholds=thresholds,
            kl_epsilon=kl_epsilon,
        )
        summaries.append(summary)
        cell_rows.extend(cells)

    metric_names = tuple(str(x) for x in config["comparisons"]["metrics"])
    comparisons = _sign_comparisons(summaries, metric_names)

    return {
        "diagnostic_id": config["diagnostic_id"],
        "status": "NON_AUTHORITATIVE_R2_COMPLEMENT_SIGN_GEOMETRY_RESULT",
        "authoritative": False,
        "selected_axis": selected_axis,
        "case_count": len(summaries),
        "cells_per_case": expected_cells,
        "cell_row_count": len(cell_rows),
        "case_summaries": summaries,
        "cell_rows": cell_rows,
        "sign_comparisons": comparisons,
        "interpretation_boundary": (
            "Deterministic geometry diagnostic only. Probability/KL/information "
            "metrics do not replace the frozen utility-RMS departure definition, "
            "do not validate a final test, do not freeze bootstrap draws or "
            "evaluation replicates, do not freeze human N, and do not authorize "
            "recruitment or runtime F1b."
        ),
    }
