# Editorial selection, news media and the observed world

## Central idea

Two accounts can both be fact-compatible while constructing very different samples from the same available reality. M1.E1 tests one narrow part of this problem: it holds a fact-compatible information pool fixed, changes the selection policy, and observes how the viewed sample balance and downstream appraisal change.

The wider media problem is larger. News organizations select events, assign prominence, choose sources, construct headlines, arrange stories and decide what is repeated. Television, newspapers, news websites and platform-distributed journalism also operate under different technical, economic and temporal constraints. CEM must therefore distinguish **editorial selection**, **agenda setting**, **presentation/framing**, **repetition**, and **platform ranking** rather than treating all of them as one generic “media bias”.

[[CONCEPT:m1-e1]] · [[VAR:Eedit]] · [[VAR:Sobs]] · [[VAR:Aissue]] · [[MECH:editorial]] · [[MODULE:MOD.16]] · [[VAL:VAL.M1.001]] · [[REF:REF.TOHIDI.2025]] · [[CODE:m1e1.editorial_select]] · [[VIEW:learning]]

## From available world to observed sample

The reference pool contains InformationUnit objects with valence values from -1 to 1, all marked fact-compatible. The editorial policy has [[VAR:Eedit]], a reference emphasis between -1 and 1, plus a fixed selection budget.

Negative emphasis favors negative-valence units; positive emphasis favors positive ones; neutral emphasis favors values closest to zero. [[CODE:m1e1.editorial_select]] implements the transparent rule. [[VAR:Sobs]] is the mean valence of selected units.

Eedit is not a measured score for a real newsroom. It is a synthetic experimental manipulation. Sobs is not “the truth of the event”; it is the balance of the observed sample.

## Gatekeeping, agenda setting and framing are related but distinct

Communication research uses **gatekeeping** for processes that determine which pieces of information pass through decision points and reach an audience. Modern gatekeeping theory extends beyond one editor: organizational routines, news values, economics, technology, sources and platform distribution can all influence what becomes visible.

**Agenda setting** concerns the relative prominence of topics or issues. If one topic repeatedly receives scarce attention while another receives little, audiences encounter a different distribution of salience even when individual reports remain accurate.

**Framing** concerns how an issue is organized and presented: which aspects are foregrounded, what causal or moral structure is emphasized, which examples and images are selected, how a headline is written and how facts are connected into a story. Chapter 10 isolates a much narrower presentation manipulation under semantic invariance; it should not be confused with the full communication-theory meaning of framing.

These distinctions matter because a single observed article can reflect several mechanisms at once. CEM's scientific strategy is to separate them experimentally whenever possible.

## Television and online news are not interchangeable channels

Television news combines selection with sequencing, audiovisual salience, limited airtime and a largely linear viewing flow. News websites can maintain large archives, update stories continuously, test headlines, link related material and expose users to home-page ordering. Social platforms may then redistribute the same journalistic material through recommendation systems and social signals.

Research on television news also identifies multiple functions beyond transmission of facts, including surveillance, interpretation, socialization and the competition for attention. Digital-news research shows that people often encounter news incidentally while using online services for other purposes, and that incidental contact should be distinguished from deeper processing of the content.

CEM does not assume that an effect estimated in one channel transfers unchanged to another. Media type, format and exposure pathway are candidate moderators, not cosmetic details.

## From sample to appraisal

M1.E1 updates [[VAR:Aissue]] using:

Aissue' = clip(Aissue + g × Sobs, -1, 1),

with g = 0.25 in the reference experiment. This equation is deliberately uncalibrated. Aissue represents issue/event appraisal in M1.E1 and is not M0 truth-belief [[VAR:B]].

The equation should be read as a transparent candidate link: a differently balanced observed sample can move appraisal. It is not a general equation for “media influence”.

## Empirical anchor

[[REF:REF.TOHIDI.2025]] reports a preregistered experiment with 2,141 participants and seven events in which positive, neutral and negative synthetic articles selected factual information differently. Negative framing produced more negative feelings and opinions than neutral framing.

CEM uses this as a directional phenomenon-level target. The study does not measure Eedit, Sobs or Aissue and cannot uniquely identify information selection separately from presentation tone. The exact mechanism therefore remains CANDIDATE.

That limitation is important. A good fit to the Tohidi pattern would not show that editorial selection is the sole cause of the human effect; it would show only that the candidate mechanism can reproduce one constrained direction while respecting the model's invariants.

## Editorial systems have incentives and institutions

[[MODULE:MOD.16]] is broader than M1.E1. Real newsrooms operate under professional norms, legal constraints, ownership structures, deadlines, competition, audience demand and commercial pressures. These factors can shape what is selected and how it is presented.

CEM should not collapse them into a single ideological score. If future work models an incentive, it must specify the observable consequence: for example, a change in selection probability, topic prominence, headline choice, verification effort or publication timing.

The same rule applies to online newspapers and television. The model should represent the mechanism being tested, not infer the mechanism from a political label attached to the outlet.

## Nested null: the essential test

When editorial selection is disabled, every condition must receive the same complete pool. The condition difference must disappear. This constraint prevents the model from manufacturing the effect through hidden changes in facts, the pool or agent state.

[[VAL:VAL.M1.001]] checks the active-selection pattern. The associated null checks convergence when selection is removed.

## Relationship to platform ranking

Editorial selection and algorithmic ranking can occur in sequence. A newsroom may first decide what to publish; a website may order the published items; a social platform may then decide which of those items reaches a particular user. These stages can interact, but they are not identical.

Chapter 11 therefore treats ranking, cross-platform flows and social feedback separately. A platform effect should not be attributed to the newsroom without evidence, and an editorial effect should not automatically be attributed to “the algorithm”.

## What this chapter does not claim

It does not claim that negative means false, that journalism can be summarized by one bias axis, that agenda setting or framing determines opinion, or that all media channels produce the same effects. It does not attribute the Tohidi effect to platform algorithms and does not extrapolate it quantitatively to real populations or particular Romanian media outlets.

## In the application

Open [[VIEW:learning]] and [[MECH:editorial]] to trace pool → selection → Sobs → Aissue. Use [[VIEW:reference]] to inspect what each variable means and does not mean. Then compare Chapter 10's presentation manipulation and Chapter 11's platform/ecosystem layer.
