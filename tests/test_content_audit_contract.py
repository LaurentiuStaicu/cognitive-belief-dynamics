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
