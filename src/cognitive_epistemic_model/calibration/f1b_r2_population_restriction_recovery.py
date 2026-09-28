from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.special import expit

from .f1b_prehuman_recovery import (
    R2Dataset,
    R2Family,
    R2Fit,
    fit_r2_candidate,
    r2_predictive_log_likelihood,
    split_crossed,
)
from .f1b_r2_restriction_recovery import (
    BootstrapCalibrationError,
    R2Restriction,
    RestrictionBootstrapPrefixSnapshot,
    restricted_family,
)


POPULATION_BOOTSTRAP_METHOD_NAMESPACE = 2


@dataclass(frozen=True)
class PopulationRestrictionPairFit:
    restriction: R2Restriction
    restricted: R2Fit
    general: R2Fit
    statistic: float


@dataclass(frozen=True)
class PopulationPairedRestrictionBootstrapResult:
    restriction: R2Restriction
    observed_statistic: float
    bootstrap_attempt_statistics: tuple[float | None, ...]
    snapshots: tuple[RestrictionBootstrapPrefixSnapshot, ...]
    held_out_participant_delta: float
    held_out_item_delta: float


@dataclass(frozen=True)
class PopulationRestrictionBootstrapResult:
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


def _population_fixed_eta(
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
    raise ValueError("INCONCLUSIVE cannot define population utility")


def fit_population_restriction_pair(
    dataset: R2Dataset,
    restriction: R2Restriction,
    *,
    mask: np.ndarray | None = None,
    nesting_tolerance: float = 1e-6,
) -> PopulationRestrictionPairFit:
    if mask is None:
        mask = np.ones(dataset.share.size, dtype=bool)
    family = restricted_family(restriction)
    restricted = fit_r2_candidate(
        family,
        dataset,
        mask,
    )
    general = fit_r2_candidate(
        R2Family.AP_C,
        dataset,
        mask,
    )
    raw = float(general.log_likelihood - restricted.log_likelihood)
    if raw < -abs(float(nesting_tolerance)):
        raise RuntimeError(
            "nested population restricted fit has higher log likelihood than "
            f"AP-GENERAL by {-raw:.6g}; optimization/nesting integrity failed"
        )
    return PopulationRestrictionPairFit(
        restriction=restriction,
        restricted=restricted,
        general=general,
        statistic=max(0.0, raw),
    )


def simulate_exact_design_under_population_restriction(
    template: R2Dataset,
    fit: R2Fit,
    *,
    rng: np.random.Generator,
) -> R2Dataset:
    if fit.family not in (R2Family.AP_A, R2Family.AP_B):
        raise ValueError("population bootstrap null fit must be ADD or CBD restricted")
    eta = _population_fixed_eta(
        fit.family,
        fit.parameters,
        template.belief,
        template.accuracy_cue,
        template.reward_context,
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


def population_held_out_predictive_deltas(
    dataset: R2Dataset,
    restriction: R2Restriction,
) -> tuple[float, float]:
    split = split_crossed(dataset.participant, dataset.item)
    pair = fit_population_restriction_pair(
        dataset,
        restriction,
        mask=split.train,
    )
    participant_delta = (
        r2_predictive_log_likelihood(
            pair.general,
            dataset,
            split.held_out_participant,
        )
        - r2_predictive_log_likelihood(
            pair.restricted,
            dataset,
            split.held_out_participant,
        )
    )
    item_delta = (
        r2_predictive_log_likelihood(
            pair.general,
            dataset,
            split.held_out_item,
        )
        - r2_predictive_log_likelihood(
            pair.restricted,
            dataset,
            split.held_out_item,
        )
    )
    return float(participant_delta), float(item_delta)


def population_bootstrap_seed_sequence(
    *,
    seed: int,
    restriction: R2Restriction,
    draw_index: int,
) -> np.random.SeedSequence:
    restriction_index = 1 if restriction is R2Restriction.ADD else 2
    return np.random.SeedSequence(
        [
            int(seed),
            int(POPULATION_BOOTSTRAP_METHOD_NAMESPACE),
            int(restriction_index),
            int(draw_index),
        ]
    )


def bootstrap_population_restriction_test_prefix_snapshots(
    dataset: R2Dataset,
    restriction: R2Restriction,
    *,
    draw_counts: tuple[int, ...],
    minimum_successful_draws_by_count: dict[int, int],
    seed: int,
    alpha: float = 0.05,
) -> PopulationPairedRestrictionBootstrapResult:
    if not draw_counts:
        raise ValueError("draw_counts must not be empty")
    normalized = tuple(int(value) for value in draw_counts)
    if tuple(sorted(set(normalized))) != normalized:
        raise ValueError("draw_counts must be unique and strictly increasing")
    if normalized[0] <= 0:
        raise ValueError("draw_counts must be positive")
    if not 0.0 < alpha < 1.0:
        raise ValueError("alpha must lie in (0,1)")

    thresholds: dict[int, int] = {}
    for count in normalized:
        if count not in minimum_successful_draws_by_count:
            raise ValueError(
                f"missing minimum successful bootstrap threshold for {count}"
            )
        minimum = int(minimum_successful_draws_by_count[count])
        if not 1 <= minimum <= count:
            raise ValueError(
                "minimum successful bootstrap threshold must lie inside its prefix"
            )
        thresholds[count] = minimum

    observed = fit_population_restriction_pair(
        dataset,
        restriction,
    )
    held_p_delta, held_i_delta = population_held_out_predictive_deltas(
        dataset,
        restriction,
    )

    attempts: list[float | None] = []
    for draw in range(normalized[-1]):
        rng = np.random.default_rng(
            population_bootstrap_seed_sequence(
                seed=seed,
                restriction=restriction,
                draw_index=draw,
            )
        )
        bootstrap_dataset = simulate_exact_design_under_population_restriction(
            dataset,
            observed.restricted,
            rng=rng,
        )
        try:
            pair = fit_population_restriction_pair(
                bootstrap_dataset,
                restriction,
            )
        except (RuntimeError, ValueError, np.linalg.LinAlgError):
            attempts.append(None)
            continue
        attempts.append(float(pair.statistic))

    snapshots: list[RestrictionBootstrapPrefixSnapshot] = []
    for count in normalized:
        prefix = attempts[:count]
        successful = [
            float(value)
            for value in prefix
            if value is not None
        ]
        failures = count - len(successful)
        if len(successful) < thresholds[count]:
            snapshots.append(
                RestrictionBootstrapPrefixSnapshot(
                    bootstrap_draws_requested=count,
                    bootstrap_draws_successful=len(successful),
                    bootstrap_fit_failures=failures,
                    critical_value=None,
                    p_value=None,
                    rejected=None,
                    bootstrap_calibration_failure=True,
                )
            )
            continue

        stats = np.asarray(successful, dtype=float)
        critical = float(
            np.quantile(stats, 1.0 - alpha, method="higher")
        )
        p_value = float(
            (1 + int(np.sum(stats >= observed.statistic)))
            / (1 + stats.size)
        )
        snapshots.append(
            RestrictionBootstrapPrefixSnapshot(
                bootstrap_draws_requested=count,
                bootstrap_draws_successful=int(stats.size),
                bootstrap_fit_failures=failures,
                critical_value=critical,
                p_value=p_value,
                rejected=bool(p_value <= alpha),
                bootstrap_calibration_failure=False,
            )
        )

    return PopulationPairedRestrictionBootstrapResult(
        restriction=restriction,
        observed_statistic=float(observed.statistic),
        bootstrap_attempt_statistics=tuple(attempts),
        snapshots=tuple(snapshots),
        held_out_participant_delta=float(held_p_delta),
        held_out_item_delta=float(held_i_delta),
    )


def bootstrap_population_restriction_test(
    dataset: R2Dataset,
    restriction: R2Restriction,
    *,
    bootstrap_draws: int,
    seed: int,
    alpha: float = 0.05,
    minimum_successful_draws: int | None = None,
) -> PopulationRestrictionBootstrapResult:
    if bootstrap_draws <= 0:
        raise ValueError("bootstrap_draws must be positive")
    if minimum_successful_draws is None:
        minimum_successful_draws = int(bootstrap_draws)
    paired = bootstrap_population_restriction_test_prefix_snapshots(
        dataset,
        restriction,
        draw_counts=(int(bootstrap_draws),),
        minimum_successful_draws_by_count={
            int(bootstrap_draws): int(minimum_successful_draws)
        },
        seed=int(seed),
        alpha=float(alpha),
    )
    snapshot = paired.snapshots[0]
    if snapshot.bootstrap_calibration_failure:
        raise BootstrapCalibrationError(
            "insufficient successful population bootstrap refits: "
            f"{snapshot.bootstrap_draws_successful}/{bootstrap_draws}"
        )
    successful = tuple(
        float(value)
        for value in paired.bootstrap_attempt_statistics
        if value is not None
    )
    if (
        snapshot.critical_value is None
        or snapshot.p_value is None
        or snapshot.rejected is None
    ):
        raise RuntimeError("population bootstrap snapshot is unexpectedly incomplete")
    return PopulationRestrictionBootstrapResult(
        restriction=restriction,
        observed_statistic=float(paired.observed_statistic),
        bootstrap_statistics=successful,
        bootstrap_draws_requested=int(snapshot.bootstrap_draws_requested),
        bootstrap_draws_successful=int(snapshot.bootstrap_draws_successful),
        bootstrap_fit_failures=int(snapshot.bootstrap_fit_failures),
        critical_value=float(snapshot.critical_value),
        p_value=float(snapshot.p_value),
        rejected=bool(snapshot.rejected),
        held_out_participant_delta=float(
            paired.held_out_participant_delta
        ),
        held_out_item_delta=float(paired.held_out_item_delta),
    )
