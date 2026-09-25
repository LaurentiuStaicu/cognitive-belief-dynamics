# F1b R1 High-Replicate Characterization

Status: **NON_AUTHORITATIVE_R1_HIGH_REPLICATE_DESIGN**

Issue: #135  
Parent: #130

Baseline main:
`2d2db50cc6455989a1aad845b731c00a5eebd608`

## Purpose

The initial three-replicate characterization was intentionally diagnostic and too coarse for a stability decision.

R1 is now separated from the structurally nested R2 problem.

This design increases R1 to 200 replicates per generator × separation × missingness cell while retaining the same candidate families and identical-data inference comparison.

## Frozen design

Candidate generators:
- SR-A — centered anti-reliability;
- SR-B — discount-only;
- SR-C — threshold/gating.

Separation:
- WEAK;
- MODERATE;
- STRONG.

Missingness:
- 0%;
- 15%.

Inference variants:
- population;
- hierarchical 0.5×;
- hierarchical 1×;
- hierarchical 2× assumed random-effect scales.

Each synthetic dataset is evaluated by all inference variants.

## Uncertainty

Every recovery, wrong-selection, inconclusive and fit-failure proportion receives a marginal 95% Wilson interval.

These intervals are descriptive marginal intervals.

No simultaneous/familywise coverage claim is made.

## Prospective design-eligibility rule

This is **not** a scientific promotion threshold.

An inference regime is merely eligible for later core-grid design work if every STRONG cell across:
- SR-A / SR-B / SR-C;
- 0% / 15% missingness

satisfies all of:

- recovery point estimate >= 0.80;
- lower 95% Wilson recovery bound >= 0.70;
- wrong-model probability <= 0.05;
- fit-failure probability <= 0.01.

The rule is frozen before the 200-replicate run.

Failure means the inference/design needs revision before a later core grid is considered.

Passing means only that later prospective core-grid design may be considered.

## Gate

`R1 high-replicate run = NOT YET EXECUTED`

`R1 authoritative core grid = NOT FROZEN`

`human N = NOT FROZEN`

`participant recruitment = NOT AUTHORIZED`

`runtime F1b = NOT AUTHORIZED`
