# TRACE — Modelling notebook

## 2026-09 — M0 reference core

**Question.** What is the smallest executable model that can reproduce the four initial empirical patterns without hard-coding Track A/Track B or a generic critical-thinking variable?

**Decision.** M0 contains familiarity, corrective accessibility, source-reliability estimation, belief, accuracy salience, and an action policy. Ground truth is isolated from human belief updating.

**Functional forms.** Bounded familiarity saturation, exponential correction decay, delta-rule reliability learning, logistic belief/action transforms. These are reference candidates, not asserted unique psychological laws.

**Replacement criterion.** Replace a functional form when a rival produces materially better out-of-sample pattern reproduction or when identifiability/diagnostics show the reference form is inadequate.

## 2026-09 — Alpha 0.3.6 scientific-readiness gate

**Question.** Is the project ready to add the first executable M1 mechanisms for world-model construction, heuristic policy selection and editorial media?

**Candidates.** (A) label the current UX/registry foundation as 0.4 immediately; (B) add all MOD.14–16 variables and parameters before diagnostics; (C) introduce a 0.3.6 methodological bridge that improves reproducibility and model diagnostics while leaving M0 numerically unchanged.

**Evidence and constraints.** The mature project roadmap reserves v0.4 for world model + heuristics + editorial media. M0 already has one synthetic single-parameter recovery test, but not a broader local trade-off diagnostic. ODD/Visual ODD and the eight-subsystem architecture are now present, while MOD.14–16 remain conceptual targets rather than tested numerical mechanisms.

**Decision.** Choose candidate C. Alpha 0.3.6 adds purpose metadata, ODD, local sensitivity/SVD diagnostics, a separate prediction-robustness report, reproducibility metadata, citation metadata and release provenance. It does not change the M0 equations or claim empirical calibration.

**Alternative rejected.** Calling the architecture-only state 0.4 would weaken the version contract. Adding numerical MOD.14–16 mechanisms before a differential pattern test would violate the extension gate.

**What would change the decision.** If a tested MOD.14–16 mechanism with an observable target, operationalisation, differential prediction and rejection criterion is available and preserves the M0 regression patterns, the project may advance to the 0.4/M1 series.

**Version introduced.** 0.3.6a0.


## 2026-09 — Alpha 0.4 M1.E1 editorial-emphasis gate

**Question.** What is the smallest empirically anchored extension that can make the distinction between available information and observed information executable without introducing platform algorithms, a generic media-bias score or an unvalidated cognitive super-variable?

**Candidates.** (A) add platform ranking and polarization immediately; (B) implement a generic media-bias coefficient; (C) implement one fixed fact-compatible information pool plus an explicit editorial-selection policy and a separate issue-appraisal state.

**Evidence.** Tohidi, Haider & Watts (2025) ran a preregistered randomized experiment across seven news events. Positive, neutral and negative synthetic articles preserved factual accuracy while selecting information by tone. Negative framing produced a -18.5 percentage-point effect on feelings relative to neutral and a -17.94 percentage-point effect on the opinion index. The study explicitly notes that its treatment combines information selection and tone variation.

**Decision.** Choose C as M1.E1. Register Eedit, Sobs and Aissue; keep negative valence distinct from falsehood; retain B as the M0 truth-belief state. Use the published magnitudes as validation context only and do not fit the demonstrative M1 gain to them.

**Nested null.** With editorial selection disabled, all conditions receive the same full fact-compatible pool and the condition difference must disappear.

**Alternative rejected.** A generic media-bias coefficient would conflate selection, tone, platform distribution and downstream response. Adding platform ranking now would prevent discrimination between editorial selection and algorithmic exposure effects.

**What would change the decision.** Replace or expand M1.E1 if a rival model produces a differential empirical prediction, better out-of-sample pattern reproduction, or evidence allows selection and presentation/tone mechanisms to be identified separately.

**Version introduced.** 0.4.0a0.


## 2026-09 — Alpha 0.4.1 M1.E2 presentation-framing gate

**Question.** After separating editorial selection from the available information pool, what is the smallest next mechanism that adds a new empirically discriminable prediction without introducing platform algorithms or a general ideology variable?

**Candidates.** (A) add a universal confirmation-frame coefficient; (B) add confirmation/refutation presentation plus a task-specific frame × prior-attitude congruence interaction; (C) jump directly to attention/CTR or platform ranking.

**Evidence.** Aruguete et al. (2024) randomized 9,512 adults in Argentina, Brazil, Chile and Colombia to semantically equivalent TRUE versus FALSE/refutation frames. Confirmation increased aggregate active engagement in all four countries, while share alone was not a robust universal outcome. Alvarado, Aruguete & Calvo (2026) report that the Confirmation × Partisan Congruence interaction is 0.124 (SE 0.040, p<0.001) for aggregate engagement, while the confirmation main effect among counter-attitudinal respondents is approximately zero (-0.010, SE 0.025).

