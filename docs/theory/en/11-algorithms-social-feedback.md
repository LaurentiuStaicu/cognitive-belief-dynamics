# Information ecosystems: algorithms, social feedback, AI and strategic influence

## Central idea

Digital information does not reach a person through one mechanism. Content can be produced strategically, selected by editors, ranked by platforms, forwarded by other users, summarized by search or AI systems, encountered across several services and interpreted through social cues. CEM therefore treats the information ecosystem as a sequence of separable stages rather than drawing a direct arrow from “the algorithm”, “the media” or “AI” to belief.

A useful causal skeleton is:

production → editorial availability → platform ranking → exposure → attention/processing → internal representation → judgment → action → social/platform feedback → later exposure.

Different mechanisms can enter at different points. Their effects can accumulate, cancel or depend on the population and network in which they operate.

[[CONCEPT:algorithm-stage]] · [[VAR:Nexp]] · [[MECH:repetition]] · [[MODULE:MOD.08]] · [[MODULE:MOD.10]] · [[MODULE:MOD.11]] · [[MODULE:MOD.12]] · [[MODULE:MOD.13]] · [[MODULE:MOD.18]] · [[MODULE:MOD.19]] · [[VIEW:structure]]

## Why “the algorithm made me believe it” is too short

Recommender systems select and order content using objectives, signals and constraints. This changes what users are likely to encounter, how often they encounter it and in what sequence. Belief change, however, is a later outcome. It depends on whether content is actually noticed, understood and integrated, and on prior knowledge, source evaluation, repetition, corrective context, congruence and social information.

A direct algorithm → belief arrow would hide these intermediate stages. In CEM, a future ranking mechanism should first produce an observable change in exposure or information composition. Existing or future cognitive mechanisms would then process that changed input.

The same logic protects against the opposite mistake. Finding no attitude change after a ranking intervention does not imply that ranking had no effect. It may have changed exposure, attention or engagement without moving the measured judgment during the study window.

## What platform experiments show

Experimental evidence does not support one universal story. Large 2023 Facebook/Instagram studies showed that substantial feed changes altered exposure and engagement patterns without detectable effects on many political attitudes or affective polarization during the study period.

By contrast, a 2026 Nature field experiment on X randomized users between algorithmic and chronological feeds for seven weeks. Enabling the algorithmic feed increased engagement and shifted some political attitudes in the direction of content disproportionately promoted by that feed. The experiment also observed changes in which accounts participants followed, providing a plausible intermediate pathway. Partisanship and affective polarization did not significantly change.

These results are not contradictory. They show why a staged architecture is necessary. Effects depend on platform, ranking intervention, content distribution, population, duration and outcome. CEM should represent those moderators rather than treating “algorithmic exposure” as a universal treatment.

## Population and network heterogeneity

[[MODULE:MOD.08]] addresses a major limitation of single-agent demonstrations. Real populations differ in prior beliefs, knowledge, attention, source repertoires, network position, media habits and exposure opportunities. Networks also differ in clustering, bridge structure, homophily and the concentration of highly connected accounts.

Once social diffusion is modeled, an average individual effect is not enough. The same mechanism can generate different population-level outcomes depending on who is connected to whom and which nodes receive or transmit content first. Conversely, a population pattern can arise from network structure even when individual updating rules are identical.

Alpha 0.4.1a1 does not simulate a population network. CEM therefore must not infer network polarization, prevalence or cascade size from its current single-agent/reference scenarios.

## Social evidence is more than engagement counts

[[MODULE:MOD.18]] covers social norms and collective evidence. Likes, shares, comments, endorsements, corrections and source similarity can act as social cues, but they do not have a fixed psychological meaning.

A 2024 series of five experiments involving more than 20,000 participants found that social cues influenced misinformation judgments when they changed perceived social consensus; simple high or low engagement counts were not universally persuasive. Credible ingroup sources also mattered under specific conditions. This is exactly the kind of contingency CEM should preserve.

A future social-evidence mechanism should therefore distinguish a raw platform metric from the interpretation the agent gives it. “10,000 likes” is an observable cue. “Most informed people believe this” is an inferred social state. They should not be the same variable.

## Cross-platform ecosystems and incidental exposure

[[MODULE:MOD.10]] represents adaptation and movement across platforms. A user may encounter a television segment, search for the topic, see a clipped version on a social platform, receive it through a messaging app and later ask an AI assistant about it. Each transition can change context, source visibility, repetition, audience and presentation.

A 2023 scoping review of incidental news exposure identified 88 studies and emphasized that digital news is often encountered while people are online for another purpose. It also distinguishes simple incidental contact from subsequent engagement and processing. This matters for CEM because **availability is not exposure, exposure is not attention, and attention is not belief**.

