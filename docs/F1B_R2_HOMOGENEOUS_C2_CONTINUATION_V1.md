# F1b R2 homogeneous Stage-C2 continuation gate

Issue: #245

Status: **D0/D1 IMPLEMENTED / C2 NOT YET EXECUTED / NO NEW DRAW GENERATED**

## Purpose

This gate is the prospective implementation boundary for continuing the 224 homogeneous H2/C1 unresolved streams beyond the retained first-199 bootstrap attempts.

It is the first component in the new homogeneous lineage that contains code capable of generating a previously unseen bootstrap draw.

Ordinary repository validation does not execute that code.

Scientific C2 execution remains a separate temporary PR after this gate is reviewed, CI-green and merged.

## Qualified inputs

H1 source:

- lineage `F1B.R2.HOMOGENEOUS_PAIRED_SOURCE.LINEAGE.V1`;
- artifact ID `10961527329`;
- JSON SHA-256
  `618b52162e98d25d41ac9cc7a6411ccfbf3c95775412a46b759e1514e90ed37e`.

H2 Stage-B:

- raw artifact ID `10962483226`;
- JSON SHA-256
  `f0f32d92e46748148f020a4e0d47d2c63e27f6ab1aa36253346e15c4dfaf01e7`;
- checkpoint SHA-256
  `9f554b3a94464782194f0921dc13718fce995e58e2e15159cb2461b3fbb3ded2`;
- unresolved-run SHA-256
  `d2db2c97ad48544c082cdffd086c022a28c6d0c75690b36a0cd0b2b381c4ebac`.

Homogeneous C1:

- retained result Git blob
  `bbcac59937966b41f265ab50fe04b19ee0bfb8cf`;
- execution artifact ID `10965746901`;
- combined result JSON SHA-256
  `823d6fedf14d371d0d58822e3176ff8abe80b5d41575f4d11214d963a5df64c9`;
- 224/224 passes;
- 224/224 exact observed statistics;
- 224/224 exact first-199 attempt hashes;
- 224/224 bootstrap-refit-failure free.

Historical C1/C2 evidence is not a source for this continuation.

## D0 frozen controller

The controller remains unchanged:

- alpha = `0.05`;
- epsilon = `0.001`;
- half-spend = `1000`;
- spending sequence `epsilon_n = epsilon*n/(1000+n)`;
- probability tolerance = `1e-12`.

The first retained segment is exactly:

- draw indices 0..198;
- total attempts n = 199.

The prospective cap remains:

`N_MAX = 10000`.

The cap is inherited from the prospective #218 contract, not selected from the homogeneous stopping results.

## D0 execution lineage

Every scientific worker must start with:

`OPENBLAS_CORETYPE=Haswell`

before Python starts.

Every worker must also report only `Haswell` at runtime.

No fallback is accepted.

OpenBLAS documents that in DYNAMIC_ARCH builds `OPENBLAS_CORETYPE` overrides runtime target autodetection and `OPENBLAS_VERBOSE=2` reports the selected target. These controls are execution-lineage constraints; they do not alter the scientific model.

## D1 target binding

Before entering the new-draw loop, the runner verifies:

1. frozen dependency lock;
2. five protected scientific file blobs;
3. the frozen resampling-risk controller config Git blob;
4. resampling-risk controller/replay file blobs;
5. historical continuation helper, homogeneous C1 binding, and OpenBLAS-lineage file blobs;
6. retained H1/H2/C1 repository-result blobs;
7. exact H1/H2/C1 Actions artifact SHA-256 values and byte sizes;
8. frozen paired/KL-v2/review/historical-design SHA-256 values;
9. H2 checkpoint and unresolved-set canonical hashes;
10. H1/H2 equality of dataset fingerprint, bootstrap stream seed, observed statistic, and first-199 attempt hash for every target.

The target set is then derived independently from H2.

Exactly 224 streams must be unresolved.

The C1 combined execution artifact must contain exactly those same 224 run IDs and every row must retain:

- C1 qualification pass;
- exact dataset fingerprint;
- observed-statistic match;
- exact first-199 attempt hash;
- bootstrap-refit-failure freedom.

Resolved H2 streams cannot enter the binding.

D1 itself generates no new bootstrap draw.

## D2 scientific continuation

For each bound target:

1. regenerate the original dataset;
2. require exact dataset fingerprint;
3. refit the unchanged observed restriction pair;
4. require observed-statistic absolute delta <= `1e-10`;
5. verify the retained H1/H2/C1 first-199 prefix binding;
6. initialize the partial exceedance sum at n=199;
7. generate the first new bootstrap draw at index `199`;
8. continue with contiguous indices only;
9. update the unchanged sequential boundary after each successful fit;
10. stop immediately on a lower boundary, upper boundary, bootstrap-refit failure, or n=10000.

