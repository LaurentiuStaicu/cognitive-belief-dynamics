from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, ValidationError

from cognitive_epistemic_model.uncertainty import (
    InvalidProbabilityVectorError,
    ProbabilityUnavailableError,
    require_finite_scenario_probabilities,
)


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas/decision_uncertainty.schema.json"
REGISTRY = ROOT / "model/contracts/decision_uncertainty_v1.json"
INTERVENTIONS = ROOT / "web/public/model/interventions.json"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def uncertainty(registry: dict, uncertainty_id: str) -> dict:
    return next(item for item in registry["uncertainties"] if item["id"] == uncertainty_id)


def validator() -> Draft202012Validator:
    schema = load(SCHEMA)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def test_oa6a_registry_validates_against_draft_2020_12_schema():
    validator().validate(load(REGISTRY))


def test_oa6a_probability_policy_is_fail_closed_by_default():
    registry = load(REGISTRY)
    assert registry["probability_policy"] == {
        "finite_scenarios_default": "NOT_AVAILABLE",
        "infer_probabilities": False,
        "expected_value_requires_explicit_probabilities": True,
    }
    for item in registry["uncertainties"]:
        if item["probability_status"] == "NOT_AVAILABLE":
            assert "scenario_probabilities" not in item
            assert "probability_distribution" not in item


def test_response_profiles_match_existing_planner_without_probability_inference():
    registry = load(REGISTRY)
    interventions = load(INTERVENTIONS)
    item = uncertainty(registry, "UNC.PLANNER.RESPONSE.PROFILES")

    expected = [(profile["id"], profile["scale"]) for profile in interventions["profiles"]]
    observed = [(scenario["id"], scenario["value"]) for scenario in item["finite_scenarios"]]

    assert observed == expected == [("low", 0.7), ("reference", 1), ("high", 1.3)]
    assert item["role"] == "SCIENTIFIC_UNCERTAINTY"
    assert item["uncertainty_type"] == "PARAMETER"
    assert item["probability_status"] == "NOT_AVAILABLE"

    with pytest.raises(ProbabilityUnavailableError):
        require_finite_scenario_probabilities(item)


def test_decision_assumptions_are_not_scientific_parameters():
    registry = load(REGISTRY)
    objective = uncertainty(registry, "UNC.PLANNER.OBJECTIVE.WEIGHT")
    costs = uncertainty(registry, "UNC.PLANNER.EFFORT.COSTS")
    timing = uncertainty(registry, "UNC.PLANNER.ACTIVATION.TIMING")

    assert objective["role"] == costs["role"] == timing["role"] == "DECISION_ASSUMPTION"
    assert objective["uncertainty_type"] == "PREFERENCE"
    assert costs["uncertainty_type"] == "IMPLEMENTATION"
    assert timing["uncertainty_type"] == "SCENARIO"
    assert objective["bounded_range"] == {"minimum": 0, "maximum": 100, "unit": "percent"}
    assert costs["bounded_range"] == {
        "minimum": 1,
        "maximum": 20,
        "unit": "user_supplied_effort_units",
    }
    assert [scenario["value"] for scenario in timing["finite_scenarios"]] == [2, 5]


def test_structural_scope_uncertainty_remains_qualitative():
    item = uncertainty(load(REGISTRY), "UNC.PLANNER.STRUCTURAL.SCOPE")
    assert item["role"] == "SCIENTIFIC_UNCERTAINTY"
    assert item["uncertainty_type"] == "STRUCTURAL"
    assert item["quantification_status"] == "QUALITATIVE"
    assert item["probability_status"] == "NOT_AVAILABLE"
    assert "finite_scenarios" not in item
    assert "bounded_range" not in item


def test_schema_rejects_probabilities_attached_to_not_available_finite_scenarios():
    registry = deepcopy(load(REGISTRY))
    item = uncertainty(registry, "UNC.PLANNER.RESPONSE.PROFILES")
    item["scenario_probabilities"] = [1 / 3, 1 / 3, 1 / 3]

    with pytest.raises(ValidationError):
        validator().validate(registry)


def test_schema_requires_explicit_weights_when_finite_scenario_probability_status_is_declared():
    registry = deepcopy(load(REGISTRY))
    item = uncertainty(registry, "UNC.PLANNER.RESPONSE.PROFILES")
    item["probability_status"] = "USER_DECLARED"

    with pytest.raises(ValidationError):
        validator().validate(registry)


def test_probability_guard_accepts_only_explicit_normalized_weights():
    registry = deepcopy(load(REGISTRY))
    item = uncertainty(registry, "UNC.PLANNER.RESPONSE.PROFILES")
    item["probability_status"] = "USER_DECLARED"
    item["scenario_probabilities"] = [0.2, 0.5, 0.3]
    validator().validate(registry)
    assert require_finite_scenario_probabilities(item) == (0.2, 0.5, 0.3)

    item["scenario_probabilities"] = [0.2, 0.5, 0.4]
    with pytest.raises(InvalidProbabilityVectorError):
        require_finite_scenario_probabilities(item)
