# Phase C.1 source-registration gate

This file is temporary audit bookkeeping. It documents the metadata changes that must be made before Phase C.1 is merged.

## theory_index.json module coverage to reconcile

- THEORY.02.PROCESSING_METACONTROL: add `MOD.15` alongside `MOD.02` and `MOD.09`.
- THEORY.07.SOURCE_RELIABILITY: add `MOD.20`.
- THEORY.10.PRESENTATION_CONGRUENCE: add `MOD.05` while retaining the existing executable-module links.
- THEORY.11.ALGORITHMS_SOCIAL_FEEDBACK: add `MOD.08` and `MOD.19`; retain `MOD.10` and `MOD.18`.
- THEORY.12.INTERVENTIONS: add `MOD.11`, `MOD.12`, and `MOD.13`.

## Romanian index labels/summaries to clean

At minimum remove untranslated prose-level uses of:

- `baseline`
- `pool`
- `ranking`
- `framing`
- `task-specific`
- `nested`
- `engagement`
- `ground truth`

Literal code identifiers remain unchanged.

## Background sources to register

Expanded conceptual coverage should be linked as `BACKGROUND_THEORY`, not `MODEL_EVIDENCE`, unless a source is already an explicit model validation target.

Priority additions:

- misinformation exposure concentration / heterogeneity: https://www.nature.com/articles/s41586-024-07417-w
- human–automation appropriate reliance: https://pubmed.ncbi.nlm.nih.gov/15151155/
- automation-bias review: https://pubmed.ncbi.nlm.nih.gov/21335679/
- metacognition/confidence review: https://pubmed.ncbi.nlm.nih.gov/37722748/
- decentering review: https://pmc.ncbi.nlm.nih.gov/articles/PMC5103165/

## Synchronization rule

After editing `model/theory_index.json`, regenerate or copy the same canonical metadata to `web/public/model/theory_index.json` using the repository's established resource-sync process. Do not hand-maintain divergent copies.

## Merge condition

Delete this TODO or mark every item complete before Phase C.1 is considered merge-ready.