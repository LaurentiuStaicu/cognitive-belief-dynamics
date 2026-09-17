# ADR 0028 — WCAG 2.2 AA audit baseline

Status: ADOPT_WITH_LIMITS
Date: 2026-09-17
Track: OA-8 — Trust Hardening

## Context

The optimization architecture requires a WCAG 2.2 AA audit plus separate screen-reader and manual-keyboard release gates. The web application already contains several accessibility-oriented invariants (responsive reflow, 200% text checks, visible focus treatment, semantic controls and a 44 CSS px target token), but those checks are distributed across feature smoke tests and do not constitute an explicit WCAG audit boundary.

WCAG 2.2 is a W3C Recommendation. Level AA includes all Level A and AA success criteria. Relevant new WCAG 2.2 AA criteria for CEM include 2.4.11 Focus Not Obscured (Minimum), 2.5.7 Dragging Movements and 2.5.8 Target Size (Minimum).

Authoritative references:

- https://www.w3.org/TR/WCAG22/
- https://www.w3.org/WAI/WCAG22/quickref/
- https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum
- https://www.w3.org/WAI/WCAG22/Understanding/dragging-movements
- https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum

## Decision

Adopt a dedicated Playwright-based WCAG 2.2 AA regression baseline, but explicitly do not treat automated success as a WCAG conformance claim.

The automated baseline runs against the built application and checks the currently exposed primary and secondary surfaces in Understand / Analyze / Act / Library. It covers reproducible invariants that can be tested without subjective interpretation:

- descriptive page title and valid page-language state;
- unique DOM IDs;
- visible interactive controls have an accessible-name source;
- no visible focusable controls inside `aria-hidden="true"` content;
- non-inline control targets sampled by the gate are at least 24×24 CSS px;
- sampled keyboard-focusable controls are not fully outside the viewport or completely obscured by author-created content after focus;
- primary navigation can be activated with the keyboard and exposes state through `aria-pressed`;
- RO/EN switching updates the document language metadata;
- all primary/secondary surfaces reflow without horizontal page overflow at 320 CSS px;
- all primary/secondary surfaces avoid horizontal page overflow when root text is scaled to 200%;
- the canonical visual target token remains 44 CSS px.

The gate is intentionally narrower than full WCAG 2.2 AA conformance. It is a regression detector, not an accessibility certification tool.

## Manual audit remains mandatory

The following remain explicit manual or assistive-technology audit work and cannot be promoted to PASS merely because the automated baseline is green:

- complete keyboard traversal, focus order and no-keyboard-trap verification across every dynamic state;
- focus visibility and Focus Not Obscured verification for all transient panels, dialogs, overlays and viewport states;
- screen-reader semantics, landmark navigation, accessible names/descriptions, live regions and status announcements;
- color contrast, non-text contrast and content-on-hover/focus review;
- Dragging Movements inventory and confirmation of a non-drag single-pointer alternative wherever dragging provides functionality;
- Target Size exception review for inline links, labels that enlarge checkbox/radio targets, spatial controls and any intentionally undersized target;
- charts/graphs: non-visual equivalents, reading order and keyboard/assistive-technology access;
- form error identification, instructions and status messaging in realistic task flows;
- criteria that are not applicable to the present application must be recorded as N/A with a reason rather than silently omitted.

A later OA-8 slice will record the manual keyboard/screen-reader audit results separately. Automated and manual evidence must remain distinguishable.

## Scientific and product boundary

This slice changes no scientific model, equation, coefficient, evidence snapshot, epistemic status, provenance relation, persistence schema or decision output. Accessibility-test success is not evidence of scientific validity.

No native GTK4/Granite/Flatpak accessibility claim is made here. Native accessibility is evaluated in OA-9 against the native implementation.

## Consequences

Positive:

- WCAG-related regressions become visible in the authoritative browser gate;
- coverage is applied across all four product surfaces rather than one feature at a time;
- the project gains an explicit audit boundary and avoids equating automation with conformance.

Limitations:

- the accessible-name and focus-obscuration checks are conservative browser heuristics, not replacements for the browser accessibility tree or assistive-technology testing;
- target-size automation intentionally excludes categories with normative WCAG exceptions or spatial semantics and therefore requires manual review;
- a green CI run means only that the encoded automated invariants passed.

## Exit gate for OA-8B

- existing scientific/reference CI remains unchanged and green;
- existing browser smoke remains green;
- dedicated `test:a11y` browser gate passes on the built app;
- audit boundary is documented as automated PARTIAL coverage plus mandatory manual follow-up;
- no WCAG conformance claim is emitted by the application or release process.
