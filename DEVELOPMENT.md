# Development and continuity state

## Purpose

This file is the repository-side handoff for continuing Cognitive Belief Dynamics (CBD) development without relying on any particular chat session, local workspace, or developer memory. It records the current engineering/audit state, the source-of-truth hierarchy, known scientific boundaries, and the next decision gates.

It does **not** replace `STATUS.md`. Scientific claims and paradigm boundaries are canonical in `STATUS.md` and the model/contracts themselves.

## Source-of-truth order

When resuming work, use this order:

1. `STATUS.md` — current scientific paradigm and validation boundary.
2. `model/` registries and `model/contracts/` — canonical model structure, evidence, measurement and benchmark contracts.
3. `model/benchmarks/results/` plus provenance/checksum files — retained authoritative numerical results.
4. `tests/` and `.github/workflows/cbd-validation.yml` — executable verification gates.
5. `requirements/ci-py312-linux.lock.txt` — frozen GitHub-hosted Ubuntu / CPython 3.12 CI environment snapshot.
6. `CHANGELOG.md`, `CITATION.cff` and `releases/` — version/release history and citation metadata.
7. this file — current development queue and continuity notes.

If a chat, issue comment, branch description, or external note conflicts with these surfaces, the repository sources above take precedence.

## Current release line

- immutable baseline release: **v0.1.0**, tagged at the historical scientific-core snapshot;
- maintenance release candidate: **v0.1.1**;
- v0.1.1 changes repository verification, provenance checking, canonical status reporting, reproducibility metadata, presentation, and evidence metadata after source-level content audit;
- v0.1.1 does **not** change the scientific equations, retained benchmark values, thresholds, or seeds. The evidence **set** is retained, while `model/evidence_snapshot.json` advances to an audited r2 metadata snapshot.

## Audited canonical model surface

At the v0.1.1 preparation point, the canonical registries contain:

- 20 conceptual modules; 7 currently have variables assigned in `model/variables.json`, while 13 have no registered variables/link endpoints through that registry and therefore remain conceptual expansion territory rather than executable modules;
- 19 registered variables;
- 22 registered processes: 12 `implemented_m0` and 10 `candidate`;
- 10 registered links;
- 16 registered references;
- 8 subsystems: 4 `partial`, 3 `future`, 1 `active`;
- 15 validation patterns: 8 descriptive patterns and 7 negative constraints;
- 4 empirical targets, all used for directional validation only;
- 17 dependencies in the frozen M0 computational-dependency contract.

`cemodel validate` checks schemas, duplicate IDs, module/variable/link/reference integrity, DOI consistency, evidence targets, validation-pattern references, the evidence snapshot and the computational-dependency contract. Dedicated tests cover M0 behavior, M1.E1-E3 candidate surfaces, M1.E4 contracts/recovery/authoritative results, MOD.14/world-model behavior, structural integrity and CI reproducibility. The v0.1.1 release gate also parses every repository JSON artifact in the canonical artifact roots, validates every JSON Schema as Draft 2020-12, and requires an explicit schema mapping for every scientific contract.

## Retained M1.E4 scientific state

Two retained synthetic results must always be reported together:

- participant-aware confirmation: all 18 primary P64_X10 cells meet the 0.80 recovery gate, minimum observed recovery 0.92;
- separate Phase M protocol robustness: `PROTOCOL_ROBUSTNESS_FAIL`, with 3 of 18 cells below 0.80 and minimum recovery 0.56.

The failing cells are `ITEM_MODERATE__EVSD`, `ITEM_HIGH__EVSD` and `COMBINED_ADVERSE__EVSD`.

These are synthetic model-recovery / misspecification results. They do not identify EVSD or 2HT as human truth, identify Pencode, validate a human sample size, or authorize recruitment.

## Known audit boundaries and open scientific gaps

### Benchmark provenance maturity

The current repository has uniform machine-readable provenance sidecars for the later participant-confirmation and Phase M robustness results. Earlier Phase F/G/I results predate that convention: their exact commit/run/artifact information was recorded in historical PR audit records plus retained checksum files rather than uniform sidecars. v0.1.1 centralizes the verified historical trace in `model/benchmarks/results/PROVENANCE.md` without inventing missing fields. This is a traceability improvement, not a change to any result.

### Evidence scope

