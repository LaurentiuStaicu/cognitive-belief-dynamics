# How CEM is validated

## Central idea

A model can be implemented correctly and still be scientifically weak. CEM therefore separates several questions that are often blurred together: does the software do what the specification says; can the model reproduce relevant empirical patterns; does a new mechanism explain something a simpler model cannot; are parameters identified by data; does the model generalize beyond the cases used to build it; and is it adequate for the purpose for which someone wants to use it?

[[CONCEPT:odd]] · [[CONCEPT:model-validation]] · [[VAL:VAL.M0.001]] · [[VAL:VAL.M1.003]] · [[CODE:registry.validate_model_dir]] · [[VIEW:process]] · [[VIEW:reference]]

## Verification is not validation

Software verification asks questions such as: does a function stay inside its declared domain? Does a fixed random seed reproduce the same run? Do Registry references resolve? Does the web build compile? Do exported reference runs reproduce byte-for-byte where that is required?

These tests are indispensable because a scientific argument cannot survive an implementation bug. But passing them establishes only that the implemented model behaves according to its specification. It does not establish that the specification is a good account of human cognition.

Scientific validation asks different questions: does the model reproduce observations that matter for its stated purpose, under constraints that make trivial solutions difficult?

## Pattern tests and empirical targets

CEM stores empirical findings as **targets**, not automatically as parameters. A target can be directional, ordinal, qualitative or quantitative. For example, [[VAL:VAL.M0.001]] tests a repetition pattern, while [[VAL:VAL.M1.003]] tests heterogeneity in the presentation-framing × congruence relation.

A model that reproduces a target has passed one test. It has not been proven true. Different mechanisms can generate the same aggregate output, and a flexible model can sometimes fit a pattern for the wrong reason.

That is why CEM also exposes intermediate trajectories. If familiarity, corrective accessibility or source reliability is supposed to mediate an effect, the internal path should behave coherently rather than only the final number matching.

## Empirical target versus parameter

A published effect size may constrain what the model ought eventually to reproduce, but it does not become a simulator coefficient by copying the number.

If a study reports an 18-percentage-point difference, inserting 0.18 into an internal coefficient with a different scale and meaning would be invalid. Calibration requires an observation model linking latent simulator states to measured variables, a dataset, an estimation procedure, uncertainty quantification and evaluation on information not used to fit the parameters.

Alpha 0.4.1a1 is not calibrated in that sense.

## Nested nulls and model discrimination

A new mechanism is more informative when it predicts something that a simpler model cannot reproduce while all other relevant conditions remain controlled.

M1.E1 therefore includes a null in which editorial selection is disabled and every condition receives the same information set. M1.E2 compares NULL, FRAME_ONLY and FRAME_CONGRUENCE. These are **nested comparisons**: the more complex model should earn its additional component by reproducing a differential pattern that the smaller model misses.

A nested null does not prove that the added mechanism is the unique cause. It shows that, within the simulator, the declared difference depends on that component. **Model discrimination** then requires empirical data capable of favoring one candidate explanation over another.

## Calibration, estimation and uncertainty

Calibration asks which parameter values are supported by data. It is different from choosing plausible values for demonstration.

A defensible calibration workflow needs at least:
- a clear mapping from model states to observed measurements;
- data with known measurement properties;
- an estimation method;
- parameter uncertainty;
- checks for confounding or non-identifiability;
- predictive evaluation on held-out or genuinely external data.

CEM's current reference coefficients satisfy none of these requirements as population estimates. They are useful because they make the mechanisms inspectable, not because their numerical values describe a country or a person.

## Identifiability and sensitivity

A parameter is **practically identifiable** when the available data and design constrain it sufficiently for the intended inference. **Structural identifiability** is a stronger mathematical question about whether distinct parameter values can, in principle, produce indistinguishable observations under an idealized design.

CEM currently has local sensitivity and practical-identifiability diagnostics. They can reveal that several parameter combinations produce similar behavior around a reference configuration. They do not prove structural identifiability and do not provide posterior distributions.

Sensitivity analysis answers another question: if a parameter or assumption changes within a plausible range, how much does the conclusion change? A result that reverses under small perturbations deserves less confidence than one that is stable across a justified range.

## External validity and transport

A mechanism supported in one task, population, country or platform may not transfer unchanged to another. The chapters on framing, algorithms and interventions repeatedly emphasize this point because many findings are context-dependent.

External validation should therefore preserve the relevant moderators rather than ask only whether “the effect replicates”. A future CEM calibration may need hierarchical or context-specific parameters rather than one global coefficient.

The model should also distinguish **failure to generalize** from **failure of the mechanism itself**. A mechanism may be valid under narrower activation conditions than originally assumed.

## Triangulation and competing explanations

Confidence increases when different sources of evidence converge: controlled experiments, field experiments, longitudinal data, behavioral traces and independent replications can constrain different parts of a model.

But triangulation is not vote counting. Two studies that measure the same proxy with the same confound do not become independent evidence merely because there are two of them.

CEM should prefer evidence that helps distinguish mechanisms. A negative result is scientifically valuable when it can remove, narrow or revise a candidate component instead of merely prompting another free parameter.

## ODD, TRACE and provenance

[[CONCEPT:odd]] provides a standardized description of purpose, entities, processes, scheduling, design concepts, initialization, inputs and submodels. The 2020 ODD update explicitly discusses the need to document model rationale and fitness for purpose. TRACE complements this by recording modelling decisions, alternatives and evaluation steps.

[[VIEW:process]] exposes Visual ODD. [[VIEW:reference]] exposes variables, evidence, limitations and evidence snapshots. Published runs and provenance hashes help verify that the interface displays outputs generated by the declared model.

Documentation improves reproducibility, but documentation itself is not empirical validation.

## Fitness for purpose

Validity is not a single universal badge. A model can be adequate for one purpose and inadequate for another.

M0 may be useful for demonstrating mechanism interactions and regression-testing qualitative patterns while being wholly unsuitable for estimating the prevalence of a belief in Romania. M1 may discriminate candidate mechanisms in controlled synthetic tasks while being unsuitable for recommending a real platform policy.

Every release should therefore state:
- the questions it is designed to answer;
- the level at which its claims apply;
- the data that constrain it;
- the important mechanisms it omits;
- the uses for which it should not be treated as valid.

## What would increase confidence

Confidence in CEM would increase through preregistered external validation, independent datasets, direct measurement of key constructs, calibrated observation models, explicit uncertainty, out-of-sample prediction, competing-model comparisons and successful replication by others.

It would increase even more if some plausible mechanisms were rejected. A model that can only grow and never lose a component is difficult to falsify.

## What this chapter does not claim

“All tests are green” does not mean “the theory is true”. A green CI run supports technical integrity and the reproducibility defined by the test suite. Scientific status depends on the quality of evidence, discriminative tests, calibration, generalization and fitness for the intended purpose.
