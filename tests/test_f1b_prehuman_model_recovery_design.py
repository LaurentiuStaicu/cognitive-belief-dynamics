from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "model" / "contracts" / "f1b_prehuman_model_recovery_contract.json"
SCHEMA = ROOT / "schemas" / "f1b_prehuman_model_recovery_contract.schema.json"
CONFIG = ROOT / "model" / "benchmarks" / "f1b_prehuman_model_recovery_design.json"
DOC = ROOT / "docs" / "F1B_PREHUMAN_MODEL_RECOVERY_DESIGN.md"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_f1b_prehuman_recovery_contract_validates_strict_schema() -> None:
    contract = load(CONTRACT)
    schema = load(SCHEMA)
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(contract)


def test_f1b_design_is_specification_only_and_pre_human() -> None:
    contract = load(CONTRACT)
    config = load(CONFIG)

    assert contract["status"] == "PROSPECTIVE_SYNTHETIC_MODEL_RECOVERY_DESIGN"
    assert contract["baseline"]["main_commit"] == "0e3423035c32f2285e7a430df69a6788de068fd5"
    assert contract["baseline"]["f1a_stage"] == "RECOVERY_TESTED"
    assert contract["scope"]["specification_only"] is True
    assert contract["scope"]["recovery_engine_allowed_in_this_change"] is False
    assert contract["scope"]["runtime_f1b_change_allowed"] is False
    assert contract["scope"]["m0_equation_change_allowed"] is False
    assert contract["scope"]["human_recruitment_allowed"] is False
    assert contract["scope"]["human_data_collection_allowed"] is False
    assert config["execution_boundary"]["recovery_engine_present"] is False
    assert config["execution_boundary"]["authoritative_run_allowed"] is False
    assert config["execution_boundary"]["human_n_frozen"] is False
    assert config["execution_boundary"]["human_recruitment_allowed"] is False
    assert config["execution_boundary"]["runtime_f1b_change_allowed"] is False


def test_r1_candidate_families_preserve_source_weighting_discrimination() -> None:
    contract = load(CONTRACT)
    r1 = contract["recovery_problems"]["R1"]
    candidates = {row["id"]: row for row in r1["candidate_families"]}

    assert set(candidates) == {"SR-A", "SR-B", "SR-C"}
    assert candidates["SR-A"]["source_weight_expression"] == "2*T-1"
    assert candidates["SR-B"]["source_weight_expression"] == "T"
    assert candidates["SR-C"]["tau_grid"] == [0.4, 0.5, 0.6]
    assert r1["synthetic_factor_grid"]["reliability_T"] == [0.2, 0.5, 0.8]
    assert min(r1["synthetic_factor_grid"]["reliability_T"]) < 0.5
    assert max(r1["synthetic_factor_grid"]["reliability_T"]) > 0.5
    assert any(x < 0 for x in r1["synthetic_factor_grid"]["signed_evidence_E"])
    assert any(x > 0 for x in r1["synthetic_factor_grid"]["signed_evidence_E"])


def test_r2_candidate_families_include_current_additive_and_flexible_models() -> None:
    contract = load(CONTRACT)
    r2 = contract["recovery_problems"]["R2"]
    candidates = {row["id"]: row for row in r2["candidate_families"]}

    assert set(candidates) == {"AP-A", "AP-B", "AP-C"}
    assert "(1-W)*R" in candidates["AP-A"]["expression"]
    assert "beta_r*R" in candidates["AP-B"]["expression"]
    assert "beta_ar*A*R" in candidates["AP-C"]["expression"]
    assert r2["synthetic_factor_grid"]["accuracy_cue_A"] == [0, 1]
    assert 0.0 in r2["synthetic_factor_grid"]["reward_context_R"]


def test_design_search_jointly_varies_participants_items_and_missingness() -> None:
    contract = load(CONTRACT)
    config = load(CONFIG)

    assert contract["design_search"]["status"] == "DESIGN_SEARCH_ONLY_NOT_HUMAN_N"
    assert contract["design_search"]["participant_count_grid"] == [96, 192, 384]
    assert contract["design_search"]["item_count_grid"] == [36, 72, 144]
    assert contract["design_search"]["missingness_rate_grid"] == [0.0, 0.1, 0.2]
    assert contract["design_search"]["human_sample_size_frozen"] is False
    assert contract["design_search"]["participant_item_joint_search_required"] is True
    assert config["design_search"]["search_axes_are_human_sample_recommendations"] is False


def test_recovery_rule_allows_inconclusive_and_keeps_wrong_probability_visible() -> None:
    contract = load(CONTRACT)
    config = load(CONFIG)

    assert contract["selection_rule"]["forced_winner_allowed"] is False
    assert "INCONCLUSIVE" in contract["selection_rule"]["decision"]
    assert contract["selection_rule"]["held_out_participant_generalization_required"] is True
    assert contract["selection_rule"]["held_out_item_generalization_required"] is True
    assert contract["recovery_gate"]["minimum_correct_model_recovery_probability_each_declared_core_cell"] == 0.8
    assert contract["recovery_gate"]["threshold_status"] == "CBD_SYNTHETIC_DESIGN_CONVENTION"
    assert contract["recovery_gate"]["wrong_model_probability_must_be_reported_separately"] is True
    assert contract["recovery_gate"]["authoritative_core_cells_not_yet_frozen"] is True
    assert config["selection"]["allow_inconclusive"] is True


def test_crossed_random_effects_and_provenance_are_required() -> None:
    contract = load(CONTRACT)

    crossed = contract["crossed_random_effects"]
    assert crossed["required"] is True
    assert crossed["participant_random_intercept"] is True
    assert crossed["item_random_intercept"] is True
    assert crossed["participant_random_slope_scenarios_required"] is True
    assert crossed["item_random_slope_scenarios_required"] is True

    provenance = contract["provenance_contract"]
    assert all(provenance.values())


def test_document_freezes_boundaries_without_runtime_promotion() -> None:
    text = DOC.read_text(encoding="utf-8")

    for token in (
        "PROSPECTIVE_SYNTHETIC_MODEL_RECOVERY_DESIGN",
        "SR-A",
        "SR-B",
        "SR-C",
        "AP-A",
        "AP-B",
        "AP-C",
        "INCONCLUSIVE",
        "CBD_SYNTHETIC_DESIGN_CONVENTION",
        "not human sample-size recommendations",
        "participant recruitment = NOT_AUTHORIZED",
    ):
        assert token in text

    assert "EncounterContext or DecisionOpportunity runtime objects" in text
