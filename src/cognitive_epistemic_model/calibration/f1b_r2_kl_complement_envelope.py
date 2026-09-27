from __future__ import annotations

from collections import Counter
from math import isclose
from typing import Iterable

import numpy as np
from scipy.special import expit

from .f1b_r2_controlled_departures import (
    DepartureAxis,
    departure_direction,
    design_arrays,
    general_utility,
)
from .f1b_r2_distance_definition_review import (
    project_general_surface_to_cbd_closure,
)
from .f1b_r2_restriction_recovery import (
    cbd_fit_to_general_coefficients,
)


class ComplementKLEnvelopeError(RuntimeError):
    pass


def _validate_config(
    config: dict,
    kl_config: dict,
    review_config: dict,
) -> None:
    if (
        config["status"]
        != "NON_AUTHORITATIVE_KL_COMPLEMENT_ENVELOPE_DIAGNOSTIC"
    ):
        raise ValueError("unsupported complement KL envelope status")
    if config["selected_axis"] != "COMPLEMENT_RELATION_VIOLATION":
        raise ValueError("complement envelope axis changed unexpectedly")
    if [float(x) for x in config["frozen_targets"]] != [0.001, 0.005, 0.01]:
        raise ValueError("frozen v1 target grid changed unexpectedly")

    grid = config["scalar_grid"]
    if (
        float(grid["start"]) != 0.0
        or float(grid["step"]) != 0.025
        or float(grid["maximum"]) != 20.0
        or int(grid["expected_point_count"]) != 801
    ):
        raise ValueError("frozen complement scalar grid changed unexpectedly")

    scientific = config["scientific_projection"]
    if scientific["candidate_id"] != "BERNOULLI_KL_GENERAL_TO_CBD":
        raise ValueError("scientific KL candidate changed unexpectedly")
    if scientific["direction"] != "GENERAL_TO_CBD":
        raise ValueError("scientific KL direction changed unexpectedly")
    if [int(x) for x in scientific["diagnostic_domain_multipliers"]] != [
        int(x) for x in review_config["diagnostic_domain_multipliers"]
    ]:
        raise ValueError("scientific projection domains differ from #171")

    kl_scientific = kl_config["scientific_projection"]
    if kl_scientific["candidate_id"] != scientific["candidate_id"]:
        raise ValueError("envelope candidate differs from KL v1")
    if [float(x) for x in kl_config["target_mean_bernoulli_kl"]] != [
        float(x) for x in config["frozen_targets"]
    ]:
        raise ValueError("envelope target grid differs from KL v1")

    forbidden = (
        "v1_target_revision_allowed",
        "scalar_range_revision_allowed",
        "ray_revision_allowed",
        "stochastic_simulation_allowed",
        "bootstrap_allowed",
        "paired_bootstrap_authorized",
    )
    if any(bool(config["execution_boundary"][key]) for key in forbidden):
        raise ValueError("complement envelope execution boundary violated")


def _design_arrays(kl_config: dict) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    design = kl_config["design_cells"]
    return design_arrays(
        tuple(float(x) for x in design["belief_B"]),
        tuple(float(x) for x in design["accuracy_cue_A"]),
        tuple(float(x) for x in design["reward_context_R"]),
    )


def _projection_starts(
    historical_departure_config: dict,
    anchor_parameters: tuple[float, ...],
) -> list[tuple[float, ...]]:
    starts = [
        tuple(float(x) for x in row)
        for row in historical_departure_config["cbd_projection"][
            "deterministic_starts"
        ]
    ]
    if len(starts) != 7:
        raise ValueError("envelope diagnostic requires seven frozen CBD starts")
    starts.append(tuple(float(x) for x in anchor_parameters))
    return starts


def _scalar_grid(config: dict) -> list[float]:
    raw = config["scalar_grid"]
    start = float(raw["start"])
    step = float(raw["step"])
    maximum = float(raw["maximum"])
    expected = int(raw["expected_point_count"])
    count = int(round((maximum - start) / step)) + 1
    values = [start + index * step for index in range(count)]
    tolerance = float(
        config["numerical_integrity"]["scalar_grid_tolerance"]
    )
    if len(values) != expected:
        raise ValueError("scalar grid point count does not match frozen design")
    if not isclose(values[-1], maximum, rel_tol=0.0, abs_tol=tolerance):
        raise ValueError("scalar grid does not terminate at frozen maximum")
    values[-1] = maximum
    return values


