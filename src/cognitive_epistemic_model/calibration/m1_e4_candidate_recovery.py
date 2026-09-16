from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from math import isclose
from typing import Iterable

import numpy as np
from scipy.optimize import minimize
from scipy.special import gammaln, ndtr, ndtri, xlog1py, xlogy


class RecoveryFamily(str, Enum):
    EVSD = "EVSD"
    TWO_HT = "2HT"
    INCONCLUSIVE = "INCONCLUSIVE"


@dataclass(frozen=True)
class RecognitionCounts:
    n_target: int
    n_foil: int
    n_hit: int
    n_fa: int

    def __post_init__(self) -> None:
        if self.n_target <= 0 or self.n_foil <= 0:
            raise ValueError("target and foil totals must be positive")
        if not 0 <= self.n_hit <= self.n_target:
            raise ValueError("n_hit must lie in [0, n_target]")
        if not 0 <= self.n_fa <= self.n_foil:
            raise ValueError("n_fa must lie in [0, n_foil]")

    @property
    def n_miss(self) -> int:
        return self.n_target - self.n_hit

    @property
    def n_cr(self) -> int:
        return self.n_foil - self.n_fa


@dataclass(frozen=True)
class ConditionFit:
    memory: float
    biases: tuple[float, ...]
    log_likelihood: float


@dataclass(frozen=True)
class CandidateFit:
    family: RecoveryFamily
    conditions: dict[str, ConditionFit]
    log_likelihood: float
    parameter_count: int

    @property
    def aic(self) -> float:
        return 2.0 * self.parameter_count - 2.0 * self.log_likelihood


def evsd_probabilities(d: float, criterion: float) -> tuple[float, float]:
    if d < 0:
        raise ValueError("EVSD d must be non-negative")
    hit = float(ndtr(d / 2.0 - criterion))
    false_alarm = float(ndtr(-d / 2.0 - criterion))
    return hit, false_alarm


def two_ht_probabilities(ddet: float, guess_seen: float) -> tuple[float, float]:
    if not 0.0 <= ddet <= 1.0:
        raise ValueError("2HT Ddet must be in [0, 1]")
    if not 0.0 <= guess_seen <= 1.0:
        raise ValueError("2HT g must be in [0, 1]")
    false_alarm = (1.0 - ddet) * guess_seen
    hit = ddet + false_alarm
    return hit, false_alarm


def _binomial_log_likelihood(successes: int, total: int, probability: float) -> float:
    eps = np.finfo(float).eps
    p = float(np.clip(probability, eps, 1.0 - eps))
    log_choose = gammaln(total + 1) - gammaln(successes + 1) - gammaln(total - successes + 1)
    return float(
        log_choose
        + xlogy(successes, p)
        + xlog1py(total - successes, -p)
    )


def _point_log_likelihood(counts: RecognitionCounts, hit: float, false_alarm: float) -> float:
    return (
        _binomial_log_likelihood(counts.n_hit, counts.n_target, hit)
        + _binomial_log_likelihood(counts.n_fa, counts.n_foil, false_alarm)
    )


def simulate_condition(
    *,
    family: RecoveryFamily,
    memory: float,
    biases: Iterable[float],
    n_target: int,
    n_foil: int,
    rng: np.random.Generator,
) -> tuple[RecognitionCounts, ...]:
    points: list[RecognitionCounts] = []
    for bias in biases:
        if family is RecoveryFamily.EVSD:
            hit, false_alarm = evsd_probabilities(memory, float(bias))
        elif family is RecoveryFamily.TWO_HT:
            hit, false_alarm = two_ht_probabilities(memory, float(bias))
        else:
            raise ValueError("only EVSD and 2HT can generate recognition data")
        points.append(
            RecognitionCounts(
                n_target=n_target,
                n_foil=n_foil,
                n_hit=int(rng.binomial(n_target, hit)),
                n_fa=int(rng.binomial(n_foil, false_alarm)),
            )
        )
    return tuple(points)


