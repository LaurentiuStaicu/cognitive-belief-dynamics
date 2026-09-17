<!-- Shared InfoClar Model Suite product header reference: CEM / World3 / Macro -->
<p align="center">
  <img src="web/public/icon.svg" width="96" height="96" alt="Cognitive Epistemic Model icon">
</p>

<h1 align="center">Cognitive Epistemic Model</h1>

<p align="center">
  Understand belief-formation mechanisms, explore how factors interact, and compare priorities and actions through an evidence-aware research prototype.
</p>

<p align="center">
  <a href="https://github.com/LaurentiuStaicu/cognitive-epistemic-model/releases/tag/v0.4.3a0"><img alt="Version 0.4.3a0" src="https://img.shields.io/badge/Version-0.4.3a0-4e9a06"></a>
  <img alt="elementary OS: Web-first" src="https://img.shields.io/badge/elementary_OS-Web--first-64baff">
  <a href="#releases-and-licensing"><img alt="License: MIT + CC BY 4.0" src="https://img.shields.io/badge/License-MIT_%2B_CC_BY_4.0-blue"></a>
</p>

<table align="center" role="presentation">
  <tr>
    <td align="center" width="220"><a href="https://laurentiustaicu.github.io/cognitive-epistemic-model/"><strong>Open Web App</strong></a></td>
    <td align="center" width="220"><strong>Download Flatpak</strong><br><sub>Planned</sub></td>
  </tr>
</table>

> **Alpha 0.4.3a0 — Optimization & Visual Polish Consolidation.** M1 remains a candidate, uncalibrated extension retaining the M0 baseline.
> Software tests do not establish psychological validity or population prevalence.

This release consolidates the web Optimization Architecture through OA-8 and Visual Polish through VP-5. It does not activate M1.E4 or change the scientific outputs of the retained M0 / M1.E1–E3 mechanisms. See the [closure audit](docs/ALPHA_0.4.3a0_OA_VP_CLOSURE_AUDIT.md).

## Project priorities

1. Understand mechanisms through visual interactions and detailed explanations.
2. Prioritize factors to address under explicit objectives and assumptions.
3. Plan necessary actions and timing.

[Project priorities and elementary OS / Flatpak v1 direction](docs/PROJECT_PRIORITIES.md)
are persistent requirements. The web interface already follows a system-font,
light/dark, keyboard-accessible visual foundation for the future native app.

## Browser application

The interface runs in a modern browser on Linux, Windows and macOS. No Flatpak or
Windows installation is required. The public alpha is hosted on GitHub Pages.
Choose RO or EN in the application header.

- **Understanding (start here):** three integrated modes now separate explanation from
  execution without duplicating the model. **Theory** provides a 16-chapter bilingual
  reader with epistemic-status labels, validated cross-links and a contextual inspector.
  **Mechanisms** retains the M0 Narrative Laboratory plus the M1.E1 editorial-selection,
  M1.E2 presentation-framing and M1.E3 headline-access comparators. **Guided tour** leads the reader through
  ten deep-linked steps spanning theory, executable mechanisms, scenarios, evidence,
  validation and planning, with browser-history return to the exact tour step.
- **Interventions:** compare all 16 bundles under an effort budget, adjust objective
  weights and timing, inspect interactions and conditional factor priorities, test
  three response assumptions and export the analysis. See [scope and calculation](docs/INTERVENTIONS.md).
- **Scenarios:** four Python-generated reference runs, play/pause, step selection,
  exact values in a table and JSON export. Each step now explains state changes
  and decomposes belief/sharing latent scores into signed contributions.
- **Comparisons:** paired belief/sharing plots against repetition only, synchronized
  step inspection, mean differences, explicit input contrasts and JSON export.
- **Structure:** a computational map of core dependencies and optional contextual
  inputs, four mechanism focus views, keyboard-accessible node/link inspection,
  formulas and code provenance. The original evidence-registry map remains selectable.
- **Visual ODD:** a registry-driven view of Initialisation, Submodels, Observation and
  Scales, complemented by the [M0 ODD](docs/ODD_MAIN.md), [M1.E1 ODD](docs/ODD_M1.md) and [M1.E2 ODD](docs/ODD_M1_E2.md).
- **Registry:** nineteen variables, ten registered evidence-qualified links, four M1 empirical
  targets and twenty conceptual modules.

Scenarios replay saved output from the Python simulator; the browser does not
recalculate arbitrary parameter combinations. The computational map explains 17 dependencies, with coefficients in the details
  and contextual inputs optionally visible. It is separate from the evidence registry. Each registered link now includes a DOI source, a bilingual finding/limitation
