# ODD description — Cognitive Epistemic Model M0

Baseline retained in software: Alpha 0.4.0a0  
Model specification: M0  
Status: retained uncalibrated baseline; active candidate extension is M1 (see `ODD_M1.md`)

This document follows the Overview, Design concepts and Details (ODD) structure.
The registry-driven Visual ODD in the web application is complementary: it shows
the executable cycle, while this document records purpose, assumptions and
fitness-for-purpose boundaries in prose.

## 1. Overview

### 1.1 Purpose and patterns

M0 is the smallest executable reference model currently used to test whether a
small set of candidate mechanisms can reproduce five registered qualitative
patterns without hard-coding Track A/Track B or a generic critical-thinking
variable.

The registered patterns are maintained in `model/validation_tests.json`:

- repeated exposure can increase truth judgment under comparable conditions;
- corrective context can reduce belief and partial regression can occur as its
  accessibility decays;
- learned source reliability can alter the weight placed on comparable evidence;
- accuracy salience can improve sharing discernment in a reward-competing context;
- belief and sharing can dissociate.

M0 is fit for mechanism demonstration and software/pattern regression. It is not
currently fit for population prevalence estimation, individual diagnosis,
Romania forecasting, calibrated policy-effect estimation or quantitative
prediction outside the synthetic reference tasks.

### 1.2 Entities, state variables and scales

Current executable entities are:

- `HumanAgent`: familiarity, corrective-context accessibility, estimated source
  reliability, prior claim belief, accuracy baseline and sharing bias;
- `InformationItem / claim`: identified by claim id in the reference tasks;
- `Source`: identified by source id and represented in the agent by an estimated
  reliability state;
- events: exposure, correction, source feedback and decision.

The core registered variables are maintained in `model/variables.json`.
The 20 conceptual modules are maintained in `model/modules.json`; they are a
scientific map, not 20 executable software engines. The executable architecture
is grouped into eight subsystems in `model/subsystems.json`.

Time is represented by discrete abstract event steps. A step is not a day, month
or year.

### 1.3 Process overview and scheduling

Events are processed in non-decreasing abstract time. Input order resolves ties
between simultaneous events; this is a computational convention and has no
psychological interpretation.

The current process registry is `model/processes.json` and the implementation
is shown in the Visual ODD view:

1. initialisation;
2. event scheduling;
3. state updates;
4. belief formation;
5. action policy;
6. event/outcome logging;
7. scientific pattern checks.

## 2. Design concepts

### 2.1 Basic principles

The executable M0 deliberately separates:

`simulated world truth -> information/evidence available to the agent -> internal state -> judgment -> action`

Ground truth is never passed directly to the belief-update function.

Candidate functional forms are:

- bounded familiarity saturation;
- exponential corrective-accessibility decay;
- delta-rule source-reliability learning;
- logistic belief transform;
- logistic sharing/action transform.

These are reference candidates, not asserted unique psychological laws.

### 2.2 Emergence

Belief and sharing trajectories emerge from the sequence of events and current
agent state under the reference equations. No Track A/B class is assigned to the
agent.

### 2.3 Adaptation and objectives

M0 has limited adaptation: source-reliability estimates update from feedback and
familiarity/correction states update through events. It does not contain a
general-purpose optimizer or an explicit long-term agent objective.

### 2.4 Sensing and information

The agent receives only event payloads and evidence signals exposed by the
simulation. M0 itself does not represent editorial sampling, world-model construction or heuristic-policy selection. Alpha 0.4 adds the separate M1.E1 editorial-emphasis candidate described in `ODD_M1.md`; it does not retrofit those constructs into M0.

### 2.5 Interaction

M0 reference runs use one agent, one claim and one source at a time. There is no
social network interaction in the current reference model.

### 2.6 Stochasticity

The Share action is sampled from the calculated sharing probability using a
seeded NumPy random generator. Scientific diagnostics that need deterministic
outputs use latent probabilities/states rather than sampled Share outcomes.

### 2.7 Observation

The simulator logs each event, state changes and decision observations. Published
reference runs store full step trajectories. Software tests are distinct from
scientific pattern tests.

## 3. Details

### 3.1 Initialisation

Reference runs initialise one agent with claim prior 0.3, default source
reliability estimate 0.5 and seed 7 unless a test states otherwise. Reference
parameters are defined in `ModelParams` in
`src/cognitive_epistemic_model/state.py`.

Parameters are demonstrative and are not population estimates.

### 3.2 Input data

The current reference runs are synthetic and do not ingest external empirical
datasets at runtime. Evidence citations in `model/references.json` support
phenomenon-level claims and limitations; they are not calibration datasets.

### 3.3 Submodels

#### Familiarity

Exposure updates familiarity with bounded saturation using `alpha_f`.

#### Corrective context

A correction increases corrective-context accessibility using `alpha_c`.
Accessibility subsequently decays exponentially with `lambda_c`.

#### Source reliability

Feedback updates the agent's estimated source reliability using `alpha_t`.
This state is an internal estimate, not true source reliability.

#### Belief

Prior belief, familiarity, source-weighted evidence and signed corrective context
enter the M0 logistic belief transform. The output is a latent propensity to
judge the claim as true, not knowledge or ideology.

#### Accuracy salience and sharing

An accuracy cue modifies the weight placed on accuracy in the action calculation.
Belief, accuracy weight, reward context and sharing bias determine the sharing
probability. A seeded random draw produces the observed Share action.

## 4. Verification, diagnostics and fitness for purpose

The Python suite separately tests implementation invariants, registered M0
patterns, ground-truth isolation, deterministic replay, intervention arithmetic
and release consistency.

Alpha 0.3.6 adds a local sensitivity-based practical-identifiability diagnostic
and a separate local prediction-robustness diagnostic. These do not establish
structural identifiability, parameter uncertainty or empirical calibration.

A functional form should be replaced when a rival produces materially better
out-of-sample pattern reproduction or when identifiability/diagnostics show the
reference form is inadequate.

## 5. Extension gate retained for future M1 additions

No new world-model, heuristic or editorial-media variable becomes executable
only because it enriches the conceptual story. Each addition must specify:

1. an observed phenomenon;
2. an operational measurement;
3. a differential prediction relative to the smaller model;
4. a rejection/removal criterion.

Any M1 extension must retain the M0 regression patterns or document explicitly
why the scientific target changed.

## References for documentation protocol

- Grimm et al. (2020), "The ODD Protocol for Describing Agent-Based and Other
  Simulation Models", JASSS 23(2):7.
- Visual ODD (2024) is used only as the complementary visual organisation of
  Initialisation, Submodels, Observation and Scales.