def simulate_dataset(
    *,
    family: RecoveryFamily,
    memory_by_condition: dict[str, float],
    biases: tuple[float, ...],
    n_target: int,
    n_foil: int,
    rng: np.random.Generator,
) -> dict[str, tuple[RecognitionCounts, ...]]:
    return {
        condition: simulate_condition(
            family=family,
            memory=memory,
            biases=biases,
            n_target=n_target,
            n_foil=n_foil,
            rng=rng,
        )
        for condition, memory in memory_by_condition.items()
    }


def _corrected_rates(points: tuple[RecognitionCounts, ...]) -> tuple[np.ndarray, np.ndarray]:
    hit = np.asarray([(p.n_hit + 0.5) / (p.n_target + 1.0) for p in points])
    fa = np.asarray([(p.n_fa + 0.5) / (p.n_foil + 1.0) for p in points])
    return hit, fa


def fit_evsd_condition(points: tuple[RecognitionCounts, ...]) -> ConditionFit:
    hit, fa = _corrected_rates(points)
    z_hit = ndtri(hit)
    z_fa = ndtri(fa)
    d0 = float(np.clip(np.median(z_hit - z_fa), 0.05, 3.5))
    c0 = np.clip(-0.5 * (z_hit + z_fa), -3.0, 3.0)
    x0 = np.concatenate(([d0], c0))

    def objective(x: np.ndarray) -> float:
        d = float(x[0])
        total = 0.0
        for criterion, counts in zip(x[1:], points, strict=True):
            h, f = evsd_probabilities(d, float(criterion))
            total += _point_log_likelihood(counts, h, f)
        return -total

    result = minimize(
        objective,
        x0=x0,
        method="L-BFGS-B",
        bounds=[(1e-6, 4.0)] + [(-4.0, 4.0)] * len(points),
    )
    if not result.success:
        raise RuntimeError(f"EVSD fit failed: {result.message}")
    return ConditionFit(
        memory=float(result.x[0]),
        biases=tuple(float(x) for x in result.x[1:]),
        log_likelihood=float(-result.fun),
    )


def fit_two_ht_condition(points: tuple[RecognitionCounts, ...]) -> ConditionFit:
    hit, fa = _corrected_rates(points)
    ddet0 = float(np.clip(np.median(hit - fa), 0.02, 0.95))
    g0 = np.clip(fa / max(1.0 - ddet0, 1e-6), 0.02, 0.98)
    x0 = np.concatenate(([ddet0], g0))

    def objective(x: np.ndarray) -> float:
        ddet = float(x[0])
        total = 0.0
        for guess, counts in zip(x[1:], points, strict=True):
            h, f = two_ht_probabilities(ddet, float(guess))
            total += _point_log_likelihood(counts, h, f)
        return -total

    bounds = [(1e-6, 1.0 - 1e-6)] + [(1e-6, 1.0 - 1e-6)] * len(points)
    result = minimize(
        objective,
        x0=x0,
        method="L-BFGS-B",
        bounds=bounds,
    )
    if not result.success:
        # SciPy's default L-BFGS-B line-search budget can terminate abnormally
        # for an otherwise stable optimum on some pooled-count surfaces.
        # Retry from the identical starting point with only the line-search
        # budget increased. The objective, bounds, data, and parameterization
        # remain unchanged.
        result = minimize(
            objective,
            x0=x0,
            method="L-BFGS-B",
            bounds=bounds,
            options={"maxls": 100},
        )
    if not result.success:
        raise RuntimeError(f"2HT fit failed after bounded retry: {result.message}")
    return ConditionFit(
        memory=float(result.x[0]),
        biases=tuple(float(x) for x in result.x[1:]),
        log_likelihood=float(-result.fun),
    )


