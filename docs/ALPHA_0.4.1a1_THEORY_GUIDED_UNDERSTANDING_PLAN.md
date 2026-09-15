# Alpha 0.4.1a1 planning contract — Theory & Guided Understanding

Status: planning-only contract. No M0 or M1 equation, coefficient, empirical target,
intervention arithmetic, or scientific pattern is changed by this document.

Target software release: **Alpha 0.4.1a1**

## 1. Why this release exists

Alpha 0.4.1a0 contains a scientifically traceable M0 baseline plus M1.E1 editorial
selection/emphasis and M1.E2 semantic-equivalent presentation framing ×
prior-attitude congruence. The application exposes the mechanisms, registries,
scenarios and ODD structure, but a user who does not already know the theory can
still fail to form a coherent mental model of:

- what problem CEM is trying to solve;
- how world state, available information, observed information, internal state,
  judgment and action differ;
- why M0, M1.E1 and M1.E2 are separate;
- what the variables mean and what they explicitly do not mean;
- which concepts are executable, conceptual, empirically supported or
  interpretive;
- how a theoretical statement maps to a model variable, equation, scenario,
  evidence source and implementation function.

This is not a minor help-text problem. It is an information-architecture and
explanatory-layer problem.

The attached UX review already identified the core issue: long-form explanatory
text is not inherently the problem; the problem is the spatial/temporal
decoupling between explanation and model dynamics. Alpha 0.4.1a1 therefore
builds an interactive explanatory layer without deleting the existing detailed
prose.

## 2. Version decision

Use **0.4.1a1**, not 0.4.2a0.

Rationale:

- Python pre-release identifiers order alpha releases by the numeric suffix
  (`a0`, `a1`, `a2`, ...);
- this release does not add a new scientific mechanism;
- Alpha 0.4.2a0 remains reserved for the next causal-stage extension
  (currently the leading candidate is an attention/consumption gate);
- 0.4.1a1 is therefore a new alpha iteration of the same 0.4.1 scientific
  specification with a substantially improved explanatory/learning interface.

## 3. Top-level navigation decision

Retain the top-level label:

**1 · Înțelegere / 1 · Understanding**

Do **not** add an eighth equal top-level tab called Theory.

Inside Understanding introduce three clearly labelled internal modes:

1. **Teorie / Theory**
2. **Mecanisme / Mechanisms**
3. **Tur ghidat / Guided tour**

The current Understanding content becomes **Mechanisms**. Existing functionality
is retained; it is not deleted or rewritten into a tutorial.

Theory becomes the default mode for a first-time/opening visit unless a persisted
user choice selects another mode.

Guided tour is a tutorial sequence and is not the canonical theory text.

Why this architecture:

- the project priority remains understanding first;
- theory, mechanism exploration and guided usage belong to the same top-level
  user intent;
- GNOME HIG recommends a small number of equivalent views and a simple
  hierarchy below them rather than a growing row of peer views;
- elementary HIG supports sidebars as high-level/category navigation when a
  content area contains many locations;
- W3C cognitive-accessibility guidance recommends explicit hierarchy, clear
  purpose, visible location and logically grouped sections.

## 4. Documentation-function separation

Alpha 0.4.1a1 uses a Diátaxis-inspired separation.

### Theory = explanation

Answers:

- Why does this distinction matter?
- What is the theoretical mechanism?
- What evidence supports it?
- What are the competing interpretations?
- What does CEM choose to represent?
- What are the limitations?

Theory should remain coherent prose and should not become a button manual.

### Guided tour = tutorial

Answers:

- What should I click first?
- What should I notice?
- What changes when I switch this condition?
- Where do I go next?

The tour teaches by leading the user through working examples.

### Registry / ODD = reference

Answers:

- What is the exact variable ID?
- What is its domain/range?
- What is the exact registered relation?
- Which DOI supports the registered phenomenon?
- Which implementation file/function is canonical?

### Planning = task-oriented application

Priorities and actions remain the place for applying the model to intervention
comparison. They are not merged into Theory.

## 5. Theory information architecture

Theory should read as a coherent book/course rather than as software-file
documentation.

### Chapter 0 — What is CEM?

Questions:

- What problem is the model trying to study?
- What is an epistemic process?
- What is a cognitive-epistemic model?
- What can the current model do?
- What can it not do?

Must explicitly introduce:

- M0 retained baseline;
- M1.E1 and M1.E2;
- demonstration coefficients;
- non-calibration;
- no population Track A/B estimates;
- no individual diagnosis.

Application links:

- Visual ODD overview;
- Registry;
- current release metadata.

### Chapter 1 — World, information and internal representation

