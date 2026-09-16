# ADR 0021 — OA-7 illustrative-plan operationalization boundary

Status: Proposed.

## Context

The OA-7 runtime intentionally exposes only Indicators supported by the current M0 model. At present, those Indicators cover the proximal result. Intermediate and final result stages remain explicitly `NOT_OPERATIONALIZED`.

The original Reality Loop schema required non-empty `indicator_ids` arrays for proximal, intermediate and final Action Canvas stages for every ImplementationPlan. That made an epistemically honest illustrative plan impossible without fabricating unsupported Indicators.

## Decision

For `plan_scope = ILLUSTRATIVE`:

- Action Canvas result-stage `indicator_ids` arrays may be empty;
- the plan-level `indicator_ids` list remains non-empty, so an ImplementationPlan still references at least one real Indicator;
- runtime must preserve the distinction between operationalized and non-operationalized stages.

For `plan_scope = REAL_WORLD`:

- population, context and primary outcome remain mandatory;
- proximal, intermediate and final Action Canvas result stages each require at least one Indicator.

## Rationale

The contract should not force placeholder measurements merely to satisfy shape completeness. An empty stage-level Indicator list is more truthful than inventing a measurement procedure that the model does not support.

This keeps the product contract aligned with the previously integrated Action Canvas and Indicator-object boundaries.

## Scientific boundary

This change does not promote evidence, add a model variable, change an equation, or create a new measurement claim. It only corrects the product-schema distinction between illustrative planning and real-world operationalization.

## Implementation consequence

Once this patch is integrated, the runtime may materialize a canonical `ILLUSTRATIVE` ImplementationPlan using the two supported proximal M0 Indicators while leaving intermediate/final Indicator lists empty.

`ObservedOutcome` remains out of scope until a persisted ImplementationPlan and frozen ProspectiveSnapshot exist.
