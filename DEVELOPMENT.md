# Development and continuity state

## Purpose

This file is the repository-side handoff for continuing Cognitive Belief Dynamics (CBD) development without relying on any particular chat session, local workspace, or developer memory. It records the current engineering/audit state, the source-of-truth hierarchy, known scientific boundaries, and the next decision gates.

It does **not** replace `STATUS.md`. Scientific claims and paradigm boundaries are canonical in `STATUS.md` and the model/contracts themselves.

## Source-of-truth order

When resuming work, use this order:

1. `STATUS.md` — current scientific paradigm and validation boundary.
2. `model/` registries and `model/contracts/` — canonical model structure, evidence, measurement and benchmark contracts.
3. `model/benchmarks/results/` plus provenance/checksum files — retained authoritative numerical results.
4. `model/audits/` — versioned source/data/semantic audits, repaired findings, and explicit open gaps.
5. `tests/` and `.github/workflows/cbd-validation.yml` — executable verification gates.
6. `requirements/ci-py312-linux.lock.txt` — frozen GitHub-hosted Ubuntu / CPython 3.12 CI environment snapshot.
7. `CHANGELOG.md`, `CITATION.cff` and `releases/` — version/release history and citation metadata.
8. this file — current development queue and continuity notes.

If a chat, issue comment, branch description, or external note conflicts with these surfaces, the repository sources above take precedence.

## Current release line

- immutable public baseline release: **v0.1.1**, tagged at commit `9bc57322f7d2e1d53bf9c33e67f083e667a64569`;
- v0.1.1 preserves the v0.1.0 scientific equations and retained benchmark values while adding the audited maintenance/reproducibility/provenance improvements recorded in the release manifest;
- the current `main` line is post-release research development. It contains the optional F1a progressive-endogenization layer at `RECOVERY_TESTED` status while retaining v0.1.1 as the package/citation version until a separate release decision is made;
- F1a is not part of the immutable v0.1.1 tag and does not retroactively change that release.

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

## Content/data audit state

v0.1.1 includes `model/audits/content_audit_2026-09-21.json`. It audits bibliographic identity, reported numerical values, source-versus-repository claims, source-to-model mappings, registry/contract/code concordance, and explicit non-claims. CI requires coverage of every current reference, empirical target, variable, link, process and scientific contract. Repaired metadata and unresolved gaps are recorded separately; a passing content-audit contract therefore does not mean that every conceptual mechanism is empirically established.

## Retained M1.E4 scientific state

Two retained synthetic results must always be reported together:

- participant-aware confirmation: all 18 primary P64_X10 cells meet the 0.80 recovery gate, minimum observed recovery 0.92;
- separate Phase M protocol robustness: `PROTOCOL_ROBUSTNESS_FAIL`, with 3 of 18 cells below 0.80 and minimum recovery 0.56.

The failing cells are `ITEM_MODERATE__EVSD`, `ITEM_HIGH__EVSD` and `COMBINED_ADVERSE__EVSD`.

These are synthetic model-recovery / misspecification results. They do not identify EVSD or 2HT as human truth, identify Pencode, validate a human sample size, or authorize recruitment.

## Known audit boundaries and open scientific gaps

### Restored historical provenance documents

Three benchmark configurations retained source-document paths that became dangling during the scientific-core reset. v0.1.1 restores the exact historical Phase I screening audit, Phase L robustness contract and Phase M robustness contract from their original PR-head commits. Their Git blob SHAs match the historical blobs byte-for-byte. These files are historical snapshots: references inside them to Alpha 0.4.3a0 and evidence snapshot r1 describe the phase at the time it was frozen and do not supersede current `STATUS.md`, the v0.1.1 release manifest or evidence snapshot r2.

CI now requires every declared benchmark `source_*` path to resolve.

### Benchmark provenance maturity

The current repository has uniform machine-readable provenance sidecars for the later participant-confirmation and Phase M robustness results. Earlier Phase F/G/I results predate that convention: their exact commit/run/artifact information was recorded in historical PR audit records plus retained checksum files rather than uniform sidecars. v0.1.1 centralizes the verified historical trace in `model/benchmarks/results/PROVENANCE.md` without inventing missing fields. This is a traceability improvement, not a change to any result.

### Evidence scope

`model/evidence_snapshot.json` is a bounded evidence snapshot, not a systematic review or calibration dataset. v0.1.1 advances it to `EVIDENCE.M1.2026-09-21.r2` after source-level content auditing. The evidence set is retained; r2 records corrected/qualified metadata (including sample-flow and archive-integrity context) rather than silently altering r1.

### Registry semantics versus runtime storage

The content audit distinguishes a registered model variable from a persisted runtime field. `F`, `C`, and `T` are persisted in `AgentState`; `Nexp` is a conceptual/exogenous exposure count while M0 consumes discrete `ExposureEvent` objects; `B` and `W` are computed at decision time and are not automatically persisted between events. Registry definitions state these distinctions explicitly so `STATE_FAST` is not misread as a storage guarantee.

