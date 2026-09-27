# F1b R2 KL-Controlled Departure Design v1

Status: **IMPLEMENTED / DETERMINISTIC / NOT YET EXECUTED**

Issue: #178  
Scientific distance decision: PR #177  
Implementation baseline: `dc36599e3060081a70c941dc523cd265bb6ec697`

## Purpose

Implement the first prospectively versioned R2 departure generator whose strength is defined by directed Bernoulli information loss rather than historical bounded utility-RMS distance.

The scientific distance is:

`D_KL = min_{q in closure(CBD)} mean_j KL(Bern(p_general,j) || Bern(q_j))`

with direction:

`general generator -> CBD restricted response family`.

The design measure is the frozen uniform 18-cell B×A×R grid.

## Version

`F1B.R2.KL_CONTROLLED_DEPARTURE.V1`

Historical #158 departures remain historical and are not regenerated or relabeled.

## Structural rays

The structural perturbation rays are intentionally preserved:

- standalone accuracy main effect;
- complement-relation violation;
- combined violation.

Their historical utility-RMS normalization is used only to define ray direction and mixture.

It no longer defines departure strength.

## KL target grid

Frozen before execution:

- 0.001 mean KL;
- 0.005 mean KL;
- 0.010 mean KL.

Units are nats per Bernoulli observation under the uniform 18-cell design measure.

The grid was chosen from the deterministic D3 geometry reviewed in #171, not from historical rejection rates.

## Scientific projection

The generator calls the same closure projection engine already audited in #171.

CBD response surfaces use:

`(sharing_bias, W0, W1, beta_reward)`

with:

`W0,W1 in [0,1]`.

Projection retains the nested scientific domains:

- 8×;
- 16×;
- 32×.

For each scalar evaluation the engine retains:
- every optimizer start;
- success/failure;
- selected response surface;
- objective;
- active closure/scientific-domain boundaries;
- D1/D2/D3/Fisher diagnostics.

A `SCIENTIFIC_DOMAIN_UNRESOLVED` projection fails closed.

A `NON_ATTAINED_OR_CLOSURE_LIMIT` projection is allowed but remains explicit.

Operational AP-A fitter bounds are unchanged.

## Root solving

For each anchor × axis × sign × target:

1. evaluate the anchor at scalar 0;
2. scan the positive scalar ray in increments of 0.025;
3. select the first interval crossing the KL target;
4. solve inside that bracket with Brent's method;
5. require achieved mean-KL error <= 1e-7.

Frozen numerical settings:

- scan step: 0.025;
- max scalar: 20;
- xtol: 1e-10;
- rtol: 1e-10;
- max iterations: 200.

The complete scan and root traces are retained in the execution result.

## Generated grid

If deterministic qualification succeeds:

- standalone: 12 cases;
- complement: 12 cases;
- combined: 12 cases;
- total: 36 cases.

Every case retains both signs and both applicable anchors.

## Diagnostics

At the KL-selected projection each case retains:

- achieved mean KL;
- selected CBD closure surface;
- attainment status;
- utility RMS;
- probability RMS;
- sqrt(2×mean KL);
- local information-weighted logit distance;
- nearest ADD RMS;
- probability extrema;
- saturation counts.

D1 and D2 are additionally re-projected independently at the final generator surface so their nearest-distance diagnostics remain comparable with #171.

## ADD specificity

Standalone-accuracy cases continue to use the CBD∩ADD anchors.

They must remain exactly ADD-compatible within the retained `1e-10` utility-RMS tolerance.

Failure is a design-generation error.

## Test discipline

The implementation PR does not generate the 36-case result.

Tests cover:

- the frozen config/boundary;
- a CBD anchor projecting to approximately zero KL;
- preservation of structural rays;
- exact standalone ADD compatibility;
- a synthetic known-answer first-crossing root solve.

The full deterministic grid is executed only after this implementation is integrated.

## Next gate

After this implementation passes CI and is merged:

1. execute all 36 deterministic KL cases;
2. retain the exact artifact and compact scientific result;
3. audit target attainment, closure cases, saturation and ADD specificity;
4. only if the deterministic design qualifies may a separate paired same-dataset bootstrap design be frozen.

## Boundary

`KL GENERATOR V1 = IMPLEMENTED / NOT YET EXECUTED`

`STOCHASTIC SIMULATION = NOT AUTHORIZED`

`PAIRED BOOTSTRAP = NOT AUTHORIZED`

`AUTHORITATIVE DRAWS / EVALUATION COUNT / POWER = NOT FROZEN`

`AUTHORITATIVE CORE GRID = NOT FROZEN`

`HUMAN N = NOT FROZEN`

`PARTICIPANT RECRUITMENT = NOT AUTHORIZED`

`RUNTIME F1B = NOT AUTHORIZED`
