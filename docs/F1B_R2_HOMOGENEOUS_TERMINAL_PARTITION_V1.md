# F1b R2 homogeneous terminal resampling partition

Issue: #250

Status: **E0/E1 IMPLEMENTED / NO NEW BOOTSTRAP DRAWS / INTERPRETATION NOT YET EXECUTED**

## Purpose

This gate composes the complete homogeneous terminal resampling-risk state after H2 and C2.

It does not run the scientific simulator, fitter or sequential continuation again.

Inputs are frozen by exact artifact/hash:
- H2 raw Stage-B replay;
- C2 combined prospective continuation result;
- retained H2 and C2 result Git blobs;
- the pre-existing role-definition, controller, replay and C2 implementation Git blobs.

## Required terminal partition

The composition must contain exactly:
- 750 unique restriction runs;
- 526 H2 terminal decisions;
- 201 C2 terminal decisions;
- 23 C2 `SEQUENTIAL_UNRESOLVED_AT_CAP`;
- 727 total terminal decisions;
- zero bootstrap-refit-failure states.

The exact 224 H2 unresolved IDs must equal the exact 224 C2 target IDs.

The exact 23 C2 unresolved-at-cap IDs remain unresolved and are never imputed.

## Frozen scientific role semantics

Five roles are recognized.

### CBD_NULL_FALSE_REJECTION

Restriction: `CBD_COMPLEMENT_RESTRICTION`.

Expected direction: `NOT_REJECT_P_GT_ALPHA`.

A reject is a false-rejection diagnostic, not evidence of desired detection.

### ADD_NULL_FALSE_REJECTION

Restriction: `ADD_RESTRICTION`.

Expected direction: `NOT_REJECT_P_GT_ALPHA`.

A reject is a false-rejection diagnostic.

### CBD_DEPARTURE_DETECTION

Restriction: `CBD_COMPLEMENT_RESTRICTION`.

Expected direction: `REJECT_P_LE_ALPHA`.

This is a departure-detection diagnostic.

### ADD_SPECIFICITY_NEGATIVE_CONTROL

Restriction: `ADD_RESTRICTION`.

Expected direction: `NOT_REJECT_P_GT_ALPHA`.

A reject is a negative-control failure diagnostic.

### ADD_DEPARTURE_DIAGNOSTIC

Restriction: `ADD_RESTRICTION`.

Expected direction: `REJECT_P_LE_ALPHA`.

This is a departure-detection diagnostic.

These labels and directions are frozen before the terminal characterization is executed.

## Descriptive characterization

The output reports counts and proportions:
- globally;
- by restriction;
- by role;
- by axis;
- by KL target;
- by sign;
- by anchor;
- by evaluation replicate.

For every stratum:
- total count;
- resolved count;
- unresolved-at-cap count;
- reject count;
- not-reject count;
- expected-direction count;
- opposite-direction count;
- resolved-only descriptive proportions;
- total-denominator lower/upper bounds obtained by assigning every unresolved stream to either extreme.

Resolved-only proportions are explicitly descriptive and must not silently replace the full denominator.

The extreme bounds are descriptive bounds, not confidence intervals and not validated power estimates.

## Unresolved-at-cap characterization

For each of the 23 unresolved streams the result retains:
- full scientific identity;
- terminal n;
- terminal exceedance sum;
- lower and upper boundaries;
- distance above the lower boundary;
- distance below the upper boundary.

Boundary proximity is descriptive only and must not be converted to a missing decision.

## Interpretation decision

The implementation predeclares:
- `READY_FOR_NEXT_RECOVERY_POWER_CHARACTERIZATION` when partition integrity passes, all five semantic roles are valid, every role has at least one resolved decision, unresolved outcomes remain un-imputed, and descriptive bounds are computable;
- `CHARACTERIZATION_REFINEMENT_REQUIRED` if the terminal partition is valid but a role has no resolved decision or cannot support descriptive bounds;
- `STRUCTURAL_REDESIGN_REQUIRED` only when the frozen role semantics cannot be mapped to the scientific restriction question.

This gate does not itself validate recovery power.

## Implementation

Added:
- `model/benchmarks/f1b_r2_homogeneous_terminal_partition_v1.json`;
- `src/cognitive_epistemic_model/calibration/f1b_r2_homogeneous_terminal_partition.py`;
- `scripts/build_f1b_r2_homogeneous_terminal_partition.py`;
- dedicated fail-closed tests.

No simulator, fitter, controller or bootstrap continuation file is modified.

## Boundary

`H2 + C2 COMPOSITION ONLY`

`NEW BOOTSTRAP DRAWS = NOT AUTHORIZED`

`CAP EXTENSION = NOT AUTHORIZED`

`UNRESOLVED IMPUTATION = NOT AUTHORIZED`

`POWER = NOT YET VALIDATED`

`AUTHORITATIVE CORE GRID / HUMAN N = NOT FROZEN`

`PARTICIPANT RECRUITMENT = NOT AUTHORIZED`

`RUNTIME F1B = NOT AUTHORIZED`
