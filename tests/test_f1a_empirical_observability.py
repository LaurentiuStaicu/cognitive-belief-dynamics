from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "model" / "experiments" / "f1a_empirical_observability_contract.json"
SCHEMA = ROOT / "schemas" / "f1a_empirical_observability_contract.schema.json"
AUDIT = ROOT / "docs" / "F1A_EMPIRICAL_OBSERVABILITY_AUDIT.md"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_f1a_empirical_observability_contract_matches_schema() -> None:
    contract = load(CONTRACT)
    schema = load(SCHEMA)
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(contract)


def test_empirical_audit_does_not_promote_f1a() -> None:
    contract = load(CONTRACT)
    assert contract["status"] == "EMPIRICAL_BRIDGE_AUDIT_ONLY"
    assert contract["current_stage"] == "RECOVERY_TESTED"
    assert contract["candidate_stage"] == "EMPIRICALLY_CONSTRAINED"
    assert contract["promotion_authorized"] is False
    assert contract["estimand"]["empirical_estimation_authorized"] is False
    assert contract["partial_constraint_policy"]["stage_promotion_from_partial_constraints_allowed"] is False
    assert contract["partial_constraint_policy"]["q_transmit_must_remain_calibration_only_until_direct_bridge"] is True


def test_action_and_delivery_proxies_are_not_silently_equated_with_exposure() -> None:
    contract = load(CONTRACT)
    separation = contract["construct_separation"]
    assert all(separation.values())
    required = set(contract["required_measurements"])
    assert "recipient_specific_delivery_or_impression_event_for_same_item" in required
    assert "negative_share_edge_opportunities_without_exposure" in required
    assert "platform_impression_to_cognitive_exposure_measurement_bridge" in required


def test_public_candidate_sources_are_component_constraints_only() -> None:
    contract = load(CONTRACT)
    sources = {row["id"]: row for row in contract["candidate_sources"]}

    bluesky = sources["DATA.BLUESKY.SOCIAL.V3"]
    assert bluesky["verdict"] == "PARTIAL_EMPIRICAL_CONSTRAINT_ONLY"
    assert "recipient_specific_impression_log" in bluesky["missing_for_q_transmit"]

    higgs = sources["DATA.SNAP.HIGGS"]
    assert higgs["verdict"] == "PARTIAL_EMPIRICAL_CONSTRAINT_ONLY_HISTORICAL"
    assert "recipient_specific_impression_log" in higgs["missing_for_q_transmit"]

    prospective = sources["DATA.BLUESKY.ATPROTO.PROSPECTIVE"]
    assert "protocol_lexicon_defines_interaction_seen_token" in prospective["observed"]
    assert "interaction_request_id" in prospective["observed"]
    assert "cognitive_exposure_measurement_bridge" in prospective["missing_for_q_transmit"]
    assert "DEPLOYMENT_ACCESS_PRIVACY_REVIEW_REQUIRED" in prospective["verdict"]

    meta = sources["DATA.META.FIES.2020.SOMAR"]
    assert meta["verdict"] == "ACCESS_AND_MEASUREMENT_REVIEW_REQUIRED"


def test_empirical_promotion_gate_requires_observability_not_action_proxy() -> None:
    gate = load(CONTRACT)["empirical_promotion_gate"]
    assert gate["numerator_defined"] is True
    assert gate["denominator_defined"] is True
    assert gate["negative_opportunities_observable"] is True
    assert gate["action_only_proxy_for_exposure_forbidden"] is True
    assert gate["all_requirements_must_be_satisfied_before_promotion"] is True


def test_empirical_observability_audit_states_current_blocker() -> None:
    text = AUDIT.read_text(encoding="utf-8")
    for token in (
        "EMPIRICAL_BRIDGE_AUDIT_ONLY",
        "F1a remains **RECOVERY_TESTED**",
        "reposts are not exposure logs",
        "Feed output is a candidate-delivery surface",
        "interactionSeen",
        "platform-level seen event",
        "No empirical promotion is authorized by this audit",
    ):
        assert token.lower() in text.lower()
