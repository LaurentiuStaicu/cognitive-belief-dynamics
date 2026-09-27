# F1b R2 CBD Closure Projection — Nested-Feasible Continuation

Status: **NUMERICAL-INTEGRITY IMPLEMENTATION / SCIENTIFIC DEFINITION UNCHANGED**

Issue: #187  
Baseline: `bf4e0184da867f1b2df4f27e8d9eaaa7d7871c7d`

## Problem

The #182 complement-envelope run exposed numerical increases in the selected closure objective when widening the diagnostic domain.

Observed first failures:

- A1− scalar 3.65: increase `1.2069843145778858e-09`;
- A2− scalar 3.50: increase `2.8114650947597131e-08`.

The frozen nested-objective tolerance is `1e-10`.

Because 8× is a subset of 16× and 16× is a subset of 32×, the selected solution from the preceding narrower domain remains feasible in the wider domain.

A true wider-domain minimum therefore cannot be worse.

The observed increases are numerical optimizer drift.

## Numerical correction

The scientific objective, domains and tolerance are unchanged.

At each widened domain the projector now:

1. runs every frozen common optimizer start unchanged;
2. carries the preceding selected response surface forward as an exact feasible candidate;
3. runs an additional optimizer start from that same preceding solution;
4. selects the lowest objective among:
   - frozen optimized starts;
   - optimized continuation start;
   - exact carried feasible candidate.

This enforces the mathematical nesting property without accepting a looser tolerance.

## Retained diagnostics

Each widened domain now records:

- previous domain multiplier;
- previous selected objective;
- exact carried feasible objective;
- carried-minus-previous objective;
- optimized continuation objective;
- best optimized objective before carry-forward comparison;
- raw apparent nested increase;
- whether the exact carry-forward candidate was selected;
- selected candidate source;
- feasible-candidate count.

The existing nested-objective guard remains active after selection.

## Counting semantics

`successful_start_count` and `failed_start_count` continue to refer only to optimizer starts.

The exact carry-forward candidate is not counted as an optimizer start.

It is included only in `feasible_candidate_count` and the continuation metadata.

## Scientific boundary

Nothing changes in:

- D1 stabilized utility RMS;
- D2 probability RMS;
- D3 Bernoulli KL;
- D3 direction;
- CBD response-family closure;
- 8× / 16× / 32× domains;
- original frozen starts;
- L-BFGS-B method and options;
- nested tolerance `1e-10`;
- operational fitter;
- KL v1 targets;
- structural rays;
- scalar range.

Historical #171 results remain historical results from their original source commit.

The corrected projector is prospective numerical infrastructure.

## Validation sequence

After this implementation is integrated:

1. reproduce the retained #171 12-surface closure review;
2. compare attainment counts, closure identities and response surfaces against the retained result;
3. retain any differences explicitly;
4. rerun the two #182 minus rays;
5. only then resume the complete envelope gate.

## Boundary

`NUMERICAL NESTING = EXPLICITLY ENFORCED`

`NESTED TOLERANCE = UNCHANGED`

`SCIENTIFIC DISTANCE / DOMAINS = UNCHANGED`

`#182 ENVELOPE = STILL BLOCKED UNTIL REGRESSION PASSES`

`STOCHASTIC CHARACTERIZATION / PAIRED BOOTSTRAP = NOT AUTHORIZED`
