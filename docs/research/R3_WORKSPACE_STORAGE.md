# R3 — Workspace Storage: IndexedDB transaction, migration and recovery design

Status: **ADOPT_WITH_LIMITS**

Date: 2026-09-16

## Question

How should CEM persist OA-7 Reality Loop objects without silently mutating Workspace v1, losing provenance, or allowing retrospective observations to overwrite prospective decision state?

## Current repository state

- Workspace document schema is version 1.
- Runtime persistence currently uses localStorage keys `cem.workspace.v1.active` and `cem.workspace.v1.recovery`.
- Workspace v1 contains versions, case refs and provenance, but no SimulationResult, DecisionAnalysis, ImplementationPlan, ObservedOutcome or DecisionAutopsy arrays.
- OA-7 contract explicitly marks Reality Loop storage as `RESERVED_NOT_IN_WORKSPACE_V1` and `migration_required = true`.
- AdaptivePlan runtime is currently `EPHEMERAL_NOT_WORKSPACE` and therefore is not yet a canonical ImplementationPlan.
- Canonical ObservedOutcome requires an `implementation_plan_id` and `prospective_snapshot_id`.

## External platform constraints

IndexedDB schema upgrades occur inside the exclusive `versionchange` transaction opened by `IDBFactory.open()` when a higher integer database version is requested. Object stores/indexes must be created or changed there.

Normal data writes use readwrite transactions. If an unhandled request error occurs, the transaction is aborted and its changes are rolled back. Transactions should be short-lived and must not be deferred to unload handlers.

Durability can be requested with the standard transaction durability hint. `strict` asks the user agent to verify persistence before considering the transaction committed; it is a hint, not an absolute guarantee.

References:

- MDN, Using IndexedDB: https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API/Using_IndexedDB
- Indexed Database API 3.0: https://www.w3.org/TR/IndexedDB-3/
- MDN, IDBDatabase.transaction(): https://developer.mozilla.org/en-US/docs/Web/API/IDBDatabase/transaction

## Decision

Adopt IndexedDB as the durable browser persistence layer for Reality Loop objects, while keeping the **Workspace document schema version independent from the storage-database version**.

Do **not** add OA-7 objects directly to Workspace v1 JSON.

Introduce a browser database with a storage schema version and separate object stores:

1. `workspace_documents`
   - key: `workspace_id`;
   - stores the canonical Workspace v1 document;
   - one active document per workspace ID.

2. `reality_loop_objects`
   - key: stable object `id`;
   - stores distinct OA-7 typed objects;
   - indexes: `object_type`, `case_id`, `implementation_plan_id`, `indicator_id`, `created_at` where applicable;
   - canonical object types remain SimulationResult, DecisionAnalysis, ImplementationPlan, ObservedOutcome and DecisionAutopsy.

3. `workspace_recovery`
   - key: `workspace_id`;
   - stores the prior committed Workspace document / storage manifest needed for recovery.

4. `import_originals`
   - key: import token;
   - stores the untouched imported source text before migration/installation.

5. `storage_meta`
   - key/value metadata including storage schema version and completed legacy migration marker.

## Storage schema version versus Workspace schema version

These are separate version dimensions:

- Workspace document schema stays `1` until a deliberate document-contract migration is approved.
- IndexedDB database/storage schema starts at integer version `1`.
- Future IndexedDB object-store/index changes increment the database version and execute in `upgradeneeded`.

This prevents storage implementation details from masquerading as changes to the portable Workspace contract.

## Legacy localStorage migration

Migration from current localStorage must be **copy-first and fail-safe**:

1. Open/create the IndexedDB schema.
2. Read legacy active, recovery and import-original localStorage values without modifying them.
3. Parse and validate the active Workspace using existing Workspace v1 validation.
4. In one bounded readwrite transaction, write the active Workspace, recovery snapshot/import source where present, and a migration marker.
5. Wait for transaction completion.
6. Read the written Workspace back and revalidate it.
7. Only after successful verification may the application mark IndexedDB as authoritative.
8. Legacy localStorage keys should remain temporarily as rollback material until a separately tested cleanup policy is approved.

If any parse, validation, transaction or verification step fails, the migration aborts and localStorage remains authoritative.

## Cross-tab / version-change behavior

