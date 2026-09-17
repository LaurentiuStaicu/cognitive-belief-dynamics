# World, information and internal representation

## Central idea

CEM begins with a simple but consequential distinction: a state of the world is not identical to the information available about it; available information is not identical to what an agent observes; and observed information is not identical to the internal representation constructed by that agent.

The conceptual chain is:

world → available information → selection and presentation → observed information → internal representation → judgment → action.

[[CONCEPT:world-model]] · [[MODULE:MOD.14]] · [[MECH:editorial]] · [[MECH:presentation]] · [[VIEW:learning]]

## Why the stages cannot be collapsed

If an analysis jumps directly from “what exists in the world” to “what a person believes”, intermediate differences can be misattributed to the individual. Information environments filter, order and format information before the agent processes it. Memory, expectations, knowledge and context then contribute to an internal representation that may be incomplete.

The separation supports different causal questions. M1.E1 asks what happens when one factual pool is selected differently. M1.E2 asks what happens when the same semantic proposition is expressed through confirmation or refutation. A future ranking mechanism would separately ask which content reaches exposure. None of these changes in the information pipeline automatically implies a change in belief.

## Relationship to predictive-processing theories

Predictive processing is useful background theory: perception and interpretation can be treated as constructive processes in which expectations interact with incoming signals. Neuroscience literature discusses generative models and prediction-error signals, especially in sensory processing. Yet the framework has several variants, and there is active debate about how strongly available evidence discriminates it from alternative accounts.

CEM does not implement neural predictive coding and does not claim that MOD.14 instantiates a complete brain theory. It uses a smaller and more testable distinction: external information and internal representation should not be treated as the same variable.

This is why [[CONCEPT:world-model]] is a conceptual bridge connected to executable components without being advertised as a unified theory of the brain.

## Ground truth and what the agent knows

In M0, synthetic truth belongs to the simulation environment. It is used to construct and evaluate scenarios but is never passed directly to the belief-update function. This creates an epistemic boundary: the external evaluator can know whether the synthetic claim is true or false, while the agent must work with exposures, evidence, corrections and estimated source reliability.

Passing ground truth directly into belief formation would confuse model evaluation with agent information and remove the very epistemic problem the model is intended to study.

## Selection and presentation are different mechanisms

[[MECH:editorial]] changes the observed factual subset from a fixed pool. [[MECH:presentation]] holds proposition meaning fixed while comparing confirmation and refutation form. In real environments, selection, tone, headlines, ordering and ranking can coexist. CEM separates them deliberately so that each causal stage can make a differential prediction.

This is a general project rule: when two mechanisms can be confounded, the model should try to separate them with controlled conditions and nested nulls rather than hide them inside a global coefficient.

## What this chapter does not claim

It does not claim that people “hallucinate reality”, that perception is arbitrary, or that every interpretation is equally valid. It does not claim that predictive processing is a definitively established account of all cognition. It does not claim that M1.E1 or M1.E2 exhaust the filters that shape information.

## In the application

Use [[VIEW:learning]] to compare M1.E1 and M1.E2. Chapters 9 and 10 connect these distinctions to executable variables and their model-discrimination tests.