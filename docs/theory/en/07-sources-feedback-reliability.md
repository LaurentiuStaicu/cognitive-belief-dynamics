# Sources, epistemic authority and estimated reliability

## Central idea

Information is not evaluated independently of its source. People can use cues about expertise, trustworthiness, institutional role and prior experience to decide how much weight to place on a claim. M0 represents only a minimal part of this problem: the agent maintains an estimate of source reliability and updates it after feedback.

[[VAR:T]] · [[VAR:B]] · [[MECH:source]] · [[VAL:VAL.M0.003]] · [[CODE:m0.update_reliability]] · [[MODULE:MOD.20]] · [[VIEW:runs:source:6]]

## Three things must remain separate

First is the source's actual performance or quality in the experimental environment. Second is what the agent believes about that source. Third is the truth of the current claim. In CEM, [[VAR:T]] represents only the agent's estimated reliability. T is not truth and is not an objectively universal reputation score.

This separation prevents circularity. A source should not count as “good” merely because the agent trusts it, and a statement does not become true because it came from a positively evaluated source. Conversely, a source can be reliable on average and still be wrong on a particular claim.

## Reference learning rule

M0 uses a simple delta rule:

T' = clamp01(T + alpha_t × (outcome - T)),

where outcome is 1 for correct feedback and 0 for incorrect feedback in the synthetic task. Inspect [[CODE:m0.update_reliability]].

When evidence enters belief computation, M0 maps T from [0,1] to a source weight in [-1,1] using 2T - 1. Comparable evidence can therefore have different impact depending on estimated reliability.

This is a deliberately simple modelling choice. It does not assume optimal Bayesian updating, an empirically fixed alpha_t, or one-dimensional trust.

## What the empirical literature adds

Experiments on source credibility show that people can use information about source reliability when updating beliefs. Sanna and Lagnado's 2025 experiments are especially useful for CEM because they distinguish source feedback from claim truth and show that both trustworthiness and expertise can contribute to reliability judgments.

The literature also shows why CEM should not collapse all source evaluation into one psychological essence called “trust”. Expertise concerns whether a source is competent in the relevant domain. Trustworthiness concerns whether the source is expected to communicate honestly or faithfully. Familiarity, group membership, institutional reputation and past predictive performance can provide additional cues. These cues can agree, but they need not.

M0 compresses this multidimensional problem into T for a controlled reference mechanism. That compression is a limitation, not an ontological claim.

## Source reliability is not the same as epistemic authority

[[MODULE:MOD.20]] reserves a broader question: how do people and societies rely on epistemic institutions and authorities?

An epistemic institution can organize expertise, verification, correction, accountability and records across many individuals. Scientific journals, statistical agencies, courts, professional bodies, newsrooms and fact-checking organizations differ greatly, but they illustrate why institutional credibility cannot be reduced to the personal trustworthiness of one speaker.

Institutional authority can provide a useful shortcut when direct verification is too costly. It can also fail through conflicts of interest, weak procedures, opacity or historical loss of trust. A complete model therefore needs to distinguish at least **claimed authority**, **procedural safeguards**, **domain expertise**, **observed track record** and **the agent's estimate of reliability**.

Alpha 0.4.1a1 does not execute these institutional layers. T should never be presented as a numerical score for “science”, “the media”, “the government” or another institution.

## Feedback, disagreement and revision

Source evaluation can change when predictions are confirmed, claims are corrected or independent sources disagree. That learning is potentially bidirectional: source beliefs affect how evidence is interpreted, while interpreted outcomes later affect source beliefs.

This creates a possible feedback loop. A rich model would need to guard against circularity by preserving external observations and by distinguishing source performance from the agent's interpretation of that performance.

M0 models only a controlled version of this loop. It does not model coalitions of sources, institutional endorsement, coordinated reputation attacks, prestige cascades or strategic attempts to mimic authority.

## Social identity and credibility cues

Similarity to a source can sometimes matter, but similarity is not equivalent to credibility. Large experiments on social and source cues show contingent effects: perceived consensus and credible ingroup sources can influence judgments, while simple engagement counts do not operate as universal persuasion signals.

For CEM this is a warning against a direct “ingroup source → belief” rule. Identity, credibility and social consensus belong to separable causal stages and should be measured independently when possible.

## M0 pattern

[[VAL:VAL.M0.003]] checks whether source feedback can change T and whether comparable evidence is then weighted differently. Open [[VIEW:runs:source:6]] for the reference scenario.

The pattern test validates an internal dependency of the candidate model. It does not establish that the delta rule is the unique psychological learning rule.

## What this chapter does not claim

It does not claim that trust is fixed, one-dimensional or independent of identity and context. It does not claim that experts or “verified sources” are infallible. It does not treat T as truth, and it does not infer institutional legitimacy from popularity. It also does not claim that distrust is necessarily irrational: sometimes distrust reflects relevant evidence, while in other cases it can be produced by misleading signals.

## Epistemic status

The M0 source-learning mechanism is EXECUTABLE/CANDIDATE. Source-credibility effects have empirical support. The exact delta rule and 2T - 1 mapping remain REFERENCE_CANDIDATE. The broader institutional layer in [[MODULE:MOD.20]] is CONCEPTUAL and requires separate operationalization and validation.
