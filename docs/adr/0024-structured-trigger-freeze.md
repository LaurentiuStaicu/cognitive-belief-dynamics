# ADR 0024 — OA-7 structured prospective trigger freeze

Status: Proposed.

## Context

PR #70 introduced canonical append-only ObservedOutcome records and post-merge CI #269 passed.

The next OA-7 slice must compare persisted observations with the prospective trigger that was frozen into an ImplementationPlan. The existing plan preserved the IF condition only as bilingual explanatory text. Parsing that prose would make trigger evaluation dependent on natural-language interpretation and could silently change semantics across languages or copy edits.

## Decision

The adaptive IF step now carries both:

- the existing bilingual `trigger_condition` copy for human readability; and
- a machine-readable `trigger` object containing:
  - `indicator_id`;
  - `comparator` = LT / LTE / GTE / GT;
  - numeric `threshold`;
  - `unit`;
  - `origin = USER_DECLARED`.

A complete AdaptivePlanDraft must preserve this structured trigger. A canonical ImplementationPlan freeze fails closed if:

- WATCH has no Indicator;
- IF has no structured trigger; or
- the IF trigger Indicator differs from the WATCH Indicator.

The structured trigger is copied into the frozen ImplementationPlan and is therefore part of the prospective snapshot semantics. Runtime-only TriggerDraft IDs remain excluded from the canonical plan.

## Evaluation boundary

This ADR does not evaluate any trigger.

A later slice may evaluate only persisted ObservedOutcome records against the frozen structured trigger. It must not:

- parse `trigger_condition` prose to recover semantics;
- substitute SimulationResult values for observations;
- poll external sources in the background;
- execute THEN / STOP / REASSESS automatically;
- mutate the frozen ImplementationPlan or ProspectiveSnapshot.

## Provenance rationale

The existing OA-7 provenance rule remains append-only. W3C PROV models revision as derivation into a new entity rather than silent mutation of the prior entity. Preserving machine-readable prospective trigger semantics supports later retrospective comparison without rewriting the prior plan.

Reference: https://www.w3.org/TR/prov-primer/#section-derivation

## Observation rationale

ObservedOutcome already preserves feature of interest, observed property, procedure, phenomenon time, result time and result. This is the minimal observation boundary adopted from the OGC Observations, Measurements and Samples conceptual model.

Reference: https://www.ogc.org/standards/om/

## Scientific boundary

This is product-contract and provenance work only.

No equation, coefficient, model output, evidence state, intervention ranking, semantic relation, reference run or release version changes. Trigger thresholds remain user declarations and do not become scientifically validated thresholds.

## Regression requirements

- IF requires a structured trigger in the JSON schema;
- the contract fixture validates only with the structured trigger present;
- the trigger Indicator is the watched Indicator;
- trigger unit matches the referenced Indicator in the contract fixture;
- runtime AdaptivePlanDraft carries the structured condition;
- canonical ImplementationPlan preserves it while dropping runtime-only TriggerDraft identity;
- all existing OA and browser regressions remain green.

## Next gate

After this PR and post-merge CI are green, OA-7 may add a read-only trigger-evaluation view that consumes persisted ObservedOutcome records. That evaluation remains derived, non-executing and non-mutating.
