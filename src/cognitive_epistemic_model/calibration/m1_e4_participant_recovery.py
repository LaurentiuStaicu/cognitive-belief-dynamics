from __future__ import annotations

from dataclasses import dataclass
from math import log, pi, sqrt
from typing import Iterable

import numpy as np
from scipy.optimize import minimize
from scipy.special import expit, gammaln, logsumexp, xlog1py, xlogy

from cognitive_epistemic_model.calibration.m1_e4_candidate_recovery import (
    RecoveryFamily,
    RecognitionCounts,
    fit_candidate,
)


CONDITIONS = ("complex", "simple")


@dataclass(frozen=True)
class ParticipantDataset:
    hits: np.ndarray
    false_alarms: np.ndarray
    n_target_per_cell: int
    n_foil_per_cell: int

    def __post_init__(self) -> None:
        if self.hits.shape != self.false_alarms.shape:
            raise ValueError("hits and false_alarms must have identical shapes")
        if self.hits.ndim != 3 or self.hits.shape[1] != 2:
            raise ValueError("expected shape participants x 2 conditions x bias points")
        if self.n_target_per_cell <= 0 or self.n_foil_per_cell <= 0:
            raise ValueError("per-cell trial counts must be positive")
        if np.any(self.hits < 0) or np.any(self.hits > self.n_target_per_cell):
            raise ValueError("hit counts out of bounds")
        if np.any(self.false_alarms < 0) or np.any(
            self.false_alarms > self.n_foil_per_cell
        ):
            raise ValueError("false-alarm counts out of bounds")

    @property
    def participants(self) -> int:
        return int(self.hits.shape[0])

    @property
    def operating_points(self) -> int:
        return int(self.hits.shape[2])


@dataclass(frozen=True)
class HierarchicalFit:
    family: RecoveryFamily
    population_memory: dict[str, float]
    population_biases: tuple[float, ...]
    sigma_memory: float
    sigma_bias: float
    log_likelihood: float
    parameter_count: int

    @property
    def aic(self) -> float:
        return 2.0 * self.parameter_count - 2.0 * self.log_likelihood


def _logit(value: float) -> float:
    eps = 1e-7
    x = float(np.clip(value, eps, 1.0 - eps))
    return float(np.log(x / (1.0 - x)))


def _binomial_ll_array(
    successes: np.ndarray,
    total: int,
    probability: np.ndarray,
) -> np.ndarray:
    eps = np.finfo(float).eps
    p = np.clip(probability, eps, 1.0 - eps)
    s = successes.astype(float)
    log_choose = (
        gammaln(total + 1)
        - gammaln(s + 1)
        - gammaln(total - s + 1)
    )
    return log_choose + xlogy(s, p) + xlog1py(total - s, -p)


