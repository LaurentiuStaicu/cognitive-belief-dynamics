# F1b R2 paired inference-method cost characterization — 2026-09-28

Issue: #259

Status: **OPERATIONAL PASS / ALL FOUR INFERENCE VARIANTS ELIGIBLE FOR PROSPECTIVE PAIRED CHARACTERIZATION / NO METHOD SELECTED**

## Purpose

Measure operational stability and approximate method-call cost before committing to a larger paired method-characterization matrix.

This stage does not estimate calibration, specificity, detection probability or power.

## Frozen source

The exact retained homogeneous H1 source was reused:
- artifact ID `10961527329`;
- JSON SHA-256 `618b52162e98d25d41ac9cc7a6411ccfbf3c95775412a46b759e1514e90ed37e`;
- evaluation replicate 0 only;
- same 3 datasets / 4 restriction runs as the earlier paired smoke;
- missingness 0.

No new scientific dataset was introduced.

## Inference variants

Exactly four variants were executed:
- `POPULATION`;
- `HIERARCHICAL_0.5X`;
- `HIERARCHICAL_1X`;
- `HIERARCHICAL_2X`.

Each method × restriction run used:
- 199 bootstrap attempts;
- minimum 180 successful attempts;
- the same observed scientific dataset;
- method-specific bootstrap namespace;
- common random numbers across the three hierarchical scale variants.

`HIERARCHICAL_1X` was required to reproduce the retained H1 complete 199-attempt sequence exactly.

## Execution provenance

Temporary execution:
- PR #263 — closed unmerged;
- workflow run `36436783347`;
- execution head `b0081a88d947b50940044e41412d49f8a6be6fb1`;
- qualified main baseline `58f7f21b7e04188d00141ab9e62e9f32b5acf2cf`.

Artifact:
- ID `10975124614`;
- ZIP SHA-256 `adfbe78bb715681a1c38ef529f61fa25138d2b92ae2f47a0212160d003497d51`;
- result JSON SHA-256 `84be8c916b8d5b90f4163bb58c468e026ebb17a4d104ab537a51fe644fc9123a`;
- result JSON size: 24,170 bytes;
- runtime OpenBLAS: `Haswell, Haswell`.

## Operational result

Every inference variant executed:
- 4 restriction runs;
- 796 attempted bootstrap draws;
- 796 successful bootstrap refits;
- 0 bootstrap fit failures;
- 0 calibration failures.

Total operational failures:
- 0.

`HIERARCHICAL_1X`:
- complete 199-attempt H1 prefix exact on all 4 restriction runs.

Therefore all four inference variants remain operationally eligible for a prospective paired scientific characterization.

## Cost profile

One-time design/dataset preparation:
- 74.3306 s.

Method-call totals over the same 4 restriction runs:

### POPULATION
- total: 9.7003 s;
- 0.01219 s per attempted bootstrap draw.

### HIERARCHICAL_0.5X
- total: 15.2305 s;
- 0.01913 s per attempted bootstrap draw.

### HIERARCHICAL_1X
- total: 15.0619 s;
- 0.01892 s per attempted bootstrap draw.

### HIERARCHICAL_2X
- total: 16.6596 s;
- 0.02093 s per attempted bootstrap draw.

The population comparator is faster in this small operational sample, but cost is not a method-selection criterion.

The timing profile must not be extrapolated mechanically to the full future simulation matrix; one-time design generation, runner variation and later missingness/data-generation work are distinct costs.

## Interpretation

This stage establishes:
- all four variants can execute cleanly;
- 0.5× / 1× / 2× hierarchical scale sensitivity is computationally feasible;
- the population comparator is computationally feasible;
- deterministic pairing/common-random-number comparison is feasible;
- the current 1× hierarchical lineage remains exactly reproducible.

It does not establish:
- population superiority;
- hierarchical superiority;
- false-rejection control;
- specificity;
- detection probability;
- robustness to missingness 0.15;
- variance-scale scientific robustness;
- validated power;
- evaluation-replicate adequacy beyond the S4 precision calculation.

## Next gate

Freeze a prospective paired method-characterization design before any broader simulation.

That design must:
- retain identical datasets across methods;
- include all four operationally qualified inference variants;
- include missingness 0 and 0.15;
- retain KL 0.001 / 0.002 / 0.003;
- predeclare scientific method-selection criteria;
- retain three-outcome reporting;
- use enough paired evaluation replicates for the method-screening decision while avoiding the full n=100/cell budget until scientifically eligible variants are narrowed.

The later broad characterization target remains n=100 per scientific cell because the S4 worst-case component MCSE criterion is <=0.05.

## Boundary

`PAIRED COST CHARACTERIZATION = PASS / RETAINED`

`ALL FOUR INFERENCE VARIANTS = OPERATIONALLY ELIGIBLE`

`METHOD SELECTED = NO`

`MISSINGNESS 0.15 = NOT YET CHARACTERIZED`

`POWER = NOT VALIDATED`

`N_EVAL BROAD TARGET = 100/CELL / NOT YET EXECUTED`

`AUTHORITATIVE CORE GRID / HUMAN N = NOT FROZEN`

`PARTICIPANT RECRUITMENT = NOT AUTHORIZED`

`RUNTIME F1B = NOT AUTHORIZED`
