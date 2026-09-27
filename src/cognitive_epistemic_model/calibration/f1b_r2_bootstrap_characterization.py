from __future__ import annotations

from collections import defaultdict
from dataclasses import asdict, dataclass
from math import sqrt

import numpy as np

from .f1b_hierarchical_recovery import RandomEffectScales
from .f1b_prehuman_recovery import R2Family, simulate_r2_dataset
from .f1b_r2_controlled_departures import (
    DepartureAxis,
    generate_controlled_departure_design,
    solve_departure_case,
)
from .f1b_r2_restriction_recovery import (
    BootstrapCalibrationError,
    R2Restriction,
    bootstrap_restriction_test,
)


@dataclass(frozen=True)
class CharacterizationTrial:
    restriction: str
    identity: str
    identity_type: str
    role: str
    anchor_id: str | None
    axis: str | None
    sign: int | None
    requested_cbd_rms_distance: float | None
    achieved_cbd_rms_distance: float | None
    nearest_add_rms_distance: float | None
    bootstrap_draws: int
    evaluation_replicate: int
    observed_statistic: float | None
    critical_value: float | None
    p_value: float | None
    rejected: bool | None
    fit_failure: bool
    bootstrap_calibration_failure: bool
    bootstrap_draws_successful: int
    bootstrap_fit_failures: int
    held_out_participant_delta: float | None
    held_out_item_delta: float | None


def _scales(config: dict) -> RandomEffectScales:
    random_effects = config["random_effects"]
    multiplier = float(config["fit_scale_multiplier"])
    if multiplier <= 0.0:
        raise ValueError("fit_scale_multiplier must be positive")
    return RandomEffectScales(
        participant_intercept_sd=float(
            random_effects["participant_intercept_sd"]
        )
        * multiplier,
        item_intercept_sd=float(random_effects["item_intercept_sd"])
        * multiplier,
        participant_slope_sd=float(
            random_effects["participant_reward_slope_sd"]
        )
        * multiplier,
        item_slope_sd=float(
            random_effects["item_reward_slope_sd"]
        )
        * multiplier,
    )


def _generator_scales(config: dict) -> RandomEffectScales:
    random_effects = config["random_effects"]
    return RandomEffectScales(
        participant_intercept_sd=float(
            random_effects["participant_intercept_sd"]
        ),
        item_intercept_sd=float(random_effects["item_intercept_sd"]),
        participant_slope_sd=float(
            random_effects["participant_reward_slope_sd"]
        ),
        item_slope_sd=float(
            random_effects["item_reward_slope_sd"]
        ),
    )


def wilson_interval(
    successes: int,
    total: int,
    *,
    z: float = 1.959963984540054,
) -> tuple[float, float]:
    if total <= 0:
        return (0.0, 1.0)
    if not 0 <= successes <= total:
        raise ValueError("successes must lie in [0,total]")
    n = float(total)
    p = float(successes) / n
    z2 = float(z) ** 2
    denominator = 1.0 + z2 / n
    center = (p + z2 / (2.0 * n)) / denominator
    half = (
        float(z)
        * sqrt((p * (1.0 - p) + z2 / (4.0 * n)) / n)
        / denominator
    )
    return (max(0.0, center - half), min(1.0, center + half))


def _seeded_rng(master: int, *parts: int) -> np.random.Generator:
    return np.random.default_rng(
        np.random.SeedSequence([int(master), *(int(x) for x in parts)])
    )


def _simulate_dataset(
    *,
    family: R2Family,
    parameters: tuple[float, ...],
    config: dict,
    rng: np.random.Generator,
) -> object:
    design = config["design"]
    scales = _generator_scales(config)
    return simulate_r2_dataset(
        family=family,
        participants=int(design["participants"]),
        items=int(design["items"]),
        belief_levels=tuple(float(x) for x in design["belief_B"]),
        accuracy_levels=tuple(
            float(x) for x in design["accuracy_cue_A"]
        ),
        reward_levels=tuple(float(x) for x in design["reward_context_R"]),
        parameters=parameters,
        participant_intercept_sd=scales.participant_intercept_sd,
        item_intercept_sd=scales.item_intercept_sd,
        participant_reward_slope_sd=scales.participant_slope_sd,
        item_reward_slope_sd=scales.item_slope_sd,
        rng=rng,
        missingness_rate=float(design["missingness_rate"]),
    )


