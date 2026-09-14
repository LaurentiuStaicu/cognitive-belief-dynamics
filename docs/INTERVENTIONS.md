# Intervention planning in M0

The application supports understanding mechanisms and choosing measures together,
with explicit objectives, effort estimates and timing. It searches all feasible
subsets of four measures: repetition reduction, correct fact-check context,
accuracy cues and verified source feedback. Factor paths show their model dependencies.

## Objective and cumulative effect

Score = 100 × [w × (1 − mean false-sharing probability) +
(1 − w) × mean true-sharing probability]. The user chooses w and integer additive
effort costs/budget. Every probability is averaged over all 13 steps (0–12).
Summing over that same fixed horizon gives the same ranking. This is expected
sharing, not sampled actions, unique reach, population impact or monetary benefit.
Ties prefer lower effort, then a stable mask order. The empty bundle is always feasible.

All 16 bundles are evaluated for activation at step 2 or 5 and three parameter
profiles, giving 96 runs of paired synthetic claims. Python generates outcomes;
the browser recalculates rankings from those outcomes without duplicating M0 equations.
The best option is optimal only within this finite set and the chosen assumptions.
All selected measures share an activation time; arbitrary sequences and durations
are not optimized. The schedule explains subsequent source-feedback events.

## Mechanisms and interactions

Each claim starts with prior belief 0.5 and neutral source reliability. Exposures
occur at steps 1–4. Activated repetition reduction removes subsequent exposures
at steps 2–4 for both claims. Corrective context occurs once, with an accurate
negative direction for the false claim and positive direction for the true claim.
Accuracy cues apply from activation onward. Source feedback gives four correct
confirmations at activation and every two steps thereafter. Evidence is ±0.6,
reward context 0.5. Truth defines the synthetic environment; the agent receives
only its events/evidence, never a truth argument in belief evaluation.

Combined gain minus the sum of standalone gains measures nonadditivity of this
score in this simulation. Leave-one-out score loss ranks factor contributions
conditional on the inspected bundle. These losses need not sum to total gain and
are not universal factor weights or empirical causal estimates.

## Sensitivity and limits

The low/reference/high profiles scale beta_f, beta_correction and
beta_accuracy_cue together by 0.7/1.0/1.3. Other coefficients remain fixed.
The displayed range and top-choice count across profiles are limited sensitivity
checks, not confidence intervals, probabilities or broad robustness guarantees.
Effort is additive and user-estimated; favorable correct fact-checking and
informative-source assumptions are not guaranteed outside this simulation.

The existing seven-variable M0 does not execute all twenty conceptual modules.
Stress, sleep, institutions and algorithmic amplification require additional
mechanisms, evidence, calibration and validation before they can enter the ranking.
Real planning also requires a defined population, measurable outcomes, actual costs,
feasibility/dependencies, adverse effects and comparison against alternatives.

The design separates objectives, options and sensitivity following public guidance:
- https://analysisfunction.civilservice.gov.uk/policy-store/an-introductory-guide-to-mcda/
- https://analysisfunction.civilservice.gov.uk/policy-store/the-analysis-function-theory-of-change-toolkit/

This weighted prototype is not a complete validated MCDA or an empirical evaluation.
JSON export records settings, selected results and the full selected profile.

## Decision transparency (Alpha 0.3.3a0)

The inspector decomposes gain using mean probabilities: the false-sharing reduction
is 100 × (baseline false − bundle false), and true-sharing change is
100 × (bundle true − baseline true). These are probability percentage points.
Multiplying them by the respective fractional objective weights yields score-point
contributions whose sum is the original gain, before display rounding.

For every response profile, identical budget, availability, effort, timing and
objective settings define the feasible set. The audit reports its top choice and
score(best feasible) − score(inspected). Zero can denote a tie; sorting remains by
score, lower effort and mask order. The displayed alternative excludes the inspected
bundle; if it is the only feasible bundle no alternative is claimed.

Factor contributions distinguish standalone gain from loss when removed from the
inspected bundle. Removal loss is signed, conditional and not necessarily additive;
a negative value means removing that measure improves this objective. Exports include
all audit values. No change to simulation, ranking or uncertainty assumptions.

Methodological background: government MCDA guidance emphasizes explicit trade-offs
and sensitivity analysis, and distinguishes formal MCDA from simple weighted scoring.
Our tool is the latter, an exploratory demonstration, not a claim of MCDA compliance.
https://www.gov.uk/government/publications/green-book-supplementary-guidance-use-of-multi-criteria-decision-analysis/use-of-multi-criteria-decision-analysis-in-options-appraisal-of-economic-cases

## Selected schedule (Alpha 0.3.4a0)

bundle_schedule(mask, start) is the canonical 13-step schedule. The evaluator consumes
it and the exporter publishes 32 schedules (16 bundles × two activation times).
Response profiles share schedules; only coefficients differ.

At each step: exposure if scheduled, correction if selected, source feedback if
selected, then decision with the scheduled accuracy cue. Prevented exposure is
bookkeeping, not an executed event. Early repetition reduction prevents steps 2–4;
late activation at step 5 prevents none. Source feedback occurs at start + 0/2/4/6.
The UI shows only selected measures and exports the exact inspected schedule.

Steps remain abstract. This is a simulation calendar, not a population deployment
plan or an empirically justified intervention timetable. Tables use captions and
row/column headers: https://www.w3.org/WAI/tutorials/tables/two-headers/
