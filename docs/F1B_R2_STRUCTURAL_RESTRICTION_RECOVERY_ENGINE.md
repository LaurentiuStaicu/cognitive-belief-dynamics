# F1b R2 Structural-Restriction Recovery Engine — Smoke Stage

Status: **SMOKE_NON_AUTHORITATIVE_R2_RESTRICTION_ENGINE**

Issue: #134  
Design baseline: PR #136 / `2d2db50cc6455989a1aad845b731c00a5eebd608`

## Purpose

This module implements the first executable recovery engine for the redesigned F1b R2 action-policy problem.

It does not classify AP-A / AP-B / AP-C as mutually exclusive model labels.

Instead it tests two restrictions independently inside the encompassing AP-GENERAL action surface:

- ADD restriction;
- CBD-complement restriction.

## Fit structure

Each restriction is fit with exactly the same participant/item random-effect structure as AP-GENERAL:

- participant random intercept;
- item random intercept;
- participant reward-context slope;
- item reward-context slope.

The current penalized conditional/MAP hierarchical fitter is reused unchanged.

## Statistic

For each restriction:

`Delta_Q = Q_restricted - Q_general`

where `Q` is the penalized objective returned by the common hierarchical fitter.

Because the restricted surface is nested in AP-GENERAL, the improvement should be nonnegative up to numerical tolerance.

A material negative value is treated as an optimization/nesting integrity failure, not silently corrected.

## Parametric-bootstrap calibration

The engine does not assume a chi-square reference distribution.

For each tested restriction:

1. fit the restricted and encompassing surfaces to the observed/synthetic dataset;
2. simulate independent response data under the fitted restricted null using the same design rows and declared random-effect scales;
3. refit both surfaces to every bootstrap draw;
4. form the empirical null distribution of `Delta_Q`;
5. compute a plus-one bootstrap p-value;
6. report the empirical critical value and fit failures.

This follows the already-frozen #134 requirement for simulation-calibrated restriction testing.

## Independent outcomes

ADD and CBD-complement are tested independently.

Therefore both may be:
- not rejected;
- rejected;
- or differ.

Failure to reject is not proof that the restriction is true.

No unique model winner is required.

## Held-out prediction

Held-out participant and held-out item predictive log-likelihood deltas are retained as secondary diagnostics only.

Unseen grouping levels use the population-level zero random-effect prediction rule already frozen for the hierarchical prototype.

## Smoke boundary

The smoke config uses only a few bootstrap draws to verify the execution path.

It does not freeze:
- authoritative bootstrap draws;
- evaluation replicates;
- departure distances;
- participant×item grid;
- final inference method.

## Gate

`R2 restriction engine = IMPLEMENTED / SMOKE NON-AUTHORITATIVE`

`authoritative calibration = NOT AUTHORIZED`

`authoritative core grid = NOT FROZEN`

`human N = NOT FROZEN`

`participant recruitment = NOT AUTHORIZED`

`runtime F1b = NOT AUTHORIZED`
