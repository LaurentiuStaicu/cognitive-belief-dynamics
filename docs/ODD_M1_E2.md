# ODD extension — M1.E2 Presentation Framing × Prior-Attitude Congruence

Software version described: Alpha 0.4.1a0  
Active model specification: M1  
Retained baseline: M0  
Status: candidate, uncalibrated model-discrimination extension

This document describes M1.E2. M1.E1 remains documented in `docs/ODD_M1.md`
and the M0 baseline remains documented in `docs/ODD_MAIN.md`.

## 1. Purpose and empirical targets

M1.E2 asks whether semantically equivalent confirmation and refutation
presentations generate different active-engagement propensities, and whether that
difference is moderated by task-specific prior-attitude congruence.

Two empirical anchors are registered:

- Aruguete et al. (2024): a four-country randomized experiment showing higher
  aggregate engagement for confirmation than refutation frames using semantically
  equivalent, factually accurate statements.
- Alvarado, Aruguete & Calvo (2026): a nationally representative Argentina survey
  experiment in which the confirmation advantage is concentrated among
  pro-attitudinal audiences. The registered supplement reports a
  Confirmation × Partisan Congruence interaction of 0.124 for aggregate engagement
  and a near-zero confirmation main effect (-0.010) among counter-attitudinal
  respondents.

Published magnitudes are validation context only and do not set the M1.E2
reference coefficients.

## 2. Entities and variables

### SemanticProposition

One proposition with a fixed semantic stance and a fact-compatibility flag.

### PresentedMessage

A presentation of the same SemanticProposition under one of two frames:

- confirmation: TRUE that p
- refutation: FALSE that not-p

The two reference messages share one semantic signature.

### Fpres — Presentation frame

Reference content attribute encoded as confirmation versus refutation.

It is not truth, factuality, editorial selection or affect.

### Gatt — Prior-attitude congruence

Task-specific relation between prior stance and message semantic stance.

Reference calculation:

`Gatt = prior_stance × message_stance`

This is a modelling convenience. It is not ideology, party identity, personality
or a global confirmation-bias score.

### Pengage — Active-engagement probability

Latent probability produced by the nested reference models.

It is not M0 Share probability and not platform CTR.

### EngageIntent

Reference observable obtained by comparing `Pengage` with an explicit draw.

Pattern validation uses latent probabilities and contrasts, not the stochastic
observable.

## 3. Nested models

### M1.E2-NULL

`logit(Pengage) = b0`

Presentation frame is normalized away.

### M1.E2-A — frame only

`logit(Pengage) = b0 + beta_frame × Fpres`

Differential prediction: confirmation exceeds refutation regardless of congruence.

### M1.E2-B — frame × congruence

`logit(Pengage) = b0 + beta_frame×Fpres + beta_congruence×Gatt + beta_interaction×Fpres×Gatt`

Differential prediction:

- confirmation advantage is positive for congruent messages;
- confirmation advantage collapses toward zero for counter-attitudinal messages.

The current coefficients are demonstrative reference values chosen to make the
model-discrimination contrast explicit. They are not fit to the published
regression coefficients.

## 4. Registered validation patterns

### VAL.M1.002 — Semantic-equivalent presentation framing

Holding semantic content and factual compatibility fixed, the frame-only model
produces higher active-engagement propensity under confirmation than refutation.

### VAL.M1.003 — Frame × prior-attitude congruence

The confirmation–refutation contrast is larger for congruent than
counter-attitudinal messages in the interaction model.

### VAL.M1.N02 — Presentation-frame null

When frame variation is normalized away, confirmation and refutation converge.

### VAL.M1.N03 — Engagement intent is not M0 Share

M1.E2 engagement output remains separate from the retained M0 Share process.

## 5. Model-discrimination logic

M1.E2-A is the smaller candidate consistent with the aggregate 2024 confirmation
advantage.

M1.E2-B is retained only if the additional interaction term is necessary to
produce the 2026 heterogeneity pattern without changing semantic content, factual
compatibility or prior stance across frame conditions.

The extension is rejected or revised if the smaller model can reproduce the same
interaction through hidden condition changes, or if the interaction model alters
M1.E1/M0 outputs.

## 6. Explicitly deferred mechanisms

Alpha 0.4.1a0 does not require:

- cognitive difficulty as a mediator;
- negative affect as a mediator;
- platform ranking;
- attention/click gating;
- social-network amplification;
- stable ideology or party identity;
- general heuristic-policy selection;
- Reflective Distance or Jungian individuation as numerical states.

The 2024 study does not support a simple cognitive-difficulty account, and the
2026 study shows affective effects that do not map reliably onto behavioral
engagement.

## 7. Fitness-for-purpose boundary

M1.E2 can be used to demonstrate and discriminate candidate presentation-framing
mechanisms in synthetic reference tasks.

It cannot be used to estimate real-world population engagement, predict election
behavior, infer individual ideology, recommend platform policy, or convert survey
engagement intentions into observed sharing behavior.