**Decision.** Choose B as M1.E2. Keep proposition meaning and factual compatibility invariant across frame conditions. Define Fpres, task-specific Gatt, Pengage and EngageIntent. Compare presentation-normalized NULL, frame-only, and frame×congruence models. Do not fit the reference coefficients to published effect sizes.

**Nested null.** When presentation-frame variation is normalized away, confirmation and refutation must converge.

**Outcome boundary.** Aggregate active engagement is not M0 Share. M1.E2 must not silently alter M0 sharing outputs.

**Alternative rejected.** A universal frame coefficient cannot reproduce the 2026 heterogeneity pattern without hidden condition changes. Platform ranking/attention are deferred because they answer a later causal-stage question.

**What would change the decision.** Remove the interaction if a smaller model reproduces the registered heterogeneity target under invariant semantic content, or if out-of-sample evidence contradicts the congruence moderation.

**Version introduced.** 0.4.1a0.


## 2026-09 — Alpha 0.4.2 M1.E3 headline-access gate

**Question.** After separating editorial selection and presentation-framing outcomes, what is the smallest next executable stage that distinguishes a rendered headline preview from the decision to open/click fuller content?

**Candidates.** (A) add a generic latent attention variable; (B) add a broad multi-feature click model with negativity, simplicity, curiosity and ranking; (C) add one explicit PreviewImpression → Access gate with one predeclared controlled headline cue and nested NULL.

**Evidence.** Robertson et al. (2023) use a Registered Report on Upworthy randomized headline experiments and model clicks conditional on impressions with a multilevel binomial-logit specification. The main Results text reports 12,448 filtered RCTs, 53,699 headlines, more than 205 million impressions and 2,778,124 clicks, with a positive standardized negative-language coefficient. The 2024 Upworthy correction identifies a period with likely randomization problems; archive maintainers report the Robertson result remains nearly identical after restricting the reanalysis to reliable tests. A 2025 Nickl–Hills–Lorenz-Spreen preprint / APS 2026 presentation provides preliminary counterevidence by reporting no expected negativity-bias effect in a different two-stage experiment.

**Decision.** Choose C. Promote Hneg as a binary precomputed controlled cue, Paccess as a derived metric, Access as a separate observable and PreviewImpression as a separate prior event. Compare cue-insensitive NULL with a demonstrative logistic Hneg candidate. Keep the coefficient uncalibrated and independent of the source coefficient/magnitude.

**Nested null.** When Hneg is ignored by the NULL model, lower- and higher-Hneg conditions must have identical Paccess.

**Outcome boundary.** PreviewImpression, Access, attention, encoding, belief, EngageIntent and Share remain distinct. Non-click does not erase headline exposure.

**Alternative deferred.** Headline simplicity Hsimp remains a scientifically supported alternative, but its composite operationalisation, LIWC-derived components and restricted Washington Post source data make it less suitable for the first minimal reproducible comparator.

**What would change the decision.** Replace or revise M1.E3 if independent evidence contradicts the bounded access direction, if the comparator cannot preserve its invariants, if a smaller alternative cue discriminates the model more cleanly, or if the access stage fails to remain separable from downstream cognition/action.

**Release boundary.** This Phase B implementation remains on an unreleased feature branch until the Alpha 0.4.2a0 explanatory/UI layer and release audit are complete.


## 2026-09 — Alpha 0.4.2a0 Phase C explanatory-surface decision

**Question.** How should the already approved M1.E3 runtime become inspectable without
silently turning access into attention, belief, sharing or a second implementation
of the model?

**Candidates.** (A) add a new top-level application tab; (B) add a temporal access
trajectory; (C) extend Understanding → Mechanisms with one between-condition
comparator that reads the canonical M1.E3 export and links back to Theory and the
Evidence Registry.

**Decision.** Choose C. The UI holds story, source, image, factual compatibility
and PreviewImpression fixed, exposes lower/higher Hneg, shows exact NULL and
Hneg-sensitive Paccess values, and displays the empirical target with its
limitations. Theory chapter 11 registers the same stage distinction and deep-links
to the comparator.

**Rejected presentation shortcuts.** A new top-level tab would fragment the existing
Understanding architecture. A temporal curve would imply a longitudinal empirical
design that M1.E3 does not have. Recomputing the logistic equation in TypeScript
would create an avoidable second source of scientific truth.

**Outcome boundary.** The UI explicitly preserves
`PreviewImpression != Access != Attention != Encoding != Belief != EngageIntent != Share`.
The illustrative binary Access draw is shown only as a demonstration; model
discrimination uses Paccess.

**Evidence boundary.** Phase C adds no new empirical evidence and therefore does not
advance the evidence snapshot beyond `EVIDENCE.M1.2026-09-16.r1`.

**Release boundary.** Phase C remains stacked and unreleased. Version metadata stays
at 0.4.1a1 until the dedicated Alpha 0.4.2a0 release-preparation audit.
