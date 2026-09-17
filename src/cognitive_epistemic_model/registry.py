from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


class RegistryError(ValueError):
    pass


def load_json(path: str | Path) -> Any:
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_items(items: list[dict], schema: dict) -> None:
    validator = Draft202012Validator(schema)
    errors: list[str] = []
    for idx, item in enumerate(items):
        for err in validator.iter_errors(item):
            errors.append(f"item {idx}: {err.message}")
    if errors:
        raise RegistryError("\n".join(errors))


def _validate_object(value: dict, schema: dict, label: str) -> None:
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(value), key=lambda err: list(err.path))
    if errors:
        raise RegistryError("\n".join(f"{label}: {err.message}" for err in errors))


def validate_model_dir(model_dir: str | Path, schema_dir: str | Path) -> dict[str, int]:
    """Validate the canonical scientific registries retained in the model core."""
    model_dir = Path(model_dir)
    schema_dir = Path(schema_dir)

    modules = load_json(model_dir / "modules.json")
    variables = load_json(model_dir / "variables.json")
    links = load_json(model_dir / "links.json")
    references = load_json(model_dir / "references.json")
    subsystems = load_json(model_dir / "subsystems.json")
    processes = load_json(model_dir / "processes.json")
    evidence_snapshot = load_json(model_dir / "evidence_snapshot.json")
    empirical_targets = load_json(model_dir / "empirical_targets.json")
    computational_dependencies = load_json(model_dir / "computational_dependencies.json")

    validate_items(modules, load_json(schema_dir / "module.schema.json"))
    validate_items(variables, load_json(schema_dir / "variable.schema.json"))
    validate_items(links, load_json(schema_dir / "link.schema.json"))
    validate_items(references, load_json(schema_dir / "reference.schema.json"))
    validate_items(subsystems, load_json(schema_dir / "subsystem.schema.json"))
    validate_items(processes, load_json(schema_dir / "process.schema.json"))
    validate_items(empirical_targets, load_json(schema_dir / "empirical_target.schema.json"))
    _validate_object(
        computational_dependencies,
        load_json(schema_dir / "computational_dependencies.schema.json"),
        "computational dependencies",
    )
    _validate_object(
        evidence_snapshot,
        load_json(schema_dir / "evidence_snapshot.schema.json"),
        "evidence snapshot",
    )

    for name, items in (
        ("modules", modules),
        ("variables", variables),
        ("links", links),
        ("references", references),
        ("subsystems", subsystems),
        ("processes", processes),
        ("empirical_targets", empirical_targets),
    ):
        duplicates = sorted(
            key for key, count in Counter(item["id"] for item in items).items() if count > 1
        )
        if duplicates:
            raise RegistryError(f"duplicate {name} IDs: {duplicates}")

    module_ids = {item["id"] for item in modules}
    variable_ids = {item["id"] for item in variables}
    missing_modules = sorted({item["conceptual_module"] for item in variables} - module_ids)
    if missing_modules:
        raise RegistryError(f"unknown module references: {missing_modules}")

    unresolved: list[tuple[str, str, str]] = []
    for link in links:
        if link["source"] not in variable_ids:
            unresolved.append((link["id"], "source", link["source"]))
        if link["target"] not in variable_ids:
            unresolved.append((link["id"], "target", link["target"]))
    if unresolved:
        raise RegistryError(f"unresolved variable references: {unresolved}")

    reference_ids = {ref["id"] for ref in references}
    validation_ids = {item["id"] for item in load_json(model_dir / "validation_tests.json")}
    for link in links:
        missing = set(link["evidence_refs"]) - reference_ids
        if missing:
            raise RegistryError(f"unresolved evidence references in {link['id']}: {sorted(missing)}")
    for target in empirical_targets:
        if target["evidence_ref"] not in reference_ids:
            raise RegistryError(f"unresolved target evidence reference: {target['id']}")
        for field in ("provenance_refs", "integrity_refs", "counterevidence_refs"):
            missing = set(target.get(field, [])) - reference_ids
            if missing:
                raise RegistryError(f"unresolved target {field} in {target['id']}: {sorted(missing)}")
        if target["pattern_id"] not in validation_ids:
            raise RegistryError(f"unresolved target pattern reference: {target['id']}")
    for ref in references:
        if ref["url"] != "https://doi.org/" + ref["doi"]:
            raise RegistryError(f"DOI URL mismatch: {ref['id']}")

    return {
        "modules": len(modules),
        "variables": len(variables),
        "links": len(links),
        "references": len(references),
        "subsystems": len(subsystems),
        "processes": len(processes),
        "empirical_targets": len(empirical_targets),
        "computational_dependencies": len(computational_dependencies["dependencies"]),
    }
