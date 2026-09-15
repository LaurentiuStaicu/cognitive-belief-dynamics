# ODD extension — M1.E3 Headline Access Gate

Software version described: Alpha 0.4.2a0 development branch (unreleased)  
Active model specification: M1  
Retained baseline: M0  
Status: candidate, uncalibrated model-discrimination extension

This document describes the first executable M1.E3 backend comparator. M1.E1
remains documented in `docs/ODD_M1.md`, M1.E2 in `docs/ODD_M1_E2.md`, and the
retained M0 baseline in `docs/ODD_MAIN.md`.

No M1.E3 user-interface comparator is introduced in this phase.

## 1. Purpose

M1.E3 adds one explicit stage between a rendered headline preview and access to
the fuller item:

`PreviewImpression → Paccess → Access`

The scientific question is deliberately narrow:

> Can a cue-sensitive access stage reproduce a registered headline-selection
> direction that the current model cannot represent explicitly, while preserving
> the retained M0, M1.E1 and M1.E2 reference outputs?

M1.E3 does not model attention, depth of reading, encoding, comprehension, belief,
endorsement or sharing.

## 2. Primary evidence and integrity context

The directional empirical target is Robertson et al. (2023), *Nature Human
Behaviour*, DOI 10.1038/s41562-023-01538-4.

The registered analysis uses randomized Upworthy headline tests and models clicks
conditional on impressions with a multilevel binomial-logit specification. In the
main Results text, the filtered confirmatory sample contains:

- 12,448 RCTs;
- 53,699 headline variants;
- more than 205 million impressions;
- 2,778,124 clicks.

The article reports a positive standardized negative-language coefficient
(beta=0.015, 99% CI 0.013–0.018) and an approximate 2.3% CTR increase per
additional negative word for an average-length headline.

Those magnitudes are stored as **context only**. They do not set the CEM
coefficient.

The article also contains a small count discrepancy: two figure captions report
53,669 headlines rather than the 53,699 stated in the main Results text. CEM
records the main-text count and preserves the discrepancy in target provenance.

The Upworthy archive Author Correction (Matias et al. 2024,
DOI 10.1038/s41597-024-03600-w) reports likely randomization problems in tests
from 25 June 2013 through 10 January 2014. The archive maintainers report that the
Robertson analyses remained nearly identical after restricting them to tests they
considered reliably randomized.

Nickl, Hills & Lorenz-Spreen (2025 preprint; same project presented at APS 2026)
is registered as preliminary counterevidence because that different experiment
did not find the expected negativity-bias effect.

Therefore M1.E3 treats the direction as a **context-bounded candidate**, not a
universal law of news consumption.

## 3. Entities and variables

### HeadlinePreview

One reference preview with fixed:

- underlying story ID;
- source ID;
- image ID;
- factual-compatibility flag;
- PreviewImpression.

The reference pair differs only in Hneg and headline ID.

### Hneg — Headline-negativity cue

Active ontology: `CONTENT_ATTRIBUTE`.

Reference encoding:

- `Hneg=0`: lower-negativity/control condition;
- `Hneg=1`: higher-negativity condition.

Hneg is a **precomputed controlled cue**.

It is not:

- a runtime sentiment analyser;
- a LIWC negative-word proportion;
- truth or factuality;
- misinformation;
- experienced emotion;
- political orientation;
- a calibrated effect-size scale.

### PreviewImpression

Active ontology: `OBSERVABLE`.

It records that the preview was rendered/available under the reference task.

It does not prove fixation, reading, attention, encoding or recall.

### Paccess

Active ontology: `DERIVED_METRIC`.

It is the latent probability of opening/clicking the full item conditional on one
registered PreviewImpression.

It is not observed population CTR and not M1.E2 Pengage or M0 Share probability.

### Access

Active ontology: `OBSERVABLE`.

Reference open/click outcome.

`Access=0` does not remove `PreviewImpression`.

## 4. Nested reference models

### M1.E3-NULL

`logit(Paccess) = b0`

Hneg is ignored.

### M1.E3-A — headline-negativity candidate

`logit(Paccess) = b0 + beta_hneg × Hneg`

Reference parameters:

- `b0 = -2.0`;
- `beta_hneg = 0.20`.

These values are deliberately demonstrative and uncalibrated.

They are not:

- the source coefficient 0.015;
- a transformation of the source's 2.3% CTR statement;
- population estimates;
- platform-specific fitted values.

With the current reference parameters:

- `Hneg=0 → Paccess ≈ 0.1192`;
- `Hneg=1 → Paccess ≈ 0.1419`.

Pattern validation uses the probability contrast, not the illustrative stochastic
Access draw.

## 5. Why a logistic reference form is reasonable but not identified

