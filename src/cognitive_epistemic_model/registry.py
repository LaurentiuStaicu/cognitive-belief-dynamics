from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


class RegistryError(ValueError):
    pass


def load_json(path: str | Path) -> Any:
    with Path(path).open("r", encoding="utf-8") as f:
        return json.load(f)


def validate_items(items: list[dict], schema: dict) -> None:
    validator = Draft202012Validator(schema)
    errors = []
    for idx, item in enumerate(items):
        for err in validator.iter_errors(item):
            errors.append(f"item {idx}: {err.message}")
    if errors:
        raise RegistryError("\n".join(errors))


def validate_model_dir(model_dir: str | Path, schema_dir: str | Path) -> dict[str, int]:
    model_dir = Path(model_dir)
    schema_dir = Path(schema_dir)

    modules = load_json(model_dir / "modules.json")
    variables = load_json(model_dir / "variables.json")
    links = load_json(model_dir / "links.json")

    validate_items(modules, load_json(schema_dir / "module.schema.json"))
    validate_items(variables, load_json(schema_dir / "variable.schema.json"))
    validate_items(links, load_json(schema_dir / "link.schema.json"))

    for name, items in (("modules", modules), ("variables", variables), ("links", links)):
        duplicates = sorted(key for key, count in Counter(x["id"] for x in items).items() if count > 1)
        if duplicates:
            raise RegistryError(f"duplicate {name} IDs: {duplicates}")

    module_ids = {x["id"] for x in modules}
    variable_ids = {x["id"] for x in variables}

    missing_modules = sorted({v["conceptual_module"] for v in variables} - module_ids)
    if missing_modules:
        raise RegistryError(f"unknown module references: {missing_modules}")

    unresolved = []
    for link in links:
        if link["source"] not in variable_ids:
            unresolved.append((link["id"], "source", link["source"]))
        if link["target"] not in variable_ids:
            unresolved.append((link["id"], "target", link["target"]))
    if unresolved:
        raise RegistryError(f"unresolved variable references: {unresolved}")

    return {"modules": len(modules), "variables": len(variables), "links": len(links)}
