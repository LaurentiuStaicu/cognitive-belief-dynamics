from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from cognitive_epistemic_model.calibration.f1b_r2_controlled_departures import (
    DepartureAxis,
    design_arrays,
    general_utility,
    project_general_to_add,
    project_general_to_cbd,
    solve_departure_case,
)
from cognitive_epistemic_model.calibration.f1b_r2_restriction_recovery import (
    cbd_fit_to_general_coefficients,
)

ROOT = Path(__file__).resolve().parents[1]
CONFIG = (
    ROOT
    / "model"
    / "benchmarks"
    / "f1b_r2_controlled_departure_design.json"
)


def load_config() -> dict:
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def arrays(config: dict) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    design = config["design_cells"]
    return design_arrays(
        tuple(design["belief_B"]),
        tuple(design["accuracy_cue_A"]),
        tuple(design["reward_context_R"]),
    )


def test_original_cbd_anchors_are_not_add_negative_controls() -> None:
    config = load_config()
    belief, accuracy, reward = arrays(config)

    for params in config["anchors"]["cbd"].values():
        beta = cbd_fit_to_general_coefficients(tuple(params))
        add = project_general_to_add(
            beta,
            belief=belief,
            accuracy=accuracy,
            reward=reward,
        )
        assert add.rms_distance > 1e-4


def test_intersection_anchors_are_exact_cbd_and_add_surfaces() -> None:
    config = load_config()
    belief, accuracy, reward = arrays(config)

    for params in config["anchors"]["cbd_add_intersection"].values():
        beta = cbd_fit_to_general_coefficients(tuple(params))
        cbd = project_general_to_cbd(
            beta,
            belief=belief,
            accuracy=accuracy,
            reward=reward,
            config=config,
        )
        add = project_general_to_add(
            beta,
            belief=belief,
            accuracy=accuracy,
            reward=reward,
        )
        assert cbd.rms_distance <= config["integrity_tolerances"]["anchor_cbd_rms"]
        assert add.rms_distance <= config["integrity_tolerances"]["add_compatibility_rms"]


def test_standalone_accuracy_departure_hits_target_and_preserves_add() -> None:
    config = load_config()
    params = tuple(
        config["anchors"]["cbd_add_intersection"][
            "CBD_ADD_INTERSECTION_ANCHOR_1"
        ]
    )
    for sign in (-1, 1):
        case = solve_departure_case(
            anchor_id="CBD_ADD_INTERSECTION_ANCHOR_1",
            anchor_parameters=params,
            axis=DepartureAxis.STANDALONE_ACCURACY_MAIN_EFFECT,
            sign=sign,
            target_distance=0.10,
            config=config,
        )
        assert case.cbd_distance_error <= 1e-6
        assert abs(case.achieved_cbd_rms_distance - 0.10) <= 1e-6
        assert case.add_compatibility_expected is True
        assert case.add_compatibility_pass is True
        assert case.nearest_add_rms_distance <= 1e-10


def test_complement_departure_hits_declared_cbd_distance() -> None:
    config = load_config()
    params = tuple(config["anchors"]["cbd"]["CBD_ANCHOR_1"])
    case = solve_departure_case(
        anchor_id="CBD_ANCHOR_1",
        anchor_parameters=params,
        axis=DepartureAxis.COMPLEMENT_RELATION_VIOLATION,
        sign=1,
        target_distance=0.10,
        config=config,
    )
    assert case.cbd_distance_error <= 1e-6
    assert abs(case.achieved_cbd_rms_distance - 0.10) <= 1e-6
    assert case.add_compatibility_expected is False


def test_departure_config_keeps_characterization_and_human_gates_closed() -> None:
    config = load_config()
    assert config["target_cbd_rms_distances"] == [0.10, 0.25, 0.50]
    assert config["departure_axes"] == [
        "STANDALONE_ACCURACY_MAIN_EFFECT",
        "COMPLEMENT_RELATION_VIOLATION",
        "COMBINED_VIOLATION",
    ]
    assert config["execution_boundary"] == {
        "bootstrap_characterization_run_allowed": False,
        "authoritative_bootstrap_draws_frozen": False,
        "authoritative_evaluation_replicates_frozen": False,
        "authoritative_core_grid_frozen": False,
        "human_n_frozen": False,
        "participant_recruitment_allowed": False,
        "runtime_f1b_change_allowed": False,
    }
