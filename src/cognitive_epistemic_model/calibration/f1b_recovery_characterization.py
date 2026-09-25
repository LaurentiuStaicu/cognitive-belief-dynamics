from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass

import numpy as np

from .f1b_hierarchical_recovery import (
    RandomEffectScales,
    fit_r1_hierarchical_candidate,
    fit_r2_hierarchical_candidate,
    select_r1_hierarchical_candidate,
    select_r2_hierarchical_candidate,
)
from .f1b_prehuman_recovery import (
    R1Family,
    R2Family,
    fit_r1_candidate,
    fit_r2_candidate,
    select_r1_candidate,
    select_r2_candidate,
    simulate_r1_dataset,
    simulate_r2_dataset,
    split_crossed,
)


R1_CANDIDATES = (R1Family.SR_A, R1Family.SR_B, R1Family.SR_C)
R2_CANDIDATES = (R2Family.AP_A, R2Family.AP_B, R2Family.AP_C)
FIT_FAILURE = "FIT_FAILURE"


@dataclass(frozen=True)
class CharacterizationOutcome:
    selected: str
    fit_failure: bool


def _rng(
    master_seed: int,
    *,
    problem: int,
    generator: int,
    regime: int,
    missingness: int,
    replicate: int,
) -> np.random.Generator:
    return np.random.default_rng(
        np.random.SeedSequence(
            [
                int(master_seed),
                int(problem),
                int(generator),
                int(regime),
                int(missingness),
                int(replicate),
            ]
        )
    )


def _scale_random_effects(
    generator_scales: dict,
    multiplier: float,
    *,
    r2: bool,
) -> RandomEffectScales:
    if multiplier <= 0.0:
        raise ValueError("variance-scale multiplier must be positive")
    if r2:
        return RandomEffectScales(
            participant_intercept_sd=float(
                generator_scales["participant_intercept_sd"]
            )
            * multiplier,
            item_intercept_sd=float(generator_scales["item_intercept_sd"])
            * multiplier,
            participant_slope_sd=float(
                generator_scales["participant_reward_slope_sd"]
            )
            * multiplier,
            item_slope_sd=float(generator_scales["item_reward_slope_sd"])
            * multiplier,
        )
    return RandomEffectScales(
        participant_intercept_sd=float(
            generator_scales["participant_intercept_sd"]
        )
        * multiplier,
        item_intercept_sd=float(generator_scales["item_intercept_sd"])
        * multiplier,
        participant_slope_sd=float(generator_scales["participant_slope_sd"])
        * multiplier,
        item_slope_sd=float(generator_scales["item_slope_sd"])
        * multiplier,
    )


def evaluate_r1_population(
    dataset,
    *,
    tau_grid: tuple[float, ...],
) -> CharacterizationOutcome:
    try:
        split = split_crossed(dataset.participant, dataset.item)
        fits = {
            family: fit_r1_candidate(
                family,
                dataset,
                split.train,
                tau_grid=tau_grid,
            )
            for family in R1_CANDIDATES
        }
        choice = select_r1_candidate(fits, dataset, split)
        return CharacterizationOutcome(choice.value, False)
    except (RuntimeError, ValueError, np.linalg.LinAlgError):
        return CharacterizationOutcome(FIT_FAILURE, True)


def evaluate_r1_hierarchical(
    dataset,
    *,
    residual_sd: float,
    scales: RandomEffectScales,
    tau_grid: tuple[float, ...],
) -> CharacterizationOutcome:
    try:
        split = split_crossed(dataset.participant, dataset.item)
        fits = {
            family: fit_r1_hierarchical_candidate(
                family,
                dataset,
                split.train,
                residual_sd=float(residual_sd),
                scales=scales,
                tau_grid=tau_grid,
            )
            for family in R1_CANDIDATES
        }
        choice = select_r1_hierarchical_candidate(fits, dataset, split)
        return CharacterizationOutcome(choice.value, False)
    except (RuntimeError, ValueError, np.linalg.LinAlgError):
        return CharacterizationOutcome(FIT_FAILURE, True)


def evaluate_r2_population(dataset) -> CharacterizationOutcome:
    try:
        split = split_crossed(dataset.participant, dataset.item)
        fits = {
            family: fit_r2_candidate(family, dataset, split.train)
            for family in R2_CANDIDATES
        }
        choice = select_r2_candidate(fits, dataset, split)
        return CharacterizationOutcome(choice.value, False)
    except (RuntimeError, ValueError, np.linalg.LinAlgError):
        return CharacterizationOutcome(FIT_FAILURE, True)


def evaluate_r2_hierarchical(
    dataset,
    *,
    scales: RandomEffectScales,
) -> CharacterizationOutcome:
    try:
        split = split_crossed(dataset.participant, dataset.item)
        fits = {
            family: fit_r2_hierarchical_candidate(
                family,
                dataset,
                split.train,
                scales=scales,
            )
            for family in R2_CANDIDATES
        }
        choice = select_r2_hierarchical_candidate(fits, dataset, split)
        return CharacterizationOutcome(choice.value, False)
    except (RuntimeError, ValueError, np.linalg.LinAlgError):
        return CharacterizationOutcome(FIT_FAILURE, True)


