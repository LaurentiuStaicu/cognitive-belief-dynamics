# Alpha 0.4.3a0 Phase E — synthetic candidate-recovery benchmark

Status: executable validation benchmark only. It is not an active M1.E4 cognitive mechanism and does not select EVSD or 2HT from empirical data.

## 1. Purpose

Phase D froze the discrimination protocol. Phase E implements the synthetic test that asks whether the planned design and fitting procedure can recover the data-generating candidate family before human data are used for model selection.

The benchmark follows the standard model-recovery workflow:

1. choose a generating model and ground-truth parameters;
2. simulate synthetic recognition data;
3. fit every candidate model to the same synthetic dataset;
4. compare the candidate fits;
5. repeat over many datasets and parameter regimes;
6. summarize generator-versus-selected outcomes as a confusion matrix;
7. evaluate parameter recovery separately.

This is the best-case identifiability test for the planned analysis pipeline.

## 2. Candidate families

The benchmark contains only the two already frozen Phase C candidates:

- EVSD — continuous evidence-strength model;
- symmetric 2HT — discrete detection plus guessing.

The benchmark module lives under calibration/validation code and is not imported into the active CEM simulation path.

## 3. Synthetic design

The full core configuration is:

`model/benchmarks/m1_e4_candidate_recovery_core.json`.

It uses:

- fixed seed: 20260916;
- 200 independent replicates per generator × memory regime × trial-count cell;
- 5 bias operating points per Hsimp condition;
- both complex and simple Hsimp conditions;
- weak, medium and strong memory regimes;
- 40, 80, 160 and 320 target trials **and** the same number of foil trials per operating point.

The trial-count grid is a prospective design sweep, not a recommendation that any one count is sufficient.

## 4. Generator grids

EVSD reference criteria:

`[-0.8, -0.4, 0.0, 0.4, 0.8]`.

EVSD memory pairs (complex, simple):

- weak: (0.45, 0.65);
- medium: (0.90, 1.10);
- strong: (1.35, 1.55).

2HT guessing settings:

`[0.15, 0.325, 0.50, 0.675, 0.85]`.

2HT detection pairs (complex, simple):

- weak: (0.18, 0.28);
- medium: (0.38, 0.48);
- strong: (0.58, 0.68).

These are benchmark stress-test values, not empirical calibration estimates.

## 5. Independent train and held-out datasets

Every replicate generates two independent datasets from the same ground-truth candidate and parameters:

- train;
- held-out.

Both EVSD and 2HT are fit to the train dataset.

This prevents the recovery decision from depending only on the same observations used to optimize parameters.

## 6. Selection rule inside the recovery benchmark

Train diagnostic:

- AIC.

Held-out diagnostic:

- predictive log likelihood.

A replicate receives a decisive model-family label only if **both** diagnostics favor the same candidate.

Otherwise:

`INCONCLUSIVE`.

No universal Delta-AIC cutoff is introduced.

This selection rule is specific to the synthetic recovery benchmark. It does not replace the broader empirical winner rule from Phase D.

## 7. Fitting constraints

For each Hsimp condition:

EVSD fit:
- one shared d across the bias operating points;
- one c per operating point.

2HT fit:
- one shared Ddet across the bias operating points;
- one g per operating point.

The same raw response data are supplied to both fits.

Likelihood surface:

- target hits: binomial;
- foil false alarms: binomial.

## 8. Required recovery outputs

The benchmark returns:

- confusion counts `P(selected label | generator)` numerators;
- normalized confusion probabilities;
- an explicit `INCONCLUSIVE` column;
- recovery/wrong/inconclusive probability for every parameter-grid cell;
- true-family memory-parameter MAE;
- true-family bias-parameter RMSE;
- minimum recovery probability over the whole core grid;
- `all_core_grid_cells_pass`.

A high aggregate average cannot hide a failed weak-memory or low-trial cell.

## 9. Design gate

A design passes the CEM core benchmark only if **every** core grid cell reaches:

`recovery_probability >= 0.80`.

Both generators must pass.

The 0.80 value remains the Phase D CEM design convention, not a universal literature threshold.

If any cell fails, the correct result is:

`DESIGN_NOT_YET_ADEQUATELY_DISCRIMINATING`.

The benchmark should then be rerun after changing design features such as trial count or operating-point placement.

## 10. Parameter recovery remains separate

For the true generating family, Phase E also tracks:

- absolute error of the memory parameter in each Hsimp condition;
- RMSE of the bias parameters.

Model recovery and parameter recovery answer different questions.

A design could correctly identify the model family while estimating some parameters poorly.

## 11. Reproducibility

The benchmark uses a frozen random seed and deterministic optimization settings.

The same configuration and software environment must reproduce the same benchmark JSON.

The CLI is:

`python scripts/run_m1_e4_candidate_recovery.py --config model/benchmarks/m1_e4_candidate_recovery_core.json --output <path>`.

An optional `--replicates` override exists only for smoke/debug runs.

Any authoritative result must use the frozen config value of 200.

## 12. CI smoke benchmark

The ordinary repository CI executes only a very small deterministic benchmark through pytest.

The smoke benchmark verifies:

- both generators simulate;
- both candidates fit;
- the same seed reproduces identical output;
- confusion counts are structurally correct;
- EVSD/2HT/INCONCLUSIVE probabilities sum to one.

The smoke run is **not** an authoritative candidate-recovery result and is not evaluated against the scientific 0.80 gate.

## 13. Interpretation boundary

A successful full benchmark means:

> under the preregistered synthetic parameter grid, the planned experimental design and fitting procedure can usually recover which of the two candidate families generated the synthetic responses.

It does not mean:

- EVSD is true;
- 2HT is true;
- Hsimp truly changes memory;
- Ddet is Pencode;
- d is Pencode;
- human recognition follows either benchmark generator exactly.

## 14. Phase E gate

Phase E may merge only if:

- benchmark contract/schema validate;
- full core config is frozen;
- both generators are implemented only in validation code;
- both candidates are refit to every synthetic dataset;
- train and held-out draws are independent;
- confusion matrix includes INCONCLUSIVE;
- parameter recovery is separately reported;
- per-grid-cell recovery cannot be hidden by aggregation;
- same-seed smoke output is reproducible;
- smoke benchmark completes in CI;
- no active model/registry/UI/Pencode is introduced;
- public version/evidence snapshot remain unchanged;
- full CI passes.

The **full 200-replicate core benchmark is a later execution gate**. Phase E constructs and validates the benchmark machinery; it does not predeclare that the design passes.