def _run_test(
    *,
    dataset,
    restriction: R2Restriction,
    config: dict,
    bootstrap_draws: int,
    bootstrap_seed: int,
) -> dict:
    try:
        result = bootstrap_restriction_test(
            dataset,
            restriction,
            scales=_scales(config),
            bootstrap_draws=int(bootstrap_draws),
            minimum_successful_draws=int(
                config["bootstrap"]["minimum_successful_draws_by_draw_count"][
                    str(int(bootstrap_draws))
                ]
            ),
            seed=int(bootstrap_seed),
            alpha=float(config["bootstrap"]["alpha"]),
        )
    except BootstrapCalibrationError:
        return {
            "fit_failure": False,
            "bootstrap_calibration_failure": True,
            "result": None,
        }
    except (RuntimeError, ValueError, np.linalg.LinAlgError):
        return {
            "fit_failure": True,
            "bootstrap_calibration_failure": False,
            "result": None,
        }
    return {
        "fit_failure": False,
        "bootstrap_calibration_failure": False,
        "result": result,
    }


def _filter_departure_cases(cases: list[dict], config: dict) -> list[dict]:
    selector = config.get("departure_case_filter")
    if selector is None:
        return cases

    def allowed(case: dict) -> bool:
        for key, allowed_values in selector.items():
            if allowed_values is None:
                continue
            value = case[key]
            if value not in allowed_values:
                return False
        return True

    filtered = [case for case in cases if allowed(case)]
    if not filtered:
        raise ValueError("departure_case_filter removed all cases")
    return filtered


def _departure_cases_for_config(
    departure_config: dict,
    config: dict,
) -> list[dict]:
    selector = config.get("departure_case_filter")
    if selector is None:
        return generate_controlled_departure_design(
            departure_config
        )["cases"]

    axis_values = selector.get("axis")
    anchor_values = selector.get("anchor_id")
    sign_values = selector.get("sign")
    distance_values = selector.get("requested_cbd_rms_distance")

    if (
        axis_values is None
        or anchor_values is None
        or sign_values is None
        or distance_values is None
    ):
        generated = generate_controlled_departure_design(departure_config)
        return _filter_departure_cases(generated["cases"], config)

    cases: list[dict] = []
    for axis_name in axis_values:
        axis = DepartureAxis(axis_name)
        anchor_block = (
            departure_config["anchors"]["cbd_add_intersection"]
            if axis is DepartureAxis.STANDALONE_ACCURACY_MAIN_EFFECT
            else departure_config["anchors"]["cbd"]
        )
        for anchor_id in anchor_values:
            if anchor_id not in anchor_block:
                raise ValueError(
                    "departure_case_filter anchor is incompatible with "
                    f"axis {axis.value}: {anchor_id}"
                )
            parameters = tuple(float(x) for x in anchor_block[anchor_id])
            for sign in sign_values:
                for distance in distance_values:
                    case = solve_departure_case(
                        anchor_id=anchor_id,
                        anchor_parameters=parameters,
                        axis=axis,
                        sign=int(sign),
                        target_distance=float(distance),
                        config=departure_config,
                    )
                    cases.append(asdict(case))

    if not cases:
        raise ValueError("departure_case_filter generated no cases")
    return cases