def simulate_participant_dataset(
    *,
    family: RecoveryFamily,
    population_memory: dict[str, float],
    population_biases: Iterable[float],
    participants: int,
    n_target_per_cell: int,
    n_foil_per_cell: int,
    sigma_memory: float,
    sigma_bias: float,
    rng: np.random.Generator,
) -> ParticipantDataset:
    if family not in (RecoveryFamily.EVSD, RecoveryFamily.TWO_HT):
        raise ValueError("only EVSD and 2HT can generate participant-aware data")
    if participants <= 1:
        raise ValueError("participant-aware simulation requires at least two participants")
    if sigma_memory < 0 or sigma_bias < 0:
        raise ValueError("heterogeneity scales must be non-negative")

    biases = np.asarray(tuple(float(x) for x in population_biases), dtype=float)
    if biases.size < 3:
        raise ValueError("at least three operating points are required")

    memory = np.asarray(
        [float(population_memory[name]) for name in CONDITIONS],
        dtype=float,
    )
    if family is RecoveryFamily.EVSD:
        if np.any(memory <= 0):
            raise ValueError("EVSD population memory must be positive")
    else:
        if np.any((memory <= 0) | (memory >= 1)):
            raise ValueError("2HT population detection must lie strictly inside (0,1)")
        if np.any((biases <= 0) | (biases >= 1)):
            raise ValueError("2HT population guessing values must lie inside (0,1)")

    participant_memory = rng.normal(0.0, sigma_memory, size=participants)
    participant_bias = rng.normal(0.0, sigma_bias, size=participants)

    hits = np.zeros((participants, 2, biases.size), dtype=int)
    false_alarms = np.zeros_like(hits)

    for p in range(participants):
        if family is RecoveryFamily.EVSD:
            memory_p = memory * np.exp(participant_memory[p])
            bias_p = biases + participant_bias[p]
            hit_prob = np.empty((2, biases.size), dtype=float)
            fa_prob = np.empty_like(hit_prob)
            for j in range(2):
                hit_prob[j] = 0.5 * (
                    1.0
                    + np.vectorize(np.math.erf)(
                        (memory_p[j] / 2.0 - bias_p) / sqrt(2.0)
                    )
                )
                fa_prob[j] = 0.5 * (
                    1.0
                    + np.vectorize(np.math.erf)(
                        (-memory_p[j] / 2.0 - bias_p) / sqrt(2.0)
                    )
                )
        else:
            memory_p = expit(
                np.asarray([_logit(x) for x in memory]) + participant_memory[p]
            )
            bias_p = expit(
                np.asarray([_logit(x) for x in biases]) + participant_bias[p]
            )
            fa_prob = np.tile((1.0 - memory_p)[:, None], (1, biases.size)) * bias_p
            hit_prob = memory_p[:, None] + fa_prob

        hits[p] = rng.binomial(n_target_per_cell, hit_prob)
        false_alarms[p] = rng.binomial(n_foil_per_cell, fa_prob)

    return ParticipantDataset(
        hits=hits,
        false_alarms=false_alarms,
        n_target_per_cell=n_target_per_cell,
        n_foil_per_cell=n_foil_per_cell,
    )


def _aggregate_for_initialization(
    dataset: ParticipantDataset,
) -> dict[str, tuple[RecognitionCounts, ...]]:
    aggregated: dict[str, tuple[RecognitionCounts, ...]] = {}
    total_target = dataset.participants * dataset.n_target_per_cell
    total_foil = dataset.participants * dataset.n_foil_per_cell

    for j, condition in enumerate(CONDITIONS):
        points = []
        for k in range(dataset.operating_points):
            points.append(
                RecognitionCounts(
                    n_target=total_target,
                    n_foil=total_foil,
                    n_hit=int(dataset.hits[:, j, k].sum()),
                    n_fa=int(dataset.false_alarms[:, j, k].sum()),
                )
            )
        aggregated[condition] = tuple(points)
    return aggregated


def _quadrature(nodes: int) -> tuple[np.ndarray, np.ndarray]:
    if nodes < 3:
        raise ValueError("at least three Gauss-Hermite nodes are required")
    x, w = np.polynomial.hermite.hermgauss(nodes)
    return x.astype(float), (np.log(w) - 0.5 * log(pi)).astype(float)


def _marginal_log_likelihood(
    *,
    family: RecoveryFamily,
    dataset: ParticipantDataset,
    population_memory: np.ndarray,
    population_biases: np.ndarray,
    sigma_memory: float,
    sigma_bias: float,
    quadrature_nodes: int,
) -> float:
    nodes, log_weights = _quadrature(quadrature_nodes)
    memory_offsets = sqrt(2.0) * sigma_memory * nodes
    bias_offsets = sqrt(2.0) * sigma_bias * nodes

    total_ll = 0.0
    for p in range(dataset.participants):
        terms: list[float] = []
        for i, u in enumerate(memory_offsets):
            if family is RecoveryFamily.EVSD:
                memory_p = population_memory * np.exp(u)
            else:
                memory_p = expit(
                    np.asarray([_logit(x) for x in population_memory]) + u
                )

            for h, v in enumerate(bias_offsets):
                if family is RecoveryFamily.EVSD:
                    bias_p = population_biases + v
                    z_hit = memory_p[:, None] / 2.0 - bias_p[None, :]
                    z_fa = -memory_p[:, None] / 2.0 - bias_p[None, :]
                    hit_prob = 0.5 * (
                        1.0
                        + np.vectorize(np.math.erf)(z_hit / sqrt(2.0))
                    )
                    fa_prob = 0.5 * (
                        1.0
                        + np.vectorize(np.math.erf)(z_fa / sqrt(2.0))
                    )
                else:
                    bias_p = expit(
                        np.asarray([_logit(x) for x in population_biases]) + v
                    )
                    fa_prob = (1.0 - memory_p)[:, None] * bias_p[None, :]
                    hit_prob = memory_p[:, None] + fa_prob

                conditional = float(
                    _binomial_ll_array(
                        dataset.hits[p],
                        dataset.n_target_per_cell,
                        hit_prob,
                    ).sum()
                    + _binomial_ll_array(
                        dataset.false_alarms[p],
                        dataset.n_foil_per_cell,
                        fa_prob,
                    ).sum()
                )
                terms.append(
                    float(log_weights[i] + log_weights[h] + conditional)
                )
        total_ll += float(logsumexp(np.asarray(terms)))
    return total_ll


