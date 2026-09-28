# F1b R2 deterministic OpenBLAS execution-lineage qualification

Issue: #227

Status: **IMPLEMENTED QUALIFICATION INFRASTRUCTURE / NOT EXECUTED / NON-AUTHORITATIVE**

## Why this gate exists

Stage C1 V1 is retained as failed. The numerical diagnosis in #223 found two reproducible trajectories under identical scientific inputs.

The final direct-correlation run showed:

- OpenBLAS `Haswell`: 13/13 source/retained trajectory;
- OpenBLAS `SkylakeX`: 3/3 failed-C1 trajectory.

The same failed trajectory occurred on both Intel and AMD runners when OpenBLAS selected `SkylakeX`. The same source trajectory occurred when OpenBLAS selected `Haswell`.

The prior isolation matrix also showed:

- `OPENBLAS_CORETYPE=Haswell`: 12/12 source trajectory;
- NumPy X86_V4 disabling did not consistently rescue;
- single-threading did not consistently rescue.

Therefore the next step is not a tolerance change or a rerun of failed C1 V1. It is a prospective numerical-execution lineage qualification.

## Candidate lineage

Candidate runtime contract:

`OPENBLAS_CORETYPE=Haswell`

The variable must be present before Python starts.

The requested environment variable is not enough by itself. The qualification must also confirm the OpenBLAS core selected at runtime.

OpenBLAS documents that a DYNAMIC_ARCH build selects a target at runtime and that `OPENBLAS_CORETYPE` can override that selection.

## Q0 — environment gate

The repository now contains:

- `model/benchmarks/f1b_r2_openblas_execution_lineage_v1.json`;
- `src/cognitive_epistemic_model/calibration/f1b_r2_openblas_lineage.py`;
- `scripts/verify_f1b_r2_openblas_lineage.py`;
- tests for fail-closed environment, runtime-core, draw-index and boundary checks.

Q0:

1. requires `OPENBLAS_CORETYPE=Haswell`;
2. verifies the frozen CI dependency-lock Git blob;
3. verifies the five protected scientific file blobs;
4. verifies the retained failed-C1 V1 result SHA-256;
5. launches a child Python process with `OPENBLAS_VERBOSE=2`;
6. forces NumPy and SciPy BLAS/LAPACK activity;
7. requires every reported OpenBLAS core to be `Haswell`;
8. records Python, NumPy, SciPy and platform identity.

Q0 runs no CBD scientific fit and generates no bootstrap draw.

## Q1 — sentinel qualification

Q1 remains an execution step, not part of the merged infrastructure.

It must use the same four predeclared #223 sentinels:

- exact-pass control;
- exact-observed/hash-failure;
- nonzero-within-tolerance/hash-failure;
- outside-tolerance/hash-failure.

Across multiple independent runners every execution must confirm:

- runtime OpenBLAS `Haswell`;
- exact dataset fingerprint;
- exact retained observed statistic;
- exact retained first-199 attempt-sequence SHA-256;
- no draw index >=199.

Any mismatch fails closed.

## Q2 — complete 224-stream qualification

Only after Q1 passes:

- replay all 224 unresolved Stage-B streams;
- use the unchanged Stage-C1 regeneration function;
- retain deterministic sharding;
- replay draw indices 0..198 only;
- require 224/224 exact attempt-sequence matches;
- retain the existing observed-statistic tolerance of `1e-10`;
- report exact observed-statistic equality separately.

Q2 does not rewrite the failed Stage-C1 V1 artifact.

## Q3 — versioned continuation lineage

If Q2 passes, a separate reviewed artifact must define a new versioned continuation lineage.

It must retain:

- failed C1 V1 as historical evidence;
- #223 OpenBLAS diagnosis;
- the exact qualified environment contract;
- Q1/Q2 artifacts and hashes;
- protected scientific blobs;
- frozen dependency-lock identity;
- unchanged sequential-controller parameters.

Only after that versioned lineage exists may a new formal C1 qualification be considered.

Stage C2 does not become authorized merely because Q0, Q1 or Q2 passes.

## Scientific boundary

This work concerns numerical reproducibility only.

It does not validate:

- model specification;
- bootstrap approximation;
- Type-I error;
- recovery power;
- human sample size;
- participant recruitment;
- runtime F1b activation.

Current boundary:

`STAGE_C1 V1 = FAILED / RETAINED`

`DETERMINISTIC EXECUTION LINEAGE = QUALIFICATION REQUIRED`

`STAGE_C2 = BLOCKED`

`AUTHORITATIVE CORE GRID / HUMAN N = NOT FROZEN`

`PARTICIPANT RECRUITMENT = NOT AUTHORIZED`

`RUNTIME F1B = NOT AUTHORIZED`
