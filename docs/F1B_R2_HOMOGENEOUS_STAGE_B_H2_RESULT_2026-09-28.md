# F1b R2 homogeneous Stage-B H2 result — 2026-09-28

Issue: #234

Status: **H2 PASS / HOMOGENEOUS STAGE-B RETAINED / NEW C1 CONTRACT REQUIRED / STAGE C2 BLOCKED**

## Purpose

H2 rebuilt the Stage-B resampling-risk provenance from the qualified homogeneous H1 paired source.

It did not inherit historical Stage-B decisions or checkpoints.

Source:
- lineage `F1B.R2.HOMOGENEOUS_PAIRED_SOURCE.LINEAGE.V1`;
- Actions artifact ID `10961527329`;
- exact H1 combined JSON SHA-256 `618b52162e98d25d41ac9cc7a6411ccfbf3c95775412a46b759e1514e90ed37e`.

## Execution

Temporary execution:
- PR #239 — closed unmerged;
- workflow run `36406702153`;
- execution PR head `3cc463ce66d40f92770c60ab186da172e29f6d1c`;
- qualified main baseline `5566decc986c5d54f7155eb6a6827cf88261089b`.

H2 result artifact:
- ID `10962483226`;
- ZIP SHA-256 `ba02c513503623296879d16661da9575ee3c8fcdecb50464612157558e7571f7`;
- raw replay JSON SHA-256 `f0f32d92e46748148f020a4e0d47d2c63e27f6ab1aa36253346e15c4dfaf01e7`;
- raw replay size 1,804,832 bytes;
- comparison JSON SHA-256 `96abf4208108a224a51ac65e1f55f44b35432cf7637ee9607b1af8120d5c43cb`.

## Controller

The resampling-risk controller remained unchanged:
- alpha = 0.05;
- epsilon = 0.001;
- half-spend = 1000;
- replay horizon = 199;
- controller ID `F1B.R2.RESAMPLING_RISK_CONTROLLER.V1`.

H2 reused only the first-199 attempt sequences already present in the H1 source.

No new bootstrap attempt was generated.

## H2 result

Across 750 restriction streams:
- bootstrap refit failures: 0;
- resolved by 49: 326;
- resolved by 99: 372;
- resolved by 199: 526;
- unresolved at 199: 224;
- sequential reject: 119;
- sequential not-reject: 407;
- sequential/fixed-199 disagreement among resolved: 0.

Stopping distribution among the 526 resolved streams:
- minimum: 5;
- median: 22;
- maximum: 189.

New homogeneous Stage-B provenance:
- stream checkpoints: 750;
- checkpoint canonical SHA-256:
  `9f554b3a94464782194f0921dc13718fce995e58e2e15159cb2461b3fbb3ded2`;
- unresolved streams: 224;
- unresolved run-ID canonical SHA-256:
  `d2db2c97ad48544c082cdffd086c022a28c6d0c75690b36a0cd0b2b381c4ebac`.

## Historical comparison

The historical raw Stage-B replay used artifact ID `10938984164`.

Across the same 750 run IDs:
- dataset fingerprints exact: 750/750;
- observed statistics exact: 601/750;
- first-199 attempt hashes exact: 600/750;
- stopping points exact: 750/750;
- numerical streams differing: 150.

Decision-state transitions:
- 407 not-reject -> not-reject;
- 119 reject -> reject;
- 224 unresolved -> unresolved.

The unresolved set is identical as a set:
- historical: 224;
- homogeneous H2: 224;
- intersection: 224;
- historical-only: 0;
- homogeneous-only: 0.

The identical unresolved-set SHA-256 is:

`d2db2c97ad48544c082cdffd086c022a28c6d0c75690b36a0cd0b2b381c4ebac`

However, the checkpoint provenance is not identical:
- historical checkpoint SHA-256:
  `2bf8fad40c6bf233184ff3d738faf0c68194fcdc7b3ff9a18b518324df13daf3`;
- homogeneous H2 checkpoint SHA-256:
  `9f554b3a94464782194f0921dc13718fce995e58e2e15159cb2461b3fbb3ded2`.

Therefore the 224-stream identity is an independently reproduced outcome, not inherited historical provenance.

## Consequence

A successor continuation contract may target the newly reproduced 224 unresolved run IDs, but it must pin:
- the H1 homogeneous source;
- the H2 raw result artifact/hash;
- the H2 checkpoint digest;
- the H2 execution lineage.

It must not cite the historical Stage-B checkpoints as its source.

The next step is a new versioned homogeneous C1 exact-replay qualification gate. Only after that new C1 passes can any Stage-C2 extension be considered.

## Boundary

`H1 HOMOGENEOUS SOURCE = QUALIFIED`

`H2 HOMOGENEOUS STAGE-B = PASS / RETAINED`

`H2 UNRESOLVED SET = 224 / INDEPENDENTLY REPRODUCED`

`HISTORICAL STAGE-B CHECKPOINTS = NOT INHERITED`

`NEW HOMOGENEOUS C1 CONTRACT = REQUIRED`

`NEW BOOTSTRAP ATTEMPTS = NOT AUTHORIZED YET`

`NEW DRAW INDEX >=199 = NOT AUTHORIZED YET`

`STAGE C2 = BLOCKED`

`STATISTICAL POWER = NOT VALIDATED`

`AUTHORITATIVE CORE GRID / HUMAN N = NOT FROZEN`

`PARTICIPANT RECRUITMENT = NOT AUTHORIZED`

`RUNTIME F1B = NOT AUTHORIZED`
