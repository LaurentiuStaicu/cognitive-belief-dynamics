# F1b R2 post-C2 scientific interpretation result — 2026-09-28

Issue: #249

Status: **S0–S3 COMPLETE / THREE-OUTCOME CHARACTERIZATION RETAINED / S4–S5 REQUIRED**

## Execution

Temporary execution:
- PR #253 — closed unmerged;
- workflow run `36427891938`;
- execution head `4a618e03d34d469fa9ac6bd87b1323e37559abf4`;
- merged interpretation gate baseline `0b793a41a086844a9afc42d6176ed1c56cb48312`.

Result artifact:
- artifact ID `10972761353`;
- ZIP SHA-256 `5535fcff31786e42764d0262f55de9f8dcd35ee6ac30bf8fe1894c5f13947637`;
- result JSON SHA-256 `89e43fb53a99cb4ffc07951c02275311858c6cd77d4230182e79d55c7ed35a22`;
- result JSON size 714,724 bytes.

No simulation, bootstrap continuation, C2 rerun or cap extension occurred.

## Final three-outcome state

Across all 750 homogeneous restriction streams:
- reject: 246;
- not-reject: 481;
- unresolved-at-cap: 23.

Primary unconditional proportions:
- reject: 0.3280;
- not-reject: 0.6413;
- unresolved: 0.0307.

Because unresolved streams remain in the denominator, the descriptive reject-proportion sensitivity interval induced only by those 23 outcomes is:

`[0.3280, 0.3587]`.

The conditional reject proportion among decided streams, 0.3384, is secondary descriptive information only.

## Identity-type check

NULL identities:
- 30 streams;
- 0 reject;
- 30 not-reject;
- 0 unresolved.

DEPARTURE identities:
- 720 streams;
- 246 reject;
- 451 not-reject;
- 23 unresolved.

This cleanly separates the null calibration evidence from the much more heterogeneous departure-detection behavior.

## Role semantics

### Null false-rejection controls

`ADD_NULL_FALSE_REJECTION`
- 10/10 not-reject;
- 0 reject;
- 0 unresolved.

`CBD_NULL_FALSE_REJECTION`
- 20/20 not-reject;
- 0 reject;
- 0 unresolved.

These are descriptive false-rejection checks, not detection-power estimates.

### ADD specificity negative control

`ADD_SPECIFICITY_NEGATIVE_CONTROL`
- total: 120;
- not-reject: 113;
- reject: 5;
- unresolved: 2;
- specificity-pass proportion: 0.9417;
- unresolved sensitivity bounds: [0.9417, 0.9583].

### Departure-detection roles

`ADD_DEPARTURE_DIAGNOSTIC`
- total: 240;
- reject: 137;
- not-reject: 96;
- unresolved: 7;
- descriptive detection proportion: 0.5708;
- unresolved sensitivity bounds: [0.5708, 0.6000].

`CBD_DEPARTURE_DETECTION`
- total: 360;
- reject: 104;
- not-reject: 242;
- unresolved: 14;
- descriptive detection proportion: 0.2889;
- unresolved sensitivity bounds: [0.2889, 0.3278].

The difference between these roles is descriptive evidence of a heterogeneous recovery surface. It is not yet a validated power comparison.

## Controlled-departure surface

By KL target, descriptive reject proportions rise across the retained grid:
- KL 0.001: 53 reject / 181 not-reject / 6 unresolved; reject bounds [0.2208, 0.2458];
- KL 0.002: 86 / 144 / 10; bounds [0.3583, 0.4000];
- KL 0.003: 107 / 126 / 7; bounds [0.4458, 0.4750].

By axis:
- combined violation: 76 reject / 154 not-reject / 10 unresolved; bounds [0.3167, 0.3583];
- complement-relation violation: 132 / 102 / 6; bounds [0.5500, 0.5750];
- standalone accuracy main effect: 38 / 195 / 7; bounds [0.1583, 0.1875].

These are descriptive across the current 10 evaluation replicates and must not be promoted to inferential recovery-power estimates before S4.

## Unresolved-at-cap

The 23 unresolved streams reproduce exact canonical SHA-256:

`673ac85475800b4e032469fbeae8ead7083e6cd90fee209f7e0c451162b13217`.

Distribution:
- restriction: ADD 9, CBD complement 14;
- role: ADD departure 7, ADD specificity negative control 2, CBD departure detection 14;
- axis: combined 10, complement relation 6, standalone accuracy 7;
- KL: 0.001 → 6, 0.002 → 10, 0.003 → 7;
- sign: minus 13, plus 10;
- evaluation replicate: 0→0, 1→1, 2→3, 3→1, 4→2, 5→3, 6→7, 7→1, 8→1, 9→4.

The replicate concentration is descriptive only. The 23 outcomes remain unresolved; no boundary proximity or cell membership is used to impute them.

## Scientific consequence

S0–S3 succeeds as a descriptive three-outcome characterization layer.

What it establishes:
- exact H2+C2 provenance composition;
- null false-rejection behavior for the retained simulation design;
- role-specific descriptive detection/specificity behavior;
- explicit unresolved sensitivity bounds;
- a heterogeneous controlled-departure recovery surface.

What it does not establish:
- stable inferential power;
- adequacy of 10 evaluation replicates;
- superiority of population-level or hierarchical recovery;
- robustness to missingness or variance misspecification;
- authoritative core grid;
- human N;
- recruitment readiness.

## Next gate

Proceed to S4–S5 only:

1. assess whether the current 10 evaluation replicates support stable characterization of the role × axis × KL × sign × anchor surface;
2. if not, predeclare additional evaluation replicates prospectively;
3. revisit population-level versus hierarchical recovery;
4. reintroduce weak/moderate/strong, missingness and random-effect variance misspecification characterization;
5. define inferential recovery/power estimands before any core-grid or human-N freeze.

No C2 cap extension is part of S4–S5.

## Boundary

`POST-C2 S0–S3 = COMPLETE / RETAINED`

`PRIMARY OUTCOME = REJECT / NOT-REJECT / UNRESOLVED`

`C2 CAP = IMMUTABLE`

`POWER = NOT YET VALIDATED`

`EVALUATION-REPLICATE ADEQUACY = NOT YET DETERMINED`

`AUTHORITATIVE CORE GRID / HUMAN N = NOT FROZEN`

`PARTICIPANT RECRUITMENT = NOT AUTHORIZED`

`RUNTIME F1B = NOT AUTHORIZED`