A mature ecosystem model would need to represent channel transitions explicitly. Alpha 0.4.1a1 only reserves that architecture.

## Human–AI epistemic intermediation

[[MODULE:MOD.11]] covers a newer information stage: AI systems can search, summarize, recommend, explain, translate or generate material before it reaches the user. In that role AI is not merely another source and not merely another ranking algorithm. It can transform the representation itself.

A 2024 interdisciplinary review of AI advice shows that reliance on AI varies with the decision task, perceived expertise, trust, transparency, characteristics of the user and properties of the advice environment. Research contains both algorithm aversion and algorithm appreciation; neither should be treated as a universal human tendency.

For CEM, the key question is not “do people trust AI?” but: **when does an AI system alter information availability, presentation, uncertainty, source visibility or the user's own decision process?** Each path would require a different model.

CEM currently has no executable LLM or AI-advice mechanism. Any future implementation must also record whether the AI output is accurate, incomplete or wrong independently of whether the user accepts it.

## Appropriate reliance: neither maximum trust nor maximum distrust

[[MODULE:MOD.12]] concerns delegation and appropriate reliance. A well-calibrated user should ideally accept useful AI assistance when it is reliable and reject or verify it when it is not. Over-reliance and under-reliance are different failure modes.

This cannot be represented adequately by one global “trust in AI” slider. Reliance may vary by task, domain expertise, uncertainty, explanation quality, consequences of error and the user's ability to verify the result. An agent can rely appropriately in one domain and poorly in another.

A future CEM mechanism should therefore compare reliance with actual system performance under the same conditions, rather than treating higher trust as automatically better.

## Skill acquisition, deskilling and human oversight

[[MODULE:MOD.13]] extends the time horizon. Repeated delegation may change what the human learns, practices, remembers or monitors. The empirical literature is still developing and is highly task-dependent.

A 2025 CHI study of 319 knowledge workers and 936 reported GenAI use cases found that greater confidence in GenAI was associated with less self-reported critical-thinking effort, while critical thinking shifted toward verification, integration and task stewardship. Because the study is observational and self-reported, it does not establish that AI causes cognitive decline.

A 2026 systematic review in healthcare similarly reports concerns about automation bias and deskilling, but notes a heterogeneous evidence base dominated by observational, simulation and conceptual studies. These findings justify a conceptual module, not a numerical deskilling coefficient.

The important distinction is between **substitution** and **reallocation**. AI may reduce effort on one subtask while increasing the need for verification, supervision or integration elsewhere. CEM should model the specific skill and task, not a global quantity called “thinking”.

## Strategic influence and adversarial production

[[MODULE:MOD.19]] asks who produces information and with what objective. Strategic actors can select topics, coordinate repetition, imitate credible sources, exploit platform incentives, generate synthetic content or target particular audiences.

This is not synonymous with false information. Strategic communication can use true, false, selectively incomplete or emotionally salient material. The causal question is how production choices change the information entering later stages.

A future adversarial-production mechanism would therefore need explicit objectives, actions and observables. It should not infer hidden intent merely from the fact that content is polarizing, popular or politically aligned.

## Three feedback loops that should remain distinct

CEM's broader architecture contains at least three conceptually different loops.

**Familiarity loop:** ranking or social circulation increases repeated exposure; repeated exposure can increase familiarity; familiar content may be easier to notice or engage with; later ranking can increase exposure again.

**Social-reinforcement loop:** action produces visible social signals; these signals alter perceived consensus or platform ranking; later users receive a changed context.

**Closure/commitment loop:** an early interpretation can reduce further search or make later information less influential. This loop is conceptual in the current release and should not be conflated with social reinforcement.

These loops can interact in real life, but separating them makes falsifiable modelling possible.

## What this chapter does not claim

It does not claim algorithms are neutral or uniquely responsible for polarization. It does not extrapolate X results to every platform. It does not treat engagement as belief, network structure as individual psychology, AI use as cognitive decline, or social consensus as truth. It does not attribute political intent to a ranking system or strategic intent to a publisher without independent evidence.

Most importantly, this chapter does not make MOD.08, MOD.10–13, MOD.18 or MOD.19 executable. It explains where they belong and what empirical distinctions would be required before implementation.

## Future model implication

[[CONCEPT:algorithm-stage]] remains CONCEPTUAL. Future ecosystem mechanisms should enter one at a time through the project extension gate: define the stage, specify observables, state the differential prediction, preserve smaller-model nulls where possible, and define what result would count against the new mechanism.
