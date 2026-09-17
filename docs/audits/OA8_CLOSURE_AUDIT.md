# OA-8 — Trust Hardening Closure Audit

Status: **CANDIDATE FOR CLOSURE**

Date: 2026-09-17

Integrated baseline audited here: `2bab46009cd1099b80ca307522d2ad63e5dd34ea`

Track: OA-8 — Trust Hardening

## 1. Scope

This audit closes the pre-v1 OA-8 trust-hardening scope. It introduces no scientific model change, no new epistemic claim and no new product behavior.

The authoritative implementation plan lists the OA-8 controls as:

- WCAG 2.2 AA audit;
- screen-reader/manual keyboard audit;
- dependency review;
- CodeQL Python + TypeScript;
- SBOM/release integration;
- untrusted import hardening;
- performance budgets;
- offline/stale-evidence policy;
- local diagnostics with no mandatory telemetry.

## 2. Integrated controls

The following controls are integrated in `main` and covered by CI or explicit contract tests:

1. **CodeQL security baseline** — Python and JavaScript/TypeScript analysis are active and green on the audited baseline.
2. **Automated WCAG 2.2 AA baseline** — automated accessibility, keyboard, reflow and target-size protections are retained as regression gates. This is not represented as a complete WCAG conformance claim.
3. **Dependency Review** — Dependency Graph is enabled and the pull-request dependency-review gate is operational. The gate is prospective and does not claim that the existing dependency set is vulnerability-free.
4. **Verified SPDX SBOM** — the verified build generates, validates and uploads an SPDX JSON SBOM; release packaging consumes the SBOM from the exact successful verification run and includes it in checksum/attestation scope.
5. **Untrusted import hardening** — portable workspace imports are bounded before expensive processing and fail closed for oversized/excessively deep/excessively large structures while retaining schema validation.
6. **Performance budgets** — deterministic build-artifact budgets guard against silent asset-size/count regressions without relying on noisy wall-clock timing.
7. **Offline / stale-evidence policy** — online/offline state does not silently strengthen or weaken epistemic status; bundled evidence remains explicitly pinned with inspectable `as_of` metadata, and no unsupported freshness threshold is invented.
8. **Local diagnostics / no telemetry** — diagnostics are local-only, minimal and explicitly declare `telemetry = NONE`; no mandatory upload path or analytics transport is introduced.

## 3. Manual keyboard / assistive-technology boundary

The detailed manual audit in `OA8_KEYBOARD_AT_MANUAL_AUDIT.md` is **DEFERRED_POST_V1** by explicit project prioritization.

This is a scope deferral, not a PASS. Therefore:

- OA-8 closure must not be described as complete WCAG 2.2 AA conformance;
- Orca + Firefox / Chromium interoperability remains unverified at the full task-matrix level;
- manual keyboard and screen-reader execution must be resumed after v1 or immediately before any release claim that depends on that evidence;
- any blocker/major finding discovered then must be fixed and retested before making the corresponding accessibility claim.

Automated accessibility regression gates remain active during pre-v1 development so the deferred manual audit starts from a hardened baseline rather than from zero.

## 4. Supply-chain gate evidence

PR #78 was integrated as merge commit `2bab46009cd1099b80ca307522d2ad63e5dd34ea` only after the exact PR head passed:

- Verify model and web;
- Dependency Review;
- CodeQL Python;
- CodeQL JavaScript/TypeScript;
- SPDX SBOM generation and inventory validation;
- SBOM artifact presence.

Post-merge on `2bab46009cd1099b80ca307522d2ad63e5dd34ea`:

- Verify model and web #299 — `success`;
- CodeQL #20 Python — `success`;
- CodeQL #20 JavaScript/TypeScript — `success`;
- post-merge SBOM generation and validation — `success`.

## 5. Scientific and epistemic invariants

OA-8 hardening does not authorize changes to:

- M0 equations or reference trajectories;
- M1.E1 / M1.E2 / M1.E3 scientific outputs;
- M1.E4 human-model activation status;
- evidence snapshot identity or evidence-strength claims;
- semantic IDs / relations / epistemic statuses;
- simulation-versus-observation boundaries;
- SimulationResult / DecisionAnalysis / ImplementationPlan / ObservedOutcome separation;
- prospective plans, trigger snapshots or retrospective append-only history.

A green trust-hardening gate means the software-control boundary passed; it does not establish psychological, empirical or real-world policy validity.

## 6. Residual limitations and deferred work

The following remain outside the completed pre-v1 OA-8 scope:

- full manual screen-reader / assistive-technology matrix;
- full manual keyboard audit record across every exposed surface;
- any universal WCAG 2.2 AA conformance claim;
- exact Python lockfile reproducibility (the SBOM records CI-resolved Python versions, not a Python lock guarantee);
- OA-9 native elementary OS / GTK4 / Granite / Flatpak implementation.

OA-9 remains intentionally deferred until the web application is at or near v1, so web and native UI development are not duplicated while modules are still changing.

## 7. Closure criteria

The pre-v1 OA-8 track may close only when:

- all OA-8 functional/security slices are integrated in `main`;
- Verify and CodeQL are green on the final integrated baseline;
- Dependency Review is operational;
- SBOM generation/validation/release integration is operational;
- import hardening, performance budgets, evidence freshness/offline policy and local diagnostics are regression-gated;
- the manual AT audit is explicitly recorded as `DEFERRED_POST_V1`, not silently treated as passed;
- no scientific baseline drift is introduced by this closure PR;
- the closure PR itself and its post-merge CI are fully green.

## 8. Exit gate

If this documentation-only closure PR and its post-merge CI are fully green, **OA-8 / Trust Hardening is formally closed for the pre-v1 web optimization scope**.

This closure does not make a WCAG conformance claim and does not execute OA-9. The next development track returns to completing the scientific/product modules toward v1; the full manual AT audit and native elementary OS / Flatpak work remain deferred as recorded above.
