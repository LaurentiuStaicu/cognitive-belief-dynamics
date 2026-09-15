# Alpha 0.4.1a1 — Phase D Guided Tour

## Purpose

Phase D adds a guided path through the existing Cognitive Epistemic Model surfaces. It is not a parallel tutorial simulation and does not introduce new scientific claims, coefficients or mechanisms.

The tour has one purpose: help a new reader connect theory, executable mechanism, state/equation, scenario, evidence, validation and planning without losing the epistemic status of each layer.

## Interaction model

The tour is implemented as ordinary in-page navigation rather than as a modal overlay or a sequence of interactive tooltips.

Each step has:

- a stable deep-link under `#understanding/tour/<slug>`;
- one explanatory purpose;
- two concrete observations to make;
- one checkpoint question;
- one explicit epistemic boundary;
- one action opening the real Theory, Mechanisms, Scenarios, Registry, Visual ODD or Planning surface.

Browser Back returns to the exact tour step after opening another application view.

This structure follows the general accessibility principle that dynamic controls need explicit roles, states and keyboard-operable behavior, while avoiding focusable content inside tooltip-style popups. The journey is also deliberately sequential: it has a defined beginning, end and useful order rather than presenting an unordered collection of hints.

Background design guidance:

- W3C WAI-ARIA / APG: https://www.w3.org/WAI/ARIA/apg/
- W3C tooltip pattern and its focus limitation: https://www.w3.org/WAI/ARIA/apg/patterns/tooltip/
- GOV.UK step-by-step navigation pattern: https://design-system.service.gov.uk/patterns/step-by-step-navigation/

## Ten-step journey

1. **Orientation** — what CEM asks and what it does not estimate.
2. **Causal chain** — world → available information → selection/presentation → observation → representation → judgment → action.
3. **Executable mechanism** — repetition as the first complete worked example.
4. **State and equation** — connect F, Nexp and B to the theory, Registry and code.
5. **Scenario** — inspect the reference trajectory rather than only an endpoint.
6. **Information environment** — distinguish editorial selection from presentation framing.
7. **Evidence** — separate model evidence, background theory and functional-form assumptions.
8. **Validation** — ask which differential result would reject or simplify a mechanism.
9. **Planning** — compare intervention bundles only after understanding mechanisms and assumptions.
10. **Synthesis** — trace an interface result back through variable, equation, source and limitation.

## Scientific boundary

The tour may summarize claims already present in the audited Theory corpus, but it must not strengthen them. In particular, it must not:

- turn demonstrative coefficients into effect-size estimates;
- turn conceptual modules into executable mechanisms;
- infer population prevalence from synthetic agents;
- equate exposure with belief;
- equate sharing with belief;
- treat planning ranks as real-world policy recommendations;
- imply that software test success validates the psychological theory.

## Accessibility and regression requirements

The merge gate requires:

- all ten steps keyboard-operable;
- `aria-current="step"` on the active step;
- semantic `progress` state;
- no modal focus trap;
- Romanian and English renderings;
- stable deep links;
- browser-history return from internal Understanding routes and external application views;
- no horizontal overflow on mobile;
- screenshots for both languages in CI;
- no regression to the Phase B placeholder.

## Completion condition

Phase D is complete only when the final PR CI is green, the bilingual screenshots are reviewed, browser-history behavior is verified, and the merged `main` workflow is green.
