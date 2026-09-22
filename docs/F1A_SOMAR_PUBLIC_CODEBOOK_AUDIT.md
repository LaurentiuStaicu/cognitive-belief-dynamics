# F1a SOMAR public-codebook compatibility audit

Status: **PUBLIC_CODEBOOK_COMPATIBILITY_AUDIT**

F1a ladder stage remains: **RECOVERY_TESTED**

This audit tests whether the public U.S. 2020 Facebook and Instagram Election Study documentation is sufficient to justify a prospective pairing design between potential exposure, actual platform views, and engagement.

It does **not** calculate any empirical ratio, estimate `q_transmit`, or authorize F1a promotion.

## Sources audited

Primary public documentation:

- SOMAR / ICPSR 300450 — Potential Exposure to Facebook Posts with Civic News URLs;
- SOMAR / ICPSR 300470 — Exposure to Facebook Posts with Civic News URLs;
- SOMAR / ICPSR 300475 — Engagement with Facebook Posts with Civic News URLs;
- U.S. 2020 Facebook and Instagram Election Study External Codebook, including v3;
- González-Bailón et al. (2023), *Science*, DOI 10.1126/science.ade7138.

The public archive also exposes documentation artifacts such as the project codebook, data dictionary and variable-description files for the political-segregation paper. The current audit uses only definitions that are actually visible in the publicly indexed material.

## Confirmed common design surface

The three URL-level datasets share the following publicly documented structure:

### Unit

Rows correspond to **URLs**.

The codebook states that each URL is represented by four rows corresponding to post-owner type:

- user;
- Page;
- group;
- all.

This owner-type dimension is therefore a required pairing key, not a cosmetic field.

### Population

The codebook describes aggregated Facebook activity data for adult U.S. monthly active users.

The active-user scope is described as users active between 2020-09-01 and 2021-02-01 whose predicted home country is the United States and whose stated age is 18 years or older.

### Time period

All three audited URL-level tables use:

`2020-09-01 -> 2021-02-01`.

### Content eligibility

Across the codebook descriptions, relevant URLs are:

- classified as civic / political-social-issue related and news by Meta classifiers;
- shared more than 100 times to Facebook by U.S. users during the study period.

Actual-exposure and engagement tables additionally condition on observed Feed views / engagement, while potential exposure conditions on possible Feed exposure through sharing by a connection.

## Confirmed construct semantics

### Potential exposure / potential audience

The potential-exposure table represents URLs in posts that users **could have viewed in their Feed because a post containing the URL was shared by one of their connections**.

This is a platform opportunity / candidate-availability construct.

It is not evidence that the user actually viewed the post.

### Actual exposure / platform view

The exposure table represents URLs that users **viewed in Facebook posts in their Feed**.

The associated paper describes the analytical distinction as the information users actually saw after algorithmic curation, compared with the inventory they could potentially have seen.

This is a platform-view construct.

It is not automatically equivalent to CBD cognitive `ExposureEvent`.

### Engagement

The engagement table measures users who engaged with posts containing civic-news URLs and the volume of their engagement. Its overview refers to posts with URLs users viewed in their Feed.

The associated Science paper treats engagement as a stage downstream from actual exposure.

This is a downstream action construct, not an exposure measure.

## Pairing result

The public documentation is sufficient to conclude that a prospective URL×owner-type pairing design is **structurally plausible**:

`PotentialExposure(URL, owner_type)`
`-> ActualView(URL, owner_type)`
`-> Engagement(URL, owner_type)`

because the public codebook aligns:

- unit level;
- study period;
- broad active-user population;
- owner-type stratification;
- broad content-classification and sharing threshold.

However, this is **not yet sufficient for numerical pairing**.

## Unresolved codebook requirements before any ratio

The publicly indexed material available in this audit does not yet establish all of the following with sufficient precision:

1. the exact variable names carrying potential audience, actual audience/viewers, total views, engaged audience and engagement volume;
2. whether each audience field counts unique users, deduplicated users, estimated users, or another population metric;
3. whether `content views` is an event count that may include repeated views by the same user;
4. whether repeated views are retained, capped, deduplicated or otherwise transformed;
5. whether the potential-audience and actual-exposure tables use perfectly identical population filters after all internal eligibility rules;
6. whether the same URL canonicalization / normalization key is used identically across potential, exposure and engagement tables;
7. whether all four owner-type rows are directly pairable or whether `all` is independently recomputed rather than a simple union/sum;
8. suppression, thresholding, privacy filtering, perturbation, rounding or minimum-cell rules applied to audience and view fields;
9. missingness conventions and whether suppressed values are distinguishable from structural zero;
10. whether URLs absent from one table should be treated as zero exposure/engagement or as outside that table's inclusion surface;
11. whether sampling, weighting or estimated-count procedures are used for any audience fields;
12. whether the public data dictionary provides stronger definitions than the codebook snippets currently indexable.

Until these questions are resolved, no ratio may be treated as empirically defined.

## Candidate aggregate component ratio

A candidate component quantity remains:

`r_view(URL, owner_type) = actual_view_audience / potential_audience`

This ratio is **not authorized for calculation yet**.

A valid implementation would require, at minimum:

- the numerator and denominator to both represent compatible user counts;
- the same URL key and owner-type row;
- identical population and period definitions;
- a defined policy for missing/suppressed rows;
- explicit evidence that actual audience is a subset-compatible realization of the potential-audience construct.

Even if valid, `r_view` would be an **aggregate PotentialDelivery→PlatformView component constraint**.

It would not be the dyadic synthetic:

`q_transmit = P(CBD ExposureEvent | realised Share-edge opportunity)`.

## Why the Science paper strengthens but does not close the bridge

González-Bailón et al. analyze aggregated data for approximately 208 million U.S. Facebook users and explicitly compare:

1. political news users could potentially have seen in Feed;
2. political news users actually saw after algorithmic curation;
3. political news with which users engaged.

This independently supports the conceptual ordering encoded in the platform-view bridge.

It does not supply a sender→recipient event lineage, nor does it establish that a platform view equals the CBD cognitive exposure construct.

## Current verdict

`PAIRING_DESIGN_PLAUSIBLE / NUMERICAL_PAIRING_NOT_YET_AUTHORIZED`

The public codebook has removed a major uncertainty: potential exposure and actual exposure are not merely vaguely related datasets; they were designed as distinct stages of the same Facebook news-exposure ecosystem with compatible high-level units.

The remaining blocker is now narrower and technical: variable-level count semantics and privacy/aggregation rules.

## Next gate

Before any numerical empirical analysis:

1. obtain the public data dictionary / variable-description definitions for the relevant URL-level tables, or inspect the equivalent current ICPSR documentation if exposed;
2. freeze the exact pairing keys and variable names;
3. write explicit missing/suppression rules;
4. verify subset compatibility of actual audience with potential audience;
5. only then decide prospectively whether `r_view` is calculable.

If those checks fail, retain the negative result and do not substitute a different denominator post hoc.

F1a remains **RECOVERY_TESTED** throughout this audit.
