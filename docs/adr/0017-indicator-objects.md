# ADR 0017 — OA-7 Indicator objects

Status: Proposed.

## Context

OA-7 Reality Loop requires Indicator objects after Action Canvas and before signposts/triggers, adaptive planning, observations and Decision Autopsy.

The current M0 planner exposes two direct proximal quantities for an inspected bundle: mean false-claim sharing probability and mean true-claim sharing probability over 13 simulated steps. It does not yet expose operational intermediate or final real-world outcomes.

OGC Observations, Measurements and Samples and SOSA/SSN distinguish the observed property, procedure and result of an observation. OA-7 adopts that separation conceptually, but this slice does not claim conformance with OGC OMS or SOSA/SSN.

## Decision

The runtime adds two read-only Indicator definitions:

- `CEM.INDICATOR.M0.FALSE_SHARING.MEAN13`
- `CEM.INDICATOR.M0.TRUE_SHARING.MEAN13`

Each Indicator carries:

- stable ID;
- bilingual label;
- observed-property identifier;
- target stage = PROXIMAL;
- NUMBER result type;
- probability unit;
- desired direction;
- explicit computation procedure;
- source refs;
- bilingual limitations.

A separate simulation reading contains the current value for the inspected bundle.

## Observation boundary

A simulation reading is not an ObservedOutcome.

The runtime reading is explicitly tagged:

- `reading_kind = SIMULATION_RESULT`;
- `observation_status = NOT_OBSERVED`;
- no phenomenon time;
- no recorded time;
- no population/context observation record.

This preserves the schema distinction between SimulationResult and ObservedOutcome.

## Coverage boundary

Indicator coverage is explicit by Action Canvas stage:

- PROXIMAL — AVAILABLE_SIMULATION_INDICATORS;
- INTERMEDIATE — NOT_OPERATIONALIZED;
- FINAL — NOT_OPERATIONALIZED.

No intermediate or final Indicator is fabricated merely to complete the visual chain.

## Storage boundary

Indicator runtime objects remain read-only and are not written into Workspace v1 in this slice.

No storage migration, prospective snapshot, trigger, adaptive plan or observation record is introduced.

## Scientific boundary

This slice does not alter equations, coefficients, bundle ranking, model artifacts, evidence status or reference runs.

The indicator values are existing M0 outputs displayed with explicit definitions and provenance.

## Regression requirements

- exactly two operational M0 Indicator definitions;
- both target PROXIMAL;
- both readings are SIMULATION_RESULT and NOT_OBSERVED;
- property, procedure and value remain separate fields;
- intermediate/final coverage stays NOT_OPERATIONALIZED;
- no observation timestamps are introduced;
- browser and existing accessibility/reflow gates remain green.
