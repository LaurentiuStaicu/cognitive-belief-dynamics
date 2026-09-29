# F1b R2 S4 W0 combined result — 2026-09-29

Issue: #259

Status: **W0 COMPLETE / EXACT COMBINE PASS / RETENTION GATE**

The temporary full-wave execution in PR #305 completed without a failed or cancelled shard. PR #305 was then closed unmerged, as required by the prospectively frozen retention sequence.

## Execution evidence

- temporary execution PR: `#305` (closed unmerged);
- workflow run: `36549608192`;
- workflow run number: `1`;
- execution head: `4de4cd9f75e520d4e8947b8a72e3587718a5bdef`;
- qualified main baseline: `ef73aa19488c6b1965c1ed125c5a709c736ebd13`;
- 250 / 250 shard jobs successful;
- exact combine job successful;
- combined artifact ID: `11040214169`;
- artifact name: `f1b-r2-s4-w0-combined`;
- artifact ZIP SHA-256: `61033699f6de85e637ef46f1841159b3af653c03045355ccad9e00efb69d2d3a`;
- combined JSON SHA-256: `096c2eca7e31b886b9bf308b77292bf9b52e64e620ff7f6dfbf81f9a736d903b`;
- combined JSON size: 29,857,067 bytes;
- evidence JSON SHA-256: `543a6582101def7e17e393c50967c81c9d4617ad188d73c32122fc1fdff42090`.

## Exact W0 contract

The combine reproduced the frozen identity exactly:

- 250 shards;
- 3,750 scientific runs;
- 15,000 method rows;
- 840 imported scientific runs;
- 3,360 retained M2 method rows;
- 2,910 new scientific runs;
- 11,640 new method executions.

Frozen identity digests all matched:

- scientific-run IDs: `7f49bc6a67508566d2143d699af8d10d1721f571c1981035cdf1aef39dad8419`;
- method-row IDs: `7a936f191cdcd58e3988db43b43dbb166a2ca18033a8c5a9913f4efee2ef8b6c`;
- imported method-row IDs: `d9d42ed4437199375c593110f555502d26a6660e81e045b9e1b105e8a1434537`;
- new method-row IDs: `dad1b46e6028a4f0a415e8c65b5442aab44eb867e446c1ecb80ab637ee033fd5`;
- shard identity: `ceef215d96b27d6a6c5ba4af60c1b8927c9370343eb43b46769ad61cf44ecc66`;
- row content: `529072c8a0bd3996d88aede0e3ecf86c61f67932d021ec76f314ef01d53c9e17`.

Every scientific run has exactly the four frozen inference methods on the same dataset identity. No denominator was reduced and no replacement replicate was introduced.

## Terminal accounting

The complete W0 method-row accounting is retained, but it is not a scientific acceptance criterion:

- resolved at 199-draw prefix: 10,579;
- resolved after sequential continuation: 3,874;
- unresolved at n=10,000 cap: 547;
- refit failures: 0;
- prefix-execution failures: 0;
- reject decisions: 4,521;
- not-reject decisions: 9,932.

Evidence provenance is exactly:
- retained M2 import: 3,360 rows;
- S4 new execution: 11,640 rows.

Per-method terminal accounting is retained in the JSON result. For reference only:

- POPULATION: 142 unresolved at cap;
- HIERARCHICAL_0.5X: 179 unresolved at cap;
- HIERARCHICAL_1X: 130 unresolved at cap;
- HIERARCHICAL_2X: 96 unresolved at cap.

These counts do not rank or select a method. Wave-level scientific interpretation remains forbidden.

## Consequence

W0 has passed its structural/provenance execution gate. Once this retention PR is merged, W1 becomes operationally authorized under the already frozen all-new-wave contract:

- evaluation replicates 25..49;
- 3,750 scientific runs;
- 15,000 new method executions;
- exactly 250 deterministic shards;
- no M2 imports;
- unchanged dataset generator, four-method order, RNG namespaces, 199-draw prefix, sequential controller, n=10,000 cap and Haswell lineage;
- scientific interpretation remains forbidden at W1 wave level.

W2 remains blocked until W1 combine is separately retained. W3 remains blocked until W2 combine is separately retained.

## Scientific boundary

This retention does not establish power and does not authorize scientific interpretation of W0 distributions. The broad S4 estimand remains the complete n=100/cell design across W0-W3.

No method or hierarchical scale is selected. Human N is not frozen. Participant recruitment and runtime F1b activation remain unauthorized.

## Release boundary

The planned next release remains v0.2.0 under Issue #277.

The release blocker remains open until all four broad waves are executed, retained, final-combined and scientifically interpreted under the predeclared S4 criteria.

## Boundary

`W0 = COMPLETE / EXACT COMBINE PASS / RETAINED AFTER MERGE`

`W1 = AUTHORIZED ONLY AFTER THIS RETENTION MERGES`

`W2 / W3 = BLOCKED BY SEQUENTIAL WAVE RETENTION`

`SCIENTIFIC INTERPRETATION = NOT AUTHORIZED`

`METHOD / SCALE SELECTED = NO`

`POWER = NOT VALIDATED`

`HUMAN N = NOT FROZEN`

`RUNTIME F1B = NOT AUTHORIZED`

`v0.2.0 BLOCKER = OPEN`
