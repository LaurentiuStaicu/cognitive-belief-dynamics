from __future__ import annotations

import copy
import json
from pathlib import Path

import numpy as np
import pytest
from scipy.special import expit

from cognitive_epistemic_model.calibration.f1b_r2_controlled_departures import (
    cbd_utility,
    design_arrays,
)
from cognitive_epistemic_model.calibration.f1b_r2_distance_definition_review import (
    _bernoulli_kl_from_probability_and_logit,
    _cbd_utility_surface_coordinates,
    _project_candidate,
    _project_candidate_closure,
    _surface_metrics,
)

ROOT = Path(__file__).resolve().parents[1]
CONFIG = (
    ROOT
    / "model"
    / "benchmarks"
    / "f1b_r2_distance_definition_review.json"
)
DEPARTURES = (
    ROOT
    / "model"
    / "benchmarks"
    / "f1b_r2_controlled_departure_design.json"
)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_distance_review_contract_is_deterministic_and_non_authoritative() -> None:
    config = load(CONFIG)
    assert config["status"] == (
        "NON_AUTHORITATIVE_R2_DISTANCE_DEFINITION_REVIEW_DESIGN"
    )
    assert config["expected_case_count"] == 12
    assert config["expected_cells_per_case"] == 18
    assert config["design_weighting"] == {
        "type": "UNIFORM_OVER_FROZEN_CELLS",
        "weight_per_cell": pytest.approx(1.0 / 18.0),
    }
    assert config["diagnostic_domain_multipliers"] == [8, 16, 32]
    assert [row["id"] for row in config["candidates"]] == [
        "STABILIZED_UTILITY_RMS",
        "PROBABILITY_RMS",
        "BERNOULLI_KL_GENERAL_TO_CBD",
    ]
    assert config["local_information_metric"]["status"] == (
        "DIAGNOSTIC_ONLY_NOT_GLOBAL_CANDIDATE"
    )
    closure = config["closure_attainment_diagnostic"]
    assert closure["status"] == (
        "REQUIRED_FOR_DISTANCE_DEFINITION_COMPLETION"
    )
    assert closure["finite_logit_surface_coordinates"] == "W0,W1 in (0,1)"
    assert closure["closed_surface_coordinates"] == "W0,W1 in [0,1]"
    assert closure["bias_reward_domain_multipliers"] == [8, 16, 32]
    assert (
        config["numerical_integrity"]["closure_boundary_tolerance"]
        == pytest.approx(1e-8)
    )

    boundary = config["execution_boundary"]
    assert boundary["stochastic_simulation_allowed"] is False
    assert boundary["model_fitting_allowed"] is False
    assert boundary["bootstrap_allowed"] is False
    assert boundary["operational_fitter_bounds_change_allowed"] is False
    assert boundary["historical_departure_regeneration_allowed"] is False
    assert boundary["metric_selection_authorized"] is False
    assert boundary["human_n_frozen"] is False
    assert boundary["participant_recruitment_allowed"] is False
    assert boundary["runtime_f1b_change_allowed"] is False


def test_stable_bernoulli_kl_is_zero_on_same_probability_surface() -> None:
    logits = np.asarray([-8.0, -1.0, 0.0, 2.0, 9.0])
    probability = expit(logits)
    kl = _bernoulli_kl_from_probability_and_logit(
        probability,
        logits,
    )
    assert np.all(kl >= -1e-14)
    assert np.max(np.abs(kl)) < 1e-12


def test_stable_bernoulli_kl_matches_direct_formula_away_from_extremes() -> None:
    p = np.asarray([0.2, 0.4, 0.7, 0.85])
    q = np.asarray([0.3, 0.5, 0.6, 0.8])
    logits_q = np.log(q / (1.0 - q))
    stable = _bernoulli_kl_from_probability_and_logit(p, logits_q)
    direct = (
        p * np.log(p / q)
        + (1.0 - p)
        * np.log((1.0 - p) / (1.0 - q))
    )
    assert stable == pytest.approx(direct, abs=1e-13)


def test_surface_metrics_are_zero_when_surfaces_are_identical() -> None:
    eta = np.asarray([-2.0, -0.5, 0.0, 1.0, 3.0])
    metrics = _surface_metrics(
        eta_general=eta,
        eta_cbd=eta.copy(),
    )
    assert metrics["utility_rms_distance"] == pytest.approx(0.0, abs=1e-14)
    assert metrics["probability_rms_distance"] == pytest.approx(
        0.0,
        abs=1e-14,
    )
    assert metrics["mean_bernoulli_kl_general_to_cbd"] == pytest.approx(
        0.0,
        abs=1e-13,
    )
    assert metrics["information_weighted_logit_distance"] == pytest.approx(
        0.0,
        abs=1e-14,
    )


