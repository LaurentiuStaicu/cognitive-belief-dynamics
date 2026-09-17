from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "model/semantic_index.json"
GENERATED = ROOT / "web/src/generated/semantic_index.json"
ADAPTER = ROOT / "web/src/semantic.ts"
MAIN = ROOT / "web/src/main.ts"
THEORY = ROOT / "web/src/theory-reader.ts"
SYNC = ROOT / "web/scripts/sync-model.mjs"


def test_web_generated_semantic_index_matches_canonical_byte_for_byte():
    assert GENERATED.read_bytes() == CANONICAL.read_bytes()


def test_web_semantic_adapter_exposes_canonical_lookup_surface():
    source = ADAPTER.read_text(encoding="utf-8")
    for symbol in (
        "semanticEntity",
        "semanticRelation",
        "semanticLabel",
        "semanticRelationsFor",
        "assertSemanticCoverage",
    ):
        assert f"function {symbol}" in source
    assert "generated/semantic_index.json" in source


def test_web_semantic_index_has_expected_oa1_surface():
    index = json.loads(GENERATED.read_text(encoding="utf-8"))
    assert len(index["entities"]) == 133
    assert len(index["relations"]) == 226
    layers = {}
    for relation in index["relations"]:
        layers[relation["layer"]] = layers.get(relation["layer"], 0) + 1
    assert layers == {
        "REGISTERED_EVIDENCE_RELATION": 10,
        "COMPUTATIONAL_DEPENDENCY": 17,
        "DOCUMENTATION_RELATION": 199,
    }


def test_registry_and_theory_consume_semantic_identity_without_replacing_registries():
    main = MAIN.read_text(encoding="utf-8")
    theory = THEORY.read_text(encoding="utf-8")

    assert "assertSemanticCoverage" in main
    assert "semanticLabel" in main
    assert "semanticEntity" in theory
    assert "semanticLabel" in theory

    # Detailed scientific metadata remains in the specialized registries.
    assert "load<Variable[]>('variables')" in main
    assert "load<Link[]>('links')" in main
    assert "TheoryVariable" in theory


def test_prebuild_sync_refreshes_semantic_adapter_artifact():
    source = SYNC.read_text(encoding="utf-8")
    assert "semantic_index" in source
    assert "computational_dependencies" in source
