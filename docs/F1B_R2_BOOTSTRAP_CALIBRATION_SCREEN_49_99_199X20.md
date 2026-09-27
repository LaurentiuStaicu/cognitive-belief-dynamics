# F1b R2 Staged Bootstrap Calibration-Specificity Screen

Status: **PREDECLARED / NON-AUTHORITATIVE / NOT YET EXECUTED**

Issue: #154  
Parent: #145  
Baseline main: `8694844a435eef47bd1cd82222d2f485882e1feb`

## Purpose

This stage follows the retained 49×5 pilot.

The pilot established that the bootstrap path executes cleanly and that the selected +0.25 standalone-accuracy departure can produce a strong CBD-restriction response. It also produced one CBD-null rejection and one ADD-specificity rejection among five replicates, which is too little evidence to judge calibration or specificity.

The next stage therefore expands replication and bootstrap draw count while keeping the scientific identity set fixed.

## Frozen design

- participants: 24
- items: 36
- missingness: 0
- fit-scale multiplier: 1×
- bootstrap draws: 49 / 99 / 199
- evaluation replicates: 20 per draw count

### Null identities

1. `CBD_ANCHOR_1` → CBD-complement restriction.
2. `CBD_ANCHOR_2` → CBD-complement restriction.
3. `ADD_ANCHOR` → ADD restriction.

### Single controlled departure

- `CBD_ADD_INTERSECTION_ANCHOR_1`
- `STANDALONE_ACCURACY_MAIN_EFFECT`
- sign `+1`
- nearest-CBD RMS distance `0.25`

The departure is tested independently against:
- CBD-complement restriction;
- ADD restriction.

Total restriction-test trials:

`5 identities × 20 replicates × 3 draw counts = 300`.

## Pre-frozen stage-advancement screen

A bootstrap draw count may advance to a broader **non-authoritative** departure characterization only if all of the following hold:

- zero fit failures;
- zero bootstrap-calibration failures;
- each null identity rejects at most 2/20;
- the ADD-specificity negative control rejects at most 2/20;
- the selected CBD departure rejects at least 16/20.

The rule is evaluated independently at 49, 99 and 199 draws.

If more than one draw count passes, the smallest passing draw count may be used in the next non-authoritative stage for computational economy.

This is not an authoritative draw-count freeze.

## Why 20 replicates

Twenty is the upper value already frozen in the broader design-search grid. This stage moves directly to that predeclared value after the completed five-replicate pilot.

Even 20 replicates are insufficient to prove exact 5% type-I error control. The screen is intended only to detect gross instability and to decide whether the broader departure grid is ready to be explored non-authoritatively.

## Boundary

`bootstrap draw count = DESIGN SEARCH ONLY`

`evaluation replicates = DESIGN SEARCH ONLY`

`false-rejection calibration = NOT VALIDATED`

`detection power = NOT VALIDATED`

`authoritative core grid = NOT FROZEN`

`human N = NOT FROZEN`

`participant recruitment = NOT AUTHORIZED`

`runtime F1b = NOT AUTHORIZED`
