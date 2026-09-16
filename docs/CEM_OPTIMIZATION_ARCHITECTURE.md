# CEM Integrated Optimization Architecture

Status: OA-0 architecture contract. This document governs the optimization track and does **not** change scientific equations, active model registration, evidence status, release version or runtime behavior.

Baseline main commit: `f896b5dfe794c6f04fbc39ad4bf7be734a3c2269`.

## 1. Purpose

The optimization track turns CEM into a coherent epistemic workbench while preserving its existing scientific boundaries.

The target workflow is:

`OBSERVE -> MODEL -> PREDICT -> TEST -> CHALLENGE -> EXPLAIN -> DECIDE -> ACT -> MEASURE -> REVISE`.

Optimization must improve understanding, traceability, decision support, real-world planning, visual clarity, accessibility, portability and maintainability without silently strengthening scientific claims.

## 2. Non-negotiable scientific boundary

OA work must not, unless a later dedicated scientific gate explicitly authorizes it:

- alter M0 equations or saved M0 reference trajectories;
- alter M1.E1, M1.E2 or M1.E3 scientific outputs;
- activate M1.E4 as a human cognitive model;
- introduce `Pencode`;
- declare EVSD or 2HT the human mechanism;
- convert synthetic steps into empirical time;
- convert software validation into psychological validation;
- convert simulation rankings into real-world recommendations;
- change evidence snapshot `EVIDENCE.M1.2026-09-16.r1`;
- change software version `0.4.2a0` merely to land OA foundation work.

Scientific development may proceed in a separate track, but cross-track merges must re-run the OA baseline and explicitly rebase the contract if the scientific baseline legitimately changes.

## 3. Architectural layers

### Layer A — Scientific Core

Canonical Python simulation, registered model data, evidence contracts, validation tests and benchmark outputs remain authoritative.

Scientific equations must not be reimplemented independently inside presentation code.

### Layer B — Semantic Spine

A canonical graph-like semantic layer identifies scientific and product entities with stable IDs and typed relationships.

Initial entity families:

- Concept
- Construct
- Variable
- Claim
- Mechanism
- Formula
- Assumption
- Evidence
- EmpiricalTarget
- Validation
- Model
- Scenario
- Prediction
- Intervention
- Outcome
- Indicator
- Observation
- Decision

Initial relation families:

- DEPENDS_ON
- SUPPORTS
- CONTRADICTS
- LIMITS
- OPERATIONALIZES
- TESTS
- PREDICTS
- TARGETS
- MEASURES
- DERIVED_FROM
- GENERATED_BY
- SUPERSEDES

The Semantic Spine is a CEM-native data model. It may be mapped to external standards later but is not required to use RDF, OWL or a graph database.

### Layer C — Epistemic Type System

Every entity capable of carrying a scientific claim must expose its epistemic status explicitly.

Initial status vocabulary:

- EMPIRICAL_PHENOMENON
- EMPIRICAL_OBSERVATION
- CANDIDATE_MECHANISM
- REFERENCE_FORM
- UNCALIBRATED_FORM
- CONCEPTUAL
- INTERPRETIVE
- VALIDATED_WITHIN_SCOPE

The type system must prevent UI or export code from silently presenting a weaker status as a stronger one.

### Layer D — Workspace and Provenance

The user works in a versioned local-first Workspace containing Cases and analyses.

A workspace records at least:

- workspace schema version;
- CEM software version;
- model specification;
- evidence snapshot;
- case/problem context;
- assumptions;
- predictions;
- analyses;
- decisions;
- action plans;
- indicators;
- observations;
- provenance.

Provenance follows the useful subset of the W3C PROV mental model: entities, activities, derivation/use/generation and responsible software/user context. CEM does not require PROV-O/RDF serialization in OA-0.

### Layer E — Product Surfaces

Primary product surfaces converge toward:

1. Understand
2. Analyze
3. Act
4. Library

Workspace/Case is the persistent context, not a fifth content silo.

### Layer F — Platform Adapters

Web and future GTK4/Granite frontends consume the same scientific and semantic artifacts.

Required principle:

`scientific parity != pixel parity`.

The native app should use native elementary OS patterns, fonts, widgets, portals and accessibility behavior rather than reproduce browser CSS pixel-for-pixel.

## 4. Universal interaction vocabulary

Where applicable, CEM should reuse a small interaction vocabulary instead of inventing unrelated controls:

- Inspect
- Trace
- Predict
- Compare
- Challenge/Test
- Save to Case

These actions operate on canonical semantic entities and produce provenance-bearing results.

## 5. Information architecture target

### Understand

Theory, mechanisms, guided learning and worked examples.

### Analyze

Scenarios, comparisons, model challenge, competing models, sensitivity and decision analysis.

### Act

Intervention analysis, action canvas, adaptive plan, monitoring and review.

### Library

Claims, evidence, variables, mechanisms, models, validation and references.

The current views remain accessible during migration. OA must not remove a capability before its replacement route is implemented, tested and documented.

## 6. Visual architecture target

Design principle: **quiet scientific interface**.

Requirements:

- system font and system color scheme;
- limited visual hierarchy;
- spacing as the primary separator;
- fewer universal “cards”;
- accent color reserved for selection, focus and primary action;
- approximately 66–72ch reading measure for long theory prose;
- two-pane layout by default where appropriate;
- optional contextual third pane on wide screens;
- semantic status never encoded by color alone;
- charts preserve exact-value/table alternatives;
- native GTK implementation minimizes custom styling.

Detailed visual tokens are deferred to OA-3 after semantic/workspace foundations are stable.

## 7. Decision architecture target

The mature decision surface must distinguish:

