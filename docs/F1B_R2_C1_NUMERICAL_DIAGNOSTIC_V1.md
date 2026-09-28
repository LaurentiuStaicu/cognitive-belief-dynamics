# F1b R2 Stage C1 numerical diagnostic V1

Status: **IMPLEMENTED DESIGN / DIAGNOSTIC ONLY / NOT YET EXECUTED**

Issue: #223

Baseline main:
`229b005c50b4349b3d4a83892af80a9b8d1af8b4`

Scientific source retained from Stage C1:
`ff63e6f72af54b78070a0d74c514805401602943`

## Why this slice exists

Stage C1 of #218 required exact reproduction of all 224 retained unresolved
resampling-risk streams before any new bootstrap draw could be generated.

The retained result merged by PR #222 failed closed:

- 224 eligible streams;
- 120 exact passes;
- 104 failures;
- all 224 synthetic dataset fingerprints reproduce exactly;
- 59 failures have a nonzero observed-statistic difference still within
  the frozen absolute tolerance of `1e-10`;
- 44 failures exceed that tolerance;
- one failure has an exactly identical observed statistic but a different
  199-attempt sequence hash.

The failure therefore cannot be diagnosed from the scalar observed statistic
alone. The retained C1 artifact does not contain the parameter vectors,
optimizer stopping path, per-draw bootstrap dataset fingerprints or regenerated
attempt statistics needed to locate the first divergence.

## Non-negotiable boundary

This diagnostic does not repair C1 and does not weaken it.

The following scientific files remain byte-identical to the lineage frozen by
the continuation design:

- `f1b_r2_paired_bootstrap_characterization.py`;
- `f1b_r2_restriction_recovery.py`;
- `f1b_prehuman_recovery.py`;
- `f1b_hierarchical_recovery.py`;
- `f1b_r2_kl_controlled_departures.py`.

The diagnostic may not change:

- L-BFGS-B starts or options;
- random-effect penalty scales;
- package versions;
- seed derivation;
- bootstrap draw ordering;
- attempt canonicalization;
- the `1e-10` observed-statistic tolerance;
- the Stage-C1 requirement of `224/224`;
- the prospective Stage-C2 cap or resampling-risk controller.

No draw index `>=199` is permitted.

## Instrumentation method

The implementation is additive.

`f1b_r2_c1_numerical_diagnostic.py` temporarily intercepts two module symbols
only while a diagnostic fit is executing:

1. the R2 hierarchical-fit symbol used by the restriction fitter;
2. the `scipy.optimize.minimize` symbol imported by the hierarchical fitter.

The wrapper then calls the exact original functions. It does not change the
objective, gradient, bounds, initial vector or optimizer options.

A `finally` block restores both symbols after every trace, including exception
paths. The implementation is intentionally single-process and single-threaded
while interception is active.

For every optimizer call it retains:

- family and fit serial;
- first-call versus retry identity;
- optimizer method and exact options;
- full hierarchical initial-vector fingerprint;
- population fixed-parameter values and fingerprint;
- success/status/message;
- iteration, function-evaluation and Jacobian-evaluation counts when returned;
- objective value;
- returned Jacobian infinity norm when returned;
- final full-vector and fixed-parameter fingerprints.

For each completed restricted/general fit it also retains the fixed parameters,
full parameter-vector fingerprint, penalized objective, log likelihood and
parameter count.

## Bootstrap probability trace without changing the simulator

The production simulator does not expose its probability vector or random
effects. The diagnostic therefore does not alter that function.

Instead, for a retained draw index it:

1. initializes the production RNG from the frozen
   `[bootstrap_stream_seed, restriction_index, draw_index]`;
2. calls the unchanged production simulator;
3. initializes a second RNG from the identical seed words;
4. reproduces the simulator's documented random-effect draws and Bernoulli
   operation in the same order;
