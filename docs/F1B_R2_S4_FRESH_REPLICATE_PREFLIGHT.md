# F1b R2 S4 fresh-replicate preflight gate

Issue: #259

Status: **FRESH SELECTION FROZEN / EXECUTOR EQUIVALENCE RETAINED / NUMERICAL PREFLIGHT NOT YET RUN**

## Purpose

The retained-M2 replay has now shown that the new S4 executor reproduces retained M2 evidence exactly.

The broad S4 study also requires genuinely new replicates outside the retained M2 prefix.

This gate freezes a small, deterministic operational preflight on fresh S4 replicates before W0.

It is not a scientific sample and cannot be interpreted as power or method performance.

## Hard prerequisite

The preflight runner is bound to the retained executor-equivalence result:
- result path: `model/results/f1b_r2_s4_new_executor_equivalence_2026-09-29.json`;
- retained-result Git blob is pinned;
- 12 selected M2 rows;
- 12 exact matches;
- zero mismatches;
- broad-executor authorization;
- retained selection and reproduced-evidence digests.

If that retained result changes, fresh-preflight execution must fail closed.

## Fresh scientific selection

Exactly 18 scientific runs are selected from the retained 15,000-run S4 matrix.

### Null

Use replicate 20 for:
- ADD_NULL;
- CBD_NULL_ANCHOR_1;
- CBD_NULL_ANCHOR_2;

at:
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

Where more than one scientific cell matches role/sign/missingness, use the lexicographically smallest `scientific_run_id`.

These 12 runs lie outside the retained M2 departure prefix 0..4.

## Frozen identities

Scientific runs:
- count: 18;
- SHA-256:
  `d55ce620877a7b64a8ce37312025756482ff287456b62811f6a5b8249197666e`.

All four frozen methods are applied to every run:
- POPULATION;
- HIERARCHICAL_0.5X;
- HIERARCHICAL_1X;
- HIERARCHICAL_2X.

Method rows:
- count: 72;
- SHA-256:
  `be00d6689e29d5af959baa747a72254f449ec4d4dd20cd070460dac71f7a0a21`.

## Coverage

The frozen preflight covers:
- all five scientific roles;
- all three null identities;
- both restriction families;
- missingness 0.00 and 0.15;
- null and departure cases;
- both departure signs;
- all four inference methods.

Selection is outcome-independent and frozen before fresh numerical execution.

## Numerical acceptance

For every selected run, fresh execution must:
- regenerate the deterministic dataset;
- preserve scientific_run_id and dataset_id;
- preserve paired missingness;
- use one shared scientific dataset/mask across methods;
- retain dataset SHA-256;
- preserve bootstrap seed/namespace;
- execute the qualified 199-draw prefix;
- continue at draw index 199 only when required;
- stop at the first refit failure;
- retain n=10,000 as the maximum total attempts;
- confirm Haswell runtime lineage.

Allowed terminal states:
- SEQUENTIAL_RESOLVED_AT_PREFIX;
- SEQUENTIAL_RESOLVED;
- SEQUENTIAL_UNRESOLVED_AT_CAP;
- BOOTSTRAP_REFIT_FAILURE_UNRESOLVED;
- PREFIX_EXECUTION_FAILURE_UNRESOLVED.

A scientifically unfavorable reject/not-reject outcome is not a preflight failure.

Only structural, provenance, pairing, numerical-lineage, identity or executor violations fail the preflight.

## W0 boundary

W0 may start only after:
1. this gate is merged and its selection is executed;
2. the 18-run / 72-method-row numerical preflight completes;
3. that result is retained;
4. broad topology and row/shard/wave contracts remain unchanged.

The preflight cannot alter W0 membership, methods, MCSE target, method selection or release semantics.

## Version boundary

The next target release remains `v0.2.0` under Issue #277.

The release blocker remains open until broad S4 is executed, retained and scientifically interpreted.

## Boundary

`FRESH PREFLIGHT RUNS = 18 / FROZEN`

`FRESH PREFLIGHT METHOD ROWS = 72 / FROZEN`

`EXECUTOR EQUIVALENCE = RETAINED AND VERIFIED`

`FRESH NUMERICAL EXECUTION = NOT YET RUN`

`W0 = NOT YET AUTHORIZED`

`POWER = NOT VALIDATED`

`v0.2.0 BLOCKER = OPEN`