Core conceptual chain:

`world state → available information → selected/presented information → observed information → internal representation → judgment → action`

Explain why these stages must not be collapsed.

Application links:

- M1.E1;
- M1.E2;
- MOD.14;
- M0 ground-truth isolation boundary.

### Chapter 2 — Fast processing, deliberation and metacontrol

Explain Type 1 / Type 2 style distinctions cautiously.

Do not describe two literal brains or equate M0 W with “System 2”.

Relate to:

- MOD.02;
- resource limitations;
- metacognitive monitoring;
- future heuristic-policy work.

Status initially: BACKGROUND_THEORY / CONCEPTUAL, not EXECUTABLE unless mapped
to an existing variable with a narrower definition.

### Chapter 3 — Uncertainty, need for closure, seizing and freezing

Recover the earlier project distinction:

- uncertainty / closure pressure;
- seizing;
- freezing;
- interpretation of subsequent information.

Do not present Track A/B as measured population classes.

Status initially: CONCEPTUAL.

### Chapter 4 — Stress, executive resources and flexibility

Explain evidence for effects on working memory and cognitive flexibility while
avoiding the simplistic claim “stress shuts down the prefrontal cortex”.

Relate to:

- MOD.01;
- MOD.02;
- MOD.06.

Status initially: BACKGROUND_THEORY / CONCEPTUAL.

### Chapter 5 — Repetition, familiarity and judged truth

Explain:

`Exposure → Familiarity → contribution to Belief`

Application links:

- `Nexp`;
- `F`;
- `B`;
- repetition mechanism;
- reference scenario;
- exact M0 equation;
- registered evidence;
- implementation code.

Status: EMPIRICAL + EXECUTABLE.

### Chapter 6 — Corrections, accessibility and memory

Explain:

- correction event;
- corrective-context accessibility;
- decay;
- why accessibility is not “memory deletion”;
- why correction does not guarantee belief change.

Application links:

- `C`;
- correction mechanism;
- scenario step 5;
- equation;
- evidence;
- code.

Status: EMPIRICAL + EXECUTABLE.

### Chapter 7 — Sources, feedback and estimated reliability

Explain:

- true source quality versus agent estimate;
- feedback update;
- source-weighted evidence;
- why `T` is not objective truth.

Application links:

- `T`;
- source scenario;
- relevant M0 relation;
- evidence and code.

Status: EMPIRICAL + EXECUTABLE.

### Chapter 8 — Belief, accuracy salience and action

Explicitly separate:

- latent truth judgment `B`;
- contextual accuracy weight `W`;
- sharing probability;
- sampled Share.

Explain why belief, endorsement and sharing are not synonyms.

Application links:

- decision mechanism;
- scenario;
- intervention planner where relevant.

Status: EXECUTABLE with registered empirical targets/limitations.

### Chapter 9 — Editorial selection and the observed world

Explain M1.E1:

`fixed fact-compatible pool → Eedit → selected sample / Sobs → Aissue`

Core boundaries:

- negative information is not false information;
- editorial emphasis is not a measured newsroom-bias score;
- `Aissue` is not M0 `B`;
- published effect sizes are benchmark context, not fitted parameters.

Application links:

- M1.E1 comparator;
- `Eedit`, `Sobs`, `Aissue`;
- ODD M1.E1;
- empirical target;
- source paper;
- implementation code.

Status: EMPIRICAL phenomenon + EXECUTABLE candidate mechanism.

### Chapter 10 — Presentation framing and prior-attitude congruence

Explain M1.E2:

- same semantic proposition;
- confirmation versus refutation;
- `Gatt` as task-specific relation;
- NULL versus frame-only versus frame×congruence;
- `Pengage` and `EngageIntent`;
- why EngageIntent is not M0 Share.

Application links:

- M1.E2 comparator;
- nested models;
- registered validation targets;
- code.

Status: EMPIRICAL phenomenon + EXECUTABLE candidate mechanism.

### Chapter 11 — Algorithms, ranking and social feedback

Explain the causal-stage distinction:

`ranking → exposure` is not automatically `ranking → belief`.

Recover three distinct loops from the historical project material:

- closure loop;
- familiarity loop;
- social-reinforcement loop.

Show which pieces are executable today and which are not.

Status:

- some background phenomena EMPIRICAL;
- platform-ranking mechanism DEFERRED/CONCEPTUAL;
- no direct algorithm→belief arrow unless separately validated.

### Chapter 12 — Interventions and where they act

Explain interventions by causal location:

- information supply;
- correction;
- source evaluation;
- accuracy attention;
- inoculation/prebunking;
- friction;
- future attention/consumption gate.

