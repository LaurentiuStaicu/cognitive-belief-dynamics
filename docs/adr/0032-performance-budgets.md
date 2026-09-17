# ADR 0032 — Deterministic web performance budgets

Status: ACCEPTED

Date: 2026-09-17

Track: OA-8 — Trust Hardening

## Context

The CEM production build is a static Vite application with bundled scientific/model assets. OA-8 requires performance budgets that detect growth regressions without making CI depend on noisy hosted-runner timing measurements.

The verified OA-8D build immediately before this decision reported approximately:

- primary JavaScript chunk: 859.12 kB uncompressed;
- secondary JavaScript chunk: 10.61 kB uncompressed;
- stylesheet: 61.25 kB uncompressed;
- 66 files in the uploaded web build artifact.

Vite already warns that the current primary chunk exceeds its generic 500 kB warning threshold. This ADR does not relabel that warning as optimal performance. It establishes a regression ceiling so later module growth cannot silently make the delivery footprint materially worse.

## Decision

### 1. Use deterministic build-artifact budgets as the OA-8 CI gate

After `vite build`, CI runs `scripts/performance-budget.mjs`. The gate measures the actual production `dist/` tree and fails if any limit is exceeded:

- largest JavaScript asset: 1,000,000 bytes;
- all JavaScript assets combined: 1,200,000 bytes;
- all CSS assets combined: 100,000 bytes;
- complete uncompressed `dist/` tree: 8 MiB;
- total built files: 120.

The limits intentionally provide bounded headroom above the current verified baseline while making significant bundle/resource growth an explicit architectural decision.

### 2. Do not use hosted-runner wall-clock timing as a required gate

Wall-clock browser/build timing on shared CI infrastructure is hardware- and load-sensitive. OA-8 therefore does not fail PRs on a single lab timing measurement.

This does not mean latency is irrelevant. Browser smoke tests continue to exercise the real production build, and future performance work may add controlled lab/field measurements where the measurement contract is stable enough to support a gate.

### 3. Budget changes require an explicit review

A budget may be changed when product scope legitimately changes, but the change must be visible in code review and justified against the then-current baseline. It must not be silently raised merely to turn a red CI run green.

### 4. Budgets are delivery constraints, not scientific constraints

No model equation, scientific artifact, evidence status, reference run, semantic relation, or epistemic claim changes in this slice.

## External basis

Google/web.dev documents performance budgets as thresholds integrated into the build process and explicitly supports resource-size and resource-count budgets. It also notes that uncompressed JavaScript size is relevant to execution cost while compressed size is relevant to transfer cost.

- https://web.dev/articles/incorporate-performance-budgets-into-your-build-tools
- https://web.dev/articles/use-lighthouse-for-performance-budgets

## OA-8F exit gate

OA-8F is complete only when:

1. the current production build passes every declared budget;
2. an intentionally oversized fixture/change would fail the budget script;
3. the budget script runs automatically as part of `npm run build`;
4. full Python/web/browser CI and CodeQL remain green;
5. no scientific baseline artifact changes.
