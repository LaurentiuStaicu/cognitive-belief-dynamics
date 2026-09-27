# F1b Recovery Characterization Result — 2026-09-27

Status: **NON_AUTHORITATIVE / NEGATIVE CHARACTERIZATION RESULT**

Source commit: `938f72789e883ff5e98c4edc58ffbf3ced84fc93`

## What was run

The integrated characterization design was executed with:
- 3 replicates per cell;
- WEAK / MODERATE / STRONG separation;
- 0% / 15% missingness;
- population-level fitting;
- hierarchical fitting at 0.5× / 1× / 2× assumed random-effect scales;
- all R1 and R2 candidate generators.

The same synthetic dataset was supplied to all inference variants within each replicate.

The retained full result contains 144 grid rows and 108 hierarchical-vs-population comparisons.

## Main result

The experiment does **not** justify freezing an authoritative recovery grid.

### R1

Mean correct recovery:
- population: 0.4815;
- hierarchical 0.5×: 0.4074;
- hierarchical 1×: 0.3704;
- hierarchical 2×: 0.1667.

The dominant outcome is `INCONCLUSIVE`, not fit failure.

No R1 inference variant shows a robust overall advantage. Over-penalized 2× hierarchical fitting materially reduces recovery and increases inconclusive results.

### R2

Mean correct recovery:
- population: 0.0926;
- hierarchical 0.5×: 0.0741;
- hierarchical 1×: 0.0926;
- hierarchical 2×: 0.1111.

No R2 variant has any cell meeting the provisional 0.80 recovery convention.

The result is overwhelmingly `INCONCLUSIVE`, with a small number of wrong-model selections. AP-C MODERATE repeatedly selects AP-A in some replicates across inference variants.

## Important negative finding

There are **no fit-failure cells** in this characterization.

Therefore the immediate problem is not solver instability. It is insufficient mechanism discrimination under the current small design, candidate geometry and strict three-way selection rule.

## Inference-method consequence

The penalized hierarchical prototype is **not sufficient for authoritative use** on this evidence.

A better next step is not to relax `INCONCLUSIVE` or post-hoc tune the existing grid. The next methodological gate should:
1. increase non-authoritative replication/design resolution;
2. diagnose which of AIC / held-out participant / held-out item causes disagreement;
3. preserve the current candidate families and negative controls while diagnosing identifiability;
4. compare a prospectively frozen marginal/Laplace route against the current conditional/MAP prototype;
5. only then reconsider an authoritative core/stress grid.

Recent GLMM methodology reinforces this caution: approximate conditional/PQL and Laplace-type inference can behave differently in binary mixed models, and practical identifiability should guide experimental design rather than be assumed from successful optimization.

## Integrity and provenance

Full compressed result:
`model/results/f1b_recovery_characterization_result_2026-09-27.json.gz`

Uncompressed result SHA-256:
`daae1845d3131b81090192bb691136f4aed8d4dddded5a1a1e12caa2a9cd07c1`

The summary JSON records Git blob SHAs for the exact code/config surfaces used.

## Gate

`authoritative core grid = NOT FROZEN`

`human N = NOT FROZEN`

`participant recruitment = NOT AUTHORIZED`

`runtime F1b = NOT AUTHORIZED`
