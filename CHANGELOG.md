# Changelog

All notable public scientific-core releases of Cognitive Belief Dynamics (CBD) are recorded here.

## Unreleased

### Progressive endogenization research

- adds an optional future-event scheduler around the unchanged `Simulator.step()` cognitive transition path;
- adds an explicit static directed synthetic network fixture and deterministic forced pass-through transmission policy;
- establishes the first F1a synthetic executable edge: realised Share(A) → delayed Exposure(B) → existing Familiarity(B) update;
- preserves v0.1.1 open-loop behavior when the endogenous layer is not invoked;
- adds separate scheduler provenance, horizon/max-event guards, backward-equivalence tests, property tests, a strict experiment contract/schema and an ODD supplement;
- classifies F1a as `SYNTHETIC_EXECUTABLE` only; it is not recovery-tested, empirically constrained or active, and the canonical System Dynamics boundary is unchanged.

## 0.1.1 - 2026-09-21

Scientific-core maintenance, reproducibility, evidence-metadata audit and repository-presentation release. No model equation, retained benchmark result, threshold or seed changes. The retained evidence set is unchanged, while its metadata snapshot advances from r1 to content-audited r2.

### Scientific integrity and reproducibility

- restored the full scientific verification harness from the pre-reset scientific baseline and repaired three stale M1.E4 schema gate counts left behind by the scientific-core reset;
- added machine-verifiable authoritative Phase M result/provenance checks preserving the retained `PROTOCOL_ROBUSTNESS_FAIL`;
- added a platform-scoped CPython 3.12/Linux CI dependency snapshot and applied it consistently to build, clean-wheel and repository-test installs;
- restored complete canonical M1.E4 status reporting so the participant-confirmation pass and the distinct Phase M robustness failure are always reported together;
- retained the v0.1.0 scientific equations, benchmark values, thresholds and seeds unchanged;
- content-audited empirical-target/sample metadata and advanced the retained evidence-set metadata to `EVIDENCE.M1.2026-09-21.r2`;
- corrected the M1.E3 Mattis et al. Journal of Communication citation/DOI and replaced the Nickl preprint access link with its canonical DOI route;
- added a versioned machine-readable content/data audit covering every current reference, empirical target, variable, link, process and scientific contract, with repaired findings and unresolved gaps separated explicitly.
- audited empirical-target study design units, analysis bases and preregistration semantics, including the distinction between a preregistered study and Alvarado's reviewer-requested post-hoc interaction analysis;
- strengthened M0 pattern tests so source-reliability learning and true-versus-false sharing discernment are tested as claimed, while preserving incomplete M0 correction/source evidence bridges as explicit open gaps;
- verified against tag v0.1.0 that both the 16-reference registry membership and all 39 embedded contract-source memberships are unchanged; r2 repairs metadata rather than adding evidence;
- restored three historical Phase I/L/M provenance documents byte-for-byte from their original PR-head commits and made benchmark `source_*` paths CI-verifiable;
- documented heterogeneous historical checksum semantics for Phase F/G/I/K/M and made Phase K byte-digest and Phase M source-aggregate linkage executable CI checks;
- removed the unsupported `Nexp <= 1,000,000` metadata bound and replaced it with an explicit unbounded non-negative conceptual-domain note;
- made variable/link registry schemas reject unknown top-level fields so scientific metadata typos fail validation;
- clarified M1.E4 historical phase guards as evidence-set-membership freezes rather than prohibitions on later versioned metadata corrections.

### Repository and continuity

- publishes the professional suite-consistent CBD landing page with light/dark conceptual assets and explicit scientific boundaries;
- adds release/readme regression checks for version consistency, local links, scientific-status consistency and Markdown integrity;
- adds `DEVELOPMENT.md` as the repository-side handoff/continuity surface for future work independent of any chat history;
- adds a machine-readable v0.1.1 release manifest linking the canonical status, citation, reproducibility lock, authoritative Phase M artifacts and development-continuity surface;
- extends the Ask the Model repository manifest so continuity and changelog information are part of canonical retrieval.

### Governance and integration

- retains the single `CBD validation` workflow for package build, clean-wheel verification, compilation, the scientific pytest harness, checkout registry validation and installed-package validation;
- retains CBD-specific contribution/support guidance, reproducibility/scientific issue forms and pull-request integrity checks;
- preserves the event-driven paradigm boundary while recording progressive endogenization and feedback-loop closure as a future research program rather than an already implemented capability.

## 0.1.0 - 2026-09-18

Initial public scientific-core baseline.

### Included

- canonical CBD model specification and registries;
- Python computational/reference implementation;
- JSON schemas and model contracts;
- empirical-target and evidence metadata;
- retained calibration and synthetic model-recovery benchmark artifacts;
- integrity/provenance artifacts required by the retained benchmarks;
- reproducibility scripts required by the scientific core;
- standardized CBD project identity and release metadata.

### Scientific status

This release is an initial research snapshot, not a claim of full empirical validation. M1.E4 recovery results are synthetic model-identifiability/discrimination results and do not establish a true human recognition architecture or identify Pencode. MOD.14 provides a normative reference computation and is not a population-calibrated model or truth oracle.

### Scope boundary

The release intentionally excludes the previous end-user product/frontend layer. Future product work should begin from the scientific-core baseline rather than reintroducing superseded application branches.
