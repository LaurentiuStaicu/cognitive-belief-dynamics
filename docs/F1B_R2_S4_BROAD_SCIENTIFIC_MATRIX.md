# F1b R2 S4 broad scientific matrix gate

Issue: #259

Status: scientific matrix frozen; methods not yet bound; no simulation executed.

## Purpose

Freeze the scientific dataset identities for the later S4 broad recovery characterization before the M2 eligible-method set is known.

This gate runs no fitter, bootstrap, sequential continuation, method comparison, or power calculation.

## Matrix

The frozen source identities are:
- 72 controlled-departure restriction cells;
- 3 null restriction identities;
- missingness 0.00 and 0.15;
- evaluation replicates exactly 0..99.

Counts:
- departure: 72 × 2 × 100 = 14,400;
- null: 3 × 2 × 100 = 600;
- total: 15,000 scientific runs before method multiplicity.

The null identities are ADD_NULL, CBD_NULL_ANCHOR_1, and CBD_NULL_ANCHOR_2.

## Precision

The prospective requirement is maximum worst-case component MCSE = 0.05.

For a component proportion:

MCSE = sqrt(p * (1-p) / n_eval).

At the worst case p=0.5 and n_eval=100:

sqrt(0.25 / 100) = 0.05.

This is a Monte Carlo precision criterion, not a power target.

## Prefix preservation

The broad matrix extends deterministic identities without modifying M1:
- departure prefix: replicates 0..4;
- null prefix: replicates 0..19.

The target is always the complete deterministic set 0..99, never a post-hoc set of additional favorable replicates.

## Implementation

Added:
- model/benchmarks/f1b_r2_s4_broad_scientific_matrix_v1.json;
- src/cognitive_epistemic_model/calibration/f1b_r2_s4_broad_scientific_matrix.py;
- scripts/build_f1b_r2_s4_broad_scientific_matrix.py;
- dedicated invariant tests.

The manifest must contain:
- 15,000 unique scientific-run IDs;
- 14,400 departure runs;
- 600 null runs;
- 7,500 runs per missingness regime;
- 150 cell × missingness strata;
- exactly 100 replicates per stratum.

## Method binding

This gate intentionally does not know the final inference-method list.

After M2 completes, a separate gate must bind the broad method set exactly to the retained M2 eligible_methods list and its exact provenance.

## Boundary

S4 scientific matrix = frozen.
S4 scientific runs = 15,000.
Evaluation replicates = exactly 0..99.
Target worst-case component MCSE = 0.05.
M2 eligible methods = not yet bound.
Inference execution = not authorized by this gate.
Power = not validated.
Core-grid and human-N freeze = not authorized by this gate.
