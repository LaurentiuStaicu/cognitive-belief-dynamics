# Alpha 0.4.3a0 planning contract — M1.E4 Headline Recognition Gate

Status: Phase A evidence/schema contract only. No executable M1.E4 mechanism, equation or UI is introduced by this document.

Target software release: **Alpha 0.4.3a0**

Working experiment name:

**M1.E4 — Headline Recognition Gate**

## 1. Scientific decision

The next M1 extension should not be called a generic “attention” mechanism.

Shulman, Markowitz & Rogers (2024) provide a preregistered signal-detection experiment in which general readers later recognized phrases from simpler headlines better than phrases from complex headlines. The directly observed/derived outcome is recognition sensitivity, d-prime. The authors interpret this pattern as evidence of greater attention and retention, but d-prime does not uniquely identify visual attention, fixation duration or an event-level encoding probability.

Therefore Phase A selects:

`PreviewImpression → Hsimp → Drecog`

where:

- `PreviewImpression` is the already registered M1.E3 preview-rendering event;
- `Hsimp` is a controlled headline-simplicity condition;
- `Drecog` is a derived signal-detection recognition-sensitivity metric.

The following remain deferred, not rejected:

- an internal latent attention variable;
- an event-level `Pencode` probability/state;
- a full-article memory mechanism after `Access`.

No runtime model may be implemented until a later phase justifies how an event-level synthetic state maps to the group-level SDT target.

## 2. Why this stage follows M1.E3 but is not conditional on Access

M1.E3 currently distinguishes:

`PreviewImpression → Hneg → Paccess → Access`.

The Shulman Study 3 mechanism experiment did not require participants to click/open a full article before the later recognition test. Participants were presented with headline stimuli and later completed a 24-item signal-detection task.

For the first M1.E4 reference contract, the conditioning event is therefore:

`PreviewImpression = 1`

not:

`Access = 1`.

This preserves the distinction:

`PreviewImpression != Access != RecognitionSensitivity`.

A later full-content encoding mechanism may legitimately condition on Access, but it would need different evidence.

## 3. Primary empirical anchor — Shulman et al. 2024, Study 3

Reference:

Shulman, H. C., Markowitz, D. M. & Rogers, T. (2024). “Reading dies in complexity: Online news consumers prefer simple writing.” *Science Advances*, 10(23), eadn2555.

DOI: https://doi.org/10.1126/sciadv.adn2555

Study 3:

- preregistered survey experiment;
- N = 524 recruited general-public participants via CloudResearch / MTurk;
- participants viewed headline sets and later completed a 24-item signal-detection recognition task;
- sensitivity d-prime was the mechanism outcome;
- simple-headline condition: M = 1.23, SD = 0.81;
- complex-headline condition: M = 0.80, SD = 0.77;
- t(483) = 6.01;
- P < 0.001;
- Cohen’s d = 0.55.

Phase A uses only the directional pattern:

`simpler controlled headline condition → higher recognition sensitivity`.

The published means and effect size are empirical context. They do not define a future CEM coefficient.

## 4. Mandatory boundary evidence — Shulman et al. 2024, Study 4

Study 4 repeats the selection and SDT design in a sample of professional writers, including many current/former journalists.

The simplicity effect is not observed:

- headline-selection difference: non-significant;
- SDT difference: t(165) = -0.44, P = 0.660;
- Cohen’s d = 0.07.

Phase A therefore treats professional expertise / task orientation as a mandatory context boundary. M1.E4 must not claim that headline simplicity universally increases recognition in every population.

The professional sample is not an independent publication, but it is a distinct participant sample and a direct within-paper boundary test.

## 5. Independent context boundary — Mattis et al. 2025

Reference:

Mattis, N., Heitz, L., Masur, P. K., Moeller, J. & van Atteveldt, W. (2025). “Nudges for news recommenders: prominent article positioning increases selection, engagement, and recall of environmental news, but reducing complexity does not.” *Journal of Communication*, 75(6), 437–449.

DOI: https://doi.org/10.1093/joc/jqaf019

The preregistered seven-day field experiment (N = 502) found that prominent positioning increased selection, reading time and factual recall, whereas automated reduction of article-text complexity did not significantly improve recall (beta = 0.04, CI -0.04 to 0.13, P = 0.310).

This is not a direct replication of headline simplicity. It manipulates article text rather than only headlines, uses a different recall outcome and occurs in a news-aggregator environment. It is nevertheless a useful independent warning against generalizing “simpler language → better memory” across stimulus levels and contexts.

