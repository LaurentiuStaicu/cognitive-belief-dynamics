# F1b R2 S4 M2 prefix-bridge result — 2026-09-29

Issue: #259

Status: **PREFIX BRIDGE COMPLETE / 3,360 M2 METHOD ROWS AUTHORIZED FOR EXACT REUSE / BROAD EXECUTION NOT YET RUN**

The prefix-bridge gate was merged in PR #281 and executed in temporary PR #282, which was closed unmerged.

Execution evidence:
- workflow run: `36469185960`;
- artifact ID: `10991217073`;
- artifact ZIP SHA-256: `e2a2ef2ddffef5a8936445e6f91564ddda160d9fa53704e280b147b1c72dd1c7`;
- bridge JSON SHA-256: `2a820cfc038076e83597be7b33f96274e1a2e4e71f012abe8d638de5e85b7e9f`;
- bridge JSON size: 2,180 bytes.

The bridge regenerated all deterministic prefix datasets and verified exact scientific identity, dataset fingerprints, M1 attempt-sequence digests, bootstrap seeds, observed statistics, M2 terminal evidence and unresolved-at-cap semantics.

## Authorized imported prefix

Exact reusable evidence:
- 840 scientific runs;
- 3,360 method rows;
- 720 departure scientific runs;
- 120 null scientific runs.

Replicate ranges:
- departure: 0..4;
- null: 0..19;
- missingness: 0.00 / 0.15.

Canonical imported identity digests:
- scientific-run IDs SHA-256:
  `9b3efdf5ba42fa13135d2098af8769a561d51faf7a5279dc2718d9d965e22c4a`;
- method-row IDs SHA-256:
  `d9d42ed4437199375c593110f555502d26a6660e81e045b9e1b105e8a1434537`.

Terminal status counts:
- `SEQUENTIAL_RESOLVED_AT_PREFIX`: 2,402;
- `SEQUENTIAL_RESOLVED`: 834;
- `SEQUENTIAL_UNRESOLVED_AT_CAP`: 124;
- `BOOTSTRAP_REFIT_FAILURE_UNRESOLVED`: 0.

Unresolved-at-cap rows remain unresolved in S4.

They are not converted into reject/not-reject outcomes.

## Broad consequence

The scientific estimand remains unchanged:
- 15,000 scientific runs;
- 60,000 method/run identities.

The bridge only avoids exact recomputation where retained evidence is byte/provenance compatible.

After import:
- imported scientific runs: 840;
- imported method rows: 3,360;
- new scientific runs requiring execution: 14,160;
- new method executions: 56,640.

Wave consequence:
- W0: 11,640 new method executions;
- W1: 15,000;
- W2: 15,000;
- W3: 15,000.

## Next gate

Before broad execution starts, freeze the operational execution topology and final combine.

The planned topology uses four deterministic replicate waves:
- W0: 0..24;
- W1: 25..49;
- W2: 50..74;
- W3: 75..99.

Within each wave, scientific runs are assigned deterministically to 250 shards.

This keeps each GitHub Actions matrix under the platform maximum of 256 jobs per workflow run while preserving exact run identity and method pairing.

## Version boundary

The next planned public scientific-core release remains v0.2.0 under Issue #277.

The prefix bridge does not close that release blocker.

v0.2.0 remains blocked until broad S4 is executed, retained and scientifically interpreted.

## Boundary

`PREFIX IMPORT = AUTHORIZED`

`IMPORTED METHOD ROWS = 3,360`

`NEW METHOD EXECUTIONS = 56,640`

`BROAD DENOMINATOR = 60,000`

`METHOD SELECTED = NO`

`POWER = NOT VALIDATED`

`v0.2.0 BLOCKER = OPEN`
