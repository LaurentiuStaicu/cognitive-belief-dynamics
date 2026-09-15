# Alpha 0.4.2a0 — final integration audit

Status: integration candidate only. This document does not authorize merge or publication.

## Integration topology

Current `main` base audited:

`50f8a68804fb51c2e431e5dbef2886f13111f703`

Integration branch:

`alpha-0.4.2a0-integration-candidate`

The candidate is built from the validated release-preparation head and contains the
complete Phase B runtime promotion, Phase C Theory/Understanding layer and
Alpha 0.4.2a0 release-preparation changes.

At audit time, GitHub comparison reports:

- status: ahead;
- ahead by 72 commits;
- behind by 0 commits;
- merge base equal to the audited `main` head.

Therefore no newer `main` change is missing from the candidate at this gate.

## Registered scientific additions relative to main

No registered object is removed.

### Variables

Main: 15  
Candidate: 19

Added exactly:

- `VAR.HEADLINE.NEGATIVITY`;
- `VAR.ACCESS.PROBABILITY`;
- `VAR.ACCESS`;
- `VAR.PREVIEW.IMPRESSION`.

### Evidence-qualified links

Main: 8  
Candidate: 10

Added exactly:

- `LINK.HEADLINE_NEGATIVITY.ACCESS_PROBABILITY`;
- `LINK.ACCESS_PROBABILITY.ACCESS`.

### Empirical targets

Main: 3  
Candidate: 4

Added exactly:

- `TARGET.M1.E3.ROBERTSON_2023`.

### Validation patterns

Main: 11  
Candidate: 15

Added exactly:

- `VAL.M1.004`;
- `VAL.M1.N04`;
- `VAL.M1.N05`;
- `VAL.M1.N06`.

### Active references

Main: 6  
Candidate: 10

Added exactly:

- `REF.ROBERTSON.2023.NEGATIVITY`;
- `REF.MATIAS.2021.UPWORTHY`;
- `REF.MATIAS.2024.UPWORTHY_CORRECTION`;
- `REF.NICKL.2025.ATTENTION_ECONOMY`.

### Visual ODD processes

Main: 19  
Candidate: 22

Added exactly:

- `ODD.M1.PROCESS.PREVIEW_IMPRESSION`;
- `ODD.M1.PROCESS.ACCESS_MODELS`;
- `ODD.M1.OBS.ACCESS_PATTERN`.

## Retained-output regression audit

The following canonical JSON exports were compared between current `main` and
the integration candidate:

- `runs.json`;
- `interventions.json`;
- `explanations.json`;
- `diagnostics.json`;
- `m1_editorial.json`;
- `m1_presentation.json`.

After recursively removing only `model_version` and `software_version` fields,
all six structures are byte-equivalent after canonical JSON parsing/serialization.

Conclusion: Alpha 0.4.2a0 does not change retained M0, intervention, diagnostic,
M1.E1 or M1.E2 numerical/model outputs.

M1.E3 is new and is therefore audited separately through its dedicated tests,
canonical export and empirical/negative validation patterns.

## Phase A contract preservation

The approved Phase A evidence/schema contract is already present on `main` and
does not appear in the `main...integration` file diff.

Implementation therefore promotes the approved contract rather than rewriting the
frozen cue-selection decision.

## Evidence snapshot transition

Main:

`EVIDENCE.M1.2026-09-15.r2`

Candidate:

`EVIDENCE.M1.2026-09-16.r1`

The candidate snapshot scope adds M1.E3 phenomenon evidence, data provenance,
randomization-integrity correction, explicit counterevidence and limitations.

The release-preparation layer does not advance this snapshot again.

## Software release metadata

Main software version:

`0.4.1a1`

Candidate software version:

`0.4.2a0`

Candidate release tag:

`v0.4.2a0`

The release reproducibility manifest enumerates M1.E1, M1.E2 and M1.E3.

Version regression now checks the M1.E3 export natively.

## M1.E3 scientific boundary

The integration candidate preserves:

`PreviewImpression != Access != Attention != Encoding != Belief != EngageIntent != Share`

and the release remains bounded to:

`PreviewImpression → Hneg → Paccess → Access`.

No downstream Access → belief / Share / Aissue / Pengage / EngageIntent coupling
is introduced.

The reference values `b0=-2.0` and `beta_hneg=0.20` remain demonstrative and
uncalibrated.

Robertson et al. source coefficients/counts remain empirical validation context,
not fitted CEM parameters.

## Validated stacked gates before integration

Phase B backend/runtime gate:

- Python tests green;
- canonical export reproduction green;
- Vite/TypeScript green;
- Playwright green.

Phase C explanatory/Theory gate:

- Python tests green;
- canonical export reproduction green;
- Vite/TypeScript green;
- Playwright green;
- Theory → M1.E3 deep link/focus green;
- mobile overflow green;
- explicit RO → EN → RO comparator localization green;
- rendered mobile comparator manually inspected.

Release-preparation gate:

- version regression including M1.E3 green;
- canonical export reproduction green;
- Vite/TypeScript green;
- Playwright green;
- release manifest updated to include M1.E3;
- retained scientific exports identical to Phase C after removal only of software
  version fields.

## Final gate required before merge

The integration candidate must receive one fresh full CI run targeting current
`main`.

After that run:

1. re-read the PR head and current `main` SHA;
2. confirm `behind_by=0`;
3. re-run the registered-ID and retained-output audits if either SHA changed;
4. inspect the final PR diff and mergeability;
5. keep the PR Draft until explicit merge/publication authorization.

A green stacked branch is not by itself authorization to publish.
