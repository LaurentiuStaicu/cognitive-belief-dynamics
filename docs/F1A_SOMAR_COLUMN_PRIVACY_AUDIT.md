# F1a SOMAR column-identity and privacy-rules audit

Status: **DOCUMENTATION_ARTIFACTS_LOCATED_COLUMN_CONTENTS_UNVERIFIED**

F1a ladder stage remains: **RECOVERY_TESTED**

This audit follows the count-semantics audit and tests the next hard gate before any numerical PotentialDelivery→PlatformView component analysis:

`COLUMN_IDENTITY_AND_PRIVACY_RULES_AUDIT`.

It does not calculate `r_view`, estimate `q_transmit`, change runtime behavior, or authorize empirical promotion.

## What is now verified

### Current ICPSR/SOMAR study identity

The current SOMAR/ICPSR catalog identifies the relevant URL-level studies as:

- ICPSR 300450 — Potential Exposure to Facebook Posts with Civic News URLs;
- ICPSR 300470 — Exposure to Facebook Posts with Civic News URLs;
- ICPSR 300475 — Engagement with Facebook Posts with Civic News URLs.

Legacy SOMAR/codebook metadata provides additional retrieval identifiers for the same titled dataset surfaces. Record 36 / DOI `10.3886/snmc-n870` identifies Potential Exposure URLs, record 34 / DOI `10.3886/n3r7-br77` identifies Engagement URLs, and record 32 unambiguously identifies Exposure URLs. For **record 32**, however, two separately indexed official **v3** codebook copies disagree on the DOI transcription: SOMAR record 68 renders `10.3886/rnr8-jj22`, while SOMAR record 70 renders `10.3886/rnr8-ij22`. The duplicate-v3 discrepancy is therefore verified, but the exact legacy DOI remains unresolved until record-level metadata or a DOI-registry response adjudicates the two strings. These legacy identifiers remain provenance/retrieval aids only; they do not establish byte identity or current-release linkage with the 2026 ICPSR collection.

The current catalog descriptions confirm that 300450 reports URL-level potential-audience information and that 300470 reports URL-level view/audience information for the same broad U.S. adult monthly-active-user study period. Both current catalog records are marked released/updated on 2026-04-01.

This is sufficient to retain the existing pairing design as plausible, but it is not sufficient to name columns or calculate a ratio or to prove that a particular documentation file belongs to that release version.

### Legacy Exposure DOI transcription conflict

The legacy Exposure record itself is stable: SOMAR search results identify **record 32** as *Exposure to Facebook Posts with Civic News URLs*. Two separately indexed official **v3** codebook copies disagree on the DOI transcription:

- v3 codebook under SOMAR record 68: `10.3886/rnr8-jj22`;
- v3 codebook under SOMAR record 70: `10.3886/rnr8-ij22`.

This is frozen as a **duplicate-v3 documentation divergence**. Because both indexed artifacts identify themselves as v3 and otherwise describe the same Exposure-to-URL dataset, the audit does not reinterpret the difference as a normal version transition and does not choose either string by majority, recency, or lexical preference. Record-level metadata or DOI-registry evidence is still required before a canonical legacy DOI can be frozen.

A third indexed source adds useful but non-decisive context: the **v2** codebook under SOMAR record 61 also renders `10.3886/rnr8-jj22`. The observed pattern is therefore `v2 jj22 + v3(record 68) jj22 + v3(record 70) ij22`. This gives `jj22` cross-version support, but the audit explicitly does **not** treat majority or cross-version repetition as registry-level adjudication.


### Legacy Potential Exposure URL aggregation scope conflict

The legacy v2 codebook contains a second independent URL/domain scope inconsistency, this time on the **denominator** side of the candidate ratio.

For *Potential Exposure to Facebook Posts with Civic News URLs*, the section identifies table `potential_exposure_facebook_posts_with_civic_news_urls`, marks its level as **URL**, states that rows correspond to URLs, and represents each URL by four post-owner rows (`user`, `Page`, `group`, `all`). However, the same overview then states that each column aggregates platform log data for the **specific domain** over the study period.

Legacy sources:
- draft codebook: https://socialmediaarchive.org/record/40/files/US2020_FB%26IG_Elections_External_Codebook.pdf
- v2 codebook: https://socialmediaarchive.org/record/61/files/US2020_FB%26IG_Elections_External_Codebook_v2.pdf

The same URL/domain wording conflict is visible in the draft, v2, and indexed v3 codebooks, so it is neither a one-copy transcription artifact nor confined to a single legacy version. The indexed v3 section still identifies the table as URL-level and says rows correspond to URLs, while retaining the same "specific domain" aggregation wording.

Additional legacy v3 source:
https://socialmediaarchive.org/record/70/files/US2020_FB%26IG_Elections_External_Codebook_v3.pdf

The inconsistency is not confined to the overview. In the v2 section, **Data categorization** says the dataset summarizes data for URLs in posts users could have viewed, while **Aggregation** explicitly says `Domain level: metrics calculated at the news source level`, and **Disclosures** says potential-audience metrics are aggregated by domain by adding daily post-level counts for URLs within that domain.

This is therefore a structural conflict between the declared table/data-categorization level and the Aggregation/Disclosures semantics. The domain-worded rules must not be imported as the URL-level denominator aggregation rule for `r_view`. The audit does not silently correct `domain` to `URL`, nor does it privilege the URL-level metadata over the domain-level technical subsections; exact denominator semantics remain unresolved until an authoritative current dictionary/codebook or other scope-resolving source establishes them.

This conflict is separate from the already-recorded Exposure-URL disclosure conflict. The numerator and denominator legacy documentation therefore each contain their own URL/domain wording ambiguity, and neither side may be repaired by inference.

### Legacy Exposure URL disclosure scope conflict

The legacy v2 external codebook exposes a separate documentation problem that affects the attempted URL-level audience pairing. The conflict can now be localized precisely across its technical subsections:

- **Data categorization:** metrics summarize attributes and views of **URLs** by users;
- **Aggregation:** explicitly **URL level**, “metrics calculated at the news story level,” with post-owner type associated with the URL;
- **Disclosures:** switches to exposed-audience metrics “aggregated by **domain**,” calculated from daily post-level exposed-audience counts for URLs within that domain.

Thus the v2 table identity and aggregation level are URL-consistent; the contradiction is specifically in the disclosure/counting semantics.

Legacy source: https://socialmediaarchive.org/record/61/files/US2020_FB%26IG_Elections_External_Codebook_v2.pdf

This is treated as an **internal documentation-scope conflict**, not as evidence that the URL table actually uses domain aggregation. It may be a copy/paste error, a stale paragraph, or an intentional rule whose scope is not evident from the indexed text. The audit does not choose among those possibilities.

A later indexed **v3** codebook narrows this conflict: its Exposure-to-URL overview says rows correspond to URLs and that each column aggregates platform log data for the **specific URL** over the study period. That resolves the overview-level URL/domain wording ambiguity for v3. However, the v3 `Disclosures` subsection itself has not been recovered through the audited surface, so the exact audience-counting/deduplication semantics remain unverified.

V3 source: https://socialmediaarchive.org/record/70/files/US2020_FB%26IG_Elections_External_Codebook_v3.pdf

Consequently, the duplicate-counting/deduplication behavior in the **v2 domain-worded disclosure paragraph must not be imported** as the URL-level rule for 300470 or the candidate `r_view`. The v3 overview is positive scope evidence, but it is not a substitute for the uninspected v3 disclosure/dictionary rows or current-release documentation.

### V3 Exposure/Potential-Exposure scope asymmetry

