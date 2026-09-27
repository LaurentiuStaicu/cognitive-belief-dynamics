# F1b R2 Controlled-Departure Generator

Status: **NON_AUTHORITATIVE_CONTROLLED_DEPARTURE_GENERATOR**

Issue: #145  
Baseline main: `bc78f0e5c25dd442389298ef83f93b070400a01a`

## Purpose

This module implements only the geometry required before R2 restriction-test characterization.

It generates AP-GENERAL synthetic surfaces at prospectively requested RMS utility distance from the nearest CBD-complement surface.

It does not yet execute bootstrap detection/false-rejection characterization.

## Frozen utility design

Distance is evaluated over the 18 declared cells:

- B = 0.2, 0.5, 0.8;
- A = 0, 1;
- R = -1, 0, 1.

Distance is RMS difference in action-logit utility.

## Nearest CBD projection

For any AP-GENERAL coefficient vector, the generator minimizes RMS utility distance over the current AP-A/CBD parameterization:

- sharing bias;
- baseline logit;
- accuracy-cue coefficient;
- reward coefficient.

The parameter bounds are identical to the current AP-A fitter.

Projection uses seven prospectively frozen deterministic starts. All failed starts are a design-generation failure; no manual rescue is permitted.

## Nearest ADD projection

ADD projection is ordinary least squares in the same 18-cell utility space with:

`beta_ab = beta_ar = 0`.

It is used as a diagnostic and for the standalone-accuracy specificity negative control.

## Important anchor correction

The original CBD_ANCHOR_1/2 are not ADD-restricted because nonzero CBD accuracy-cue effects imply nonzero AP-GENERAL interaction terms.

Therefore they cannot support an ADD-specificity negative control.

For `STANDALONE_ACCURACY_MAIN_EFFECT` the generator uses matched CBD∩ADD anchors:

- `(-0.2,-0.2,0.0,0.8)`;
- `(-0.2,0.0,0.0,1.0)`.

Adding only `beta_a` remains exactly ADD-compatible while violating CBD.

The complement and combined axes retain the original CBD anchors.

## Departure directions

Primitive directions are normalized to unit RMS utility effect before distance solving.

- standalone accuracy main effect: `beta_a`;
- complement relation violation: `beta_ar`;
- combined: sum of the two individually normalized primitive directions, then renormalized.

Both signs are retained.

## Distance solver

For every anchor × axis × sign × target:

1. scan positive scalar distance in fixed 0.05 steps to locate the first declared bracket;
2. solve inside that bracket with deterministic Brent root finding;
3. re-project the final surface to CBD;
4. require absolute RMS distance error ≤ 1e-6.

Targets remain:

- 0.10;
- 0.25;
- 0.50.

They are design-search values, not gates or human effect sizes.

## Boundary

This generator does not freeze:

- bootstrap draw count;
- evaluation replicate count;
- false-rejection/detection gates;
- participant×item human design;
- human N.

It does not authorize recruitment, human-data collection, M0 change or runtime F1b.
