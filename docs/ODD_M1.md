# ODD extension — M1 Editorial Emphasis

Software version described: Alpha 0.4.0a0  
Active model specification: M1  
Retained baseline: M0  
Status: candidate, uncalibrated mechanism extension

This document describes the first executable M1 extension. The M0 baseline remains
documented in `docs/ODD_MAIN.md` and all retained M0 regression patterns remain
release gates.

## 1. Purpose and empirical target

M1.E1 tests whether a model that explicitly separates the available information
pool from the information actually observed can reproduce a qualitative framing
pattern without changing underlying factual compatibility.

The empirical anchor is Tohidi, Haider & Watts (2025), a preregistered randomized
experiment in which factually accurate news presentations were varied through
tone-conditioned information selection. The study reports changes in feelings and
opinions, with stronger and more robust effects for negative than positive
presentations.

M1 uses these published effects as a directional benchmark only. It does not fit
its appraisal gain to the reported percentage-point treatment effects.

## 2. Entities, state variables and scales

### InformationUnit

Each unit belongs to one event, carries a signed valence in [-1, 1], and in the
registered reference experiment is required to be compatible with the factual
pool.

Negative valence is not falsehood.

### EditorialPolicy

A transparent reference policy with an emphasis parameter in [-1, 1] and a fixed
selection budget. Negative emphasis preferentially selects negative-valence units;
neutral emphasis selects units closest to neutral; positive emphasis preferentially
selects positive-valence units.

This is a modelling policy, not an estimated newsroom-bias score.

### ObservedInformation

The selected subset actually exposed in the reference condition. Its derived
`Sobs` value is the mean signed valence of selected units.

### Issue appraisal

`Aissue` is a bounded M1 state in [-1, 1]. It is distinct from M0 claim-belief
`B`. The current reference update is:

`Aissue' = clip(Aissue + g * Sobs, -1, 1)`

with demonstrative gain `g = 0.25`.

## 3. Process overview

Reference M1.E1:

1. initialise one symmetric fact-compatible information pool;
2. hold that pool fixed across all conditions;
3. apply one editorial emphasis policy;
4. derive the observed sample balance;
5. update issue appraisal using the same reference gain;
6. compare negative, neutral and positive conditions;
7. rerun with editorial selection disabled as a nested null model.

No social network, platform ranking, strategic actor, source credibility learning,
or heuristic selector is required for M1.E1.

## 4. Registered validation patterns

### VAL.M1.001 — Selective factual emphasis

With one fixed fact-compatible pool, negative editorial emphasis should generate a
more negative observed sample and issue appraisal than neutral selection.

### VAL.M1.N01 — Nested null

When editorial selection is disabled, all conditions receive the same full pool and
the condition difference must disappear.

The null constraint prevents the implementation from manufacturing the effect by
altering ground truth, the information pool, or the agent state directly.

## 5. Evidence-to-model mapping

The cited experiment directly supports a downstream effect of differently framed,
factually accurate presentations. It does not directly measure `Eedit`, `Sobs`,
or `Aissue`, and it does not identify the bounded linear appraisal update.

The experiment also notes that its treatment effect combines information-selection
and tone variation. Therefore M1.E1 must not be described as uniquely identifying
selection as the psychological causal mechanism.

Published effect sizes are stored in `model/empirical_targets.json` as empirical
context, not as fitted parameters.

## 6. What M1.E1 does not claim

M1.E1 does not claim:

- that media outlets can be summarized by one stable bias score;
- that negative reporting is false reporting;
- that selective presentation uniquely determines political opinion;
- that issue appraisal is equivalent to belief B;
- that the reference gain is a population estimate;
- that platform algorithms are responsible for the treatment effect;
- that the mechanism generalizes quantitatively to Romania or any population.

## 7. Extension criterion

M1.E1 should be replaced or expanded only when a rival mechanism adds a
differential empirical prediction or materially improves out-of-sample pattern
reproduction.

Candidate later extensions include separating selection from presentation framing,
attention/consumption gates, richer situation models, and heuristic-policy fit.
They remain outside Alpha 0.4.0a0 unless separately registered and tested.