The indexed v3 codebook makes the numerator/denominator documentation asymmetry explicit within the **same document**:

- `exposure_facebook_posts_with_civic_news_urls`: declared level **URL**; rows correspond to URLs; each column aggregates platform log data for the **specific URL**.
- `potential_exposure_facebook_posts_with_civic_news_urls`: declared level **URL**; rows correspond to URLs; yet each column is still described as aggregating platform log data for the **specific domain**.

Source: https://socialmediaarchive.org/record/70/files/US2020_FB%26IG_Elections_External_Codebook_v3.pdf

This means the v3 wording improvement on the Exposure side cannot be transferred to Potential Exposure by analogy. The denominator remains scope-conflicted on its own terms. Conversely, the URL-consistent Exposure overview still does not recover its v3 `Disclosures` subsection, so numerator duplicate-counting/deduplication semantics remain unresolved.

Status:

`V3_EXPOSURE_OVERVIEW_URL_CORRECTED / POTENTIAL_OVERVIEW_DOMAIN_WORDING_PERSISTS / NO_CROSS_INFERENCE`

### Legacy-to-current identity concordance

The legacy and current surfaces can be compared more explicitly without overstating the migration evidence.

For the three URL-level study surfaces used in this audit, the following pairs show **multi-field identity concordance**:

- legacy SOMAR record **36** ↔ current ICPSR **300450**, *Potential Exposure to Facebook Posts with Civic News URLs*;
- legacy SOMAR record **32** ↔ current ICPSR **300470**, *Exposure to Facebook Posts with Civic News URLs*;
- legacy SOMAR record **34** ↔ current ICPSR **300475**, *Engagement with Facebook Posts with Civic News URLs*.

Across each pair, the available legacy and current sources agree on the exact study title, URL level, study period (2020-09-01 through 2021-02-01), broad U.S. adult monthly-active-user population, and the corresponding potential/exposed/engaged semantic role. The legacy codebook also preserves the four owner rows (`user`, `Page`, `group`, `all`) for these URL-level tables.

This concordance does **not** establish an explicit migration crosswalk. No indexed official source recovered in this audit states record-by-record that `36 -> 300450`, `32 -> 300470`, or `34 -> 300475`, and the old record URLs now redirect to the general SOMAR home page rather than to record-specific current study pages.

The contract therefore classifies the relationship as:

`MULTI_FIELD_IDENTITY_CONCORDANCE_EXPLICIT_MIGRATION_CROSSWALK_UNVERIFIED`

This supports provenance discovery and continuity only. It does not establish current-release byte identity, collection-version linkage, documentation-file identity or physical dictionary-row identity.

### Current target documentation availability

A current content-bearing ICPSR result is now available for **300450 — Potential Exposure to Facebook Posts with Civic News URLs**. The current study page exposes the collection DOI `10.3886/ICPSR300450.V2` and, under its variable-description surface, explicitly states: **“Download the data dictionary for variables present in this dataset.”**

This closes one narrower retrieval question: for the denominator-side current collection, **data-dictionary availability is verified** on the current study page. It does not yet establish the dictionary file identity, its bytes, its exact rows, or any physical variable name. The dictionary contents remain uninspected in this audit.

The corresponding target-specific content-bearing block has not yet been recovered for **300470 — Exposure to Facebook Posts with Civic News URLs**. Current catalog identity is verified, but the current DOI/version and an explicit current-page data-dictionary offer remain unrecovered through the audited automated/indexed surface.

This asymmetry must not be converted into an absence claim. ICPSR guidance directs researchers to Data & Documentation / Codebook when variable information is not exposed by the indexed interface, and SOMAR states that restricted-use documentation is publicly downloadable before application.

Accordingly:

- `300450`: current dictionary **availability verified**; file identity and contents uninspected;
- `300470`: current target-specific dictionary availability **not yet recovered**; absence not inferred;
- exact numerator and denominator columns remain unverified;
- the variable-dictionary gate remains negative and no `r_view` calculation is authorized.

### Current study-page live retrieval state

A controlled live-retrieval check on **2026-09-25** opened the current ICPSR pages for both target studies directly from the official SOMAR catalog:

- ICPSR **300450** — Potential Exposure to Facebook Posts with Civic News URLs;
- ICPSR **300470** — Exposure to Facebook Posts with Civic News URLs.

Through the audited web surface, both direct study-page URLs currently expose only the client-side application shell rather than content-bearing DOI/version/Data & Documentation markup. The official SOMAR catalog remains content-bearing and still exposes both target descriptions and their 2026-04-01 release/update date.

A subsequent exact current indexed search on **2026-09-25** re-recovered the 300450 V2 DOI/data-dictionary block, independently reconfirming that current indexed evidence. The same search still did not recover an equivalent 300470 DOI/dictionary block. The direct study-page shell behavior is therefore recorded as a **live rendering limitation**, not as a reversal of indexed evidence.

Accordingly:

- the official indexed 300450 DOI `10.3886/ICPSR300450.V2` / V2 and explicit data-dictionary availability were re-recovered on 2026-09-25 and remain current indexed evidence;
- current shell-only rendering does **not** invalidate that recovered 300450 evidence;
- for 300470, the same shell-only state remains non-evidentiary and must not be converted into a claim that documentation is absent;
- the current 300470 DOI/version and dictionary contents remain unrecovered;
- the scientific gate is unchanged.

Status:

`CURRENT_DIRECT_PAGES_SHELL_ONLY / CATALOG_CONTENT_AVAILABLE / CURRENT_300450_INDEXED_EVIDENCE_RECONFIRMED / 300470_IDENTITY_AND_DICTIONARY_UNRECOVERED / NO_ABSENCE_INFERENCE`

### Current collection identity status

The current individual ICPSR page for **300450** exposes the collection DOI `10.3886/ICPSR300450.V2`; the current potential-exposure collection identity is therefore verified as **V2**.

Official source: https://www.icpsr.umich.edu/sites//view/studies/300450

For **300470**, the current individual study page and catalog entry are identifiable, but the current DOI/version string is not exposed through the public/indexable surface available to this audit. No `.V1`, `.V2` or other version suffix is inferred by analogy. Its exact current collection DOI/version therefore remains **unverified** in this audit.

### ICPSR collection-version linkage rule

Current ICPSR versioning guidance states that a change in any data or documentation file, or the addition or withdrawal of such a file, triggers a new version of the study/collection. ICPSR does not version individual files separately: the version statement applies to the collection as a whole.

Official source: https://www.icpsr.umich.edu/sites/icpsr/posts/shared/access-earlier-version

Therefore a legacy SOMAR filename, record number, DOI or title match is useful for retrieval and provenance, but it is not sufficient to establish that a legacy dictionary is the documentation associated with the current 2026 ICPSR collection version. Explicit collection-version linkage remains required before the physical fields or disclosure semantics can be treated as current-release facts.

### Legacy public documentation artifacts existed

The legacy SOMAR metadata surface for the same U.S. 2020 FIES political-segregation release explicitly listed public documentation artifacts including:

- `data_dictionary_political_segregation_paper.xlsx`;
- `variables_political_segregation_paper.csv`;
- `US2020_FB&IG_Elections_External_Codebook.pdf`;
- `US2020_Glossary.xlsx`.

The legacy project-level codebook is still search-indexed and identifies the relevant table names:

- `potential_exposure_facebook_posts_with_civic_news_urls`;
- `exposure_facebook_posts_with_civic_news_urls`;
- `engagement_facebook_posts_with_civic_news_urls`.

It also preserves the URL-level/four-owner-row structure already frozen by the previous audit.

Therefore the blocker is no longer whether a data dictionary ever existed. It did. The blocker is whether the exact dictionary/variable contents can be inspected and tied to the current ICPSR release version.