def _trial_from_result(
    *,
    restriction: R2Restriction,
    identity: str,
    identity_type: str,
    role: str,
    anchor_id: str | None,
    axis: str | None,
    sign: int | None,
    requested_cbd_rms_distance: float | None,
    achieved_cbd_rms_distance: float | None,
    nearest_add_rms_distance: float | None,
    bootstrap_draws: int,
    evaluation_replicate: int,
    outcome: dict,
) -> CharacterizationTrial:
    result = outcome["result"]
    if result is None:
        return CharacterizationTrial(
            restriction=restriction.value,
            identity=identity,
            identity_type=identity_type,
            role=role,
            anchor_id=anchor_id,
            axis=axis,
            sign=sign,
            requested_cbd_rms_distance=requested_cbd_rms_distance,
            achieved_cbd_rms_distance=achieved_cbd_rms_distance,
            nearest_add_rms_distance=nearest_add_rms_distance,
            bootstrap_draws=int(bootstrap_draws),
            evaluation_replicate=int(evaluation_replicate),
            observed_statistic=None,
            critical_value=None,
            p_value=None,
            rejected=None,
            fit_failure=bool(outcome["fit_failure"]),
            bootstrap_calibration_failure=bool(
                outcome["bootstrap_calibration_failure"]
            ),
            bootstrap_draws_successful=0,
            bootstrap_fit_failures=0,
            held_out_participant_delta=None,
            held_out_item_delta=None,
        )
    return CharacterizationTrial(
        restriction=result.restriction.value,
        identity=identity,
        identity_type=identity_type,
        role=role,
        anchor_id=anchor_id,
        axis=axis,
        sign=sign,
        requested_cbd_rms_distance=requested_cbd_rms_distance,
        achieved_cbd_rms_distance=achieved_cbd_rms_distance,
        nearest_add_rms_distance=nearest_add_rms_distance,
        bootstrap_draws=int(bootstrap_draws),
        evaluation_replicate=int(evaluation_replicate),
        observed_statistic=float(result.observed_statistic),
        critical_value=float(result.critical_value),
        p_value=float(result.p_value),
        rejected=bool(result.rejected),
        fit_failure=False,
        bootstrap_calibration_failure=False,
        bootstrap_draws_successful=int(result.bootstrap_draws_successful),
        bootstrap_fit_failures=int(result.bootstrap_fit_failures),
        held_out_participant_delta=float(
            result.held_out_participant_delta
        ),
        held_out_item_delta=float(result.held_out_item_delta),
    )


def _null_cases(config: dict) -> list[dict]:
    return [
        {
            "identity": "CBD_NULL_ANCHOR_1",
            "family": R2Family.AP_A,
            "parameters": tuple(
                float(x) for x in config["null_generators"]["CBD_ANCHOR_1"]
            ),
            "restriction": R2Restriction.CBD_COMPLEMENT,
            "role": "CBD_NULL_FALSE_REJECTION",
            "anchor_id": "CBD_ANCHOR_1",
            "stream": 101,
        },
        {
            "identity": "CBD_NULL_ANCHOR_2",
            "family": R2Family.AP_A,
            "parameters": tuple(
                float(x) for x in config["null_generators"]["CBD_ANCHOR_2"]
            ),
            "restriction": R2Restriction.CBD_COMPLEMENT,
            "role": "CBD_NULL_FALSE_REJECTION",
            "anchor_id": "CBD_ANCHOR_2",
            "stream": 102,
        },
        {
            "identity": "ADD_NULL",
            "family": R2Family.AP_B,
            "parameters": tuple(
                float(x) for x in config["null_generators"]["ADD_ANCHOR"]
            ),
            "restriction": R2Restriction.ADD,
            "role": "ADD_NULL_FALSE_REJECTION",
            "anchor_id": "ADD_ANCHOR",
            "stream": 103,
        },
    ]