Every open database connection must handle `versionchange` by closing the connection. The UI should require reload/reopen before continuing after a storage upgrade.

Blocked upgrade must fail visibly rather than operating with a half-upgraded schema.

## Write policy

User-authored Reality Loop records use short, scoped readwrite transactions.

Where supported, critical user-authored writes should request `{ durability: 'strict' }`; code must still treat this as a durability **hint**, not proof against every hardware/browser failure.

Never start persistence from unload/beforeunload as the primary save mechanism.

## Append-only OA-7 policy

Prospective and retrospective objects are not updated in place when their epistemic meaning changes.

- ImplementationPlan gets a stable ID and frozen ProspectiveSnapshot.
- ObservedOutcome is added with a new ID using an insert-only operation.
- Duplicate IDs fail closed.
- A correction to an observation creates a new observation/revision object; it does not overwrite the earlier record.
- DecisionAutopsy can point to observations and propose revisions, but never edits the original prospective snapshot.

This follows the same provenance principle as W3C PROV revision: a revision is a new derived entity rather than silent mutation of the original.

Reference: https://www.w3.org/TR/prov-o/

## Referential integrity policy

Before committing an ObservedOutcome, runtime validation must prove:

- referenced ImplementationPlan exists;
- referenced ProspectiveSnapshot belongs to that plan;
- referenced Indicator exists and is included in the plan;
- case IDs match;
- observed property/unit/result type are compatible with the Indicator definition;
- phenomenon time <= result time <= recorded_at;
- source refs are non-empty;
- prospective snapshot remains byte-for-byte unchanged by the transaction.

IndexedDB itself does not provide relational foreign-key constraints, so CEM must validate these references before the write and again when loading a case.

## ImplementationPlan prerequisite

A canonical ObservedOutcome cannot be created from the current `AdaptivePlanDraft`.

Before ObservedOutcome runtime, CEM must materialize an ImplementationPlan with:

- stable ImplementationPlan ID;
- case ID;
- originating DecisionAnalysis ID;
- frozen ProspectiveSnapshot ID and content hash;
- plan scope;
- Action Canvas;
- Indicator IDs;
- adaptive NOW/WATCH/IF/THEN/STOP/REASSESS steps;
- for REAL_WORLD scope: explicit population, context and primary outcome.

This materialization is a distinct small implementation concern and should be integrated before the ObservedOutcome recorder.

## Recovery policy

Recovery must operate at a committed-transaction boundary.

- Never expose partially written Reality Loop objects.
- On failed write, leave the previous committed records unchanged.
- On corrupt load, fail closed and preserve the raw record for export/diagnosis where possible.
- Recovery must not synthesize missing provenance or silently drop an invalid observation.

## Portable import/export boundary

Workspace v1 export remains unchanged until a separate portable-bundle contract is approved.

Reality Loop IndexedDB records must not be silently omitted while claiming a complete OA-7 export. Until a portable bundle exists, UI must distinguish `Workspace export` from future `Workspace + Reality Loop bundle export`.

## Security and privacy

IndexedDB remains same-origin browser storage. Imported data is untrusted and must pass schema/runtime validation before installation.

No background synchronization or cloud upload is introduced by R3.

## Decision outcome: ADOPT_WITH_LIMITS

**ADOPT**:

- IndexedDB for durable Reality Loop persistence;
- independent storage schema version;
- transaction-scoped writes;
- copy-first legacy migration;
- append-only OA-7 records;
- explicit referential validation;
- frozen prospective snapshots.

**LIMITS / deferred**:

- no Workspace v1 document-schema change in R3;
- no automatic cloud sync;
- no complete portable OA-7 bundle yet;
- no localStorage cleanup until migration/recovery tests prove rollback;
- no ObservedOutcome write until a canonical ImplementationPlan and ProspectiveSnapshot exist.

## Required implementation sequence after R3

1. IndexedDB storage adapter + legacy localStorage migration/recovery tests.
2. Canonical ImplementationPlan + ProspectiveSnapshot materialization and persistence.
3. ObservedOutcome recorder using append-only validated writes.
4. Decision Autopsy / revision trail.

This sequence does not create a new OA-7 subphase taxonomy; it is the dependency order required to implement the already approved OA-7 roadmap safely.