### Legacy documentation file-level locators

The indexed official legacy SOMAR MARC export for record **34** (*Engagement with Facebook Posts with Civic News URLs*, v1, published 2023-07-27) preserves file-level identifiers for the public documentation bundle:

- data dictionary: `data_dictionary_political_segregation_paper.xlsx`, UUID `ae0be9b4-8297-4231-9e76-08df5ac120af`, 44,149 bytes;
- variable descriptions: `variables_political_segregation_paper.csv`, UUID `086fb4cb-8cb6-4934-90c1-2a737d3dad62`, 76,863 bytes;
- project-level codebook: `US2020_FB&IG_Elections_External_Codebook.pdf`, UUID `2d333798-bd6c-478b-81b8-dc51812d96c2`, 724,746 bytes;
- glossary: `US2020_Glossary.xlsx`, UUID `b6da33f6-8850-44cb-84f4-50565cc2e17d`, 33,969 bytes.

Official legacy source: https://socialmediaarchive.org/record/34/export/hm?ln=en

These identifiers materially improve historical retrieval provenance, but they are **not** evidence that the same bytes are attached to current ICPSR 300450 or 300470, and they do not establish that the exact dictionary contents have been inspected. ICPSR collection-level version linkage remains required.

### Independent ICPSR documentation-public corroboration

ICPSR's current holdings page labels documentation files as **"public, by definition"**, including within restricted holdings. This independently corroborates the SOMAR Research Lifecycle statement that public documentation can be inspected without restricted-data approval.

Official source: https://www.icpsr.umich.edu/sites/icpsr/about/history

This is an access-classification finding only. It does not identify the current 300450/300470 documentation files, establish byte identity, or satisfy the variable-dictionary gate.

### Current SOMAR public-documentation access policy

Current SOMAR Research Lifecycle guidance states that codebooks and documentation for restricted-use datasets are publicly downloadable from the catalog so researchers can evaluate a dataset before submitting an application. The same guidance states explicitly that documentation files are publicly downloadable for both Controlled Download and Virtual Data Enclave (VDE) datasets.

Official source: https://www.icpsr.umich.edu/sites/somar/research-lifecycle

This changes the procedural interpretation of the unresolved gate, but not its scientific result. An approved restricted-data application or VDE workspace is **not a prerequisite merely to inspect the public documentation**. The next attempt should therefore begin with the public Data & Documentation files associated with ICPSR 300450 and 300470. Restricted-data access is relevant only if release-specific material needed for the scientific gate is not present in the public documentation.

### Current metadata-export routes and retired OAI path

Current ICPSR guidance distinguishes two active metadata-access routes:

1. the **ICPSR Metadata Export API** for batch search/export of collection metadata; its current user guide requires API credentials;
2. the **Export Metadata** tab on each individual study home page, where ICPSR states that study-level metadata can be downloaded in formats including Dublin Core and DDI-Codebook.

The current Object Export API documentation also clarifies a potentially useful but credential-gated dataset-level route. Its query schema allows `dataset` as a selectable object category, supports a numeric `identifier` filter, and returns only the latest version of matching products. In principle, that API could therefore recover dataset metadata tied to a known study/dataset identifier. However, the API gateway requires OAuth 2.0 client-credentials authentication with the `icpsr-objectexport` scope **and** an additional Application-Authorization bearer token before the Object Export service can be used. It is consequently classified here as **technically capable but not anonymously/publicly executable in this audit**. This restriction is procedural; it does not imply that dataset metadata are absent.

Official current sources:
- https://www.icpsr.umich.edu/sites/icpsr/about/repository-operations/accessing-metadata
- https://icpsr.github.io/metadata/icpsr_metadata_api/

The older OAI-PMH/DDI endpoint at `https://pcms.icpsr.umich.edu/pcms/api/1.0/oai/studies` is documented separately by ICPSR as a **retired metadata export service** while ICPSR transitions to the newer API. ICPSR states that the retired services would remain available **until at least August 2026**. Because this audit is being executed on **2026-09-25**, that continuity statement no longer guarantees availability at the audit date. A direct target-specific retrieval attempt through the audited web surface did not yield a 300470 metadata payload. The retired endpoint is therefore retained only as historical provenance/non-guaranteed legacy infrastructure and must not be represented as a reliable current fallback or preferred route.

Official retired-service source:
- https://www.icpsr.umich.edu/sites/icpsr/about/repository-operations/accessing-metadata/retired-metadata-export

The same official retired-service page exposes two additional reproducible metadata paths. First, it documents exact OAI `GetRecord` construction and identifies the study number itself as the record identifier; controlled probes for **300450** and **300470** were attempted with both `oai_dc` and `oai_ddi25`. The audited web surface could not retrieve those endpoint payloads. That failure is recorded as a retrieval/tooling result, not as evidence that either metadata record is absent.

Second, the page links a monthly compressed archive of **8,000+ DDI XML study records** at:

`https://www.icpsr.umich.edu/files/ICPSR/or/metadata/xml/abstracts.tar.gz`

The official link was resolved successfully on 2026-09-25, but the audited web surface reports the target as binary `application/x-gzip` content and cannot render or inspect the archive; the local execution surface also could not download it. The archive is therefore classified as **officially located but contents uninspected**. It remains potentially useful for study-level identity/provenance if obtained and inspected, but it is not a substitute for the current 300450/300470 Data Dictionary files and does not pass the variable-dictionary gate.

All of these metadata routes operate at the study/collection metadata level. They do **not** substitute for the public Data & Documentation files required by this gate. Collection metadata may help establish title, identifier, DOI/version and other provenance, but it cannot by itself establish the physical data-dictionary fields or the release-specific disclosure semantics required for `r_view`.

The current automated surface still does not expose the individual-study metadata export payload for 300470, the batch API cannot be queried here without API credentials, and the retired OAI continuity statement no longer covers the 2026-09-25 audit date. No additional 300470 DOI/version or variable information is inferred from these routes.


### 300470 versioned-route probe

Current SOMAR pages use explicit versioned study URLs. A controlled probe found that `/sites/somar/view/studies/300470/versions/V1.0` responds while several tested alternative routes are rejected.

That fact must **not** be interpreted as evidence that the current 300470 collection is V1.0. A direct current FIES counterexample is now indexed: ICPSR **300464** is reachable at a URL ending in `/versions/V1.0`, while the same indexed page exposes **Version History V2.0 [2026-04-01]** as the current published version.

Official counterexample surface:
- https://www.icpsr.umich.edu/sites/somar/view/studies/300464/versions/V1.0

Therefore a responding versioned route can represent a historical version route while the collection's current version is newer. The 300470 `V1.0` route is retained only as a route-level retrieval fact; it has **no positive evidentiary weight** for the current 300470 version.

The responding 300470 page also exposes only the client-side application shell through the audited surface and does not expose title, version label, DOI or study identifier in retrievable HTML.

Accordingly, the route probe does **not** verify V1.0. `current_collection_identity.exposure.version` remains **null/unverified**. No current-version candidate is ranked from the route probe. Version identity may be frozen only when a content-bearing authoritative target-specific source — such as current DOI/citation metadata, Version History, Export Metadata or an equivalent official record — explicitly exposes it.

### Unversioned DOI latest-version reference rule

ICPSR's current metadata style guide states that when a citation is **not** intended to identify a specific version, researchers should use the unversioned ICPSR DOI because that locator resolves to the latest archived version. Combined with the documented ICPSR DOI naming rule, the canonical unversioned reference form for study 300470 is therefore:

`https://doi.org/10.3886/ICPSR300470`

