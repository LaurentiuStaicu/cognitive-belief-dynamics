# R1 — Semantic Model Research Spike

Status: **ADOPT WITH LIMITS**  
Track: OA-1 Semantic Spine  
Baseline: `36bf6c543f7060a8069a11eacadeb920145d0590`

## 1. Question

What is the smallest semantic architecture that can give CEM stable cross-surface identity, search, inspection and later workspace/provenance support without rewriting the scientific registries or collapsing important epistemic distinctions?

## 2. Repository inventory

The current repository already contains stable families of identifiers:

- variables: `VAR.*`;
- registered evidence-qualified links: `LINK.*`;
- conceptual modules: `MOD.*`;
- references: `REF.*`;
- validation tests: `VAL.*`;
- empirical targets: `TARGET.*`;
- theory chapters: `THEORY.*`;
- glossary descriptors: `GLOSS.*`.

These IDs are already cross-referenced by Theory, Registry, browser views, validation contracts and exports. Replacing them merely for a cleaner naming convention would create avoidable migration risk.

The repository also has two relation systems that must remain distinct:

1. `model/links.json`: evidence-qualified scientific/model relations with phenomenon, mechanism and functional-form status;
2. `web/src/dependencies.ts`: computational dependencies used to explain executable equations.

The current documentation explicitly warns that the computational map is not the evidence registry. OA-1 must preserve that distinction.

## 3. Options considered

### Option A — Replace current registries with one new semantic graph

Advantages:

- conceptually clean;
- one file/API.

Rejected for OA-1 because:

- high migration risk;
- breaks or aliases many stable IDs at once;
- encourages accidental collapse of computational and evidential relations;
- makes scientific regression review unnecessarily large.

### Option B — Adopt RDF/SKOS/PROV as the native storage model

Advantages:

- established semantic-web standards;
- strong interoperability.

Rejected for OA-1 because:

- CEM does not currently need SPARQL, RDF stores or web-scale linked-data interchange;
- adds implementation complexity without solving an immediate product problem;
- PROV models provenance, not the scientific ontology itself;
- SKOS is useful for labeling discipline but need not dictate the storage technology.

### Option C — Build a generated Semantic Spine index over the existing registries

Advantages:

- preserves authoritative source files;
- preserves stable IDs;
- can be regenerated deterministically;
- gives web/native/Search/Inspector one normalized interface;
- allows staged migration;
- keeps semantic and scientific changes reviewable.

**Decision: ADOPT WITH LIMITS.**

OA-1 will implement Option C first.

## 4. Stable identity decision

Existing IDs are canonical by default.

Do not rename:

- `VAR.FAMILIARITY.CLAIM` to a new stylistic ID;
- `REF.*`, `VAL.*`, `TARGET.*`, etc.

If a later semantic entity needs a new identity, the semantic layer must expose an explicit alias/source mapping rather than silently replacing the old ID.

Glossary mechanism descriptors such as `GLOSS.MECH.REPETITION` may initially serve as semantic mechanism descriptors. A dedicated mechanism registry is **deferred** until a concrete requirement demonstrates that glossary identity is insufficient.

Theory mechanism tokens such as `repetition`, `editorial` and `presentation` must resolve through an explicit adapter table to canonical glossary/mechanism descriptors rather than through implicit string matching.

## 5. Minimal OA-1 semantic entity families

The first generated index only needs entities that already have authoritative repository objects:

- VARIABLE
- MODULE
- REFERENCE
- VALIDATION
- EMPIRICAL_TARGET
- THEORY_CHAPTER
- GLOSSARY_ENTRY

A glossary entry with `kind=MECHANISM` may expose semantic role `MECHANISM_DESCRIPTOR` without changing its stored ID.

Future Workspace objects such as Prediction, Decision, Indicator and Observation remain OA-2/OA-7 concerns and should not be invented in OA-1 merely to complete a theoretical ontology.

## 6. Relation layers

OA-1 must encode relation **layer** before relation semantics.

### 6.1 Registered evidence-qualified relation

Source: `model/links.json`.

Preserve, without flattening:

- raw `relation_type`;
- polarity;
- phenomenon evidence status;
- mechanism evidence status;
- functional-form status;
- evidence refs;
- bilingual finding/limitation summaries.

A registered relation must not be converted to a generic causal edge that loses these facets.

### 6.2 Computational dependency

Current source: `web/src/dependencies.ts`.

Represents equation/data-flow dependency, not empirical causal validation.

OA-1 should move this metadata out of TypeScript into a canonical data artifact while preserving the current formulas, files and optional `registered` cross-reference.

