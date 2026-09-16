# Alpha 0.4.3a0 Phase C — M1.E4 generative-candidate comparison

Status: pre-runtime model-comparison contract only. No active M1.E4 model, runtime, UI, Pencode or beta-simplicity parameter is introduced by this phase.

## 1. Scientific question

Phase A selected headline simplicity as the controlled cue and recognition sensitivity as the direct validation construct.

Phase B froze the measurement bridge:

raw target/foil responses -> hit/false-alarm rates -> Drecog + Crecog.

Phase C asks:

> Which classes of latent generative model could produce the same observed recognition operating point, and what additional data would actually discriminate them?

This phase must not select a cognitive mechanism merely because it can reproduce a published mean d-prime.

## 2. Core result: one yes/no operating point is not model-discriminating

For one condition with one pair of observed rates (H,F):

- an equal-variance continuous SDT model can always recover a sensitivity and criterion;
- a symmetric two-high-threshold model can also recover a detection parameter and guessing parameter whenever 0 <= F <= H <= 1.

Therefore one operating point is generically insufficient to decide whether recognition is better represented as continuous evidence strength or as discrete detection plus guessing.

The Phase C comparator must demonstrate this equifinality explicitly.

## 3. Candidate C1 — continuous evidence-strength SDT

Candidate ID:

`CANDIDATE.M1.E4.C1.EVSD`

Reference assumptions:

- foil evidence: Normal(-d/2, 1);
- target evidence: Normal(+d/2, 1);
- one response criterion c;
- response “seen” iff sampled evidence exceeds c.

Equivalent response probabilities:

`H = Phi(d/2 - c)`

`F = Phi(-d/2 - c)`.

From one nondegenerate operating point:

`d = z(H) - z(F)`

`c = -0.5 * [z(H) + z(F)]`.

The parameter `d` is a continuous evidence-separation parameter inside this candidate.

It is not:

- Pencode;
- a probability;
- neural encoding strength;
- direct attention;
- recollection probability.

The equal-variance assumption remains a simplifying reference assumption inherited from Phase B, not an established property of recognition memory.

## 4. Candidate C2 — discrete two-high-threshold + guessing

Candidate ID:

`CANDIDATE.M1.E4.C2.2HT`

For the first fair comparator, Phase C uses the symmetric two-high-threshold form with:

- `Ddet`: probability of entering the correct detection state for either target or foil;
- `g`: probability of responding “seen” from the uncertain state.

Response probabilities:

`H = Ddet + (1 - Ddet) * g`

`F = (1 - Ddet) * g`.

For one operating point with `H >= F` and `Ddet < 1`:

`Ddet = H - F`

`g = F / (1 - Ddet)`.

If `Ddet = 1`, `g` is irrelevant because the uncertain state is never entered.

`Ddet` is a model-specific detection-state probability.

It is explicitly **not** renamed `Pencode`.

A more general asymmetric 2HT model with separate old-item and new-item detection parameters would introduce at least three latent parameters for two observed response probabilities and is therefore underidentified from one operating point.

## 5. Why both candidates can fit one operating point

The continuous candidate maps one pair (H,F) to `(d,c)`.

The symmetric 2HT candidate maps the same pair (H,F) to `(Ddet,g)`.

Thus the published condition-level d-prime means from Shulman do not select either model.

Matching:

- Drecog = 1.23;
- Drecog = 0.80;

is insufficient because those summaries do not uniquely determine the raw operating points and, even if H and F were known, one point can be represented by both candidate families.

## 6. Required future discrimination data

Phase C selects two acceptable classes of additional evidence.

### A. Multiple criterion / confidence operating points

Collect multiple operating points for the same underlying stimulus condition by:

- confidence ratings;
- experimentally manipulated response bias;
- payoff/base-rate manipulation.

The primary discriminating object becomes the ROC.

Classic continuous SDT predicts a curved ROC in probability coordinates.

The basic 2HT model predicts a linear ROC when bias/guessing varies with the detection parameter held fixed.

The literature contains an active historical debate, so ROC curvature must be treated as evidence for model comparison, not an absolute theorem.

### B. Bias manipulation with invariant memory parameters

Manipulate response bias while holding encoding/stimulus conditions fixed.

Candidate-specific memory parameters should remain stable:

- EVSD: d stable, criterion c changes;
- symmetric 2HT: Ddet stable, guessing g changes.

A candidate that can fit the data only by changing its memory parameter under a pure bias manipulation fails the candidate contract.

## 7. Raw-response likelihood is the primary fitting surface

Future fitting must operate on target/foil counts, not only derived Drecog.

