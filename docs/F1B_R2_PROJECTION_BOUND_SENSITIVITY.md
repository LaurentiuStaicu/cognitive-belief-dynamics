# F1b R2 Nearest-CBD Projection-Bound Sensitivity Audit

Status: **FROZEN / NOT EXECUTED / DETERMINISTIC / NON-AUTHORITATIVE**

Issue: #167  
Baseline: `fe53de630a669a41c58d7bb685935b204599be75`

## Purpose

Stage A of the complement-sign diagnostic showed two effects:

1. equal utility-RMS departures are not equally separated on probability/KL/information scales;
2. 9 of the 12 current nearest-CBD projections are active on inherited AP-A parameter bounds.

Before any paired bootstrap stage, this audit isolates the second effect.

## Scientific objects are fixed

The audit uses the exact 12 retained complement cases from the Stage A result.

The six AP-GENERAL coefficients are fixed inputs.

The audit does not:
- regenerate departure scalar steps;
- change the controlled-departure generator;
- change the operational AP-A fitter;
- generate stochastic data;
- fit participant/item models;
- run bootstrap tests.

## Diagnostic bound grid

The same fixed general surface is reprojected under four nested bound sets:

| Bound set | sharing bias | baseline logit | beta accuracy | beta reward |
|---|---|---|---|---|
| CURRENT_1X | [-5,5] | [-4,4] | [-5,5] | [-5,5] |
| WIDE_2X | [-10,10] | [-8,8] | [-10,10] | [-10,10] |
| WIDE_4X | [-20,20] | [-16,16] | [-20,20] | [-20,20] |
| WIDE_8X | [-40,40] | [-32,32] | [-40,40] | [-40,40] |

These are sensitivity bounds only, not proposed fitter settings.

## Common deterministic start set

Every case × bound set uses:
- the seven starts already frozen in the controlled-departure design;
- the retained CURRENT_1X nearest-CBD parameters for that case.

The retained solution is included for every bound set, including CURRENT_1X, so the widened projections do not receive a privileged start.

All start outcomes are retained.

## Integrity checks

Because the feasible sets are nested, the best squared-error objective must not increase as bounds widen, within numerical tolerance `1e-10`.

The CURRENT_1X projection must reproduce the retained Stage A current projection to numerical precision.

Bound activity is recorded at absolute parameter tolerance `1e-5`.

## Metrics

For every case × bound set retain:
- selected nearest-CBD parameters;
- nearest-CBD utility RMS;
- objective;
- selected start;
- active bounds;
- successful / failed starts;
- parameter displacement from CURRENT_1X;
- probability RMS;
- absolute probability separation;
- Bernoulli KL;
- information-weighted logit distance;
- nearest-CBD probability range;
- nearest-CBD Bernoulli variance.

For every transition 1×→2×→4×→8× retain absolute and relative RMS changes.

For every anchor × requested RMS × bound set retain plus/minus contrasts.

## Interpretation

The audit does not choose an authoritative bound set.

It determines whether the Stage A sign asymmetry is:
- stable after expansion;
- materially dependent on the inherited computational bounds; or
- still unresolved because even the widest diagnostic projection remains boundary-active/non-stable.

Only after this result is retained may a paired same-dataset bootstrap stage be designed.

## Boundary

`DETERMINISTIC PROJECTION SENSITIVITY ONLY`

`ORIGINAL GENERAL SURFACES = UNCHANGED`

`OPERATIONAL FITTER BOUNDS = UNCHANGED`

`PAIRED BOOTSTRAP = NOT AUTHORIZED`

`AUTHORITATIVE BOOTSTRAP DRAWS = NOT FROZEN`

`AUTHORITATIVE EVALUATION REPLICATES = NOT FROZEN`

`AUTHORITATIVE CORE GRID = NOT FROZEN`

`HUMAN N = NOT FROZEN`

`PARTICIPANT RECRUITMENT = NOT AUTHORIZED`

`RUNTIME F1B = NOT AUTHORIZED`
