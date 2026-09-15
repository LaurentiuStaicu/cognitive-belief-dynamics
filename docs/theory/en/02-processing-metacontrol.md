# Fast processing, heuristics, deliberation and metacontrol

## Central idea

Reasoning research distinguishes relatively autonomous processing from deliberative processing that places greater demands on working memory. A second, complementary literature studies heuristics: efficient decision procedures that deliberately use only part of the available information. CEM uses both bodies of work cautiously. Neither “fast” nor “heuristic” is a synonym for irrational, and neither “slow” nor “deliberative” guarantees a correct answer.

[[CONCEPT:type1-type2]] · [[MODULE:MOD.02]] · [[MODULE:MOD.09]] · [[MODULE:MOD.15]] · [[VAR:W]] · [[VIEW:reference]]

## Type 1 and Type 2 are processing families, not two brains

Evans and Stanovich argue that a central distinction is the relative autonomy of Type 1 processing and the dependence of Type 2 processing on working memory and hypothetical thinking. The classification is influential, but familiar attributes do not always line up perfectly. Fast is not necessarily irrational, slow is not necessarily correct, and automatic is not synonymous with emotional.

CEM therefore avoids a simple “bad System 1 / good System 2” story. Automatic processing can embody well-learned expertise. Deliberation can rationalize a desired conclusion, operate on poor evidence, or consume resources without improving a decision. Critiques of dual-process theories also caution against treating every behavioral difference as evidence for two sharply separated psychological architectures.

## Heuristics are policies, not error labels

The heuristics literature provides a second correction to simplistic rational-versus-irrational language. Gigerenzer and Gaissmaier describe heuristics as efficient cognitive processes, conscious or unconscious, that ignore part of the available information. Whether a heuristic performs well depends on the task and on the structure of the environment.

That means a heuristic can save effort and still be accurate, especially when information is noisy, samples are small, time is limited, or a few cues carry most of the useful signal. The same rule can fail in another environment. This idea is often described as **ecological rationality**: performance is a property of the fit between a strategy and its environment, not only of the strategy considered in isolation.

For CEM, [[MODULE:MOD.15]] therefore represents **heuristic policy selection**, not a generic “bias module”. A future executable version should specify a set of candidate policies, the cues each policy uses, the environment in which it is applied, the cost of acquiring information and the pattern that would distinguish one policy from another. It should also allow a heuristic to outperform a more information-intensive strategy in some conditions.

Alpha 0.4.1a1 does not execute such a selector. The module is retained because heuristic choice is important to the larger architecture, but adding a numerical “heuristic tendency” now would collapse many different strategies into an uninterpretable trait.

## What metacontrol means here

Metacontrol is used as an umbrella label for selecting and regulating processing: detecting conflict, allocating attention, checking an intuition, seeking additional information, choosing a strategy, or terminating search. This connects reasoning to metacognition, the monitoring and regulation of one's own cognitive processes.

These operations should not be compressed automatically into one latent resource. A future model may need to distinguish at least strategy selection, conflict detection, resource allocation and stopping rules. The empirical question is which distinctions produce observable differences that a smaller model cannot explain.

## Why W is not “System 2”

[[VAR:W]] is the contextual weight placed on accuracy in the M0 action policy. An accuracy cue can increase W in a scenario. W is not a measure of general cognitive ability, IQ, executive function, need for cognition, or how much “System 2” a person uses. A higher W only means that accuracy is given greater weight in that simulated decision.

This boundary matters. Interpreting every accuracy-cue effect as “System 2 activation” would inflate a task-specific variable into a much broader psychological construct than its operational definition supports.

## Conflict, monitoring and resources

A future model could separate at least four questions. Was an initial response generated? Was conflict or a reason for doubt detected? Were resources available and mobilized for reconsideration? Which policy was selected after that monitoring? These stages can vary independently. A person can detect uncertainty but decide that further search is too costly; another can deliberate extensively yet use poor evidence.

CEM preserves conceptual space for these distinctions because they help explain context-dependent processing without turning people into fixed cognitive types.

## Relationship to the next chapters

Chapter 3 examines one motivation that can influence information search and commitment: need for cognitive closure. Chapter 4 treats stress and executive resources separately. Chapter 8 shows the much narrower executable role of [[VAR:W]]. This ordering is deliberate: a broad cognitive theory should not be inferred backwards from one parameter in a decision equation.

## What this chapter does not claim

It does not assert two discrete neural systems, equate fast processing with error, equate deliberation with truth, or define heuristics as biases. It does not use Type 1/Type 2 or heuristic use to classify people or populations. It does not convert W into a measure of general rationality. [[MODULE:MOD.15]] remains conceptual until a specific heuristic policy can pass the project's extension gate.

## In the application

Inspect [[VAR:W]] in [[VIEW:reference]] for its operational definition. Use the module map to locate [[MODULE:MOD.15]] and distinguish future heuristic-policy work from the currently executable M0 action rule.
