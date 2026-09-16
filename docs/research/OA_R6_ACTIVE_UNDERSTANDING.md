# R6 — Active Understanding / Learning UX Research Spike

Status: **ADOPT WITH LIMITS**  
Track: OA-5 Active Understanding  
Baseline main commit: `e7585845c9d5ade591e1ccede4d1e1b624fa210f`

## 1. Question

What is the smallest learning interaction that can make CEM easier to understand without turning the application into a quiz game, claiming educational effectiveness that has not been measured, or hiding scientific results outside an explicitly chosen learning mode?

The optimization roadmap proposes:

`Predict -> Reveal -> Explain`

plus worked examples, Challenge Model and limited competing-model comparison.

R6 decides the learning contract before OA-5 UI implementation.

## 2. Current CEM constraints

CEM already has:

- a Theory Reader;
- executable Mechanisms laboratories;
- a ten-step Guided Tour;
- Search and Universal Inspector;
- stable semantic IDs and relation layers;
- local-only lightweight Guided Tour progress;
- a versioned Workspace/Case contract;
- deterministic saved/reference model outputs.

CEM does **not** currently have evidence that its interface improves human comprehension, retention, transfer or metacognitive calibration.

Automated browser tests can verify that a learning interaction exists and preserves the scientific boundary. They cannot establish that users learned better.

## 3. Evidence reviewed

### 3.1 Prequestioning / pretesting

