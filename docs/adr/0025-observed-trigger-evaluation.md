# ADR 0025 — OA-7 persisted ObservedOutcome trigger evaluation

Status: Proposed.

## Context

PR #71 froze prospective IF trigger semantics as machine-readable data inside the canonical ImplementationPlan. Post-merge CI #271 passed on main.

The next Reality Loop step is to consume retrospective ObservedOutcome records without turning monitoring into automation or rewriting the prospective plan.

## Decision

CEM adds a read-only TriggerEvaluationProjection derived from:

1. a persisted canonical ImplementationPlan;
2. its frozen structured IF trigger;
3. persisted ObservedOutcome records queried from IndexedDB by implementation_plan_id;
4. the current IndicatorProjection used to validate identity, observed property, stage and unit.

The projection itself is not persisted.

It is fixed to:

- source = PERSISTED_OBSERVED_OUTCOME_ONLY;
- persistence = DERIVED_NOT_STORED;
- automation = NO_AUTOMATIC_ACTIONS.

Each observation is evaluated independently as:

- TRIGGER_MET;
- TRIGGER_NOT_MET; or
- NOT_EVALUABLE.

No aggregate rule such as majority, latest-wins or automatic escalation is introduced.

## Prospective time boundary

An observation whose phenomenon_time precedes the ImplementationPlan prospective_snapshot.frozen_at is NOT_EVALUABLE for confirming the prospective trigger.

This uses phenomenon_time rather than result_time because OGC Observations, Measurements and Samples defines phenomenonTime as the time to which the result applies, while resultTime is when the result became available.

References:

- https://www.ogc.org/standards/om/
- https://docs.ogc.org/is/18-088/18-088.html

This does not claim full OGC OMS conformance.

## Trigger comparison

The comparator is applied only to the machine-readable trigger frozen prospectively:

- LT: observed value < threshold;
- LTE: observed value <= threshold;
- GTE: observed value >= threshold;
- GT: observed value > threshold.

The evaluator never parses bilingual trigger prose to recover semantics.

The observed Indicator and unit must match the frozen trigger. Records with mismatched Indicators, units, invalid references or invalid time metadata fail closed as NOT_EVALUABLE.

## Persistence proof

The UI does not evaluate the form object directly.

After an ObservedOutcome append succeeds, CEM queries the canonical IndexedDB reality_loop_objects store through its existing implementation_plan_id index and rebuilds the evaluation projection from those persisted records.

## Execution boundary

TRIGGER_MET means only that a persisted observation satisfies the prospectively declared IF condition.

It does not:

- execute THEN;
- execute STOP;
- execute REASSESS;
- mutate ImplementationPlan;
- mutate ProspectiveSnapshot;
- create a Decision Autopsy automatically;
- monitor external sources in the background;
- schedule notifications.

Human review remains required.

## Provenance boundary

The prior prospective object remains immutable. Trigger evaluation is a derived read-only interpretation of a frozen plan and later observation.

This remains consistent with the OA-7 W3C PROV-inspired append-only policy in which later observations and revisions do not silently rewrite prior entities.

Reference: https://www.w3.org/TR/prov-primer/

## Scientific boundary

No model equation, coefficient, intervention ranking, evidence state, semantic relation, reference trajectory or release metadata changes.

A user-declared threshold remains a planning threshold, not an empirically validated cut-off.

A manually entered ObservedOutcome remains a user-supplied retrospective record and does not constitute model validation by itself.

## Regression requirements

- post-snapshot matching observations can produce TRIGGER_MET or TRIGGER_NOT_MET;
- pre-snapshot phenomena are NOT_EVALUABLE;
- observations for another Indicator are NOT_EVALUABLE;
- evaluation is DERIVED_NOT_STORED and NO_AUTOMATIC_ACTIONS;
- IndexedDB query is by implementation_plan_id;
- browser regression proves the frozen prospective plan is unchanged after evaluation;
- full OA and browser CI remains green.

## Next gate

After this PR and post-merge CI are green, OA-7 may proceed to Decision Autopsy / revision trail in a separate PR.
