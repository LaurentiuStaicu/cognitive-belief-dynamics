from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

from cognitive_epistemic_model.calibration.f1a_transmission_recovery import (
    run_forced_pass_through_control,
    run_recovery_benchmark,
    run_recovery_replicate,
)

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "model" / "benchmarks" / "f1a_transmission_recovery_core.json"


def load_config() -> dict:
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def test_q_zero_and_q_one_controls_are_exact() -> None:
    common = dict(
        opportunities=20,
        delay=2.0,
        master_seed=20260921,
        replicate=0,
        decision_spacing=10.0,
        sender_sharing_bias=100.0,
    )
    zero = run_recovery_replicate(q_transmit=0.0, **common)
    one = run_recovery_replicate(q_transmit=1.0, **common)

    assert zero["realised_exposures"] == 0
    assert zero["q_hat"] == 0.0
    assert one["realised_exposures"] == 20
    assert one["q_hat"] == 1.0
    assert zero["delay_realization_error"] == 0.0
    assert one["delay_realization_error"] == 0.0
    assert zero["familiarity_consistency_error"] == 0.0
    assert one["familiarity_consistency_error"] == 0.0


def test_q_one_matches_existing_forced_pass_through_exposure_count() -> None:
    q_one = run_recovery_replicate(
        q_transmit=1.0,
        opportunities=12,
        delay=2.0,
        master_seed=91,
        replicate=0,
        decision_spacing=10.0,
        sender_sharing_bias=100.0,
    )
    forced = run_forced_pass_through_control(
        opportunities=12,
        delay=2.0,
        decision_spacing=10.0,
        sender_sharing_bias=100.0,
        simulator_seed=91,
    )
    assert q_one["realised_exposures"] == forced["realised_exposures"] == 12


def test_cell_addressed_rng_is_reproducible_and_order_independent() -> None:
    kwargs = dict(
        q_transmit=0.25,
        opportunities=50,
        delay=4.0,
        master_seed=20260921,
        replicate=7,
        decision_spacing=10.0,
        sender_sharing_bias=100.0,
    )
    first = run_recovery_replicate(**kwargs)

    run_recovery_replicate(
        q_transmit=0.9,
        opportunities=25,
        delay=1.0,
        master_seed=20260921,
        replicate=99,
        decision_spacing=10.0,
        sender_sharing_bias=100.0,
    )

    second = run_recovery_replicate(**kwargs)
    assert second == first


def test_delay_changes_timing_not_q_one_full_horizon_count() -> None:
    counts = []
    for delay in (1.0, 4.0):
        result = run_recovery_replicate(
            q_transmit=1.0,
            opportunities=15,
            delay=delay,
            master_seed=12,
            replicate=0,
            decision_spacing=10.0,
            sender_sharing_bias=100.0,
        )
        counts.append(result["realised_exposures"])
        assert result["delay_realization_error"] == 0.0
    assert counts == [15, 15]


def test_smoke_benchmark_is_same_seed_reproducible_and_non_authoritative() -> None:
    config = deepcopy(load_config())
    config["replicates_per_grid_cell"] = 4
    config["generator"]["grid"] = [0.25, 0.75]
    config["observation_design"]["core_opportunity_counts"] = [10]
    config["observation_design"]["stress_opportunity_counts"] = [5]
    config["observation_design"]["abstract_delays"] = [1.0]
    config["deterministic_controls"]["q_zero"]["opportunities"] = 8
    config["deterministic_controls"]["q_one"]["opportunities"] = 8
    config["deterministic_controls"]["q_one"]["required_exposures"] = 8

    first = run_recovery_benchmark(config, authoritative=False)
    second = run_recovery_benchmark(config, authoritative=False)

    assert first == second
    assert first["status"] == "SMOKE_NON_AUTHORITATIVE"
    assert first["authoritative"] is False
    assert first["promotion_candidate"] is False
    assert first["controls"]["all_controls_pass"] is True
    assert first["structural_checks"]["all_structural_checks_pass"] is True


def test_recovery_only_policy_is_not_imported_by_active_runtime_modules() -> None:
    for relative in (
        "src/cognitive_epistemic_model/transmission.py",
        "src/cognitive_epistemic_model/endogenous.py",
        "src/cognitive_epistemic_model/simulation.py",
        "src/cognitive_epistemic_model/__init__.py",
    ):
        text = (ROOT / relative).read_text(encoding="utf-8")
        assert "RecoveryBernoulliTransmissionPolicy" not in text
        assert "f1a_transmission_recovery" not in text
