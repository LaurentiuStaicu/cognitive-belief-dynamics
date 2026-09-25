from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from math import log, pi

import numpy as np
from scipy.optimize import minimize
from scipy.special import expit, xlog1py, xlogy


class R1Family(str, Enum):
    SR_A = "SR-A"
    SR_B = "SR-B"
    SR_C = "SR-C"
    INCONCLUSIVE = "INCONCLUSIVE"


class R2Family(str, Enum):
    AP_A = "AP-A"
    AP_B = "AP-B"
    AP_C = "AP-C"
    INCONCLUSIVE = "INCONCLUSIVE"


@dataclass(frozen=True)
class R1Dataset:
    y: np.ndarray
    reliability: np.ndarray
    evidence: np.ndarray
    participant: np.ndarray
    item: np.ndarray

    def __post_init__(self) -> None:
        n = self.y.size
        if n == 0:
            raise ValueError("R1 dataset must be non-empty")
        for values in (self.reliability, self.evidence, self.participant, self.item):
            if values.size != n:
                raise ValueError("R1 arrays must have equal length")


@dataclass(frozen=True)
class R2Dataset:
    share: np.ndarray
    belief: np.ndarray
    accuracy_cue: np.ndarray
    reward_context: np.ndarray
    participant: np.ndarray
    item: np.ndarray

    def __post_init__(self) -> None:
        n = self.share.size
        if n == 0:
            raise ValueError("R2 dataset must be non-empty")
        for values in (
            self.belief,
            self.accuracy_cue,
            self.reward_context,
            self.participant,
            self.item,
        ):
            if values.size != n:
                raise ValueError("R2 arrays must have equal length")
        if np.any((self.share != 0) & (self.share != 1)):
            raise ValueError("Share observations must be binary")


@dataclass(frozen=True)
class Split:
    train: np.ndarray
    held_out_participant: np.ndarray
    held_out_item: np.ndarray


@dataclass(frozen=True)
class R1Fit:
    family: R1Family
    intercept: float
    slope: float
    sigma2: float
    log_likelihood: float
    parameter_count: int
    tau: float | None = None

    @property
    def aic(self) -> float:
        return 2.0 * self.parameter_count - 2.0 * self.log_likelihood


@dataclass(frozen=True)
class R2Fit:
    family: R2Family
    parameters: tuple[float, ...]
    log_likelihood: float
    parameter_count: int

    @property
    def aic(self) -> float:
        return 2.0 * self.parameter_count - 2.0 * self.log_likelihood


def source_weight(
    family: R1Family,
    reliability: np.ndarray,
    *,
    tau: float | None = None,
) -> np.ndarray:
    t = np.asarray(reliability, dtype=float)
    if np.any((t < 0.0) | (t > 1.0)):
        raise ValueError("reliability must lie in [0,1]")
    if family is R1Family.SR_A:
        return 2.0 * t - 1.0
    if family is R1Family.SR_B:
        return t
    if family is R1Family.SR_C:
        if tau is None or not 0.0 <= tau <= 1.0:
            raise ValueError("SR-C requires tau in [0,1]")
        return (t >= float(tau)).astype(float)
    raise ValueError("INCONCLUSIVE cannot generate source weights")


def _balanced_conditions(
    levels: tuple[tuple[float, ...], ...],
    items: int,
) -> np.ndarray:
    from itertools import product

    combos = np.asarray(list(product(*levels)), dtype=float)
    if items < len(combos):
        raise ValueError("item count must cover every declared condition combination")
    reps = int(np.ceil(items / len(combos)))
    return np.tile(combos, (reps, 1))[:items]


def _crossed_indices(participants: int, items: int) -> tuple[np.ndarray, np.ndarray]:
    if participants < 4 or items < 4:
        raise ValueError("participant/item counts must both be at least four")
    participant = np.repeat(np.arange(participants, dtype=int), items)
    item = np.tile(np.arange(items, dtype=int), participants)
    return participant, item


def split_crossed(
    participant: np.ndarray,
    item: np.ndarray,
    *,
    participant_fraction: float = 0.2,
    item_fraction: float = 0.2,
) -> Split:
    p_unique = np.unique(participant)
    i_unique = np.unique(item)
    p_hold_n = max(1, int(round(len(p_unique) * participant_fraction)))
    i_hold_n = max(1, int(round(len(i_unique) * item_fraction)))
    p_hold = set(int(x) for x in p_unique[-p_hold_n:])
    i_hold = set(int(x) for x in i_unique[-i_hold_n:])

    p_is_hold = np.asarray([int(x) in p_hold for x in participant], dtype=bool)
    i_is_hold = np.asarray([int(x) in i_hold for x in item], dtype=bool)
    train = ~(p_is_hold | i_is_hold)
    held_p = p_is_hold & ~i_is_hold
    held_i = ~p_is_hold & i_is_hold

    if not train.any() or not held_p.any() or not held_i.any():
        raise ValueError("crossed split produced an empty surface")
    return Split(train=train, held_out_participant=held_p, held_out_item=held_i)


