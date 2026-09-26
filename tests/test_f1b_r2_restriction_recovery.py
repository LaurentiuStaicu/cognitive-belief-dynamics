from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy.special import expit

from cognitive_epistemic_model.calibration.f1b_hierarchical_recovery import (
    RandomEffectScales,
)
from cognitive_epistemic_model.calibration.f1b_prehuman_recovery import (
    R2Family,
    simulate_r2_dataset,
)
from cognitive_epistemic_model.calibration.f1b_r2_restriction_recovery import (
    R2Restriction,
    add_fit_to_general_coefficients,
    bootstrap_restriction_test,
    cbd_fit_to_general_coefficients,
    fit_restriction_pair,
    run_smoke_restriction_engine,
)

ROOT = Path(__file__).resolve().parents[1]
CONFIG = (
    ROOT
    / "model"
    / "benchmarks"
    / "f1b_r2_structural_restriction_recovery_smoke.json"
)


def load_config() -> dict:
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def scales() -> RandomEffectScales:
    return RandomEffectScales(
        participant_intercept_sd=0.20,
        item_intercept_sd=0.15,
        participant_slope_sd=0.08,
        item_slope_sd=0.08,
    )


def test_cbd_mapping_satisfies_exact_general_surface_restriction() -> None:
    fixed = (-0.2, -0.3, 1.1, 0.8)
    beta = cbd_fit_to_general_coefficients(fixed)
    _, beta_b, beta_a, beta_r, beta_ab, beta_ar = beta

    assert beta_a == 0.0
    assert abs(beta_ar * (1.0 - beta_b) + beta_r * beta_ab) < 1e-12
    assert 0.0 < beta_b < 1.0
    assert 0.0 < beta_b + beta_ab < 1.0


def test_add_mapping_sets_both_interactions_to_zero() -> None:
    beta = add_fit_to_general_coefficients((-0.2, 0.8, 0.25, 0.6))
    assert beta[4] == 0.0
    assert beta[5] == 0.0


def test_nested_pair_statistic_is_nonnegative_for_add_null_smoke() -> None:
    rng = np.random.default_rng(20)
    data = simulate_r2_dataset(
        family=R2Family.AP_B,
        participants=12,
        items=18,
        belief_levels=(0.2, 0.5, 0.8),
        accuracy_levels=(0.0, 1.0),
        reward_levels=(-1.0, 0.0, 1.0),
        parameters=(-0.2, 0.8, 0.25, 0.6),
        participant_intercept_sd=0.20,
        item_intercept_sd=0.15,
        participant_reward_slope_sd=0.08,
        item_reward_slope_sd=0.08,
        rng=rng,
    )
    pair = fit_restriction_pair(
        data,
        R2Restriction.ADD,
        scales=scales(),
    )
    assert pair.restricted.family is R2Family.AP_B
    assert pair.general.family is R2Family.AP_C
    assert pair.statistic >= 0.0


def test_bootstrap_restriction_test_is_seed_reproducible() -> None:
    rng = np.random.default_rng(21)
    data = simulate_r2_dataset(
        family=R2Family.AP_A,
        participants=12,
        items=18,
        belief_levels=(0.2, 0.5, 0.8),
        accuracy_levels=(0.0, 1.0),
        reward_levels=(-1.0, 0.0, 1.0),
        parameters=(-0.2, -0.2, 1.0, 0.8),
        participant_intercept_sd=0.20,
        item_intercept_sd=0.15,
        participant_reward_slope_sd=0.08,
        item_reward_slope_sd=0.08,
        rng=rng,
    )
    first = bootstrap_restriction_test(
        data,
        R2Restriction.CBD_COMPLEMENT,
        scales=scales(),
        bootstrap_draws=2,
        minimum_successful_draws=2,
        seed=300,
    )
    second = bootstrap_restriction_test(
        data,
        R2Restriction.CBD_COMPLEMENT,
        scales=scales(),
        bootstrap_draws=2,
        minimum_successful_draws=2,
        seed=300,
    )
    assert first == second
    assert first.bootstrap_draws_successful == 2
    assert first.bootstrap_fit_failures == 0
    assert 0.0 <= first.p_value <= 1.0


def test_smoke_engine_keeps_restrictions_independent_and_gates_closed() -> None:
    config = load_config()
    result = run_smoke_restriction_engine(config)

    assert result["status"] == "SMOKE_NON_AUTHORITATIVE_R2_RESTRICTION_RESULT"
    assert result["authoritative"] is False
    assert {row["restriction"] for row in result["results"]} == {
        "ADD_RESTRICTION",
        "CBD_COMPLEMENT_RESTRICTION",
    }
    assert config["execution_boundary"] == {
        "authoritative_bootstrap_draws_frozen": False,
        "authoritative_evaluation_replicates_frozen": False,
        "authoritative_run_allowed": False,
        "human_n_frozen": False,
        "participant_recruitment_allowed": False,
        "runtime_f1b_change_allowed": False,
    }
