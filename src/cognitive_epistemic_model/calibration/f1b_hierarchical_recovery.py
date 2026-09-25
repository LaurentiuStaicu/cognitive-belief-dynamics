from __future__ import annotations

from dataclasses import dataclass
from math import log, pi

import numpy as np
from scipy.optimize import minimize
from scipy.sparse import csr_matrix, diags, hstack
from scipy.sparse.linalg import spsolve
from scipy.special import expit, xlog1py, xlogy

from .f1b_prehuman_recovery import (
    R1Dataset,
    R1Family,
    R2Dataset,
    R2Family,
    Split,
    fit_r2_candidate,
    source_weight,
)


@dataclass(frozen=True)
class RandomEffectScales:
    participant_intercept_sd: float
    item_intercept_sd: float
    participant_slope_sd: float
    item_slope_sd: float

    def __post_init__(self) -> None:
        for value in (
            self.participant_intercept_sd,
            self.item_intercept_sd,
            self.participant_slope_sd,
            self.item_slope_sd,
        ):
            if value <= 0.0:
                raise ValueError("hierarchical penalty scales must be positive")


@dataclass(frozen=True)
class R1HierarchicalFit:
    family: R1Family
    intercept: float
    slope: float
    residual_sd: float
    participant_intercepts: np.ndarray
    item_intercepts: np.ndarray
    participant_slopes: np.ndarray
    item_slopes: np.ndarray
    tau: float | None
    log_likelihood: float
    parameter_count: int
    penalized_objective: float

    @property
    def aic(self) -> float:
        return 2.0 * self.parameter_count - 2.0 * self.log_likelihood


@dataclass(frozen=True)
class R2HierarchicalFit:
    family: R2Family
    fixed_parameters: tuple[float, ...]
    participant_intercepts: np.ndarray
    item_intercepts: np.ndarray
    participant_reward_slopes: np.ndarray
    item_reward_slopes: np.ndarray
    log_likelihood: float
    parameter_count: int
    penalized_objective: float
    converged: bool

    @property
    def aic(self) -> float:
        return 2.0 * self.parameter_count - 2.0 * self.log_likelihood


def _group_counts(
    participant: np.ndarray,
    item: np.ndarray,
) -> tuple[int, int]:
    return int(np.max(participant)) + 1, int(np.max(item)) + 1


def _r1_design(
    x: np.ndarray,
    participant: np.ndarray,
    item: np.ndarray,
    *,
    participant_count: int,
    item_count: int,
) -> csr_matrix:
    n = x.size
    rows = np.arange(n, dtype=int)
    p_int = csr_matrix(
        (np.ones(n), (rows, participant)),
        shape=(n, participant_count),
    )
    i_int = csr_matrix(
        (np.ones(n), (rows, item)),
        shape=(n, item_count),
    )
    p_slope = csr_matrix(
        (x, (rows, participant)),
        shape=(n, participant_count),
    )
    i_slope = csr_matrix(
        (x, (rows, item)),
        shape=(n, item_count),
    )
    fixed = csr_matrix(np.column_stack((np.ones(n), x)))
    return hstack((fixed, p_int, i_int, p_slope, i_slope), format="csr")


