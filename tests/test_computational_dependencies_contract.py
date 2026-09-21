from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "model/computational_dependencies.json"
SCHEMA = ROOT / "schemas/computational_dependencies.schema.json"
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


def test_scientific_core_uses_single_canonical_dependency_contract():
    assert DATA.exists()
    assert not (ROOT / "web").exists()

def test_contract_keeps_computation_separate_from_evidence_registry():
    data = load(DATA)
    registered = {item["registered_relation_id"] for item in data["dependencies"] if "registered_relation_id" in item}
    assert registered == {
        "LINK.EXPOSURE.FAMILIARITY",
        "LINK.FAMILIARITY.BELIEF",
        "LINK.ACCURACY.ACTION",
    }
    assert len(registered) < len(data["dependencies"])


def test_dependency_code_files_resolve_to_actual_package_files():
    data = load(DATA)
    package = ROOT / "src" / "cognitive_epistemic_model"
    for item in data["dependencies"]:
        assert (package / item["code_file"]).is_file(), item["id"]
        if "input_binding_file" in item:
            assert (package / item["input_binding_file"]).is_file(), item["id"]


def test_correction_direction_dependency_separates_formula_and_binding():
    data = load(DATA)
    item = next(
        dep for dep in data["dependencies"]
        if dep["id"] == "COMPDEP.CORRECTION_DIRECTION.BELIEF"
    )
    assert item["code_file"] == "model.py"
    assert item["input_binding_file"] == "simulation.py"
