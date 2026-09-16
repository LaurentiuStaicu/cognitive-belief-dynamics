from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np
from jsonschema import Draft202012Validator

from cognitive_epistemic_model.calibration.m1_e4_participant_confirmation import (
    cell_seed,
    run_confirmation_cell,
    wilson_interval,
)

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "model/contracts/m1_e4_participant_confirmation.json"
SCHEMA = ROOT / "schemas/m1_e4_participant_confirmation.schema.json"
CONFIG = ROOT / "model/benchmarks/m1_e4_participant_confirmation_200.json"
SCREEN_RESULTS = (
    ROOT
    / "model/benchmarks/results/"
    / "m1_e4_participant_screening_authoritative_2026-09-16.csv"
)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def load_screening_rows() -> list[dict[str, str]]:
    with SCREEN_RESULTS.open(newline="") as handle:
        return list(csv.DictReader(handle))


def test_confirmation_contract_validates_against_schema():
    errors = sorted(
        Draft202012Validator(load_json(SCHEMA)).iter_errors(load_json(CONTRACT)),
        key=lambda error: list(error.path),
    )
    assert not errors, "\n".join(
        f"{'/'.join(map(str, error.path))}: {error.message}" for error in errors
    )


def test_confirmation_surface_is_frozen_at_29_cells():
    config = load_json(CONFIG)
    cells = config["selected_cells"]

    assert config["replicates_per_cell"] == 200
    assert config["recovery_threshold"] == 0.8
    assert config["selection_policy"]["selected_cells_total"] == 29
    assert len(cells) == 29
    assert len({cell["cell_id"] for cell in cells}) == 29

    primary = [cell for cell in cells if cell["role"] == "PRIMARY_P64_FULL_GRID"]
    boundary = [
        cell for cell in cells if cell["role"] == "BOUNDARY_MINIMUM_WITH_TIES"
    ]
    assert len(primary) == 18
    assert len(boundary) == 11
    assert {cell["allocation"] for cell in primary} == {"P64_X10"}


def test_primary_surface_contains_full_p64_stress_grid():
    config = load_json(CONFIG)
    primary = [
        cell
        for cell in config["selected_cells"]
        if cell["role"] == "PRIMARY_P64_FULL_GRID"
    ]

    keys = {
        (cell["heterogeneity"], cell["generator"], cell["regime"])
        for cell in primary
    }
    expected = {
        (heterogeneity, generator, regime)
        for heterogeneity in ("low", "moderate", "high")
        for generator in ("EVSD", "2HT")
        for regime in ("weak", "medium", "strong")
    }
    assert keys == expected


def test_boundary_surface_includes_all_minimum_ties_without_arbitrary_choice():
    config = load_json(CONFIG)
    rows = load_screening_rows()
    actual = {
        (
            cell["allocation"],
            cell["heterogeneity"],
            cell["generator"],
            cell["regime"],
        )
        for cell in config["selected_cells"]
        if cell["role"] == "BOUNDARY_MINIMUM_WITH_TIES"
    }

    expected = set()
    for allocation in ("P40_X16", "P80_X8", "P128_X5"):
        for generator in ("EVSD", "2HT"):
            candidates = [
                row
                for row in rows
                if row["allocation"] == allocation
                and row["generator"] == generator
            ]
            minimum = min(
                float(row["recovery_probability"]) for row in candidates
            )
            expected.update(
                (
                    row["allocation"],
                    row["heterogeneity"],
                    row["generator"],
                    row["regime"],
                )
                for row in candidates
                if float(row["recovery_probability"]) == minimum
            )

    assert actual == expected
    assert len(actual) == 11


def test_cell_seed_is_stable_and_cell_specific():
    a = cell_seed(20260916, "P64_X10__low__EVSD__weak")
    b = cell_seed(20260916, "P64_X10__low__EVSD__weak")
    c = cell_seed(20260916, "P64_X10__low__2HT__weak")

    assert a == b
    assert a != c
    assert 0 <= a <= 0xFFFFFFFF


def test_wilson_interval_matches_known_screening_examples():
    low_44, high_44 = wilson_interval(44, 50, 0.95)
    low_48, high_48 = wilson_interval(48, 50, 0.95)

    assert np.isclose(low_44, 0.761982, atol=1e-5)
    assert np.isclose(high_44, 0.943789, atol=1e-5)
    assert np.isclose(low_48, 0.865404, atol=1e-5)
    assert np.isclose(high_48, 0.988963, atol=1e-5)


def test_confirmation_runner_smoke_is_deterministic():
    confirmation = {
        "base_seed": 1234,
        "replicates_per_cell": 1,
        "recovery_threshold": 0.8,
        "quadrature_nodes": 3,
        "robustness_sensitivity": {"wilson_interval_level": 0.95},
    }
    screening = {
        "participant_allocations": [
            {
                "label": "SMALL",
                "participants": 6,
                "target_trials_per_participant_per_cell": 3,
                "foil_trials_per_participant_per_cell": 3,
                "total_responses_per_participant": 36,
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
            "EVSD": [
                {"label": "medium", "complex": 0.8, "simple": 1.0}
            ],
            "2HT": [
                {"label": "medium", "complex": 0.35, "simple": 0.45}
            ],
        },
    }
    cell = {
        "cell_id": "SMALL__low__EVSD__medium",
        "allocation": "SMALL",
        "heterogeneity": "low",
        "generator": "EVSD",
        "regime": "medium",
        "screening_recovery": 1.0,
        "role": "PRIMARY_P64_FULL_GRID",
    }

    first = run_confirmation_cell(
        confirmation_config=confirmation,
        screening_config=screening,
        selected_cell=cell,
    )
    second = run_confirmation_cell(
        confirmation_config=confirmation,
        screening_config=screening,
        selected_cell=cell,
    )

    assert first == second
    assert first["replicates"] == 1
    assert sum(first["selected"].values()) == 1


def test_phase_j_does_not_authorize_execution_before_phase_i_merge():
    contract = load_json(CONTRACT)
    assert contract["promotion_gate"][
        "confirmation_execution_allowed_before_phase_i_merge"
    ] is False
    assert contract["promotion_gate"]["human_protocol_design_allowed"] is False
    assert contract["promotion_gate"]["human_recruitment_allowed"] is False
    assert contract["scientific_boundaries"]["pencode_identified"] is False
    assert contract["scientific_boundaries"]["active_model_selected"] is False
