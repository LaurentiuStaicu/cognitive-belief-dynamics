# F1b R2 Complement KL Attainable-Envelope Result

Status: **COMPLETED / DETERMINISTIC / V1 COMMON TARGET GRID INFEASIBLE**

Issue: #182  
Corrected scientific source: `54b6e6d0307ee91960dd80fec0d3f008a3a3d806`  
Temporary execution PR: #200  
Actions run: `36335130114`

## Purpose

Complete the deterministic attainable-envelope diagnostic that was frozen after KL-controlled departure v1 failed on the complement axis.

The scientific definition is unchanged:

`D_KL = min_{q in closure(CBD)} mean_j KL(Bern(p_general,j) || Bern(q_j))`

with:
- direction general → CBD;
- uniform 18-cell design measure;
- the frozen complement structural ray;
- the same two CBD anchors;
- both signs;
- scalar range 0…20;
- scalar step 0.025;
- the corrected nested-feasible finite-logit and closure projectors validated by #190.

No target, ray, scalar range, scientific domain or numerical tolerance was changed for this execution.

## Exact execution

Coverage:
- 4/4 rays;
- 801 points per ray;
- 3,204 deterministic projections total;
- zero `SCIENTIFIC_DOMAIN_UNRESOLVED` points;
- standard CBD validation green.

Combined artifact:
- artifact ID: `10936214205`;
- ZIP SHA-256: `407fb0e37f302eec97076737243097882cfad92c8dc290054e2119d93bda17ec`;
- exact JSON SHA-256: `6885f32de25bc6838380d6acc9d7c7f2cda02736104dca4717fe8da7b1c733c6`;
- exact JSON size: 3,267,049 bytes.

Per-ray exact JSON SHA-256:
- A1−: `a8528871e23e733e653b8a8c803c1d8f5ec5aad6cd88753cc719a32b493ef448`;
- A1+: `49081232b6c0bc75805c887f1632df595c3122e4bcbc7598da24d76928c1bd5d`;
- A2−: `2853b36571cfa0ba5b1512a121fdf52a64192da08704cdb1b35e4e3d0afcee3e`;
- A2+: `f4e47d915eb9a8ee1a62c0f037c8a2466aeedd00708d8d302ca46e36c3362712`.

## Ray results

| Ray | Maximum mean KL | Scalar at maximum | First closure scalar | 0.001 | 0.005 | 0.010 |
|---|---:|---:|---:|---|---|---|
| A1− | 0.0144397924 | 0.475 | 0.225 | attainable | attainable | attainable |
| A1+ | 0.00396914145 | 19.175 | none | attainable | above envelope | above envelope |
| A2− | 0.0164245495 | 0.500 | 0.200 | attainable | attainable | attainable |
| A2+ | 0.00325381882 | 17.375 | none | attainable | above envelope | above envelope |

All four profiles are non-monotone on the frozen discrete grid.

### A1−

Attainment:
- finite interior: 9/801;
- closure limit: 792/801;
- first closure scalar: 0.225.

First target brackets:
- 0.001 → [0.150, 0.175];
- 0.005 → [0.300, 0.325];
- 0.010 → [0.400, 0.425].

The ray reaches all three frozen v1 targets.

### A2−

Attainment:
- finite interior: 8/801;
- closure limit: 793/801;
- first closure scalar: 0.200.

First target brackets:
- 0.001 → [0.175, 0.200];
- 0.005 → [0.300, 0.325];
- 0.010 → [0.400, 0.425].

The ray reaches all three frozen v1 targets.

### A1+

All 801 points are finite-interior.

Maximum mean KL is approximately:

`0.00396914145`

Therefore:
- 0.001 is attainable;
- 0.005 is above the frozen [0,20] envelope;
- 0.010 is above the frozen [0,20] envelope.

### A2+

All 801 points are finite-interior.

Maximum mean KL is approximately:

`0.00325381882`

Therefore:
- 0.001 is attainable;
- 0.005 is above the frozen [0,20] envelope;
- 0.010 is above the frozen [0,20] envelope.

This is the binding complement-plus envelope among the four preserved rays.

## What the corrected run changes about the original failure

The first KL v1 deterministic execution failed on both complement partitions with:

`no first positive KL target crossing within declared scalar range`

The corrected envelope shows that this statement was not scientifically correct for the minus rays.

After enforcing nested-feasible continuation:
- A1− reaches 0.001, 0.005 and 0.010;
- A2− reaches 0.001, 0.005 and 0.010.

The original minus failure was therefore a numerical optimization-integrity problem.

The true structural infeasibility lies on the preserved plus rays:
- A1+ maximum < 0.005;
- A2+ maximum < 0.005.

## Consequence for KL-controlled departure v1

The common v1 target grid:

`0.001 / 0.005 / 0.010`

cannot be generated for all preserved complement anchor×sign rays within the frozen structural rays and scalar range.

Among the three frozen v1 targets, only:

`0.001`

is attainable on all four complement rays.

This does not authorize replacing the target grid inside v1.

The v1 result remains a failed prospective design, with its original settings preserved.

## Required next gate

A separate prospective deterministic gate may define a revised common KL target grid.

That redesign must:
- use deterministic geometry only;
- preserve both complement signs and both anchors;
- not use stochastic rejection/power results;
- not widen scalar 20 retrospectively;
- not change the complement ray retrospectively;
- freeze the new target grid before any new stochastic characterization.

The other structural axes must also be respected when validating the new common grid.

## Boundary

`COMPLEMENT KL ENVELOPE = COMPLETED`

`ORIGINAL MINUS FAILURE = NUMERICAL, NOW RESOLVED`

`V1 COMMON TARGET GRID = STRUCTURALLY INFEASIBLE ON PLUS COMPLEMENT RAYS`

`V1 TARGET GRID = NOT REVISED BY THIS RESULT`

`NEW COMMON KL TARGET GRID = REQUIRES SEPARATE PROSPECTIVE GATE`

`STOCHASTIC CHARACTERIZATION = NOT AUTHORIZED`

`PAIRED BOOTSTRAP = NOT AUTHORIZED`

`AUTHORITATIVE POWER / CORE GRID / HUMAN N = NOT FROZEN`

`PARTICIPANT RECRUITMENT = NOT AUTHORIZED`

`RUNTIME F1B = NOT AUTHORIZED`
