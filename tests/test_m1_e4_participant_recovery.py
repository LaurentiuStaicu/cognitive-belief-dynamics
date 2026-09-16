from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from jsonschema import Draft202012Validator

from cognitive_epistemic_model.calibration.m1_e4_candidate_recovery import (
    RecoveryFamily,
)
from cognitive_epistemic_model.calibration.m1_e4_participant_recovery import (
    fit_hierarchical_candidate,
    run_participant_recovery_benchmark,
    select_hierarchical_candidate,
    simulate_participant_dataset,
)

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "model/contracts/m1_e4_participant_aware_recovery.json"
SCHEMA = ROOT / "schemas/m1_e4_participant_aware_recovery.schema.json"
CONFIG = ROOT / "model/benchmarks/m1_e4_participant_aware_screening.json"


def load_contract() -> dict:
    return json.loads(CONTRACT.read_text())


def load_config() -> dict:
    return json.loads(CONFIG.read_text())


def smoke_config() -> dict:
    return {
        "benchmark_id": "BENCH.M1.E4.PARTICIPANT_AWARE.SMOKE",
        "seed": 20260916,
        "replicates": 1,
        "recovery_threshold": 0.8,
        "quadrature_nodes": 3,
        "aggregate_target_per_cell": 24,
        "aggregate_foil_per_cell": 24,
        "participant_allocations": [
            {
                "label": "P6_X4",
                "participants": 6,
                "target_trials_per_participant_per_cell": 4,
                "foil_trials_per_participant_per_cell": 4,
                "total_responses_per_participant": 48,
            }
        ],
        "heterogeneity_regimes": [
            {"label": "low", "sigma_memory": 0.1, "sigma_bias": 0.1}
        ],
        "bias_grids": {
            "EVSD": [-0.5, 0.0, 0.5],
            "2HT": [0.2, 0.5, 0.8],
        },
        "memory_grids": {
            "EVSD": [{"label": "medium", "complex": 0.9, "simple": 1.1}],
            "2HT": [{"label": "medium", "complex": 0.38, "simple": 0.48}],
        },
    }


def test_participant_aware_contract_validates_against_schema():
    errors = sorted(
        Draft202012Validator(json.loads(SCHEMA.read_text())).iter_errors(load_contract()),
        key=lambda error: list(error.path),
    )
    assert not errors, "\n".join(
        f"{'/'.join(map(str, error.path))}: {error.message}" for error in errors
    )


def test_participant_allocations_preserve_640_anchor():
    config = load_config()
    assert config["aggregate_target_per_cell"] == 640
    assert config["aggregate_foil_per_cell"] == 640

    for allocation in config["participant_allocations"]:
        participants = allocation["participants"]
        assert (
            participants * allocation["target_trials_per_participant_per_cell"]
            == 640
        )
        assert (
            participants * allocation["foil_trials_per_participant_per_cell"]
            == 640
        )
        expected_total = (
            allocation["target_trials_per_participant_per_cell"]
            + allocation["foil_trials_per_participant_per_cell"]
        ) * 2 * 5
        assert allocation["total_responses_per_participant"] == expected_total


def test_participant_simulation_creates_shared_repeated_measure_structure():
    rng = np.random.default_rng(44)
    dataset = simulate_participant_dataset(
        family=RecoveryFamily.EVSD,
        population_memory={"complex": 0.9, "simple": 1.1},
        population_biases=(-0.5, 0.0, 0.5),
        participants=8,
        n_target_per_cell=5,
        n_foil_per_cell=5,
        sigma_memory=0.2,
        sigma_bias=0.2,
        rng=rng,
    )

    assert dataset.hits.shape == (8, 2, 3)
    assert dataset.false_alarms.shape == (8, 2, 3)
    assert dataset.participants == 8
    assert dataset.operating_points == 3


def test_hierarchical_candidates_fit_same_participant_level_data():
    rng = np.random.default_rng(123)
    train = simulate_participant_dataset(
        family=RecoveryFamily.EVSD,
        population_memory={"complex": 0.9, "simple": 1.1},
        population_biases=(-0.5, 0.0, 0.5),
        participants=8,
        n_target_per_cell=6,
        n_foil_per_cell=6,
        sigma_memory=0.12,
        sigma_bias=0.12,
        rng=rng,
    )
    held_out = simulate_participant_dataset(
        family=RecoveryFamily.EVSD,
        population_memory={"complex": 0.9, "simple": 1.1},
        population_biases=(-0.5, 0.0, 0.5),
        participants=8,
        n_target_per_cell=6,
        n_foil_per_cell=6,
        sigma_memory=0.12,
        sigma_bias=0.12,
        rng=rng,
    )

    evsd = fit_hierarchical_candidate(
        RecoveryFamily.EVSD, train, quadrature_nodes=3
    )
    two_ht = fit_hierarchical_candidate(
        RecoveryFamily.TWO_HT, train, quadrature_nodes=3
    )
    choice = select_hierarchical_candidate(
        evsd_fit=evsd,
        two_ht_fit=two_ht,
        held_out=held_out,
        quadrature_nodes=3,
    )

    assert np.isfinite(evsd.log_likelihood)
    assert np.isfinite(two_ht.log_likelihood)
    assert evsd.parameter_count == two_ht.parameter_count == 7
    assert choice in {
        RecoveryFamily.EVSD,
        RecoveryFamily.TWO_HT,
        RecoveryFamily.INCONCLUSIVE,
    }


def test_participant_aware_smoke_is_seed_reproducible():
    first = run_participant_recovery_benchmark(smoke_config())
    second = run_participant_recovery_benchmark(smoke_config())

    assert first == second
    assert len(first["grid_results"]) == 2
    assert set(first["confusion_counts"]) == {"EVSD", "2HT"}
    for generator in ("EVSD", "2HT"):
        assert set(first["confusion_counts"][generator]) == {
            "EVSD",
            "2HT",
            "INCONCLUSIVE",
        }


def test_screening_is_not_authorization_for_human_data_collection():
    contract = load_contract()
    config = load_config()

    assert config["replicates"] == 50
    assert config["confirmation_replicates"] == 200
    assert contract["staged_recovery"][
        "screening_is_authoritative_for_human_protocol"
    ] is False
    assert contract["staged_recovery"][
        "confirmation_required_before_human_protocol_design"
    ] is True
    assert contract["boundaries"]["human_data_collection_authorized"] is False
    assert contract["boundaries"]["pencode_identified"] is False

    version = json.loads((ROOT / "web/public/model/version.json").read_text())
    snapshot = json.loads((ROOT / "model/evidence_snapshot.json").read_text())
    assert version["software_version"] == "0.4.2a0"
    assert version["release_tag"] == "v0.4.2a0"
    assert snapshot["id"] == "EVIDENCE.M1.2026-09-16.r1"
