from __future__ import annotations

from collections import defaultdict

import numpy as np

from .f1b_prehuman_recovery import R1Family, simulate_r1_dataset
from .f1b_r1_high_replicate import wilson_interval
from .f1b_recovery_characterization import (
    FIT_FAILURE,
    _scale_random_effects,
    evaluate_r1_hierarchical,
    evaluate_r1_population,
)


R1_CANDIDATES = (R1Family.SR_A, R1Family.SR_B, R1Family.SR_C)


def _rng(
    master_seed: int,
    *,
    participant_count: int,
    item_count: int,
    generator: int,
    missingness: int,
    replicate: int,
) -> np.random.Generator:
    return np.random.default_rng(
        np.random.SeedSequence(
            [
                int(master_seed),
                0xF1B141,
                int(participant_count),
                int(item_count),
                int(generator),
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


def _metric(count: int, total: int) -> dict:
    low, high = wilson_interval(count, total)
    return {
        "count": int(count),
        "probability": count / total,
        "wilson_95": [low, high],
    }


def _row(
    *,
    participants: int,
    items: int,
    generator: str,
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
    return {
        "participants": int(participants),
        "items": int(items),
        "generator": generator,
        "separation_regime": "STRONG",
        "missingness_rate": float(missingness_rate),
        "inference": inference,
        "scale_multiplier": scale_multiplier,
        "replicates": int(replicates),
        "selected": counts,
        "recovery": _metric(correct, replicates),
        "wrong": _metric(wrong, replicates),
        "inconclusive": _metric(inconclusive, replicates),
        "fit_failure": _metric(failure, replicates),
    }


def _eligibility(rows: list[dict], config: dict) -> list[dict]:
    gate = config["design_eligibility"]
    output = []
    designs = sorted(
        {
            (row["participants"], row["items"], row["inference"])
            for row in rows
        }
    )
    for participants, items, inference in designs:
        cells = [
            row
            for row in rows
            if row["participants"] == participants
            and row["items"] == items
            and row["inference"] == inference
        ]
        checks = []
        for row in cells:
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
        eligible = len(cells) == 6 and all(
            all(v for k, v in check.items() if k.endswith("_pass"))
            for check in checks
        )
        output.append(
            {
                "participants": participants,
                "items": items,
                "inference": inference,
                "strong_cells": len(cells),
                "checks": checks,
                "eligible_for_later_core_grid_design": eligible,
            }
        )
    return output


def _pareto_eligible(eligibility: list[dict]) -> list[dict]:
    eligible = [
        row for row in eligibility
        if row["eligible_for_later_core_grid_design"]
    ]
    frontier = []
    for row in eligible:
        dominated = any(
            other["inference"] == row["inference"]
            and other["participants"] <= row["participants"]
            and other["items"] <= row["items"]
            and (
                other["participants"] < row["participants"]
                or other["items"] < row["items"]
            )
            for other in eligible
        )
        if not dominated:
            frontier.append(row)
    return sorted(
        frontier,
        key=lambda x: (x["inference"], x["participants"] * x["items"], x["participants"], x["items"]),
    )


def run_r1_design_size_search(config: dict) -> dict:
    if config["status"] != "NON_AUTHORITATIVE_R1_DESIGN_SIZE_SEARCH":
        raise ValueError("only the frozen non-authoritative R1 design-size search is accepted")

    replicates = int(config["replicates_per_cell"])
    if replicates <= 0:
        raise ValueError("replicates_per_cell must be positive")

    participants_grid = tuple(int(x) for x in config["participant_counts"])
    items_grid = tuple(int(x) for x in config["item_counts"])
    missingness_rates = tuple(float(x) for x in config["missingness_rates"])
    multipliers = tuple(float(x) for x in config["hierarchical_scale_multipliers"])
    r1 = config["R1"]
    generator_scales = r1["generator_random_effects"]

    if any(x < 4 for x in participants_grid):
        raise ValueError("participant counts must be >= 4")
    if any(x < 12 or x % 12 != 0 for x in items_grid):
        raise ValueError("item counts must be multiples of the 12 frozen R1 condition cells")
    if any(not 0.0 <= x < 1.0 for x in missingness_rates):
        raise ValueError("missingness rates must lie in [0,1)")

    counts: dict[tuple, dict[str, int]] = defaultdict(_empty_counts)

    for participants in participants_grid:
        for items in items_grid:
            for generator_index, family in enumerate(R1_CANDIDATES):
                regime = r1["generator_regimes"]["STRONG"][family.value]
                for missing_index, missingness_rate in enumerate(missingness_rates):
                    for replicate in range(replicates):
                        rng = _rng(
                            int(config["seed"]),
                            participant_count=participants,
                            item_count=items,
                            generator=generator_index,
                            missingness=missing_index,
                            replicate=replicate,
                        )
                        dataset = simulate_r1_dataset(
                            family=family,
                            participants=participants,
                            items=items,
                            reliability_levels=tuple(float(x) for x in r1["reliability_T"]),
                            evidence_levels=tuple(float(x) for x in r1["signed_evidence_E"]),
                            intercept=float(regime["intercept"]),
                            evidence_scale=float(regime["evidence_scale"]),
                            noise_sd=float(regime["noise_sd"]),
                            participant_intercept_sd=float(generator_scales["participant_intercept_sd"]),
                            item_intercept_sd=float(generator_scales["item_intercept_sd"]),
                            participant_slope_sd=float(generator_scales["participant_slope_sd"]),
                            item_slope_sd=float(generator_scales["item_slope_sd"]),
                            rng=rng,
                            missingness_rate=missingness_rate,
                            tau=float(regime["tau"]) if family is R1Family.SR_C else None,
                        )

                        population = evaluate_r1_population(
                            dataset,
                            tau_grid=tuple(float(x) for x in r1["tau_grid"]),
                        )
                        counts[
                            (
                                participants,
                                items,
                                family.value,
                                missingness_rate,
                                "POPULATION",
                                None,
                            )
                        ][population.selected] += 1

                        for multiplier in multipliers:
                            hierarchical = evaluate_r1_hierarchical(
                                dataset,
                                residual_sd=float(regime["noise_sd"]),
                                scales=_scale_random_effects(
                                    generator_scales,
                                    multiplier,
                                    r2=False,
                                ),
                                tau_grid=tuple(float(x) for x in r1["tau_grid"]),
                            )
                            counts[
                                (
                                    participants,
                                    items,
                                    family.value,
                                    missingness_rate,
                                    f"HIERARCHICAL_{multiplier:g}X",
                                    multiplier,
                                )
                            ][hierarchical.selected] += 1

    rows = [
        _row(
            participants=key[0],
            items=key[1],
            generator=key[2],
            missingness_rate=key[3],
            inference=key[4],
            scale_multiplier=key[5],
            counts=value,
            replicates=replicates,
        )
        for key, value in sorted(counts.items(), key=lambda kv: str(kv[0]))
    ]
    eligibility = _eligibility(rows, config)

    return {
        "search_id": config["search_id"],
        "status": "NON_AUTHORITATIVE_R1_DESIGN_SIZE_SEARCH_RESULT",
        "authoritative": False,
        "seed": int(config["seed"]),
        "replicates_per_cell": replicates,
        "participant_counts": list(participants_grid),
        "item_counts": list(items_grid),
        "grid_results": rows,
        "design_eligibility": eligibility,
        "pareto_eligible_designs": _pareto_eligible(eligibility),
        "interpretation_boundary": (
            "Synthetic design-size recovery search only. Any eligible participant×item count "
            "is a simulation design region, not a human sample-size recommendation, and does "
            "not select a final inference method or authorize recruitment/runtime F1b."
        ),
    }
