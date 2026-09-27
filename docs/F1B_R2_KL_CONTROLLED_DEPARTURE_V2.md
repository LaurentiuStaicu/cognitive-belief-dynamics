# F1b R2 KL-Controlled Departure Design v2

Status: **IMPLEMENTED CONTRACT / DETERMINISTIC / NOT YET EXECUTED**

Issue: #202  
Baseline: `30f6fdfd0aadfe36b64f4f876c6f6cf43103033b`

## Purpose

Define the second prospectively versioned KL-controlled synthetic departure design after the v1 common target grid was shown to be infeasible on both preserved complement-plus rays.

V2 changes only the frozen common KL target grid.

It does not change:
- the scientific KL definition;
- the structural rays;
- anchors;
- signs;
- scalar range;
- projection domains;
- optimizer tolerances;
- ADD-specificity requirement;
- any stochastic or human-study gate.

## Why v1 is not edited

V1 remains:

`F1B.R2.KL_CONTROLLED_DEPARTURE.V1`

with targets:

`0.001 / 0.005 / 0.010`

The corrected #182 envelope demonstrated:
- A1− and A2− reach all three v1 targets;
- A1+ reaches only 0.001 among the frozen targets, with envelope maximum approximately 0.00396914;
- A2+ reaches only 0.001 among the frozen targets, with envelope maximum approximately 0.00325382.

Therefore v1 is a historically valid failed design experiment.

It is not repaired in place.

## Version

`F1B.R2.KL_CONTROLLED_DEPARTURE.V2`

## Frozen common KL grid

V2 uses:

- 0.001 mean KL;
- 0.002 mean KL;
- 0.003 mean KL.

Units:

`nats per Bernoulli observation under the uniform 18-cell design measure`

These are synthetic design-strength levels.

They are not labels for small, medium or large psychological effects.

## Deterministic rationale

The grid uses only deterministic geometry.

### 0.001

This is the shared V1/V2 reference level.

The corrected envelope shows it is attainable on all four complement rays.

### 0.002

This is a round intermediate information-loss level below both complement-plus envelopes.

### 0.003

This is the round upper level.

The binding corrected complement-plus envelope is A2+:

`0.0032538188153675754`

Therefore:

`0.003 < 0.0032538188153675754`

A1+ has an even higher envelope maximum:

`0.003969141445652382`

No stochastic rejection rate or power calculation enters the target-grid choice.

## Scientific distance

Unchanged:

`D_KL = min_{q in closure(CBD)} mean_j KL(Bern(p_general,j) || Bern(q_j))`

Direction:

`general generator -> CBD restricted response-family closure`

The primary quantity is mean KL.

The design measure remains uniform over the frozen 18 B×A×R cells.

## Structural grid

V2 preserves:

- 2 applicable anchors per axis;
- 3 structural axes;
- both signs;
- 3 KL strengths.

If deterministic qualification succeeds:

`2 × 3 × 2 × 3 = 36 cases`

No sign, anchor or axis can be removed after inspecting results.

## Versioned generator contract

The shared generator now accepts only two explicit contracts:

### V1

- design ID: `F1B.R2.KL_CONTROLLED_DEPARTURE.V1`;
- status: `NON_AUTHORITATIVE_KL_CONTROLLED_DEPARTURE_V1_DESIGN`;
- targets: `0.001 / 0.005 / 0.010`.

### V2

- design ID: `F1B.R2.KL_CONTROLLED_DEPARTURE.V2`;
- status: `NON_AUTHORITATIVE_KL_CONTROLLED_DEPARTURE_V2_DESIGN`;
- targets: `0.001 / 0.002 / 0.003`.

A design ID/status/target mismatch fails closed.

Unknown future versions fail closed.

This preserves V1 semantics while preventing silent target mutation.

## Numerical infrastructure

V2 requires the corrected prospective projectors:

- closure nested-feasible continuation from PR #188;
- finite-logit nested-feasible continuation from PR #196;
- historical regression PASS retained by PR #198.

The frozen nested-objective tolerance remains:

`1e-10`

Projection domains remain:

`8× / 16× / 32×`

## First-crossing solver

Unchanged from V1:

- scalar start: 0;
- scan step: 0.025;
- scalar maximum: 20;
- Brent xtol: 1e-10;
- Brent rtol: 1e-10;
- max iterations: 200;
- first crossing only;
- target error <= 1e-7 mean KL.

If any V2 cell cannot find a first crossing, V2 fails closed.

## ADD specificity

Standalone-accuracy departures continue to use the CBD∩ADD anchors.

Every standalone case must remain ADD-compatible within:

`1e-10 utility RMS`

Failure is a design-generation error.

## Test discipline

The implementation PR does not execute the real 36-case V2 grid.

Tests verify:
- V2 configuration and binding-envelope provenance;
- V2 remains deterministic only;
- V1 still produces V1 partition/result status and its original target grid;
- V2 produces V2 partition/result status and the new target grid;
- target-grid mutation fails closed;
- design/status mismatch and unknown versions fail closed.

The real optimization grid is executed only after this implementation is integrated.

## Next gate

After implementation CI passes and V2 is merged:

1. execute six independent axis×anchor deterministic partitions;
2. require 6 cases per partition;
3. combine only exact 36/36 coverage;
4. retain the exact combined JSON artifact;
5. audit:
   - target error;
   - closure-limit status;
   - saturation;
   - ADD specificity;
   - cross-version 0.001 behavior.

Only a passing deterministic V2 result may unlock a separate paired-bootstrap design issue.

## Boundary

`V2 GRID = 0.001 / 0.002 / 0.003 MEAN KL`

`V2 IMPLEMENTATION = NO REAL 36-CASE EXECUTION YET`

`V1 = IMMUTABLE`

`D3 / RAYS / ANCHORS / SIGNS / SCALAR RANGE = UNCHANGED`

`STOCHASTIC CHARACTERIZATION = NOT AUTHORIZED`

`PAIRED BOOTSTRAP = NOT AUTHORIZED`

`AUTHORITATIVE DRAWS / POWER / CORE GRID / HUMAN N = NOT FROZEN`

`PARTICIPANT RECRUITMENT = NOT AUTHORIZED`

`RUNTIME F1B = NOT AUTHORIZED`
