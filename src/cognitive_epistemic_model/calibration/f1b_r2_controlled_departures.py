from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from math import sqrt

import numpy as np
from scipy.optimize import brentq, minimize

from .f1b_r2_restriction_recovery import (
    add_fit_to_general_coefficients,
    cbd_fit_to_general_coefficients,
)


class DepartureAxis(str, Enum):
    STANDALONE_ACCURACY_MAIN_EFFECT = "STANDALONE_ACCURACY_MAIN_EFFECT"
    COMPLEMENT_RELATION_VIOLATION = "COMPLEMENT_RELATION_VIOLATION"
    COMBINED_VIOLATION = "COMBINED_VIOLATION"


class DepartureGenerationError(RuntimeError):
    pass


@dataclass(frozen=True)
class ProjectionResult:
    coefficients: tuple[float, ...]
    rms_distance: float
    converged: bool
    start_index: int
    objective: float


@dataclass(frozen=True)
class DepartureCase:
    case_id: str
    anchor_id: str
    anchor_family: str
    axis: str
    sign: int
    requested_cbd_rms_distance: float
    achieved_cbd_rms_distance: float
    cbd_distance_error: float
    nearest_add_rms_distance: float
    scalar_step: float
    general_coefficients: tuple[float, ...]
    nearest_cbd_parameters: tuple[float, ...]
    nearest_cbd_start_index: int
    nearest_add_coefficients: tuple[float, ...]
    add_compatibility_expected: bool
    add_compatibility_pass: bool