Official current source:
- https://icpsr.github.io/metadata/icpsr_style_guide/

This narrows the discovery problem, but it does **not** close the release-identity gate. The current audited web surface did not independently recover a content-bearing resolution target for that 300470 locator, and an unversioned latest-version reference would not by itself expose the current version number or the current version-specific DOI. Those version-bearing fields remain necessary for tying the exact Data & Documentation artifacts to a specific current collection release. Accordingly, the audit records the unversioned locator as a documented discovery/reference form only and keeps `current_collection_identity.exposure.doi` and `.version` null.

### DOI existence versus DOI-value retrieval for ICPSR 300470

ICPSR's current metadata schema, last updated **2026-09-22**, defines the Digital Object Identifier (DOI) as a **required** non-repeatable field for an ICPSR data collection. Its usage guidance states that an ICPSR DOI contains the ICPSR study number and a version component. The same documentation states that substantive changes create a new major version and a new version-specific DOI. The legacy ICPSR metadata schema likewise defines DOI as required.

Official sources:
- https://icpsr.github.io/metadata/icpsr_metadata_schema/
- https://icpsr.github.io/metadata/icpsr_legacy_schema/

This narrows the interpretation of the unresolved 300470 identity. The audit no longer treats the missing visible DOI string as evidence that ICPSR 300470 might lack a DOI. Instead, the **concrete current DOI/version value has not been recovered through the audited public/indexable or automated metadata surfaces**.

The schema pattern is not a substitute for the record itself. In particular, the audit does **not** construct a suffix such as `.V1`, `.V2`, or any other version from the study number, from ICPSR 300450, or from adjacent study numbers. The exact 300470 version remains unresolved until the current record or an official metadata export exposes it.


### Migration-crosswalk metadata route

The legacy ICPSR metadata schema contains an `External Source ID` field, but ICPSR explicitly documents that field as an **internal element that is not publicly displayed**. It consists of an ICPSR-defined source-organization code plus a depositor-supplied identifier.

The current ICPSR metadata schema does not expose an `External Source ID` field. It does, however, expose `Version History`, including `Version Number`, `Version Date` and `Version Note`; `Version Note` is explicitly defined as provenance information about a collection version.

Therefore a public `Export Metadata` payload should **not** be expected to reveal the old SOMAR record number through `External Source ID`. For a public explicit migration crosswalk, the admissible targets are instead:

- current `Version History` / `Version Note`;
- current citation or DOI metadata that explicitly references a legacy identifier;
- an official record-specific redirect or migration table;
- another official content-bearing metadata surface that states the legacy-to-current relation.

No such 300450/300470 migration-provenance payload has yet been recovered through the audited surface. This refines the retrieval strategy but does not change the scientific gate.

### ICPSR indexed-documentation discovery fallback

Current ICPSR guidance exposes a second public discovery route that must be distinguished from the SOMAR thematic/catalog search already discussed above.

The **Social Science Variables Database (SSVD)** searches structured variable-level documentation across variable names or labels, question text when present, and value labels. Each returned variable links back to its source study. ICPSR also states explicitly that not every catalog study has variable-level documentation in SSVD, so failure to obtain an SSVD hit cannot establish that a variable is absent.

Official source: https://www.icpsr.umich.edu/sites/icpsr/find-data/ssvd

For broader discovery, ICPSR recommends the **main data search**, which it states searches all documentation available for its studies, including variable descriptions. ICPSR separately documents a variable-search function on an individual study homepage that can expose variable name, label/question text, type and dataset when such structured documentation is available.

Official sources:
- https://www.icpsr.umich.edu/sites/icpsr/posts/shared/how-can-i-find-data-that-include-my-desired-variables
- https://www.icpsr.umich.edu/sites/icpsr/teaching-learning/find-use-data

This does not contradict the SOMAR catalog-search limitation. The SOMAR collection/catalog surface and ICPSR main search are different search scopes; ICPSR also notes that thematic-collection searches do not search across the full ICPSR collection.

The legacy concrete public ICPSR variable-search endpoint is `https://www.icpsr.umich.edu/web/ICPSR/search/variables`. The current automated audit surface can retrieve the base endpoint but does not execute its parameterized query URLs. A separate probe of the modern route `https://www.icpsr.umich.edu/sites/search/variables` on 2026-09-25 likewise could not execute parameterized searches for `potential audience` or `audience size`, and exact external searches did not recover target-specific variable pages for 300450 or 300470. By contrast, the study-search surface continues to expose only the catalog-level summaries for those targets. These failures are retrieval/indexing limitations, **not** valid evidence that the target variables are absent.

ICPSR's current dataset-finding guide also instructs researchers that when the Variables tab does not expose variables, the corresponding information should be obtained from the codebook under Data & Documentation. Parameterized variable-search queries and the Variables tab are therefore discovery conveniences, not substitutes for the release documentation required by this gate.

Official additional source: https://www.icpsr.umich.edu/sites/icpsr/teaching-learning/build-your-data-skills/how-to-find-a-dataset

In the current audit, these indexed-search routes did **not** yield a verifiable variable-level result for ICPSR 300450 or 300470 through the available automated surface. They are therefore recorded only as a **public discovery fallback**. A future search hit would still need current-release identity and exact release semantics before it could satisfy the gate. This discovery route **does not pass the variable-dictionary gate** and does not authorize calculation.

### Public Data facet versus restricted-use status

The current ICPSR SOMAR search page exposes a **Public Data** availability facet while the same current catalog results for ICPSR 300450 and 300470 explicitly state that the data are restricted and require an application.

Official current sources:
- https://www.icpsr.umich.edu/sites/search/studies?fq=OWNER%3Asomar&rows=50&sort=score+desc&start=0
- https://icpsr.github.io/metadata/icpsr_metadata_api/

ICPSR's Metadata Export API documentation resolves the apparent tension: ICPSR tracks **data availability** and **restriction type** as separate systems-level metadata concepts. Its documented examples include collections available to the general public that nevertheless carry restricted-use requirements.

Therefore the search facet must not be interpreted as evidence that the restricted analytic data files are openly downloadable. It also does not establish that the public codebook/data-dictionary files for 300450 or 300470 have been inspected. File-level documentation access, current collection identity, and exact dictionary contents remain separate gates.

### Manual browser retrieval path

ICPSR documents an explicit browser route for recovering variable documentation when a Variables tab or Explore Data surface is unavailable. From the current study homepage, open **Data & Documentation**, locate the relevant dataset, open the **Download** dropdown next to that dataset, and select **Codebook** or **ICPSR Codebook**. ICPSR separately advises researchers considering restricted data to inspect the codebook from the Data & Documentation tab before deciding whether restricted access is needed.

Official sources:
- https://www.icpsr.umich.edu/sites/icpsr/teaching-learning/teach-with-data/adopt-a-dataset-classroom-edition
- https://www.icpsr.umich.edu/sites/icpsr/teaching-learning/teach-with-data/navigating-restricted-data/how-do-i-know
- https://www.icpsr.umich.edu/sites/somar/research-lifecycle

For F1a, the documented manual sequence is therefore:

`current study page -> Data & Documentation -> relevant dataset -> Download dropdown -> Codebook / ICPSR Codebook -> inspect variables -> record collection version and documentation-file identity`.

This is now the preferred noninferential fallback when the automated/indexed surfaces do not expose the file listing. A controlled 2026-09-25 search exhaustively retried target-specific indexed discovery for `300450` and `300470` using combinations of **Data & Documentation**, **Codebook**, **ICPSR Codebook**, **data dictionary** and **download**. Those searches re-exposed the catalog descriptions but did not recover a target-specific documentation-file URL or dataset-file listing. Direct study-page retrieval remains shell-only through the audited surface.

