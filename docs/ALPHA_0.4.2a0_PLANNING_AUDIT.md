# Alpha 0.4.2a0 — planning audit for M1.E3 Headline Access Gate

Status: **planning architecture accepted; executable cue deliberately unresolved pending Phase A**.

Audited on: 2026-09-16

This audit evaluates `docs/ALPHA_0.4.2a0_PLAN.md` before any executable
equation, model variable, registry mutation or user-interface component is added.

## 1. Audit question

The planning contract must answer two separate questions:

1. Is an explicit `PreviewImpression → Access/click` stage scientifically and
   architecturally justified?
2. Which headline cue, if any, is sufficiently well supported and reproducible
   to become the first executable M1.E3 candidate?

The first question can be accepted before the second is resolved.

## 2. Result

### Architecture: PASS

The evidence supports treating access/click as a distinct observable stage.

The accepted distinction is:

`PreviewImpression != Access != Attention != Encoding != Belief != EngageIntent != Share`

This is compatible with the Upworthy archive, which records assignments/impressions
and clicks as distinct variables, and with later work distinguishing headline
selection from recognition/processing.

The new stage is also non-redundant with M1.E2. M1.E2 models active engagement
intent under semantically equivalent confirmation/refutation presentation and
task-specific congruence. M1.E3 models whether a rendered headline preview is
opened/clicked. Different observables, different empirical tasks and different
null tests are therefore required.

### Cue selection: HOLD for Phase A

No headline cue is approved for executable implementation by this planning PR.

Phase A must compare Candidate N (negativity) and Candidate S (simplicity) using
predeclared evidence and reproducibility criteria and select exactly one or reject
both.

## 3. Candidate N — headline negativity

### Strengths

- Robertson et al. (2023) is a Registered Report using large-scale Upworthy
  randomized headline experiments.
- The registered direction is clear: more negative wording predicts greater click
  propensity within same-story headline tests.
- The Upworthy archive is publicly available and licensed CC BY 4.0, supporting
  independent reproduction.
- After the 2024 Upworthy archive correction identified a period with likely
  randomization problems, the archive maintainers report that the Robertson
  analysis was re-run on tests considered reliable and the main findings were
  nearly identical.
- Qiu & Golman (2024) provide cross-context predictive support from WeChat,
  although not randomized causal replication.

### Weaknesses / boundaries

- The main causal evidence remains concentrated in one historical platform and
  period: Upworthy, 2013–2015.
- The 2.3% figure is context- and scale-specific and cannot be copied into a CEM
  coefficient.
- A 2025 Nickl–Hills–Lorenz-Spreen preprint, later presented at APS 2026,
  reports no expected negativity-bias effect in a different two-stage experiment.
  This is preliminary evidence, but it blocks a universality claim.
- Sentiment operationalisation in the original work relies partly on licensed
  dictionary tooling; runtime reproduction therefore needs an explicit open or
  precomputed strategy.

## 4. Candidate S — headline simplicity

### Strengths

- Shulman, Markowitz & Rogers (2024) analyze headline field experiments from two
  distinct publisher contexts: The Washington Post (2021–2022) and Upworthy
  (2013–2015).
- The Washington Post component is independent of the Upworthy archive and much
  more recent than the Upworthy experiments.
- A preregistered follow-up signal-detection experiment separates the click
  result from later recognition/processing, supporting the architectural
  distinction between access and internal processing.
- The simplicity construct is explicitly decomposed into common words,
  readability, analytic writing and character count.

### Weaknesses / boundaries

- The Washington Post Study Set 1 data are restricted by a data-use agreement
  and cannot be redistributed publicly.
- The composite simplicity index includes LIWC-derived components. LIWC is
  licensed software and cannot be redistributed as an open runtime dependency.
- Some component behavior differs across publisher datasets; the composite must
  therefore not be treated as a universal psycholinguistic constant.
- A 2025 news-aggregator field experiment found no significant effect from
  reducing article-text complexity. This is not a direct headline replication,
  but it limits generalization from headline simplicity to all forms of
  accessibility.

## 5. Evidence independence audit

The following pairs must **not** be counted as independent replications:

- Robertson et al. (2023) and Gligorić et al. (2023): both analyze the Upworthy
  Research Archive.
- Nickl et al. (2025 preprint) and the APS 2026 abstract: the same underlying
  two-stage project.
- The Upworthy portion of Shulman et al. (2024) and other Upworthy analyses:
  same source archive, even when the research question differs.

