# F1b R2 homogeneous paired-source H1 result — 2026-09-28

Issue: #234

Status: **H1 PASS / NEW HOMOGENEOUS PAIRED SOURCE QUALIFIED / H2 REQUIRED / STAGE C2 BLOCKED**

## Purpose

H1 regenerated the complete F1b R2 paired-bootstrap source under one prospectively homogeneous numerical execution lineage.

Candidate lineage:

`OPENBLAS_CORETYPE=Haswell`

This is a new numerical provenance line. It does not rewrite the retained heterogeneous historical source and it does not claim that Haswell was the historical runtime for every old shard.

OpenBLAS documents `OPENBLAS_CORETYPE` as the runtime target override for DYNAMIC_ARCH builds. The H0/H1 gate also requires runtime confirmation of the selected target rather than trusting the environment variable alone.

## Execution

Temporary execution:
- PR #236 — execution only, closed unmerged;
- workflow run `36401867007`, run number 2;
- PR head `101b9e6258cff944db9f4ae9f6112afa75ca6d39`;
- workflow checkout merge commit recorded by the H1 wrapper: `76f8ef85c99bbc24418e849133b2bbcb336ced33`;
- qualified main baseline: `066a738f353fd2ab37428103e9b4786b96a6cc94`;
- retained scientific-source identity: `6ad6be092fd3e6b9ec17c3935e19711710690beb`.

The temporary PR changed only the execution workflow. The H0 verifier protected the scientific and paired execution files before generation.

## H1 generation

The unchanged paired-characterization runner was executed in five computational shards:

| Shard | Replicates | Restriction runs | Fit failures | Runtime OpenBLAS |
| --- | --- | ---: | ---: | --- |
| R00_01 | 0–1 | 150 | 0 | Haswell / Haswell |
| R02_03 | 2–3 | 150 | 0 | Haswell / Haswell |
| R04_05 | 4–5 | 150 | 0 | Haswell / Haswell |
| R06_07 | 6–7 | 150 | 0 | Haswell / Haswell |
| R08_09 | 8–9 | 150 | 0 | Haswell / Haswell |

Combined source:
- evaluation replicates: 0..9;
- unique datasets: 390;
- restriction runs: 750;
- snapshots: 2,250;
- paired comparisons: 2,250;
- fit failures: 0;
- maximum bootstrap draw index: 198;
- no draw index >=199 generated.

New homogeneous combined JSON:
- SHA-256: `618b52162e98d25d41ac9cc7a6411ccfbf3c95775412a46b759e1514e90ed37e`;
- size: 9,013,549 bytes;
- Actions artifact ID: `10961527329`;
- artifact ZIP SHA-256: `f3a622ae3607c2308879a7d12629119cc5f100f9d4df4327ec1c8627d299eb27`.

The retained heterogeneous source was not overwritten.

## Independent H1 replay qualification

Generation success was not sufficient for acceptance.

A separate runner replayed a deterministic 16-stream subset spanning:
- evaluation replicates 0, 7, 8 and 9;
- NULL and DEPARTURE identities;
- ADD and CBD-complement restrictions.

Result:

`16 / 16 exact`

For every selected stream:
- dataset fingerprint matched exactly;
- observed statistic matched exactly;
- complete first-199 attempt-sequence SHA-256 matched exactly.

The replay process itself reported only:

`Haswell, Haswell`

Replay artifact:
- ID `10962056060`;
- ZIP SHA-256 `c5c0692a96f7cfa2ab71c0952a9650f5e52a9914869f09b3f3bef3f69260c7b6`;
- replay result JSON SHA-256 `30bd20f7d12a76b7183ba56d28a344b7b3e3b215ef53cf68b926e0f88df3bda4`.

Therefore the prospectively homogeneous H1 source passes its predeclared cross-runner reproducibility gate.

## Historical-source comparison

Comparison with the retained heterogeneous source was diagnostic only and was not used to tune or accept H1.

Across all 750 restriction runs:
- dataset fingerprints exact: 750/750;
- observed statistics exact: 601/750;
- first-199 attempt sequences exact: 600/750;
- maximum observed-statistic absolute delta: `3.6021344840264646e-07`.

The boundary is exact by evaluation replicate.

Replicates 0–7:
- 600/600 dataset fingerprints exact;
- 600/600 observed statistics exact;
- 600/600 first-199 attempt sequences exact.

Replicate 8:
- 75/75 dataset fingerprints exact;
- 0/75 observed statistics exact;
- 0/75 attempt sequences exact.

Replicate 9:
- 75/75 dataset fingerprints exact;
- 1/75 observed statistics exact;
- 0/75 attempt sequences exact.

This is consistent with the already retained source-lineage diagnosis: the old combined source contains multiple numerical trajectories, while the H1 source uses one runtime-verified Haswell trajectory for all replicates.

Historical-comparison artifact:
- ID `10961641260`;
- ZIP SHA-256 `1c2bbdd357824183dd52844af0915fb53998d537cd1cb1e52309703de3a436ef`;
- comparison JSON SHA-256 `cf3d00f6b3556f9eef281fbba72ce8deae80e436e0cb246642852e1bc1c02755`.

## Decision

H1 passes.

The new combined source is accepted as the input for H2 provenance rebuilding.

This does **not** permit inheritance of the historical Stage-B terminal/unresolved decisions. H2 must rerun the unchanged resampling-risk controller from the new homogeneous source through the retained 199-attempt prefix and create new checkpoints and aggregate outcomes.

The historical source and all historical Stage-B/C1 results remain retained evidence.

## Boundary

`HISTORICAL PAIRED SOURCE = RETAINED / NUMERICALLY HETEROGENEOUS`

`H1 HOMOGENEOUS HASWELL SOURCE = PASS / QUALIFIED`

`H1 INDEPENDENT REPLAY = PASS 16/16`

`H2 STAGE-B REBUILD = REQUIRED`

`HISTORICAL STAGE-B CHECKPOINTS = NOT INHERITED`

`NEW DRAW INDEX >=199 = NOT AUTHORIZED`

`STAGE C2 = BLOCKED`

`STATISTICAL POWER = NOT VALIDATED`

`AUTHORITATIVE CORE GRID / HUMAN N = NOT FROZEN`

`PARTICIPANT RECRUITMENT = NOT AUTHORIZED`

`RUNTIME F1B = NOT AUTHORIZED`
