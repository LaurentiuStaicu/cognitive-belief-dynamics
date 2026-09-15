# Belief, accuracy attention and action

## Central idea

Judging a claim to be true and deciding to share it are different outcomes. Sharing can depend on accuracy, but also on social rewards, relevance, identity, entertainment and other motives. M0 explicitly separates belief [[VAR:B]], contextual accuracy weight [[VAR:W]], latent sharing probability and sampled action [[VAR:Share]].

[[VAR:B]] · [[VAR:W]] · [[VAR:Share]] · [[MECH:accuracy]] · [[VAL:VAL.M0.N01]] · [[REF:REF.PENNYCOOK.2021]] · [[CODE:m0.share_probability]] · [[VIEW:runs:accuracy:5]]

## From belief to action probability

M0 first computes B without direct access to simulated ground truth. An accuracy cue can then shift W through a logistic transform of its reference value.

Sharing probability is:

P(Share) = logistic(sharing_bias + W × (2B - 1) + beta_reward × (1 - W) × reward_context).

The identifiers in the equation retain their code names. Inspect [[CODE:m0.share_probability]] for the implementation.

The equation shows why B and Share are not synonyms. With larger W, accuracy and belief carry more weight in action utility. With smaller W, reward_context can matter more. Share is then sampled from the probability; two runs can have the same latent probability but different observed actions when the random draw differs.

## What accuracy-prompt research says

Pennycook and colleagues experimentally showed that shifting attention toward accuracy can improve discernment about what people say they would share. A later meta-analysis covering 20 experiments and 26,863 participants found improved sharing discernment, driven mainly by reduced intentions to share false headlines.

This literature supports the idea that accuracy can be underweighted at the moment of sharing and that a contextual cue can change choice. It does not establish W as a literal latent psychological state and does not estimate the M0 equation.

## Why the separation matters epistemically

If someone shares content, we cannot safely infer that they believe it. Sharing is a social action with several possible utilities. Conversely, a person can believe a claim and not share it. This dissociation constrains inferences from visible platform behavior to private belief.

[[VAL:VAL.M0.N01]] also protects the ground-truth boundary: action must arise from agent states and action context rather than hidden simulator truth.

## Attention, not “intelligence”

[[VAR:W]] is not IQ, System 2, morality or general critical-thinking ability. It is a contextual accuracy weight in the M0 action policy. An accuracy cue does not “make the person smarter”; in the model it only changes which criterion receives more weight at that moment.

This boundary is essential. An effect on W cannot be used as evidence that a person has become globally more rational, attentive or competent.

## From stated intention to real behavior

Much of the experimental literature measures sharing intentions or choices in controlled tasks. These outcomes are informative, but they are not identical to observed sharing on a real platform, where interface design, perceived audience, norms, reputation, social costs and real consequences also matter.

CEM should therefore keep the observable level explicit. A mechanism that is useful for explaining sharing intention does not automatically become a valid model of behavior on every platform.

## What this chapter does not claim

It does not claim that all misinformation sharing is caused by inattention or that accuracy prompts solve misinformation. Real effects depend on intervention design, population, content and platform. It also does not claim that sharing something proves acceptance of it as true.

## In the application

Use [[VIEW:runs:accuracy:5]] for the M0 scenario and [[VIEW:planning]] for demonstrative intervention combinations. Chapter 10 introduces a different outcome, EngageIntent, which must remain separate from Share.
