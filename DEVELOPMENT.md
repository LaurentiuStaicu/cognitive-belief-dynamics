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
8. `README.md` plus `.github/readme_design_contract.json` — canonical repository landing-page presentation and its frozen editorial/visual rules.
9. this file — current development queue and continuity notes.

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

The subsequent SOMAR column-identity/privacy audit (`docs/F1A_SOMAR_COLUMN_PRIVACY_AUDIT.md`; `model/experiments/f1a_somar_column_privacy_audit.json`) retains a controlled negative result. Current ICPSR records identify the relevant URL-level potential-exposure, exposure and engagement studies, and legacy SOMAR metadata identifies dedicated public dictionary/variable-description artifacts. Current SOMAR guidance now also verifies that codebooks and documentation for restricted-use datasets are publicly downloadable before application, including Controlled Download and VDE datasets. The exact dictionary rows have still not been inspected and version-linked through the automated web surface used for this audit; that is treated as a tooling/retrieval limitation rather than a VDE-approval requirement. The record-34 MARC export is now explicitly scoped to direct attachment evidence for record 34 only: equivalent record-level manifests proving the same documentation UUIDs on legacy records 32/36 were not recovered. This nonrecovery is not evidence of absence, but record-34 file locators must not be used as direct file-identity proof for Exposure/Potential Exposure or current 300450/300470. Legacy search results do independently mark records 32 and 36 as `Multiple Files` with the US2020 external codebook, so target-specific multi-file documentation availability is supported even though exact dictionary/CSV identities and record-34 UUID reuse are not. The exact legacy record-34 file UUIDs and byte sizes for the public data dictionary, variable descriptions, project codebook and glossary are now retained as retrieval provenance, and current ICPSR holdings documentation independently labels documentation files public by definition. These facts still do not establish that the legacy bytes are attached to the 2026 ICPSR collections. A 2026-09-25 link-health check also found that the tested legacy `socialmediaarchive.org` record/codebook/glossary URLs now redirect to the current SOMAR home page instead of serving the original artifacts; those URLs are therefore retained as historical/indexed provenance locators only, not live retrieval endpoints, without invalidating the historical evidence already captured. SOMAR's official Winter 2026 newsletter independently documents the website/archive transition to the ICPSR platform and unified interface, so the redirect state is now classified as consistent with an announced platform transition rather than unexplained link failure. Legacy records 36/32/34 and current ICPSR 300450/300470/300475 also show multi-field identity concordance across exact title, URL level, study period, broad population and semantic role, but no explicit indexed migration crosswalk or record-specific redirect has been recovered; this is provenance continuity only, not current-release linkage. External Source ID is not a viable public crosswalk field: ICPSR's legacy schema marks it internal/not publicly displayed and the current schema does not expose it. Public migration provenance should instead be sought in Version History/Version Note, citation metadata or an explicit official crosswalk. The legacy Exposure DOI ambiguity is now more precisely classified from two separately indexed official v3 codebook copies: SOMAR record 68 records `10.3886/rnr8-jj22`, while record 70 records `10.3886/rnr8-ij22`. This duplicate-v3 documentation divergence is verified, but neither string is treated as canonical without record-level metadata or DOI-registry adjudication. A v2 codebook copy at record 61 independently also renders `10.3886/rnr8-jj22`, so the exact evidence pattern is v2+one-v3 support for `jj22` versus a second v3 copy supporting `ij22`. This strengthens provenance for `jj22` but is deliberately not treated as canonical DOI adjudication. Both current and legacy ICPSR metadata schemas require a collection DOI; therefore ICPSR 300470 is treated as having an expected canonical DOI field whose concrete value/version is not yet recovered, and no suffix is inferred from neighboring records. A controlled SOMAR versioned-route probe is now explicitly non-inferential: although the 300470 V1.0 route responds, ICPSR 300464 provides a current FIES counterexample in which a `/versions/V1.0` URL is reachable while the indexed Version History exposes current V2.0 [2026-04-01]. Route responsiveness therefore carries no positive weight for current-version inference; 300470 DOI/version remain null until target-specific content-bearing metadata are recovered. The next operational fallback is the documented ICPSR browser route through Data & Documentation and the per-dataset Download menu to Codebook / ICPSR Codebook; the route itself is not evidence of variable content and does not relax the gate. After the documented public catalog, manual Data & Documentation, indexed-search and metadata routes are exhausted, the next non-restricted step is a documentation-locator request to SOMAR support for current 300450/300470 public documentation and the current 300470 DOI/version. That request is not a VDE/data-access request and cannot change scientific state unless target-specific official evidence is returned, archived and inspected. The official US2020 project FAQ also separates the platform-data code pipeline into two stages: a Meta-only upstream layer generated research-specific tables from internal data, while downstream preprocessing/analysis was accessible to academics. Although replication data and code are archived in SOMAR/VDE, public sources do not establish that the archive contains the complete upstream generator or current 300450/300470 physical schema; controlled code must therefore be inspected and version-linked rather than presumed to replace the dictionary gate. Current ICPSR 300450 now has target-specific confirmation on its current V2 study page that a data dictionary is downloadable for variables in the dataset; only availability is verified, not file identity or contents. A 2026-09-25 live-retrieval check now records that direct audited access to both 300450 and 300470 serves only the client-side shell, while the SOMAR catalog remains content-bearing. This does not invalidate the previously recovered official indexed 300450 V2 DOI/data-dictionary availability; it is a rendering/indexing limitation and cannot be used as evidence that 300470 documentation is absent. No equivalent content-bearing target-specific dictionary offer has yet been recovered for 300470, so numerator-side documentation remains a retrieval target rather than an absence finding. The legacy codebook appendix explicitly maps the Science paper `10.1126/science.ade7138` to the Potential Exposure URL, Exposure URL and Engagement URL dataset family, which strengthens provenance for the conceptual pairing but does not establish current-release field identity. The Science funnel is now scoped explicitly to its analysis inventory: friends, followed Pages and joined Groups supply political-news posts, and the algorithm selects from that inventory into Feed. Because the standalone Exposure release description does not explicitly repeat the Potential table's connection-based eligibility restriction—and the project Glossary's generic Feed definition allows suggested posts—the paper's subset relation is not transferred automatically to raw 300450/300470 fields. The candidate `r_view` is therefore conceptually conditional on proving a shared release inventory, not unconditionally justified. This stricter boundary is propagated back into the canonical count-semantics and PlatformView bridge contracts, their schemas/tests/docs, and `STATUS.md`, so no older surface retains the unconditional `CONCEPTUALLY_JUSTIFIED_NUMERICALLY_BLOCKED` state. The earlier public-codebook `hard_gates` object is also disambiguated: its booleans are requirements, not satisfied-state claims, and release-level subset/shared-inventory compatibility is explicitly unsatisfied. The frozen SOMAR Help draft is correspondingly narrowed to a documentation-location request for current row-universe/eligibility, absent-row and any explicitly documented shared-inventory relationship rules; it does not ask support to decide compatibility and remains `READY_NOT_SENT`. The Science paper's audience funnel is now separated explicitly from release-field arithmetic: potential and exposed audiences are defined as unique-user sets, but legacy disclosure text can multi-count users across posts/days and the current release `audience size` deduplication horizon is unverified. Thus even a located `audience size` column cannot be used as a probability-like `r_view` numerator/denominator until dictionary semantics establish equivalence to the paper's set cardinalities.S.-based connection, while Exposure includes URLs actually viewed in Feed. Although common filters include URL level, the same population/period, civic/news classification and >100 U.S. shares, identical row universes are not guaranteed. A missing numerator row must therefore not be coerced to zero or lost via inner join without explicit absent-row semantics from the target release. The Science paper further states that each analyzed URL has potential, exposed and engaged audience measures, which supports same-URL conceptual pairing in the published analysis. This does not establish rowwise joinability of current 300450/300470 release files: URL-key identity, asymmetric filtering/suppression and absent-row semantics still require target release documentation. The Science segregation index also uses `v_n`, described as total unique views, as an analysis weighting quantity; because the paper separately defines exposed audience as unique users and does not map `v_n` to a released physical field, `v_n` is not admissible as an `r_view` numerator/denominator without current dictionary linkage. A coauthor research page's `Replication` link for this paper resolves to the general US2020 SOMAR collection and is reused across project publications, so it does not identify an article-specific public code package. Replication code/data are a separate controlled-access surface: Science and the current author research page direct eligible researchers to apply for them, whereas public current-release documentation remains the preferred first gate source. Lack of a public code repository is therefore non-evidentiary for documentation availability. A published U.S. 2020 FIES article additionally identifies the controlled replication-code package DOI `10.3886/spb3-g558`; retain it as a VDE provenance locator only, because its contents and exact scope to Science `ade7138` / current 300450-300470 fields have not been inspected or independently linked. The ICPSR search Public Data facet is also not an unrestricted-file signal: current 300450/300470 descriptions remain restricted, and ICPSR documents availability and restriction type as separate systems-level metadata dimensions. Consequently `r_view` remains numerically unauthorized, no field names are guessed, and generic disclosure-control claims from unrelated Meta datasets are not imported into FIES. Derived daily ideological-segregation aggregation rules are also explicitly isolated from the base 300450/300470 surfaces: a derived sum-of-views exposure quantity and summed daily post-level audience counts cannot substitute for target audience-size fields without exact dictionary mapping. The indexed US2020 Glossary independently confirms that `Audience` is a user/participant count for at-least-one organic-content view, whereas `Content views` is a screen-appearance count. This corroborates the count-semantics audit and forbids using content-view event volume as `r_view`'s audience numerator, while leaving physical field identity and aggregation/deduplication release semantics unresolved. The same Glossary defines `Potential audience` as adult U.S. monthly-active users who can potentially see content because it was shared by a connection, independently corroborating the denominator's connection-inventory interpretation without identifying the physical 300450 field. The US2020 project codebook also makes the field-level authority explicit: each per-dataset data dictionary records variable name, description, type, group, map keys, aggregation methods and disclosures. Consequently, narrative labels such as “audience size” can guide discovery but cannot freeze a physical field, aggregation rule or privacy/disclosure interpretation without the target dictionary rows. The v2 Exposure-to-URL technical section is now decomposed more precisely: Data categorization and Aggregation are URL-level, while the Disclosures paragraph alone switches to domain-level exposed-audience counting. The legacy numerator conflict is therefore localized to counting/deduplication semantics, not to the declared table or aggregation level. The indexed v3 Exposure-to-URL overview also narrows the numerator-side legacy scope conflict by stating that each column aggregates data for the specific URL. This resolves the v2 overview-level wording ambiguity but not the v3 disclosure semantics: the `Disclosures` subsection remains unrecovered, so the v2 domain-worded duplicate-counting rules remain inadmissible and the numerator-side semantics stay blocked. The same v3 codebook is asymmetric across the candidate pair: Exposure-to-URL uses `specific URL`, whereas Potential-Exposure-to-URL remains a URL-level table whose overview says `specific domain`. The Exposure correction must therefore not be generalized to Potential Exposure; denominator scope remains independently unresolved. The older `f1a_somar_count_semantics_audit` is now aligned with the same shared-inventory boundary: its candidate status is conditional, its next gate requires an explicit shared-inventory rule, and no raw 300470 audience subset relation is assumed without release mapping. The next admissible gate remains `OFFICIAL_VARIABLE_DICTIONARY_CONTENT_ACCESS`, with the public Data & Documentation files for ICPSR 300450 and 300470 as the preferred first route. ICPSR main data search and SSVD are retained as auxiliary public discovery routes because ICPSR documents main search as indexing available study documentation, including variable descriptions; SSVD is explicitly incomplete, and no current 300450/300470 variable-level hit has been accepted as evidence. The global ICPSR variable-search endpoint itself is identifiable, but parameterized queries cannot be executed through the current automated audit surface, so that limitation is not interpreted as variable absence. The legacy Exposure-URL codebook also contains an internal URL-context/domain-disclosure scope conflict, so its domain duplicate-counting paragraph is not used to freeze URL-level audience semantics. The legacy Potential-Exposure-URL section has an independent structural URL/domain conflict on the denominator side: draft, v2 and indexed v3 identify the table as URL-level, while v2 Data categorization describes URLs but its Aggregation and Disclosures subsections explicitly use domain-level semantics. Because the contradiction persists across legacy versions and across subsections, no side is privileged by inference and the domain-worded rules are not used to freeze URL-level potential-audience semantics.

