# Initial evidence audit — 2026-09-13

This is a bounded bibliographic check of the three currently registered links,
not an exhaustive or systematic literature review, a replication, or calibration.
Bibliography and access scope live in `model/references.json`; bilingual findings
and model-specific limitations live in `model/links.json` and are displayed in the
browser. DOI links identify papers; consulted-source links show the text accessed.

## Separate the levels of support

The earlier `mechanism_evidence_status` field mixed evidence about a phenomenon
with evidence for a particular implementation. All three exact M0 mechanisms are
now marked `CANDIDATE`; the experimental or meta-analytic label is recorded
separately as `phenomenon_evidence_status`. `REFERENCE_CANDIDATE` continues to
identify the chosen functional forms. These labels are not interchangeable.

| Registered link | Reference | Scope of support for M0 |
| --- | --- | --- |
| Exposure → familiarity | Hasher et al. (1977), DOI 10.1016/S0022-5371(77)80012-1 | Indirect background for the latent familiarity state; its update equation is a modelling choice. |
| Familiarity → belief | Dechêne et al. (2010), DOI 10.1177/1088868309352251 | Phenomenon-level synthesis; not an estimate of this implementation’s coefficient. |
| Accuracy salience → sharing | Pennycook et al. (2021), DOI 10.1038/s41586-021-03344-2 | Intervention-level evidence; not direct measurement of latent W. |

The mechanistic classifications above are this project's assessment of the
source-to-model mapping, not classifications supplied by the cited authors.
The graph’s CAUSAL/MODERATING labels describe proposed model relationships;
they should be read together with their candidate status and limitations.

## Reading scope and provenance

The author-hosted abstracts were consulted for Hasher and Pennycook. For Dechêne,
the abstract and selected mechanism sections of an author-affiliated
PDF were consulted. The publisher's Nature page was unavailable in this session;
the MIT-hosted publication abstract supplied the relevant description. These
access limits are recorded per reference and are visible in the interface.

No source files are copied into this repository. Summaries are original and short.
The DOI records and source pages are linked for inspection. This audit does not
claim to have assessed all later replications, moderators or corrections.

## What changed and what did not

Only registries, validation rules, evidence presentation and documentation changed.
No agent update, equation, parameter or saved numerical reference run changed.
The first two links relate to the same broader repetition literature and must not
be counted as two independent validations of the complete causal chain.

The current graph remains incomplete relative to the executable model. Correction,
source learning and the full sharing equation need additional registered links and
separate evidence reviews. A complete ODD description, measurement mapping and
out-of-sample calibration remain future work.
