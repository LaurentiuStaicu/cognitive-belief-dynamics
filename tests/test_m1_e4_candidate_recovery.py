from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import numpy as np
from jsonschema import Draft202012Validator
from scipy.optimize import minimize as scipy_minimize

import cognitive_epistemic_model.calibration.m1_e4_candidate_recovery as candidate_recovery

from cognitive_epistemic_model.calibration.m1_e4_candidate_recovery import (
    RecognitionCounts,
    RecoveryFamily,
    evsd_probabilities,
    fit_candidate,
    run_recovery_benchmark,
    simulate_dataset,
    two_ht_probabilities,
)

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "model/contracts/m1_e4_candidate_recovery_benchmark.json"
SCHEMA = ROOT / "schemas/m1_e4_candidate_recovery_benchmark.schema.json"
CONFIG = ROOT / "model/benchmarks/m1_e4_candidate_recovery_core.json"


def load_contract() -> dict:
    return json.loads(CONTRACT.read_text())


def load_config() -> dict:
    return json.loads(CONFIG.read_text())


def smoke_config() -> dict:
    return {
        "benchmark_id": "BENCH.M1.E4.CANDIDATE_RECOVERY.SMOKE",
        "seed": 12345,
        "replicates": 2,
        "recovery_threshold": 0.8,
        "trial_counts_per_operating_point": [30],
        "bias_grids": {
            "EVSD": [-0.6, 0.0, 0.6],
            "2HT": [0.2, 0.5, 0.8],
        },
        "memory_grids": {
            "EVSD": [
                {"label": "medium", "complex": 0.8, "simple": 1.0}
            ],
            "2HT": [
                {"label": "medium", "complex": 0.35, "simple": 0.45}
            ],
        },
    }


def test_candidate_recovery_contract_validates_against_schema():
    errors = sorted(
        Draft202012Validator(json.loads(SCHEMA.read_text())).iter_errors(load_contract()),
        key=lambda error: list(error.path),
    )
    assert not errors, "\n".join(
        f"{'/'.join(map(str, error.path))}: {error.message}" for error in errors
    )


def test_core_config_matches_frozen_protocol():
    contract = load_contract()
    config = load_config()

    assert config["seed"] == contract["simulation_design"]["seed"]
    assert config["replicates"] == contract["simulation_design"]["replicates_per_grid_cell"]
    assert config["recovery_threshold"] == contract["design_gate"]["minimum_recovery_probability_each_core_grid_cell"]
    assert config["trial_counts_per_operating_point"] == [40, 80, 160, 320]
    assert len(config["bias_grids"]["EVSD"]) == 5
    assert len(config["bias_grids"]["2HT"]) == 5
    assert {row["label"] for row in config["memory_grids"]["EVSD"]} == {"weak", "medium", "strong"}
    assert {row["label"] for row in config["memory_grids"]["2HT"]} == {"weak", "medium", "strong"}


def test_candidate_probability_functions_respect_model_constraints():
    h_e, f_e = evsd_probabilities(1.0, 0.2)
    h_t, f_t = two_ht_probabilities(0.4, 0.3)

    assert 0.0 < f_e < h_e < 1.0
    assert 0.0 <= f_t < h_t <= 1.0
    assert np.isclose(h_t - f_t, 0.4)


def test_two_ht_fit_retries_exact_phase_j_replication_111_surface(monkeypatch):
    points = (
        RecognitionCounts(640, 640, 467, 37),
        RecognitionCounts(640, 640, 494, 69),
        RecognitionCounts(640, 640, 534, 106),
        RecognitionCounts(640, 640, 571, 143),
        RecognitionCounts(640, 640, 605, 165),
    )
    calls: list[dict | None] = []

    def controlled_minimize(*args, **kwargs):
        calls.append(kwargs.get("options"))
        if len(calls) == 1:
            return SimpleNamespace(success=False, message="ABNORMAL")
        return scipy_minimize(*args, **kwargs)

    monkeypatch.setattr(candidate_recovery, "minimize", controlled_minimize)

    fit = candidate_recovery.fit_two_ht_condition(points)

    assert calls == [None, {"maxls": 100}]
    assert np.isclose(fit.log_likelihood, -31.276238797970336, rtol=1e-10, atol=1e-8)
    assert np.isclose(fit.memory, 0.6723864052458528, rtol=1e-8, atol=1e-8)
    assert np.allclose(
        fit.biases,
        (
            0.17612793696506446,
            0.3201504368954919,
            0.4999999934348496,
            0.6748664513277185,
            0.8230582278270012,
        ),
        rtol=1e-8,
        atol=1e-8,
    )


def test_both_candidate_families_fit_same_dataset_surface():
    rng = np.random.default_rng(17)
    dataset = simulate_dataset(
        family=RecoveryFamily.EVSD,
        memory_by_condition={"complex": 0.8, "simple": 1.0},
        biases=(-0.6, 0.0, 0.6),
        n_target=80,
        n_foil=80,
        rng=rng,
    )

    evsd = fit_candidate(RecoveryFamily.EVSD, dataset)
    two_ht = fit_candidate(RecoveryFamily.TWO_HT, dataset)

    assert np.isfinite(evsd.log_likelihood)
    assert np.isfinite(two_ht.log_likelihood)
    assert evsd.parameter_count == two_ht.parameter_count == 8
    assert set(evsd.conditions) == {"complex", "simple"}
    assert set(two_ht.conditions) == {"complex", "simple"}


def test_smoke_benchmark_is_seed_reproducible_and_has_confusion_matrix():
    first = run_recovery_benchmark(smoke_config())
    second = run_recovery_benchmark(smoke_config())

    assert first == second
    assert set(first["confusion_counts"]) == {"EVSD", "2HT"}

    for generator in ("EVSD", "2HT"):
        assert set(first["confusion_counts"][generator]) == {
            "EVSD",
            "2HT",
            "INCONCLUSIVE",
        }
        assert sum(first["confusion_counts"][generator].values()) == 2

    assert len(first["grid_results"]) == 2
    for row in first["grid_results"]:
        assert sum(row["selected"].values()) == row["replicates"]
        assert np.isclose(
            row["recovery_probability"]
            + row["wrong_probability"]
            + row["inconclusive_probability"],
            1.0,
        )
        assert row["passes_recovery_threshold"] == (
            row["recovery_probability"] >= first["recovery_threshold"]
        )


def test_benchmark_does_not_turn_model_recovery_into_empirical_winner_claim():
    contract = load_contract()
    assert contract["promotion_gate"]["active_model_registration_allowed"] is False
    assert contract["promotion_gate"]["winner_declaration_allowed"] is False
    assert contract["promotion_gate"]["pencode_allowed"] is False
    assert contract["promotion_gate"]["ui_allowed"] is False
    assert contract["design_gate"]["ci_smoke_run_is_authoritative"] is False

    version = json.loads((ROOT / "web/public/model/version.json").read_text())
    snapshot = json.loads((ROOT / "model/evidence_snapshot.json").read_text())
    assert version["software_version"] == "0.4.2a0"
    assert version["release_tag"] == "v0.4.2a0"
    assert snapshot["id"] == "EVIDENCE.M1.2026-09-16.r1"