This is an architectural relocation only; it must not change equations or reference trajectories.

### 6.3 Documentation relation

Theory/glossary references to variables, modules, validations, evidence and views.

These relations support navigation/search and do not imply scientific support unless their role explicitly says so.

## 7. Epistemic status decision

A single scalar `epistemic_status` is insufficient.

The repository already contains orthogonal status dimensions:

- phenomenon evidence status;
- mechanism evidence status;
- functional-form status;
- conceptual/interpretive status;
- executability;
- validation scope.

OA-1 therefore uses **status facets**, not one ordered maturity score.

Candidate normalized shape:

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

Only facets that exist for the source entity are emitted.

There is no rule that `EXECUTABLE` implies `EMPIRICALLY_VALIDATED`, and no ordering that automatically upgrades `CANDIDATE` to a stronger status.

OA-1 schema work must define allowed values per facet from values already present in the repository before adding new vocabulary.

## 8. Multilingual labels

CEM keeps existing bilingual labels as authoritative presentation strings.

The semantic index may normalize them to:

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

Design inspiration: SKOS distinguishes preferred and alternative labels and allows one preferred label per language. OA-1 adopts that discipline without requiring RDF/SKOS serialization.

Alternative labels are primarily for Search: abbreviations, short names, common English/Romanian variants and legacy terms.

## 9. Schema strategy

Use JSON Schema Draft 2020-12 explicitly with `$schema` and stable `$id` values.

Prefer small reusable definitions using `$defs`/`$ref`.

The first semantic schema should validate a generated index; it should not force all existing source files to migrate simultaneously.

Strictness principle:

- required identity/type/source fields;
- constrained known status facets;
- deterministic cross-reference validation in Python tests;
- avoid accepting arbitrary undeclared semantic relation kinds.

## 10. Provenance boundary

Semantic source mapping is not full provenance.

OA-1 records where a semantic entity came from, for example:

```json
{
  "source": {
    "registry": "model/variables.json",
    "source_id": "VAR.FAMILIARITY.CLAIM"
  }
}
```

OA-2 will introduce execution/workspace provenance.

W3C PROV remains a conceptual mapping target for OA-2: Entity, Activity, Usage, Generation and Revision are useful provenance concepts, but OA-1 does not require PROV-O/RDF.

## 11. Architecture Decision Records

From OA-1 onward, major architectural decisions use short immutable ADRs.

ADR rule:

- capture context, decision and consequences;
- accepted ADRs are not rewritten to pretend a later decision was always true;
- a changed decision is represented by a superseding ADR.

## 12. Proposed OA-1 implementation slices

### OA-1A — schema and index contract

- `schemas/semantic_index.schema.json`;
- allowed entity/relation-layer/status-facet vocabulary;
- adapter contract tests.

No web UI change.

### OA-1B — deterministic semantic compiler

Generate a semantic index from:

- variables;
- modules;
- references;
- validations;
- empirical targets;
- theory index;
- glossary.

Add cross-reference integrity checks.

No scientific numerical change.

### OA-1C — computational dependency extraction

Move the 17 current computational dependencies and extra graph nodes from TypeScript metadata to canonical JSON/data generation.

TypeScript becomes a consumer.

Scientific formulas and graph meaning remain byte/semantically equivalent.

### OA-1D — web semantic adapter

Theory/Registry can begin consuming semantic identity/labels without changing top-level information architecture.

Search and Universal Inspector remain OA-4.

## 13. Acceptance criteria

R1/OA-1 must preserve:

- all existing canonical IDs;
- all existing deep links or explicit aliases;
- separation of computational dependency from evidence-qualified registered relation;
- every existing evidence/mechanism/functional-form status;
- RO/EN preferred labels;
- existing model/reference outputs;
- evidence snapshot and release version.

The generated semantic index must be deterministic and must not contain a scientific statement stronger than its source.

## 14. Research basis

External design references consulted:

- W3C PROV Primer: https://www.w3.org/TR/prov-primer/
- W3C SKOS Primer: https://www.w3.org/TR/skos-primer
- W3C SKOS Reference: https://www.w3.org/TR/skos-reference/
- JSON Schema Draft 2020-12: https://json-schema.org/draft/2020-12
- JSON Schema structuring guidance: https://json-schema.org/understanding-json-schema/structuring
- Architecture Decision Record overview: https://martinfowler.com/bliki/ArchitectureDecisionRecord.html

These references inform architecture and interoperability only. They do not establish CEM scientific validity.
