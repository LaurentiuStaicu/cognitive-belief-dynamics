# Alpha 0.4.2a0 — Phase A evidence/schema contract for M1.E3

Status: **evidence/schema only — no executable M1.E3 mechanism and no UI**.

Date: 2026-09-16

Parent planning contract:

- `docs/ALPHA_0.4.2a0_PLAN.md`
- `docs/ALPHA_0.4.2a0_PLANNING_AUDIT.md`

Machine-readable Phase A contract:

- `model/contracts/m1_e3_evidence_contract.json`
- validated by `schemas/evidence_contract.schema.json`

## 1. Phase A purpose

Phase A turns the audited planning decision into a machine-checkable evidence
contract before the model acquires a new equation.

It must answer:

1. which cue is selected for the first bounded M1.E3 candidate;
2. which evidence supports, limits or challenges that selection;
3. how the cue can be represented reproducibly without restricted runtime
   dependencies;
4. how platform A/B evidence is represented without forcing it into participant
   trial fields such as `n_recruited`;
5. which quantities and validation patterns are reserved for a later executable
   phase;
6. which invariants must hold before any M1.E3 implementation can be accepted.

## 2. Cue-selection decision

### Selected for first executable candidate: Candidate N — Hneg

Phase A selects **headline negativity** as the first bounded cue for M1.E3.

This is not a claim that negativity is the strongest or most universal driver of
news access. It is a model-development decision based on the best combination of
minimality, open reproducibility and discriminating evidence.

Reasons:

- Robertson et al. (2023) is a Registered Report using a very large set of
  same-story headline field experiments.
- The Upworthy Research Archive is public under CC BY 4.0.
- The archive's 2024 randomization correction is known and can be explicitly
  represented in provenance.
- The archive maintainers report that the Robertson result remained nearly
  identical when rerun on tests considered reliable after the correction.
- The construct needed by a first reference model is relatively narrow:
  negative-language cue → access/click direction.
- Robertson reports robustness across alternative sentiment dictionaries, making
  the published direction less dependent on one exact dictionary implementation.
- The first CEM implementation can use **precomputed controlled cue metadata**
  rather than distributing a licensed sentiment dictionary.

### Deferred, not rejected: Candidate S — Hsimp

Headline simplicity remains scientifically important and is not removed from the
research programme.

Strengths that justify retaining it:

- independent Washington Post headline experiments from 2021–2022;
- convergent Upworthy results;
- preregistered follow-up evidence separating selection from later
  recognition/processing.

Reasons it is not the first executable cue:

- the published simplicity index is composite;
- some component behavior differs across publisher datasets;
- LIWC contributes to the operationalisation and cannot be redistributed as an
  open dependency;
- Washington Post Study Set 1 source data are restricted by a data-use agreement;
- using only an open subset or a newly invented simplicity proxy would require an
  additional operationalisation-validation step.

Candidate S remains a planned alternative and a future robustness/generalisation
test.

## 3. Selected operationalisation

Phase A freezes the **reference comparator encoding**, not the executable equation.

Selected strategy:

`PRECOMPUTED_CONTROLLED_CUE`

Reference cue:

`Hneg ∈ {0, 1}`

Interpretation:

- `Hneg = 0`: reference control / lower-negativity headline condition;
- `Hneg = 1`: reference higher-negativity headline condition.

This binary condition is a **directional abstraction** of the empirical construct.
It is not the original LIWC negative-word proportion and is not an empirical
effect-size scale.

The later executable phase may use this binary cue only for the registered
between-condition comparator unless a new contract explicitly approves a
continuous operationalisation.

### Why binary first

The first scientific question is model discrimination:

> Does an explicit access stage allow a controlled headline-cue difference to
> change access propensity while all upstream and downstream registered states
> remain fixed?

A binary cue is sufficient for that question and avoids false precision.

## 4. Runtime licensing boundary

M1.E3 runtime must not require redistribution of:

- LIWC software;
- LIWC dictionaries;
- NRC sentiment lexicons;
- restricted Washington Post data.