## 6. Architecture evidence — exposure, access and cognition remain separate

González-Bailón et al. (2023) distinguish potential exposure, actual exposure after feed curation and later engagement across Facebook news consumption.

Robertson et al. (2023) distinguish URLs shown in Google Search from URLs users select.

These sources justify preserving stage boundaries, but they do not calibrate recognition or encoding.

M1.E4 must therefore retain:

`PreviewImpression != Access != Attention != Encoding != RecognitionSensitivity != Belief != EngageIntent != Share`.

## 7. Construct decision

### Selected — Drecog

`Drecog` is a condition-level / task-level signal-detection sensitivity metric derived from hits and false alarms in a recognition probe set.

Ontology role if later promoted: `DERIVED_METRIC`.

It is:

- recognition discrimination/sensitivity;
- directly tied to the published SDT outcome.

It is not:

- a gaze measure;
- fixation duration;
- an event-level neural encoding state;
- comprehension;
- belief;
- recall probability for one item;
- intelligence or expertise.

### Deferred — Aattn

A latent internal “attention allocation” state is not selected for the next phase because the primary source does not directly measure eye movements, fixation, dwell time or a unique attention state.

### Deferred — Pencode

An event-level `Pencode` is not selected because a group-level d-prime difference does not by itself determine a unique item-level encoding probability.

A later bridge contract would need an explicit measurement/model mapping before any executable Pencode equation is permitted.

## 8. Cue decision — Hsimp

The deferred M1.E3 simplicity candidate becomes the planned M1.E4 cue.

Reference encoding:

- `Hsimp = 0`: complex/control headline condition;
- `Hsimp = 1`: simpler headline condition.

The cue will be stored as precomputed controlled stimulus metadata. CEM will not reproduce the proprietary LIWC-based composite at runtime.

`Hsimp` is not education, intelligence, comprehension ability, source quality or article difficulty.

## 9. Required reference comparator

The planned comparator must hold fixed, as far as the stimulus design permits:

- underlying story / semantic topic;
- source identity;
- factual compatibility;
- preview rendering;
- number and timing of headline exposures;
- probe format and delay;
- agent/task state in the reference experiment;
- M0 belief/share state;
- M1.E1 editorial condition;
- M1.E2 presentation/congruence state;
- M1.E3 access mechanism output must not be treated as the cause of Drecog in the initial comparator.

The manipulated quantity is only the registered `Hsimp` condition.

## 10. Planned validation patterns

### VAL.M1.005 — Headline simplicity recognition differential

Holding the registered comparator conditions fixed, the simpler Hsimp condition must produce higher Drecog than the complex/control condition.

### VAL.M1.N07 — Recognition null

When Hsimp variation is normalized away, otherwise identical conditions must converge in Drecog.

### VAL.M1.N08 — Recognition sensitivity is not attention

A Drecog difference must not be relabeled as a directly observed attention, gaze or fixation difference.

### VAL.M1.N09 — Recognition sensitivity is not downstream belief/action

M1.E4 must not directly mutate M0 belief/Share, M1.E1 Aissue, M1.E2 Pengage/EngageIntent or M1.E3 Access.

### VAL.M1.N10 — Professional-sample boundary

The implementation/documentation must preserve the Study 4 null as a context boundary and must not state a universal simplicity effect across expert/professional readers.

## 11. Promotion gate

Phase A may merge only if:

- the evidence contract validates against schema;
- Drecog is the only selected outcome construct;
- Aattn and Pencode remain explicitly deferred;
- Hsimp is precomputed rather than runtime-LIWC dependent;
- the primary Study 3 effect and Study 4 null boundary are recorded natively;
- Mattis et al. 2025 is preserved as independent context-boundary evidence;
- the comparator is conditioned on PreviewImpression rather than Access;
- planned M1.E4 quantities are absent from the active variable registry;
- planned M1.E4 validation IDs are absent from active validation tests;
- no M1.E4 runtime source file exists;
- no UI is added;
- retained M0/M1.E1/M1.E2/M1.E3 outputs remain unchanged;
- full CI passes.

## 12. Explicitly forbidden in Phase A

No:

- `Pencode` equation;
- beta-simplicity value;
- recognition simulator;
- attention state;
- eye-tracking claim;
- active M1.E4 registry promotion;
- active M1.E4 empirical target;
- Theory/UI comparator;
- downstream belief or sharing coupling;
- calibration claim.

Phase A ends with a falsifiable evidence/schema contract only.
