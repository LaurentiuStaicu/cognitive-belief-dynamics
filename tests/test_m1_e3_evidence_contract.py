from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "model/contracts/m1_e3_evidence_contract.json"
SCHEMA_PATH = ROOT / "schemas/m1_e3_evidence_contract.schema.json"


def load_contract() -> dict:
    return json.loads(CONTRACT_PATH.read_text())


def test_m1_e3_phase_a_contract_validates_against_schema():
    contract = load_contract()
    schema = json.loads(SCHEMA_PATH.read_text())
    errors = sorted(
        Draft202012Validator(schema).iter_errors(contract),
        key=lambda error: list(error.path),
    )
    assert not errors, "\n".join(
        f"{'/'.join(map(str, error.path))}: {error.message}" for error in errors
    )


def test_m1_e3_phase_a_selects_exactly_one_cue_and_preserves_alternative():
    contract = load_contract()
    selected = contract["candidate_decision"]["selected"]
    deferred = contract["candidate_decision"]["deferred"]

    assert selected["id"] == "CANDIDATE_N"
    assert selected["cue"] == "Hneg"
    assert selected["decision"] == "SELECTED_FOR_NEXT_PHASE"

    assert len(deferred) == 1
    assert deferred[0]["id"] == "CANDIDATE_S"
    assert deferred[0]["cue"] == "Hsimp"
    assert deferred[0]["decision"] == "DEFERRED_NOT_REJECTED"


def test_m1_e3_source_ids_are_unique_and_independence_groups_are_explicit():
    sources = load_contract()["sources"]
    ids = [source["id"] for source in sources]
    assert len(ids) == len(set(ids))

    by_id = {source["id"]: source for source in sources}
    upworthy = {
        "SRC.M1.E3.ROBERTSON.2023",
        "SRC.M1.E3.MATIAS_ARCHIVE.2021",
        "SRC.M1.E3.MATIAS_CORRECTION.2024",
        "SRC.M1.E3.GLIGORIC.2023",
        "SRC.M1.E3.SHULMAN_UPWORTHY.2024",
    }
    assert {
        by_id[source_id]["independence_group"] for source_id in upworthy
    } == {"UPWORTHY_ARCHIVE_2013_2015"}

    # The APS 2026 presentation is supplemental provenance for the Nickl preprint,
    # not a second independent study record.
    nickl = by_id["SRC.M1.E3.NICKL.2025"]
    assert nickl["independence_group"] == "NICKL_ATTENTION_ECONOMY_2025"
    assert any("psychologicalscience.org" in url for url in nickl["supplemental_urls"])
    assert not any("APS" in source["id"] for source in sources)


def test_m1_e3_contract_records_upworthy_integrity_and_reproducibility_constraints():
    contract = load_contract()
    sources = {source["id"]: source for source in contract["sources"]}

    correction = sources["SRC.M1.E3.MATIAS_CORRECTION.2024"]
    assert correction["evidence_role"] == "INTEGRITY_CORRECTION"
    assert "randomization" in correction["notes"].lower()

    operationalization = contract["operationalization"]
    assert operationalization["selected_strategy"] == "PRECOMPUTED_CONTROLLED_CUE"
    assert operationalization["runtime_lexicon_dependency"] is False
    assert operationalization["exact_replication_claim"] is False

    restricted = set(operationalization["restricted_resources_not_redistributed"])
    assert "LIWC software and dictionaries" in restricted
    assert "NRC sentiment/emotion lexicons" in restricted
    assert "Washington Post Study Set 1 headline data" in restricted


def test_m1_e3_platform_target_preserves_native_counts_and_effect_metric():
    target = load_contract()["empirical_target"]
    design = target["design"]

    assert design["design_family"] == "PLATFORM_AB_TEST_ARCHIVE"
    assert design["n_experiments"] == 12448
    assert design["n_variants"] == 53699
    assert design["n_impressions_min"] == 205_000_000
    assert design["n_clicks"] == 2_778_124

    contexts = {item["metric"]: item for item in target["effect_context"]}
    assert contexts["LOG_ODDS_COEFFICIENT"]["value"] == 0.015
    assert contexts["RELATIVE_CHANGE_PERCENT"]["value"] == 2.3
    assert all(item["use"] == "MAGNITUDE_CONTEXT_ONLY" for item in contexts.values())


def test_m1_e3_phase_a_contract_preserves_historical_pre_promotion_gate():
    contract = load_contract()
    gate = contract["promotion_gate"]

    assert gate["active_registry_mutation_allowed"] is False
    assert gate["executable_equation_allowed"] is False
    assert gate["ui_allowed"] is False
    assert "no_beta_neg_value" in contract["forbidden_changes"]


def test_m1_e3_phase_b_promotion_matches_the_approved_phase_a_contract():
    contract = load_contract()

    active_variables = {
        item["id"] for item in json.loads((ROOT / "model/variables.json").read_text())
    }
    active_validations = {
        item["id"] for item in json.loads((ROOT / "model/validation_tests.json").read_text())
    }
    active_targets = {
        item["id"]: item
        for item in json.loads((ROOT / "model/empirical_targets.json").read_text())
    }

    assert contract["candidate_decision"]["selected"]["cue"] == "Hneg"

    assert {
        "VAR.HEADLINE.NEGATIVITY",
        "VAR.ACCESS.PROBABILITY",
        "VAR.ACCESS",
        "VAR.PREVIEW.IMPRESSION",
    }.issubset(active_variables)

    assert {
        "VAL.M1.004",
        "VAL.M1.N04",
        "VAL.M1.N05",
        "VAL.M1.N06",
    }.issubset(active_validations)

    target = active_targets["TARGET.M1.E3.ROBERTSON_2023"]
    planned = contract["empirical_target"]
    assert target["study"]["n_experiments"] == planned["design"]["n_experiments"]
    assert target["study"]["n_variants"] == planned["design"]["n_variants"]
    assert target["study"]["n_impressions_min"] == planned["design"]["n_impressions_min"]
    assert target["study"]["n_clicks"] == planned["design"]["n_clicks"]

    active_effects = {item["metric"]: item for item in target["effects"]}
    planned_effects = {item["metric"]: item for item in planned["effect_context"]}
    assert active_effects["LOG_ODDS_COEFFICIENT"]["estimate"] == planned_effects["LOG_ODDS_COEFFICIENT"]["value"]
    assert active_effects["RELATIVE_CHANGE_PERCENT"]["estimate"] == planned_effects["RELATIVE_CHANGE_PERCENT"]["value"]


def test_m1_e3_phase_b_advances_evidence_snapshot_but_not_phase_a_contract():
    contract = load_contract()
    snapshot = json.loads((ROOT / "model/evidence_snapshot.json").read_text())

    assert snapshot["id"] == "EVIDENCE.M1.2026-09-16.r1"

    def all_keys(value):
        if isinstance(value, dict):
            for key, item in value.items():
                yield key
                yield from all_keys(item)
        elif isinstance(value, list):
            for item in value:
                yield from all_keys(item)

    keys = set(all_keys(contract))
    assert "beta_neg" not in keys
    assert "equation" not in keys
    assert "functional_form" not in keys