def _apply_missingness(
    arrays: tuple[np.ndarray, ...],
    *,
    rate: float,
    rng: np.random.Generator,
) -> tuple[np.ndarray, ...]:
    if not 0.0 <= rate < 1.0:
        raise ValueError("missingness rate must lie in [0,1)")
    if rate == 0.0:
        return arrays
    keep = rng.random(arrays[0].size) >= rate
    if keep.sum() < 8:
        raise RuntimeError("missingness removed too many synthetic observations")
    return tuple(values[keep] for values in arrays)


def simulate_r1_dataset(
    *,
    family: R1Family,
    participants: int,
    items: int,
    reliability_levels: tuple[float, ...],
    evidence_levels: tuple[float, ...],
    intercept: float,
    evidence_scale: float,
    noise_sd: float,
    participant_intercept_sd: float,
    item_intercept_sd: float,
    participant_slope_sd: float,
    item_slope_sd: float,
    rng: np.random.Generator,
    missingness_rate: float = 0.0,
    tau: float | None = None,
) -> R1Dataset:
    if family is R1Family.INCONCLUSIVE:
        raise ValueError("INCONCLUSIVE cannot generate R1 data")
    if noise_sd <= 0:
        raise ValueError("noise_sd must be positive")
    conditions = _balanced_conditions((reliability_levels, evidence_levels), items)
    participant, item = _crossed_indices(participants, items)
    reliability = conditions[item, 0]
    evidence = conditions[item, 1]
    base = evidence * source_weight(family, reliability, tau=tau)

    p_intercept = rng.normal(0.0, participant_intercept_sd, participants)
    i_intercept = rng.normal(0.0, item_intercept_sd, items)
    p_slope = rng.normal(0.0, participant_slope_sd, participants)
    i_slope = rng.normal(0.0, item_slope_sd, items)

    y = (
        float(intercept)
        + float(evidence_scale) * base
        + p_intercept[participant]
        + i_intercept[item]
        + p_slope[participant] * base
        + i_slope[item] * base
        + rng.normal(0.0, noise_sd, base.size)
    )
    y, reliability, evidence, participant, item = _apply_missingness(
        (y, reliability, evidence, participant, item),
        rate=missingness_rate,
        rng=rng,
    )
    return R1Dataset(
        y=np.asarray(y, dtype=float),
        reliability=np.asarray(reliability, dtype=float),
        evidence=np.asarray(evidence, dtype=float),
        participant=np.asarray(participant, dtype=int),
        item=np.asarray(item, dtype=int),
    )


def _gaussian_fit(
    y: np.ndarray,
    x: np.ndarray,
    *,
    extra_parameters: int = 0,
) -> tuple[float, float, float, float, int]:
    design = np.column_stack((np.ones(y.size), x))
    coef, *_ = np.linalg.lstsq(design, y, rcond=None)
    resid = y - design @ coef
    sigma2 = max(float(np.mean(resid**2)), 1e-10)
    ll = float(-0.5 * y.size * (log(2.0 * pi * sigma2) + 1.0))
    return float(coef[0]), float(coef[1]), sigma2, ll, 3 + int(extra_parameters)


def fit_r1_candidate(
    family: R1Family,
    dataset: R1Dataset,
    mask: np.ndarray,
    *,
    tau_grid: tuple[float, ...],
) -> R1Fit:
    if family is R1Family.INCONCLUSIVE:
        raise ValueError("INCONCLUSIVE cannot be fit")
    y = dataset.y[mask]
    reliability = dataset.reliability[mask]
    evidence = dataset.evidence[mask]

    if family is not R1Family.SR_C:
        x = evidence * source_weight(family, reliability)
        intercept, slope, sigma2, ll, k = _gaussian_fit(y, x)
        return R1Fit(family, intercept, slope, sigma2, ll, k)

    best: R1Fit | None = None
    for tau in tau_grid:
        x = evidence * source_weight(family, reliability, tau=float(tau))
        intercept, slope, sigma2, ll, k = _gaussian_fit(
            y,
            x,
            extra_parameters=1,
        )
        fit = R1Fit(
            family,
            intercept,
            slope,
            sigma2,
            ll,
            k,
            tau=float(tau),
        )
        if best is None or fit.aic < best.aic:
            best = fit
    if best is None:
        raise ValueError("SR-C tau grid must be non-empty")
    return best


