# F1a platform-view empirical component bridge

Status: **EMPIRICAL_COMPONENT_BRIDGE_DESIGN_ONLY**

F1a ladder stage remains: **RECOVERY_TESTED**

This design refines the post-recovery empirical measurement architecture after the F1a observability audit. It does not estimate an empirical transmission parameter, does not add a runtime event, and does not promote F1a to EMPIRICALLY_CONSTRAINED.

## Why a separate platform-view layer is needed

The current synthetic F1a shortcut maps a realised Share over an eligible directed edge directly to a recipient `ExposureEvent`.

The empirical evidence audit shows that real platform data distinguish multiple stages that the synthetic architecture intentionally collapsed:

`realised Share`
`-> PotentialDelivery / eligible audience`
`-> PlatformView / seen event`
`-> CognitiveExposure`
`-> downstream engagement/share`

These stages should not be collapsed simply because one dataset contains a variable called "exposure".

In CBD, the existing `ExposureEvent` enters the Familiarity update and therefore represents a cognitive-model input. A platform view is an observable platform event. It can be evidence for an exposure opportunity, but it is not automatically proof that the information was attended to, encoded, or made familiar in the cognitive sense used by CBD.

## Empirical basis for the component split

### SOMAR civic-news potential exposure

ICPSR 300450, *Potential Exposure to Facebook Posts with Civic News URLs*, measures users who potentially viewed posts with civic-news URLs shared by one of their connections. The public metadata describe URL-level metrics for U.S. adult monthly active Facebook users aggregated over 2020-09-01 to 2021-02-01 and include potential audience size.

This is evidence for a **PotentialDelivery / eligible-audience** construct.

It is not a dyadic event table identifying which specific sender Share caused which recipient opportunity.

### SOMAR civic-news actual exposure

ICPSR 300470, *Exposure to Facebook Posts with Civic News URLs*, measures users who viewed such posts. The public metadata describe URL-level metrics over the same broad U.S. adult Facebook population and study period and include content views and audience size.

This is evidence for a distinct **PlatformView** construct.

It is still aggregated at URL level in the public description, not an A→B Share-to-view lineage table.

### SOMAR civic-news engagement

ICPSR 300475, *Engagement with Facebook Posts with Civic News URLs*, measures users who engaged with such posts and the volume of engagement. The public metadata describe URL-level metrics and include content views and audience size.

This supports a separate **downstream action conditional on platform exposure** layer, subject to exact codebook definitions.

### Participant-level and daily exposure surfaces

ICPSR 300396 contains participant-level Facebook activity metrics including User connections, Time spent, Content views and Content engagement.

ICPSR 300446 contains daily domain-level views for consenting passive-tracking participants.

ICPSR 300458 contains participant × deceptive-network exposure/engagement aggregates.

These sources offer stronger person-level or person-by-source-group measurement than URL population aggregates, but the public descriptions still do not establish a complete event-level sender→recipient Share lineage.

### FIES experimental measurement

The FIES like-minded-sources experiment explicitly reports Facebook Feed exposure in terms of respondent **views** and reports engagement conditional on exposure. This provides substantive support for treating platform views as a separately observable stage rather than inferring exposure from engagement actions.

The paper does not establish that every platform view equals the CBD cognitive exposure construct.

### Bluesky prospective seen events

AT Protocol defines `interactionSeen` as a feed item seen by a user and provides item/request linkage fields such as item URI, `feedContext` and `reqId`.

This supports the same conceptual separation prospectively:

`candidate delivery -> platform seen event -> cognitive exposure`.

Current deployment/access/privacy conditions must be verified before any study, and a seen event remains a platform measurement rather than a direct cognitive state measurement.

## Proposed measurement constructs

### PotentialDelivery

Definition:

A platform-level opportunity in which content is eligible or potentially available to a recipient under the empirically defined platform relation and observation window.

Examples:

- SOMAR potential audience for content shared by a connection;
- a returned feed candidate in a prospectively instrumented feed system.

Non-claims:

- not proof of rendering;
- not proof of viewing;
- not cognitive exposure.

### PlatformView

Definition:

A platform-observed view/seen event under the source dataset's operational definition.

Examples:

- Facebook content view in SOMAR/FIES;
- prospective AT Protocol `interactionSeen` if deployed and available under an approved study.

