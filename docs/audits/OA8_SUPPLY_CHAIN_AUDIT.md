# OA-8D Supply-Chain Audit — Dependency Review + SBOM

Status: PENDING_CI

Date: 2026-09-17

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

## Closure checklist

- [ ] Verify model and web — green on exact PR head
- [ ] Dependency Review — green on exact PR head
- [ ] CodeQL Python — green on exact PR head
- [ ] CodeQL JavaScript/TypeScript — green on exact PR head
- [ ] SPDX SBOM inventory assertion — green
- [ ] SBOM workflow artifact present
- [ ] post-merge Verify model and web — green
- [ ] post-merge CodeQL — green

Do not change `Status` to `COMPLETE` before all applicable closure checks are evidenced on the integrated commit.
