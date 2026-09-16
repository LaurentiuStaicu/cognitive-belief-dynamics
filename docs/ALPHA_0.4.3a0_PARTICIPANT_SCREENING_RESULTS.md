# Alpha 0.4.3a0 Phase I — authoritative participant-aware screening result

Status: authoritative 50-replicate screening result for design reduction. This is **not** a 200-replicate confirmation and does not authorize a human experiment.

## 1. Provenance

Phase H main commit:

`b725e14a8a226e67e1c2bc4f7c82b11dd15442a7`

Vectorized marginal-likelihood implementation:

`f1123a4dce74c2b7c43917fd73d69080102d1799`

Equivalence-test commit:

`f5866784561b163f3a0c4b44ccff6bed146e4347`

Authoritative screening run used for persistent results:

`35069251436`

The run contains 12 allocation × heterogeneity shards, each with all six
generator × memory-regime cells.

The complete 72-cell table is versioned at:

`model/benchmarks/results/m1_e4_participant_screening_authoritative_2026-09-16.csv`.

Per-shard `result.json` SHA-256 checksums are versioned at:

`model/benchmarks/results/m1_e4_participant_screening_authoritative_2026-09-16.sha256`.

## 2. Numerical implementation audit

The original nested Python implementation of the same Gauss-Hermite marginal
likelihood was too slow for the frozen 72-cell screen.

Phase I therefore vectorized the participant × memory-node × bias-node
calculation. The probability model, quadrature nodes, parameterization,
optimizer, seed, candidate families, train criterion and held-out criterion were
not changed.

A regression test compares the vectorized likelihood directly against a
loop-based reference implementation for both EVSD and 2HT.

Two complete vectorized screening runs were also compared.

Their byte-level `result.json` files were not always identical because some
continuous optimizer estimates differed at small floating-point scale. However,
the complete scientific decision surface was identical:

- 72 / 72 cells passed in both runs;
- global minimum recovery was 0.88 in both;
- every allocation had the same minimum recovery;
- generator-selection confusion counts were identical;
- the same cells occupied the lower-recovery boundary.

Therefore Phase I requires **decision-level reproducibility** for this
optimization pipeline rather than pretending that floating-point optimizer
outputs are bitwise invariant across separate CI jobs.

This distinction is documented rather than hiding the numerical variation.

## 3. Frozen screening design

The Phase H contract was preserved:

- aggregate target responses per Hsimp × bias cell: 640;
- aggregate foil responses per Hsimp × bias cell: 640;
- five bias operating points;
- both Hsimp conditions within participant;
- held-out data from an independent new participant cohort;
- five-point Gauss-Hermite quadrature per random-effect dimension;
- 50 screening replicates per cell;
- recovery convention: 0.80.

Participant allocations:

| Allocation | Participants | target + foil / participant / Hsimp×bias cell | Total responses / participant |
| --- | ---: | ---: | ---: |
| P40_X16 | 40 | 16 + 16 | 320 |
| P64_X10 | 64 | 10 + 10 | 200 |
| P80_X8 | 80 | 8 + 8 | 160 |
| P128_X5 | 128 | 5 + 5 | 100 |

Heterogeneity stress regimes:

- low: sigma_memory = 0.10, sigma_bias = 0.10;
- moderate: 0.25 / 0.25;
- high: 0.40 / 0.40.

Each allocation therefore contributes:

3 heterogeneity × 3 memory regimes × 2 generators = 18 cells.

Total:

72 cells.

## 4. Overall screening result

`PARTICIPANT_AWARE_SCREENING_PASS`

All 72 screening cells exceed the existing 0.80 point-estimate convention.

Global minimum recovery:

`0.88`.

There were no decisive wrong-family selections in the complete screen.

Across 1,800 EVSD-generated replicates:

- EVSD selected: 1,780 = 0.9889;
- 2HT selected: 0;
- inconclusive: 20 = 0.0111.

Across 1,800 2HT-generated replicates:

- 2HT selected: 1,751 = 0.9728;
- EVSD selected: 0;
- inconclusive: 49 = 0.0272.

The residual failure mode is therefore inconclusiveness, not systematic
model-family reversal.

## 5. Allocation-level result

