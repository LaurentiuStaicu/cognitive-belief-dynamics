from __future__ import annotations

import json
from dataclasses import fields
from pathlib import Path

from jsonschema import Draft202012Validator

from cognitive_epistemic_model.endogenous import SchedulerTraceEntry, run_endogenous
from cognitive_epistemic_model.events import DecisionEvent
from cognitive_epistemic_model.network import StaticDirectedNetwork
from cognitive_epistemic_model.simulation import Simulator
from cognitive_epistemic_model.state import AgentState
from cognitive_epistemic_model.transmission import ForcedPassThroughPolicy

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "model" / "experiments" / "f1a_endogenous_transmission_experiment.json"
SCHEMA = ROOT / "schemas" / "f1a_endogenous_transmission_experiment.schema.json"


def test_f1a_contract_matches_strict_schema() -> None:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(contract)


def test_f1a_contract_preserves_v011_scientific_boundaries() -> None:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    assert contract["baseline"]["release"] == "v0.1.1"
    assert contract["baseline"]["commit"] == "9bc57322f7d2e1d53bf9c33e67f083e667a64569"
    assert contract["implementation_boundary"]["reuses_existing_simulator_step"] is True
    assert contract["implementation_boundary"]["public_api_export_allowed"] is False
    assert contract["promotion_gate"] == {
        "active_model_registration_allowed": False,
        "empirical_parameter_claim_allowed": False,
        "evidence_set_expansion_allowed": False,
        "canonical_paradigm_change_allowed": False,
        "next_status_candidate": "SYNTHETIC_EXECUTABLE",
    }


def test_f1a_protected_core_files_are_declared() -> None:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    protected = set(contract["implementation_boundary"]["protected_files"])
    assert protected == {
        "src/cognitive_epistemic_model/simulation.py",
        "src/cognitive_epistemic_model/events.py",
        "src/cognitive_epistemic_model/model.py",
        "src/cognitive_epistemic_model/updates.py",
    }


def test_f1a_odd_supplement_is_explicitly_synthetic() -> None:
    text = (ROOT / "docs" / "ODD_ENDOGENOUS_SCHEDULER.md").read_text(encoding="utf-8")
    for token in (
        "STRUCTURAL_SYNTHETIC_EXPERIMENT_ONLY",
        "abstract event time",
        "ForcedPassThroughPolicy",
        "does not reclassify CBD",
        "extreme synthetic software fixture",
    ):
        assert token in text


def test_f1a_trace_fields_match_machine_readable_contract() -> None:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    expected = set(contract["provenance_contract"]["required_fields"])
    actual = {field.name for field in fields(SchedulerTraceEntry)}
    assert actual == expected


def test_authoritative_f1a_fixture_executes_from_contract() -> None:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    fixture = contract["authoritative_fixture"]

    agents = {
        agent_id: AgentState(agent_id=agent_id)
        for agent_id in fixture["agents"]
    }
    agents["A"].sharing_bias = float(fixture["sender_sharing_bias"])

    simulator = Simulator(agents, seed=int(fixture["simulator_seed"]))
    network = StaticDirectedNetwork(
        nodes=tuple(fixture["agents"]),
        edges=(tuple(fixture["directed_edge"]),),
    )
    policy = ForcedPassThroughPolicy(delay=float(fixture["synthetic_delay"]))

    result = run_endogenous(
        simulator,
        [
            DecisionEvent(
                time=float(fixture["decision_time"]),
                agent_id="A",
                claim_id=fixture["claim_id"],
                source_id=fixture["source_id"],
                evidence_signal=0.0,
            )
        ],
        network=network,
        policy=policy,
    )

    assert [entry.event_type for entry in result.log] == [
        "DecisionEvent",
        "ExposureEvent",
    ]
    assert result.log[0].observation is not None
    assert result.log[0].observation["share"] is True
    assert result.log[1].agent_id == "B"
    assert agents["B"].f(fixture["claim_id"]) == simulator.params.alpha_f
