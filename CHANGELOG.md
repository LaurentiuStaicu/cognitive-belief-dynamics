# Changelog

All notable public scientific-core releases of Cognitive Belief Dynamics (CBD) are recorded here.

## Unreleased

### Repository presentation

- redesigns the public README as a reader-oriented explanation of the model, following the suite presentation lineage established by Ask the Model first and Romanian Monetary Dynamics second;
- separates public explanation from technical traceability: internal phase codes, experiment identifiers, benchmark cell counts, thresholds and promotion states remain in STATUS.md, DEVELOPMENT.md, CHANGELOG.md, docs/ and machine-readable scientific artifacts rather than the landing-page narrative;
- updates the README design contract and regression tests so the landing page explains the research purpose, conceptual model, current capabilities, scientific limits and research direction before routing readers to technical reference material;
- preserves the approved repository icon and badge labels while marking the older README preview / conceptual assets as historical, non-canonical presentation artifacts;
- changes repository presentation only; no model equation, parameter, scientific result, dataset, release version or validation boundary is changed.

### Progressive endogenization research

- corrects a scope overreach in the legacy audit: a deleted-Page/pseudonymization exclusion recovered from potential-audience domain/derived documentation is not demonstrably part of the target Potential-Exposure-URL section, so it is not imported as a 300450/300470 filter-compatibility blocker.

