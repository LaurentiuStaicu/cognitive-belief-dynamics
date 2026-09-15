from pathlib import Path
import json
import re
import shutil

import pytest

from cognitive_epistemic_model.theory import TheoryContractError, extract_tokens, validate_theory_contract

ROOT = Path(__file__).resolve().parents[1]


def test_theory_contract_has_complete_bilingual_phase_c_corpus():
    counts = validate_theory_contract(
        root=ROOT,
        model_dir=ROOT / "model",
        schema_dir=ROOT / "schemas",
    )
    assert counts["theory_chapters"] == 16
    assert counts["theory_glossary"] >= 15
    assert counts["theory_tokens"] >= 60
    assert counts["theory_code_refs"] >= 10

    chapters = json.loads((ROOT / "model/theory_index.json").read_text())
    assert [chapter["order"] for chapter in chapters] == list(range(16))
    for chapter in chapters:
        for lang in ("ro", "en"):
            path = ROOT / chapter["source_paths"][lang]
            assert path.is_file()
            text = path.read_text()
            assert text.lstrip().startswith("# ")
            assert "Schelet Alpha 0.4.1a1" not in text
            assert "Phase A. Conținutul teoretic complet nu este încă redactat." not in text
            assert "Phase A. Full theoretical content has not yet been drafted." not in text
            words = re.findall(r"\b[\w’'-]+\b", text, flags=re.UNICODE)
            assert len(words) >= 250, f"{path}: only {len(words)} words"
            assert text.count("\n## ") >= 5, f"{path}: insufficient explanatory structure"

    roles = {
        source["role"]
        for chapter in chapters
        for source in chapter["sources"]
    }
    assert {"MODEL_EVIDENCE", "BACKGROUND_THEORY", "INTERPRETIVE_SOURCE"} <= roles


def test_theory_index_covers_every_declared_conceptual_module():
    chapters = json.loads((ROOT / "model/theory_index.json").read_text())
    modules = json.loads((ROOT / "model/modules.json").read_text())
    covered = {
        module_id
        for chapter in chapters
        for module_id in chapter.get("module_ids", [])
    }
    declared = {module["id"] for module in modules}
    assert covered == declared, f"missing={sorted(declared - covered)} extra={sorted(covered - declared)}"


def test_romanian_theory_metadata_avoids_untranslated_editorial_jargon():
    chapters = json.loads((ROOT / "model/theory_index.json").read_text())
    discouraged = {
        "baseline",
        "pool",
        "ranking",
        "framing",
        "task-specific",
        "nested",
        "engagement",
        "ground truth",
        "provenance",
        "pattern-tests",
    }
    for chapter in chapters:
        prose = " ".join(
            [
                chapter["label"]["ro"],
                chapter["summary"]["ro"],
                chapter["what_it_does_not_claim"]["ro"],
            ]
        ).lower()
        found = sorted(term for term in discouraged if term in prose)
        assert not found, f"{chapter['id']}: untranslated editorial jargon {found}"


def test_bilingual_chapter_titles_and_section_structure_match_index():
    chapters = json.loads((ROOT / "model/theory_index.json").read_text())
    for chapter in chapters:
        texts = {}
        for lang in ("ro", "en"):
            path = ROOT / chapter["source_paths"][lang]
            text = path.read_text()
            texts[lang] = text
            first_heading = next(line[2:] for line in text.splitlines() if line.startswith("# "))
            assert first_heading == chapter["label"][lang], (
                f"{chapter['id']} {lang}: index label {chapter['label'][lang]!r} "
                f"!= chapter H1 {first_heading!r}"
            )
        assert texts["ro"].count("\n## ") == texts["en"].count("\n## "), (
            f"{chapter['id']}: Romanian/English section counts diverge"
        )


def test_token_extractor_supports_all_phase_a_reference_kinds():
    sample = " ".join(
        [
            "[[VAR:F]]",
            "[[MODULE:MOD.14]]",
            "[[MECH:repetition]]",
            "[[VAL:VAL.M0.001]]",
            "[[REF:REF.DECHENE.2010]]",
            "[[VIEW:runs:repetition:4]]",
            "[[CODE:m0.update_familiarity]]",
            "[[CONCEPT:m0]]",
        ]
    )
    assert {kind for kind, _ in extract_tokens(sample)} == {
        "VAR", "MODULE", "MECH", "VAL", "REF", "VIEW", "CODE", "CONCEPT"
    }


def _copy_theory_fixture(tmp_path: Path) -> Path:
    root = tmp_path / "checkout"
    shutil.copytree(ROOT / "model", root / "model")
    shutil.copytree(ROOT / "schemas", root / "schemas")
    shutil.copytree(ROOT / "docs/theory", root / "docs/theory")
    shutil.copytree(ROOT / "src", root / "src")
    return root


def test_unresolved_theory_token_is_rejected(tmp_path):
    root = _copy_theory_fixture(tmp_path)
    path = root / "docs/theory/en/05-repetition-familiarity-truth.md"
    path.write_text(path.read_text() + "\n[[VAR:DOES_NOT_EXIST]]\n")
    with pytest.raises(TheoryContractError, match="unresolved VAR token"):
        validate_theory_contract(root=root, model_dir=root / "model", schema_dir=root / "schemas")


def test_interpretive_item_cannot_be_silently_marked_executable(tmp_path):
    root = _copy_theory_fixture(tmp_path)
    path = root / "model/theory_glossary.json"
    glossary = json.loads(path.read_text())
    item = next(entry for entry in glossary if entry["token"] == "reflective-distance")
    item["executable"] = True
    path.write_text(json.dumps(glossary))
    with pytest.raises(TheoryContractError, match="cannot be executable"):
        validate_theory_contract(root=root, model_dir=root / "model", schema_dir=root / "schemas")


def test_broken_theory_code_reference_is_rejected(tmp_path):
    root = _copy_theory_fixture(tmp_path)
    path = root / "model/theory_index.json"
    chapters = json.loads(path.read_text())
    chapter = next(item for item in chapters if item["id"] == "THEORY.05.REPETITION_FAMILIARITY_TRUTH")
    chapter["code_refs"][0]["symbol"] = "function_that_does_not_exist"
    path.write_text(json.dumps(chapters))
    with pytest.raises(TheoryContractError, match="unresolved code ref"):
        validate_theory_contract(root=root, model_dir=root / "model", schema_dir=root / "schemas")


def test_missing_bilingual_source_is_rejected(tmp_path):
    root = _copy_theory_fixture(tmp_path)
    (root / "docs/theory/ro/00-ce-este-cem.md").unlink()
    with pytest.raises(TheoryContractError, match="missing theory source"):
        validate_theory_contract(root=root, model_dir=root / "model", schema_dir=root / "schemas")
