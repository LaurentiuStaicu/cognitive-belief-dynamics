# Interventions: where to act in the causal chain

## Central idea

An intervention is easier to interpret when it is placed at the stage it is intended to modify. CEM separates interventions on information supply, correction, source evaluation, accuracy attention and, in future versions, attention/consumption or ranking.

[[VAR:C]] · [[VAR:W]] · [[MECH:correction]] · [[MECH:accuracy]] · [[VIEW:planning]]

## Executable M0 interventions

The current planner compares four measures: repetition reduction, corrective context, accuracy cues and verified source feedback. Each acts at a different mechanism location.

Repetition reduction changes scheduled exposures and therefore familiarity. Corrective context encodes [[VAR:C]]. An accuracy cue changes [[VAR:W]] in the action policy. Source feedback updates estimated reliability.

This is more informative than a single “anti-misinformation” score because two interventions can reach the same final outcome through different paths and can interact non-additively.

## What research says about debunking and prebunking

Contemporary reviews show that debunking can reduce misinformation influence and that fears of a general backfire effect were often overstated. Corrections may nevertheless fail to reach the original audience, and residual influence can persist.

Prebunking or psychological inoculation attempts to prepare people before exposure, for example by explaining manipulation techniques. Large experiments have found improvements in discernment of misinformation techniques. These interventions are relevant BACKGROUND_THEORY, but CEM does not yet have a separate executable prebunking mechanism.

Accuracy prompts have more direct experimental and meta-analytic support for sharing discernment, which is why M0 contains [[MECH:accuracy]].

## Friction and verification

Friction interventions add a cost or pause before sharing: opening an article, confirming intent, checking a source or performing an extra step. CEM has no generic friction variable yet. A future implementation must state whether friction changes attention, action probability, available time or some other mechanism.

Likewise, training in source credibility evaluation, including lateral reading, has an empirical information-literacy base but should not be equated with the M0 delta rule.

## What the current planner optimizes

The planner evaluates every feasible subset of four measures over a synthetic 13-step horizon and a weighted objective trading off reduced false-sharing probability against preserved true-sharing probability. Effort costs are user supplied. Low/reference/high profiles are sensitivity checks, not confidence intervals.

[[VIEW:planning]] does not estimate real cost-effectiveness, population effects, reach, implementation or equity. “Best bundle” only means best within the finite option set and selected assumptions.

## The causal-location principle

For every new intervention ask:
1. Which stage does it modify?
2. What observable or latent variable changes?
3. Which pattern differs from the null?
4. Which adverse effect or trade-off should be tracked?
5. What data could falsify the mechanism?

This discipline prevents measures from entering the model merely because they sound useful.

## What this chapter does not claim

It does not turn a demonstrative CEM intervention into a policy recommendation. It does not assume real-world effects add linearly and does not combine experiments from different populations as if they were one parameter set.

## In the application

Use [[VIEW:planning]] after inspecting mechanisms. The planner is a scenario laboratory: it exposes dependencies and trade-offs before suggesting what should be measured in a real evaluation.