That result is deliberately narrower than saying the manual route failed. The documented `Data & Documentation -> dataset -> Download -> Codebook / ICPSR Codebook` sequence requires interaction with the dynamic study interface and has **not** been executed to completion in this audit. The automated/indexed route is therefore classified as exhausted for the available audited tooling, while the manual interactive route remains required and unexhausted. The SOMAR Help draft consequently remains `READY_NOT_SENT`: its manual-route-first precondition is still unsatisfied.

A separate direct-route control provides one further constraint. ICPSR currently exposes content-bearing dataset pages on other collections with the route shape `/sites/<collection>/view/studies/<study>/datasets/<dataset_number>`; for example, NaNDA study 38580 dataset 1 exposes a `Documentation files` section with Codebook and Documentation downloads. Controlled probes of the analogous SOMAR candidate routes were then expanded noninferentially across `datasets/1` through `datasets/5` for both 300450 and 300470. None of the ten candidate URLs yielded content through the audited web surface, and the earlier exact searches did not index the target candidate dataset routes. This does **not** establish that either target lacks a dataset page, that the dataset number lies outside 1–5, or that any probed number is intrinsically invalid. The result only exhausts this small direct-route discovery range for the available audited surface. The target dataset number remains unverified and must be obtained from the actual Data & Documentation interface rather than inferred from the control study or from failed URL probes.

This route does **not** pass the variable-dictionary gate by itself. The current 300450 and 300470 dataset-file listings and exact dictionary contents still have to be recovered, inspected, and tied to their current collection versions before any physical field can be frozen or any ratio calculated.

### Manual retrieval evidence protocol

The remaining browser step is now frozen as a reproducible evidence-capture protocol rather than an informal navigation instruction. ICPSR guidance says the codebook is accessed from the **Data & Documentation** tab by opening the arrow/dropdown next to the dataset, while SOMAR states that codebooks and documentation for restricted-use, Controlled Download and VDE datasets are publicly downloadable before an application is submitted.

For **each** target study, the manual retrieval record must capture:

- canonical current study page and study number;
- current collection version and version-specific DOI as displayed by ICPSR;
- Data & Documentation dataset label;
- documentation artifact title, type and direct/canonical URL;
- enough file identity to distinguish the retrieved artifact from legacy SOMAR copies;
- retrieval date and the evidence source used to bind the artifact to the current collection.

For the field-level gate, the retrieved documentation must then expose or unambiguously define:

- the physical URL/pairing key or keys;
- the physical post-owner/type key if present;
- the physical **potential audience** count field for 300450;
- the physical **audience size** count field for 300470;
- aggregation and deduplication semantics for those count fields;
- disclosure/suppression rules;
- row-inclusion/eligibility rules;
- missing-value and absent-row semantics;
- whether zero exposure is represented as a row with zero, an absent row, another encoding, or is undocumented;
- any explicit current-release relationship establishing that numerator and denominator refer to a compatible eligible inventory.

A label match such as “potential audience size” or “audience size” is insufficient by itself. A legacy file with a matching title is also insufficient without current-release linkage. The gate remains negative if any required item needed for safe pairing is absent, ambiguous, or only inferable.

Passing this protocol does not itself authorize empirical promotion. It only supplies the evidence needed to decide whether the existing r_view = exposed_audience / potential_audience candidate can be mapped to current physical release fields under compatible row-universe, counting and disclosure semantics.

#
## Scope correction: deleted-Page potential-audience rule

A legacy rule excluding potential exposures through Page posts deleted before pseudonymization was recovered in indexed codebook text, but the audited snippets do **not** establish that this rule belongs to the target `potential_exposure_facebook_posts_with_civic_news_urls` section. The recovered wording is associated with other potential-audience domain/derived surfaces.

Accordingly, this rule is **not** used as evidence of a target-specific 300450 denominator filter and is not used to strengthen `table_specific_additional_filter_compatibility`. Target-specific filter compatibility remains unresolved for the independent reasons already retained in this audit.

Status:

`NON_TARGET_SCOPE_RULE_NOT_IMPORTED`

## V3 URL row-universe asymmetry

The same v3 codebook establishes that the Potential-Exposure and Exposure URL tables share several inclusion boundaries:

- level: URL;
- population: U.S. adult monthly active users;
- period: 2020-09-01 through 2021-02-01;
- civic/news classification by Meta internal classifiers;
- URL shared more than 100 times to Facebook by U.S. users during the study period.

But the final inclusion criterion is **not the same**:

- Potential Exposure: URL was **potentially viewed** in Feed because a post containing it was shared by a U.S.-based connection;
- Exposure: URL was actually **viewed** by U.S. users in Feed.

Therefore the two physical row universes are not established as identical. In particular, a URL can be conceptually eligible for the Potential table while lacking an Exposure row if no qualifying view occurred. The audit must not interpret absence from Exposure as `0` exposed users, nor silently remove such URLs with an inner join, until the target release documentation defines absent-row and zero semantics.

This is distinct from the paper-level statement that each analyzed URL has potential/exposed/engaged audience measures: the publication's analysis universe does not prove that the separately released current files preserve identical rows after filtering, suppression or release processing.

Status:

`COMMON_BASE_FILTERS_VERIFIED / ROW_UNIVERSE_IDENTITY_UNVERIFIED / NAIVE_INNER_JOIN_FORBIDDEN`

## Science inventory funnel vs release-field scope

The Science analysis supplies an important qualification to the candidate `r_view` interpretation. In the published analysis:

- political-news posts from **friends, Pages and Groups** form the content `inventory`;
- that inventory is determined by the user's underlying network: friending individuals, following Pages and joining Groups;
- Facebook's algorithm ranks content **from that inventory** and presents a selection in Feed;
- actual exposure is therefore a downstream subset of potential exposure **within that analysis inventory**.

This establishes a genuine conceptual funnel for the paper. It does **not** yet establish the same subset relation for the raw public release fields:

- Potential Exposure explicitly requires that the URL could have been viewed because a post containing it was shared by a U.S.-based connection;
- Exposure requires that the URL was viewed in Feed, but its standalone public description does not explicitly repeat the same connection-inventory restriction;
- the project Glossary defines Facebook Feed broadly enough to include suggested posts as well as connected users/Pages/Groups.

Therefore the paper's nested analysis universe cannot be silently transferred to all raw 300450/300470 rows. Before a release-field `exposed_audience / potential_audience` ratio can be interpreted as a fraction or view rate, current documentation or an explicit analysis rule must show that numerator and denominator refer to the **same inventory**.

Candidate status:

`CONCEPTUALLY_CONDITIONAL_ON_SHARED_INVENTORY / RELEASE_SHARED_INVENTORY_UNVERIFIED / NUMERICALLY_BLOCKED`

## Science unique-audience vs release-metric boundary

The Science paper defines the audience funnel at the level of **unique-user sets**:

- potential audience of a URL: the set of unique users who could have been exposed to that content;
- exposed audience: the set of unique users who actually saw a post containing that URL in Feed;
- the schematic ordering is inventory → algorithmic curation → Feed, so the conceptual exposed audience follows potential exposure.

This supports the **conceptual** ratio:

`exposed_unique_users / potential_unique_users`

but it does **not** yet authorize substituting a released `audience size` column into that ratio. Legacy codebook disclosure text contains audience-counting rules that can count the same user more than once across posts or days, and for the target URL datasets those disclosure rules are themselves scope-conflicted. Therefore the release metric's deduplication horizon and equivalence to the paper's unique-user set cardinality remain unverified.