def fit_candidate(
    family: RecoveryFamily,
    dataset: dict[str, tuple[RecognitionCounts, ...]],
) -> CandidateFit:
    if family not in (RecoveryFamily.EVSD, RecoveryFamily.TWO_HT):
        raise ValueError("only EVSD and 2HT can be fit")
    fit_fn = fit_evsd_condition if family is RecoveryFamily.EVSD else fit_two_ht_condition
    conditions = {name: fit_fn(points) for name, points in dataset.items()}
    log_likelihood = sum(fit.log_likelihood for fit in conditions.values())
    parameter_count = sum(1 + len(fit.biases) for fit in conditions.values())
    return CandidateFit(
        family=family,
        conditions=conditions,
        log_likelihood=log_likelihood,
        parameter_count=parameter_count,
    )


def predictive_log_likelihood(
    fit: CandidateFit,
    dataset: dict[str, tuple[RecognitionCounts, ...]],
) -> float:
    total = 0.0
    for condition, points in dataset.items():
        params = fit.conditions[condition]
        if len(points) != len(params.biases):
            raise ValueError("held-out operating points must match fitted bias settings")
        for bias, counts in zip(params.biases, points, strict=True):
            if fit.family is RecoveryFamily.EVSD:
                h, f = evsd_probabilities(params.memory, bias)
            else:
                h, f = two_ht_probabilities(params.memory, bias)
            total += _point_log_likelihood(counts, h, f)
    return total


def select_candidate(
    *,
    evsd_fit: CandidateFit,
    two_ht_fit: CandidateFit,
    held_out: dict[str, tuple[RecognitionCounts, ...]],
    tolerance: float = 1e-9,
) -> RecoveryFamily:
    aic_delta = evsd_fit.aic - two_ht_fit.aic
    if abs(aic_delta) <= tolerance:
        return RecoveryFamily.INCONCLUSIVE
    aic_choice = RecoveryFamily.EVSD if aic_delta < 0 else RecoveryFamily.TWO_HT

    evsd_pred = predictive_log_likelihood(evsd_fit, held_out)
    two_ht_pred = predictive_log_likelihood(two_ht_fit, held_out)
    pred_delta = evsd_pred - two_ht_pred
    if abs(pred_delta) <= tolerance:
        return RecoveryFamily.INCONCLUSIVE
    pred_choice = RecoveryFamily.EVSD if pred_delta > 0 else RecoveryFamily.TWO_HT

    return aic_choice if aic_choice is pred_choice else RecoveryFamily.INCONCLUSIVE


def _bias_rmse(estimated: tuple[float, ...], truth: tuple[float, ...]) -> float:
    if len(estimated) != len(truth):
        raise ValueError("estimated and true bias grids must align")
    return float(np.sqrt(np.mean((np.asarray(estimated) - np.asarray(truth)) ** 2)))


