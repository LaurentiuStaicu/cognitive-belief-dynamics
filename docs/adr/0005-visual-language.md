# ADR 0005 — OA-3 visual language

Status: Accepted for OA-3B implementation.

## Context

OA-3A fixed the information architecture. OA-3B needs a single visual contract so
navigation, Theory, Registry, charts and later workspace surfaces do not evolve as
independent style islands.

Project priorities already require a system-first font stack, neutral shared
surfaces, system light/dark preference, semantic colors, a 6 px spacing rhythm,
at least 12 px content margins, visible keyboard focus, readable text at 200% and
chart patterns in addition to color.

The elementary HIG currently recommends at least 12 px between widgets and window
borders and 6 px between buttons. WCAG 2.2 defines a 24 x 24 CSS px minimum target
at Level AA; CEM retains its stronger existing 44 px control target. WCAG reflow
and visible focus remain regression gates.

## Decision

OA-3B defines one versionless UI contract (it is not scientific/model versioning):

- spacing unit: 6 px, scale 6/12/18/24/36/48 px;
- content edge minimum: 12 px;
- system UI font first, Inter only as a local fallback, no network font dependency;
- prose reader width: 72 ch;
- interactive target minimum: 44 px;
- focus ring: 3 px with a 3 px offset;
- adaptive shell breakpoints: 760 px compact, 1050 px medium;
- shared base/raised/inset surface roles derived from the existing light/dark theme;
- chart series retain three different stroke patterns as well as colors;
- epistemic status labels remain textual and gain distinct short markers. Colors are
  redundant category cues, never evidence-strength scores.

## Epistemic presentation

The following categories receive visual markers without changing their scientific
meaning: EMPIRICAL, EXECUTABLE, CONCEPTUAL, INTERPRETIVE, EXPERIMENTAL,
META_ANALYTIC, CANDIDATE and REFERENCE_CANDIDATE.

Registry evidence fields continue to expose their original status strings and
localized text. Theory keeps the canonical status values already stored in its
content index. OA-3B changes presentation only.

## Adaptive shell

Desktop shows four equal primary domain targets. Compact layouts use two columns,
and very narrow layouts one column. Secondary views stack on compact widths.
Existing reflow and 200% text browser tests remain authoritative.

## Boundaries

- no Search or Universal Inspector (OA-4);
- no new scientific status, score or evidence hierarchy;
- no equation, coefficient, semantic ID, evidence source, workspace schema,
  reference output or release-version change;
- no claim that the web CSS is native GTK/AppCenter compliance.

## External design basis

- elementary HIG: Creating Layouts;
- elementary HIG: Text;
- elementary HIG: Accessible Configuration;
- W3C WCAG 2.2 target size and focus guidance;
- W3C WCAG reflow guidance.
