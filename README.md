<p align="center">
  <img src="assets/icon.png" alt="Cognitive Belief Dynamics icon" width="112">
</p>

<h2 align="center">Cognitive Belief Dynamics (CBD)</h2>

<p align="center">
  <a href="https://github.com/LaurentiuStaicu/cognitive-belief-dynamics/releases/latest"><img alt="Latest release" src="https://img.shields.io/github/v/tag/LaurentiuStaicu/cognitive-belief-dynamics?sort=semver&style=flat-square&label=release&color=333333"></a>
  <a href="https://github.com/LaurentiuStaicu/cognitive-belief-dynamics/actions/workflows/cbd-validation.yml"><img alt="CBD validation" src="https://img.shields.io/github/actions/workflow/status/LaurentiuStaicu/cognitive-belief-dynamics/cbd-validation.yml?branch=main&event=push&style=flat-square&label=CBD%20validation&color=707070"></a>
  <a href="LICENSING.md"><img alt="MIT / CC BY 4.0" src="https://img.shields.io/badge/license-MIT%20%2F%20CC%20BY%204.0-a0a0a0?style=flat-square"></a>
</p>

<p align="center"><small><strong>A research model for studying how information exposure, memory, corrective context, perceived source reliability and decision context can shape evolving cognitive states and probabilistic sharing decisions.</strong></small></p>

<p align="center"><small>
<a href="#what-is-cbd">Overview</a> ·
<a href="#conceptual-model">Conceptual model</a> ·
<a href="#research-questions-cbd-can-explore">Research questions</a> ·
<a href="#current-capabilities-and-scientific-limits">Capabilities & limits</a> ·
<a href="#using-and-reproducing-cbd">Use & reproduce</a> ·
<a href="#where-to-go-next">Documentation</a>
</small></p>

---

### What is CBD?

Cognitive Belief Dynamics (CBD) is a scientific model for studying how an agent's cognitive state can evolve over time as information is encountered, remembered, corrected, re-evaluated and acted upon.

Its central premise is that responses to information are **history-dependent**. The same message may have different effects depending on what an agent has previously seen, what corrective context remains accessible, how reliable the source is believed to be, and what incentives or accuracy cues are present when a decision is made.

CBD therefore represents cognition as a **dynamic process rather than a sequence of isolated reactions**. Earlier events can leave persistent effects, some of those effects can decay, repeated exposure can accumulate, and later decisions can depend on the state produced by the preceding history.

Technically, CBD is an **event-driven cognitive state-transition and agent-level stochastic dynamical model informed by systems thinking**. It is **not currently a formal System Dynamics model** because the present architecture does not yet implement a complete set of closed endogenous feedback loops.

CBD is intended as a transparent research model and computational reference implementation. It is not an end-user application, a truth-assessment system or a validated general model of human cognition.

### Research purpose

CBD addresses a problem that is difficult to study with isolated, one-step representations: the effect of information can depend on **what happened before**, **when it happened** and **what context is present when a later judgment or action is made**.

Exposure, correction, memory, source evaluation and decision context are therefore represented within a common temporal framework. This makes it possible to examine how candidate mechanisms interact across an information history instead of treating each mechanism as if it acted independently at a single moment.

The purpose of CBD is not to replace empirical research with simulation. It is to make assumptions explicit enough to be inspected, combined, challenged and progressively tested against evidence. In that role, the model can help distinguish consequences of a declared mechanism from claims that have actually been established empirically.

CBD is primarily intended for researchers, model reviewers and developers interested in cognitive and information dynamics who need a transparent computational framework with explicit assumptions, evidence boundaries and reproducible behavior.

### Conceptual model

CBD organizes the problem around four connected ideas.

| Concept | What it represents in CBD |
| --- | --- |
| **Information history** | What the agent has been exposed to, corrected about or told about a source over time |
| **Evolving cognitive state** | Persistent quantities that summarize how earlier information remains relevant to later processing |
| **Decision context** | The information and incentives present when the agent must form a judgment or decide whether to share |
| **Probabilistic action** | The fact that the same modeled state does not force a single deterministic behavior |

The current model represents several mechanisms that connect these ideas. Repeated exposure can increase familiarity with a claim. Corrective information can remain accessible and then become less available with time. Feedback can change the agent's estimate of a source's reliability. Prior belief, evidence, familiarity, corrective context and decision incentives can then combine to influence belief-related and sharing outcomes.

The important point is not the internal implementation of each calculation, but the **dependency structure**: present decisions can depend on accumulated history, timing and context rather than only on the most recent message.

<p align="center"><code>information history → evolving cognitive state → decision context → probabilistic action</code></p>

This also explains why CBD is dynamic. If two agents receive the same final message but arrive there through different prior histories, the model can represent different states at the moment of decision.

### Research questions CBD can explore

CBD is designed to support controlled research questions about information-processing dynamics rather than to produce a single universal prediction.

