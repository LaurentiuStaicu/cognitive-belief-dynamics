# Initial evidence audit — 2026-09-13

This is a bounded bibliographic check of the three currently registered links,
not an exhaustive or systematic literature review, a replication, or calibration.
Bibliography and access scope live in `model/references.json`; bilingual findings
and model-specific limitations live in `model/links.json` and are displayed in the
browser. DOI links identify papers; consulted-source links show the text accessed.

## Separate the levels of support

The earlier `mechanism_evidence_status` field mixed evidence about a phenomenon
with evidence for a particular implementation. All three exact M0 mechanisms are
now marked `CANDIDATE`; the experimental or meta-analytic label is recorded
separately as `phenomenon_evidence_status`. `REFERENCE_CANDIDATE` continues to
identify the chosen functional forms. These labels are not interchangeable.

| Registered link | Reference | Scope of support for M0 |
| --- | --- | --- |
| Exposure → familiarity | Hasher et al. (1977), DOI 10.1016/S0022-5371(77)80012-1 | Indirect background for the latent familiarity state; its update equation is a modelling choice. |
| Familiarity → belief | Dechêne et al. (2010), DOI 10.1177/1088868309352251 | Phenomenon-level synthesis; not an estimate of this implementation’s coefficient. |
| Accuracy salience → sharing | Pennycook et al. (2021), DOI 10.1038/s41586-021-03344-2 | Intervention-level evidence; not direct measurement of latent W. |

The mechanistic classifications above are this project's assessment of the
source-to-model mapping, not classifications supplied by the cited authors.
The graph’s CAUSAL/MODERATING labels describe proposed model relationships;
they should be read together with their candidate status and limitations.

## Reading scope and provenance

The author-hosted abstracts were consulted for Hasher and Pennycook. For Dechêne,
the abstract and selected mechanism sections of an author-affiliated
PDF were consulted. The publisher's Nature page was unavailable in this session;
the MIT-hosted publication abstract supplied the relevant description. These
access limits are recorded per reference and are visible in the interface.

No source files are copied into this repository. Summaries are original and short.
The DOI records and source pages are linked for inspection. This audit does not
claim to have assessed all later replications, moderators or corrections.

## What changed and what did not

Only registries, validation rules, evidence presentation and documentation changed.
No agent update, equation, parameter or saved numerical reference run changed.
The first two links relate to the same broader repetition literature and must not
be counted as two independent validations of the complete causal chain.

The current graph remains incomplete relative to the executable model. Correction,
source learning and the full sharing equation need additional registered links and
separate evidence reviews. A complete ODD description, measurement mapping and
out-of-sample calibration remain future work.


## Alpha 0.4 M1 evidence extension — 2026-09-15

The evidence registry now includes `REF.TOHIDI.2025` and two candidate M1 links:
`Eedit → Sobs` and `Sobs → Aissue`. The empirical benchmark is stored separately
in `model/empirical_targets.json` so published treatment effects cannot silently
become simulator parameters.

Tohidi, Haider & Watts (2025), DOI 10.1038/s41598-025-29519-9, report a
preregistered randomized experiment with 2,141 recruited participants and seven
events. Their synthetic positive, neutral and negative articles were constructed
by selecting factually accurate information according to tone while preserving
comparable content composition. Negative framing produced substantially more
negative feelings and opinions than neutral framing.

For the Cognitive Epistemic Model this source supports the **phenomenon-level
directional target**: factually accurate presentations with different emphases can
produce different downstream evaluations. It does **not** directly validate the
scalar `Eedit`, `Sobs` or `Aissue` states, the deterministic reference
selection rule, or the bounded linear appraisal gain.

The paper explicitly notes that its treatment effect combines information
selection with tone variation. Consequently, Alpha 0.4.0a0 must not describe
`LINK.EDITORIAL.OBSERVED_SAMPLE` or `LINK.OBSERVED_SAMPLE.APPRAISAL` as uniquely
identified psychological mechanisms. Their exact mechanism status remains
`CANDIDATE` and their functional forms remain `REFERENCE_CANDIDATE`.

Published magnitudes such as the negative-vs-neutral feeling effect (-18.5
percentage points; 95% CI [-21.2, -15.8]) and the opinion-index effect (-17.94
percentage points; 95% CI [-21.76, -14.11]) are validation context only. The M1
appraisal gain is not fitted to those values.

The registered nested-null constraint is part of the evidence-to-model mapping:
when editorial selection is disabled, all model conditions receive the same full
fact-compatible pool and the simulated condition difference must disappear. This
is a model-discrimination constraint, not a claim made by the cited authors.

The M0 evidence audit above remains applicable to the retained M0 baseline.


## Alpha 0.4.1 M1.E2 evidence extension — 2026-09-15

