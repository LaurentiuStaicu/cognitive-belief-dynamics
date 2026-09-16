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
