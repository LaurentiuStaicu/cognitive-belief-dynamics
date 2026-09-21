<p align="center">
  <img src="assets/icon.png" alt="Cognitive Belief Dynamics icon" width="112">
</p>

<h2 align="center">Cognitive Belief Dynamics (CBD)</h2>

<p align="center">
  <a href="https://github.com/LaurentiuStaicu/cognitive-belief-dynamics/releases/latest"><img alt="Version: 0.1.0" src="https://img.shields.io/github/v/tag/LaurentiuStaicu/cognitive-belief-dynamics?sort=semver&style=flat-square&label=release&color=333333"></a>
  <a href="https://github.com/LaurentiuStaicu/cognitive-belief-dynamics/actions/workflows/cbd-validation.yml"><img alt="CBD validation" src="https://img.shields.io/github/actions/workflow/status/LaurentiuStaicu/cognitive-belief-dynamics/cbd-validation.yml?branch=main&event=push&style=flat-square&label=CBD%20validation&color=707070"></a>
  <a href="LICENSING.md"><img alt="MIT / CC BY 4.0" src="https://img.shields.io/badge/license-MIT%20%2F%20CC%20BY%204.0-a0a0a0?style=flat-square"></a>
</p>

<p align="center"><small><strong>An event-driven cognitive state-transition and agent-level stochastic dynamical model of how information, memory, uncertainty and context can change agent states over time.</strong></small></p>

<p align="center"><small>
<a href="#what-is-cbd">Overview</a> ·
<a href="#model-at-a-glance">Model structure</a> ·
<a href="#scientific-status-at-a-glance">Scientific status</a> ·
<a href="#reproduce-the-computational-baseline">Reproduce</a> ·
<a href="#evidence-contracts-and-provenance">Evidence & provenance</a> ·
<a href="#documentation">Documentation</a>
</small></p>

---

### What is CBD?

Cognitive Belief Dynamics (CBD) is a scientific model core for representing how persistent agent-level cognitive states can change across ordered information events through memory, saturation, decay, nonlinear transformations and stochastic decisions.

CBD is a **dynamical model informed by systems thinking**, but it is **not currently a formal System Dynamics model**. The present implementation does not contain the closed endogenous feedback structure required for that classification: for example, a Share action does not automatically create future exposure, and event schedules remain externally supplied.

CBD also separates what is executable from what is empirical, conceptual or interpretive. This prevents mathematical reference operators, theoretical framing and synthetic recovery benchmarks from being presented as stronger evidence than they actually provide.

### Model at a glance

| Dimension | CBD boundary |
| --- | --- |
| Canonical paradigm | Event-driven cognitive state-transition and agent-level stochastic dynamical model |
| Core dynamics | Persistent states, temporal ordering, memory, saturation, decay, nonlinear transformations, stochastic decisions |
| Event boundary | Event schedule externally supplied; Share does not automatically generate future exposure |
| Evidence levels | EXECUTABLE, EMPIRICAL, CONCEPTUAL, INTERPRETIVE |
| MOD.14 | Normative proposition-level Bayesian reference operator with explicit uncertainty |
| M1.E4 retained evidence | Synthetic model-recovery / identifiability-discrimination benchmarks |
| Human validation | Not established |
| Current public release | **v0.1.0 scientific-core baseline** |

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/readme/cbd-concept-overview-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="assets/readme/cbd-concept-overview-light.svg">
    <img src="assets/readme/cbd-concept-overview-light.svg" width="760" alt="Diagram showing CBD agent states, event-driven updates, nonlinear dynamics, evidence levels and validation boundaries.">
  </picture>
</p>

The figure is an orientation view, not a causal-loop diagram. It deliberately avoids closed-loop System Dynamics notation because CBD does not currently implement that paradigm.

### How CBD is structured

| Layer | Role | Current boundary |
| --- | --- | --- |
| **Persistent agent state** | Stores belief-related states, familiarity, memory and source-related estimates between events | Agent-level state, not a population calibration |
| **Event-driven updates** | Applies exposure, access, correction, presentation and evidence events in explicit temporal order | Event schedule remains exogenous |
| **Memory / decay / nonlinear dynamics** | Represents saturation, memory persistence/decay, nonlinear transformations and stochastic decisions | Dynamical behavior without closed endogenous SD loops |
| **Evidence levels** | Separates executable relations from empirical claims, conceptual organization and interpretive theory | Levels must not be collapsed into one validation claim |
| **Validation boundary** | Uses synthetic recovery/identifiability benchmarks where retained | Synthetic success is not human validation |

### Scientific status at a glance

| Scientific dimension | Current state |
| --- | --- |
| Canonical paradigm | **Event-driven cognitive state-transition / agent-level stochastic dynamics** |
| Formal System Dynamics classification | **No** |
| Public scientific-core release | **v0.1.0** |
| Evidence levels | **Executable / empirical / conceptual / interpretive** |
| M1.E4 participant-aware confirmation | **PASS — 18 / 18 primary P64_X10 cells meet the 0.80 recovery gate** |
| Minimum observed participant-confirmation recovery | **0.92** |
| Phase M protocol robustness | **PROTOCOL_ROBUSTNESS_FAIL — 3 / 18 cells below 0.80; minimum recovery 0.56** |\n| M1.E4 result type | **Synthetic recovery / identifiability-discrimination only** |
| Human-participant validation | **Not established** |
| Pencode | **Not identified or estimated** |
| Participant recruitment | **Not authorized by current baseline** |