The evidence registry adds `REF.ARUGUETE.2024` and `REF.ALVARADO.2026`.
Published results are stored separately in `model/empirical_targets.json` and are
not used as simulator coefficients.

Aruguete et al. (2024), DOI 10.1038/s41598-024-53337-0, report randomized
confirmation/refutation fact-check experiments in Argentina, Brazil, Chile and
Colombia with 9,512 adult respondents. Confirmation and refutation conveyed
semantically equivalent, factually accurate content. Aggregate active engagement
was higher under confirmation in all four countries: +18.2 pp in Argentina and
approximately +13, +15 and +14 pp in Brazil, Chile and Colombia. Likes were
consistently higher; share alone was statistically significant only in Argentina.

For CEM this supports the phenomenon-level target that presentation frame can
change active-engagement propensity while semantic content and factual
compatibility remain fixed. It does not justify replacing M0 Share with an
aggregate engagement outcome.

Alvarado, Aruguete & Calvo (2026), DOI 10.1057/s41599-026-08888-0, report a
nationally representative Argentina survey experiment with 2,075 recruited adults.
The supplemental interaction model uses N=1,901 complete regression cases.
The Confirmation × Partisan Congruence coefficient for aggregate engagement is
0.124 (SE 0.040, p<0.001); the confirmation main effect for counter-attitudinal
respondents is -0.010 (SE 0.025). The interaction is also positive for likes
(0.130) and shares (0.068).

CEM generalizes this only into a task-specific `Gatt` relation between prior stance
and message stance. The model does not infer a stable ideology or party identity.
The reference logistic coefficients are demonstrative and not estimated from the
published regressions.

The 2024 article reports no evidence for a simple cognitive-difficulty explanation,
and the 2026 article shows that affective penalties of negation do not reliably map
onto behavioral engagement. Alpha 0.4.1 therefore does not require either mediator.

The evidence snapshot advances to `EVIDENCE.M1.2026-09-15.r2`; the revision suffix
prevents one identifier from referring to two different evidence sets on the same date.


## Alpha 0.4.2 M1.E3 evidence extension — 2026-09-16

M1.E3 adds a bounded headline-access candidate between a registered preview
impression and a click/open outcome. The active registry adds
`REF.ROBERTSON.2023.NEGATIVITY`, the Upworthy archive descriptor and 2024
correction, plus `REF.NICKL.2025.ATTENTION_ECONOMY` as preliminary
counterevidence.

Robertson et al. (2023), DOI 10.1038/s41562-023-01538-4, is a Registered Report
using Upworthy headline A/B tests. In the filtered confirmatory sample the main
Results text reports 12,448 RCTs, 53,699 headlines, more than 205 million
impressions and 2,778,124 clicks. The source models clicks conditional on
impressions with a multilevel binomial logistic model and reports a positive
standardized coefficient for negative-word proportion (beta=0.015; 99% CI
0.013–0.018). For an average-length headline the authors report an approximate
2.3% CTR increase per additional negative word.

CEM uses only the **directional target** `higher Hneg → higher Paccess`.
The model's `Hneg` is a precomputed binary controlled condition, not the source
study's continuous LIWC-based predictor. The reference logistic intercept and
`beta_hneg` are demonstrative and are not fitted to either 0.015 or 2.3%.

The article contains a small internal count discrepancy: the main Results text
reports 53,699 headlines, while two figure captions report 53,669. The active
target records the main-text count and preserves the discrepancy in its
`count_note` rather than silently choosing a different number.

The Upworthy Research Archive Author Correction (Matias et al. 2024,
DOI 10.1038/s41597-024-03600-w) reports likely randomization problems in tests
fielded from 25 June 2013 through 10 January 2014 and recommends excluding that
period from causal analysis. The archive maintainers subsequently report that the
Robertson analysis was re-run on tests they considered reliable and that the main
results were nearly indistinguishable. The correction and reanalysis are
provenance/integrity context, not independent replication.

Nickl, Hills & Lorenz-Spreen (2025 preprint; same project presented at APS 2026)
is registered as preliminary counterevidence rather than hidden. The APS abstract
reports no expected negativity-bias effect in its different two-stage experiment.
This blocks a universality claim even though it does not overturn the much larger
registered Upworthy result.

The M1.E3 functional form remains a **REFERENCE_CANDIDATE**. Its first comparator
uses a NULL model versus a cue-sensitive logistic model because the source study
itself uses a binomial-logit analysis for click probability; CEM does not claim
that its binary cue, intercept or coefficient reproduces the source model.

`PreviewImpression`, `Access`, attention, belief, active-engagement intent and
sharing remain separate constructs. In particular, `Access=0` does not erase
the prior headline impression.

The evidence snapshot advances to `EVIDENCE.M1.2026-09-16.r1`.
