from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "model" / "experiments" / "f1a_somar_public_codebook_audit.json"
SCHEMA = ROOT / "schemas" / "f1a_somar_public_codebook_audit.schema.json"
DOC = ROOT / "docs" / "F1A_SOMAR_PUBLIC_CODEBOOK_AUDIT.md"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_somar_public_codebook_audit_matches_schema() -> None:
    contract = load(CONTRACT)
    schema = load(SCHEMA)
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(contract)


def test_public_codebook_audit_does_not_authorize_calculation_or_promotion() -> None:
    audit = load(CONTRACT)
    assert audit["current_stage"] == "RECOVERY_TESTED"
    assert audit["empirical_promotion_authorized"] is False
    assert audit["numerical_pairing_authorized"] is False
    assert audit["candidate_component_quantity"]["status"] == "NOT_AUTHORIZED_FOR_CALCULATION"
    assert audit["candidate_component_quantity"]["equivalent_to_q_transmit"] is False


def test_confirmed_pairing_surface_is_url_owner_period_population_aligned() -> None:
    confirmed = load(CONTRACT)["confirmed_compatibility"]
    assert confirmed["unit_level"] == "URL"
    assert confirmed["owner_type_rows"] == ["user", "Page", "group", "all"]
    assert confirmed["time_period_start"] == "2020-09-01"
    assert confirmed["time_period_end"] == "2021-02-01"
    assert confirmed["population_scope"] == "ADULT_US_FACEBOOK_MONTHLY_ACTIVE_USERS"
    assert confirmed["active_user_age_minimum"] == 18
    assert confirmed["science_paper_orders_potential_actual_engagement"] is True


def test_variable_semantics_and_privacy_rules_remain_hard_blockers() -> None:
    audit = load(CONTRACT)
    unresolved = set(audit["unresolved_requirements"])
    for token in (
        "audience_unique_deduplicated_estimated_or_other_semantics",
        "repeated_view_handling",
        "owner_all_row_union_or_recomputation_semantics",
        "suppression_thresholding_perturbation_rounding_rules",
        "missingness_and_structural_zero_distinction",
        "actual_audience_subset_compatibility_with_potential_audience",
    ):
        assert token in unresolved


def test_all_hard_gates_are_required_before_calculation() -> None:
    gates = load(CONTRACT)["hard_gates"]
    assert gates["all_must_be_satisfied_before_calculation"] is True
    assert gates["public_variable_dictionary_or_equivalent_inspected"] is True
    assert gates["exact_variable_names_frozen"] is True
    assert gates["numerator_denominator_same_count_semantics"] is True
    assert gates["missing_suppression_policy_frozen"] is True
    assert gates["actual_subset_compatibility_verified"] is True
    assert gates["no_post_hoc_denominator_substitution"] is True


def test_document_preserves_nonclaim_boundary() -> None:
    text = DOC.read_text(encoding="utf-8").lower()
    for token in (
        "public_codebook_compatibility_audit",
        "pairing_design_plausible / numerical_pairing_not_yet_authorized",
        "not authorized for calculation yet",
        "not the dyadic synthetic",
        "variable-level count semantics and privacy/aggregation rules",
        "f1a remains **recovery_tested**",
    ):
        assert token in text
