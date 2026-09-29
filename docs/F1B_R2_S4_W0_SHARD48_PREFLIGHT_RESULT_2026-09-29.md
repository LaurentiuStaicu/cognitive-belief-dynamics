# F1b R2 S4 W0 shard-48 production-runner preflight result — 2026-09-29

Issue: #259

Status: **PRODUCTION-RUNNER PREFLIGHT PASS / FULL W0 AUTHORIZED AFTER RETENTION**

The prospectively frozen shard-48 integration preflight was executed in temporary PR #303 and closed unmerged after evidence capture.

Execution evidence:
- workflow run: `36546677350`;
- execution head: `0b91b8106b598abf5e8266285bc9cf42eaad1fff`;
- qualified main baseline: `5a02b796157d99636d5a3c2a3dd4c2aa6f732d43`;
- artifact ID: `11023527802`;
- artifact name: `f1b-r2-s4-w0-shard-48-preflight`;
- artifact ZIP SHA-256:
  `a10f19ed8ce48a5955d7630d1f802c640c8768cb09d6b3d0bd74054c1519bf92`.

Frozen outcome-independent selection:
- selection rule: smallest W0 shard index with exactly 15 scientific runs, 5 imported scientific runs and 10 new scientific runs;
- selected shard: 48;
- scientific runs: 15;
- imported scientific runs: 5;
- new scientific runs: 10;
- method rows: 60;
- retained M2 imports: 20;
- new method executions: 40.

Evidence hashes:
- selection JSON SHA-256:
  `a562e140462704f9340dea876ab56f1c34a493a60b3c7f71f856b2fb8808ef5b`;
- shard result JSON SHA-256:
  `c1616a0587950d9d0f4c7c7e74f328a6f6dd18d38e02db3a3574155c37b967ef`;
- core JSON SHA-256:
  `a79fd356c00dc9ad04eb27a7ded4d939ce0f80accbcf2285fab0992ff9419b8b`;
- core log SHA-256:
  `18dd8de98d3cc40e16f905c7087571de7803bbdadc0b4b3b8fcae064fc4be53c`;
- scientific-run IDs SHA-256:
  `bbdc9422c791bad7736dc2d617e7e6e921b2afe9797caff95b4aa2055ba2a99e`;
- method-row IDs SHA-256:
  `20183113e595791603b0b2bbecd741230826085d732a4560d5fb1df98c1a9a4e`.

The production path passed:
- exact retained W0 plan binding;
- exact shard-48 selection;
- exact imported/new workload counts;
- four-method coverage per scientific run;
- paired dataset SHA across methods;
- retained M2 evidence origin for imported rows;
- S4 new-execution origin for new rows;
- retained H1/S4/M2/W0-plan provenance hashes;
- Haswell numerical lineage;
- production shard-result schema.

Observed terminal states:
- 52 resolved at prefix;
- 7 resolved after continuation;
- 1 unresolved at the n=10,000 cap;
- 0 refit failures;
- 0 prefix execution failures.

Observed decisions:
- 46 not-reject;
- 13 reject;
- the unresolved-at-cap row has no decision and remains in the denominator.

These scientific outcomes were not acceptance criteria and are not a performance estimate.

## Consequence

After this result is retained on main, the unchanged 250-shard W0 matrix is operationally authorized.

W0 remains:
- 3,750 scientific runs;
- 15,000 method rows;
- 3,360 retained M2 imported rows;
- 11,640 new method executions;
- 250 deterministic shards;
- fail-fast=false;
- max-parallel=20.

W1 remains blocked until W0 is fully executed, all 250 shards are combined, the combined result is retained, and the frozen W0 contract passes.

No scientific interpretation, method/scale selection, power validation, human-N freeze, participant recruitment, runtime F1b activation or version bump is authorized by this preflight.

## Boundary

`SHARD-48 PRODUCTION PREFLIGHT = PASS`

`FULL W0 = AUTHORIZED AFTER RETENTION`

`W1 = BLOCKED`

`SCIENTIFIC INTERPRETATION = NOT AUTHORIZED`

`METHOD SELECTED = NO`

`POWER = NOT VALIDATED`

`v0.2.0 BLOCKER = OPEN`
