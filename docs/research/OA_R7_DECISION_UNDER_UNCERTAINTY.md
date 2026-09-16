# OA R7 — Decision Under Uncertainty

Status: **ADOPT WITH LIMITS — research and decision contract only**

Date: 2026-09-16

Target stage: **OA-6 — Decision Under Uncertainty**

Baseline: `e62324dcd4551dafe423387b6e8217e1eac021e6` (OA-5 closed; post-merge CI #223 successful).

## 1. Research question

How should CEM help a user compare and plan interventions when:

- model parameters are demonstrative rather than population-calibrated;
- some uncertainties are parameter-like while others are structural, evidential, preference-based or implementation-related;
- several objectives may conflict;
- probabilities over future states are unavailable or unjustified;
- the current planner already supports budget, objective weights, intervention timing, three ±30% response profiles, bundle comparison, interaction audits and a stability count;
- the application must not turn exploratory outputs into a real-world policy recommendation.

The problem is not simply “show error bars”. It is to design a decision surface that makes uncertainty part of the reasoning process while preserving the scientific boundaries of CEM.

## 2. Current CEM baseline

The existing planner is already conservative in several important ways.

It states that:

- intervention priorities depend on objective, effort and assumptions;
- the three response profiles are a limited sensitivity test, not confidence intervals;
- the score is not a probability;
- the “remains top-ranked 3/3” indicator is exploratory stability, not a probability;
- effort units are user-supplied rather than observed costs;
- favorable synthetic conditions are not guaranteed in practice;
- simulated interaction differences do not establish real-world synergy;
- factor contributions are conditional, not universal factor weights;
- the resulting plan is illustrative and uncalibrated.

These boundaries should be preserved. OA-6 should improve uncertainty reasoning around this planner, not replace those warnings with stronger-looking but unjustified statistics.

## 3. Research synthesis

### 3.1 Deep uncertainty requires stress testing, not forced prediction

Robust Decision Making (RDM) treats models as exploratory tools when stakeholders do not know or agree on the correct model, future conditions or valuation of outcomes. Rather than first choosing one forecast and optimizing against it, RDM stress-tests candidate strategies across many plausible futures, identifies conditions under which strategies fail, and searches for strategies that remain acceptable across a wide range of cases.

For CEM this implies:

- do not convert the existing three response profiles into a pseudo-probability distribution;
- do not call the current best bundle “most likely best”;
- use scenarios/profiles to test vulnerability and robustness;
- keep the distinction between “best under this assumption” and “robust across assumptions” explicit.

Primary research basis:

- Lempert, R. J. (2019), “Robust Decision Making”, in *Decision Making under Deep Uncertainty*: https://link.springer.com/chapter/10.1007/978-3-030-05252-2_2
- RAND Robust Decision Making overview: https://www.rand.org/pubs/tools/TL320/tool/robust-decision-making.html
- Lempert et al. (2006), robust strategies and narrative scenarios: https://doi.org/10.1287/mnsc.1050.0472

### 3.2 Different uncertainty types must remain separate

NICE guidance explicitly distinguishes different sources of uncertainty, including parameter and structural uncertainty, and asks decision makers to consider whether the uncertainty represented in an analysis has been adequately captured and which uncertainty may or may not be reduced through further evidence.

IPCC practice also separates:

- qualitative confidence in a finding, grounded in evidence and agreement;
- probabilistic likelihood, which is a separate quantitative concept.

For CEM this means one generic “uncertainty score” is inappropriate.

OA-6 should maintain an uncertainty ledger with separate dimensions such as:

1. **Parameter uncertainty** — uncertainty in numerical inputs/coefficients.
2. **Structural uncertainty** — uncertainty about equations, mechanisms, omitted relationships or model form.
3. **Evidence uncertainty** — limitations in the evidence supporting a relation or intervention rationale.
4. **Scenario uncertainty** — uncertainty about external conditions or context.
5. **Preference uncertainty** — uncertainty or disagreement in objective weights and trade-offs.
6. **Implementation uncertainty** — uncertainty in feasibility, cost, timing, adherence or operational execution.
7. **Measurement uncertainty** — uncertainty in observed quantities used to anchor or evaluate a decision.

These categories may overlap in practice, but the UI must not collapse them into a single confidence percentage.

Primary basis:

- NICE, “Exploring uncertainty”: https://www.nice.org.uk/consultations/2261/1/economic-evaluation
- IPCC AR6 WGI Chapter 1, uncertainty and calibrated language: https://www.ipcc.ch/report/ar6/wg1/chapter/chapter-1/

### 3.3 Decision uncertainty is not scientific confidence

A decision can be unstable even when one scientific result is well supported, and a decision can remain stable despite wide scientific uncertainty if all plausible states favor the same action.

Therefore CEM should distinguish:

- **scientific/evidential uncertainty** about the model and its inputs;
- **decision uncertainty** about whether a different admissible assumption set changes the preferred decision;
- **learner confidence** from OA-5, which is a personal metacognitive state and must remain unrelated to both.

No UI element may reuse the same “confidence” vocabulary for all three.

### 3.4 Robustness should be presented as performance across declared scenarios

For the current CEM planner, the first safe robustness layer can be deterministic and scenario-based.

Candidate bundle-level metrics that are valid without inventing probabilities:

- number or proportion of declared scenarios in which the bundle is feasible;
- number or proportion of declared scenarios in which it meets a user-declared acceptability threshold;
- worst observed score or gain across the declared scenario set;
- best observed score or gain across the declared scenario set;
- score/gain range across the declared scenario set;
- rank range across the declared scenario set;
- **regret** per scenario, defined relative to the best feasible bundle in that same scenario;
- maximum regret across the declared scenario set;
- median/mean regret only when the aggregation rule is explicitly user-selected and not presented as an expected value;
- conditions/scenarios in which the bundle ceases to be acceptable.

A “3/3 profiles” indicator may remain, but its label should make the denominator concrete: “top-ranked in 3 of 3 declared response profiles”, never “75%/100% chance” or similar.

### 3.5 Expected utility requires justified probabilities and utilities

Expected-value or expected-utility analysis is appropriate only when:

- probabilities over relevant states are available and defensible;
- consequences can be mapped to a declared utility/value function;
- the decision maker accepts the aggregation.

CEM does not currently satisfy these requirements for its ±30% profiles.

Therefore OA-6 must not:

- assign equal probability 1/3 to low/reference/high by default;
- infer probability weights from profile spacing;
- label a weighted mean across arbitrary profiles “expected outcome”;
- calculate expected value of perfect information (EVPI) from uncalibrated scenario weights.

The architecture may reserve fields for probability-bearing uncertainty objects later, but missing probabilities must remain missing.

### 3.6 Value of information is useful, but numerical VOI is deferred

NICE decision methods use uncertainty analysis partly to identify which uncertainties matter to the decision and which evidence could reduce them. This is highly relevant to CEM’s epistemic purpose.

OA-6 should therefore support an **information-priority** concept before it supports numeric VOI.

Safe first-stage questions are:

- Which uncertain assumptions cause the preferred bundle to change?
- Which uncertain assumptions drive the largest regret or largest threshold failures?
- Which uncertainties are reducible by measurement, experiment, literature review or implementation study?
- Which are structural/value uncertainties that additional data may not resolve?
- Would resolving a given uncertainty change the decision?

A numeric EVPI/EVSI module is deferred until CEM has defensible probability distributions and a declared utility model.

Primary basis:

- NICE, uncertainty and decision error: https://www.nice.org.uk/consultations/2261/1/committee-recommendations
- NICE, early-use assessments and prioritizing uncertainties for further data collection: https://www.nice.org.uk/process/pmg48/chapter/early-use-healthtech-guidance-assessments

### 3.7 Adaptive decisions need monitoring and trigger conditions

Decision Making under Deep Uncertainty literature emphasizes adaptive strategies: choose an initial action, monitor the system, and define conditions under which the plan should change.

CEM already has intervention timing and a schedule representation, so OA-6 should extend planning with a bounded adaptive layer rather than introduce a new forecasting engine.

A future adaptive plan should be able to record:

- current action/bundle;
- monitored indicator;
- trigger condition;
- alternative action;
- reason/provenance for the trigger;
- earliest/latest reassessment point;
- whether the trigger is executable, empirical, conceptual or user-defined.

This is not a claim that CEM predicts when the trigger will occur.

Useful background:

- *Decision Making under Deep Uncertainty: From Theory to Practice* (open access): https://link.springer.com/book/10.1007/978-3-030-05252-2

### 3.8 Uncertainty visualization must avoid point-estimate fixation

Research on uncertainty visualization shows that users can overweight central estimates and neglect uncertainty. Distributional or discrete representations can improve some probability judgments, while means/point estimates can bias attention.

For CEM:

- if a genuine probability distribution is available later, prefer a representation that makes the distribution visible rather than only a mean ± interval;
- for the current finite scenario set, use scenario dots/rows/small multiples or a scenario matrix rather than fake density plots;
- never render the low/reference/high profiles as a smooth probability distribution;
- display exact numeric tables alongside graphics;
- encode distinctions with labels/patterns as well as color;
- show the scenario source and quantification status next to the visualization.

Evidence basis:

- Kale, Kay & Hullman (2021), uncertainty visualizations and decision strategies: https://idl.uw.edu/papers/effect-size-judgments
- Padilla et al. (2021), multiple types of uncertainty and quantile-dotplot reasoning: https://pmc.ncbi.nlm.nih.gov/articles/PMC7868089/

## 4. OA-6 product decision

**ADOPT WITH LIMITS.**

OA-6 should add a **Decision Under Uncertainty** layer to the existing Act / Priorities & Plan surface.

It should not create a separate “oracle” that chooses for the user.

The system should answer four questions in sequence:

1. **What is uncertain?**
   - explicit uncertainty ledger;
   - source/provenance;
   - quantification status;
   - reducibility;
   - affected model objects and decisions.

2. **What changes if assumptions change?**
   - scenario/profile comparison;
   - rank stability;
   - threshold stability;
   - regret;
   - failure conditions.

3. **Which decisions are robust enough for the declared objective?**
   - robustness table/frontier;
   - no universal winner label;
   - explicit trade-offs and exceptions.

4. **What should be learned or monitored next?**
   - information-priority list;
   - reducible vs irreducible uncertainty;
   - monitoring/reassessment triggers;
   - no numeric VOI until probability/utility prerequisites exist.

## 5. Canonical uncertainty object

OA-6 should begin with a schema-validated uncertainty registry rather than hard-coded UI metadata.

Proposed conceptual shape:

```text
id
label.ro / label.en
uncertainty_type
target_ids[]
source_kind
source_refs[]
quantification_status
value_domain / scenarios
probability_status
reducibility
decision_relevance
limitations.ro / limitations.en
```

Required `quantification_status` classes:

- `QUALITATIVE`
- `BOUNDED_RANGE`
- `FINITE_SCENARIOS`
- `PROBABILITY_DISTRIBUTION`

Required `probability_status` classes:

- `NOT_AVAILABLE`
- `USER_DECLARED`
- `EMPIRICALLY_ESTIMATED`
- `MODEL_DERIVED`

The registry must fail closed: a finite scenario set cannot be consumed by an expected-value calculation unless probabilities are explicitly present and valid.

## 6. First executable scope

The safest first executable OA-6 scope is the existing intervention planner, because its uncertainty boundaries are already explicit.

OA-6 should initially reuse:

- the 16 existing intervention bundles;
- the low/reference/high response profiles;
- the existing objective weight;
- user-supplied effort costs;
- early/late activation;
- existing bundle score/gain calculations.

It should derive only new decision-audit quantities such as:

- per-profile rank;
- rank range;
- per-profile regret;
- maximum regret;
- acceptable/not acceptable per user-defined threshold;
- threshold coverage across the finite profile set;
- profile(s) causing a decision switch.

No new M0/M1 equation is required for this first scope.

## 7. Proposed implementation slices

These slices are defined by this R7 contract and therefore are not ad-hoc phases.

### OA-6A — uncertainty contract and registry

- add schema and canonical uncertainty objects for the existing planner assumptions;
- encode the three response profiles explicitly as `FINITE_SCENARIOS`;
- encode objective weight, user cost and intervention timing as decision assumptions, not scientific parameters;
- add validation that no probabilities are inferred for finite scenarios.

### OA-6B — robustness and regret engine

- pure deterministic functions over the existing planner bundle/profile table;
- compute rank range, threshold coverage, per-scenario regret and maximum regret;
- expose decision-switch conditions;
- no stochastic sampling and no pseudo-probabilities.

### OA-6C — Decision Under Uncertainty UI

Inside **Acționează / Priorități și plan**:

- “Ce este incert?” uncertainty ledger;
- scenario comparison matrix;
- robustness/regret panel;
- threshold control;
- explicit “why does the decision switch?” explanation;
- canonical links to Search/Inspector/Theory/Registry.

### OA-6D — information priority and adaptive reassessment

- identify decision-sensitive uncertainties;
- mark reducible vs not readily reducible;
- allow a user to record monitoring indicators and reassessment triggers;
- do not implement numeric EVPI/EVSI unless a later scientific contract adds valid probability distributions and utility functions.

### OA-6E — closure audit

- scientific-output invariant audit;
- accessibility/reflow/keyboard audit;
- bilingual semantic parity;
- no “probability”, “confidence interval”, “likelihood” or “expected value” language where prerequisites are absent;
- post-merge CI gate before OA-7.

## 8. UI language rules

Preferred:

- “declared scenarios”
- “robust across 3 of 3 declared profiles”
- “maximum regret within this scenario set”
- “decision changes under…”
- “uncertainty not quantified probabilistically”
- “user-declared objective weight”
- “illustrative response profile”
- “information priority”
- “reassessment trigger”

Prohibited unless mathematically justified:

- “95% confidence” for scenario ranges;
- “probability this is the best option” from rank frequency;
- “expected outcome” from unweighted profiles;
- “risk” when only a non-probabilistic scenario difference is represented;
- “EVPI/EVSI” without a probability model and utility/value function;
- “recommended policy” for the current illustrative CEM planner.

## 9. Accessibility and cognition requirements

- uncertainty cannot be conveyed by color alone;
- every uncertainty graphic requires a text/table equivalent;
- no animation is required to understand uncertainty;
- exact scenario labels and values remain visible to keyboard users;
- compact/mobile layouts must preserve one-dimensional reflow;
- graphs should show the denominator for finite-scenario summaries;
- point estimates must not visually dominate uncertainty ranges/scenario spread;
- scientific confidence, decision robustness and learner confidence must use distinct terminology and visual treatment.

## 10. Test contract

OA-6 implementation must include tests that:

1. reject expected-value calculations for scenarios with `NOT_AVAILABLE` probabilities;
2. preserve exact existing bundle scores and reference outputs;
3. compute zero regret for the best bundle in each scenario;
4. compute non-negative regret within numeric tolerance;
5. identify a decision switch when profile-specific top bundles differ;
6. preserve ties deterministically without representing tie-break order as evidence;
7. distinguish rank frequency from probability;
8. keep objective-weight changes separate from scientific uncertainty;
9. keep user cost assumptions separate from model parameter uncertainty;
10. keep uncertainty registry semantic IDs canonical and Inspector-searchable;
11. preserve keyboard operation and 320 CSS px / 200% text reflow;
12. preserve RO/EN semantic parity.

## 11. Exit gate for R7

R7 is complete when this document is integrated after CI and no executable OA-6 code has been introduced by the research PR.

The next implementation gate is **OA-6A — uncertainty contract and registry**.

## 12. Research sources

- Lempert RJ. Robust Decision Making. In: *Decision Making under Deep Uncertainty*. Springer, 2019. https://link.springer.com/chapter/10.1007/978-3-030-05252-2_2
- RAND. Robust Decision Making. https://www.rand.org/pubs/tools/TL320/tool/robust-decision-making.html
- Lempert RJ, Groves DG, Popper SW, Bankes SC. A General, Analytic Method for Generating Robust Strategies and Narrative Scenarios. *Management Science*. 2006. https://doi.org/10.1287/mnsc.1050.0472
- Marchau VAWJ et al., eds. *Decision Making under Deep Uncertainty: From Theory to Practice*. Springer, 2019. https://link.springer.com/book/10.1007/978-3-030-05252-2
- NICE. Health technology evaluations manual — Exploring uncertainty. https://www.nice.org.uk/consultations/2261/1/economic-evaluation
- NICE. Committee recommendations — decision uncertainty. https://www.nice.org.uk/consultations/2261/1/committee-recommendations
- NICE. Early-use HealthTech guidance assessments. https://www.nice.org.uk/process/pmg48/chapter/early-use-healthtech-guidance-assessments
- IPCC. AR6 WGI Chapter 1 — uncertainty and calibrated language. https://www.ipcc.ch/report/ar6/wg1/chapter/chapter-1/
- Kale A, Kay M, Hullman J. Visual Reasoning Strategies for Effect Size Judgments and Decisions. *IEEE TVCG*. 2021. https://idl.uw.edu/papers/effect-size-judgments
- Padilla LMK, Powell M, Kay M, Hullman J. Uncertain About Uncertainty. *Frontiers in Psychology*. 2021. https://pmc.ncbi.nlm.nih.gov/articles/PMC7868089/

## 13. Claim boundary

This research contract does not establish that any RDM, regret, scenario or uncertainty-visualization method will improve real CEM user decisions.

It establishes an architectural direction that is more compatible with the current epistemic state of CEM than assigning unjustified probabilities to uncalibrated profiles.

Human evaluation of comprehension and decision quality remains necessary before claiming decision-support effectiveness.
