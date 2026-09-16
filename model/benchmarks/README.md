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