For each condition j and criterion/bias setting k:

`Nhit_jk ~ Binomial(Ntarget_jk, Hpred_jk)`

`Nfa_jk ~ Binomial(Nfoil_jk, Fpred_jk)`.

The model comparison must retain:

- Nhit;
- Nmiss;
- Nfa;
- Ncr;
- predicted H and F;
- derived Drecog and Crecog;
- model log-likelihood or equivalent proper scoring metric.

Drecog/Crecog are diagnostics/summary validation layers, not the only fitting target.

## 8. Fairness constraints

The candidate comparison must be parameter-count aware.

The initial comparator uses:

- C1 EVSD: one memory parameter d per Hsimp condition plus criterion parameters for response settings;
- C2 symmetric 2HT: one detection parameter Ddet per Hsimp condition plus guessing parameters for response settings.

No candidate may receive an extra condition-specific free parameter merely to force a better fit unless the competing candidate receives an analogous degree of flexibility and the scientific rationale is explicit.

Model selection must report:

- log-likelihood;
- parameter count;
- AIC or another predeclared penalized criterion;
- out-of-sample or held-out predictive fit when enough operating points exist.

AIC alone is not causal proof; it is only one model-comparison diagnostic.

## 9. Hsimp effect contract

If a future dataset supports a simplicity effect, the candidate-specific statement is:

### EVSD

`d_simple > d_complex`

with response criterion allowed to vary independently.

### symmetric 2HT

`Ddet_simple > Ddet_complex`

with guessing allowed to vary independently.

Neither inequality is equivalent to:

`Pencode_simple > Pencode_complex`.

The latter remains forbidden unless independently identified in a later contract.

## 10. Counterevidence and model uncertainty

Phase C retains the literature conflict rather than encoding a preferred winner.

Relevant evidence includes:

- recognition ROC work supporting continuous SDT over simple threshold models;
- validation studies showing 2HT can function as a useful measurement model;
- work demonstrating that recognition-memory SDT often requires unequal variance rather than the simplest equal-variance form.

Therefore CEM does not declare either C1 or C2 the true cognitive architecture in this phase.

## 11. Planned validation patterns

### VAL.M1.G01 — one-point equifinality

For at least one nondegenerate synthetic operating point, both C1 and C2 must reconstruct the same H and F exactly within numerical tolerance.

### VAL.M1.G02 — EVSD inverse consistency

For nondegenerate H,F, the EVSD inverse mapping to d,c and forward mapping back to H,F must be numerically consistent.

### VAL.M1.G03 — symmetric 2HT inverse consistency

For valid H,F with H >= F, the 2HT inverse mapping to Ddet,g and forward mapping back to H,F must be numerically consistent.

### VAL.M1.GN01 — Pencode remains absent

Neither EVSD d nor 2HT Ddet may be relabeled as Pencode.

### VAL.M1.GN02 — one operating point cannot select a model family

Documentation and future code must reject any claim that a single H,F point or a single mean d-prime identifies C1 versus C2.

### VAL.M1.GN03 — bias manipulation preserves memory parameter

Under a synthetic pure-bias manipulation, candidate tests must vary c or g while holding d or Ddet fixed.

### VAL.M1.GN04 — raw-response fitting required

Future candidate fitting must use raw/binomial response data when available rather than fitting only the published mean Drecog.

### VAL.M1.GN05 — ROC assumptions are model-specific

ROC curvature/linearity expectations must be represented as candidate predictions with documented assumptions, not as universal facts.

## 12. Promotion gate

Phase C may merge only if:

- exactly two primary candidate families are frozen;
- formulas and inverse mappings are explicit;
- one-point equifinality is demonstrated;
- asymmetric 2HT underidentification is documented;
- Pencode remains blocked;
- future discrimination requires multiple operating points or bias manipulation;
- raw-response likelihood is the primary future fitting surface;
- parameter-count fairness is explicit;
- planned generative validation IDs remain absent from the active validation registry;
- no recognition/encoding runtime is added;
- no UI is added;
- active variables, links, references, targets and evidence snapshot remain unchanged;
- retained M0/M1.E1/M1.E2/M1.E3 outputs remain reproducible;
- full CI passes.

## 13. Forbidden changes

No:

- active C1 or C2 model registration;
- runtime model fitting;
- runtime recognition simulator;
- Pencode;
- beta-simplicity;
- new attention state;
- UI comparator;
- winner declaration between C1 and C2;
- calibration to Shulman mean d-prime alone;
- release-version change;
- evidence-snapshot change.

Phase C ends with a formal model-discrimination design, not a selected cognitive mechanism.
