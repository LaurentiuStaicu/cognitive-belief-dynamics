from __future__ import annotations

from dataclasses import asdict, dataclass
from math import sqrt

import numpy as np
from scipy.optimize import brentq
from scipy.special import expit

from .f1b_r2_controlled_departures import (
    DepartureAxis,
    departure_direction,
    design_arrays,
    general_utility,
    project_general_to_add,
)
from .f1b_r2_distance_definition_review import (
    cbd_surface_utility,
    project_general_surface_to_cbd_closure,
    response_surface_diagnostics,
)
from .f1b_r2_restriction_recovery import (
    cbd_fit_to_general_coefficients,
)


class KLControlledDepartureGenerationError(RuntimeError):
    pass


_DESIGN_CONTRACTS = {
    "F1B.R2.KL_CONTROLLED_DEPARTURE.V1": {
        "status": "NON_AUTHORITATIVE_KL_CONTROLLED_DEPARTURE_V1_DESIGN",
        "targets": (0.001, 0.005, 0.010),
        "partition_status": (
            "NON_AUTHORITATIVE_KL_CONTROLLED_DEPARTURE_V1_PARTITION"
        ),
        "result_status": "NON_AUTHORITATIVE_KL_CONTROLLED_DEPARTURE_V1_RESULT",
        "version_label": "v1",
    },
    "F1B.R2.KL_CONTROLLED_DEPARTURE.V2": {
        "status": "NON_AUTHORITATIVE_KL_CONTROLLED_DEPARTURE_V2_DESIGN",
        "targets": (0.001, 0.002, 0.003),
        "partition_status": (
            "NON_AUTHORITATIVE_KL_CONTROLLED_DEPARTURE_V2_PARTITION"
        ),
        "result_status": "NON_AUTHORITATIVE_KL_CONTROLLED_DEPARTURE_V2_RESULT",
        "version_label": "v2",
    },
}


def _design_contract(config: dict) -> dict:
    design_id = str(config.get("design_id", ""))
    contract = _DESIGN_CONTRACTS.get(design_id)
    if contract is None:
        raise ValueError(
            f"unsupported KL controlled-departure design_id: {design_id}"
        )
    if str(config.get("status", "")) != str(contract["status"]):
        raise ValueError(
            "KL controlled-departure status does not match design_id"
        )
    return contract


@dataclass(frozen=True)
class KLControlledDepartureCase:
    case_id: str
    design_version: str
    anchor_id: str
    anchor_family: str
    axis: str
    sign: int
    requested_mean_bernoulli_kl: float
    achieved_mean_bernoulli_kl: float
    mean_kl_error: float
    scalar_step: float
    general_coefficients: tuple[float, ...]
    structural_direction: tuple[float, ...]
    cbd_attainment_status: str
    cbd_closure_boundary_components: tuple[str, ...]
    cbd_scientific_domain_components: tuple[str, ...]
    selected_cbd_surface_coordinates: tuple[float, ...]
    utility_rms_diagnostic_at_kl_projection: float
    probability_rms_diagnostic_at_kl_projection: float
    sqrt_2_mean_kl_diagnostic: float
    information_weighted_logit_distance: float
    d1_nearest_utility_rms: float
    d1_attainment_status: str
    d2_nearest_probability_rms: float
    d2_attainment_status: str
    nearest_add_rms_distance: float
    nearest_add_coefficients: tuple[float, ...]
    add_compatibility_expected: bool
    add_compatibility_pass: bool
    min_probability_general: float
    max_probability_general: float
    min_probability_cbd: float
    max_probability_cbd: float
    generator_outside_005_095_count: int
    generator_outside_010_090_count: int
    cbd_outside_005_095_count: int
    cbd_outside_010_090_count: int
    first_crossing_bracket: tuple[float, float]


def _anchor_block_for_axis(axis: DepartureAxis, config: dict) -> dict:
    if axis is DepartureAxis.STANDALONE_ACCURACY_MAIN_EFFECT:
        return config["anchors"]["cbd_add_intersection"]
    return config["anchors"]["cbd"]


