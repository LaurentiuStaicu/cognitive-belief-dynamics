# ADR 0004 — OA-3 information architecture

Status: Accepted for OA-3A implementation.

## Context

CEM accumulated seven top-level views while preserving the user's priority order: understand mechanisms first, analyze/prioritize second and plan action third. The flat navigation exposed every surface simultaneously but did not communicate that task hierarchy.

OA-3 must reorganize the application without deleting scientific or explanatory surfaces, renaming canonical scientific IDs, changing model behavior or pulling Search/Universal Inspector forward from OA-4.

W3C landmark guidance also favors logical page regions and uniquely labelled navigation landmarks when more than one navigation area exists.

## Decision

The application uses four stable user-purpose domains:

1. Înțelege / Understand: Theory & mechanisms (learning), Map (structure), Methodology · Visual ODD (process).
2. Analizează / Analyze: Scenarios (runs), Comparisons (comparison).
3. Acționează / Act: Priorities & plan (planning).
4. Bibliotecă / Library: Scientific registry (reference).

The existing internal view IDs remain unchanged. They are implementation routes, not user-facing information-architecture labels.

The UI exposes two navigation landmarks: primary purpose/domain navigation and secondary views within the active domain. Each landmark has a distinct accessible label. Switching a primary domain opens its declared default child view. Internal links may still navigate directly to any existing view, in which case the active domain is derived from the view.

## Invariants

- all seven pre-OA-3 views remain mapped exactly once;
- learning remains the initial/default application view;
- project priority remains Understanding → Analyze → Act, with Library supporting all three rather than becoming a scientific workflow stage;
- Theory remains inside Understanding rather than becoming a duplicate top-level route;
- Registry remains directly discoverable under Library;
- RO/EN labels remain available;
- keyboard focus order follows DOM/visual order;
- no Search or Universal Inspector is added in OA-3;
- no equation, parameter, evidence status, semantic ID, reference output, workspace schema or release version changes.

## Consequences

The application gains a stable task-oriented shell while preserving all existing functionality and deep navigation behavior. OA-3B may now define visual tokens and responsive shell styling against a fixed IA instead of styling a moving target.

## External design basis

- W3C WAI-ARIA APG landmark guidance;
- WCAG 2.2 navigation/focus requirements;
- WCAG 2.1 reflow requirement.

These sources guide interface accessibility, not scientific validity.
