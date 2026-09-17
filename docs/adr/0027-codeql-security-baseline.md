# ADR 0027 — OA-8 CodeQL security baseline

Status: Proposed.

## Context

OA-7 is complete within roadmap scope after PR #74 and post-merge CI #279.

OA-8 Trust Hardening requires, among other gates, CodeQL coverage for Python and TypeScript. CEM currently has authoritative Python model/tooling code and a TypeScript web application, while no CodeQL workflow exists on `main`.

GitHub documents CodeQL support for both `python` and `javascript-typescript`. Public GitHub repositories are eligible for code scanning with CodeQL advanced setup.

Authoritative references:

- https://docs.github.com/en/code-security/concepts/code-scanning/codeql/codeql-code-scanning
- https://docs.github.com/en/code-security/how-tos/find-and-fix-code-vulnerabilities/configure-code-scanning/configuring-advanced-setup-for-code-scanning
- https://docs.github.com/en/code-security/reference/code-scanning/workflow-configuration-options

## Decision

Add a dedicated `.github/workflows/codeql.yml` workflow with a two-language matrix:

- `python`;
- `javascript-typescript`.

The workflow runs on:

- pull requests targeting `main`;
- pushes to `main`;
- explicit manual dispatch.

Each language is analyzed independently with `fail-fast: false` so one extractor failure does not hide the state of the other language.

The CodeQL query suite is `security-extended`, adding security queries beyond the default suite while remaining an official built-in GitHub suite.

## Supply-chain boundary

Repository workflows already pin third-party GitHub Actions by immutable commit SHA. This PR preserves that policy.

CodeQL Action v4.38.0 is pinned to:

`b96794f015dfd88f77b49b1c93e0fa7110f94c63`

rather than referencing a mutable major-version tag.

The existing checkout action remains pinned to the repository's current reviewed SHA.

## Permissions

The CodeQL job receives only the permissions required for analysis and SARIF upload:

- `contents: read`;
- `actions: read`;
- `packages: read`;
- `security-events: write`.

No repository-content write permission is introduced.

## Build boundary

Python and JavaScript/TypeScript are interpreted CodeQL languages. This slice does not duplicate CEM's existing application build or model test pipeline inside CodeQL. Functional correctness remains the responsibility of `Verify model and web`; CodeQL adds static security analysis as a separate trust gate.

## Scientific boundary

This PR changes no scientific model equation, parameter, evidence state, semantic relation, result fixture, intervention ranking, calibration state or release metadata.

A successful CodeQL scan is evidence about static security checks only. It is not evidence of scientific correctness, complete security, accessibility, privacy compliance or empirical validity.

## OA-8 sequencing

This is the first narrow OA-8 implementation slice. It does not close the other OA-8 requirements.

Subsequent separate slices remain required for:

- WCAG 2.2 AA and manual keyboard/screen-reader audit;
- dependency review;
- SBOM/release integration;
- untrusted import hardening;
- performance budgets;
- offline/stale-evidence policy;
- local diagnostics without mandatory telemetry.

Native elementary OS / GTK4 / Granite / Flatpak work remains deferred until the planned web modules are complete and the product approaches version 1.

## Exit gate

This slice can be integrated only if:

1. the existing full model/web CI is green;
2. CodeQL completes successfully for Python;
3. CodeQL completes successfully for JavaScript/TypeScript;
4. no workflow permission broader than documented above is introduced;
5. any findings are reviewed rather than silently ignored.
