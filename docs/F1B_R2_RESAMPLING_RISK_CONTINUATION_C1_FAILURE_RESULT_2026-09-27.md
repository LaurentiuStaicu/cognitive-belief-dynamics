# F1b R2 Resampling-Risk Continuation — Stage C1 Failure Result

Status: **FAILED CLOSED / STAGE C2 BLOCKED / NON-AUTHORITATIVE**

Issue: #218  
Scientific source: `ff63e6f72af54b78070a0d74c514805401602943`

## Purpose

Stage C1 was designed to answer one narrow question before any new bootstrap attempt was generated:

> Can the current code and execution environment reproduce the exact retained first-199 bootstrap statistic sequence for every one of the 224 Stage-B unresolved streams?

The answer is no.

No bootstrap draw index >=199 was generated.

## Exact execution

Temporary Stage-C1 execution:
- PR #220;
- Actions run `36345806090`;
- eight deterministic SHA256(run_id) shards.

Because every shard failed closed after uploading its exact diagnostic artifact, the normal combined job was correctly skipped.

Recovery-combine PR #221 then downloaded only those eight immutable artifacts and combined them without rerunning any:
- synthetic dataset;
- observed restriction fit;
- bootstrap fit;
- bootstrap attempt.

Recovered combined diagnostic:
- artifact ID: `10941310440`;
- ZIP SHA-256:
  `3b9c81f9bb842a83c2427dbd961d5d8efd3a4d4c1c85b672fbb3afdc08fcf2aa`;
- exact JSON SHA-256:
  `016a5c6d76ca17bca666a3133715e36523a7d217eb9b8d2e67ba63772b9d9c5a`;
- exact JSON size: 320,497 bytes.

## Gate result

Required:

`224 / 224 exact reproductions`

Observed:

`120 / 224 exact reproductions`

Therefore:

`STAGE C1 = FAIL`

and

`STAGE C2 = NOT AUTHORIZED`.

## Dataset reproduction

All 224 synthetic datasets reproduce exactly:

`224 / 224 dataset SHA-256 matches`.

This is important because it excludes:
- dataset seed drift;
- dataset case-order drift;
- evaluation-replicate seed drift;
- V2 departure reconstruction drift;
- participant/item design drift.

The failure occurs downstream of deterministic dataset generation.

## Observed-fit reproduction

Observed-statistic absolute tolerance was prospectively frozen at:

`1e-10`.

Results:
- within tolerance: 180 / 224;
- outside tolerance: 44 / 224;
- maximum absolute drift:
  approximately `5.0846563e-7`.

Cumulative drift counts:
- <=1e-12: 124;
- <=1e-11: 136;
- <=1e-10: 180;
- <=1e-9: 204;
- <=1e-8: 217;
- <=1e-7: 222;
- <=1e-6: 224.

The observed statistic is therefore often numerically very close, but exact continuation requires more than a close observed statistic.

## Bootstrap-prefix reproduction

Exact canonical first-199 attempt-sequence SHA-256 match:

`120 / 224`.

Mismatch:

`104 / 224`.

Failure patterns:

1. dataset exact + observed statistic within tolerance + attempt hash exact:
   - 120 runs;

2. dataset exact + observed statistic within tolerance + attempt hash mismatch:
   - 60 runs;

3. dataset exact + observed statistic outside tolerance + attempt hash mismatch:
   - 44 runs.

Thus 60 streams fail exact continuation even though the observed statistic already satisfies the frozen 1e-10 tolerance.

This demonstrates that simply widening the observed-statistic tolerance cannot restore exact stream identity.

## Restriction context

ADD restriction:
- total: 91;
- exact C1 PASS: 49;
- observed statistic within tolerance: 78;
- exact attempt hash: 49.

CBD-complement restriction:
- total: 133;
- exact C1 PASS: 71;
- observed statistic within tolerance: 102;
- exact attempt hash: 71.

The problem is not isolated to one restriction family.

## Role context

CBD departure detection:
- 70 / 131 exact.

ADD departure diagnostic:
- 36 / 74 exact.

ADD specificity negative control:
- 13 / 17 exact.

CBD null:
- 1 / 2 exact.

The failure is not isolated to a single scientific role.

## Axis context

Standalone accuracy:
- 33 / 65 exact.

Complement relation:
- 51 / 84 exact.

Combined violation:
- 35 / 73 exact.

Null:
- 1 / 2 exact.

Again, the failure is not confined to one controlled-departure axis.

## Cross-shard variation

Exact PASS rates differ substantially across runners:

- shard 0: 5 / 21;
- shard 1: 9 / 31;
- shard 2: 7 / 21;
- shard 3: 25 / 29;
- shard 4: 14 / 21;
- shard 5: 26 / 30;
- shard 6: 7 / 38;
- shard 7: 27 / 33.

All shards used:
- the same source commit;
- the same package lock;
- the same exact paired artifact;
- the same deterministic dataset seeds;
- the same scientific code blobs.

Combined with 224/224 exact dataset regeneration, this pattern is consistent with insufficient numerical reproducibility in the fit/bootstrap optimization path across execution environments.

That is a diagnostic interpretation, not a claim that a specific BLAS library or CPU instruction is proven to be the cause.

## Why the gate is not relaxed

The C1 contract was frozen before execution.

It required exact first-199 attempt-sequence hashes because a future sequential continuation must be the same stochastic process as the retained prefix.

Relaxing the hash requirement after observing 120/224 would redefine the gate post hoc.

Likewise, increasing the observed-statistic tolerance would not solve the 60 runs that are already within 1e-10 but still have different attempt hashes.

Therefore:
- no tolerance is widened;
- no seed is changed;
- no favorable subset is selected;
- no Stage-C2 stream is continued.

## Scientific implication

The retained bootstrap result remains valid as the historical computation that was actually performed.

What fails is a stronger claim:

> that the current distributed runner environment can reconstruct enough hidden numerical fit state to continue those historical bootstrap streams exactly.

The original paired artifact retained:
- dataset identities and fingerprints;
- bootstrap stream seeds;
- observed statistic;
- first-199 bootstrap statistics.

It did not retain all optimizer state needed to bypass refitting the original restricted model when continuing the parametric bootstrap.

Therefore exact continuation cannot currently be qualified by reconstruction alone.

## Next gate

The next step is a separate numerical-reproducibility / resumable-bootstrap-state redesign.

That gate should determine prospectively whether to:

1. make the fitter sufficiently reproducible under a controlled execution environment; and/or
2. retain the exact fitted restricted-model state required to resume a bootstrap stream without re-solving the original observed fit; and
3. verify reproducibility of bootstrap fits themselves on identical bootstrap datasets.

No new bootstrap draw beyond index 198 should be generated while this redesign is unresolved.

## Boundary

`STAGE C1 = FAILED CLOSED`

`DATASET REPRODUCTION = 224 / 224 EXACT`

`FIRST-199 BOOTSTRAP SEQUENCE REPRODUCTION = 120 / 224 EXACT`

`STAGE C2 = BLOCKED`

`N_MAX 10000 POLICY = NOT EXECUTED`

`RETROSPECTIVE TOLERANCE RELAXATION = NOT ALLOWED`

`NEW BOOTSTRAP DRAW INDEX >=199 = NOT AUTHORIZED`

`FIXED DRAW COUNT = NOT SELECTED`

`POWER = NOT VALIDATED`

`AUTHORITATIVE CORE GRID / HUMAN N = NOT FROZEN`

`PARTICIPANT RECRUITMENT = NOT AUTHORIZED`

`RUNTIME F1B = NOT AUTHORIZED`
