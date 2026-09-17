# Corrections, accessibility and memory

## Central idea

A correction can reduce the influence of misinformation without “deleting” it from memory. Research on the continued influence effect shows that retracted information can continue to affect reasoning, and correction effectiveness depends partly on how corrective information is integrated and retrieved.

[[VAR:C]] · [[VAR:B]] · [[MECH:correction]] · [[VAL:VAL.M0.002]] · [[CODE:m0.decay_correction]] · [[VIEW:runs:correction:5]]

## What research says

The Nature Reviews Psychology review by Ecker and colleagues synthesizes proposed mechanisms behind resistance to correction and distinguishes problems of integration, retrieval and mental-model coherence. Meta-analyses reviewed there show a robust continued-influence phenomenon, while also showing that corrections generally help and can substantially reduce misinformation influence.

A 2024 review focused on memory emphasizes that correction durability may decline over time and that memory for both the correction and its source matters. This supports the idea of dynamic accessibility but does not identify the CEM equation.

## How M0 implements it

A correction encodes corrective-context accessibility through:

C' = clamp01(C + alpha_c × (1 - C)).

Between events, M0 uses exponential decay:

C(t + dt) = clamp01(C(t) × exp(-lambda_c × dt)).

Inspect [[CODE:m0.decay_correction]]. In belief computation, the correction contributes beta_correction × C × direction, where direction can reduce or support the current claim depending on the correction event.

The representation separates the historical occurrence of a correction from its current accessibility. A correction can have been delivered while its influence on a later judgment declines.

## Why C is not “memory”

[[VAR:C]] is not a full measure of episodic or semantic memory. It has no explicit interference, reconsolidation, multiple sources, retrieval cues or narrative representations. It is a simplified corrective-accessibility state introduced to test a pattern.

This prevents statements such as “after X steps a person forgets the correction”. Steps are abstract, and lambda_c is demonstrative rather than an estimated psychological constant.

## M0 pattern

[[VAL:VAL.M0.002]] tracks two components: correction reduces belief in the reference condition, and partial regression can occur as corrective accessibility decays. [[VIEW:runs:correction:5]] displays the trajectory, not a real-time forecast.

## What this chapter does not claim

It does not claim that repeating a myth inside a correction inevitably strengthens it; contemporary reviews indicate that such backfire effects are much less general than once feared. Nor does it claim that all corrections are equally effective. Source credibility, wording, alternative explanations, timing and audience reach can matter.

## Intervention implication

In CEM, “corrective context” is a demonstrative intervention on one specific state. In the real world, correction strategies must also be evaluated for reach, comprehension, source, repetition and persistence. Chapter 12 separates those levels.