# F1b R2 Nearest-CBD Projection-Bound Sensitivity — Result

Status: **COMPLETED / NON-AUTHORITATIVE DETERMINISTIC DIAGNOSTIC**

Issue: #167  
Scientific source: `2ed9685b4a0f952a5c4c501116eb3f2e1e16c6e9`  
Execution run: `36321330611`  
Temporary execution PR: #169

## Execution integrity

The frozen diagnostic completed successfully.

- fixed retained complement cases: 12;
- nested projection bound sets: 4;
- case-bound projections: 48;
- common deterministic starts per projection: 8;
- optimizer starts total: 384;
- successful starts: 384;
- failed starts: 0;
- nested-objective checks: passed.

Exact execution result:
- Actions artifact: `10932059775`;
- artifact ZIP SHA-256: `63f1c4f1c170ed85a90e48e8ead56a4ec24079a4219d8c3faa3004ef3a7c47f0`;
- exact JSON SHA-256: `ea8584a1edb3a80ed8751aa1dd6ea504817204cd4d11ebc34a9f42f6d327b55a`.

The full 384-start result is deterministically reconstructible from the integrated audit engine and retained input surfaces.

## Boundary activity

| Bound set | Cases with selected solution on a bound |
|---|---:|
| CURRENT_1X | 9/12 |
| WIDE_2X | 9/12 |
| WIDE_4X | 1/12 |
| WIDE_8X | 0/12 |

WIDE_4X → WIDE_8X is effectively stable for the retained cases.

- 9/12 cases have zero nearest-CBD RMS change;
- the largest absolute change is approximately `1.07e-6`;
- no selected WIDE_8X projection is boundary-active.

Thus the widened diagnostic projection has reached a practically stable region for this case set.

## Current-bound dependence

The current AP-A computational bounds materially affect the nearest-CBD distances used to construct/interpret the medium and large complement departures.

| Anchor | Sign | Nominal RMS | CURRENT_1X | WIDE_8X |
|---|---:|---:|---:|---:|
| A1 | − | 0.10 | 0.1000 | 0.1000 |
| A1 | + | 0.10 | 0.1000 | 0.1000 |
| A1 | − | 0.25 | 0.2500 | 0.2478 |
| A1 | + | 0.25 | 0.2500 | 0.1785 |
| A1 | − | 0.50 | 0.5000 | 0.3174 |
| A1 | + | 0.50 | 0.5000 | 0.1811 |
| A2 | − | 0.10 | 0.1000 | 0.0995 |
| A2 | + | 0.10 | 0.1000 | 0.1000 |
| A2 | − | 0.25 | 0.2500 | 0.2471 |
| A2 | + | 0.25 | 0.2500 | 0.1624 |
| A2 | − | 0.50 | 0.5000 | 0.3367 |
| A2 | + | 0.50 | 0.5000 | 0.1651 |

The largest change occurs for A2 / plus / nominal RMS 0.50:

`0.5000 → 0.1651`

approximately a 67% reduction in distance to the widened CBD surface.

This is too large to treat the current bounded distance as merely a numerically convenient representation of an otherwise unchanged scientific distance.

## Sign geometry after bound expansion

The bound audit does not remove the sign asymmetry.

At WIDE_8X, plus/minus probability-RMS ratios are:

| Anchor | Nominal RMS | Probability RMS +/− | Mean KL +/− | Information distance +/− |
|---|---:|---:|---:|---:|
| A1 | 0.10 | 0.940 | 0.932 | 0.974 |
| A1 | 0.25 | 0.688 | 0.494 | 0.700 |
| A1 | 0.50 | 0.542 | 0.308 | 0.557 |
| A2 | 0.10 | 0.936 | 0.930 | 0.973 |
| A2 | 0.25 | 0.625 | 0.409 | 0.635 |
| A2 | 0.50 | 0.463 | 0.226 | 0.476 |

Therefore two findings coexist:

1. the inherited AP-A computational bounds materially distort the nominal medium/large nearest-CBD distance;
2. substantial plus/minus probability/information asymmetry remains even after the projection is no longer boundary-active.

The Stage A asymmetry was therefore not a pure optimizer-bound artifact, but the original nominal utility-RMS distance was also not bound-invariant.

## Consequence

The routing condition from #167 is the mixed/material-bound-dependence case.

Do **not** proceed directly to paired 49/99/199 bootstrap characterization.

The next gate must clarify the scientific definition of nearest-CBD distance independently of the operational fitter bounds.

Questions that must be resolved prospectively include:

- whether the scientific CBD manifold is intended to be bounded at all;
- whether computational bounds should be excluded from the geometry definition and retained only for fitting;
- whether departure strength should continue to be defined by utility RMS to an effectively unconstrained CBD surface;
- whether probability/information geometry should remain diagnostic or become part of the design-strength definition;
- how to preserve comparability of the already-retained #158 results without rewriting them retrospectively.

No prior result is invalidated or rewritten. The audit explains a limitation of the distance definition used in that characterization.

## Boundary

`PROJECTION-BOUND SENSITIVITY = COMPLETE`

`CURRENT BOUNDED DISTANCE = MATERIALLY BOUND-DEPENDENT`

`WIDE PROJECTION = STABLE FOR RETAINED CASES`

`INTRINSIC SIGN ASYMMETRY = STILL PRESENT`

`OPERATIONAL FITTER BOUNDS = UNCHANGED`

`PAIRED BOOTSTRAP = NOT YET AUTHORIZED`

`49 DRAWS = NOT AUTHORITATIVELY FROZEN`

`20 REPLICATES = NOT AUTHORITATIVELY FROZEN`

`AUTHORITATIVE POWER = NOT VALIDATED`

`AUTHORITATIVE CORE GRID = NOT FROZEN`

`HUMAN N = NOT FROZEN`

`PARTICIPANT RECRUITMENT = NOT AUTHORIZED`

`RUNTIME F1B = NOT AUTHORIZED`
