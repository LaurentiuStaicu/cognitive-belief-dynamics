# Alpha 0.4.2a0 planning contract — M1.E3 Headline Access Gate

Status: planning-only scientific contract. No executable Alpha 0.4.2 mechanism is introduced by this document.

Target software release: **Alpha 0.4.2a0**

Working experiment name:

**M1.E3 — Headline Access Gate (negativity candidate)**

## 1. Decision

Alpha 0.4.2a0 should test a new causal stage between a rendered information preview and access to the fuller content.

The initial executable mechanism should be deliberately narrow:

`headline impression → headline cue → access probability → click/open`

The first cue tested should be **headline negativity**.

The gate itself is the scientific extension. Negativity is the first executable predictor because it has a large randomized field-experiment anchor. Other cues, including linguistic simplicity, are important evidence that access selection is not unique to negativity, but they should not be introduced as additional coefficients in the same first implementation.

This extension remains inside the Alpha 0.4 / M1 family because it adds one separable information-processing stage while retaining M0, M1.E1 and M1.E2 unchanged.

## 2. Why this stage is distinct

The current M1 pathway already separates:

- M1.E1: which fact-compatible information is selected for observation;
- M1.E2: how semantically fixed content is presented and how presentation interacts with task-specific prior-attitude congruence;
- M0: downstream belief, familiarity, source-feedback and sharing processes.

M1.E3 should add a distinct stage:

`available/selected preview → impression → access gate → fuller-content availability for downstream processing`

This must not be collapsed into:

- editorial selection;
- presentation framing;
- platform ranking;
- attention as an internal latent state;
- reading completion;
- belief;
- active-engagement intention;
- sharing.

A headline can be seen without the article being opened. Therefore:

`PreviewImpression != Access`

and

`Access != Attention != Encoding != Belief != EngageIntent != Share`.

The headline itself remains an observed stimulus even when the user does not click. A failed access gate must not be interpreted as zero cognitive exposure to the headline.

## 3. Terminology correction: access gate, not generic “attention gate”

The literature motivating this release uses several related but non-identical observables.

Robertson et al. (2023) directly measure click-through rate:

`CTR = clicks / impressions`

This is an **access / selection** observable. It does not directly measure gaze allocation, depth of processing or article completion.

Shulman, Markowitz & Rogers (2024) provide two complementary layers of evidence:

1. large-scale field experiments showing that simpler headlines receive more clicks;
2. a follow-up signal-detection experiment in which simpler headlines also produce stronger later recognition, interpreted as greater attention and processing.

The architecture should therefore keep access and internal attention conceptually separate. Alpha 0.4.2a0 should implement only the directly observed access gate. A later model may add an attention/encoding state if it has its own empirical target and rejection criterion.

## 4. Primary empirical anchor — Robertson et al. 2023

Reference:

Robertson, C. E., Pröllochs, N., Schwarzenegger, K., Pärnamets, P., Van Bavel, J. J. & Feuerriegel, S. (2023). “Negativity drives online news consumption.” *Nature Human Behaviour*, 7, 812–822.

DOI: https://doi.org/10.1038/s41562-023-01538-4

Design:

- Registered Report.
- Upworthy randomized headline experiments.
- 22,743 RCTs in the archive.
- Approximately 105,000 headline variations.
- Approximately 5.7 million clicks.
- More than 370 million impressions.
- Confirmatory analyses compare variants belonging to the same underlying news story.

Primary target:

A higher proportion of negative words in a headline increases click propensity.

The paper reports that, for a headline of average length, one additional negative word is associated with an approximately 2.3% increase in click-through rate.

Important boundary:

The published magnitude is validation context only. Alpha 0.4.2a0 must **not** translate “2.3% per word” directly into a CEM coefficient unless a separately justified scale mapping and calibration procedure are introduced.

Additional robustness relevant to model design:

- the negative-language direction survives controls for headline length and complexity;
- robustness checks excluding image-changing experiments produce nearly identical conclusions;
- positive wording shows an opposite average association in the registered analysis.

Limits:

- Upworthy was an unusual and historically specific click-oriented publisher;
- the experiments were run in 2013–2015;
- headline variants were not guaranteed to be perfectly semantically equivalent;
- CTR is not reading completion or belief change;
- the dataset is aggregated at headline level rather than individual-user level.

## 5. Supporting registered evidence — Gligorić et al. 2023

Reference:

Gligorić, K., Lifchits, G., West, R. & Anderson, A. (2023). “Linguistic effects on news headline success: Evidence from thousands of online field experiments.” *PLOS ONE*, 18(3), e0281682.