A preregistered meta-analysis of the prequestion effect found a moderate benefit for material directly targeted by prequestions (Hedges' g = 0.54, k = 97) but essentially no general benefit for untested material (g = 0.04, k = 91).

Consequence for CEM:

- a prediction step is justified for the **specific concept/result that is revealed immediately afterwards**;
- CEM must not claim that answering one prediction improves broad model understanding or transfer;
- challenge items should map directly to the explanation that follows.

Primary source:
- St. Hilaire KJ, Chan JCK, Ahn D. Guessing as a learning intervention: A meta-analytic review of the prequestion effect. Psychonomic Bulletin & Review. 2024;31:411–441. doi:10.3758/s13423-023-02353-8.

A broad review likewise concludes that prequestioning/pretesting can improve subsequent learning but that effects vary by procedure, material and assessment.

Primary source:
- Pan SC, Carpenter SK. Prequestioning and Pretesting Effects: a Review of Empirical Research, Theoretical Perspectives, and Implications for Educational Practice. Educational Psychology Review. 2023;35:97. doi:10.1007/s10648-023-09814-5.

Earlier experimental work shows that unsuccessful retrieval attempts can potentiate subsequent learning when followed by the correct information.

Sources:
- Kornell N, Hays MJ, Bjork RA. Unsuccessful retrieval attempts enhance subsequent learning. J Exp Psychol Learn Mem Cogn. 2009;35(4):989–998. doi:10.1037/a0015729.
- Richland LE, Kornell N, Kao LS. The pretesting effect: do unsuccessful retrieval attempts enhance learning? J Exp Psychol Appl. 2009;15(3):243–257. doi:10.1037/a0016496.
- Kornell N et al. When and why a failed test potentiates the effectiveness of subsequent study. J Exp Psychol Learn Mem Cogn. 2012. PMID 22582968.

### 3.2 Retrieval practice

Retrieval practice has a strong literature for later retention, but OA-5 is not a memory-training product and should not treat every CEM interaction as a test.

Consequence:

- later OA-5 iterations may repeat a small number of concept checks;
- initial OA-5 does not introduce spaced-repetition scheduling or a learning-score system.

Source:
- Roediger HL, Karpicke JD. The Power of Testing Memory: Basic Research and Implications for Educational Practice. Perspectives on Psychological Science. 2006.

### 3.3 Worked examples and guidance

Worked examples are generally useful for novices because they reduce unnecessary problem-solving search and allow attention to be allocated to the solution structure. Benefits can diminish as expertise grows.

Consequence for CEM:

- OA-5 should not open with an unguided challenge for every mechanism;
- each learning family should have at least one worked example before or alongside challenge items;
- challenge difficulty should be shallow at first and guidance can fade only where the interface has a clear explanation path.

Sources:
- van Gog T, Paas F, Sweller J. Cognitive Load Theory: Advances in Research on Worked Examples, Animations, and Cognitive Load Measurement. Educational Psychology Review. 2010;22:375–378. doi:10.1007/s10648-010-9145-4.
- van Gog T, Rummel N. Example-Based Learning: Integrating Cognitive and Social-Cognitive Research Perspectives. Educational Psychology Review. 2010;22:155–174. doi:10.1007/s10648-010-9134-7.
- Sweller J et al. Cognitive Architecture and Instructional Design: 20 Years Later. Educational Psychology Review. 2019. doi:10.1007/s10648-019-09465-5.

### 3.4 Productive failure / problem solving before instruction

Problem solving before instruction can help conceptual learning in some settings, but effects are conditional and do not generalize automatically across domains. Studies also show situations in which instruction-first improves procedural fluency or productive-failure effects do not replicate.

Consequence:

- CEM must not label prediction errors as inherently “productive”;
- prediction remains a short preparatory act followed immediately by reveal/explanation;
- no prolonged unguided problem-solving stage is required for OA-5.

Sources:
- Hartmann C, van Gog T, Rummel N. Preparatory effects of problem solving versus studying examples prior to instruction. Instructional Science. 2021;49:1–21. doi:10.1007/s11251-020-09528-z.
- Loibl K et al. The effect of contrasting cases during problem solving prior to and after instruction. Instructional Science. 2020;48:115–136. doi:10.1007/s11251-020-09504-7.
- “When failure fails to be productive: probing the effectiveness of productive failure for learning beyond STEM domains.” Instructional Science. 2021. doi:10.1007/s11251-020-09525-2.

### 3.5 Confidence and feedback

Confidence judgments can be useful for comparing what the learner expected with what the model/result shows. Feedback can improve retention even for correct answers made with low confidence.

Consequence:

- OA-5 may optionally collect confidence with a prediction;
- confidence is a learner-entered metacognitive judgment, **not** a scientific confidence estimate and not a diagnostic measure;
- CEM should not calculate a global “epistemic competence”, “rationality” or intelligence score;
- any calibration summary is descriptive, local and clearly scoped to answered OA-5 items.

Source:
- Butler AC et al. Correcting a metacognitive error: feedback increases retention of low-confidence correct responses. J Exp Psychol Learn Mem Cogn. 2008. PMID 18605878.

### 3.6 Worked-example comparison and erroneous/contrasting cases

Comparing cases can help attention to structural differences in some settings, but results are mixed and boundary conditions matter.

Consequence:

- “Challenge Model” may compare **existing scientifically registered alternatives** when the repository already has them;
- OA-5 must not manufacture competing scientific models merely to make a pedagogical exercise;
- contrasting correct/incorrect or null/richer models is permitted only when the contrast is already part of CEM's scientific/validation artifacts.

Sources:
- Loibl K et al. Instructional Science. 2020;48:115–136. doi:10.1007/s11251-020-09504-7.
- Conditions for Effective Learning from Erroneous Examples: A Systematic Review. Educational Psychology Review. 2025. doi:10.1007/s10648-025-10071-x.

## 4. Decision

**ADOPT WITH LIMITS.**

OA-5 will implement an explicit Active Understanding learning mode built from a small state machine:

1. **Worked example / context**
2. **Predict**
3. optional **Confidence**
4. **Reveal**
5. **Compare prediction with model result**
6. **Explain**
7. **Epistemic boundary**
8. optional **Try another / Challenge**

The reveal must use existing canonical CEM outputs, equations, semantic identities and evidence/status metadata.

The prediction step must never change the model result.

## 5. First OA-5 concept families

The first implementation must cover the three boundaries already named in the OA-5 exit gate.

### AU-1 — Exposure versus familiarity

Learning target:
- exposure count/event is not the same variable as familiarity;
- repeated exposures can update F according to the reference model;
- F is not truth or evidence strength.

Candidate challenge:
- predict the direction of F after the next registered exposure;
- reveal the saved reference frame and signed decomposition;
- explain which event and equation produced the change.

### AU-2 — Belief versus sharing

Learning target:
- latent truth-belief B and sharing probability/decision are distinct;
- an accuracy cue can affect the sharing pathway without directly changing B.

Candidate challenge:
- predict which observable/latent quantity changes directly after the accuracy cue;
- reveal the saved reference frame;
- compare B, W and Share/Pshare using existing step explanations.

### AU-3 — Computation versus scientific causal evidence

Learning target:
- a computational dependency is not automatically an empirically validated causal relationship;
- evidence-qualified registered links and executable dependencies are separate Semantic Spine relation layers.

Candidate challenge:
- classify a displayed relation as computational dependency, registered evidence relation or documentation relation;
- reveal using Universal Inspector;
- explain the available evidence/status facets.

These three concept families are required before OA-5 may claim the Active Understanding foundation is complete.

## 6. Challenge Model boundary

Challenge Model is permitted only over existing alternatives.

Initial eligible candidates include:

- explicit null versus richer nested comparator outputs already registered by M1 stages;
- registered validation/null-model contrasts;
- saved scenario contrasts where the invariant/change is explicitly documented.

Not allowed in OA-5:

- inventing a new scientific comparator;
- fitting a new mechanism for learning UX;
- presenting a pedagogical distractor as a scientifically plausible model unless it is explicitly labelled as a didactic misconception rather than a scientific candidate.

## 7. Prediction format

Start with categorical or directional predictions where the scientific target supports them.

Preferred first formats:

- increase / decrease / approximately unchanged;
- A / B / neither;
- relation-layer classification;
- choose which of two already-defined model outputs is directly affected.

Avoid initially:

- exact numerical guesses that imply calibrated knowledge when coefficients are demonstrative;
- free-form scoring by an LLM;
- unbounded text grading;
- confidence percentages presented as probabilities of scientific truth.

## 8. Reveal and explanation contract

A reveal must provide, where available:

- canonical entity/result ID;
- user's prediction;
- actual saved/model result;
- concise correctness/contrast statement;
- mechanism explanation;
- equation or signed decomposition;
- evidence/status facet;
- explicit “what this does not establish” boundary;
- link to Theory, Universal Inspector or the originating application surface.

A reveal must not:

- strengthen the scientific status;
- claim a mechanism is true because the user predicted it incorrectly/correctly;
- replace a scientific result with a pedagogical approximation if the canonical result is available.

## 9. Confidence contract

Confidence is optional.

Initial UI should use a small ordinal scale rather than a false-precision percentage, for example:

- low;
- medium;
- high.

Stored meaning:

“learner confidence in their own prediction before reveal”.

It is not:

- confidence interval;
- Bayesian posterior;
- model confidence;
- evidence quality;
- psychological trait.

## 10. Local prediction history

OA-5 history is local-only.

For the first implementation:

- do not modify `workspace.schema.json`;
- use a separate versioned local learning-history record;
- store only challenge ID, canonical target refs, prediction category, optional confidence, outcome category and timestamp;
- no free-form personal notes by default;
- no telemetry, remote analytics, account or cloud sync;
- provide clear/delete-local-history control before expanding history depth;
- bound retention rather than allowing unbounded local growth.

Prediction history is a learning aid, not scientific provenance and not a replacement for Workspace/Case provenance.

## 11. Evaluation boundary

Automated tests can verify:

- prediction precedes reveal in Active Understanding;
- the scientific result is not hidden in normal Analyze/Mechanisms/Registry modes;
- reveal values equal canonical saved/model outputs;
- the three required conceptual boundaries have challenge coverage;
- RO/EN parity;
- keyboard/focus behavior;
- mobile/200% text reflow;
- history is local, bounded and clearable.

Automated tests cannot verify:

- increased comprehension;
- improved retention;
- transfer;
- metacognitive calibration;
- educational superiority over the existing Theory/Guided Tour.

Any claim that OA-5 improves learning effectiveness requires a separate user-study/evaluation design.

## 12. UX design consequences

- Active Understanding is an explicit mode under Understand; it does not alter default Analyze results.
- “Predict” is low-stakes and may be skipped.
- Reveal is immediate after submission.
- Wrong predictions receive neutral discrepancy feedback, not punitive scoring.
- The canonical explanation is more important than a points/reward system.
- No streaks, leaderboard, badges or global score are required.
- Worked examples should precede or accompany challenge items for novice concepts.
- A user can always open Theory or Universal Inspector from the reveal.

## 13. Accessibility consequences

OA-5 should use ordinary semantic form controls where possible.

Required behavior:

- visible prompt and labels;
- keyboard-operable choices;
- explicit Submit/Reveal action;
- reveal region announced without moving the user into an unexpected modal;
- focus moved only after explicit user action and to a stable heading/region;
- no drag-only interaction;
- no timed response requirement;
- correctness not encoded by color alone;
- reflow at mobile/200% text remains a release gate.

## 14. Acceptance criteria for R6

R6 is complete because it records:

- the learning question;
- authoritative literature sources;
- benefits and boundary conditions;
- the ADOPT WITH LIMITS decision;
- initial challenge families;
- local-history/privacy boundary;
- automated-testing versus human-learning-evidence boundary;
- consequences for OA-5 schemas/UI/tests.

## 15. Consequences for OA-5 implementation slices

Recommended slices:

### OA-5A — Active Understanding contract

- canonical challenge-item schema/data contract;
- state machine;
- local bounded learning-history contract;
- deterministic fixtures for AU-1/AU-2/AU-3;
- no UI.

### OA-5B — Predict / Reveal / Explain UI

- explicit Active mode under Understand;
- worked example;
- prediction + optional confidence;
- canonical reveal/explanation;
- keyboard/mobile/RO-EN tests.

### OA-5C — Challenge Model

- consume existing registered null/comparator alternatives only;
- side-by-side model assumptions/predictions/status;
- no new scientific model.

### OA-5D — Audit and learning-boundary completion

- verify all three required concept families;
- clear/delete local history;
- cross-link to Theory/Search/Inspector;
- manual usability/accessibility audit;
- post-merge regression.

## 16. Research conclusion

The literature supports using short, targeted prediction/prequestion steps followed by immediate corrective information, and supports worked examples as an important scaffold for novices.

It does **not** justify treating prediction-first learning as universally superior, assuming transfer to untested concepts, or interpreting a learner's confidence/performance as a global epistemic trait.

Therefore CEM should implement Active Understanding as a constrained explanatory interaction around canonical model results, not as a gamified assessment system.
