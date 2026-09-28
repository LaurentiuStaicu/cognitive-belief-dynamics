# F1b R2 homogeneous Stage-C1 exact-replay result — 2026-09-28

Issue: #241

Status: **C1 PASS 224/224 / RETAINED / SEPARATE C2 CONTRACT REQUIRED**

## Purpose

This result qualifies exact numerical reproduction of the homogeneous H2 unresolved streams before any bootstrap draw index >=199 is generated.

The result belongs only to the prospectively homogeneous numerical lineage.

## Qualified source provenance

H1 homogeneous source:

- lineage: `F1B.R2.HOMOGENEOUS_PAIRED_SOURCE.LINEAGE.V1`;
- artifact ID: `10961527329`;
- combined JSON SHA-256:
  `618b52162e98d25d41ac9cc7a6411ccfbf3c95775412a46b759e1514e90ed37e`.

H2 homogeneous Stage-B:

- raw replay artifact ID: `10962483226`;
- raw replay JSON SHA-256:
  `f0f32d92e46748148f020a4e0d47d2c63e27f6ab1aa36253346e15c4dfaf01e7`;
- unresolved run-ID canonical SHA-256:
  `d2db2c97ad48544c082cdffd086c022a28c6d0c75690b36a0cd0b2b381c4ebac`;
- stream-checkpoint canonical SHA-256:
  `9f554b3a94464782194f0921dc13718fce995e58e2e15159cb2461b3fbb3ded2`.

The 224 target streams were derived from H2. Historical Stage-B checkpoints were not used.

## Execution

Temporary execution:

- PR #243 — closed unmerged;
- workflow run `36412794404`;
- execution head `91cd706e94c9a596a1f52d7cbe758a3ac4060a03`;
- qualified main baseline `8c7f5760bdba915662d92ff29fb0098a3baec023`.

Runtime contract:

`OPENBLAS_CORETYPE=Haswell`

Every scientific shard runtime-confirmed:

`Haswell, Haswell`

No environment fallback occurred.

The workflow was split into eight deterministic SHA256(run_id) shards with counts:

- shard 0: 21;
- shard 1: 31;
- shard 2: 21;
- shard 3: 29;
- shard 4: 21;
- shard 5: 30;
- shard 6: 38;
- shard 7: 33.

Total:

`224`

## Exact C1 result

All 224 streams passed.

- exact dataset fingerprints: 224/224;
- observed statistic within the frozen `1e-10` tolerance: 224/224;
- observed statistic exactly equal: 224/224;
- nonzero observed deltas: 0;
- maximum observed-statistic absolute delta: `0.0`;
- exact first-199 attempt-sequence SHA-256: 224/224;
- bootstrap refit failure free: 224/224;
- qualification failures: 0.

Therefore:

`C1 GATE = PASS`

This result is stronger than merely satisfying the historical observed-statistic tolerance: every observed statistic reproduced bit-for-bit at the Python float level reported by the retained result.

## Retained execution artifact

Combined Actions artifact:

- ID `10965746901`;
- name `f1b-r2-homogeneous-c1-combined`;
- ZIP SHA-256:
  `ea723fdc3051b185a8c4d3dba1754b1bbb5edd25d8a05bf82fc8411bb8bb1b02`;
- combined JSON SHA-256:
  `823d6fedf14d371d0d58822e3176ff8abe80b5d41575f4d11214d963a5df64c9`;
- combined JSON size: 361,598 bytes.

The retained machine-readable repository result is:

`model/results/f1b_r2_homogeneous_c1_exact_replay_2026-09-28.json`

It records each shard artifact ID, artifact ZIP digest, partition JSON digest, count and runtime core identity.

## Scientific boundary

C1 is a numerical reproducibility gate only.

It does not establish:

- validity of the model specification;
- validity of the parametric-bootstrap approximation;
- Type-I error control beyond the already defined controller;
- statistical power;
- an authoritative core grid;
- human sample size;
- participant recruitment readiness;
- runtime F1b activation.

No new bootstrap attempt was generated.

No draw index >=199 was generated.

## Consequence

The homogeneous numerical lineage is now reproducible through the retained first-199 bootstrap prefix for every H2 unresolved stream.

This result still does not authorize Stage C2 directly.

Before draw index 199 or higher is generated, a separate prospective C2 contract must freeze:

- this C1 result and artifact/hash;
- the H1 source;
- the H2 checkpoint provenance;
- the unchanged controller;
- the homogeneous Haswell execution lineage;
- continuation seed/draw identity;
- stopping and refit-failure semantics;
- the prospective maximum attempt cap.

Therefore:

`H1 HOMOGENEOUS SOURCE = QUALIFIED`

`H2 HOMOGENEOUS STAGE-B = PASS / RETAINED`

`C1 HOMOGENEOUS EXACT REPLAY = PASS 224/224 / RETAINED`

`NEW DRAW INDEX >=199 = NOT YET AUTHORIZED`

`SEPARATE PROSPECTIVE C2 CONTRACT = REQUIRED`

`STATISTICAL POWER = NOT VALIDATED`

`AUTHORITATIVE CORE GRID / HUMAN N = NOT FROZEN`

`PARTICIPANT RECRUITMENT = NOT AUTHORIZED`

`RUNTIME F1B = NOT AUTHORIZED`