summary and the scope of the bibliographic check. Phenomenon-level evidence is
separated from the candidate mechanism and uncalibrated functional form in M0.
See the [initial evidence audit](docs/EVIDENCE.md); this is not a systematic review.

### Pentru utilizatorii din România

Interfața pornește în română; butonul **EN / RO** schimbă limba. Poți selecta un
scenariu, urmări fiecare pas și compara convingerea cu probabilitatea de distribuire.
Pașii reprezintă unități abstracte, nu ani sau zile. Rulările sunt demonstrații ale
modelului, nu estimări despre persoane sau despre populația României.

## Scientific scope

The active candidate specification is **M1**, retaining **M0** as an explicit baseline.
M0 contains familiarity, correction accessibility, source-reliability estimation,
belief formation, accuracy salience and a sharing policy. M1.E1 adds a fixed
fact-compatible information pool, editorial emphasis, observed-sample balance and
issue appraisal. M1.E2 adds semantic-equivalent presentation framing, task-specific
prior-attitude congruence and active-engagement intent, explicitly distinct from M0
Share. M1.E3 adds a separate PreviewImpression → Access gate with a controlled
binary headline-negativity cue and a nested NULL comparator. Functional forms are
reference candidates, not established unique psychological laws.

- Simulated ground truth is never passed directly into the M0 belief-update function.
- Negative information is not equated with false information in M1.
- M1 issue appraisal `Aissue` is distinct from M0 claim-belief `B`.
- Published framing-effect magnitudes and interaction coefficients are empirical context, not fitted M1 parameters.
- `Gatt` is task-specific congruence, not ideology or party identity.
- `EngageIntent` and `Pengage` are distinct from M0 `Share` and its probability.
- `PreviewImpression`, `Access`, attention, belief, `EngageIntent` and `Share` remain distinct stages/constructs.
- The M1.E3 `Hneg` cue and logistic coefficients are demonstrative; Robertson et al. effect magnitudes are validation context, not fitted parameters.
- Track A/B are conceptual descriptions, not fixed classes or hard-coded agent states.
- Jungian individuation and the ego–Self axis remain a separate interpretive layer.
- A reproduced pattern is not proof of a unique mechanism.
- No Track A/B population estimates, individual diagnoses or Romania forecasts.

See [claim boundaries](docs/CLAIMS.md), [modelling decisions](docs/TRACE.md),
[M0 ODD](docs/ODD_MAIN.md), [M1.E1 ODD](docs/ODD_M1.md), [M1.E2 ODD](docs/ODD_M1_E2.md), [M1.E3 ODD](docs/ODD_M1_E3.md), [Alpha 0.4 scientific scope](docs/ALPHA_0.4_SCOPE.md)
and [development handoff](docs/HANDOFF.md).

## Run locally

Python 3.12+ and Node.js 24 are used by CI.

```bash
python -m pip install -e '.[test]'
python -m pytest
cemodel validate --root .
cemodel demo
python scripts/export_web.py
cd web
npm ci
npm run build
npm run preview
```

For browser regression checks:

```bash
npx playwright install chromium
npm run test:browser
```

Installed Python wheels contain registries and schemas: `cemodel validate` works
outside the source checkout. Web builds copy canonical registries automatically;
`python scripts/export_web.py` regenerates deterministic M0 reference runs, the M1.E1
editorial experiment, the M1.E2 nested presentation-model comparison, explicit run-purpose metadata and local M0 diagnostics. Software
version, active model specification (M1), retained baseline (M0) and evidence snapshot
are recorded separately.

## Verification and hosting

[GitHub Actions](https://github.com/LaurentiuStaicu/cognitive-epistemic-model/actions)
checks Python tests, installed package resources, exact regeneration of the saved
runs, TypeScript/build and browser interactions at desktop/mobile sizes. A successful
run provides a downloadable static web artifact. Deployment uses only that verified
artifact.

GitHub Pages is configured with **GitHub Actions** as its source. The dependent
**Publish web application** workflow deploys the verified build after successful
checks. The initial live deployment was confirmed on 2026-09-13.

## Releases and licensing

[Alpha 0.4.3a0 — Optimization & Visual Polish Consolidation release notes and downloads](https://github.com/LaurentiuStaicu/cognitive-epistemic-model/releases/tag/v0.4.3a0).
See [CHANGELOG.md](CHANGELOG.md). Releases attach the CI-verified web build and its
SHA-256 checksum and release provenance attestation; GitHub also provides source archives. The native elementary OS
Flatpak remains a near-v1 goal after the planned modules are integrated. This alpha has no native installer.

Original code: MIT. Original documentation and registries: CC BY 4.0.
See [LICENSING.md](LICENSING.md) for scope and third-party exclusions.
