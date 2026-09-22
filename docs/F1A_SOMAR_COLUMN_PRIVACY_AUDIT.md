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

The current catalog descriptions confirm that 300450 reports URL-level potential-audience information and that 300470 reports URL-level view/audience information for the same broad U.S. adult monthly-active-user study period.

This is sufficient to retain the existing pairing design as plausible, but it is not sufficient to name columns or calculate a ratio.

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

## Access result

The old direct SOMAR file routes now migrate/redirect into the current ICPSR/SOMAR environment. The current indexable study pages expose study-level descriptions but not the exact variable-dictionary rows needed for the gate.

The available web surface in this audit therefore does **not** establish:

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

The candidate quantity remains conceptually:

`r_view(URL, owner_type) = exposed_audience_users / potential_audience_users`

but neither numerator nor denominator may be mapped to a physical release column until the official variable dictionary contents are inspected.

## What would satisfy the gate

The gate can pass only with an official, version-identifiable source that exposes the relevant dictionary rows, for example:

1. a public ICPSR/SOMAR data-dictionary or variable-description download whose contents can be inspected;
2. an official ICPSR variable/documentation endpoint exposing the exact fields;
3. approved SOMAR/VDE access to the release documentation/data package.

The successful source must establish, prospectively:

- exact potential-audience field;
- exact exposed-audience field;
- owner-type field;
- URL/key field and canonicalization/linkage rule;
- missing/suppressed/zero encoding;
- release count transformation and privacy rules;
- version identity for both 300450 and 300470;
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
