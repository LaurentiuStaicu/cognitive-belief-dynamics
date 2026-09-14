# Comparing saved reference scenarios

The Comparisons view supports the understanding priority by putting each saved
scenario alongside the repetition-only reference. It reads existing runs.json;
no new model equations, parameters or stochastic samples are introduced.

Two plots use the same 0–1 vertical scale and full step 0–12 horizontal range.
Reference is dashed and selected scenario solid. Exact values and differences are
available at a shared selected step and in a 13-row table. Mean differences cover
all 13 steps, including pre-intervention steps. First divergence uses a 1e-12
numeric tolerance, not displayed three-decimal rounding. Selection can open the
same scenario/step in the detailed explanation view. JSON export preserves both
source runs, contextual contrast, selected step, pointwise differences and means.

Every contrast has the same initial agent state, four exposures at steps 1–4,
coefficients and reward context. The input differences are:
- Repetition vs itself: zero differences; overlapping curves are expected.
- Correction: one negative correction at step 5, then accessibility decay.
- Accuracy: cue from step 5; B remains unchanged while W and P can change.
- Source: negative feedback at 2/4/6/8 AND evidence +0.6 instead of 0. This is a
  joint-input contrast and cannot be called the isolated effect of feedback.

Differences are scenario-model outcomes, not estimated empirical effects, observed
population counts or calibrated causal effects. Lower belief/sharing is not
universally better. Unlike the intervention lab, these scenarios do not pair a
false and true claim for a decision objective. Use the lab to compare bundles,
objectives, effort and limited sensitivity; do not rank real interventions from
these curves alone.

Design reference consulted 2026-09-14:
https://analysisfunction.civilservice.gov.uk/policy-store/charts-a-checklist/
Use comparable scales, readable labels and text/data alternatives. The browser
checks verify all four numeric contrasts, the joint-input limitation, download,
scenario/step handoff, mobile/200% text reflow and light/dark appearance.
