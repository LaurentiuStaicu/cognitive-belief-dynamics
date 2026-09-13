# Cognitive Epistemic Model

An evidence-bound, falsifiable computational model of how people construct, revise, and act on beliefs inside modern information ecosystems.

> **Status:** pre-release staging for `v0.2.0 — First Public Executable Model`.

The project separates empirical phenomena, candidate mechanisms, functional forms, observables, and interpretive layers. The current executable core (`M0`) is intentionally minimal: familiarity, correction accessibility, source-reliability learning, belief formation, accuracy salience, and action/sharing.

## Scientific guardrails

- Ground truth exists in the simulated world but is never passed directly into the human belief-update function.
- `Track A/Track B`, “critical thinking”, and Jungian individuation are not hard-coded agent states.
- A reproduced pattern is not treated as proof of a unique psychological mechanism.
- Every public claim is scoped to the model purpose, validation evidence, and known limitations.

## Planned public interface

The first public release will include an interactive web presentation with:

- **Open application** button (browser-based; OS independent)
- structure view of variables/links/evidence
- Visual ODD process view
- animated run/replay view
- bilingual RO/EN explanations
- accessible structured HTML alternative to the graph

## Local quick start

```bash
python -m pip install -e '.[test]'
pytest
cemodel validate --root .
cemodel demo
```

Installed wheels include the model registries and schemas. After installing a
wheel, `cemodel validate` works independently of the current directory.

## Current handoff

The recovered staging source and verification results are documented in
[docs/HANDOFF.md](docs/HANDOFF.md). This is an alpha development snapshot;
the public browser application is not yet deployed.

## License

Software code: MIT. Scientific registries/documentation: intended for CC BY 4.0 in the public release; final file-level licensing metadata will be added before tagging `v0.2.0`.