| Research question | What CBD provides |
| --- | --- |
| How can repeated exposure change later responses? | A persistent familiarity mechanism with bounded accumulation |
| How can the timing of corrections matter? | Corrective context that can persist and decay over time |
| How can judgments about a source affect later processing? | A source-reliability state that can be updated from feedback |
| Why can event order matter even when the same events occur? | State that carries information from earlier events into later ones |
| How can accuracy cues or incentives alter a decision? | Decision context that can change the relative influence of accuracy-related and other factors |
| How can uncertainty be represented without forcing identical outcomes? | Probabilistic decisions with reproducible stochastic simulation |
| How might information eventually propagate between agents? | A limited research path toward linking one agent's sharing action to another agent's later exposure |

These capabilities make CBD suitable for exploring **mechanisms, temporal ordering, path dependence, uncertainty and candidate feedback structures** under explicit assumptions.

### Current capabilities and scientific limits

CBD currently supports a working agent-level simulation in which exposure, correction and source feedback can alter persistent agent state, while decision events evaluate the state accumulated up to that point in the current decision context.

In the stable model, the sequence of information-related events is **supplied from outside the model**. CBD therefore represents how an agent changes across that history, but it does not yet generate a complete social information environment on its own.

Current development also contains a limited optional research path in which a sharing action can generate a later exposure for another eligible agent. This extends the model toward inter-agent propagation, but it does not yet create a complete self-sustaining feedback system.

The model can therefore be used to study dynamic cognitive mechanisms under controlled conditions, but its outputs must be interpreted within clear scientific boundaries:

- CBD is **not currently a validated predictor of individual or population human behavior**.
- It is not a truth detector, a diagnostic system or an automatic judge of whether a claim is correct.
- A mechanism being computationally implemented does not make it an established human cognitive law.
- Synthetic recovery, simulation tests and software verification do **not** by themselves establish human validation.
- The conceptual model is broader than the currently executable core.
- Evidence for one mechanism or component must not be generalized into validation of the whole model.
- Reproducibility of a simulation means that the same assumptions and inputs can reproduce the same computational result; it does not by itself establish real-world validity.

For the exact current implementation, evidence qualifications and open scientific gates, [STATUS.md](STATUS.md) is the canonical source.

### Research direction

CBD is intended to become more endogenous only where the scientific question and evidence justify doing so. The distinction between present capability and intended mature direction is deliberate.

| Area | Current model | Intended mature direction, if evidence supports it |
| --- | --- | --- |
| Information sequence | Supplied from outside the stable model | More future events can arise from earlier modeled actions |
| Inter-agent propagation | Limited optional sharing-to-exposure research path | Empirically constrained propagation across agents and networks |
| Network / platform context | Supplied explicitly when needed | Evidence-grounded mechanisms for how network and platform structure shape exposure and action |
| Feedback | No complete endogenous cognitive-social feedback system | Closed feedback structures where they are scientifically necessary |
| Learning / adaptation | Not part of the stable executable core | Explicit adaptation mechanisms with defined states and validation rules |
| Empirical status | Computational, synthetic and component-level evidence with explicit limits | Calibration and validation appropriate to each mechanism and population of interest |

A more mature CBD may therefore represent a cycle in which a decision to share affects another agent's exposure, that exposure changes the recipient's state, and the recipient's later state influences another decision. Whether such a structure should remain an event-driven agent model or justify a stronger System Dynamics classification must be determined by the actual scientific structure, not by a desire for uniformity across projects.

The objective is not maximum complexity. It is a model in which every added mechanism has a clear role, explicit assumptions, traceable evidence and an appropriate validation strategy.

### Using and reproducing CBD

For readers who want to inspect or run the computational model, CBD requires **Python 3.12 or newer**. The current development branch can be cloned and checked with:

~~~bash
git clone https://github.com/LaurentiuStaicu/cognitive-belief-dynamics.git
cd cognitive-belief-dynamics
python -m pip install .
cemodel validate --root .
cemodel demo
~~~

The default branch can contain scientifically reviewed work added after the latest public release. For a frozen, citable and reproducible snapshot, use the corresponding tag from [Releases](https://github.com/LaurentiuStaicu/cognitive-belief-dynamics/releases).

<details>
<summary><strong>Exact CI-oriented reproduction</strong></summary>

The canonical reference path is scoped to GitHub-hosted Ubuntu and CPython 3.12:

~~~bash
python -m pip install "pip==26.2.1"
python -m pip install -c requirements/ci-py312-linux.lock.txt build pytest hypothesis hatchling
python -m build --no-isolation
python -m pip install -c requirements/ci-py312-linux.lock.txt dist/*.whl
python -m compileall -q src scripts tests
python -m pytest
cemodel validate --root .
~~~

See [.github/workflows/cbd-validation.yml](.github/workflows/cbd-validation.yml).

</details>

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
