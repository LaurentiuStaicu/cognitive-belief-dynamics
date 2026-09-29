# F1b R2 S4 broad execution topology result — 2026-09-29

Issue: #259

Status: **TOPOLOGY COMPLETE / 1,000 DETERMINISTIC SHARDS / BROAD NUMERICAL EXECUTION NOT YET RUN**

The topology gate was merged in PR #284 and executed in temporary PR #285, which was closed unmerged.

Execution evidence:
- workflow run: `36528991962`;
- artifact ID: `11016235168`;
- artifact ZIP SHA-256: `d6bdb313545ca33ca09e48379b1bb7d4f7c8d7fc790f86f15cd83c9b1f2d5a6b`;
- topology JSON SHA-256: `31121be6270423489828d4544bece75f9264aff2c7bfcd8e703e6a10d4f7fa69`;
- topology JSON size: 255,623 bytes.

## Frozen topology

The complete broad design remains:
- 15,000 scientific runs;
- 60,000 method/run identities;
- 3,360 retained M2 method rows imported;
- 56,640 new method executions.

Execution is partitioned into:
- 4 replicate waves;
- 250 deterministic scientific-run shards per wave;
- 1,000 shards total.

Wave ranges:
- W0: replicates 0..24;
- W1: 25..49;
- W2: 50..74;
- W3: 75..99.

Canonical complete assignment SHA-256:

`7d37f2384c1003490a4b6e7a091f8648ed61e72241f964d3ce0336229f63dbce`

## Per-wave plan

W0:
- 3,750 scientific runs;
- 840 imported;
- 2,910 new;
- 3,360 imported method rows;
- 11,640 new method executions;
- shard size range: 5..29 scientific runs.

W1:
- 3,750 new scientific runs;
- 15,000 new method executions;
- shard size range: 5..27.

W2:
- 3,750 new scientific runs;
- 15,000 new method executions;
- shard size range: 6..27.

W3:
- 3,750 new scientific runs;
- 15,000 new method executions;
- shard size range: 4..27.

All 1,000 shards are non-empty.

## Operational cost check

Observed M2 shard timing was used only to check operational feasibility.

M2 observed:
- median ≈102 seconds/scientific run;
- p95 ≈218 seconds/run;
- slowest observed ≈252 seconds/run.

For the largest 29-run S4 shard:
- p95 extrapolation ≈105 minutes;
- slowest-observed-rate extrapolation ≈122 minutes.

This remains below the GitHub-hosted default 360-minute job timeout.

No scientific criterion depends on runtime.

## Next gate

Before W0 may begin, the new S4 executor must pass an exact equivalence gate against retained M2.

The gate uses 12 rows:
- 4 methods;
- 3 terminal status classes per method:
  - resolved at prefix;
  - resolved after continuation;
  - unresolved at cap.

For each method/status pair the lexicographically smallest retained M2 scientific-run ID is selected.

The new executor must reproduce retained M2 numerical evidence exactly under the same Haswell lineage.

## Version boundary

The planned next release remains v0.2.0 under Issue #277.

The topology does not close that release blocker.

The release remains blocked until broad S4 is executed, retained and scientifically interpreted.

## Boundary

`TOPOLOGY = COMPLETE / RETAINED`

`WAVES = 4`

`SHARDS = 1,000`

`NEW METHOD EXECUTIONS = 56,640`

`BROAD NUMERICAL EXECUTION = NOT STARTED`

`POWER = NOT VALIDATED`

`v0.2.0 BLOCKER = OPEN`
