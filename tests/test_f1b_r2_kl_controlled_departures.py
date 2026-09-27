from __future__ import annotations

import json
from math import sqrt
from pathlib import Path

import numpy as np
from scipy.special import expit

import cognitive_epistemic_model.calibration.f1b_r2_kl_controlled_departures as klgen
from cognitive_epistemic_model.calibration.f1b_r2_controlled_departures import (
    DepartureAxis,
    departure_direction,
    design_arrays,
    project_general_to_add,
)
from cognitive_epistemic_model.calibration.f1b_r2_distance_definition_review import (
    project_general_surface_to_cbd_closure,
)
from cognitive_epistemic_model.calibration.f1b_r2_restriction_recovery import (
    cbd_fit_to_general_coefficients,
)

ROOT = Path(__file__).resolve().parents[1]
CONFIG = (
    ROOT
    / "model"
    / "benchmarks"
    / "f1b_r2_kl_controlled_departure_design_v1.json"
)
REVIEW = (
    ROOT
    / "model"
    / "benchmarks"
    / "f1b_r2_distance_definition_review.json"
)
HISTORICAL = (
    ROOT
    / "model"
    / "benchmarks"
    / "f1b_r2_controlled_departure_design.json"
)
DECISION = (
    ROOT
    / "model"
    / "benchmarks"
    / "f1b_r2_scientific_distance_definition_decision.json"
)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def design_arrays_from_config() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    design = load(CONFIG)["design_cells"]
    return design_arrays(
        tuple(float(x) for x in design["belief_B"]),
        tuple(float(x) for x in design["accuracy_cue_A"]),
        tuple(float(x) for x in design["reward_context_R"]),
    )


def test_kl_v1_contract_matches_scientific_distance_decision() -> None:
    config = load(CONFIG)
    decision = load(DECISION)
    selected = decision["selected_candidate"]

    assert config["design_id"] == "F1B.R2.KL_CONTROLLED_DEPARTURE.V1"
    assert config["issue"] == 178
    assert config["target_mean_bernoulli_kl"] == [0.001, 0.005, 0.01]
    assert config["expected_case_count"] == 36
    assert config["scientific_projection"]["candidate_id"] == (
        selected["candidate_id"]
    )
    assert config["scientific_projection"]["direction"] == (
        selected["direction"]
    )
    assert config["scientific_projection"][
        "restricted_set"
    ] == "CLOSURE_OF_CBD_RESPONSE_FAMILY"
    assert config["distance_solver"] == {
        "scan_step": 0.025,
        "max_scalar": 20.0,
        "xtol": 1e-10,
        "rtol": 1e-10,
        "maxiter": 200,
        "first_crossing_required": True,
    }


def test_kl_v1_boundary_remains_deterministic_only() -> None:
    boundary = load(CONFIG)["execution_boundary"]
    assert boundary == {
        "stochastic_simulation_allowed": False,
        "bootstrap_allowed": False,
        "operational_fitter_bounds_change_allowed": False,
        "historical_departure_rewrite_allowed": False,
        "paired_bootstrap_authorized": False,
        "authoritative_bootstrap_draws_frozen": False,
        "authoritative_evaluation_replicates_frozen": False,
        "authoritative_power_validated": False,
        "authoritative_core_grid_frozen": False,
        "human_n_frozen": False,
        "participant_recruitment_allowed": False,
        "runtime_f1b_change_allowed": False,
    }


def test_a_declared_cbd_anchor_has_zero_kl_to_scientific_closure() -> None:
    config = load(CONFIG)
    review = load(REVIEW)
    historical = load(HISTORICAL)
    belief, accuracy, reward = design_arrays_from_config()

    anchor = tuple(
        float(x)
        for x in config["anchors"]["cbd"]["CBD_ANCHOR_1"]
    )
    coefficients = tuple(
        float(x) for x in cbd_fit_to_general_coefficients(anchor)
    )
    starts = [
        tuple(float(x) for x in row)
        for row in historical["cbd_projection"]["deterministic_starts"]
    ]
    starts.append(anchor)

    projection = project_general_surface_to_cbd_closure(
        candidate_id="BERNOULLI_KL_GENERAL_TO_CBD",
        general_coefficients=coefficients,
        belief=belief,
        accuracy=accuracy,
        reward=reward,
        logit_starts=starts,
        review_config=review,
        departure_config=historical,
    )
    assert projection["attainment_status"] == "FINITE_INTERIOR_ATTAINED"
    assert projection["scientific_domain_components"] == []
    assert (
        projection["selected_widest_domain"]["primary_distance"]
        <= config["integrity_tolerances"]["anchor_mean_kl"]
    )


