from __future__ import annotations

from hashlib import sha256
from math import sqrt
from statistics import NormalDist

import numpy as np

from cognitive_epistemic_model.calibration.m1_e4_candidate_recovery import (
    RecoveryFamily,
)
from cognitive_epistemic_model.calibration.m1_e4_participant_recovery import (
    CONDITIONS,
    fit_hierarchical_candidate,
    select_hierarchical_candidate,
    simulate_participant_dataset,
)


def cell_seed(base_seed: int, cell_id: str) -> int:
    payload = f"{int(base_seed)}|{cell_id}|phase-j-v1".encode()
    return int(sha256(payload).hexdigest()[:8], 16)


def wilson_interval(successes: int, trials: int, level: float = 0.95) -> tuple[float, float]:
    if trials <= 0:
        raise ValueError("trials must be positive")
    if not 0 <= successes <= trials:
        raise ValueError("successes must lie in [0, trials]")
    if not 0.0 < level < 1.0:
        raise ValueError("level must lie in (0, 1)")

    p = successes / trials
    z = NormalDist().inv_cdf(0.5 + level / 2.0)
    z2 = z * z
    denominator = 1.0 + z2 / trials
    center = (p + z2 / (2.0 * trials)) / denominator
    radius = (
        z
        * sqrt((p * (1.0 - p) / trials) + z2 / (4.0 * trials * trials))
        / denominator
    )
    return max(0.0, center - radius), min(1.0, center + radius)


def _lookup_by_label(items: list[dict], label: str) -> dict:
    matches = [item for item in items if item["label"] == label]
    if len(matches) != 1:
        raise ValueError(f"expected exactly one item with label {label!r}")
    return matches[0]


def _lookup_cell_inputs(
    screening_config: dict,
    selected_cell: dict,
) -> tuple[dict, dict, dict[str, float], tuple[float, ...]]:
    allocation = _lookup_by_label(
        screening_config["participant_allocations"],
        selected_cell["allocation"],
    )
    heterogeneity = _lookup_by_label(
        screening_config["heterogeneity_regimes"],
        selected_cell["heterogeneity"],
    )
    generator = selected_cell["generator"]
    memory_regime = _lookup_by_label(
        screening_config["memory_grids"][generator],
        selected_cell["regime"],
    )
    truth = {
        "complex": float(memory_regime["complex"]),
        "simple": float(memory_regime["simple"]),
    }
    biases = tuple(float(x) for x in screening_config["bias_grids"][generator])
    return allocation, heterogeneity, truth, biases


