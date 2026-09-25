# F1b Recovery Characterization

Status: **NON_AUTHORITATIVE_CHARACTERIZATION_DESIGN**

Issue: #132  
Parent methodological gate: #130

Baseline main:
`0941856056297c8b5cc7df90e87b9357d856ff36`

## Purpose

This characterization compares the integrated population-level smoke fitter with the penalized hierarchical prototype on exactly the same synthetic participant×item datasets.

It is designed to answer a narrower question before any authoritative recovery grid is frozen:

> Does explicit participant/item fitting improve or destabilize model-family recovery, and how sensitive is that result to misspecified random-effect penalty scales?

## Common-data rule

For every replicate:
1. generate one synthetic dataset;
2. fit the population-level candidate set;
3. fit the hierarchical candidate set at 0.5×, 1× and 2× assumed random-effect scales;
4. record all selections separately.

No inference class receives a different synthetic draw.

## Characterization axes

The non-authoritative design crosses:

- WEAK / MODERATE / STRONG candidate separation;
- 0% / 15% missingness;
- population-level fitting;
- hierarchical fitting at 0.5× / 1× / 2× generator random-effect scales;
- all R1 source-weighting generators;
- all R2 action-policy generators.

The scale multiplier changes the **fitter's assumed penalty scale only**. It does not alter the generator's true heterogeneity.

## Outcomes

Each cell reports four mutually exclusive outcomes:

- correct-model recovery;
- wrong-model selection;
- INCONCLUSIVE;
- FIT_FAILURE.

Fit failure is never silently dropped and is not recoded as inconclusive.

The characterization also reports hierarchical-minus-population deltas for:
- recovery;
- wrong selection;
- inconclusive outcomes;
- fit failure.

## Methodological boundary

The current hierarchical engine is a penalized conditional/MAP prototype.

Recent GLMM methodology reinforces the need for this boundary: approximate methods including PQL/conditional penalization and Laplace can perform differently across nonlinear/binary settings, and Laplace itself can be biased in some binary/correlated regimes. Therefore robustness to penalty-scale misspecification is a diagnostic, not validation of a final marginal likelihood.

The characterization cannot by itself determine that:
- the hierarchical prototype is the final inference method;
- 1× penalty scales are empirically correct;
- any candidate family is a human mechanism;
- any participant/item count is adequate for a human study.

## Gate

`authoritative characterization = NOT YET RUN`

`authoritative core grid = NOT FROZEN`

`human N = NOT FROZEN`

`participant recruitment = NOT AUTHORIZED`

`runtime F1b = NOT AUTHORIZED`