def _saturation_counts(probabilities: np.ndarray) -> tuple[int, int]:
    p = np.asarray(probabilities, dtype=float)
    return (
        int(np.sum((p < 0.05) | (p > 0.95))),
        int(np.sum((p < 0.10) | (p > 0.90))),
    )


def _project_kl_closure(
    coefficients: np.ndarray,
    *,
    belief: np.ndarray,
    accuracy: np.ndarray,
    reward: np.ndarray,
    starts: list[tuple[float, ...]],
    review_config: dict,
    historical_departure_config: dict,
) -> dict:
    return project_general_surface_to_cbd_closure(
        candidate_id="BERNOULLI_KL_GENERAL_TO_CBD",
        general_coefficients=coefficients,
        belief=belief,
        accuracy=accuracy,
        reward=reward,
        logit_starts=starts,
        review_config=review_config,
        departure_config=historical_departure_config,
    )


def _point_summary(
    *,
    scalar: float,
    coefficients: np.ndarray,
    projection: dict,
    belief: np.ndarray,
    accuracy: np.ndarray,
    reward: np.ndarray,
) -> dict:
    widest = projection["selected_widest_domain"]
    metrics = widest["surface_metrics"]
    eta_general = general_utility(
        coefficients,
        belief,
        accuracy,
        reward,
    )
    p_general = expit(eta_general)
    outside_005, outside_010 = _saturation_counts(p_general)
    return {
        "scalar": float(scalar),
        "mean_bernoulli_kl": float(widest["primary_distance"]),
        "attainment_status": str(projection["attainment_status"]),
        "closure_boundary_components": [
            str(x) for x in projection["closure_boundary_components"]
        ],
        "scientific_domain_components": [
            str(x) for x in projection["scientific_domain_components"]
        ],
        "selected_cbd_surface_coordinates": [
            float(x)
            for x in widest["selected_surface_coordinates"]
        ],
        "utility_rms_diagnostic": float(metrics["utility_rms_distance"]),
        "probability_rms_diagnostic": float(
            metrics["probability_rms_distance"]
        ),
        "information_weighted_logit_distance": float(
            metrics["information_weighted_logit_distance"]
        ),
        "min_probability_general": float(metrics["min_probability_general"]),
        "max_probability_general": float(metrics["max_probability_general"]),
        "min_probability_cbd": float(metrics["min_probability_cbd"]),
        "max_probability_cbd": float(metrics["max_probability_cbd"]),
        "generator_outside_005_095_count": outside_005,
        "generator_outside_010_090_count": outside_010,
    }


def _first_crossing(
    profile: list[dict],
    target: float,
    *,
    tolerance: float,
) -> dict:
    for previous, current in zip(profile, profile[1:], strict=False):
        left = float(previous["mean_bernoulli_kl"])
        right = float(current["mean_bernoulli_kl"])
        if left < target - tolerance and right >= target - tolerance:
            return {
                "target": float(target),
                "classification": "TARGET_ATTAINABLE_WITHIN_V1_RANGE",
                "first_crossing_bracket": [
                    float(previous["scalar"]),
                    float(current["scalar"]),
                ],
                "bracket_kl": [left, right],
                "first_scalar_at_or_above_target": float(current["scalar"]),
            }

    maximum_row = max(
        profile,
        key=lambda row: float(row["mean_bernoulli_kl"]),
    )
    maximum = float(maximum_row["mean_bernoulli_kl"])
    terminal = float(profile[-1]["mean_bernoulli_kl"])
    if target > maximum + tolerance:
        classification = "TARGET_ABOVE_RAY_ENVELOPE_WITHIN_V1_RANGE"
    else:
        classification = "NON_MONOTONE_NO_FIRST_CROSSING_AT_GRID_RESOLUTION"
    return {
        "target": float(target),
        "classification": classification,
        "first_crossing_bracket": None,
        "bracket_kl": None,
        "first_scalar_at_or_above_target": None,
        "maximum_observed_mean_kl": maximum,
        "scalar_at_maximum": float(maximum_row["scalar"]),
        "terminal_mean_kl_at_scalar_20": terminal,
    }


