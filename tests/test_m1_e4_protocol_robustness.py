from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from cognitive_epistemic_model.calibration.m1_e4_candidate_recovery import RecoveryFamily
from cognitive_epistemic_model.calibration.m1_e4_protocol_robustness import (
    phase_m_cell_seed,
    run_protocol_robustness_cell,
    simulate_protocol_stress_dataset,
    summarize_protocol_robustness_results,
    wilson_interval,
)

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "model/benchmarks/m1_e4_protocol_robustness_200.json"


def load_config() -> dict:
    return json.loads(CONFIG.read_text())


def profile(config: dict, profile_id: str) -> dict:
    return next(x for x in config["profiles"] if x["id"] == profile_id)


def test_phase_m_surface_is_frozen_to_nine_profiles_and_eighteen_cells():
    config = load_config()
    ids = [x["id"] for x in config["profiles"]]

    assert len(ids) == len(set(ids)) == 9
    assert config["generators"] == ["EVSD", "2HT"]
    assert config["selected_cells_total"] == 18
    assert config["replicates_per_cell"] == 200
    assert config["recovery_threshold"] == 0.8
    assert ids == [
        "REFERENCE",
        "ITEM_MODERATE",
        "ITEM_HIGH",
        "RHO_POSITIVE",
        "RHO_NEGATIVE",
        "SERIAL_DEGRADATION",
        "MAR_LIKE_ATTRITION",
        "LATENT_ASSOCIATED_ATTRITION",
        "COMBINED_ADVERSE",
    ]


def test_phase_m_design_stays_in_phase_k_limiting_region():
    config = load_config()
    assert config["allocation"] == {
        "label": "P64_X10",
        "generated_participants": 64,
        "target_trials_per_participant_per_cell": 10,
        "foil_trials_per_participant_per_cell": 10,
        "bias_operating_points": 5,
        "hsimp_conditions": 2,
    }
    assert config["participant_heterogeneity"] == {
        "label": "low",
        "sigma_memory": 0.1,
        "sigma_bias": 0.1,
    }
    assert config["weak_memory_truth"]["EVSD"] == {
        "complex": 0.45,
        "simple": 0.65,
    }
    assert config["weak_memory_truth"]["2HT"] == {
        "complex": 0.18,
        "simple": 0.28,
    }


def test_phase_m_cell_seeds_are_deterministic_and_unique():
    config = load_config()
    seeds = {
        phase_m_cell_seed(config["base_seed"], p["id"], generator)
        for p in config["profiles"]
        for generator in config["generators"]
    }
    assert len(seeds) == 18
    assert phase_m_cell_seed(20260917, "REFERENCE", "EVSD") == phase_m_cell_seed(
        20260917, "REFERENCE", "EVSD"
    )


def test_reference_generator_is_seed_reproducible():
    config = load_config()
    kwargs = dict(
        family=RecoveryFamily.EVSD,
        population_memory={"complex": 0.8, "simple": 1.0},
        population_biases=(-0.5, 0.0, 0.5),
        generated_participants=10,
        n_target_per_cell=5,
        n_foil_per_cell=5,
        sigma_memory=0.1,
        sigma_bias=0.1,
        profile=profile(config, "REFERENCE"),
    )
    first, first_diag = simulate_protocol_stress_dataset(
        **kwargs, rng=np.random.default_rng(77)
    )
    second, second_diag = simulate_protocol_stress_dataset(
        **kwargs, rng=np.random.default_rng(77)
    )

    assert np.array_equal(first.hits, second.hits)
    assert np.array_equal(first.false_alarms, second.false_alarms)
    assert first_diag == second_diag
    assert first.participants == 10
    assert first.operating_points == 3


def test_item_stress_changes_shared_item_realization_without_changing_shape():
    config = load_config()
    common = dict(
        family=RecoveryFamily.TWO_HT,
        population_memory={"complex": 0.35, "simple": 0.48},
        population_biases=(0.2, 0.5, 0.8),
        generated_participants=12,
        n_target_per_cell=6,
        n_foil_per_cell=6,
        sigma_memory=0.1,
        sigma_bias=0.1,
    )
    reference, _ = simulate_protocol_stress_dataset(
        **common,
        profile=profile(config, "REFERENCE"),
        rng=np.random.default_rng(101),
    )
    stressed, diagnostics = simulate_protocol_stress_dataset(
        **common,
        profile=profile(config, "ITEM_HIGH"),
        rng=np.random.default_rng(101),
    )

    assert reference.hits.shape == stressed.hits.shape == (12, 2, 3)
    assert diagnostics.item_memory_sd == 0.3
    assert diagnostics.item_bias_sd == 0.3
    assert not (
        np.array_equal(reference.hits, stressed.hits)
        and np.array_equal(reference.false_alarms, stressed.false_alarms)
    )


