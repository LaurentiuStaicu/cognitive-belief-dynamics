# Cognitive Epistemic Model

**Explore how exposure, correction and source feedback shape beliefs and sharing.**

An interactive, evidence-aware research prototype with a minimal Python reference
model (M0) and a Romanian / English browser interface.

> **Alpha 0.2.0a0.** Demonstration coefficients are not empirically calibrated.
> Software tests do not establish psychological validity or population prevalence.

## Project priorities

1. Understand mechanisms through visual interactions and detailed explanations.
2. Prioritize factors to address under explicit objectives and assumptions.
3. Plan necessary actions and timing.

[Project priorities and elementary OS / Flatpak v1 direction](docs/PROJECT_PRIORITIES.md)
are persistent requirements. The web interface already follows a system-font,
light/dark, keyboard-accessible visual foundation for the future native app.

## Browser application

[![Deschide aplicația / Open app](https://img.shields.io/badge/Deschide_aplica%C8%9Bia_%2F_Open_app-087F73?style=for-the-badge)](https://laurentiustaicu.github.io/cognitive-epistemic-model/)

**[https://laurentiustaicu.github.io/cognitive-epistemic-model/](https://laurentiustaicu.github.io/cognitive-epistemic-model/)**

The interface runs in a modern browser on Linux, Windows and macOS. No Flatpak or
Windows installation is required. The public alpha is hosted on GitHub Pages.
Choose RO or EN in the application header.

- **Understanding (start here):** seven explained variables, four selectable mechanism
  paths, interactions, mathematical details and direct scenario exploration.
- **Interventions:** compare all 16 bundles under an effort budget, adjust objective
  weights and timing, inspect interactions and conditional factor priorities, test
  three response assumptions and export the analysis. See [scope and calculation](docs/INTERVENTIONS.md).
- **Scenarios:** four Python-generated reference runs, play/pause, step selection,
  exact values in a table and JSON export.
- **Structure:** interactive variable/link graph and keyboard-accessible inspection.
- **Process:** an ODD-inspired overview of event scheduling, state updates,
  judgments and decisions; not yet a complete ODD specification.
- **Registry:** seven variables, three registered links and twenty conceptual modules.

Scenarios replay saved output from the Python simulator; the browser does not
recalculate arbitrary parameter combinations. The graph shows registered links,
not every dependency in the equations. Each registered link now includes a DOI source, a bilingual finding/limitation
summary and the scope of the bibliographic check. Phenomenon-level evidence is
separated from the candidate mechanism and uncalibrated functional form in M0.
See the [initial evidence audit](docs/EVIDENCE.md); this is not a systematic review.

### Pentru utilizatorii din România

Interfața pornește în română; butonul **EN / RO** schimbă limba. Poți selecta un
scenariu, urmări fiecare pas și compara convingerea cu probabilitatea de distribuire.
Pașii reprezintă unități abstracte, nu ani sau zile. Rulările sunt demonstrații ale
modelului, nu estimări despre persoane sau despre populația României.

## Scientific scope

M0 contains familiarity, correction accessibility, source-reliability estimation,
belief formation, accuracy salience and a sharing policy. Functional forms are
reference candidates, not established unique psychological laws.

- Simulated ground truth is never passed directly into the belief-update function.
- Track A/B are conceptual descriptions, not fixed classes or hard-coded agent states.
- Jungian individuation and the ego–Self axis remain a separate interpretive layer.
- A reproduced pattern is not proof of a unique mechanism.
- No Track A/B population estimates, individual diagnoses or Romania forecasts.

See [claim boundaries](docs/CLAIMS.md), [modelling decisions](docs/TRACE.md) and
[development handoff](docs/HANDOFF.md).

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
`python scripts/export_web.py` regenerates deterministic reference runs.

## Verification and hosting

[GitHub Actions](https://github.com/LaurentiuStaicu/cognitive-epistemic-model/actions)
checks Python tests, installed package resources, exact regeneration of the saved
runs, TypeScript/build and browser interactions at desktop/mobile sizes. A successful
run provides a downloadable static web artifact. Deployment uses only that verified
artifact.

GitHub Pages is configured with **GitHub Actions** as its source. The dependent
**Publish web application** workflow deploys the verified build after successful
checks. The initial live deployment was confirmed on 2026-09-13.

## License status

The staging metadata designates code as MIT. Documentation/registries are intended
for CC BY 4.0; final license texts and file-level notices remain a release gate
before tagging a public release.
