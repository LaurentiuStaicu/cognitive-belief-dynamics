from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

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
