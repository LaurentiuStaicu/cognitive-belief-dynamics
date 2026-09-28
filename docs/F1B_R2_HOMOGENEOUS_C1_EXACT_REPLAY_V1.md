# F1b R2 homogeneous Stage-C1 exact replay

Issue: #241

Status: **C0 IMPLEMENTED / C1 NOT YET EXECUTED / STAGE C2 BLOCKED**

## Purpose

This gate qualifies exact numerical reproduction of the 224 homogeneous H2 unresolved streams before any bootstrap draw index >=199 may be generated.

It is tied only to the prospectively homogeneous lineage:

- H1 source lineage: `F1B.R2.HOMOGENEOUS_PAIRED_SOURCE.LINEAGE.V1`;
- H1 source artifact ID: `10961527329`;
- H1 combined JSON SHA-256:
  `618b52162e98d25d41ac9cc7a6411ccfbf3c95775412a46b759e1514e90ed37e`;
- H2 raw Stage-B artifact ID: `10962483226`;
- H2 raw replay JSON SHA-256:
  `f0f32d92e46748148f020a4e0d47d2c63e27f6ab1aa36253346e15c4dfaf01e7`;
- H2 unresolved run-ID canonical SHA-256:
  `d2db2c97ad48544c082cdffd086c022a28c6d0c75690b36a0cd0b2b381c4ebac`;
- H2 stream-checkpoint canonical SHA-256:
  `9f554b3a94464782194f0921dc13718fce995e58e2e15159cb2461b3fbb3ded2`.

Historical Stage-B checkpoints are not a permitted input.

## Runtime lineage

Every C1 worker must start with:

`OPENBLAS_CORETYPE=Haswell`

before Python initialization.

The scientific worker must also report only `Haswell` at runtime. A requested environment variable without runtime confirmation is insufficient.

The candidate is an execution-lineage control only. It does not alter the scientific model, fitter, seeds, data identities or controller.

## Provenance binding

The C1 runner verifies:

1. frozen dependency-lock Git blob;
2. retained H1 result Git blob and H1 decision state;
3. retained H2 result Git blob and H2 decision state;
4. exact H1 source artifact SHA-256 and byte size;
5. exact H2 raw replay artifact SHA-256 and byte size;
6. all five protected scientific-file Git blobs;
7. the pre-existing Stage-C1 qualification implementation Git blob;
8. frozen paired/KL-v2/review/historical-design SHA-256 values.

The H2 raw artifact is not trusted through the retained summary alone.

The gate independently derives:

- the 224 unresolved run IDs from H2 `replay_rows`;
- all 750 H2 stream checkpoints;
- the canonical compact-JSON SHA-256 for both.

The derived hashes must exactly match the retained H2 provenance.

## C1 scientific execution

The new layer calls the existing Stage-C1 regeneration implementation unchanged.

For each of the 224 H2 unresolved streams it:

1. joins the run to the exact H1 homogeneous paired source;
2. joins the run to its independently verified H2 checkpoint;
3. regenerates the original dataset from the frozen identity and seed;
4. requires exact dataset fingerprint equality;
5. refits the unchanged restricted/general models;
6. compares the regenerated observed statistic using the frozen absolute tolerance `1e-10`;
7. reports exact observed-statistic equality separately;
8. regenerates the complete retained bootstrap prefix at draw indices 0..198;
9. requires exact first-199 attempt-sequence SHA-256 equality to both H1 and H2;
10. requires zero bootstrap refit failures.

No draw index >=199 is permitted.

## Acceptance

C1 passes only at:

`224 / 224`

with:

- exact dataset fingerprints;
- observed-statistic delta <= `1e-10`;
- exact first-199 attempt hashes;
- zero bootstrap refit failures;
- runtime-confirmed homogeneous Haswell execution.

The result additionally reports:

- exact observed-statistic equality count;
- number of nonzero observed deltas;
- maximum observed-statistic absolute delta;
- per-shard qualification counts.

## Implementation

Added:

- `model/benchmarks/f1b_r2_homogeneous_c1_exact_replay_v1.json`;
- `src/cognitive_epistemic_model/calibration/f1b_r2_homogeneous_c1_exact_replay.py`;
- `scripts/run_f1b_r2_homogeneous_c1_qualification.py`;
- `scripts/combine_f1b_r2_homogeneous_c1_qualification.py`;
- dedicated fail-closed tests.

The old scientific/qualification implementation remains unchanged and pinned by Git blob.

## Decision boundary

If C1 passes, the next step is a separate prospective homogeneous C2 contract. C1 itself does not authorize any new draw.

If C1 fails, Stage C2 remains blocked and the failure must be diagnosed without relaxing the environment, tolerance, hash equality, seed derivation, fitter settings or controller.

Therefore:

`H1 HOMOGENEOUS SOURCE = QUALIFIED`

`H2 HOMOGENEOUS STAGE-B = PASS / RETAINED`

`C0 HOMOGENEOUS C1 CONTRACT = IMPLEMENTED`

`C1 EXACT REPLAY = NOT YET EXECUTED`

`NEW DRAW INDEX >=199 = NOT AUTHORIZED`

`STAGE C2 = BLOCKED`

`STATISTICAL POWER = NOT VALIDATED`

`AUTHORITATIVE CORE GRID / HUMAN N = NOT FROZEN`

`PARTICIPANT RECRUITMENT = NOT AUTHORIZED`

`RUNTIME F1B = NOT AUTHORIZED`
