# World-model construction

> **Module:** MOD.14 · **Status:** mixed EMPIRICAL / EXECUTABLE / CONCEPTUAL / INTERPRETIVE

## What is being constructed?

A world model in CEM is an **agent-relative, partial and revisable representation of states of affairs**. It is not external reality itself. The distinction matters because an agent never receives “the world” directly: available information is filtered by perception and access, only some of it is attended or encoded, memory supplies prior information, communicated claims carry source and provenance cues, and uncertainty remains after any update.

MOD.14 therefore connects several processes that already exist elsewhere in CEM. It does not create a second familiarity state, a second source-reliability variable or a second belief variable. Existing `F`, `C`, `T`, `B`, `Sobs`, `Aissue`, preview/access and presentation constructs retain their meanings.

## The mechanism loop

The explanatory loop is:

**available/observed information → observation & selection → prior/memory retrieval → provenance & source evaluation → social-context interpretation → proposition revision where diagnostic evidence is available → explicit uncertainty → contradiction/correction-driven reassessment**.

This is an organizing architecture rather than a universal linear causal equation. In a particular task, some stages may be absent, repeated or coupled.

## EMPIRICAL layer

Several parts of the loop are supported as phenomena. Controlled multisensory experiments show that people can combine uncertain cues in ways close to reliability-weighted statistical integration in particular tasks. Situation-model research describes integrated mental representations built during comprehension. Schema and prior knowledge can affect interpretation and memory. Source-monitoring research shows that people make source attributions and can misattribute information. Research on misinformation and correction shows that prior knowledge, repetition, social factors and memory revision can all matter.

The empirical conclusion is therefore **not** that one master equation explains world-model construction. The stronger and better-supported conclusion is that representation construction is selective, history-dependent, source-sensitive and uncertainty-bearing, with effects that depend on task and context.

## EXECUTABLE layer: a narrow normative reference

MOD.14 executes only a proposition-level Bayesian reference update when two inputs are explicitly supplied: a prior probability `Pprior` and a defensible diagnostic likelihood ratio `LR`.

`Pwm = (Pprior × LR) / (Pprior × LR + 1 − Pprior)`

If `LR > 1`, the posterior moves toward the proposition; if `0 < LR < 1`, it moves away; `LR = 1` leaves it unchanged. The operator refuses invalid or missing likelihood ratios. CEM does not silently turn source trust, familiarity, social agreement or salience into an LR.

A second executable quantity is normalized binary Shannon entropy:

`Uwm = −p log2(p) − (1−p) log2(1−p)`

`Uwm` is largest at `p = 0.5` and zero at `p = 0` or `p = 1`. It describes uncertainty **inside this narrow binary normative state**. It does not measure ignorance about model misspecification, conflicting ontologies or unknown unknowns.

## Why `Pwm` is not `B`

`B` is CEM's existing latent propensity to judge a claim as true at a given time. It belongs to the descriptive simulation architecture. `Pwm` is a transparent normative reference probability produced only from declared probabilistic inputs. A person may have a high `B` while a domain-specific normative model yields a low `Pwm`, or vice versa. MOD.14 treats that gap as potentially informative rather than forcing the two quantities to agree.

## Perception and attention

CEM already distinguishes information availability from actual access. A preview impression is not proof that a message was visually fixated, read, encoded or comprehended. MOD.14 therefore uses **observation/selection** as a conceptual gate. It does not introduce an invented continuous “attention coefficient.” Future task-specific work may add validated attention measurements, but they must retain their own measurement semantics.

## Memory, priors and schemas

Prior information can come from stored knowledge, episodic memory, learned regularities or task instructions. Schema research indicates that prior structures can improve some forms of processing while also biasing or distorting others. Because direction depends on task, MOD.14 refuses a universal positive or negative sign from “schema strength” to belief updating.

A numerical `Pprior` is allowed only when a task or domain gives it a defensible probabilistic interpretation. Otherwise prior knowledge remains conceptual or is represented by the existing task-specific CEM constructs.

## Sources, provenance and epistemic vigilance

Source monitoring concerns attribution of information to origins and contexts. Epistemic-vigilance theory highlights evaluation of communicated information and communicators. CEM already has `T`, the agent's task-relevant estimate of source reliability. MOD.14 keeps three things separate:

1. **provenance** — where an evidence item came from and under what acquisition conditions;
2. **agent-estimated source reliability `T`** — a psychological state;
3. **diagnostic likelihood ratio `LR`** — a domain-specific statistical quantity.

None is automatically substituted for another.

## Social context

Communicated information is interpreted socially: who says it, how many apparently independent sources support it, what norms are active, and what incentives are perceived can matter. But social agreement is especially vulnerable to dependence: ten reposts of one original report are not ten independent observations. MOD.14 therefore keeps social context conceptual unless a validated task-specific measurement bridge supplies diagnostic evidence without double counting.

## Contradiction, correction and revision

A useful world model must remain revisable. New counterevidence can move a normative posterior back toward uncertainty or toward the opposite proposition. Human descriptive updating may be slower or asymmetric; CEM's existing correction-accessibility and continued-influence neighborhood is the appropriate place to represent those descriptive mechanisms.

## Predictive coding and the Bayesian brain

Predictive-coding and Bayesian-brain frameworks are valuable interpretive models: they emphasize generative expectations, prediction errors and uncertainty. In MOD.14 they remain **INTERPRETIVE** unless a specific experiment supplies variables and a validated functional form. CEM does not convert these frameworks into a whole-brain equation merely because they are mathematically expressible.

## Falsification and uncertainty

Empirical statements in MOD.14 have weakening conditions. Reliability-sensitive integration should track experimentally manipulated diagnostic reliability in the tasks claiming that mechanism. Source/provenance effects should reproduce when source information is available and attended. Prior/schema effects require task-specific direction, measurement and adequate power. A null or reversed result weakens that task-level claim; it should not be hidden by changing an arbitrary coefficient.

The executable Bayes rule has a different status: its tests establish software and algebraic correctness, not population validity. Claiming that people follow it in a particular domain would require separate human data and calibration.

## Boundaries

MOD.14 does not reactivate M1.E4, Pencode, human recruitment or population calibration. Phase M remains unchanged. The module is complete as a scientific and software architecture for explanation and normative reference computation, while its richer descriptive social/memory bridges intentionally remain conceptual until evidence justifies operationalization.