- SimulationResult
- DecisionAnalysis
- ImplementationPlan
- ObservedOutcome

These objects must not be automatically substituted for one another.

Optimization evolves from a single highest-score presentation toward:

- explicit assumptions;
- uncertainty decomposition;
- sensitivity;
- robustness;
- trade-offs;
- switching assumptions;
- failure regions;
- research-priority / decision-sensitivity analysis.

Formal Value of Information is permitted only when probability distributions and the decision model justify it.

## 8. Reality-loop target

CEM may support real-world action only through an explicitly separate implementation/evaluation layer.

Action Canvas chain:

`Problem -> target mechanism -> intervention -> proximal result -> intermediate result -> final outcome`.

Every transition should be able to expose assumption, evidence and indicator.

Adaptive planning vocabulary:

- NOW
- WATCH
- IF
- THEN
- STOP
- REASSESS

Observed outcomes return to the Case and may motivate model/assumption revision. They do not retroactively change prior predictions.

## 9. Local-first and privacy boundary

Personal workspaces, predictions, notes and calibration history are local by default.

Web target: IndexedDB or another transactional local store, selected in OA-2 after a focused storage spike.

Native target: application-specific XDG data with Flatpak portals for import/export.

No account, cloud sync, telemetry or remote analytics is required by the architecture contract.

Any later sync/telemetry proposal requires a separate privacy and security review.

## 10. Accessibility boundary

Web target: WCAG 2.2 AA.

In addition to automated checks, release gates require manual keyboard and assistive-technology review for the major surfaces.

New interactions must provide alternatives to dragging when dragging is not essential and must preserve adequate pointer-target size/spacing.

The native app must use GTK/Granite accessibility semantics rather than emulate accessibility through custom-drawn widgets wherever a native widget exists.

## 11. Optimization phases

### OA-0 — Architecture contract and baseline

Documentation, baseline manifest and invariant tests only.

### OA-1 — Semantic Spine

Stable IDs, semantic entities/relations, epistemic type rules, adapters from current registries.

### OA-2 — Workspace + provenance

Versioned Workspace/Case schema, local persistence, import/export, migrations, recovery and provenance.

### OA-3 — Information architecture + visual language

Understand / Analyze / Act / Library migration and visual-system implementation.

### OA-4 — Universal Inspector + Search

Canonical inspector, cross-surface deep links and semantic search.

### OA-5 — Active Understanding

Predict -> Reveal -> Explain, worked examples, challenge mode and existing-model comparison.

### OA-6 — Decision under uncertainty

Assumption register, uncertainty taxonomy, sensitivity, robustness and research-priority analysis.

### OA-7 — Reality Loop

Action Canvas, adaptive planning, indicators, observations, review and decision autopsy.

### OA-8 — Trust hardening

Accessibility gates, import security, dependency review, CodeQL, SBOM, performance budgets and offline policy.

### OA-9 — Native elementary OS

GTK4/Granite/Flatpak application using canonical artifacts and web/native scientific parity tests.

## 12. Required research spikes

Each spike ends with one of: ADOPT, ADOPT_WITH_LIMITS, DEFER, REJECT.

- R1 Semantic model: minimum entities/relations required by current and planned CEM.
- R2 Provenance: exact CEM subset/map of PROV concepts.
- R3 Workspace storage: IndexedDB transaction/migration/recovery design.
- R4 IA usability: whether the four-surface navigation is comprehensible to new users.
- R5 Search: static index versus library; RO/EN, diacritics and fuzzy matching.
- R6 Learning UX: predict-first impact on comprehension and calibration.
- R7 Decision methods: justified subset of robustness, sensitivity, VoI and adaptive pathways.
- R8 Native: current elementary runtime, Granite APIs, portals and AppCenter requirements immediately before OA-9.

## 13. Cross-cutting Definition of Done

Every OA implementation PR must answer all applicable gates:

- Scientific: no unsupported claim strengthening.
- Semantic: stable ID and epistemic status where required.
- UX: clear user purpose and route.
- Accessibility: keyboard, scaling and semantic controls.
- RO/EN: parity for all user-facing behavior in scope.
- Provenance: derivation of user-visible analytical results is inspectable.
- Reproducibility: deterministic fixture or invariant test.
- Security: imported/untrusted input validated.
- Migration: persistent data remains recoverable.
- Visual: conforms to the current CEM visual contract.
- Performance: no unexplained startup/interaction regression.
- Documentation: scope and boundaries updated.

## 14. OA-0 authoritative baseline

OA-0 begins from main commit:

`f896b5dfe794c6f04fbc39ad4bf7be734a3c2269`

with:

- software version `0.4.2a0`;
- active model specification `M1`;
- retained baseline `M0`;
- evidence snapshot `EVIDENCE.M1.2026-09-16.r1`;
- Phase J/K authoritative participant-confirmation hash `88c16c2143e7131a4ec8915dbb726ece7e859a797162df173b89743837335f89`.

The optimization track may change architecture and interaction while this baseline remains unchanged. If a separate scientific PR legitimately changes the baseline, the optimization track must update its baseline in an explicit, auditable rebase PR rather than silently accepting drift.

## 15. Reference guidance

Primary external guidance used to define this contract:

- elementary HIG: https://docs.elementary.io/hig
- elementary AppCenter requirements: https://docs.elementary.io/develop/appcenter/publishing-requirements
- WCAG 2.2: https://www.w3.org/TR/WCAG22/
- W3C PROV Primer: https://www.w3.org/TR/prov-primer/
- FAIR4RS principles: https://www.rd-alliance.org/wp-content/uploads/2022/03/FAIR4RS20principles20v1.0.pdf

These sources guide product architecture and quality. They do not validate the CEM scientific model.