MOD.14 provides a transparent normative reference computation when a defensible prior probability and diagnostic likelihood ratio are supplied. It is **not** a population-calibrated cognitive law, **not a literal neural implementation of Bayes**, and not a truth oracle.

For the exact current scientific boundary, see [STATUS.md](STATUS.md).

### What CBD establishes — and what it does not

**CBD currently provides:**

- a canonical model specification and computational reference implementation;
- persistent state and ordered event-update mechanisms;
- schemas and model/evidence contracts;
- explicit separation of executable, empirical, conceptual and interpretive claims;
- retained calibration and synthetic model-recovery benchmark artifacts;
- integrity/provenance artifacts for retained benchmarks;
- Python build/test validation for the computational baseline.

**CBD does not currently establish:**

- that CBD is a formal System Dynamics model;
- population calibration of the full model;
- human-participant validation of M1.E4;
- EVSD or 2HT as the true human recognition architecture;
- identification or estimation of Pencode;
- authorization of participant recruitment;
- that MOD.14 is a literal neural implementation of Bayes;
- a general-purpose truth, prediction, diagnostic or decision system.

### Reproduce the computational baseline

CBD requires **Python 3.12 or newer**.

The GitHub validation workflow builds the package from source, checks a clean wheel installation and runs the retained Python test suite:

~~~bash
python -m pip install --upgrade pip build pytest
python -m build
python -m pip install dist/*.whl
python -m compileall -q src scripts tests
python -m pytest -q
~~~

A successful run verifies package/build integrity and the retained executable test patterns. It does **not** constitute human validation, population calibration or empirical identification of every conceptual mechanism.

See [.github/workflows/cbd-validation.yml](.github/workflows/cbd-validation.yml) for the canonical automated path.

Retained M1.E4 benchmark reproduction scripts are under [scripts/](scripts/). Their results must be interpreted through the corresponding contracts in [model/contracts/](model/contracts/).

### Evidence, contracts and provenance

CBD treats evidence status as part of the model specification.

~~~text
model variable / mechanism
          ↓
evidence or measurement contract
          ↓
executable / empirical / conceptual / interpretive status
          ↓
calibration or synthetic recovery benchmark
          ↓
bounded scientific interpretation
~~~

Important boundaries include:

- synthetic recovery is not human validation;
- normative computation is not descriptive cognitive truth;
- source/provenance cues are not automatically diagnostic likelihood ratios;
- uncertainty estimates are not truth certification;
- failed or inconclusive benchmark cells remain scientific results rather than being converted into positive model-selection claims.

### Repository map

| Path | Purpose |
| --- | --- |
| [src/cognitive_epistemic_model/](src/cognitive_epistemic_model/) | Executable computational/reference implementation |
| [model/](model/) | Canonical model registries, variables, processes, links and evidence snapshots |
| [model/contracts/](model/contracts/) | Measurement, evidence, benchmark and world-model contracts |
| [model/benchmarks/](model/benchmarks/) | Frozen synthetic recovery configurations and retained outputs |
| [schemas/](schemas/) | JSON schemas for canonical model artifacts |
| [scripts/](scripts/) | M1.E4 retained benchmark reproduction scripts |
| [tests/](tests/) | Executable model-pattern and regression tests |
| [releases/](releases/) | Frozen release notes |

### Where should I start?

| If you want to… | Start here |
| --- | --- |
| Understand the paradigm | This README → **How CBD is structured** |
| See the exact scientific boundary | [STATUS.md](STATUS.md) |
| Inspect canonical variables/processes | [model/](model/) |
| Inspect evidence and benchmark contracts | [model/contracts/](model/contracts/) |
| Inspect retained synthetic recovery results | [model/benchmarks/](model/benchmarks/) |
| Reproduce executable tests | **Reproduce the computational baseline** above |
| Contribute | [Contributing](.github/CONTRIBUTING.md) |
| Get support | [Support](.github/SUPPORT.md) |
| Cite CBD | [CITATION.cff](CITATION.cff) |

### Documentation

- [STATUS.md](STATUS.md) — canonical paradigm and validation boundary.
- [model/contracts/world_model_v1.json](model/contracts/world_model_v1.json) — MOD.14 world-model contract and epistemic-level separation.
- [model/benchmarks/README.md](model/benchmarks/README.md) — retained synthetic benchmark interpretation.
- [LICENSING.md](LICENSING.md) — licensing scope for code, schemas, model artifacts and benchmark outputs.
- [CHANGELOG.md](CHANGELOG.md) — released and unreleased changes.
- [releases/](releases/) — frozen release notes.
- [CITATION.cff](CITATION.cff) — citation metadata.

### Support, citation and license

For reproducible software/test problems or scientific/model concerns, use the structured repository issue forms. See [Contributing](.github/CONTRIBUTING.md) and [Support](.github/SUPPORT.md).

If you use CBD in research, cite the exact released version using [CITATION.cff](CITATION.cff).

CBD is maintained by **Laurentiu Staicu**. Source code and schemas are MIT licensed; original model registries, calibration artifacts, benchmark outputs and other original model data are CC BY 4.0 where applicable. See [LICENSING.md](LICENSING.md) for the exact scope.
