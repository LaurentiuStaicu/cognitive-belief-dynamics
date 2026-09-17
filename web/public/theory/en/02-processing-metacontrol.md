# Fast processing, deliberation and metacontrol

## Central idea

A large body of reasoning research distinguishes relatively fast, autonomous processing from deliberative processing that places greater demands on working memory. In CEM this family of ideas is useful for discussing metacontrol: when and to what extent an initial response is monitored, suspended, checked or replaced.

[[CONCEPT:type1-type2]] · [[MODULE:MOD.02]] · [[MODULE:MOD.09]] · [[MODULE:MOD.15]] · [[VAR:W]] · [[VIEW:reference]]

## Type 1 and Type 2 are processing families, not two brains

Evans and Stanovich argue that a central distinction is the relative autonomy of Type 1 processing and the dependence of Type 2 processing on working memory and hypothetical thinking. The classification is influential, but familiar attributes do not always line up perfectly. Fast is not necessarily irrational, slow is not necessarily correct, and automatic is not synonymous with emotional.

CEM therefore avoids a simple “bad System 1 / good System 2” story. Automatic processing can embody well-learned expertise. Deliberation can rationalize a desired conclusion, operate on poor evidence, or consume resources without improving a decision. Critiques of dual-process theory also show that some observed differences may be quantitative rather than evidence for two sharply separated psychological architectures.

## Attention and encoding come before judgment

Reasoning is constrained by what is noticed and encoded. A claim that is physically present in the environment may have little effect if it receives no attention or is only weakly encoded. Conversely, salience, repetition, novelty, emotional relevance and task goals can alter which cues enter later judgment.

[[MODULE:MOD.09]] reserves this stage in the CEM architecture. The current simulator does not contain a general attention-allocation equation, and it would be misleading to treat observed exposure as identical to attended or remembered exposure. A future executable attention mechanism should therefore separate at least availability, attention, encoding and later accessibility.

This distinction also matters for interventions. A warning, correction or source label can only affect a later judgment if it is encountered and processed strongly enough to become usable evidence.

## Heuristics are conditional policies, not errors by definition

Heuristics are simplified decision rules or cue-use strategies. They can be efficient when the cue used is informative in the environment, and they can fail when the cue is poorly matched to the task. CEM therefore treats heuristic processing as a candidate policy-selection problem rather than as a synonym for bias.

[[MODULE:MOD.15]] is reserved for future heuristic-policy mechanisms. An executable version would need to state which cue is used, under which conditions the policy is selected, what information it ignores, and which environments make it perform well or poorly. Labels such as “availability”, “authority” or “social proof” should not become free-floating error coefficients.

This ecological view is important because the same shortcut may be adaptive in one environment and misleading in another. A model should predict the conditions under which the strategy changes outcomes, not merely attach a negative label to fast processing.

## What metacontrol means here

Metacontrol is used as an umbrella label for selecting and regulating processing: detecting conflict, allocating attention, checking an intuition, seeking additional information, switching strategy, or terminating search. This connects reasoning to metacognition, the monitoring and regulation of one's own cognitive processes.

Within the conceptual architecture, [[MODULE:MOD.02]] can host future policy-selection or resource-control mechanisms. The current release does not compress these functions into a single executable coefficient.

## Why W is not “System 2”

[[VAR:W]] is the contextual weight placed on accuracy in the M0 action policy. An accuracy cue can increase W in a scenario. W is not a measure of general cognitive ability, IQ, executive function, attention span, or how much “System 2” a person uses. A higher W only means that accuracy is given greater weight in that simulated decision.

This boundary matters. Interpreting every accuracy-cue effect as “System 2 activation” would inflate a task-specific variable into a much broader psychological construct than its operational definition supports.

## Conflict, monitoring and resources

A future model could separate at least four questions: is an initial response generated; is relevant information attended and encoded; is a reason for doubt or conflict detected; and are resources available and mobilized for reconsideration? These stages are not yet executable. CEM nevertheless reserves conceptual space for them because they can explain why the same person may process similar information differently across contexts.

## What this chapter does not claim

It does not assert two discrete neural systems, equate fast processing with error, or equate deliberation with truth. It does not use Type 1/Type 2 to classify people or populations. It does not convert W into a measure of general rationality. It also does not claim that heuristics are inherently defective or that attention can be inferred simply from content being present on a screen.

## In the application

Inspect [[VAR:W]] in [[VIEW:reference]] for its operational definition. Chapter 8 shows exactly where W enters the distinction between belief and action. [[MODULE:MOD.09]] and [[MODULE:MOD.15]] remain conceptual placeholders until attention and heuristic selection receive explicit observables, executable rules and discriminating tests.