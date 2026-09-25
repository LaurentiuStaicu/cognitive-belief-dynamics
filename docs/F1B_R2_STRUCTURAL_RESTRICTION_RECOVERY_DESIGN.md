# F1b R2 Structural-Restriction Recovery Design

Status: **PROSPECTIVE_STRUCTURAL_RESTRICTION_RECOVERY_DESIGN**

Issue: #134  
Parent issues: #125, #130  
Baseline main: `938f72789e883ff5e98c4edc58ffbf3ced84fc93`

## Why the former R2 recovery design is rejected

The first characterization showed overwhelmingly inconclusive AP-A/AP-B/AP-C label recovery.

This is not merely a small-sample problem.

The flexible action surface can be written as:

`u = b + beta_b*(2B-1) + beta_a*A + beta_r*R + beta_ab*A*(2B-1) + beta_ar*A*R`

with binary accuracy cue `A ∈ {0,1}`.

AP-B is the direct restriction:

`beta_ab = beta_ar = 0`.

The current CBD AP-A equation is also exactly representable inside this surface.

Let:

`W0 = logistic(logit(accuracy_baseline))`

`W1 = logistic(logit(accuracy_baseline) + beta_accuracy_cue)`

and `g = beta_reward`.

Then AP-A maps to:

`beta_a = 0`

`beta_b = W0`

`beta_ab = W1-W0`

`beta_r = g*(1-W0)`

`beta_ar = g*(W0-W1)`.

Therefore, where defined, the CBD surface satisfies:

`beta_ar*(1-beta_b) + beta_r*beta_ab = 0`

with:

`0 < beta_b < 1`

and:

`0 < beta_b+beta_ab < 1`.

The former three-label recovery task forced exclusive classification among nested surfaces. That is not the right scientific question.

## New scientific question

The encompassing flexible surface is retained as the observation-level action surface.

We test whether data are compatible with, or detect departures from, two explicit restrictions.

### ADD restriction

`beta_ab = beta_ar = 0`

This represents no accuracy-dependent change in the belief or reward slopes.

### CBD complement restriction

`beta_a = 0`

`beta_ar*(1-beta_b) + beta_r*beta_ab = 0`

plus valid implied `W0/W1` bounds.

This represents the observable restriction implied by the current CBD complement structure.

These tests are independent. A dataset can legitimately be compatible with both restrictions, with one, or with neither.

No unique model winner is required.

## Distance from a restriction

Raw coefficient distance is not the primary design quantity.

The preferred design quantity is:

`RMS utility distance to the nearest restricted surface`

evaluated over the frozen `B × A × R` design cells.

This makes departure size interpretable on the action-logit utility scale and avoids declaring one arbitrary coefficient perturbation to be universally weak or strong.

The initial candidate search distances are:

`0.10, 0.25, 0.50` logit-utility units.

These are design-search values only, not gates or empirically calibrated effects.

## Violation axes

The first recovery design should distinguish:

1. standalone accuracy main-effect violation;
2. complement-relation violation;
3. combined violation.

The generator must control distance from the CBD manifold prospectively.

## Test calibration

The current hierarchical fitter is a penalized conditional/MAP prototype, not a validated marginal-likelihood GLMM.

Therefore a standard chi-square reference distribution is not assumed.

The first recovery engine should:

1. fit the restricted and encompassing surfaces with the same random-effect structure;
2. compute a prospectively defined penalized-objective improvement statistic;
3. simulate independent null datasets under the restricted model;
4. calibrate the rejection threshold by parametric bootstrap;
5. evaluate false rejection on independent null replicates;
6. evaluate detection on independent departure replicates.

Nominal false-rejection target:

`0.05`

The actual achieved false-rejection rate must be reported.

Held-out participant and item predictive scores remain secondary generalization diagnostics.

## Outcomes

The design does not force one label.

Report separately:

- CBD restriction rejected / not rejected;
- ADD restriction rejected / not rejected;
- fit failure;
- bootstrap-calibration failure.

Failure to reject is not proof that a mechanism is true.

## Gate

`current R2 label-classification design = REJECTED FOR AUTHORITATIVE USE`

`R2 structural-restriction recovery = DESIGN FROZEN / ENGINE NOT YET IMPLEMENTED`

`authoritative core grid = NOT FROZEN`

`human N = NOT FROZEN`

`participant recruitment = NOT AUTHORIZED`

`runtime F1b = NOT AUTHORIZED`
