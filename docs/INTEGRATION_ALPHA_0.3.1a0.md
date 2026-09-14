# Alpha 0.3.1a0 integration review

The user supplied ARCHITECTURAL_RATIONALE_ALPHA_0.3.1a0(1).md and
TRANSITION_REPORT_ALPHA_0.3.1a0(1).md, attributed to Gemini/Antigravity.
Their reported Vite/TypeScript success concerns their environment; the supplied
React component was not compiled unchanged in this repository.

## Architecture decision

Keep the existing vanilla TypeScript, Cytoscape, canonical Python-generated JSON,
bilingual inspector and evidence registry. The proposal imports absent graphData,
modelData, React, Tailwind and Lucide dependencies. Port its useful behaviours in
web/src/visual-stage.ts rather than maintaining two competing implementations.
No scientific equations or intervention rankings are changed.

## Adopted and corrected

- Optional four functional bands; explicitly computational organization, not proven
  neurocognitive stages. Theme tokens and system fonts follow the existing elementary
  visual foundation: https://docs.elementary.io/hig/reference/text .
- Optional neighbourhood dimming, visible upstream/downstream navigation and formulas.
  Graph styling uses the existing renderer: https://js.cytoscape.org/ .
- Edge markers distinguish reference-direction effects, contextual interactions and
  sampling. C→B depends on correction direction; T→B depends on evidence; W→P depends
  on belief and reward. These are not unconditional negative or positive effects.
- Manual guided routes replace decorative automatic impulse animation. They select
  a saved scenario and step, never pretend to inject an event. No autoplay or motion
  is introduced, including when reduced motion is requested.
- Snapshot values use canonical logs. Nexp counts ExposureEvent entries cumulatively,
  not frame.time. Share reads the boolean RNG outcome, never a probability threshold.
  Missing contextual input values are not invented. Frame values are post-step
  snapshots, not intermediate states between arrows in a tour.
- Internal registry correspondence is not preregistration or proof of the mechanism.
  Existing evidence assessments, source links and calibration boundaries are retained.
- Keyboard selectors and buttons supplement the canvas, with responsive controls,
  light/dark support and no scientific meaning dependent on colour alone.

## Version and verification

Python/public version: 0.3.1a0; npm SemVer equivalent: 0.3.1-alpha.0.
Regenerate exports; run Python tests, TypeScript/Vite and browser smoke checks.
Browser coverage checks exposure counts and sampled outcomes at steps 0, 4, 5 and
12 for every reference run, bands, guided navigation and scenario-step handoff,
plus existing mechanism, comparison, planning, mobile and theme checks.
Existing CI gates deployment and release assets on the exact verified commit.
