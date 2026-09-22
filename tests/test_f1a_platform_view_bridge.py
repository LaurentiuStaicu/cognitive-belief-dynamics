from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "model" / "experiments" / "f1a_platform_view_bridge_contract.json"
SCHEMA = ROOT / "schemas" / "f1a_platform_view_bridge_contract.schema.json"
DOC = ROOT / "docs" / "F1A_PLATFORM_VIEW_BRIDGE_DESIGN.md"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_platform_view_bridge_contract_matches_schema() -> None:
    contract = load(CONTRACT)
    schema = load(SCHEMA)
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(contract)


def test_bridge_does_not_promote_or_change_runtime() -> None:
    contract = load(CONTRACT)
    assert contract["status"] == "EMPIRICAL_COMPONENT_BRIDGE_DESIGN_ONLY"
    assert contract["current_stage"] == "RECOVERY_TESTED"
    assert contract["promotion_authorized"] is False
    assert contract["runtime_change_authorized"] is False
    assert contract["synthetic_parameter_boundary"]["status"] == "CALIBRATION_ONLY_NOT_ACTIVE_RUNTIME"
    assert contract["synthetic_parameter_boundary"]["direct_empirical_estimation_authorized"] is False


def test_potential_view_and_cognitive_exposure_are_separate_constructs() -> None:
    constructs = load(CONTRACT)["constructs"]
    assert constructs["potential_delivery"]["maps_directly_to_cognitive_exposure"] is False
    assert constructs["platform_view"]["maps_directly_to_cognitive_exposure"] is False
    assert constructs["cognitive_exposure"]["existing_runtime_construct"] is True
    assert constructs["cognitive_exposure"]["empirical_mapping_required"] is True


def test_candidate_ratios_are_codebook_gated_and_not_q_transmit() -> None:
    quantities = {row["id"]: row for row in load(CONTRACT)["candidate_component_quantities"]}
    view = quantities["CANDIDATE.R_VIEW.AGGREGATE"]
    engage = quantities["CANDIDATE.R_ENGAGE_GIVEN_VIEW"]

    assert view["current_status"] == "CODEBOOK_GATED_NOT_AUTHORIZED_FOR_CALCULATION"
    assert view["equivalent_to_q_transmit"] is False
    assert engage["current_status"] == "CODEBOOK_GATED_NOT_AUTHORIZED_FOR_CALCULATION"
    assert engage["equivalent_to_cognitive_exposure_probability"] is False


def test_somar_sources_map_to_distinct_measurement_roles() -> None:
    sources = {row["id"]: row for row in load(CONTRACT)["source_mapping"]}

    assert sources["ICPSR.300450"]["bridge_role"] == "POTENTIAL_DELIVERY"
    assert sources["ICPSR.300450"]["public_unit"] == "URL_LEVEL_STUDY_PERIOD_AGGREGATE"
    assert sources["ICPSR.300470"]["bridge_role"] == "PLATFORM_VIEW"
    assert sources["ICPSR.300470"]["public_unit"] == "URL_LEVEL_STUDY_PERIOD_AGGREGATE"
    assert sources["ICPSR.300475"]["bridge_role"] == "DOWNSTREAM_PLATFORM_ACTION"
    assert sources["ICPSR.300446"]["public_unit"] == "PARTICIPANT_DAILY_DOMAIN_LEVEL_AGGREGATE"
    assert sources["ICPSR.300458"]["public_unit"] == "PARTICIPANT_X_NETWORK_AGGREGATE"

    assert all(
        row["dyadic_share_view_lineage_publicly_documented"] is False
        for row in sources.values()
    )


def test_numerical_analysis_is_blocked_until_codebook_gate() -> None:
    gate = load(CONTRACT)["codebook_gate"]
    assert gate["required_before_numerical_analysis"] is True
    required = set(gate["requirements"])
    for token in (
        "unique_user_vs_event_count_semantics",
        "repeated_view_handling",
        "potential_and_actual_population_filter_compatibility",
        "privacy_suppression_rounding_rules",
        "participant_connection_to_item_share_view_linkability",
        "sender_recipient_lineage_presence_or_absence",
    ):
        assert token in required


def test_bridge_interpretation_forbids_proxy_collapse() -> None:
    interpretation = load(CONTRACT)["evidence_interpretation"]
    assert interpretation["platform_view_is_directly_observable_candidate"] is True
    assert interpretation["platform_view_equals_cognitive_exposure"] is False
    assert interpretation["potential_delivery_equals_platform_view"] is False
    assert interpretation["engagement_equals_exposure"] is False
    assert interpretation["aggregate_ratio_equals_dyadic_probability"] is False
    assert interpretation["component_constraints_can_be_retained_without_stage_promotion"] is True


def test_bridge_document_states_non_promotion_boundary() -> None:
    text = DOC.read_text(encoding="utf-8").lower()
    for token in (
        "empirical_component_bridge_design_only",
        "f1a remains **recovery_tested**",
        "platformview",
        "cognitiveexposure",
        "codebook gate before numerical analysis",
        "not the dyadic f1a `q_transmit`",
        "no numerical bridge is authorized",
    ):
        assert token in text
