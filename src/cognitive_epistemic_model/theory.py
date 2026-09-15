from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


TOKEN_RE = re.compile(r"\[\[(VAR|MODULE|MECH|VAL|REF|VIEW|CODE|CONCEPT):([^\]]+)\]\]")
ALLOWED_VIEW_PREFIXES = {"learning", "planning", "structure", "runs", "comparison", "process", "reference"}


class TheoryContractError(ValueError):
    pass


def _load(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _validate_items(items: list[dict], schema: dict, label: str) -> None:
    validator = Draft202012Validator(schema)
    errors: list[str] = []
    for idx, item in enumerate(items):
        for err in validator.iter_errors(item):
            errors.append(f"{label} item {idx}: {err.message}")
    if errors:
        raise TheoryContractError("\n".join(errors))


def _duplicates(values: list[str]) -> list[str]:
    return sorted(value for value, count in Counter(values).items() if count > 1)


def _resolve_source(root: Path, source_path: str) -> Path:
    direct = root / source_path
    if direct.is_file():
        return direct
    prefix = "docs/theory/"
    if source_path.startswith(prefix):
        bundled = root / "theory" / source_path[len(prefix):]
        if bundled.is_file():
            return bundled
    raise TheoryContractError(f"missing theory source: {source_path}")


def _code_symbol_exists(root: Path, ref: dict) -> bool:
    path = root / ref["path"]
    if not path.is_file():
        return False
    text = path.read_text(encoding="utf-8")
    if ref["language"] == "PYTHON":
        pattern = rf"^(?:async\s+)?(?:def|class)\s+{re.escape(ref['symbol'])}\b"
    else:
        pattern = rf"\b(?:function|class|const|let|var)\s+{re.escape(ref['symbol'])}\b"
    return re.search(pattern, text, flags=re.MULTILINE) is not None


def extract_tokens(text: str) -> list[tuple[str, str]]:
    return [(kind, value.strip()) for kind, value in TOKEN_RE.findall(text)]


def validate_theory_contract(
    *,
    root: str | Path,
    model_dir: str | Path,
    schema_dir: str | Path,
    validate_sources: bool = True,
    validate_code: bool = True,
) -> dict[str, int]:
    root = Path(root)
    model_dir = Path(model_dir)
    schema_dir = Path(schema_dir)

    chapters = _load(model_dir / "theory_index.json")
    glossary = _load(model_dir / "theory_glossary.json")
    variables = _load(model_dir / "variables.json")
    modules = _load(model_dir / "modules.json")
    validations = _load(model_dir / "validation_tests.json")
    references = _load(model_dir / "references.json")

    _validate_items(chapters, _load(schema_dir / "theory_index.schema.json"), "theory_index")
    _validate_items(glossary, _load(schema_dir / "theory_glossary.schema.json"), "theory_glossary")

    duplicate_chapters = _duplicates([item["id"] for item in chapters])
    duplicate_orders = _duplicates([str(item["order"]) for item in chapters])
    duplicate_glossary_ids = _duplicates([item["id"] for item in glossary])
    duplicate_glossary_tokens = _duplicates([f"{item['kind']}:{item['token']}" for item in glossary])
    if duplicate_chapters:
        raise TheoryContractError(f"duplicate theory chapter IDs: {duplicate_chapters}")
    if duplicate_orders:
        raise TheoryContractError(f"duplicate theory chapter orders: {duplicate_orders}")
    if duplicate_glossary_ids:
        raise TheoryContractError(f"duplicate theory glossary IDs: {duplicate_glossary_ids}")
    if duplicate_glossary_tokens:
        raise TheoryContractError(f"duplicate theory glossary tokens: {duplicate_glossary_tokens}")

    chapter_ids = {item["id"] for item in chapters}
    module_ids = {item["id"] for item in modules}
    variable_ids = {item["id"] for item in variables}
    variable_tokens = variable_ids | {item["short_name"] for item in variables}
    validation_ids = {item["id"] for item in validations}
    reference_ids = {item["id"] for item in references}
    mechanism_tokens = {
        item["token"] for item in glossary if item["kind"] == "MECHANISM"
    }
    concept_tokens = {
        item["token"] for item in glossary if item["kind"] == "CONCEPT"
    }

    code_refs: dict[str, dict] = {}
    for chapter in chapters:
        missing_prereq = set(chapter["prerequisites"]) - chapter_ids
        missing_modules = set(chapter["module_ids"]) - module_ids
        missing_variables = set(chapter["variable_ids"]) - variable_ids
        missing_mechanisms = set(chapter["mechanism_ids"]) - mechanism_tokens
        missing_validations = set(chapter["validation_ids"]) - validation_ids
        missing_evidence = set(chapter["evidence_refs"]) - reference_ids
        if missing_prereq:
            raise TheoryContractError(f"{chapter['id']}: unresolved prerequisites {sorted(missing_prereq)}")
        if missing_modules:
            raise TheoryContractError(f"{chapter['id']}: unresolved modules {sorted(missing_modules)}")
        if missing_variables:
            raise TheoryContractError(f"{chapter['id']}: unresolved variables {sorted(missing_variables)}")
        if missing_mechanisms:
            raise TheoryContractError(f"{chapter['id']}: unresolved mechanisms {sorted(missing_mechanisms)}")
        if missing_validations:
            raise TheoryContractError(f"{chapter['id']}: unresolved validation IDs {sorted(missing_validations)}")
        if missing_evidence:
            raise TheoryContractError(f"{chapter['id']}: unresolved evidence refs {sorted(missing_evidence)}")
        for source in chapter["sources"]:
            if source["role"] == "MODEL_EVIDENCE" and source["ref"] not in reference_ids:
                raise TheoryContractError(f"{chapter['id']}: unresolved model-evidence source {source['ref']}")
        for ref in chapter["code_refs"]:
            if ref["id"] in code_refs:
                raise TheoryContractError(f"duplicate code ref ID: {ref['id']}")
            code_refs[ref["id"]] = ref
            if validate_code and not _code_symbol_exists(root, ref):
                raise TheoryContractError(
                    f"{chapter['id']}: unresolved code ref {ref['id']} -> {ref['path']}::{ref['symbol']}"
                )

    for entry in glossary:
        missing_chapters = set(entry["related_chapters"]) - chapter_ids
        if missing_chapters:
            raise TheoryContractError(f"{entry['id']}: unresolved related chapters {sorted(missing_chapters)}")
        statuses = set(entry["epistemic_status"])
        if entry["executable"] and (statuses & {"CONCEPTUAL", "INTERPRETIVE"}) and "EXECUTABLE" not in statuses:
            raise TheoryContractError(
                f"{entry['id']}: conceptual/interpretive item cannot be executable without EXECUTABLE status"
            )
        if entry["kind"] == "MECHANISM" and entry["token"] not in {
            mechanism for chapter in chapters for mechanism in chapter["mechanism_ids"]
        }:
            raise TheoryContractError(f"{entry['id']}: mechanism token is not used by any theory chapter")

    token_count = 0
    if validate_sources:
        for chapter in chapters:
            for lang in ("ro", "en"):
                path = _resolve_source(root, chapter["source_paths"][lang])
                text = path.read_text(encoding="utf-8")
                if not text.lstrip().startswith("# "):
                    raise TheoryContractError(f"{chapter['id']}:{lang}: theory source must start with an h1")
                for kind, value in extract_tokens(text):
                    token_count += 1
                    if kind == "VAR" and value not in variable_tokens:
                        raise TheoryContractError(f"{chapter['id']}:{lang}: unresolved VAR token {value}")
                    if kind == "MODULE" and value not in module_ids:
                        raise TheoryContractError(f"{chapter['id']}:{lang}: unresolved MODULE token {value}")
                    if kind == "MECH" and value not in mechanism_tokens:
                        raise TheoryContractError(f"{chapter['id']}:{lang}: unresolved MECH token {value}")
                    if kind == "VAL" and value not in validation_ids:
                        raise TheoryContractError(f"{chapter['id']}:{lang}: unresolved VAL token {value}")
                    if kind == "REF" and value not in reference_ids:
                        raise TheoryContractError(f"{chapter['id']}:{lang}: unresolved REF token {value}")
                    if kind == "CODE" and value not in code_refs:
                        raise TheoryContractError(f"{chapter['id']}:{lang}: unresolved CODE token {value}")
                    if kind == "CONCEPT" and value not in concept_tokens:
                        raise TheoryContractError(f"{chapter['id']}:{lang}: unresolved CONCEPT token {value}")
                    if kind == "VIEW":
                        prefix = value.split(":", 1)[0]
                        if prefix not in ALLOWED_VIEW_PREFIXES:
                            raise TheoryContractError(f"{chapter['id']}:{lang}: unresolved VIEW token {value}")

    return {
        "theory_chapters": len(chapters),
        "theory_glossary": len(glossary),
        "theory_tokens": token_count,
        "theory_code_refs": len(code_refs),
    }
