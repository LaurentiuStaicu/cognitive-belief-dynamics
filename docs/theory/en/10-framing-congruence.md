# Presentation framing and attitudinal congruence

## Central idea

The same factual meaning can be expressed through different linguistic forms. M1.E2 asks whether confirmation versus refutation framing changes active-engagement propensity and whether that difference depends on the relation between the participant's prior stance and the semantic stance of the message.

[[CONCEPT:m1-e2]] · [[VAR:Fpres]] · [[VAR:Gatt]] · [[VAR:Pengage]] · [[VAR:EngageIntent]] · [[MECH:presentation]] · [[VAL:VAL.M1.003]] · [[REF:REF.ALVARADO.2026]] · [[CODE:m1e2.active_engagement_probability]] · [[VIEW:learning]]

## Semantic invariance

M1.E2 constructs one SemanticProposition and two PresentedMessage objects sharing the same semantic_signature. One condition expresses “TRUE that p”, the other “FALSE that not-p”. [[VAR:Fpres]] codes presentation form, not truth and not editorial selection.

This invariance is essential: if meaning changed across conditions, a difference could no longer be attributed to framing.

## Congruence is relational and task-specific

[[VAR:Gatt]] is calculated as prior_stance × message_stance and remains in [-1,1]. It is not ideology, party identity, personality or a global “confirmation bias” score. It only represents whether prior stance and message meaning align in this task.

The design permits an interaction test without turning a local experimental relation into a stable psychological identity.

## Three nested models

NULL: logit(Pengage) = b0. Frame variation is normalized and confirmation/refutation must converge.

FRAME_ONLY: logit(Pengage) = b0 + beta_frame × Fpres. Confirmation has a uniform advantage.

FRAME_CONGRUENCE adds beta_congruence × Gatt and beta_interaction × Fpres × Gatt. The confirmation advantage can be larger for congruent messages and collapse toward zero for counter-attitudinal messages.

[[CODE:m1e2.active_engagement_probability]] contains these exact forms. Coefficients are demonstrative and are not fitted to published regressions.

## Empirical evidence

Aruguete and colleagues (2024) found an aggregate active-engagement advantage for confirmation over refutation across four Latin American countries using factually accurate, semantically equivalent content. Share by itself was not a universally robust outcome.

[[REF:REF.ALVARADO.2026]] reports an interaction between confirmation frame and partisan congruence in a nationally representative Argentina survey experiment. CEM cautiously generalizes only the relational pattern required for model discrimination.

[[VAL:VAL.M1.003]] requires the confirmation-refutation contrast to be larger for congruent than counter-attitudinal messages.

## Pengage and EngageIntent are not Share

[[VAR:Pengage]] is a latent probability for the M1.E2 outcome. [[VAR:EngageIntent]] is the observable obtained by comparing the probability with an explicit draw. Neither is M0 [[VAR:Share]]. Keeping outcomes separate prevents an aggregate-engagement result from being used as unsupported evidence for behavioral sharing.

## What this chapter does not claim

It does not claim that confirmation is always more effective, that the effect generalizes universally across cultures, or that Gatt measures political identity. It does not require cognitive difficulty or negative affect as mediators because the anchor studies do not make either pathway necessary.

## In the application

Use [[VIEW:learning]] for the NULL → FRAME_ONLY → FRAME_CONGRUENCE comparison and the [[MECH:presentation]] inspector to see exactly what remains invariant and what changes.