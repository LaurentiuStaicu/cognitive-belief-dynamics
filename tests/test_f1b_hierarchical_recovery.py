from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from cognitive_epistemic_model.calibration.f1b_hierarchical_recovery import (
    RandomEffectScales,
    fit_r1_hierarchical_candidate,
    fit_r2_hierarchical_candidate,
    select_r1_hierarchical_candidate,
    select_r2_hierarchical_candidate,
)
from cognitive_epistemic_model.calibration.f1b_prehuman_recovery import (
    R1Family,
    R2Family,
    simulate_r1_dataset,
    simulate_r2_dataset,
    split_crossed,
)

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "model" / "benchmarks" / "f1b_hierarchical_recovery_prototype.json"


def load_config() -> dict:
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def test_hierarchical_prototype_is_explicitly_non_authoritative() -> None:
    config = load_config()
    assert config["status"] == "NON_AUTHORITATIVE_PENALIZED_HIERARCHICAL_PROTOTYPE"
    assert config["inference_class"] == "PENALIZED_CONDITIONAL_MAP_PROTOTYPE"
    assert config["authoritative_marginal_likelihood_claim"] is False
    assert config["variance_scale_multipliers"] == [0.5, 1.0, 2.0]
    assert config["execution_boundary"] == {
        "authoritative_core_grid_allowed": False,
        "human_n_frozen": False,
        "participant_recruitment_allowed": False,
        "runtime_f1b_change_allowed": False,
    }


def test_r1_hierarchical_fit_keeps_unseen_group_effects_zero() -> None:
    cfg = load_config()
    r1 = cfg["R1"]
    rng = np.random.default_rng(100)
    data = simulate_r1_dataset(
        family=R1Family.SR_A,
        participants=12,
        items=12,
        reliability_levels=(0.2, 0.5, 0.8),
        evidence_levels=(-1.0, -0.5, 0.5, 1.0),
        intercept=0.0,
        evidence_scale=1.0,
        noise_sd=r1["residual_sd"],
        participant_intercept_sd=0.20,
        item_intercept_sd=0.20,
        participant_slope_sd=0.10,
        item_slope_sd=0.10,
        rng=rng,
    )
    split = split_crossed(data.participant, data.item)
    scales = RandomEffectScales(**r1["matched_scales"])
    fit = fit_r1_hierarchical_candidate(
        R1Family.SR_A,
        data,
        split.train,
        residual_sd=r1["residual_sd"],
        scales=scales,
        tau_grid=tuple(r1["tau_grid"]),
    )

    held_participants = np.unique(data.participant[split.held_out_participant])
    held_items = np.unique(data.item[split.held_out_item])
    assert np.allclose(fit.participant_intercepts[held_participants], 0.0)
    assert np.allclose(fit.participant_slopes[held_participants], 0.0)
    assert np.allclose(fit.item_intercepts[held_items], 0.0)
    assert np.allclose(fit.item_slopes[held_items], 0.0)


def test_r1_hierarchical_candidates_fit_same_crossed_surface() -> None:
    cfg = load_config()
    r1 = cfg["R1"]
    rng = np.random.default_rng(101)
    data = simulate_r1_dataset(
        family=R1Family.SR_B,
        participants=12,
        items=12,
        reliability_levels=(0.2, 0.5, 0.8),
        evidence_levels=(-1.0, -0.5, 0.5, 1.0),
        intercept=0.0,
        evidence_scale=1.0,
        noise_sd=r1["residual_sd"],
        participant_intercept_sd=0.20,
        item_intercept_sd=0.20,
        participant_slope_sd=0.10,
        item_slope_sd=0.10,
        rng=rng,
    )
    split = split_crossed(data.participant, data.item)
    scales = RandomEffectScales(**r1["matched_scales"])
    fits = {
        family: fit_r1_hierarchical_candidate(
            family,
            data,
            split.train,
            residual_sd=r1["residual_sd"],
            scales=scales,
            tau_grid=tuple(r1["tau_grid"]),
        )
        for family in (R1Family.SR_A, R1Family.SR_B, R1Family.SR_C)
    }
    assert select_r1_hierarchical_candidate(fits, data, split) in R1Family


def test_r2_hierarchical_fit_keeps_unseen_group_effects_zero() -> None:
    cfg = load_config()
    r2 = cfg["R2"]
    rng = np.random.default_rng(102)
    data = simulate_r2_dataset(
        family=R2Family.AP_A,
        participants=12,
        items=18,
        belief_levels=(0.2, 0.5, 0.8),
        accuracy_levels=(0.0, 1.0),
        reward_levels=(-1.0, 0.0, 1.0),
        parameters=(-0.2, 0.0, 1.2, 1.0),
        participant_intercept_sd=0.25,
        item_intercept_sd=0.20,
        participant_reward_slope_sd=0.10,
        item_reward_slope_sd=0.10,
        rng=rng,
    )
    split = split_crossed(data.participant, data.item)
    scales = RandomEffectScales(**r2["matched_scales"])
    fit = fit_r2_hierarchical_candidate(
        R2Family.AP_A,
        data,
        split.train,
        scales=scales,
    )

    held_participants = np.unique(data.participant[split.held_out_participant])
    held_items = np.unique(data.item[split.held_out_item])
    assert np.allclose(fit.participant_intercepts[held_participants], 0.0)
    assert np.allclose(fit.participant_reward_slopes[held_participants], 0.0)
    assert np.allclose(fit.item_intercepts[held_items], 0.0)
    assert np.allclose(fit.item_reward_slopes[held_items], 0.0)


def test_r2_hierarchical_candidates_fit_same_crossed_surface() -> None:
    cfg = load_config()
    r2 = cfg["R2"]
    rng = np.random.default_rng(103)
    data = simulate_r2_dataset(
        family=R2Family.AP_B,
        participants=12,
        items=18,
        belief_levels=(0.2, 0.5, 0.8),
        accuracy_levels=(0.0, 1.0),
        reward_levels=(-1.0, 0.0, 1.0),
        parameters=(-0.2, 0.9, 0.35, 0.65),
        participant_intercept_sd=0.25,
        item_intercept_sd=0.20,
        participant_reward_slope_sd=0.10,
        item_reward_slope_sd=0.10,
        rng=rng,
    )
    split = split_crossed(data.participant, data.item)
    scales = RandomEffectScales(**r2["matched_scales"])
    fits = {
        family: fit_r2_hierarchical_candidate(
            family,
            data,
            split.train,
            scales=scales,
        )
        for family in (R2Family.AP_A, R2Family.AP_B, R2Family.AP_C)
    }
    assert select_r2_hierarchical_candidate(fits, data, split) in R2Family
