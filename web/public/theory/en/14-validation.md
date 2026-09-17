# How an epistemic model is validated

## Central idea

A model can be correctly implemented and still be scientifically weak. CEM separates software verification, pattern reproduction, empirical-evidence mapping, model discrimination, calibration and limitation analysis.

[[CONCEPT:odd]] · [[CONCEPT:model-validation]] · [[VAL:VAL.M0.001]] · [[VAL:VAL.M1.003]] · [[CODE:registry.validate_model_dir]] · [[VIEW:process]] · [[VIEW:reference]]

## Software verification versus scientific tests

Software tests ask questions such as: does a function stay in its declared range; does a seed reproduce a run; are registry references resolvable; does the web build compile? These are necessary but do not establish that a psychological mechanism is correct.

Scientific tests ask whether a model reproduces an externally relevant pattern under constraints that prevent trivial solutions. [[VAL:VAL.M0.001]] tests a repetition pattern; [[VAL:VAL.M1.003]] tests framing × congruence heterogeneity.

## Empirical target versus parameter

A published result can be stored as an empirical target without becoming a simulator coefficient. If a study reports an 18-percentage-point difference, CEM must not silently insert 0.18 into an internal coefficient with a different scale and meaning.

Calibration would require an observation model connecting simulator states to the experimental measure, a dataset, an estimation procedure and out-of-sample checks. Alpha 0.4.1a1 is not calibrated in this sense.

## Nested nulls and model discrimination

A new mechanism is more informative when it produces a prediction the smaller model cannot produce without hidden changes. M1.E1 therefore has a null in which editorial selection is disabled and all conditions receive the same pool. M1.E2 compares NULL, frame-only and frame × congruence.

A nested null does not prove the mechanism. It shows that the simulated effect depends on the declared component. Model discrimination then requires data capable of favoring one account over another.

## Identifiability and sensitivity

CEM includes local sensitivity and practical-identifiability diagnostics. These can expose parameter trade-offs around a reference configuration. They do not establish structural identifiability, produce parameter posterior distributions, or replace empirical calibration.

A model can reproduce a final pattern for the wrong internal reason. Intermediate trajectories therefore matter, not only end outcomes.

## ODD, TRACE and provenance

[[CONCEPT:odd]] gives a standardized description of purpose, entities, processes, design concepts, initialization and submodels. ODD is used to improve clarity and replication. TRACE documents modelling decisions and rejected alternatives.

[[VIEW:process]] shows Visual ODD. [[VIEW:reference]] exposes variables, evidence, limitations and the evidence snapshot. Published runs and provenance hashes allow users to verify that the application displays outputs produced by the declared model.

## Fitness for purpose

Validity is purpose-dependent. M0 can be useful for mechanism demonstration and pattern regression tests without being fit to estimate belief prevalence in a country. M1 can discriminate candidate mechanisms in synthetic tasks without being fit for platform-policy recommendations.

Every release must explicitly state what it is and is not fit for.

## What would increase confidence

Confidence would increase through preregistered external validation, independent datasets, direct construct measurement, calibration with uncertainty, out-of-sample prediction and comparison with simpler rival models. Negative results must be able to remove mechanisms rather than merely add parameters.

## What this chapter does not claim

“All tests are green” does not mean “the theory is true”. Green CI certifies the technical integrity and reproducibility defined by the suite; scientific status depends on evidence, discriminative tests and scope.