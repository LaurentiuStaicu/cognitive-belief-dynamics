# ADR 0007 — OA-5A Active Understanding contract

Status: Proposed for OA-5A implementation.

## Context

R6 adopted Active Understanding with limits. OA-5A establishes the data and interaction contract before any user-facing learning UI.

## Decision

OA-5A adds exactly three foundation challenge families from R6:

- AU-1: exposure versus familiarity;
- AU-2: belief versus sharing;
- AU-3: computational dependency versus registered evidence relation.

The canonical challenge registry is schema-validated and contains only bilingual prompts, categorical choices, canonical semantic references, explanation/boundary copy, and deterministic fixtures tied to already-existing CEM artifacts.

The runtime interaction is a small state machine:

`WORKED_EXAMPLE -> PREDICT -> REVEAL -> EXPLAIN -> BOUNDARY -> COMPLETE`.

Prediction is optional: an explicit skip may advance from PREDICT to REVEAL. A submitted prediction may include learner confidence `low | medium | high`. Confidence is a learner-entered metacognitive judgment only.

Prediction never mutates or replaces the canonical result.

## Local history

Learning history is separate from Workspace/Case provenance.

Version 1 stores only:

- challenge ID;
- canonical target refs;
- prediction category;
- optional learner confidence;
- correct/incorrect outcome category;
- timestamp.

It uses local storage key `cem.active-understanding.history.v1`, is capped at 100 records, fails closed on corrupt/future data, and provides a clear operation.

It stores no free-form notes, telemetry, account identity, cloud state, scientific provenance, or psychological trait score.

## Scientific boundary

OA-5A adds no model equation, coefficient, empirical target, evidence status, semantic entity family or scientific comparator.

AU-1 resolves against the existing Repetition reference run.
AU-2 resolves against the existing Accuracy cue -> W computational dependency.
AU-3 explicitly contrasts the computational-dependency layer with the registered-evidence layer.

No UI is added in OA-5A. User-facing Active Understanding is deferred to OA-5B.

## Exit gate

OA-5A is complete only when:

- JSON Schema validation passes;
- AU-1/AU-2/AU-3 semantic references resolve;
- deterministic fixtures match canonical artifacts;
- TypeScript state-machine tests pass;
- local history is bounded and clearable;
- Workspace schema remains unchanged;
- full Python, TypeScript and browser regression CI stays green.