| Allocation | Minimum recovery | Cells >= 0.80 | Mean recovery | Mean wrong | Mean inconclusive |
| --- | ---: | ---: | ---: | ---: | ---: |
| P40_X16 | 0.94 | 18 / 18 | 0.9833 | 0.0000 | 0.0167 |
| P64_X10 | **0.96** | **18 / 18** | **0.9911** | **0.0000** | **0.0089** |
| P80_X8 | 0.90 | 18 / 18 | 0.9733 | 0.0000 | 0.0267 |
| P128_X5 | 0.88 | 18 / 18 | 0.9756 | 0.0000 | 0.0244 |

The screening therefore nominates `P64_X10` as the strongest candidate for
confirmation, but screening alone does not establish that it is the optimal
human-study design.

## 6. Boundary cells

The global limiting cell is:

`P128_X5 × low heterogeneity × EVSD × weak memory`

with:

- recovery = 0.88;
- wrong = 0.00;
- inconclusive = 0.12.

The next limiting EVSD cell is:

`P80_X8 × low × EVSD × weak`

with:

- recovery = 0.90;
- wrong = 0.00;
- inconclusive = 0.10.

For P40_X16, the lowest cell is:

`P40_X16 × low × EVSD × weak`

with recovery = 0.94.

For P64_X10, the minimum observed recovery is 0.96.

The lower boundary being concentrated in weak-EVSD/low-heterogeneity regions is
a reason to preserve those regions in confirmation rather than selecting only
the highest average-performing cells.

## 7. Monte Carlo precision

The screening uses 50 replicates per cell, so point estimates are intentionally
coarse.

For the global limiting cell:

`44 / 50 = 0.88`.

Its Wilson 95% interval is approximately:

`0.762–0.944`.

Thus this screening cell passes the preregistered point-estimate threshold but
does **not** demonstrate with high Monte Carlo precision that its underlying
recovery probability exceeds 0.80.

For a 0.96 cell:

`48 / 50 = 0.96`;

the Wilson 95% interval is approximately:

`0.865–0.989`.

This reinforces the Phase H rule: 50-replicate screening reduces the design
space; it cannot authorize a human protocol.

## 8. Proposed 200-replicate confirmation set

The confirmation phase should not merely rerun the global average.

### Selected allocation

Confirm **all 18 cells of P64_X10**:

- all 3 heterogeneity regimes;
- all 3 memory regimes;
- both generator families.

This tests whether the apparent P64 advantage survives increased Monte Carlo
precision across its entire preregistered stress grid.

### Boundary checks from alternative allocations

Additionally confirm the worst EVSD and worst 2HT cell for each non-selected
allocation.

At minimum this includes:

- P40_X16 × low × EVSD × weak;
- the lowest-recovery P40_X16 2HT cell;
- P80_X8 × low × EVSD × weak;
- P80_X8 × low × 2HT × weak;
- P128_X5 × low × EVSD × weak;
- a lowest-recovery P128_X5 2HT boundary cell.

This yields a compact confirmation surface that preserves both candidate
families and the participant-vs-trials trade-off.

The exact tie choice among equally low 2HT cells must be frozen in the Phase J
confirmation contract **before** its 200-replicate execution.

## 9. Why P64_X10 is only a nominee

P64_X10 balances:

- more participants than P40_X16;
- more within-participant responses than P80_X8/P128_X5;
- the highest minimum recovery in screening;
- the highest mean recovery;
- the lowest inconclusive fraction.

But the current simulator still omits item random effects, fatigue, learning,
block-order carryover, missingness/dropout and correlated memory/bias random
effects.

Therefore P64_X10 is a **confirmation nominee**, not an experimental sample-size
recommendation.

## 10. Scientific interpretation

The screening supports one narrow conclusion:

> Under the frozen Phase H participant-random-effect simulator and tested
> parameter grid, redistributing the aggregate 640+640 response target across
> realistic participant allocations does not destroy EVSD-vs-2HT
> discriminability.

It does not show:

- that EVSD is true;
- that 2HT is true;
- that P64_X10 is universally optimal;
- that 64 participants are sufficient for a real experiment;
- that item heterogeneity is negligible;
- that Pencode is identified.

## 11. Phase I gate

Phase I may merge when:

- the 72-cell result table is versioned;
- shard checksums and execution provenance are versioned;
- the loop-vs-vectorized likelihood equivalence test passes in repository CI;
- all 72 screening cells are structurally audited;
- the decision-level reproducibility audit is documented;
- no active scientific registry/runtime/UI/Pencode is introduced;
- version and evidence snapshot remain unchanged;
- full CI passes.

After Phase I merge, the next phase is to freeze the exact **200-replicate
confirmation contract**, not to design or recruit a human sample.