Current coauthor replication links are also treated only as navigation provenance: Hunt Allcott's page reuses legacy SOMAR record 43 across multiple US2020 publications, while Jennifer Pan's page links to the US2020 collection search. No metadata crosswalk has been recovered that equates record 43 with the independently cited replication-code DOI `10.3886/spb3-g558` or with an ade7138-specific package.

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
- GitHub Pages publishes from `main` / root and has completed a successful build on the v0.1.1 release commit. GitHub Pages may use the root `README.md` itself as the site entry file when no `index.html` or `index.md` is present. The root `README.md` therefore remains the canonical content source even when the same content is rendered through the Pages URL; Pages must not introduce divergent scientific, release or visual-identity claims.

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

1. Keep F1a at **RECOVERY_TESTED**. The SOMAR column/privacy gate is a retained negative result, not a failed reason to substitute a different empirical quantity.
2. Treat candidate `r_view` only as `exposed_audience_users / potential_audience_users`; `content_views` remains an invalid numerator for this unique-user fraction.
3. Obtain **official variable-dictionary content** for ICPSR 300450 and 300470, first through their public ICPSR/SOMAR Data & Documentation files, then through an official variable/documentation endpoint if needed. In a normal browser, ICPSR documents the sequence `study page -> Data & Documentation -> dataset Download dropdown -> Codebook / ICPSR Codebook`; use this as the noninferential manual fallback when automated listing fails, and record the collection version plus documentation-file identity before reading fields. If those public routes still do not locate the target documentation, SOMAR explicitly invites researchers to contact `somar-help@umich.edu`; use this as a documentation-locator escalation before any VDE fallback, not as evidence that the gate has passed. The exact support request is now frozen in the audit as `READY_NOT_SENT`; it asks for public documentation/version identifiers only and must not be sent or treated as evidence without a separate user action and an actual official response. Current SOMAR guidance says restricted-dataset documentation is publicly downloadable before application; approved SOMAR/VDE release documentation is only a fallback if the public material cannot resolve a required release-specific field or disclosure rule. Legacy record-34 UUID/size locators may guide retrieval but must not be treated as current-release file identity. Use ICPSR main data search / SSVD only as discovery aids; an indexed hit still requires current-release linkage and release-semantic verification.
4. Before any calculation, verify the exact potential-audience, exposed-audience, owner-type and URL/key fields and tie both tables to explicit release versions. For 300470, recover the concrete current DOI/version from the study record or official metadata export; schema-level DOI patterns are not sufficient to infer the version. Resolve the legacy Exposure-URL URL/domain disclosure-scope conflict rather than treating its domain-worded paragraph as the URL aggregation rule. Resolve the legacy Potential-Exposure-URL URL/domain aggregation-scope conflict independently; do not correct `domain` to `URL` by inference.
5. Freeze release-specific suppression/minimum-cell, perturbation/noise, rounding, estimated-count, missing/suppressed/zero, absent-row and URL-canonicalization semantics. Do not import privacy rules from unrelated Meta data products.
6. Treat owner_type=`all` as the documented combined posts-from-users/Pages/groups category, but do not assume its audience count equals a simple sum of the component rows.
7. Only after `OFFICIAL_VARIABLE_DICTIONARY_CONTENT_ACCESS` resolves the field and disclosure semantics may a separate prospective empirical-analysis contract authorize an `r_view` calculation. If access remains unavailable, retain the negative result.
8. Keep PlatformView→CBD CognitiveExposure unresolved until a prospective cognitive measurement bridge is justified; even a valid FIES `r_view` is not dyadic `q_transmit`.
9. Do not begin recipient Decision generation or the full Share→Exposure→Decision→Share loop until source-attribution, item-identity and decision-opportunity contracts identified in Issue #110 are resolved.
10. Treat any future M1.E4 item-heterogeneity redesign as a separate prospective post-M1 research program.

## How to resume after context loss

Start by reading, in order:

`README.md -> STATUS.md -> DEVELOPMENT.md -> CHANGELOG.md -> CITATION.cff`

Then inspect the latest GitHub release/tag, the most recent green `CBD validation` run, open issues/PRs, and the contracts/results relevant to the task.

Do not infer the current model state from old branches or historical chat text when the canonical repository disagrees.
