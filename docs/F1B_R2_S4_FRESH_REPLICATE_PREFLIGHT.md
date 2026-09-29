# F1b R2 S4 fresh-replicate preflight gate

Issue: #259

Status: **FRESH EXECUTION SELECTION FROZEN / NUMERICAL PREFLIGHT NOT YET RUN**

## Purpose

The retained-M2 equivalence replay validates that the new S4 executor reproduces retained M2 evidence exactly.

The broad S4 study also requires thousands of genuinely new scientific replicates outside the M2 prefix.

This gate freezes a small, deterministic operational preflight on fresh S4 replicates before W0.

It is not a scientific sample and cannot be interpreted as power or method performance.

## Prerequisite

The numerical preflight may execute only after the retained-M2 equivalence result is retained with:
- 12 selected rows;
- 12 exact matches;
- zero mismatches;
- broad executor authorization.

This gate may be implemented before that retained result exists, but may not execute before it exists.

## Fresh scientific selection

Exactly 18 scientific runs are selected from the retained 15,000-run S4 matrix.

### Null

Use replicate 20 for:
- ADD_NULL;
- CBD_NULL_ANCHOR_1;
- CBD_NULL_ANCHOR_2;

at both:
- missingness 0.00;
- missingness 0.15.

These six runs lie outside the retained M2 null prefix 0..19.

### Departure

Use replicate 5 for:
- ADD_SPECIFICITY_NEGATIVE_CONTROL;
- ADD_DEPARTURE_DIAGNOSTIC;
- CBD_DEPARTURE_DETECTION;

for:
- sign -1;
- sign +1;
- missingness 0.00;
- missingness 0.15.

Where more than one scientific cell matches role/sign/missingness, choose the lexicographically smallest scientific_run_id.

These 12 runs lie outside the retained M2 departure prefix 0..4.

## Frozen identities

Scientific runs:
- count: 18;
- SHA-256:
  `d55ce620877a7b64a8ce37312025756482ff287456b62811f6a5b8249197666e`.

Apply all four frozen methods to every run:
- POPULATION;
- HIERARCHICAL_0.5X;
- HIERARCHICAL_1X;
- HIERARCHICAL_2X.

Method rows:
- count: 72;
- SHA-256:
  `be00d6689e29d5af959baa747a72254f449ec4d4dd20cd070460dac71f7a0a21`.

## Coverage

The frozen selection covers:
- all five scientific roles;
- all three null identities;
- both restriction families;
- missingness 0.00 and 0.15;
- null and departure cases;
- both departure signs;
- all four inference methods.

The selection is outcome-independent and was frozen before fresh numerical execution.

## Numerical acceptance

For every selected run, fresh execution must:
- regenerate the deterministic dataset;
- match scientific_run_id and dataset_id;
- preserve paired missingness;
- use one shared dataset/mask across methods;
- retain dataset SHA-256;
- retain bootstrap seed/namespace;
- execute the qualified 199-draw prefix;
- continue at draw index 199 only when required;
- stop on the first refit failure;
- retain n=10,000 as the maximum total attempts;
- confirm Haswell runtime lineage.

Allowed terminal states:
- SEQUENTIAL_RESOLVED_AT_PREFIX;
- SEQUENTIAL_RESOLVED;
- SEQUENTIAL_UNRESOLVED_AT_CAP;
- BOOTSTRAP_REFIT_FAILURE_UNRESOLVED;
- PREFIX_EXECUTION_FAILURE_UNRESOLVED.

A scientifically unfavorable decision is not a preflight failure.

Only a structural, provenance, pairing, lineage, identity or executor violation fails the preflight.

## W0 boundary

W0 may start only after:
1. retained-M2 executor equivalence is retained;
2. this fresh-replicate preflight is numerically executed and retained;
3. the broad topology and row/shard/wave schema remain unchanged.

The preflight cannot alter W0 membership, methods, MCSE target, method selection, or release semantics.

## Version boundary

The next target release remains v0.2.0 under Issue #277.

The release blocker remains open until broad S4 is executed, retained and scientifically interpreted.

## Boundary

`FRESH PREFLIGHT RUNS = 18 / FROZEN`

`FRESH PREFLIGHT METHOD ROWS = 72 / FROZEN`

`FRESH NUMERICAL EXECUTION = NOT YET RUN`

`W0 = NOT YET AUTHORIZED`

`POWER = NOT VALIDATED`

`v0.2.0 BLOCKER = OPEN`
