# CEM Semantic Contract — OA-1 / R1 refinement

Status: R1 research decision refining the OA-0 planning contract. No runtime semantic migration occurs in this document-only phase.

## 1. Purpose

The Semantic Spine gives the same scientific object one stable identity across Theory, Mechanisms, Structure, Registry, Search, Workspace, provenance and future GTK/native surfaces.

It is intentionally smaller than a general ontology and begins as a generated adapter/index over existing registries.

## 2. Design rules

1. Stable identifiers outlive labels and translations.
2. Existing repository IDs are canonical by default; stylistic renaming is not a migration goal.
3. Labels are localized presentation; IDs are canonical identity.
4. Scientific status is explicit data, not inferred from CSS or prose.
5. Epistemic status is multidimensional; do not collapse phenomenon evidence, mechanism status, functional-form status, conceptual status and executability into one scalar label.
6. Computational dependency and empirical/evidence-qualified relations are different relation layers.
7. Provenance relations are different from scientific/semantic relations.
8. Existing registries remain authoritative until an OA-1 adapter proves lossless indexing/migration.
9. No UI code may manufacture a stronger epistemic status than the source entity carries.
10. New semantic types are added only when an existing type cannot express a required distinction.

## 3. OA-1 first-slice entity vocabulary

OA-1 indexes entities that already exist authoritatively in the repository:

### Variable

Registered state/input/output quantity with an ontology role and model scope.

### Module

Registered conceptual module.

### Reference

Bibliographic/source record with study type, review scope and provenance metadata.

### Validation

Test or criterion evaluating a specified prediction, negative constraint or invariant.

### EmpiricalTarget

Observable pattern used to test/discriminate model behavior.

### TheoryChapter

Versioned bilingual theory/documentation chapter with explicit cross-links and claim boundaries.

### GlossaryEntry

Bilingual explanatory descriptor. Entries whose current `kind` is `MECHANISM` may expose semantic role `MECHANISM_DESCRIPTOR`.

### ComputationalNode

A non-registered computational input or intermediate output used to explain executable data flow. It is not promoted to a registered psychological variable merely because it is executable.

The broader OA architecture still anticipates future objects such as Claim, Assumption, Prediction, Intervention, Indicator, Observation and Decision, but OA-1 does not invent them before a source-of-truth object exists.

## 4. Relation layers

OA-1 represents relation **layer** before flattening relation semantics.

### Registered evidence-qualified relation

Source: `model/links.json`.

Preserve:

- source/target IDs;
- raw relation type;
- polarity;
- phenomenon evidence status;
- mechanism evidence status;
- functional-form status;
- evidence references;
- bilingual finding and limitation summaries.

These are not interchangeable with computational dependencies.

### Computational dependency

Canonical source after OA-1C: `model/computational_dependencies.json`.

Represents equation/data-flow dependency and code/formula provenance. It does not by itself assert empirical causation.

The web TypeScript layer adapts this canonical data for graph rendering and is not a second scientific metadata source.

### Documentation relation

Theory/glossary cross-links to variables, modules, validations, references and views.

Documentation relations support navigation/search. They do not imply evidential support unless an explicit role says so.

## 5. Epistemic status facets

A single `epistemic_status` field is insufficient for the current repository.

OA-1 uses optional orthogonal facets derived from existing source fields.

Illustrative normalized shape:

```json
{
  "status_facets": {
    "phenomenon_evidence": "EXPERIMENTAL",
    "mechanism": "CANDIDATE",
    "functional_form": "REFERENCE_CANDIDATE",
    "implementation": ["EXECUTABLE"]
  }
}
```

Allowed values must be enumerated from the repository before schema implementation. OA-1 must not create a maturity ordering that implies, for example:

- EXECUTABLE => EMPIRICALLY_VALIDATED;
- CANDIDATE => VALIDATED;
- REFERENCE_CANDIDATE => calibrated law.

Theory/glossary values such as `CONCEPTUAL`, `EMPIRICAL` and `EXECUTABLE` are preserved as source facets/roles rather than silently mapped to a stronger universal status.

