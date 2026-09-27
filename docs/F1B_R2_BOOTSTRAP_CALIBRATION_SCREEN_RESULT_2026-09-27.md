# F1b R2 Staged Bootstrap Calibration-Specificity Screen — Result

Status: **COMPLETED / NON-AUTHORITATIVE DESIGN SEARCH**

Issue: #154  
Parent: #145  
Scientific source: `9206c8e96adc10818d20bff93a290daf0392fe92`  
Execution run: `36300108050`

## Purpose

Execute the prospectively frozen 49 / 99 / 199 bootstrap-draw screen with 20 evaluation replicates per draw count before expanding the R2 controlled-departure grid.

The screen retains the same three null identities and the same single `+0.25` standalone-accuracy departure used by the preceding pilot. It is a design-search gate only.

## Execution integrity

- participants: 24;
- items: 36;
- missingness: 0;
- fit-scale multiplier: 1×;
- evaluation replicates: 20 per draw count;
- bootstrap draws: 49 / 99 / 199;
- total restriction tests: 300;
- fit failures: 0;
- bootstrap-calibration failures: 0;
- bootstrap-fit failures: 0.

The temporary execution workflow partitioned the frozen screen by bootstrap draw count only. This does not change the scientific cells because the retained characterization engine keys its evaluation and bootstrap random streams explicitly by draw count and evaluation replicate. The temporary workflow PR is not part of the scientific implementation and must not be merged.

## Predeclared advancement rule

A draw count passes only if all of the following hold:

1. zero fit failures;
2. zero bootstrap-calibration failures;
3. every null identity rejects at most 2/20;
4. the ADD-specificity negative control rejects at most 2/20;
5. the retained `+0.25` CBD departure rejects at least 16/20.

## Result

| Bootstrap draws | CBD null A1 | CBD null A2 | ADD null | ADD specificity | CBD departure | Verdict |
|---:|---:|---:|---:|---:|---:|---|
| 49 | 1/20 | 0/20 | 1/20 | 1/20 | 16/20 | PASS |
| 99 | 1/20 | 1/20 | 1/20 | 3/20 | 14/20 | FAIL |
| 199 | 0/20 | 2/20 | 1/20 | 1/20 | 13/20 | FAIL |

The 49-draw cell therefore passes the prospectively frozen stage-advancement screen. The 99-draw cell fails both the specificity and CBD-departure thresholds. The 199-draw cell fails the CBD-departure threshold.

For 49 draws, the retained CBD-departure rejection rate is 0.80 with Wilson 95% interval approximately `[0.584, 0.919]`. The three null/specificity rejection rates are 0.05, 0.00, 0.05 and 0.05 respectively, with wide intervals because each cell contains only 20 evaluation replicates.

## Interpretation

This result does **not** show that 49 bootstrap draws are statistically superior to 99 or 199. The evaluation datasets are independently seeded by draw count, so the non-monotone 0.80 / 0.70 / 0.65 CBD-departure rates contain evaluation Monte Carlo variation as well as bootstrap-draw effects.

The only permitted inference from the predeclared rule is operational:

`49 draws = ELIGIBLE FOR THE NEXT NON-AUTHORITATIVE BROADER DEPARTURE CHARACTERIZATION`

The smallest passing draw count may be used there for computational economy, exactly as declared before execution.

## Retention

The repository result retains every prospectively required aggregate output, Wilson interval, held-out participant/item mean delta, failure count, advancement verdict and execution provenance.

The exact per-partition trial payloads are identified by GitHub Actions artifact IDs and SHA-256 hashes in the retained JSON result.

## Boundary

`49 bootstrap draws = NOT AUTHORITATIVELY FROZEN`

`20 evaluation replicates = NOT AUTHORITATIVELY FROZEN`

`exact alpha=0.05 calibration = NOT VALIDATED`

`authoritative specificity/power = NOT VALIDATED`

`authoritative core grid = NOT FROZEN`

`human N = NOT FROZEN`

`participant recruitment = NOT AUTHORIZED`

`runtime F1b = NOT AUTHORIZED`

## Next gate

Proceed to a broader **non-authoritative** controlled-departure characterization using 49 bootstrap draws, while restoring the frozen scientific dimensions omitted from this calibration screen:

- both relevant anchors;
- all declared departure axes;
- both signs;
- target nearest-CBD RMS distances 0.10 / 0.25 / 0.50;
- CBD and ADD restriction diagnostics as prospectively defined in #145.

The next stage must be frozen before execution and must not convert 49 draws, 20 replicates, the core grid or human N into authoritative choices.
