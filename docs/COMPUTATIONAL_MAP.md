# Computational map of M0

The Understanding priority requires seeing how calculations connect, including
relationships that do not yet have an evidence-registry assessment. The map offers:
- Core: seven registered variables plus the intermediate probability output P,
  connected by seven paths.
- Context: 18 nodes and 17 dependencies including prior, evidence, correction
  direction, cue, baseline accuracy, reward/bias, feedback, correction event,
  elapsed time and random draw.
- Registry: the original seven-variable, three-link evidence view.
- Mechanism focus: repetition, correction, source/evidence or decision.

Nodes and edges can be inspected with keyboard selectors as well as graph clicks.
Connected edges highlight when a node is selected. Core nodes are circles,
probability is rectangular and input nodes are rounded rectangles. Solid edges
have a registry correspondence; dashed edges are documented from code only.
Solid does not mean an empirically validated causal relation. The registered
W → Share path is mediated by P in the computational map, with that distinction
explicit in its description. Reference formulas and calibrated effects remain distinct.

Source-of-truth review: model.py, updates.py and simulation.py, 2026-09-13.
The explanatory dependency metadata is now canonical data in
model/computational_dependencies.json. web/src/dependencies.ts only adapts that
generated/public data for the interface; it is not a second scientific source.
Do not change equations or coefficients by editing the dependency registry. Internal latent logits,
parameter nodes and state-update self-loops are not drawn separately; reward/bias
are grouped in one input node and coefficient roles appear in edge details.
Nexp describes event counts, not a stored Simulator counter used by an equation.

Key boundaries visible in the map:
- Ground truth is not a direct belief input.
- Computed B does not automatically replace the fixed prior.
- Correction direction is separate from accessibility C.
- T below 0.5 reverses evidence sign by model choice.
- W affects belief and reward weights; it does not universally suppress sharing.
- Random sampling affects Share, not P or B.
- M0 does not generate future exposures from sharing; no contagion/network feedback
  loop is implied. Familiarity/source estimates have no time decay in current M0.

Validation: TypeScript build and browser regression cover core/context/registry
switching, mechanism filtering, accessible edge explanations, existing numeric
scenario outputs, themes and responsive layout. Model outputs are unchanged.
Future equation changes must also review these explanatory dependencies.
