# Alpha 0.4.0a0 — scientific and UX scope

Status: implementation contract for the `alpha-0.4-narrative-laboratory` branch.

## Why this document exists

The project history fixes the scientific meaning of v0.4 as:

`world model + heuristics + editorial media`

The UX work started from v0.3.5a0 is therefore a foundation for Alpha 0.4, not the complete scientific release by itself.

## Non-negotiable project order

1. Understand mechanisms.
2. Prioritise factors conditional on objectives, interactions, feasibility, cost and uncertainty.
3. Plan actions, dependencies, timing, monitoring and reassessment.

Extended prose remains core content. UI simplification must organise complexity rather than remove scientific qualifications.

## Alpha 0.4 architecture

The 20 conceptual modules remain the scientific map. They are not 20 independent software engines.

The executable architecture is organised into eight subsystems:

- WORLD / INFORMATION
- HUMAN AGENT
- SOURCES / INSTITUTIONS
- MEDIA / STRATEGIC ACTORS
- PLATFORM / NETWORK
- AI SYSTEM
- LEARNING / ADAPTATION
- OBSERVATION / VALIDATION

Jungian individuation remains an interpretive/meta layer and is not a ninth numerical engine.

## Ontology roles

Executable objects should use one primary role:

- ENTITY
- STATE_FAST
- STATE_SLOW
- PARAMETER
- EXOGENOUS_INPUT
- CONTENT_ATTRIBUTE
- POLICY
- PROCESS
- OBSERVABLE
- DERIVED_METRIC

`INTERPRETIVE_CONSTRUCT` is documentation-level metadata, not an executable ontology role.

## Scientific additions targeted by v0.4

### MOD.14 — World-model construction

The model must preserve the distinction:

`ACTUAL WORLD → SAMPLED / OBSERVED INFORMATION → PERCEIVED / INTERPRETED WORLD → DECISION`

World-model construction is not one explanatory super-variable. Candidate levels include perceptual, semantic, causal and social models. Additional levels remain conceptual unless operationalisation and tests justify execution.

### MOD.15 — Heuristic policy selection

A heuristic is a POLICY, not automatically a bias or an irrationality score.

The central quantity is the fit between a policy and the information environment. Candidate mechanisms enter executable code only through explicit empirical pattern tests.

### MOD.16 — Editorial media system

Editorial media is distinct from platform ranking. Candidate processes include:

`world events → selection / gatekeeping → agenda → framing → presentation / repetition → direct audience + platform redistribution`

Editorial selection, ownership/funding incentives, journalistic norms, visual/verbal framing and platform redistribution must not be collapsed into one generic algorithm.

## Extension gate

No new variable or mechanism enters executable simulation merely because it makes the conceptual story richer.

Every executable addition must answer:

1. What observed phenomenon does it explain?
2. How can it be measured or operationalised?
3. What different prediction does it produce relative to the model without it?
4. What result would make us remove or reject it?

An extension M1 must reproduce its target pattern and retain the existing M0 scientific patterns. Otherwise it is rejected or revised.

## M0 integrity during the Alpha 0.4 transition

Until an extension passes the gate above:

- M0 equations remain unchanged.
- M0 coefficients remain demonstrative and uncalibrated.
- Ground truth stays isolated from human belief updating.
- Steps remain abstract units.
- Track A/B remains interpretive and has no population prevalence.
- No individual diagnosis is produced.
- Computational dependencies are not presented as empirically proven causal effects.

## Three complementary visual questions

The frontend should distinguish:

### NARRATIVE LABORATORY
What does this mechanism mean and how does a reference run evolve?

### SYSTEM MAP
What variables and registered dependencies are represented?

### VISUAL ODD
How does the simulator itself run?

Visual ODD is registry-driven. It is not a manually maintained diagram separate from the implementation.

For the current M0 it should expose:

- Initialisation
- Submodels / process schedule
- Observation
- Scales

This follows the 2024 Visual ODD structure while preserving the project's own scientific boundaries.

## Release rule

Alpha 0.4.0a0 is not complete merely when the UI redesign is complete.

The release requires:

- Narrative Laboratory foundation;
- registry-driven Visual ODD;
- eight-subsystem architecture recorded and validated;
- MOD.14–16 scientific scope recorded;
- no untested numerical mechanism introduced;
- explicit pattern-test contract for every future executable MOD.14–16 extension;
- all M0 regression, registry, build and browser tests passing.

Native GTK4/Granite/Flatpak remains a later v1-oriented implementation target; the web architecture should remain mappable to native patterns without binding the web code to a specific GTK widget.
