from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "model" / "experiments" / "f1a_somar_count_semantics_audit.json"
SCHEMA = ROOT / "schemas" / "f1a_somar_count_semantics_audit.schema.json"
DOC = ROOT / "docs" / "F1A_SOMAR_COUNT_SEMANTICS_AUDIT.md"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_count_semantics_audit_matches_schema() -> None:
    audit = load(CONTRACT)
    schema = load(SCHEMA)
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(audit)


def test_audit_does_not_authorize_calculation_or_promotion() -> None:
    audit = load(CONTRACT)
    assert audit["current_stage"] == "RECOVERY_TESTED"
    assert audit["empirical_promotion_authorized"] is False
    assert audit["numerical_calculation_authorized"] is False
    assert audit["next_gate"]["automatic_calculation_allowed"] is False
    assert audit["next_gate"]["shared_inventory_rule_required"] is True


def test_audience_and_views_are_distinct_estimands() -> None:
    s = load(CONTRACT)["resolved_semantics"]
    assert s["audience"] == "NUMBER_OF_USERS_OR_PARTICIPANTS_WHO_VIEWED_ORGANIC_CONTENT_AT_LEAST_ONCE"
    assert s["content_views"] == "NUMBER_OF_TIMES_CONTENT_APPEARED_ON_SCREEN"
    assert s["facebook_view_threshold"] == "VISIBLE_PORTION_RENDERED_MORE_THAN_250_MS"
    assert s["repeated_views_can_increase_content_views"] is True


def test_candidate_r_view_uses_user_counts_not_view_volume() -> None:
    q = load(CONTRACT)["candidate_component_quantity"]
    assert q["formula"] == "exposed_audience_users / potential_audience_users"
    assert q["numerator_semantics"] == "UNIQUE_USERS_VIEWED_AT_LEAST_ONCE"
    assert q["content_views_allowed_as_numerator"] is False
    assert q["status"] == "CONCEPTUALLY_CONDITIONAL_ON_SHARED_INVENTORY_NUMERICALLY_BLOCKED"
    assert q["paper_analysis_shared_inventory_supported"] is True
    assert q["current_release_shared_inventory_verified"] is False
    assert q["interpretable_as_release_view_rate_without_shared_inventory_proof"] is False
    assert q["equivalent_to_q_transmit"] is False


def test_domain_level_pair_is_only_a_separate_coarser_fallback_candidate() -> None:
    alt = load(CONTRACT)["alternative_domain_level_pair"]
    assert alt["potential_exposure"]["icpsr"] == "300434"
    assert alt["potential_exposure"]["current_catalog_advertises_potential_audience_size"] is True
    assert alt["exposure"]["icpsr"] == "300468"
    assert alt["exposure"]["current_catalog_advertises_audience_size"] is True
    assert alt["same_study_period_high_level"] is True
    assert alt["same_active_user_population_high_level"] is True
    assert alt["current_physical_count_fields_verified"] is False
    assert alt["current_shared_inventory_verified"] is False
    assert alt["absent_row_semantics_verified"] is False
    assert alt["current_release_linkage_verified"] is False
    assert alt["aggregation_equivalent_to_url_level"] is False
    assert alt["automatic_substitution_for_url_level_r_view_allowed"] is False
    assert alt["status"] == "COARSER_FALLBACK_CANDIDATE_SEPARATE_PROSPECTIVE_CONTRACT_REQUIRED"


def test_alternative_daily_weekly_surfaces_do_not_bypass_count_field_gate() -> None:
    alt = load(CONTRACT)["alternative_single_surface_candidates"]
    assert alt["decision"] == "NO_PUBLICLY_ESTABLISHED_SINGLE_SURFACE_COUNT_SUBSTITUTE"
    for key, aggregation in (("icpsr_300456", "DAILY"), ("icpsr_300459", "WEEKLY")):
        candidate = alt[key]
        assert candidate["aggregation"] == aggregation
        assert candidate["legacy_codebook_audience_stage_dimension_present"] is True
        assert candidate["publicly_indexed_raw_or_unique_audience_count_fields_established"] is False
        assert candidate["substitute_for_r_view_count_pair_authorized"] is False
        assert candidate["current_catalog_metric_families"] == [
            "IDEOLOGICAL_SEGREGATION_INDEX",
            "FAVORABILITY_SCORE",
            "CONTENT_ATTRIBUTES",
            "USER_ATTRIBUTES",
        ]


def test_owner_all_and_funnel_semantics_are_resolved_without_sum_assumption() -> None:
    s = load(CONTRACT)["resolved_semantics"]
    assert s["owner_all"] == "POSTS_FROM_USERS_PAGES_AND_GROUPS"
    assert s["owner_all_simple_sum_assumed"] is False
    assert s["inventory_ranked_into_feed"] is True
    assert s["exposed_audience"] == "UNIQUE_USERS_WHO_SAW_POST_CONTAINING_URL_IN_FEED"


def test_remaining_gate_is_column_identity_privacy_and_linkage() -> None:
    audit = load(CONTRACT)
    assert audit["next_gate"]["name"] == "COLUMN_IDENTITY_AND_PRIVACY_RULES_AUDIT"
    blockers = set(audit["unresolved_blockers"])
    for token in (
        "exact_potential_audience_column_name",
        "exact_exposed_audience_column_name",
        "suppression_minimum_cell_perturbation_rounding_rules",
        "missing_suppressed_vs_structural_zero_encoding",
        "url_canonicalization_and_key_identity",
        "release_version_row_linkage_rule",
        "paper_shared_inventory_to_release_field_scope_equivalence",
    ):
        assert token in blockers


def test_document_preserves_numerical_block_and_stage_boundary() -> None:
    text = DOC.read_text(encoding="utf-8").lower()
    for token in (
        "count_semantics_partially_resolved",
        "content_views / potential_audience_users",
        "column_identity_and_privacy_rules_unresolved",
        "numerical `r_view` calculation remains unauthorized",
        "shared-inventory",
        "f1a therefore remains **recovery_tested**",
    ):
        assert token in text


def test_known_privacy_controls_are_resolved_but_additional_release_controls_remain_open() -> None:
    audit = load(CONTRACT)
    resolved = set(audit["resolved_blockers"])
    assert "analysis_uses_aggregate_not_individual_level_exposure_engagement_metrics" in resolved
    assert "url_inclusion_requires_more_than_100_us_shares_for_privacy" in resolved
    unresolved = set(audit["unresolved_blockers"])
    assert "suppression_minimum_cell_perturbation_rounding_rules" in unresolved
