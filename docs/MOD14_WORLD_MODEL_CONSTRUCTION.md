# MOD.14 — World-model construction / Construirea modelului realității

Status: integrated scientific design for Alpha; population calibration is not claimed.

## Scientific question

MOD.14 asks how an agent-relative internal representation can be constructed and revised when the agent has access only to selected observations, memory and prior information, source/provenance cues, social context and uncertain evidence. The module does **not** equate an internal representation with external reality. It treats a world model as partial, task-bound and revisable.

## Audit of existing CEM structure

The pre-MOD.14 CEM already contains constructs that must not be duplicated: claim familiarity `F`, corrective-context accessibility `C`, estimated source reliability `T`, latent claim-belief propensity `B`, exposure history `Nexp`, observed-sample balance `Sobs`, issue appraisal `Aissue`, preview impression and access, presentation variables and prior-attitude congruence. MOD.14 therefore acts as an integration layer around these neighboring constructs rather than creating a second familiarity, memory, trust or belief system.

`B` remains the existing descriptive latent propensity to judge a claim true in M0. `Aissue` remains the bounded M1 issue-appraisal state. `Pwm`, introduced only inside the MOD.14 world-model contract, is a **normative proposition-level reference probability** used to demonstrate transparent evidence updating when a defensible diagnostic likelihood ratio is externally available. These quantities are intentionally not interchangeable.

The existing decision-uncertainty machinery is also distinct. It represents registered scenario uncertainty for decision analysis and refuses to manufacture scenario probabilities. `Uwm` is only binary Shannon entropy derived from `Pwm`; it is not a replacement for decision uncertainty, metacognitive confidence or model uncertainty.

## Literature audit and epistemic classification

### EMPIRICAL

Ernst and Banks (2002) showed in a controlled visual–haptic task that observed cue integration could closely approximate a reliability-weighted maximum-likelihood integrator. This supports the narrower proposition that uncertainty-sensitive integration can be observed in specific controlled tasks; it does not establish a universal Bayes algorithm for cognition.

Zwaan and Radvansky (1998) reviewed situation models as integrated mental representations of described states of affairs. Johnson, Hashtroudi and Lindsay (1993) reviewed source monitoring and source-attribution phenomena. Ecker et al. (2022) reviewed cognitive, social and affective drivers of misinformation belief and barriers to knowledge revision. These literatures support the inclusion of representation, provenance and revision as empirical phenomena, but they do not provide a universal scalar equation mapping memory, source, social context and attention into a single posterior.

Knill and Pouget (2004) reviewed Bayesian computational theories of perception and action and emphasized uncertainty representation. Their review is relevant to the computational framing but is not evidence that all higher-level belief updating literally implements Bayes' rule.

Sperber et al. (2010) proposed epistemic vigilance as a suite of mechanisms for evaluating communicated information. MOD.14 uses this as a conceptual/empirical organizing source for source/social evaluation, not as an executable universal mechanism.

### EXECUTABLE

The executable surface is intentionally narrow. When a binary prior probability `p0` and a defensible likelihood ratio `LR` are supplied by a domain-specific diagnostic/measurement model, MOD.14 computes:

`p1 = (p0 × LR) / (p0 × LR + 1 − p0)`

Equivalently, posterior odds equal prior odds multiplied by `LR`. The derived proposition uncertainty is binary Shannon entropy:

`Uwm = −p log2(p) − (1−p) log2(1−p)`

with the conventional endpoint value zero. These are normative reference calculations. They do not assert a neural implementation and they do not estimate human-population parameters.

The executable operator fails closed. MOD.14 does not turn familiarity, source trust, repetition, agreement, salience or attention into an LR. Sequential LRs must not be multiplied naively when evidence items are dependent.

### CONCEPTUAL

The conceptual world-model loop has seven stages: observation/selection; retrieval of prior information and memory; provenance/source evaluation; social-context interpretation; proposition update where justified diagnostic evidence exists; explicit retention of uncertainty; contradiction/correction-driven reassessment.

