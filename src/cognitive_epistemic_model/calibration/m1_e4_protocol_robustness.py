from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from math import log, sqrt
from statistics import NormalDist

import numpy as np
from scipy.special import expit, ndtr

from cognitive_epistemic_model.calibration.m1_e4_candidate_recovery import (
    RecoveryFamily,
)
from cognitive_epistemic_model.calibration.m1_e4_participant_recovery import (
    CONDITIONS,
    ParticipantDataset,
    _logit,
    fit_hierarchical_candidate,
    select_hierarchical_candidate,
)


@dataclass(frozen=True)
class StressDiagnostics:
    generated_participants: int
    retained_participants: int
    retention_fraction: float
    item_memory_sd: float
    item_bias_sd: float
    participant_memory_bias_rho: float
    serial_memory_slope: float
    attrition_type: str


def phase_m_cell_seed(base_seed: int, profile_id: str, generator: str) -> int:
    payload = f"{int(base_seed)}|{profile_id}|{generator}|phase-m-v1".encode()
    return int(sha256(payload).hexdigest()[:8], 16)


def _validate_profile(profile: dict) -> None:
    item_memory_sd = float(profile["item_memory_sd"])
    item_bias_sd = float(profile["item_bias_sd"])
    rho = float(profile["participant_memory_bias_rho"])
    if item_memory_sd < 0 or item_bias_sd < 0:
        raise ValueError("item stress scales must be non-negative")
    if not -0.95 <= rho <= 0.95:
        raise ValueError("participant random-effect correlation must lie in [-0.95,0.95]")
    attrition = profile["attrition"]
    if attrition["type"] not in {"NONE", "MAR_LIKE", "LATENT_MEMORY_ASSOCIATED"}:
        raise ValueError("unsupported attrition type")


