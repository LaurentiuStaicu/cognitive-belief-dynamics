from __future__ import annotations

import json
from itertools import product
from pathlib import Path

import numpy as np
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = (
    ROOT
    / "model"
    / "experiments"
    / "f1b_r2_controlled_departure_characterization_contract.json"
)
SCHEMA = (
    ROOT
    / "schemas"
    / "f1b_r2_controlled_departure_characterization_contract.schema.json"
)
DESIGN = (
    ROOT
    / "model"
    / "benchmarks"
    / "f1b_r2_controlled_departure_characterization_design.json"
)
DOC = ROOT / "docs" / "F1B_R2_CONTROLLED_DEPARTURE_CHARACTERIZATION_DESIGN.md"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def utility_effect(direction: np.ndarray) -> np.ndarray:
    cells = np.asarray(
        list(product([0.2, 0.5, 0.8], [0.0, 1.0], [-1.0, 0.0, 1.0])),
        dtype=float,
    )
    B, A, R = cells[:, 0], cells[:, 1], cells[:, 2]
    centered = 2.0 * B - 1.0
    X = np.column_stack(
        (
            np.ones(cells.shape[0]),
            centered,
            A,
            R,
            A * centered,
            A * R,
        )
    )
    return X @ direction


def test_contract_validates_and_keeps_all_gates_closed() -> None:
    contract = load(CONTRACT)
    schema = load(SCHEMA)
    design = load(DESIGN)

    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(contract)

    assert contract["status"] == "PROSPECTIVE_CONTROLLED_DEPARTURE_CHARACTERIZATION_DESIGN"
    assert contract["scope"]["design_only"] is True
    assert contract["scope"]["projection_engine_allowed_in_this_change"] is False
    assert contract["scope"]["characterization_engine_allowed_in_this_change"] is False
    assert contract["scope"]["authoritative_run_allowed"] is False
    assert contract["scope"]["human_n_frozen"] is False
    assert contract["scope"]["participant_recruitment_allowed"] is False
    assert contract["scope"]["runtime_f1b_change_allowed"] is False

    assert design["projection_engine_present"] is False
    assert design["characterization_engine_present"] is False


def test_departure_grid_requires_both_signs_and_all_frozen_distances() -> None:
    contract = load(CONTRACT)
    departure = contract["departure_grid"]

    assert departure["axes"] == [
        "STANDALONE_ACCURACY_MAIN_EFFECT",
        "COMPLEMENT_RELATION_VIOLATION",
        "COMBINED_VIOLATION",
    ]
    assert departure["signs"] == [-1, 1]
    assert departure["target_rms_distances"] == [0.1, 0.25, 0.5]


def test_standalone_accuracy_direction_is_add_compatible() -> None:
    contract = load(CONTRACT)
    direction = np.asarray(
        contract["direction_normalization"]["standalone_accuracy_main_effect"],
        dtype=float,
    )
    # ADD permits b, beta_b, beta_a, beta_r and forbids only interactions.
    assert direction[4] == 0.0
    assert direction[5] == 0.0
    assert np.sqrt(np.mean(utility_effect(direction) ** 2)) > 0.0
    assert (
        contract["specificity_controls"][
            "add_rejection_on_standalone_accuracy_axis_counts_as_specificity_failure"
        ]
        is True
    )


def test_direction_normalization_inputs_are_nonzero_in_utility_space() -> None:
    contract = load(CONTRACT)
    for key in (
        "standalone_accuracy_main_effect",
        "complement_relation_violation",
    ):
        direction = np.asarray(contract["direction_normalization"][key], dtype=float)
        rms = float(np.sqrt(np.mean(utility_effect(direction) ** 2)))
        assert rms > 0.0


def test_projection_and_root_solver_are_fully_prospective() -> None:
    contract = load(CONTRACT)
    projection = contract["cbd_projection"]
    solver = contract["distance_solver"]

    assert projection["optimizer"] == "L-BFGS-B"
    assert projection["select_best_successful_start"] is True
    assert projection["failed_projection_is_design_generation_failure"] is True
    assert solver["scalar_step_bracket_grid"] == [
        0,
        0.125,
        0.25,
        0.5,
        1,
        2,
        4,
        8,
        16,
    ]
    assert solver["root_solver"] == "BRENTQ"
    assert solver["achieved_distance_absolute_tolerance"] == 1e-6
    assert solver["no_bracket_is_design_generation_failure"] is True


def test_bootstrap_search_is_non_authoritative_and_independent() -> None:
    contract = load(CONTRACT)
    bootstrap = contract["bootstrap_characterization"]

    assert bootstrap["method"] == "PARAMETRIC_BOOTSTRAP"
    assert bootstrap["chi_square_reference_assumed"] is False
    assert bootstrap["bootstrap_draw_grid"] == [49, 99, 199]
    assert bootstrap["calibration_and_evaluation_streams_independent"] is True
    assert bootstrap["authoritative_bootstrap_draws_frozen"] is False
    assert bootstrap["authoritative_evaluation_replicates_frozen"] is False


def test_document_preserves_restriction_testing_boundary() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "No unique winner is required" in text
    assert "Failure to reject is not proof" in text
    assert "participant recruitment = NOT AUTHORIZED" in text
    assert "runtime F1b = NOT AUTHORIZED" in text
