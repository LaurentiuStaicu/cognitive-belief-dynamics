# ADR 0020 — R3 IndexedDB adapter and legacy Workspace migration

Status: Proposed.

## Scope

Implements only the first R3 dependency:

- IndexedDB schema/adapter;
- copy-first migration of current Workspace v1 localStorage data;
- verification and recovery preservation.

It does not yet persist ImplementationPlan, ProspectiveSnapshot, ObservedOutcome or DecisionAutopsy.

## Database schema

Database: `cem-reality-loop`, storage version 1.

Object stores:

- `workspace_documents` — keyPath `workspace_id`;
- `reality_loop_objects` — keyPath `id`, with non-unique indexes for object type, case, implementation plan, indicator and creation time;
- `workspace_recovery` — keyPath `workspace_id`;
- `import_originals` — keyPath `id`;
- `storage_meta` — keyPath `key`.

Workspace document schema remains version 1 and is independent from the IndexedDB integer database version.

## Migration

At startup, after the existing WorkspaceStore has loaded or created the localStorage Workspace:

1. inspect active/recovery/import-original legacy keys;
2. validate all Workspace documents before opening a write transaction;
3. write active/recovery/import source + migration metadata in one readwrite transaction;
4. wait for transaction completion;
5. read the active Workspace back;
6. revalidate and compare it byte-semantically with the parsed source object;
7. retain every localStorage key.

If validation or IndexedDB migration fails, the application logs the failure and continues using localStorage as the authoritative Workspace store.

## Authority boundary

This PR does **not** switch WorkspaceStore to IndexedDB.

IndexedDB is a verified secondary copy preparing the durable Reality Loop storage layer. localStorage remains authoritative until a later explicit cutover PR with its own recovery tests.

## IndexedDB lifecycle

Schema creation occurs only in `upgradeneeded` / the versionchange transaction. Open connections close on `versionchange`. Blocked upgrades fail visibly.

Critical migration writes request `durability:'strict'` where supported, with standard readwrite fallback because durability is a browser hint rather than an absolute guarantee.

References:
- https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API/Using_IndexedDB
- https://developer.mozilla.org/en-US/docs/Web/API/IDBDatabase/versionchange_event
- https://www.w3.org/TR/IndexedDB-3/

## Scientific boundary

No model artifact, equation, coefficient, evidence state, score, reference run or semantic relation changes.

## Next dependency

After integration and green post-merge CI:

1. materialize/persist canonical ImplementationPlan + frozen ProspectiveSnapshot;
2. only then add ObservedOutcome records.
