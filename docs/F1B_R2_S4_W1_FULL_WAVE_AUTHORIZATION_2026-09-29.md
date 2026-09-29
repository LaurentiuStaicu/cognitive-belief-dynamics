# F1b R2 S4 W1 full-wave authorization — 2026-09-29

Issue: #259

Status: **W1 PREFLIGHT RETAINED / FULL W1 OPERATIONALLY AUTHORIZED / EXECUTION NEXT**

W1 shard-11 integration evidence was retained on `main` through PR #309. This gate performs only the explicit authorization transition required by the frozen W1 contract.

## Retained predecessor

- W1 shard-11 retention PR: `#309`;
- retention merge: `482e38e86c996fae9c56ba4a8af2584c88db5547`;
- retained result blob: `4dc28d64ef81c2070467dc197064e9b4f37173e7`;
- retained status: `NON_AUTHORITATIVE_S4_W1_SHARD11_PREFLIGHT_COMPLETE_RETAINED`;
- structural/provenance preflight: PASS;
- Haswell lineage: confirmed.

## Authorization transition

The W1 execution config is changed only in authorization/provenance metadata:

- retained preflight result is bound explicitly;
- `preflight_retained = true`;
- `full_wave_execution_authorized = true`.

The config blob changes from:
`d3aa34e2e92eb88056b0cc7cfdb0510ee2270073`

to:
`47e025f001bd5d28094eef7fd9ba36adff72ee93`.

The fail-closed test is updated so any mismatch between the two authorization flags remains invalid.

No executor, fitter, bootstrap logic, dataset generator, RNG namespace, sequential controller, scientific matrix, topology or W0 evidence module is changed.

## Frozen full-W1 contract

Full W1 remains exactly:

- evaluation replicates: 25..49;
- 3,750 scientific runs;
- 15,000 method rows;
- zero imported evidence;
- 250 deterministic shards;
- scientific-run-ID SHA-256:
  `42a1803705c0c4f7efbfae0983a7c57f20036c76cd933c99af3fcd4e3cd9087c`;
- method-row-ID SHA-256:
  `2191e0aceb072c20bca90dab1b6db3ed8bffef997bf2ead8ec2ace2ac4a81957`;
- shard-plan SHA-256:
  `36d294a165ec1e8a8baffac70516ce7fceab149998079b534998503f3f578175`;
- four frozen methods;
- Haswell numerical lineage;
- 199-draw prefix;
- sequential cap n=10,000.

## Consequence

After this authorization PR passes CBD validation and merges, the next action is the exact full-W1 temporary execution workflow.

That workflow must:
- verify this authorization record and all protected blobs;
- rebuild the exact W1 plan;
- execute exactly shards 0..249 with `fail-fast=false` and `max-parallel=20`;
- keep all four methods for one scientific run in the same shard;
- combine only after all 250 shards succeed;
- require exact 3,750 / 15,000 coverage and frozen digests;
- retain unresolved/failure rows in denominators;
- upload a non-authoritative combined W1 candidate for separate retention.

W1 wave-level scientific interpretation remains forbidden.

W2 remains blocked until the exact W1 combined result is separately retained on `main`.

## Boundary

`W1 PREFLIGHT = RETAINED`

`FULL W1 AUTHORIZATION = YES AFTER THIS GATE MERGES`

`FULL W1 EXECUTION = NEXT`

`W2 / W3 = BLOCKED`

`SCIENTIFIC INTERPRETATION = NOT AUTHORIZED`

`METHOD / SCALE SELECTED = NO`

`POWER = NOT VALIDATED`

`HUMAN N = NOT FROZEN`

`RUNTIME F1B = NOT AUTHORIZED`

`v0.2.0 BLOCKER = OPEN`