Until the current target Data Dictionary rows establish the aggregation/deduplication semantics, `r_view` cannot be interpreted numerically as a probability or fraction of potential users even if columns labelled `audience size` are located.

Status:

`CONCEPTUAL_UNIQUE_USER_FUNNEL_VERIFIED / RELEASE_METRIC_EQUIVALENCE_UNVERIFIED`

## Science analysis-weighting boundary

The Science paper defines a segregation index in which `C_n` and `L_n` are the counts of conservatives and liberals exposed to a domain or URL `n`, while `v_n` is described as the **total number of unique views** for that domain or URL. In that equation, `v_n` functions as an analysis-specific visit/view weighting quantity.

The same paper separately defines the **exposed audience** of a URL as the set of unique users who saw a post containing that URL in Feed.

Those two published descriptions are not enough to map `v_n` to a physical release column. The paper does not establish that `v_n` is the current released `exposed_audience_users` field, `content_views`, or any other specific release variable.

Therefore `v_n` cannot be used as the numerator or denominator of `r_view`, cannot resolve the current 300470 column identity, and cannot substitute for the official variable dictionary. A current-release dictionary mapping remains required.

### Science paper-to-dataset mapping

The legacy US2020 project codebook contains an appendix that explicitly maps publications to the study tables used by each paper. For *Asymmetric ideological segregation in exposure to political news on Facebook* (Science, DOI `10.1126/science.ade7138`), that mapping includes the URL-level Potential Exposure, Exposure and Engagement datasets used by this audit, along with the related domain, coexposure and segregation tables.

This is direct provenance support for selecting the Potential-Exposure-URL and Exposure-URL surfaces as the conceptual numerator/denominator family. It does not establish current 2026 release linkage, exact physical columns, release-specific privacy semantics or numerical compatibility.

The paper additionally states that **for each URL** it has measures of the potential, exposed and engaged audience. This strengthens same-URL conceptual pairing for the published analysis. It still does not establish that the separate current 300450/300470 release files preserve identical URL rows after filtering, suppression or missingness handling, nor that their physical URL keys are directly joinable. Those remain release-specific dictionary/file gates.

The paper itself defines the funnel as potential exposure -> actual exposure -> engagement and defines the potential and exposed URL audiences as sets of unique users, but the current-release physical fields still require official dictionary inspection.

### Replication-code access is a separate gate

The publication and current author-facing research pages distinguish the study's replication code/data access from its public documentation surface.

The Science data-availability statement says that deidentified data and analysis code from the study are archived in SOMAR for eligible university IRB-approved research or validation, with ICPSR vetting applications. The current author research page correspondingly directs readers to **apply for replication code and data** rather than offering a public code repository. ICPSR's release announcement likewise states that the U.S. 2020 datasets are accessed through SOMAR's Virtual Data Enclave after application.

This does not make restricted code access a prerequisite for the present documentation gate. SOMAR's current guidance separately states that codebooks and documentation for restricted-use datasets are publicly downloadable before application.

A separate published U.S. 2020 FIES article gives a concrete controlled-code citation:

- *Meta Platforms, Inc. Replication Code for U.S. 2020 Facebook and Instagram Election Study*;
- distributor: Inter-university Consortium for Political and Social Research;
- distribution date: 2023-07-27;
- DOI: `10.3886/spb3-g558`;
- archived at SOMAR/ICPSR and cited as available through the VDE.

This DOI is useful as a provenance and future controlled-retrieval locator. It does not by itself identify the physical columns required by the F1a gate. The coauthor research page's Replication link for the Science paper points to the general US2020 SOMAR collection search and the same collection link is reused across multiple US2020 publications; it therefore does not resolve an article-specific public code package for `ade7138`. The package contents were not inspected in this audit, and the audit has not independently established that this general FIES replication-code package contains the exact Science `ade7138` analysis code or the current 300450/300470 release-field mappings.

Accordingly:

- public current-release Codebook / Data Dictionary retrieval remains the preferred first route;
- absence of a public GitHub/OSF/Zenodo replication-code repository is not evidence that public documentation is absent;
- controlled replication code is only a fallback if public documentation cannot resolve a required release-specific field or disclosure rule;
- even controlled code cannot substitute for explicit current-release/version linkage before physical fields are frozen.

### Two-stage replication-code scope boundary

The official U.S. 2020 Facebook & Instagram Election Study FAQ distinguishes **two code stages** for platform-usage research.

First, Meta employees wrote and executed the code that generated the research-specific platform-usage tables from Meta's internal data, because the academic team could not access the internal logs. The academic team reviewed this table-generation code as part of the production pipeline.

Second, preprocessing and analysis operated on the resulting research-specific tables in Meta's Researcher Platform. At this stage the academic team could write, execute and modify code. The FAQ also states that academics had access to aggregate political-news domain and URL data for all U.S. adult Facebook users.

The same FAQ confirms that replication data and code are archived at SOMAR/ICPSR and made available through the VDE, including platform-wide data in aggregated form as shared with the academic team.

This public statement does **not** establish that the archived package contains the complete upstream table-generation layer, the current ICPSR 300450/300470 release schema, or the exact current physical fields. Consequently, obtaining controlled replication code cannot be assumed prospectively to reveal the upstream transformations or to substitute automatically for the current-release Codebook/Data Dictionary.

Any future VDE/code route must therefore be inspected directly and tied to the target collection version before it can resolve the physical-column gate.

Official project source:
- https://medium.com/@2020_election_research_project/us-2020-facebook-instagram-election-study-frequently-asked-questions-faq-266d30cbe95b

### Author-facing replication navigation locators

Current coauthor research pages expose more than one legacy SOMAR navigation target for replication access.

On Hunt Allcott's research page, **Apply for replication code and data** for the Science paper points to legacy SOMAR **record 43**. The same link target is reused on that page for multiple U.S. 2020 Facebook and Instagram Election Study publications. The live legacy record-43 URL now redirects to the current SOMAR home page, and this audit did not recover a record-43 metadata payload or file listing.

Jennifer Pan's current research page uses a replication link to the general US2020 SOMAR collection search, also reused across multiple US2020 publications.

These different legacy targets therefore behave as replication-access/navigation locators, not as evidence of distinct article-specific public packages. In particular, the record-43 link does not establish that record 43 is the DOI package `10.3886/spb3-g558`, and no indexed metadata crosswalk was recovered that equates those identifiers.

The independently published replication-code DOI remains a valid controlled-code provenance locator, but its contents were not inspected and its exact scope to Science `ade7138` remains unverified. Neither author-facing navigation link satisfies the exact 300450/300470 variable-dictionary gate.

### Official SOMAR Help escalation

SOMAR's current Research Lifecycle guidance explicitly tells researchers who cannot find the data they are looking for to contact the SOMAR team for help locating the relevant resource. The current application guide lists `somar-help@umich.edu` for questions about SOMAR datasets and VDE access.

For the F1a gate, this creates a procedural step **before any VDE application**:

`public study page / Data & Documentation -> manual Codebook route -> indexed variable/documentation discovery -> SOMAR Help request to locate the public current-release documentation -> VDE documentation only if the required release-specific item is genuinely unavailable publicly`.

The support request should ask only for the public current-release codebook/data dictionary or its canonical location for ICPSR 300450 and 300470. It does not require a restricted-data application merely to ask where public documentation is located.

A reply from support would still need to identify a version-bearing official artifact before the column gate can pass. The act of contacting support is not evidence of field identity, privacy semantics or numerical compatibility.

### Derived segregation-table aggregation boundary