def _unpack(
    family: RecoveryFamily,
    x: np.ndarray,
    operating_points: int,
) -> tuple[np.ndarray, np.ndarray, float, float]:
    if family is RecoveryFamily.EVSD:
        memory = np.exp(x[:2])
        biases = x[2 : 2 + operating_points]
    else:
        memory = expit(x[:2])
        biases = expit(x[2 : 2 + operating_points])

    sigma_memory = float(np.exp(x[-2]))
    sigma_bias = float(np.exp(x[-1]))
    return np.asarray(memory), np.asarray(biases), sigma_memory, sigma_bias


def fit_hierarchical_candidate(
    family: RecoveryFamily,
    dataset: ParticipantDataset,
    *,
    quadrature_nodes: int = 5,
) -> HierarchicalFit:
    if family not in (RecoveryFamily.EVSD, RecoveryFamily.TWO_HT):
        raise ValueError("only EVSD and 2HT can be fit")

    pooled = fit_candidate(family, _aggregate_for_initialization(dataset))
    memory0 = np.asarray(
        [pooled.conditions[name].memory for name in CONDITIONS],
        dtype=float,
    )
    biases0 = np.mean(
        np.asarray([pooled.conditions[name].biases for name in CONDITIONS]),
        axis=0,
    )

    if family is RecoveryFamily.EVSD:
        x0 = np.concatenate(
            (
                np.log(np.clip(memory0, 1e-3, 4.0)),
                biases0,
                np.log([0.20, 0.20]),
            )
        )
        bounds = (
            [(-5.0, np.log(4.0))] * 2
            + [(-4.0, 4.0)] * dataset.operating_points
            + [(-5.0, 0.0), (-5.0, 0.0)]
        )
    else:
        x0 = np.concatenate(
            (
                np.asarray([_logit(x) for x in memory0]),
                np.asarray([_logit(x) for x in np.clip(biases0, 1e-4, 1 - 1e-4)]),
                np.log([0.20, 0.20]),
            )
        )
        bounds = (
            [(-6.0, 6.0)] * (2 + dataset.operating_points)
            + [(-5.0, 0.0), (-5.0, 0.0)]
        )

    def objective(x: np.ndarray) -> float:
        memory, biases, sigma_memory, sigma_bias = _unpack(
            family, x, dataset.operating_points
        )
        return -_marginal_log_likelihood(
            family=family,
            dataset=dataset,
            population_memory=memory,
            population_biases=biases,
            sigma_memory=sigma_memory,
            sigma_bias=sigma_bias,
            quadrature_nodes=quadrature_nodes,
        )

    result = minimize(
        objective,
        x0=x0,
        method="L-BFGS-B",
        bounds=bounds,
        options={"maxiter": 250, "ftol": 1e-8},
    )
    if not result.success:
        raise RuntimeError(f"hierarchical {family.value} fit failed: {result.message}")

    memory, biases, sigma_memory, sigma_bias = _unpack(
        family, result.x, dataset.operating_points
    )
    return HierarchicalFit(
        family=family,
        population_memory={
            condition: float(memory[j]) for j, condition in enumerate(CONDITIONS)
        },
        population_biases=tuple(float(x) for x in biases),
        sigma_memory=sigma_memory,
        sigma_bias=sigma_bias,
        log_likelihood=float(-result.fun),
        parameter_count=2 + dataset.operating_points + 2,
    )


