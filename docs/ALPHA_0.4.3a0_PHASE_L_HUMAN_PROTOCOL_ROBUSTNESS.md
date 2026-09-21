# Alpha 0.4.3a0 Phase L — Prospective Human-Protocol Robustness Contract

Status: **planning/research-only contract**. This phase does not authorize human recruitment, does not activate M1.E4, does not introduce `Pencode`, and does not select EVSD or 2HT as the human recognition architecture.

## 1. Purpose

Phase K established only a synthetic model-recovery result for the frozen participant-aware simulator. Under that simulator, the primary `P64_X10` surface passed the preregistered recovery convention. Phase K explicitly retained the following omitted factors:

- item random effects;
- fatigue;
- learning/practice;
- block/order effects and possible behavioral carryover;
- missingness/dropout;
- correlated participant memory/bias random effects.

Phase L answers the next question prospectively:

> Which omitted structures can materially change the ability of the planned human experiment and analysis to discriminate the frozen EVSD and 2HT candidate families, which can be controlled mainly by protocol design, and which require another synthetic robustness gate before recruitment could ever be considered?

Phase L freezes that decision before any additional stress simulation is executed.

## 2. Inherited scientific boundary

Phase L inherits without modification:

- active software/model metadata: Alpha `0.4.3a0`, active specification `M1`, baseline `M0`;
- evidence snapshot: `EVIDENCE.M1.2026-09-16.r1`;
- active executable mechanisms: M1.E1, M1.E2 and M1.E3 only;
- planned M1.E4 empirical construct: recognition sensitivity `Drecog`;
- raw recognition cells: `Nhit`, `Nmiss`, `Nfa`, `Ncr`;
- measurement separation `Drecog != Crecog`;
- candidate families: `CANDIDATE.M1.E4.C1.EVSD` and `CANDIDATE.M1.E4.C2.2HT`;
- `Pencode.status = NOT_IDENTIFIED_BY_CURRENT_MEASUREMENT`;
- raw-response likelihood as the primary future fitting surface;
- participant-aware Phase K analysis with marginal AIC plus held-out predictive log likelihood and a decisive family label only when both diagnostics agree.

Nothing in Phase L is evidence that either candidate is true in humans.

## 3. Source-task constraint

The primary empirical anchor remains Shulman, Markowitz & Rogers (2024), Study 3.

The source design used:

- a general-public sample;
- 10 headline-selection exposures;
- simple versus complex headline conditions;
- a later 24-item yes/no signal-detection recognition task;
- participant-level recognition sensitivity as the reported mechanism outcome.

The source condition is between participants. Therefore a classic treatment carryover from `Hsimp=simple` to `Hsimp=complex` is **not** an inherent requirement of the source design.

However, the planned model-discrimination experiment requires more information than one yes/no operating point. If future criterion/bias manipulations are implemented within participant, period/order and behavioral carryover become design variables that must be counterbalanced and stress-tested. If bias settings are implemented between participants, this carryover pathway is avoided at the cost of a larger participant allocation problem.

Phase L does not choose the final bias-manipulation implementation. It requires that the choice be frozen before the next authoritative simulation.

## 4. Why item effects are a mandatory robustness axis

The Phase K simulator varies participants but does not include stimulus-item heterogeneity.

Psychological experiments with repeated responses to multiple stimuli are cross-classified by participants and items. Mixed-effects methodology shows that ignoring item variability or using an under-specified random-effects structure can impair generalization and distort uncertainty for fixed effects.

Therefore item effects are **not optional** for the next synthetic gate.

The next simulator must support, at minimum:

- item-specific baseline recognition difficulty / lure confusability;
- item-to-item variation in the condition-sensitive memory signal when justified by the design;
- crossed participant × item response generation rather than treating all probes as exchangeable copies of one average item.

The next analysis comparison must state its intended generalization target explicitly:

1. new participants with the registered stimulus set; and
2. if claims are intended to generalize beyond the exact registered headlines/probes, new participants **and new items**.

A participant-only held-out cohort is insufficient to establish generalization beyond a fixed item set.

## 5. Correlated participant random effects are a mandatory robustness axis

Phase K includes participant memory and response-bias random effects but treats the omitted correlation between them as a boundary.

That independence assumption is not empirically established.

Phase L therefore requires the next synthetic gate to include:

- the current zero-correlation case as the reference;
- at least one non-zero positive memory/bias correlation stress regime;
- at least one non-zero negative memory/bias correlation stress regime.

Numeric magnitudes must be frozen before execution and labeled by provenance status. If no empirical estimate exists, the values must be described as **demonstrative stress values**, not population estimates.

The next gate must report whether candidate-family recovery is stable to this dependence assumption and whether parameter-recovery degradation is concentrated in either family.

## 6. Fatigue, practice and serial position

Repeated cognitive tasks can show practice/retest effects, and within-session performance can change with trial position through learning, adaptation or fatigue.

For the planned recognition experiment these effects must not be collapsed into one unobserved psychological mechanism. Phase L treats them as nuisance structures that can mimic or mask condition differences if stimulus assignment or probe type is systematically aligned with serial position.

The human protocol must therefore predeclare:

- randomization or counterbalancing of item/probe order;
- whether target and foil probes are interleaved;
- whether simple/complex stimulus properties can become correlated with serial position;
- planned breaks, if any;
- whether trial position/block is retained in the analysis dataset.

The next synthetic gate must include at least one bounded serial-position degradation scenario. Separate fatigue and practice parameters are required only if the final protocol gives them distinguishable temporal signatures. Otherwise a transparent monotonic or blockwise nuisance trend is sufficient for robustness testing and must not be interpreted as a fitted human cognitive law.

## 7. Order and behavioral carryover for bias manipulation

Phase C established that multiple operating points or a response-bias manipulation are required to discriminate the candidate families.

If multiple bias/criterion settings are administered within participant, the protocol must predeclare:

- block sequence generation;
- counterbalancing/randomization;
- whether the same item can recur across settings;
- any washout or separation logic that is psychologically meaningful;
- the analysis term used for period/order;
- what evidence would be treated as unacceptable carryover.

Because behavioral carryover cannot be assumed away after observing the data, the final design should prevent or orthogonalize it where possible rather than depend on a post-hoc carryover test.

If the final design assigns one bias setting per participant, this specific carryover gate can be removed prospectively, but the resulting larger participant-allocation surface must be re-evaluated in simulation.

## 8. Missingness and dropout

Phase L separates three different events:

1. participant recruitment/eligibility failure;
2. participant dropout or non-completion;
3. trial/probe-level missing response among otherwise retained participants.

They may not be collapsed into one complete-case filter.

The human protocol must prospectively define:

- which participants enter the analysis population;
- all exclusion rules;
- how incomplete target/foil counts are represented;
- whether the primary likelihood can use unequal observed trial counts;
- what auxiliary variables relevant to missingness will be retained;
- sensitivity analyses for departures from an ignorable missingness assumption.

The next synthetic gate must include:

- an ignorable/approximately MAR-like missingness regime;
- at least one outcome- or latent-state-associated adverse sensitivity regime representing informative missingness.

No single-imputation shortcut may be the primary strategy merely to restore balanced cells.

No numeric dropout or missing-response rate is treated as empirically calibrated unless supported by an appropriate source or pilot dataset.

## 9. Exclusions and data-quality rules

All exclusion and data-quality rules must be frozen before outcome inspection.

They may use protocol-level variables such as:

- consent/eligibility;
- duplicate participation;
- impossible or technically invalid response records;
- predeclared attention/data-quality checks;
- minimum usable target/foil observations needed for the chosen likelihood.

They may **not** depend on:

- which candidate family fits a participant better;
- whether the participant supports the expected Hsimp direction;
- whether excluding the participant increases family-recovery or statistical significance;
- post-hoc thresholds chosen after viewing condition outcomes.

Excluded, missing and analyzed observations must remain separately auditable.

## 10. Recruitment and stopping rule

Recruitment must remain unauthorized throughout Phase L.

Before any future recruitment authorization, the protocol must freeze either:

- a fixed participant and item allocation justified by the final simulation-based design analysis; or
- a formally specified sequential design whose stopping rule and operating characteristics have themselves been prospectively simulated.

Unregistered outcome-dependent peeking and stopping is forbidden.

The final sample-size argument must account for both participant and stimulus variability where the scientific claim intends to generalize over both.

The existing `P64_X10` result is therefore a synthetic allocation result for the current simulator, **not** a human sample-size authorization.

## 11. Primary estimand and analysis topology

The future human protocol must distinguish three levels:

### Measurement level

Raw target/foil responses and the derived `Drecog` / `Crecog` summaries.

### Candidate-model level

EVSD and symmetric 2HT fitted to the same raw-response surface with parameter-count fairness.

### Model-discrimination level

The predeclared combination of:

- marginal fit criterion on training data;
- predictive fit on held-out participants;
- item-generalization diagnostic when claims extend beyond the exact stimulus set;
- separate wrong-family and inconclusive outcomes.

No p-value, AIC difference or predictive score alone constitutes proof of a cognitive architecture.

The train/validation partition rule must be frozen before data collection. Data from one participant may not leak across participant-held-out evaluation. If item-held-out prediction is claimed, the relevant items may not leak across that evaluation boundary either.

## 12. Required Phase M synthetic robustness gate

Phase L concludes that **another prospective synthetic gate is justified before any recruitment authorization**.

The reason is not that Phase K failed. Phase K passed its own frozen question. The reason is that two omitted structures — crossed item variability and participant memory/bias dependence — directly affect the generalization and identifiability problem and cannot be eliminated solely by interface or protocol wording. Serial-position and missingness assumptions can also materially alter the raw-response surface.

Phase M must therefore stress the frozen candidate-discrimination pipeline across at least these axes:

- item heterogeneity;
- participant memory/bias correlation;
- serial-position nuisance;
- missingness mechanism;
- the final chosen bias-setting allocation/order design.

It must preserve the Phase J/K distinction between:

- correct-family recovery;
- wrong-family selection;
- inconclusive selection;
- parameter-recovery error.

The inherited formal recovery convention remains:

`recovery_probability >= 0.80`

for every prospectively designated primary robustness cell.

Wilson lower-bound results remain a separately reported Monte Carlo precision sensitivity and may not silently replace the formal rule.

Phase M must define its complete stress surface, parameter provenance and Monte Carlo replication count **before** the authoritative run.

## 13. ADEMP-style simulation specification requirement

Before Phase M execution, its contract must explicitly register:

- **Aim** — what robustness question is being tested;
- **Data-generating mechanisms** — including every nuisance axis and its provenance status;
- **Estimands/targets** — family recovery, wrong-family rate, inconclusive rate and parameter-recovery diagnostics;
- **Methods** — identical candidate fitting/selection logic across generators;
- **Performance measures** — including Monte Carlo uncertainty.

The number of simulation replicates must be justified by desired Monte Carlo precision rather than inherited mechanically from Phase J.

## 14. M1 completion decision after Phase M

A successful Phase M would establish only this narrower statement:

> The planned EVSD-vs-2HT discrimination procedure remains recoverable across the prospectively frozen synthetic participant/item/protocol nuisance regimes tested.

It still would not establish:

- that EVSD is the true human model;
- that 2HT is the true human model;
- that the real human process lies within either candidate family;
- that `Pencode` is identified;
- that a human effect has been calibrated for a target population.

After Phase M, CEM must make a separate explicit decision between:

