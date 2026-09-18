from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "model/contracts/m1_e4_evidence_contract.json"
SCHEMA_PATH = ROOT / "schemas/m1_e4_evidence_contract.schema.json"


def load_contract() -> dict:
    return json.loads(CONTRACT_PATH.read_text())


def test_m1_e4_phase_a_contract_validates_against_schema():
    contract = load_contract()
    schema = json.loads(SCHEMA_PATH.read_text())
    errors = sorted(
        Draft202012Validator(schema).iter_errors(contract),
        key=lambda error: list(error.path),
    )
    assert not errors, "\n".join(
        f"{'/'.join(map(str, error.path))}: {error.message}" for error in errors
    )


def test_m1_e4_selects_recognition_sensitivity_not_attention_or_pencode():
    decision = load_contract()["construct_decision"]
    selected = decision["selected"]
    deferred = {item["short_name"]: item for item in decision["deferred"]}

    assert selected["short_name"] == "Drecog"
    assert selected["ontology_type"] == "DERIVED_METRIC"
    assert selected["decision"] == "SELECTED_FOR_NEXT_PHASE"

    assert deferred["Aattn"]["decision"] == "DEFERRED_NOT_REJECTED"
    assert deferred["Pencode"]["decision"] == "DEFERRED_NOT_REJECTED"


def test_m1_e4_conditions_on_preview_impression_not_access():
    stage = load_contract()["stage_decision"]
    assert stage["conditioning_event"] == "PreviewImpression"
    assert stage["requires_access"] is False


def test_m1_e4_freezes_hsimp_as_precomputed_binary_metadata():
    cue = load_contract()["cue_decision"]["selected"]

    assert cue["short_name"] == "Hsimp"
    assert cue["strategy"] == "PRECOMPUTED_CONTROLLED_STIMULUS_METADATA"
    assert cue["runtime_liwc_dependency"] is False
    assert cue["exact_replication_claim"] is False
    assert cue["reference_encoding"] == {
        "type": "BINARY",
        "control": 0,
        "treatment": 1,
        "control_label": "complex_control",
        "treatment_label": "simpler_headline",
    }


def test_m1_e4_primary_target_preserves_shulman_study3_values():
    target = load_contract()["empirical_target"]
    assert target["source_id"] == "SRC.M1.E4.SHULMAN_GENERAL.2024"
    assert target["design"]["n_recruited"] == 524
    assert target["design"]["n_probe_items"] == 24
    assert target["design"]["preregistered"] is True

    effects = {(item["metric"], item.get("condition")): item for item in target["effect_context"]}
    simple = effects[("DPRIME_MEAN", "simpler_headline")]
    complex_ = effects[("DPRIME_MEAN", "complex_headline")]
    t_stat = effects[("T_STATISTIC", None)]
    cohens_d = effects[("COHENS_D", None)]

    assert (simple["value"], simple["sd"]) == (1.23, 0.81)
    assert (complex_["value"], complex_["sd"]) == (0.8, 0.77)
    assert (t_stat["value"], t_stat["df"], t_stat["p_upper_bound"]) == (6.01, 483, 0.001)
    assert cohens_d["value"] == 0.55


def test_m1_e4_preserves_professional_writer_null_as_boundary():
    boundary = load_contract()["boundary_target"]
    assert boundary["source_id"] == "SRC.M1.E4.SHULMAN_PROFESSIONALS.2024"
    assert boundary["expected_interpretation"] == "NO_UNIVERSAL_SIMPLICITY_EFFECT"
    effect = boundary["effect_context"]
    assert effect == {
        "metric": "T_STATISTIC",
        "value": -0.44,
        "df": 165,
        "p_value": 0.66,
        "cohens_d": 0.07,
    }


def test_m1_e4_sources_have_unique_ids_and_independence_groups():
    sources = load_contract()["sources"]
    ids = [source["id"] for source in sources]
    assert len(ids) == len(set(ids))
    assert all(source["independence_group"] for source in sources)

    by_id = {source["id"]: source for source in sources}
    assert by_id["SRC.M1.E4.SHULMAN_GENERAL.2024"]["evidence_role"] == "PRIMARY_RECOGNITION_TARGET"
    assert by_id["SRC.M1.E4.SHULMAN_PROFESSIONALS.2024"]["evidence_role"] == "COUNTEREVIDENCE_BOUNDARY"
    assert by_id["SRC.M1.E4.MATTIS.2025"]["evidence_role"] == "INDEPENDENT_CONTEXT_BOUNDARY"
    assert (
        by_id["SRC.M1.E4.SHULMAN_GENERAL.2024"]["independence_group"]
        != by_id["SRC.M1.E4.SHULMAN_PROFESSIONALS.2024"]["independence_group"]
    )


def test_m1_e4_planned_objects_are_not_active():
    contract = load_contract()
    active_variables = json.loads((ROOT / "model/variables.json").read_text())
    active_validations = json.loads((ROOT / "model/validation_tests.json").read_text())
    active_targets = json.loads((ROOT / "model/empirical_targets.json").read_text())

    active_short_names = {item["short_name"] for item in active_variables}
    planned_short_names = {item["short_name"] for item in contract["planned_quantities"]}
    assert planned_short_names.isdisjoint(active_short_names)

    active_validation_ids = {item["id"] for item in active_validations}
    planned_validation_ids = {
        item["id"] for item in contract["validation_contract"]["planned_patterns"]
    }
    assert planned_validation_ids.isdisjoint(active_validation_ids)

    assert contract["empirical_target"]["id"] not in {item["id"] for item in active_targets}


def test_m1_e4_phase_a_forbids_runtime_and_ui():
    contract = load_contract()
    gate = contract["promotion_gate"]
    assert gate["active_registry_mutation_allowed"] is False
    assert gate["executable_equation_allowed"] is False
    assert not (ROOT / "web").exists()

    forbidden = set(contract["forbidden_changes"])
    assert "no_M1_E4_equation" in forbidden
    assert "no_Pencode_equation" in forbidden
    assert "no_attention_state" in forbidden
    assert "no_runtime_recognition_mechanism" in forbidden
    assert "no_UI_comparator" in forbidden

    assert not (ROOT / "src/cognitive_epistemic_model/recognition.py").exists()
    assert not (ROOT / "web/src/recognition-stage.ts").exists()
