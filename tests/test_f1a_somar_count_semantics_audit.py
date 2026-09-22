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
    assert q["status"] == "CONCEPTUALLY_JUSTIFIED_NUMERICALLY_BLOCKED"
    assert q["equivalent_to_q_transmit"] is False


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
    ):
        assert token in blockers


def test_document_preserves_numerical_block_and_stage_boundary() -> None:
    text = DOC.read_text(encoding="utf-8").lower()
    for token in (
        "count_semantics_partially_resolved",
        "content_views / potential_audience_users",
        "column_identity_and_privacy_rules_unresolved",
        "numerical `r_view` calculation remains unauthorized",
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
