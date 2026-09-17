# Alpha 0.4.3a0 Phase M — Prospective Protocol Robustness Stress Gate

Status: **prospective synthetic robustness contract + tooling**. No authoritative Phase M result exists until this contract/tooling is merged to `main` and the frozen matrix is executed from a fresh workflow. This phase does not authorize recruitment, activate M1.E4, introduce `Pencode`, or select EVSD/2HT as the human recognition architecture.

## 1. Aim

Phase K established participant-aware synthetic family recovery under a deliberately bounded model. Phase L then classified the most consequential omitted structures and required a final pre-human synthetic gate.

Phase M asks one narrow question:

> Does the already-frozen EVSD-vs-2HT family-discrimination pipeline remain recoverable in the Phase-K limiting design region when prospectively specified item, dependence, serial-position and missingness misspecifications are introduced into the data-generating process but not granted to the fitted candidate models?

This is a robustness-to-misspecification experiment. It is not a search for nuisance values that make the pipeline pass.

## 2. Frozen scientific boundary

Phase M preserves:

- software version `0.4.3a0` / tag `v0.4.3a0`;
- active model specification `M1`, retained baseline `M0`;
- evidence snapshot `EVIDENCE.M1.2026-09-16.r1`;
- executable M1.E1, M1.E2 and M1.E3 only;
- planned M1.E4 measurement target `Drecog` and raw target/foil responses;
- candidate families `CANDIDATE.M1.E4.C1.EVSD` and `CANDIDATE.M1.E4.C2.2HT`;
- `Pencode` as not identified and not active;
- the Phase-K selection rule: train marginal AIC and held-out marginal predictive log likelihood must agree, otherwise `INCONCLUSIVE`.

The fitted Phase-M candidates intentionally retain the Phase-K participant-only independent-random-effects analysis. The richer nuisance structures exist only in the synthetic generator. This is necessary for a genuine robustness test rather than a test that gives the analysis the answer.

## 3. Why the stress surface is concentrated in the limiting region

Phase K already covered the full P64 participant-aware grid over three participant-heterogeneity regimes, three memory regimes and both generator families with 200 replicates/cell.

The limiting primary cell was:

`P64_X10 × low heterogeneity × EVSD × weak memory`

with recovery `0.92`.

Phase M therefore does **not** repeat the complete Phase-K grid. It keeps the participant allocation, weak-memory regime and low participant heterogeneity fixed and varies only the new Phase-L nuisance axes. Both generator families are evaluated symmetrically.

This is a prospective stress design, not post-hoc deletion of difficult cells.

## 4. Fixed allocation and candidate surface

Allocation:

- `64` participants generated before attrition;
- `10` target and `10` foil responses per participant × Hsimp condition × bias operating point;
- two Hsimp conditions (`complex`, `simple`);
- five bias operating points;
- within-participant bias blocks in independently randomized order;
- independent held-out cohort with independently generated items.

Participant heterogeneity remains the Phase-K low regime:

- `sigma_memory = 0.10`;
- `sigma_bias = 0.10`.

Weak-memory truth remains:

EVSD:

- complex `d = 0.45`;
- simple `d = 0.65`.

2HT:

- complex `Ddet = 0.18`;
- simple `Ddet = 0.28`.

Bias grids remain:

- EVSD `[-0.8, -0.4, 0.0, 0.4, 0.8]`;
- 2HT `[0.15, 0.325, 0.5, 0.675, 0.85]`.

No value above is a population estimate.

## 5. Item heterogeneity generator

Phase K treats all trials inside one participant/condition/bias cell as exchangeable binomial repetitions. Phase M introduces crossed item variability shared across participants.

For every synthetic dataset, distinct target and foil item effects are generated for every Hsimp × bias cell and retained across participants in that dataset.

Two demonstrative stress scales are frozen:

- `ITEM_MODERATE`: memory/item SD `0.15`, response-tendency/item SD `0.15`;
- `ITEM_HIGH`: memory/item SD `0.30`, response-tendency/item SD `0.30`.

For EVSD, item memory effects perturb target/foil evidence separation and item response-tendency effects perturb criterion. For 2HT, item memory effects perturb target/foil detection probability on the logit scale and item response-tendency effects perturb guessing on the logit scale.

These values are **demonstrative stress values**, not empirical estimates of headline or recognition-probe variance.

