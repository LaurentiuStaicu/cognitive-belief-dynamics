# ADR 0008 — OA-5B Active Understanding UI

Status: Proposed for OA-5B implementation.

## Context

OA-5A established the schema, deterministic AU-1/AU-2/AU-3 fixtures, interaction state machine and bounded local history contract. R6 requires a user-facing learning surface only after that contract is green.

## Decision

Add an explicit fourth Understanding mode, **Active Understanding**, under the existing `learning` application view.

The surface implements the contract sequence:

`Worked example -> Predict -> Reveal -> Explain -> Epistemic boundary -> Complete`.

The user may explicitly skip prediction. A submitted prediction may optionally include low/medium/high self-rated confidence. The canonical answer is read from the contract; the prediction cannot modify it.

Feedback is neutral: the interface says that a prediction matches or differs from the canonical result. It does not award points, ranks, streaks, traits or psychological labels.

The surface is bilingual and deep-linkable as:

- `#understanding/active/AU-1`
- `#understanding/active/AU-2`
- `#understanding/active/AU-3`

## Data and provenance

The canonical source remains `model/contracts/active_understanding_v1.json`.

The web prebuild copies that file to `public/model/active_understanding.json` as a runtime projection. It is not a second scientific source of truth.

Learning history uses the OA-5A local store and remains outside Workspace/Case provenance. The UI exposes a clear-history control and displays only the bounded categorical records allowed by the contract.

## Scientific boundary

OA-5B changes no model equation, coefficient, semantic entity/relation, empirical target, evidence status or scientific comparator.

Results remain normally visible in Theory, Mechanisms, Scenarios, Comparison, Map and Registry. Predict-before-reveal exists only inside the explicit Active Understanding mode.

## Accessibility

The UI uses fieldset/legend for prediction choices, native radio controls, labelled select controls, progress semantics, visible keyboard focus inherited from the application, an aria-live challenge stage, and responsive one-column reflow.

The browser gate verifies Romanian/English rendering, submit and skip flows, local history, mobile reflow and no regression of the other Understanding modes.
