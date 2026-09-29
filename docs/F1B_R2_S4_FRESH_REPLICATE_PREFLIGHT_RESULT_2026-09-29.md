# F1b R2 S4 fresh-replicate preflight result — 2026-09-29

Issue: #259

Status: **FRESH PREFLIGHT COMPLETE / STRUCTURAL PASS / W0 AUTHORIZED AFTER RETENTION**

The retained-bound fresh-replicate preflight gate was merged in PR #293 and executed in temporary PR #294, which was closed unmerged.

Execution evidence:
- workflow run: `36538099199`;
- artifact ID: `11019688175`;
- artifact ZIP SHA-256: `69d405dd5fcc34cdbf8d38d7e8a2ec870eae531342a0b104527558d774b4f13a`;
- selection JSON SHA-256: `c602f7582238c34691cbae8bd2019c5f6d5ca606439779600a43ac552c1459e9`;
- result JSON SHA-256: `288f0be87a9ba43fd18234d2832535215cbecfbf87c9de7c66f0bae42045cf3b`;
- OpenBLAS lineage: Haswell.

The preflight executed:
- 18 genuinely fresh S4 scientific runs;
- 72 method rows;
- departure replicate 5;
- null replicate 20;
- missingness 0.00 / 0.15;
- all five scientific roles;
- all three null identities;
- both departure signs;
- all four M2-eligible methods.

Identity digests:
- scientific-run IDs SHA-256:
  `d55ce620877a7b64a8ce37312025756482ff287456b62811f6a5b8249197666e`;
- method-row IDs SHA-256:
  `be00d6689e29d5af959baa747a72254f449ec4d4dd20cd070460dac71f7a0a21`.

Observed terminal-state summary:
- 67 resolved at the n=199 prefix;
- 5 resolved after continuation;
- zero unresolved-at-cap;
- zero refit/prefix execution failures;
- terminal n: min 199, median 199, max 3359.

Observed decisions were:
- 61 not-reject;
- 11 reject.

Those decisions are not acceptance criteria and are not a performance sample.

The gate passed because executor/provenance/pairing/lineage invariants passed on fresh scientific identities.

## Consequence

After this result is retained on main, W0 may be executed under the frozen S4 topology.

W0 contains:
- 3,750 scientific runs;
- 3,360 imported M2 method rows;
- 11,640 new method executions.

W1-W3 remain blocked until the W0 execution/result path is defined and retained according to the frozen broad topology.

## Version boundary

The next target release remains v0.2.0 under Issue #277.

This preflight does not close the release blocker.

The release remains blocked until all four broad S4 waves are complete, retained, combined and scientifically interpreted.

## Boundary

`FRESH EXECUTOR PREFLIGHT = PASS`

`W0 = AUTHORIZED AFTER RETENTION`

`BROAD SCIENTIFIC INTERPRETATION = NOT AUTHORIZED`

`METHOD SELECTED = NO`

`POWER = NOT VALIDATED`

`v0.2.0 BLOCKER = OPEN`
