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
    references = load_json(model_dir / "references.json")
    subsystems = load_json(model_dir / "subsystems.json")
    processes = load_json(model_dir / "processes.json")
    evidence_snapshot = load_json(model_dir / "evidence_snapshot.json")
    empirical_targets = load_json(model_dir / "empirical_targets.json")
    computational_dependencies = load_json(
        model_dir / "computational_dependencies.json"
    )
    theory_index = load_json(model_dir / "theory_index.json")
    theory_glossary = load_json(model_dir / "theory_glossary.json")

    validate_items(modules, load_json(schema_dir / "module.schema.json"))
    validate_items(variables, load_json(schema_dir / "variable.schema.json"))
    validate_items(links, load_json(schema_dir / "link.schema.json"))
    validate_items(references, load_json(schema_dir / "reference.schema.json"))
    validate_items(subsystems, load_json(schema_dir / "subsystem.schema.json"))
    validate_items(processes, load_json(schema_dir / "process.schema.json"))
    validate_items(empirical_targets, load_json(schema_dir / "empirical_target.schema.json"))
    computational_validator = Draft202012Validator(
        load_json(schema_dir / "computational_dependencies.schema.json")
    )
    computational_errors = sorted(
        computational_validator.iter_errors(computational_dependencies),
        key=lambda err: list(err.path),
    )
    if computational_errors:
        raise RegistryError(
            "\n".join(
                f"computational dependencies: {err.message}"
                for err in computational_errors
            )
        )
    validate_items(theory_index, load_json(schema_dir / "theory_index.schema.json"))
    validate_items(theory_glossary, load_json(schema_dir / "theory_glossary.schema.json"))
    snapshot_validator = Draft202012Validator(load_json(schema_dir / "evidence_snapshot.schema.json"))
    snapshot_errors = sorted(snapshot_validator.iter_errors(evidence_snapshot), key=lambda err: list(err.path))
    if snapshot_errors:
        raise RegistryError("\n".join(f"evidence snapshot: {err.message}" for err in snapshot_errors))

    for name, items in (("modules", modules), ("variables", variables), ("links", links), ("references", references), ("subsystems", subsystems), ("processes", processes), ("empirical_targets", empirical_targets), ("theory_index", theory_index), ("theory_glossary", theory_glossary)):
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

    computational_nodes = computational_dependencies["nodes"]
    computational_edges = computational_dependencies["dependencies"]
    duplicate_node_ids = sorted(
        key
        for key, count in Counter(node["id"] for node in computational_nodes).items()
        if count > 1
    )
    duplicate_node_semantic_ids = sorted(
        key
        for key, count in Counter(
            node["semantic_id"] for node in computational_nodes
        ).items()
        if count > 1
    )
    duplicate_dependency_ids = sorted(
        key
        for key, count in Counter(
            edge["id"] for edge in computational_edges
        ).items()
        if count > 1
    )
    if duplicate_node_ids:
        raise RegistryError(
            f"duplicate computational node IDs: {duplicate_node_ids}"
        )
    if duplicate_node_semantic_ids:
        raise RegistryError(
            "duplicate computational node semantic IDs: "
            f"{duplicate_node_semantic_ids}"
        )
    if duplicate_dependency_ids:
        raise RegistryError(
            f"duplicate computational dependency IDs: {duplicate_dependency_ids}"
        )

    graph_ids = {item["short_name"] for item in variables} | {
        item["id"] for item in computational_nodes
    }
    semantic_endpoint_ids = variable_ids | {
        item["semantic_id"] for item in computational_nodes
    }
    link_ids = {item["id"] for item in links}
    for edge in computational_edges:
        if edge["source"] not in graph_ids or edge["target"] not in graph_ids:
            raise RegistryError(
                f"{edge['id']}: unresolved computational graph endpoint"
            )
        if (
            edge["source_semantic_id"] not in semantic_endpoint_ids
            or edge["target_semantic_id"] not in semantic_endpoint_ids
        ):
            raise RegistryError(
                f"{edge['id']}: unresolved computational semantic endpoint"
            )
        registered = edge.get("registered_relation_id")
        if registered is not None and registered not in link_ids:
            raise RegistryError(
                f"{edge['id']}: unresolved registered relation {registered}"
            )

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
                raise RegistryError(
                    f"unresolved target {field} in {target['id']}: {sorted(missing)}"
                )
        if target["pattern_id"] not in validation_ids:
            raise RegistryError(f"unresolved target pattern reference: {target['id']}")
    for ref in references:
        if ref["url"] != "https://doi.org/" + ref["doi"]:
            raise RegistryError(f"DOI URL mismatch: {ref['id']}")

    from .theory import validate_theory_contract
    root = model_dir.parent
    theory_counts = validate_theory_contract(
        root=root,
        model_dir=model_dir,
        schema_dir=schema_dir,
        validate_sources=True,
        validate_code=(root / "src").is_dir(),
    )

    from .semantic import (
        build_semantic_index,
        semantic_index_json,
        validate_semantic_index,
    )

    semantic_index = build_semantic_index(model_dir)
    validate_semantic_index(
        semantic_index,
        schema_dir / "semantic_index.schema.json",
    )
    semantic_path = model_dir / "semantic_index.json"
    if not semantic_path.is_file():
        raise RegistryError("missing generated semantic index: semantic_index.json")
    if semantic_path.read_text(encoding="utf-8") != semantic_index_json(semantic_index):
        raise RegistryError(
            "generated semantic index is stale; run python scripts/export_semantic.py"
        )

    return {
        "modules": len(modules),
        "variables": len(variables),
        "links": len(links),
        "references": len(references),
        "subsystems": len(subsystems),
        "processes": len(processes),
        "empirical_targets": len(empirical_targets),
        "computational_nodes": len(computational_nodes),
        "computational_dependencies": len(computational_edges),
        "semantic_entities": len(semantic_index["entities"]),
        "semantic_relations": len(semantic_index["relations"]),
        **theory_counts,
    }
