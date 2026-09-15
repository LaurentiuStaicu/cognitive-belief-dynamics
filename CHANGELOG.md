# Changelog

## Alpha 0.3.5a0 — Consistent interface wording

- Shared label module: one canonical name per scenario across every view.
- Guided tours named distinctly from reference scenarios.
- Untranslated English words removed from Romanian labels (MOD.12, MOD.13).
- Romanian spelling and agreement fixes; unified English terminology and spelling.
- Accessible language-switch label, non-Roman-numeral pause control, bilingual page metadata.
- Presentation only: equations, coefficients and exported trajectories unchanged.

## Alpha 0.3.4a0 — Selected intervention schedule

- Canonical Python schedule shared by the evaluator and exported calendar.
- Selected measures, effective times and event-order ledger in RO/EN.
- Explicit no-action case for late repetition reduction and empty bundles.
- Calendar included in plan export; equations and numerical outcomes preserved.

## Alpha 0.3.3a0 — Explain intervention priorities

- Objective gain decomposition, inspected rank and feasible-alternative gap.
- Per-profile top choices and gaps using the same decision constraints.
- Signed standalone and conditional removal gains for selected factors.
- Decision audit included in JSON exports; numerical model unchanged.

## Alpha 0.3.2a0 — Explanations along the graph

- Explain eight core factors using canonical step values and exported score terms.
- Add source/evidence tour, previous-factor navigation and manual-selection cancellation.
- Keep explanations synchronized when changing the timeline.
- Equations and numerical trajectories unchanged.

## Alpha 0.3.1a0 — M0 Visual Stage

- Functional bands, selection focus and navigable upstream/downstream dependencies.
- Context-sensitive edge markers and manual guided tours for repetition, correction and sharing.
- Graph snapshots use logged exposure counts and actual sampled actions; open the same scenario step for full explanations.
- Adapted the supplied React proposal to the existing TypeScript/Cytoscape architecture.
- M0 equations and reference trajectories unchanged; see docs/INTEGRATION_ALPHA_0.3.1a0.md.

## 0.3.0a0 — 2026-09-14

First GitHub pre-release. Adds the mechanism learning view, computational map,
evidence-registry explanations, intervention bundle planning, per-step score
explanations and paired scenario comparisons. Adopts system typography and
light/dark themes in preparation for elementary OS. Adds visible versioning,
consistent export metadata, release notes, licenses and verified web release assets.
M0 equations, coefficients and numerical trajectories are unchanged.

## 0.2.0a0 — initial development stage

Python M0 reference simulator and initial web explorer. Work was published as
commits and GitHub Pages deployments, without a separate GitHub Release.
