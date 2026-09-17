# ADR 0034 — Local diagnostics without mandatory telemetry

Status: ACCEPTED

Date: 2026-09-17

Track: OA-8 — Trust Hardening

## Context

OA-8 requires diagnostics that help reproduce runtime/support state without creating an analytics or telemetry dependency. CEM is local-first and does not require accounts, cloud sync, or remote diagnostics.

## Decision

### 1. Diagnostics are explicit local records

The web runtime exposes a small local-diagnostics record and serializer/download helper. The record is generated only in the local browser process and is not uploaded by the diagnostics module.

Every record declares:

- `scope = LOCAL_RUNTIME_ONLY`;
- `telemetry = NONE`.

### 2. Minimize collected fields

The diagnostics schema contains only:

- software version and optional release tag;
- model specification;
- evidence snapshot ID and `as_of` date;
- online/offline state;
- localStorage availability;
- IndexedDB availability;
- service-worker controlled/not-controlled state;
- generation timestamp.

It deliberately excludes:

- workspace/case content;
- notes, search queries, history or learner records;
- URLs/location history;
- user-agent/device fingerprint fields;
- names, email addresses, IP addresses or account identifiers.

### 3. No mandatory telemetry transport

The diagnostics module contains no network upload API, analytics integration, `fetch`, `sendBeacon`, remote endpoint, or background reporting behavior. Sharing an exported diagnostics file, if ever requested for support, remains an explicit user action outside this module.

### 4. Diagnostics do not establish scientific validity

A healthy runtime-capability record says nothing about empirical validity, psychological validation, calibration, or evidence strength. It is operational support metadata only.

## OA-8H exit gate

OA-8H is complete when:

1. diagnostics serialization is deterministic for fixed inputs/time;
2. the record contains only the declared minimal fields;
3. offline/unavailable capabilities are represented explicitly rather than treated as exceptions;
4. no telemetry/network transport is introduced by the diagnostics module;
5. full Verify and CodeQL remain green;
6. no scientific baseline artifact changes.
