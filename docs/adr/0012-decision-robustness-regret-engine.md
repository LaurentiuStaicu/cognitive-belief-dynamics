# ADR 0012 — OA-6B deterministic robustness and regret engine

Status: Proposed for OA-6B integration.

## Context

R7 authorizes deterministic robustness and regret over the existing planner bundle/profile table after OA-6A establishes the uncertainty registry and the fail-closed probability boundary.

The current low/reference/high response profiles are finite declared scenarios with no probabilities. OA-6B therefore must not compute expected values, likelihoods, probability-of-best values or confidence intervals.

## Decision

OA-6B adds a pure TypeScript engine in `web/src/decision-robustness.ts`.

For every declared scenario, it computes:

- the best feasible score;
- the complete top set, preserving score ties;
- score rank where equal scores receive equal rank;
- regret relative to the best feasible score in that same scenario;
- optional acceptability against an explicitly supplied gain threshold.

Across scenarios, it computes for each alternative:

- feasible scenario count and denominator;
- top-rank scenario count and denominator;
- optional acceptable-scenario count and denominator;
- rank range;
- score range;
- gain range;
- maximum regret across scenarios where the alternative is feasible.

It also compares each scenario's complete top set with an explicit reference scenario and reports decision-switch conditions.

## Tie boundary

Alternative IDs are sorted only to make output serialization deterministic. ID order is never used to assign a better scientific or decision rank.

If two alternatives have scores equal within the declared numerical tolerance, both have the same rank and both appear in the top set when tied for best.

## Probability boundary

The engine accepts no scenario weights.

Its output explicitly declares:

`probabilityInterpretation = NOT_APPLICABLE_FINITE_DECLARED_SCENARIOS`.

Counts such as “top-ranked in 3 of 3 scenarios” or “acceptable in 2 of 3 scenarios” are scenario coverage summaries, not probabilities.

OA-6A remains the gate for any future probability-bearing consumer.

## Scientific-output boundary

OA-6B changes no intervention artifact, score formula, bundle, coefficient, reference run, evidence status, semantic status or release metadata.

The engine is not yet wired into the planner UI; that is OA-6C.

## Regression basis

Tests use the existing canonical `web/public/model/interventions.json` table.

They confirm:

- the default planner setting keeps bundle 14 top-ranked in all three profiles;
- a real existing decision switch is detected at budget 2, weight 50%, step 2: low -> bundle 10, reference/high -> bundle 6;
- regret is zero for scenario-best alternatives and never negative;
- score ties keep equal rank;
- threshold coverage remains a count/denominator rather than probability;
- malformed scenario tables fail closed.

## Next slice

After OA-6B integration and green post-merge CI, OA-6C may expose the uncertainty ledger, scenario comparison, robustness/regret and decision-switch explanations in the Act / Priorities & Plan UI.