def _reversal_rows(profile: list[dict], *, tolerance: float) -> list[dict]:
    changes: list[tuple[int, int]] = []
    previous_sign = 0
    previous_index = 0
    for index in range(1, len(profile)):
        delta = (
            float(profile[index]["mean_bernoulli_kl"])
            - float(profile[index - 1]["mean_bernoulli_kl"])
        )
        sign = 1 if delta > tolerance else (-1 if delta < -tolerance else 0)
        if sign == 0:
            continue
        if previous_sign != 0 and sign != previous_sign:
            changes.append((previous_index, index))
        previous_sign = sign
        previous_index = index
    return [
        {
            "from_scalar": float(profile[left]["scalar"]),
            "to_scalar": float(profile[right]["scalar"]),
            "mean_kl_before": float(profile[left]["mean_bernoulli_kl"]),
            "mean_kl_after": float(profile[right]["mean_bernoulli_kl"]),
        }
        for left, right in changes
    ]


def scan_complement_kl_ray(
    config: dict,
    kl_config: dict,
    review_config: dict,
    historical_departure_config: dict,
    *,
    anchor_id: str,
    sign: int,
) -> dict:
    _validate_config(config, kl_config, review_config)
    if anchor_id not in config["anchors"]:
        raise ValueError("unsupported complement envelope anchor")
    if sign not in (-1, 1):
        raise ValueError("complement envelope sign must be -1 or +1")

    anchors = kl_config["anchors"]["cbd"]
    if anchor_id not in anchors:
        raise ValueError("complement envelope anchor absent from KL v1")
    anchor_parameters = tuple(float(x) for x in anchors[anchor_id])
    anchor_general = np.asarray(
        cbd_fit_to_general_coefficients(anchor_parameters),
        dtype=float,
    )
    belief, accuracy, reward = _design_arrays(kl_config)
    direction = departure_direction(
        DepartureAxis.COMPLEMENT_RELATION_VIOLATION,
        belief=belief,
        accuracy=accuracy,
        reward=reward,
    )
    starts = _projection_starts(
        historical_departure_config,
        anchor_parameters,
    )

    profile: list[dict] = []
    for scalar in _scalar_grid(config):
        coefficients = anchor_general + float(sign) * scalar * direction
        try:
            projection = _project_kl_closure(
                coefficients,
                belief=belief,
                accuracy=accuracy,
                reward=reward,
                starts=starts,
                review_config=review_config,
                historical_departure_config=historical_departure_config,
            )
        except ValueError as exc:
            raise ComplementKLEnvelopeError(
                "CBD closure projection failed at "
                f"anchor={anchor_id} sign={sign} scalar={scalar:.17g}: {exc}"
            ) from exc
        point = _point_summary(
            scalar=scalar,
            coefficients=coefficients,
            projection=projection,
            belief=belief,
            accuracy=accuracy,
            reward=reward,
        )
        if point["scientific_domain_components"]:
            raise ComplementKLEnvelopeError(
                "SCIENTIFIC_DOMAIN_UNRESOLVED at "
                f"{anchor_id} sign={sign} scalar={scalar}"
            )
        profile.append(point)

    if len(profile) != int(config["scalar_grid"]["expected_point_count"]):
        raise ComplementKLEnvelopeError(
            "complement KL profile has unexpected point count"
        )

    tolerance = float(
        config["numerical_integrity"]["monotonicity_tolerance"]
    )
    target_tolerance = float(
        config["numerical_integrity"]["target_comparison_tolerance"]
    )
    maximum_row = max(
        profile,
        key=lambda row: float(row["mean_bernoulli_kl"]),
    )
    reversals = _reversal_rows(profile, tolerance=tolerance)
    monotone = all(
        float(current["mean_bernoulli_kl"])
        >= float(previous["mean_bernoulli_kl"]) - tolerance
        for previous, current in zip(profile, profile[1:], strict=False)
    )
    first_closure = next(
        (
            row
            for row in profile
            if row["closure_boundary_components"]
            or row["attainment_status"] == "NON_ATTAINED_OR_CLOSURE_LIMIT"
        ),
        None,
    )
    attainment_counts = Counter(
        str(row["attainment_status"]) for row in profile
    )

    target_results = [
        _first_crossing(
            profile,
            float(target),
            tolerance=target_tolerance,
        )
        for target in config["frozen_targets"]
    ]
    maximum = float(maximum_row["mean_bernoulli_kl"])
    terminal = float(profile[-1]["mean_bernoulli_kl"])
    for result in target_results:
        if result["first_crossing_bracket"] is None:
            result["non_monotone_after_maximum"] = any(
                float(row["mean_bernoulli_kl"]) < maximum - tolerance
                for row in profile[
                    profile.index(maximum_row) + 1 :
                ]
            )

    return {
        "diagnostic_id": str(config["diagnostic_id"]),
        "status": "NON_AUTHORITATIVE_KL_COMPLEMENT_ENVELOPE_RAY_RESULT",
        "authoritative": False,
        "anchor_id": str(anchor_id),
        "sign": int(sign),
        "point_count": len(profile),
        "scalar_start": float(profile[0]["scalar"]),
        "scalar_end": float(profile[-1]["scalar"]),
        "maximum_mean_bernoulli_kl": maximum,
        "scalar_at_maximum": float(maximum_row["scalar"]),
        "terminal_mean_bernoulli_kl": terminal,
        "monotone_non_decreasing": bool(monotone),
        "direction_reversal_count": len(reversals),
        "direction_reversals": reversals,
        "attainment_counts": dict(attainment_counts),
        "first_closure_scalar": (
            float(first_closure["scalar"])
            if first_closure is not None
            else None
        ),
        "target_results": target_results,
        "profile": profile,
    }


