# F1b R2 S4 W0 execution-plan result — 2026-09-29

Issue: #259

Status: **W0 PLAN COMPLETE / EXACT CONTRACT PASS / SHARD-48 PREFLIGHT NEXT**

The W0 plan gate was merged in PR #296, the W0 runner/combine harness was merged in PR #297, and the raw-M2 status binding was corrected in PR #300. The exact retained-bound plan was then rerun in temporary PR #301.

Execution evidence:
- temporary execution PR: `#301` (do not merge);
- workflow run: `36545789907`;
- workflow run number: `2`;
- execution head: `510ee77096463d495d8e1e2dfb011a5b98f35309`;
- qualified main baseline: `2b5c479810dfa3ab408f817226e8ce3aab94a1e0`;
- artifact ID: `11022700618`;
- artifact name: `f1b-r2-s4-w0-execution-plan`;
- artifact ZIP SHA-256: `42362b49bdc22e60b63cf00d2de35b9813544a7d5f6dd94a26b9468c69b469a8`.

The plan contract passed exactly:
- W0 scientific runs: 3,750;
- W0 method rows: 15,000;
- imported scientific runs: 840;
- imported M2 method rows: 3,360;
- new scientific runs: 2,910;
- new method executions: 11,640;
- deterministic shards: 250;
- shard size range: 5..29 scientific runs.

Frozen identity digests:
- scientific-run IDs SHA-256:
  `7f49bc6a67508566d2143d699af8d10d1721f571c1981035cdf1aef39dad8419`;
- method-row IDs SHA-256:
  `7a936f191cdcd58e3988db43b43dbb166a2ca18033a8c5a9913f4efee2ef8b6c`;
- imported method-row IDs SHA-256:
  `d9d42ed4437199375c593110f555502d26a6660e81e045b9e1b105e8a1434537`;
- new method-row IDs SHA-256:
  `dad1b46e6028a4f0a415e8c65b5442aab44eb867e446c1ecb80ab637ee033fd5`;
- shard-plan SHA-256:
  `1e248f24362eb9cdf1a9a81d7088120ed64e4333cfc711e2848d6e3e6c531f45`.

No numerical W0 science was executed by this plan run. No method/scale was selected, no scientific interpretation was authorized, power remains unvalidated, and v0.2.0 remains blocked.

## Next gate

The next step is the already prospectively frozen production-runner integration preflight on W0 shard 48.

Shard 48 is selected by the outcome-independent rule: the smallest shard index with exactly 15 scientific runs, 5 imported prefix runs and 10 new runs.

Required workload:
- 15 scientific runs;
- 5 imported scientific runs;
- 10 new scientific runs;
- 60 method rows;
- 20 retained M2 imports;
- 40 new method executions.

Acceptance remains structural/provenance only. Observed reject/not-reject/unresolved outcomes are not acceptance criteria.

Only after shard 48 passes and its result is retained may the full 250-shard W0 matrix launch unchanged.

## Boundary

`W0 PLAN = COMPLETE / RETAINED AFTER MERGE`

`W0 NUMERICAL EXECUTION = NOT STARTED`

`SHARD-48 INTEGRATION PREFLIGHT = NEXT`

`SCIENTIFIC INTERPRETATION = NOT AUTHORIZED`

`METHOD SELECTED = NO`

`POWER = NOT VALIDATED`

`v0.2.0 BLOCKER = OPEN`
