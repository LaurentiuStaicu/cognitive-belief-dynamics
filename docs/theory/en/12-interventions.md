# Interventions: where to act in the causal chain

## Central idea

An intervention is easier to understand when it is placed at the stage it is intended to modify. CEM currently separates interventions on information supply, correction, source evaluation and accuracy attention. Future versions may add interventions on attention and consumption, social evidence, AI intermediation or platform ranking, but only after those mechanisms are operationalized and tested.

[[VAR:C]] · [[VAR:W]] · [[MECH:correction]] · [[MECH:accuracy]] · [[VIEW:planning]]

## Executable M0 interventions

The current planner compares four measures: repetition reduction, corrective context, accuracy cues and verified source feedback. Each acts at a different mechanism location.

Repetition reduction changes scheduled exposures and therefore familiarity. Corrective context updates [[VAR:C]]. An accuracy cue changes [[VAR:W]] in the action policy. Source feedback updates estimated reliability.

This separation is more informative than a single “anti-misinformation” score because two interventions can reach the same final outcome through different paths and their combination can be non-additive.

## Debunking and prebunking

Contemporary reviews show that debunking and correction can reduce misinformation influence, and that fears of a general backfire effect have often been overstated. Corrections may nevertheless fail to reach the same audience as the original information, and residual influence can persist.

Psychological inoculation, often called *prebunking*, attempts to prepare people before exposure, for example by explaining manipulation techniques. Experiments and recent syntheses indicate improved discernment under some conditions. In CEM these findings remain BACKGROUND_THEORY: there is no separate executable inoculation mechanism yet.

Accuracy prompts have a more direct experimental relationship with sharing discernment and are therefore represented in M0 through [[MECH:accuracy]].

## Friction, verification and information literacy

Some interventions add a small pause or extra cost before sharing: opening an article, confirming intent, checking a source or performing an extra step. CEM has no generic friction variable. A future implementation must state whether the intervention changes attention, deliberation time, action probability or another mechanism.

Likewise, training in source-credibility evaluation, including lateral reading across independent sources, has an empirical information-literacy base. It should not be equated with the simplified delta rule through which M0 updates T.

## Ecosystem-level interventions

Chapter 11 shows that some interventions do not target individual cognition directly. They can modify content production, editorial selection, recommendation policy, the visibility of social evidence, interface design, or the way an AI system communicates uncertainty and sources.

This distinction matters for public policy. A platform intervention and a user-focused intervention can share a final objective while having very different costs, mechanisms, adverse effects and distributions of benefits.

CEM does not yet compare those broader interventions numerically. Each first needs a clear causal location and an observable outcome.

## What the current planner optimizes

The planner evaluates every feasible combination of the four executable measures over a synthetic 13-step horizon. Its weighted objective attempts to reduce false-sharing probability while avoiding excessive reduction in true-sharing probability. Effort costs are supplied by the user.

Low/reference/high profiles are sensitivity analyses, not confidence intervals. [[VIEW:planning]] does not estimate real cost-effectiveness, population effects, audience reach, implementation feasibility or equity in the distribution of costs and benefits.

“Best combination” means only the best among the finite options evaluated under the selected assumptions and weights.

## The causal-location principle

For each proposed intervention, ask at least five questions:

1. Which stage of the chain does it modify?
2. Which observable or latent variable changes?
3. Which pattern should differ from the null model?
4. Which adverse effect, trade-off or distributional effect should be tracked?
5. What data could count against the proposed mechanism?

This discipline prevents a measure from entering the model merely because it sounds useful.

## Cumulative impact is not simple addition

Two interventions can act on the same stage, successive stages or different branches. Their combined effect can be sub-additive, approximately additive or super-additive. Maximizing cumulative impact therefore does not justify adding effect sizes from unrelated studies.

CEM can explore interactions inside its own assumptions, but real recommendations require evidence about implementation, context, cost, adverse effects and transportability.

## What this chapter does not claim

It does not turn a demonstrative CEM intervention into a policy recommendation. It does not assume real-world effects add linearly and does not treat experiments from different populations as if they were directly comparable parameters.

## In the application

Use [[VIEW:planning]] only after inspecting mechanisms and evidence. The planner is a scenario laboratory: it exposes dependencies and trade-offs and helps formulate questions for real evaluation; it does not replace that evaluation.
