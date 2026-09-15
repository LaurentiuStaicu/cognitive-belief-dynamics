# Sources, feedback and estimated reliability

## Central idea

Information is not evaluated independently of its source. People can use cues about expertise, trustworthiness and prior experience to decide how much weight to place on a claim. M0 represents a minimal version: the agent maintains an estimate of source reliability and updates it after feedback.

[[VAR:T]] · [[VAR:B]] · [[MECH:source]] · [[VAL:VAL.M0.003]] · [[CODE:m0.update_reliability]] · [[VIEW:runs:source:6]]

## Three things must remain separate

First is the source's actual quality in the experimental environment. Second is what the agent believes about that source. Third is the truth of the current claim. In CEM, [[VAR:T]] represents only the agent's reliability estimate. T is not truth and is not an objectively universal reputation score.

This prevents circularity: a source should not count as “good” merely because the agent believes it, and a statement does not become true because it came from a positively evaluated source.

## Reference learning rule

M0 uses a simple delta rule:

T' = clamp01(T + alpha_t × (outcome - T)),

where outcome is 1 for correct feedback and 0 for incorrect feedback in the synthetic task. Inspect [[CODE:m0.update_reliability]].

When evidence enters belief computation, M0 maps T from [0,1] to a source weight in [-1,1] using 2T - 1. The same evidence signal can therefore have different impact depending on estimated reliability.

This is a deliberately simple modelling choice. It does not assume optimal Bayesian updating, an empirically fixed alpha_t, or one-dimensional trust.

## What research shows

Credibility experiments show that perceived source credibility can shape belief uptake and maintenance. Recent work on misinformation updating finds that people can incorporate source-reliability information and can revise source evaluations after contradictory feedback.

Research often separates components such as expertise and trustworthiness. CEM currently compresses them into T for the reference mechanism; that compression is a limitation rather than an ontological claim.

## Feedback can create loops

If source evaluation affects evidence interpretation and interpreted outcomes later affect source evaluation, a feedback loop becomes possible. Research suggests such dynamics can depend on initial credibility. M0 does not model all social feedback loops, but source learning provides a base for testing richer versions later.

## M0 pattern

[[VAL:VAL.M0.003]] checks whether source feedback can change T and whether comparable evidence is then weighted differently. Open [[VIEW:runs:source:6]] for the reference scenario.

## What this chapter does not claim

It does not claim that trust is fixed, one-dimensional or independent of identity and context. It does not claim that “verified sources” are infallible. It does not treat T as truth or convert social reputation into an intrinsic property of a person or institution.

## Epistemic status

The mechanism is EXECUTABLE/CANDIDATE. Research provides BACKGROUND_THEORY and phenomenon-level support for credibility effects; the delta rule and 2T - 1 mapping remain REFERENCE_CANDIDATE until calibration and comparison with alternatives.