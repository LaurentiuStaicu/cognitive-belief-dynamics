from __future__ import annotations

import numpy as np

from cognitive_epistemic_model.calibration.f1b_prehuman_recovery import (
    R2Family,
    simulate_r2_dataset,
)
from cognitive_epistemic_model.calibration.f1b_r2_population_restriction_recovery import (
    POPULATION_BOOTSTRAP_METHOD_NAMESPACE,
    bootstrap_population_restriction_test,
    bootstrap_population_restriction_test_prefix_snapshots,
    fit_population_restriction_pair,
    population_bootstrap_seed_sequence,
    population_held_out_predictive_deltas,
    simulate_exact_design_under_population_restriction,
)
from cognitive_epistemic_model.calibration.f1b_r2_restriction_recovery import (
    R2Restriction,
)


def _dataset(
    family: R2Family,
    parameters: tuple[float, ...],
    *,
    seed: int,
    participants: int = 10,
    items: int = 18,
    random_effect_sd: float = 0.0,
    missingness_rate: float = 0.0,
):
    return simulate_r2_dataset(
        family=family,
        participants=participants,
        items=items,
        belief_levels=(0.2, 0.5, 0.8),
        accuracy_levels=(0.0, 1.0),
        reward_levels=(-1.0, 0.0, 1.0),
        parameters=parameters,
        participant_intercept_sd=random_effect_sd,
        item_intercept_sd=random_effect_sd,
        participant_reward_slope_sd=random_effect_sd,
        item_reward_slope_sd=random_effect_sd,
        rng=np.random.default_rng(seed),
        missingness_rate=missingness_rate,
    )


def test_population_add_pair_is_nested_and_finite() -> None:
    dataset = _dataset(
        R2Family.AP_B,
        (-0.2, 0.8, 0.25, 0.6),
        seed=101,
    )
    pair = fit_population_restriction_pair(
        dataset,
        R2Restriction.ADD,
    )
    assert pair.restricted.family is R2Family.AP_B
    assert pair.general.family is R2Family.AP_C
    assert np.isfinite(pair.statistic)
    assert pair.statistic >= 0.0
    assert (
        pair.general.log_likelihood + 1e-6
        >= pair.restricted.log_likelihood
    )


def test_population_general_departure_improves_over_add_restriction() -> None:
    dataset = _dataset(
        R2Family.AP_C,
        (-0.2, 0.5, 0.0, 0.5, 1.4, 1.2),
        seed=102,
        participants=24,
        items=36,
    )
    pair = fit_population_restriction_pair(
        dataset,
        R2Restriction.ADD,
    )
    assert pair.statistic > 1.0


def test_population_bootstrap_simulation_preserves_exact_design() -> None:
    dataset = _dataset(
        R2Family.AP_A,
        (-0.2, -0.2, 1.0, 0.8),
        seed=103,
    )
    pair = fit_population_restriction_pair(
        dataset,
        R2Restriction.CBD_COMPLEMENT,
    )
    first = simulate_exact_design_under_population_restriction(
        dataset,
        pair.restricted,
        rng=np.random.default_rng(777),
    )
    second = simulate_exact_design_under_population_restriction(
        dataset,
        pair.restricted,
        rng=np.random.default_rng(777),
    )
    assert np.array_equal(first.share, second.share)
    assert np.array_equal(first.belief, dataset.belief)
    assert np.array_equal(first.accuracy_cue, dataset.accuracy_cue)
    assert np.array_equal(first.reward_context, dataset.reward_context)
    assert np.array_equal(first.participant, dataset.participant)
    assert np.array_equal(first.item, dataset.item)


def test_population_bootstrap_namespace_is_method_specific() -> None:
    sequence = population_bootstrap_seed_sequence(
        seed=20260928,
        restriction=R2Restriction.ADD,
        draw_index=4,
    )
    expected = np.random.SeedSequence(
        [
            20260928,
            POPULATION_BOOTSTRAP_METHOD_NAMESPACE,
            1,
            4,
        ]
    )
    hierarchical_shape = np.random.SeedSequence([20260928, 1, 4])
    assert np.array_equal(
        sequence.generate_state(8),
        expected.generate_state(8),
    )
    assert not np.array_equal(
        sequence.generate_state(8),
        hierarchical_shape.generate_state(8),
    )


def test_population_holdouts_are_finite_with_crossed_heterogeneity() -> None:
    dataset = _dataset(
        R2Family.AP_A,
        (-0.2, -0.2, 1.0, 0.8),
        seed=104,
        participants=12,
        items=18,
        random_effect_sd=0.15,
    )
    participant_delta, item_delta = population_held_out_predictive_deltas(
        dataset,
        R2Restriction.CBD_COMPLEMENT,
    )
    assert np.isfinite(participant_delta)
    assert np.isfinite(item_delta)


def test_population_prefix_bootstrap_is_exactly_reproducible() -> None:
    dataset = _dataset(
        R2Family.AP_B,
        (-0.2, 0.8, 0.25, 0.6),
        seed=105,
        participants=8,
        items=18,
    )
    kwargs = dict(
        dataset=dataset,
        restriction=R2Restriction.ADD,
        draw_counts=(3, 5),
        minimum_successful_draws_by_count={3: 3, 5: 5},
        seed=9901,
    )
    first = bootstrap_population_restriction_test_prefix_snapshots(**kwargs)
    second = bootstrap_population_restriction_test_prefix_snapshots(**kwargs)
    assert first.observed_statistic == second.observed_statistic
    assert first.bootstrap_attempt_statistics == (
        second.bootstrap_attempt_statistics
    )
    assert first.snapshots == second.snapshots
    assert len(first.bootstrap_attempt_statistics) == 5
    assert first.snapshots[0].bootstrap_draws_requested == 3
    assert first.snapshots[1].bootstrap_draws_requested == 5


def test_population_single_count_bootstrap_uses_parametric_calibration() -> None:
    dataset = _dataset(
        R2Family.AP_B,
        (-0.2, 0.8, 0.25, 0.6),
        seed=106,
        participants=8,
        items=18,
    )
    result = bootstrap_population_restriction_test(
        dataset,
        R2Restriction.ADD,
        bootstrap_draws=5,
        minimum_successful_draws=5,
        seed=9902,
    )
    assert result.bootstrap_draws_requested == 5
    assert result.bootstrap_draws_successful == 5
    assert result.bootstrap_fit_failures == 0
    assert len(result.bootstrap_statistics) == 5
    assert 0.0 < result.p_value <= 1.0
    assert np.isfinite(result.critical_value)
    assert isinstance(result.rejected, bool)