def test_structural_rays_are_preserved_but_strength_is_not_utility_rms() -> None:
    config = load(CONFIG)
    belief, accuracy, reward = design_arrays_from_config()

    standalone = departure_direction(
        DepartureAxis.STANDALONE_ACCURACY_MAIN_EFFECT,
        belief=belief,
        accuracy=accuracy,
        reward=reward,
    )
    complement = departure_direction(
        DepartureAxis.COMPLEMENT_RELATION_VIOLATION,
        belief=belief,
        accuracy=accuracy,
        reward=reward,
    )
    combined = departure_direction(
        DepartureAxis.COMBINED_VIOLATION,
        belief=belief,
        accuracy=accuracy,
        reward=reward,
    )

    assert standalone.shape == complement.shape == combined.shape == (6,)
    assert np.count_nonzero(standalone) == 1
    assert np.count_nonzero(complement) == 1

    for direction in (standalone, complement, combined):
        effect = (
            klgen.general_utility(
                direction,
                belief,
                accuracy,
                reward,
            )
        )
        assert abs(float(np.sqrt(np.mean(effect**2))) - 1.0) < 1e-12

    assert config["target_units"].startswith(
        "NATS_PER_BERNOULLI_OBSERVATION"
    )


def test_standalone_ray_remains_exactly_add_compatible() -> None:
    config = load(CONFIG)
    belief, accuracy, reward = design_arrays_from_config()
    anchor_parameters = tuple(
        float(x)
        for x in config["anchors"]["cbd_add_intersection"][
            "CBD_ADD_INTERSECTION_ANCHOR_1"
        ]
    )
    anchor = np.asarray(
        cbd_fit_to_general_coefficients(anchor_parameters),
        dtype=float,
    )
    direction = departure_direction(
        DepartureAxis.STANDALONE_ACCURACY_MAIN_EFFECT,
        belief=belief,
        accuracy=accuracy,
        reward=reward,
    )
    candidate = anchor + 0.75 * direction
    add = project_general_to_add(
        candidate,
        belief=belief,
        accuracy=accuracy,
        reward=reward,
    )
    assert add.rms_distance <= config["integrity_tolerances"][
        "add_compatibility_rms"
    ]


def test_first_crossing_solver_targets_kl_not_ray_length(monkeypatch) -> None:
    config = load(CONFIG)
    review = load(REVIEW)
    historical = load(HISTORICAL)
    anchor_parameters = tuple(
        float(x)
        for x in config["anchors"]["cbd_add_intersection"][
            "CBD_ADD_INTERSECTION_ANCHOR_1"
        ]
    )
    anchor_general = np.asarray(
        cbd_fit_to_general_coefficients(anchor_parameters),
        dtype=float,
    )
    w = float(expit(anchor_parameters[1]))
    surface = (
        float(anchor_parameters[0]),
        w,
        w,
        float(anchor_parameters[3]),
    )

    def fake_project(
        coefficients: np.ndarray,
        **kwargs,
    ) -> dict:
        candidate_id = kwargs.get(
            "candidate_id",
            "BERNOULLI_KL_GENERAL_TO_CBD",
        )
        beta_a = abs(float(np.asarray(coefficients)[2] - anchor_general[2]))
        scalar = beta_a / sqrt(2.0)
        primary = 0.01 * scalar * scalar
        if candidate_id == "STABILIZED_UTILITY_RMS":
            primary = scalar
        elif candidate_id == "PROBABILITY_RMS":
            primary = 0.1 * scalar
        return {
            "attainment_status": "FINITE_INTERIOR_ATTAINED",
            "closure_boundary_components": [],
            "scientific_domain_components": [],
            "selected_widest_domain": {
                "primary_distance": float(primary),
                "selected_surface_coordinates": list(surface),
            },
            "domain_results": [],
            "domain_transitions": [],
        }

    monkeypatch.setattr(klgen, "_project", fake_project)

    result = klgen.solve_kl_controlled_departure_case(
        anchor_id="CBD_ADD_INTERSECTION_ANCHOR_1",
        anchor_parameters=anchor_parameters,
        axis=DepartureAxis.STANDALONE_ACCURACY_MAIN_EFFECT,
        sign=1,
        target_mean_kl=0.001,
        config=config,
        review_config=review,
        historical_departure_config=historical,
    )

    assert result["requested_mean_bernoulli_kl"] == 0.001
    assert abs(result["achieved_mean_bernoulli_kl"] - 0.001) <= 1e-7
    assert result["mean_kl_error"] <= 1e-7
    assert result["first_crossing_bracket"] == (0.3, 0.325)
    assert result["add_compatibility_expected"] is True
    assert result["add_compatibility_pass"] is True
    assert result["scan_records"][0]["scalar"] == 0.0
    assert result["root_trace"]
