# F1b R2 Complement-Relation Sign Geometry Diagnostic

Status: **FROZEN / NOT EXECUTED / NON-AUTHORITATIVE**

Issue: #163  
Baseline: `b4ab87583aa47ecefe87e840063c970fa8997310`

## Question

Does the plus/minus detection asymmetry observed for the complement-relation departure already exist in deterministic probability/information geometry, before any stochastic data generation, mixed-effects fitting or bootstrap calibration?

## Frozen cases

Use exactly:

- CBD_ANCHOR_1 and CBD_ANCHOR_2;
- COMPLEMENT_RELATION_VIOLATION only;
- both signs;
- nearest-CBD utility RMS 0.10 / 0.25 / 0.50.

Total: 12 cases × 18 B×A×R cells.

## Diagnostics

Retain the original utility geometry and compute, without simulation:

- probability-scale RMS distance after the logistic transform;
- mean/max absolute probability difference;
- mean/max Bernoulli KL from general to nearest CBD;
- Bernoulli variance / saturation diagnostics;
- local information-weighted logit distance;
- cellwise utility/probability/KL values.

Compare plus versus minus within each anchor and requested RMS on the prospectively declared metrics.

## Decision boundary

Stage A does not select a sign and does not change the departure definition.

If deterministic probability/KL/information geometry is already strongly asymmetric, the next stochastic stage must account for that structural asymmetry.

If geometry is approximately symmetric, the next stage should prioritize paired same-dataset bootstrap-draw stability and fitter/penalty sensitivity.

Stage B is not frozen by this document.

## Prohibitions

- no stochastic dataset generation;
- no model fitting;
- no paired-bootstrap execution;
- no authoritative bootstrap setting;
- no core-grid or human-N freeze;
- no recruitment;
- no runtime F1b change.
