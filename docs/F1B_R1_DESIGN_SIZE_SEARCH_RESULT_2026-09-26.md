# F1b R1 Design-Size Recovery Search Result — 2026-09-26

Status: **NON_AUTHORITATIVE_R1_DESIGN_SIZE_SEARCH_RESULT**

Source scientific commit: `a4ed691e96f49449bdb50d565293da5ce41c61e2`  
Frozen config SHA-256: `0b68b1894ac6127d4be41c41bb46a59d2ce8eb759fa6d772aa6d9579264ae358`  
Replicates per generator × missingness cell: **200**

## Reproducibility verification

The frozen search was executed twice:

1. serial workflow run `36258023526`, artifact `10911018426`;
2. exact 3×3 participant×item matrix workflow run `36258243687`, combined artifact `10911870581`.

The scientific JSON payloads are exactly equal after removing only the matrix-specific provenance field `execution_strategy`.

The retained JSON is the unmodified serial-run result. No replicate override was used in either execution.

Serial artifact digest:
`sha256:71af82e849f3ddc2c8201b427c2925f5b8bd7b4db64a34979ae1369f4b5ffd02`

Matrix artifact digest:
`sha256:d7d05355cf9666fb997fbd697df70638c9033f2698eb14370550b293ecff3c39`

## Prospective gate

A participant×item × inference design is eligible only if all six STRONG cells
(SR-A/SR-B/SR-C × 0%/15% missingness) satisfy the pre-frozen #135/#141 criteria:

- recovery point estimate ≥ 0.80;
- Wilson-95 lower recovery bound ≥ 0.70;
- wrong-model probability ≤ 0.05;
- fit-failure probability ≤ 0.01.

Passing means only eligibility for later core-grid design work.

## Result

Eligible POPULATION designs:

`24×96, 48×48, 48×96, 96×48, 96×96`

Eligible HIERARCHICAL_0.5X designs:

`24×96, 48×48, 48×96, 96×96`

Eligible HIERARCHICAL_1X designs:

`none`

Eligible HIERARCHICAL_2X designs:

`none`

Pareto frontier — POPULATION:

`24×96, 48×48`

Pareto frontier — HIERARCHICAL_0.5X:

`24×96, 48×48`

No HIERARCHICAL_1X or HIERARCHICAL_2X design passes the frozen gate.

## Design-size summary

| Design | Population min recovery | H0.5 min recovery | Population eligible | H0.5 eligible |
| --- | ---: | ---: | --- | --- |
| 24×24 | 0.655 | 0.585 | NO | NO |
| 24×48 | 0.740 | 0.650 | NO | NO |
| 24×96 | 0.885 | 0.845 | YES | YES |
| 48×24 | 0.705 | 0.530 | NO | NO |
| 48×48 | 0.895 | 0.800 | YES | YES |
| 48×96 | 0.950 | 0.880 | YES | YES |
| 96×24 | 0.720 | 0.480 | NO | NO |
| 96×48 | 0.905 | 0.730 | YES | NO |
| 96×96 | 0.940 | 0.840 | YES | YES |

Across eligible and borderline designs, **SR-B remains the limiting generator**.

At 24×96, HIERARCHICAL_0.5X has:
- minimum recovery = **0.845**;
- minimum Wilson-95 lower bound = **0.788**;
- maximum wrong-model probability = **0.000**;
- fit-failure probability = **0.000**.

At 48×48, HIERARCHICAL_0.5X has:
- minimum recovery = **0.800**;
- minimum Wilson-95 lower bound = **0.739**;
- maximum wrong-model probability = **0.005**;
- fit-failure probability = **0.000**.

## Participants versus items

Under this frozen R1 design, increasing the number of items is markedly more effective than increasing participants alone.

Starting from 24×24:

- POPULATION: increasing items to 96 raises minimum recovery from 0.655 to 0.885 (**+0.230**), whereas increasing participants to 96 at 24 items raises it only to 0.720 (**+0.065**).
- HIERARCHICAL_0.5X: increasing items to 96 raises minimum recovery from 0.585 to 0.845 (**+0.260**), whereas increasing participants to 96 at 24 items changes it to 0.480 (**−0.105**).

Thus 96×96 is eligible for POPULATION and HIERARCHICAL_0.5X but is Pareto-dominated: it adds no new design-eligibility frontier beyond 24×96 and 48×48.

## Inference-method implication

This search does **not** select POPULATION as the final human-analysis method.

It also does not validate the 0.5× hierarchical penalty scale as the final estimator.

Instead it shows:

- the original 24×24 design limitation can be overcome for R1;
- item count is a major design lever;
- HIERARCHICAL_0.5X has eligible synthetic design regions;
- HIERARCHICAL_1X and HIERARCHICAL_2X remain unsuitable under the current conditional/MAP selection scheme;
- inference-method diagnostics under #130 are still required before an authoritative core grid or human design is frozen.

## Scientific boundary

This result does not:

- validate SR-A, SR-B or SR-C as a human mechanism;
- freeze a human participant count;
- freeze an authoritative core/stress grid;
- select a final mixed-effects estimator;
- authorize recruitment or human-data collection;
- authorize runtime F1b;
- change M0 or `source_weight(T)`.

Current gate:

`R1 DESIGN-SIZE SEARCH = COMPLETED / NON-AUTHORITATIVE`

`R1 SYNTHETIC DESIGN REGION = ELIGIBLE EXISTS`

`FINAL INFERENCE METHOD = NOT SELECTED`

`AUTHORITATIVE CORE GRID = NOT FROZEN`

`HUMAN N = NOT FROZEN`

`PARTICIPANT RECRUITMENT = NOT AUTHORIZED`

`RUNTIME F1B = NOT AUTHORIZED`
