from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError

from cognitive_epistemic_model.workspace import WorkspaceError, validate_workspace_document


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas/workspace.schema.json"
FIXTURE = ROOT / "model/contracts/workspace_fixture_v1.json"
SEMANTIC = ROOT / "model/semantic_index.json"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def validator() -> Draft202012Validator:
    schema = load(SCHEMA)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def test_workspace_fixture_validates_against_draft_2020_12_schema():
    validator().validate(load(FIXTURE))


def test_workspace_fixture_resolves_all_semantic_refs_and_current_revision():
    validate_workspace_document(
        load(FIXTURE),
        schema_path=SCHEMA,
        semantic_index=load(SEMANTIC),
    )


def test_workspace_versions_remain_separate_dimensions():
    versions = load(FIXTURE)["versions"]
    assert versions["software_version"] == "0.4.2a0"
    assert versions["model_specification"] == "M1"
    assert versions["evidence_snapshot"] == "EVIDENCE.M1.2026-09-16.r1"
    assert versions["semantic_schema_version"] == "1"
    assert versions["semantic_baseline_contract"] == "OA0.BASELINE.2026-09-16"


def test_workspace_references_ids_not_embedded_ui_or_scientific_objects():
    case = load(FIXTURE)["case"]
    assert all(isinstance(value, str) for value in case["entity_refs"])
    assert all(isinstance(value, str) for value in case["relation_refs"])

    broken = load(FIXTURE)
    broken["case"]["entity_refs"][0] = {
        "id": "GLOSS.MECH.REPETITION",
        "label": "duplicated UI copy",
    }
    with pytest.raises(ValidationError):
        validator().validate(broken)


def test_unknown_future_workspace_schema_is_rejected_not_rewritten():
    broken = load(FIXTURE)
    broken["schema_version"] = "2"
    original = copy.deepcopy(broken)

    with pytest.raises(WorkspaceError):
        validate_workspace_document(
            broken,
            schema_path=SCHEMA,
            semantic_index=load(SEMANTIC),
        )

    assert broken == original


def test_workspace_rejects_unresolved_semantic_reference():
    broken = load(FIXTURE)
    broken["case"]["entity_refs"].append("VAR.DOES.NOT.EXIST")

    with pytest.raises(WorkspaceError, match="unresolved workspace semantic entity refs"):
        validate_workspace_document(
            broken,
            schema_path=SCHEMA,
            semantic_index=load(SEMANTIC),
        )


def test_workspace_requires_current_revision_to_be_generated():
    broken = load(FIXTURE)
    broken["provenance"]["current_revision_id"] = "CEM.WORKSPACE.REV.missing"

    with pytest.raises(WorkspaceError, match="current workspace revision was not generated"):
        validate_workspace_document(
            broken,
            schema_path=SCHEMA,
            semantic_index=load(SEMANTIC),
        )


def test_workspace_root_rejects_collapsed_generic_version_field():
    broken = load(FIXTURE)
    broken["version"] = "0.4.2a0"

    with pytest.raises(ValidationError):
        validator().validate(broken)