def design_arrays(
    belief_levels: tuple[float, ...],
    accuracy_levels: tuple[float, ...],
    reward_levels: tuple[float, ...],
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    from itertools import product

    cells = np.asarray(
        list(product(belief_levels, accuracy_levels, reward_levels)),
        dtype=float,
    )
    return cells[:, 0], cells[:, 1], cells[:, 2]


def general_design_matrix(
    belief: np.ndarray,
    accuracy: np.ndarray,
    reward: np.ndarray,
) -> np.ndarray:
    centered = 2.0 * np.asarray(belief, dtype=float) - 1.0
    a = np.asarray(accuracy, dtype=float)
    r = np.asarray(reward, dtype=float)
    return np.column_stack(
        (
            np.ones(centered.size),
            centered,
            a,
            r,
            a * centered,
            a * r,
        )
    )


def general_utility(
    coefficients: tuple[float, ...] | np.ndarray,
    belief: np.ndarray,
    accuracy: np.ndarray,
    reward: np.ndarray,
) -> np.ndarray:
    beta = np.asarray(coefficients, dtype=float)
    if beta.shape != (6,):
        raise ValueError("AP-GENERAL coefficients must have length six")
    return general_design_matrix(belief, accuracy, reward) @ beta


def rms_distance(left: np.ndarray, right: np.ndarray) -> float:
    delta = np.asarray(left, dtype=float) - np.asarray(right, dtype=float)
    return float(sqrt(float(np.mean(delta**2))))


def _cbd_general_coefficients(
    parameters: tuple[float, ...] | np.ndarray,
) -> np.ndarray:
    return np.asarray(
        cbd_fit_to_general_coefficients(tuple(float(x) for x in parameters)),
        dtype=float,
    )


def cbd_utility(
    parameters: tuple[float, ...] | np.ndarray,
    belief: np.ndarray,
    accuracy: np.ndarray,
    reward: np.ndarray,
) -> np.ndarray:
    return general_utility(
        _cbd_general_coefficients(parameters),
        belief,
        accuracy,
        reward,
    )


def _projection_bounds(config: dict) -> list[tuple[float, float]]:
    bounds = config["cbd_projection"]["parameter_bounds"]
    return [
        tuple(float(x) for x in bounds["sharing_bias"]),
        tuple(float(x) for x in bounds["baseline_logit"]),
        tuple(float(x) for x in bounds["beta_accuracy"]),
        tuple(float(x) for x in bounds["beta_reward"]),
    ]


def project_general_to_cbd(
    coefficients: tuple[float, ...] | np.ndarray,
    *,
    belief: np.ndarray,
    accuracy: np.ndarray,
    reward: np.ndarray,
    config: dict,
) -> ProjectionResult:
    target = general_utility(coefficients, belief, accuracy, reward)
    bounds = _projection_bounds(config)
    starts = config["cbd_projection"]["deterministic_starts"]
    if not starts:
        raise ValueError("at least one deterministic CBD projection start is required")

    best: ProjectionResult | None = None
    for index, start in enumerate(starts):
        x0 = np.asarray(start, dtype=float)
        if x0.shape != (4,):
            raise ValueError("CBD projection starts must each have four parameters")

        def objective(parameters: np.ndarray) -> float:
            delta = cbd_utility(
                parameters,
                belief,
                accuracy,
                reward,
            ) - target
            return float(np.mean(delta**2))

        result = minimize(
            objective,
            x0=x0,
            method="L-BFGS-B",
            bounds=bounds,
            options={
                "maxiter": int(config["cbd_projection"]["maxiter"]),
                "ftol": float(config["cbd_projection"]["ftol"]),
            },
        )
        if not result.success:
            continue
        candidate = ProjectionResult(
            coefficients=tuple(float(x) for x in result.x),
            rms_distance=float(sqrt(max(0.0, float(result.fun)))),
            converged=True,
            start_index=int(index),
            objective=float(result.fun),
        )
        if best is None or candidate.objective < best.objective:
            best = candidate

    if best is None:
        raise DepartureGenerationError(
            "all deterministic CBD projection starts failed"
        )
    return best


def project_general_to_add(
    coefficients: tuple[float, ...] | np.ndarray,
    *,
    belief: np.ndarray,
    accuracy: np.ndarray,
    reward: np.ndarray,
) -> ProjectionResult:
    target = general_utility(coefficients, belief, accuracy, reward)
    matrix = general_design_matrix(belief, accuracy, reward)[:, :4]
    fitted, *_ = np.linalg.lstsq(matrix, target, rcond=None)
    add_general = np.asarray(
        add_fit_to_general_coefficients(tuple(float(x) for x in fitted)),
        dtype=float,
    )
    predicted = general_utility(add_general, belief, accuracy, reward)
    return ProjectionResult(
        coefficients=tuple(float(x) for x in add_general),
        rms_distance=rms_distance(target, predicted),
        converged=True,
        start_index=0,
        objective=float(np.mean((target - predicted) ** 2)),
    )


def _raw_direction(axis: DepartureAxis) -> np.ndarray:
    if axis is DepartureAxis.STANDALONE_ACCURACY_MAIN_EFFECT:
        return np.asarray((0.0, 0.0, 1.0, 0.0, 0.0, 0.0))
    if axis is DepartureAxis.COMPLEMENT_RELATION_VIOLATION:
        return np.asarray((0.0, 0.0, 0.0, 0.0, 0.0, 1.0))
    raise ValueError("combined direction is composed after primitive normalization")


def _normalize_direction(
    direction: np.ndarray,
    *,
    belief: np.ndarray,
    accuracy: np.ndarray,
    reward: np.ndarray,
) -> np.ndarray:
    effect = general_design_matrix(belief, accuracy, reward) @ direction
    scale = float(sqrt(float(np.mean(effect**2))))
    if scale <= 0.0:
        raise ValueError("departure direction has zero RMS utility effect")
    return np.asarray(direction, dtype=float) / scale


def departure_direction(
    axis: DepartureAxis,
    *,
    belief: np.ndarray,
    accuracy: np.ndarray,
    reward: np.ndarray,
) -> np.ndarray:
    if axis is DepartureAxis.COMBINED_VIOLATION:
        accuracy_direction = _normalize_direction(
            _raw_direction(DepartureAxis.STANDALONE_ACCURACY_MAIN_EFFECT),
            belief=belief,
            accuracy=accuracy,
            reward=reward,
        )
        complement_direction = _normalize_direction(
            _raw_direction(DepartureAxis.COMPLEMENT_RELATION_VIOLATION),
            belief=belief,
            accuracy=accuracy,
            reward=reward,
        )
        return _normalize_direction(
            accuracy_direction + complement_direction,
            belief=belief,
            accuracy=accuracy,
            reward=reward,
        )
    return _normalize_direction(
        _raw_direction(axis),
        belief=belief,
        accuracy=accuracy,
        reward=reward,
    )


def _anchor_block_for_axis(axis: DepartureAxis, config: dict) -> dict:
    if axis is DepartureAxis.STANDALONE_ACCURACY_MAIN_EFFECT:
        return config["anchors"]["cbd_add_intersection"]
    return config["anchors"]["cbd"]


def _distance_to_cbd(
    coefficients: np.ndarray,
    *,
    belief: np.ndarray,
    accuracy: np.ndarray,
    reward: np.ndarray,
    config: dict,
) -> ProjectionResult:
    return project_general_to_cbd(
        coefficients,
        belief=belief,
        accuracy=accuracy,
        reward=reward,
        config=config,
    )


def _find_first_bracket(
    anchor: np.ndarray,
    direction: np.ndarray,
    sign: int,
    target: float,
    *,
    belief: np.ndarray,
    accuracy: np.ndarray,
    reward: np.ndarray,
    config: dict,
) -> tuple[float, float]:
    search = config["distance_solver"]
    step = float(search["scan_step"])
    maximum = float(search["max_scalar"])
    if step <= 0.0 or maximum <= 0.0:
        raise ValueError("distance solver scan_step/max_scalar must be positive")

    previous_scalar = 0.0
    previous_value = -float(target)
    scalar = step
    while scalar <= maximum + 1e-15:
        beta = anchor + float(sign) * scalar * direction
        projection = _distance_to_cbd(
            beta,
            belief=belief,
            accuracy=accuracy,
            reward=reward,
            config=config,
        )
        value = projection.rms_distance - float(target)
        if previous_value <= 0.0 <= value:
            return previous_scalar, scalar
        previous_scalar = scalar
        previous_value = value
        scalar += step

    raise DepartureGenerationError(
        "no first positive distance bracket found within declared scalar range"
    )


def solve_departure_case(
    *,
    anchor_id: str,
    anchor_parameters: tuple[float, ...],
    axis: DepartureAxis,
    sign: int,
    target_distance: float,
    config: dict,
) -> DepartureCase:
    if sign not in (-1, 1):
        raise ValueError("departure sign must be -1 or +1")
    if target_distance <= 0.0:
        raise ValueError("target distance must be positive")

    design = config["design_cells"]
    belief, accuracy, reward = design_arrays(
        tuple(float(x) for x in design["belief_B"]),
        tuple(float(x) for x in design["accuracy_cue_A"]),
        tuple(float(x) for x in design["reward_context_R"]),
    )
    anchor = _cbd_general_coefficients(anchor_parameters)
    anchor_projection = _distance_to_cbd(
        anchor,
        belief=belief,
        accuracy=accuracy,
        reward=reward,
        config=config,
    )
    if anchor_projection.rms_distance > float(
        config["integrity_tolerances"]["anchor_cbd_rms"]
    ):
        raise DepartureGenerationError(
            f"declared CBD anchor does not project to zero: "
            f"{anchor_projection.rms_distance:.6g}"
        )

    direction = departure_direction(
        axis,
        belief=belief,
        accuracy=accuracy,
        reward=reward,
    )
    low, high = _find_first_bracket(
        anchor,
        direction,
        sign,
        target_distance,
        belief=belief,
        accuracy=accuracy,
        reward=reward,
        config=config,
    )

    def root_objective(scalar: float) -> float:
        beta = anchor + float(sign) * float(scalar) * direction
        projection = _distance_to_cbd(
            beta,
            belief=belief,
            accuracy=accuracy,
            reward=reward,
            config=config,
        )
        return projection.rms_distance - float(target_distance)

    scalar = float(
        brentq(
            root_objective,
            low,
            high,
            xtol=float(config["distance_solver"]["xtol"]),
            rtol=float(config["distance_solver"]["rtol"]),
            maxiter=int(config["distance_solver"]["maxiter"]),
        )
    )
    beta = anchor + float(sign) * scalar * direction
    cbd_projection = _distance_to_cbd(
        beta,
        belief=belief,
        accuracy=accuracy,
        reward=reward,
        config=config,
    )
    error = abs(cbd_projection.rms_distance - float(target_distance))
    if error > float(config["integrity_tolerances"]["target_distance_error"]):
        raise DepartureGenerationError(
            f"departure target error exceeds tolerance: {error:.6g}"
        )

    add_projection = project_general_to_add(
        beta,
        belief=belief,
        accuracy=accuracy,
        reward=reward,
    )
    add_expected = (
        axis is DepartureAxis.STANDALONE_ACCURACY_MAIN_EFFECT
    )
    add_pass = (
        add_projection.rms_distance
        <= float(config["integrity_tolerances"]["add_compatibility_rms"])
    )
    if add_expected and not add_pass:
        raise DepartureGenerationError(
            "standalone-accuracy specificity departure is not ADD-compatible"
        )

    anchor_family = (
        "CBD_ADD_INTERSECTION"
        if add_expected
        else "CBD"
    )
    case_id = (
        f"{anchor_id}__{axis.value}__"
        f"{'PLUS' if sign > 0 else 'MINUS'}__"
        f"RMS_{target_distance:.2f}"
    )
    return DepartureCase(
        case_id=case_id,
        anchor_id=anchor_id,
        anchor_family=anchor_family,
        axis=axis.value,
        sign=int(sign),
        requested_cbd_rms_distance=float(target_distance),
        achieved_cbd_rms_distance=float(cbd_projection.rms_distance),
        cbd_distance_error=float(error),
        nearest_add_rms_distance=float(add_projection.rms_distance),
        scalar_step=scalar,
        general_coefficients=tuple(float(x) for x in beta),
        nearest_cbd_parameters=tuple(
            float(x) for x in cbd_projection.coefficients
        ),
        nearest_cbd_start_index=int(cbd_projection.start_index),
        nearest_add_coefficients=tuple(
            float(x) for x in add_projection.coefficients
        ),
        add_compatibility_expected=bool(add_expected),
        add_compatibility_pass=bool(add_pass),
    )


def generate_controlled_departure_design(config: dict) -> dict:
    if config["status"] != "NON_AUTHORITATIVE_CONTROLLED_DEPARTURE_GENERATOR":
        raise ValueError("unsupported controlled-departure config status")

    results: list[dict] = []
    for axis_name in config["departure_axes"]:
        axis = DepartureAxis(axis_name)
        anchors = _anchor_block_for_axis(axis, config)
        for anchor_id, values in anchors.items():
            parameters = tuple(float(x) for x in values)
            for sign in (-1, 1):
                for target in config["target_cbd_rms_distances"]:
                    case = solve_departure_case(
                        anchor_id=anchor_id,
                        anchor_parameters=parameters,
                        axis=axis,
                        sign=sign,
                        target_distance=float(target),
                        config=config,
                    )
                    results.append(asdict(case))

    expected_count = (
        len(config["departure_axes"])
        * 2
        * 2
        * len(config["target_cbd_rms_distances"])
    )
    if len(results) != expected_count:
        raise DepartureGenerationError(
            f"unexpected controlled-departure case count: "
            f"{len(results)} != {expected_count}"
        )

    return {
        "design_id": config["design_id"],
        "status": "NON_AUTHORITATIVE_CONTROLLED_DEPARTURE_RESULT",
        "authoritative": False,
        "case_count": len(results),
        "cases": results,
        "interpretation_boundary": (
            "Controlled synthetic departure geometry only. Exact RMS distance "
            "generation does not establish detection power, freeze bootstrap "
            "draws/evaluation replicates, validate a human mechanism, freeze "
            "human N, authorize recruitment, or activate runtime F1b."
        ),
    }
