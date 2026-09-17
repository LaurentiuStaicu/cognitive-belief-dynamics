# Belief, accuracy attention and action

## Central idea

Believing a claim and deciding to share it are different outcomes. Sharing can depend on accuracy but also on social rewards, relevance, identity, entertainment and other motives. M0 explicitly separates belief [[VAR:B]], accuracy weight [[VAR:W]], latent sharing probability and sampled action [[VAR:Share]].

[[VAR:B]] · [[VAR:W]] · [[VAR:Share]] · [[MECH:accuracy]] · [[VAL:VAL.M0.N01]] · [[REF:REF.PENNYCOOK.2021]] · [[CODE:m0.share_probability]] · [[VIEW:runs:accuracy:5]]

## From belief to action probability

M0 first computes B without direct access to ground truth. An accuracy cue can then shift W through a logistic transform of the agent's accuracy baseline.

Sharing probability is:

P(Share) = logistic(sharing_bias + W × (2B - 1) + beta_reward × (1 - W) × reward_context).

Inspect [[CODE:m0.share_probability]].

The equation shows why B and Share are not synonyms. With larger W, accuracy/belief carries more weight in action utility. With smaller W, reward_context can matter more. Share is finally sampled from the probability; two runs can have the same latent probability but different observed actions if random draws differ.

## What accuracy-prompt research says

Pennycook and colleagues experimentally showed that shifting attention toward accuracy can improve sharing discernment. A later internal meta-analysis of 20 experiments with a total N of 26,863 found improved sharing discernment, driven mainly by reduced intentions to share false headlines.

This literature supports the idea that accuracy can be underweighted at the moment of sharing and that a cue can alter choice. It does not establish W as a literal latent psychological state or estimate the M0 equation.

## Why the separation matters epistemically

If someone shares content, we cannot safely infer that they believe it. Sharing is a social action with multiple possible utilities. Conversely, a person can believe a claim and not share it. This dissociation constrains inferences from platform behavior to private belief.

[[VAL:VAL.M0.N01]] protects the ground-truth boundary: action must arise from agent states and decision context rather than hidden simulator truth.

## Attention, not “intelligence”

[[VAR:W]] is not IQ, System 2, morality or general critical-thinking capacity. It is a contextual accuracy weight in the M0 action policy. An accuracy cue does not “make the person smarter”; in the model it changes which criterion receives more weight at that moment.

## What this chapter does not claim

It does not claim that all misinformation sharing is caused by inattention or that accuracy prompts solve misinformation. Real effects depend on design, population, content and platform. Sharing intentions in experiments are also not identical to observed platform behavior.

## In the application

Use [[VIEW:runs:accuracy:5]] for the M0 scenario and [[VIEW:planning]] for demonstrative intervention bundles. Chapter 10 introduces a different outcome, EngageIntent, which must remain separate from Share.