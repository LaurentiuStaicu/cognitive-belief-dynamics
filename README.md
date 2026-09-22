<p align="center">
  <img src="assets/icon.png" alt="Cognitive Belief Dynamics icon" width="112">
</p>

<h2 align="center">Cognitive Belief Dynamics (CBD)</h2>

<p align="center">
  <a href="https://github.com/LaurentiuStaicu/cognitive-belief-dynamics/releases/latest"><img alt="Latest release" src="https://img.shields.io/github/v/tag/LaurentiuStaicu/cognitive-belief-dynamics?sort=semver&style=flat-square&label=release&color=333333"></a>
  <a href="https://github.com/LaurentiuStaicu/cognitive-belief-dynamics/actions/workflows/cbd-validation.yml"><img alt="CBD validation" src="https://img.shields.io/github/actions/workflow/status/LaurentiuStaicu/cognitive-belief-dynamics/cbd-validation.yml?branch=main&event=push&style=flat-square&label=CBD%20validation&color=707070"></a>
  <a href="LICENSING.md"><img alt="MIT / CC BY 4.0" src="https://img.shields.io/badge/license-MIT%20%2F%20CC%20BY%204.0-a0a0a0?style=flat-square"></a>
</p>

<p align="center"><small><strong>An event-driven cognitive state-transition and agent-level stochastic dynamical model for studying how information, memory, uncertainty and context can change modeled agent states and decisions over time.</strong></small></p>

<p align="center"><small>
<a href="#what-is-cbd">Overview</a> ·
<a href="#how-cbd-works">How it works</a> ·
<a href="#what-cbd-can-do-today">Capabilities</a> ·
<a href="#research-direction">Research direction</a> ·
<a href="#limitations-and-scientific-boundaries">Limitations</a> ·
<a href="#quick-start">Quick start</a> ·
<a href="#reproduce-the-computational-baseline">Reproduce</a> ·
<a href="#where-to-go-next">Documentation</a>
</small></p>

---

### What is CBD?

Cognitive Belief Dynamics (CBD) is a scientific model core for studying how an agent's modeled cognitive state can change across a sequence of information-related events.

The central idea is simple: what happens now can depend on what happened before. Repeated exposure can increase familiarity, corrective information can remain accessible and then fade with time, feedback about a source can change estimated source reliability, and the agent's current state can influence a later probabilistic decision.

CBD is therefore a **dynamical model**: state persists through time, event order matters, some effects accumulate or decay, and decisions are not represented as fixed one-step responses.

Technically, CBD is an **event-driven cognitive state-transition and agent-level stochastic dynamical model informed by systems thinking**. It is **not currently a formal System Dynamics model** because the present architecture does not yet contain a complete set of closed endogenous feedback loops.

<p align="center"><code>information event → agent state update → memory / decay → decision context → probabilistic action</code></p>

### How CBD works

CBD represents agents, persistent state, ordered events and decision rules. The model advances when an event occurs rather than by continuously updating every variable at every instant.

**1. An agent carries state forward.**  
The executable core stores quantities such as familiarity with a claim, accessibility of corrective context and an estimated reliability for a source. It also stores baseline inputs used when a decision is made, such as prior belief, accuracy orientation and sharing bias.

**2. Events change only the parts of state they are meant to affect.**  
An exposure increases familiarity using a bounded saturating update. A correction increases access to corrective context. Source feedback moves the estimated reliability of a source toward the observed outcome. These updates are explicit and inspectable.

**3. Time can change what remains available.**  
Corrective-context accessibility decays as time passes. This means that identical events can have different consequences depending on their timing and on the state accumulated beforehand.

**4. A decision combines current state and current context.**  
At decision time, CBD combines prior belief, familiarity, an evidence signal, estimated source reliability and accessible corrective context. Accuracy cues and reward context can alter the weight given to accuracy versus other incentives. Nonlinear transformations keep the resulting quantities bounded.

**5. Action is probabilistic rather than predetermined.**  
The model computes a sharing probability and uses a seeded random draw to determine whether sharing occurs. The seed makes a run reproducible while preserving stochastic behavior.

Every processed event is logged with its time, agent, input payload, state change and, when applicable, decision output. This makes the computational path inspectable rather than hiding the result behind a single final number.

### What CBD can do today

The current repository can:

- simulate ordered exposure, correction, source-feedback and decision events for one or more agents;
- preserve agent state across events so that earlier events can influence later ones;
- represent bounded accumulation, temporal decay and nonlinear transformations;
- compute belief-related and sharing outcomes from the modeled state and decision context;
- generate seeded stochastic decisions that can be reproduced exactly when the same inputs and seed are used;
- record event-by-event state changes and observations for inspection and testing;
- validate the repository's scientific registries, schemas and cross-references through the supplied command-line validator.

The stable release baseline uses externally supplied event schedules. Current development work also includes an optional research path in which a realised sharing action can schedule a delayed exposure for another eligible agent under an explicitly supplied network and transmission policy. This is a limited research capability, not a complete self-sustaining social-information system.

The exact release-versus-development boundary changes as the research progresses. [STATUS.md](STATUS.md) is the canonical source for that boundary.

### Research direction

CBD is intended to evolve by adding endogenous behavior only where the scientific question and evidence justify it.

A mature version may progressively allow more future events to arise from earlier modeled actions: for example, a decision to share may influence another agent's exposure, that exposure may alter later state, and later state may affect another decision. Network, platform and learning mechanisms can be added only when their system boundary, measurement meaning and validation strategy are explicit.

This direction does **not** imply that CBD must become a classical System Dynamics model. The modeling paradigm should change only if the scientific problem requires structures that the event-driven agent-level architecture cannot represent adequately.

The aim is therefore not to maximize model complexity. It is to make each added mechanism explicit, testable, traceable and scientifically defensible.

### Limitations and scientific boundaries

CBD should not be interpreted as more than the evidence and implementation support.

- It is **not currently a complete endogenous System Dynamics model**.
- It is **not a validated predictor of individual human behavior or population behavior**.
- It is **not a truth detector, diagnostic system or automatic judge of whether a claim is correct**.
- A computationally executable mechanism is not automatically an empirically established cognitive law.
- Synthetic recovery, simulation tests and software verification can show that a mechanism is implemented or recoverable under controlled conditions; they do **not** by themselves establish human validation.
- The conceptual model is broader than the currently executable core. A concept being documented in the repository does not mean that it already runs in the simulator.
- Empirical evidence is retained with explicit scope and qualification. Partial evidence for one component must not be generalized into validation of the whole model.

For the exact current scientific state, evidence qualifications and open research gates, use [STATUS.md](STATUS.md) rather than inferring them from this introductory page.

### Quick start

CBD requires **Python 3.12 or newer**.

**1. Check Python**

~~~bash
python --version
~~~

The reported version must be 3.12 or newer. If your default Python is older, use a Python 3.12+ environment before continuing.

**2. Clone the repository**

~~~bash
git clone https://github.com/LaurentiuStaicu/cognitive-belief-dynamics.git
cd cognitive-belief-dynamics
~~~

**3. Install the package**

~~~bash
python -m pip install .
~~~

**4. Validate the repository**

~~~bash
cemodel validate --root .
~~~

A successful validation prints the registry counts and returns without an error. A validation failure should not be ignored: it can indicate a schema, reference or checkout-consistency problem.

**5. Run the demonstration**

~~~bash
cemodel demo
~~~

The demo processes two exposures followed by a decision for one example agent and prints the event log as JSON. The output lets you see the ordered events, the state changes they produced and the final decision observation.

If the cemodel command is not found after installation, confirm that you are using the same Python environment in which the package was installed.

### Reproduce the computational baseline

For exact CI-oriented reproduction, the canonical path is scoped to GitHub-hosted Ubuntu and **CPython 3.12**:

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

The public landing page describes the model and its usable scientific boundary. Internal experiment identifiers, audit codes, benchmark cell counts and development gates are retained in the technical files where they support traceability, reproducibility and continuation of work.

### Support, citation and license

For reproducible software/test problems or scientific/model concerns, use the structured repository issue forms. See [Contributing](.github/CONTRIBUTING.md) and [Support](.github/SUPPORT.md).

If you use CBD in research, cite the exact released version using [CITATION.cff](CITATION.cff). Released tags are treated as immutable historical version points; release-specific notes and manifests are retained under [releases/](releases/).

CBD is maintained by **Laurentiu Staicu**. Source code and schemas are MIT licensed; original model registries, benchmark outputs, audit metadata and other original model data are CC BY 4.0 where applicable. Third-party materials retain their original terms. See [LICENSING.md](LICENSING.md).
