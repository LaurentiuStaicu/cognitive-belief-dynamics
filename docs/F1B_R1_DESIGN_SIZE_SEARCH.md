# F1b R1 Participant×Item Design-Size Search

Status: **NON_AUTHORITATIVE_R1_DESIGN_SIZE_SEARCH**

Issue: #141  
Parent: #130

Baseline:
`b923e5f49f5b1261f998da4f773b93877eb62c62`

## Purpose

The 200-replicate R1 characterization under the current 24×24 synthetic design failed the prospectively frozen eligibility rule for every inference regime.

This search asks one narrow question:

> Can increasing participants and/or items make the same R1 candidate families recoverable without changing the selection rule or scientific interpretation?

## Frozen axes

Participants:
`24, 48, 96`

Items:
`24, 48, 96`

The item counts are multiples of the 12 frozen R1 condition cells.

Only STRONG separation is searched because the existing design-eligibility rule is defined on STRONG cells.

Missingness:
`0%, 15%`

Inference:
- population;
- hierarchical 0.5×;
- hierarchical 1×;
- hierarchical 2× stress.

Replicates:
`200` per participant×item×generator×missingness cell.

## Unchanged eligibility rule

Every SR-A/SR-B/SR-C × missingness STRONG cell must satisfy:

- recovery >= 0.80;
- lower Wilson 95% recovery bound >= 0.70;
- wrong <= 0.05;
- fit failure <= 0.01.

No threshold is relaxed after observing #135.

## Interpretation

The search reports eligible participant×item regions and a Pareto frontier by inference regime.

These are synthetic design regions only.

An eligible 48×96 or 96×48 result would **not** mean that 48 or 96 human participants/items are approved.

If only the population fitter becomes eligible, that does not authorize population-only inference for human data.

If no hierarchical regime becomes eligible even at 96×96, return to inference-method diagnostics under #130 rather than enlarging N indefinitely.

## Gate

`authoritative core grid = NOT FROZEN`

`human N = NOT FROZEN`

`participant recruitment = NOT AUTHORIZED`

`runtime F1b = NOT AUTHORIZED`