1. **close M1 at the scientifically justified pre-human boundary** and proceed to application simplification/Simple Mode while retaining the human study as future validation work; or
2. prepare a preregistered human protocol for external execution, without presenting recruitment or resulting data collection as necessary for the software architecture itself.

No indefinite sequence of M1 extensions is permitted merely because additional cognitive mechanisms can be imagined.

## 15. Phase L exit gate

Phase L may merge only if:

- this contract remains planning/research-only;
- item effects are classified as a mandatory Phase M axis;
- correlated participant memory/bias effects are classified as a mandatory Phase M axis;
- serial-position/fatigue/practice are represented as protocol-controlled nuisance structure with at least one Phase M stress scenario;
- carryover requirements depend prospectively on the selected bias-manipulation design rather than being copied mechanically from crossover trials;
- missingness/dropout and exclusions are prospectively separated;
- the recruitment/stopping rule remains blocked until Phase M and protocol freeze;
- Phase M is explicitly required before any recruitment authorization;
- `Pencode` remains absent;
- EVSD and 2HT remain candidate families with no winner declaration;
- no active variable, link, empirical target, validation registry, runtime model or UI changes;
- software version remains `0.4.3a0`;
- evidence snapshot remains `EVIDENCE.M1.2026-09-16.r1`;
- retained M0/M1.E1/M1.E2/M1.E3 outputs remain unchanged;
- full repository CI passes.

## 16. Forbidden changes in Phase L

No:

- human recruitment or recruitment authorization;
- IRB/ethics approval claim;
- active M1.E4 runtime;
- `Pencode` equation or proxy;
- EVSD/2HT winner declaration;
- fitted human coefficient;
- population calibration;
- new user-facing M1.E4 UI;
- change to M0/M1.E1/M1.E2/M1.E3 scientific outputs;
- change to release version or evidence snapshot.

## 17. Methodological anchors

Primary empirical task:

- Shulman HC, Markowitz DM, Rogers T. *Reading dies in complexity: Online news consumers prefer simple writing.* Science Advances. 2024;10(23):eadn2555. doi:10.1126/sciadv.adn2555.

Crossed participant/item effects and confirmatory mixed models:

- Barr DJ, Levy R, Scheepers C, Tily HJ. *Random effects structure for confirmatory hypothesis testing: Keep it maximal.* Journal of Memory and Language. 2013;68(3):255–278. doi:10.1016/j.jml.2012.11.001.

Simulation-based mixed-model design/power:

- Kumle L, Võ ML-H, Draschkow D. *Estimating power in (generalized) linear mixed models: An open introduction and tutorial in R.* Behavior Research Methods. 2021;53:2528–2543. doi:10.3758/s13428-021-01546-0.

Practice/retest effects:

- Calamia M, Markon K, Tranel D. *Scoring higher the second time around: meta-analyses of practice effects in neuropsychological assessment.* The Clinical Neuropsychologist. 2012;26(4):543–570. doi:10.1080/13854046.2012.680913.

Order/carryover design principles:

- Dwan K et al. *CONSORT 2010 statement: extension to randomised crossover trials.* BMJ. 2019;366:l4378. doi:10.1136/bmj.l4378. These principles are used only where the future CEM bias-manipulation design actually creates repeated treatment/criterion periods.

Missing-data planning and sensitivity:

- National Research Council. *The Prevention and Treatment of Missing Data in Clinical Trials.* National Academies Press, 2010. The general design principle retained here is to prevent missingness where possible, predeclare assumptions and report sensitivity to unverifiable missing-data mechanisms; CEM is not classified as a clinical trial by citing this source.

Prospective simulation design/reporting:

- ADEMP-style planning as adapted for simulation studies in psychology: aims, data-generating mechanism, estimands/targets, methods and performance measures, with explicit Monte Carlo uncertainty and reproducibility.

Phase L ends with a frozen robustness decision and a required Phase M synthetic gate. It does not end with a human cognitive-model selection.
