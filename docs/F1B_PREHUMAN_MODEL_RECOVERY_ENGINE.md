# F1b Synthetic Recovery Engine — Smoke Stage

Status: **SMOKE_NON_AUTHORITATIVE**

Issue: #128  
Design issue: #126  
Parent F1b research issue: #125

## Purpose

This module implements the first executable synthetic model-recovery smoke engine for F1b. It is calibration/recovery infrastructure only.

It does not create F1b runtime events, alter M0 equations, collect human data, freeze a human sample size, or authorize an authoritative benchmark.

## R1

The engine simulates participant×item repeated continuous synthetic judgments under:

- SR-A: centered anti-reliability, `2*T-1`;
- SR-B: discount-only comparator, `T`;
- SR-C: threshold/gating comparator.

Participant and item intercepts and slopes are present in the generator.

All three candidates are fit to every generated dataset.

## R2

The engine simulates realised binary Share under:

- AP-A: current CBD complement-interaction action structure;
- AP-B: additive comparator;
- AP-C: flexible interaction comparator.

Participant and item intercepts and reward slopes are present in the generator.

All three candidates are fit to every generated dataset.

## Selection

The smoke engine uses three diagnostics:

1. in-sample AIC;
2. held-out participant predictive log likelihood;
3. held-out item predictive log likelihood.

A family is selected only when all three identify the same candidate.

Otherwise the result is:

`INCONCLUSIVE`

This is deliberately stricter than forcing a winner.

## Current limitation

The first smoke fitter estimates population-level candidate surfaces while participant/item heterogeneity enters the generator as a robustness challenge. It is not yet the final hierarchical inference engine for an authoritative design search.

Therefore smoke results are useful for:
- code-path verification;
- deterministic provenance;
- candidate separability checks;
- failure-mode discovery.

They are not sufficient for:
- freezing core recovery cells;
- freezing human N;
- empirical calibration;
- scientific promotion.

## Provenance

The CLI runner stores:
- source commit;
- config SHA-256;
- contract SHA-256;
- seed;
- replicate override.

Any replicate override remains non-authoritative.

## Gate

`authoritative recovery = NOT AUTHORIZED`

`human N = NOT FROZEN`

`participant recruitment = NOT AUTHORIZED`

`runtime F1b = NOT AUTHORIZED`
