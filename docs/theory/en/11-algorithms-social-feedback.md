# Algorithms, ranking and social feedback

## Central idea

A ranking algorithm can influence which information is seen, how often and in what order, but this is a different causal stage from directly forming a belief. CEM deliberately separates ranking → exposure from exposure → processing → belief → action.

[[CONCEPT:algorithm-stage]] · [[VAR:Nexp]] · [[MECH:repetition]] · [[MODULE:MOD.18]] · [[VIEW:structure]]

## Why “the algorithm made me believe it” is too short

Recommender systems select and order content using objectives, signals and constraints. This can change the distribution of exposures. Effects on belief then depend on content, attention, prior knowledge, source, repetition, congruence and social context.

A direct algorithm → belief arrow would therefore hide multiple observable stages. In CEM, a future ranking mechanism should first produce an explicit change in observed information or [[VAR:Nexp]], after which existing cognitive mechanisms can process that input.

## What platform experiments show

Experimental evidence does not support one universal story. The 2023 Facebook/Instagram election studies showed that large feed changes can alter exposure and engagement without detectable effects on polarization or many political attitudes during the study period. That result cautions against automatically inferring “different feed” → “different opinion”.

By contrast, a 2026 Nature field experiment on X randomized users between algorithmic and chronological feeds for seven weeks and found that switching the algorithm on increased engagement and shifted some political attitudes in the direction of content promoted by the feed. The study also observed changes in which accounts participants followed, providing a plausible intermediate pathway. Effects were not universal: partisanship and affective polarization did not significantly change.

Together these results support a staged architecture: algorithms can alter exposure and can sometimes produce downstream attitude effects, but direction and magnitude depend on platform, intervention, population and outcome.

## Social feedback as a loop

A user sees content, acts on it, the system observes that action, and selection can change. Other users' reactions can also become social cues. This creates a loop:

ranking → exposure → action → platform signal → ranking.

Another possible loop is:

source/content exposure → familiarity or appraisal → action → social feedback → future exposure.

MOD.18 reserves this level in the conceptual map, but Alpha 0.4.1a1 does not yet execute a recommender system or social network.

## Connection to repetition

If ranking increases content frequency, it can alter [[VAR:Nexp]], after which [[MECH:repetition]] can affect familiarity. This does not mean every algorithmic amplification produces illusory truth: content must actually be observed and processed, and the repetition effect must generalize to that content domain.

## What this chapter does not claim

It does not claim algorithms are neutral, nor that they are the single cause of polarization. It does not extrapolate X results to Facebook, TikTok or every platform. It does not infer political intention from content distributions and does not treat engagement as synonymous with belief.

## Future M1 implication

[[CONCEPT:algorithm-stage]] remains CONCEPTUAL. To become executable it needs an explicit ranking policy, observable input, exposure output, nested null and a differential pattern that the model without ranking cannot reproduce.