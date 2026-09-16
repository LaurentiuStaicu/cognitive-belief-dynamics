from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas/active_understanding.schema.json"
CONTRACT = ROOT / "model/contracts/active_understanding_v1.json"
SEMANTIC = ROOT / "model/semantic_index.json"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def challenge(contract: dict, challenge_id: str) -> dict:
    return next(item for item in contract["challenges"] if item["id"] == challenge_id)


def test_active_understanding_contract_validates_against_draft_2020_12_schema():
    schema = load(SCHEMA)
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(load(CONTRACT))


def test_oa5a_has_exactly_the_three_r6_foundation_families():
    contract = load(CONTRACT)
    assert [item["id"] for item in contract["challenges"]] == ["AU-1", "AU-2", "AU-3"]
    assert {item["family"] for item in contract["challenges"]} == {
        "EXPOSURE_VS_FAMILIARITY",
        "BELIEF_VS_SHARING",
        "COMPUTATION_VS_CAUSAL_EVIDENCE",
    }


def test_all_canonical_semantic_refs_resolve_without_new_semantic_types():
    contract = load(CONTRACT)
    semantic = load(SEMANTIC)
    entity_ids = {item["id"] for item in semantic["entities"]}
    relation_ids = {item["id"] for item in semantic["relations"]}

    for item in contract["challenges"]:
        assert set(item["worked_example_refs"]) <= entity_ids
        assert set(item["canonical_target_refs"]) <= entity_ids
        assert set(item["canonical_relation_refs"]) <= relation_ids


def test_au1_fixture_is_the_existing_canonical_repetition_run_delta():
    item = challenge(load(CONTRACT), "AU-1")
    fixture = item["fixture"]
    data = load(ROOT / fixture["artifact_path"])
    run = next(run for run in data["runs"] if run["id"] == fixture["run_id"])
    before = next(frame for frame in run["frames"] if frame["time"] == fixture["from_time"])
    after = next(frame for frame in run["frames"] if frame["time"] == fixture["to_time"])

    assert before[fixture["field"]] == fixture["expected_from"] == 0.0
    assert after[fixture["field"]] == fixture["expected_to"] == 0.35
    assert after[fixture["field"]] > before[fixture["field"]]
    assert item["correct_choice_id"] == "INCREASE"


def test_au2_fixture_targets_accuracy_salience_not_belief():
    item = challenge(load(CONTRACT), "AU-2")
    semantic = load(SEMANTIC)
    relations = {rel["id"]: rel for rel in semantic["relations"]}
    relation = relations[item["fixture"]["relation_id"]]

    assert relation["layer"] == "COMPUTATIONAL_DEPENDENCY"
    assert relation["source"] == "COMP.NODE.ACCURACY_CUE_INPUT"
    assert relation["target"] == item["fixture"]["expected_target_id"] == "VAR.ACCURACY.SALIENCE"
    assert relation["target"] != "VAR.BELIEF.CLAIM"
    assert item["correct_choice_id"] == "ACCURACY_SALIENCE"


def test_au3_fixture_preserves_computational_and_evidence_layers_separately():
    item = challenge(load(CONTRACT), "AU-3")
    semantic = load(SEMANTIC)
    relations = {rel["id"]: rel for rel in semantic["relations"]}
    fixture = item["fixture"]

    assert relations[fixture["relation_id"]]["layer"] == fixture["expected_layer"] == "COMPUTATIONAL_DEPENDENCY"
    assert relations[fixture["contrast_relation_id"]]["layer"] == fixture["contrast_layer"] == "REGISTERED_EVIDENCE_RELATION"
    assert fixture["relation_id"] != fixture["contrast_relation_id"]
    assert item["correct_choice_id"] == "COMPUTATIONAL_DEPENDENCY"


def test_learning_history_contract_is_local_bounded_and_not_workspace_provenance():
    contract = load(CONTRACT)
    workspace_schema = load(ROOT / "schemas/workspace.schema.json")

    assert contract["history_storage_key"].startswith("cem.active-understanding.")
    assert 1 <= contract["max_history_records"] <= 100
    assert contract["confidence_scale"] == ["low", "medium", "high"]
    assert "learning" not in json.dumps(workspace_schema).lower()
    assert "challenge" not in json.dumps(workspace_schema).lower()