def hierarchical_predictive_log_likelihood(
    fit: HierarchicalFit,
    dataset: ParticipantDataset,
    *,
    quadrature_nodes: int = 5,
) -> float:
    memory = np.asarray([fit.population_memory[x] for x in CONDITIONS], dtype=float)
    biases = np.asarray(fit.population_biases, dtype=float)
    return _marginal_log_likelihood(
        family=fit.family,
        dataset=dataset,
        population_memory=memory,
        population_biases=biases,
        sigma_memory=fit.sigma_memory,
        sigma_bias=fit.sigma_bias,
        quadrature_nodes=quadrature_nodes,
    )


def select_hierarchical_candidate(
    *,
    evsd_fit: HierarchicalFit,
    two_ht_fit: HierarchicalFit,
    held_out: ParticipantDataset,
    quadrature_nodes: int = 5,
    tolerance: float = 1e-9,
) -> RecoveryFamily:
    aic_delta = evsd_fit.aic - two_ht_fit.aic
    if abs(aic_delta) <= tolerance:
        return RecoveryFamily.INCONCLUSIVE
    aic_choice = RecoveryFamily.EVSD if aic_delta < 0 else RecoveryFamily.TWO_HT

    evsd_pred = hierarchical_predictive_log_likelihood(
        evsd_fit, held_out, quadrature_nodes=quadrature_nodes
    )
    two_ht_pred = hierarchical_predictive_log_likelihood(
        two_ht_fit, held_out, quadrature_nodes=quadrature_nodes
    )
    pred_delta = evsd_pred - two_ht_pred
    if abs(pred_delta) <= tolerance:
        return RecoveryFamily.INCONCLUSIVE
    pred_choice = RecoveryFamily.EVSD if pred_delta > 0 else RecoveryFamily.TWO_HT

    return aic_choice if aic_choice is pred_choice else RecoveryFamily.INCONCLUSIVE