`model/evidence_snapshot.json` is a bounded evidence snapshot, not a systematic review or calibration dataset. v0.1.1 advances it to `EVIDENCE.M1.2026-09-21.r2` after source-level content auditing. The evidence set is retained; r2 records corrected/qualified metadata (including sample-flow and archive-integrity context) rather than silently altering r1.

### Registry semantics versus runtime storage

The content audit distinguishes a registered model variable from a persisted runtime field. `F`, `C`, and `T` are persisted in `AgentState`; `Nexp` is a conceptual/exogenous exposure count while M0 consumes discrete `ExposureEvent` objects; `B` and `W` are computed at decision time and are not automatically persisted between events. Registry definitions state these distinctions explicitly so `STATE_FAST` is not misread as a storage guarantee.

### Conceptual modules versus executable model

The 20-module registry is a conceptual map, not a claim that all modules are executable. The current executable core is narrower. In particular, Platform / Network, AI System, and Learning / Adaptation remain future subsystems.

### Endogenous feedback

CBD is currently an event-driven cognitive state-transition and agent-level stochastic dynamical model informed by systems thinking. Event schedules remain externally supplied and Share does not automatically create future exposure.

The future research program is **progressive endogenization**, tracked in GitHub Issue #110. The first candidate closure is:

`Share -> transmission/network -> delayed Exposure -> Familiarity/Belief -> Action/Share`

No such loop is active in v0.1.1. The model should be reclassified as formal System Dynamics only if the implemented scientific structure eventually justifies that term. A hybrid event-driven / agent-network / System Dynamics architecture remains an acceptable future outcome.

### M1.E4 item heterogeneity

Phase M shows an asymmetric loss of EVSD-family recovery under item-level heterogeneity. The current participant-level aggregate count representation does not preserve item identity, so a future crossed participant-item model would require a new prospective data/measurement contract rather than a post-hoc patch to M1.

M1 remains closed at the retained pre-human boundary.

### Parameter-domain audit

The default `ModelParams` values are demonstrative rather than population estimates. The current dataclass does not enforce a complete scientific parameter-domain contract for arbitrary user-supplied alpha/beta values. Existing state updates remain bounded where implemented, but this is an open model-governance item: parameter admissibility should be specified prospectively before exposing free parameter editing or calibration. No bounds are invented in v0.1.1 merely to make the API stricter.

### Product layer

The scientific-core repository does not currently contain an end-user application. Product/interface work must consume the scientific core without silently changing its claims or contracts.

## Reproducibility path

Canonical CI runs on GitHub-hosted Ubuntu with CPython 3.12 and the scoped lock file:

`requirements/ci-py312-linux.lock.txt`

The validation gate builds source and wheel distributions, verifies a clean wheel install and package version, compiles Python sources, runs the complete pytest harness, validates canonical registries from the checkout, and validates/demo-runs the installed package outside the checkout.

The lock file is an exact CI snapshot, not a universal cross-platform dependency lock. `pyproject.toml` remains the supported dependency-range declaration for ordinary installations.

## Release procedure

For a new release:

1. decide whether the change is patch/minor/major based on the software/repository API and scientific scope;
2. update package version, `CITATION.cff`, `STATUS.md`, `CHANGELOG.md`, README, release note, release manifest and CI version assertion together;
3. run the full `CBD validation` workflow;
4. review scientific boundaries and retained-result wording against authoritative artifacts;
5. obtain explicit merge approval;
6. merge the release PR;
7. create the matching Git tag and GitHub release from the exact merged commit;
8. verify that the tag, GitHub release, citation metadata and README all report the same version.

Released tags are immutable historical snapshots and must not be rewritten to correct later-discovered documentation problems; corrections go into a new release.

## Current next gates

1. Complete and visually review the v0.1.1 professional landing page/release candidate.
2. Require green full CI on the exact release-candidate head.
3. Merge only after explicit approval.
4. Tag and publish v0.1.1 from the exact merged commit.
5. Verify the published release metadata and latest-release badge.
6. Resume scientific research from Issue #110: progressive endogenization and feedback-loop closure.
7. Treat any future M1.E4 item-heterogeneity redesign as a new prospective post-M1 research program.

## How to resume after context loss

Start by reading, in order:

`README.md -> STATUS.md -> DEVELOPMENT.md -> CHANGELOG.md -> CITATION.cff`

Then inspect the latest GitHub release/tag, the most recent green `CBD validation` run, open issues/PRs, and the contracts/results relevant to the task.

Do not infer the current model state from old branches or historical chat text when the canonical repository disagrees.