def run_recovery_benchmark(config: dict) -> dict:
    seed = int(config["seed"])
    replicates = int(config["replicates"])
    threshold = float(config["recovery_threshold"])
    if replicates <= 0:
        raise ValueError("replicates must be positive")
    if not 0.0 < threshold <= 1.0:
        raise ValueError("recovery_threshold must be in (0, 1]")

    rng = np.random.default_rng(seed)
    evsd_biases = tuple(float(x) for x in config["bias_grids"]["EVSD"])
    two_ht_biases = tuple(float(x) for x in config["bias_grids"]["2HT"])
    if len(evsd_biases) < 3 or len(two_ht_biases) < 3:
        raise ValueError("benchmark requires at least three bias settings per generator")

    rows: list[dict] = []
    aggregate = {
        RecoveryFamily.EVSD.value: {x.value: 0 for x in RecoveryFamily},
        RecoveryFamily.TWO_HT.value: {x.value: 0 for x in RecoveryFamily},
    }

    for n_trials in config["trial_counts_per_operating_point"]:
        n_target = int(n_trials)
        n_foil = int(n_trials)
        for family in (RecoveryFamily.EVSD, RecoveryFamily.TWO_HT):
            family_grid = config["memory_grids"][family.value]
            true_biases = evsd_biases if family is RecoveryFamily.EVSD else two_ht_biases

            for regime in family_grid:
                memory_truth = {
                    "complex": float(regime["complex"]),
                    "simple": float(regime["simple"]),
                }
                selected = {x.value: 0 for x in RecoveryFamily}
                memory_errors = {"complex": [], "simple": []}
                bias_errors: list[float] = []

                for _ in range(replicates):
                    train = simulate_dataset(
                        family=family,
                        memory_by_condition=memory_truth,
                        biases=true_biases,
                        n_target=n_target,
                        n_foil=n_foil,
                        rng=rng,
                    )
                    held_out = simulate_dataset(
                        family=family,
                        memory_by_condition=memory_truth,
                        biases=true_biases,
                        n_target=n_target,
                        n_foil=n_foil,
                        rng=rng,
                    )

                    evsd_fit = fit_candidate(RecoveryFamily.EVSD, train)
                    two_ht_fit = fit_candidate(RecoveryFamily.TWO_HT, train)
                    choice = select_candidate(
                        evsd_fit=evsd_fit,
                        two_ht_fit=two_ht_fit,
                        held_out=held_out,
                    )
                    selected[choice.value] += 1
                    aggregate[family.value][choice.value] += 1

                    true_fit = evsd_fit if family is RecoveryFamily.EVSD else two_ht_fit
                    for condition, truth in memory_truth.items():
                        memory_errors[condition].append(
                            abs(true_fit.conditions[condition].memory - truth)
                        )
                        bias_errors.append(
                            _bias_rmse(true_fit.conditions[condition].biases, true_biases)
                        )

                correct = selected[family.value]
                recovery_probability = correct / replicates
                rows.append(
                    {
                        "generator": family.value,
                        "regime": str(regime["label"]),
                        "n_target_per_operating_point": n_target,
                        "n_foil_per_operating_point": n_foil,
                        "operating_points": len(true_biases),
                        "replicates": replicates,
                        "selected": selected,
                        "recovery_probability": recovery_probability,
                        "wrong_probability": selected[
                            RecoveryFamily.TWO_HT.value
                            if family is RecoveryFamily.EVSD
                            else RecoveryFamily.EVSD.value
                        ]
                        / replicates,
                        "inconclusive_probability": selected[RecoveryFamily.INCONCLUSIVE.value]
                        / replicates,
                        "memory_parameter_mae": {
                            key: float(np.mean(values))
                            for key, values in memory_errors.items()
                        },
                        "bias_parameter_rmse": float(np.mean(bias_errors)),
                        "passes_recovery_threshold": recovery_probability >= threshold,
                    }
                )

    confusion_probability: dict[str, dict[str, float]] = {}
    for generator, counts in aggregate.items():
        total = sum(counts.values())
        confusion_probability[generator] = {
            selected: (count / total if total else 0.0)
            for selected, count in counts.items()
        }

    return {
        "benchmark_id": config["benchmark_id"],
        "seed": seed,
        "replicates_per_grid_cell": replicates,
        "recovery_threshold": threshold,
        "selection_rule": "AIC_AND_HELD_OUT_LOG_LIKELIHOOD_MUST_AGREE",
        "confusion_counts": aggregate,
        "confusion_probability": confusion_probability,
        "grid_results": rows,
        "minimum_grid_recovery_probability": min(
            row["recovery_probability"] for row in rows
        ),
        "all_core_grid_cells_pass": all(
            row["passes_recovery_threshold"] for row in rows
        ),
        "interpretation_boundary": (
            "Synthetic design diagnostic only. Passing recovery does not establish "
            "that EVSD or 2HT is the true recognition architecture, and model-family "
            "selection does not identify Pencode."
        ),
    }
