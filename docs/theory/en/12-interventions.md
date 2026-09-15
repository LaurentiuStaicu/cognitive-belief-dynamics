# Interventions, human–AI mediation and causal location

## Central idea

An intervention is easier to interpret when it is placed at the stage it is intended to modify. CEM separates interventions on information supply, correction, source evaluation, accuracy attention and, in future versions, attention, ranking, human–AI intermediation and oversight.

[[VAR:C]] · [[VAR:W]] · [[MECH:correction]] · [[MECH:accuracy]] · [[MODULE:MOD.11]] · [[MODULE:MOD.12]] · [[MODULE:MOD.13]] · [[VIEW:planning]]

## Executable M0 interventions

The current planner compares four measures: repetition reduction, corrective context, accuracy cues and verified source feedback. Each acts at a different mechanism location.

Repetition reduction changes scheduled exposures and therefore familiarity. Corrective context encodes [[VAR:C]]. An accuracy cue changes [[VAR:W]] in the action policy. Source feedback updates estimated reliability.

This is more informative than a single “anti-misinformation” score because two interventions can reach the same final outcome through different paths and can interact non-additively.

## What research says about debunking and prebunking

Contemporary reviews show that debunking can reduce misinformation influence and that fears of a general backfire effect were often overstated. Corrections may nevertheless fail to reach the original audience, and residual influence can persist. Detailed corrections and alternative explanations often perform better than bare negations, but effectiveness varies with topic, population and context.

Prebunking or psychological inoculation attempts to prepare people before exposure, for example by explaining manipulation techniques. Large experiments have found improvements in recognition of manipulative techniques, while recent work also shows that such gains do not automatically imply better truth discernment for every type of content. CEM therefore treats prebunking as relevant BACKGROUND_THEORY rather than as a validated generic coefficient.

Accuracy prompts have more direct experimental and meta-analytic support for sharing discernment, which is why M0 contains [[MECH:accuracy]]. Even here, the intervention is task-specific and does not imply a general increase in intelligence or rationality.

## Friction and verification

Friction interventions add a cost or pause before sharing: opening an article, confirming intent, checking a source or performing an extra step. CEM has no generic friction variable yet. A future implementation must state whether friction changes attention, action probability, available time or some other mechanism.

Likewise, training in source credibility evaluation, including lateral reading, has an empirical information-literacy base but should not be equated with the M0 delta rule.

## Human–AI epistemic intermediation

AI systems can enter the information chain in several roles: search or retrieval interface, summarizer, recommender, writing assistant, decision aid, tutor, conversational adviser or autonomous filter. These roles are not equivalent. They can change which information is surfaced, how evidence is compressed, how uncertainty is expressed and how much verification effort remains with the human user.

[[MODULE:MOD.11]] reserves human–AI epistemic intermediation. A future executable model should identify where the AI sits in the causal chain: before exposure, during evidence integration, at judgment, or at action. Treating “AI influence” as one undifferentiated effect would hide these distinct pathways.

The model should also distinguish AI output quality from user reliance. A highly accurate system can still be misused, and an imperfect system can still be useful when the user verifies it appropriately.

## Trust, reliance and overreliance

Human-factors research distinguishes trust from reliance. Trust is an attitude or expectation; reliance is behavior. Appropriate reliance means using automation when it is likely to help and withholding or checking it when its limitations are relevant.

[[MODULE:MOD.12]] reserves delegation and appropriate reliance. Research on automation bias shows that people can over-rely on decision support, especially when verification is difficult or cognitive load is high. More recent AI experiments likewise document cases in which people follow AI advice despite conflicting contextual information. These findings justify modelling reliance as a separate outcome rather than assuming that trust, acceptance and correctness are the same variable.

A future CEM mechanism should therefore include at least perceived reliability, actual system performance, verification cost and the user's decision to accept, inspect or override the recommendation.

## Skill acquisition, deskilling and oversight

Repeated delegation can change what the human continues to practise. In some domains, automation may support learning or free resources for higher-level work; in others, reduced practice can weaken the ability to perform or verify the task independently. Evidence is domain-dependent, and the strongest recent deskilling literature is concentrated in professional settings such as healthcare and other decision-support tasks.

[[MODULE:MOD.13]] reserves skill acquisition, deskilling and human oversight. CEM should not encode a generic “AI causes deskilling” rule. An executable version would need a task-specific skill state, practice or feedback dynamics, independent-performance tests and a model of how oversight quality changes over time.

Human oversight is meaningful only if the human retains the information, time and competence needed to challenge the system. A nominal “human in the loop” is not equivalent to effective review.

## What the current planner optimizes

The planner evaluates every feasible subset of four M0 measures over a synthetic 13-step horizon and a weighted objective trading off reduced false-sharing probability against preserved true-sharing probability. Effort costs are user supplied. Low/reference/high profiles are sensitivity checks, not confidence intervals.

[[VIEW:planning]] does not estimate real cost-effectiveness, population effects, reach, implementation or equity. “Best bundle” only means best within the finite option set and selected assumptions. Human–AI interventions are not yet part of the executable planner.

## The causal-location principle

For every new intervention ask:
1. Which stage does it modify?
2. What observable or latent variable changes?
3. Which pattern differs from the null?
4. Which adverse effect or trade-off should be tracked?
5. What data could falsify the mechanism?
6. Does the intervention alter future capability, not only the immediate decision?

This discipline prevents measures from entering the model merely because they sound useful.

## What this chapter does not claim

It does not turn a demonstrative CEM intervention into a policy recommendation. It does not assume real-world effects add linearly and does not combine experiments from different populations as if they were one parameter set. It does not claim AI advice is inherently superior or inferior to human judgment, that trust equals reliance, or that automation inevitably causes deskilling.

## In the application

Use [[VIEW:planning]] after inspecting mechanisms. The planner is a scenario laboratory: it exposes dependencies and trade-offs before suggesting what should be measured in a real evaluation. [[MODULE:MOD.11]], [[MODULE:MOD.12]] and [[MODULE:MOD.13]] remain conceptual until human–AI roles, reliance decisions and skill dynamics are operationalized and tested.