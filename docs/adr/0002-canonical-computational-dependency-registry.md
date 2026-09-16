# ADR-0002 — Canonical computational-dependency registry

Status: **proposed**

## Context

CEM currently has two deliberately different relation systems:

1. `model/links.json` contains evidence-qualified registered relations;
2. `web/src/dependencies.ts` contains 17 executable equation/data-flow dependencies plus 11 auxiliary graph nodes.

The second set is scientifically meaningful explanatory metadata, but it currently exists only in presentation-layer TypeScript. OA-1 requires scientific identity and explanatory metadata to have a canonical non-UI source while preserving the distinction between computation and empirical evidence.

Several dependency endpoints such as `F`, `B`, `W`, `Nexp` and `Share` already correspond to canonical `VAR.*` records. Creating new semantic entities for those graph short names would duplicate identity. Other graph nodes such as `Prior`, `Evidence`, `Random` and intermediate `P` have no registered variable identity and need explicit computational-node identity if the Semantic Spine is to reference them.

## Decision

Adopt `model/computational_dependencies.json` as the canonical source for the current M0 explanatory computational graph.

The registry preserves two identity layers explicitly:

- `graph_id`, `source_graph_id`, `target_graph_id` preserve current UI graph compatibility;
- `source_semantic_id` and `target_semantic_id` resolve to canonical `VAR.*` IDs or explicit `COMP.NODE.*` auxiliary computational nodes.

The 17 computational edges receive stable `COMPDEP.*` semantic IDs.

Only the 11 genuinely auxiliary graph nodes receive new `COMP.NODE.*` IDs. Existing variables are referenced through their current canonical `VAR.*` IDs.

The registry preserves, byte-for-byte in meaning:

- RO/EN explanatory text;
- displayed formula;
- source code filename;
- current graph endpoint IDs;
- optional cross-reference to a registered evidence-qualified `LINK.*` relation.

A computational dependency remains a separate relation layer and does **not** become an empirical causal claim merely because an optional `registered_relation_id` exists.

Migration is staged:

1. OA-1C contract PR introduces canonical data, schema and parity tests while legacy TypeScript remains the active web source;
2. the follow-up compiler/consumer cutover adds the dependencies to the generated Semantic Spine and makes TypeScript consume generated/canonical data;
3. only after parity tests pass is duplicated literal metadata removed from TypeScript.

## Alternatives considered

### Keep dependencies in TypeScript

Rejected because presentation code would remain a scientific/explanatory source of truth and future Web/GTK consumers could diverge.

### Convert all graph short names into new semantic entities

Rejected because `F`, `B`, `W`, `Nexp`, `Share`, etc. already have canonical registered variable identity. Duplication would complicate Search, Inspector and provenance.

### Merge computational dependencies into `model/links.json`

Rejected because it would collapse equation/data-flow dependency into evidence-qualified scientific relations and violate the existing epistemic boundary.

### Infer computational dependencies automatically from Python AST/code

Deferred. It would add substantial tooling complexity and could lose explanatory wording and conceptual dependencies that are intentionally documented rather than trivially recoverable from syntax.

## Consequences

Positive:

- Web and future GTK can share one computational dependency source;
- Semantic Spine can reference canonical variable identities;
- evidence-qualified and computational relation layers remain distinct;
- future Universal Inspector/Search can trace graph edges without parsing TypeScript;
- UI graph compatibility is preserved during migration.

Costs:

- temporary duplication exists until the consumer cutover;
- auxiliary `COMP.NODE.*` identity is introduced and must be validated;
- the semantic-index schema/compiler must be extended in the follow-up slice.

## Scientific boundary

This decision changes metadata location only. It does not change equations, parameters, model execution, reference trajectories, evidence status, release version, M1.E4 status or the active evidence snapshot.