The legacy codebook exposes an important table-specific rule for the **daily ideological segregation** derived surface. In that table, the disclosure text states that exposed-audience metrics report a **sum of views**, while potential and engaged audience metrics are constructed by adding daily audience counts for posts associated with a URL or domain across the study period. The same user can therefore contribute more than once across different posts or days.

Legacy source: https://socialmediaarchive.org/record/61/files/US2020_FB%26IG_Elections_External_Codebook_v2.pdf

This is not the same release surface as ICPSR 300450 or 300470. The current ICPSR catalog describes 300450 with **potential audience size**, while 300470 separately includes **content views** and **audience size**.

Current catalog source: https://www.icpsr.umich.edu/sites/search/studies?fq=OWNER%3Asomar&rows=50&sort=score+desc&start=0

Therefore the derived ideological-segregation aggregation rules must not be imported into 300450 or 300470. In particular, the derived `sum of views` quantity is not treated as current 300470 `audience size`, and neither that quantity nor the derived potential-audience aggregation can be used as the `r_view` numerator/denominator without exact target dictionary mapping.

Status:

`DERIVED_TABLE_AGGREGATION_RULES_SCOPE_LOCKED_TO_DERIVED_SURFACE`

## Legacy documentation attachment scope

The indexed MARC export for legacy SOMAR **record 34** directly proves that the following public documentation artifacts were attached to that record, with the retained UUID/byte-size locators:

- `data_dictionary_political_segregation_paper.xlsx`;
- `variables_political_segregation_paper.csv`;
- `US2020_FB&IG_Elections_External_Codebook.pdf`;
- `US2020_Glossary.xlsx`.

Legacy SOMAR search results independently mark both target records **32** (Exposure URL) and **36** (Potential Exposure URL) as **Multiple Files** and associate each with `US2020_FB&IG_Elections_External_Codebook`. This supports target-specific multi-file documentation availability.

The audited public search still did **not** recover equivalent record-level manifests for records 32/36 proving that the same dictionary/CSV UUIDs from record 34 were attached there. That nonrecovery is not evidence that those records lacked such files. It means only that the record-34 manifest cannot be used as direct **file-identity** proof for records 32/36.

Therefore record-34 UUIDs remain useful retrieval/provenance locators, but they cannot establish legacy target-record file identity and cannot establish current ICPSR 300450/300470 attachment or byte identity.

Status:

`TARGET_RECORDS_MULTIPLE_FILES_VERIFIED / RECORD_34_EXACT_UUID_ATTACHMENT_VERIFIED / RECORD_32_36_SAME_UUID_ATTACHMENT_UNVERIFIED / CURRENT_LINKAGE_UNVERIFIED`

## Legacy source live-retrieval state

A current link-health check on **2026-09-25** found that the tested legacy `socialmediaarchive.org` artifact URLs no longer serve the historical record/file surfaces through the audited public web path. The tested record-34 MARC export, v2/v3 external-codebook URLs, and indexed Glossary spreadsheet-view URL redirect to the current ICPSR SOMAR home page.

This redirect behavior now has direct official context. SOMAR's **Winter 2026 newsletter** states that the SOMAR website and archive data **transitioned to the ICPSR platform**, with resources, studies and features accessed through ICPSR's unified interface. The observed redirect of old `socialmediaarchive.org` URLs is therefore consistent with an announced platform transition rather than treated merely as unexplained link failure.

Official transition source: https://www.icpsr.umich.edu/sites/somar/somar-newsletter-archive/somar-newsletter-winter-2026

This changes the **retrieval status**, not the historical evidence classification. The legacy URLs remain useful as historical/indexed provenance locators for metadata and content recovered earlier in the audit, but they must no longer be described or relied upon as currently live artifact-download endpoints. The redirects do **not** invalidate previously recovered historical metadata/codebook evidence, do not establish anything about current 300450/300470 file identity, and do not authorize any numerical pairing.

Current redirect target:

`https://www.icpsr.umich.edu/sites/somar/home`

Status:

`LEGACY_INDEXED_PROVENANCE_RETAINED / ORIGINAL_URLS_REDIRECT / LIVE_ARTIFACT_RETRIEVAL_UNAVAILABLE_ON_AUDITED_SURFACE / SCIENTIFIC_GATE_UNCHANGED`

## US2020 Glossary audience/view semantic distinction

An indexed spreadsheet-view of the public **US2020 Glossary** provides an independent project-level semantic distinction:

- **Audience:** the number of users or participants who viewed a piece of organic content at least once;
- **Content views:** the number of times content appeared on the participant/user screen during the study period.
- **Potential audience:** a group of adult U.S. monthly active users that can potentially see a piece of content because it was shared by one of their connections.

This confirms that audience-user counts and view-event counts are different estimands and independently supports the connection-inventory meaning of the potential-audience denominator. Therefore the current 300470 catalog phrase `content views and audience size` cannot be collapsed into a single quantity, `content views` is not an admissible numerator for `r_view`, and the Glossary still does not identify the physical 300450 denominator field.

The glossary does **not** identify the exact released audience column, the URL/post-owner key, the aggregation/deduplication horizon, missing/suppression rules, or current 2026 collection linkage. Those remain target Data Dictionary questions.

Status:

`AUDIENCE_USER_COUNT_VS_VIEW_EVENT_COUNT_VERIFIED / TARGET_RELEASE_FIELD_MAPPING_UNVERIFIED`

Source: indexed US2020 Glossary spreadsheet viewer.

## Data-dictionary semantic authority

The US2020 project codebook explicitly defines a **separate data dictionary for each dataset**. For every variable, that dictionary records the **variable name, description, type, group, map keys, aggregation methods and disclosures**. The codebook therefore identifies the data dictionary—not narrative prose labels—as the field-level authority for the exact information this F1a gate needs.

This sharpens the gate without changing its outcome: exact numerator/denominator field identity, key structure, aggregation semantics and disclosure controls must be read from the target 300450/300470 dictionary rows. Project-codebook prose can guide discovery and conceptual interpretation, but it cannot substitute for those rows. The codebook statement does not identify or inspect the current 2026 dictionary files, so numerical pairing remains unauthorized.

Source: https://socialmediaarchive.org/record/70/files/US2020_FB%26IG_Elections_External_Codebook_v3.pdf

Status:

`FIELD_LEVEL_DOCUMENTATION_AUTHORITY_CONFIRMED / TARGET_DICTIONARY_ROWS_UNINSPECTED`

## Access result

The old direct SOMAR file routes now migrate/redirect into the current ICPSR/SOMAR environment. The current automated/indexable web surface exposes study-level descriptions but does not expose the exact variable-dictionary rows needed for the gate.

Because current SOMAR policy says those documentation files are publicly downloadable, this is treated as a **tooling/retrieval limitation of this audit**, not as evidence that documentation access itself requires VDE or restricted-data approval. Current SOMAR guidance also states that the dataset search matches study metadata but does **not** search inside data or documentation files. Failure to recover a variable name through catalog search therefore cannot be treated as evidence that the variable is absent from the public data dictionary.

The material actually inspected in this audit therefore still does **not** establish:

- the exact released potential-audience column name;
- the exact released exposed-audience column name;
- count transformation/disclosure-control semantics;
- missing/suppressed/zero encoding;
- URL key/canonicalization fields;
- release-version row linkage.

No field name is inferred from prose labels such as “potential audience size” or “audience size.”

## Privacy/disclosure-control result

The previous audit already established two public privacy facts for this study surface:

- analysis is aggregate rather than individual-level;
- URL inclusion is limited to URLs shared more than 100 times by U.S.-based users.

This audit finds no authoritative public text on the currently indexable study pages that resolves whether the released audience values additionally use suppression, minimum-cell rules, perturbation/noise, rounding, estimated counts, or other disclosure controls.

