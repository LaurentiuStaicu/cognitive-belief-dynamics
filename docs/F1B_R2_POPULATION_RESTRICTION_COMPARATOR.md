# F1b R2 population-level restriction comparator

Issue: #259

Status: **IMPLEMENTATION PROTOTYPE / NON-AUTHORITATIVE / NO METHOD SELECTION**

## Purpose

Provide a population-level inference counterpart to the existing hierarchical R2 restriction engine.

The scientific restrictions are unchanged:
- ADD restriction → AP-B;
- CBD-complement restriction → AP-A;
- encompassing general surface → AP-C.

The purpose is to support a future paired comparison of inference paradigms on exactly the same synthetic datasets.

## Population inference

The population comparator uses the existing fixed-effect fitter:

`fit_r2_candidate`

and therefore estimates no participant/item random effects.

For a restriction pair:
- fit the restricted family;
- fit AP-C to the same observations;
- define the observed improvement statistic as:
  `logLik(AP-C) - logLik(restricted)`;
- fail closed if numerical optimization violates nesting beyond tolerance.

No chi-square reference is introduced.

## Parametric bootstrap

Calibration is performed under the fitted population restricted model.

Bootstrap datasets:
- preserve the exact observed design coordinates;
- preserve participant and item identifiers only as design metadata;
- include no participant/item random-effect terms;
- use Bernoulli responses generated from the restricted population fitted probabilities.

Population bootstrap streams use a dedicated deterministic method namespace so they cannot collide with the existing hierarchical bootstrap stream.

## Held-out diagnostics

The same crossed split contract is retained:
- held-out participant;
- held-out item.

Because the population model has no grouping-level effects, prediction for held-out grouping levels requires no random-effect substitution.

Held-out participant/item log-likelihood deltas remain secondary diagnostics.

## Future paired method comparison

The future S5 comparison must:
- generate a scientific dataset once;
- retain participant/item heterogeneity in the generator;
- apply population and hierarchical inference variants to the same dataset;
- keep missingness masks and scientific seeds identical across inference methods;
- use method-specific bootstrap namespaces;
- retain fit/bootstrap failures explicitly.

Thus the population comparator is allowed to be scientifically misspecified relative to a random-effect generator. That misspecification is part of the inference-method comparison and must not be hidden by simulating a different observed dataset for the population method.

## Boundary

This implementation does not:
- select population over hierarchical inference;
- validate Type-I error or power;
- freeze evaluation replicates;
- freeze bootstrap effort;
- change the existing hierarchical engine;
- add an external dependency;
- freeze a core grid or human N;
- authorize recruitment or runtime F1b.

Next step after CI-green merge:
- execute a small paired smoke on identical datasets;
- verify method-specific bootstrap namespaces and diagnostics;
- characterize computational cost before freezing the paired method-characterization run.
