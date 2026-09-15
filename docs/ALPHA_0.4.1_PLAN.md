# Alpha 0.4.1a0 planning contract — M1.E2 Presentation Framing × Prior-Attitude Congruence

Status: planning-only contract. No executable Alpha 0.4.1 mechanism is introduced by this document.

## Decision

The next candidate release is **Alpha 0.4.1a0**.

Working experiment name:

**M1.E2 — Semantic-equivalent Presentation Framing × Prior-Attitude Congruence**

This remains inside the Alpha 0.4 / M1 family. It is a distinct scientific extension,
but not large enough to justify Alpha 0.5.

Alpha 0.4.0a0 remains the retained M1.E1 baseline:

`fixed fact-compatible pool → editorial emphasis → observed sample → issue appraisal`

Alpha 0.4.1a0 should add the next separable stage:

`fixed selected semantic content → presentation frame → engagement intent`

with prior-attitude congruence tested as a moderator.

## Why this is the next extension

The project contract requires every executable addition to have:

1. an observed target phenomenon;
2. operationalisation;
3. a differential prediction relative to the smaller model;
4. a rejection/removal criterion.

The 2024 four-country confirmation/refutation experiment provides a strong
cross-context presentation-framing target using semantically equivalent statements:

- confirmation: `It is TRUE that p`;
- refutation: `It is FALSE that not-p`.

Across Argentina, Brazil, Chile and Colombia, confirmation increased aggregate
engagement. The effect was especially stable for likes; sharing and commenting
were substantially less consistent.

The 2026 Argentina election experiment adds a crucial heterogeneity result:
the confirmation advantage is concentrated among pro-attitudinal audiences.
Among counter-attitudinal audiences, neither frame produces meaningful extra
engagement.

Therefore Alpha 0.4.1 should not encode a universal framing coefficient. It should
compare a smaller frame-only model with a frame × congruence model.

## Empirical anchors

### REF candidate: Aruguete et al. 2024

Aruguete et al. (2024), Scientific Reports,
DOI: 10.1038/s41598-024-53337-0.

Design: four-country survey experiment, semantically equivalent confirmation and
refutation fact-check frames, 9,512 adult respondents.

Primary useful target for M1.E2:

- aggregate active engagement is higher for confirmation than refutation;
- likes show the most consistent country-level frame effect;
- share alone is not a robust universal outcome.

Interpretation boundary:

The study discusses cognitive-difficulty and affective-valence mechanisms, but its
results do not justify implementing one unique latent mediator. Reading-time
results do not support a simple "refutation is harder, therefore engagement is
lower" mechanism.

### REF candidate: Alvarado, Aruguete & Calvo 2026

Alvarado, Aruguete & Calvo (2026), Humanities and Social Sciences Communications,
DOI: 10.1057/s41599-026-08888-0.

Design: nationally representative Argentina survey experiment during the 2023
presidential runoff, N=2,075.

Primary useful target for M1.E2:

- pro-attitudinal / congruent messages generate the largest engagement gains;
- the confirmation advantage is concentrated among congruent audiences;
- counter-attitudinal messages show no meaningful additional engagement from
  either frame;
- negation has a modest affective penalty, but that penalty does not reliably map
  onto behavioral engagement.

Interpretation boundary:

Partisan identity is not required as a permanent agent trait in Alpha 0.4.1.
The executable construct should be relational and task-specific:
`prior stance × current message → congruence`.

## Model-comparison design

Alpha 0.4.1 should compare three nested models.

### M1.E2-NULL — presentation normalized

Semantic proposition and outcome remain fixed; presentation frame is removed.

Prediction:

`confirmation = refutation`

for active-engagement intent, conditional on the same congruence state.

### M1.E2-A — frame only

Reference form:

`P(engage) = logistic(b0 + beta_frame * Fpres)`

where `Fpres` encodes confirmation versus refutation.

Differential prediction:

`confirmation > refutation`

regardless of prior-attitude congruence.

This is the smallest model consistent with the aggregate 2024 pattern.

### M1.E2-B — frame × congruence

Reference form:

`P(engage) = logistic(b0 + beta_frame*Fpres + beta_congruence*Gatt + beta_interaction*Fpres*Gatt)`

where `Gatt` is a relational message–prior-attitude congruence state.

Differential prediction:

- confirmation advantage is larger for congruent/pro-attitudinal messages;
- confirmation advantage is small or approximately absent for
  counter-attitudinal messages.

This is the additional prediction suggested by the 2026 study.

## New executable quantities

Only the following new quantities are justified for the initial candidate.

### Fpres — Presentation frame

Ontology role: CONTENT_ATTRIBUTE or POLICY, to be decided during implementation
based on where the transformation is represented.

Reference values:

- confirmation;
- refutation.

What it is not:

- truth value;
- factuality;
- editorial selection;
- emotional valence itself.

### Gatt — Prior-attitude congruence

Ontology role: DERIVED_METRIC or STATE_FAST relation.

Definition:

Task-specific congruence between an agent's prior stance toward the proposition
and the current message content.

What it is not:

- stable ideology;
- party identity;
- personality;
- general confirmation bias score.

### Pengage — Active-engagement probability

