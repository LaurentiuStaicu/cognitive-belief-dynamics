# F1b R2 S4 M2 prefix-bridge gate

Issue: #259

Status: **PREFIX REUSE CONTRACT IMPLEMENTED / BROAD EXECUTION NOT YET RUN**

## Purpose

The broad S4 matrix contains the complete M2 scientific matrix as a deterministic prefix.

This gate decides whether retained M2 terminal evidence may be imported into the broad S4 result without recomputation.

Import is allowed only when exact scientific, numerical and provenance identity is demonstrated.

## Frozen sources

The bridge pins:
- H1 source artifact;
- M1 combined artifact;
- M2 combined artifact;
- S4 broad scientific-matrix artifact;
- the M1/M2/S4 design and implementation blobs required to regenerate and identify the prefix.

All source JSONs are verified by SHA-256 before use.

## Exact overlap

Required overlap:
- 840 scientific runs;
- 3,360 method rows;
- 720 departure scientific runs;
- 120 null scientific runs.

Replicate identity:
- departure: 0..4;
- null: 0..19;
- missingness: 0.00 / 0.15.

Every prefix scientific run must exist in the 15,000-run S4 manifest.

Every scientific run must have exactly the four frozen methods.

## Row-level bridge checks

For each imported method row the gate requires:

- exact scientific_run_id;
- exact dataset_id;
- exact identity / identity_type;
- exact restriction and scientific role;
- exact anchor / axis / sign / KL;
- exact evaluation replicate;
- exact missingness;
- deterministic dataset regeneration with the same SHA-256;
- exact M1/M2 observed statistic;
- exact bootstrap base seed;
- exact retained M1 attempt-sequence digest;
- exact regenerated M1 attempt-sequence digest;
- `m1_prefix_exact = true`;
- zero new refit failure;
- valid M2 terminal status and controller-consistent terminal n.

Allowed imported M2 statuses:
- `SEQUENTIAL_RESOLVED_AT_PREFIX`;
- `SEQUENTIAL_RESOLVED`;
- `SEQUENTIAL_UNRESOLVED_AT_CAP`.

Unresolved-at-cap rows remain unresolved.

They are not converted into decisions for broad S4.

## Frozen expected M2 status counts

Across the 3,360 imported method rows:
- resolved at n=199 prefix: 2,402;
- resolved after continuation: 834;
- unresolved at n=10,000 cap: 124;
- bootstrap-refit-failure unresolved: 0.

A different count fails closed.

## Broad consequence

If all bridge checks pass:

- retained/imported scientific runs: 840;
- retained/imported method rows: 3,360;
- new scientific runs requiring broad execution: 14,160;
- new method executions: 56,640.

The full broad estimand remains:
- 15,000 scientific runs;
- 60,000 method/run identities.

Import does not shrink any denominator.

A row that fails the bridge must be recomputed in broad S4 rather than dropped or replaced.

## Wave consequence

All prefix rows lie in W0.

W0:
- total scientific runs: 3,750;
- imported: 840;
- new scientific runs: 2,910;
- new method executions: 11,640.

W1-W3:
- 3,750 new scientific runs each;
- 15,000 new method executions each.

Total new method executions if the bridge passes: 56,640.

## Boundary

This gate does not:
- select an inference method;
- select a hierarchical scale;
- change M2;
- change the S4 scientific matrix;
- change the broad estimand;
- validate power;
- freeze human N;
- authorize recruitment or runtime F1b;
- change the package version.

The planned v0.2.0 release remains blocked on the completed and interpreted broad S4 result.
