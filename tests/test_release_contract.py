from __future__ import annotations

import hashlib
import json
import re
import tomllib
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
    readme = read("README.md")
    assert "releases/latest" in readme
    assert "shields.io/github/v/tag/LaurentiuStaicu/cognitive-belief-dynamics" in readme
    assert f"v{VERSION}" not in readme
    assert f"v{VERSION}" in read("STATUS.md")
    assert f"## {VERSION} - {RELEASE_DATE}" in read("CHANGELOG.md")
    assert f"# Cognitive Belief Dynamics v{VERSION}" in read(f"releases/v{VERSION}.md")
    workflow = read(".github/workflows/cbd-validation.yml")
    assert re.search(
        rf"cbd\.__version__\s*==\s*['\"]{re.escape(VERSION)}['\"]",
        workflow,
    )


def test_python_distribution_metadata_preserves_dual_license_scope() -> None:
    project = tomllib.loads(read("pyproject.toml"))["project"]
    assert project["license"] == "MIT AND CC-BY-4.0"
    assert set(project["license-files"]) == {
        "LICENSE",
        "LICENSES/CC-BY-4.0.txt",
        "LICENSING.md",
    }
    for path in project["license-files"]:
        assert (ROOT / path).is_file()


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


def test_evidence_metadata_revision_is_consistent_across_release_surfaces() -> None:
    manifest = json.loads(read(f"releases/v{VERSION}.manifest.json"))
    revision = manifest["evidence_metadata_revision"]
    snapshot = json.loads(read("model/evidence_snapshot.json"))
    assert revision["release_snapshot"] == snapshot["id"] == "EVIDENCE.M1.2026-09-21.r2"
    assert revision["prior_snapshot"] == "EVIDENCE.M1.2026-09-16.r1"
    assert revision["evidence_set_changed"] is False
    assert revision["metadata_corrected_or_qualified"] is True

    for path in ("STATUS.md", "DEVELOPMENT.md", f"releases/v{VERSION}.md"):
        surface = read(path)
        assert "EVIDENCE.M1.2026-09-21.r2" in surface

    assert "EVIDENCE.M1.2026-09-21.r2" not in read("README.md")
    assert "evidence snapshot is changed" not in read("STATUS.md").lower()


def test_evidence_set_identity_fingerprint_matches_current_registry() -> None:
    manifest = json.loads(read(f"releases/v{VERSION}.manifest.json"))
    identity = manifest["evidence_set_identity"]
    references = json.loads(read("model/references.json"))
    payload = "\n".join(sorted(item["id"] for item in references)) + "\n"
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()

    assert len(references) == identity["reference_count"] == 16
    assert digest == identity["release_reference_ids_sha256"]
    assert identity["prior_reference_ids_sha256"] == identity["release_reference_ids_sha256"]
    assert identity["prior_release"] == "v0.1.0"


def test_release_manifest_distinguishes_executable_and_metadata_changes() -> None:
    manifest = json.loads(read(f"releases/v{VERSION}.manifest.json"))
    assert manifest["scientific_model_change"] is False
    assert manifest["executable_equation_change"] is False
    assert manifest["retained_benchmark_result_change"] is False
    assert manifest["scientific_metadata_change"] is True
    assert "metadata" in manifest["scientific_model_change_definition"].lower()


def test_contract_source_set_identity_matches_current_contracts() -> None:
    manifest = json.loads(read(f"releases/v{VERSION}.manifest.json"))
    identity = manifest["contract_source_set_identity"]

    current: set[tuple[str, str]] = set()
    for path in sorted((ROOT / "model" / "contracts").glob("*.json")):
        contract = json.loads(path.read_text(encoding="utf-8"))
        for key in ("sources", "references"):
            for source in contract.get(key, []):
                if isinstance(source, dict) and source.get("id"):
                    current.add((str(path.relative_to(ROOT)), source["id"]))

    assert len(current) == identity["release_source_occurrences"] == 39
    assert identity["prior_source_occurrences"] == 39
    assert identity["source_membership_changed"] is False
    correction = identity["identifier_corrections"][0]
    assert correction["source_id"] == "SRC.M1.E3.MATTIS_HEITZ.2025"
    assert correction["prior_doi"] == "10.1093/joc/jqaf030"
    assert correction["corrected_doi"] == "10.1093/joc/jqaf019"
    assert correction["membership_change"] is False


def _git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    payload = b"blob " + str(len(data)).encode("ascii") + b"\0" + data
    return hashlib.sha1(payload).hexdigest()


def test_restored_historical_provenance_documents_match_original_git_blobs() -> None:
    manifest = json.loads(read(f"releases/v{VERSION}.manifest.json"))
    docs = manifest["historical_provenance_documents"]
    assert len(docs) == 3
    for item in docs:
        path = ROOT / item["path"]
        assert path.is_file()
        assert item["restored_byte_identical"] is True
        assert _git_blob_sha(path) == item["historical_blob_sha"]
        assert len(item["historical_source_commit"]) == 40


def test_community_health_contract_tracks_release_version() -> None:
    contract = json.loads(read(".github/community_health_contract.json"))
    assert contract["current_public_version"] == VERSION
    assert all("v0.1.0" not in item for item in contract["invariants"])


def test_readme_has_compact_use_and_exact_reproduction_paths() -> None:
    readme = read("README.md")
    assert "### Using and reproducing CBD" in readme
    assert "python -m pip install ." in readme
    assert "cemodel demo" in readme
    assert "Exact CI-oriented reproduction" in readme
    assert "requirements/ci-py312-linux.lock.txt" in readme


def test_readme_does_not_claim_platform_enforced_release_immutability() -> None:
    readme = read("README.md")
    assert "GitHub releases/tags provide immutable version points" not in readme
    assert "treated as immutable historical version points by project policy" in readme
