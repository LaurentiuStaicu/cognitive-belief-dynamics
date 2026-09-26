from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

import numpy as np
from scipy.special import expit

from .f1b_hierarchical_recovery import (
    R2HierarchicalFit,
    RandomEffectScales,
    fit_r2_hierarchical_candidate,
    r2_hierarchical_predictive_log_likelihood,
)
from .f1b_prehuman_recovery import (
    R2Dataset,
    R2Family,
    simulate_r2_dataset,
    split_crossed,
)


class R2Restriction(str, Enum):
    ADD = "ADD_RESTRICTION"
    CBD_COMPLEMENT = "CBD_COMPLEMENT_RESTRICTION"


class BootstrapCalibrationError(RuntimeError):
    pass


@dataclass(frozen=True)
class RestrictionPairFit:
    restriction: R2Restriction
    restricted: R2HierarchicalFit
    general: R2HierarchicalFit
    statistic: float


@dataclass(frozen=True)
class RestrictionBootstrapResult:
    restriction: R2Restriction
    observed_statistic: float
    bootstrap_statistics: tuple[float, ...]
    bootstrap_draws_requested: int
    bootstrap_draws_successful: int
    bootstrap_fit_failures: int
    critical_value: float
    p_value: float
    rejected: bool
    held_out_participant_delta: float
    held_out_item_delta: float


def restricted_family(restriction: R2Restriction) -> R2Family:
    if restriction is R2Restriction.ADD:
        return R2Family.AP_B
    if restriction is R2Restriction.CBD_COMPLEMENT:
        return R2Family.AP_A
    raise ValueError(f"unsupported restriction: {restriction}")


def _fixed_eta(
    family: R2Family,
    params: tuple[float, ...] | np.ndarray,
    belief: np.ndarray,
    accuracy: np.ndarray,
    reward: np.ndarray,
) -> np.ndarray:
    p = np.asarray(params, dtype=float)
    centered = 2.0 * belief - 1.0
    if family is R2Family.AP_A:
        bias, baseline_logit, beta_accuracy, beta_reward = p
        w = expit(baseline_logit + beta_accuracy * accuracy)
        return bias + w * centered + beta_reward * (1.0 - w) * reward
    if family is R2Family.AP_B:
        bias, beta_b, beta_a, beta_r = p
        return bias + beta_b * centered + beta_a * accuracy + beta_r * reward
    if family is R2Family.AP_C:
        bias, beta_b, beta_a, beta_r, beta_ab, beta_ar = p
        return (
            bias
            + beta_b * centered
            + beta_a * accuracy
            + beta_r * reward
            + beta_ab * accuracy * centered
            + beta_ar * accuracy * reward
        )
    raise ValueError("INCONCLUSIVE cannot define utility")


def cbd_fit_to_general_coefficients(
    fixed_parameters: tuple[float, ...],
) -> tuple[float, float, float, float, float, float]:
    bias, baseline_logit, beta_accuracy, beta_reward = fixed_parameters
    w0 = float(expit(baseline_logit))
    w1 = float(expit(baseline_logit + beta_accuracy))
    return (
        float(bias),
        w0,
        0.0,
        float(beta_reward) * (1.0 - w0),
        w1 - w0,
        float(beta_reward) * (w0 - w1),
    )


def add_fit_to_general_coefficients(
    fixed_parameters: tuple[float, ...],
) -> tuple[float, float, float, float, float, float]:
    bias, beta_b, beta_a, beta_r = fixed_parameters
    return (
        float(bias),
        float(beta_b),
        float(beta_a),
        float(beta_r),
        0.0,
        0.0,
    )


def general_coefficients(
    fit: R2HierarchicalFit,
) -> tuple[float, float, float, float, float, float]:
    if fit.family is R2Family.AP_A:
        return cbd_fit_to_general_coefficients(fit.fixed_parameters)
    if fit.family is R2Family.AP_B:
        return add_fit_to_general_coefficients(fit.fixed_parameters)
    if fit.family is R2Family.AP_C:
        return tuple(float(x) for x in fit.fixed_parameters)
    raise ValueError("unsupported fitted family")


