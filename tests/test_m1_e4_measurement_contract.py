from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "model/contracts/m1_e4_measurement_contract.json"
SCHEMA_PATH = ROOT / "schemas/m1_e4_measurement_contract.schema.json"


def load_contract() -> dict:
    return json.loads(CONTRACT_PATH.read_text())


def test_m1_e4_measurement_contract_validates_against_schema():
    contract = load_contract()
    schema = json.loads(SCHEMA_PATH.read_text())
    errors = sorted(
        Draft202012Validator(schema).iter_errors(contract),
        key=lambda error: list(error.path),
    )
    assert not errors, "\n".join(
        f"{'/'.join(map(str, error.path))}: {error.message}" for error in errors
    )


def test_m1_e4_measurement_uses_standard_sdt_contingency_cells():
    cells = load_contract()["raw_cells"]
    by_name = {cell["short_name"]: cell["standard_sdt_role"] for cell in cells}
    assert by_name == {
        "Nhit": "HIT",
        "Nmiss": "MISS",
        "Nfa": "FALSE_ALARM",
        "Ncr": "CORRECT_REJECTION",
    }


def test_m1_e4_measurement_does_not_invent_probe_split():
    task = load_contract()["source_task"]
    assert task["reported_probe_count"] == 24
    assert task["target_foil_split_known_from_main_text"] is False


def test_m1_e4_measurement_freezes_reference_sdt_estimator():
    estimator = load_contract()["reference_estimator"]
    assert estimator["family"] == "EQUAL_VARIANCE_GAUSSIAN_YES_NO_SDT"
    assert estimator["inverse_cdf"] == "STANDARD_NORMAL"
    assert estimator["drecog_formula"] == "Phi^-1(Hstar) - Phi^-1(Fstar)"
    assert estimator["crecog_formula"] == "-0.5 * (Phi^-1(Hstar) + Phi^-1(Fstar))"

    correction = estimator["extreme_rate_correction"]
    assert correction["method"] == "HAUTUS_LOG_LINEAR"
    assert correction["apply_to_all_cells"] is True
    assert correction["corrected_hit_rate"] == "(Nhit + 0.5) / (Nhit + Nmiss + 1)"
    assert correction["corrected_false_alarm_rate"] == "(Nfa + 0.5) / (Nfa + Ncr + 1)"
    assert correction["source_exact_replication_claim"] is False


def test_m1_e4_measurement_separates_sensitivity_and_criterion():
    quantities = {item["short_name"]: item for item in load_contract()["measurement_quantities"]}
    assert quantities["Drecog"]["role"] == "PRIMARY_VALIDATION_METRIC"
    assert quantities["Crecog"]["role"] == "AUXILIARY_RESPONSE_CRITERION_DIAGNOSTIC"
    assert quantities["Drecog"]["status"] == "MEASUREMENT_ONLY"
    assert quantities["Crecog"]["status"] == "MEASUREMENT_ONLY"


def test_m1_e4_measurement_blocks_pencode_identification():
    ident = load_contract()["identifiability"]
    assert ident["pencode"]["status"] == "NOT_IDENTIFIED_BY_CURRENT_MEASUREMENT"
    assert "event-level Pencode" in ident["drecog_alone_does_not_identify"]
    assert set(ident["pencode"]["forbidden_shortcuts"]) == {
        "logistic(Drecog)",
        "Phi(Drecog)",
        "Drecog / constant",
        "condition_mean_dprime_as_item_probability",
    }


def test_m1_e4_measurement_reference_inverse_requires_criterion():
    inverse = load_contract()["identifiability"]["drecog_plus_crecog_reference_inverse"]
    assert inverse["z_hit"] == "Drecog / 2 - Crecog"
    assert inverse["z_false_alarm"] == "-Drecog / 2 - Crecog"


def test_m1_e4_msep_is_measurement_model_only():
    quantities = {item["short_name"]: item for item in load_contract()["measurement_quantities"]}
    msep = quantities["Msep"]
    assert msep["role"] == "REFERENCE_MEASUREMENT_MODEL_BRIDGE"
    assert msep["status"] == "MEASUREMENT_MODEL_ONLY"
    assert msep["reference_identity"] == "Msep = Drecog"


def test_m1_e4_equal_variance_is_bounded_assumption():
    boundary = load_contract()["model_assumption_boundary"]
    assert boundary["equal_variance_status"] == "REFERENCE_MEASUREMENT_ASSUMPTION_ONLY"
    assert boundary["single_operating_point_sufficient_for_richer_model"] is False


def test_m1_e4_measurement_validation_patterns_are_not_active():
    contract = load_contract()
    active = json.loads((ROOT / "model/validation_tests.json").read_text())
    active_ids = {item["id"] for item in active}
    planned_ids = {
        item["id"]
        for item in contract["validation_contract"]["planned_patterns"]
    }
    assert planned_ids.isdisjoint(active_ids)


def test_m1_e4_measurement_quantities_are_not_active_variables():
    contract = load_contract()
    active = json.loads((ROOT / "model/variables.json").read_text())
    active_short_names = {item["short_name"] for item in active}
    measurement_names = {item["short_name"] for item in contract["measurement_quantities"]}
    assert measurement_names.isdisjoint(active_short_names)
    assert "Pencode" not in active_short_names


def test_m1_e4_phase_b_forbids_runtime_ui_and_release_mutation():
    contract = load_contract()
    gate = contract["promotion_gate"]
    assert gate["active_registry_mutation_allowed"] is False
    assert gate["executable_cognitive_equation_allowed"] is False
    assert gate["measurement_formula_documentation_allowed"] is True
    assert gate["ui_allowed"] is False

    assert not (ROOT / "src/cognitive_epistemic_model/recognition.py").exists()
    assert not (ROOT / "src/cognitive_epistemic_model/encoding.py").exists()
    assert not (ROOT / "web/src/recognition-stage.ts").exists()

    snapshot = json.loads((ROOT / "model/evidence_snapshot.json").read_text())
    assert snapshot["id"] == "EVIDENCE.M1.2026-09-16.r1"