def _r1_unpack(
    beta: np.ndarray,
    *,
    participant_count: int,
    item_count: int,
) -> tuple[float, float, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    offset = 0
    intercept = float(beta[offset])
    slope = float(beta[offset + 1])
    offset += 2
    p_int = np.asarray(beta[offset : offset + participant_count], dtype=float)
    offset += participant_count
    i_int = np.asarray(beta[offset : offset + item_count], dtype=float)
    offset += item_count
    p_slope = np.asarray(beta[offset : offset + participant_count], dtype=float)
    offset += participant_count
    i_slope = np.asarray(beta[offset : offset + item_count], dtype=float)
    return intercept, slope, p_int, i_int, p_slope, i_slope


def _r1_fit_for_tau(
    *,
    family: R1Family,
    dataset: R1Dataset,
    mask: np.ndarray,
    residual_sd: float,
    scales: RandomEffectScales,
    tau: float | None,
    extra_parameters: int,
) -> R1HierarchicalFit:
    if residual_sd <= 0.0:
        raise ValueError("residual_sd must be positive")
    participant_count, item_count = _group_counts(
        dataset.participant,
        dataset.item,
    )
    reliability = dataset.reliability[mask]
    evidence = dataset.evidence[mask]
    x = evidence * source_weight(family, reliability, tau=tau)
    y = dataset.y[mask]
    participant = dataset.participant[mask]
    item = dataset.item[mask]
    design = _r1_design(
        x,
        participant,
        item,
        participant_count=participant_count,
        item_count=item_count,
    )

    lambdas = np.concatenate(
        (
            np.zeros(2),
            np.full(
                participant_count,
                (residual_sd / scales.participant_intercept_sd) ** 2,
            ),
            np.full(
                item_count,
                (residual_sd / scales.item_intercept_sd) ** 2,
            ),
            np.full(
                participant_count,
                (residual_sd / scales.participant_slope_sd) ** 2,
            ),
            np.full(
                item_count,
                (residual_sd / scales.item_slope_sd) ** 2,
            ),
        )
    )
    normal = design.T @ design + diags(lambdas, format="csr")
    rhs = design.T @ y
    beta = np.asarray(spsolve(normal.tocsc(), rhs), dtype=float)
    prediction = np.asarray(design @ beta, dtype=float)
    residual = y - prediction
    sigma2 = residual_sd**2
    log_likelihood = float(
        -0.5
        * np.sum(
            np.log(2.0 * pi * sigma2)
            + residual**2 / sigma2
        )
    )
    penalty = float(np.sum(lambdas * beta**2))
    objective = float(np.sum(residual**2) + penalty)

    (
        intercept,
        slope,
        p_int,
        i_int,
        p_slope,
        i_slope,
    ) = _r1_unpack(
        beta,
        participant_count=participant_count,
        item_count=item_count,
    )
    train_participants = set(int(x) for x in np.unique(participant))
    train_items = set(int(x) for x in np.unique(item))
    for index in range(participant_count):
        if index not in train_participants:
            p_int[index] = 0.0
            p_slope[index] = 0.0
    for index in range(item_count):
        if index not in train_items:
            i_int[index] = 0.0
            i_slope[index] = 0.0

    train_p = len(train_participants)
    train_i = len(train_items)
    parameter_count = (
        2
        + 2 * train_p
        + 2 * train_i
        + int(extra_parameters)
    )
    return R1HierarchicalFit(
        family=family,
        intercept=intercept,
        slope=slope,
        residual_sd=float(residual_sd),
        participant_intercepts=p_int,
        item_intercepts=i_int,
        participant_slopes=p_slope,
        item_slopes=i_slope,
        tau=tau,
        log_likelihood=log_likelihood,
        parameter_count=parameter_count,
        penalized_objective=objective,
    )


def fit_r1_hierarchical_candidate(
    family: R1Family,
    dataset: R1Dataset,
    mask: np.ndarray,
    *,
    residual_sd: float,
    scales: RandomEffectScales,
    tau_grid: tuple[float, ...],
) -> R1HierarchicalFit:
    if family is R1Family.INCONCLUSIVE:
        raise ValueError("INCONCLUSIVE cannot be fit")
    if family is not R1Family.SR_C:
        return _r1_fit_for_tau(
            family=family,
            dataset=dataset,
            mask=mask,
            residual_sd=residual_sd,
            scales=scales,
            tau=None,
            extra_parameters=0,
        )

    fits = [
        _r1_fit_for_tau(
            family=family,
            dataset=dataset,
            mask=mask,
            residual_sd=residual_sd,
            scales=scales,
            tau=float(tau),
            extra_parameters=1,
        )
        for tau in tau_grid
    ]
    if not fits:
        raise ValueError("SR-C tau grid must be non-empty")
    return min(fits, key=lambda fit: fit.aic)


def r1_hierarchical_predictive_log_likelihood(
    fit: R1HierarchicalFit,
    dataset: R1Dataset,
    mask: np.ndarray,
) -> float:
    reliability = dataset.reliability[mask]
    evidence = dataset.evidence[mask]
    x = evidence * source_weight(
        fit.family,
        reliability,
        tau=fit.tau,
    )
    p = dataset.participant[mask]
    i = dataset.item[mask]
    mean = (
        fit.intercept
        + fit.slope * x
        + fit.participant_intercepts[p]
        + fit.item_intercepts[i]
        + fit.participant_slopes[p] * x
        + fit.item_slopes[i] * x
    )
    residual = dataset.y[mask] - mean
    sigma2 = fit.residual_sd**2
    return float(
        -0.5
        * np.sum(
            np.log(2.0 * pi * sigma2)
            + residual**2 / sigma2
        )
    )


def _r2_fixed_eta_and_jacobian(
    family: R2Family,
    fixed: np.ndarray,
    belief: np.ndarray,
    accuracy: np.ndarray,
    reward: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    centered = 2.0 * belief - 1.0
    if family is R2Family.AP_A:
        bias, baseline_logit, beta_accuracy, beta_reward = fixed
        w = expit(baseline_logit + beta_accuracy * accuracy)
        eta = bias + w * centered + beta_reward * (1.0 - w) * reward
        shared = w * (1.0 - w) * (centered - beta_reward * reward)
        jac = np.column_stack(
            (
                np.ones(belief.size),
                shared,
                accuracy * shared,
                (1.0 - w) * reward,
            )
        )
        return eta, jac
    if family is R2Family.AP_B:
        eta = (
            fixed[0]
            + fixed[1] * centered
            + fixed[2] * accuracy
            + fixed[3] * reward
        )
        jac = np.column_stack(
            (
                np.ones(belief.size),
                centered,
                accuracy,
                reward,
            )
        )
        return eta, jac
    if family is R2Family.AP_C:
        eta = (
            fixed[0]
            + fixed[1] * centered
            + fixed[2] * accuracy
            + fixed[3] * reward
            + fixed[4] * accuracy * centered
            + fixed[5] * accuracy * reward
        )
        jac = np.column_stack(
            (
                np.ones(belief.size),
                centered,
                accuracy,
                reward,
                accuracy * centered,
                accuracy * reward,
            )
        )
        return eta, jac
    raise ValueError("INCONCLUSIVE cannot define R2 utility")


def _r2_fixed_bounds(family: R2Family) -> list[tuple[float, float]]:
    if family is R2Family.AP_A:
        return [
            (-5.0, 5.0),
            (-4.0, 4.0),
            (-5.0, 5.0),
            (-5.0, 5.0),
        ]
    if family is R2Family.AP_B:
        return [(-5.0, 5.0)] * 4
    if family is R2Family.AP_C:
        return [(-5.0, 5.0)] * 6
    raise ValueError("INCONCLUSIVE cannot define fixed bounds")


def _bernoulli_log_likelihood(
    y: np.ndarray,
    eta: np.ndarray,
) -> float:
    probability = np.clip(
        expit(eta),
        np.finfo(float).eps,
        1.0 - np.finfo(float).eps,
    )
    return float(
        np.sum(
            xlogy(y, probability)
            + xlog1py(1 - y, -probability)
        )
    )


def fit_r2_hierarchical_candidate(
    family: R2Family,
    dataset: R2Dataset,
    mask: np.ndarray,
    *,
    scales: RandomEffectScales,
) -> R2HierarchicalFit:
    if family is R2Family.INCONCLUSIVE:
        raise ValueError("INCONCLUSIVE cannot be fit")

    participant_count, item_count = _group_counts(
        dataset.participant,
        dataset.item,
    )
    participant = dataset.participant[mask]
    item = dataset.item[mask]
    belief = dataset.belief[mask]
    accuracy = dataset.accuracy_cue[mask]
    reward = dataset.reward_context[mask]
    y = dataset.share[mask].astype(float)

    population = fit_r2_candidate(family, dataset, mask)
    fixed0 = np.asarray(population.parameters, dtype=float)
    fixed_count = fixed0.size
    random_count = 2 * participant_count + 2 * item_count
    x0 = np.concatenate((fixed0, np.zeros(random_count)))

    p_int_start = fixed_count
    i_int_start = p_int_start + participant_count
    p_slope_start = i_int_start + item_count
    i_slope_start = p_slope_start + participant_count

    inv_var = (
        1.0 / scales.participant_intercept_sd**2,
        1.0 / scales.item_intercept_sd**2,
        1.0 / scales.participant_slope_sd**2,
        1.0 / scales.item_slope_sd**2,
    )

    def unpack(
        vector: np.ndarray,
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        fixed = vector[:fixed_count]
        p_int = vector[p_int_start:i_int_start]
        i_int = vector[i_int_start:p_slope_start]
        p_slope = vector[p_slope_start:i_slope_start]
        i_slope = vector[i_slope_start:]
        return fixed, p_int, i_int, p_slope, i_slope

    def objective_and_gradient(
        vector: np.ndarray,
    ) -> tuple[float, np.ndarray]:
        fixed, p_int, i_int, p_slope, i_slope = unpack(vector)
        fixed_eta, fixed_jac = _r2_fixed_eta_and_jacobian(
            family,
            fixed,
            belief,
            accuracy,
            reward,
        )
        eta = (
            fixed_eta
            + p_int[participant]
            + i_int[item]
            + p_slope[participant] * reward
            + i_slope[item] * reward
        )
        probability = expit(eta)
        residual = probability - y
        nll = -_bernoulli_log_likelihood(y, eta)
        penalty = 0.5 * (
            inv_var[0] * float(np.sum(p_int**2))
            + inv_var[1] * float(np.sum(i_int**2))
            + inv_var[2] * float(np.sum(p_slope**2))
            + inv_var[3] * float(np.sum(i_slope**2))
        )
        grad_fixed = fixed_jac.T @ residual
        grad_p_int = (
            np.bincount(
                participant,
                weights=residual,
                minlength=participant_count,
            )
            + inv_var[0] * p_int
        )
        grad_i_int = (
            np.bincount(
                item,
                weights=residual,
                minlength=item_count,
            )
            + inv_var[1] * i_int
        )
        reward_residual = residual * reward
        grad_p_slope = (
            np.bincount(
                participant,
                weights=reward_residual,
                minlength=participant_count,
            )
            + inv_var[2] * p_slope
        )
        grad_i_slope = (
            np.bincount(
                item,
                weights=reward_residual,
                minlength=item_count,
            )
            + inv_var[3] * i_slope
        )
        gradient = np.concatenate(
            (
                grad_fixed,
                grad_p_int,
                grad_i_int,
                grad_p_slope,
                grad_i_slope,
            )
        )
        return float(nll + penalty), gradient

    bounds = _r2_fixed_bounds(family) + [(None, None)] * random_count
    result = minimize(
        objective_and_gradient,
        x0=x0,
        method="L-BFGS-B",
        jac=True,
        bounds=bounds,
        options={"maxiter": 400, "ftol": 1e-10, "maxls": 50},
    )
    if not result.success:
        result = minimize(
            objective_and_gradient,
            x0=x0,
            method="L-BFGS-B",
            jac=True,
            bounds=bounds,
            options={"maxiter": 800, "ftol": 1e-9, "maxls": 100},
        )
    if not result.success:
        raise RuntimeError(
            f"hierarchical {family.value} fit failed: {result.message}"
        )

    fixed, p_int, i_int, p_slope, i_slope = unpack(result.x)
    train_participants = set(int(x) for x in np.unique(participant))
    train_items = set(int(x) for x in np.unique(item))
    p_int = np.asarray(p_int, dtype=float).copy()
    i_int = np.asarray(i_int, dtype=float).copy()
    p_slope = np.asarray(p_slope, dtype=float).copy()
    i_slope = np.asarray(i_slope, dtype=float).copy()

    for index in range(participant_count):
        if index not in train_participants:
            p_int[index] = 0.0
            p_slope[index] = 0.0
    for index in range(item_count):
        if index not in train_items:
            i_int[index] = 0.0
            i_slope[index] = 0.0

    fixed_eta, _ = _r2_fixed_eta_and_jacobian(
        family,
        fixed,
        belief,
        accuracy,
        reward,
    )
    eta = (
        fixed_eta
        + p_int[participant]
        + i_int[item]
        + p_slope[participant] * reward
        + i_slope[item] * reward
    )
    log_likelihood = _bernoulli_log_likelihood(y, eta)
    train_p = len(train_participants)
    train_i = len(train_items)
    parameter_count = fixed_count + 2 * train_p + 2 * train_i

    return R2HierarchicalFit(
        family=family,
        fixed_parameters=tuple(float(x) for x in fixed),
        participant_intercepts=p_int,
        item_intercepts=i_int,
        participant_reward_slopes=p_slope,
        item_reward_slopes=i_slope,
        log_likelihood=log_likelihood,
        parameter_count=parameter_count,
        penalized_objective=float(result.fun),
        converged=True,
    )


def r2_hierarchical_predictive_log_likelihood(
    fit: R2HierarchicalFit,
    dataset: R2Dataset,
    mask: np.ndarray,
) -> float:
    participant = dataset.participant[mask]
    item = dataset.item[mask]
    belief = dataset.belief[mask]
    accuracy = dataset.accuracy_cue[mask]
    reward = dataset.reward_context[mask]
    fixed_eta, _ = _r2_fixed_eta_and_jacobian(
        fit.family,
        np.asarray(fit.fixed_parameters, dtype=float),
        belief,
        accuracy,
        reward,
    )
    eta = (
        fixed_eta
        + fit.participant_intercepts[participant]
        + fit.item_intercepts[item]
        + fit.participant_reward_slopes[participant] * reward
        + fit.item_reward_slopes[item] * reward
    )
    return _bernoulli_log_likelihood(
        dataset.share[mask].astype(float),
        eta,
    )


def _unique_choice(
    scores: dict[str, float],
    *,
    maximize: bool,
    tolerance: float,
) -> str | None:
    ordered = sorted(
        scores.items(),
        key=lambda item: item[1],
        reverse=maximize,
    )
    if len(ordered) < 2:
        return ordered[0][0] if ordered else None
    if abs(ordered[0][1] - ordered[1][1]) <= tolerance:
        return None
    return ordered[0][0]


def select_r1_hierarchical_candidate(
    fits: dict[R1Family, R1HierarchicalFit],
    dataset: R1Dataset,
    split: Split,
    *,
    tolerance: float = 1e-8,
) -> R1Family:
    aic = {family.value: fit.aic for family, fit in fits.items()}
    held_p = {
        family.value: r1_hierarchical_predictive_log_likelihood(
            fit,
            dataset,
            split.held_out_participant,
        )
        for family, fit in fits.items()
    }
    held_i = {
        family.value: r1_hierarchical_predictive_log_likelihood(
            fit,
            dataset,
            split.held_out_item,
        )
        for family, fit in fits.items()
    }
    choices = (
        _unique_choice(aic, maximize=False, tolerance=tolerance),
        _unique_choice(held_p, maximize=True, tolerance=tolerance),
        _unique_choice(held_i, maximize=True, tolerance=tolerance),
    )
    if None in choices or len(set(choices)) != 1:
        return R1Family.INCONCLUSIVE
    return R1Family(choices[0])


def select_r2_hierarchical_candidate(
    fits: dict[R2Family, R2HierarchicalFit],
    dataset: R2Dataset,
    split: Split,
    *,
    tolerance: float = 1e-8,
) -> R2Family:
    aic = {family.value: fit.aic for family, fit in fits.items()}
    held_p = {
        family.value: r2_hierarchical_predictive_log_likelihood(
            fit,
            dataset,
            split.held_out_participant,
        )
        for family, fit in fits.items()
    }
    held_i = {
        family.value: r2_hierarchical_predictive_log_likelihood(
            fit,
            dataset,
            split.held_out_item,
        )
        for family, fit in fits.items()
    }
    choices = (
        _unique_choice(aic, maximize=False, tolerance=tolerance),
        _unique_choice(held_p, maximize=True, tolerance=tolerance),
        _unique_choice(held_i, maximize=True, tolerance=tolerance),
    )
    if None in choices or len(set(choices)) != 1:
        return R2Family.INCONCLUSIVE
    return R2Family(choices[0])
