# F1b Recovery Characterization Result — 2026-09-26

Status: **NON_AUTHORITATIVE_CHARACTERIZATION_RESULT**

Scientific source commit: `938f72789e883ff5e98c4edc58ffbf3ced84fc93`

Replicates per cell: **3**

This retained run does not freeze the authoritative core grid, human N, or the final inference method.

## Aggregate recovery by problem and inference

| Problem | Inference | N synthetic replicates | Correct | Wrong | Inconclusive | Fit failure |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| R1 | HIERARCHICAL_0.5X | 54 | 0.407 | 0.000 | 0.593 | 0.000 |
| R1 | HIERARCHICAL_1X | 54 | 0.370 | 0.019 | 0.611 | 0.000 |
| R1 | HIERARCHICAL_2X | 54 | 0.167 | 0.019 | 0.815 | 0.000 |
| R1 | POPULATION | 54 | 0.481 | 0.019 | 0.500 | 0.000 |
| R2 | HIERARCHICAL_0.5X | 54 | 0.074 | 0.037 | 0.889 | 0.000 |
| R2 | HIERARCHICAL_1X | 54 | 0.093 | 0.037 | 0.870 | 0.000 |
| R2 | HIERARCHICAL_2X | 54 | 0.111 | 0.056 | 0.833 | 0.000 |
| R2 | POPULATION | 54 | 0.093 | 0.037 | 0.870 | 0.000 |

## Moderate separation, no missingness

| Problem | Generator | Inference | Correct | Wrong | Inconclusive | Fit failure |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| R1 | SR-A | HIERARCHICAL_0.5X | 0.333 | 0.000 | 0.667 | 0.000 |
| R1 | SR-A | HIERARCHICAL_1X | 0.333 | 0.000 | 0.667 | 0.000 |
| R1 | SR-A | HIERARCHICAL_2X | 0.000 | 0.000 | 1.000 | 0.000 |
| R1 | SR-A | POPULATION | 0.667 | 0.000 | 0.333 | 0.000 |
| R1 | SR-B | HIERARCHICAL_0.5X | 0.000 | 0.000 | 1.000 | 0.000 |
| R1 | SR-B | HIERARCHICAL_1X | 0.000 | 0.333 | 0.667 | 0.000 |
| R1 | SR-B | HIERARCHICAL_2X | 0.000 | 0.000 | 1.000 | 0.000 |
| R1 | SR-B | POPULATION | 0.667 | 0.000 | 0.333 | 0.000 |
| R1 | SR-C | HIERARCHICAL_0.5X | 0.667 | 0.000 | 0.333 | 0.000 |
| R1 | SR-C | HIERARCHICAL_1X | 0.667 | 0.000 | 0.333 | 0.000 |
| R1 | SR-C | HIERARCHICAL_2X | 0.333 | 0.000 | 0.667 | 0.000 |
| R1 | SR-C | POPULATION | 1.000 | 0.000 | 0.000 | 0.000 |
| R2 | AP-A | HIERARCHICAL_0.5X | 0.000 | 0.000 | 1.000 | 0.000 |
| R2 | AP-A | HIERARCHICAL_1X | 0.333 | 0.000 | 0.667 | 0.000 |
| R2 | AP-A | HIERARCHICAL_2X | 0.333 | 0.000 | 0.667 | 0.000 |
| R2 | AP-A | POPULATION | 0.000 | 0.000 | 1.000 | 0.000 |
| R2 | AP-B | HIERARCHICAL_0.5X | 0.000 | 0.000 | 1.000 | 0.000 |
| R2 | AP-B | HIERARCHICAL_1X | 0.000 | 0.000 | 1.000 | 0.000 |
| R2 | AP-B | HIERARCHICAL_2X | 0.333 | 0.000 | 0.667 | 0.000 |
| R2 | AP-B | POPULATION | 0.000 | 0.000 | 1.000 | 0.000 |
| R2 | AP-C | HIERARCHICAL_0.5X | 0.000 | 0.333 | 0.667 | 0.000 |
| R2 | AP-C | HIERARCHICAL_1X | 0.000 | 0.333 | 0.667 | 0.000 |
| R2 | AP-C | HIERARCHICAL_2X | 0.000 | 0.333 | 0.667 | 0.000 |
| R2 | AP-C | POPULATION | 0.000 | 0.333 | 0.667 | 0.000 |

## Interpretation boundary

Non-authoritative inference characterization only. Population-level and penalized hierarchical recovery are compared on identical synthetic datasets. These results do not freeze an authoritative core grid, human sample size, variance model, empirical mechanism, or F1b runtime behavior.

No scientific promotion is authorized by this run.
