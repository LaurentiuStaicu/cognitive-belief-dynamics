# F1b R2 S4 W1 all-new-wave execution gate

Issue: #259

Status: **W1 IMPLEMENTATION GATE / PREFLIGHT REQUIRED / FULL W1 NOT YET STARTED**

W0 is retained on `main` through PR #306. This authorizes implementation and qualification of W1, but not immediate full-wave execution.

## Purpose

W1 is the first S4 wave with no retained M2 imports. Its execution layer must therefore be a thin all-new wrapper around the already qualified shared scientific executor.

The retained W0 modules are evidence-bearing and must not be refactored merely to create reuse.

## Frozen W1 identity

- evaluation replicates: 25..49;
- scientific runs: 3,750;
- method rows: 15,000;
- imported scientific runs: 0;
- imported method rows: 0;
- new scientific runs: 3,750;
- new method executions: 15,000;
- deterministic shards: 250;
- scientific-run-ID SHA-256:
  `42a1803705c0c4f7efbfae0983a7c57f20036c76cd933c99af3fcd4e3cd9087c`;
- method-row-ID SHA-256:
  `2191e0aceb072c20bca90dab1b6db3ed8bffef997bf2ead8ec2ace2ac4a81957`;
- shard-plan SHA-256:
  `36d294a165ec1e8a8baffac70516ce7fceab149998079b534998503f3f578175`;
- shard size range: 5..27 scientific runs.

## Implementation boundary

The all-new-wave layer may:
- select exact wave membership;
- build and validate deterministic shard plans;
- validate all-new shard evidence;
- combine an exact 250-shard wave.

It must reuse unchanged:
- `f1b_r2_s4_broad_executor.run_new_stream()`;
- the H1/S4 scientific sources;
- the dataset generator;
- the four-method order;
- RNG namespaces;
- the 199-draw prefix;
- sequential controller;
- n=10,000 cap;
- Haswell numerical lineage.

No retained/imported evidence is permitted in W1-W3.

## Deterministic preflight

Before full W1 execution, run exactly W1 shard 11.

Frozen preflight identity:
- scientific runs: 15;
- method rows: 60;
- scientific-run-ID SHA-256:
  `da11844e3c88b0f2dd95c039efb1f7f0ba398d3d48518d4c136a039c084e25a2`;
- method-row-ID SHA-256:
  `a6917767655c652a0977e8455f069db50e95fa6f91d9a7fd9de7d48bdb6f99da`.

Acceptance is structural/provenance only. Scientific outcomes are not acceptance criteria.

Full W1 remains blocked until this preflight passes under Haswell and its result is separately retained on `main`.

## Boundary

`W0 = RETAINED`

`W1 IMPLEMENTATION = AUTHORIZED`

`W1 PREFLIGHT = REQUIRED BEFORE FULL W1`

`FULL W1 EXECUTION = NOT YET AUTHORIZED`

`W2 / W3 = BLOCKED`

`SCIENTIFIC INTERPRETATION = NOT AUTHORIZED`

`METHOD / SCALE SELECTED = NO`

`POWER = NOT VALIDATED`

`v0.2.0 BLOCKER = OPEN`
