# F1a SOMAR count-semantics audit

Status: **COUNT_SEMANTICS_PARTIALLY_RESOLVED**

F1a ladder stage remains: **RECOVERY_TESTED**

This audit follows the public-codebook compatibility audit and asks whether the public U.S. 2020 FIES documentation resolves the meaning of the numerator and denominator needed for an aggregate PotentialDelivery→PlatformView realization rate.

It does not calculate a value, estimate `q_transmit`, change runtime behavior, or authorize empirical promotion.

## Public definitions now resolved

The public U.S. 2020 FIES glossary/codebook defines:

### Audience

For this study, **Audience** is the number of users or participants who viewed a piece of organic content at least once.

Therefore audience is a user-count / reached-user construct, not a raw view-event count.

### Content views

**Content views** are the number of times specified content appeared on a participant or user's screen during the study period.

For Facebook, a view is counted when content renders in the visible portion of the web browser or mobile device for more than **250 milliseconds**.

Because this is a count of appearances, repeated appearances can contribute multiple views.

Therefore `content views` must not be used as the numerator of a unique-user realization fraction whose denominator is potential audience.

### Potential audience

**Potential audience** is the group of adult U.S. monthly active users who can potentially see a piece of content because it was shared by one of their connections.

### Exposed audience

**Exposed audience** is defined as users whose Feed a post appeared in.

The González-Bailón et al. analysis further states that, for a URL, the exposed audience is the set of unique users who saw a post containing that URL in their Feed.

### Engaged audience

For the political-news exposure funnel, the engaged audience is the set of unique users who clicked, reacted, liked, reshared, or commented on the post containing the URL.

Engagement is therefore downstream from view/exposure.

## Post-owner aggregation semantics now resolved

The v3 codebook's aggregation section defines post-owner type:

- `All`: posts from users, Pages and groups;
- `User`: posts from users to their profile;
- `Page`: posts from Pages;
- `Group`: posts from users to groups.

Thus `owner_type=all` is explicitly the combined owner category across those three source classes.

This resolves the earlier ambiguity about whether `all` was an unrelated category.

It does not prove that its numeric values are a simple arithmetic sum of the other rows, because audience counts may overlap across owner types. The `all` row should therefore be treated as its own combined audience aggregation unless the data dictionary states otherwise.

## Funnel subset semantics

The Science paper describes the study's information funnel as:

`Inventory / Potential audience -> Algorithmic curation -> Feed / Exposed audience -> Social curation -> Engaged audience`.

It states that the inventory is determined by users' underlying network choices, including friends, Pages and Groups, and that Facebook's algorithm ranks content from that inventory and presents a selection in users' Feeds.

This supports the intended study-level interpretation that exposed audience is a realization after ranking from the potential inventory.

Accordingly, an aggregate audience realization fraction is conceptually defensible **within this study's operationalization**, subject to row/variable compatibility and privacy/missingness checks.

This does not establish a general platform law and does not imply that every possible Facebook exposure mechanism in every period is connection-mediated.

## Candidate component quantity refined

The candidate quantity should use unique-user audience counts:

`r_view(URL, owner_type) = exposed_audience_users / potential_audience_users`

and **not**:

`content_views / potential_audience_users`.

Reason:

- numerator and denominator of `r_view` should both represent users;
- `content_views` counts screen appearances and can reflect repeated appearances;
- using views over potential users could exceed one merely because users viewed the same content repeatedly, changing the estimand.

If numerically valid, `r_view` would estimate an aggregate curation/view realization fraction for a URL and owner category during the study period.

It remains distinct from the synthetic dyadic:

`q_transmit = P(CBD ExposureEvent | realised Share-edge opportunity)`.

## What remains unresolved before calculation

The public material audited here still does not expose enough detail to authorize numerical pairing.

Required unresolved items are now narrower:

1. exact data-dictionary column names for potential audience and exposed audience in the relevant URL tables;
2. whether those columns are raw unique-user counts, privacy-protected counts, transformed counts, or estimates;
3. privacy suppression, minimum-cell, perturbation, rounding or other disclosure-control rules;
4. missing-value encoding and distinction between missing/suppressed values and structural zero;
5. whether URLs absent from a table mean zero audience or exclusion from that table's release surface;
6. exact URL canonicalization/key identity across potential, exposure and engagement tables;
7. whether the `all` audience row is computed as a deduplicated union across owner types, as expected for an audience construct, and how overlap is handled;
8. whether the released potential/exposed audience variables apply any additional table-specific filters not visible in the high-level codebook;
9. whether any weighting or estimation procedure is used for released audience counts;
10. the exact linkage/versioning rule needed to ensure that rows from 300450 and 300470 refer to the same URL representation and compatible release version.

## Current gate decision

The earlier blocker:

`AUDIENCE_AND_REPEAT_VIEW_SEMANTICS_UNKNOWN`

is now **resolved**.

The next blocker is:

`COLUMN_IDENTITY_AND_PRIVACY_RULES_UNRESOLVED`.

Numerical `r_view` calculation remains unauthorized until those remaining items are prospectively frozen in an empirical-analysis contract.

## Scientific boundary

Even after a valid aggregate `r_view` is obtained:

- it constrains the PotentialDelivery→PlatformView component;
- it is population/platform/time specific to the audited FIES surface;
- it does not directly identify sender→recipient transmission;
- it does not map PlatformView automatically to CBD `ExposureEvent`;
- it does not activate `q_transmit`;
- it does not by itself promote F1a to `EMPIRICALLY_CONSTRAINED`.

F1a therefore remains **RECOVERY_TESTED**.
