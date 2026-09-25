# F1b Pre-human Model-Recovery Design

Status: **PROSPECTIVE_SYNTHETIC_MODEL_RECOVERY_DESIGN**

Issue: #126  
Parent F1b research issue: #125  
Baseline main commit: `0e3423035c32f2285e7a430df69a6788de068fd5`

## Purpose

This design freezes the first executable specification layer that must exist before any F1b human study. It does not implement F1b runtime behavior, collect human data, change M0 equations, or select a human sample size.

CBD already uses prospective synthetic recovery gates for M1.E4 and F1a. F1b reuses that discipline but adapts it to crossed participant×item binary/repeated-measures designs.

## Recovery problem R1 — source reliability × evidence

R1 compares three predeclared source-weighting families on a common synthetic belief/judgment surface:

- **SR-A** — current CBD reference: `w(T)=2T-1`;
- **SR-B** — discount-only synthetic comparator: `w(T)=T`;
- **SR-C** — threshold/gating synthetic comparator.

The synthetic reliability grid must span below, at, and above the current neutral point:

`T = {0.2, 0.5, 0.8}`

Signed synthetic evidence spans both directions:

`E = {-1.0, -0.5, 0.5, 1.0}`

These values are design-search codes only. They are not approved empirical mappings.

## Recovery problem R2 — action policy

R2 compares:

- **AP-A** — current CBD complement-interaction action structure;
- **AP-B** — additive action comparator;
- **AP-C** — flexible interaction comparator.

The design-search surface includes:

`B = {0.2, 0.5, 0.8}`

accuracy cue:

`A = {0,1}`

and synthetic reward context:

`R = {-1,0,1}`

Again, these are synthetic recovery codes, not human-calibrated values.

## Crossed participant and item variation

Every later executable benchmark must simulate both participant and item variability. Random-intercept-only recovery is not sufficient as the sole evidence. Participant/item slope heterogeneity must appear in declared stress/core scenarios before a human design is frozen.

## Design-search axes

The initial search grid is:

- participants: 96, 192, 384;
- items: 36, 72, 144;
- synthetic missingness: 0%, 10%, 20%.

These numbers are **not human sample-size recommendations**. They define a broad simulation surface used to locate regions where model discrimination becomes reliable.

The design must search participant count and item count jointly.

## Selection rule

The recovery pipeline must allow `INCONCLUSIVE`.

A candidate is selected only when:
1. the prospectively declared in-sample complexity-adjusted diagnostic favors it; and
2. the prospectively declared held-out predictive diagnostic favors it.

Held-out checks must test both participant and item generalization where feasible.

## Recovery convention

The initial core-cell convention may reuse the existing CBD synthetic gate:

`P(correct model) >= 0.80`

This is a **CBD_SYNTHETIC_DESIGN_CONVENTION**, not a universal scientific threshold.

Wrong-model probability and inconclusive probability must be reported separately.

Core cells are not yet frozen in this specification-only change. Stress cells are non-gating.

## Power and model recovery

A later design is not adequate merely because one coefficient can reach statistical significance.

The primary question is whether the proposed participant×item design can recover the generating candidate mechanism under:
- weak/moderate/strong separation;
- participant heterogeneity;
- item heterogeneity;
- missingness;
- null/negative controls.

Simulation-based power for declared primary effects is downstream of model recovery.

## Provenance

A later executable runner must retain:
- source commit;
- config SHA-256;
- contract SHA-256;
- deterministic seed;
- exact candidate set;
- exact selection rule;
- authoritative/non-authoritative flag;
- any debug override.

## Explicit limits

This specification does not:
- implement a recovery engine;
- perform an authoritative run;
- freeze human N;
- authorize participant recruitment;
- change `source_weight(T)=2T-1`;
- create EncounterContext or DecisionOpportunity runtime objects;
- change the CBD paradigm;
- promote F1b.

Current state:

`F1b pre-human recovery = DESIGN_SPECIFICATION_ONLY`

`runtime F1b integration = NOT_AUTHORIZED`

`participant recruitment = NOT_AUTHORIZED`
