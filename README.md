<p align="center">
  <img src="assets/icon.png" alt="Cognitive Belief Dynamics icon" width="112">
</p>

<h2 align="center">Cognitive Belief Dynamics (CBD)</h2>

<p align="center">
  <a href="https://github.com/LaurentiuStaicu/cognitive-belief-dynamics/releases/latest"><img alt="Latest release" src="https://img.shields.io/github/v/tag/LaurentiuStaicu/cognitive-belief-dynamics?sort=semver&style=flat-square&label=release&color=333333"></a>
  <a href="https://github.com/LaurentiuStaicu/cognitive-belief-dynamics/actions/workflows/cbd-validation.yml"><img alt="CBD validation" src="https://img.shields.io/github/actions/workflow/status/LaurentiuStaicu/cognitive-belief-dynamics/cbd-validation.yml?branch=main&event=push&style=flat-square&label=CBD%20validation&color=707070"></a>
  <a href="LICENSING.md"><img alt="MIT / CC BY 4.0" src="https://img.shields.io/badge/license-MIT%20%2F%20CC%20BY%204.0-a0a0a0?style=flat-square"></a>
</p>

<p align="center"><small><strong>A research model of how information exposure, memory, corrective context, perceived source reliability and decision context influence modeled cognitive states and probabilistic sharing decisions over time.</strong></small></p>

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

Cognitive Belief Dynamics (CBD) studies how the cognitive state of a modeled agent — a simplified representation of an information-processing individual — can evolve as information is encountered, remembered, corrected, re-evaluated and acted upon.

Its central premise is that responses to information are **history-dependent**. The same message may have different effects depending on prior exposure, accessible corrective context, perceived source reliability and the context in which a later decision is made.

CBD therefore represents information-related cognition as a **dynamic process rather than a sequence of isolated reactions**: earlier effects can persist or decay, repeated exposure can accumulate, and later decisions can depend on the preceding history. Its scope is intentionally narrower than cognition as a whole.

Technically, CBD is an **event-driven cognitive state-transition and agent-level stochastic dynamical model informed by systems thinking**. It is **not currently a formal System Dynamics model** because it lacks a complete set of closed endogenous feedback loops. CBD is a research model and computational reference implementation, not an end-user application, truth-assessment system or validated general model of human cognition.

### Research purpose

CBD addresses a problem that one-step representations handle poorly: information effects can depend on **what happened before**, **when it happened** and **what context is present at a later judgment or action**. Exposure, correction, memory, source evaluation and decision context are therefore represented within one temporal framework.

CBD does not replace empirical research with simulation. Its purpose is to make assumptions explicit enough to inspect, combine, challenge and progressively test against evidence, helping separate the consequences of a declared mechanism from claims that have actually been established empirically.

The model is primarily intended for researchers, model reviewers and developers interested in cognitive and information dynamics who need explicit assumptions, evidence boundaries and reproducible behavior.

### Conceptual model

CBD organizes the problem around four connected ideas.

- **Information history:** what the agent has been exposed to, corrected about or told about a source over time.
- **Evolving cognitive state:** persistent quantities that summarize how earlier information remains relevant to later processing.
- **Decision context:** the information and incentives present when the agent must form a judgment or decide whether to share.
- **Probabilistic action:** the same modeled state does not force a single deterministic behavior.

The current model represents several mechanisms that connect these ideas. Repeated exposure can increase familiarity with a claim. Corrective information can remain accessible and then become less available with time. Feedback can change the agent's estimate of a source's reliability. Prior belief, evidence, familiarity, corrective context and decision incentives can then combine to influence belief-related and sharing outcomes.

The key idea is the **dependency structure**: present decisions can depend on accumulated history, timing and context rather than only on the most recent message.

<p align="center"><code>information history → evolving cognitive state → decision context → probabilistic action</code></p>

If two agents receive the same final message through different prior histories, CBD can represent different states at the moment of decision.

### Research questions CBD can explore

CBD is designed to support controlled research questions about information-processing dynamics rather than to produce a single universal prediction.

- **Repeated exposure:** how can repeated encounters with the same claim change later responses? CBD allows familiarity to accumulate while remaining bounded.
- **Timing of corrections:** how can a correction matter differently depending on when it occurs? Corrective context can remain available for a period and become less accessible with time.
- **Source judgments:** how can perceived source reliability affect later processing? CBD can revise that estimate when feedback is supplied.
- **Event order:** why can the same set of events lead to different later states when the order changes? Earlier events can alter the state carried into later ones.
- **Decision context:** how can accuracy cues or incentives alter a judgment or sharing decision? Their influence is represented at the moment of decision.
- **Uncertainty:** how can the model avoid forcing identical outcomes from identical-looking situations? Decisions can remain probabilistic while simulations remain reproducible.
- **Inter-agent propagation:** how might one agent's action eventually affect another agent's information history? An experimental path can link sharing to a later exposure.

These capabilities make CBD suitable for exploring **mechanisms, temporal ordering, path dependence, uncertainty and possible feedback structures** under explicit assumptions.

### Scientific foundations