def _empty_counts(candidate_values: tuple[str, ...]) -> dict[str, int]:
    return {
        **{value: 0 for value in candidate_values},
        "INCONCLUSIVE": 0,
        FIT_FAILURE: 0,
    }


def _record(
    table: dict[tuple, dict[str, int]],
    key: tuple,
    outcome: CharacterizationOutcome,
    candidate_values: tuple[str, ...],
) -> None:
    if key not in table:
        table[key] = _empty_counts(candidate_values)
    table[key][outcome.selected] += 1


def _row(
    *,
    problem: str,
    generator: str,
    regime: str,
    missingness_rate: float,
    inference: str,
    scale_multiplier: float | None,
    counts: dict[str, int],
    replicates: int,
) -> dict:
    correct = counts[generator]
    failure = counts[FIT_FAILURE]
    inconclusive = counts["INCONCLUSIVE"]
    wrong = replicates - correct - failure - inconclusive
    return {
        "problem": problem,
        "generator": generator,
        "separation_regime": regime,
        "missingness_rate": float(missingness_rate),
        "inference": inference,
        "scale_multiplier": scale_multiplier,
        "replicates": int(replicates),
        "selected": counts,
        "recovery_probability": correct / replicates,
        "wrong_probability": wrong / replicates,
        "inconclusive_probability": inconclusive / replicates,
        "fit_failure_probability": failure / replicates,
    }


def _comparisons(rows: list[dict]) -> list[dict]:
    grouped: dict[tuple[str, str, str, float], dict[str, dict]] = defaultdict(dict)
    for row in rows:
        key = (
            row["problem"],
            row["generator"],
            row["separation_regime"],
            row["missingness_rate"],
        )
        grouped[key][row["inference"]] = row

    output: list[dict] = []
    for key, variants in sorted(grouped.items()):
        population = variants.get("POPULATION")
        if population is None:
            continue
        for inference, row in sorted(variants.items()):
            if inference == "POPULATION":
                continue
            output.append(
                {
                    "problem": key[0],
                    "generator": key[1],
                    "separation_regime": key[2],
                    "missingness_rate": key[3],
                    "hierarchical_inference": inference,
                    "recovery_delta_vs_population": (
                        row["recovery_probability"]
                        - population["recovery_probability"]
                    ),
                    "wrong_delta_vs_population": (
                        row["wrong_probability"]
                        - population["wrong_probability"]
                    ),
                    "inconclusive_delta_vs_population": (
                        row["inconclusive_probability"]
                        - population["inconclusive_probability"]
                    ),
                    "fit_failure_delta_vs_population": (
                        row["fit_failure_probability"]
                        - population["fit_failure_probability"]
                    ),
                }
            )
    return output


