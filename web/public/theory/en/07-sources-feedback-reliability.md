# Sources, feedback and estimated reliability

## Central idea

Information is not evaluated independently of its source. People can use cues about expertise, trustworthiness, track record and institutional role to decide how much weight to place on a claim. M0 represents a minimal version: the agent maintains an estimate of source reliability and updates it after feedback.

[[VAR:T]] · [[VAR:B]] · [[MECH:source]] · [[MODULE:MOD.20]] · [[VAL:VAL.M0.003]] · [[CODE:m0.update_reliability]] · [[VIEW:runs:source:6]]

## Three things must remain separate

First is the source's actual performance in the experimental environment. Second is what the agent believes about that source. Third is the truth of the current claim. In CEM, [[VAR:T]] represents only the agent's estimated reliability. T is not truth and is not an objectively universal reputation score.

This separation prevents circularity: a source should not count as “good” merely because an agent trusts it, and a statement does not become true merely because it comes from a positively evaluated source.

## Reference learning rule

M0 uses a simple delta rule:

T' = clamp01(T + alpha_t × (outcome - T)),

where outcome is 1 for correct feedback and 0 for incorrect feedback in the synthetic task. Inspect [[CODE:m0.update_reliability]].

When evidence enters belief computation, M0 maps T from [0,1] to a source weight in [-1,1] using 2T - 1. The same evidence signal can therefore have different impact depending on estimated reliability.

This is a deliberately simple modelling choice. It does not assume optimal Bayesian updating, an empirically fixed alpha_t, or one-dimensional trust.

## Credibility is multidimensional

Research on source credibility commonly distinguishes dimensions such as expertise and trustworthiness. Other cues can include transparency, independence, track record, consensus among relevant experts and whether a source has incentives that may distort reporting. These cues do not collapse naturally into one universal scale.

CEM currently compresses them into T for the reference mechanism. That compression is useful for a minimal executable test, but it is a limitation rather than an ontological claim about how trust works.

Source evaluation is also context-dependent. A source can be highly reliable in one domain and weak in another. Future models should therefore avoid treating reputation as a context-free property of a person, institution or platform.

## Institutions, authority and distributed knowledge

Modern agents often rely on information they cannot personally verify. Scientific journals, public-health agencies, statistical offices, courts, newsrooms, universities and professional bodies can function as epistemic institutions: they organize expertise, procedures, records and accountability so that knowledge can be produced and checked at scales beyond individual cognition.

[[MODULE:MOD.20]] reserves this institutional layer. Institutional authority should not be represented as a magical truth signal. Its epistemic value can depend on procedures such as transparency, reproducibility, conflict-of-interest management, correction mechanisms, independence and the quality of specialist expertise.

The inverse mistake is equally important: the fact that institutions can fail does not imply that all sources become epistemically equivalent. A useful model must allow both institutional error and differential reliability.

CEM therefore separates at least three levels that future work may model independently: the agent's trust in an institution, observable features of the institution or its process, and the empirical performance of claims produced through that process.

## Feedback can create loops

If source evaluation affects evidence interpretation and interpreted outcomes later affect source evaluation, a feedback loop becomes possible. Research suggests such dynamics can depend on initial credibility. M0 does not model all social feedback loops, but source learning provides a base for testing richer versions later.

Institutional settings add further loops. Corrections, retractions, audits and public explanations can reduce trust in the short term while improving long-run reliability. Conversely, prestige can sustain trust even when direct feedback is sparse. These possibilities should not be hidden inside T without explicit assumptions.

## M0 pattern

[[VAL:VAL.M0.003]] checks whether source feedback can change T and whether comparable evidence is then weighted differently. Open [[VIEW:runs:source:6]] for the reference scenario.

## What this chapter does not claim

It does not claim that trust is fixed, one-dimensional or independent of identity and context. It does not claim that “verified sources” or institutions are infallible. It does not treat T as truth, convert social reputation into an intrinsic property, or infer reliability from status alone. It also does not claim that distrust is irrational by definition; the relevant question is whether confidence in a source is calibrated to evidence about its performance and procedures.

## Epistemic status

The M0 source mechanism is EXECUTABLE/CANDIDATE. Research provides BACKGROUND_THEORY and phenomenon-level support for credibility effects; the delta rule and 2T - 1 mapping remain REFERENCE_CANDIDATE until calibration and comparison with alternatives. [[MODULE:MOD.20]] remains CONCEPTUAL until institutional features, observables and differential predictions are specified.