Each intervention must link to the mechanism/variable it changes and clearly
state whether the implementation is demonstrative, empirically anchored or
future/conceptual.

### Chapter 13 — Self-integration, individuation and Reflective Distance

Preserve the historical Jung/individuation material as an interpretive layer.

Do not convert Reflective Distance into a numerical model state in this release.

Explicitly mark:

- Jungian individuation = INTERPRETIVE/THEORETICAL;
- potential links to metacognition/autonomy = hypotheses or conceptual bridges;
- no claim that MOD.17 is an executable psychological scale.

### Chapter 14 — How CEM is validated

Explain:

- implementation test versus scientific pattern test;
- empirical target;
- nested null;
- model discrimination;
- calibration versus demonstration;
- local diagnostics versus structural identifiability;
- evidence snapshot;
- ODD;
- reproducibility and provenance.

This chapter should make the scientific status of the model understandable
without requiring the reader to inspect GitHub.

### Chapter 15 — How to use CEM

Short orientation, not the full tutorial.

Explain the workflow:

`Understand → explore mechanism → inspect evidence → compare factors → plan action`

Then offer a clear action:

**Start Guided Tour →**

## 6. Epistemic-status system

Every theory concept or relationship must expose one or more explicit status
labels.

Canonical statuses:

### EMPIRICAL

There is empirical evidence for the phenomenon/relationship described at the
declared level.

This does not imply that the exact CEM functional form is empirically identified.

### EXECUTABLE

The construct or relationship exists in the running model and has a canonical
implementation.

### CONCEPTUAL

The construct belongs to the planned architecture or explanatory map but is not
yet an executable, falsifiable model component.

### INTERPRETIVE

The material provides philosophical, historical or integrative interpretation
rather than a directly executable empirical construct.

These labels can coexist where necessary. Example:

M1.E2 presentation framing:
- EMPIRICAL phenomenon;
- EXECUTABLE candidate model;
- REFERENCE_CANDIDATE functional form.

The UI must never make CONCEPTUAL or INTERPRETIVE content look equivalent to
EXECUTABLE content.

## 7. Evidence-role separation

Theory introduces a second citation role without weakening the existing model
evidence registry.

### MODEL_EVIDENCE

Used when a source supports:

- a registered phenomenon;
- a validation target;
- a registered model link;
- a model-discrimination claim.

These sources remain in the canonical model evidence registry.

### BACKGROUND_THEORY

Used for:

- explanatory frameworks;
- historical theoretical context;
- review material;
- concepts not yet executable.

A BACKGROUND_THEORY citation must not silently become evidence for an executable
functional form.

### INTERPRETIVE_SOURCE

Used for:

- Jung;
- Frankl;
- philosophical/epistemological interpretation;
- historical conceptual framing.

These sources must never be counted as empirical calibration evidence.

## 8. Content-storage architecture

Do not hardcode the full theory book in `web/src/learning.ts`.

Proposed structure:

```
docs/theory/
  ro/
    00-ce-este-cem.md
    01-lume-informatie-reprezentare.md
    02-procesare-metacontrol.md
    ...
    15-cum-folosesc-cem.md
  en/
    00-what-is-cem.md
    01-world-information-representation.md
    ...
    15-using-cem.md

model/theory_index.json
model/theory_glossary.json
schemas/theory_index.schema.json
schemas/theory_glossary.schema.json
```

The Markdown is source content.

`theory_index.json` is navigation/mapping metadata.

`theory_glossary.json` stores canonical short definitions and mappings used by
inline inspectors.

## 9. Theory index contract

Each chapter entry should include at minimum:

- `id`;
- `order`;
- bilingual title;
- bilingual summary;
- source Markdown paths;
- prerequisites;
- epistemic status;
- `module_ids`;
- `variable_ids`;
- `mechanism_ids`;
- `validation_ids`;
- `evidence_refs`;
- background-theory refs where relevant;
- code references;
- related application views;
- anchor IDs;
- “what this chapter does not claim”.

All referenced IDs must resolve at build/test time.

## 10. Reactive-token syntax

Theory prose may use validated tokens, for example:

- `[[VAR:F]]`
- `[[MODULE:MOD.14]]`
- `[[MECH:repetition]]`
- `[[VAL:VAL.M1.003]]`
- `[[REF:REF.ARUGUETE.2024]]`
- `[[VIEW:reference]]`
- `[[VIEW:runs:repetition:4]]`
- `[[CODE:cognitive_epistemic_model.updates:update_familiarity]]`

Build/rendering converts these to keyboard-accessible interactive references.

A broken token is a CI failure.