def r1_predictive_log_likelihood(
    fit: R1Fit,
    dataset: R1Dataset,
    mask: np.ndarray,
) -> float:
    reliability = dataset.reliability[mask]
    evidence = dataset.evidence[mask]
    x = evidence * source_weight(fit.family, reliability, tau=fit.tau)
    residual = dataset.y[mask] - (fit.intercept + fit.slope * x)
    return float(
        -0.5
        * np.sum(
            np.log(2.0 * pi * fit.sigma2)
            + residual**2 / fit.sigma2
        )
    )


def _unique_choice(
    scores: dict[str, float],
    *,
    maximize: bool,
    tolerance: float,
) -> str | None:
    ordered = sorted(scores.items(), key=lambda kv: kv[1], reverse=maximize)
    if len(ordered) < 2:
        return ordered[0][0] if ordered else None
    if abs(ordered[0][1] - ordered[1][1]) <= tolerance:
        return None
    return ordered[0][0]


def select_r1_candidate(
    fits: dict[R1Family, R1Fit],
    dataset: R1Dataset,
    split: Split,
    *,
    tolerance: float = 1e-8,
) -> R1Family:
    aic = {family.value: fit.aic for family, fit in fits.items()}
    held_p = {
        family.value: r1_predictive_log_likelihood(
            fit,
            dataset,
            split.held_out_participant,
        )
        for family, fit in fits.items()
    }
    held_i = {
        family.value: r1_predictive_log_likelihood(
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


def _r2_eta(
    family: R2Family,
    params: np.ndarray,
    belief: np.ndarray,
    accuracy: np.ndarray,
    reward: np.ndarray,
) -> np.ndarray:
    centered_belief = 2.0 * belief - 1.0
    if family is R2Family.AP_A:
        bias, baseline_logit, beta_accuracy, beta_reward = params
        w = expit(baseline_logit + beta_accuracy * accuracy)
        return bias + w * centered_belief + beta_reward * (1.0 - w) * reward
    if family is R2Family.AP_B:
        bias, beta_b, beta_a, beta_r = params
        return (
            bias
            + beta_b * centered_belief
            + beta_a * accuracy
            + beta_r * reward
        )
    if family is R2Family.AP_C:
        bias, beta_b, beta_a, beta_r, beta_ab, beta_ar = params
        return (
            bias
            + beta_b * centered_belief
            + beta_a * accuracy
            + beta_r * reward
            + beta_ab * accuracy * centered_belief
            + beta_ar * accuracy * reward
        )
    raise ValueError("INCONCLUSIVE cannot define an action utility")


def simulate_r2_dataset(
    *,
    family: R2Family,
    participants: int,
    items: int,
    belief_levels: tuple[float, ...],
    accuracy_levels: tuple[float, ...],
    reward_levels: tuple[float, ...],
    parameters: tuple[float, ...],
    participant_intercept_sd: float,
    item_intercept_sd: float,
    participant_reward_slope_sd: float,
    item_reward_slope_sd: float,
    rng: np.random.Generator,
    missingness_rate: float = 0.0,
) -> R2Dataset:
    if family is R2Family.INCONCLUSIVE:
        raise ValueError("INCONCLUSIVE cannot generate R2 data")
    conditions = _balanced_conditions(
        (belief_levels, accuracy_levels, reward_levels),
        items,
    )
    participant, item = _crossed_indices(participants, items)
    belief = conditions[item, 0]
    accuracy = conditions[item, 1]
    reward = conditions[item, 2]

    eta = _r2_eta(
        family,
        np.asarray(parameters, dtype=float),
        belief,
        accuracy,
        reward,
    )
    p_intercept = rng.normal(0.0, participant_intercept_sd, participants)
    i_intercept = rng.normal(0.0, item_intercept_sd, items)
    p_slope = rng.normal(0.0, participant_reward_slope_sd, participants)
    i_slope = rng.normal(0.0, item_reward_slope_sd, items)

    eta = (
        eta
        + p_intercept[participant]
        + i_intercept[item]
        + p_slope[participant] * reward
        + i_slope[item] * reward
    )
    share = rng.binomial(1, expit(eta)).astype(int)
    share, belief, accuracy, reward, participant, item = _apply_missingness(
        (share, belief, accuracy, reward, participant, item),
        rate=missingness_rate,
        rng=rng,
    )
    return R2Dataset(
        share=np.asarray(share, dtype=int),
        belief=np.asarray(belief, dtype=float),
        accuracy_cue=np.asarray(accuracy, dtype=float),
        reward_context=np.asarray(reward, dtype=float),
        participant=np.asarray(participant, dtype=int),
        item=np.asarray(item, dtype=int),
    )


def _bernoulli_log_likelihood(y: np.ndarray, eta: np.ndarray) -> float:
    p = np.clip(
        expit(eta),
        np.finfo(float).eps,
        1.0 - np.finfo(float).eps,
    )
    return float(np.sum(xlogy(y, p) + xlog1py(1 - y, -p)))


def fit_r2_candidate(
    family: R2Family,
    dataset: R2Dataset,
    mask: np.ndarray,
) -> R2Fit:
    if family is R2Family.INCONCLUSIVE:
        raise ValueError("INCONCLUSIVE cannot be fit")
    belief = dataset.belief[mask]
    accuracy = dataset.accuracy_cue[mask]
    reward = dataset.reward_context[mask]
    y = dataset.share[mask]

    if family is R2Family.AP_A:
        x0 = np.asarray([0.0, 0.0, 0.5, 0.5], dtype=float)
        bounds = [
            (-5.0, 5.0),
            (-4.0, 4.0),
            (-5.0, 5.0),
            (-5.0, 5.0),
        ]
    elif family is R2Family.AP_B:
        x0 = np.asarray([0.0, 0.5, 0.0, 0.5], dtype=float)
        bounds = [(-5.0, 5.0)] * 4
    else:
        x0 = np.asarray([0.0, 0.5, 0.0, 0.5, 0.0, 0.0], dtype=float)
        bounds = [(-5.0, 5.0)] * 6

    def objective(x: np.ndarray) -> float:
        return -_bernoulli_log_likelihood(
            y,
            _r2_eta(family, x, belief, accuracy, reward),
        )

    result = minimize(
        objective,
        x0=x0,
        method="L-BFGS-B",
        bounds=bounds,
        options={"maxiter": 300, "ftol": 1e-10},
    )
    if not result.success:
        result = minimize(
            objective,
            x0=x0,
            method="L-BFGS-B",
            bounds=bounds,
            options={"maxiter": 500, "maxls": 100, "ftol": 1e-9},
        )
    if not result.success:
        raise RuntimeError(f"{family.value} fit failed: {result.message}")
    return R2Fit(
        family=family,
        parameters=tuple(float(x) for x in result.x),
        log_likelihood=float(-result.fun),
        parameter_count=len(result.x),
    )


def r2_predictive_log_likelihood(
    fit: R2Fit,
    dataset: R2Dataset,
    mask: np.ndarray,
) -> float:
    return _bernoulli_log_likelihood(
        dataset.share[mask],
        _r2_eta(
            fit.family,
            np.asarray(fit.parameters, dtype=float),
            dataset.belief[mask],
            dataset.accuracy_cue[mask],
            dataset.reward_context[mask],
        ),
    )


def select_r2_candidate(
    fits: dict[R2Family, R2Fit],
    dataset: R2Dataset,
    split: Split,
    *,
    tolerance: float = 1e-8,
) -> R2Family:
    aic = {family.value: fit.aic for family, fit in fits.items()}
    held_p = {
        family.value: r2_predictive_log_likelihood(
            fit,
            dataset,
            split.held_out_participant,
        )
        for family, fit in fits.items()
    }
    held_i = {
        family.value: r2_predictive_log_likelihood(
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


def _seed(
    master: int,
    problem: int,
    generator: int,
    replicate: int,
) -> np.random.Generator:
    return np.random.default_rng(
        np.random.SeedSequence(
            [int(master), int(problem), int(generator), int(replicate)]
        )
    )


def _r1_choice(
    config: dict,
    family: R1Family,
    regime: dict,
    replicate: int,
) -> R1Family:
    family_index = (R1Family.SR_A, R1Family.SR_B, R1Family.SR_C).index(family)
    rng = _seed(config["seed"], 1, family_index, replicate)
    r1 = config["R1"]
    random = r1["random_effects"]
    dataset = simulate_r1_dataset(
        family=family,
        participants=int(r1["participants"]),
        items=int(r1["items"]),
        reliability_levels=tuple(float(x) for x in r1["reliability_T"]),
        evidence_levels=tuple(float(x) for x in r1["signed_evidence_E"]),
        intercept=float(regime["intercept"]),
        evidence_scale=float(regime["evidence_scale"]),
        noise_sd=float(regime["noise_sd"]),
        participant_intercept_sd=float(random["participant_intercept_sd"]),
        item_intercept_sd=float(random["item_intercept_sd"]),
        participant_slope_sd=float(random["participant_slope_sd"]),
        item_slope_sd=float(random["item_slope_sd"]),
        rng=rng,
        missingness_rate=float(config["missingness_rate"]),
        tau=float(regime["tau"]) if family is R1Family.SR_C else None,
    )
    split = split_crossed(dataset.participant, dataset.item)
    fits = {
        candidate: fit_r1_candidate(
            candidate,
            dataset,
            split.train,
            tau_grid=tuple(float(x) for x in r1["tau_grid"]),
        )
        for candidate in (R1Family.SR_A, R1Family.SR_B, R1Family.SR_C)
    }
    return select_r1_candidate(fits, dataset, split)


def _r2_choice(
    config: dict,
    family: R2Family,
    regime: dict,
    replicate: int,
) -> R2Family:
    family_index = (R2Family.AP_A, R2Family.AP_B, R2Family.AP_C).index(family)
    rng = _seed(config["seed"], 2, family_index, replicate)
    r2 = config["R2"]
    random = r2["random_effects"]
    dataset = simulate_r2_dataset(
        family=family,
        participants=int(r2["participants"]),
        items=int(r2["items"]),
        belief_levels=tuple(float(x) for x in r2["belief_B"]),
        accuracy_levels=tuple(float(x) for x in r2["accuracy_cue_A"]),
        reward_levels=tuple(float(x) for x in r2["reward_context_R"]),
        parameters=tuple(float(x) for x in regime["parameters"]),
        participant_intercept_sd=float(random["participant_intercept_sd"]),
        item_intercept_sd=float(random["item_intercept_sd"]),
        participant_reward_slope_sd=float(
            random["participant_reward_slope_sd"]
        ),
        item_reward_slope_sd=float(random["item_reward_slope_sd"]),
        rng=rng,
        missingness_rate=float(config["missingness_rate"]),
    )
    split = split_crossed(dataset.participant, dataset.item)
    fits = {
        candidate: fit_r2_candidate(candidate, dataset, split.train)
        for candidate in (R2Family.AP_A, R2Family.AP_B, R2Family.AP_C)
    }
    return select_r2_candidate(fits, dataset, split)


def _summary(
    generator: str,
    selected: dict[str, int],
    replicates: int,
) -> dict:
    correct = selected[generator]
    inconclusive = selected["INCONCLUSIVE"]
    wrong = replicates - correct - inconclusive
    return {
        "generator": generator,
        "replicates": replicates,
        "selected": selected,
        "recovery_probability": correct / replicates,
        "wrong_probability": wrong / replicates,
        "inconclusive_probability": inconclusive / replicates,
    }


def run_smoke_benchmark(config: dict) -> dict:
    if config.get("status") != "SMOKE_CONFIG_NON_AUTHORITATIVE":
        raise ValueError(
            "F1b engine currently accepts smoke/non-authoritative configs only"
        )
    replicates = int(config["replicates"])
    if replicates <= 0:
        raise ValueError("replicates must be positive")

    r1_rows = []
    for family in (R1Family.SR_A, R1Family.SR_B, R1Family.SR_C):
        selected = {x.value: 0 for x in R1Family}
        regime = config["R1"]["generator_regimes"][family.value]
        for replicate in range(replicates):
            choice = _r1_choice(config, family, regime, replicate)
            selected[choice.value] += 1
        r1_rows.append(_summary(family.value, selected, replicates))

    r2_rows = []
    for family in (R2Family.AP_A, R2Family.AP_B, R2Family.AP_C):
        selected = {x.value: 0 for x in R2Family}
        regime = config["R2"]["generator_regimes"][family.value]
        for replicate in range(replicates):
            choice = _r2_choice(config, family, regime, replicate)
            selected[choice.value] += 1
        r2_rows.append(_summary(family.value, selected, replicates))

    return {
        "benchmark_id": config["benchmark_id"],
        "status": "SMOKE_NON_AUTHORITATIVE",
        "authoritative": False,
        "seed": int(config["seed"]),
        "replicates": replicates,
        "R1": {"grid_results": r1_rows},
        "R2": {"grid_results": r2_rows},
        "interpretation_boundary": (
            "Smoke-only synthetic recovery engine check. Results do not freeze "
            "core cells, human N, empirical mechanisms, parameter values, or "
            "F1b runtime behavior."
        ),
    }