DOI: https://doi.org/10.1371/journal.pone.0281682

This registered report also analyzes the Upworthy archive and finds that negative emotion words, headline length and several linguistic features predict headline success.

It is **not an independent replication** of Robertson et al. because both use the same underlying experiment archive. It should therefore be registered as convergent analysis / methodological support rather than counted as a second independent empirical anchor.

Its useful contribution for CEM is the explicit same-article / same-image comparison logic used when constructing comparable headline pairs.

## 6. Independent support for a cue-sensitive access stage — Shulman et al. 2024

Reference:

Shulman, H. C., Markowitz, D. M. & Rogers, T. (2024). “Reading dies in complexity: Online news consumers prefer simple writing.” *Science Advances*, 10(23), eadn2555.

DOI: https://doi.org/10.1126/sciadv.adn2555

Evidence relevant to the architecture:

- more than 30,000 headline field experiments were analyzed across The Washington Post and Upworthy;
- simpler headlines received more clicks than more complex variants;
- The Washington Post component supplies an independent traditional-newsroom dataset;
- a preregistered follow-up signal-detection experiment found greater recognition/sensitivity for simpler headlines among general readers.

Interpretation for M1.E3:

This study supports the idea that **access selection is cue-sensitive** and that headline features can influence both clicking and, separately, internal processing.

However, Alpha 0.4.2a0 should not add a “simplicity coefficient.” Simplicity is retained as an external architecture check demonstrating that the access gate should not be defined as “the negativity mechanism.”

## 7. Background architecture evidence — exposure is not engagement

Two large-scale studies support preserving multiple stages in the information funnel.

González-Bailón et al. (2023), *Science*:
https://doi.org/10.1126/science.ade7138

The study distinguishes potential exposure, actual exposure after curation, and later engagement on Facebook.

Robertson et al. (2023), *Nature*:
https://doi.org/10.1038/s41586-023-06078-5

The study distinguishes URLs shown in Google Search from URLs users select.

These sources are **BACKGROUND_THEORY** for stage separation. They do not calibrate the headline-access mechanism and must not be used to infer political behavior in CEM.

## 8. Descriptive ecosystem evidence — not a causal target

Nickl, Moussaïd & Lorenz-Spreen (2025), “The evolution of online news headlines,” *Humanities and Social Sciences Communications*:
https://doi.org/10.1057/s41599-025-04514-7

Across roughly 40 million headlines, the authors find long-run increases in several features previously associated with clickbait style or higher CTR, including negativity.

This is descriptive production-side evidence. It should not be registered as causal evidence that negativity increases individual clicking.

## 9. Proposed entities and quantities

### HeadlinePreview

A preview object shown to the agent before full-content access.

Minimum fields for the reference experiment:

- one stable underlying article/story identifier;
- headline text or abstract feature representation;
- headline negativity cue;
- optional fixed image identifier;
- factual-compatibility flag;
- one preview impression.

The initial candidate should not require a realistic natural-language generator.

### Hneg — Headline negativity cue

Ontology role: CONTENT_ATTRIBUTE.

Reference interpretation:

A bounded or standardized representation of negative wording in the headline.

It is not:

- article truth;
- article factuality;
- issue valence;
- editorial-selection score;
- emotion experienced by the agent;
- political orientation;
- misinformation.

The exact numerical encoding must be chosen during implementation and documented. The first model should prefer the simplest encoding that can express the registered differential prediction.

### Paccess — Access probability

Ontology role: DERIVED_METRIC / latent action probability.

Definition:

Probability of opening/clicking the full item after one registered preview impression.

It is not:

- M0 Share probability;
- M1.E2 Pengage;
- attention;
- reading duration;
- comprehension;
- belief;
- endorsement;
- population CTR.

### Access

Ontology role: OBSERVABLE.

Reference binary outcome:

- open/click;
- no open/click.

Pattern validation should be based primarily on Paccess contrasts rather than stochastic one-draw outcomes.

### PreviewImpression

Ontology role: OBSERVABLE / EVENT.

Definition:

The preview/headline was rendered to the synthetic agent.

Important boundary:

An impression means only that the preview is available/visible under the reference task. It does not prove visual fixation, reading, encoding or recall.

## 10. Minimal candidate model

### M1.E3-NULL — access insensitive to headline negativity

Reference form:

`logit(Paccess) = b0`

Prediction:

Headline variants converge when the negativity cue is normalized away.

### M1.E3-A — negativity-sensitive access gate

Reference form:

`logit(Paccess) = b0 + beta_neg × Hneg`

Differential prediction:

