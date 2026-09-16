from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "model/computational_dependencies.json"
SCHEMA = ROOT / "schemas/computational_dependencies.schema.json"
WEB_GENERATED = ROOT / "web/src/generated/computational_dependencies.json"
ADAPTER = ROOT / "web/src/dependencies.ts"
VARIABLES = ROOT / "model/variables.json"
LINKS = ROOT / "model/links.json"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_computational_dependency_contract_validates():
    schema = load(SCHEMA)
    Draft202012Validator.check_schema(schema)
    errors = list(Draft202012Validator(schema).iter_errors(load(DATA)))
    assert not errors, "\n".join(error.message for error in errors)


def test_computational_dependency_contract_has_frozen_m0_surface():
    data = load(DATA)
    assert data["schema_version"] == "1"
    assert data["model_scope"] == "M0"
    assert data["purpose"] == "COMPUTATIONAL_EXPLANATION_ONLY"
    assert len(data["extra_nodes"]) == 11
    assert len(data["dependencies"]) == 17
    assert len({item["semantic_id"] for item in data["extra_nodes"]}) == 11
    assert len({item["graph_id"] for item in data["extra_nodes"]}) == 11
    assert len({item["id"] for item in data["dependencies"]}) == 17
    assert len({item["graph_id"] for item in data["dependencies"]}) == 17


def test_variable_graph_map_resolves_existing_canonical_variables():
    data = load(DATA)
    variables = load(VARIABLES)
    by_short = {item["short_name"]: item["id"] for item in variables}
    assert data["variable_graph_map"] == {
        "Nexp": by_short["Nexp"],
        "F": by_short["F"],
        "C": by_short["C"],
        "T": by_short["T"],
        "B": by_short["B"],
        "W": by_short["W"],
        "Share": by_short["Share"],
    }


def test_dependency_semantic_endpoints_and_registered_links_resolve():
    data = load(DATA)
    variable_ids = {item["id"] for item in load(VARIABLES)}
    extra_ids = {item["semantic_id"] for item in data["extra_nodes"]}
    allowed = variable_ids | extra_ids
    link_ids = {item["id"] for item in load(LINKS)}

    for item in data["dependencies"]:
        assert item["source_semantic_id"] in allowed
        assert item["target_semantic_id"] in allowed
        if "registered_relation_id" in item:
            assert item["registered_relation_id"] in link_ids


def test_web_generated_dependency_data_matches_canonical_byte_for_byte():
    assert WEB_GENERATED.read_bytes() == DATA.read_bytes()


def test_typescript_dependency_adapter_consumes_generated_canonical_data():
    adapter = ADAPTER.read_text(encoding="utf-8")
    assert "generated/computational_dependencies.json" in adapter
    assert "F′ = F + αf(1 − F)" not in adapter
    assert "LINK.EXPOSURE.FAMILIARITY" not in adapter

def test_contract_keeps_computation_separate_from_evidence_registry():
    data = load(DATA)
    registered = {item["registered_relation_id"] for item in data["dependencies"] if "registered_relation_id" in item}
    assert registered == {
        "LINK.EXPOSURE.FAMILIARITY",
        "LINK.FAMILIARITY.BELIEF",
        "LINK.ACCURACY.ACTION",
    }
    assert len(registered) < len(data["dependencies"])
