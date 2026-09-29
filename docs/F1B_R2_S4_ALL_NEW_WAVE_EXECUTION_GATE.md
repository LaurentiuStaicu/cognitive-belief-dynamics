# F1b R2 S4 all-new-wave execution gate

Issue: #259

Status: **W1 WRAPPER IMPLEMENTATION GATE / W1 AUTHORIZED / W2-W3 BLOCKED**

W0 is retained on `main` after exact 250-shard execution and combine. The next operational step is W1, covering evaluation replicates 25..49.

W1 differs from W0 only in evidence provenance: every W1 scientific run is new. No retained M2 row may enter W1.

## Architecture

The scientific execution path remains the already qualified shared `run_new_stream()` implementation.

This gate adds only an all-new-wave layer for:
- wave membership;
- deterministic shard planning;
- no-import enforcement;
- shard result validation;
- exact wave combine validation.

The retained W0 execution, shard and combine modules are not refactored or rewritten.

## Frozen wave identities

W1:
- evaluation replicates 25..49;
- 3,750 scientific runs;
- 15,000 method rows;
- 250 deterministic shards;
- scientific-run digest `42a1803705c0c4f7efbfae0983a7c57f20036c76cd933c99af3fcd4e3cd9087c`;
- method-row digest `2191e0aceb072c20bca90dab1b6db3ed8bffef997bf2ead8ec2ace2ac4a81957`;
- shard-plan digest `36d294a165ec1e8a8baffac70516ce7fceab149998079b534998503f3f578175`;
- shard size range 5..27.

W2 and W3 identities are retained in the same configuration so later waves can reuse the wrapper without changing scientific fitting/bootstrap logic, but current authorization is W1 only.

## W1 implementation preflight

The preflight is selected before implementation by the outcome-independent rule:

> smallest W1 shard index with exactly 15 scientific runs.

This is shard 11:
- 15 scientific runs;
- 60 method rows;
- zero imports;
- scientific-run digest `da11844e3c88b0f2dd95c039efb1f7f0ba398d3d48518d4c136a039c084e25a2`;
- method-row digest `a6917767655c652a0977e8455f069db50e95fa6f91d9a7fd9de7d48bdb6f99da`.

The full W1 wave remains blocked until this wrapper preflight passes under Haswell lineage and is separately retained on `main`.

## Fail-closed requirements

The all-new layer rejects:
- W2/W3 execution before authorization;
- a replicate outside the requested wave;
- any imported evidence origin;
- missing/duplicate method rows;
- method-set changes;
- dataset-pairing changes;
- stable-shard assignment changes;
- wrong run/method/shard-plan digests;
- missing/duplicate shards at combine;
- wave-level scientific interpretation;
- method/scale selection;
- release-blocker shortcuts.

## Boundary

`W0 = RETAINED`

`W1 = AUTHORIZED FOR WRAPPER QUALIFICATION`

`FULL W1 = BLOCKED UNTIL PREFLIGHT RETENTION`

`W2 / W3 = NOT AUTHORIZED`

`SCIENTIFIC INTERPRETATION = NOT AUTHORIZED`

`METHOD / SCALE SELECTED = NO`

`POWER = NOT VALIDATED`

`HUMAN N = NOT FROZEN`

`RUNTIME F1B = NOT AUTHORIZED`

`v0.2.0 BLOCKER = OPEN`
