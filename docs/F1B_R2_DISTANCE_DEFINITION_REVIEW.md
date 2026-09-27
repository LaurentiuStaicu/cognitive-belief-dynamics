# F1b R2 Scientific Nearest-CBD Distance Definition Review

Status: **FROZEN / NOT EXECUTED / DETERMINISTIC / NON-AUTHORITATIVE**

Issue: #171  
Baseline: `895b62e61483043c5c9eb6824c7deac1971fb14f`

## Purpose

Review the scientific definition of distance from a fixed AP-GENERAL response surface to the CBD-restricted family before any paired bootstrap or human-N gate.

The review was required because the retained bound-sensitivity audit established that the original bounded utility-RMS construction is materially affected by inherited AP-A computational bounds, while substantial plus/minus geometry asymmetry remains even after the projection is stabilized.

## Frozen targets

Use exactly the 12 retained complement-relation general surfaces from:

`model/results/f1b_r2_complement_sign_geometry_case_summary_2026-09-27.tsv`

Their six AP-GENERAL coefficients are fixed.

Do not regenerate their historical departure scalar steps and do not rewrite their historical nominal 0.10 / 0.25 / 0.50 labels.

## Design measure

All distances in this review use the same explicit measure:

- the frozen 18 B×A×R cells;
- uniform weight = 1/18 per cell.

Distance is therefore explicitly conditional on this synthetic design measure.

## Candidate definitions

### D1 — stabilized utility/logit RMS

Minimize mean squared utility/logit difference to the CBD family and report its square root.

This continues the original scientific concept but removes the operational 1× fitter box from the intended distance definition.

### D2 — probability RMS

Transform both surfaces through the logistic link, minimize mean squared probability difference and report its square root.

The CBD parameters are re-optimized under this objective; probability RMS is not merely evaluated at the utility-RMS projection.

### D3 — directed Bernoulli KL information projection

Minimize the uniform-cell mean:

`KL(Bern(p_general) || Bern(p_CBD))`.

The direction is fixed prospectively because it measures expected Bernoulli log-loss when the CBD family approximates the declared general generator.

The review also reports `sqrt(2 × mean KL)` only as a scale diagnostic.

### Local Fisher/information distance

The existing information-weighted logit distance is retained as a local diagnostic, not promoted to a fourth global candidate.

## Optimization protocol

Every fixed surface and candidate uses the same nine deterministic starts:

- the seven original CBD projection starts;
- the retained current 1× nearest-CBD solution;
- the reconstructed WIDE_8X solution from the retained bound-sensitivity engine.

Every candidate is optimized independently on nested diagnostic domains:

- 8×;
- 16×;
- 32×.

The engine retains every start result, the selected surface, active bounds and objective changes as the diagnostic domain expands.

A widening-domain objective may not increase beyond numerical tolerance.

No candidate becomes scientifically preferred merely because it is easier to optimize.

## Stable KL evaluation

The Bernoulli KL objective is evaluated from probabilities for the fixed generator and log-probabilities derived stably from the CBD logits.

This avoids turning arbitrary probability clipping into part of the distance definition.

## Required outputs

For every case × candidate:

- selected CBD parameters;
- objective and primary distance;
- utility RMS;
- probability RMS;
- mean/max Bernoulli KL;
- local information-weighted logit distance;
- probability extrema;
- domain stability;
- active bounds;
- all optimizer starts.

The selected widest-domain solutions also retain all 18 cellwise utility/probability/KL residuals.

For every fixed surface the review reports pairwise probability-RMS differences among the three selected CBD projections.

For every anchor × historical nominal distance it reports both signs under every candidate without treating symmetry as a validity requirement.

## Decision discipline

The deterministic comparison does not itself select a metric.

A later scientific decision may use:

- relation to the Bernoulli observation model;
- parameterization invariance;
- independence from arbitrary operational fitter bounds;
- numerical existence/stability;
- explicit design weighting;
- behavior under saturation;
- suitability for controlled departures from a restricted response family.

It may not use:

- historical #158 bootstrap power;
- monotonicity of historical rejection rates;
- smaller historical plus/minus asymmetry;
- computational convenience;
- preservation of old coefficients for its own sake.

## Literature basis

The review is consistent with the distinction in information geometry between a statistical manifold, divergences such as KL, and the local Fisher metric. It also uses the misspecification interpretation in which a restricted likelihood family approximates a generator through an information projection.

These foundations motivate the candidates; they do not pre-select the CBD distance.

## Historical boundary

All previously retained results keep their original meanings.

In particular, #158 remains a characterization of the bounded utility-RMS design that was actually frozen and executed. #163/#166 and #167/#170 remain diagnostics of that historical design.

If a different distance is later adopted, it starts a new prospectively versioned departure design.

## Boundary

`DISTANCE-DEFINITION REVIEW = DETERMINISTIC ONLY`

`METRIC SELECTION = NOT AUTHORIZED BY THIS IMPLEMENTATION PR`

`OPERATIONAL FITTER BOUNDS = UNCHANGED`

`PAIRED BOOTSTRAP = NOT AUTHORIZED`

`AUTHORITATIVE BOOTSTRAP DRAWS = NOT FROZEN`

`AUTHORITATIVE EVALUATION REPLICATES = NOT FROZEN`

`AUTHORITATIVE POWER = NOT VALIDATED`

`AUTHORITATIVE CORE GRID = NOT FROZEN`

`HUMAN N = NOT FROZEN`

`PARTICIPANT RECRUITMENT = NOT AUTHORIZED`

`RUNTIME F1B = NOT AUTHORIZED`