def run_participant_recovery_benchmark(config: dict) -> dict:
    seed = int(config["seed"])
    replicates = int(config["replicates"])
    threshold = float(config["recovery_threshold"])
    quadrature_nodes = int(config["quadrature_nodes"])

    if replicates <= 0:
        raise ValueError("replicates must be positive")
    if not 0.0 < threshold <= 1.0:
        raise ValueError("recovery threshold must lie in (0,1]")

    rng = np.random.default_rng(seed)
    rows: list[dict] = []
    aggregate = {
        RecoveryFamily.EVSD.value: {x.value: 0 for x in RecoveryFamily},
        RecoveryFamily.TWO_HT.value: {x.value: 0 for x in RecoveryFamily},
    }

    for allocation in config["participant_allocations"]:
        participants = int(allocation["participants"])
        trials = int(allocation["target_trials_per_participant_per_cell"])
        if participants * trials != int(config["aggregate_target_per_cell"]):
            raise ValueError("participant allocation does not preserve aggregate target anchor")
        if participants * int(allocation["foil_trials_per_participant_per_cell"]) != int(
            config["aggregate_foil_per_cell"]
        ):
            raise ValueError("participant allocation does not preserve aggregate foil anchor")

        for heterogeneity in config["heterogeneity_regimes"]:
            sigma_memory = float(heterogeneity["sigma_memory"])
            sigma_bias = float(heterogeneity["sigma_bias"])

            for family in (RecoveryFamily.EVSD, RecoveryFamily.TWO_HT):
                biases = tuple(float(x) for x in config["bias_grids"][family.value])
                for regime in config["memory_grids"][family.value]:
                    truth = {
                        "complex": float(regime["complex"]),
                        "simple": float(regime["simple"]),
                    }
                    selected = {x.value: 0 for x in RecoveryFamily}
                    memory_errors = {"complex": [], "simple": []}
                    sigma_memory_errors: list[float] = []
                    sigma_bias_errors: list[float] = []

                    for _ in range(replicates):
                        train = simulate_participant_dataset(
                            family=family,
                            population_memory=truth,
                            population_biases=biases,
                            participants=participants,
                            n_target_per_cell=trials,
                            n_foil_per_cell=int(
                                allocation["foil_trials_per_participant_per_cell"]
                            ),
                            sigma_memory=sigma_memory,
                            sigma_bias=sigma_bias,
                            rng=rng,
                        )
                        held_out = simulate_participant_dataset(
                            family=family,
                            population_memory=truth,
                            population_biases=biases,
                            participants=participants,
                            n_target_per_cell=trials,
                            n_foil_per_cell=int(
                                allocation["foil_trials_per_participant_per_cell"]
                            ),
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
                        aggregate[family.value][choice.value] += 1

                        true_fit = evsd_fit if family is RecoveryFamily.EVSD else two_ht_fit
                        for condition in CONDITIONS:
                            memory_errors[condition].append(
                                abs(true_fit.population_memory[condition] - truth[condition])
                            )
                        sigma_memory_errors.append(
                            abs(true_fit.sigma_memory - sigma_memory)
                        )
                        sigma_bias_errors.append(abs(true_fit.sigma_bias - sigma_bias))

                    recovery = selected[family.value] / replicates
                    wrong_family = (
                        RecoveryFamily.TWO_HT.value
                        if family is RecoveryFamily.EVSD
                        else RecoveryFamily.EVSD.value
                    )
                    rows.append(
                        {
                            "generator": family.value,
                            "allocation": allocation["label"],
                            "participants": participants,
                            "target_trials_per_participant_per_cell": trials,
                            "foil_trials_per_participant_per_cell": int(
                                allocation["foil_trials_per_participant_per_cell"]
                            ),
                            "total_responses_per_participant": int(
                                allocation["total_responses_per_participant"]
                            ),
                            "heterogeneity": heterogeneity["label"],
                            "sigma_memory": sigma_memory,
                            "sigma_bias": sigma_bias,
                            "regime": regime["label"],
                            "replicates": replicates,
                            "selected": selected,
                            "recovery_probability": recovery,
                            "wrong_probability": selected[wrong_family] / replicates,
                            "inconclusive_probability": selected[
                                RecoveryFamily.INCONCLUSIVE.value
                            ]
                            / replicates,
                            "memory_parameter_mae": {
                                key: float(np.mean(values))
                                for key, values in memory_errors.items()
                            },
                            "sigma_memory_mae": float(np.mean(sigma_memory_errors)),
                            "sigma_bias_mae": float(np.mean(sigma_bias_errors)),
                            "passes_recovery_threshold": recovery >= threshold,
                        }
                    )

    confusion_probability: dict[str, dict[str, float]] = {}
    for generator, counts in aggregate.items():
        total = sum(counts.values())
        confusion_probability[generator] = {
            selected: count / total if total else 0.0
            for selected, count in counts.items()
        }

    return {
        "benchmark_id": config["benchmark_id"],
        "seed": seed,
        "replicates_per_grid_cell": replicates,
        "quadrature_nodes": quadrature_nodes,
        "aggregate_target_per_cell": config["aggregate_target_per_cell"],
        "aggregate_foil_per_cell": config["aggregate_foil_per_cell"],
        "selection_rule": "HIERARCHICAL_AIC_AND_NEW_COHORT_PREDICTIVE_LL_MUST_AGREE",
        "confusion_counts": aggregate,
        "confusion_probability": confusion_probability,
        "grid_results": rows,
        "minimum_grid_recovery_probability": min(
            row["recovery_probability"] for row in rows
        ),
        "all_grid_cells_pass": all(row["passes_recovery_threshold"] for row in rows),
        "interpretation_boundary": (
            "Participant-aware synthetic design diagnostic only. Random effects model "
            "participant memory ability and response-bias heterogeneity shared across "
            "repeated blocks. Item heterogeneity, fatigue, carryover and empirical "
            "model truth remain outside this benchmark."
        ),
    }