def run_confirmation_cell(
    *,
    confirmation_config: dict,
    screening_config: dict,
    selected_cell: dict,
) -> dict:
    replicates = int(confirmation_config["replicates_per_cell"])
    threshold = float(confirmation_config["recovery_threshold"])
    quadrature_nodes = int(confirmation_config["quadrature_nodes"])
    generator = RecoveryFamily(selected_cell["generator"])
    rng = np.random.default_rng(
        cell_seed(confirmation_config["base_seed"], selected_cell["cell_id"])
    )

    allocation, heterogeneity, truth, biases = _lookup_cell_inputs(
        screening_config,
        selected_cell,
    )

    participants = int(allocation["participants"])
    n_target = int(allocation["target_trials_per_participant_per_cell"])
    n_foil = int(allocation["foil_trials_per_participant_per_cell"])
    sigma_memory = float(heterogeneity["sigma_memory"])
    sigma_bias = float(heterogeneity["sigma_bias"])

    selected = {x.value: 0 for x in RecoveryFamily}
    memory_errors = {condition: [] for condition in CONDITIONS}
    sigma_memory_errors: list[float] = []
    sigma_bias_errors: list[float] = []

    for _ in range(replicates):
        train = simulate_participant_dataset(
            family=generator,
            population_memory=truth,
            population_biases=biases,
            participants=participants,
            n_target_per_cell=n_target,
            n_foil_per_cell=n_foil,
            sigma_memory=sigma_memory,
            sigma_bias=sigma_bias,
            rng=rng,
        )
        held_out = simulate_participant_dataset(
            family=generator,
            population_memory=truth,
            population_biases=biases,
            participants=participants,
            n_target_per_cell=n_target,
            n_foil_per_cell=n_foil,
            sigma_memory=sigma_memory,
            sigma_bias=sigma_bias,
            rng=rng,
        )

        evsd_fit = fit_hierarchical_candidate(
            RecoveryFamily.EVSD,
            train,
            quadrature_nodes=quadrature_nodes,
        )
        two_ht_fit = fit_hierarchical_candidate(
            RecoveryFamily.TWO_HT,
            train,
            quadrature_nodes=quadrature_nodes,
        )
        choice = select_hierarchical_candidate(
            evsd_fit=evsd_fit,
            two_ht_fit=two_ht_fit,
            held_out=held_out,
            quadrature_nodes=quadrature_nodes,
        )
        selected[choice.value] += 1

        true_fit = evsd_fit if generator is RecoveryFamily.EVSD else two_ht_fit
        for condition in CONDITIONS:
            memory_errors[condition].append(
                abs(true_fit.population_memory[condition] - truth[condition])
            )
        sigma_memory_errors.append(abs(true_fit.sigma_memory - sigma_memory))
        sigma_bias_errors.append(abs(true_fit.sigma_bias - sigma_bias))

    correct = selected[generator.value]
    wrong_family = (
        RecoveryFamily.TWO_HT.value
        if generator is RecoveryFamily.EVSD
        else RecoveryFamily.EVSD.value
    )
    recovery = correct / replicates
    low, high = wilson_interval(
        correct,
        replicates,
        level=float(
            confirmation_config["robustness_sensitivity"]["wilson_interval_level"]
        ),
    )

    return {
        "cell_id": selected_cell["cell_id"],
        "role": selected_cell["role"],
        "allocation": selected_cell["allocation"],
        "heterogeneity": selected_cell["heterogeneity"],
        "generator": generator.value,
        "regime": selected_cell["regime"],
        "screening_recovery": float(selected_cell["screening_recovery"]),
        "seed": cell_seed(
            confirmation_config["base_seed"],
            selected_cell["cell_id"],
        ),
        "participants": participants,
        "target_trials_per_participant_per_cell": n_target,
        "foil_trials_per_participant_per_cell": n_foil,
        "replicates": replicates,
        "selected": selected,
        "recovery_probability": recovery,
        "wrong_probability": selected[wrong_family] / replicates,
        "inconclusive_probability": selected[RecoveryFamily.INCONCLUSIVE.value]
        / replicates,
        "wilson_lower": low,
        "wilson_upper": high,
        "passes_formal_recovery_gate": recovery >= threshold,
        "passes_secondary_wilson_margin": low >= threshold,
        "memory_parameter_mae": {
            key: float(np.mean(values))
            for key, values in memory_errors.items()
        },
        "sigma_memory_mae": float(np.mean(sigma_memory_errors)),
        "sigma_bias_mae": float(np.mean(sigma_bias_errors)),
    }


def summarize_confirmation(
    confirmation_config: dict,
    results: list[dict],
) -> dict:
    expected_ids = {
        item["cell_id"] for item in confirmation_config["selected_cells"]
    }
    actual_ids = {row["cell_id"] for row in results}
    if expected_ids != actual_ids:
        raise ValueError("confirmation results do not match the frozen cell set")

    primary = [row for row in results if row["role"] == "PRIMARY_P64_FULL_GRID"]
    boundary = [
        row for row in results if row["role"] == "BOUNDARY_MINIMUM_WITH_TIES"
    ]

    return {
        "benchmark_id": confirmation_config["benchmark_id"],
        "replicates_per_cell": confirmation_config["replicates_per_cell"],
        "selected_cells_total": len(results),
        "primary_cells": len(primary),
        "boundary_cells": len(boundary),
        "primary_minimum_recovery": min(
            row["recovery_probability"] for row in primary
        ),
        "primary_all_formal_gate_pass": all(
            row["passes_formal_recovery_gate"] for row in primary
        ),
        "primary_all_secondary_wilson_margin_pass": all(
            row["passes_secondary_wilson_margin"] for row in primary
        ),
        "boundary_minimum_recovery": min(
            row["recovery_probability"] for row in boundary
        ),
        "wrong_family_selections_total": sum(
            row["selected"][
                "2HT" if row["generator"] == "EVSD" else "EVSD"
            ]
            for row in results
        ),
        "inconclusive_total": sum(
            row["selected"]["INCONCLUSIVE"] for row in results
        ),
        "results": sorted(results, key=lambda row: row["cell_id"]),
        "interpretation_boundary": (
            "A confirmation pass validates the frozen synthetic participant-aware "
            "design under the tested model families and parameter grid. It does not "
            "establish human cognitive truth, identify Pencode, or by itself authorize "
            "participant recruitment."
        ),
    }
