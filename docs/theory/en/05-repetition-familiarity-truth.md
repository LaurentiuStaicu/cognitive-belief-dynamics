# Repetition, familiarity and judged truth

## Central idea

Repetition can increase the probability that a statement is judged true even when repetition adds no new evidence. This is the illusory truth effect. M0 represents it through a minimal path: exposures increase a familiarity state, and familiarity contributes positively to the log-odds of belief.

[[VAR:Nexp]] · [[VAR:F]] · [[VAR:B]] · [[MECH:repetition]] · [[VAL:VAL.M0.001]] · [[REF:REF.DECHENE.2010]] · [[CODE:m0.update_familiarity]] · [[VIEW:runs:repetition:4]]

## What research says

Dechêne and colleagues' meta-analysis synthesized 51 studies and confirmed that repetition raises subjective truth ratings. Later work shows that the effect can occur even when participants possess relevant knowledge, but it is not unlimited and depends on item type, instructions, veracity cues and context.

A much newer 2026 meta-analysis covering 182 studies estimated a small-to-moderate average effect after adjustment for small-study effects, with substantial heterogeneity. That result is useful precisely because it prevents “repetition increases perceived truth” from becoming a universal law.

A 2026 study of evaluative social-political opinion statements found negligible repetition effects within the tested bounds. CEM treats this as a reason not to automatically generalize the M0 mechanism from factual claims to normative or identity-laden opinions.

## How M0 implements it

[[VAR:Nexp]] counts scenario exposures. [[VAR:F]] is the agent's latent familiarity with the claim. The reference update is saturating:

F' = clamp01(F + alpha_f × (1 - F)).

Each additional exposure can increase F, but the marginal increment declines as familiarity approaches 1. Inspect [[CODE:m0.update_familiarity]].

In belief computation, familiarity contributes beta_f × F to latent log-odds. [[VAR:B]] is obtained through a logistic transform together with the prior, source-weighted evidence and corrective context. Ground truth does not enter that function.

The saturating form is a REFERENCE_CANDIDATE modelling choice. Research supports the repetition/familiarity phenomenon, not the exact alpha_f value or this unique saturation equation.

## Why familiarity is not truth

F is an internal state representing familiarity with a statement. It is not the statement's truth, amount of evidence, real-world event frequency or source reliability. A true and a false claim can both become familiar when repeated.

This separation is a core epistemic rule in CEM: a mechanism that changes judgment must not be reinterpreted as a property of the external world.

## Pattern test

[[VAL:VAL.M0.001]] requires repeated exposure to be able to increase judged truth under comparable conditions. The test checks a qualitative pattern; it does not reproduce a population effect size. Open [[VIEW:runs:repetition:4]] to inspect the published trajectory.

## What this chapter does not claim

It does not claim that every repetition persuades, that the effect is identical for facts and opinions, or that familiarity overrides knowledge. It does not claim that media or algorithms automatically create beliefs through repetition alone; exposure, selection, attention and context would need to be modelled separately.

## Evidence and epistemic status

[[REF:REF.DECHENE.2010]] is MODEL_EVIDENCE for the illusory-truth phenomenon. Hasher and colleagues provide historical background for familiarity. Later studies and meta-analyses are BACKGROUND_THEORY that constrain generalization; they do not calibrate M0 coefficients.