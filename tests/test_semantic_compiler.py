from __future__ import annotations

import json
from pathlib import Path

from cognitive_epistemic_model.semantic import (
    build_semantic_index,
    semantic_index_json,
    validate_semantic_index,
)

ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / "model"
SCHEMA = ROOT / "schemas" / "semantic_index.schema.json"
GENERATED = MODEL / "semantic_index.json"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_semantic_compiler_builds_schema_valid_index():
    index = build_semantic_index(MODEL)
    validate_semantic_index(index, SCHEMA)


def test_semantic_compiler_matches_committed_generated_index_byte_for_byte():
    index = build_semantic_index(MODEL)
    assert semantic_index_json(index) == GENERATED.read_text(encoding="utf-8")


def test_semantic_compiler_is_deterministic():
    first = semantic_index_json(build_semantic_index(MODEL))
    second = semantic_index_json(build_semantic_index(MODEL))
    assert first == second


def test_semantic_compiler_entity_coverage_matches_authoritative_sources():
    index = build_semantic_index(MODEL)
    expected = set()
    for name in (
        "variables",
        "modules",
        "references",
        "validation_tests",
        "empirical_targets",
        "theory_index",
        "theory_glossary",
    ):
        expected |= {item["id"] for item in load(MODEL / f"{name}.json")}
    expected |= {
        item["semantic_id"]
        for item in load(MODEL / "computational_dependencies.json")["extra_nodes"]
    }
    expected |= {
        item["id"]
        for item in load(MODEL / "contracts" / "world_model_v1.json")["variables"]
    }

    actual = {item["id"] for item in index["entities"]}
    assert actual == expected
    assert len(actual) == len(expected)


def test_semantic_compiler_preserves_registered_links_exactly():
    index = build_semantic_index(MODEL)
    links = load(MODEL / "links.json")
    expected_ids = {item["id"] for item in links}
    registered = [
        relation
        for relation in index["relations"]
        if relation["layer"] == "REGISTERED_EVIDENCE_RELATION"
    ]

    assert {item["id"] for item in registered} == expected_ids
    assert len(registered) == 10

    source_by_id = {item["id"]: item for item in links}
    for relation in registered:
        source = source_by_id[relation["id"]]
        assert relation["relation_type"] == source["relation_type"]
        assert relation["polarity"] == source["polarity"]
        assert relation["evidence_refs"] == source["evidence_refs"]
        assert relation["status_facets"] == {
            "phenomenon_evidence": source["phenomenon_evidence_status"],
            "mechanism_evidence": source["mechanism_evidence_status"],
            "functional_form": source["functional_form_status"],
        }


def test_semantic_compiler_documentation_relations_are_resolved():
    index = build_semantic_index(MODEL)
    entity_ids = {item["id"] for item in index["entities"]}
    documentation = [
        relation
        for relation in index["relations"]
        if relation["layer"] == "DOCUMENTATION_RELATION"
    ]

    assert len(documentation) == 199
    for relation in documentation:
        assert relation["source"] in entity_ids
        assert relation["target"] in entity_ids


def test_semantic_compiler_imports_computational_dependencies_exactly():
    index = build_semantic_index(MODEL)
    source = load(MODEL / "computational_dependencies.json")
    expected = {item["id"]: item for item in source["dependencies"]}
    compiled = {
        relation["id"]: relation
        for relation in index["relations"]
        if relation["layer"] == "COMPUTATIONAL_DEPENDENCY"
    }

    assert set(compiled) == set(expected)
    assert len(compiled) == 17
    for relation_id, relation in compiled.items():
        item = expected[relation_id]
        assert relation["source"] == item["source_semantic_id"]
        assert relation["target"] == item["target_semantic_id"]
        assert relation["formula"] == item["formula"]
        assert relation["code_file"] == item["code_file"]
        assert relation.get("registered_relation_id") == item.get("registered_relation_id")


def test_semantic_compiler_counts_all_three_relation_layers():
    index = build_semantic_index(MODEL)
    counts = {}
    for relation in index["relations"]:
        counts[relation["layer"]] = counts.get(relation["layer"], 0) + 1
    assert counts == {
        "REGISTERED_EVIDENCE_RELATION": 10,
        "COMPUTATIONAL_DEPENDENCY": 17,
        "DOCUMENTATION_RELATION": 199,
    }
    assert len(index["relations"]) == 226


def test_semantic_related_ids_all_resolve():
    index = build_semantic_index(MODEL)
    entity_ids = {item["id"] for item in index["entities"]}
    for entity in index["entities"]:
        assert set(entity.get("related_ids", [])) <= entity_ids


def test_semantic_compiler_preserves_bilingual_theory_and_glossary_labels():
    index = build_semantic_index(MODEL)
    by_id = {item["id"]: item for item in index["entities"]}

    theory = by_id["THEORY.01.WORLD_INFORMATION_REPRESENTATION"]
    assert set(theory["labels"]["preferred"]) == {"ro", "en"}

    mechanism = by_id["GLOSS.MECH.REPETITION"]
    assert set(mechanism["labels"]["preferred"]) == {"ro", "en"}
    assert "repetition" in mechanism["labels"]["alternative"]["und"]