New draw range:

`199..9999`.

The RNG identity remains:

`SeedSequence([bootstrap_stream_seed, restriction_index, draw_index])`.

The continuation never regenerates or overwrites indices 0..198.

## Boundary decisions

Lower boundary:

`REJECT_P_LE_ALPHA`.

Upper boundary:

`NOT_REJECT_P_GT_ALPHA`.

A bootstrap-refit failure stops the stream as:

`BOOTSTRAP_REFIT_FAILURE_UNRESOLVED`.

The failed attempt is retained as a failed attempt. It is not deleted, imputed or renormalized.

A stream that reaches n=10000 without a boundary remains:

`SEQUENTIAL_UNRESOLVED_AT_CAP`.

It is not classified from a fixed-size p-value.

## Partitioning

Execution uses 16 fixed shards:

`SHA256(run_id) modulo 16`.

Sharding does not depend on any outcome or scientific stratum.

Every stream keeps exactly the same run-to-shard mapping on retry.

## Reporting checkpoints

Aggregate state is retained at total n:

- 199;
- 499;
- 999;
- 1999;
- 4999;
- 10000.

These checkpoints are descriptive only.

They do not change stopping or the prospective cap.

## Per-stream provenance

C2 retains:

- H1/H2/C1 binding;
- run/scientific identity;
- bootstrap stream seed;
- regenerated dataset/observed verification;
- prior n=199 exceedance sum;
- retained-prefix SHA-256;
- first/last new draw index;
- number of new attempts and successful refits;
- new-segment SHA-256;
- full prefix+continuation SHA-256;
- status/decision/stopping n;
- boundary hit;
- failure n/draw index where applicable;
- terminal n/sum/boundaries;
- checkpoint states;
- runtime OpenBLAS identity copied into every per-stream row after the scientific worker's actual core report is verified.

## Aggregate provenance

The combiner requires all 16 shards and exactly 224 unique run IDs.

It reports:

- newly resolved/reject/not-reject;
- refit-failure unresolved;
- unresolved at cap;
- total new attempts;
- successful new fits;
- stopping distribution;
- reporting-checkpoint counts;
- restriction/role/axis/KL/sign/anchor/evaluation-replicate strata.

## Ordinary CI safety

The repository tests exercise:

- contract validation;
- environment guards;
- draw-index guards;
- H1/H2/C1 retained-result bindings;
- synthetic 224-target binding;
- synthetic 16-shard combination.

They do not call the scientific C2 continuation loop.

Therefore merging the gate implementation does not itself generate draw index 199.

## Execution boundary

After this implementation is merged, C2 must be run from a separate temporary execution PR.

That workflow must:

- download the exact H1, H2 and C1 artifacts;
- set `OPENBLAS_CORETYPE=Haswell` before Python startup;
- run 16 deterministic shards;
- capture `OPENBLAS_VERBOSE=2`;
- verify every scientific worker reports only `Haswell`;
- annotate the shard and every per-stream row with those verified runtime cores before combination;
- upload every shard and combined result;
- close the temporary PR unmerged.

The C2 result must then be retained in a separate reviewed PR.

## Scientific boundary

C2 remains a numerical resampling-risk continuation.

It does not validate:

- model specification;
- parametric-bootstrap approximation;
- scientific Type-I error;
- recovery power;
- authoritative core grid;
- human N;
- participant recruitment;
- runtime F1b activation.

The n=10000 cap is a computational truncation, not a selected fixed bootstrap draw count.

## Boundary

`H1 HOMOGENEOUS SOURCE = QUALIFIED`

`H2 HOMOGENEOUS STAGE-B = PASS / RETAINED`

`C1 HOMOGENEOUS EXACT REPLAY = PASS 224/224 / RETAINED`

`C2 D0/D1 IMPLEMENTATION = PRESENT / NOT YET EXECUTED`

`FIRST NEW DRAW INDEX 199 = NOT YET GENERATED`

`MAXIMUM TOTAL ATTEMPTS = 10000 / PROSPECTIVE`

`RESOLVED H2 STREAMS = TERMINAL / NOT EXTENDED`

`HISTORICAL C2 = NOT INHERITED`

`FIXED BOOTSTRAP DRAW COUNT = NOT SELECTED`

`POWER = NOT VALIDATED`

`AUTHORITATIVE CORE GRID / HUMAN N = NOT FROZEN`

`PARTICIPANT RECRUITMENT = NOT AUTHORIZED`

`RUNTIME F1B = NOT AUTHORIZED`