5. fingerprints the random effects and probability vector;
6. constructs a diagnostic dataset;
7. requires exact array equality and an identical canonical dataset fingerprint
   between the diagnostic dataset and the unchanged production simulator output.

The probability trace is accepted only after that equality assertion passes.

## Diagnostic sentinel selection

The initial diagnostic uses four deterministic strata from the already-retained
C1 result. Inside each stratum, the lexicographically first `run_id` is selected.

The strata are:

1. `EXACT_PASS_CONTROL`;
2. `EXACT_OBSERVED_HASH_FAILURE`;
3. `WITHIN_TOLERANCE_HASH_FAILURE`;
4. `OUTSIDE_TOLERANCE_HASH_FAILURE`.

The exact-observed/hash-failure stratum is required to contain exactly one row,
matching the retained C1 audit.

This is a diagnostic partition of an already-observed failure artifact. It is
not a new inferential sampling rule and it does not alter any scientific
decision boundary.

## Prefix tracing

For each selected run the diagnostic:

1. regenerates the original synthetic dataset through the unchanged continuation
   regeneration path;
2. traces the observed restricted/general fit;
3. replays retained bootstrap draw indices from `0` upward;
4. fingerprints the bootstrap probabilities and generated dataset for each draw;
5. traces the restricted/general bootstrap fit;
6. compares the regenerated statistic with the retained attempt statistic;
7. records the exceedance indicator relative to the corresponding observed
   statistic;
8. stops after the first exact per-attempt divergence.

An exact-pass control therefore reaches all 199 retained draws. A failing
sentinel can stop earlier once the first divergent draw has been localized.

The helper rejects negative indices, duplicate/out-of-order indices and every
index greater than `198`.

## Environment identity

Each execution records:

- Python executable and version;
- NumPy version;
- SciPy version;
- platform and machine identity;
- CPU model where `/proc/cpuinfo` exposes it;
- NumPy build configuration;
- common BLAS/OpenMP thread environment variables;
- `threadpoolctl` runtime library/thread information when available.

CPU/BLAS differences remain hypotheses until controlled comparison demonstrates
an association with divergence.

## Repetition design

The first execution phase is:

- exactly two repeats in the same Python process for each sentinel;
- one or more fresh-process executions using the same frozen environment;
- comparison of the resulting diagnostic artifacts.

A separately identified runner comparison is deferred until same-environment
determinism has been characterized. This avoids confounding case composition
with runner differences.

## What would count as useful localization

The trace should identify the earliest layer that changes:

1. original dataset;
2. population initialization;
3. hierarchical optimizer path or fitted vector;
4. bootstrap probability vector/random effects;
5. bootstrap dataset;
6. bootstrap restricted/general fit;
7. scalar statistic;
8. exceedance decision.

The current retained evidence already rules out layer 1 for all 224 streams.

A divergence at a later layer is diagnostic evidence only. It is not permission
to change the environment or scientific algorithm until a separate lineage
qualification defines and validates such a change prospectively.

## Acceptance

This implementation slice is acceptable only if:

- all five protected scientific file blobs remain unchanged;
- ordinary CBD validation passes;
- unit tests prove deterministic sentinel selection;
- unit tests prove draw indices `>=199` fail closed;
- unit tests prove the probability-trace simulator reproduces the unchanged
  production simulator exactly;
- unit tests prove optimizer interception restores the original symbols.

## Boundary

`STAGE_C1 = FAILED / RETAINED`

`STAGE_C2 = BLOCKED`

`DIAGNOSTIC_SURFACE = ADDITIVE / NON_AUTHORITATIVE`

`SCIENTIFIC_FITTER = UNCHANGED`

`NEW_DRAW_INDEX >=199 = NOT AUTHORIZED`

`POWER = NOT VALIDATED`

`AUTHORITATIVE CORE GRID / HUMAN N = NOT FROZEN`

`PARTICIPANT RECRUITMENT = NOT AUTHORIZED`

`RUNTIME F1B = NOT AUTHORIZED`
