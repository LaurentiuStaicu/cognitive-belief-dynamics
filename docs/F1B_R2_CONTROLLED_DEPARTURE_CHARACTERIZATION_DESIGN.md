# F1b R2 Controlled-Departure and Bootstrap Characterization Design

Status: **PROSPECTIVE_CONTROLLED_DEPARTURE_CHARACTERIZATION_DESIGN**

Issue: #145  
Parent issues: #125, #130, #134  
Baseline main: `bc78f0e5c25dd442389298ef83f93b070400a01a`

## Purpose

The R2 restriction engine is implemented and smoke-qualified. The next problem is to generate departures at known distance from the CBD-complement manifold without defining effect size by arbitrary coefficient perturbation.

This design freezes that procedure before any projection or characterization engine is written.

## Primary distance

Departure strength is:

`RMS utility distance to the nearest CBD-complement surface`

over the frozen 18 cells:

`B={0.2,0.5,0.8} × A={0,1} × R={-1,0,1}`.

Raw coefficient distance is not used as the scientific design quantity.

## Nearest-CBD projection

For each general six-coefficient action surface, project numerically onto the four-parameter CBD-complement surface.

The optimization uses:

- the same AP-A parameter bounds as the current fitter;
- deterministic multi-start;
- source CBD anchor;
- an algebraic general→CBD approximate start;
- a neutral start;
- L-BFGS-B;
- best successful solution.

A failed projection is a design-generation failure.

The algebraic start uses the current exact CBD nesting relations where possible:

- `W0 = clip(beta_b)`;
- `W1 = clip(beta_b+beta_ab)`;
- baseline/accuracy logits from W0/W1;
- reward coefficient from `beta_r/(1-W0)`.

## Nearest-ADD projection

ADD is a linear restriction.

Its nearest utility surface is obtained by least-squares projection onto the columns:

`1, (2B-1), A, R`

with both interaction coefficients fixed to zero.

## Departure axes

Three frozen axes are used.

### Standalone accuracy main effect

`d_A=(0,0,1,0,0,0)`

This violates CBD but remains exactly ADD-compatible.

Therefore ADD rejection on this axis is a pre-frozen specificity failure.

### Complement-relation violation

`d_C=(0,0,0,0,0,1)`

This perturbs the accuracy×reward term away from the CBD complement relation.

### Combined violation

RMS-normalize d_A and d_C separately, sum them, then RMS-normalize the combined vector.

Every axis is tested in both positive and negative directions.

## Exact target distances

Retain:

- 0.10;
- 0.25;
- 0.50;

RMS utility-logit units to the nearest CBD surface.

For each anchor×axis×sign×distance, move along the normalized direction and repeatedly re-project to CBD. Use the first bracket crossing the target and Brent root-finding.

Frozen scalar bracket grid:

`0, 0.125, 0.25, 0.5, 1, 2, 4, 8, 16`.

Required final distance error:

`<= 1e-6`.

## Synthetic anchors

Two CBD anchors are required:

- CBD_ANCHOR_1 = `(-0.2,-0.2,1.0,0.8)`;
- CBD_ANCHOR_2 = `(-0.2,0.0,1.2,1.0)`;

in AP-A parameter order:

`sharing_bias, baseline_logit, beta_accuracy, beta_reward`.

ADD null anchor:

`(-0.2,0.8,0.25,0.6)`

in AP-B parameter order.

These are synthetic design anchors, not human estimates.

## Bootstrap characterization

The current R2 engine uses parametric bootstrap because no asymptotic chi-square reference is assumed.

The first draw-count search is:

`49, 99, 199`.

These are characterization values only.

Calibration and evaluation random streams must be independent.

Authoritative evaluation replicates are not yet frozen.

Wilson 95% intervals are required for false-rejection and detection rates.

## Independent restriction interpretation

ADD and CBD are tested independently.

Valid outcomes include:

- neither rejected;
- ADD only;
- CBD only;
- both.

No unique winner is required.

Failure to reject is not proof that a restriction is true.

## Gate

`R2 restriction engine = IMPLEMENTED / SMOKE NON-AUTHORITATIVE`

`controlled-departure design = FROZEN / ENGINE NOT YET IMPLEMENTED`

`authoritative bootstrap draws = NOT FROZEN`

`authoritative evaluation replicates = NOT FROZEN`

`authoritative core grid = NOT FROZEN`

`human N = NOT FROZEN`

`participant recruitment = NOT AUTHORIZED`

`runtime F1b = NOT AUTHORIZED`