General Meta statements about differential privacy in other Data for Good releases are **not** imported into FIES as evidence of a specific transformation. Dataset-specific rules are required.

Thus the privacy state remains:

`AGGREGATE_ONLY + URL_SHARE_THRESHOLD_GT_100 + ADDITIONAL_RELEASE_CONTROLS_UNVERIFIED`.

## Column-identity gate decision

The exact column gate does **not** pass.

Current verdict:

`DOCUMENTATION_ARTIFACTS_LOCATED / COLUMN_CONTENTS_NOT_VERIFIED / NUMERICAL_PAIRING_NOT_AUTHORIZED`.

The candidate quantity remains conceptually **conditional on a verified shared inventory**:

`r_view(URL, owner_type) = exposed_audience_users / potential_audience_users`

The Science paper verifies the nested funnel within its analysis inventory, but the current 300450/300470 release fields have not yet been proven to implement that same inventory boundary.

but neither numerator nor denominator may be mapped to a physical release column until the official variable dictionary contents are inspected.

### Support escalation package

The automated/indexed public-retrieval routes have been exercised without recovering the current 300470 version-specific DOI/version or the target-specific current data-dictionary contents. The documented manual ICPSR browser route — `Data & Documentation -> dataset -> Download -> Codebook / ICPSR Codebook` — has **not** been executed to completion in this audit and must not be described as exhausted. SOMAR's Research Lifecycle states that codebooks and documentation for restricted-use and VDE datasets are publicly downloadable from the catalog, and ICPSR guidance directs researchers to review those codebooks before applying for restricted data.

The next non-restricted operational step is therefore the **manual public Data & Documentation / Codebook retrieval** for ICPSR 300450 and 300470. A public-documentation locator request to `somar-help@umich.edu` is prepared as the subsequent escalation only if that manual route fails to locate the required current documentation. This is not a request for restricted data or VDE access.

The request scope is limited to:

- the direct current V2 public data-dictionary download or file identity for ICPSR 300450;
- the current collection DOI/version and Version History or citation surface for ICPSR 300470;
- the direct current public data-dictionary or variable-description download/file identity for ICPSR 300470;
- the current public documentation location, if one exists, for row inclusion/eligibility rules, pairing keys and absent-row semantics for each target study;
- the current public documentation location, if one exists, that defines the relationship between the eligible population/inventory in 300450 and the exposed-audience population/inventory in 300470;
- confirmation of the current public-documentation location for both target studies.

The request must explicitly avoid asking SOMAR to calculate `r_view`, infer physical fields, adjudicate whether the releases are scientifically compatible, or treat legacy documentation as current-release documentation. It asks for the location of existing documentation only. A support reply by itself does not pass the gate: before any scientific state change, the reply must provide target-specific official links/identifiers or point to an official current artifact, and that evidence must be archived in the audit. Numerical pairing remains blocked until the actual documentation contents are inspected.

Status: **support draft ready; not sent; send precondition not yet satisfied; manual public-documentation retrieval comes first**.

### Prepared SOMAR Help request — not sent

The public-documentation escalation is operationally reproducible, but it is not yet the next action. The following message is retained as a draft with machine-readable status **`READY_NOT_SENT`**. It has **not** been sent, does not authorize sending, and its send precondition remains false until the manual ICPSR Data & Documentation / Codebook route has been attempted without recovering the required target documentation.

Recipient: `somar-help@umich.edu`

Subject: **Public documentation location for ICPSR 300450 and 300470**

```text
Dear SOMAR team,

I am conducting a reproducibility/provenance audit of two datasets in the U.S. 2020 Facebook and Instagram Election Study and am trying to locate their current public documentation. I am requesting public documentation only; I am not requesting restricted data or Virtual Data Enclave access.

Could you please point me to the current official public documentation for the following studies?

1. ICPSR 300450 — Potential Exposure to Facebook Posts with Civic News URLs
   - the direct public Data Dictionary and/or variable-descriptions download for the current V2 collection;
   - if possible, the current documentation file identity or canonical Data & Documentation link;
   - the current public documentation section, README, codebook, or data-dictionary material that defines row inclusion/eligibility, pairing keys, and the meaning of a URL row being absent from the release, if those rules are documented publicly.

2. ICPSR 300470 — Exposure to Facebook Posts with Civic News URLs
   - ICPSR's current metadata style guide gives the unversioned latest-version reference form as `https://doi.org/10.3886/ICPSR300470`; I am specifically trying to identify the current version number and version-specific DOI, or the current Version History / citation surface that exposes them;
   - the direct public Data Dictionary and/or variable-descriptions download for that current collection;
   - if possible, the current documentation file identity or canonical Data & Documentation link;
   - the current public documentation section, README, codebook, or data-dictionary material that defines row inclusion/eligibility, pairing keys, and the meaning of a URL row being absent from the release, if those rules are documented publicly.

If the current public documentation explicitly describes the relationship between the eligible population/inventory in 300450 and the exposed-audience population/inventory in 300470, could you please point me to that documentation location as well? I am asking only for the location of any existing documentation, not for SOMAR to make an interpretive determination.

If available, I would also appreciate confirmation that the documentation links above correspond to the current releases of these studies (the catalog currently lists them as released/updated on 2026-04-01).

For clarity, I am not asking SOMAR to provide restricted data, grant VDE access, infer variable names, interpret the fields, decide whether the two releases are scientifically compatible, or calculate any research quantity. I only need the canonical current-release public documentation or its official location so that field identity, version linkage, row-universe rules, missing/absent-row semantics, and release semantics can be checked directly.

I have located legacy SOMAR documentation for the same titled study surfaces, but I am deliberately not treating those legacy files as current-release documentation without an explicit current linkage.

Thank you for your help.
```

The request is deliberately narrower than a data-access application. It requests public current-release documentation, version identifiers, and the location of any existing documentation for row-universe/eligibility and absent-row semantics. It does not request restricted data, VDE access, inferred field names, interpretive adjudication of shared-inventory compatibility, or calculation of `r_view`.

A future SOMAR reply does not itself pass the scientific gate. Any returned target-specific official link or identifier must be archived in the audit, the linked current-release artifact must be inspected, and the physical field / privacy / missingness / linkage semantics must still be verified before numerical pairing can be authorized.

## What would satisfy the gate

The gate can pass only with an official, version-identifiable source that exposes the relevant dictionary rows, for example:

1. the public Data & Documentation download for ICPSR 300450 and 300470, with the data-dictionary or variable-description contents inspected and tied to the relevant release version;
2. an official ICPSR variable/documentation endpoint exposing the exact fields and release identity;
3. approved SOMAR/VDE release documentation only if the public documentation is insufficient to resolve a required release-specific field or disclosure rule.

The successful source must establish, prospectively:

- exact potential-audience field;
- exact exposed-audience field;
- owner-type field;
- URL/key field and canonicalization/linkage rule;
- missing/suppressed/zero encoding;
- release count transformation and privacy rules;
- version identity for both 300450 and 300470;
- row inclusion/eligibility and absent-row semantics for both target releases;
- evidence that any release-level `r_view` numerator and denominator refer to the same eligible content/user inventory;
- compatibility of the numerator and denominator release surfaces.

## Current scientific boundary

F1a remains **RECOVERY_TESTED**.

This audit does not authorize:

- an `r_view` calculation;
- an empirical value for `q_transmit`;
- mapping PlatformView to CBD CognitiveExposure;
- runtime parameter activation;
- promotion to `EMPIRICALLY_CONSTRAINED`.

A negative access result is retained rather than substituting guessed field names or a different denominator.
