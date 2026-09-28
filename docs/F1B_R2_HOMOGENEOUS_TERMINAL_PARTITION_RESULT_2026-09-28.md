# F1b R2 homogeneous terminal-partition result — 2026-09-28

Issue: #250

Status: **E1–E5 COMPLETE / READY FOR NEXT RECOVERY-POWER CHARACTERIZATION / POWER NOT YET VALIDATED**

## Execution

Temporary execution:
- PR #257 — closed unmerged;
- workflow run `36431385526`;
- execution head `ccb57e97066c4ce79f52f2026e80ccd0ab8c92a2`;
- qualified main baseline `14e2b7916a0289bbd215192e7a78c38562fb29db`.

Result artifact:
- artifact ID `10973182815`;
- ZIP SHA-256:
  `be5582e49b9ad80dd7eb61f3e251db5605f82c06cdb068479e920cca3b16a611`;
- result JSON SHA-256:
  `40e6a70bfb2630517186712e5db12225a1dd08ffab2344e2eaef856a8b0623ac`;
- result JSON size: 1,231,594 bytes.

No simulator, fitter or sequential bootstrap continuation was run.

## Terminal partition

The retained H2 + C2 artifacts compose exactly:
- 750 unique scientific streams;
- 526 decisions inherited from H2 Stage-B;
- 201 decisions reached prospectively in C2;
- 23 `SEQUENTIAL_UNRESOLVED_AT_CAP`;
- 727 total terminal sequential decisions;
- zero bootstrap-refit failures.

The 23 unresolved run IDs reproduce canonical SHA-256:

`673ac85475800b4e032469fbeae8ead7083e6cd90fee209f7e0c451162b13217`.

## Global descriptive state

Across all 750 streams:
- reject: 246;
- not-reject: 481;
- unresolved-at-cap: 23.

Reject:
- resolved-only descriptive proportion: 0.3384;
- full-denominator descriptive bounds with unresolved assigned to either extreme:
  `[0.3280, 0.3587]`.

Expected scientific direction:
- resolved decisions in expected direction: 384;
- opposite direction: 343;
- resolved-only descriptive proportion: 0.5282;
- full-denominator descriptive bounds:
  `[0.5120, 0.5427]`.

These are characterization summaries, not validated power estimates.

## Five-role semantic audit

### ADD_NULL_FALSE_REJECTION
- 10 total;
- 10 resolved;
- 0 reject;
- 10 not-reject;
- 0 unresolved;
- expected-direction bounds: `[1.0000, 1.0000]`.

### CBD_NULL_FALSE_REJECTION
- 20 total;
- 20 resolved;
- 0 reject;
- 20 not-reject;
- 0 unresolved;
- expected-direction bounds: `[1.0000, 1.0000]`.

### ADD_SPECIFICITY_NEGATIVE_CONTROL
- 120 total;
- 118 resolved;
- 5 reject;
- 113 not-reject;
- 2 unresolved;
- expected-direction bounds: `[0.9417, 0.9583]`.

### ADD_DEPARTURE_DIAGNOSTIC
- 240 total;
- 233 resolved;
- 137 reject;
- 96 not-reject;
- 7 unresolved;
- expected-direction bounds: `[0.5708, 0.6000]`.

### CBD_DEPARTURE_DETECTION
- 360 total;
- 346 resolved;
- 104 reject;
- 242 not-reject;
- 14 unresolved;
- expected-direction bounds: `[0.2889, 0.3278]`.

The departure roles therefore remain strongly heterogeneous. This is evidence that the recovery surface needs further characterization, not evidence for a single pooled power value.

## Unresolved-at-cap boundary distance

For the 23 unresolved streams at n=10,000:

Distance above lower boundary:
- minimum: 16;
- median: 83;
- maximum: 181.

Distance below upper boundary:
- minimum: 5;
- median: 103;
- maximum: 170.

Boundary proximity is retained descriptively only. No missing terminal decision is inferred from these distances.

## E5 interpretation decision

All predeclared conditions pass:
- terminal-partition integrity;
- all five role semantics valid;
- every role has at least one resolved decision;
- unresolved outcomes retained without imputation;
- descriptive bounds computable for every role.

Therefore the versioned E5 conclusion is:

`READY_FOR_NEXT_RECOVERY_POWER_CHARACTERIZATION`

This means the resampling-risk layer is sufficiently interpretable to define the next prospective characterization study.

It does **not** mean:
- inferential power is validated;
- the current ten evaluation replicates are adequate;
- a population-level or hierarchical fitter has been selected;
- missingness or variance misspecification has been qualified;
- an authoritative core grid can be frozen;
- human N can be frozen.

## Next gate

Proceed to S4–S5:

1. quantify Monte Carlo precision at the scientific-cell level;
2. decide prospectively whether additional evaluation replicates are required;
3. preserve explicit three-outcome handling;
4. compare population-level versus hierarchical recovery;
5. characterize weak/moderate/strong regimes;
6. characterize missingness;
7. characterize random-effect variance misspecification;
8. define recovery/power estimands before any core-grid or human-N freeze.

The number of future simulation repetitions must be justified by target Monte Carlo precision, not selected from observed favorable rates.

## Boundary

`TERMINAL PARTITION = COMPLETE / RETAINED`

`E5 = READY FOR NEXT RECOVERY-POWER CHARACTERIZATION`

`POWER = NOT YET VALIDATED`

`EVALUATION-REPLICATE ADEQUACY = NOT YET DETERMINED`

`C2 CAP = IMMUTABLE`

`UNRESOLVED IMPUTATION = NOT AUTHORIZED`

`AUTHORITATIVE CORE GRID / HUMAN N = NOT FROZEN`

`PARTICIPANT RECRUITMENT = NOT AUTHORIZED`

`RUNTIME F1B = NOT AUTHORIZED`