def run_characterization(config: dict) -> dict:
    if config["status"] != "NON_AUTHORITATIVE_CHARACTERIZATION_DESIGN":
        raise ValueError("only non-authoritative characterization configs are accepted")
    replicates = int(config["replicates_per_cell"])
    if replicates <= 0:
        raise ValueError("replicates_per_cell must be positive")

    scale_multipliers = tuple(
        float(x) for x in config["hierarchical_scale_multipliers"]
    )
    if not scale_multipliers or any(x <= 0 for x in scale_multipliers):
        raise ValueError("hierarchical scale multipliers must be positive")
    missingness_rates = tuple(float(x) for x in config["missingness_rates"])
    if any(not 0.0 <= x < 1.0 for x in missingness_rates):
        raise ValueError("missingness rates must lie in [0,1)")

    counts: dict[tuple, dict[str, int]] = {}
    seed = int(config["seed"])

    r1 = config["R1"]
    r1_generator_scales = r1["generator_random_effects"]
    for generator_index, family in enumerate(R1_CANDIDATES):
        for regime_index, regime_name in enumerate(config["separation_regimes"]):
            regime = r1["generator_regimes"][regime_name][family.value]
            for missing_index, missingness_rate in enumerate(missingness_rates):
                for replicate in range(replicates):
                    rng = _rng(
                        seed,
                        problem=1,
                        generator=generator_index,
                        regime=regime_index,
                        missingness=missing_index,
                        replicate=replicate,
                    )
                    dataset = simulate_r1_dataset(
                        family=family,
                        participants=int(r1["participants"]),
                        items=int(r1["items"]),
                        reliability_levels=tuple(
                            float(x) for x in r1["reliability_T"]
                        ),
                        evidence_levels=tuple(
                            float(x) for x in r1["signed_evidence_E"]
                        ),
                        intercept=float(regime["intercept"]),
                        evidence_scale=float(regime["evidence_scale"]),
                        noise_sd=float(regime["noise_sd"]),
                        participant_intercept_sd=float(
                            r1_generator_scales["participant_intercept_sd"]
                        ),
                        item_intercept_sd=float(
                            r1_generator_scales["item_intercept_sd"]
                        ),
                        participant_slope_sd=float(
                            r1_generator_scales["participant_slope_sd"]
                        ),
                        item_slope_sd=float(
                            r1_generator_scales["item_slope_sd"]
                        ),
                        rng=rng,
                        missingness_rate=missingness_rate,
                        tau=(
                            float(regime["tau"])
                            if family is R1Family.SR_C
                            else None
                        ),
                    )
                    population = evaluate_r1_population(
                        dataset,
                        tau_grid=tuple(float(x) for x in r1["tau_grid"]),
                    )
                    pop_key = (
                        "R1",
                        family.value,
                        regime_name,
                        missingness_rate,
                        "POPULATION",
                        None,
                    )
                    _record(
                        counts,
                        pop_key,
                        population,
                        tuple(x.value for x in R1_CANDIDATES),
                    )
                    for multiplier in scale_multipliers:
                        hierarchical = evaluate_r1_hierarchical(
                            dataset,
                            residual_sd=float(regime["noise_sd"]),
                            scales=_scale_random_effects(
                                r1_generator_scales,
                                multiplier,
                                r2=False,
                            ),
                            tau_grid=tuple(
                                float(x) for x in r1["tau_grid"]
                            ),
                        )
                        label = f"HIERARCHICAL_{multiplier:g}X"
                        key = (
                            "R1",
                            family.value,
                            regime_name,
                            missingness_rate,
                            label,
                            multiplier,
                        )
                        _record(
                            counts,
                            key,
                            hierarchical,
                            tuple(x.value for x in R1_CANDIDATES),
                        )

    r2 = config["R2"]
    r2_generator_scales = r2["generator_random_effects"]
    for generator_index, family in enumerate(R2_CANDIDATES):
        for regime_index, regime_name in enumerate(config["separation_regimes"]):
            regime = r2["generator_regimes"][regime_name][family.value]
            for missing_index, missingness_rate in enumerate(missingness_rates):
                for replicate in range(replicates):
                    rng = _rng(
                        seed,
                        problem=2,
                        generator=generator_index,
                        regime=regime_index,
                        missingness=missing_index,
                        replicate=replicate,
                    )
                    dataset = simulate_r2_dataset(
                        family=family,
                        participants=int(r2["participants"]),
                        items=int(r2["items"]),
                        belief_levels=tuple(float(x) for x in r2["belief_B"]),
                        accuracy_levels=tuple(
                            float(x) for x in r2["accuracy_cue_A"]
                        ),
                        reward_levels=tuple(
                            float(x) for x in r2["reward_context_R"]
                        ),
                        parameters=tuple(float(x) for x in regime["parameters"]),
                        participant_intercept_sd=float(
                            r2_generator_scales["participant_intercept_sd"]
                        ),
                        item_intercept_sd=float(
                            r2_generator_scales["item_intercept_sd"]
                        ),
                        participant_reward_slope_sd=float(
                            r2_generator_scales["participant_reward_slope_sd"]
                        ),
                        item_reward_slope_sd=float(
                            r2_generator_scales["item_reward_slope_sd"]
                        ),
                        rng=rng,
                        missingness_rate=missingness_rate,
                    )
                    population = evaluate_r2_population(dataset)
                    pop_key = (
                        "R2",
                        family.value,
                        regime_name,
                        missingness_rate,
                        "POPULATION",
                        None,
                    )
                    _record(
                        counts,
                        pop_key,
                        population,
                        tuple(x.value for x in R2_CANDIDATES),
                    )
                    for multiplier in scale_multipliers:
                        hierarchical = evaluate_r2_hierarchical(
                            dataset,
                            scales=_scale_random_effects(
                                r2_generator_scales,
                                multiplier,
                                r2=True,
                            ),
                        )
                        label = f"HIERARCHICAL_{multiplier:g}X"
                        key = (
                            "R2",
                            family.value,
                            regime_name,
                            missingness_rate,
                            label,
                            multiplier,
                        )
                        _record(
                            counts,
                            key,
                            hierarchical,
                            tuple(x.value for x in R2_CANDIDATES),
                        )

    rows = [
        _row(
            problem=key[0],
            generator=key[1],
            regime=key[2],
            missingness_rate=key[3],
            inference=key[4],
            scale_multiplier=key[5],
            counts=value,
            replicates=replicates,
        )
        for key, value in sorted(counts.items(), key=lambda item: str(item[0]))
    ]

    return {
        "characterization_id": config["characterization_id"],
        "status": "NON_AUTHORITATIVE_CHARACTERIZATION_RESULT",
        "authoritative": False,
        "seed": seed,
        "replicates_per_cell": replicates,
        "separation_regimes": list(config["separation_regimes"]),
        "missingness_rates": list(missingness_rates),
        "hierarchical_scale_multipliers": list(scale_multipliers),
        "grid_results": rows,
        "comparisons": _comparisons(rows),
        "interpretation_boundary": (
            "Non-authoritative inference characterization only. Population-level "
            "and penalized hierarchical recovery are compared on identical synthetic "
            "datasets. These results do not freeze an authoritative core grid, human "
            "sample size, variance model, empirical mechanism, or F1b runtime behavior."
        ),
    }
