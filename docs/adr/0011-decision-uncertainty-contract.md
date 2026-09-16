# ADR 0011 — OA-6A uncertainty contract and registry

Status: Proposed for OA-6A integration.

## Context

R7 authorizes Decision Under Uncertainty with an explicit restriction: the current low/reference/high planner profiles are finite sensitivity scenarios, not draws from a calibrated probability distribution.

The existing planner also contains user-controlled objective weights, user-supplied effort units and two intervention-timing choices. Those inputs influence the ranking but are not scientific model parameters.

OA-6 therefore needs a typed uncertainty layer before any robustness or regret calculation is added.

## Decision

OA-6A adds:

- `schemas/decision_uncertainty.schema.json`;
- `model/contracts/decision_uncertainty_v1.json`;
- a small fail-closed probability guard in `cognitive_epistemic_model.uncertainty`;
- regression tests that bind the response-profile scales and timing choices to the existing intervention artifact.

The registry separates:

- `SCIENTIFIC_UNCERTAINTY` from `DECISION_ASSUMPTION`;
- parameter uncertainty from structural uncertainty;
- preference assumptions from implementation assumptions;
- finite scenarios from bounded ranges and probability distributions.

The initial registry contains no probability-bearing object.

## Probability boundary

For finite scenarios, `NOT_AVAILABLE` means exactly that: no probability vector may be present.

A future finite-scenario object may use `USER_DECLARED`, `EMPIRICALLY_ESTIMATED` or `MODEL_DERIVED` only when an explicit probability vector is supplied.

The runtime guard refuses to invent equal weights and rejects missing, mismatched, out-of-range or non-normalized vectors.

Therefore neither scenario count nor scenario spacing can silently become probability.

## Scientific-output boundary

OA-6A does not change:

- any M0/M1 equation or coefficient;
- the 16 intervention bundles;
- the current planner score;
- any reference run;
- evidence status;
- semantic relation status;
- release metadata.

It adds product decision metadata and validation only.

## Next slice

After OA-6A integration and post-merge CI, OA-6B may implement deterministic robustness/regret functions over the existing bundle/profile table.