def _aggregate_trials(trials: list[CharacterizationTrial]) -> list[dict]:
    groups: dict[tuple, list[CharacterizationTrial]] = defaultdict(list)
    for trial in trials:
        key = (
            trial.restriction,
            trial.identity,
            trial.identity_type,
            trial.role,
            trial.anchor_id,
            trial.axis,
            trial.sign,
            trial.requested_cbd_rms_distance,
            trial.bootstrap_draws,
        )
        groups[key].append(trial)

    rows: list[dict] = []
    for key, values in sorted(groups.items(), key=lambda item: str(item[0])):
        total = len(values)
        fit_failures = sum(value.fit_failure for value in values)
        calibration_failures = sum(
            value.bootstrap_calibration_failure for value in values
        )
        successful = [
            value
            for value in values
            if not value.fit_failure
            and not value.bootstrap_calibration_failure
            and value.rejected is not None
        ]
        rejected = sum(bool(value.rejected) for value in successful)
        all_rejected = rejected
        conditional_interval = wilson_interval(rejected, len(successful))
        all_interval = wilson_interval(all_rejected, total)

        rows.append(
            {
                "restriction": key[0],
                "identity": key[1],
                "identity_type": key[2],
                "role": key[3],
                "anchor_id": key[4],
                "axis": key[5],
                "sign": key[6],
                "requested_cbd_rms_distance": key[7],
                "bootstrap_draws": key[8],
                "evaluation_replicates": total,
                "successful_tests": len(successful),
                "rejections": rejected,
                "rejection_probability_all_replicates": (
                    all_rejected / total if total else 0.0
                ),
                "rejection_wilson_95_all_replicates": list(all_interval),
                "rejection_probability_successful_tests": (
                    rejected / len(successful) if successful else None
                ),
                "rejection_wilson_95_successful_tests": (
                    list(conditional_interval) if successful else None
                ),
                "fit_failure_count": fit_failures,
                "fit_failure_probability": fit_failures / total,
                "bootstrap_calibration_failure_count": calibration_failures,
                "bootstrap_calibration_failure_probability": (
                    calibration_failures / total
                ),
                "mean_bootstrap_fit_failures": (
                    float(
                        np.mean(
                            [
                                value.bootstrap_fit_failures
                                for value in successful
                            ]
                        )
                    )
                    if successful
                    else None
                ),
                "mean_held_out_participant_delta": (
                    float(
                        np.mean(
                            [
                                value.held_out_participant_delta
                                for value in successful
                            ]
                        )
                    )
                    if successful
                    else None
                ),
                "mean_held_out_item_delta": (
                    float(
                        np.mean(
                            [
                                value.held_out_item_delta
                                for value in successful
                            ]
                        )
                    )
                    if successful
                    else None
                ),
            }
        )
    return rows


