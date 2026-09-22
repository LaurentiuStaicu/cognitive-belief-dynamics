from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "model" / "experiments" / "f1a_somar_column_privacy_audit.json"
SCHEMA = ROOT / "schemas" / "f1a_somar_column_privacy_audit.schema.json"
DOC = ROOT / "docs" / "F1A_SOMAR_COLUMN_PRIVACY_AUDIT.md"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_column_privacy_audit_matches_schema() -> None:
    audit = load(CONTRACT)
    schema = load(SCHEMA)
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(audit)


def test_audit_preserves_recovery_tested_boundary() -> None:
    audit = load(CONTRACT)
    assert audit["current_stage"] == "RECOVERY_TESTED"
    assert audit["empirical_promotion_authorized"] is False
    assert audit["numerical_calculation_authorized"] is False
    assert audit["next_gate"]["automatic_calculation_allowed"] is False


def test_exact_columns_remain_unverified() -> None:
    audit = load(CONTRACT)
    q = audit["candidate_component_quantity"]
    assert q["exact_numerator_column_verified"] is False
    assert q["exact_denominator_column_verified"] is False
    assert "exact_potential_audience_column_name" in audit["unresolved_blockers"]
    assert "exact_exposed_audience_column_name" in audit["unresolved_blockers"]


def test_no_cross_product_privacy_inference() -> None:
    p = load(CONTRACT)["privacy_state"]
    assert p["aggregate_only"] is True
    assert p["url_share_threshold_gt_100_us_users"] is True
    assert p["additional_release_controls_verified"] is False
    assert p["differential_privacy_assumed_from_other_meta_products"] is False


def test_legacy_artifacts_are_identified_but_not_claimed_inspected() -> None:
    d = load(CONTRACT)["verified_legacy_documentation"]
    assert d["data_dictionary_filename"] == "data_dictionary_political_segregation_paper.xlsx"
    assert d["variable_descriptions_filename"] == "variables_political_segregation_paper.csv"
    assert d["exact_dictionary_contents_inspected"] is False
    assert d["current_release_version_linkage_verified"] is False


def test_doc_keeps_negative_gate_explicit() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "NUMERICAL_PAIRING_NOT_AUTHORIZED" in text
    assert "No field name is inferred" in text
    assert "F1a remains **RECOVERY_TESTED**" in text