def _anchor_general_coefficients(
    parameters: tuple[float, ...],
) -> np.ndarray:
    return np.asarray(
        cbd_fit_to_general_coefficients(
            tuple(float(value) for value in parameters)
        ),
        dtype=float,
    )


def _projection_starts(
    historical_departure_config: dict,
    anchor_parameters: tuple[float, ...],
) -> list[tuple[float, ...]]:
    starts = [
        tuple(float(value) for value in row)
        for row in historical_departure_config["cbd_projection"][
            "deterministic_starts"
        ]
    ]
    if len(starts) != 7:
        raise ValueError("KL design requires the frozen seven CBD starts")
    starts.append(tuple(float(value) for value in anchor_parameters))
    return starts


def _validate_config(
    config: dict,
    review_config: dict,
) -> None:
    contract = _design_contract(config)
    forbidden = (
        "stochastic_simulation_allowed",
        "bootstrap_allowed",
        "operational_fitter_bounds_change_allowed",
        "historical_departure_rewrite_allowed",
        "paired_bootstrap_authorized",
    )
    if any(bool(config["execution_boundary"][key]) for key in forbidden):
        raise ValueError("KL controlled-departure execution boundary violated")

    scientific = config["scientific_projection"]
    if scientific["candidate_id"] != "BERNOULLI_KL_GENERAL_TO_CBD":
        raise ValueError("KL design candidate changed unexpectedly")
    if scientific["direction"] != "GENERAL_TO_CBD":
        raise ValueError("KL direction changed unexpectedly")
    expected_domains = [
        int(value) for value in scientific["diagnostic_domain_multipliers"]
    ]
    review_domains = [
        int(value) for value in review_config["diagnostic_domain_multipliers"]
    ]
    if expected_domains != review_domains:
        raise ValueError("scientific projection domains differ from #171")

    targets = [float(value) for value in config["target_mean_bernoulli_kl"]]
    expected_targets = [float(value) for value in contract["targets"]]
    if targets != expected_targets:
        raise ValueError(
            "KL target grid does not match the frozen design contract"
        )
    if any(value <= 0.0 for value in targets):
        raise ValueError("KL targets must be positive")

    design = config["design_cells"]
    cell_count = (
        len(design["belief_B"])
        * len(design["accuracy_cue_A"])
        * len(design["reward_context_R"])
    )
    if cell_count != 18:
        raise ValueError("KL design must retain the frozen 18 cells")
    declared_weight = float(design["weight_per_cell"])
    if abs(declared_weight - 1.0 / 18.0) > 1e-15:
        raise ValueError("KL design weight must be uniform 1/18")


def _project(
    coefficients: np.ndarray,
    *,
    belief: np.ndarray,
    accuracy: np.ndarray,
    reward: np.ndarray,
    starts: list[tuple[float, ...]],
    review_config: dict,
    historical_departure_config: dict,
    candidate_id: str = "BERNOULLI_KL_GENERAL_TO_CBD",
) -> dict:
    projection = project_general_surface_to_cbd_closure(
        candidate_id=candidate_id,
        general_coefficients=coefficients,
        belief=belief,
        accuracy=accuracy,
        reward=reward,
        logit_starts=starts,
        review_config=review_config,
        departure_config=historical_departure_config,
    )
    if projection["attainment_status"] == "SCIENTIFIC_DOMAIN_UNRESOLVED":
        raise KLControlledDepartureGenerationError(
            "scientific CBD projection remains domain-unresolved"
        )
    return projection


def _selected_distance(projection: dict) -> float:
    return float(projection["selected_widest_domain"]["primary_distance"])


def _selected_surface_coordinates(projection: dict) -> tuple[float, ...]:
    return tuple(
        float(value)
        for value in projection["selected_widest_domain"][
            "selected_surface_coordinates"
        ]
    )


def _saturation_counts(probabilities: np.ndarray) -> tuple[int, int]:
    p = np.asarray(probabilities, dtype=float)
    outside_005 = int(np.sum((p < 0.05) | (p > 0.95)))
    outside_010 = int(np.sum((p < 0.10) | (p > 0.90)))
    return outside_005, outside_010


