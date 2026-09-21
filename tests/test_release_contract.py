from __future__ import annotations

import json
import re
from pathlib import Path

import cognitive_epistemic_model as cbd

ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.1.1"
RELEASE_DATE = "2026-09-21"


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_version_surfaces_are_consistent() -> None:
    assert cbd.__version__ == VERSION
    citation = read("CITATION.cff")
    assert re.search(rf"(?m)^version:\s*{re.escape(VERSION)}\s*$", citation)
    assert re.search(rf"(?m)^date-released:\s*{RELEASE_DATE}\s*$", citation)
    assert f"v{VERSION}" in read("README.md")
    assert f"v{VERSION}" in read("STATUS.md")
    assert f"## {VERSION} - {RELEASE_DATE}" in read("CHANGELOG.md")
    assert f"# Cognitive Belief Dynamics v{VERSION}" in read(f"releases/v{VERSION}.md")
    workflow = read(".github/workflows/cbd-validation.yml")
    assert f"cbd.__version__ == '{VERSION}'" in workflow


def test_release_manifest_routes_exist() -> None:
    manifest = json.loads(read(f"releases/v{VERSION}.manifest.json"))
    assert manifest["release"] == VERSION
    assert manifest["date"] == RELEASE_DATE
    assert manifest["scientific_model_change"] is False
    for path in manifest["canonical_surfaces"].values():
        assert (ROOT / path).exists()
    for path in manifest["reproducibility"].values():
        assert (ROOT / path).exists()
    for path in manifest["retained_scientific_artifacts"].values():
        assert (ROOT / path).exists()


def test_release_manifest_preserves_scientific_boundaries() -> None:
    manifest = json.loads(read(f"releases/v{VERSION}.manifest.json"))
    boundary = manifest["scientific_boundaries"]
    assert boundary["formal_system_dynamics"] is False
    assert boundary["human_validation"] is False
    assert boundary["pencode_identified"] is False
    assert boundary["participant_recruitment_authorized"] is False


def test_atm_retrieval_includes_continuity_surfaces() -> None:
    manifest = json.loads(read(".atm/repository.json"))
    canonical = manifest["retrieval"]["canonical"]
    assert manifest["version_source"] == {"type": "cff", "path": "CITATION.cff"}
    assert "DEVELOPMENT.md" in canonical
    assert "CHANGELOG.md" in canonical


def test_development_handoff_has_source_of_truth_and_resume_protocol() -> None:
    text = read("DEVELOPMENT.md")
    for token in (
        "Source-of-truth order",
        "Known audit boundaries and open scientific gaps",
        "Release procedure",
        "Current next gates",
        "How to resume after context loss",
        "Issue #110",
    ):
        assert token in text
