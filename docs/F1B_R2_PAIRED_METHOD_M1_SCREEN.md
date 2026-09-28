# F1b R2 paired inference-method M1 screen

Issue: #259

Status: **IMPLEMENTED / PROSPECTIVE SCREENING DESIGN / NOT YET EXECUTED**

## Purpose

M1 is the first scientific screening comparison of the four operationally qualified R2 restriction-inference variants:

- `POPULATION`;
- `HIERARCHICAL_0.5X`;
- `HIERARCHICAL_1X`;
- `HIERARCHICAL_2X`.

It is intentionally smaller than the later n=100/cell broad characterization.

M1 can eliminate inference variants showing gross pathology. It cannot validate power or select a human sample size.

## Scientific design

Missingness regimes:
- 0.00;
- 0.15.

Departure surface:
- all 72 frozen `role × axis × KL × sign × anchor` cells;
- KL 0.001 / 0.002 / 0.003;
- 5 evaluation replicates per departure cell per missingness regime.

Null calibration:
- ADD null: 20 replicates/regime;
- CBD null anchor 1: 20;
- CBD null anchor 2: 20.

Per missingness regime:
- 60 null restriction runs;
- 360 departure restriction runs;
- 420 total restriction runs.

Across both regimes:
- 840 scientific restriction runs;
- 4 inference variants;
- 3,360 method executions.

## Complete-data / missingness pairing

For a fixed scientific identity and replicate, complete data are generated with the existing stable H1 seed contract.

The missingness=0.15 dataset uses the same complete-data random stream and applies missingness only after outcomes are generated.

The implementation verifies that every retained 0.15 observation is an exact participant/item/response/covariate subset of the matching complete dataset.

All four inference variants receive the exact same observed dataset and missingness mask.

No failed method receives a regenerated dataset.

## Bootstrap screen

Every method execution uses:
- exactly 199 attempted bootstrap draws;
- >=180 successful refits for a valid snapshot;
- alpha 0.05;
- no draw index >=199.

M1 uses the label:

`FIXED_199_SCREEN_ONLY`

This is not a C2-style terminal sequential decision.

The later M2 stage, if reached, is responsible for sequential-resolution/unresolved-at-cap characterization.

## Eligibility criteria

### Operational

Method-wide fit/calibration failure proportion:
- <=0.02.

Within each role × missingness stratum:
- <=0.05.

Failures remain in scientific denominators.

### Null false-rejection gross screen

Within each missingness regime:
- pooled 60-null false-rejection proportion <=0.15.

Within each 20-replicate null identity:
- <=5 false rejections.

Passing does not validate nominal Type-I error.

### ADD specificity

Within each missingness regime:
- pooled standalone-accuracy ADD false-rejection <=0.20.

At each KL pooled across anchor/sign:
- <=0.30.

### Strong-departure signal separation

At KL=0.003, separately for:
- CBD departure detection;
- ADD departure diagnostic;

expected-direction rejection must exceed the same-method/same-regime pooled null false-rejection rate by >=0.10.

This is a minimal signal-separation rule, not a power target.

### Missingness degradation

Missingness 0.15 relative to 0.00 may increase:
- pooled null false rejection by <=0.10;
- pooled ADD-specificity false rejection by <=0.10.

Strong KL expected-direction rejection may decrease by <=0.20 for each departure role.

### Hierarchical scale sensitivity

0.5× / 1× / 2× are evaluated independently.

Additionally report a scale-sensitivity flag when maximum-minus-minimum expected-direction rate exceeds 0.20 for any missingness regime in:
- ADD specificity;
- strong CBD departure detection;
- strong ADD departure diagnostic.

The flag does not automatically choose 1×.

## Decision states

Each inference variant receives exactly one:

- `M1_ELIGIBLE`;
- `M1_INELIGIBLE_OPERATIONAL`;
- `M1_INELIGIBLE_NULL_OR_SPECIFICITY`;
- `M1_INELIGIBLE_SIGNAL_SEPARATION`;
- `M1_INELIGIBLE_MISSINGNESS`.

Multiple variants may remain eligible.

If none are eligible, inference redesign is required.

If one or more are eligible, only those variants may proceed to a separately frozen M2 sequential-resolution characterization.

## Broad-characterization boundary

M1 does not spend the final Monte Carlo budget.

The later broad target remains:
- n_eval = 100 per scientific departure cell;
- worst-case component MCSE <=0.05.

The n=100 run is authorized only for inference variant(s) still scientifically eligible after M1 and M2.

## Implementation

Added:
- frozen benchmark contract;
- pure validation / eligibility module;
- deterministic sharded runner;
- fail-closed shard combiner;
- dedicated tests.

No M1 scientific result is included in this PR.

## Boundary

`M1 DESIGN = FROZEN / NOT EXECUTED`

`BOOTSTRAP PREFIX = 199 / NO CONTINUATION`

`MISSINGNESS = 0 AND 0.15`

`METHOD SELECTED = NO`

`POWER VALIDATED = NO`

`BROAD N_EVAL = 100/CELL / NOT EXECUTED`

`AUTHORITATIVE CORE GRID / HUMAN N = NOT FROZEN`

`PARTICIPANT RECRUITMENT = NOT AUTHORIZED`

`RUNTIME F1B = NOT AUTHORIZED`
