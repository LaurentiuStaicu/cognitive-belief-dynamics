# F1b R2 Finite-Logit Projection — Nested-Feasible Continuation

Status: **NUMERICAL-INTEGRITY IMPLEMENTATION / SCIENTIFIC DEFINITION UNCHANGED**

Issue: #195  
Baseline: `e623705f24dce27e74947acfeee95ab99ae26150`

## Problem

The historical regression gate #190 exposed a finite-logit nested-domain optimizer drift after the closure projector had already been corrected.

Measured first failure:

- case: `CBD_ANCHOR_1__COMPLEMENT_RELATION_VIOLATION__MINUS__RMS_0.50`;
- candidate: `PROBABILITY_RMS`;
- transition: 8× → 16×;
- previous objective: `0.0058707141891874114`;
- wider selected objective: `0.0058707212894386898`;
- increase: `7.1002512784176797e-09`;
- frozen tolerance: `1e-10`;
- successful starts: 9/9;
- active bounds at the wider selected solution: none.

Because the 8× parameter box is a strict subset of the 16× box, the 8× selected parameter vector remains feasible at 16×.

A true wider-domain minimum therefore cannot be worse.

The measured increase is numerical optimizer/selection drift.

## Numerical correction

The finite-logit scientific candidate objective and parameterization are unchanged.

At each widened domain:

1. every frozen common start is optimized unchanged;
2. the previous selected parameter vector is retained as an exact feasible candidate;
3. its objective is evaluated exactly in the widened domain;
4. an additional deterministic optimization starts from that vector;
5. the selected result is the lowest objective among:
   - all common optimized starts;
   - the optimized continuation start;
   - the exact carried feasible candidate.

The existing nested-objective guard remains active after selection.

## Retained metadata

Each widened domain records:

- selected start source;
- feasible-candidate count;
- previous domain multiplier;
- previous selected objective;
- exact carried feasible objective;
- carried-minus-previous objective;
- optimized continuation objective;
- raw best optimized objective;
- raw apparent nested increase;
- whether the exact carry-forward candidate was selected.

## Counting semantics

`successful_start_count` and `failed_start_count` count optimizer starts only.

The exact feasible carry-forward candidate is not an optimizer start and is counted only in `feasible_candidate_count`.

## Scientific boundary

Nothing changes in:

- D1 stabilized utility RMS;
- D2 probability RMS;
- D3 Bernoulli KL;
- finite-logit CBD parameterization;
- 8× / 16× / 32× domains;
- frozen common starts;
- L-BFGS-B method/options;
- nested tolerance `1e-10`;
- closure projection;
- operational fitter;
- KL v1 targets/rays/range;
- historical #171 artifact.

## Validation sequence

After this implementation is integrated:

1. resume #190;
2. rerun all 12 retained surfaces × 3 candidates;
3. compare the corrected exact result against the immutable historical #171 artifact;
4. retain attainment/closure identities and response-surface/objective differences;
5. only if regression is acceptable may #182 resume.

## Boundary

`FINITE-LOGIT NESTING = EXPLICITLY ENFORCED`

`NESTED TOLERANCE = UNCHANGED`

`SCIENTIFIC DISTANCE / DOMAINS = UNCHANGED`

`HISTORICAL #171 = IMMUTABLE`

`#190 REGRESSION = REQUIRED BEFORE #182`

`STOCHASTIC / PAIRED BOOTSTRAP = NOT AUTHORIZED`
