# Alpha 0.4.3a0 Phase D — M1.E4 discrimination dataset/protocol

Status: protocol-only. No model winner, runtime, Pencode, active M1.E4 registry promotion or UI.

## 1. Purpose

Phase C proved one-point equifinality between the EVSD and symmetric 2HT candidate families.

Phase D freezes the minimum data and decision protocol required before CEM may select between them.

## 2. Primary discrimination route — experimentally manipulated binary bias

The preferred route uses ordinary binary old/new recognition responses under experimentally manipulated response bias.

For each Hsimp condition, the same recognition-memory manipulation is tested under at least three independent criterion settings:

- liberal;
- approximately neutral;
- conservative.

Three nondegenerate operating points are the structural minimum because two points alone cannot distinguish a straight segment from a curved function.

This is a minimum identifiability gate, not a claim of statistical adequacy.

Preferred design:

- five or more bias conditions/operating points per Hsimp condition when feasible;
- randomized or counterbalanced bias manipulation;
- unchanged stimulus/encoding conditions across bias settings;
- raw target/foil response counts retained separately for every operating point.

Acceptable bias manipulations include:

- payoff matrix changes;
- target/foil base-rate changes;
- explicit response-criterion instructions, provided they are preregistered and do not alter encoding.

The binary-bias route is primary because confidence-rating ROCs can require additional response-mapping assumptions for threshold models.

## 3. Supplemental route — confidence ROC

A confidence-rating ROC may be collected as supplemental evidence.

The conventional preferred scale is six ordered responses from sure-new to sure-old. This produces five nontrivial cumulative ROC thresholds.

Rules:

- confidence bins and anchors must be preregistered;
- participants must not be forced post hoc into equally populated bins;
- raw category frequencies for targets and foils must be retained;
- the confidence ROC may not be the sole decisive evidence if the competing threshold model requires an additional rating-mapping layer.

A confidence-only dataset can support model fit diagnostics, but the strongest model-discrimination claim requires convergence with experimental bias manipulation or another independently identified criterion manipulation.

## 4. Minimum operating-point contract

Per Hsimp condition:

- hard minimum: 3 nondegenerate operating points;
- preferred: >=5 operating points;
- each point must have both target and foil observations;
- degenerate points at exactly 0 or 1 may be retained but do not count toward the minimum unless finite-rate correction and uncertainty are explicitly modeled;
- the operating points must span meaningfully different false-alarm rates.

CEM does not set a universal participant/trial N in this phase.

Instead, the study must pass prospective simulation-based design analysis.

## 5. Prospective candidate-recovery simulation

Before collecting or accepting a discrimination dataset, simulate data from both candidate families across a preregistered parameter grid.

The simulation must vary at least:

- memory strength/detection over weak, medium and strong regimes;
- liberal to conservative response settings;
- plausible target/foil trial counts;
- both Hsimp conditions.

The chosen sample/trial design is acceptable only if candidate recovery is adequate under both generating families.

Reference adequacy gate:

- >=0.80 probability of selecting the true generating family across the core preregistered parameter grid;
- no core region may show catastrophic asymmetric recovery where one family is almost always selected regardless of generator.

This 0.80 threshold is a CEM design convention, not a universal literature law.

## 6. Raw likelihood surface

Primary fitting must use response frequencies, not Drecog alone.

For operating point k and Hsimp condition j:

Nhit_jk ~ Binomial(Ntarget_jk, Hpred_jk)

Nfa_jk ~ Binomial(Nfoil_jk, Fpred_jk)

Retain:

- Nhit;
- Nmiss;
- Nfa;
- Ncr;
- Hobs/Fobs;
- Hpred/Fpred;
- Drecog/Crecog;
- model log-likelihood;
- parameter estimates;
- parameter count.

## 7. Candidate invariance contract

Under a manipulation intended only to alter response bias:

EVSD:
- d is shared across bias settings within the same Hsimp condition;
- c varies by bias setting.

2HT:
- Ddet is shared across bias settings within the same Hsimp condition;
- g varies by bias setting.