- adds an optional future-event scheduler around the unchanged `Simulator.step()` cognitive transition path;
- adds an explicit static directed synthetic network fixture and deterministic forced pass-through transmission policy;
- establishes the first F1a synthetic executable edge: realised Share(A) → delayed Exposure(B) → existing Familiarity(B) update;
- preserves v0.1.1 open-loop behavior when the endogenous layer is not invoked;
- adds separate scheduler provenance, horizon/max-event guards, backward-equivalence tests, property tests, a strict experiment contract/schema and an ODD supplement;
- prospectively freezes a synthetic `q_transmit` recovery design before execution, with 20 core cells and 10 explicitly non-gating stress cells;
- retains an authoritative 200-replicate-per-cell recovery result: all 20 core cells pass the 0.80 gate, minimum core recovery 0.885, deterministic/structural controls pass, and the result reproduces byte-for-byte in CI;
- advances F1a to `RECOVERY_TESTED` only; `q_transmit` remains calibration-only, F1a is not empirically constrained or active, and the canonical System Dynamics boundary is unchanged.
- adds a post-recovery empirical-observability audit: Bluesky/SNAP-style public data may constrain topology and action components, but no current audited public source supplies the recipient-specific exposure/impression and negative-opportunity measurements required to estimate the present `q_transmit`; no empirical promotion is authorized.
- adds a platform-view component bridge based on SOMAR/FIES public metadata, separating potential delivery, actual platform view and cognitive exposure; candidate aggregate view/engagement ratios remain restricted-codebook-gated and are explicitly not `q_transmit`.
- audits the public SOMAR project codebook and confirms structural compatibility across URL-level potential exposure, actual exposure and engagement (URL × owner type, common study period and broad active-user population), while keeping all numerical pairing blocked pending exact variable/count/privacy semantics.
- resolves public FIES count semantics needed for the candidate platform-view component: Audience is a unique-user/participant count, Content views are repeated-capable screen-appearance counts (Facebook visible render >250 ms), and owner-type `all` combines user/Page/group posts; `r_view` is conceptually restricted to exposed-audience users / potential-audience users and remains numerically blocked pending exact columns and privacy/missingness/linkage rules.
- records the next SOMAR column/privacy gate as a controlled negative result: official legacy dictionary/variable-description artifacts and the relevant current ICPSR studies are identifiable, but the exact release columns, disclosure-control transformations, missingness encoding and cross-release linkage are not inspectable from the currently available public web surface; no column names are guessed and no `r_view` calculation is authorized.
- clarifies the SOMAR documentation-access route using current official guidance: codebooks and documentation for restricted-use datasets are publicly downloadable before application, so the unresolved column gate reflects uninspected exact dictionary rows and release linkage rather than a requirement for VDE approval merely to read public documentation.
- retains file-level UUID/byte-size locators for the legacy record-34 public documentation bundle as retrieval provenance only; these identifiers do not establish current 2026 collection linkage or inspected dictionary contents.
- narrows legacy file-level provenance: the indexed MARC manifest directly proves the public documentation UUIDs/byte sizes only for record 34; no record-level manifest was recovered proving the same UUID attachments for legacy records 32/36, so record-34 locators are not treated as direct file-identity evidence for Exposure/Potential Exposure or for current 300450/300470.
- refines the legacy attachment evidence: records 32 and 36 are each independently indexed as `Multiple Files` and associated with the US2020 external codebook, confirming target-specific multi-file documentation availability; exact dictionary/CSV identity and reuse of record-34 UUIDs remain unverified.
- records legacy-source link rot explicitly: the tested `socialmediaarchive.org` record/codebook/glossary URLs now redirect to the current SOMAR home page, so they remain historical/indexed provenance locators only and are not treated as live artifact-download endpoints; previously recovered historical evidence is retained and the scientific gate is unchanged.
- corroborates that redirect state with SOMAR's official Winter 2026 transition notice, which states that the SOMAR website and archive data moved to the ICPSR platform and that resources/studies/features are now accessed through the ICPSR unified interface; old URLs are therefore classified as historical locators within an announced platform migration, not unexplained dead links.
- records a separate current-page rendering limitation: direct audited retrieval of both ICPSR 300450 and 300470 now exposes only the client-side shell while the SOMAR catalog remains content-bearing; previously recovered official indexed 300450 V2 DOI/data-dictionary availability is retained, and shell-only rendering for 300470 is explicitly non-evidentiary rather than documentation absence.
- restores canonical cross-surface consistency for the F1a `r_view` candidate: count-semantics, PlatformView bridge, schemas, tests, human-readable docs and `STATUS.md` now all require explicit shared-inventory compatibility before interpreting exposed-audience / potential-audience as a release-field view-rate fraction; the prior unconditional `CONCEPTUALLY_JUSTIFIED_NUMERICALLY_BLOCKED` label is removed.
- removes an ambiguity in the earlier public-codebook audit: `hard_gates` are now explicitly modeled as requirements rather than satisfaction flags, `currently_satisfied=false`, and the candidate ratio records `shared_inventory_required=true` / `shared_inventory_verified=false`; the formerly misleading `actual_subset_compatibility_verified=true` key is removed.
- refines the frozen SOMAR Help draft so the public-documentation locator also asks where current row inclusion/eligibility, pairing-key, absent-row and shared-inventory relationship rules are documented, while explicitly avoiding any request for SOMAR to adjudicate scientific compatibility; request status remains `READY_NOT_SENT`.
- classifies the legacy-to-current study relationship as multi-field identity concordance rather than an explicitly verified migration crosswalk: records 36/32/34 align with ICPSR 300450/300470/300475 across exact title, URL level, study period, broad population and semantic role, but no indexed official record-to-study crosswalk or record-specific redirect was recovered.
- rules out legacy External Source ID as a public crosswalk route because ICPSR documents it as internal/not publicly displayed and the current schema no longer exposes it; Version History/Version Note remain valid public provenance targets, but no 300450/300470 migration payload has been recovered.
- refines the legacy Exposure DOI ambiguity using two separately indexed official v3 codebook copies: SOMAR record 68 gives `10.3886/rnr8-jj22` while record 70 gives `10.3886/rnr8-ij22`; the audit freezes this as a duplicate-v3 transcription divergence and selects neither value without record-level metadata or DOI-registry adjudication.
- further characterizes the legacy Exposure DOI conflict: v2 record 61 and v3 record 68 both render `10.3886/rnr8-jj22`, while v3 record 70 renders `10.3886/rnr8-ij22`; this cross-version support for `jj22` is retained as provenance evidence but is explicitly insufficient for canonical DOI selection without record-level metadata or registry adjudication.
- distinguishes DOI existence from DOI-value retrieval for ICPSR 300470: both current and legacy ICPSR metadata schemas require a collection DOI, while the concrete current DOI/version remains unrecovered and is not inferred from schema patterns or neighboring studies.
- corrects the interpretation of the 300470 versioned-route probe: a current FIES counterexample (ICPSR 300464) is reachable at a `/versions/V1.0` URL while its indexed Version History exposes current V2.0 [2026-04-01], so route responsiveness carries no positive evidentiary weight for the current 300470 version; canonical DOI/version remain unverified.
- records ICPSR's documented manual Data & Documentation → dataset Download → Codebook / ICPSR Codebook route as the noninferential retrieval fallback when automated file listings are unavailable; this operationalizes the next gate without treating navigation guidance as verified variable content.
- prepares a reproducible SOMAR Help public-documentation locator request for ICPSR 300450/300470 and freezes it as `READY_NOT_SENT`; the draft explicitly excludes restricted data/VDE access, field inference and numerical calculation, and a future support reply cannot change scientific state without target-specific official artifacts being archived and inspected.
- operationalizes the post-web documentation-locator escalation: SOMAR support may be asked only for current public 300450/300470 documentation links/identifiers and 300470 DOI/version metadata; no restricted-data/VDE request is implied, and a support reply cannot pass the scientific gate without archived target-specific official evidence and inspected documentation contents.
- adds SOMAR Help (`somar-help@umich.edu`) as the official documentation-locator escalation after public/manual/indexed retrieval routes and before any VDE fallback; asking support to locate public documentation is procedural only and does not pass the column gate.
- verifies current data-dictionary availability directly on the ICPSR 300450 study page (V2) while keeping the dictionary file identity, contents and denominator column uninspected; no equivalent target-specific content-bearing dictionary offer has yet been recovered for 300470, and that indexing asymmetry is not treated as evidence of absence.
- adds the indexed US2020 Glossary as an independent semantic authority: `Audience` is a user/participant count for at-least-one organic-content view, while `Content views` is a screen-appearance count; this bars content-view events from the `r_view` numerator but does not identify the physical audience field or resolve aggregation/deduplication/current-release linkage.
- extends the Glossary evidence with its `Potential audience` definition: adult U.S. monthly-active users who can potentially see content because it was shared by a connection; this independently supports the denominator concept while remaining non-evidentiary for the physical 300450 field and release aggregation semantics.
- records the US2020 codebook's explicit documentation contract: each dataset's data dictionary is the field-level source for variable name, description, type, group, map keys, aggregation methods and disclosures; narrative codebook prose therefore cannot substitute for the uninspected current 300450/300470 dictionary rows, and the negative numerical gate is preserved.
- localizes the legacy Exposure-URL inconsistency at subsection level: v2 Data categorization and Aggregation are explicitly URL-level, while only Disclosures switches to domain-level audience counting; the table/aggregation level is therefore not reclassified as domain-level, but counting/deduplication semantics remain blocked pending v3/current dictionary disclosure evidence.
- narrows the legacy Exposure-URL scope conflict using the indexed v3 codebook: the v3 overview now states that each column aggregates data for the specific URL, resolving the overview-level URL/domain ambiguity; because the v3 Disclosures subsection remains unrecovered, exact audience counting/deduplication semantics and the numerical gate remain unresolved.
- records an explicit v3 numerator/denominator scope asymmetry: Exposure-to-URL now says columns aggregate the specific URL, while Potential-Exposure-to-URL remains declared URL-level but says columns aggregate the specific domain; the numerator wording correction is therefore not propagated to the denominator by inference, and both remaining semantic gates stay blocking.
- separates controlled replication-code access from the public documentation gate: Science/current author materials direct researchers to apply for analysis/replication code and data, while public Codebook/Data Dictionary retrieval remains the first route; lack of a public code repository is not treated as missing documentation.
- distinguishes author-facing replication navigation locators from package identity: Hunt Allcott's page routes several US2020 publications through legacy SOMAR record 43 while Jennifer Pan's page uses the US2020 collection search; neither link is treated as an article-specific package, and record 43 is not equated with DOI 10.3886/spb3-g558 without an explicit crosswalk.
- records the published FIES replication-code DOI `10.3886/spb3-g558` as a controlled SOMAR/ICPSR VDE provenance locator only; its contents and scope to Science `ade7138` are uninspected/unverified here, so it does not substitute for target-specific current-release dictionary evidence.
- records the official US2020 two-stage code architecture: Meta-only upstream code generated research-specific platform tables while downstream preprocessing/analysis was executable by academics; the public FAQ confirms VDE replication archives but does not establish that they contain the complete upstream generator or current 300450/300470 release schema, so replication code is not presumed to substitute for the dictionary gate.
- records the legacy codebook paper-to-dataset mapping for Science `10.1126/science.ade7138`, explicitly associating the paper with the Potential-Exposure-URL, Exposure-URL and Engagement-URL surfaces while keeping current-release linkage, exact columns and privacy semantics unresolved.
- tightens the `r_view` conceptual status: the Science paper verifies a nested inventory→Feed funnel for political-news posts supplied by friends, Pages and Groups, but the standalone Exposure release description does not explicitly restate the Potential table's connection-based eligibility restriction; `r_view` is therefore now `CONCEPTUALLY_CONDITIONAL_ON_SHARED_INVENTORY_NUMERICALLY_BLOCKED` until current-release inventory equivalence is established.
- aligns the older F1a count-semantics contract with that stricter boundary: its candidate status is now conditional on shared inventory, the unresolved gate includes paper-to-release inventory equivalence, and no raw 300470 audience is assumed to be a subset of raw 300450 potential audience without explicit release mapping.
- separates the Science paper's conceptual unique-user audience funnel from release-field arithmetic: the paper defines potential and exposed audiences as unique-user sets, but legacy disclosure text contains multi-counting rules and current `audience size` deduplication semantics remain unverified; `r_view` therefore cannot yet be interpreted as a probability/fraction of potential users from release fields.
- separates the Science segregation-index weighting quantity `v_n` (`total number of unique views`) from release-field identity: the paper does not establish that `v_n` equals the released exposed-audience or content-views field, so it is explicitly barred from the `r_view` numerator/denominator until official dictionary mapping exists.
- strengthens the conceptual pairing evidence from the Science paper: it states that each analyzed URL has potential, exposed and engaged audience measures, supporting same-URL analysis pairing; this is explicitly separated from current-release row identity, URL-key equivalence, suppression/filter symmetry and absent-row semantics, which remain unverified for 300450/300470.
- identifies a v3 row-universe asymmetry that blocks naive rowwise `r_view`: Potential Exposure and Exposure share URL level, population, study period, civic/news classification and the >100-share threshold, but Potential requires potential Feed eligibility while Exposure requires an actual Feed view; absent Exposure rows therefore cannot be assumed zero or silently dropped by inner join without release-specific absent-row semantics.
- records that the coauthor-facing `Replication` link for `ade7138` targets the general US2020 SOMAR collection and is reused across multiple project papers; it is not treated as an article-specific public replication package.
- separates ICPSR search availability facets from restricted-use status: the SOMAR search can expose a Public Data facet while 300450/300470 remain explicitly restricted; ICPSR documents availability and restriction type as separate metadata concepts, so the facet is not treated as unrestricted-file evidence or as a passed documentation gate.
- distinguishes SOMAR thematic/catalog search from ICPSR main data search and SSVD: ICPSR documents the latter as indexing available documentation/variable descriptions, while SSVD coverage is incomplete; these routes are discovery fallbacks only and no 300450/300470 variable hit is treated as gate-passing evidence.
- records the public ICPSR variable-search endpoint and makes its current parameterized-query retrieval failure explicitly non-evidentiary; ICPSR guidance redirects missing Variables-tab information to the codebook/Data & Documentation route.
- records the legacy Exposure-URL codebook scope conflict in which URL-level context is followed by domain-level disclosure wording; those duplicate-counting rules are not imported into the URL-level `r_view` gate.
- locks derived ideological-segregation aggregation rules to their own release surface: its exposed-audience disclosure uses a sum of views and potential/engaged metrics sum daily post-level audience counts, but these rules are not imported into base ICPSR 300450/300470, where content views and audience size are distinct catalog quantities.
- records an independent Potential-Exposure-URL structural scope conflict: draft, v2 and indexed v3 identify an URL-level table, while v2 Data categorization remains URL-oriented but its Aggregation and Disclosures subsections explicitly use domain-level semantics; the repeated contradiction is not repaired by inference, so both numerator and denominator URL-level aggregation remain scope-gated.
- corroborates the SOMAR access interpretation with current ICPSR holdings documentation that labels documentation files public by definition, while keeping collection-version identity as a separate unresolved gate.

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
