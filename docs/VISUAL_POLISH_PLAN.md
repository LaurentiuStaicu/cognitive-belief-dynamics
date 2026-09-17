# CEM Visual Polish Plan

Status: active pre-simplification visual-refinement track after OA-8 closure.

## 1. Purpose

Visual Polish refines the existing web interface without adding scientific capability, changing model outputs, or beginning the Simple/Advanced split. The goal is a quieter, more mature, elementary-inspired interface that preserves every currently reachable function while reducing unnecessary visual competition.

This phase is intentionally separate from later product simplification. Visual Polish changes presentation and hierarchy; simplification will later decide what remains visible by default in Simple Mode and what is gated behind the inactive Advanced Mode.

## 2. Design basis

Primary references:

- elementary OS Human Interface Guidelines: consistency, concision, sane defaults, spacing and understandable copy;
- WCAG 2.2 and WAI cognitive-accessibility guidance: visible focus, non-text contrast, reflow, adequate target size, consistent visual design and avoidance of unnecessarily dense layouts.

Existing CEM constraints are retained:

- 6 px spacing rhythm;
- minimum 12 px content margin;
- 44 px interactive target baseline;
- 72ch reader width;
- explicit focus ring;
- color never carries scientific or epistemic meaning alone;
- RO/EN and light/dark remain first-class;
- no automatic motion is introduced.

## 3. Non-goals

Visual Polish MUST NOT:

- change model equations, coefficients, simulations, rankings or reference outputs;
- strengthen evidence status or scientific claims;
- add calibration, robustness, RDM/PRIM, Monte Carlo or other Advanced-only capability;
- implement the Simple/Advanced product split;
- delete or hide existing functionality as a product decision;
- begin GTK4/Granite/Flatpak work;
- silently weaken OA-8 accessibility/security/performance gates.

## 4. Delivery slices

### VP-0 — Contract and baseline

- freeze Visual Polish scope and invariants;
- audit the existing visual token layers and duplicated one-off rules;
- identify representative surfaces across Understand / Analyze / Act / Library;
- record visual acceptance criteria before styling changes.

Exit gate: documentation-only or token-neutral changes; full existing CI green.

### VP-1 — Typography, surfaces and spacing

- consolidate typography scale and vertical rhythm;
- reduce unnecessary bolding and competing emphasis;
- normalize card/panel radius, border weight and surface hierarchy;
- use whitespace to separate sections instead of stacking equally strong boxes;
- preserve readable line lengths and text spacing at zoom/reflow conditions.

Exit gate: no functional DOM/behavior change; light/dark and RO/EN checked; WCAG automated gates green.

### VP-2 — Navigation, controls and interaction states

- harmonize primary/secondary navigation hierarchy;
- normalize button, select, input, details/summary and inline-action styling;
- keep primary actions visually dominant and secondary actions quieter;
- make hover/focus/pressed/disabled states consistent;
- retain minimum target and focus requirements.

Exit gate: keyboard traversal unchanged or improved; no control becomes color-only or hover-only.

### VP-3 — Charts and data-dense surfaces

- refine gridlines, axes, legends, labels and tooltips;
- keep primary traces clear and secondary traces visually quieter;
- reduce label competition while preserving exact values and accessible interpretation;
- standardize numeric typography and table density;
- preserve scientific distinction between series and statuses without relying on color alone.

Exit gate: graph meaning and values byte-for-byte/semantically unchanged; responsive chart behavior remains usable.

### VP-4 — Responsive, light/dark and cross-view consistency

- audit all primary and secondary surfaces at desktop/tablet/mobile widths;
- verify 320 CSS px reflow and 200% text scaling remain intact;
- normalize spacing and hierarchy between views;
- verify light/dark contrast and forced-colors behavior;
- fix visual regressions without introducing layout-specific feature forks.

Exit gate: existing OA-8 accessibility/regression suites green; no two-dimensional page scrolling except intrinsically two-dimensional content.

### VP-5 — Visual closure audit

- compare all seven current views and secondary surfaces against the Visual Polish contract;
- remove accidental styling drift and redundant overrides where safe;
- document remaining density problems that belong to the later Simple/Advanced simplification phase rather than Visual Polish;
- close Visual Polish only after post-merge CI is green.

## 5. Acceptance criteria

A surface is visually polished when:

1. one primary element or task has clear visual priority;
2. headings, body text, metadata and status text form a consistent hierarchy;
3. borders and boxes are used to communicate structure, not as decoration around every block;
4. spacing follows the existing 6 px rhythm unless content semantics justify otherwise;
5. controls with equivalent roles look and behave consistently;
6. charts remain readable without visually overpowering surrounding explanation;
7. light/dark, RO/EN, keyboard focus, reflow and target-size behavior remain valid;
8. no scientific value, evidence state or application behavior changes.

## 6. Relationship to the frozen roadmap

After Visual Polish closes:

1. freeze the final M1 Definition of Done;
2. finish M1 without opening new analytical branches;
3. perform the Simple/Advanced simplification split;
4. validate Simple Mode;
5. continue remaining modules under a Simple-first rule;
6. stabilize the complete web application toward v1;
7. implement the native elementary OS Flatpak only after all planned modules are integrated;
8. reactivate and extend Advanced Mode later when empirical calibration/data justify it.