Independent evidence relevant to the cue-selection decision includes:

- Washington Post headline experiments in Shulman et al. for simplicity;
- WeChat observational/predictive data in Qiu & Golman for negativity/context;
- the Nickl two-stage experiment as preliminary counterevidence;
- the Mattis/Heitz news-aggregator experiment as a context boundary rather than
  a direct headline-simplicity replication.

## 6. Data integrity audit

The Upworthy Research Archive published an Author Correction in 2024 describing
likely randomization problems from 25 June 2013 to 10 January 2014.

Phase A must record:

- the archive correction;
- the reliable-test filtering rule or provenance used in any reproduction;
- the archive maintainers' report that the Robertson negativity results were
  robust to reliable-test reanalysis;
- the fact that an old analysis over the full archive and a corrected analysis
  are not two independent studies.

No new empirical target should cite “Upworthy randomized experiments” without this
post-publication integrity context.

## 7. Reproducibility and licensing audit

The M1.E3 implementation must remain reproducible without shipping restricted
third-party dictionaries.

Phase A must choose between:

### Strategy A — precomputed cue metadata

Use fixed cue values/stimuli with provenance to a published or archived analysis.
Restricted source tools are not redistributed.

### Strategy B — open proxy

Define an open-source cue calculation and register it as a **proxy
operationalisation**, including the ways in which it differs from the published
LIWC-based construct.

An open proxy is not an exact replication unless equivalence is separately shown.

The same rule applies to restricted Washington Post data: the published result can
serve as evidence, but non-public source data cannot become a hidden dependency of
the CEM build.

## 8. Separation from M1.E2

M1.E2 and M1.E3 both involve information presentation but are not the same
mechanism.

M1.E2:
- manipulates confirmation/refutation presentation of semantically fixed content;
- uses prior-attitude congruence;
- outcome: `Pengage / EngageIntent`;
- empirical anchors: survey experiments.

M1.E3:
- manipulates or characterizes a headline-level access cue;
- outcome: `Paccess / Access`;
- empirical anchors: headline field experiments / click behavior;
- non-click preserves the `PreviewImpression`.

Therefore Phase A must reject any schema or UI design that aliases `Access` to
`EngageIntent` or `Share`.

## 9. Phase A cue-selection criteria

Before a cue can be frozen, Phase A must produce a transparent comparison on:

1. construct validity;
2. observable match to `Access`;
3. causal identification;
4. independence/diversity of evidence;
5. context robustness and counterevidence;
6. data availability;
7. licensing/open reproducibility;
8. operationalisation stability;
9. comparator invariants;
10. ability to define a discriminating null and rejection criterion.

No weighted score is required. If criteria point in different directions, the
decision must state the trade-off explicitly.

## 10. Planning verdict

**GO for M1.E3 as an access-stage architecture.**

**NO GO yet for either Hneg or Hsimp as an executable variable.**

The planning contract may be merged as the scientific scope boundary for
Alpha 0.4.2a0. The next branch must be Phase A evidence/schema only.

Phase A may add/extend schemas, reference metadata, empirical-target structures,
validation-pattern declarations and invariant tests. It must not add the M1.E3
access equation, runtime mechanism or UI comparator.

## 11. Sources audited

- Robertson et al. (2023), Nature Human Behaviour:
  https://doi.org/10.1038/s41562-023-01538-4
- Matias et al. (2021), Scientific Data, Upworthy Research Archive:
  https://doi.org/10.1038/s41597-021-00934-7
- Matias et al. (2024), Author Correction:
  https://doi.org/10.1038/s41597-024-03600-w
- Upworthy Research Archive reliability update:
  https://upworthy.natematias.com/2024-06-upworthy-archive-update.html
- Gligorić et al. (2023), PLOS ONE:
  https://doi.org/10.1371/journal.pone.0281682
- Shulman, Markowitz & Rogers (2024), Science Advances:
  https://doi.org/10.1126/sciadv.adn2555
- Qiu & Golman (2024), Applied Cognitive Psychology:
  https://doi.org/10.1002/acp.4195
- Nickl, Hills & Lorenz-Spreen (2025), PsyArXiv:
  https://doi.org/10.31234/osf.io/ntsg9_v1
- APS 2026 presentation of the same Nickl project:
  https://www.psychologicalscience.org/conventions/archive/2026annual/paper/61983/
- Mattis & Heitz (2025), Journal of Communication:
  https://doi.org/10.1093/joc/jqaf030
