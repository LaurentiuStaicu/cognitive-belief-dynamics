# F1b R2 S4 new-executor equivalence gate

Issue: #259

Status: **NEW EXECUTOR IMPLEMENTED / EXACT 12-ROW M2 REPLAY REQUIRED / BROAD EXECUTION BLOCKED**

## Purpose

Broad S4 contains 56,640 new method executions for scientific runs that have no retained M1/M2 terminal row.

Those runs need a new executor path that:
- generates the deterministic 199-attempt prefix;
- applies the same M2 sequential boundaries at n=199;
- continues with the same qualified controller when still active;
- stops on the first refit failure;
- retains unresolved-at-cap outcomes.

Before that path can be used on any new S4 scientific replicate, it must reproduce retained M2 evidence exactly.

This gate is an implementation-equivalence check, not a new scientific screen.

## Prefix failure semantics

For a new S4 method/run pair:

1. fit the observed restriction model;
2. generate draw indices 0..198 one by one using the existing M1/M2 RNG namespaces;
3. if the observed fit fails, retain:
   `PREFIX_EXECUTION_FAILURE_UNRESOLVED`;
4. if a bootstrap refit fails, stop immediately at that attempt and retain:
   `BOOTSTRAP_REFIT_FAILURE_UNRESOLVED`;
5. never redraw, reseed or fill a failed attempt;
6. only a complete failure-free 199-attempt prefix enters the M2 resampling-risk controller.

The old M1 fixed-screen helper deliberately continued after refit failures in order to count successful attempts against its >=180 threshold.

That behavior is not used by the S4 sequential executor.

## Failure-free sequential path

For 199 successful prefix attempts:
- calculate the same partial sum as M2;
- apply the same n=199 lower/upper boundaries;
- if resolved, stop at n=199;
- otherwise continue at draw index 199.

Continuation reuses:
- controller `F1B.R2.RESAMPLING_RISK_CONTROLLER.V1`;
- alpha 0.05;
- epsilon 0.001;
- half-spend 1000;
- first new draw index 199;
- maximum total attempts 10,000;
- first-refit-failure stop;
- unresolved-at-cap retention.

Population and hierarchical RNG namespaces remain unchanged.

## Exact equivalence selection

The retained M2 source contains four inference methods and three terminal status classes needed for broad execution:

- `SEQUENTIAL_RESOLVED_AT_PREFIX`;
- `SEQUENTIAL_RESOLVED`;
- `SEQUENTIAL_UNRESOLVED_AT_CAP`.

For each method × status pair select the lexicographically smallest retained M2 `scientific_run_id`.

This produces:
- 12 retained method rows;
- 7 unique scientific runs.

Canonical selected-row identity SHA-256:

`41062e2bf501799a41b78d412b33551685045b98b9a67c9d50a9a26131c16b36`

The selection is independent of scientific role, KL magnitude, direction or favorable outcome.

## Required equality

For every selected retained M2 row, the new executor must regenerate the scientific dataset and reproduce exactly:

- dataset SHA-256;
- inference method;
- bootstrap base seed;
- 199-attempt prefix SHA-256;
- observed statistic;
- prefix sum;
- prefix decision and boundary;
- continuation flag;
- first new draw index;
- new-attempt count;
- successful/failure counts;
- new-attempt sequence SHA-256;
- terminal status;
- terminal decision and boundary;
- terminal n;
- terminal sum;
- failure n.

Any mismatch blocks broad S4.

## Numerical lineage

The equivalence run must start Python with:

`OPENBLAS_CORETYPE=Haswell`

OpenBLAS verbose output from the scientific process must also report only the qualified Haswell lineage.

No fallback is allowed.

## Implementation

Added:
- `model/benchmarks/f1b_r2_s4_new_executor_equivalence_v1.json`;
- `src/cognitive_epistemic_model/calibration/f1b_r2_s4_broad_executor.py`;
- `src/cognitive_epistemic_model/calibration/f1b_r2_s4_new_executor_equivalence.py`;
- `scripts/run_f1b_r2_s4_new_executor_equivalence.py`;
- dedicated fail-closed/unit tests.

M1 and M2 retained implementations/results are not modified.

## Next step

Only after exact 12/12 equivalence is executed and retained may the same qualified executor implementation blob be used for W0-W3.

Broad execution remains:
- 15,000 scientific runs;
- 60,000 method identities;
- 3,360 validated imported M2 rows;
- 56,640 new method executions.

## Version boundary

The planned next release remains v0.2.0 under Issue #277.

This equivalence gate does not close the release blocker.

## Boundary

`EQUIVALENCE ROWS = 12 / FROZEN`

`UNIQUE SCIENTIFIC RUNS = 7`

`BROAD EXECUTION = BLOCKED UNTIL 12/12 EXACT`

`METHOD SELECTED = NO`

`POWER = NOT VALIDATED`

`v0.2.0 BLOCKER = OPEN`