### Conceptual modules versus executable model

The 20-module registry is a conceptual map, not a claim that all modules are executable. The current executable core is narrower. In particular, Platform / Network, AI System, and Learning / Adaptation remain future subsystems.

### Endogenous feedback

The immutable v0.1.1 release remains the open-loop baseline: event schedules are externally supplied and Share does not create future exposure.

Post-release `main` contains the first optional progressive-endogenization experiment, F1a:

`realised Share(A) -> synthetic directed transmission -> delayed Exposure(B) -> existing Familiarity(B) update`

Its machine-readable contract is `model/experiments/f1a_endogenous_transmission_experiment.json`; the scheduler/network documentation is `docs/ODD_ENDOGENOUS_SCHEDULER.md`. F1a is now classified **RECOVERY_TESTED**.

The recovery step was prospective rather than post-hoc. The frozen design (`model/benchmarks/f1a_transmission_recovery_core.json`) defined a calibration-only conditional transmission parameter `q_transmit`, 20 gating core cells, 10 non-gating N=25 stress cells, 200 replicates per cell, the estimator, error tolerance, and the 0.80 recovery gate before the authoritative result was accepted. The retained result is `model/benchmarks/results/f1a_transmission_recovery_authoritative_2026-09-21.json`; the explicit promotion record is `model/experiments/f1a_recovery_promotion_2026-09-21.json`.

All 20 core cells passed, with minimum recovery probability 0.885. The stress grid intentionally includes cells below 0.80 (minimum 0.725), consistent with the pre-run exact-binomial analysis that made N=25 non-gating. q=0/q=1 controls, delay realization, familiarity consistency, sensitivity monotonicity, isolated RNG behavior and byte-for-byte rerun reproducibility all pass.

F1a remains deliberately narrow:
- `q_transmit` is calibration-only and is not imported into the active runtime policy;
- no empirical reach, attention, ranking, platform, population or social-network parameter is claimed;
- the synthetic network remains static, directed and unweighted;
- generated events use strictly positive abstract delay with no empirical time unit;
- no recipient DecisionEvent is generated;
- no source-selection, platform-ranking or adaptive-network process is introduced;
- the v0.1.1 cognitive transition equations remain owned by `Simulator.step()`;
- no automatic further maturity promotion is allowed.

The next possible validation-ladder stage is **EMPIRICALLY_CONSTRAINED**. Reaching it requires a separate evidence and measurement/observability bridge; the recovery benchmark alone cannot supply empirical meaning or activate `q_transmit`.

The canonical paradigm remains an event-driven cognitive state-transition and agent-level stochastic dynamical model informed by systems thinking. F1a alone is not a basis for formal System Dynamics reclassification.

The progressive-endogenization research program and its validation ladder remain tracked in GitHub **Issue #110**.

The subsequent SOMAR column-identity/privacy audit (`docs/F1A_SOMAR_COLUMN_PRIVACY_AUDIT.md`; `model/experiments/f1a_somar_column_privacy_audit.json`) retains a controlled negative result. Current ICPSR records identify the relevant URL-level potential-exposure, exposure and engagement studies, and legacy SOMAR metadata identifies dedicated public dictionary/variable-description artifacts. However, the exact dictionary rows cannot currently be inspected and version-linked through the available public web surface. Consequently `r_view` remains numerically unauthorized, no field names are guessed, and generic disclosure-control claims from unrelated Meta datasets are not imported into FIES. The next admissible gate is `OFFICIAL_VARIABLE_DICTIONARY_CONTENT_ACCESS`.

### M1.E4 item heterogeneity

Phase M shows an asymmetric loss of EVSD-family recovery under item-level heterogeneity. The current participant-level aggregate count representation does not preserve item identity, so a future crossed participant-item model would require a new prospective data/measurement contract rather than a post-hoc patch to M1.

M1 remains closed at the retained pre-human boundary.

### M0 evidence-bridge gaps

The content audit identified two M0 descriptive patterns whose executable dependencies exist but whose empirical bridge is not yet represented as a dedicated `links.json` relation: `VAL.M0.002` (correction / partial regression) and `VAL.M0.003` (source-reliability weighting). External literature supports the broad phenomena, but v0.1.1 does not silently expand the r2 evidence set or promote the current functional forms to empirical laws. A future versioned evidence refresh should decide which sources, constructs, and limitations belong in those links.

### Parameter-domain audit

The default `ModelParams` values are demonstrative rather than population estimates. The current dataclass does not enforce a complete scientific parameter-domain contract for arbitrary user-supplied alpha/beta values. Existing state updates remain bounded where implemented, but this is an open model-governance item: parameter admissibility should be specified prospectively before exposing free parameter editing or calibration. No bounds are invented in v0.1.1 merely to make the API stricter.

