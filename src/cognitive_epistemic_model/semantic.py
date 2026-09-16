from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


SEMANTIC_SCHEMA_VERSION = "1"


class SemanticIndexError(ValueError):
    pass


def _load(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _source(path: str, source_id: str) -> dict[str, str]:
    return {"path": path, "source_id": source_id}


def _labels(
    preferred: dict[str, str],
    *,
    alternative: dict[str, list[str]] | None = None,
) -> dict[str, Any]:
    value: dict[str, Any] = {"preferred": preferred}
    cleaned: dict[str, list[str]] = {}
    for lang, labels in (alternative or {}).items():
        unique = sorted({label for label in labels if label and label not in preferred.values()})
        if unique:
            cleaned[lang] = unique
    if cleaned:
        value["alternative"] = cleaned
    return value


def _documentation_relation(
    *,
    source_id: str,
    target_id: str,
    relation_type: str,
    source_path: str,
) -> dict[str, Any]:
    return {
        "id": f"SEMREL.DOC.{source_id}.{relation_type}.{target_id}",
        "layer": "DOCUMENTATION_RELATION",
        "source": source_id,
        "target": target_id,
        "source_record": _source(source_path, source_id),
        "relation_type": relation_type,
    }


def build_semantic_index(model_dir: str | Path) -> dict[str, Any]:
    """Build the OA-1 semantic adapter from authoritative CEM registries.

    The returned index is descriptive metadata only. It does not execute or alter
    scientific equations and does not infer stronger epistemic status than the
    source registries provide.
    """

    model_dir = Path(model_dir)

    baseline = _load(model_dir / "contracts" / "oa0_optimization_baseline.json")
    variables = _load(model_dir / "variables.json")
    modules = _load(model_dir / "modules.json")
    references = _load(model_dir / "references.json")
    validations = _load(model_dir / "validation_tests.json")
    targets = _load(model_dir / "empirical_targets.json")
    chapters = _load(model_dir / "theory_index.json")
    glossary = _load(model_dir / "theory_glossary.json")
    links = _load(model_dir / "links.json")
    computational = _load(model_dir / "computational_dependencies.json")

    entities: list[dict[str, Any]] = []
    relations: list[dict[str, Any]] = []

    validation_by_id = {item["id"]: item for item in validations}
    mechanism_by_token = {
        item["token"]: item["id"]
        for item in glossary
        if item["kind"] == "MECHANISM"
    }

    for item in variables:
        entity: dict[str, Any] = {
            "id": item["id"],
            "semantic_type": "VARIABLE",
            "labels": _labels(
                item["label"],
                alternative={"und": [item["short_name"]]},
            ),
            "source": _source("model/variables.json", item["id"]),
            "short_name": item["short_name"],
            "summary": {"en": item["definition"]},
            "related_ids": [item["conceptual_module"]],
        }
        entities.append(entity)

    for item in modules:
        entities.append(
            {
                "id": item["id"],
                "semantic_type": "MODULE",
                "labels": _labels(item["label"]),
                "source": _source("model/modules.json", item["id"]),
            }
        )

    for item in computational["nodes"]:
        entities.append(
            {
                "id": item["semantic_id"],
                "semantic_type": "COMPUTATIONAL_NODE",
                "labels": _labels(
                    item["label"],
                    alternative={"und": [item["id"]]},
                ),
                "source": _source(
                    "model/computational_dependencies.json",
                    item["id"],
                ),
                "short_name": item["id"],
            }
        )

    for item in references:
        entities.append(
            {
                "id": item["id"],
                "semantic_type": "REFERENCE",
                "labels": _labels({"und": item["citation"]}),
                "source": _source("model/references.json", item["id"]),
            }
        )

    for item in validations:
        entities.append(
            {
                "id": item["id"],
                "semantic_type": "VALIDATION",
                "labels": _labels({"en": item["name"]}),
                "source": _source("model/validation_tests.json", item["id"]),
                "summary": {"en": item["pattern"]},
            }
        )

    for item in targets:
        related = [item["pattern_id"], item["evidence_ref"]]
        for field in ("provenance_refs", "integrity_refs", "counterevidence_refs"):
            related.extend(item.get(field, []))
        # Empirical targets currently have no dedicated bilingual display label.
        # Preserve identity instead of inventing a stronger or translated claim.
        linked_validation = validation_by_id[item["pattern_id"]]
        entities.append(
            {
                "id": item["id"],
                "semantic_type": "EMPIRICAL_TARGET",
                "labels": _labels(
                    {"und": item["id"]},
                    alternative={"en": [linked_validation["name"]]},
                ),
                "source": _source("model/empirical_targets.json", item["id"]),
                "summary": {"en": item["model_match"]},
                "related_ids": sorted(set(related)),
            }
        )

    for item in chapters:
        related = (
            list(item["prerequisites"])
            + list(item["module_ids"])
            + list(item["variable_ids"])
            + list(item["validation_ids"])
            + list(item["evidence_refs"])
        )
        mechanism_ids: list[str] = []
        for token in item["mechanism_ids"]:
            try:
                mechanism_ids.append(mechanism_by_token[token])
            except KeyError as exc:
                raise SemanticIndexError(
                    f"{item['id']}: unresolved mechanism token {token!r}"
                ) from exc
        related.extend(mechanism_ids)

        entities.append(
            {
                "id": item["id"],
                "semantic_type": "THEORY_CHAPTER",
                "labels": _labels(item["label"]),
                "source": _source("model/theory_index.json", item["id"]),
                "status_facets": {"source_tags": item["epistemic_status"]},
                "summary": item["summary"],
                "related_ids": sorted(set(related)),
            }
        )

        for target_id in item["module_ids"]:
            relations.append(
                _documentation_relation(
                    source_id=item["id"],
                    target_id=target_id,
                    relation_type="USES_MODULE",
                    source_path="model/theory_index.json",
                )
            )
        for target_id in item["variable_ids"]:
            relations.append(
                _documentation_relation(
                    source_id=item["id"],
                    target_id=target_id,
                    relation_type="USES_VARIABLE",
                    source_path="model/theory_index.json",
                )
            )
        for target_id in mechanism_ids:
            relations.append(
                _documentation_relation(
                    source_id=item["id"],
                    target_id=target_id,
                    relation_type="DESCRIBES_MECHANISM",
                    source_path="model/theory_index.json",
                )
            )
        for target_id in item["validation_ids"]:
            relations.append(
                _documentation_relation(
                    source_id=item["id"],
                    target_id=target_id,
                    relation_type="REFERENCES_VALIDATION",
                    source_path="model/theory_index.json",
                )
            )
        for target_id in item["evidence_refs"]:
            relations.append(
                _documentation_relation(
                    source_id=item["id"],
                    target_id=target_id,
                    relation_type="CITES_REFERENCE",
                    source_path="model/theory_index.json",
                )
            )
        for target_id in item["prerequisites"]:
            relations.append(
                _documentation_relation(
                    source_id=item["id"],
                    target_id=target_id,
                    relation_type="PREREQUISITE_CHAPTER",
                    source_path="model/theory_index.json",
                )
            )

    for item in glossary:
        role = (
            "MECHANISM_DESCRIPTOR"
            if item["kind"] == "MECHANISM"
            else "CONCEPT_DESCRIPTOR"
        )
        entities.append(
            {
                "id": item["id"],
                "semantic_type": "GLOSSARY_ENTRY",
                "semantic_roles": [role],
                "labels": _labels(
                    item["label"],
                    alternative={"und": [item["token"]]},
                ),
                "source": _source("model/theory_glossary.json", item["id"]),
                "status_facets": {"source_tags": item["epistemic_status"]},
                "summary": item["short_definition"],
                "related_ids": sorted(set(item["related_chapters"])),
            }
        )
        for target_id in item["related_chapters"]:
            relations.append(
                _documentation_relation(
                    source_id=item["id"],
                    target_id=target_id,
                    relation_type="RELATED_CHAPTER",
                    source_path="model/theory_glossary.json",
                )
            )

    for item in links:
        relations.append(
            {
                "id": item["id"],
                "layer": "REGISTERED_EVIDENCE_RELATION",
                "source": item["source"],
                "target": item["target"],
                "source_record": _source("model/links.json", item["id"]),
                "relation_type": item["relation_type"],
                "polarity": item["polarity"],
                "status_facets": {
                    "phenomenon_evidence": item["phenomenon_evidence_status"],
                    "mechanism_evidence": item["mechanism_evidence_status"],
                    "functional_form": item["functional_form_status"],
                },
                "evidence_refs": item["evidence_refs"],
            }
        )

    for item in computational["dependencies"]:
        relation = {
            "id": item["id"],
            "layer": "COMPUTATIONAL_DEPENDENCY",
            "source": item["source_semantic_id"],
            "target": item["target_semantic_id"],
            "source_record": _source(
                "model/computational_dependencies.json",
                item["id"],
            ),
            "formula": item["formula"],
            "code_file": item["code_file"],
        }
        if item.get("registered_relation_id"):
            relation["registered_relation_id"] = item["registered_relation_id"]
        relations.append(relation)

    entities.sort(key=lambda item: item["id"])
    relations.sort(key=lambda item: item["id"])

    entity_ids = [item["id"] for item in entities]
    relation_ids = [item["id"] for item in relations]
    if len(entity_ids) != len(set(entity_ids)):
        raise SemanticIndexError("duplicate semantic entity IDs")
    if len(relation_ids) != len(set(relation_ids)):
        raise SemanticIndexError("duplicate semantic relation IDs")

    entity_id_set = set(entity_ids)
    for relation in relations:
        if relation["source"] not in entity_id_set:
            raise SemanticIndexError(
                f"{relation['id']}: unresolved semantic source {relation['source']}"
            )
        if relation["target"] not in entity_id_set:
            raise SemanticIndexError(
                f"{relation['id']}: unresolved semantic target {relation['target']}"
            )
        for ref_id in relation.get("evidence_refs", []):
            if ref_id not in entity_id_set:
                raise SemanticIndexError(
                    f"{relation['id']}: unresolved semantic evidence reference {ref_id}"
                )

    return {
        "schema_version": SEMANTIC_SCHEMA_VERSION,
        "baseline_contract": baseline["contract_id"],
        "source_paths": sorted(
            [
                "model/contracts/oa0_optimization_baseline.json",
                "model/computational_dependencies.json",
                "model/empirical_targets.json",
                "model/links.json",
                "model/modules.json",
                "model/references.json",
                "model/theory_glossary.json",
                "model/theory_index.json",
                "model/validation_tests.json",
                "model/variables.json",
            ]
        ),
        "entities": entities,
        "relations": relations,
    }


def validate_semantic_index(
    index: dict[str, Any],
    schema_path: str | Path,
) -> None:
    schema = _load(Path(schema_path))
    Draft202012Validator.check_schema(schema)
    errors = sorted(
        Draft202012Validator(schema).iter_errors(index),
        key=lambda error: list(error.absolute_path),
    )
    if errors:
        raise SemanticIndexError(
            "\n".join(
                f"{'/'.join(str(part) for part in error.absolute_path)}: {error.message}"
                for error in errors
            )
        )


def semantic_index_json(index: dict[str, Any]) -> str:
    """Canonical deterministic JSON serialization for generated artifacts."""
    return json.dumps(
        index,
        indent=2,
        ensure_ascii=False,
        sort_keys=True,
    ) + "\n"
