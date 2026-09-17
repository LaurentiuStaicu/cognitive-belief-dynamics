# ADR 0033 — Offline and stale-evidence policy

Status: ACCEPTED

Date: 2026-09-17

Track: OA-8 — Trust Hardening

## Context

CEM is a static, local-first web application whose scientific/evidence artifacts are bundled with the verified release. The application does not currently perform live evidence synchronization and does not register a service worker.

OA-8 requires a clear policy for network loss and evidence freshness so connectivity, browser caching, and scientific currency are not conflated.

## Decision

### 1. The evidence snapshot is pinned and bundled

The runtime evidence state is identified by the release's canonical `model/evidence_snapshot.json`, including `id`, `model_specification`, and `as_of`.

Its runtime trust mode is always:

- `PINNED_BUNDLED_SNAPSHOT`;
- freshness: `NOT_LIVE_VERIFIED`.

Being online must never upgrade the bundled snapshot to “current”, “fresh”, or “live verified”.

### 2. Connectivity does not change epistemic status

The network state is reported independently as `ONLINE` or `OFFLINE`. Switching between those states cannot alter:

- evidence snapshot identity;
- model specification;
- evidence status;
- scientific validation status;
- interpretation of stored results.

### 3. No arbitrary stale threshold

CEM exposes the snapshot `as_of` date and a deterministic age in days, but OA-8 does not invent a universal number of days after which scientific evidence becomes “stale”. Evidence domains differ in update cadence, and the repository currently has no authoritative refresh-SLA contract.

A future evidence-refresh process may introduce a domain-specific freshness policy, but that would require an explicit evidence/governance decision.

### 4. Offline behavior is bounded honestly

The current web build has no service worker and therefore makes no guarantee that a first visit or arbitrary asset reload will work without network access. Browser cache may allow some previously loaded content to remain available, but CEM does not claim that as a controlled offline package.

The runtime policy therefore reports:

`offline_guarantee = NONE_WITHOUT_PRIOR_BROWSER_CACHE`

The future native/Flatpak application is a separate delivery target and may have a stronger offline contract when implemented after the web application approaches v1.

### 5. Fail closed on invalid evidence dates

The trust-status helper rejects malformed `as_of` values and snapshots dated in the future relative to the supplied runtime clock rather than generating misleading freshness metadata.

## Scientific boundary

This policy describes provenance/freshness and delivery state only. It does not change equations, parameters, reference runs, evidence classifications, semantic relations, or model outputs.

## OA-8G exit gate

OA-8G is complete when:

1. current canonical snapshot identity/as-of are consumed by regression tests;
2. online and offline states preserve identical evidence identity/status;
3. online connectivity never implies live verification;
4. no arbitrary stale threshold is introduced;
5. no unsupported offline guarantee is claimed;
6. full Verify and CodeQL remain green.
