# F1b R2 S4 W1 shard-11 preflight result — 2026-09-29

Issue: #259

Status: **W1 SHARD-11 PREFLIGHT COMPLETE / STRUCTURAL PASS / FULL W1 AUTHORIZED AFTER RETENTION**

The deterministic W1 shard-11 integration preflight ran in temporary PR #308 after the all-new-wave execution layer was retained through PR #307. The temporary PR was closed unmerged after evidence capture.

## Execution evidence

- temporary execution PR: `#308` (closed unmerged);
- workflow run: `36592144220`;
- run attempt: `1`;
- execution branch head: `7ecd804994f584c85363b6dc3121aa9e57d29a33`;
- pull-request merge ref: `d7f175317f4868f6d5c8e8e4bc22cfd0a72297c8`;
- qualified main baseline: `65b59e6dbfbe74d3841b19639f944ebe023053b8`;
- preflight job: success;
- artifact ID: `11045603524`;
- artifact name: `f1b-r2-s4-w1-shard11-preflight`;
- artifact ZIP SHA-256: `bc1393d3e8fdc57aa6ee4c9f39879673ef8b3052b08e03219001f9af0562499f`;
- W1 plan JSON SHA-256: `a80193e8cbdb151efd4c07b4c8a1e71b8c7749adc54016267297ba4d28e0d169`;
- shard-result JSON SHA-256: `4a7e12f690f26c2d678573b5b1cd84b689cbc9184e27f7761d77d2ce1b2f70ef`;
- evidence JSON SHA-256: `ddc17fa82f0570bb93f9a8c7e4c6065b927c71e94d04e1ce2ecab11b4303cac1`;
- OpenBLAS reported cores: `Haswell, Haswell`.

## Exact W1 plan identity

The preflight rebuilt and validated the complete frozen W1 plan before executing the selected shard:

- evaluation replicates: 25..49;
- 3,750 scientific runs;
- 15,000 method rows;
- zero imported scientific runs or method rows;
- 250 deterministic shards;
- scientific-run-ID SHA-256:
  `42a1803705c0c4f7efbfae0983a7c57f20036c76cd933c99af3fcd4e3cd9087c`;
- method-row-ID SHA-256:
  `2191e0aceb072c20bca90dab1b6db3ed8bffef997bf2ead8ec2ace2ac4a81957`;
- shard-plan SHA-256:
  `36d294a165ec1e8a8baffac70516ce7fceab149998079b534998503f3f578175`.

## Preflight identity and result

The prospectively selected shard 11 matched exactly:

- 15 scientific runs;
- 60 method rows;
- 0 imported rows;
- 60 `S4_NEW_EXECUTION` rows;
- scientific-run-ID SHA-256:
  `da11844e3c88b0f2dd95c039efb1f7f0ba398d3d48518d4c136a039c084e25a2`;
- method-row-ID SHA-256:
  `a6917767655c652a0977e8455f069db50e95fa6f91d9a7fd9de7d48bdb6f99da`.

Terminal accounting was retained exhaustively:
- resolved at the 199-draw prefix: 44;
- resolved after sequential continuation: 13;
- unresolved at the n=10,000 cap: 3;
- refit failures: 0;
- prefix-execution failures: 0;
- reject decisions: 29;
- not-reject decisions: 28.

These observed outcome counts were not acceptance criteria and do not rank or select an inference method.

## Provenance gate

The workflow verified exact Git blob identities for:
- the retained W1 execution contract;
- the retained W0 predecessor result;
- the all-new-wave planning/shard layer;
- the unchanged shared broad executor `run_new_stream()`;
- the W1 plan builder and shard runner.

The retained H1 and S4 raw-source SHA-256 values also matched before execution.

## Consequence

The shard-11 integration preflight passed its structural/provenance gate under the required Haswell lineage.

Once this retention PR is merged, full W1 becomes operationally authorized under the already frozen contract:
- exactly 3,750 W1 scientific runs;
- exactly 15,000 new method executions;
- exactly 250 deterministic shards;
- no imported evidence;
- unchanged scientific executor, RNG namespaces, sequential controller and cap;
- no wave-level scientific interpretation.

W2 remains blocked until the full W1 exact combine is separately retained on `main`.

## Scientific boundary

This preflight does not validate power and does not authorize interpretation of its reject/not-reject/unresolved distribution. It does not select a method or hierarchical scale.

Human N is not frozen. Participant recruitment and runtime F1b activation remain unauthorized.

## Release boundary

The planned next release remains v0.2.0 under Issue #277.

The release blocker remains open until W0-W3 are executed, retained, final-combined and scientifically interpreted under the predeclared S4 criteria.

## Boundary

`W1 SHARD-11 PREFLIGHT = COMPLETE / STRUCTURAL PASS / RETAINED AFTER MERGE`

`FULL W1 = AUTHORIZED ONLY AFTER THIS RETENTION MERGES`

`W2 / W3 = BLOCKED BY SEQUENTIAL WAVE RETENTION`

`SCIENTIFIC INTERPRETATION = NOT AUTHORIZED`

`METHOD / SCALE SELECTED = NO`

`POWER = NOT VALIDATED`

`HUMAN N = NOT FROZEN`

`RUNTIME F1B = NOT AUTHORIZED`

`v0.2.0 BLOCKER = OPEN`
