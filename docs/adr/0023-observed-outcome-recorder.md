# ADR 0023 — OA-7 persistent ObservedOutcome recorder

Status: Proposed.

## Context

PR #69 materialized and persisted the canonical illustrative ImplementationPlan and embedded ProspectiveSnapshot. Post-merge CI #265 passed on `main`.

OA-7 can therefore add the first canonical retrospective record without rewriting any prospective state.

## Decision

This slice adds a manual `ObservedOutcome` recorder that follows the existing Reality Loop schema.

An observation is created only after a canonical ImplementationPlan has been frozen. Before append, the runtime verifies:

- the referenced ImplementationPlan exists in `reality_loop_objects`;
- `case_id` matches the persisted plan;
- `prospective_snapshot_id` exactly matches the snapshot embedded in that plan;
- the selected Indicator ID is frozen into the plan;
- the Indicator belongs to the corresponding Action Canvas result stage;
- observed property, stage and unit match the current Indicator definition.

The observation is then appended with IndexedDB `add()`; it never updates the ImplementationPlan or the ProspectiveSnapshot.

## Manual-observation boundary

The recorder does not infer an observation from a SimulationResult.

All retrospective fields are user supplied except canonical identities and Indicator-derived metadata:

- population;
- context;
- outcome description;
- feature of interest;
- procedure;
- phenomenon time;
- result time;
- result value;
- source references;
- optional quality note.

The currently operational M0 Indicators are numeric probabilities, so this slice accepts only finite values in `[0,1]` and records unit `probability`.

## Bilingual free-text boundary

The schema requires bilingual copy fields. This slice does not invent translations: user-entered free text is preserved verbatim in both schema language slots. The UI states this explicitly.

## Time boundary

The recorder rejects:

- invalid date-times;
- `phenomenon_time > result_time`;
- `result_time > recorded_at`.

`recorded_at` is generated at append time.

## Provenance boundary

Each record is:

- `retrospective = true`;
- `mutation_policy = APPEND_ONLY_NO_RETROACTIVE_PREDICTION_EDIT`.

Duplicate IDs continue to fail closed because the shared Reality Loop persistence adapter uses IndexedDB `add()`.

## Scientific boundary

This slice changes no model equation, parameter, empirical evidence state, ranking, simulation result or recommendation status.

The plan remains `ILLUSTRATIVE` / `DRAFT`. Recording an ObservedOutcome does not convert the M0 simulation into empirical validation or a real-world recommendation.

## Regression requirements

Unit tests must cover:

- exact canonical shape;
- plan/snapshot/Indicator reference mismatches;
- source de-duplication;
- probability range validation;
- temporal ordering.

Browser regression must:

1. freeze a real illustrative ImplementationPlan;
2. record a manual ObservedOutcome;
3. read both records from IndexedDB;
4. confirm the prospective plan is byte-for-byte unchanged;
5. confirm the outcome references the frozen plan/snapshot/Indicator and carries retrospective append-only policy.