### Runtime input-domain validation

Runtime domain enforcement is currently uneven. Some domains (for example `evidence_signal` and `correction_direction`) are rejected when the belief function executes, while probability-like inputs passed through `logit()` are clamped and dataclass annotations such as boolean event fields are not runtime validators. This is recorded as an API/scientific-boundary gap rather than silently changed in v0.1.1. A future hardening release should define admissible domains and rejection-versus-clamping semantics explicitly before changing runtime behavior.

### Product layer

The scientific-core repository does not currently contain an end-user application. Product/interface work must consume the scientific core without silently changing its claims or contracts.

## Reproducibility path

Canonical CI runs on GitHub-hosted Ubuntu with CPython 3.12 and the scoped lock file:

`requirements/ci-py312-linux.lock.txt`

The validation gate builds source and wheel distributions, verifies a clean wheel install and package version, compiles Python sources, runs the complete pytest harness, validates canonical registries from the checkout, and validates/demo-runs the installed package outside the checkout.

The lock file is an exact CI snapshot, not a universal cross-platform dependency lock. `pyproject.toml` remains the supported dependency-range declaration for ordinary installations.

### Post-release repository governance

The mandatory v0.1.1 publication/governance pass is complete:

- v0.1.1 is published as an immutable GitHub release on the exact validated release commit;
- repository topics are populated;
- the active `main` ruleset requires pull-request integration and the `Build and test CBD` status check, blocks force pushes/deletion, and preserves merge commits;
- CodeQL default setup is enabled and has successfully analyzed Python and GitHub Actions;
- secret scanning and push protection are enabled;
- Dependabot vulnerability alerts and security updates are enabled;
- GitHub Pages publishes from `main` / root and has completed a successful build on the v0.1.1 release commit.

Optional archive/discovery work such as Zenodo, Software Heritage, social preview and future REUSE/SPDX per-file metadata may be added later, but these items do not block the current scientific research program.

## Release procedure

For a new release:

1. decide whether the change is patch/minor/major based on the software/repository API and scientific scope;
2. update package version, `CITATION.cff`, `STATUS.md`, `CHANGELOG.md`, README, release note, release manifest and CI version assertion together; verify that `CITATION.cff` `date-released` equals the actual publication date rather than a stale planned date;
3. run the full `CBD validation` workflow;
4. review scientific boundaries and retained-result wording against authoritative artifacts;
5. obtain explicit merge approval;
6. merge the release PR;
7. create the matching Git tag and GitHub release from the exact merged commit;
8. verify that the tag, GitHub release, citation metadata and README all report the same version.

Released tags are immutable historical snapshots and must not be rewritten to correct later-discovered documentation problems; corrections go into a new release.

## Current next gates

1. Keep F1a at **RECOVERY_TESTED**. Public FIES documentation now resolves Audience versus Content views semantics and the intended potential→exposed→engaged funnel, but no numerical empirical component has yet been estimated.
2. Treat candidate `r_view` only as `exposed_audience_users / potential_audience_users`. Never substitute `content_views` for exposed audience: Content views are screen-appearance counts and can include repeated views, whereas Audience is a user/participant count viewed at least once.
3. Resolve the exact released column names and definitions for potential audience and exposed audience in ICPSR 300450 and 300470.
4. Audit privacy/disclosure controls: suppression/minimum-cell rules, perturbation/noise, rounding, estimated-count semantics, and how such transformations affect ratios.
5. Freeze missing/suppressed/structural-zero handling, absent-URL semantics, URL canonicalization, release-version row linkage and any table-specific filters before pairing rows.
6. Treat owner_type=`all` as the documented combined posts-from-users/Pages/groups category, but do not assume its audience count equals a simple sum of the three component rows because users can overlap.
7. Only after the `COLUMN_IDENTITY_AND_PRIVACY_RULES_AUDIT` passes may a separate prospective empirical-analysis contract authorize an `r_view` calculation. If any gate fails, retain the negative result rather than substituting a different denominator post hoc.
8. Keep PlatformView→CBD CognitiveExposure unresolved until a prospective cognitive measurement bridge is justified; even a valid FIES `r_view` is not dyadic `q_transmit`.
9. Do not begin recipient Decision generation or the full Share→Exposure→Decision→Share loop until source-attribution, item-identity and decision-opportunity contracts identified in Issue #110 are resolved.
10. Treat any future M1.E4 item-heterogeneity redesign as a separate prospective post-M1 research program.

## How to resume after context loss

Start by reading, in order:

`README.md -> STATUS.md -> DEVELOPMENT.md -> CHANGELOG.md -> CITATION.cff`

Then inspect the latest GitHub release/tag, the most recent green `CBD validation` run, open issues/PRs, and the contracts/results relevant to the task.

Do not infer the current model state from old branches or historical chat text when the canonical repository disagrees.
