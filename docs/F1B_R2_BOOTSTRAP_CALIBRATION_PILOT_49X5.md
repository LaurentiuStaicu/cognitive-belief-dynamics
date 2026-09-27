# F1b R2 Bootstrap Calibration Pilot — 49×5

Status: **PREDECLARED / NON-AUTHORITATIVE / NOT YET EXECUTED**

Issue: #150  
Parent: #145  
Baseline main: `59c99f8c1cf2294c9d246a82075f9f2f5b6712da`

## Purpose

Freeze the exact first low-cost pilot for the integrated R2 structural-restriction bootstrap engine before any pilot result is observed.

The pilot is not a power study and does not estimate a 5% false-rejection rate precisely.

## Frozen execution

- participants: 24
- items: 36
- missingness: 0
- fit-scale multiplier: 1×
- bootstrap draws: 49
- evaluation replicates: 5
- seed: 20260927

### Null identities

1. `CBD_ANCHOR_1` tested against the CBD-complement restriction.
2. `CBD_ANCHOR_2` tested against the CBD-complement restriction.
3. `ADD_ANCHOR` tested against the ADD restriction.

### Controlled departure

- anchor: `CBD_ADD_INTERSECTION_ANCHOR_1`
- axis: `STANDALONE_ACCURACY_MAIN_EFFECT`
- sign: `+1`
- nearest-CBD RMS target: `0.25`

The same departure is tested independently against:

- CBD-complement restriction — basic departure-response diagnostic;
- ADD restriction — specificity negative control.

Thus each evaluation replicate contains five restriction tests and the full pilot contains exactly 25 trials.

## Questions the pilot may answer

The result may identify:

- bootstrap execution/calibration failures;
- gross null false-rejection pathology;
- gross ADD-specificity failure;
- obvious absence of CBD response at the selected 0.25 departure;
- approximate computational feasibility.

## Questions the pilot may not answer

Five evaluation replicates are too few to establish:

- calibrated 5% false-rejection control;
- detection power;
- superiority of 49 versus 99 or 199 draws;
- adequacy across axes, signs, or departure distances;
- an authoritative evaluation-replicate count;
- a core/stress grid;
- a human sample size.

## Scientific boundary

`49 bootstrap draws = PILOT VALUE ONLY`

`5 evaluation replicates = PILOT VALUE ONLY`

`authoritative core grid = NOT FROZEN`

`human N = NOT FROZEN`

`participant recruitment = NOT AUTHORIZED`

`runtime F1b = NOT AUTHORIZED`