LIWC is licensed software and its dictionaries cannot be redistributed through
the open repository. NRC lexicons also prohibit redistribution under their stated
terms.

Phase A therefore permits evidence derived from those tools while requiring the
CEM reference comparator itself to use only project-owned/precomputed metadata.

No source lexicon is copied into the repository.

## 5. Upworthy integrity boundary

The Upworthy Research Archive Author Correction reports likely randomization
problems between 25 June 2013 and 10 January 2014.

The evidence contract must retain all three facts simultaneously:

1. the original archive contains the affected period;
2. the issue was discovered and publicly corrected;
3. the archive maintainers report that the Robertson negativity result remained
   nearly identical after rerunning on tests they consider reliable.

The correction is not an independent replication of Robertson.

## 6. Planned quantities — not active variables yet

Phase A reserves names and ontology roles only.

### Hneg

Planned ontology: `CONTENT_ATTRIBUTE`.

Definition:

Controlled headline-negativity condition used by the reference M1.E3 comparator.

What it is not:

- truth;
- factuality;
- misinformation;
- article valence;
- experienced emotion;
- political orientation;
- source quality.

### Paccess

Planned ontology: `DERIVED_METRIC`.

Definition:

Latent probability of opening/clicking a full item after one registered preview
impression.

What it is not:

- observed population CTR;
- attention;
- reading time;
- comprehension;
- belief;
- `Pengage`;
- `Share`.

### Access

Planned ontology: `OBSERVABLE`.

Definition:

Reference open/click outcome.

### PreviewImpression

Planned ontology: `OBSERVABLE`.

Definition:

Registered event that the preview/headline was rendered under the reference task.

Important:

`Access = 0` does not delete or reverse `PreviewImpression`.

## 7. Empirical target contract

Planned target ID:

`TARGET.M1.E3.ROBERTSON_2023`

Planned validation pattern:

`VAL.M1.004`

Use:

`DIRECTIONAL_VALIDATION_ONLY`

Primary empirical statement:

For otherwise comparable headline variants from the same underlying story,
higher negative-language content is associated with greater click propensity in
the registered Upworthy analysis.

Magnitude context that may be stored but not fitted:

- published standardized negative-word coefficient;
- reported approximate 2.3% CTR increase for one additional negative word in a
  headline of average length.

The target must explicitly state that these magnitudes do not set a CEM
coefficient.

## 8. Why the current empirical-target schema is insufficient

The current `empirical_target.schema.json` assumes participant-style studies with:

- `n_recruited`;
- `n_analyzed`;
- `event_count`;
- an `estimate_pp` effect field.

That representation works for the existing survey experiments but is semantically
wrong for a platform A/B archive with counts such as:

- experiments/tests;
- headline variants;
- impressions/assignments;
- clicks.

Likewise, the Robertson effect is not naturally represented as percentage points.

Phase A therefore specifies a future backward-compatible schema extension with:

### Design families

At minimum:

- `PARTICIPANT_EXPERIMENT`;
- `PLATFORM_AB_TEST_ARCHIVE`.

A later schema revision may add observational or meta-analytic target families if
needed.

### Platform A/B counts

The platform design must permit:

- `n_experiments`;
- `n_variants`;
- `n_impressions`;
- `n_clicks`.

Participant counts must not be fabricated to satisfy an old schema.

### Effect metrics

A target effect must support an explicit metric label rather than forcing
`estimate_pp`.

Candidate metrics include:

- `PERCENTAGE_POINTS`;
- `LOG_ODDS_COEFFICIENT`;
- `ODDS_RATIO`;
- `RELATIVE_CHANGE_PERCENT`;
- `STANDARDIZED_EFFECT`;
- `DIRECTION_ONLY`.

Existing `estimate_pp` targets must remain valid for backward compatibility.

## 9. Reference metadata extension contract

The current reference registry stores bibliographic identity and review scope but
cannot encode important evidence-audit distinctions.

A later Phase A implementation may extend reference metadata with optional,
backward-compatible fields for:

- `publication_status`;
- `evidence_roles`;
- `independence_group`;
- `data_access`;
- `data_license_note`;
- `supplemental_urls`;
- `integrity_notes`.

These fields must remain generic enough for later mechanisms.

Required semantic distinctions for M1.E3 include:

- primary selected-cue causal evidence;
- same-dataset convergent analysis;
- cross-context predictive support;
- alternative-cue evidence;
- preliminary counterevidence;
- context boundary;
- data provenance;
- integrity correction.

## 10. Evidence-independence groups

At minimum Phase A reserves these groups:

### UPWORTHY_ARCHIVE_2013_2015

Includes uses of the same Upworthy archive such as Robertson, Gligorić and the
Upworthy component of Shulman.

They are separate analyses, not independent source populations.

### SHULMAN_WAPO_2021_2022

Washington Post field experiments.

Independent from the Upworthy archive, but source data are restricted.

### NICKL_ATTENTION_ECONOMY_2025

The 2025 preprint and APS 2026 presentation are the same underlying project.

They must never be counted twice.

### WECHAT_2021_QIU

Cross-context observational/predictive support.

Not a causal replication.

## 11. Planned validation contract

Phase A reserves but does not activate:

### VAL.M1.004 — Headline-negativity access differential

Higher registered `Hneg` must correspond to higher future `Paccess` in the
selected reference comparator.

### VAL.M1.N04 — Access-gate null

When the selected cue is normalized/disabled in the later mechanism, otherwise
identical conditions converge.

### VAL.M1.N05 — Access is not downstream cognition

Changing the selected access cue may not directly mutate retained:

- M0 `B`;
- M0 `Share`;
- M1.E1 `Aissue`;
- M1.E2 `Pengage / EngageIntent`.

### VAL.M1.N06 — Non-click preserves headline exposure

`Access = 0` must not erase `PreviewImpression`.

These IDs remain absent from the active `model/validation_tests.json` during
Phase A.

## 12. Comparator invariants

The later executable comparator must hold fixed:

- underlying story/article ID;
- source identity;
- full article content;
- factual-compatibility flag;
- image identity or absence of image;
- one preview opportunity per condition;
- agent state;
- editorial-selection condition;
- M1.E2 prior-attitude/congruence state;
- retained M0 states before access.

The first reference comparator does not claim perfect natural-language semantic
equivalence unless the final stimuli are independently audited for that property.

## 13. Active-registry boundary

During Phase A:

- do not add Hneg/Paccess/Access/PreviewImpression to active `variables.json`;
- do not add VAL.M1.004/N04/N05/N06 to active `validation_tests.json`;
- do not add TARGET.M1.E3 to active `empirical_targets.json`;
- do not add an M1.E3 causal link;
- do not update the active evidence snapshot solely because a planning contract
  exists;
- do not add a runtime equation;
- do not add UI.

The machine-readable Phase A contract is packaged and testable but is not part of
the executable model specification.

## 14. Promotion gate to executable work

Promotion from Phase A requires all of the following:

1. machine-readable evidence contract validates;
2. selected cue is exactly one candidate;
3. deferred candidate remains documented;
4. source independence groups are explicit;
5. Upworthy integrity correction and robust reanalysis are represented;
6. runtime dependency on restricted lexicons is false;
7. empirical target design can represent platform A/B counts without fabricated
   participant counts;
8. effect metadata can represent non-percentage-point metrics;
9. planned quantities remain absent from the active model;
10. planned validation IDs remain absent from active validation;
11. all retained M0/M1.E1/M1.E2 tests and exports remain unchanged;
12. CI is green.

Only the next explicitly approved implementation phase may promote contract items
into the active registry and define an executable access function.

## 15. Phase A acceptance result

Phase A is complete when the evidence/schema contract and its regression tests are
green.

Completion of Phase A means:

**the evidence and data representation are ready for mechanism implementation.**

It does not mean:

**M1.E3 has been implemented or scientifically validated.**
