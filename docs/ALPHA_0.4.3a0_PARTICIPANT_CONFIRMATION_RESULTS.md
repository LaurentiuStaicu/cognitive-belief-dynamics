# Alpha 0.4.3a0 Phase K — authoritative participant confirmation result

Status: authoritative 200-replicate confirmation result for the frozen Phase J synthetic participant-aware design. This result does **not** select a human cognitive model and does not authorize recruitment.

## 1. Provenance

Optimizer hardening was merged to `main` at:

`76aca60beb49a4e2ce5d96abaa564a67282ba811`.

The authoritative confirmation was then executed from a fresh one-shot workflow commit:

`faa8b4223960bb60dfa10654a7107d4158021f7f`.

GitHub Actions run:

`35081097627`.

The run executed the complete frozen Phase J surface from zero:

- 18 primary `P64_X10` cells;
- 11 boundary cells;
- 29 cells total;
- 200 independent replicates per cell;
- 5,800 recovery replicates total.

Persistent files:

- `model/benchmarks/results/m1_e4_participant_confirmation_authoritative_2026-09-16.json`;
- `model/benchmarks/results/m1_e4_participant_confirmation_authoritative_2026-09-16.provenance.json`;
- `model/benchmarks/results/m1_e4_participant_confirmation_authoritative_2026-09-16.sha256`;
- `model/benchmarks/results/m1_e4_participant_confirmation_authoritative_2026-09-16.shards.sha256`.

Authoritative JSON SHA-256:

`88c16c2143e7131a4ec8915dbb726ece7e859a797162df173b89743837335f89`.

The 29 shard-result hashes are preserved separately.

## 2. Numerical incident and clean rerun

The first attempted confirmation run was diagnostic only: 28/29 cells produced valid outputs, while `P128_X5 × high × 2HT × strong` encountered a SciPy L-BFGS-B line-search termination during pooled 2HT initialization.

The failure was isolated to replication 111 and reproduced on its exact pooled-count surface.

The numerical hardening retained:

- the same likelihood;
- the same 2HT equations;
- the same parameter bounds;
- the same initial point;
- the same data;
- the same random seed;
- the same optimizer family.

Only after an explicit optimizer failure, the identical L-BFGS-B fit is retried with a larger bounded line-search budget (`maxls=100`).

A deterministic regression test forces the first call to fail and verifies the retry on the exact Phase J pooled-count surface.

The authoritative run `35081097627` was then executed **from zero** after the hardening merged. No scientific result from the earlier 28/29 diagnostic run was reused.

The formerly failing boundary cell completed successfully in the authoritative run:

- recovery = 0.995;
- wrong-family = 0.000;
- inconclusive = 0.005;
- Wilson 95% = 0.9722–0.9991.

## 3. Formal Phase J result

Verdict:

`PARTICIPANT_CONFIRMATION_PASS`.

All 18 primary `P64_X10` cells satisfy the formal Phase J gate:

`recovery_probability >= 0.80`.

Primary minimum recovery:

`0.92`.

The limiting primary cell is:

`P64_X10 × low heterogeneity × EVSD × weak memory`

with:

- recovery = 184/200 = 0.92;
- wrong-family = 1/200 = 0.005;
- inconclusive = 15/200 = 0.075;
- Wilson 95% = 0.8740–0.9502.

Thus the formal point-estimate gate passes across the complete P64 stress grid.

## 4. Prospective Wilson sensitivity

Phase J prospectively defined, but did not substitute, a stronger secondary condition:

`Wilson lower 95% bound >= 0.80`.

All 18 primary P64 cells also pass this condition.

The lowest primary Wilson lower bound is:

`0.8740105117`

in the same `P64_X10 × low × EVSD × weak` cell.

Therefore the Phase J result passes both:

1. the authoritative point-estimate gate;
2. the preregistered secondary Monte Carlo precision sensitivity.

The second result strengthens the Monte Carlo precision interpretation but does not redefine the formal gate.

## 5. Primary P64 aggregate

Across the 18 P64 cells:

- total replicates: 3,600;
- correct family recovery: 3,556;
- wrong-family selections: 1;
- inconclusive selections: 43;
- mean cell recovery: 0.9878;
- minimum cell recovery: 0.92.

By generator:

EVSD-generated primary cells:

- 1,779 / 1,800 correct;
- 1 / 1,800 wrong-family;
- 20 / 1,800 inconclusive;
- minimum recovery = 0.92.

2HT-generated primary cells:

- 1,777 / 1,800 correct;
- 0 / 1,800 wrong-family;
- 23 / 1,800 inconclusive;
- minimum recovery = 0.97.

The residual difficulty remains concentrated in the weak-EVSD region rather than showing systematic reversal toward the competing family.

## 6. Boundary diagnostics

All 11 boundary cells also completed.

Boundary minimum recovery:

`0.885`.

The limiting boundary cell is:

`P128_X5 × low heterogeneity × EVSD × weak memory`

with:

- recovery = 177/200 = 0.885;
- wrong-family = 1/200 = 0.005;
- inconclusive = 22/200 = 0.110;
- Wilson 95% = 0.8334–0.9221.

The minimum boundary Wilson lower bound remains above 0.80.

Boundary cells were diagnostic by contract and did not define the formal P64 gate. Their favorable result therefore should not be used retrospectively to redefine the selection rule.

## 7. Complete confusion counts

Across all 29 confirmation cells and 5,800 replicates:

- correct-family selections: 5,662;
- wrong-family selections: 3;
- inconclusive selections: 135.

All three wrong-family selections occurred in low-heterogeneity EVSD-weak cells:

- `P40_X16 × low × EVSD × weak`;
- `P64_X10 × low × EVSD × weak`;
- `P128_X5 × low × EVSD × weak`.

This pattern is reported descriptively. It is not evidence that the true human process belongs to either candidate family.

## 8. Parameter recovery

Phase J also reports parameter-recovery MAE for the true generating family:

- memory parameters by Hsimp condition;
- `sigma_memory`;
- `sigma_bias`.

No parameter-recovery threshold was preregistered as a Phase J pass/fail gate.

Consequently, family-recovery success must not be translated into a claim of exact parameter recovery. The persistent JSON retains every per-cell MAE for later protocol design and stress testing.

## 9. Scientific interpretation boundary

The authoritative confirmation supports the following narrow conclusion:

> Under the frozen Phase H/Phase J synthetic participant-aware simulator, the complete P64_X10 stress grid is recoverable at the preregistered 0.80 convention with 200 Monte Carlo replicates per cell, and every primary cell also has a Wilson 95% lower bound above 0.80.

It does **not** establish:

- EVSD as the true human recognition architecture;
- 2HT as the true human recognition architecture;
- that the real human process lies inside either family;
- that 64 participants are sufficient for a real study;
- that Pencode is identified;
- that omitted design effects are negligible.

## 10. Remaining simulator boundaries

The current participant-aware simulator still excludes:

- item random effects;
- fatigue;
- practice / learning;
- block-order carryover;
- missingness / dropout;
- correlated participant memory/bias random effects.

Phase J passing therefore justifies moving from basic synthetic family-recovery validation to **human-protocol drafting plus prospective robustness decisions**.

It does not yet authorize participant recruitment.

Before recruitment, the project must explicitly decide which omitted factors require another frozen simulation gate and must document the experimental protocol, analysis plan, exclusion/missingness policy and stopping rules prospectively.

## 11. Phase K integration gate

Phase K may merge when:

- the authoritative JSON is versioned byte-for-byte;
- run provenance is versioned;
- the 29 shard checksums are versioned;
- repository tests reproduce the frozen decision summary;
- the exact primary and boundary cell counts are validated;
- the formal and Wilson gates remain distinct;
- no EVSD/2HT active-model registration occurs;
- no Pencode is introduced;
- no recruitment authorization occurs;
- software version remains `0.4.2a0`;
- evidence snapshot remains `EVIDENCE.M1.2026-09-16.r1`;
- full CI passes.

After Phase K, the next scientific task is a prospective human-protocol robustness phase, not model activation.
