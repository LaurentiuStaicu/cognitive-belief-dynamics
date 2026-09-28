# F1b R2 homogeneous Stage-C2 continuation result — 2026-09-28

Issue: #245

Status: **C2 COMPLETE / 201 NEWLY RESOLVED / 23 UNRESOLVED AT CAP / SCIENTIFIC INTERPRETATION GATE REQUIRED**

## Purpose

This result retains the first prospective Stage-C2 continuation executed on the qualified homogeneous numerical lineage.

It is downstream of:
- H1 homogeneous paired source qualification;
- H2 independent Stage-B rebuild;
- homogeneous C1 exact replay PASS 224/224;
- merged C2 implementation gate PR #246.

The temporary execution PR #247 was closed unmerged after evidence capture.

## Frozen lineage

C2 used only the qualified homogeneous lineage:
- H1 source artifact ID: `10961527329`;
- H1 source JSON SHA-256:
  `618b52162e98d25d41ac9cc7a6411ccfbf3c95775412a46b759e1514e90ed37e`;
- H2 raw replay artifact ID: `10962483226`;
- H2 raw replay JSON SHA-256:
  `f0f32d92e46748148f020a4e0d47d2c63e27f6ab1aa36253346e15c4dfaf01e7`;
- H2 target-set SHA-256:
  `d2db2c97ad48544c082cdffd086c022a28c6d0c75690b36a0cd0b2b381c4ebac`;
- homogeneous C1 combined artifact ID: `10965746901`;
- homogeneous C1 combined JSON SHA-256:
  `823d6fedf14d371d0d58822e3176ff8abe80b5d41575f4d11214d963a5df64c9`.

Historical C2 provenance was not used.

## Execution

Temporary execution:
- PR #247 — closed unmerged;
- workflow run `36416797671`;
- execution head `b42344485b75f73afb5d21d18f3fcf2510de5dd7`;
- qualified main baseline `ea1a1a34f39c0aae7c6afe70b00683c9aa0e42ad`.

Combined result artifact:
- artifact ID `10968522362`;
- artifact ZIP SHA-256:
  `6862d7270b580f9428e8465447df33034ddd2a764075db62daed5f85579dfaa3`;
- combined JSON SHA-256:
  `03009d7b586502f500062d67792f048e768fe737670823b2e033cb82c59a867a`;
- combined JSON size: 644,933 bytes.

All 16 scientific shards completed successfully.

Every scientific worker reported only:
`Haswell`

through runtime OpenBLAS evidence.

## Controller

The controller remained unchanged:
- alpha = 0.05;
- epsilon = 0.001;
- half-spend = 1000;
- prior retained attempts = 199;
- first new draw index = 199;
- maximum new draw index = 9999;
- maximum total attempts = 10000.

The 10,000 cap is the prospectively frozen computational truncation from the continuation design. It is not a fixed bootstrap sample size selected from these results.

## Target-set integrity

C2 continued exactly the 224 homogeneous H2 unresolved streams.

Checks:
- target stream count: 224;
- target run-ID digest:
  `d2db2c97ad48544c082cdffd086c022a28c6d0c75690b36a0cd0b2b381c4ebac`;
- exact dataset fingerprints: 224/224;
- exact observed statistics: 224/224;
- maximum observed-statistic absolute delta: 0;
- H2-resolved streams extended: 0;
- every stream's first new draw index: 199.

## C2 result

Across 224 continued streams:
- newly resolved: 201;
- newly reject: 127;
- newly not-reject: 74;
- bootstrap-refit-failure unresolved: 0;
- unresolved at cap: 23;
- total new bootstrap fits attempted: 401,601;
- total successful new bootstrap fits: 401,601.

Stopping n among the 201 newly resolved streams:
- minimum: 202;
- median: 519;
- maximum: 8,529.

The 23 cap-unresolved streams remain first-class unresolved outcomes. They are not converted to decisions using a fixed-size p-value.

Canonical SHA-256 of the 23 unresolved-at-cap run IDs:
`673ac85475800b4e032469fbeae8ead7083e6cd90fee209f7e0c451162b13217`

## Reporting checkpoints

Cumulative newly resolved:
- n=199: 0 / 224;
- n=499: 98 / 224;
- n=999: 144 / 224;
- n=1999: 172 / 224;
- n=4999: 194 / 224;
- n=10000: 201 / 224.

Active/unresolved at those checkpoints:
- 224;
- 126;
- 80;
- 52;
- 30;
- 23.

No bootstrap refit failure occurred at any checkpoint.

## Interpretation

C2 completes the prospectively defined numerical continuation of the sequential resampling-risk controller.

It does not by itself establish:
- scientific Type-I error;
- model validity;
- recovery power;
- an authoritative core grid;
- human N;
- recruitment readiness;
- runtime F1b activation.

The fact that 23 streams remain unresolved at the prospectively frozen cap is itself a retained scientific-computational outcome and must not be erased by extending the cap post hoc.

The next step is a separate scientific interpretation gate that decides what the C2 result implies for subsequent recovery/power/core-grid characterization without retroactively tuning the C2 controller or cap.

## Boundary

`H1 HOMOGENEOUS SOURCE = QUALIFIED`

`H2 HOMOGENEOUS STAGE-B = PASS / RETAINED`

`C1 HOMOGENEOUS EXACT REPLAY = PASS 224/224 / RETAINED`

`C2 PROSPECTIVE CONTINUATION = COMPLETE`

`C2 NEWLY RESOLVED = 201 / 224`

`C2 UNRESOLVED AT CAP = 23 / 224`

`BOOTSTRAP REFIT FAILURES = 0`

`FIXED BOOTSTRAP DRAW COUNT = NOT SELECTED`

`POWER = NOT VALIDATED`

`AUTHORITATIVE CORE GRID / HUMAN N = NOT FROZEN`

`PARTICIPANT RECRUITMENT = NOT AUTHORIZED`

`RUNTIME F1B = NOT AUTHORIZED`
