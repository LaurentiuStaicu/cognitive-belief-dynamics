# OA-5 closure audit — Active Understanding

Status: **CLOSURE CANDIDATE — requires OA-5D PR CI and post-merge CI**

Baseline audited: `f32bd39e3f8bcfbebaddb0c7cad89369c46dd998` (OA-5C merged in main; post-merge CI #221 successful).

## Scope

This audit closes the OA-5 foundation defined by the optimization plan and R6. It audits learning interaction and integration only. It does not claim that CEM improves learning, retention, transfer or metacognitive calibration; R6 explicitly requires human evaluation before any such effectiveness claim.

## Slice coverage

- OA-5 R6: ADOPT WITH LIMITS research contract.
- OA-5A: schema-validated AU-1/AU-2/AU-3 challenge contract, state machine and bounded local history.
- OA-5B: explicit Active Understanding UI with Worked example -> Predict -> Reveal -> Explain -> Epistemic boundary -> Complete.
- OA-5C: Challenge Model over the already-registered M1.E3 NULL versus headline-negativity alternatives.
- OA-5D: cross-link integration, focus behavior and closure regression.

## Required concept families

AU-1 passes the closure candidate gate: exposure remains distinct from familiarity; the canonical Repetition fixture retains F: 0.0 -> 0.35 after the first exposure; familiarity is explicitly not truth or evidence strength.

AU-2 passes the closure candidate gate: Accuracy cue -> W remains the direct computational target; belief B and Share remain distinct from the accuracy-salience pathway.

AU-3 passes the closure candidate gate: `COMPDEP.EXPOSURE.FAMILIARITY` remains a `COMPUTATIONAL_DEPENDENCY`; `LINK.EXPOSURE.FAMILIARITY` remains a separate `REGISTERED_EVIDENCE_RELATION`. Executability is not presented as population causal validation.

## Learning-state and privacy boundaries

Prediction is optional and cannot mutate the canonical result. Learner confidence remains low/medium/high and is explicitly separate from scientific confidence. History remains local-only, schema-versioned, bounded to 100 records, fail-closed on corrupt/future data, user-clearable and outside Workspace/Case provenance.

## Challenge Model boundary

The Challenge Model consumes only the existing M1.E3 NULL and headline-negativity alternatives. It reuses canonical Paccess values, held-fixed context, experiment purpose, calibration status, empirical target and validation IDs. It introduces no new scientific comparator and no winner claim.

## Theory / Search / Inspector integration

For every AU foundation challenge, Theory resolves from the existing THEORY worked-example anchor, Search receives an exact canonical semantic entity ID, and Universal Inspector receives the canonical relation ID when available.

The M1.E3 Challenge Model links to the existing algorithms/social-feedback Theory chapter, `VAR.HEADLINE.NEGATIVITY` in Search and `VAR.ACCESS.PROBABILITY` in Universal Inspector.

Search and Inspector remount independently, preserving the current Active Understanding session stage.

## Scoped usability and accessibility audit

The OA-5 surface uses native buttons, radio controls, select controls, fieldset/legend, progress and ordinary semantic headings. There is no timed response, drag-only task, custom combobox, modal Inspector or color-only correctness encoding.

Explicit cross-link actions move focus to a stable destination only after activation. The Theory article is programmatically focusable for direct chapter navigation. Global Search remains a search landmark and Universal Inspector remains a top-level complementary `aside`.

Browser regression covers explicit focus destinations, mobile horizontal reflow, 200% text reflow and RO/EN behavior. OA-5D does **not** claim manual screen-reader certification; the broader screen-reader/manual keyboard audit remains OA-8 Trust Hardening.

External accessibility basis:

- https://www.w3.org/WAI/fundamentals/accessibility-principles/
- https://www.w3.org/WAI/ARIA/apg/practices/landmark-regions/
- https://www.w3.org/WAI/content-assets/wai-aria-practices/patterns/landmarks/examples/search.html
- https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/

## Scientific-output invariant

OA-5D is UI/test/documentation integration only. It must not modify files under `model/`, scientific schemas, reference runs, evidence snapshot, equations, coefficients or release metadata.

## Closure gate

OA-5 may be declared closed only if dedicated OA-5D unit tests, full Python/reference reproduction, TypeScript/Vite, Playwright, scientific-output diff audit, PR CI and post-merge CI all pass.

Only after those conditions are satisfied may R7 / OA-6 Decision Under Uncertainty begin.
