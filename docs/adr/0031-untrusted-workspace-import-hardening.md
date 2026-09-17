# ADR 0031 — Untrusted workspace import hardening

Status: ACCEPTED

Date: 2026-09-17

Track: OA-8 — Trust Hardening

## Context

CEM supports portable local workspace files (`.cem.json`). Imported files are user-controlled input. The OA-2 contract already provides versioned JSON import, migration, schema validation, recovery preservation, and fail-closed rejection for corrupt/future schema versions. OA-8 requires an additional resource-safety boundary for untrusted imports.

This ADR does not change the workspace scientific meaning, canonical schema, model equations, evidence statuses, semantic relations, reference runs, or UI interpretation.

## Decision

### 1. Keep JSON + canonical schema as the semantic boundary

CEM continues to accept only JSON workspace data and validates the resulting workspace with the existing canonical workspace validator. No native object serialization, executable format, polymorphic type reconstruction, script execution, or remote import is introduced.

### 2. Add an input resource envelope before migration/provenance work

Portable workspace imports are bounded by:

- maximum UTF-8 input size: 5 MiB;
- maximum parsed structural depth: 64 levels;
- maximum parsed node count: 100,000 values/containers;
- top-level value must be a JSON object.

The text-size limit is checked before `JSON.parse`. Structural limits are checked immediately after parsing and before cloning, migration, validation, or provenance expansion.

The traversal is iterative so the hardening check itself does not depend on recursive JavaScript stack depth.

### 3. File reads fail before allocation beyond the declared envelope

`readWorkspaceFile()` checks `File.size` before calling `file.text()`. Direct callers of `importWorkspaceText()` are independently protected by the UTF-8 byte-length check, so bypassing the file helper does not bypass the resource limit.

### 4. File extension and MIME type are not trusted as security proofs

The exported convention remains `.cem.json`, but import safety is based on bounded JSON parsing plus canonical schema validation rather than trusting a client-supplied filename or MIME type. This preserves compatibility with valid portable workspaces while avoiding a false security claim based on metadata that can be spoofed.

### 5. Fail closed without touching persistent state

All import-envelope failures throw a `WorkspaceImportError` subtype before `installWorkspaceImport()` can modify active, recovery, or original-import storage keys.

Existing behavior remains:

- corrupt JSON is rejected;
- unsupported future schema versions are rejected;
- current schema is validated;
- legacy v0 is migrated under the existing explicit migration path;
- previous active workspace is preserved as recovery only after a valid import is ready to install.

## Threat boundary

These controls mitigate accidental or malicious resource amplification from oversized or pathologically structured local JSON input. They do not claim to make arbitrary files trustworthy and do not replace canonical schema validation.

Because CEM parses plain JSON and does not instantiate attacker-selected executable classes, this slice avoids native-object deserialization mechanisms entirely.

## External basis

- OWASP Input Validation Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html
- OWASP File Upload Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html
- OWASP Deserialization Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Deserialization_Cheat_Sheet.html

## OA-8E exit gate

OA-8E is complete only when, on the exact PR head:

1. existing v0/v1 workspace import and round-trip tests remain green;
2. corrupt and future-schema rejection remains green;
3. oversized input is rejected before parse/install;
4. top-level non-object input is rejected;
5. excessive nesting is rejected;
6. excessive node count is rejected;
7. full Python/web/browser CI and CodeQL remain green;
8. no scientific baseline artifact changes.
