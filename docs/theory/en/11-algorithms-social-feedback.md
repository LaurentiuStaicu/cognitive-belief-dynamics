# Algorithms, networks, cross-platform dynamics and social feedback

## Central idea

A ranking algorithm can influence which information is seen, how often and in what order, but this is a different causal stage from directly forming a belief. CEM deliberately separates ranking → exposure from exposure → processing → belief → action.

[[CONCEPT:algorithm-stage]] · [[VAR:Nexp]] · [[MECH:repetition]] · [[MODULE:MOD.08]] · [[MODULE:MOD.10]] · [[MODULE:MOD.18]] · [[MODULE:MOD.19]] · [[VIEW:structure]]

## Why “the algorithm made me believe it” is too short

Recommender systems select and order content using objectives, signals and constraints. This can change the distribution of exposures. Effects on belief then depend on content, attention, prior knowledge, source, repetition, congruence and social context.

A direct algorithm → belief arrow would therefore hide multiple observable stages. In CEM, a future ranking mechanism should first produce an explicit change in observed information or [[VAR:Nexp]], after which existing cognitive mechanisms can process that input.

## What platform experiments show

Experimental evidence does not support one universal story. The 2023 Facebook/Instagram election studies showed that large feed changes can alter exposure and engagement without detectable effects on polarization or many political attitudes during the study period. That result cautions against automatically inferring “different feed” → “different opinion”.

By contrast, a 2026 Nature field experiment on X randomized users between algorithmic and chronological feeds for seven weeks and found that switching the algorithm on increased engagement and shifted some political attitudes in the direction of content promoted by the feed. The study also observed changes in which accounts participants followed, providing a plausible intermediate pathway. Effects were not universal: partisanship and affective polarization did not significantly change.

Together these results support a staged architecture: algorithms can alter exposure and can sometimes produce downstream attitude effects, but direction and magnitude depend on platform, intervention, population and outcome.

## Exposure is heterogeneous, not evenly distributed

Average exposure can hide concentrated tails. Research on online misinformation shows that problematic content is often consumed disproportionately by a relatively small subset of users rather than uniformly across the population. A model calibrated only to a population mean can therefore miss the users and network locations where repeated exposure is highest.

[[MODULE:MOD.08]] reserves population and network heterogeneity. A future executable model should represent variation in activity, connectivity, source-following patterns and exposure opportunities instead of assuming interchangeable agents. Heterogeneity should be measured or explicitly scenario-defined; it should not be added merely to make a simulation look realistic.

## Social feedback as a loop

A user sees content, acts on it, the system observes that action, and selection can change. Other users' reactions can also become social cues. This creates a loop:

ranking → exposure → action → platform signal → ranking.

Another possible loop is:

source/content exposure → familiarity or appraisal → action → social feedback → future exposure.

[[MODULE:MOD.18]] reserves social norms and collective evidence. Counts of likes, shares, comments or endorsements can become cues, but they are not direct measures of truth or genuine consensus. A future social-proof mechanism should separate the observed cue from the underlying population state that generated it.

## Cross-platform ecosystems

Information rarely remains on one platform. A claim can move from a television segment to an online newspaper, then to a social network, messaging app, search engine, video platform or AI assistant, acquiring new framing and audiences at each step. Users also move between services, and content created on one platform can be amplified on another.

[[MODULE:MOD.10]] reserves this cross-platform ecosystem. The important modelling point is that platforms are not independent exposure containers. Cross-platform transmission can create repeated exposure, alter apparent source diversity and change which interventions are reachable. A future mechanism therefore needs explicit transfer rules rather than assuming that exposure on one service is equivalent to exposure everywhere.

## Strategic influence is not ordinary diffusion

Some information spreads because many individuals independently choose to share it. Other information is deliberately produced, targeted or amplified by coordinated actors. Computational-propaganda research distinguishes actors, content production, dissemination methods and amplification, including automation, coordinated campaigns and microtargeting.

[[MODULE:MOD.19]] reserves strategic influence and adversarial production. This stage should not be collapsed into “misinformation”. Strategic influence can use false, misleading, selectively true or entirely factual material. The relevant additional feature is intentional or coordinated intervention in production and distribution, not factuality alone.

A future executable mechanism should therefore distinguish organic diffusion from coordinated production or amplification and should require observable signatures or externally defined scenarios. CEM should not infer hostile intent merely from a content pattern.

## Connection to repetition

If ranking, social feedback, cross-platform transfer or coordinated amplification increases content frequency, it can alter [[VAR:Nexp]], after which [[MECH:repetition]] can affect familiarity. This does not mean every amplification produces illusory truth: content must actually be observed and processed, and the repetition effect must generalize to that content domain.

## What this chapter does not claim

It does not claim algorithms are neutral, nor that they are the single cause of polarization. It does not extrapolate X results to Facebook, TikTok or every platform. It does not assume average exposure describes every user, equate social endorsement with truth, infer strategic intent from popularity, or treat engagement as synonymous with belief.

## Future-model implication

The ranking stage and modules for network heterogeneity, cross-platform transmission, social feedback and strategic influence remain CONCEPTUAL. To become executable, each needs explicit inputs and outputs, a null model, measurable or scenario-defined assumptions, and a differential pattern that a simpler model cannot reproduce.