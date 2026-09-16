# ADR 0006 — OA-4 Search and Universal Inspector semantic contract

Status: Accepted for OA-4A implementation.

## Context

OA-1 created a deterministic Semantic Spine over canonical repository identities. OA-3 established the four-domain information architecture and visual language. OA-4 may now add Search and Universal Inspector, but neither may become a second ontology or flatten scientific status facets.

## Decision

### Search

Search is a lexical retrieval layer over `semantic_index.json`. It searches semantic entities across canonical ID, short name, bilingual preferred labels, alternative labels, semantic metadata and summaries.

Ranking is deterministic and deliberately simple. Exact canonical identity and names outrank prefix/token/summary matches. The internal `retrievalScore` exists only to order lexical results. It is never an evidence-strength, maturity, causal-confidence, importance or intervention-priority score and must not be presented as one.

Empty queries return no results rather than dumping the complete semantic index. Type filtering is allowed but does not mutate or reclassify entities.

### Universal Inspector

The Inspector consumes the same Semantic Spine. It can inspect either an entity or a relation by canonical ID. Entity inspection preserves source mapping, status facets and related relations separated by relation layer. Relation inspection preserves registered-evidence facets, evidence refs, computational formula/code metadata and documentation layer distinctions.

No relation is relabelled as causal merely because it is connected to an entity.

### UI semantics for later OA-4 slices

- Search will use a dedicated HTML `search` landmark with a native `input type=search`.
- OA-4 will initially render results as ordinary semantic HTML rather than implementing a custom ARIA combobox. This avoids unnecessary focus complexity. If autocomplete/arrow-key selection is later added, it must implement the WAI-ARIA combobox pattern and be tested with browser/assistive-technology combinations.
- The desktop Universal Inspector will be a labelled top-level `aside`/complementary landmark because it supports the active main content and remains meaningful separately.
- Compact layout may reposition the inspector, but should not make it modal unless a genuine interaction requirement appears. If it becomes modal later, that requires a separate dialog/focus contract.

## Boundaries

- no new semantic entity family or status vocabulary in OA-4A;
- no fuzzy/ML semantic ranking in OA-4A;
- no external search service or network dependency;
- no mutation of Semantic Spine, scientific registries, equations, evidence, workspace schema or reference outputs;
- no claim that retrieval rank measures scientific importance.

## External basis

- W3C WAI-ARIA APG Combobox Pattern;
- W3C APG Landmark Regions guidance for `search` and `complementary`;
- WCAG 2.2 focus, target-size and reflow requirements inherited from OA-3.
