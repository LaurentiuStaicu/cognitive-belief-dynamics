# F1b R2 homogeneous Stage-B rebuild

Issue: #234

Status: **H2 CONTRACT IMPLEMENTED / H2 NOT YET EXECUTED / STAGE C2 BLOCKED**

## Purpose

H2 rebuilds the Stage-B resampling-risk provenance from the newly qualified homogeneous H1 paired source.

H1 source:
- numerical lineage: `F1B.R2.HOMOGENEOUS_PAIRED_SOURCE.LINEAGE.V1`;
- Actions artifact ID: `10961527329`;
- combined JSON SHA-256: `618b52162e98d25d41ac9cc7a6411ccfbf3c95775412a46b759e1514e90ed37e`;
- restriction runs: 750;
- retained bootstrap attempts per run: 199;
- bootstrap refit failures: 0.

The historical heterogeneous paired source and historical Stage-B result remain retained evidence only.

## Frozen controller

H2 reuses the existing controller algorithm and all controller parameters unchanged:

- controller: `F1B.R2.RESAMPLING_RISK_CONTROLLER.V1`;
- alpha: 0.05;
- epsilon: 0.001;
- half-spend: 1000;
- spending sequence: `epsilon*n/(1000+n)`;
- replay horizon: 199;
- probability tolerance: `1e-12`;
- bootstrap refit failure policy: `BOOTSTRAP_REFIT_FAILURE_UNRESOLVED`;
- unchanged decision semantics and boundary initialization.

The historical controller configuration file is not edited. H2 verifies that file and the controller implementation blobs, then constructs an in-memory replay-source binding for the H1 artifact only.

Therefore the only provenance change is the paired source.

## No new bootstrap computation

H2 is a replay of the already generated first-199 attempt sequences.

It:
- does not fit a new bootstrap replicate;
- does not generate a new bootstrap attempt;
- does not generate draw index >=199;
- does not alter attempt ordering or canonicalization;
- does not inherit historical Stage-B terminal decisions;
- does not inherit the historical unresolved set;
- does not inherit historical stream checkpoints.

## H2 output

Execution must produce a new versioned Stage-B result containing:
- terminal decisions;
- unresolved stream set;
- stream checkpoints;
- aggregate summaries;
- exact H1 source identity and hash;
- frozen-controller identity;
- execution provenance.

The result must then be compared with the historical Stage-B result as sensitivity evidence only. Differences must not be used to tune the controller.

## Next gate

Only after the new H2 result is retained may a successor continuation contract define the C1 exact-replay gate for the new unresolved set.

The historical 526 resolved / 224 unresolved partition cannot authorize the new lineage.

## Boundary

`H1 HOMOGENEOUS SOURCE = QUALIFIED`

`H2 STAGE-B REBUILD = REQUIRED / NOT YET EXECUTED`

`HISTORICAL STAGE-B = RETAINED / NOT INHERITED`

`CONTROLLER = UNCHANGED`

`NEW BOOTSTRAP ATTEMPTS = NOT AUTHORIZED`

`NEW DRAW INDEX >=199 = NOT AUTHORIZED`

`STAGE C2 = BLOCKED`

`STATISTICAL POWER = NOT VALIDATED`

`AUTHORITATIVE CORE GRID / HUMAN N = NOT FROZEN`

`PARTICIPANT RECRUITMENT = NOT AUTHORIZED`

`RUNTIME F1B = NOT AUTHORIZED`
