# F1a empirical observability and evidence-bridge audit

Status: **EMPIRICAL_BRIDGE_AUDIT_ONLY**

Current F1a ladder stage: **RECOVERY_TESTED**

Candidate next stage: **EMPIRICALLY_CONSTRAINED**

This audit asks what real-world observations would be required to constrain the F1a transmission mechanism without silently replacing its estimand. It does not activate an empirical parameter and does not change the current F1a stage.

## Current estimand

The recovery benchmark defines:

`q_transmit = P(realised recipient ExposureEvent | realised Share-edge opportunity)`

under a deliberately simple directed dyad.

To estimate this quantity empirically, both the numerator and denominator must have defensible observational counterparts.

Required measurement components are:

1. a realised Share by sender A for a specific information item;
2. an eligible A→B transmission relation at the relevant time;
3. a recipient-specific delivery/impression/view event for B for that same item or an explicitly defined transmission descendant;
4. timestamps sufficient to preserve causal ordering and define delay;
5. negative Share-edge opportunities in which no recipient exposure occurred;
6. item/content identity and provenance sufficient to distinguish the same claim from the same concrete information item;
7. sender/transmitter identity separated from original content source;
8. an explicit bridge from platform-level delivery/impression to the CBD cognitive `ExposureEvent`.

Without items 1–5, the current binomial estimand is not identifiable. Without item 8, a platform impression can at most constrain a platform-delivery construct, not automatically the cognitive exposure state used by CBD.

## Why reposts are not exposure logs

A repost is a downstream action. It proves that a user acted on content, but it does not enumerate all users who saw the content and chose not to repost it.

Recent diffusion literature explicitly distinguishes reshare cascades from exposure cascades and notes that empirical platform data commonly observe the former more readily than the latter. Studies that reconstruct "virtual timelines" from follower links and repost histories are inference procedures, not direct observation of impressions or cognitive exposure.

Therefore CBD must not estimate `q_transmit` by dividing reposts by follower edges or by reconstructed visible opportunities and then describe the result as observed exposure probability.

## Candidate source audit

### 1. Bluesky Social Dataset v3

Sources:

- Zenodo v3: https://zenodo.org/records/14669616
- dataset paper: DOI 10.1371/journal.pone.0310330

Documented observables include:

- directed follower relations;
- complete collected post histories for the sampled users;
- timestamped reply, repost and quote interactions;
- derived interaction graphs;
- posts present in 11 collected thematic feed-generator outputs;
- feed bookmarks and likes to posts appearing in those feeds.

Useful F1a constraints:

- network topology summaries and directed-degree distributions;
- observed repost/quote action frequencies;
- activity timing;
- item/reference lineage for quotes/replies and reconstructed repost metadata;
- properties of selected feed-output candidate sets.

Important limitations for current `q_transmit`:

- the follower graph is primarily a collection-period snapshot, not a complete edge-state history for every event;
- feed output is an algorithm/feed-level candidate set, not a per-user historical impression log;
- the public dataset description does not provide a user×item table proving that recipient B actually viewed item I;
- downstream likes/reposts are selected actions and do not enumerate non-engaging viewers;
- therefore realised cognitive ExposureEvent is not directly observed.

Verdict:

**PARTIAL_EMPIRICAL_CONSTRAINT_ONLY**.

Bluesky can constrain synthetic topology/activity design choices in a future separately contracted experiment, but it does not by itself identify the present F1a `q_transmit`.

### 2. Bluesky / AT Protocol prospective instrumentation

Sources:

- API reference: https://docs.bsky.app/docs/api/app-bsky-feed-get-feed
- feed-generator architecture: https://github.com/bluesky-social/feed-generator

A feed generator receives feed requests and returns post URIs/candidate items. **Feed output is a candidate-delivery surface**, not proof that a client rendered, displayed, attended to, or cognitively encoded each item.

The current AT Protocol lexicon adds an important prospective measurement capability: `app.bsky.feed.defs#interactionSeen` is explicitly described as **"Feed item was seen by user"**. The interaction object can also carry the item AT URI, `feedContext`, and a per-request `reqId`, which creates a protocol-level route for linking a seen event back to a served feed item/request.

This does **not** make the existing public Bluesky Social Dataset an impression log. It also does not prove that a third-party research feed generator can currently receive all such UI events in production. Bluesky's social-app issue #7285 documents that forwarding UI interaction events such as `interactionSeen` to third-party feed generators had not yet been implemented there because permissions/privacy controls were unresolved. Because implementation state can change, any prospective study must verify current client behavior, endpoint delivery, consent/privacy controls, and retention semantics at study start rather than infer access from the lexicon alone.