def _participant_random_effects(
    participants: int,
    sigma_memory: float,
    sigma_bias: float,
    rho: float,
    rng: np.random.Generator,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    if participants <= 1:
        raise ValueError("at least two generated participants are required")
    if sigma_memory < 0 or sigma_bias < 0:
        raise ValueError("participant heterogeneity scales must be non-negative")
    covariance = np.asarray([[1.0, rho], [rho, 1.0]], dtype=float)
    standardized = rng.multivariate_normal(
        mean=np.zeros(2, dtype=float), covariance=covariance, size=participants
    )
    z_memory = standardized[:, 0]
    return z_memory * sigma_memory, standardized[:, 1] * sigma_bias, z_memory


def _retention_mask(
    *,
    z_memory: np.ndarray,
    attrition: dict,
    rng: np.random.Generator,
) -> np.ndarray:
    kind = attrition["type"]
    if kind == "NONE":
        return np.ones(z_memory.size, dtype=bool)

    base_probability = float(attrition["base_probability"])
    if not 0.0 <= base_probability < 1.0:
        raise ValueError("base attrition probability must lie in [0,1)")

    if kind == "MAR_LIKE":
        probabilities = np.full(z_memory.size, base_probability, dtype=float)
    else:
        coefficient = float(attrition["memory_logit_coefficient"])
        maximum = float(attrition["maximum_probability"])
        if not base_probability < maximum < 1.0:
            raise ValueError("maximum attrition probability must exceed base and be below 1")
        logits = _logit(base_probability) + coefficient * z_memory
        probabilities = np.minimum(expit(logits), maximum)

    return rng.random(z_memory.size) >= probabilities


def _item_effects(
    conditions: int,
    operating_points: int,
    trials: int,
    memory_sd: float,
    bias_sd: float,
    rng: np.random.Generator,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    shape = (conditions, operating_points, trials)
    return (
        rng.normal(0.0, memory_sd, size=shape),
        rng.normal(0.0, bias_sd, size=shape),
        rng.normal(0.0, memory_sd, size=shape),
        rng.normal(0.0, bias_sd, size=shape),
    )


def simulate_protocol_stress_dataset(
    *,
    family: RecoveryFamily,
    population_memory: dict[str, float],
    population_biases: tuple[float, ...],
    generated_participants: int,
    n_target_per_cell: int,
    n_foil_per_cell: int,
    sigma_memory: float,
    sigma_bias: float,
    profile: dict,
    rng: np.random.Generator,
) -> tuple[ParticipantDataset, StressDiagnostics]:
    """Generate Phase-M data with nuisance structure absent from the fitted model."""
    if family not in (RecoveryFamily.EVSD, RecoveryFamily.TWO_HT):
        raise ValueError("Phase M supports only EVSD and 2HT generators")
    if n_target_per_cell <= 0 or n_foil_per_cell <= 0:
        raise ValueError("trial counts must be positive")
    _validate_profile(profile)

    biases = np.asarray(tuple(float(x) for x in population_biases), dtype=float)
    if biases.size < 3:
        raise ValueError("at least three bias operating points are required")
    memory = np.asarray([float(population_memory[x]) for x in CONDITIONS], dtype=float)

    if family is RecoveryFamily.EVSD:
        if np.any(memory <= 0):
            raise ValueError("EVSD memory values must be positive")
    else:
        if np.any((memory <= 0) | (memory >= 1)):
            raise ValueError("2HT detection values must lie in (0,1)")
        if np.any((biases <= 0) | (biases >= 1)):
            raise ValueError("2HT guessing values must lie in (0,1)")

    rho = float(profile["participant_memory_bias_rho"])
    participant_memory, participant_bias, z_memory = _participant_random_effects(
        generated_participants, sigma_memory, sigma_bias, rho, rng
    )
    keep = _retention_mask(z_memory=z_memory, attrition=profile["attrition"], rng=rng)
    if int(keep.sum()) < 2:
        raise RuntimeError("attrition left fewer than two participants")

    participant_memory = participant_memory[keep]
    participant_bias = participant_bias[keep]
    retained = int(keep.sum())

    item_memory_sd = float(profile["item_memory_sd"])
    item_bias_sd = float(profile["item_bias_sd"])
    target_mem, target_bias, foil_mem, foil_bias = _item_effects(
        len(CONDITIONS), biases.size, n_target_per_cell, item_memory_sd, item_bias_sd, rng
    )
    if n_foil_per_cell != n_target_per_cell:
        foil_mem = rng.normal(
            0.0, item_memory_sd, size=(len(CONDITIONS), biases.size, n_foil_per_cell)
        )
        foil_bias = rng.normal(
            0.0, item_bias_sd, size=(len(CONDITIONS), biases.size, n_foil_per_cell)
        )

    hits = np.zeros((retained, len(CONDITIONS), biases.size), dtype=int)
    false_alarms = np.zeros_like(hits)
    centered_positions = np.arange(biases.size, dtype=float) - (biases.size - 1.0) / 2.0
    serial_slope = float(profile["serial_memory_slope"])

    for p in range(retained):
        sequence = rng.permutation(biases.size)
        position_by_bias = np.empty(biases.size, dtype=float)
        position_by_bias[sequence] = centered_positions

        for j in range(len(CONDITIONS)):
            for k in range(biases.size):
                serial_shift = serial_slope * position_by_bias[k]

                if family is RecoveryFamily.EVSD:
                    base_d = memory[j] * np.exp(participant_memory[p] + serial_shift)
                    target_d = base_d * np.exp(target_mem[j, k])
                    foil_d = base_d * np.exp(foil_mem[j, k])
                    target_c = biases[k] + participant_bias[p] + target_bias[j, k]
                    foil_c = biases[k] + participant_bias[p] + foil_bias[j, k]
                    hit_prob = ndtr(target_d / 2.0 - target_c)
                    fa_prob = ndtr(-foil_d / 2.0 - foil_c)
                else:
                    base_detection_logit = _logit(memory[j]) + participant_memory[p] + serial_shift
                    target_detection = expit(base_detection_logit + target_mem[j, k])
                    foil_detection = expit(base_detection_logit + foil_mem[j, k])
                    base_guess_logit = _logit(float(biases[k])) + participant_bias[p]
                    target_guess = expit(base_guess_logit + target_bias[j, k])
                    foil_guess = expit(base_guess_logit + foil_bias[j, k])
                    hit_prob = target_detection + (1.0 - target_detection) * target_guess
                    fa_prob = (1.0 - foil_detection) * foil_guess

                hits[p, j, k] = int((rng.random(n_target_per_cell) < hit_prob).sum())
                false_alarms[p, j, k] = int(
                    (rng.random(n_foil_per_cell) < fa_prob).sum()
                )

    dataset = ParticipantDataset(
        hits=hits,
        false_alarms=false_alarms,
        n_target_per_cell=n_target_per_cell,
        n_foil_per_cell=n_foil_per_cell,
    )
    diagnostics = StressDiagnostics(
        generated_participants=generated_participants,
        retained_participants=retained,
        retention_fraction=retained / generated_participants,
        item_memory_sd=item_memory_sd,
        item_bias_sd=item_bias_sd,
        participant_memory_bias_rho=rho,
        serial_memory_slope=serial_slope,
        attrition_type=str(profile["attrition"]["type"]),
    )
    return dataset, diagnostics


def wilson_interval(successes: int, total: int, level: float = 0.95) -> tuple[float, float]:
    if total <= 0 or not 0.0 < level < 1.0:
        raise ValueError("invalid Wilson interval inputs")
    p = successes / total
    z = NormalDist().inv_cdf(0.5 + level / 2.0)
    z2 = z * z
    denominator = 1.0 + z2 / total
    center = (p + z2 / (2.0 * total)) / denominator
    half = z * sqrt(p * (1.0 - p) / total + z2 / (4.0 * total * total)) / denominator
    return max(0.0, center - half), min(1.0, center + half)


def _profile_by_id(config: dict, profile_id: str) -> dict:
    matches = [x for x in config["profiles"] if x["id"] == profile_id]
    if len(matches) != 1:
        raise ValueError(f"profile {profile_id!r} must occur exactly once")
    return matches[0]


def run_protocol_robustness_cell(
    config: dict,
    *,
    profile_id: str,
    generator: str,
    replicate_override: int | None = None,
) -> dict:
    profile = _profile_by_id(config, profile_id)
    try:
        family = RecoveryFamily(generator)
    except ValueError as exc:
        raise ValueError("generator must be EVSD or 2HT") from exc
    if family not in (RecoveryFamily.EVSD, RecoveryFamily.TWO_HT):
        raise ValueError("generator must be EVSD or 2HT")

    replicates = int(config["replicates_per_cell"] if replicate_override is None else replicate_override)
    if replicates <= 0:
        raise ValueError("replicates must be positive")
    threshold = float(config["recovery_threshold"])
    quadrature_nodes = int(config["quadrature_nodes"])
    allocation = config["allocation"]
    generated_participants = int(allocation["generated_participants"])
    n_target = int(allocation["target_trials_per_participant_per_cell"])
    n_foil = int(allocation["foil_trials_per_participant_per_cell"])
    sigma_memory = float(config["participant_heterogeneity"]["sigma_memory"])
    sigma_bias = float(config["participant_heterogeneity"]["sigma_bias"])
    truth = {k: float(v) for k, v in config["weak_memory_truth"][family.value].items()}
    biases = tuple(float(x) for x in config["bias_grids"][family.value])
    seed = phase_m_cell_seed(int(config["base_seed"]), profile_id, family.value)
    rng = np.random.default_rng(seed)

    selected = {x.value: 0 for x in RecoveryFamily}
    memory_errors = {name: [] for name in CONDITIONS}
    sigma_memory_errors: list[float] = []
    sigma_bias_errors: list[float] = []
    retained_train: list[int] = []
    retained_held_out: list[int] = []

    for _ in range(replicates):
        train, train_diag = simulate_protocol_stress_dataset(
            family=family,
            population_memory=truth,
            population_biases=biases,
            generated_participants=generated_participants,
            n_target_per_cell=n_target,
            n_foil_per_cell=n_foil,
            sigma_memory=sigma_memory,
            sigma_bias=sigma_bias,
            profile=profile,
            rng=rng,
        )
        held_out, held_diag = simulate_protocol_stress_dataset(
            family=family,
            population_memory=truth,
            population_biases=biases,
            generated_participants=generated_participants,
            n_target_per_cell=n_target,
            n_foil_per_cell=n_foil,
            sigma_memory=sigma_memory,
            sigma_bias=sigma_bias,
            profile=profile,
            rng=rng,
        )
        retained_train.append(train_diag.retained_participants)
        retained_held_out.append(held_diag.retained_participants)

        evsd_fit = fit_hierarchical_candidate(
            RecoveryFamily.EVSD, train, quadrature_nodes=quadrature_nodes
        )
        two_ht_fit = fit_hierarchical_candidate(
            RecoveryFamily.TWO_HT, train, quadrature_nodes=quadrature_nodes
        )
        choice = select_hierarchical_candidate(
            evsd_fit=evsd_fit,
            two_ht_fit=two_ht_fit,
            held_out=held_out,
            quadrature_nodes=quadrature_nodes,
        )
        selected[choice.value] += 1

        true_fit = evsd_fit if family is RecoveryFamily.EVSD else two_ht_fit
        for condition in CONDITIONS:
            memory_errors[condition].append(
                abs(true_fit.population_memory[condition] - truth[condition])
            )
        sigma_memory_errors.append(abs(true_fit.sigma_memory - sigma_memory))
        sigma_bias_errors.append(abs(true_fit.sigma_bias - sigma_bias))

    correct = selected[family.value]
    wrong_family = (
        RecoveryFamily.TWO_HT.value
        if family is RecoveryFamily.EVSD
        else RecoveryFamily.EVSD.value
    )
    recovery = correct / replicates
    lower, upper = wilson_interval(correct, replicates)
    mcse = sqrt(recovery * (1.0 - recovery) / replicates)

    return {
        "benchmark_id": config["benchmark_id"],
        "phase": "M",
        "profile_id": profile_id,
        "generator": family.value,
        "cell_id": f"{profile_id}__{family.value}",
        "seed": seed,
        "replicates": replicates,
        "selected": selected,
        "recovery_probability": recovery,
        "wrong_probability": selected[wrong_family] / replicates,
        "inconclusive_probability": selected[RecoveryFamily.INCONCLUSIVE.value] / replicates,
        "wilson_95": {"lower": lower, "upper": upper},
        "monte_carlo_standard_error": mcse,
        "passes_formal_gate": recovery >= threshold,
        "passes_secondary_wilson_sensitivity": lower >= threshold,
        "memory_parameter_mae": {
            key: float(np.mean(values)) for key, values in memory_errors.items()
        },
        "sigma_memory_mae": float(np.mean(sigma_memory_errors)),
        "sigma_bias_mae": float(np.mean(sigma_bias_errors)),
        "retention": {
            "generated_participants": generated_participants,
            "mean_retained_train": float(np.mean(retained_train)),
            "minimum_retained_train": int(min(retained_train)),
            "mean_retained_held_out": float(np.mean(retained_held_out)),
            "minimum_retained_held_out": int(min(retained_held_out)),
        },
        "profile": profile,
        "interpretation_boundary": (
            "Synthetic protocol-robustness cell only. Nuisance values are demonstrative, "
            "the fitted candidates intentionally omit the added nuisance structure, and "
            "the result does not identify a human cognitive architecture or authorize recruitment."
        ),
    }


def summarize_protocol_robustness_results(config: dict, rows: list[dict]) -> dict:
    expected = {
        f"{profile['id']}__{generator}"
        for profile in config["profiles"]
        for generator in config["generators"]
    }
    by_id = {row["cell_id"]: row for row in rows}
    if set(by_id) != expected or len(rows) != len(expected):
        missing = sorted(expected - set(by_id))
        extra = sorted(set(by_id) - expected)
        raise ValueError(f"Phase M cell surface mismatch; missing={missing}, extra={extra}")

    ordered = [by_id[cell_id] for cell_id in sorted(expected)]
    failed = [row["cell_id"] for row in ordered if not row["passes_formal_gate"]]
    wilson_failed = [
        row["cell_id"]
        for row in ordered
        if not row["passes_secondary_wilson_sensitivity"]
    ]
    return {
        "benchmark_id": config["benchmark_id"],
        "phase": "M",
        "status": "PROTOCOL_ROBUSTNESS_PASS" if not failed else "PROTOCOL_ROBUSTNESS_FAIL",
        "selected_cells_total": len(ordered),
        "replicates_per_cell": int(config["replicates_per_cell"]),
        "formal_gate": float(config["recovery_threshold"]),
        "formal_failed_cells": failed,
        "secondary_wilson_failed_cells": wilson_failed,
        "minimum_recovery_probability": min(row["recovery_probability"] for row in ordered),
        "minimum_wilson_lower": min(row["wilson_95"]["lower"] for row in ordered),
        "wrong_family_selections_total": sum(
            row["selected"][
                RecoveryFamily.TWO_HT.value
                if row["generator"] == RecoveryFamily.EVSD.value
                else RecoveryFamily.EVSD.value
            ]
            for row in ordered
        ),
        "inconclusive_total": sum(
            row["selected"][RecoveryFamily.INCONCLUSIVE.value] for row in ordered
        ),
        "results": ordered,
        "interpretation_boundary": (
            "Phase M closes a prospective synthetic stress gate only. PASS/FAIL does not "
            "select a human model, identify Pencode, validate a human sample size or authorize recruitment."
        ),
    }