def run_bootstrap_characterization(
    config: dict,
    departure_config: dict,
) -> dict:
    if config["status"] not in (
        "NON_AUTHORITATIVE_R2_BOOTSTRAP_CHARACTERIZATION_DESIGN",
        "SMOKE_NON_AUTHORITATIVE_R2_BOOTSTRAP_CHARACTERIZATION",
    ):
        raise ValueError("unsupported R2 bootstrap characterization status")

    draw_grid = [int(x) for x in config["bootstrap"]["draw_grid"]]
    replicate_grid = [
        int(x) for x in config["evaluation_replicate_grid"]
    ]
    if any(value <= 0 for value in draw_grid + replicate_grid):
        raise ValueError("draw/replicate grid values must be positive")

    departure_cases = _departure_cases_for_config(
        departure_config,
        config,
    )
    trials: list[CharacterizationTrial] = []
    master_seed = int(config["seed"])

    for bootstrap_draws in draw_grid:
        for evaluation_replicates in replicate_grid:
            for null in _null_cases(config):
                for replicate in range(evaluation_replicates):
                    rng = _seeded_rng(
                        master_seed,
                        1,
                        int(null["stream"]),
                        int(bootstrap_draws),
                        int(evaluation_replicates),
                        int(replicate),
                    )
                    dataset = _simulate_dataset(
                        family=null["family"],
                        parameters=null["parameters"],
                        config=config,
                        rng=rng,
                    )
                    outcome = _run_test(
                        dataset=dataset,
                        restriction=null["restriction"],
                        config=config,
                        bootstrap_draws=bootstrap_draws,
                        bootstrap_seed=(
                            master_seed
                            + 1_000_000
                            + null["stream"] * 10_000
                            + bootstrap_draws * 100
                            + evaluation_replicates * 10
                            + replicate
                        ),
                    )
                    trials.append(
                        _trial_from_result(
                            restriction=null["restriction"],
                            identity=null["identity"],
                            identity_type="NULL",
                            role=null["role"],
                            anchor_id=null["anchor_id"],
                            axis=None,
                            sign=None,
                            requested_cbd_rms_distance=0.0,
                            achieved_cbd_rms_distance=0.0,
                            nearest_add_rms_distance=None,
                            bootstrap_draws=bootstrap_draws,
                            evaluation_replicate=replicate,
                            outcome=outcome,
                        )
                    )

            for case_index, case in enumerate(departure_cases):
                for replicate in range(evaluation_replicates):
                    rng = _seeded_rng(
                        master_seed,
                        2,
                        case_index,
                        int(bootstrap_draws),
                        int(evaluation_replicates),
                        int(replicate),
                    )
                    dataset = _simulate_dataset(
                        family=R2Family.AP_C,
                        parameters=tuple(
                            float(x) for x in case["general_coefficients"]
                        ),
                        config=config,
                        rng=rng,
                    )
                    for restriction_index, restriction in enumerate(
                        (
                            R2Restriction.CBD_COMPLEMENT,
                            R2Restriction.ADD,
                        ),
                        start=1,
                    ):
                        if restriction is R2Restriction.CBD_COMPLEMENT:
                            role = "CBD_DEPARTURE_DETECTION"
                        elif case["add_compatibility_expected"]:
                            role = "ADD_SPECIFICITY_NEGATIVE_CONTROL"
                        else:
                            role = "ADD_DEPARTURE_DIAGNOSTIC"

                        outcome = _run_test(
                            dataset=dataset,
                            restriction=restriction,
                            config=config,
                            bootstrap_draws=bootstrap_draws,
                            bootstrap_seed=(
                                master_seed
                                + 2_000_000
                                + case_index * 100_000
                                + restriction_index * 10_000
                                + bootstrap_draws * 100
                                + evaluation_replicates * 10
                                + replicate
                            ),
                        )
                        trials.append(
                            _trial_from_result(
                                restriction=restriction,
                                identity=case["case_id"],
                                identity_type="DEPARTURE",
                                role=role,
                                anchor_id=case["anchor_id"],
                                axis=case["axis"],
                                sign=int(case["sign"]),
                                requested_cbd_rms_distance=float(
                                    case["requested_cbd_rms_distance"]
                                ),
                                achieved_cbd_rms_distance=float(
                                    case["achieved_cbd_rms_distance"]
                                ),
                                nearest_add_rms_distance=float(
                                    case["nearest_add_rms_distance"]
                                ),
                                bootstrap_draws=bootstrap_draws,
                                evaluation_replicate=replicate,
                                outcome=outcome,
                            )
                        )

    trial_dicts = [trial.__dict__ for trial in trials]
    return {
        "characterization_id": config["characterization_id"],
        "status": (
            "SMOKE_NON_AUTHORITATIVE_R2_BOOTSTRAP_RESULT"
            if config["status"].startswith("SMOKE_")
            else "NON_AUTHORITATIVE_R2_BOOTSTRAP_CHARACTERIZATION_RESULT"
        ),
        "authoritative": False,
        "draw_grid": draw_grid,
        "evaluation_replicate_grid": replicate_grid,
        "departure_case_count": len(departure_cases),
        "trial_count": len(trials),
        "trials": trial_dicts,
        "aggregate": _aggregate_trials(trials),
        "interpretation_boundary": (
            "Bootstrap characterization only. Draw counts and evaluation "
            "replicates remain design-search values. Failure to reject is not "
            "proof of a restriction; rejection does not identify a unique "
            "psychological mechanism. No result freezes a core grid, human N, "
            "recruitment, or runtime F1b."
        ),
    }