Held-out prediction uses a new participant cohort **and independently generated items**. Phase M therefore asks for generalization beyond the exact synthetic item realization, while still acknowledging that the fitted model does not contain an explicit item random effect.

## 6. Correlated participant memory/bias random effects

Phase K generates participant memory and response-bias random effects independently. Phase L identified this as an unverified assumption.

Phase M freezes two symmetric dependence stresses:

- `RHO_POSITIVE`: `rho(memory,bias) = +0.50`;
- `RHO_NEGATIVE`: `rho(memory,bias) = -0.50`.

The candidate fitter continues to assume independence. Passing therefore means family recovery tolerates this specific misspecification; it does not estimate the human correlation.

## 7. Serial-position nuisance and randomized block order

All participants receive the five bias operating points in an independently randomized order.

The `SERIAL_DEGRADATION` profile applies a demonstrative latent memory slope of:

`-0.08` per centered block position.

For EVSD this operates multiplicatively on `d`; for 2HT it operates additively on the logit of `Ddet`.

The analysis does not receive a serial-position term. The stress therefore tests whether counterbalanced/randomized order is sufficient for candidate-family recovery under a bounded within-session trend.

The slope is not interpreted as a fatigue coefficient measured in humans. Practice/retest effects are well documented in repeated cognitive assessment, but Phase M uses only a transparent nuisance trend rather than claiming a unique fatigue or learning mechanism.

## 8. Missingness/attrition mechanisms

Phase M tests participant-level attrition before fitting. Trial-level missing responses remain a required field-level distinction in any future human protocol but are not separately parameterized in this final synthetic gate.

Two mechanisms are frozen:

### MAR_LIKE_ATTRITION

Every generated participant has independent dropout probability `0.10`.

This is an approximately ignorable design stress, not a claim that a human study will have 10% attrition.

### LATENT_ASSOCIATED_ATTRITION

Base dropout probability is `0.10`, with participant latent memory standardized effect `z_memory` shifting dropout odds:

`logit(Pdrop) = logit(0.10) - 0.75 × z_memory`

and `Pdrop` is capped at `0.35` for this bounded stress experiment.

Lower latent-memory participants therefore have higher dropout probability. The fitter does not observe the latent selection mechanism.

This is a missing-not-at-random-style sensitivity stress, not an empirical missingness model.

National Academies missing-data guidance motivates prospective missingness assumptions and sensitivity analysis; citing that source does not classify CEM as a clinical trial.

## 9. Frozen nine profiles

Every profile is run once under EVSD truth and once under 2HT truth, giving `18` primary cells.

1. `REFERENCE` — Phase-K generator assumptions.
2. `ITEM_MODERATE` — item SDs 0.15 / 0.15.
3. `ITEM_HIGH` — item SDs 0.30 / 0.30.
4. `RHO_POSITIVE` — participant random-effect correlation +0.50.
5. `RHO_NEGATIVE` — participant random-effect correlation -0.50.
6. `SERIAL_DEGRADATION` — randomized block order + serial memory slope -0.08.
7. `MAR_LIKE_ATTRITION` — independent participant dropout 0.10.
8. `LATENT_ASSOCIATED_ATTRITION` — bounded latent-memory-associated dropout.
9. `COMBINED_ADVERSE` — item SDs 0.30 / 0.30, rho -0.50, serial slope -0.08, latent-associated attrition.

The complete surface is frozen before execution. No profile may be deleted after seeing results.

## 10. ADEMP specification

### Aim

Quantify robustness of candidate-family recovery to prospectively frozen nuisance misspecifications in the Phase-K limiting region.

### Data-generating mechanisms

The nine profiles above, both generator families, fixed P64_X10 allocation, low participant heterogeneity and weak-memory truth.

### Estimands / targets

For each cell:

- correct-family recovery probability;
- wrong-family selection probability;
- inconclusive probability;
- true-family memory-parameter MAE;
- true-family participant heterogeneity MAE;
- retained-participant count diagnostics.

### Methods

Unchanged Phase-K candidate fitting and selection rule. The richer nuisance structures are not added to either candidate fitter.

### Performance measures

- formal recovery pass/fail;
- Wilson 95% interval for recovery;
- Monte Carlo standard error of recovery;
- wrong/inconclusive separation;
- parameter-recovery diagnostics.