Robertson et al. model click counts as binomial with a logit link for CTR and
experiment-level heterogeneity.

CEM adopts only the broad Bernoulli/logit architecture because its synthetic
reference outcome is also binary.

CEM does **not** reproduce:

- the source's continuous standardized negative-language predictor;
- story-level random intercepts;
- varying slopes;
- headline-length, complexity or platform-age controls;
- the source coefficient scale.

The CEM functional form therefore remains `REFERENCE_CANDIDATE`, not
`EMPIRICALLY_ESTIMATED`.

## 6. Comparator invariants

The reference lower- and higher-Hneg conditions hold fixed:

- underlying story;
- source;
- image;
- factual compatibility;
- one preview impression;
- model parameters;
- agent/downstream state.

No M0, M1.E1 or M1.E2 variable is supplied to `access_probability()`.

This structural isolation is part of the negative constraint, not merely a
documentation statement.

## 7. Registered validation patterns

### VAL.M1.004 — Headline-negativity access differential

Under the selected candidate and fixed comparator invariants:

`Paccess(Hneg=1) > Paccess(Hneg=0)`.

### VAL.M1.N04 — Access-gate null

Under M1.E3-NULL:

`Paccess(Hneg=1) = Paccess(Hneg=0)`.

### VAL.M1.N05 — Access is not downstream cognition

The M1.E3 comparator must not directly mutate:

- M0 belief B;
- M0 Share;
- M1.E1 Aissue;
- M1.E2 Pengage;
- M1.E2 EngageIntent.

### VAL.M1.N06 — Non-click preserves headline exposure

A realized `Access=0` leaves `PreviewImpression=true`.

## 8. Observable boundary

The Upworthy archive distinguishes package impressions from clicks. M1.E3 keeps
the analogous model distinction explicit.

The following are not interchangeable:

`PreviewImpression != Access != Attention != Encoding != Belief != EngageIntent != Share`.

A click/open means only access under the reference task.

## 9. Evidence-to-model mapping

The active empirical target is
`TARGET.M1.E3.ROBERTSON_2023`.

It stores platform-native design quantities rather than fabricated participant
counts:

- number of experiments;
- headline variants;
- impressions;
- clicks.

The active empirical-target schema is backward-compatible with existing
participant experiments while adding `PLATFORM_AB_TEST_ARCHIVE` support.

The target also registers:

- data provenance;
- the archive-integrity correction;
- preliminary counterevidence.

## 10. Reproducibility and licensing

Runtime M1.E3 does not depend on LIWC, NRC or restricted Washington Post data.

The reference cue is stored directly as project-controlled metadata.

This is a deliberate abstraction from the source operationalisation and must not
be described as an exact LIWC replication.

## 11. Explicitly deferred

This phase does not implement:

- natural-language sentiment scoring;
- continuous Hneg;
- calibrated beta_hneg;
- internal attention;
- gaze/fixation;
- reading completion;
- memory/encoding dynamics;
- linguistic simplicity Hsimp;
- platform ranking;
- network amplification;
- integration of Access into downstream belief or sharing.

## 12. Rejection / revision criteria

Revise or reject the candidate if:

- the Hneg differential disappears under the selected implementation;
- the NULL model does not converge;
- comparator invariants differ between conditions;
- non-click removes the preview impression;
- M1.E3 changes retained M0/M1.E1/M1.E2 outputs;
- the demonstrative coefficient is described as empirically calibrated;
- future independent evidence materially contradicts the bounded direction;
- a smaller or more reproducible alternative cue provides better model
  discrimination.

## 13. Phase boundary

Phase B promoted the evidence/schema contract into an executable backend and
generated artifact while intentionally omitting user-facing M1.E3 presentation.

Phase C is stacked on that exact Phase B head and adds the bounded explanatory
surface required by the planning contract:

- Theory chapter 11 distinguishes preview impression, access and downstream
  cognition;
- the theory glossary exposes an executable `access` mechanism;
- Understanding → Mechanisms renders a bilingual NULL-versus-Hneg comparator;
- the comparator reads the deterministic `m1_access.json` export and does not
  introduce a second implementation of the equations;
- no temporal curve is introduced because the reference experiment is
  between-condition rather than longitudinal;
- no Access → belief / EngageIntent / Share propagation is added.

The comparator must display the fixed story, source, image and preview
opportunity, exact Paccess values, registered empirical target and limitations,
and the boundary:

`PreviewImpression != Access != Attention != Encoding != Belief != EngageIntent != Share`.

Phase C remains **unreleased and unmerged**. The public software metadata stays
at Alpha 0.4.1a1 until a separate Alpha 0.4.2a0 release-preparation branch
synchronizes version metadata and passes the complete scientific/software audit.
