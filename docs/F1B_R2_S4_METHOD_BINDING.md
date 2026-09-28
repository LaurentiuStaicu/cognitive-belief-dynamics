# F1b R2 S4 method-binding gate

Issue: #259

Status: **M2 METHODS BOUND TO RETAINED S4 MATRIX / BROAD EXECUTION NOT YET RUN**

## Purpose

This gate joins two independently retained results without changing either one:

1. the completed M2 inference-method eligibility result;
2. the completed S4 broad scientific matrix manifest.

It defines the exact method-bound broad execution identity before any broad method run begins.

## Retained M2 source

The binding pins:
- workflow run `36450594439`;
- artifact ID `10987519941`;
- combined JSON SHA-256 `b9034afd6b6837c8433e0d42fd90911a7b560e18225de7d551f559330742c808`;
- row-identity SHA-256 `b21ee68fd61a0f1364c0722e73ff472119075ae32ee380021b8a671df76c4707`.

The exact eligible-method order is:
1. `POPULATION`;
2. `HIERARCHICAL_0.5X`;
3. `HIERARCHICAL_1X`;
4. `HIERARCHICAL_2X`.

All four are M2-eligible.

No method is selected as winner.

Hierarchical scale sensitivity remains part of the retained scientific result.

## Retained S4 matrix source

The binding pins:
- workflow run `36463026247`;
- artifact ID `10988228984`;
- manifest JSON SHA-256 `f0691a0dc153f2ee1463f5115feeff448b49e7d2fb7accd6568a0fb8c43a5f01`;
- canonical 15,000-run ID SHA-256 `851e7336387901ca15d2486ed8efc19cd090ffac869b760352106a3f455f2b43`.

The retained matrix contains:
- 15,000 scientific runs;
- 14,400 departure;
- 600 null;
- missingness 0.00 / 0.15;
- evaluation replicates exactly 0..99;
- 150 cell × missingness strata;
- 100 replicates per stratum.

The prospective worst-case component MCSE target remains 0.05.

## Bound broad execution

The only admissible broad design is:

`15,000 scientific runs × 4 methods = 60,000 method executions`.

Every scientific run must be evaluated by every method.

A failed or unresolved method/run pair may not be replaced by another replicate.

All methods must see the same scientific dataset and missingness mask for a given scientific run.

Hierarchical scale variants preserve the common-random-number contract.

Population preserves its distinct bootstrap namespace.

## Implementation

Added:
- `model/benchmarks/f1b_r2_s4_method_binding_v1.json`;
- `src/cognitive_epistemic_model/calibration/f1b_r2_s4_method_binding.py`;
- `scripts/build_f1b_r2_s4_method_binding.py`;
- dedicated fail-closed tests.

The runner verifies:
- exact Git blobs of the retained M2 and S4 result files;
- exact protected M2/S4 design and implementation blobs;
- exact method order/set;
- exact scientific-run count and run-ID digest;
- exact 60,000 method-execution count;
- unchanged non-selection and scientific-boundary semantics.

## What this gate authorizes

After successful execution of the binding runner, the project may design/execute the exact broad characterization defined above.

It does not authorize:
- dropping a method;
- selecting a hierarchical scale;
- changing the scientific matrix;
- validating power;
- freezing a human N;
- participant recruitment;
- runtime F1b activation;
- the v0.2.0 release.

The v0.2.0 release gate remains blocked until the broad characterization itself is executed, retained and scientifically interpreted.

## Boundary

`M2 ELIGIBLE METHODS = 4 / 4 / FROZEN`

`S4 SCIENTIFIC RUNS = 15,000 / FROZEN`

`S4 METHOD EXECUTIONS = 60,000 / FROZEN`

`METHOD SELECTED = NO`

`BROAD EXECUTION = NOT YET PERFORMED`

`POWER = NOT VALIDATED`

`v0.2.0 BLOCKER = NOT YET CLOSED`
