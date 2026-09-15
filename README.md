<p align="center">
  <img src="web/public/icon.svg" width="96" height="96" alt="Cognitive Epistemic Model icon">
</p>

<h1 align="center">Cognitive Epistemic Model</h1>

<p align="center">
  Understand belief-formation mechanisms, explore how factors interact, and compare priorities and actions through an evidence-aware research prototype.
</p>

<p align="center">
  <a href="https://github.com/LaurentiuStaicu/cognitive-epistemic-model/releases"><img alt="Latest alpha release" src="https://img.shields.io/github/v/release/LaurentiuStaicu/cognitive-epistemic-model?display_name=tag&include_prereleases&sort=semver"></a>
  <img alt="Development stage: alpha" src="https://img.shields.io/badge/stage-alpha-e5a50a">
  <img alt="Available application: Web" src="https://img.shields.io/badge/app-Web-4a90d9">
  <img alt="elementary OS Flatpak: planned" src="https://img.shields.io/badge/elementary_OS_Flatpak-planned-64baff">
  <a href="LICENSE"><img alt="Code license: MIT" src="https://img.shields.io/badge/code_license-MIT-blue"></a>
  <a href="LICENSING.md"><img alt="Documentation license: CC BY 4.0" src="https://img.shields.io/badge/docs-CC_BY_4.0-blue"></a>
</p>

<p align="center">
  <a href="https://laurentiustaicu.github.io/cognitive-epistemic-model/">
    <img alt="Deschide aplicația / Open app" src="https://img.shields.io/badge/Deschide_aplica%C8%9Bia_%2F_Open_app-087F73?style=for-the-badge">
  </a>
</p>

> **Alpha 0.4.0a0.** M1 is a candidate, uncalibrated extension retaining the M0 baseline.
> Software tests do not establish psychological validity or population prevalence.

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

- **Understanding (start here):** the M0 Narrative Laboratory combines full explanatory
  prose with a contextual inspector and four temporal mechanism paths. A separate M1
  editorial-emphasis laboratory holds one fact-compatible information pool fixed and
  compares negative, neutral and positive observed samples against a nested null model.
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
  Scales, complemented by the [M0 ODD](docs/ODD_MAIN.md) and [M1 ODD](docs/ODD_M1.md).
- **Registry:** eleven variables, five registered evidence-qualified links, one M1 empirical
  target and twenty conceptual modules.

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
issue appraisal. Functional forms are reference candidates, not established unique
psychological laws.

- Simulated ground truth is never passed directly into the M0 belief-update function.
- Negative information is not equated with false information in M1.
- M1 issue appraisal `Aissue` is distinct from M0 claim-belief `B`.
- Published framing-effect magnitudes are empirical context, not fitted M1 parameters.
- Track A/B are conceptual descriptions, not fixed classes or hard-coded agent states.
- Jungian individuation and the ego–Self axis remain a separate interpretive layer.
- A reproduced pattern is not proof of a unique mechanism.
- No Track A/B population estimates, individual diagnoses or Romania forecasts.

See [claim boundaries](docs/CLAIMS.md), [modelling decisions](docs/TRACE.md),
[M0 ODD](docs/ODD_MAIN.md), [M1 ODD](docs/ODD_M1.md), [Alpha 0.4 scientific scope](docs/ALPHA_0.4_SCOPE.md)
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
editorial experiment, explicit run-purpose metadata and local M0 diagnostics. Software
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

[Alpha 0.4.0a0 — release notes and downloads](https://github.com/LaurentiuStaicu/cognitive-epistemic-model/releases/tag/v0.4.0a0).
See [CHANGELOG.md](CHANGELOG.md). Releases attach the CI-verified web build and its
SHA-256 checksum and release provenance attestation; GitHub also provides source archives. The native elementary OS
Flatpak remains a near-v1 goal. This alpha has no native installer.

Original code: MIT. Original documentation and registries: CC BY 4.0.
See [LICENSING.md](LICENSING.md) for scope and third-party exclusions.
