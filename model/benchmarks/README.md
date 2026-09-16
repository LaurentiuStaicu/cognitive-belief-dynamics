# Benchmark configurations

This directory contains prospective synthetic validation configurations. These are
not empirical calibration datasets and are not active CEM runtime state.

## M1.E4 candidate recovery

`m1_e4_candidate_recovery_core.json` is the frozen full Phase E configuration
for EVSD-versus-2HT model recovery.

Authoritative execution rules:

- use the committed seed;
- use 200 replicates per core grid cell;
- do not use the CLI `--replicates` override;
- retain the complete JSON output;
- report every generator × memory-regime × trial-count cell;
- do not replace per-cell results with an aggregate average;
- keep `INCONCLUSIVE` as an explicit selection outcome.

The ordinary CI suite runs only a small deterministic smoke benchmark. A green
CI smoke test demonstrates that the benchmark machinery is reproducible and
operational; it does not establish that the full experimental design passes the
0.80 recovery gate.


## Authoritative Phase F result — 2026-09-16

The frozen 200-replicate-per-cell configuration was executed in GitHub Actions
run `35064052116`.

Published persistent summary files:

- `results/m1_e4_candidate_recovery_authoritative_2026-09-16.csv`;
- `results/m1_e4_candidate_recovery_authoritative_2026-09-16.sha256`.

The full GitHub Actions artifact contains the authoritative JSON. Its SHA-256 is:

`c8aad7d5fcab17ddc114b0a0e1776e576e30056e21f0307fbb0a32722128cea7`.

Result:

- minimum cell recovery: `0.225`;
- 17 / 24 grid cells below `0.80`;
- best tested trial-count design (320 target + 320 foil per operating point):
  5 / 6 generator × regime cells pass;
- limiting cell: EVSD weak at `0.745`, with only `0.005` wrong selection and
  `0.250` inconclusive.

Verdict:

`DESIGN_NOT_YET_ADEQUATELY_DISCRIMINATING`.

No empirical model selection is authorized by this result.


## Authoritative Phase G trial-count refinement — 2026-09-16

The controlled trial-count refinement was executed in GitHub Actions run
`35065350252` from workflow commit
`5094b9fa90093ad695ddbef7a290843628f647eb`.

Authoritative JSON SHA-256:

`80635b2e44eb0991fe8db446c163a0a2c3ff9dbab8396342098bdba6f72694b4`.

The refinement preserved seed, 200 replicates, recovery threshold, five
operating points, memory grids and model-selection rule. Only aggregate
target/foil response count per operating point changed to 480 / 640 / 960.

Results:

- 480+480: minimum recovery `0.835`, 6/6 cells pass;
- 640+640: minimum recovery `0.920`, 6/6 cells pass;
- 960+960: minimum recovery `0.945`, 6/6 cells pass;
- overall targeted minimum: `0.835`;
- all 18 targeted cells pass the predeclared `0.80` point-estimate convention.

The limiting 480 EVSD-weak cell is 167/200 recovered. Because its secondary
Wilson 95% Monte Carlo interval includes 0.80, the results report 640+640 as the
more robust provisional aggregate design anchor; this interval criterion is a
post-result sensitivity analysis and is not substituted for the preregistered
point-estimate gate.

The benchmark counts are aggregate response counts, not a per-participant trial
requirement. Human-data collection remains blocked pending participant-aware /
hierarchical design recovery.


## Participant-aware hierarchical screening

`m1_e4_participant_aware_screening.json` translates the Phase G aggregate
640-target + 640-foil cell anchor into repeated-measures participant allocations.

Candidate allocations:

- 40 participants × 16 target + 16 foil responses per Hsimp×bias cell;
- 64 × 10+10;
- 80 × 8+8;
- 128 × 5+5.

All preserve the same aggregate cell totals.

The simulator adds participant-level memory and response-bias random effects
shared across the participant's repeated Hsimp/bias measurements. Candidate fits
use participant-level binomial counts and marginalize those random effects with
Gauss-Hermite quadrature.

