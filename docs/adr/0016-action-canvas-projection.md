# ADR 0016 — OA-7 read-only Action Canvas projection

Status: Proposed.

## Context

OA-7 Reality Loop is now contract-bound in main. The implementation roadmap orders Action Canvas before Indicator objects, signposts/triggers, adaptive plans, observations and Decision Autopsy.

The current intervention planner already has canonical problem framing, intervention levers, mechanism paths and direct simulated outputs. It does not yet have runtime Indicator objects or a persisted ImplementationPlan.

## Decision

The first OA-7 implementation slice is a read-only Action Canvas projection inside the existing planner.

It renders exactly six stages:

1. Problem
2. Target mechanism
3. Intervention
4. Proximal result
5. Intermediate result
6. Final outcome

The first three stages are derived from existing planner inputs. The proximal stage uses only direct M0 simulation output versus baseline. Intermediate and final stages are explicitly marked NOT_OPERATIONALIZED.

## Boundary

The Action Canvas is not an ImplementationPlan and is not stored in Workspace.

It may not:

- create Indicator IDs;
- record observations;
- imply a real-world population effect;
- convert the planner score into a final outcome;
- persist prospective snapshots;
- alter model equations, intervention scores or evidence status.

The UI states these limits directly.

## Rationale

This allows users to see the intended causal/decision chain while preserving epistemic honesty about missing stages. It also creates the correct handoff to the next roadmap item, Indicator objects, without inventing measurement objects early.

## Regression requirements

- exactly six stages;
- inspected bundle controls the mechanism/intervention projection;
- proximal result is tagged SIMULATED_OUTPUT;
- intermediate and final stages remain NOT_OPERATIONALIZED;
- no Action Canvas state is persisted;
- existing OA-6 reflow/browser gates remain green.
