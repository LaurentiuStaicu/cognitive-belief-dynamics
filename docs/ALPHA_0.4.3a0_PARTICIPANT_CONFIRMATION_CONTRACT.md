# Alpha 0.4.3a0 Phase J — prospective 200-replicate participant confirmation contract

Status: prospective confirmation contract and tooling only. Confirmation execution is blocked until Phase I is merged.

## 1. Purpose

Phase I screened 72 participant-aware cells at 50 replicates per cell.

The screen reduced the design space but was intentionally too small to support a human-study design decision.

Phase J freezes the confirmation surface **before** any 200-replicate confirmation is run.

This prevents post-hoc selection of convenient parameter cells.

## 2. Source screening result

Phase I screening:

- 72 / 72 cells passed the 0.80 point-estimate screening convention;
- global minimum recovery = 0.88;
- no decisive wrong-family selections;
- P64_X10 had the strongest allocation profile:
  - minimum recovery = 0.96;
  - mean recovery = 0.9911;
  - mean inconclusive = 0.0089.

These observations nominate P64_X10 for confirmation; they do not prove that it is the optimal human-study allocation.

## 3. Frozen confirmation surface

Total confirmation cells:

`29`.

### Primary surface

All 18 P64_X10 screening cells:

- 3 heterogeneity regimes;
- 3 memory regimes;
- 2 generators.

No P64 cell may be dropped after seeing confirmation results.

### Boundary surface

For each non-selected allocation and each generator family, Phase J includes **every cell tied for the lowest screening recovery**.

This produces 11 boundary cells:

P40_X16:
- EVSD: low × weak;
- 2HT: high × strong;
- 2HT: low × weak;
- 2HT: moderate × medium;
- 2HT: moderate × strong.

P80_X8:
- EVSD: low × weak;
- 2HT: low × weak.

P128_X5:
- EVSD: low × weak;
- 2HT: high × strong;
- 2HT: moderate × medium;
- 2HT: moderate × strong.

The rule is:

`INCLUDE_ALL_TIES`.

There is no arbitrary tie-break after screening.

## 4. Replication level

Every frozen confirmation cell uses:

`200` independent recovery replicates.

This matches the confirmation level declared in Phase H before screening execution.

No authoritative run may use the CLI replicate override.

## 5. Cell-specific deterministic RNG

Confirmation will be parallelized.

To prevent job scheduling from changing random streams, each cell has an independent deterministic seed:

`seed_cell = uint32(first 8 hex digits of SHA256(base_seed | cell_id | phase-j-v1))`.

Base seed:

`20260916`.

Thus rerunning a cell produces the same synthetic train/held-out sequence regardless of shard order.

## 6. Formal confirmation gate

The existing CEM convention remains the formal rule.

For every one of the 18 primary P64_X10 cells:

`recovery_probability >= 0.80`.

All 18 must pass.

This is the authoritative Phase J point-estimate gate.

Boundary cells are diagnostic. A failed boundary cell does not mathematically invalidate P64_X10, but it must be reported and constrains claims about other participant/trial allocations.

Wrong-family and inconclusive rates remain separate outputs and may not be collapsed into a single hidden error measure.

## 7. Monte Carlo precision sensitivity

For every confirmation cell Phase J also reports a 95% Wilson interval for recovery.

Secondary robustness flag:

`Wilson lower 95% bound >= 0.80`.

For P64_X10, Phase J reports whether **all 18** primary cells satisfy this stronger condition.

This is a prospectively defined sensitivity analysis.

It does **not** replace the formal point-estimate gate.

## 8. Parameter recovery

For the true generating family, confirmation continues to report:

- memory-parameter MAE by Hsimp condition;
- sigma_memory MAE;
- sigma_bias MAE.

Successful family recovery does not imply accurate parameter recovery.

Both must remain visible.

## 9. Model-recovery interpretation

Model recovery is a best-case validation.

It asks whether the planned analysis can recover a known synthetic generator when the truth is one of the candidate models.

Passing does not imply:

- EVSD is the true human recognition architecture;
- 2HT is the true human recognition architecture;
- the real cognitive process lies inside either candidate family;
- Pencode is identified.

The parameter regions used for recovery matter, which is why the complete P64 stress grid and lower-recovery boundary cells are retained.

## 10. Hierarchical model retained unchanged

Phase J inherits the Phase H/Phase I participant-aware likelihood:

- participant-level target/foil binomial counts;
- shared participant memory random effect;
- shared participant response-bias random effect;
- 5-point Gauss-Hermite quadrature per random-effect dimension;
- marginal AIC on train;
- marginal predictive log likelihood on a new participant cohort;
- decisive family label only when both diagnostics agree.

The vectorized marginal likelihood is covered by a direct loop-reference equivalence regression test.

## 11. Remaining human-study boundaries

Even a Phase J pass does not immediately authorize recruitment.

The current simulator still excludes:

- item random effects;
- fatigue;
- learning/practice;
- block-order carryover;
- missingness/dropout;
- correlated memory/bias random effects.

A Phase J pass would justify moving from synthetic design validation to **drafting** the human experimental protocol and deciding which of these remaining factors require another prospective simulation gate before recruitment.

## 12. Promotion gate

Phase J tooling may merge only after Phase I is merged and if:

- the 29-cell surface is frozen;
- all P64 cells are present;
- every minimum-recovery boundary tie is included;
- seed derivation is deterministic;
- 200 replicates are fixed;
- formal and Wilson sensitivity rules remain distinct;
- confirmation smoke tests pass;
- no active registry/model/UI/Pencode changes occur;
- release version and evidence snapshot remain unchanged;
- full CI passes.

The 200-replicate confirmation itself is a later explicit execution gate.