def fit_restriction_pair(
    dataset: R2Dataset,
    restriction: R2Restriction,
    *,
    scales: RandomEffectScales,
    mask: np.ndarray | None = None,
    nesting_tolerance: float = 1e-6,
) -> RestrictionPairFit:
    if mask is None:
        mask = np.ones(dataset.share.size, dtype=bool)
    family = restricted_family(restriction)
    restricted = fit_r2_hierarchical_candidate(
        family,
        dataset,
        mask,
        scales=scales,
    )
    general = fit_r2_hierarchical_candidate(
        R2Family.AP_C,
        dataset,
        mask,
        scales=scales,
    )
    raw = float(restricted.penalized_objective - general.penalized_objective)
    if raw < -abs(float(nesting_tolerance)):
        raise RuntimeError(
            "nested restricted fit has lower penalized objective than AP-GENERAL "
            f"by {-raw:.6g}; optimization/nesting integrity failed"
        )
    statistic = max(0.0, raw)
    return RestrictionPairFit(
        restriction=restriction,
        restricted=restricted,
        general=general,
        statistic=statistic,
    )


def simulate_exact_design_under_restriction(
    template: R2Dataset,
    fit: R2HierarchicalFit,
    *,
    scales: RandomEffectScales,
    rng: np.random.Generator,
) -> R2Dataset:
    if fit.family not in (R2Family.AP_A, R2Family.AP_B):
        raise ValueError("bootstrap null fit must be ADD or CBD restricted")
    participant_count = int(np.max(template.participant)) + 1
    item_count = int(np.max(template.item)) + 1

    eta = _fixed_eta(
        fit.family,
        fit.fixed_parameters,
        template.belief,
        template.accuracy_cue,
        template.reward_context,
    )
    p_intercept = rng.normal(
        0.0,
        scales.participant_intercept_sd,
        participant_count,
    )
    i_intercept = rng.normal(
        0.0,
        scales.item_intercept_sd,
        item_count,
    )
    p_slope = rng.normal(
        0.0,
        scales.participant_slope_sd,
        participant_count,
    )
    i_slope = rng.normal(
        0.0,
        scales.item_slope_sd,
        item_count,
    )
    eta = (
        eta
        + p_intercept[template.participant]
        + i_intercept[template.item]
        + p_slope[template.participant] * template.reward_context
        + i_slope[template.item] * template.reward_context
    )
    share = rng.binomial(1, expit(eta)).astype(int)
    return R2Dataset(
        share=share,
        belief=template.belief.copy(),
        accuracy_cue=template.accuracy_cue.copy(),
        reward_context=template.reward_context.copy(),
        participant=template.participant.copy(),
        item=template.item.copy(),
    )


def held_out_predictive_deltas(
    dataset: R2Dataset,
    restriction: R2Restriction,
    *,
    scales: RandomEffectScales,
) -> tuple[float, float]:
    split = split_crossed(dataset.participant, dataset.item)
    pair = fit_restriction_pair(
        dataset,
        restriction,
        scales=scales,
        mask=split.train,
    )
    participant_delta = (
        r2_hierarchical_predictive_log_likelihood(
            pair.general,
            dataset,
            split.held_out_participant,
        )
        - r2_hierarchical_predictive_log_likelihood(
            pair.restricted,
            dataset,
            split.held_out_participant,
        )
    )
    item_delta = (
        r2_hierarchical_predictive_log_likelihood(
            pair.general,
            dataset,
            split.held_out_item,
        )
        - r2_hierarchical_predictive_log_likelihood(
            pair.restricted,
            dataset,
            split.held_out_item,
        )
    )
    return float(participant_delta), float(item_delta)


def bootstrap_restriction_test(
    dataset: R2Dataset,
    restriction: R2Restriction,
    *,
    scales: RandomEffectScales,
    bootstrap_draws: int,
    seed: int,
    alpha: float = 0.05,
    minimum_successful_draws: int | None = None,
) -> RestrictionBootstrapResult:
    if bootstrap_draws <= 0:
        raise ValueError("bootstrap_draws must be positive")
    if not 0.0 < alpha < 1.0:
        raise ValueError("alpha must lie in (0,1)")
    if minimum_successful_draws is None:
        minimum_successful_draws = bootstrap_draws
    if not 1 <= minimum_successful_draws <= bootstrap_draws:
        raise ValueError("minimum_successful_draws must lie in [1, bootstrap_draws]")

    observed = fit_restriction_pair(
        dataset,
        restriction,
        scales=scales,
    )
    held_p_delta, held_i_delta = held_out_predictive_deltas(
        dataset,
        restriction,
        scales=scales,
    )

    successful: list[float] = []
    failures = 0
    restriction_index = (
        1 if restriction is R2Restriction.ADD else 2
    )
    for draw in range(bootstrap_draws):
        rng = np.random.default_rng(
            np.random.SeedSequence(
                [int(seed), int(restriction_index), int(draw)]
            )
        )
        bootstrap_dataset = simulate_exact_design_under_restriction(
            dataset,
            observed.restricted,
            scales=scales,
            rng=rng,
        )
        try:
            pair = fit_restriction_pair(
                bootstrap_dataset,
                restriction,
                scales=scales,
            )
        except (RuntimeError, ValueError, np.linalg.LinAlgError):
            failures += 1
            continue
        successful.append(float(pair.statistic))

    if len(successful) < int(minimum_successful_draws):
        raise BootstrapCalibrationError(
            "insufficient successful bootstrap refits: "
            f"{len(successful)}/{bootstrap_draws}"
        )

    stats = np.asarray(successful, dtype=float)
    critical = float(
        np.quantile(stats, 1.0 - alpha, method="higher")
    )
    p_value = float(
        (1 + int(np.sum(stats >= observed.statistic)))
        / (1 + stats.size)
    )
    return RestrictionBootstrapResult(
        restriction=restriction,
        observed_statistic=float(observed.statistic),
        bootstrap_statistics=tuple(float(x) for x in stats),
        bootstrap_draws_requested=int(bootstrap_draws),
        bootstrap_draws_successful=int(stats.size),
        bootstrap_fit_failures=int(failures),
        critical_value=critical,
        p_value=p_value,
        rejected=bool(p_value <= alpha),
        held_out_participant_delta=held_p_delta,
        held_out_item_delta=held_i_delta,
    )


