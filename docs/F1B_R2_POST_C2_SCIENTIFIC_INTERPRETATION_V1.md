# F1b R2 post-C2 scientific interpretation gate

Issue: #249

Status: **S0–S3 IMPLEMENTED / DESCRIPTIVE CHARACTERIZATION ONLY / POWER NOT YET VALIDATED**

## Purpose

This gate reconstructs the final three-outcome state of all 750 homogeneous F1b R2 characterization streams after retained H2 + C2.

It performs no new bootstrap simulation and does not change:
- the scientific model;
- the fitter;
- the sequential controller;
- alpha, epsilon or half-spend;
- the C2 cap;
- any C2 terminal decision;
- any C2 unresolved-at-cap status.

## Frozen inputs

H2:
- retained result:
  `model/results/f1b_r2_homogeneous_stage_b_rebuild_2026-09-28.json`;
- raw artifact ID: `10962483226`;
- raw JSON SHA-256:
  `f0f32d92e46748148f020a4e0d47d2c63e27f6ab1aa36253346e15c4dfaf01e7`;
- total streams: 750;
- unresolved at n=199: 224.

C2:
- retained result:
  `model/results/f1b_r2_homogeneous_c2_continuation_2026-09-28.json`;
- combined artifact ID: `10968522362`;
- combined JSON SHA-256:
  `03009d7b586502f500062d67792f048e768fe737670823b2e033cb82c59a867a`;
- continued streams: 224;
- resolved prospectively: 201;
- unresolved at cap: 23;
- maximum total attempts: 10000.

## Three-outcome rule

Primary characterization always keeps:
- `REJECT_P_LE_ALPHA`;
- `NOT_REJECT_P_GT_ALPHA`;
- `SEQUENTIAL_UNRESOLVED_AT_CAP`.

Unresolved streams remain in the primary denominator.

Decided-only proportions may be reported only as secondary descriptive quantities.

For every group the characterization reports a reject-proportion interval induced solely by unresolved streams:

`[reject / total, (reject + unresolved) / total]`.

This is a sensitivity bound, not a confidence interval.

## Final 750-stream integrity

The gate requires exactly:
- reject: 246;
- not-reject: 481;
- unresolved-at-cap: 23.

The exact C2 target set must equal the 224 H2-unresolved streams.

Any H2-resolved stream appearing in C2 fails closed.

The exact 23 unresolved-at-cap run IDs must reproduce SHA-256:

`673ac85475800b4e032469fbeae8ead7083e6cd90fee209f7e0c451162b13217`.

## Role semantics

Rejection is not interpreted uniformly across roles.

Detection roles:
- `ADD_DEPARTURE_DIAGNOSTIC`;
- `CBD_DEPARTURE_DETECTION`.

For these roles:
- reject = detection;
- not-reject = missed detection;
- unresolved = indeterminate.

Negative-control roles:
- `ADD_NULL_FALSE_REJECTION`;
- `ADD_SPECIFICITY_NEGATIVE_CONTROL`;
- `CBD_NULL_FALSE_REJECTION`.

For these roles:
- reject = false detection;
- not-reject = specificity pass;
- unresolved = indeterminate.

The implementation therefore does not collapse all streams into one “power” estimate.

## Aggregation

The runner produces descriptive three-outcome summaries by:
- restriction;
- role;
- identity type;
- axis;
- KL target;
- sign;
- anchor;
- evaluation replicate.

It also retains the exact 23 unresolved rows for later S4/S5 adequacy analysis.

## Implementation

Added:
- `model/benchmarks/f1b_r2_post_c2_scientific_interpretation_v1.json`;
- `src/cognitive_epistemic_model/calibration/f1b_r2_post_c2_scientific_interpretation.py`;
- `scripts/run_f1b_r2_post_c2_scientific_interpretation.py`;
- dedicated fail-closed tests.

## Next gate

After this descriptive layer is reviewed and executed against the retained artifacts, the next scientific step is S4/S5:

- assess evaluation-replicate adequacy;
- decide whether additional prospective characterization replicates are required;
- revisit population-level versus hierarchical recovery, missingness and variance-misspecification sensitivity;
- define inferential recovery/power estimands before any core-grid or human-N freeze.

No C2 cap extension is part of that decision.

## Boundary

`C2 = COMPLETE / IMMUTABLE`

`UNRESOLVED AT CAP = 23 / RETAINED`

`THREE-OUTCOME PRIMARY ESTIMAND = REQUIRED`

`DESCRIPTIVE CHARACTERIZATION = IMPLEMENTED`

`POWER = NOT VALIDATED`

`AUTHORITATIVE CORE GRID = NOT FROZEN`

`HUMAN N = NOT FROZEN`

`PARTICIPANT RECRUITMENT = NOT AUTHORIZED`

`RUNTIME F1B = NOT AUTHORIZED`
