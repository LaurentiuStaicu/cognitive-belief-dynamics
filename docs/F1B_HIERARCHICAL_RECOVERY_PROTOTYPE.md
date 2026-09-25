# F1b Hierarchical Recovery Prototype

Status: **NON_AUTHORITATIVE_PENALIZED_HIERARCHICAL_PROTOTYPE**

Issue: #130

Baseline main:
`d274c84606a6bec6c57659538db5db48078cb7c8`

## Purpose

The first F1b smoke engine injects participant/item heterogeneity but fits population-level candidate surfaces.

This prototype adds explicit participant/item random-effect terms to the fitting model before any authoritative core-grid or human-N freeze.

## Inference class

The prototype uses penalized conditional/MAP fitting implemented only with NumPy/SciPy.

It is not a final marginal-likelihood GLMM implementation.

Therefore:
- AIC is a provisional conditional complexity diagnostic;
- random-effect penalty scales are externally supplied design hyperparameters;
- variance-component estimation is not yet authoritative;
- no human-study adequacy claim is permitted.

## R1

R1 uses a sparse penalized Gaussian mixed-effects surface with:
- participant random intercept;
- item random intercept;
- participant random slope on the candidate source/evidence contrast;
- item random slope on the same contrast.

The three source-weighting families remain SR-A, SR-B and SR-C.

Unseen participant/item levels are forced to population-level zero random effects during held-out prediction.

## R2

R2 uses penalized logistic mixed-effects fitting with:
- participant random intercept;
- item random intercept;
- participant random reward-context slope;
- item random reward-context slope.

The fixed action families remain AP-A, AP-B and AP-C.

The optimizer uses an analytic gradient and Gaussian random-effect penalties.

Unseen participant/item levels are forced to zero random effects during held-out prediction.

## Required next validation

Before any authoritative recovery grid:

1. characterize candidate recovery under this prototype;
2. vary fitting penalty scales below/matched/above generator heterogeneity;
3. compare population-level smoke and hierarchical-prototype recovery;
4. quantify convergence/boundary behavior;
5. decide whether Laplace/marginal-likelihood refinement is required;
6. freeze the final inference method prospectively.

## Boundary

`authoritative core grid = NOT FROZEN`

`human N = NOT FROZEN`

`participant recruitment = NOT AUTHORIZED`

`runtime F1b = NOT AUTHORIZED`
