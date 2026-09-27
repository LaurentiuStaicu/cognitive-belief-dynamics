# F1b R2 Broad Controlled-Departure Characterization — 49×20

Status: **FROZEN / NOT EXECUTED / NON-AUTHORITATIVE**

Issue: #158  
Parent design: #145  
Preceding calibration screen: #154  
Baseline: `1b13c0c38c7a20b23ab88d72a0d3366885e59ebe`

## Purpose

Characterize the complete R2 controlled-departure surface after the staged calibration/specificity screen selected 49 bootstrap draws for advancement within design search.

This stage is not an authoritative power study and does not freeze 49 draws.

## Independence from the calibration screen

The master seed is frozen to:

`2026092702`

This is different from the earlier characterization seed. The broad stage therefore does not reuse the evaluation sample on which 49 draws passed #154.

## Synthetic design

- participants: 24;
- items: 36;
- B: 0.2 / 0.5 / 0.8;
- A: 0 / 1;
- R: -1 / 0 / 1;
- missingness: 0;
- random-effect scales unchanged;
- fit-scale multiplier: 1×.

Bootstrap:
- draws: 49;
- alpha: 0.05;
- minimum successful draws: 45.

Evaluation:
- 20 replicates per scientific cell.

## Complete departure grid

### Standalone accuracy main effect

Use:
- CBD_ADD_INTERSECTION_ANCHOR_1;
- CBD_ADD_INTERSECTION_ANCHOR_2.

Cross:
- both signs;
- RMS distances 0.10 / 0.25 / 0.50.

Total: 12 cases.

These departures are exactly ADD-compatible by construction, so ADD rejection is a specificity diagnostic.

### Complement-relation violation

Use CBD_ANCHOR_1 / CBD_ANCHOR_2 × both signs × all three distances.

Total: 12 cases.

### Combined violation

Use CBD_ANCHOR_1 / CBD_ANCHOR_2 × both signs × all three distances.

Total: 12 cases.

### Total workload

- 36 departure cases;
- two restriction tests per departure;
- three null identities;
- 75 restriction identities per replicate;
- 20 evaluation replicates;
- 1500 restriction tests.

No axis, anchor, sign or distance may be omitted after inspecting results.

## Safe execution partitioning

Do not shard by departure axis, anchor or filtered case list.

The retained engine currently keys departure RNG by `case_index`, so filtered departure sharding could change the generated data.

Use only the integrated replicate partitioner:

- R00_04 → 0–4;
- R05_09 → 5–9;
- R10_14 → 10–14;
- R15_19 → 15–19.

Every shard must retain the scientific evaluation count of 20 in the config and select only execution replicate indices. The integrated combiner must reject overlap or incomplete coverage and recompute aggregate outputs from the union of trials.

## Required retained outputs

Per aggregate cell:
- restriction;
- identity;
- anchor;
- axis;
- sign;
- requested / achieved nearest-CBD RMS distance;
- nearest-ADD RMS distance;
- rejections / 20;
- Wilson 95% interval;
- fit failure count;
- bootstrap-calibration failure count;
- bootstrap-fit failures;
- held-out participant delta;
- held-out item delta.

Also retain execution provenance and exact partition identities.

## Interpretation

Report:
1. fresh-seed CBD/ADD null false rejection;
2. CBD detection surface across all 36 departures;
3. ADD specificity across all 12 standalone cases;
4. ADD decisions on complement/combined cases descriptively;
5. sign asymmetry;
6. distance-ordering diagnostics;
7. fit/calibration failures;
8. held-out participant/item deltas.

Do not select only favorable cases. Failure to reject does not prove a restriction. Rejection does not identify a unique psychological mechanism.

## Boundary

`49 BOOTSTRAP DRAWS = SCREENED FOR THIS NON-AUTHORITATIVE STAGE ONLY`

`20 EVALUATION REPLICATES = STAGED DESIGN-SEARCH COUNT ONLY`

`AUTHORITATIVE BOOTSTRAP DRAWS = NOT FROZEN`

`AUTHORITATIVE EVALUATION REPLICATES = NOT FROZEN`

`AUTHORITATIVE CORE GRID = NOT FROZEN`

`HUMAN N = NOT FROZEN`

`PARTICIPANT RECRUITMENT = NOT AUTHORIZED`

`RUNTIME F1B = NOT AUTHORIZED`
