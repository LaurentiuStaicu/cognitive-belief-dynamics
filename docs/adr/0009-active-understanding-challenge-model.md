# ADR 0009 — OA-5C Challenge Model

Status: Proposed for OA-5C implementation.

## Context

R6 permits Challenge Model only when CEM already contains scientifically registered alternatives. It forbids manufacturing a new comparator for pedagogical purposes.

The merged M1.E3 access artifact already contains an eligible contrast under one held-fixed context:

- `null`: the access gate ignores Hneg;
- `headline_negativity`: Hneg enters the demonstrative access logit.

The same story, source, image and PreviewImpression are held fixed across lower- and higher-negativity conditions. The registered negative constraint `VAL.M1.N04` requires the NULL predictions to converge, while `VAL.M1.004` records the directional Hneg contrast.

## Decision

OA-5C adds a Challenge Model surface inside Active Understanding at:

`#understanding/active/challenge-model`

It projects values directly from the already-loaded canonical `m1_access.json` artifact. It does not implement a second logistic function, refit parameters, create a new model family, or alter M1.E3 outputs.

The surface shows side by side:

- held-fixed context;
- each existing model assumption;
- canonical lower-/higher-Hneg Paccess;
- canonical ΔPaccess;
- experiment purpose;
- calibration status;
- empirical target ID;
- registered validation IDs;
- the existing interpretation boundary.

A link opens the complete M1.E3 mechanism comparator.

## Fail-closed projection

`projectAccessChallenge()` rejects the Challenge Model projection if:

- story, source, image or PreviewImpression differ across the two conditions;
- cue values no longer match the registered control/treatment encoding;
- the NULL model no longer preserves equal Paccess across Hneg conditions.

These checks protect the pedagogical contrast from silently drifting away from the scientific artifact.

## Scientific boundary

OA-5C changes no equation, coefficient, empirical target, evidence status, semantic identity, model selection result or release metadata.

The displayed difference is a model-discrimination demonstration. It does not select a universally true model and does not turn uncalibrated coefficients into population causal estimates.

## Accessibility and regression

The comparison uses ordinary headings, definition lists and buttons. It remains keyboard-operable and reflows to one column on compact layouts.

CI adds a unit gate for canonical projection/fail-closed invariants and Playwright coverage for direct routing, canonical deltas, status text, validation boundary, mobile reflow and the link back to the full M1.E3 comparator.
