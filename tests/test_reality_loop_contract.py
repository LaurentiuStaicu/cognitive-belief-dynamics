from __future__ import annotations

from copy import deepcopy
from datetime import datetime
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, ValidationError


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas/reality_loop.schema.json"
CONTRACT = ROOT / "model/contracts/reality_loop_v1.json"
WORKSPACE_SCHEMA = ROOT / "schemas/workspace.schema.json"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def validator() -> Draft202012Validator:
    schema = load(SCHEMA)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def test_oa7_reality_loop_contract_validates_against_draft_2020_12_schema():
    validator().validate(load(CONTRACT))


def test_oa7_keeps_decision_object_types_structurally_distinct():
    contract = load(CONTRACT)
    sim = contract["simulation_results"][0]
    analysis = contract["decision_analyses"][0]
    plan = contract["implementation_plans"][0]
    observed = contract["observed_outcomes"][0]

    assert [sim["object_type"], analysis["object_type"], plan["object_type"], observed["object_type"]] == [
        "SimulationResult",
        "DecisionAnalysis",
        "ImplementationPlan",
        "ObservedOutcome",
    ]
    assert len({sim["id"], analysis["id"], plan["id"], observed["id"]}) == 4
    assert plan["decision_analysis_id"] == analysis["id"]
    assert observed["implementation_plan_id"] == plan["id"]


def test_oa7_real_world_plan_requires_population_context_and_outcome():
    contract = deepcopy(load(CONTRACT))
    plan = contract["implementation_plans"][0]
    assert plan["plan_scope"] == "REAL_WORLD"

    for field in ("population", "context", "primary_outcome"):
        broken = deepcopy(contract)
        del broken["implementation_plans"][0][field]
        with pytest.raises(ValidationError):
            validator().validate(broken)

def test_oa7_illustrative_plan_may_leave_unoperationalized_later_stage_indicators_empty():
    contract = deepcopy(load(CONTRACT))
    plan = contract["implementation_plans"][0]
    plan["plan_scope"] = "ILLUSTRATIVE"
    plan.pop("population", None)
    plan.pop("context", None)
    plan.pop("primary_outcome", None)
    plan["action_canvas"]["intermediate_result"]["indicator_ids"] = []
    plan["action_canvas"]["final_outcome"]["indicator_ids"] = []
    validator().validate(contract)


def test_oa7_real_world_plan_still_requires_operational_indicators_for_all_result_stages():
    contract = deepcopy(load(CONTRACT))
    for stage in ("proximal_result", "intermediate_result", "final_outcome"):
        broken = deepcopy(contract)
        broken["implementation_plans"][0]["action_canvas"][stage]["indicator_ids"] = []
        with pytest.raises(ValidationError):
            validator().validate(broken)



def test_oa7_action_canvas_and_adaptive_vocabulary_are_complete():
    contract = load(CONTRACT)
    plan = contract["implementation_plans"][0]
    assert list(plan["action_canvas"]) == [
        "problem",
        "target_mechanism",
        "intervention",
        "proximal_result",
        "intermediate_result",
        "final_outcome",
    ]
    assert {step["phase"] for step in plan["adaptive_plan"]} == {
        "NOW", "WATCH", "IF", "THEN", "STOP", "REASSESS"
    }

    indicator_ids = {item["id"] for item in contract["indicators"]}
    assert set(plan["indicator_ids"]) <= indicator_ids
    for key in ("proximal_result", "intermediate_result", "final_outcome"):
        assert set(plan["action_canvas"][key]["indicator_ids"]) <= indicator_ids


def test_oa7_observed_outcome_uses_observation_metadata_without_rewriting_prediction():
    contract = load(CONTRACT)
    plan = contract["implementation_plans"][0]
    observed = contract["observed_outcomes"][0]

    assert observed["prospective_snapshot_id"] == plan["prospective_snapshot"]["id"]
    assert plan["prospective_snapshot"]["revision_policy"] == "APPEND_ONLY_NO_RETROACTIVE_EDIT"
    assert observed["mutation_policy"] == "APPEND_ONLY_NO_RETROACTIVE_PREDICTION_EDIT"
    assert observed["retrospective"] is True

    for field in (
        "feature_of_interest",
        "observed_property",
        "procedure",
        "phenomenon_time",
        "result_time",
        "result",
    ):
        assert field in observed

    assert parse_time(observed["phenomenon_time"]) <= parse_time(observed["result_time"])
    assert parse_time(observed["result_time"]) <= parse_time(observed["recorded_at"])

    broken = deepcopy(contract)
    broken["observed_outcomes"][0]["revised_prediction"] = {"value": 1}
    with pytest.raises(ValidationError):
        validator().validate(broken)


def test_oa7_decision_autopsy_is_append_only_revision_proposal_not_backfill():
    contract = load(CONTRACT)
    autopsy = contract["decision_autopsies"][0]
    observed_ids = {item["id"] for item in contract["observed_outcomes"]}

    assert autopsy["prior_prediction_mutated"] is False
    assert set(autopsy["observed_outcome_ids"]) <= observed_ids
    assert autopsy["revision_proposals"]
    assert all(item["status"] in {"PROPOSED", "ACCEPTED", "REJECTED"} for item in autopsy["revision_proposals"])


def test_oa7_contract_does_not_silently_change_workspace_v1():
    contract = load(CONTRACT)
    workspace = load(WORKSPACE_SCHEMA)

    assert contract["storage_boundary"] == {
        "current_workspace_schema_version": "1",
        "integration_status": "RESERVED_NOT_IN_WORKSPACE_V1",
        "migration_required": True,
    }
    workspace_text = json.dumps(workspace)
    for reserved in (
        "SimulationResult",
        "DecisionAnalysis",
        "ImplementationPlan",
        "ObservedOutcome",
        "DecisionAutopsy",
    ):
        assert reserved not in workspace_text


def test_oa7_provenance_policy_is_append_only_and_observations_cannot_mutate_prospective_records():
    policy = load(CONTRACT)["provenance_policy"]
    assert policy == {
        "alignment": "W3C_PROV_INSPIRED",
        "revision_policy": "APPEND_ONLY",
        "observations_may_mutate_prospective": False,
        "observations_may_propose_revision": True,
    }


def test_oa7_contract_remains_product_metadata_not_scientific_promotion():
    contract = load(CONTRACT)
    sim = contract["simulation_results"][0]
    analysis = contract["decision_analyses"][0]

    assert contract["status"] == "PRE_EXECUTABLE_PRODUCT_CONTRACT"
    assert sim["epistemic_scope"] == "ILLUSTRATIVE_UNCALIBRATED"
    assert analysis["recommendation_status"] == "NOT_A_REAL_WORLD_RECOMMENDATION"