If a candidate requires its memory parameter to change substantially across a pure-bias manipulation to fit the data, that is a candidate-specific failure.

## 8. Model-comparison diagnostics

Both candidates must be fitted with the same raw-response dataset and predeclared optimization rules.

Required diagnostics:

- maximized log-likelihood;
- parameter count;
- AIC;
- AICc when the effective sample-to-parameter ratio makes the small-sample correction relevant;
- held-out predictive log likelihood or equivalent proper predictive score when the number of operating points/trials permits;
- parameter-recovery and candidate-recovery results from simulation;
- residuals in H/F space;
- qualitative ROC-shape/invariance checks.

No single diagnostic is sufficient by itself.

## 9. Winner-selection rule

Selection is permitted only if all of the following hold:

1. candidate-recovery simulation passed before fitting the empirical dataset;
2. one candidate has better penalized in-sample fit;
3. the same candidate has better held-out predictive performance with uncertainty excluding no difference when held-out evaluation is feasible;
4. its memory parameter is stable under the pure-bias manipulation as specified by that candidate;
5. the competing candidate shows a material qualitative or predictive failure, not merely a tiny numerical disadvantage;
6. conclusions are stable to documented reasonable analysis choices.

If these conditions do not converge, the result is:

INCONCLUSIVE_MODEL_DISCRIMINATION

No winner is selected.

Phase D intentionally does not set a universal Delta-AIC cutoff as the sole rule.

## 10. Hsimp comparison

Only after a candidate family passes the discrimination protocol may the simplicity contrast be interpreted within that family.

EVSD target:
d_simple > d_complex

2HT target:
Ddet_simple > Ddet_complex

Neither statement licenses:

Pencode_simple > Pencode_complex.

## 11. Required dataset schema

Each aggregate row must identify:

- dataset_id;
- Hsimp condition;
- bias_condition_id;
- bias_manipulation_type;
- Ntarget;
- Nfoil;
- Nhit;
- Nmiss;
- Nfa;
- Ncr;
- confidence scale metadata if applicable;
- preregistration/provenance reference.

Participant-level data are preferred when ethically/licentially available, but aggregate cell counts are sufficient for the initial binomial candidate comparison.

## 12. Planned validation patterns

VAL.M1.D01 — minimum operating points:
each Hsimp condition has at least three nondegenerate operating points.

VAL.M1.D02 — operating-point span:
false-alarm rates vary across the bias conditions.

VAL.M1.D03 — prospective candidate recovery:
the selected data design meets the preregistered recovery gate under both generators.

VAL.M1.D04 — raw-likelihood fit:
candidate comparison is fitted to target/foil response counts.

VAL.M1.D05 — bias invariance:
EVSD d or 2HT Ddet remains shared across pure-bias settings.

VAL.M1.DN01 — confidence ROC not sole decisive evidence:
confidence-only mapping cannot by itself support the strongest winner claim.

VAL.M1.DN02 — no single-metric winner:
AIC alone, Drecog alone or ROC visual appearance alone cannot select the model.

VAL.M1.DN03 — inconclusive is allowed:
discordant diagnostics must produce INCONCLUSIVE_MODEL_DISCRIMINATION.

VAL.M1.DN04 — Pencode remains blocked:
model-family selection does not identify an item-level encoding probability.

## 13. Promotion gate

Phase D may merge only if:

- protocol schema validates;
- minimum and preferred operating-point rules are explicit;
- binary bias manipulation is the primary route;
- confidence ROC is supplemental/bounded;
- candidate-recovery simulation is mandatory;
- raw likelihood is primary;
- invariance tests are explicit;
- model selection requires convergent diagnostics;
- inconclusive outcome is first-class;
- planned Phase D validations remain inactive;
- no model winner/runtime/UI/Pencode is added;
- active registries/evidence snapshot/release metadata are unchanged;
- retained outputs reproduce;
- full CI passes.

Phase D ends with a preregistration-ready discrimination protocol, not a selected recognition architecture.
