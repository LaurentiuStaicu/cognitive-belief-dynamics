from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

BASELINE = ROOT / "model/contracts/oa0_optimization_baseline.json"
VERSION = ROOT / "web/public/model/version.json"
SNAPSHOT = ROOT / "model/evidence_snapshot.json"
VARIABLES = ROOT / "model/variables.json"
CONFIRMATION_SHA = (
    ROOT
    / "model/benchmarks/results"
    / "m1_e4_participant_confirmation_authoritative_2026-09-16.sha256"
)


def load(path: Path):
    return json.loads(path.read_text())


def test_oa0_baseline_pins_historical_release_and_scientific_contract():
    baseline = load(BASELINE)
    version = load(VERSION)
    snapshot = load(SNAPSHOT)

    assert baseline["software_version"] == "0.4.2a0"
    assert baseline["release_tag"] == "v0.4.2a0"
    assert version["software_version"] == "0.4.3a0"
    assert version["release_tag"] == "v0.4.3a0"
    assert (
        baseline["active_model_specification"]
        == version["model_specification"]
        == snapshot["model_specification"]
        == "M1"
    )
    assert (
        baseline["baseline_model_specification"]
        == version["baseline_model_specification"]
        == "M0"
    )
    assert (
        baseline["evidence_snapshot"]
        == version["evidence_snapshot"]
        == snapshot["id"]
        == "EVIDENCE.M1.2026-09-16.r1"
    )


def test_oa0_baseline_pins_authoritative_m1_e4_confirmation_without_activation():
    baseline = load(BASELINE)
    digest, path = CONFIRMATION_SHA.read_text().strip().split("  ", 1)

    assert (
        baseline["authoritative_m1_e4_confirmation_sha256"]
        == digest
        == "88c16c2143e7131a4ec8915dbb726ece7e859a797162df173b89743837335f89"
    )
    assert path.endswith(
        "m1_e4_participant_confirmation_authoritative_2026-09-16.json"
    )

    version = load(VERSION)
    assert version["model_specification"] == "M1"
    assert "M1.E4" not in version["model_specification"]


def test_oa0_baseline_preserves_pencode_as_non_active():
    variables = load(VARIABLES)
    serialized = json.dumps(variables).lower()

    assert "pencode" not in serialized


def test_oa0_contract_documents_exist():
    required = [
        ROOT / "docs/CEM_OPTIMIZATION_ARCHITECTURE.md",
        ROOT / "docs/CEM_OPTIMIZATION_IMPLEMENTATION_PLAN.md",
        ROOT / "docs/CEM_SEMANTIC_CONTRACT.md",
        ROOT / "docs/CEM_QUALITY_MATRIX.md",
    ]
    for path in required:
        assert path.is_file(), path
        assert path.read_text().strip(), path