## 11. Contextual inspector

Theory uses a persistent contextual inspector rather than hover-only cards.

Selecting a token can show:

### For a variable

- symbol;
- full name;
- definition;
- range/domain;
- what it is not;
- epistemic status;
- equation involvement;
- module;
- evidence;
- “Open in Registry”;
- “Open mechanism”;
- “Open code”.

### For a mechanism

- mechanism name;
- compact causal path;
- executable status;
- equation;
- current reference output or mini-visual;
- registered pattern test;
- empirical target;
- link to full Mechanisms mode.

### For a conceptual construct

- definition;
- conceptual module;
- status = CONCEPTUAL/INTERPRETIVE;
- explicitly no fake equation or value;
- related empirical literature;
- candidate future model links.

Hover may preview, but click/Enter controls the persistent inspector.
Escape returns focus to the invoking token.

## 12. Theory page layout

### Wide desktop

Three functional regions:

1. chapter sidebar;
2. prose reader;
3. contextual inspector.

The prose column must remain readable around 68–72ch.

The inspector is sticky only when available height/zoom permits it.

### Medium widths

Chapter sidebar collapses into a chapter selector.
Reader + inspector remain two regions if usable.

### Narrow / high zoom

Single-column order:

1. chapter/section selector;
2. theory content;
3. contextual inspector immediately after the active reference or in a clearly
   reachable disclosure panel.

No horizontal scrolling for normal content.

## 13. Internal navigation

Understanding should expose a small view switcher:

`Teorie | Mecanisme | Tur ghidat`

Three items fit the HIG recommendation for a small view switcher.

Theory chapter navigation uses one sidebar/list level only.

Do not create nested accordion hierarchies inside the chapter sidebar.

Support deep links:

- `#understanding/theory/world-information`
- `#understanding/theory/repetition`
- `#understanding/mechanisms/editorial`
- `#understanding/tour/step-4`

Browser Back/Forward must preserve the user's conceptual path.

## 14. Guided tour

The initial guided tour should contain approximately ten steps:

1. What CEM is and is not.
2. World versus information versus internal state.
3. Repetition: inspect `Nexp → F → B`.
4. Correction: jump to the correction event and inspect `C`.
5. Source feedback: inspect `T`.
6. Belief versus action: compare `B`, sharing probability and Share.
7. M1.E1: hold world/facts fixed and change editorial selection.
8. M1.E2: hold semantics fixed and change confirmation/refutation frame.
9. Open Registry and inspect evidence/status.
10. Continue to Priorities & Actions.

The tour must:

- use existing executable scenarios and comparators;
- never introduce a separate toy model with different equations;
- allow exit and resume;
- show progress;
- preserve keyboard operation;
- never require hover.

## 15. Source-linking policy

Every important theoretical claim should provide human-readable source links.

For executable concepts, Theory should provide both:

- evidence link(s);
- model/implementation link(s).

Code links shown in a released build must be pinned to the current release tag or
commit, not `main`, so the explanation always matches the code the user is
running.

## 16. ODD versus Theory

ODD remains the canonical model-description protocol.

Theory does not replace ODD.

ODD answers:

- purpose;
- entities/state;
- process/scheduling;
- design concepts;
- initialization;
- inputs;
- submodels.

Theory adds:

- conceptual rationale;
- prior knowledge;
- narrative explanation;
- competing interpretations;
- evidence context;
- links from concepts to implementation.

The two surfaces must cross-link.

## 17. Search and findability

Initial Alpha 0.4.1a1 does not require a global fuzzy search engine.

It must provide:

- chapter sidebar;
- in-page headings;
- browser-find compatible text;
- deep links;
- glossary/index navigation.

A future search control may be added if real content size makes navigation
insufficient.

## 18. Accessibility requirements

At minimum:

- logical h1→h2→h3 hierarchy;
- labelled regions;
- meaningful link text;
- visible keyboard focus;
- Enter/Space activation for interactive references;
- Escape closes/dismisses contextual inspector state where applicable;
- no essential hover-only content;
- current chapter and current Understanding mode exposed programmatically;
- reflow at 320 CSS px;
- usable at 200% zoom;
- `prefers-reduced-motion`;
- `forced-colors`;
- dark/light compatibility;
- equations accompanied by text interpretation;
- graphics accompanied by textual values/description.

W3C cognitive guidance should be treated as a usability requirement, not merely a
screen-reader checklist: page purpose, hierarchy and current location must remain
obvious.

## 19. Content-governance rule

No theory paragraph should silently strengthen a model claim.

For every chapter, authors must distinguish:

1. what the literature supports;
2. what CEM currently implements;
3. what CEM only hypothesizes/plans;
4. what is interpretive.

Where historical project material is stronger than current evidence, Theory must
preserve the idea but label/qualify it rather than presenting it as settled fact.

## 20. Scientific non-goals for Alpha 0.4.1a1

Do not add:

- attention/consumption gate;
- new M1 equations;
- platform-ranking mechanism;
- social-network reinforcement mechanism;
- Track A/B prevalence;
- stress coefficients;
- Reflective Distance numeric state;
- heuristic selector;
- new intervention calibration.

This release explains the current model; it does not enlarge the scientific
state space.

## 21. Implementation phases

### Phase A — content/data contract

- add theory schemas;
- add `theory_index.json`;
- add glossary;
- establish status and evidence-role enums;
- establish token resolver;
- add bilingual chapter skeletons.

### Phase B — Theory reader

- add internal Understanding switcher;
- chapter sidebar;
- Markdown rendering;
- deep linking;
- contextual inspector;
- variable/module/evidence/code links.

### Phase C — canonical content

Write and review chapters 0–15.

Each chapter must pass a source/status audit before release.

### Phase D — Guided tour

Implement the ten-step tutorial using existing M0/M1 components.

### Phase E — accessibility and regression

- keyboard;
- focus restoration;
- reflow;
- dark/light;
- forced colors;
- reduced motion;
- browser history;
- deep links;
- bilingual parity.

## 22. Tests

### Schema/content tests

- every theory index entry validates;
- every RO chapter has one EN counterpart;
- chapter IDs/orders are unique;
- all referenced variables/modules/validation tests/evidence refs exist;
- all interactive tokens resolve;
- every executable code reference resolves to a declared mapping;
- no INTERPRETIVE concept is flagged executable;
- no CONCEPTUAL concept receives a fake equation/value.

### Web tests

- default Understanding mode is Theory for a fresh session;
- switching Theory/Mechanisms/Guided Tour preserves state where expected;
- a theory variable token opens the correct inspector;
- “Open mechanism” navigates to the correct mechanism;
- “Open in Registry” opens the correct registry item;
- Back returns to the originating theory section;
- one full theory→mechanism→registry→theory journey passes;
- one full Guided Tour passes by keyboard;
- narrow viewport remains usable;
- 200% zoom remains usable.

### Release regression

All current M0/M1 tests remain byte-identical except intentional software-version
metadata.

No `runs.json`, `interventions.json`, M1.E1 or M1.E2 numerical output is
allowed to change in this release.

## 23. Release acceptance gate

Alpha 0.4.1a1 is releasable only when:

- Theory is the default first-time Understanding surface;
- all 16 chapters exist in RO and EN;
- each chapter exposes its epistemic status;
- all executable concepts map to current model elements;
- conceptual/interpretive concepts are visibly distinguished;
- Guided Tour is complete;
- all tokens/deep links resolve;
- code links are release-pinned;
- accessibility requirements pass;
- current scientific outputs are unchanged;
- Python/registry tests pass;
- canonical export reproduction remains byte-identical;
- TypeScript/Vite passes;
- Playwright passes;
- Pages/release provenance pipeline remains unchanged and green.

## 24. External design/documentation references used for this contract

- Diátaxis: https://diataxis.fr/
- GNOME HIG Navigation: https://developer.gnome.org/hig/guidelines/navigation.html
- GNOME HIG View Switchers: https://developer.gnome.org/hig/patterns/nav/view-switchers.html
- GNOME HIG Sidebars: https://developer.gnome.org/hig/patterns/nav/sidebars.html
- elementary HIG Creating Layouts: https://docs.elementary.io/hig/widgets/creating-layouts
- W3C WAI Page Structure: https://www.w3.org/WAI/tutorials/page-structure/
- W3C Cognitive Accessibility — Clear Purpose:
  https://www.w3.org/WAI/WCAG2/supplemental/patterns/o1p01-clear-purpose/
- W3C Cognitive Accessibility — Page Structure:
  https://www.w3.org/WAI/WCAG2/supplemental/patterns/o2p03-page-structure/
- ODD Protocol (Grimm et al. 2020):
  https://jasss.soc.surrey.ac.uk/23/2/7.html
- Python Packaging Version Specifiers:
  https://packaging.python.org/en/latest/specifications/version-specifiers/

## 25. Immediate next step after approval of this planning contract

Create a separate implementation branch from the release baseline and implement
**Phase A only** first: schemas, theory index, glossary, token-resolution contract,
chapter skeletons and tests.

Do not begin full prose authoring or Guided Tour UI until the content/data contract
is validated by CI.
