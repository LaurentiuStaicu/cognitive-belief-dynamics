from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from cognitive_epistemic_model.calibration.f1b_prehuman_recovery import (
    R1Family,
    R2Family,
    fit_r1_candidate,
    fit_r2_candidate,
    run_smoke_benchmark,
    select_r1_candidate,
    select_r2_candidate,
    simulate_r1_dataset,
    simulate_r2_dataset,
    source_weight,
    split_crossed,
)

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "model" / "benchmarks" / "f1b_prehuman_model_recovery_smoke.json"


def load_config() -> dict:
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def test_source_weight_candidates_keep_anti_reliability_discount_and_gate_distinct() -> None:
    t = np.asarray([0.2, 0.5, 0.8])
    assert np.allclose(source_weight(R1Family.SR_A, t), [-0.6, 0.0, 0.6])
    assert np.allclose(source_weight(R1Family.SR_B, t), [0.2, 0.5, 0.8])
    assert np.allclose(
        source_weight(R1Family.SR_C, t, tau=0.5),
        [0.0, 1.0, 1.0],
    )


def test_r1_smoke_surface_has_crossed_holdouts_and_all_candidates_fit() -> None:
    cfg = load_config()
    r1 = cfg["R1"]
    rng = np.random.default_rng(10)
    data = simulate_r1_dataset(
        family=R1Family.SR_A,
        participants=12,
        items=12,
        reliability_levels=tuple(r1["reliability_T"]),
        evidence_levels=tuple(r1["signed_evidence_E"]),
        intercept=0.0,
        evidence_scale=1.0,
        noise_sd=0.4,
        participant_intercept_sd=0.1,
        item_intercept_sd=0.1,
        participant_slope_sd=0.05,
        item_slope_sd=0.05,
        rng=rng,
    )
    split = split_crossed(data.participant, data.item)
    assert split.train.any()
    assert split.held_out_participant.any()
    assert split.held_out_item.any()

    fits = {
        family: fit_r1_candidate(
            family,
            data,
            split.train,
            tau_grid=(0.4, 0.5, 0.6),
        )
        for family in (R1Family.SR_A, R1Family.SR_B, R1Family.SR_C)
    }
    choice = select_r1_candidate(fits, data, split)
    assert choice in R1Family


def test_r2_smoke_surface_is_binary_and_all_candidates_fit() -> None:
    cfg = load_config()
    r2 = cfg["R2"]
    rng = np.random.default_rng(11)
    data = simulate_r2_dataset(
        family=R2Family.AP_A,
        participants=12,
        items=18,
        belief_levels=tuple(r2["belief_B"]),
        accuracy_levels=tuple(r2["accuracy_cue_A"]),
        reward_levels=tuple(r2["reward_context_R"]),
        parameters=(-0.2, 0.0, 1.2, 1.0),
        participant_intercept_sd=0.1,
        item_intercept_sd=0.1,
        participant_reward_slope_sd=0.05,
        item_reward_slope_sd=0.05,
        rng=rng,
    )
    assert set(np.unique(data.share)).issubset({0, 1})
    split = split_crossed(data.participant, data.item)
    fits = {
        family: fit_r2_candidate(family, data, split.train)
        for family in (R2Family.AP_A, R2Family.AP_B, R2Family.AP_C)
    }
    choice = select_r2_candidate(fits, data, split)
    assert choice in R2Family


def test_smoke_benchmark_is_seed_reproducible_and_non_authoritative() -> None:
    config = load_config()
    first = run_smoke_benchmark(config)
    second = run_smoke_benchmark(config)

    assert first == second
    assert first["status"] == "SMOKE_NON_AUTHORITATIVE"
    assert first["authoritative"] is False

    for problem in ("R1", "R2"):
        rows = first[problem]["grid_results"]
        assert len(rows) == 3
        for row in rows:
            assert (
                row["recovery_probability"]
                + row["wrong_probability"]
                + row["inconclusive_probability"]
            ) == 1.0
            assert sum(row["selected"].values()) == row["replicates"]


def test_smoke_config_keeps_human_and_runtime_gates_closed() -> None:
    config = load_config()
    boundary = config["execution_boundary"]

    assert boundary == {
        "authoritative_run_allowed": False,
        "human_n_frozen": False,
        "participant_recruitment_allowed": False,
        "runtime_f1b_change_allowed": False,
    }
