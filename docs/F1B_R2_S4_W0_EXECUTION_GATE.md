# F1b R2 S4 W0 execution gate

Issue: #259

Status: **W0 EXECUTION PLAN FROZEN / W0 NUMERICAL EXECUTION NOT YET RUN**

## Purpose

This gate authorizes only the first broad S4 wave after:
- retained M2 eligibility;
- retained S4 matrix;
- retained method binding;
- retained M2→S4 prefix bridge;
- retained execution topology;
- retained new-executor equivalence;
- retained fresh-replicate preflight.

It does not authorize W1-W3 or scientific interpretation.

## W0 identity

Replicate range:

`0..24`

Exact W0 scientific matrix:
- 3,750 scientific runs;
- 15,000 method/run identities;
- all four frozen methods.

Imported retained M2 evidence:
- 840 scientific runs;
- 3,360 method rows.

New W0 execution:
- 2,910 scientific runs;
- 11,640 method executions.

Canonical W0 digests:
- scientific-run IDs:
  `7f49bc6a67508566d2143d699af8d10d1721f571c1981035cdf1aef39dad8419`;
- all method-row IDs:
  `7a936f191cdcd58e3988db43b43dbb166a2ca18033a8c5a9913f4efee2ef8b6c`;
- imported method-row IDs:
  `d9d42ed4437199375c593110f555502d26a6660e81e045b9e1b105e8a1434537`;
- new method-row IDs:
  `dad1b46e6028a4f0a415e8c65b5442aab44eb867e446c1ecb80ab637ee033fd5`.

## Sharding

W0 uses exactly 250 deterministic shards.

Assignment reuses the qualified topology hash:

`stable_shard(scientific_run_id, 250)`

which corresponds to SHA-256 first-eight-byte big-endian modulo 250.

All four methods for one scientific run remain in the same shard.

Observed deterministic W0 shard load:
- minimum: 5 scientific runs;
- maximum: 29 scientific runs;
- empty shards: 0.

Canonical shard-plan SHA-256:

`1e248f24362eb9cdf1a9a81d7088120ed64e4333cfc711e2848d6e3e6c531f45`.

## Runner policy

The eventual W0 matrix must use:
- shard indices exactly 0..249;
- `fail-fast: false`;
- `max-parallel: 20`;
- Haswell numerical lineage;
- exact broad executor;
- 199-draw prefix;
- unchanged sequential controller and n=10,000 cap;
- stop on first refit failure.

Imported M2 rows are not recomputed.

New W0 rows are executed with the qualified S4 broad executor.

A failed shard may only be rerun for the same shard identity.

## Wave combine

W0 is complete only when all 250 shard artifacts are present.

The combine must require:
- exactly 3,750 scientific runs;
- exactly 15,000 method rows;
- exactly 3,360 imported rows;
- exactly 11,640 new rows;
- no duplicate or missing identities;
- unresolved and refit-failure outcomes retained in denominators.

The W0 combine may retain descriptive summaries but must not perform final S4 scientific interpretation or method selection.

After the W0 result is retained, W1 may be authorized under a separately retained execution result path.

## Version boundary

The target next release remains v0.2.0 under Issue #277.

W0 alone does not close the release blocker.

v0.2.0 remains blocked until W0-W3 are complete, final-combined, retained and scientifically interpreted.

## Boundary

`W0 PLAN = FROZEN`

`W0 SCIENTIFIC RUNS = 3,750`

`W0 METHOD ROWS = 15,000`

`W0 IMPORTED ROWS = 3,360`

`W0 NEW EXECUTIONS = 11,640`

`W0 NUMERICAL EXECUTION = NOT YET RUN`

`W1-W3 = NOT YET AUTHORIZED`

`POWER = NOT VALIDATED`

`v0.2.0 BLOCKER = OPEN`
