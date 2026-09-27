# F1b R2 KL-Controlled Departure V2 Qualification Result

Status: **DETERMINISTIC QUALIFICATION PASS / NON-AUTHORITATIVE**

Issue: #202  
Scientific source: `63c1784332eb2de22da5d4d1bf47af5f8f2133f8`

## Result

The complete V2 grid qualified deterministically.

Frozen target grid:

- 0.001 mean Bernoulli KL;
- 0.002 mean Bernoulli KL;
- 0.003 mean Bernoulli KL.

All 36 required cases were generated:

- 12 standalone-accuracy cases;
- 12 complement-relation cases;
- 12 combined-violation cases.

No sign, anchor, axis or target was omitted.

## Numerical gate

Maximum target error:

`5.648593572049609e-13`

Frozen tolerance:

`1e-7`

Therefore every generated case satisfies the target-accuracy gate by a wide margin.

There are:

- 33 finite-interior projections;
- 3 closure-limit projections;
- 0 `SCIENTIFIC_DOMAIN_UNRESOLVED` cases.

Standalone ADD compatibility remains exact at numerical precision:

maximum nearest-ADD RMS:

`2.2765964667815184e-16`.

## Closure-limit cases

All three closure-limit cases occur on the complement-minus rays.

1. A1− / target 0.003:
   - boundary: `W1=HIGH`;
   - scalar: `0.2591010650985558`.

2. A2− / target 0.002:
   - boundary: `W1=HIGH`;
   - scalar: `0.23512443721415008`.

3. A2− / target 0.003:
   - boundary: `W1=HIGH`;
   - scalar: `0.2699141039186232`.

Closure-limit status is explicitly allowed by the frozen V2 contract and is not converted into an invented finite parameter vector.

## Complement-plus saturation context

The common V2 grid is reachable on both preserved plus rays, but the upper level is not equally mild in response space.

A1+ / 0.003:
- scalar: `1.121871183813979`;
- generator probability range: approximately 0.0570–0.9172;
- 0 cells outside [0.05, 0.95];
- 3 cells outside [0.10, 0.90].

A2+ / 0.003:
- scalar: `2.6890660270805204`;
- generator probability range: approximately 0.00387–0.99424;
- 6/18 cells outside [0.05, 0.95];
- 6/18 cells outside [0.10, 0.90].

This saturation is retained as design context. It is not a deterministic qualification failure because the target is reached with a finite-interior CBD projection and all frozen numerical gates pass.

It must, however, remain visible in any later stochastic interpretation.

## Per-axis summary

Standalone accuracy:
- 12/12 finite interior;
- 0 closure-limit;
- maximum scalar approximately 0.22873;
- zero generator cells outside [0.05, 0.95].

Complement relation:
- 9/12 finite interior;
- 3 closure-limit;
- maximum scalar approximately 2.68907;
- maximum saturation count: 6/18 cells outside [0.05, 0.95].

Combined violation:
- 12/12 finite interior;
- 0 closure-limit;
- maximum scalar approximately 0.28633;
- zero generator cells outside [0.05, 0.95].

## Per-target summary

At 0.001:
- 12/12 finite interior;
- no closure-limit case.

At 0.002:
- 11 finite interior;
- 1 closure-limit.

At 0.003:
- 10 finite interior;
- 2 closure-limit.

## Cross-version 0.001 check

Exact V1 partition artifacts exist for standalone and combined axes, giving eight directly comparable 0.001 cases.

Across those eight cases:

- attainment changes: 0;
- closure-identity changes: 0;
- maximum scalar change: approximately `1.34e-11`;
- maximum AP-GENERAL coefficient change: approximately `1.89e-11`;
- maximum selected CBD surface-coordinate change: approximately `3.33e-7`.

The V1 complement partitions did not write exact partition artifacts because each partition later failed at an unreachable higher V1 target, so no direct exact-artifact comparison is claimed there.

Historical V1 remains immutable.

## Exact execution provenance

Temporary execution PR: #204  
Actions run: `36336694463`

Combined artifact:
- artifact ID: `10937835482`;
- ZIP SHA-256:
  `87c56a14a045e798d2964471f64d8c59b9ca45b905df484427995a118ef76da8`;
- exact JSON SHA-256:
  `cc0b95f4bba63dc721a864b4dbe53be9c0c8a07071991575ea2a438d410d4ef7`;
- exact JSON size: 33,934,395 bytes.

The exact artifact contains all 36 cases, AP-GENERAL coefficients, selected CBD surfaces, scan/root traces and projection diagnostics.

The repository retains the scientific qualification summary plus exact hashes/provenance rather than duplicating the 33.9 MB artifact.

## Verdict

The deterministic V2 gate passes.

This establishes that the common KL grid:

`0.001 / 0.002 / 0.003`

is constructible across every frozen axis, anchor and sign under the corrected projectors and scalar range.

It does not establish statistical detection power.

## Next gate

The next permitted stage is a separate paired same-dataset bootstrap characterization design.

That future design must be frozen before execution and must ensure:
- bootstrap draw count is excluded from synthetic-dataset RNG identity;
- 49 / 99 / 199 draw settings see exactly the same datasets;
- fit/bootstrap failures remain separate outcomes;
- no authoritative power, human N or recruitment claim is made from a design-search stage.

## Boundary

`V2 DETERMINISTIC QUALIFICATION = PASS`

`V2 GRID = 0.001 / 0.002 / 0.003 MEAN KL`

`V1 = IMMUTABLE HISTORICAL DESIGN`

`STATISTICAL POWER = NOT VALIDATED`

`PAIRED BOOTSTRAP = NOT YET AUTHORIZED`

`AUTHORITATIVE BOOTSTRAP DRAWS / EVALUATION REPLICATES = NOT FROZEN`

`AUTHORITATIVE CORE GRID / HUMAN N = NOT FROZEN`

`PARTICIPANT RECRUITMENT = NOT AUTHORIZED`

`RUNTIME F1B = NOT AUTHORIZED`
