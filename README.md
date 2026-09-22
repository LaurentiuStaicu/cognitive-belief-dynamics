<p align="center">
  <img src="assets/icon.png" alt="Cognitive Belief Dynamics icon" width="112">
</p>

<h2 align="center">Cognitive Belief Dynamics (CBD)</h2>

<p align="center">
  <a href="https://github.com/LaurentiuStaicu/cognitive-belief-dynamics/releases/latest"><img alt="Latest release" src="https://img.shields.io/github/v/tag/LaurentiuStaicu/cognitive-belief-dynamics?sort=semver&style=flat-square&label=release&color=333333"></a>
  <a href="https://github.com/LaurentiuStaicu/cognitive-belief-dynamics/actions/workflows/cbd-validation.yml"><img alt="CBD validation" src="https://img.shields.io/github/actions/workflow/status/LaurentiuStaicu/cognitive-belief-dynamics/cbd-validation.yml?branch=main&event=push&style=flat-square&label=CBD%20validation&color=707070"></a>
  <a href="LICENSING.md"><img alt="MIT / CC BY 4.0" src="https://img.shields.io/badge/license-MIT%20%2F%20CC%20BY%204.0-a0a0a0?style=flat-square"></a>
</p>

<p align="center"><small><strong>A research model of how information exposure, memory, corrective context, source reliability and decision context can shape evolving agent states and probabilistic sharing decisions.</strong></small></p>

<p align="center"><small>
<a href="#what-is-cbd">Overview</a> ·
<a href="#model-at-a-glance">Model</a> ·
<a href="#current-capabilities-and-limits">Capabilities & limits</a> ·
<a href="#research-direction">Research direction</a> ·
<a href="#quick-start">Quick start</a> ·
<a href="#where-to-go-next">Documentation</a>
</small></p>

---

### What is CBD?

Cognitive Belief Dynamics (CBD) is a scientific model core for studying how a modeled agent's cognitive state can change across a sequence of information-related events.

The central idea is that a response to information need not depend only on the current message. Earlier exposure can increase familiarity, corrective information can remain accessible and later fade, feedback can change an agent's estimate of source reliability, and the state accumulated so far can influence a later decision.

This makes CBD a **dynamical model**: state persists through time, event order matters, some effects accumulate or decay, and action is probabilistic rather than represented as a fixed one-step response.

Technically, CBD is an **event-driven cognitive state-transition and agent-level stochastic dynamical model informed by systems thinking**. It is **not currently a formal System Dynamics model** because the present architecture does not yet implement a complete set of closed endogenous feedback loops.

CBD is intended as a transparent research model and computational reference implementation. It is not an end-user application and it is not a validated general model of human cognition.

### Model at a glance

| Dimension | Current CBD representation |
| --- | --- |
| Unit of analysis | A modeled agent whose state persists across events |
| Time | Ordered discrete events; elapsed time also matters for decay |
| Persistent state | Familiarity, corrective-context accessibility and estimated source reliability |
| Baseline agent inputs | Prior belief, accuracy baseline and sharing bias |
| Core event types | Exposure, correction, source feedback and decision |
| Decision-time context | Evidence signal, accuracy cue and reward context |
| Core dynamics | Bounded accumulation, temporal decay and nonlinear transformations |
| Decision output | Computed belief, sharing probability and a seeded stochastic share / no-share action |
| Current endogeneity | Stable release baseline is externally scheduled; limited inter-agent event generation exists only as an optional research path |
| Scientific boundary | Computational and synthetic verification do not by themselves establish human or population validation |
| Modeling paradigm | Event-driven agent-level dynamical model; not currently formal System Dynamics |

<p align="center"><code>event → state update → persisted memory / elapsed-time effects → decision context → probabilistic action</code></p>

### How CBD works

CBD advances when a relevant event occurs. This event-driven architecture is useful for questions in which exposure, correction, source feedback and decisions occur at identifiable times while agent state must persist between those events.

**1. The agent carries state forward.**  
The executable core stores familiarity with claims, accessibility of corrective context and estimated reliability for sources. It also stores baseline inputs used when a decision is evaluated.

**2. Each event has a defined role.**  
Exposure increases familiarity through a bounded saturating update. A correction increases access to corrective context. Source feedback adjusts the estimated reliability of the source toward the observed outcome. The model changes only the quantities associated with the event being processed.

**3. Timing changes later state.**  
Corrective-context accessibility decays as time passes. Two otherwise identical sequences can therefore produce different later states when their timing differs.

**4. A decision combines state with current context.**  
At decision time, CBD combines prior belief, familiarity, an evidence signal, source-reliability estimate and accessible corrective context. Accuracy cues and reward context can alter how accuracy-related and other incentives contribute to the decision calculation.

**5. Action remains stochastic.**  
The model converts the decision state into a sharing probability and uses a seeded random draw to determine whether sharing occurs. The seed makes the same run reproducible without making the underlying decision rule deterministic.

Every processed event is logged with its time, agent, event payload, state change and, when applicable, decision output. The computational path can therefore be inspected event by event.

### Current capabilities and limits