def test_attrition_profile_preserves_auditable_generated_and_retained_counts():
    config = load_config()
    stressed, diagnostics = simulate_protocol_stress_dataset(
        family=RecoveryFamily.EVSD,
        population_memory={"complex": 0.8, "simple": 1.0},
        population_biases=(-0.5, 0.0, 0.5),
        generated_participants=64,
        n_target_per_cell=4,
        n_foil_per_cell=4,
        sigma_memory=0.1,
        sigma_bias=0.1,
        profile=profile(config, "MAR_LIKE_ATTRITION"),
        rng=np.random.default_rng(20260917),
    )

    assert diagnostics.generated_participants == 64
    assert 2 <= diagnostics.retained_participants <= 64
    assert stressed.participants == diagnostics.retained_participants
    assert diagnostics.retention_fraction == diagnostics.retained_participants / 64
    assert diagnostics.attrition_type == "MAR_LIKE"


def test_phase_m_wilson_and_mc_precision_conventions_are_consistent():
    config = load_config()
    lower, upper = wilson_interval(160, 200)
    assert 0.0 < lower < 0.8 < upper < 1.0
    assert np.isclose(config["precision_sensitivity"]["mcse_max_at_200"], np.sqrt(0.25 / 200))
    assert np.isclose(
        config["precision_sensitivity"]["mcse_at_recovery_0_8"],
        np.sqrt(0.8 * 0.2 / 200),
    )
    assert config["precision_sensitivity"]["replaces_formal_gate"] is False


def _smoke_config() -> dict:
    return {
        "benchmark_id": "BENCH.M1.E4.PROTOCOL_ROBUSTNESS.SMOKE",
        "base_seed": 9,
        "replicates_per_cell": 1,
        "recovery_threshold": 0.8,
        "quadrature_nodes": 3,
        "allocation": {
            "label": "P12_X6",
            "generated_participants": 12,
            "target_trials_per_participant_per_cell": 6,
            "foil_trials_per_participant_per_cell": 6,
            "bias_operating_points": 3,
            "hsimp_conditions": 2,
        },
        "participant_heterogeneity": {
            "label": "smoke",
            "sigma_memory": 0.1,
            "sigma_bias": 0.1,
        },
        "bias_grids": {
            "EVSD": [-0.5, 0.0, 0.5],
            "2HT": [0.2, 0.5, 0.8],
        },
        "weak_memory_truth": {
            "EVSD": {"complex": 0.8, "simple": 1.1},
            "2HT": {"complex": 0.35, "simple": 0.5},
        },
        "profiles": [
            {
                "id": "REFERENCE",
                "item_memory_sd": 0.0,
                "item_bias_sd": 0.0,
                "participant_memory_bias_rho": 0.0,
                "serial_memory_slope": 0.0,
                "attrition": {"type": "NONE"},
            }
        ],
        "generators": ["EVSD", "2HT"],
    }


def test_phase_m_cell_runner_keeps_wrong_and_inconclusive_separate():
    result = run_protocol_robustness_cell(
        _smoke_config(), profile_id="REFERENCE", generator="EVSD"
    )
    assert result["replicates"] == 1
    assert sum(result["selected"].values()) == 1
    assert np.isclose(
        result["recovery_probability"]
        + result["wrong_probability"]
        + result["inconclusive_probability"],
        1.0,
    )
    assert result["profile_id"] == "REFERENCE"
    assert result["retention"]["generated_participants"] == 12


def test_phase_m_summary_requires_complete_frozen_surface():
    config = load_config()
    rows = []
    for p in config["profiles"]:
        for generator in config["generators"]:
            selected = {"EVSD": 0, "2HT": 0, "INCONCLUSIVE": 0}
            selected[generator] = 200
            rows.append(
                {
                    "cell_id": f"{p['id']}__{generator}",
                    "generator": generator,
                    "recovery_probability": 1.0,
                    "wilson_95": {"lower": 0.98, "upper": 1.0},
                    "passes_formal_gate": True,
                    "passes_secondary_wilson_sensitivity": True,
                    "selected": selected,
                }
            )
    summary = summarize_protocol_robustness_results(config, rows)
    assert summary["status"] == "PROTOCOL_ROBUSTNESS_PASS"
    assert summary["selected_cells_total"] == 18
    assert summary["formal_failed_cells"] == []


def test_phase_m_does_not_promote_m1_e4_or_change_scientific_boundary():
    snapshot = json.loads((ROOT / "model/evidence_snapshot.json").read_text())
    active_variables = (ROOT / "model/variables.json").read_text().lower()

    assert snapshot["model_specification"] == "M1"
    release_manifest = json.loads((ROOT / "releases/v0.1.1.manifest.json").read_text())
    evidence_revision = release_manifest["evidence_metadata_revision"]
    assert evidence_revision["prior_snapshot"] == "EVIDENCE.M1.2026-09-16.r1"
    assert evidence_revision["release_snapshot"] == snapshot["id"]
    assert evidence_revision["evidence_set_changed"] is False
    assert evidence_revision["metadata_corrected_or_qualified"] is True
    assert '"pencode"' not in active_variables
    assert not (ROOT / "web").exists()