For the same underlying article and reference impression context:

`higher Hneg → higher Paccess`

The coefficient is initially a **demonstrative reference value**, not a fitted estimate of the Robertson effect.

No additional mediator is required for Alpha 0.4.2a0.

In particular, the model must not introduce hidden states called “threat,” “arousal,” “interest” or “attention” merely to explain the sign of beta_neg. Those are candidate explanations in the broader literature, not uniquely identified mediators in the headline experiments.

## 11. Required invariants in the reference comparator

To attribute the difference to the candidate headline cue, the comparator must hold fixed:

- underlying article/story;
- full article content;
- factual compatibility;
- preview opportunity / impression count;
- image, if an image is shown;
- agent state;
- source identity;
- editorial-selection condition;
- M1.E2 congruence state;
- downstream M0 states before access.

The negative and comparison headline variants do **not** need to be claimed as perfectly semantically identical unless the stimuli actually satisfy that stronger constraint.

## 12. Registered validation patterns to add during implementation

### VAL.M1.004 — Headline negativity access differential

Holding the underlying article, source, impression opportunity and other registered conditions fixed, a headline with the higher registered negativity cue produces higher Paccess.

### VAL.M1.N04 — Access-gate null

When beta_neg is disabled or Hneg is normalized, the otherwise identical headline conditions converge in Paccess.

### VAL.M1.N05 — Access is not downstream cognition

Changing Hneg or Paccess must not directly mutate:

- M0 belief B;
- M0 Share;
- M1.E1 Aissue;
- M1.E2 Pengage / EngageIntent.

Any future propagation from full-content access into those states requires an explicit later integration contract.

### VAL.M1.N06 — Non-click still preserves headline exposure

When Access = 0, the model must not erase the PreviewImpression or imply that the headline was never observed.

This prevents the access gate from silently becoming an all-or-none exposure gate.

## 13. Model-discrimination question

The scientific question for Alpha 0.4.2a0 is intentionally narrow:

> Does adding a headline-cue-sensitive access stage produce a registered access differential that the current model, which has no explicit click/open gate, cannot represent without changing another causal stage?

The release is justified only if the answer is yes while M0, M1.E1 and M1.E2 remain unchanged in their own reference tests.

## 14. Rejection or revision criteria

Reject or revise M1.E3 if any of the following occurs:

- the observed contrast can only be produced by changing the underlying article rather than the preview cue;
- the implementation changes impression counts between conditions;
- the effect is created through hidden changes in source, agent state, editorial selection or M1.E2 congruence;
- Access is reported as attention, reading completion, comprehension, belief or endorsement;
- a non-click is represented as if the headline had never been exposed;
- beta_neg is presented as empirically calibrated from the reported 2.3% figure without an explicit scale mapping and fitting procedure;
- the same registered differential is already trivially produced by an existing M1.E2 parameter under identical observables, making the new stage non-identifiable;
- adding M1.E3 alters retained M0, M1.E1 or M1.E2 reference outputs outside a separately approved integration experiment;
- the reference comparator cannot keep the underlying story and other registered conditions invariant;
- empirical review shows that the negativity direction is too platform-specific to support even a bounded candidate demonstration.

## 15. Mechanisms explicitly deferred

Alpha 0.4.2a0 should not implement:

- a generic internal attention state;
- gaze duration or fixation;
- reading completion;
- comprehension;
- memory/encoding dynamics;
- curiosity-gap mechanisms;
- linguistic simplicity as a second executable coefficient;
- arousal, fear or threat as required mediators;
- platform recommendation/ranking;
- social-network amplification;
- stable user ideology or partisan identity;
- personalized click propensity fitted to individual users;
- integrated downstream belief effects of clicking.

Each of these requires a distinct observable target and rejection criterion.

## 16. Proposed causal placement

The explanatory chain should become:

`information pool`
→ `editorial selection (M1.E1)`
→ `preview/headline rendered`
→ `PreviewImpression`
→ `headline access gate (M1.E3)`
→ `Access`
→ `full-content availability for later processing`

M1.E2 should remain a separate presentation/engagement experiment rather than being silently forced into this chain until an explicit integration study defines their ordering in a shared task.

This is important: Alpha 0.4.2a0 adds a separable experiment, not a claim that every current M1 comparator is already one fully integrated causal pipeline.

## 17. UI / explanatory design

Do not add a new top-level tab.

Extend **Understanding → Mechanisms** with a separate M1.E3 between-condition comparator.

The comparator should show:

- one fixed underlying article/story;
- one fixed source;
- one fixed image or no image in both conditions;
- two controlled headline variants;
- Hneg for each variant;
- one PreviewImpression per condition;
- exact Paccess values;
- NULL versus negativity-gate comparison;
- the empirical target and its limitations;
- a stage diagram making `impression → access` explicit;
- a warning that `Access != attention != belief != sharing`.

No temporal curve should be introduced unless a later empirical design is explicitly temporal.

## 18. Evidence-registration rule

The evidence registry must distinguish:

- PRIMARY_MODEL_EVIDENCE:
  - Robertson et al. 2023 negativity → CTR;
- CONVERGENT_SAME_DATASET:
  - Gligorić et al. 2023;
- INDEPENDENT_BACKGROUND / ARCHITECTURE_SUPPORT:
  - Shulman et al. 2024;
- BACKGROUND_THEORY for stage separation:
  - González-Bailón et al. 2023;
  - Robertson et al. 2023 Google Search;
- DESCRIPTIVE_CONTEXT:
  - Nickl et al. 2025.

The Upworthy Scientific Data archive should be registered as data provenance:

Matias, Munger, Le Quere & Ebersole (2021):
https://doi.org/10.1038/s41597-021-00934-7

No source should be counted twice as if two analyses of the same archive were independent replications.

## 19. Evidence snapshot rule

Implementation of Alpha 0.4.2a0 will change the evidence set and therefore must not reuse:

`EVIDENCE.M1.2026-09-15.r2`

A new immutable evidence snapshot must be generated when references and empirical targets are actually registered.

Planning documents alone do not change the evidence snapshot.

## 20. Release acceptance criteria

Alpha 0.4.2a0 is releasable only when:

- the empirical references and their source roles are registered correctly;
- same-archive analyses are not labeled as independent replication;
- Hneg, Paccess, Access and PreviewImpression have explicit ontology roles;
- M1.E3-NULL and M1.E3-A are executable and compared;
- VAL.M1.004, VAL.M1.N04, VAL.M1.N05 and VAL.M1.N06 pass;
- the underlying story, source, impression opportunity and other comparator invariants remain fixed;
- Paccess is kept separate from Pengage, Share and belief;
- non-click does not erase headline exposure;
- no published effect size is silently used as a fitted coefficient;
- all retained M0, M1.E1 and M1.E2 scientific regression tests remain green;
- ODD, TRACE, CLAIMS, EVIDENCE, Theory and HANDOFF are updated;
- the Understanding comparator is bilingual, keyboard-accessible and responsive;
- canonical exports reproduce byte-for-byte;
- Python, registry validation, TypeScript/Vite and Playwright pass;
- release artifact provenance remains valid.

## 21. What would come after M1.E3

Only after the access gate is stable should the project consider an internal attention/encoding mechanism.

The strongest current candidate evidence for that later stage is the Shulman et al. signal-detection result showing stronger recognition for simpler headlines among general readers.

Such a later mechanism would need to answer a different question:

`conditional on a rendered or accessed item, what determines depth of processing / encoding?`

That is not the question answered by Alpha 0.4.2a0.

## 22. Planning sources

Primary causal target:

- Robertson et al. (2023), *Nature Human Behaviour*:
  https://doi.org/10.1038/s41562-023-01538-4

Same-archive registered support:

- Gligorić et al. (2023), *PLOS ONE*:
  https://doi.org/10.1371/journal.pone.0281682

Independent field and attention support:

- Shulman, Markowitz & Rogers (2024), *Science Advances*:
  https://doi.org/10.1126/sciadv.adn2555

Exposure/access/engagement stage separation:

- González-Bailón et al. (2023), *Science*:
  https://doi.org/10.1126/science.ade7138
- Robertson et al. (2023), *Nature*:
  https://doi.org/10.1038/s41586-023-06078-5

Descriptive ecosystem context:

- Nickl, Moussaïd & Lorenz-Spreen (2025):
  https://doi.org/10.1057/s41599-025-04514-7

Dataset provenance:

- Matias et al. (2021), *Scientific Data*:
  https://doi.org/10.1038/s41597-021-00934-7

## 23. Immediate next step after approval of this contract

Do **not** implement the mechanism immediately.

First perform a Phase A-style data/evidence contract on a new implementation branch:

1. register source roles and the new empirical target;
2. define the exact Hneg encoding and comparator stimuli;
3. define Paccess / Access / PreviewImpression schemas;
4. register the four validation patterns and nulls;
5. verify that existing M1.E2 terminology cannot collide with the new access observable;
6. add schema and invariant tests before adding equations or UI.

Only after those gates pass should M1.E3-NULL and M1.E3-A be implemented.
