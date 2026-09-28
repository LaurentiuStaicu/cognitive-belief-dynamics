# F1b R2 homogeneous paired-source numerical lineage

Issue: #234

Status: **H0 IMPLEMENTED / H1 NOT YET EXECUTED / NON-AUTHORITATIVE**

## Why a new paired source is required

The retained paired-bootstrap source was generated in five independent execution shards and is now known to contain multiple reproducible numerical trajectories.

The retained evidence shows:

- the Stage-C1-eligible portion from evaluation replicates 0–7 reproduces exactly under the tested OpenBLAS `Haswell` path;
- the 49 Stage-C1-eligible streams from evaluation replicates 8–9 reproduce exactly under the tested OpenBLAS `SkylakeX` path;
- seven independent naturally SkylakeX-capable runners reproduced those 49 R08_09 streams exactly, for 343/343 exact source reproductions.

The historical source remains valid provenance evidence. It is not a valid homogeneous numerical lineage for prospective continuation.

The project must not repair this by selecting a different OpenBLAS core for each historical shard.

## H0 — frozen contract

The new prospective numerical lineage is:

`F1B.R2.HOMOGENEOUS_PAIRED_SOURCE.LINEAGE.V1`

Candidate runtime:

`OPENBLAS_CORETYPE=Haswell`

This variable must be set before Python starts, and the actual runtime OpenBLAS core must be verified.

OpenBLAS DYNAMIC_ARCH supports runtime target selection. The documented `OPENBLAS_CORETYPE` variable overrides that target selection, while `OPENBLAS_VERBOSE=2` reports the selected target.

H0 protects:

- the five scientific files already frozen by the numerical-lineage investigation;
- the paired-characterization runner;
- the paired-characterization combiner;
- the frozen dependency lock;
- the paired design;
- the KL-v2 design and retained deterministic qualification;
- the distance-definition review;
- the historical controlled-departure design.

H0 also preserves:

- the existing scientific characterization identity;
- the existing dataset identities;
- the existing seed derivation;
- the 10 evaluation-replicate identities;
- bootstrap ordering;
- draw prefixes 49, 99 and 199;
- maximum retained draw index 198.

The new numerical lineage identity is external provenance metadata. It is deliberately not inserted into the scientific dataset identity because doing so would alter the frozen RNG identity.

## H0 verifier

The repository contains:

- `model/benchmarks/f1b_r2_homogeneous_paired_source_lineage_v1.json`;
- `src/cognitive_epistemic_model/calibration/f1b_r2_homogeneous_paired_lineage.py`;
- `scripts/verify_f1b_r2_homogeneous_paired_lineage.py`;
- dedicated fail-closed tests.

The verifier:

1. requires `OPENBLAS_CORETYPE=Haswell`;
2. verifies the dependency-lock Git blob;
3. verifies all protected scientific-file Git blobs;
4. verifies both protected execution-script Git blobs;
5. verifies SHA-256 for all frozen design/qualification inputs;
6. starts a child process with `OPENBLAS_VERBOSE=2`;
7. triggers NumPy and SciPy BLAS/LAPACK activity;
8. requires every reported OpenBLAS instance to be `Haswell`;
9. records Python, NumPy, SciPy, platform, CPU and relevant thread environment.

The H0 verifier performs no CBD scientific fit and generates no bootstrap draw.

## H1 — full homogeneous source regeneration

H1 is a separate temporary execution step after this infrastructure is merged.

It must use the unchanged paired-characterization runner and unchanged combiner.

Complete workload:

- evaluation replicates: 0..9;
- unique datasets: 390;
- restriction runs: 750;
- draw-count snapshots: 2,250;
- paired draw-count comparisons: 2,250;
- nested draw grid: 49 / 99 / 199;
- maximum draw index: 198.

The previous five two-replicate computational shards may be reused only if every worker uses the same prospective Haswell contract and independently confirms the actual OpenBLAS runtime core.

The combined scientific source JSON receives a new artifact and exact hash. A separate wrapper records the numerical-lineage identity and runtime provenance.

The old heterogeneous source is never overwritten.

## H1 acceptance

Generation success alone is insufficient.

A separate replay must verify a deterministic validation subset spanning:

- null and departure cases;
- both restrictions;
- evaluation replicates including 0, 7, 8 and 9.

Every validation stream must reproduce the newly generated homogeneous source exactly for:

- dataset fingerprint;
- observed statistic;
- complete first-199 attempt-sequence SHA-256.

Both generation and validation processes must runtime-confirm `Haswell`.

Historical-source comparison is retained as sensitivity evidence only. Equality to the heterogeneous source is not an H1 acceptance requirement.

## H2 — rebuild resampling-risk provenance

Historical Stage-B decisions cannot be inherited because they were computed from the heterogeneous source.

After H1 is retained and independently qualified, H2 must rerun the unchanged resampling-risk controller from the new homogeneous paired source through the retained 199-attempt prefix.

Unchanged controller:

- alpha = 0.05;
- epsilon = 0.001;
- half-spend = 1000;
- spending sequence `epsilon*n/(1000+n)`.

H2 must create a new versioned set of:

- terminal decisions;
- unresolved streams;
- stream checkpoints;
- aggregate summaries;
- source and artifact hashes.

Only after H2 is retained may a new continuation/C1 gate be specified for the new unresolved set.

## Boundary

`HISTORICAL PAIRED SOURCE = RETAINED / NUMERICALLY HETEROGENEOUS`

`H0 HOMOGENEOUS CONTRACT = IMPLEMENTED / NOT YET EXECUTED`

`H1 FULL SOURCE REGENERATION = REQUIRED`

`H2 STAGE-B REBUILD = REQUIRED AFTER H1`

`HISTORICAL STAGE-B CHECKPOINTS = NOT INHERITED`

`NEW DRAW INDEX >=199 = NOT AUTHORIZED`

`STAGE C2 = BLOCKED`

`STATISTICAL POWER = NOT VALIDATED`

`AUTHORITATIVE CORE GRID / HUMAN N = NOT FROZEN`

`PARTICIPANT RECRUITMENT = NOT AUTHORIZED`

`RUNTIME F1B = NOT AUTHORIZED`
