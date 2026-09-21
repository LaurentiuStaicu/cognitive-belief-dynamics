from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "model" / "audits" / "content_audit_2026-09-21.json"
SCHEMA = ROOT / "schemas" / "content_audit.schema.json"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_content_audit_validates_against_schema() -> None:
    audit = load(AUDIT)
    schema = load(SCHEMA)
    Draft202012Validator.check_schema(schema)
    errors = sorted(Draft202012Validator(schema).iter_errors(audit), key=lambda e: list(e.path))
    assert errors == [], "; ".join(error.message for error in errors)


def test_content_audit_covers_every_current_registry_object() -> None:
    audit = load(AUDIT)
    expected = {
        "references": {x["id"] for x in load(ROOT / "model" / "references.json")},
        "empirical_targets": {x["id"] for x in load(ROOT / "model" / "empirical_targets.json")},
        "variables": {x["id"] for x in load(ROOT / "model" / "variables.json")},
        "links": {x["id"] for x in load(ROOT / "model" / "links.json")},
        "processes": {x["id"] for x in load(ROOT / "model" / "processes.json")},
    }
    for key, ids in expected.items():
        assert {x["id"] for x in audit[key]} == ids


def test_content_audit_covers_every_scientific_contract() -> None:
    audit = load(AUDIT)
    expected = {
        str(path.relative_to(ROOT))
        for path in (ROOT / "model" / "contracts").glob("*.json")
    }
    assert {x["path"] for x in audit["scientific_contracts"]} == expected


def test_content_audit_records_repaired_error_and_open_gaps() -> None:
    audit = load(AUDIT)
    findings = {x["id"]: x for x in audit["repaired_findings"]}
    assert findings["CA.F001"]["severity"] == "ERROR"
    assert findings["CA.F001"]["status"] == "REPAIRED_METADATA"
    assert any(x["area"] == "parameter domains" for x in audit["open_gaps"])
    assert any(x["area"] == "endogeneity" for x in audit["open_gaps"])


def test_content_audit_is_tied_to_r2_evidence_metadata() -> None:
    audit = load(AUDIT)
    snapshot = load(ROOT / "model" / "evidence_snapshot.json")
    assert audit["evidence_snapshot"] == snapshot["id"]
    assert snapshot["id"] == "EVIDENCE.M1.2026-09-21.r2"


def test_content_audit_covers_primary_benchmark_configs_and_results() -> None:
    audit = load(AUDIT)
    expected = {
        "model/benchmarks/m1_e4_candidate_recovery_core.json",
        "model/benchmarks/m1_e4_candidate_recovery_trial_count_refinement.json",
        "model/benchmarks/m1_e4_participant_aware_screening.json",
        "model/benchmarks/m1_e4_participant_confirmation_200.json",
        "model/benchmarks/m1_e4_protocol_robustness_200.json",
        "model/benchmarks/results/m1_e4_candidate_recovery_authoritative_2026-09-16.csv",
        "model/benchmarks/results/m1_e4_trial_count_refinement_authoritative_2026-09-16.csv",
        "model/benchmarks/results/m1_e4_participant_screening_authoritative_2026-09-16.csv",
        "model/benchmarks/results/m1_e4_participant_confirmation_authoritative_2026-09-16.json",
        "model/benchmarks/results/m1_e4_protocol_robustness_authoritative_2026-09-17.json",
    }
    assert {item["path"] for item in audit["benchmark_artifacts"]} == expected


def test_content_audit_covers_modules_subsystems_and_validation_patterns() -> None:
    audit = load(AUDIT)
    expected = {
        "modules": {x["id"] for x in load(ROOT / "model/modules.json")},
        "subsystems": {x["id"] for x in load(ROOT / "model/subsystems.json")},
        "validation_patterns": {x["id"] for x in load(ROOT / "model/validation_tests.json")},
    }
    for key, ids in expected.items():
        assert {x["id"] for x in audit[key]} == ids

    assert len(audit["modules"]) == 20
    assert len(audit["subsystems"]) == 8
    assert len(audit["validation_patterns"]) == 15


def _embedded_contract_sources() -> set[tuple[str, str]]:
    pairs: set[tuple[str, str]] = set()
    for path in sorted((ROOT / "model" / "contracts").glob("*.json")):
        contract = load(path)
        for key in ("sources", "references"):
            values = contract.get(key, [])
            if isinstance(values, list):
                for source in values:
                    if isinstance(source, dict) and source.get("id"):
                        pairs.add((str(path.relative_to(ROOT)), source["id"]))
    return pairs


def test_content_audit_covers_every_embedded_contract_source() -> None:
    audit = load(AUDIT)
    actual = {(item["path"], item["id"]) for item in audit["embedded_contract_sources"]}
    assert actual == _embedded_contract_sources()


def test_embedded_source_identifier_duplicates_do_not_conflict() -> None:
    audit = load(AUDIT)
    identifiers: dict[str, set[str]] = {}
    for item in audit["embedded_contract_sources"]:
        if item["identifier"] == "NO_EXTERNAL_IDENTIFIER":
            continue
        identifiers.setdefault(item["id"], set()).add(item["identifier"])
    assert all(len(values) == 1 for values in identifiers.values())


def test_empirical_target_design_structure_is_semantically_explicit() -> None:
    targets = {x["id"]: x for x in load(ROOT / "model" / "empirical_targets.json")}
    for target in targets.values():
        study = target["study"]
        if "design_family" in study:
            continue
        assert "event_count" not in study
        assert study["design_structure"]

    tohidi = {
        row["unit_type"]: row["count"]
        for row in targets["TARGET.M1.E1.TOHIDI_2025"]["study"]["design_structure"]
    }
    assert tohidi == {"news_events": 7, "framing_conditions": 3}

    aruguete = {
        row["unit_type"]: row["count"]
        for row in targets["TARGET.M1.E2.ARUGUETE_2024"]["study"]["design_structure"]
    }
    assert aruguete["countries"] == 4
    assert aruguete["primary_frame_arms"] == 2

    alvarado = {
        row["unit_type"]: row["count"]
        for row in targets["TARGET.M1.E2.ALVARADO_2026"]["study"]["design_structure"]
    }
    assert alvarado["facebook_style_posts"] == 8
    assert alvarado["candidates"] * alvarado["claim_contents"] * alvarado["frame_types"] == 8
