# F1b R2 Resampling-Risk Controller V1

Status: **PROTOTYPE IMPLEMENTED / ALGORITHMIC VALIDATION ONLY**

Issue: #213  
Baseline: `126737d3cbb42f1de65c5ac3989012fc6671080f`

## Purpose

Provide a sequential Monte Carlo decision controller whose numerical error target is defined before looking at the replay outcome.

The controller addresses one narrow question:

> Given a valid bootstrap stream, how many resamples are needed before the Monte Carlo implementation can classify the ideal bootstrap p-value as being on one side of alpha with a prospectively bounded resampling risk?

It does not validate the scientific model or the parametric bootstrap approximation.

## Frozen prototype parameters

- alpha = 0.05;
- resampling-risk bound epsilon = 0.001;
- half-spend = 1000;
- spending sequence:

  `epsilon_n = epsilon * n / (1000 + n)`.

These values follow the Gandy sequential resampling-risk construction and the default parameterization currently exposed by the R package `simctest`.

The Python implementation is internal to CBD; R is not a runtime dependency.

## Bernoulli stream

For observed statistic `t` and bootstrap statistics `T_i`:

`X_i = 1[T_i >= t]`.

The controller tracks:

`S_n = sum X_i`.

At the decision threshold `p = alpha`, it recursively propagates the exact surviving Bernoulli probability mass that has not crossed either boundary.

For each n it chooses:

- the smallest upper boundary `U_n` whose cumulative upper-boundary probability does not exceed `epsilon_n`;
- the largest lower boundary `L_n` whose cumulative lower-boundary probability does not exceed `epsilon_n`.

## Decisions

- `S_n <= L_n` → `REJECT_P_LE_ALPHA`;
- `S_n >= U_n` → `NOT_REJECT_P_GT_ALPHA`;
- no boundary by the available prefix → `SEQUENTIAL_UNRESOLVED`.

Unresolved is a first-class output.

It is not recoded as non-rejection.

## Failure semantics

If a bootstrap-refit failure occurs in the prefix, the Bernoulli stream required by the risk guarantee is no longer complete.

The prototype therefore returns:

`BOOTSTRAP_REFIT_FAILURE_UNRESOLVED`

and does not renormalize around the failed draw.

## Exact probability accounting

The implementation stores at every n:

- `L_n`;
- `U_n`;
- spending allowance;
- cumulative lower-boundary probability under `p=alpha`;
- cumulative upper-boundary probability under `p=alpha`;
- surviving probability.

The invariant is:

`survivor + lower_hit + upper_hit = 1`

within the declared numerical tolerance.

Each cumulative boundary-hit probability must remain no larger than the current spending allowance.

## Behavior through 199 draws

For the frozen prototype:

At n=99:
- lower boundary = -1;
- upper boundary = 17.

Thus rejection is not yet possible through the lower boundary at n=99 under epsilon = 0.001.

At n=199:
- lower boundary = 0;
- upper boundary = 25.

A zero-exceedance stream first reaches the reject boundary at n=173.

A stream with a high exceedance rate can reach the non-reject boundary much earlier; for example an all-exceedance stream stops at n=5.

This behavior is intentional: a 0.1% resampling-risk target is stricter than merely computing a fixed-size Monte Carlo p-value.

## Stage-A tests

The repository tests require:

1. initial boundaries `U_1=2`, `L_1=-1`;
2. monotone spending;
3. both cumulative boundary probabilities below the spending allowance;
4. probability-mass conservation;
5. deterministic repeated boundary generation;
6. early upper-boundary stopping;
7. conservative lower-boundary stopping;
8. unresolved near-threshold behavior;
9. fail-closed bootstrap-refit failure handling;
10. invalid parameter rejection;
11. terminality of a reached decision.

## Stage B is still closed

This PR does not replay the retained #206 bootstrap streams.

After the controller passes the full CBD CI, the next step is a temporary replay-only execution using the exact #206 combined artifact:

- artifact ID `10938668225`;
- JSON SHA-256
  `b2727462b5bd09e5570090a42d7c90da8866e02100e0f4ccad551d8958a3d301`.

That replay may consume only the retained first 199 attempts.

No new bootstrap attempt is authorized by this implementation.

## Methodological boundary

A resampling-risk bound is conditional on the bootstrap sampling mechanism.

It does not bound:

- restriction-model misspecification;
- parametric-bootstrap approximation error;
- scientific Type-I error;
- power uncertainty;
- human-sample uncertainty.

## Boundary

`RESAMPLING-RISK CONTROLLER V1 = IMPLEMENTED`

`ALPHA = 0.05`

`EPSILON = 0.001`

`HALFSPEND = 1000`

`NEW BOOTSTRAP ATTEMPTS = NOT AUTHORIZED`

`DRAW COUNT = NOT SELECTED`

`POWER = NOT VALIDATED`

`AUTHORITATIVE CORE GRID / HUMAN N = NOT FROZEN`

`PARTICIPANT RECRUITMENT = NOT AUTHORIZED`

`RUNTIME F1B = NOT AUTHORIZED`