Non-claims:

- not automatically attention;
- not automatically comprehension;
- not automatically Familiarity update.

### CognitiveExposure

Definition:

The existing CBD `ExposureEvent` construct that enters the Familiarity process.

Empirical mapping requirement:

A future measurement model must state the assumptions or experimental evidence used to map PlatformView into CognitiveExposure. The mapping may be probabilistic and may depend on duration, visibility, repeated presentation, task context, or other variables, but no such functional form is authorized here.

## Candidate empirical component quantities

The following are **candidate descriptive constraints**, not currently estimated parameters:

### Potential-to-view realization

Concept:

`r_view = observed platform-view audience / potential audience`

This ratio may be meaningful only when a codebook audit confirms that numerator and denominator:

- use compatible user populations;
- refer to the same content unit and observation period;
- use compatible unique-user versus event-count semantics;
- apply compatible privacy/suppression rules;
- treat repeated views consistently.

Until those conditions are verified, this ratio must not be computed or interpreted.

Even when valid, an aggregate URL/domain-level `r_view` is **not** the dyadic F1a `q_transmit`. It is an aggregate empirical component constraint on the PotentialDelivery→PlatformView layer.

### Engagement conditional on view

Concept:

`r_engage = engaged audience / viewed audience`

This is also codebook-dependent. It constrains a downstream platform-action layer, not cognitive exposure.

## Dataset mapping

| Dataset | Publicly documented unit | Potential opportunity | Actual view | Engagement | Dyadic Share→View lineage | Candidate role |
| --- | --- | --- | --- | --- | --- | --- |
| ICPSR 300450 | URL-level, study-period aggregate | yes | no | no | no | PotentialDelivery |
| ICPSR 300470 | URL-level, study-period aggregate | no | yes | no | no | PlatformView |
| ICPSR 300475 | URL-level, study-period aggregate | no | views included | yes | no | downstream action |
| ICPSR 300446 | participant/day × domain aggregate | no | yes | not primary | no | participant-level view timing |
| ICPSR 300458 | participant × deceptive-network aggregate | not established publicly | yes | yes | no | participant/source-group exposure |
| ICPSR 300396 | participant-level platform metrics | connections available | views | engagement | not established publicly | participant-level bridge feasibility |
| AT Protocol prospective | request/item-level if instrumented | candidate item | `interactionSeen` if available | other interaction events | potentially linkable by request/item, deployment-dependent | prospective fine-grained measurement |

## Codebook gate before numerical analysis

Public study descriptions are sufficient to justify a measurement architecture, but not a numerical calibration.

Before calculating any empirical ratio or fitting any component parameter, the exact restricted-data codebooks must establish:

1. variable names and definitions;
2. row unit and grouping keys;
3. whether audience fields count unique users;
4. whether view fields are users, events, or both;
5. repeated-view handling;
6. whether potential and actual exposure datasets use identical eligibility/population filters;
7. time-window compatibility;
8. content URL/domain normalization;
9. privacy thresholding, suppression and rounding;
10. missingness rules;
11. weighting or sampling rules;
12. whether participant-level connections can be linked to item-level Share/View records;
13. whether any sender→recipient lineage is preserved or deliberately removed.

No numerical bridge is authorized until this gate is satisfied.

## Relationship to q_transmit

The recovery benchmark's `q_transmit` is a synthetic collapsed parameter:

`P(CBD ExposureEvent | realised Share-edge opportunity)`.

The empirical component architecture reveals that this shortcut may conflate at least:

- eligibility/potential delivery;
- actual platform view;
- cognitive encoding/exposure.

Therefore the current q must remain **calibration-only**.

A future empirically constrained model may choose either:

1. to replace the collapsed q with multiple measured/estimated component transitions; or
2. to retain a collapsed q only if a dataset directly observes a compatible end-to-end numerator and denominator.

Neither decision is made here.

## Validation ladder consequence

F1a remains **RECOVERY_TESTED**.

This bridge can support future component-level empirical constraints without promoting the full F1a loop. Promotion to EMPIRICALLY_CONSTRAINED requires a separate prospective empirical analysis contract and a measurement bridge that satisfies the existing empirical-observability gate.

No ACTIVE status, runtime activation, recipient Decision generation, full feedback closure, or System Dynamics reclassification is authorized by this design.