## 6. Multilingual labels

Current bilingual labels remain authoritative.

The generated semantic index may normalize them to:

```json
{
  "preferred_labels": {
    "ro": "...",
    "en": "..."
  },
  "alternative_labels": {
    "ro": [],
    "en": []
  }
}
```

Preferred-label discipline follows the useful SKOS idea of one preferred label per language. Alternative labels support Search, abbreviations, synonyms and legacy terms.

CEM does not require RDF or SKOS serialization.

## 7. Required common metadata

For generated semantic entities, where applicable:

- id
- semantic_type
- preferred_labels (RO/EN)
- alternative_labels
- description/summary
- status_facets
- model_scope
- source registry/path and source ID
- related entity IDs
- evidence/reference IDs
- limitations/boundaries

Identity, semantic type and source mapping are mandatory.

## 8. Stable ID policy

Existing IDs remain canonical by default:

- `VAR.*`
- `LINK.*`
- `MOD.*`
- `REF.*`
- `VAL.*`
- `TARGET.*`
- `THEORY.*`
- `GLOSS.*`

OA-1 must not mass-rename them into a stylistically uniform namespace.

When a later object genuinely needs a new identity, introduce explicit aliases/source mapping and preserve old references.

Theory mechanism tokens such as `repetition`, `editorial` and `presentation` must resolve through an explicit adapter table rather than implicit string matching.

## 9. Schema strategy

Use JSON Schema Draft 2020-12 explicitly with `$schema` and stable `$id` identifiers.

Prefer reusable `$defs` and `$ref` definitions.

The first semantic schema validates the generated index; it does not force every source registry to migrate simultaneously.

Cross-reference integrity is validated in Python tests in addition to structural JSON Schema validation.

## 10. Separation from provenance

Semantic relations answer questions such as:

- What does this variable depend on computationally?
- What registered relation connects these variables?
- What evidence/references are attached?
- Which theory chapter explains this entity?

Provenance answers:

- Which analysis generated this result?
- Which model/evidence snapshot/settings were used?
- Which version revised an earlier entity?

OA-1 records source mapping only.

OA-2 may map execution/workspace provenance to W3C PROV concepts such as Entity, Activity, Usage, Generation and Revision, but the semantic layer remains CEM-native.

## 11. OA-1 implementation slices

### OA-1A — schema and index contract

- `schemas/semantic_index.schema.json`;
- entity/relation-layer/status-facet vocabulary;
- deterministic fixture;
- adapter contract tests.

No web UI change.

### OA-1B — deterministic semantic compiler

Generate semantic entities/relations from current authoritative registries and theory/glossary indices.

### OA-1C — computational dependency extraction

Move the 11 auxiliary graph nodes and 17 computational dependencies into a schema-validated canonical registry, compile them into the Semantic Spine and make TypeScript a consumer while preserving existing graph behavior.

### OA-1D — web semantic adapter

Allow existing Theory/Registry surfaces to consume normalized semantic identity/labels without changing the OA-3 information architecture.

Search and Universal Inspector remain OA-4.

## 12. OA-1 migration gate

OA-1 cannot merge as complete until:

- current variables/modules/references/validations/targets/theory/glossary have lossless semantic representation or explicit deferral;
- current registered links retain every evidence/mechanism/functional-form status;
- computational dependencies remain a separate layer;
- old IDs/deep links remain resolvable;
- generated web artifacts remain scientifically identical;
- semantic metadata cannot strengthen current scientific status;
- RO/EN labels retain parity;
- semantic output is deterministic;
- schema and cross-reference tests pass.

## 13. Explicit non-goals

OA-1 does not require:

- RDF;
- OWL;
- SPARQL;
- graph database;
- automatic causal discovery;
- automatic literature inference;
- automatic claim strengthening;
- one universal confidence/maturity score;
- merging all current model JSON into one monolithic file;
- creation of future Workspace entities before OA-2.
