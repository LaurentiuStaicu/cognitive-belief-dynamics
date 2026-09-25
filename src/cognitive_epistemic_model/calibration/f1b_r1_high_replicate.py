from __future__ import annotations

from collections import defaultdict
from math import sqrt

import numpy as np

from .f1b_prehuman_recovery import (
    R1Family,
    simulate_r1_dataset,
)
from .f1b_recovery_characterization import (
    FIT_FAILURE,
    _scale_random_effects,
    evaluate_r1_hierarchical,
    evaluate_r1_population,
)


R1_CANDIDATES = (R1Family.SR_A, R1Family.SR_B, R1Family.SR_C)


def wilson_interval(
    successes: int,
    total: int,
    *,
    z: float = 1.959963984540054,
) -> tuple[float, float]:
    if total <= 0:
        raise ValueError("total must be positive")
    if not 0 <= successes <= total:
        raise ValueError("successes must lie in [0,total]")
    p = successes / total
    z2 = z * z
    denom = 1.0 + z2 / total
    center = (p + z2 / (2.0 * total)) / denom
    half = (
        z
        * sqrt(
            p * (1.0 - p) / total
            + z2 / (4.0 * total * total)
        )
        / denom
    )
    low = max(0.0, center - half)
    high = min(1.0, center + half)
    if successes == 0:
        low = 0.0
    if successes == total:
        high = 1.0
    return low, high


def _rng(
    master_seed: int,
    *,
    generator: int,
    regime: int,
    missingness: int,
    replicate: int,
) -> np.random.Generator:
    return np.random.default_rng(
        np.random.SeedSequence(
            [
                int(master_seed),
                0xF1B1,
                int(generator),
                int(regime),
                int(missingness),
                int(replicate),
            ]
        )
    )


def _empty_counts() -> dict[str, int]:
    return {
        R1Family.SR_A.value: 0,
        R1Family.SR_B.value: 0,
        R1Family.SR_C.value: 0,
        R1Family.INCONCLUSIVE.value: 0,
        FIT_FAILURE: 0,
    }


def _summary_row(
    *,
    generator: str,
    regime: str,
    missingness_rate: float,
    inference: str,
    scale_multiplier: float | None,
    counts: dict[str, int],
    replicates: int,
) -> dict:
    correct = counts[generator]
    inconclusive = counts[R1Family.INCONCLUSIVE.value]
    failure = counts[FIT_FAILURE]
    wrong = replicates - correct - inconclusive - failure

    def metric(count: int) -> dict:
        low, high = wilson_interval(count, replicates)
        return {
            "count": count,
            "probability": count / replicates,
            "wilson_95": [low, high],
        }

    return {
        "generator": generator,
        "separation_regime": regime,
        "missingness_rate": float(missingness_rate),
        "inference": inference,
        "scale_multiplier": scale_multiplier,
        "replicates": replicates,
        "selected": counts,
        "recovery": metric(correct),
        "wrong": metric(wrong),
        "inconclusive": metric(inconclusive),
        "fit_failure": metric(failure),
    }


def _eligibility(rows: list[dict], config: dict) -> list[dict]:
    gate = config["design_eligibility"]
    inferences = sorted({row["inference"] for row in rows})
    output: list[dict] = []
    for inference in inferences:
        strong = [
            row
            for row in rows
            if row["inference"] == inference
            and row["separation_regime"] == "STRONG"
        ]
        checks = []
        for row in strong:
            checks.append(
                {
                    "generator": row["generator"],
                    "missingness_rate": row["missingness_rate"],
                    "recovery_probability_pass": (
                        row["recovery"]["probability"]
                        >= gate["strong_point_recovery_minimum"]
                    ),
                    "recovery_wilson_lower_pass": (
                        row["recovery"]["wilson_95"][0]
                        >= gate["strong_recovery_wilson_lower_minimum"]
                    ),
                    "wrong_probability_pass": (
                        row["wrong"]["probability"]
                        <= gate["wrong_probability_maximum"]
                    ),
                    "fit_failure_probability_pass": (
                        row["fit_failure"]["probability"]
                        <= gate["fit_failure_probability_maximum"]
                    ),
                }
            )
        eligible = bool(strong) and all(
            all(
                value
                for key, value in check.items()
                if key.endswith("_pass")
            )
            for check in checks
        )
        output.append(
            {
                "inference": inference,
                "strong_cells": len(strong),
                "checks": checks,
                "eligible_for_later_core_grid_design": eligible,
            }
        )
    return output