## 11. Monte Carlo replication count

Every cell uses `200` independent replicates.

This value is retained for a precision reason rather than inherited mechanically:

- for any Bernoulli proportion, the maximum Monte Carlo standard error at 200 replicates is `sqrt(0.25/200) ≈ 0.0354`;
- at the formal threshold `p = 0.80`, MCSE is `sqrt(0.8×0.2/200) ≈ 0.0283`.

A 95% Wilson interval is reported for every cell. Its lower bound is a **secondary Monte Carlo-precision sensitivity**, not a replacement for the preregistered point-estimate rule.

## 12. Deterministic cell-specific random streams

Base seed:

`20260917`.

For each profile × generator cell:

`seed_cell = uint32(first 8 hex digits of SHA256(base_seed | profile_id | generator | phase-m-v1))`.

Each cell can therefore execute on an independent matrix runner without changing its random stream when job order changes.

## 13. Formal gate and outcome taxonomy

Formal gate:

`recovery_probability >= 0.80`

for **all 18 prospectively frozen cells**.

The authoritative aggregate verdict is:

- `PROTOCOL_ROBUSTNESS_PASS` if all 18 cells pass;
- `PROTOCOL_ROBUSTNESS_FAIL` otherwise.

Wrong-family and inconclusive selections remain distinct.

The Wilson lower-bound >= 0.80 condition is reported separately and cannot retrospectively become the formal gate.

## 14. Interpretation if Phase M passes

A PASS means only:

> Under the frozen synthetic generator families and the specific nuisance regimes tested, the existing participant-aware EVSD-vs-2HT discrimination pipeline retained at least 0.80 correct-family recovery in every Phase-M stress cell.

It does not mean:

- either candidate is true in humans;
- the nuisance values are population estimates;
- P64 is a validated human sample size;
- `Pencode` exists or is identified;
- recruitment is ethically/scientifically authorized;
- M1.E4 should become executable in CEM.

## 15. Interpretation if Phase M fails

A FAIL is scientifically informative and must not trigger post-hoc tuning of the frozen gate.

It means the current prospective human-discrimination design is not robust to at least one predeclared synthetic nuisance profile at the current allocation/analysis.

The failed result must be preserved. CEM may still close M1 at the **pre-human software/research boundary**, explicitly marking the proposed human discrimination design as not recruitment-ready.

A future external validation program could redesign and preregister a human study without blocking application simplification or the remaining conceptual modules.

## 16. Authoritative execution rule

The 200-replicate Phase-M matrix is blocked until:

- this document, config, generator/tooling and regression tests are merged to `main`;
- PR CI is completely green;
- post-merge Verify/CodeQL are green;
- the exact 18-cell matrix and SHA256 seed scheme are versioned.

The authoritative run must execute from a fresh workflow on the merged contract/tooling. Results from smoke runs or failed/partial authoritative attempts are diagnostic only and may not be combined with a later clean run.

## 17. Phase M result integration and M1 closure

After the authoritative run, one result/audit integration must persist:

- all 18 cell results;
- run provenance;
- checksums;
- aggregate PASS/FAIL;
- exact failed cells if any;
- the distinction between formal point-estimate and Wilson sensitivity;
- no winner claim between EVSD and 2HT.

After result integration and green post-merge CI, M1 is to be closed at the scientifically justified **pre-human boundary** unless a separate user decision explicitly starts an external human-validation program.

Closure means:

- M1.E1–E3 remain the active executable M1 surface;
- M1.E4 remains a documented pre-human research program, not active runtime;
- Pencode remains blocked;
- EVSD/2HT remain unresolved candidate families;
- human recruitment remains outside current CEM development;
- application development proceeds to simplification / Simple Mode.

## 18. Forbidden changes

No:

- human recruitment or recruitment authorization;
- ethics/IRB approval claim;
- active M1.E4 variable/link/validation/runtime/UI registration;
- `Pencode` equation or proxy;
- EVSD/2HT winner declaration;
- fitted human coefficient or population calibration;
- modification of M0/M1.E1/M1.E2/M1.E3 equations or outputs;
- version bump;
- evidence-snapshot change;
- post-hoc removal of Phase-M profiles after execution.

Phase M is the last synthetic robustness gate in the current M1 completion track.