Ontology role: DERIVED_METRIC / latent action probability.

Definition:

Probability of an active engagement response under the reference M1.E2 task.

What it is not:

- M0 Share;
- observed platform CTR;
- population engagement rate;
- endorsement.

### EngageIntent

Ontology role: OBSERVABLE.

Definition:

Reference binary or categorical outcome corresponding to an active stated response
such as like/share/comment versus ignore.

Important boundary:

`EngageIntent != Share`.

The 2024 study's strongest reproducible outcome is aggregate active engagement and
likes, while share alone is less consistent across countries. Alpha 0.4.1 must not
silently reinterpret aggregate engagement as M0 Share.

## Registered pattern tests to add

### VAL.M1.002 — Semantic-equivalent presentation framing

Holding proposition meaning, truth compatibility and selected content fixed,
confirmation framing should produce higher active-engagement propensity than
refutation framing in the relevant reference condition.

### VAL.M1.003 — Frame × prior-attitude congruence

The confirmation–refutation engagement contrast should be larger for congruent
messages than for counter-attitudinal messages.

### VAL.M1.N02 — Presentation-frame null

When presentation-frame variation is disabled, otherwise identical conditions
must converge.

### VAL.M1.N03 — Engagement intent is not M0 Share

An M1.E2 effect on aggregate engagement intent must not automatically modify or be
reported as the M0 Share process.

## Rejection criteria

Reject or revise M1.E2 if any of the following occurs:

- the frame-only model already reproduces the 2026 congruence interaction without
  an interaction term because of hidden condition changes;
- semantic content or truth compatibility differs between confirmation and
  refutation conditions;
- the effect is generated by directly changing agent stance instead of changing
  presentation frame;
- `Gatt` becomes a disguised stable ideology variable;
- M1.E2 requires rewriting M1.E1 or M0 rather than extending them;
- old M0 or M1.E1 registered pattern tests fail without an explicitly justified
  scope change;
- empirical evidence does not support a distinct prediction beyond the smaller
  model.

## Mechanisms explicitly deferred

The following should remain outside Alpha 0.4.1a0:

- cognitive difficulty as a required mediator;
- negative affect as a required mediator of engagement;
- platform ranking or recommendation algorithms;
- network amplification;
- attention/click gate;
- stable ideology or party identity as a general agent variable;
- heuristic-policy selection (MOD.15);
- Reflective Distance / Jungian individuation as numerical variables.

Reflective Distance remains interpretive because the historical project material
treats it as a convergence construct across multiple theoretical traditions rather
than a single settled measurable variable.

## UI / explanatory design

Do not add a new top-level tab.

Extend the existing Understanding architecture with a separate M1.E2
between-condition comparator.

The comparator should show:

- one fixed semantic proposition;
- confirmation and refutation forms side by side;
- a congruence toggle: congruent / counter-attitudinal;
- exact model outputs for `Pengage`;
- model comparison: NULL vs frame-only vs frame×congruence;
- the empirical target and its limitations;
- explicit warning that `EngageIntent` is not M0 Share.

No time-series metaphor should be used unless the empirical design is temporal.

## Evidence snapshot rule

The current evidence snapshot identity must not be reused after the evidence set
changes.

Alpha 0.4.1 should adopt an immutable snapshot identifier that can distinguish
multiple evidence changes on the same day, for example:

`EVIDENCE.M1.2026-09-15.r2`

or a content-derived suffix.

The exact scheme should be chosen once and then validated by schema.

## Release acceptance criteria

Alpha 0.4.1a0 is releasable only when:

- both empirical references are in the evidence registry;
- empirical targets are stored separately from model parameters;
- M1.E2-NULL, M1.E2-A and M1.E2-B are executable and compared;
- VAL.M1.002, VAL.M1.003, VAL.M1.N02 and VAL.M1.N03 pass;
- semantic equivalence and truth compatibility are invariant across frame
  conditions;
- M1.E1 outputs remain unchanged;
- all retained M0 tests remain green;
- ODD, TRACE, CLAIMS, EVIDENCE and handoff are updated;
- the Understanding comparator is keyboard-accessible and responsive;
- generated outputs reproduce byte-for-byte;
- Python, registry validation, TypeScript/Vite and Playwright all pass;
- release manifest and artifact provenance remain valid.

## Candidate follow-up

If Alpha 0.4.1 succeeds, the preferred next subversion is Alpha 0.4.2a0:
an attention/consumption gate anchored in large randomized headline experiments,
kept separate from editorial selection and presentation framing.

Key reference for that later gate:
Robertson et al. (2023), "Negativity drives online news consumption",
Nature Human Behaviour, DOI 10.1038/s41562-023-01538-4.

## Planning sources

- Aruguete et al. (2024), Scientific Reports,
  https://doi.org/10.1038/s41598-024-53337-0
- Alvarado, Aruguete & Calvo (2026), Humanities and Social Sciences Communications,
  https://doi.org/10.1057/s41599-026-08888-0
- Flusberg et al. (2024), Psychological Science in the Public Interest,
  https://doi.org/10.1177/15291006241246966
- Robertson et al. (2023), Nature Human Behaviour,
  https://doi.org/10.1038/s41562-023-01538-4
