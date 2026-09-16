# ADR 0013 — OA-6C Decision Under Uncertainty UI

Status: Proposed for OA-6C integration.

## Context

OA-6A established a typed uncertainty registry with a fail-closed probability boundary. OA-6B added deterministic scenario robustness, regret, rank-range and decision-switch calculations over the existing planner table.

R7 next requires those objects to become visible inside **Act / Priorities & Plan** without changing the scientific model or presenting finite sensitivity scenarios as probabilities.

## Decision

OA-6C adds a Decision Under Uncertainty section to the existing intervention planner.

The section exposes four questions:

1. **What is uncertain?**
   - the five OA-6A registry entries;
   - scientific uncertainty versus decision assumption;
   - uncertainty type, quantification status, probability status, reducibility and limitations.

2. **What changes across declared scenarios?**
   - the existing low/reference/high profiles in a text/table matrix;
   - the top feasible bundle in each profile;
   - selected-bundle rank, gain and regret in each profile.

3. **How robust is the currently selected top bundle?**
   - top-rank scenario count / denominator;
   - user-declared gain-threshold coverage / denominator;
   - rank range;
   - maximum regret.

4. **Why does the decision switch?**
   - explicit scenario conditions whose complete top set differs from the selected reference profile;
   - no probability-of-switch language.

The acceptability threshold is a user preference. It does not alter any model score.

## Canonical navigation

OA-6C links to existing Theory and Semantic Spine objects for context:

- Theory chapter 12 — interventions;
- `VAR.FAMILIARITY.CLAIM`;
- `VAR.CORRECTION.ACCESS`;
- `VAR.ACCURACY.SALIENCE`;
- `VAR.ACTION.SHARE`.

These are navigation/context links only. OA-6C does not register a new causal or evidence relation between an uncertainty object and those entities.

Search and Inspector actions remount only their own global surfaces, preserving the current planner state. The Registry action opens the already-registered Share entity.

## Probability boundary

The UI states explicitly that:

- low/reference/high are declared finite sensitivity scenarios;
- `probability_status = NOT_AVAILABLE`;
- `3 / 3` is scenario coverage, not a probability;
- regret and rank range are not confidence intervals;
- the planner remains illustrative and uncalibrated.

No expected value, likelihood, probability-of-best, EVPI or EVSI is introduced.

## Export

The existing plan export gains a `decision_uncertainty` section containing:

- OA-6A registry ID;
- user-declared gain threshold;
- the deterministic OA-6B audit.

Existing score decomposition, schedule and model outputs are unchanged.

## Accessibility and reflow

The section uses ordinary details/summary, labels, number input, tables and buttons.

Exact numeric values are available in tables; no uncertainty distinction depends on color alone. Existing mobile overflow regression covers the planning view at compact width, and OA-6C adds browser assertions for the uncertainty surface and its global Search/Inspector focus behavior.

## Scientific-output boundary

OA-6C changes no file under `model/`, no intervention artifact, equation, coefficient, score formula, bundle, reference run, evidence status, semantic identity/status or release metadata.

The copied `decision_uncertainty.json` web asset is generated at build time from the already-canonical OA-6A contract.

## Next slice

After OA-6C integration and green post-merge CI, OA-6D may add information-priority and adaptive reassessment/trigger recording. Numeric VOI remains prohibited without a later probability-and-utility contract.