def _case_id(
    *,
    version: str,
    anchor_id: str,
    axis: DepartureAxis,
    sign: int,
    target: float,
) -> str:
    return (
        f"{version}__{anchor_id}__{axis.value}__"
        f"{'PLUS' if sign > 0 else 'MINUS'}__KL_{target:.3f}"
    )


def solve_kl_controlled_departure_case(
    *,
    anchor_id: str,
    anchor_parameters: tuple[float, ...],
    axis: DepartureAxis,
    sign: int,
    target_mean_kl: float,
    config: dict,
    review_config: dict,
    historical_departure_config: dict,
) -> dict:
    _validate_config(config, review_config)
    if sign not in (-1, 1):
        raise ValueError("departure sign must be -1 or +1")
    if target_mean_kl <= 0.0:
        raise ValueError("target mean KL must be positive")

    design = config["design_cells"]
    belief, accuracy, reward = design_arrays(
        tuple(float(value) for value in design["belief_B"]),
        tuple(float(value) for value in design["accuracy_cue_A"]),
        tuple(float(value) for value in design["reward_context_R"]),
    )
    anchor = _anchor_general_coefficients(anchor_parameters)
    direction = departure_direction(
        axis,
        belief=belief,
        accuracy=accuracy,
        reward=reward,
    )
    starts = _projection_starts(
        historical_departure_config,
        anchor_parameters,
    )

    evaluation_records: list[dict] = []
    cache: dict[float, dict] = {}

    def evaluate(scalar: float, *, phase: str) -> dict:
        key = float(scalar)
        if key in cache:
            cached = cache[key]
            cached["phases"].append(str(phase))
            return cached

        coefficients = anchor + float(sign) * key * direction
        projection = _project(
            coefficients,
            belief=belief,
            accuracy=accuracy,
            reward=reward,
            starts=starts,
            review_config=review_config,
            historical_departure_config=historical_departure_config,
        )
        row = {
            "evaluation_index": len(evaluation_records),
            "scalar": key,
            "phases": [str(phase)],
            "mean_bernoulli_kl": _selected_distance(projection),
            "attainment_status": projection["attainment_status"],
            "closure_boundary_components": list(
                projection["closure_boundary_components"]
            ),
            "scientific_domain_components": list(
                projection["scientific_domain_components"]
            ),
            "selected_cbd_surface_coordinates": list(
                _selected_surface_coordinates(projection)
            ),
            "projection": projection,
        }
        cache[key] = row
        evaluation_records.append(row)
        return row

    anchor_row = evaluate(0.0, phase="ANCHOR")
    anchor_distance = float(anchor_row["mean_bernoulli_kl"])
    if anchor_distance > float(
        config["integrity_tolerances"]["anchor_mean_kl"]
    ):
        raise KLControlledDepartureGenerationError(
            "declared CBD anchor does not project to zero mean KL: "
            f"{anchor_distance:.6g}"
        )

    solver = config["distance_solver"]
    scan_step = float(solver["scan_step"])
    max_scalar = float(solver["max_scalar"])
    if scan_step <= 0.0 or max_scalar <= 0.0:
        raise ValueError("KL scalar scan bounds must be positive")

    scan_records: list[dict] = [
        {
            "scalar": 0.0,
            "mean_bernoulli_kl": anchor_distance,
            "difference_from_target": (
                anchor_distance - float(target_mean_kl)
            ),
        }
    ]
    previous_scalar = 0.0
    previous_difference = anchor_distance - float(target_mean_kl)
    bracket: tuple[float, float] | None = None

    step_index = 1
    while True:
        scalar = float(step_index) * scan_step
        if scalar > max_scalar + 1e-15:
            break
        row = evaluate(scalar, phase="SCAN")
        distance = float(row["mean_bernoulli_kl"])
        difference = distance - float(target_mean_kl)
        scan_records.append(
            {
                "scalar": scalar,
                "mean_bernoulli_kl": distance,
                "difference_from_target": difference,
            }
        )
        if previous_difference <= 0.0 <= difference:
            bracket = (previous_scalar, scalar)
            break
        previous_scalar = scalar
        previous_difference = difference
        step_index += 1

    if bracket is None:
        raise KLControlledDepartureGenerationError(
            "no first positive KL target crossing within declared scalar range"
        )

    root_trace: list[dict] = []

    def root_objective(scalar: float) -> float:
        row = evaluate(float(scalar), phase="ROOT")
        difference = (
            float(row["mean_bernoulli_kl"]) - float(target_mean_kl)
        )
        root_trace.append(
            {
                "call_index": len(root_trace),
                "scalar": float(scalar),
                "mean_bernoulli_kl": float(
                    row["mean_bernoulli_kl"]
                ),
                "difference_from_target": difference,
            }
        )
        return difference

    scalar = float(
        brentq(
            root_objective,
            bracket[0],
            bracket[1],
            xtol=float(solver["xtol"]),
            rtol=float(solver["rtol"]),
            maxiter=int(solver["maxiter"]),
        )
    )
    solution_row = evaluate(scalar, phase="SOLUTION")
    achieved = float(solution_row["mean_bernoulli_kl"])
    target_error = abs(achieved - float(target_mean_kl))
    if target_error > float(
        config["integrity_tolerances"]["target_mean_kl_error"]
    ):
        raise KLControlledDepartureGenerationError(
            "KL departure target error exceeds tolerance: "
            f"{target_error:.6g}"
        )

    beta = anchor + float(sign) * scalar * direction
    kl_projection = solution_row["projection"]
    selected_coordinates = _selected_surface_coordinates(kl_projection)
    eta_general = general_utility(
        beta,
        belief,
        accuracy,
        reward,
    )
    eta_cbd = cbd_surface_utility(
        surface_coordinates=selected_coordinates,
        belief=belief,
        accuracy=accuracy,
        reward=reward,
    )
    metrics = response_surface_diagnostics(
        eta_general=eta_general,
        eta_cbd=eta_cbd,
    )

    d1_projection = _project(
        beta,
        belief=belief,
        accuracy=accuracy,
        reward=reward,
        starts=starts,
        review_config=review_config,
        historical_departure_config=historical_departure_config,
        candidate_id="STABILIZED_UTILITY_RMS",
    )
    d2_projection = _project(
        beta,
        belief=belief,
        accuracy=accuracy,
        reward=reward,
        starts=starts,
        review_config=review_config,
        historical_departure_config=historical_departure_config,
        candidate_id="PROBABILITY_RMS",
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
        raise KLControlledDepartureGenerationError(
            "standalone KL departure is not ADD-compatible"
        )

    p_general = expit(eta_general)
    p_cbd = expit(eta_cbd)
    gen_005, gen_010 = _saturation_counts(p_general)
    cbd_005, cbd_010 = _saturation_counts(p_cbd)

    anchor_family = (
        "CBD_ADD_INTERSECTION" if add_expected else "CBD"
    )
    case = KLControlledDepartureCase(
        case_id=_case_id(
            version=str(config["design_id"]),
            anchor_id=anchor_id,
            axis=axis,
            sign=sign,
            target=target_mean_kl,
        ),
        design_version=str(config["design_id"]),
        anchor_id=str(anchor_id),
        anchor_family=anchor_family,
        axis=axis.value,
        sign=int(sign),
        requested_mean_bernoulli_kl=float(target_mean_kl),
        achieved_mean_bernoulli_kl=achieved,
        mean_kl_error=target_error,
        scalar_step=scalar,
        general_coefficients=tuple(float(value) for value in beta),
        structural_direction=tuple(
            float(value) for value in direction
        ),
        cbd_attainment_status=str(
            kl_projection["attainment_status"]
        ),
        cbd_closure_boundary_components=tuple(
            str(value)
            for value in kl_projection["closure_boundary_components"]
        ),
        cbd_scientific_domain_components=tuple(
            str(value)
            for value in kl_projection["scientific_domain_components"]
        ),
        selected_cbd_surface_coordinates=selected_coordinates,
        utility_rms_diagnostic_at_kl_projection=float(
            metrics["utility_rms_distance"]
        ),
        probability_rms_diagnostic_at_kl_projection=float(
            metrics["probability_rms_distance"]
        ),
        sqrt_2_mean_kl_diagnostic=float(
            metrics["sqrt_2_mean_kl_diagnostic"]
        ),
        information_weighted_logit_distance=float(
            metrics["information_weighted_logit_distance"]
        ),
        d1_nearest_utility_rms=float(
            d1_projection["selected_widest_domain"][
                "primary_distance"
            ]
        ),
        d1_attainment_status=str(
            d1_projection["attainment_status"]
        ),
        d2_nearest_probability_rms=float(
            d2_projection["selected_widest_domain"][
                "primary_distance"
            ]
        ),
        d2_attainment_status=str(
            d2_projection["attainment_status"]
        ),
        nearest_add_rms_distance=float(add_projection.rms_distance),
        nearest_add_coefficients=tuple(
            float(value) for value in add_projection.coefficients
        ),
        add_compatibility_expected=bool(add_expected),
        add_compatibility_pass=bool(add_pass),
        min_probability_general=float(np.min(p_general)),
        max_probability_general=float(np.max(p_general)),
        min_probability_cbd=float(np.min(p_cbd)),
        max_probability_cbd=float(np.max(p_cbd)),
        generator_outside_005_095_count=gen_005,
        generator_outside_010_090_count=gen_010,
        cbd_outside_005_095_count=cbd_005,
        cbd_outside_010_090_count=cbd_010,
        first_crossing_bracket=tuple(
            float(value) for value in bracket
        ),
    )
    return {
        **asdict(case),
        "scan_records": scan_records,
        "root_trace": root_trace,
        "projection_evaluations": evaluation_records,
        "kl_projection_at_solution": kl_projection,
        "d1_projection_at_solution": d1_projection,
        "d2_projection_at_solution": d2_projection,
    }


def _expected_case_keys(config: dict) -> list[tuple[str, str, int, float]]:
    keys: list[tuple[str, str, int, float]] = []
    for axis_name in config["departure_axes"]:
        axis = DepartureAxis(str(axis_name))
        anchors = _anchor_block_for_axis(axis, config)
        for anchor_id in anchors:
            for sign in (-1, 1):
                for target in config["target_mean_bernoulli_kl"]:
                    keys.append(
                        (
                            axis.value,
                            str(anchor_id),
                            int(sign),
                            float(target),
                        )
                    )
    return keys


def _case_key(case: dict) -> tuple[str, str, int, float]:
    return (
        str(case["axis"]),
        str(case["anchor_id"]),
        int(case["sign"]),
        float(case["requested_mean_bernoulli_kl"]),
    )


def _validate_generated_cases(cases: list[dict], config: dict) -> None:
    if any(
        case["cbd_attainment_status"] == "SCIENTIFIC_DOMAIN_UNRESOLVED"
        for case in cases
    ):
        raise KLControlledDepartureGenerationError(
            "generated KL design contains domain-unresolved cases"
        )
    if any(
        float(case["mean_kl_error"])
        > float(config["integrity_tolerances"]["target_mean_kl_error"])
        for case in cases
    ):
        raise KLControlledDepartureGenerationError(
            "generated KL design exceeds target tolerance"
        )
    for case in cases:
        if (
            case["axis"]
            == DepartureAxis.STANDALONE_ACCURACY_MAIN_EFFECT.value
            and not bool(case["add_compatibility_pass"])
        ):
            raise KLControlledDepartureGenerationError(
                "standalone KL design contains an ADD-incompatible case"
            )


def generate_kl_controlled_departure_partition(
    config: dict,
    review_config: dict,
    historical_departure_config: dict,
    *,
    axis_name: str,
    anchor_id: str,
) -> dict:
    _validate_config(config, review_config)
    axis = DepartureAxis(str(axis_name))
    anchors = _anchor_block_for_axis(axis, config)
    if anchor_id not in anchors:
        raise ValueError(
            f"anchor {anchor_id} is incompatible with axis {axis.value}"
        )
    parameters = tuple(float(value) for value in anchors[anchor_id])

    cases: list[dict] = []
    for sign in (-1, 1):
        for target in config["target_mean_bernoulli_kl"]:
            cases.append(
                solve_kl_controlled_departure_case(
                    anchor_id=str(anchor_id),
                    anchor_parameters=parameters,
                    axis=axis,
                    sign=sign,
                    target_mean_kl=float(target),
                    config=config,
                    review_config=review_config,
                    historical_departure_config=historical_departure_config,
                )
            )
    if len(cases) != 6:
        raise KLControlledDepartureGenerationError(
            f"unexpected deterministic partition size: {len(cases)}"
        )
    _validate_generated_cases(cases, config)
    contract = _design_contract(config)
    return {
        "design_id": str(config["design_id"]),
        "status": str(contract["partition_status"]),
        "authoritative": False,
        "partition": {
            "axis": axis.value,
            "anchor_id": str(anchor_id),
        },
        "case_count": len(cases),
        "target_mean_bernoulli_kl": [
            float(value)
            for value in config["target_mean_bernoulli_kl"]
        ],
        "cases": cases,
        "interpretation_boundary": (
            "Execution-only deterministic partition of the frozen KL "
            f"{contract['version_label']} design. A partition is not a "
            "complete scientific result."
        ),
    }


def combine_kl_controlled_departure_partitions(
    partitions: list[dict],
    config: dict,
) -> dict:
    if not partitions:
        raise ValueError("at least one KL partition is required")

    contract = _design_contract(config)
    expected_keys = _expected_case_keys(config)
    expected_key_set = set(expected_keys)
    if len(expected_keys) != int(config["expected_case_count"]):
        raise ValueError("frozen KL expected-case count is inconsistent")

    cases: list[dict] = []
    seen_partitions: set[tuple[str, str]] = set()
    for partition in partitions:
        if partition["design_id"] != str(config["design_id"]):
            raise ValueError("KL partition design_id mismatch")
        if partition["status"] != str(contract["partition_status"]):
            raise ValueError("unsupported KL partition status")
        if partition["authoritative"] is not False:
            raise ValueError("KL partition cannot be authoritative")
        if partition["target_mean_bernoulli_kl"] != [
            float(value)
            for value in config["target_mean_bernoulli_kl"]
        ]:
            raise ValueError("KL partition target grid mismatch")
        selector = (
            str(partition["partition"]["axis"]),
            str(partition["partition"]["anchor_id"]),
        )
        if selector in seen_partitions:
            raise ValueError(f"duplicate KL execution partition: {selector}")
        seen_partitions.add(selector)
        cases.extend(partition["cases"])

    keys = [_case_key(case) for case in cases]
    if len(keys) != len(set(keys)):
        raise ValueError("duplicate scientific KL case across partitions")
    actual_key_set = set(keys)
    if actual_key_set != expected_key_set:
        missing = [
            key for key in expected_keys if key not in actual_key_set
        ]
        extra = [
            key for key in keys if key not in expected_key_set
        ]
        raise ValueError(
            "KL partition coverage is incomplete or invalid "
            f"(missing={missing}, extra={extra})"
        )

    _validate_generated_cases(cases, config)
    order = {key: index for index, key in enumerate(expected_keys)}
    cases = sorted(cases, key=lambda case: order[_case_key(case)])
    return {
        "design_id": str(config["design_id"]),
        "status": str(contract["result_status"]),
        "authoritative": False,
        "case_count": len(cases),
        "target_mean_bernoulli_kl": [
            float(value)
            for value in config["target_mean_bernoulli_kl"]
        ],
        "cases": cases,
        "execution_partition_count": len(partitions),
        "interpretation_boundary": (
            "Deterministic KL-controlled synthetic departure geometry only. "
            "Exact information-divergence generation does not establish "
            "bootstrap stability, detection power, a human effect size, "
            "human N, recruitment, or runtime F1b."
        ),
    }


def generate_kl_controlled_departure_design(
    config: dict,
    review_config: dict,
    historical_departure_config: dict,
) -> dict:
    _validate_config(config, review_config)
    partitions: list[dict] = []
    for axis_name in config["departure_axes"]:
        axis = DepartureAxis(str(axis_name))
        anchors = _anchor_block_for_axis(axis, config)
        for anchor_id in anchors:
            partitions.append(
                generate_kl_controlled_departure_partition(
                    config,
                    review_config,
                    historical_departure_config,
                    axis_name=axis.value,
                    anchor_id=str(anchor_id),
                )
            )
    return combine_kl_controlled_departure_partitions(
        partitions,
        config,
    )