The stages organize already-existing CEM mechanisms and identify measurement bridges that future empirical work could test. They are not assumed to form a single linear causal chain in every task.

### INTERPRETIVE

Predictive-coding, Bayesian-brain and related generative-model accounts are useful ways to think about internal representations and prediction error. MOD.14 does not encode them as a universal equation. “Constructed reality” means an internal, partial and revisable model of external states of affairs; it does not mean cognition creates the external world.

## Variables and relations

The canonical world-model contract defines `Pprior`, externally supplied `LR`, normative posterior `Pwm`, derived uncertainty `Uwm`, and a provenance record `Prov`. It also defines mechanism entities for observation/selection, prior-memory retrieval, provenance/source evaluation, social context, normative updating, uncertainty tracking and contradiction/reassessment.

Relations are tagged by epistemic level and sign. The only fixed executable mapping is the Bayes update and the entropy derivation. All paths from psychological/social constructs into evidence diagnosticity are marked as requiring a measurement bridge rather than receiving invented coefficients.

## Temporal semantics

Time is a discrete evidence-update event. It has no automatic mapping to seconds, days or years. An update cycle may contain observation, context retrieval, provenance evaluation, a diagnostic update if one is justified, uncertainty retention and later reassessment. This matches the existing CEM practice of avoiding false real-time interpretation of abstract simulation steps.

## Falsification and weakening conditions

Empirical claims are paired with conditions that would weaken them. Reliability-sensitive cue integration should vary with experimentally estimated diagnostic reliability in the specific tasks claiming that mechanism. Schema/prior effects require reproducible outcome differences after manipulation and adequate manipulation checks. Source/provenance effects require reproducible attribution/evaluation differences when source information is available and attended.

The Bayes formula itself is not an empirical theory of human cognition to be “validated” by population fit. Its test is software/algebraic correctness. Any claim that it is a useful descriptive approximation in a specific human task would require separate empirical validation.

## Software boundary

`src/cognitive_epistemic_model/world_model.py` implements only the normative operator and entropy metric. Contract tests enforce the four epistemic levels, cross-link resolution, non-duplication and the M1/Phase M boundary. UI integration presents the mechanism loop, a small interactive update example, evidence, limitations and cross-links in bilingual EN/RO form.

MOD.14 does not reactivate M1.E4, Pencode estimation, human recruitment or population calibration. The recorded Phase M result is untouched.

## Primary references

- Ernst, M. O., & Banks, M. S. (2002). *Humans integrate visual and haptic information in a statistically optimal fashion*. Nature, 415, 429–433. https://doi.org/10.1038/415429a
- Knill, D. C., & Pouget, A. (2004). *The Bayesian brain: the role of uncertainty in neural coding and computation*. Trends in Neurosciences, 27, 712–719. https://doi.org/10.1016/j.tins.2004.10.007
- Zwaan, R. A., & Radvansky, G. A. (1998). *Situation models in language comprehension and memory*. Psychological Bulletin, 123, 162–185. https://doi.org/10.1037/0033-2909.123.2.162
- Johnson, M. K., Hashtroudi, S., & Lindsay, D. S. (1993). *Source monitoring*. Psychological Bulletin, 114, 3–28. https://doi.org/10.1037/0033-2909.114.1.3
- Sperber, D., Clément, F., Heintz, C., Mascaro, O., Mercier, H., Origgi, G., & Wilson, D. (2010). *Epistemic Vigilance*. Mind & Language, 25, 359–393. https://doi.org/10.1111/j.1468-0017.2010.01394.x
- Ecker, U. K. H., Lewandowsky, S., Cook, J., et al. (2022). *The psychological drivers of misinformation belief and its resistance to correction*. Nature Reviews Psychology, 1, 13–29. https://doi.org/10.1038/s44159-021-00006-y
