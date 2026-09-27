# F1b R2 Complement KL Attainable-Envelope Diagnostic

Status: **IMPLEMENTED / DETERMINISTIC / NOT YET EXECUTED**

Issue: #182  
Baseline: `5f789b80c24ee12fa7d1880e6975f0b3953a3bb1`

## Why this diagnostic exists

The first deterministic execution of KL-controlled departure v1 failed for both complement-relation anchor partitions.

The failure was the frozen v1 guard:

`no first positive KL target crossing within declared scalar range`

The scalar range, structural ray and target grid are not changed here.

This diagnostic characterizes the envelope of the design that actually failed before any prospective redesign decision.

## Frozen scientific geometry

Distance remains directed mean Bernoulli KL:

`general generator -> CBD response-family closure`.

The diagnostic reuses:
- the same 18-cell uniform design measure;
- the same complement structural direction;
- the same CBD anchors;
- both signs;
- the same audited closure projector;
- the same 8× / 16× / 32× scientific domains.

## Frozen scalar profile

Each of the four rays is evaluated at:

`0, 0.025, 0.050, ..., 20.000`

for exactly 801 points.

Total complete diagnostic:

`4 × 801 = 3204` deterministic projections.

No scalar range or grid density is changed after observing the result.

## Per-point retention

Each point retains compactly:
- scalar;
- mean KL;
- finite-interior / closure-limit status;
- closure components;
- scientific-domain components;
- selected CBD response coordinates;
- utility RMS diagnostic;
- probability RMS diagnostic;
- local Fisher/information-weighted logit diagnostic;
- probability extrema;
- generator saturation counts.

The complete per-start optimizer payload is not duplicated at every point. It is reconstructible from the integrated #171 projection engine, exact input configs and source commit.

Any `SCIENTIFIC_DOMAIN_UNRESOLVED` point fails the diagnostic.

## Target classification

The original v1 targets remain:

- 0.001;
- 0.005;
- 0.010 mean KL.

For each ray, the diagnostic reports the first discrete 0.025 bracket when it exists.

If no crossing exists it retains:
- maximum observed mean KL;
- scalar of the maximum;
- terminal mean KL at scalar 20;
- whether the profile falls after its maximum.

No new root is solved here.

## Non-monotonicity

The diagnostic retains:
- monotone-nondecreasing flag;
- discrete direction-reversal count;
- reversal locations;
- first closure-limit scalar;
- attainment-state counts.

This prevents a target-grid redesign from assuming that departure strength grows monotonically along a structural coefficient ray.

## Execution partitioning

The four rays are independent deterministic partitions:

- A1 / minus;
- A1 / plus;
- A2 / minus;
- A2 / plus.

A fail-closed combiner requires all four 801-point profiles and exact source/config provenance.

## Decision boundary

This implementation does not revise v1.

After execution, a separate prospective decision may revise the common KL target grid only from deterministic envelope geometry.

It may not:
- keep only the easier sign;
- widen scalar 20 retrospectively;
- change the complement ray retrospectively;
- use stochastic rejection rates to choose targets.

## Boundary

`D3 = UNCHANGED`

`V1 TARGETS = DIAGNOSED ONLY`

`SCALAR RANGE = UNCHANGED`

`STOCHASTIC CHARACTERIZATION = NOT AUTHORIZED`

`PAIRED BOOTSTRAP = NOT AUTHORIZED`

`AUTHORITATIVE POWER / CORE GRID / HUMAN N = NOT FROZEN`

`PARTICIPANT RECRUITMENT = NOT AUTHORIZED`

`RUNTIME F1B = NOT AUTHORIZED`