def run_smoke_restriction_engine(config: dict) -> dict:
    if config["status"] != "SMOKE_NON_AUTHORITATIVE_R2_RESTRICTION_ENGINE":
        raise ValueError("only the non-authoritative smoke config is accepted")

    random_effects = config["random_effects"]
    scales = RandomEffectScales(
        participant_intercept_sd=float(
            random_effects["participant_intercept_sd"]
        ),
        item_intercept_sd=float(random_effects["item_intercept_sd"]),
        participant_slope_sd=float(
            random_effects["participant_reward_slope_sd"]
        ),
        item_slope_sd=float(random_effects["item_reward_slope_sd"]),
    )
    design = config["design"]
    bootstrap = config["bootstrap"]
    results: list[dict] = []

    cases = (
        (
            "ADD_NULL",
            R2Family.AP_B,
            tuple(float(x) for x in config["null_generators"]["ADD_NULL"]),
            R2Restriction.ADD,
            11,
        ),
        (
            "CBD_NULL",
            R2Family.AP_A,
            tuple(float(x) for x in config["null_generators"]["CBD_NULL"]),
            R2Restriction.CBD_COMPLEMENT,
            12,
        ),
    )
    for label, family, parameters, restriction, stream in cases:
        rng = np.random.default_rng(
            np.random.SeedSequence([int(config["seed"]), int(stream)])
        )
        dataset = simulate_r2_dataset(
            family=family,
            participants=int(design["participants"]),
            items=int(design["items"]),
            belief_levels=tuple(float(x) for x in design["belief_B"]),
            accuracy_levels=tuple(
                float(x) for x in design["accuracy_cue_A"]
            ),
            reward_levels=tuple(
                float(x) for x in design["reward_context_R"]
            ),
            parameters=parameters,
            participant_intercept_sd=scales.participant_intercept_sd,
            item_intercept_sd=scales.item_intercept_sd,
            participant_reward_slope_sd=scales.participant_slope_sd,
            item_reward_slope_sd=scales.item_slope_sd,
            rng=rng,
            missingness_rate=float(design["missingness_rate"]),
        )
        result = bootstrap_restriction_test(
            dataset,
            restriction,
            scales=scales,
            bootstrap_draws=int(bootstrap["draws"]),
            minimum_successful_draws=int(
                bootstrap["minimum_successful_draws"]
            ),
            seed=int(config["seed"]) + stream * 1000,
            alpha=float(bootstrap["alpha"]),
        )
        results.append(
            {
                "case": label,
                "restriction": result.restriction.value,
                "observed_statistic": result.observed_statistic,
                "bootstrap_draws_requested": result.bootstrap_draws_requested,
                "bootstrap_draws_successful": result.bootstrap_draws_successful,
                "bootstrap_fit_failures": result.bootstrap_fit_failures,
                "critical_value": result.critical_value,
                "p_value": result.p_value,
                "rejected": result.rejected,
                "held_out_participant_delta": result.held_out_participant_delta,
                "held_out_item_delta": result.held_out_item_delta,
            }
        )

    return {
        "engine_id": config["engine_id"],
        "status": "SMOKE_NON_AUTHORITATIVE_R2_RESTRICTION_RESULT",
        "authoritative": False,
        "results": results,
        "interpretation_boundary": (
            "Smoke-only restriction-engine verification. Bootstrap draws are "
            "not frozen for authoritative calibration and no result validates "
            "a human mechanism, freezes human N, authorizes recruitment, or "
            "activates runtime F1b."
        ),
    }
