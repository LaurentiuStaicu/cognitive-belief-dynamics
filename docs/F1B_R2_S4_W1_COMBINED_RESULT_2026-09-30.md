# F1b R2 S4 W1 combined result — 2026-09-30

Issue: #259

Status: **W1 COMPLETE / EXACT COMBINE PASS / RETENTION GATE**

The temporary full-wave execution in PR #311 completed successfully. Its exact combined artifact was captured and independently hash-checked, and PR #311 was then closed unmerged as required by the prospectively frozen retention sequence.

## Execution evidence

- temporary execution PR: `#311` (closed unmerged);
- workflow run: `36603368092`;
- workflow run number / attempt: `1 / 1`;
- execution head: `b2431c6f9f9649b3beba5ffd581502f9ab30d6bb`;
- pull-request merge ref: `b6f6bcadb2ab33f146f7e3b11f14efea1a386636`;
- qualified main baseline: `b1e69e58b9ff364a2b4aa9ca407bee4bed69effc`;
- 250 / 250 shard jobs successful;
- exact combine successful;
- combined artifact ID: `11067119910`;
- artifact name: `f1b-r2-s4-w1-combined`;
- artifact ZIP SHA-256: `d14ba5b4dedfc0ee0a398d9d3029c167913e96eb39c4328b8717aed6da315621`;
- artifact ZIP size: `1,439,141` bytes;
- W1 plan JSON SHA-256: `a72fa4782ecfd055045cf3e33f81290fcf4034181fec97daecd0224e366bad8b`;
- combined JSON SHA-256: `4616d17cd3a6e673c1f589fb92b2fe633e6e45a2b0e594adc5dabbb46acdb913`;
- combined JSON size: `29,862,477` bytes;
- evidence JSON SHA-256: `8f17eab3cba5ffcad5e9b7b6e5b5a6a144912b0bd9ae016ae5d9cce58bedb4d1`;
- evidence JSON size: `1,666` bytes.

## Exact W1 contract

The combine reproduced the frozen W1 identity exactly:

- evaluation replicates 25..49;
- 250 shards;
- 3,750 scientific runs;
- 15,000 method rows;
- zero imported scientific runs;
- zero imported method rows;
- 3,750 new scientific runs;
- 15,000 new method executions.

Frozen identity digests all matched:

- scientific-run IDs: `42a1803705c0c4f7efbfae0983a7c57f20036c76cd933c99af3fcd4e3cd9087c`;
- method-row IDs: `2191e0aceb072c20bca90dab1b6db3ed8bffef997bf2ead8ec2ace2ac4a81957`;
- shard-plan: `36d294a165ec1e8a8baffac70516ce7fceab149998079b534998503f3f578175`;
- shard identity: `2e6d18c2d114a7709e7f09844353ad3738d206bc735e6a9e7cfc003b101e6928`;
- row content: `1c24c5f9048527d71908fc7686e9261a29f6b9595f5d755ca143ce33b9cd56e7`.

Every shard passed the production-shard validation and required Haswell numerical-lineage gate before it could satisfy the matrix dependency. The combine was therefore eligible only after the complete shard matrix succeeded.

## Terminal accounting

The complete W1 accounting is retained, but none of these outcome counts is a wave acceptance criterion:

- resolved at 199-draw prefix: 10,827;
- resolved after sequential continuation: 3,650;
- unresolved at n=10,000 cap: 523;
- reject decisions: 4,278;
- not-reject decisions: 10,199;
- evidence origin: exactly 15,000 `S4_NEW_EXECUTION` rows.

Per-method unresolved-at-cap accounting is retained in the JSON result. For reference only:

- POPULATION: 136;
- HIERARCHICAL_0.5X: 134;
- HIERARCHICAL_1X: 146;
- HIERARCHICAL_2X: 107.

These counts do not rank or select a method or hierarchical scale. Wave-level scientific interpretation remains forbidden.

## Consequence

W1 has passed its structural/provenance execution gate. Once this retention PR is merged, W2 becomes operationally eligible for the already prospectively frozen predecessor-driven promotion patch:

- W2 evaluation replicates 50..74;
- 3,750 scientific runs / 15,000 method rows;
- zero imports;
- exact W2 run/method/shard-plan digests already frozen in Issue #259;
- unchanged four-method order, shared `run_new_stream()`, RNG namespaces, 199-draw prefix, sequential controller, n=10,000 cap and Haswell lineage;
- no new scientific/method-selection preflight;
- W2 execution remains blocked until the promotion patch itself passes normal CBD validation and is merged.

W3 remains blocked until W2 exact combine is separately retained.

## Scientific boundary

This retention does not establish power and does not authorize scientific interpretation of W1 distributions. The broad S4 estimand remains the complete n=100/cell design across W0-W3.

No method or hierarchical scale is selected. Human N is not frozen. Participant recruitment and runtime F1b activation remain unauthorized.

## Release boundary

The planned next release remains v0.2.0 under Issue #277. The release blocker remains open until all four broad waves are executed, retained, final-combined and scientifically interpreted under the predeclared S4 criteria.

## Boundary

`W1 = COMPLETE / EXACT COMBINE PASS / RETAINED AFTER MERGE`

`W2 = PROMOTION ELIGIBLE ONLY AFTER THIS RETENTION MERGES; EXECUTION NOT YET AUTHORIZED`

`W3 = BLOCKED BY SEQUENTIAL WAVE RETENTION`

`SCIENTIFIC INTERPRETATION = NOT AUTHORIZED`

`METHOD / SCALE SELECTED = NO`

`POWER = NOT VALIDATED`

`HUMAN N = NOT FROZEN`

`RUNTIME F1B = NOT AUTHORIZED`

`v0.2.0 BLOCKER = OPEN`
