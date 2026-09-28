# F1b R2 Stage C1: retained failure and diagnostic boundary

Date: 2026-09-28
Scientific source: `ff63e6f72af54b78070a0d74c514805401602943`
Parent: #218. Execution: #220. Recovery combination: #221.

## Verified result

This audit reads the existing combined artifact only. It does not rerun a fit,
generate a dataset, or generate a bootstrap attempt.

The downloaded ZIP SHA-256 is
`3b9c81f9bb842a83c2427dbd961d5d8efd3a4d4c1c85b672fbb3afdc08fcf2aa`.
Artifact ID: `10941310440`, recovery run: `36346378109`.
The exact JSON is retained at
`model/results/f1b_r2_continuation_c1_failed_2026-09-27.json`.
Its 320497 bytes have SHA-256
`016a5c6d76ca17bca666a3133715e36523a7d217eb9b8d2e67ba63772b9d9c5a`.
Both hashes and the JSON size were checked locally against the recorded #221
provenance before this retention change.

There are 224 distinct eligible rows; all datasets reproduce exactly.
Observed-statistic tolerance remains absolute `1e-10`.

| Observed statistic | Attempt sequence | Count |
| --- | --- | ---: |
| Exactly identical | Exact hash match | 120 |
| Exactly identical | Hash mismatch | 1 |
| Different, within tolerance | Hash mismatch | 59 |
| Outside tolerance | Hash mismatch | 44 |

C1 therefore remains FAIL: 120 pass and 104 fail.
The maximum observed-statistic delta is `5.084656322651426e-7`.

| Restriction | Eligible | C1 pass | Observed-statistic failure |
| --- | ---: | ---: | ---: |
| CBD complement | 133 | 71 | 31 |
| Additive | 91 | 49 | 13 |

These are descriptive counts conditional on the 224 previously unresolved streams,
not population estimates, power estimates, or a new selection rule.

## What the code establishes

The original paired bootstrap and C1 both construct each RNG with
`SeedSequence([bootstrap_stream_seed, restriction_index, draw_index])`.
C1 reuses the same restriction fitting and exact-design simulation functions.
This source inspection does not establish machine-level equivalence.

The observed statistic is a clipped difference of two penalized objectives.
Equality of this scalar does not prove equality of either fitted parameter vector.
The bootstrap generator uses the re-estimated restricted fixed parameters,
fresh random effects, and Bernoulli sampling. A changed fitted parameter vector
can therefore alter bootstrap inputs even when the original dataset and seed match.

The hierarchical fit starts from a population-level fit, then uses L-BFGS-B:
first `maxiter=400, ftol=1e-10, maxls=50`; on failure it retries from the same
initial point with `maxiter=800, ftol=1e-9, maxls=100`.
The returned fit records convergence as a boolean but does not retain the
optimizer stopping message, iteration count, gradient, or retry-path identity.

SciPy defines ftol as a relative objective-improvement stopping criterion.
It is not an absolute error bound for the fitted objective, an agreement
tolerance between machines, or a parameter-error guarantee.
Reference: https://docs.scipy.org/doc/scipy/reference/optimize.minimize-lbfgsb.html
This observation is not a proposal to change either optimizer tolerance or C1.

## Particularly informative existing case

The following retained row has exactly equal observed statistics but unequal
attempt-sequence hashes:

`F1B.R2.KL_V2.PAIRED_BOOTSTRAP_DRAW_STABILITY.2026-09-27|V2|F1B.R2.KL_CONTROLLED_DEPARTURE.V2__CBD_ANCHOR_2__COMPLEMENT_RELATION_VIOLATION__PLUS__KL_0.001|REPLICATE=1|RESTRICTION=ADD_RESTRICTION`

It demonstrates that scalar observed-statistic agreement is insufficient.
It does not prove that the restricted parameters or bootstrap datasets agree.

## What is not identifiable from this artifact

C1 retains regenerated sequence hashes, not regenerated per-attempt statistics,
bootstrap dataset fingerprints, fitted parameter vectors, or optimizer traces.
Consequently this artifact cannot locate the first divergent draw, measure
per-attempt numeric drift, or determine whether Bernoulli exceedance decisions changed.

CPU/BLAS/threading differences are hypotheses, not an established root cause.
Cross-shard pass-rate variation also confounds runner differences with case
composition and is not a controlled hardware comparison.

## Next diagnostic design proposal — not executed

Preserve the original artifacts, code, seeds, ordering, fit settings and gate.
Instrument a separate diagnostic surface to compare, in order:

1. Original dataset fingerprint.
2. Population fit and hierarchical initial-vector fingerprints.
3. Restricted/general fitted parameter vectors and objective values, including
   optimizer message, iteration count, stopping path and projected gradient.
4. Restricted-model bootstrap probabilities and random-stream identity.
5. Per-draw bootstrap dataset fingerprint for retained indices 0..198 only.
6. Restricted/general bootstrap fits, statistic, and exceedance indicator.

Capture Python/package build identity, CPU, actual BLAS runtime and thread counts.
Diagnostic controls should include repeated execution in one process, a fresh
process in the same environment, and a separately identified runner environment.
These controls would distinguish within-environment nondeterminism from
cross-environment divergence. No result is claimed here.

Any prospective change to the numerical environment or scientific fitting path
requires explicit lineage qualification; it must not be substituted into the
current C1 execution to turn its retained failure into a pass.

## Boundary

`STAGE_C1 = FAILED / RETAINED`
`STAGE_C2 = BLOCKED_BY_STAGE_C1_REPRODUCTION_FAILURE`

The 526 previously resolved Stage-B decisions remain terminal.
The 224 unresolved streams remain unresolved for continuation purposes.
No new draw index >=199, threshold relaxation, scientific model change,
power claim, human-N freeze, recruitment, or runtime F1b activation is made.
