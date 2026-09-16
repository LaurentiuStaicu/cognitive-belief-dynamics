# ADR 0022 — OA-7 canonical illustrative ImplementationPlan and frozen snapshot

Status: Proposed.

## Context

R3 IndexedDB storage is integrated. OA-7 Action Canvas, Indicator objects, trigger drafts and the adaptive six-phase draft are also integrated.

ObservedOutcome cannot be recorded canonically until there is a durable prospective plan to reference.

## Decision

This slice materializes a canonical `ImplementationPlan` only when the adaptive draft is complete.

The plan is intentionally:

- `plan_scope = ILLUSTRATIVE`;
- `status = DRAFT`;
- linked only to the two operational M0 proximal Indicators;
- explicit that intermediate and final result Indicator lists are empty.

It does not become a real-world implementation plan.

## Frozen ProspectiveSnapshot

At freeze time the plan receives:

- a new ImplementationPlan ID;
- a new ProspectiveSnapshot ID;
- one shared creation/freeze timestamp;
- `APPEND_ONLY_NO_RETROACTIVE_EDIT`.

The snapshot is embedded in the canonical persisted ImplementationPlan record. ObservedOutcome can later reference the plan ID and embedded snapshot ID and verify that the snapshot belongs to that plan.

## Append-only persistence

The Reality Loop object store must use IndexedDB `add()`, not `put()`, for canonical prospective records.

A duplicate ID therefore fails closed and aborts the transaction rather than overwriting an existing plan.

This matches the OA-7 provenance policy and the W3C PROV revision model: a revision is represented as a new derived entity rather than silent mutation of the original.

Reference: https://www.w3.org/TR/prov-o/#wasRevisionOf

## Adaptive-plan boundary

Freeze is available only when all six phases are `DEFINED` in canonical order:

NOW / WATCH / IF / THEN / STOP / REASSESS.

Runtime-only fields such as readiness and TriggerDraft IDs are not promoted into the canonical ImplementationPlan schema.

## DecisionAnalysis reference

The current planner creates an originating runtime DecisionAnalysis identifier for the frozen plan. This slice does not yet persist a separate DecisionAnalysis object; the identifier is a provenance reference required by the OA-7 product contract.

No ObservedOutcome is permitted to depend on this reference. ObservedOutcome referential checks depend on ImplementationPlan, ProspectiveSnapshot and Indicator identities.

## Scientific boundary

No model equation, coefficient, score, evidence status, semantic relation or reference run changes.

Freezing a plan records a user's prospective planning state; it does not validate the intervention, calibrate the model, or create empirical evidence.

## Next dependency

After this PR and green post-merge CI, OA-7 may add the ObservedOutcome recorder with explicit retrospective metadata and append-only writes.