Even when `interactionSeen` is available, it is a **platform-level seen event**, not automatically a CBD cognitive `ExposureEvent`. A prospective measurement design should therefore retain distinct constructs such as:

`EligibleTransmission -> ReturnedCandidate -> interactionSeen / RenderedImpression -> CognitiveExposure`.

Verdict:

**PROSPECTIVE_INSTRUMENTATION_CANDIDATE / DEPLOYMENT_ACCESS_AND_PRIVACY_VERIFICATION_REQUIRED**.

This is not an existing empirical calibration dataset and must not be treated as one.

### 3. SNAP Higgs Twitter dataset

Source:

- https://snap.stanford.edu/data/higgs-twitter.html

Documented observables include:

- directed follower network;
- retweet, reply and mention networks;
- timestamped RT/MT/RE activity.

Useful F1a constraints:

- topology;
- interaction-layer structure;
- historical action timing and retweet activity.

Limitations:

- no recipient-level impression/view log;
- follower/action data do not reveal all exposure opportunities or non-action exposures;
- the data describe a narrow 2012 event and platform context.

Verdict:

**PARTIAL_EMPIRICAL_CONSTRAINT_ONLY / HISTORICAL_STRESS_REFERENCE**.

It is useful for structural benchmarking, not direct `q_transmit` estimation.

### 4. Meta U.S. 2020 Facebook and Instagram Election Study / SOMAR

Source:

- https://www.icpsr.umich.edu/sites/somar/view/studies/300396/versions/V2.0

The study contains randomized platform interventions, including chronological-feed, reshare-holdout and like-minded-source-demotion conditions, with sensitive files available only in a Virtual Data Enclave.

Potential value:

- causal constraints on platform-mediated changes in exposure/engagement under controlled interventions;
- possible access to richer platform-use variables than public social-media archives.

Current limitations:

- restricted access;
- the public record is insufficient to establish that the exact F1a numerator and denominator are available;
- exact measurement fields, temporal granularity, item identity and impression semantics require codebook/VDE audit before use.

Verdict:

**ACCESS_AND_MEASUREMENT_REVIEW_REQUIRED**.

No F1a empirical claim may be made from the public dataset description alone.

## Empirical-constraint levels

To avoid an all-or-nothing use of real data, F1a may record component-specific evidence without promoting the whole loop:

### Topology-constrained

Real directed-network statistics can inform a synthetic network generator or stress envelope.

This does not constrain `q_transmit`.

### Action-constrained

Observed repost/quote/activity rates and timing can constrain downstream action benchmarks.

This does not identify latent exposure probability.

### Delivery/impression-constrained

Requires recipient-specific evidence that an item was actually delivered/rendered to a user and a defensible denominator of eligible opportunities.

This could constrain a platform-level impression probability, but still requires a bridge before equating it with cognitive `ExposureEvent`.

### Cognitive-exposure-constrained

Requires an explicit measurement model linking observed presentation/view/attention data to the CBD exposure construct.

Only this level can directly constrain the existing F1a cognitive exposure edge without redefining the model variable.

## Promotion rule

F1a remains **RECOVERY_TESTED**.

A future promotion to **EMPIRICALLY_CONSTRAINED** requires a prospective contract that:

- names the empirical dataset/version and access state;
- freezes the observational unit;
- defines numerator and denominator;
- distinguishes eligibility, candidate delivery, rendered impression and cognitive exposure;
- defines item/source/transmitter identity;
- specifies missingness and unobserved exposure handling;
- identifies how negative opportunities are measured;
- states the target population/platform/time period;
- specifies train/calibration versus validation partitions where applicable;
- includes falsification/negative controls;
- quantifies uncertainty;
- prevents action-only datasets from being relabeled as exposure data.

If only topology or action constraints are available, those may be retained as **partial empirical component constraints** while the F1a ladder stage remains RECOVERY_TESTED.

## Current conclusion

The strongest open public candidate, Bluesky, is valuable for the next generation of synthetic topology/activity stress tests and for item-level diffusion research. It is not sufficient on its own to estimate the present cognitive `q_transmit`.

The scientifically correct next step is therefore not a numerical calibration. It is to either:

1. define a partial topology/action empirical bridge while keeping q calibration-only; or
2. identify or prospectively collect a dataset with recipient-specific impression/view measurements and an explicit cognitive-exposure bridge.

No empirical promotion is authorized by this audit.
