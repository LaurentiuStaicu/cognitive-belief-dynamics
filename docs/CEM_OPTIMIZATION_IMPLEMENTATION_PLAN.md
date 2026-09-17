# CEM Optimization Implementation Plan — OA-0

Status: operational plan for the optimization track. This plan is subordinate to `CEM_OPTIMIZATION_ARCHITECTURE.md`.

## 1. Delivery model

Each optimization phase follows:

1. focused research spike when required;
2. contract/schema PR;
3. implementation PR;
4. regression/audit gate;
5. merge;
6. post-merge verification.

Scientific-model changes use a separate track and cannot be smuggled into OA implementation PRs.

## 2. Phase sequence

### OA-0 — Architecture contract and baseline

Deliverables:

- integrated architecture contract;
- semantic contract;
- authoritative baseline manifest;
- quality matrix;
- invariant test;
- draft research-spike backlog.

Exit gate:

- no scientific output change;
- baseline test passes;
- full existing CI passes;
- PR remains documentation/infrastructure only.

### OA-1 — Semantic Spine

Research spike R1 decides minimum entity/relationship vocabulary from current repository content.

Implementation:

- semantic schemas;
- current-registry adapters;
- stable IDs/aliases;
- epistemic status validation;
- semantic export consumed by web;
- regression proof that existing numerical artifacts remain unchanged.

Exit gate:

- lossless representation of current variables, links, modules, references and validations;
- deep links preserved or aliased;
- no status strengthening;
- full CI passes.

### OA-2 — Workspace + Provenance

Research spikes R2/R3 cover provenance subset and persistence/migration strategy.

Implementation:

- `workspace.schema.json`;
- Case / Analysis / Prediction / Decision records;
- local persistence adapter;
- autosave;
- versioned export/import;
- migration engine;
- recovery snapshot;
- result provenance.

Exit gate:

- save/load round-trip;
- export/import round-trip;
- old-schema migration fixtures;
- corrupt/future schema safe rejection;
- no remote account dependency.

### OA-3 — Information Architecture + Visual Language

Research spike R4 checks comprehension of the four primary surfaces.

Implementation:

- Understand / Analyze / Act / Library navigation;
- transitional routes from old views;
- quiet-scientific visual tokens;
- reading/research layouts;
- responsive two-pane/optional three-pane behavior;
- systematic RO/EN microcopy pass.

Exit gate:

- every current feature remains reachable;
- old deep links redirect or remain valid;
- mobile and 200% text tests pass;
- screenshots audited in RO/EN light/dark.

### OA-4 — Universal Inspector + Search

Research spike R5 selects the smallest adequate search implementation.

Implementation:

- canonical entity inspector;
- semantic cross-links;
- global search;
- deep-linkable search/inspection targets;
- keyboard-first access.

Exit gate:

- every indexed canonical entity can be located and inspected;
- diacritics and RO/EN labels work;
- search startup cost remains within budget.

### OA-5 — Active Understanding

Research spike R6 defines usability/learning evaluation.

Implementation:

- Predict -> Reveal -> Explain in Guided/Learning mode;
- worked examples;
- Challenge Model using existing mechanisms/comparators;
- initial competing-model comparison where scientifically available;
- local prediction/confidence history only.

Exit gate:

- no new scientific claim;
- model result hidden until prediction only in explicit learning mode;
- comprehension tests cover exposure/familiarity, belief/share and computation/causation boundaries.

### OA-6 — Decision Under Uncertainty

Research spike R7 decides supported subset of sensitivity/robustness/VoI methods.

Implementation order:

1. Assumption Register;
2. uncertainty taxonomy;
3. deterministic sensitivity;
4. robustness across declared scenarios/profiles;
5. switching assumptions/failure regions;
6. research-priority analysis;
7. formal VoI only where probabilistic inputs justify it.

Exit gate:

- current score remains reproducible;
- “highest score” is explicitly conditional;
- simulation result is not presented as recommendation;
- uncertainty representation is decomposed rather than a single unsupported confidence score.

### OA-7 — Reality Loop

Implementation:

- Action Canvas;
- Indicator objects;
- signposts/triggers;
- adaptive NOW/WATCH/IF/THEN/STOP/REASSESS plan;
- ObservedOutcome records;
- Decision Autopsy / revision trail.

Exit gate:

- SimulationResult, DecisionAnalysis, ImplementationPlan and ObservedOutcome are distinct schema types;
- retrospective observations cannot overwrite prospective predictions;
- real-world planning requires explicit population/context/outcome fields.

### OA-8 — Trust Hardening

Progressively introduced earlier, fully gated here:

- WCAG 2.2 AA audit;
- screen-reader/manual keyboard audit;
- dependency review;
- CodeQL Python + TypeScript;
- SBOM/release integration;
- untrusted import hardening;
- performance budgets;
- offline/stale-evidence policy;
- local diagnostics with no mandatory telemetry.

### OA-9 — Native elementary OS — DEFERRED UNTIL NEAR v1

OA-9 is deliberately outside the current optimization critical path. The Web application remains the only active implementation while M1 is completed, the Simple-mode simplification is performed and the remaining modules are integrated. Native implementation begins only after the product is functionally stable and close to version 1.0; Web and Flatpak then become the two official variants of the same product.

Research spike R8 rechecks current platform/runtime requirements immediately before native implementation so the future package does not freeze outdated GTK/Granite/Flatpak assumptions.

Future implementation:

- GTK4/Granite;
- Meson;
- Gettext;
- Flatpak;
- portals;
- AppStream/desktop/icon metadata;
- canonical artifact adapters;
- scientific parity fixtures shared with web.

Future exit gate:

- reproducible Flatpak;
- installation test on supported elementary OS runtime;
- parity of scientific values/status/provenance with web;
- native system font/theme/accessibility;
- no broad filesystem permissions without explicit justification.

Until that gate is opened, new module development targets the Web implementation and shared scientific/semantic artifacts rather than parallel native UI work.

## 3. Research spike contract

Every spike must record:

- question;
- candidate options;
- authoritative sources;
- constraints;
- test/prototype if needed;
- decision: ADOPT / ADOPT_WITH_LIMITS / DEFER / REJECT;
- consequences for schemas/UI/tests.

A spike is not complete merely because sources were collected.

## 4. Branch and PR discipline

Recommended naming:

- `oa-0-...`
- `oa-1-...`
- etc.

Recommended labels:

- `track:optimization`
- `area:semantic`
- `area:workspace`
- `area:ux`
- `area:visual`
- `area:a11y`
- `area:security`
- `area:decision`
- `area:native`
- `gate:research`
- `gate:integration`

No OA phase should be delivered as one large multi-concern PR.

## 5. Compatibility rule

If a separate scientific track legitimately changes version, active model, evidence snapshot or authoritative output:

1. merge and verify the scientific change first;
2. create an explicit OA baseline-rebase PR;
3. update `oa0_optimization_baseline.json` or its successor;
4. explain every changed invariant;
5. re-run all OA regression gates.

Silent baseline drift is forbidden.

## 6. Deferred features

Not part of the current OA critical path:

- OA-9 native elementary OS / Flatpak implementation before the near-v1 gate;
- general-purpose AI chatbot inside CEM;
- cloud accounts/sync;
- real-time collaboration;
- plugin marketplace;
- automatic causal discovery;
- automatic literature-to-mechanism promotion;
- global single-number confidence score.

These require independent need, risk and privacy justification or, for OA-9, the explicit near-v1 product gate described above.