@pytest.mark.parametrize(
    "candidate_id",
    [
        "STABILIZED_UTILITY_RMS",
        "PROBABILITY_RMS",
        "BERNOULLI_KL_GENERAL_TO_CBD",
    ],
)
def test_each_candidate_recovers_zero_for_an_exact_cbd_surface(
    candidate_id: str,
) -> None:
    config = copy.deepcopy(load(CONFIG))
    config["diagnostic_domain_multipliers"] = [8]
    departure_config = load(DEPARTURES)
    design = departure_config["design_cells"]
    belief, accuracy, reward = design_arrays(
        tuple(float(x) for x in design["belief_B"]),
        tuple(float(x) for x in design["accuracy_cue_A"]),
        tuple(float(x) for x in design["reward_context_R"]),
    )

    exact_parameters = (-0.2, -0.2, 1.0, 0.8)
    eta = cbd_utility(
        exact_parameters,
        belief,
        accuracy,
        reward,
    )
    starts = [
        tuple(float(x) for x in row)
        for row in departure_config["cbd_projection"][
            "deterministic_starts"
        ]
    ]
    assert exact_parameters in starts

    result = _project_candidate(
        candidate_id=candidate_id,
        eta_general=eta,
        belief=belief,
        accuracy=accuracy,
        reward=reward,
        starts=starts,
        config=config,
        departure_config=departure_config,
    )
    selected = result["selected_widest_domain"]
    assert selected["objective"] < 1e-12
    assert selected["primary_distance"] < 1e-6
    assert selected["surface_metrics"]["utility_rms_distance"] < 1e-6
    assert selected["surface_metrics"]["probability_rms_distance"] < 1e-6
    assert (
        selected["surface_metrics"][
            "mean_bernoulli_kl_general_to_cbd"
        ]
        < 1e-10
    )


def test_review_cannot_select_metric_from_historical_detection() -> None:
    config = load(CONFIG)
    rules = config["comparison_rules"]
    assert rules["do_not_select_by_historical_detection"] is True
    assert rules["do_not_require_sign_symmetry"] is True
    assert config["execution_boundary"]["metric_selection_authorized"] is False



@pytest.mark.parametrize(
    "candidate_id",
    [
        "STABILIZED_UTILITY_RMS",
        "PROBABILITY_RMS",
        "BERNOULLI_KL_GENERAL_TO_CBD",
    ],
)
def test_closure_projection_recovers_finite_interior_cbd_surface(
    candidate_id: str,
) -> None:
    config = copy.deepcopy(load(CONFIG))
    config["diagnostic_domain_multipliers"] = [8]
    departure_config = load(DEPARTURES)
    design = departure_config["design_cells"]
    belief, accuracy, reward = design_arrays(
        tuple(float(x) for x in design["belief_B"]),
        tuple(float(x) for x in design["accuracy_cue_A"]),
        tuple(float(x) for x in design["reward_context_R"]),
    )
    exact_parameters = (-0.2, -0.2, 1.0, 0.8)
    eta = cbd_utility(
        exact_parameters,
        belief,
        accuracy,
        reward,
    )
    starts = [
        tuple(float(x) for x in row)
        for row in departure_config["cbd_projection"]["deterministic_starts"]
    ]
    result = _project_candidate_closure(
        candidate_id=candidate_id,
        eta_general=eta,
        belief=belief,
        accuracy=accuracy,
        reward=reward,
        logit_starts=starts,
        config=config,
        departure_config=departure_config,
    )
    selected = result["selected_widest_domain"]
    assert selected["objective"] < 1e-12
    assert result["attainment_status"] == "FINITE_INTERIOR_ATTAINED"
    assert result["closure_boundary_components"] == []


@pytest.mark.parametrize(
    "candidate_id",
    [
        "STABILIZED_UTILITY_RMS",
        "PROBABILITY_RMS",
        "BERNOULLI_KL_GENERAL_TO_CBD",
    ],
)
def test_closure_projection_identifies_nonattained_boundary_surface(
    candidate_id: str,
) -> None:
    config = copy.deepcopy(load(CONFIG))
    config["diagnostic_domain_multipliers"] = [8]
    departure_config = load(DEPARTURES)
    design = departure_config["design_cells"]
    belief, accuracy, reward = design_arrays(
        tuple(float(x) for x in design["belief_B"]),
        tuple(float(x) for x in design["accuracy_cue_A"]),
        tuple(float(x) for x in design["reward_context_R"]),
    )
    eta = _cbd_utility_surface_coordinates(
        (-0.2, 1.0, 0.7, 0.8),
        belief,
        accuracy,
        reward,
    )
    starts = [
        tuple(float(x) for x in row)
        for row in departure_config["cbd_projection"]["deterministic_starts"]
    ]
    result = _project_candidate_closure(
        candidate_id=candidate_id,
        eta_general=eta,
        belief=belief,
        accuracy=accuracy,
        reward=reward,
        logit_starts=starts,
        config=config,
        departure_config=departure_config,
    )
    selected = result["selected_widest_domain"]
    assert selected["objective"] < config["numerical_integrity"][
        "zero_surface_tolerance"
    ]
    assert result["attainment_status"] == "NON_ATTAINED_OR_CLOSURE_LIMIT"
    assert "W0=HIGH" in result["closure_boundary_components"]


def test_surface_coordinate_and_finite_logit_parameterizations_match() -> None:
    departure_config = load(DEPARTURES)
    design = departure_config["design_cells"]
    belief, accuracy, reward = design_arrays(
        tuple(float(x) for x in design["belief_B"]),
        tuple(float(x) for x in design["accuracy_cue_A"]),
        tuple(float(x) for x in design["reward_context_R"]),
    )
    logit_parameters = (-0.2, -0.4, 1.3, 0.9)
    w0 = float(expit(logit_parameters[1]))
    w1 = float(expit(logit_parameters[1] + logit_parameters[2]))
    assert _cbd_utility_surface_coordinates(
        (logit_parameters[0], w0, w1, logit_parameters[3]),
        belief,
        accuracy,
        reward,
    ) == pytest.approx(
        cbd_utility(
            logit_parameters,
            belief,
            accuracy,
            reward,
        ),
        abs=1e-14,
    )