| CBD can currently… | Current boundary |
| --- | --- |
| Simulate ordered exposure, correction, source-feedback and decision events | Events are supplied to the stable release baseline from outside the model |
| Preserve state across events | Only explicitly implemented state variables persist |
| Represent familiarity accumulation and corrective-context decay | These are formal model mechanisms, not automatically established human cognitive laws |
| Update an estimated source-reliability state from feedback | The estimate is a model state, not a guarantee of real-world source quality |
| Compute decision-time belief and sharing probability | Outputs depend on the supplied model inputs and parameters |
| Produce reproducible stochastic share / no-share actions | Reproducibility comes from seeded randomness; it does not remove stochasticity |
| Log state transitions and observations | The log supports inspection and testing, not causal proof by itself |
| Validate schemas, registries and repository cross-references | Software/scientific-integrity checks are distinct from empirical validation |
| Experimentally schedule a delayed exposure for another eligible agent after sharing | This optional research path does not yet form a complete self-sustaining social-information feedback system |

CBD is **not currently a validated predictor of individual or population human behavior**, a truth detector, a diagnostic system or an automatic judge of whether a claim is correct. The conceptual model is broader than the currently executable core, and synthetic recovery or software verification do **not** by themselves establish human validation.

For the exact current implementation, evidence qualifications and open scientific gates, [STATUS.md](STATUS.md) is the canonical source.

### Research direction

CBD is intended to become more endogenous only where the scientific question and evidence justify doing so.

A more mature model may allow additional future events to arise from earlier modeled actions. For example, a decision to share may contribute to another agent's later exposure; that exposure may alter the recipient's state; and the recipient's later state may influence another decision. Network, platform and learning mechanisms can be integrated only when their system boundary, measurement meaning and validation strategy are explicit.

This direction does **not** require CBD to become a classical System Dynamics model. A change of modeling paradigm should occur only if the scientific problem requires feedback, interaction or emergence that the event-driven agent-level architecture cannot represent adequately.

The objective is therefore not maximum complexity. It is a model in which each added mechanism is explicit, testable, traceable and scientifically defensible.

### Quick start

CBD requires **Python 3.12 or newer** and Git if you want to clone the repository.

**1. Check Python**

~~~bash
python --version
~~~

**Expected result:** Python reports version 3.12 or newer. If your default Python is older, switch to a Python 3.12+ environment before continuing.

**2. Choose the snapshot you want to use**

For current development and the newest research state:

~~~bash
git clone https://github.com/LaurentiuStaicu/cognitive-belief-dynamics.git
cd cognitive-belief-dynamics
~~~

The default branch can contain scientifically reviewed work added after the latest public release. If you need a frozen, citable and reproducible snapshot instead, use the corresponding tag from [Releases](https://github.com/LaurentiuStaicu/cognitive-belief-dynamics/releases).

For routine development or experimentation, using an isolated Python environment is recommended before installing the package.

**3. Install CBD**

~~~bash
python -m pip install .
~~~

**Expected result:** installation completes without a dependency or build error.

**4. Validate the checkout**

~~~bash
cemodel validate --root .
~~~

**Expected result:** the command prints the canonical registry counts and exits successfully. A validation failure should be investigated rather than ignored because it can indicate a schema, reference or checkout-consistency problem.

**5. Run the demonstration**

~~~bash
cemodel demo
~~~

**Expected result:** JSON output showing two exposures followed by a decision for one example agent. The log exposes event order, state changes and the final decision observation.

If `cemodel` is not found after installation, confirm that the shell is using the same Python environment in which CBD was installed.

### Reproduce the computational baseline

For exact CI-oriented reproduction, the canonical reference path is scoped to GitHub-hosted Ubuntu and **CPython 3.12**:

~~~bash
python -m pip install "pip==26.2.1"
python -m pip install -c requirements/ci-py312-linux.lock.txt build pytest hypothesis hatchling
python -m build --no-isolation
python -m pip install -c requirements/ci-py312-linux.lock.txt dist/*.whl
python -m compileall -q src scripts tests
python -m pytest
cemodel validate --root .
~~~

The workflow also verifies a clean wheel installation, package metadata, bundled registries and the demonstration command. See [.github/workflows/cbd-validation.yml](.github/workflows/cbd-validation.yml).

A passing computational baseline means that the declared software, schemas, tests and retained scientific artifacts satisfy the repository's verification rules. It does **not** mean that the full model has been empirically validated as a model of human cognition.

### Where to go next

| If you want to… | Start here |
| --- | --- |
| Understand the exact current scientific boundary | [STATUS.md](STATUS.md) |
| Continue development or recover context after an interruption | [DEVELOPMENT.md](DEVELOPMENT.md) |
| See what changed and why | [CHANGELOG.md](CHANGELOG.md) |
| Inspect the executable implementation | [src/cognitive_epistemic_model/](src/cognitive_epistemic_model/) |
| Inspect canonical model, evidence and scientific contracts | [model/](model/) |
| Inspect schemas and validation structure | [schemas/](schemas/) and [tests/](tests/) |
| Reproduce a released snapshot | [releases/](releases/) and the corresponding Git tag |
| Cite CBD | [CITATION.cff](CITATION.cff) |

The landing page explains the model and its public scientific boundary. Internal experiment identifiers, audit codes, benchmark cell counts and development gates remain in the technical records where they support traceability, reproducibility and continuation of work.

### Support, citation and license

For reproducible software/test problems or scientific/model concerns, use the structured repository issue forms. See [Contributing](.github/CONTRIBUTING.md) and [Support](.github/SUPPORT.md).

If you use CBD in research, cite the exact released version using [CITATION.cff](CITATION.cff). Released tags are treated as immutable historical version points by project policy; release-specific notes and manifests are retained under [releases/](releases/).

CBD is maintained by **Laurentiu Staicu**. Source code and schemas are MIT licensed; original model registries, benchmark outputs, audit metadata and other original model data are CC BY 4.0 where applicable. Third-party materials retain their original terms. See [LICENSING.md](LICENSING.md).
