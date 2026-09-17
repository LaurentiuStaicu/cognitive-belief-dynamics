# ADR 0030 — Dependency review and SBOM supply-chain boundary

Status: ACCEPTED

Date: 2026-09-17

Track: OA-8 — Trust Hardening

## Context

CEM currently has two package ecosystems used by the verified build:

- Python dependencies declared in `pyproject.toml`;
- npm dependencies locked by `web/package-lock.json`.

The repository already runs full model/web verification and CodeQL. OA-8 also requires dependency review and a release-visible software bill of materials (SBOM) so dependency changes and shipped dependency inventory are inspectable.

This ADR does not change any scientific model, evidence status, equation, reference run, semantic relation, UI behavior, or OA baseline.

## Decision

### 1. Pull-request dependency review

A dedicated `Dependency review` workflow runs on pull requests targeting `main` using GitHub's dependency review action pinned to an exact commit.

The gate evaluates both runtime and development scopes and fails when a pull request introduces a dependency with a known vulnerability of `high` severity or above.

The dependency review gate is prospective: it protects against newly introduced dependency risk. It does not claim that the existing dependency set is vulnerability-free.

### 2. Verified-build SBOM

The authoritative `Verify model and web` workflow generates an SPDX JSON SBOM using Anchore Syft through `anchore/sbom-action`, pinned to an exact action commit.

The SBOM is generated only after the normal Python tests, reference-run reproduction, web build and browser tests have passed far enough to reach the supply-chain steps. The workflow validates that the resulting SBOM contains the direct runtime dependencies expected from both ecosystems:

- Python: `numpy`, `scipy`, `jsonschema`;
- web runtime: `cytoscape`, `d3`.

The verified SBOM is uploaded as the workflow artifact `cognitive-epistemic-model-sbom`.

### 3. Python dependency materialization boundary

The project currently has no Python lockfile. Syft's Python source catalogers do not treat `pyproject.toml` itself as a resolved lock inventory. Therefore, before SBOM generation, CI installs the project into a temporary `.sbom-python` target inside the workspace. Syft then sees the resolved installed Python package metadata together with the npm lockfile.

Consequences:

- the SBOM records the Python versions actually resolved in that CI run;
- it is not a claim that those Python versions are globally or permanently reproducible from `pyproject.toml` alone;
- exact Python dependency reproducibility remains a separate future decision if/when a Python lock strategy is adopted.

No generated `.sbom-python` content is committed to the repository.

### 4. Release provenance

The alpha-release workflow downloads the SBOM artifact from the exact successful verification run associated with the release commit. The SBOM is then:

- attached to the release assets;
- included in `SHA256SUMS.txt`;
- included in the GitHub artifact attestation subject set.

The release workflow fails if the expected verified SBOM artifact is missing.

## Security and trust interpretation

The SBOM is an inventory/provenance artifact, not a security certificate. Dependency Review is a change gate, not proof that no vulnerable dependency exists. CodeQL remains a separate source-code security analysis gate.

These controls are complementary:

`Dependency Review -> verified build -> SPDX SBOM -> checksum + attestation -> release asset`

## External basis

- GitHub Dependency Review documentation: https://docs.github.com/en/code-security/concepts/supply-chain-security/dependency-review
- GitHub SBOM documentation: https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/establish-provenance-and-integrity/export-dependencies-as-sbom
- Dependency Review Action: https://github.com/actions/dependency-review-action
- Anchore SBOM Action / Syft: https://github.com/anchore/sbom-action

## OA-8D exit gate

OA-8D is complete only when, on the exact PR head:

1. the normal `Verify model and web` workflow is green;
2. Dependency Review is green;
3. CodeQL Python is green;
4. CodeQL JavaScript/TypeScript is green;
5. the SBOM artifact is present and passes the workflow inventory assertion;
6. the PR remains scientifically inert relative to the OA baseline.

After merge, the same normal post-merge verification must be green before OA-8D is considered integrated.
