# F1b R2 paired inference-method M2 sequential-resolution gate

Issue: #259

Status: **IMPLEMENTED / PROSPECTIVE SEQUENTIAL-RESOLUTION DESIGN / NOT YET EXECUTED**

## Purpose

M2 converts the retained M1 fixed-199 prefixes into proper terminal sequential outcomes using the already qualified resampling-risk controller.

M2 does not reinterpret the fixed-199 M1 reject/not-reject snapshot as a terminal sequential decision.

Each method-specific stream is replayed exactly through draw index 198. Only streams still between the sequential boundaries may continue.

## M1 binding

M2 is bound to the retained M1 result:
- result:
  `model/results/f1b_r2_paired_method_m1_screen_2026-09-28.json`;
- M1 combined artifact ID: `10979254047`;
- combined JSON SHA-256:
  `dda3978acbf13ae9dba4d548ae8355413b29c8cac24ad86d5b8905de56d81042`;
- 840 scientific runs;
- 3,360 method-specific streams;
- 199 prefix attempts per stream;
- zero retained prefix refit failures.

M2 method membership is exactly the M1 eligible set:
- `POPULATION`;
- `HIERARCHICAL_0.5X`;
- `HIERARCHICAL_1X`;
- `HIERARCHICAL_2X`.

The M1 `HIERARCHICAL_SCALE_SENSITIVE` result remains active.

## Scientific matrix

M2 uses the exact M1 scientific matrix:
- missingness 0.00 and 0.15;
- all 72 departure cells;
- 5 departure replicates/cell/regime;
- 20 replicates per null identity/regime;
- 840 scientific restriction runs.

The exact same observed dataset and missingness mask are used across methods.

Hierarchical 0.5× / 1× / 2× retain common random numbers.

Population retains its separate bootstrap method namespace.

## Exact prefix replay

Before any new draw, every stream must reproduce:
- exact dataset fingerprint;
- exact M1 observed statistic;
- exact bootstrap base seed;
- exact 199-attempt sequence SHA-256;
- zero prefix refit failures.

Any mismatch fails closed.

A stream already on a sequential boundary at n=199 becomes terminal immediately and is not extended.

## Sequential controller

M2 reuses:

`F1B.R2.RESAMPLING_RISK_CONTROLLER.V1`

without modification:
- alpha = 0.05;
- epsilon = 0.001;
- half-spend = 1000;
- probability tolerance = 1e-12;
- prior attempts = 199;
- first new draw index = 199;
- maximum total attempts = 10,000;
- stop on lower/upper boundary;
- stop on first new bootstrap refit failure.

Terminal outcomes are:
- `REJECT_P_LE_ALPHA`;
- `NOT_REJECT_P_GT_ALPHA`;
- `BOOTSTRAP_REFIT_FAILURE_UNRESOLVED`;
- `SEQUENTIAL_UNRESOLVED_AT_CAP`.

The sequential-test design follows the same uniformly bounded resampling-risk logic already qualified for the homogeneous C2 continuation.

## M2 eligibility

M2 eligibility is about operational interpretability and sequential resolution, not power.

A method is `M2_ELIGIBLE` only if all rules pass.

### Refit stability

- overall refit-failure proportion <= 0.02;
- every role × missingness refit-failure proportion <= 0.05.

These are unchanged from the M1 operational screen.

### Overall resolution

By n=10,000:
- terminal reject/not-reject proportion >= 0.80.

Equivalently, combined refit-failure + unresolved-at-cap mass must be <= 0.20.

### Stratum resolution

Within every role × missingness stratum:
- terminal reject/not-reject proportion >= 0.60.

This prevents a method from being treated as broadly characterizable when a scientific stratum remains majority-indeterminate.

## Decision states

Each method receives exactly one:
- `M2_ELIGIBLE`;
- `M2_INELIGIBLE_REFIT_STABILITY`;
- `M2_INELIGIBLE_OVERALL_RESOLUTION`;
- `M2_INELIGIBLE_STRATUM_RESOLUTION`.

Multiple methods may remain eligible.

If no method remains eligible, inference redesign is required.

If one or more methods remain eligible, only those methods may proceed to the broad n_eval=100/cell characterization.

## Reporting

M2 reports:
- reject/not-reject/refit-failure/unresolved-at-cap counts;
- overall and role × missingness resolution;
- stopping-n distribution;
- checkpoints at n=199/499/999/1999/4999/10000;
- three-outcome expected-direction bounds;
- pairwise terminal-decision concordance;
- hierarchical terminal scale-sensitivity summaries.

No scale is selected by the largest detection rate.

## Sharding

Execution is prospectively fixed at 80 shards.

Shard assignment:
`SHA256(scientific_run_id) mod 80`.

All four methods for a scientific run remain in the same shard.

This is an operational partition only; it does not alter the scientific design.

## Broad-characterization boundary

M2 does not spend the final Monte Carlo replication budget.

The later broad target remains:
- n_eval = 100 per departure cell;
- worst-case component MCSE <= 0.05.

The n=100 requirement follows from the prospectively chosen CBD precision criterion for a Bernoulli component:

`sqrt(0.25 / n_eval) <= 0.05`.

Simulation-study methodology recommends choosing repetition counts from desired Monte Carlo precision and reporting Monte Carlo uncertainty rather than treating an arbitrary number of repetitions as adequate.

## Implementation

Added:
- frozen M2 benchmark contract;
- pure replay/continuation/evaluation module;
- deterministic 80-shard runner;
- fail-closed combiner;
- synthetic eligibility tests.

No M2 scientific result is included in this PR.

## Boundary

`M1 = COMPLETE / RETAINED`

`M2 DESIGN = FROZEN / NOT EXECUTED`

`M2 METHODS = ALL FOUR M1-ELIGIBLE VARIANTS`

`HIERARCHICAL SCALE SENSITIVE = RETAINED`

`CONTROLLER = UNCHANGED`

`POWER VALIDATED = NO`

`BROAD N_EVAL=100/CELL = NOT EXECUTED`

`AUTHORITATIVE CORE GRID / HUMAN N = NOT FROZEN`

`PARTICIPANT RECRUITMENT = NOT AUTHORIZED`

`RUNTIME F1B = NOT AUTHORIZED`
