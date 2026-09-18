from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "model" / "contracts" / "world_model_v1.json"
SCHEMA = ROOT / "schemas" / "world_model.schema.json"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_world_model_contract_is_schema_valid():
    contract = load(CONTRACT)
    schema = load(SCHEMA)
    Draft202012Validator.check_schema(schema)
    errors = list(Draft202012Validator(schema).iter_errors(contract))
    assert not errors, "\n".join(error.message for error in errors)


def test_all_four_epistemic_levels_are_explicit_and_unique():
    levels = [item["level"] for item in load(CONTRACT)["epistemic_levels"]]
    assert levels == ["EMPIRICAL", "EXECUTABLE", "CONCEPTUAL", "INTERPRETIVE"]


def test_world_model_cross_links_resolve_without_redefining_existing_cem_constructs():
    contract = load(CONTRACT)
    variables = {item["id"] for item in load(ROOT / "model" / "variables.json")}
    modules = {item["id"] for item in load(ROOT / "model" / "modules.json")}
    for item in contract["cross_links"]:
        assert item["target"] in variables | modules

    forbidden_duplicates = {
        "VAR.FAMILIARITY.CLAIM",
        "VAR.CORRECTION.ACCESS",
        "VAR.RELIABILITY.ESTIMATE",
        "VAR.BELIEF.CLAIM",
        "VAR.ISSUE.APPRAISAL",
    }
    assert not (forbidden_duplicates & {item["id"] for item in contract["variables"]})


def test_executable_surface_is_narrow_and_requires_external_diagnosticity():
    contract = load(CONTRACT)
    executable_mechanisms = {
        item["id"] for item in contract["mechanisms"] if "EXECUTABLE" in item["status"]
    }
    assert executable_mechanisms == {
        "WM.MECH.NORMATIVE_UPDATE",
        "WM.MECH.UNCERTAINTY_TRACKING",
    }
    text = json.dumps(contract, ensure_ascii=False).lower()
    assert "measurement model" in text
    assert "fail closed" in text


def test_phase_m_and_blocked_human_work_remain_unchanged():
    limitations = " ".join(load(CONTRACT)["limitations"]).lower()
    assert "m1.e4" in limitations
    assert "pencode" in limitations
    assert "human recruitment" in limitations
    assert "phase m remains unchanged" in limitations
