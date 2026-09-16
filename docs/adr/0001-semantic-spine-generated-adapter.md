# ADR-0001 — Semantic Spine as a generated adapter over existing registries

Status: Proposed in R1  
Date: 2026-09-16

## Context

CEM needs stable cross-surface identity for future Search, Universal Inspector, Workspace, provenance and native GTK parity.

The repository already has multiple mature, cross-referenced registries with stable IDs. It also intentionally separates computational dependencies from evidence-qualified scientific/model links.

Replacing all current registries with one new ontology would create a large migration surface and risk collapsing epistemically distinct relations.

## Decision

Build the first Semantic Spine as a **deterministically generated semantic index/adaptor** over existing authoritative registries.

Specifically:

1. Existing IDs remain canonical by default.
2. Source registries remain authoritative in OA-1.
3. Semantic records include explicit source registry/source ID.
4. Registered evidence-qualified relations and computational dependencies remain separate relation layers.
5. Epistemic state is represented by orthogonal status facets rather than one scalar maturity label.
6. Preferred RO/EN labels are separated from optional alternative/search labels.
7. JSON Schema Draft 2020-12 is the native validation technology.
8. SKOS and W3C PROV are conceptual interoperability references, not required storage formats.
9. Full user/workspace provenance is deferred to OA-2.

## Consequences

### Positive

- low-risk staged migration;
- stable deep links;
- deterministic index generation;
- easier web/native parity;
- Search/Inspector can later consume one normalized interface;
- scientific source-of-truth files do not need simultaneous restructuring;
- relation/status nuance is preserved.

### Costs

- adapters must be maintained while source registries remain heterogeneous;
- the semantic index initially duplicates some presentation metadata;
- future schema evolution requires alias/migration rules.

### Explicitly rejected for now

- mandatory RDF/OWL/SPARQL stack;
- graph database;
- destructive ID renaming;
- one universal `epistemic_status` score;
- merging computational and evidence relations into a single causal edge.

## Supersession rule

If a later architecture makes the generated adapter unnecessary, this ADR remains historical and a new ADR must supersede it rather than editing this decision retroactively.
