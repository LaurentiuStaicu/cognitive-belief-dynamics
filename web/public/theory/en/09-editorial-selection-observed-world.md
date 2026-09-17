# Editorial selection and the observed world

## Central idea

Two presentations can both be fact-compatible while constructing very different samples from the same available reality. M1.E1 tests this without equating negativity with falsity: it holds a fact-compatible information pool fixed, changes the selection policy, and observes how the viewed sample balance and downstream appraisal change.

[[CONCEPT:m1-e1]] · [[VAR:Eedit]] · [[VAR:Sobs]] · [[VAR:Aissue]] · [[MECH:editorial]] · [[VAL:VAL.M1.001]] · [[REF:REF.TOHIDI.2025]] · [[CODE:m1e1.editorial_select]] · [[VIEW:learning]]

## From available world to observed sample

The reference pool contains InformationUnit objects with valence values from -1 to 1, all marked fact-compatible. The editorial policy has [[VAR:Eedit]], a reference emphasis between -1 and 1, plus a fixed selection budget.

Negative emphasis favors negative-valence units; positive emphasis favors positive ones; neutral emphasis favors values closest to zero. [[CODE:m1e1.editorial_select]] implements the transparent rule. [[VAR:Sobs]] is the mean valence of selected units.

Eedit is not a measured score for a real newsroom. It is a synthetic experimental manipulation. Sobs is not “the truth of the event”; it is the balance of the observed sample.

## From sample to appraisal

M1.E1 updates [[VAR:Aissue]] using:

Aissue' = clip(Aissue + g × Sobs, -1, 1),

with g = 0.25 in the reference experiment. This equation is deliberately uncalibrated. Aissue represents issue/event appraisal in M1.E1 and is not M0 truth-belief [[VAR:B]].

## Empirical anchor

[[REF:REF.TOHIDI.2025]] reports a preregistered experiment with 2,141 participants and seven events in which positive, neutral and negative synthetic articles selected factual information differently. Negative framing produced more negative feelings and opinions than neutral framing.

CEM uses this as a directional phenomenon-level target. The study does not measure Eedit, Sobs or Aissue and cannot uniquely identify information selection separately from presentation tone. The exact mechanism therefore remains CANDIDATE.

## Nested null: the essential test

When editorial selection is disabled, every condition must receive the same complete pool. The condition difference must disappear. This constraint prevents the model from manufacturing the effect through hidden changes in facts, the pool or agent state.

[[VAL:VAL.M1.001]] checks the active-selection pattern. The associated null checks convergence when selection is removed.

## What this chapter does not claim

It does not claim that negative means false, that journalism can be summarized by one bias axis, or that information selection uniquely determines opinion. It does not attribute the Tohidi effect to platform algorithms and does not extrapolate it quantitatively to real populations.

## In the application

Open [[VIEW:learning]] and [[MECH:editorial]] to trace pool → selection → Sobs → Aissue. The distinction matters in Chapter 11, where algorithmic ranking is located at a different causal stage.