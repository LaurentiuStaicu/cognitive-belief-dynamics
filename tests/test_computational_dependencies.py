from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / "model"
WEB = ROOT / "web/public/model"
SCHEMA = ROOT / "schemas/computational_dependencies.schema.json"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_computational_dependency_registry_validates():
    registry = load(MODEL / "computational_dependencies.json")
    schema = load(SCHEMA)
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(registry)


def test_computational_dependency_surface_is_frozen_at_11_nodes_17_edges():
    registry = load(MODEL / "computational_dependencies.json")

    assert len(registry["nodes"]) == 11
    assert len(registry["dependencies"]) == 17
    assert len({item["id"] for item in registry["nodes"]}) == 11
    assert len({item["semantic_id"] for item in registry["nodes"]}) == 11
    assert len({item["id"] for item in registry["dependencies"]}) == 17


def test_computational_graph_and_semantic_endpoints_resolve():
    registry = load(MODEL / "computational_dependencies.json")
    variables = load(MODEL / "variables.json")
    links = load(MODEL / "links.json")

    graph_ids = {item["short_name"] for item in variables} | {
        item["id"] for item in registry["nodes"]
    }
    semantic_ids = {item["id"] for item in variables} | {
        item["semantic_id"] for item in registry["nodes"]
    }
    link_ids = {item["id"] for item in links}

    for edge in registry["dependencies"]:
        assert edge["source"] in graph_ids
        assert edge["target"] in graph_ids
        assert edge["source_semantic_id"] in semantic_ids
        assert edge["target_semantic_id"] in semantic_ids
        if "registered_relation_id" in edge:
            assert edge["registered_relation_id"] in link_ids


def test_web_copy_is_byte_identical_to_canonical_registry():
    assert (
        (WEB / "computational_dependencies.json").read_bytes()
        == (MODEL / "computational_dependencies.json").read_bytes()
    )


def test_semantic_index_contains_all_computational_nodes_and_dependencies():
    registry = load(MODEL / "computational_dependencies.json")
    semantic = load(MODEL / "semantic_index.json")

    entities = {item["id"]: item for item in semantic["entities"]}
    relations = {item["id"]: item for item in semantic["relations"]}

    for node in registry["nodes"]:
        entity = entities[node["semantic_id"]]
        assert entity["semantic_type"] == "COMPUTATIONAL_NODE"
        assert entity["short_name"] == node["id"]

    for edge in registry["dependencies"]:
        relation = relations[edge["id"]]
        assert relation["layer"] == "COMPUTATIONAL_DEPENDENCY"
        assert relation["source"] == edge["source_semantic_id"]
        assert relation["target"] == edge["target_semantic_id"]
        assert relation["formula"] == edge["formula"]
        assert relation["code_file"] == edge["code_file"]