CBD separates evidence for a **phenomenon** from evidence for a particular **model mechanism, mathematical form or parameter value**. Support for one level is not automatically treated as validation of the others.

The repository links modeled relationships to cited research and records scope limitations alongside those links. [STATUS.md](STATUS.md) summarizes the current scientific boundary, while the machine-readable model and evidence records are retained under [model/](model/) for audit and reproducibility. The retained evidence set is an auditable project resource, not a systematic review or a dataset for population calibration.

### Current capabilities and scientific limits

CBD currently supports a working agent-level simulation in which exposure, correction and source feedback can alter persistent agent state, while decision events evaluate the state accumulated up to that point in the current decision context. At decision time, the model can produce belief-related outputs, a sharing probability and a probabilistic share / no-share outcome.

In the stable model, the sequence of information-related events is **supplied from outside the model**. CBD therefore represents how an agent changes across that history, but it does not yet generate a complete social information environment on its own.

Current development also contains a limited optional research path in which a sharing action can generate a later exposure for another eligible agent. This extends the model toward inter-agent propagation, but it does not yet create a complete self-sustaining feedback system.

CBD can therefore be used to study dynamic cognitive mechanisms under controlled conditions, but its outputs have clear scientific boundaries:

- CBD is **not currently a validated predictor of individual or population human behavior**.
- It is not a truth detector, a diagnostic system or an automatic judge of whether a claim is correct.
- A mechanism being computationally implemented does not make it an established human cognitive law.
- Synthetic recovery, simulation tests and software verification do **not** by themselves establish human validation.
- Not every concept documented in CBD is currently implemented in the simulator.
- Evidence for one mechanism or component must not be generalized into validation of the whole model.
- Reproducibility of a simulation means that the same assumptions and inputs can reproduce the same computational result; it does not by itself establish real-world validity.

For the exact current implementation, evidence qualifications and unresolved scientific questions, [STATUS.md](STATUS.md) is the canonical source.

### Research direction

CBD is intended to generate more of its own future information sequence from earlier modeled actions only where the scientific question and evidence justify doing so. The distinction between present capability and intended mature direction is deliberate.

- **Information sequence:** Current — supplied from outside the stable model. Possible mature direction — more future events arise from earlier modeled actions.
- **Inter-agent propagation:** Current — limited sharing-to-exposure research path. Possible mature direction — empirically constrained propagation across agents and networks.
- **Network / platform context:** Current — supplied when needed. Possible mature direction — evidence-grounded effects on exposure and action.
- **Feedback:** Current — no complete action-to-information-to-action cycle. Possible mature direction — closed feedback where scientifically necessary.
- **Broader adaptation:** Current — specific states update, but there is no general adaptive learning system. Possible mature direction — additional adaptation with explicit states, evidence and validation.
- **Empirical status:** Current — computational, synthetic and component-level evidence. Possible mature direction — calibration and validation appropriate to each mechanism and population.

A more mature CBD may represent a cycle in which sharing affects another agent's exposure, that exposure changes the recipient's state, and the recipient's later state influences another decision. Whether this should remain an event-driven agent model or eventually justify describing CBD as formal System Dynamics must follow the scientific structure, not a desire for uniformity across projects.

The objective is not maximum complexity, but mechanisms with clear roles, explicit assumptions, traceable evidence and appropriate validation.

### Using and reproducing CBD

For readers who want to inspect or run the computational model, CBD requires **Python 3.12 or newer**. The current development branch can be cloned and checked with:

~~~bash
git clone https://github.com/LaurentiuStaicu/cognitive-belief-dynamics.git
cd cognitive-belief-dynamics
python -m pip install .
cemodel validate --root .
cemodel demo
~~~

The default branch can contain post-release research changes that have passed the repository's review and CI gates. For a frozen, citable and reproducible snapshot, use the corresponding tag from [Releases](https://github.com/LaurentiuStaicu/cognitive-belief-dynamics/releases).

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

- **Current scientific boundary:** [STATUS.md](STATUS.md)
- **Model definitions and evidence records:** [model/](model/)
- **Executable implementation:** [src/cognitive_epistemic_model/](src/cognitive_epistemic_model/)
- **Reproducibility and verification:** [schemas/](schemas/) and [tests/](tests/)
- **Change history:** [CHANGELOG.md](CHANGELOG.md)
- **Development continuity:** [DEVELOPMENT.md](DEVELOPMENT.md)
- **Released snapshots:** [releases/](releases/) and the corresponding Git tag
- **Citation:** [CITATION.cff](CITATION.cff)


### Support, citation and license

For reproducible software/test problems or scientific/model concerns, use the structured repository issue forms. See [Contributing](.github/CONTRIBUTING.md) and [Support](.github/SUPPORT.md).

If you use CBD in research, cite the exact released version using [CITATION.cff](CITATION.cff). Released tags are treated as immutable historical version points by project policy; release-specific notes and manifests are retained under [releases/](releases/).

CBD is maintained by **Laurentiu Staicu**. Source code and schemas are MIT licensed; original model registries, benchmark outputs, audit metadata and other original model data are CC BY 4.0 where applicable. Third-party materials retain their original terms. See [LICENSING.md](LICENSING.md).
