from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas/semantic_index.schema.json"
FIXTURE = ROOT / "model/contracts/semantic_index_fixture_v1.json"


def load(path: Path):
    return json.loads(path.read_text())


def validator() -> Draft202012Validator:
    schema = load(SCHEMA)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def test_semantic_index_fixture_validates_against_draft_2020_12_schema():
    validator().validate(load(FIXTURE))


def test_semantic_index_fixture_keeps_relation_layers_distinct():
    fixture = load(FIXTURE)
    layers = {relation["layer"] for relation in fixture["relations"]}
    assert layers == {
        "REGISTERED_EVIDENCE_RELATION",
        "COMPUTATIONAL_DEPENDENCY",
        "DOCUMENTATION_RELATION",
    }


def test_semantic_index_uses_status_facets_not_scalar_epistemic_status():
    fixture = load(FIXTURE)
    for entity in fixture["entities"]:
        assert "epistemic_status" not in entity
    for relation in fixture["relations"]:
        assert "epistemic_status" not in relation


def test_semantic_index_rejects_scalar_epistemic_status():
    fixture = load(FIXTURE)
    broken = copy.deepcopy(fixture)
    broken["entities"][0]["epistemic_status"] = "VALIDATED"

    with pytest.raises(ValidationError):
        validator().validate(broken)


def test_registered_relation_requires_separate_evidence_status_facets():
    fixture = load(FIXTURE)
    broken = copy.deepcopy(fixture)
    relation = broken["relations"][0]
    relation.pop("status_facets")

    with pytest.raises(ValidationError):
        validator().validate(broken)


def test_semantic_index_rejects_unknown_relation_layer():
    fixture = load(FIXTURE)
    broken = copy.deepcopy(fixture)
    broken["relations"][0]["layer"] = "GENERIC_CAUSAL_EDGE"

    with pytest.raises(ValidationError):
        validator().validate(broken)


def test_semantic_entity_and_relation_ids_are_unique_in_fixture():
    fixture = load(FIXTURE)
    entity_ids = [entity["id"] for entity in fixture["entities"]]
    relation_ids = [relation["id"] for relation in fixture["relations"]]

    assert len(entity_ids) == len(set(entity_ids))
    assert len(relation_ids) == len(set(relation_ids))


def test_noncomputational_fixture_relations_resolve_to_semantic_entities():
    fixture = load(FIXTURE)
    entity_ids = {entity["id"] for entity in fixture["entities"]}

    for relation in fixture["relations"]:
        if relation["layer"] == "COMPUTATIONAL_DEPENDENCY":
            continue
        assert relation["source"] in entity_ids
        assert relation["target"] in entity_ids


def test_fixture_registered_evidence_refs_resolve_to_reference_entities():
    fixture = load(FIXTURE)
    reference_ids = {
        entity["id"]
        for entity in fixture["entities"]
        if entity["semantic_type"] == "REFERENCE"
    }

    relation = next(
        relation
        for relation in fixture["relations"]
        if relation["layer"] == "REGISTERED_EVIDENCE_RELATION"
    )
    assert set(relation["evidence_refs"]) <= reference_ids


def test_computational_dependency_uses_canonical_semantic_endpoints():
    fixture = load(FIXTURE)
    entity_ids = {entity["id"] for entity in fixture["entities"]}
    relation = next(
        relation
        for relation in fixture["relations"]
        if relation["layer"] == "COMPUTATIONAL_DEPENDENCY"
    )

    assert relation["source"] in entity_ids
    assert relation["target"] in entity_ids
    assert relation["source"] == "VAR.EXPOSURE.COUNT"
    assert relation["target"] == "VAR.FAMILIARITY.CLAIM"


def test_multilingual_label_contract_allows_one_preferred_string_per_language():
    fixture = load(FIXTURE)
    labels = fixture["entities"][0]["labels"]["preferred"]

    assert labels["ro"] == "Familiaritatea afirmației"
    assert labels["en"] == "Claim familiarity"