def run_r1_high_replicate_characterization(config: dict) -> dict:
    if config["status"] != "NON_AUTHORITATIVE_R1_HIGH_REPLICATE_DESIGN":
        raise ValueError("only the non-authoritative R1 design is accepted")

    replicates = int(config["replicates_per_cell"])
    if replicates <= 0:
        raise ValueError("replicates_per_cell must be positive")

    r1 = config["R1"]
    scale_multipliers = tuple(
        float(x) for x in config["hierarchical_scale_multipliers"]
    )
    missingness_rates = tuple(float(x) for x in config["missingness_rates"])
    regimes = tuple(str(x) for x in config["separation_regimes"])
    generator_scales = r1["generator_random_effects"]

    counts: dict[tuple, dict[str, int]] = defaultdict(_empty_counts)

    for generator_index, family in enumerate(R1_CANDIDATES):
        for regime_index, regime_name in enumerate(regimes):
            regime = r1["generator_regimes"][regime_name][family.value]
            for missing_index, missingness_rate in enumerate(missingness_rates):
                for replicate in range(replicates):
                    rng = _rng(
                        int(config["seed"]),
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
                            generator_scales["participant_intercept_sd"]
                        ),
                        item_intercept_sd=float(
                            generator_scales["item_intercept_sd"]
                        ),
                        participant_slope_sd=float(
                            generator_scales["participant_slope_sd"]
                        ),
                        item_slope_sd=float(
                            generator_scales["item_slope_sd"]
                        ),
                        rng=rng,
                        missingness_rate=float(missingness_rate),
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
                    counts[
                        (
                            family.value,
                            regime_name,
                            missingness_rate,
                            "POPULATION",
                            None,
                        )
                    ][population.selected] += 1

                    for multiplier in scale_multipliers:
                        hierarchical = evaluate_r1_hierarchical(
                            dataset,
                            residual_sd=float(regime["noise_sd"]),
                            scales=_scale_random_effects(
                                generator_scales,
                                multiplier,
                                r2=False,
                            ),
                            tau_grid=tuple(
                                float(x) for x in r1["tau_grid"]
                            ),
                        )
                        counts[
                            (
                                family.value,
                                regime_name,
                                missingness_rate,
                                f"HIERARCHICAL_{multiplier:g}X",
                                multiplier,
                            )
                        ][hierarchical.selected] += 1

    rows = [
        _summary_row(
            generator=key[0],
            regime=key[1],
            missingness_rate=key[2],
            inference=key[3],
            scale_multiplier=key[4],
            counts=value,
            replicates=replicates,
        )
        for key, value in sorted(counts.items(), key=lambda item: str(item[0]))
    ]

    return {
        "characterization_id": config["characterization_id"],
        "status": "NON_AUTHORITATIVE_R1_HIGH_REPLICATE_RESULT",
        "authoritative": False,
        "seed": int(config["seed"]),
        "replicates_per_cell": replicates,
        "grid_results": rows,
        "design_eligibility": _eligibility(rows, config),
        "interpretation_boundary": (
            "R1 design characterization only. Passing the prospective design-"
            "eligibility rule permits only later core-grid design work; it does "
            "not validate a human source-weighting mechanism, freeze human N, "
            "or authorize F1b runtime behavior."
        ),
    }