Phase H uses a staged recovery design:

- screening: 50 replicates across the complete 72-cell allocation ×
  heterogeneity × memory × generator grid;
- confirmation: 200 replicates for selected/worst cells before any human
  protocol is designed.

The screening result is not authorization for human data collection.


## Authoritative Phase I participant-aware screening — 2026-09-16

The participant-aware 72-cell screen was completed from the Phase H model using
50 replicates per cell.

Persistent result files:

- `results/m1_e4_participant_screening_authoritative_2026-09-16.csv`;
- `results/m1_e4_participant_screening_authoritative_2026-09-16.sha256`.

Authoritative decision surface:

- 72 / 72 cells pass the 0.80 screening convention;
- global minimum recovery = `0.88`;
- no decisive wrong-family selections;
- EVSD generator: 1780 / 1800 EVSD, 0 / 1800 2HT, 20 inconclusive;
- 2HT generator: 1751 / 1800 2HT, 0 / 1800 EVSD, 49 inconclusive.

Allocation minima:

- P40_X16: 0.94;
- P64_X10: 0.96;
- P80_X8: 0.90;
- P128_X5: 0.88.

P64_X10 is therefore nominated for 200-replicate confirmation across its entire
18-cell stress grid. Screening alone does not authorize a human protocol.

The marginal-likelihood implementation was vectorized for computational
feasibility. A repository test compares the vectorized calculation directly
against a loop-based reference for both candidate families. Separate CI runs can
show tiny floating-point differences in continuous optimizer estimates, so Phase I
records decision-level reproducibility rather than falsely requiring bitwise
identity of optimized parameter values.


## Phase J prospective 200-replicate confirmation

`m1_e4_participant_confirmation_200.json` freezes the confirmation surface
before any 200-replicate execution.

Selection:

- all 18 P64_X10 cells;
- all minimum-recovery boundary ties for each non-selected allocation and
  generator family;
- total = 29 cells.

Every cell receives a deterministic SHA-256-derived random seed so parallel job
ordering cannot alter its synthetic stream.

Formal gate:

- all 18 P64_X10 cells must have observed recovery >= 0.80 at 200 replicates.

Secondary sensitivity:

- report the 95% Wilson interval per cell;
- report whether all 18 P64 cells have Wilson lower bound >= 0.80;
- this does not replace the formal point-estimate gate.

Phase J is prospective tooling only until Phase I is merged. Confirmation
execution and human-protocol design remain blocked.


## Authoritative Phase J participant confirmation — 2026-09-16

The frozen 29-cell Phase J confirmation was executed from hardened `main`
commit `76aca60beb49a4e2ce5d96abaa564a67282ba811` in GitHub Actions run
`35081097627`.

Persistent files:

- `results/m1_e4_participant_confirmation_authoritative_2026-09-16.json`;
- `results/m1_e4_participant_confirmation_authoritative_2026-09-16.provenance.json`;
- `results/m1_e4_participant_confirmation_authoritative_2026-09-16.sha256`;
- `results/m1_e4_participant_confirmation_authoritative_2026-09-16.shards.sha256`.

Authoritative JSON SHA-256:

`88c16c2143e7131a4ec8915dbb726ece7e859a797162df173b89743837335f89`.

Result:

- all 18 primary P64_X10 cells pass the formal 0.80 recovery gate;
- primary minimum recovery = `0.92`;
- all 18 primary cells also have Wilson 95% lower bound >= 0.80;
- minimum primary Wilson lower bound = `0.8740105117`;
- boundary minimum recovery = `0.885`;
- across all 5,800 replicates: 5,662 correct-family, 3 wrong-family and
  135 inconclusive selections.

The limiting primary cell is P64_X10 × low heterogeneity × EVSD × weak memory
(184/200 correct, 1 wrong-family, 15 inconclusive).

This is a synthetic model-recovery result. It does not select EVSD or 2HT as
human truth, identify Pencode, or authorize participant recruitment. The next
scientific task is prospective human-protocol robustness work addressing which
currently omitted factors require additional frozen simulation gates.
