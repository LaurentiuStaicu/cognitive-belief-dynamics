# ADR 0029 — OA-8 keyboard and assistive-technology audit gate

Status: Proposed.

## Context

OA-8 already has:

- CodeQL baseline for Python and JavaScript/TypeScript;
- an automated WCAG 2.2 AA browser regression baseline.

Those checks reduce regressions but cannot establish complete accessibility or assistive-technology interoperability. W3C WAI explicitly states that automated tools alone cannot determine whether a site is accessible and that knowledgeable human evaluation is required. WAI-ARIA APG also recommends testing implementations with relevant browser and assistive-technology combinations.

References:

- https://www.w3.org/WAI/test-evaluate/
- https://www.w3.org/WAI/test-evaluate/conformance/wcag-em/
- https://www.w3.org/WAI/ARIA/apg/practices/keyboard-interface/
- https://www.w3.org/WAI/ARIA/apg/practices/read-me-first/

## Decision

OA-8 separates this gate into two evidence classes.

### Automated keyboard traversal prerequisite

A dedicated Playwright regression performs real `Tab` traversal on every currently exposed primary/secondary surface.

For each stable surface it:

- identifies visible, enabled sequential keyboard-focus candidates;
- handles native radio-group sequential focus semantics;
- starts from a body focus sentinel;
- presses `Tab` rather than programmatically focusing each control;
- fails if any expected sequential focus target is never reached within a bounded traversal;
- therefore catches focus traps and controls that are nominally focusable but unreachable by sequential keyboard navigation.

This is regression evidence only.

### Manual keyboard + AT audit

`docs/audits/OA8_KEYBOARD_AT_MANUAL_AUDIT.md` is the canonical manual execution protocol.

Its initial document status is `PENDING_MANUAL_EXECUTION`.

The primary Linux AT matrix is:

- Orca + Firefox;
- Orca + Chromium.

The protocol also requires manual keyboard-only traversal, RO/EN coverage, dynamic-state focus review, graph/non-visual-alternative review and explicit PASS / FAIL / NOT_APPLICABLE / NOT_TESTED results.

## Non-claims

A green automated keyboard traversal does not mean:

- WCAG 2.2 AA conformance;
- screen-reader usability;
- correct announcement wording in every AT;
- correct behavior on untested browser/AT combinations;
- accessibility on future native GTK/Flatpak surfaces.

A manual PASS is scoped to the exact audited commit and recorded environments.

## Scientific boundary

No equation, coefficient, evidence snapshot, epistemic status, semantic relation, persistence schema, intervention ranking, reference run or scientific output changes in this slice.

## Exit gate for this PR

- existing Verify model and web CI remains green;
- CodeQL remains green;
- automated exhaustive Tab traversal is green across all exposed surfaces;
- the manual audit protocol is present with `PENDING_MANUAL_EXECUTION`;
- no manual result is fabricated.

## Follow-up

A later OA-8 manual-audit execution record must populate the protocol with real environment/version data and findings. Any blocker/major finding is fixed in a separate focused PR and retested before the manual gate can be closed.
