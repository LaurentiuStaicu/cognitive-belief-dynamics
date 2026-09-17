from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "model/contracts/m1_e4_discrimination_protocol.json"
SCHEMA = ROOT / "schemas/m1_e4_discrimination_protocol.schema.json"


def load_contract() -> dict:
    return json.loads(CONTRACT.read_text())


def test_discrimination_protocol_validates_against_schema():
    errors = sorted(
        Draft202012Validator(json.loads(SCHEMA.read_text())).iter_errors(load_contract()),
        key=lambda error: list(error.path),
    )
    assert not errors, "\n".join(
        f"{'/'.join(map(str, error.path))}: {error.message}" for error in errors
    )


def test_primary_route_requires_three_and_prefers_five_operating_points():
    contract = load_contract()
    primary = contract["primary_route"]
    rules = contract["operating_point_rules"]

    assert primary["type"] == "EXPERIMENTALLY_MANIPULATED_BINARY_BIAS_ROC"
    assert primary["minimum_operating_points_per_hsimp"] == 3
    assert primary["preferred_operating_points_per_hsimp"] >= 5
    assert rules["hard_minimum_non_degenerate_per_hsimp"] == 3
    assert rules["preferred_minimum_per_hsimp"] >= 5
    assert rules["degenerate_points_count_toward_minimum"] is False


def test_confidence_roc_is_supplemental_not_decisive():
    route = load_contract()["supplemental_route"]
    assert route["type"] == "CONFIDENCE_RATING_ROC"
    assert route["preferred_scale_points"] == 6
    assert route["nontrivial_cumulative_thresholds"] == 5
    assert route["sole_decisive_evidence_allowed"] is False
    assert route["raw_category_frequencies_required"] is True


def test_candidate_recovery_simulation_is_mandatory_and_symmetric():
    simulation = load_contract()["prospective_design_simulation"]
    assert simulation["required"] is True
    assert set(simulation["candidate_generators"]) == {
        "CANDIDATE.M1.E4.C1.EVSD",
        "CANDIDATE.M1.E4.C2.2HT",
    }
    assert simulation["minimum_core_candidate_recovery_probability"] == 0.8
    assert simulation["threshold_status"] == "CEM_DESIGN_CONVENTION"
    assert simulation["catastrophic_asymmetric_recovery_allowed"] is False


def test_dataset_schema_preserves_raw_sdt_counts():
    fields = set(load_contract()["dataset_schema"]["required_fields"])
    assert {
        "Ntarget",
        "Nfoil",
        "Nhit",
        "Nmiss",
        "Nfa",
        "Ncr",
        "hsimp",
        "bias_condition_id",
    }.issubset(fields)


def test_candidate_bias_invariance_is_explicit():
    invariance = load_contract()["fitting_protocol"]["candidate_invariance"]
    assert "share d" in invariance["EVSD"]
    assert "vary c" in invariance["EVSD"]
    assert "share Ddet" in invariance["2HT"]
    assert "vary g" in invariance["2HT"]


def test_no_single_metric_can_select_winner():
    contract = load_contract()
    assert contract["fitting_protocol"]["single_metric_winner_allowed"] is False
    assert contract["winner_rule"]["universal_delta_aic_cutoff"] is False
    assert contract["winner_rule"]["discordant_result"] == "INCONCLUSIVE_MODEL_DISCRIMINATION"


def test_pencode_remains_blocked():
    boundary = load_contract()["pencode_boundary"]
    assert boundary["status"] == "NOT_IDENTIFIED_AND_NOT_ACTIVE"
    assert boundary["model_selection_identifies_pencode"] is False


def test_phase_d_validation_patterns_are_not_active():
    contract = load_contract()
    planned = {item["id"] for item in contract["validation_contract"]["planned_patterns"]}
    active = {
        item["id"]
        for item in json.loads((ROOT / "model/validation_tests.json").read_text())
    }
    assert planned.isdisjoint(active)


def test_phase_d_forbids_registry_runtime_ui_and_release_changes():
    gate = load_contract()["promotion_gate"]
    assert gate["active_registry_mutation_allowed"] is False
    assert gate["runtime_model_selection_allowed"] is False
    assert gate["winner_declaration_allowed"] is False
    assert gate["ui_allowed"] is False

    assert not (ROOT / "src/cognitive_epistemic_model/recognition.py").exists()
    assert not (ROOT / "src/cognitive_epistemic_model/encoding.py").exists()
    assert not (ROOT / "web/src/recognition-stage.ts").exists()

    version = json.loads((ROOT / "web/public/model/version.json").read_text())
    snapshot = json.loads((ROOT / "model/evidence_snapshot.json").read_text())
    assert version["software_version"] == "0.4.3a0"
    assert version["release_tag"] == "v0.4.3a0"
    assert snapshot["id"] == "EVIDENCE.M1.2026-09-16.r1"
