# F1b R2 Resampling-Risk Replay V1

Status: **IMPLEMENTED / REPLAY-ONLY / NOT YET EXECUTED**

Issue: #213  
Controller Stage A: PR #214  
Baseline: `ab9886ceced97b192f4c278ea4ea28a7f59a07d6`

## Purpose

Replay the exact retained first-199 bootstrap attempts from the completed paired KL V2 characterization through the frozen Gandy-style resampling-risk controller.

This stage consumes retained bootstrap statistics only.

It does not:
- regenerate a synthetic dataset;
- refit a bootstrap replicate;
- extend any stream beyond 199 attempts;
- select 49, 99 or 199 as authoritative.

## Exact source

Retained paired artifact:
- artifact ID: `10938668225`;
- exact JSON SHA-256:
  `b2727462b5bd09e5570090a42d7c90da8866e02100e0f4ccad551d8958a3d301`;
- exact JSON size: 9,013,672 bytes;
- restriction runs: 750;
- bootstrap attempts per run: 199;
- retained bootstrap-refit failures: 0.

The runner verifies the exact JSON SHA-256 before parsing.

## Controller

Frozen parameters:
- alpha = 0.05;
- epsilon = 0.001;
- half-spend = 1000;
- maximum replay horizon = 199.

For each retained run:

`X_i = 1[T_i >= t_observed]`

and

`S_n = sum_{i=1}^n X_i`.

The replay stops when the frozen controller reaches either:
- lower boundary → `REJECT_P_LE_ALPHA`;
- upper boundary → `NOT_REJECT_P_GT_ALPHA`.

If neither boundary is reached by 199:

`SEQUENTIAL_UNRESOLVED`.

Unresolved is not recoded as a fixed-199 decision.

## Exact stream checkpoint

For every one of the 750 retained runs the replay stores:
- run ID;
- dataset SHA-256;
- bootstrap stream seed;
- observed statistic;
- SHA-256 of the canonical first-199 attempt sequence.

Canonical attempt hash:
- JSON array;
- `null` for failed attempts;
- compact separators;
- `allow_nan=false`;
- UTF-8;
- SHA-256.

## Retained fixed-199 consistency check

The replay independently reconstructs the plus-one Monte Carlo p-value:

`p = (1 + number_of_exceedances) / 200`.

This reconstructed p-value and reject/not-reject state must match the retained 199-draw snapshot exactly within numerical tolerance.

A mismatch fails closed.

## Outputs

Per run retain:
- scientific identity and role;
- restriction;
- anchor / axis / sign / KL target;
- evaluation replicate;
- stream checkpoint;
- sequential status;
- decision, if resolved;
- stopping n and S_n;
- boundary hit;
- terminal state;
- full S_199;
- resolved by 49 / 99 / 199 flags;
- reconstructed fixed-199 plus-one p-value;
- retained fixed-199 p-value/decision;
- sequential-vs-fixed disagreement, only when sequentially resolved.

Aggregate globally and by:
- restriction;
- role;
- axis;
- KL target;
- sign;
- anchor.

Each aggregate retains:
- resolved by 49;
- resolved by 99;
- resolved by 199;
- unresolved at 199;
- reject / not-reject counts among resolved;
- sequential-vs-fixed disagreement count;
- stopping-n histogram.

## Failure semantics

If a retained bootstrap attempt is `null`, the controller itself returns:

`BOOTSTRAP_REFIT_FAILURE_UNRESOLVED`.

For the frozen #213 replay source, the expected bootstrap-refit failure count is zero.

Therefore any observed failure count other than zero makes the exact replay source inconsistent with the frozen contract and fails the complete replay.

## Interpretation

The resampling-risk controller addresses only Monte Carlo implementation uncertainty conditional on the retained bootstrap mechanism.

It does not bound:
- model misspecification;
- bootstrap approximation error;
- scientific Type-I error;
- detection power;
- human-sample uncertainty.

A stream unresolved at 199 remains unresolved even if the retained fixed-199 test rejected or did not reject.

## Next gate

After the exact replay is retained, the project may determine:
- how many streams resolve by 49 / 99 / 199;
- which scientific strata remain unresolved;
- whether a prospectively frozen extension beyond 199 is computationally justified.

No extension cap beyond 199 is defined here.

## Boundary

`STAGE A CONTROLLER = VALIDATED`

`STAGE B REPLAY UTILITY = IMPLEMENTED / NOT YET EXECUTED`

`SOURCE = EXACT RETAINED 199-ATTEMPT STREAMS ONLY`

`NEW BOOTSTRAP ATTEMPTS = NOT AUTHORIZED`

`UNRESOLVED = FIRST-CLASS OUTCOME`

`DRAW COUNT = NOT SELECTED`

`POWER = NOT VALIDATED`

`AUTHORITATIVE CORE GRID / HUMAN N = NOT FROZEN`

`PARTICIPANT RECRUITMENT = NOT AUTHORIZED`

`RUNTIME F1B = NOT AUTHORIZED`
