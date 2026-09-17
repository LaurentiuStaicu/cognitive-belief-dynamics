# OA-8D Supply-Chain Audit — Dependency Review + SBOM

Status: COMPLETE

Date: 2026-09-17

Integrated commit: `2bab46009cd1099b80ca307522d2ad63e5dd34ea`

Scope: OA-8D trust-hardening slice only.

## Controls introduced

- pull-request Dependency Review gate for runtime + development dependency changes;
- fail threshold: newly introduced known vulnerabilities at `high` severity or above;
- exact-commit pinning for Dependency Review and SBOM actions;
- SPDX JSON SBOM generated from the verified repository workspace;
- npm inventory from `web/package-lock.json`;
- Python runtime inventory materialized from the versions resolved by CI because Python is not currently lockfile-pinned;
- required direct runtime inventory assertion for `numpy`, `scipy`, `jsonschema`, `cytoscape`, and `d3`;
- workflow artifact `cognitive-epistemic-model-sbom`;
- release integration with checksum and GitHub artifact attestation.

## Interpretation boundary

This record does not claim that the repository has no vulnerable dependencies. Dependency Review prevents specified classes of newly introduced dependency risk; CodeQL covers separate source-code security checks; the SBOM records dependency inventory/provenance.

The Python portion is a CI-resolution snapshot, not a lockfile guarantee. Exact Python environment locking is not introduced in OA-8D.

## Scientific-invariance check

OA-8D changes only GitHub Actions and documentation. It does not alter:

- model equations or coefficients;
- evidence snapshot or empirical targets;
- M0/M1 reference results;
- semantic IDs, relations, or epistemic statuses;
- web runtime behavior;
- decision/reality-loop contracts.

## Closure evidence

On PR #78 head `8a4fa0c31687d1bd9dce699728eeb55f17a3baa6`:

- [x] Verify model and web #298 — green
- [x] Dependency Review #2 — green after Dependency Graph enablement
- [x] CodeQL Python #19 — green
- [x] CodeQL JavaScript/TypeScript #19 — green
- [x] SPDX SBOM inventory assertion — green
- [x] SBOM workflow artifact present

On integrated commit `2bab46009cd1099b80ca307522d2ad63e5dd34ea`:

- [x] post-merge Verify model and web #299 — green
- [x] post-merge CodeQL #20 Python — green
- [x] post-merge CodeQL #20 JavaScript/TypeScript — green
- [x] post-merge SBOM generation, validation and artifact upload — green

OA-8D is therefore integrated and complete within its declared scope.
