# Presentation framing, attitudinal congruence and identity context

## Central idea

The same factual meaning can be expressed through different linguistic forms. M1.E2 asks whether confirmation versus refutation framing changes active-engagement propensity and whether that difference depends on the relation between the participant's prior stance and the semantic stance of the message.

This is a deliberately narrow question. Prior-attitude congruence can correlate with identity, partisanship or motivated reasoning in some real settings, but it is not identical to any of them. CEM keeps the experimental relation local before introducing broader social-identity mechanisms.

[[CONCEPT:m1-e2]] · [[VAR:Fpres]] · [[VAR:Gatt]] · [[VAR:Pengage]] · [[VAR:EngageIntent]] · [[MECH:presentation]] · [[MODULE:MOD.05]] · [[VAL:VAL.M1.003]] · [[REF:REF.ALVARADO.2026]] · [[CODE:m1e2.active_engagement_probability]] · [[VIEW:learning]]

## Semantic invariance

M1.E2 constructs one SemanticProposition and two PresentedMessage objects sharing the same semantic_signature. One condition expresses “TRUE that p”, the other “FALSE that not-p”. [[VAR:Fpres]] codes presentation form, not truth and not editorial selection.

This invariance is essential. If semantic content changed across conditions, a difference could no longer be attributed cleanly to presentation form.

The manipulation should therefore be read as a controlled language contrast, not as a general model of news framing. Chapter 9 uses framing in the broader communication-theory sense, where selection, emphasis, examples, headlines and narrative organization may all change.

## Congruence is relational and task-specific

[[VAR:Gatt]] is calculated as prior_stance × message_stance and remains in [-1,1]. It is not ideology, party identity, personality or a global “confirmation bias” score. It only represents whether prior stance and message meaning align in this task.

The design permits an interaction test without turning a local experimental relation into a stable psychological identity. The same person can be congruent with one message, incongruent with another and neutral toward a third.

## Three nested models

NULL: logit(Pengage) = b0. Frame variation is normalized and confirmation/refutation must converge.

FRAME_ONLY: logit(Pengage) = b0 + beta_frame × Fpres. Confirmation has a uniform advantage.

FRAME_CONGRUENCE adds beta_congruence × Gatt and beta_interaction × Fpres × Gatt. The confirmation advantage can be larger for congruent messages and collapse toward zero for counter-attitudinal messages.

[[CODE:m1e2.active_engagement_probability]] contains these exact forms. Coefficients are demonstrative and are not fitted to published regressions.

The nested sequence is scientifically useful because it asks whether a more complex relation explains a pattern that the smaller model cannot reproduce. It is not evidence that the interaction term reveals one unique psychological mechanism.

## Empirical evidence

Aruguete and colleagues (2024) found an aggregate active-engagement advantage for confirmation over refutation across four Latin American countries using factually accurate, semantically equivalent content. Share by itself was not a universally robust outcome.

[[REF:REF.ALVARADO.2026]] reports an interaction between confirmation frame and partisan congruence in a nationally representative Argentina survey experiment. CEM cautiously generalizes only the relational pattern required for model discrimination.

[[VAL:VAL.M1.003]] therefore requires the confirmation-refutation contrast to be larger for congruent than counter-attitudinal messages.

## Congruence, identity and motivated reasoning are not synonyms

Political-psychology research documents robust partisan favoritism in many judgments, but the mechanisms remain debated. Motivational accounts emphasize goals such as protecting valued identities or desired conclusions. Cognitive accounts emphasize prior beliefs, information environments, selective exposure, memory and inferential processes. Contemporary reviews increasingly warn against treating all partisan differences as one universal motivated-reasoning mechanism.

For CEM, [[MODULE:MOD.05]] reserves the broader layer of social identity and polarization. If identity becomes executable, the model must specify what identity variable is measured, when it is activated, which outcome it changes and what prediction distinguishes identity effects from simple prior-belief congruence.

M1.E2 does **not** yet make that step. [[VAR:Gatt]] is a relation between a task-specific prior stance and message stance. Calling it “identity strength” or “partisanship” would be an invalid reinterpretation of the variable.

## Why this distinction matters for causal explanation

Imagine that confirmation framing produces more engagement for congruent content. At least several explanations remain possible: the wording may be easier to process; it may feel less confrontational; it may fit prior expectations; it may protect identity; or the result may depend on norms and platform context. The observed interaction alone does not uniquely identify one mediator.

CEM therefore models the **pattern** first and leaves mediators unexecuted unless evidence and experimental design discriminate among them. This keeps the computational claim smaller than the psychological story.

## Pengage and EngageIntent are not Share

[[VAR:Pengage]] is a latent probability for the M1.E2 outcome. [[VAR:EngageIntent]] is the observable obtained by comparing the probability with an explicit random draw. Neither is M0 [[VAR:Share]]. Keeping outcomes separate prevents an aggregate-engagement result from being used as unsupported evidence for behavioral sharing.

The distinction also matters because “engagement” can combine behaviors with different meanings: liking, commenting, clicking or intending to interact need not reflect the same belief or motive.

## What this chapter does not claim

It does not claim that confirmation is always more effective, that the effect generalizes universally across cultures, that Gatt measures political identity, or that identity always distorts reasoning. It does not require cognitive difficulty, negative affect or motivated reasoning as mediators because the anchor studies do not uniquely identify those pathways.

## In the application

Use [[VIEW:learning]] for the NULL → FRAME_ONLY → FRAME_CONGRUENCE comparison and the [[MECH:presentation]] inspector to see exactly what remains invariant and what changes. Use [[VIEW:reference]] to keep [[VAR:Gatt]] separate from broader conceptual constructs in [[MODULE:MOD.05]].
