# ADR 0015 — OA-7 Reality Loop contract and schema

Status: Proposed for OA-7 contract/schema integration.

## Context

The optimization roadmap already defines OA-7 as **Reality Loop**. It requires:

- Action Canvas;
- Indicator objects;
- signposts/triggers;
- adaptive NOW / WATCH / IF / THEN / STOP / REASSESS planning;
- ObservedOutcome records;
- Decision Autopsy / revision trail.

The exit gate requires `SimulationResult`, `DecisionAnalysis`, `ImplementationPlan` and `ObservedOutcome` to remain distinct schema types; retrospective observations must not overwrite prospective predictions; and real-world planning must carry explicit population, context and outcome fields.

No additional research spike is required by the roadmap for OA-7. R8 is reserved for the native elementary OS implementation immediately before OA-9.

## Decision

OA-7 begins with a pre-executable product contract:

- `schemas/reality_loop.schema.json`;
- `model/contracts/reality_loop_v1.json`;
- contract tests only.

No UI, storage migration or runtime execution is introduced in this PR.

## Four-object separation

The schema reserves four distinct decision objects:

1. **SimulationResult** — prospective model-output reference with explicit epistemic scope.
2. **DecisionAnalysis** — consumes SimulationResult refs and remains conditional rather than automatically becoming a recommendation.
3. **ImplementationPlan** — derives from a DecisionAnalysis, freezes a prospective snapshot, owns Action Canvas/indicators/adaptive planning, and requires population/context/outcome fields for REAL_WORLD scope.
4. **ObservedOutcome** — retrospective observation linked to the plan, frozen snapshot and indicator; it appends evidence without editing the prior prediction.

## Observation-model basis

OGC Observations, Measurements and Samples provides a generic conceptual model in which an observation links a feature of interest, observed property, procedure and result, together with observation/result timing. OA-7 adopts only this minimal conceptual pattern; it does **not** claim full OGC OMS conformance.

Source: https://www.ogc.org/standards/om/

## Provenance basis

W3C PROV distinguishes entities, activities, generation/usage and revisions. A revision is represented as a new derived entity rather than silent mutation of the original. OA-7 therefore uses a small PROV-inspired append-only rule:

- prospective snapshots are frozen;
- observations append new records;
- Decision Autopsy may propose a revision;
- a new revision does not retroactively rewrite the prior prospective object.

OA-7 does not claim full PROV-O serialization.

Source: https://www.w3.org/TR/prov-o/

## Action Canvas

The contract freezes the chain already required by the architecture:

`Problem -> target mechanism -> intervention -> proximal result -> intermediate result -> final outcome`.

Result stages link to explicit Indicator IDs.

## Adaptive vocabulary

The schema reserves exactly:

- NOW
- WATCH
- IF
- THEN
- STOP
- REASSESS

`WATCH` requires an Indicator ref; `IF` requires a trigger condition; `THEN`, `STOP` and `REASSESS` require an explicit action.

This is a prospective planning grammar, not background automation.

## Decision Autopsy

Decision Autopsy is an append-only retrospective review object. It references prior DecisionAnalysis, ImplementationPlan and ObservedOutcome records and may contain revision proposals for model assumptions, decision analyses, implementation plans or indicators.

`prior_prediction_mutated` is fixed to `false`.

## Workspace/storage boundary

The existing Workspace schema remains version 1 and is intentionally unchanged in this PR.

The Reality Loop contract states:

- `RESERVED_NOT_IN_WORKSPACE_V1`;
- storage migration is required before runtime persistence.

This prevents contract metadata from silently becoming stored application state.

## Scientific boundary

The contract fixture is synthetic and non-scientific.

This PR changes no equation, coefficient, evidence snapshot, active semantic relation, reference run, intervention score or release metadata.

The illustrative SimulationResult is explicitly `ILLUSTRATIVE_UNCALIBRATED`, and DecisionAnalysis explicitly remains `NOT_A_REAL_WORLD_RECOMMENDATION`.

## First implementation gate after this contract

Only after this contract/schema PR and post-merge CI are green should OA-7 implementation begin.

The implementation must follow the existing repository rule of small, separate PRs rather than introducing Action Canvas, storage migration, observations and autopsy in one multi-concern change.