def _selector(result: dict) -> tuple[str, int]:
    return str(result["anchor_id"]), int(result["sign"])


def combine_complement_kl_envelope_rays(
    rays: Iterable[dict],
    config: dict,
) -> dict:
    values = list(rays)
    expected = [
        (str(anchor), int(sign))
        for anchor in config["anchors"]
        for sign in config["signs"]
    ]
    by_selector: dict[tuple[str, int], dict] = {}
    for result in values:
        selector = _selector(result)
        if selector in by_selector:
            raise ValueError(f"duplicate complement envelope ray: {selector}")
        if (
            result["diagnostic_id"] != str(config["diagnostic_id"])
            or result["status"]
            != "NON_AUTHORITATIVE_KL_COMPLEMENT_ENVELOPE_RAY_RESULT"
            or result["authoritative"] is not False
        ):
            raise ValueError("incompatible complement envelope ray result")
        if int(result["point_count"]) != int(
            config["scalar_grid"]["expected_point_count"]
        ):
            raise ValueError("complement envelope ray has incomplete coverage")
        by_selector[selector] = result

    if set(by_selector) != set(expected):
        missing = [selector for selector in expected if selector not in by_selector]
        extra = [selector for selector in by_selector if selector not in expected]
        raise ValueError(
            "complement envelope coverage is incomplete "
            f"(missing={missing}, extra={extra})"
        )

    ordered = [by_selector[selector] for selector in expected]
    return {
        "diagnostic_id": str(config["diagnostic_id"]),
        "status": "NON_AUTHORITATIVE_KL_COMPLEMENT_ENVELOPE_RESULT",
        "authoritative": False,
        "ray_count": len(ordered),
        "point_count": sum(int(row["point_count"]) for row in ordered),
        "rays": ordered,
        "interpretation_boundary": (
            "Deterministic attainable-envelope diagnostic for the frozen "
            "KL v1 complement rays only. It does not revise the v1 target "
            "grid, scalar range, ray, stochastic design, or human/runtime gates."
        ),
    }


def run_complement_kl_envelope_diagnostic(
    config: dict,
    kl_config: dict,
    review_config: dict,
    historical_departure_config: dict,
) -> dict:
    rays = [
        scan_complement_kl_ray(
            config,
            kl_config,
            review_config,
            historical_departure_config,
            anchor_id=str(anchor),
            sign=int(sign),
        )
        for anchor in config["anchors"]
        for sign in config["signs"]
    ]
    return combine_complement_kl_envelope_rays(rays, config)
