# Step explanations

Priority 1: connect visible trajectories to their generating mechanisms.
For each of the four reference scenarios, explanations.json stores all 13 frames:
- Prior, familiarity, source-weighted evidence and corrective-context contributions
  to belief log-odds, plus the actual simulator latent score.
- Bias, W-weighted belief and reward contributions to the sharing latent score.
- Contextual inputs and differences from the previous frame.

The read-only Python helper explanations.py decomposes reference logs. It does not
change model.py, updates.py or simulation.py and does not generate another action
sample. Tests reconstruct both simulator probabilities from the exported terms
and verify correction direction, source feedback and cue/conviction separation.
The original runs.json remains byte-identical. Existing saved model outputs and
intervention rankings are unchanged.

The browser displays signed values and horizontal bars around a centered zero,
with one fixed scale across both score panels and all steps of the scenario.
They are latent-score terms, not percentages, probability-point effects, causal
attributions or recommended intervention priorities. Nonlinear transformation and
interactions prevent reading intervention effects directly from these bars.

Narrative explanations are specific to these four reference scenarios and their
fixed inputs. They must be reviewed before arbitrary scenario editing is added.
Prior, baseline accuracy and sharing bias are those of the reference agent;
this helper is not a general-purpose log attribution API for arbitrary agents.
The first step has no previous-step comparison. Random Share can differ even
when its deterministic probability remains unchanged.

The scenario download includes the explanation alongside the original data.
Previous/next and timeline controls work with keyboard; pointing at a rendered
part of the line chart displays the nearest shown step's exact values without
changing the selected step. The readout reverts on pointer exit. The timeline
remains the way to select an unshown future step.

Design guidance: https://analysisfunction.civilservice.gov.uk/policy-store/charts-a-checklist/
Consulted 2026-09-14 for legible annotations, accessible text/data alternatives,
and consistent scales. This is model output, not a population statistical chart.

Validation: 30 Python tests, TypeScript/build and browser regression of all four
scenarios, signed terms, previous-step control, downloads, RO/EN, graph/registry,
light/dark styles, mobile and 200% text reflow. Empirical validation is separate.
