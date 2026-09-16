import test from 'node:test';
import assert from 'node:assert/strict';
import {
 CEM_STORAGE_DB_NAME,
 CEM_STORAGE_DB_VERSION,
 CEM_STORAGE_STORES,
 inspectLegacyWorkspaceStorage
} from '../src/workspace-indexeddb.ts';
import {
 WORKSPACE_ACTIVE_KEY,
 WORKSPACE_RECOVERY_KEY,
 type StorageLike,
 type WorkspaceDocument
} from '../src/workspace-store.ts';
import {WORKSPACE_IMPORT_ORIGINAL_KEY} from '../src/workspace-portable.ts';

class MemoryStorage implements StorageLike{
 readonly values=new Map<string,string>();
 getItem(key:string){return this.values.get(key)??null;}
 setItem(key:string,value:string){this.values.set(key,value);}
 removeItem(key:string){this.values.delete(key);}
}

const workspace=():WorkspaceDocument=>({
 schema_version:'1',
 workspace_id:'CEM.WORKSPACE.idb-test',
 created_at:'2026-09-16T18:00:00Z',
 updated_at:'2026-09-16T18:00:00Z',
 versions:{
  software_version:'0.4.2a0',release_tag:'v0.4.2a0',model_specification:'M1',
  evidence_snapshot:'EVIDENCE.M1.2026-09-16.r1',semantic_schema_version:'1',
  semantic_baseline_contract:'OA0.BASELINE.2026-09-16'
 },
 case:{id:'CEM.CASE.idb-test',title:'IndexedDB migration case',entity_refs:[],relation_refs:[]},
 provenance:{
  current_revision_id:'CEM.WORKSPACE.REV.idb-test',
  activities:[{
   id:'CEM.ACTIVITY.idb-test.create',type:'CREATE',timestamp:'2026-09-16T18:00:00Z',
   agent:{kind:'SOFTWARE',id:'CEM.WEB',version:'0.4.2a0'},used:[],
   generated:[{kind:'WORKSPACE_REVISION',id:'CEM.WORKSPACE.REV.idb-test'}]
  }]
 }
});

const validate=(document:WorkspaceDocument)=>{
 assert.equal(document.schema_version,'1');
 assert.match(document.workspace_id,/^CEM\.WORKSPACE\./);
};

test('R3 IndexedDB schema keeps storage version separate and reserves all adopted stores',()=>{
 assert.equal(CEM_STORAGE_DB_NAME,'cem-reality-loop');
 assert.equal(CEM_STORAGE_DB_VERSION,1);
 assert.deepEqual(Object.keys(CEM_STORAGE_STORES).sort(),[
  'import_originals','reality_loop_objects','storage_meta','workspace_documents','workspace_recovery'
 ]);
});

test('R3 legacy inspection is copy-first and preserves active/recovery/import raw values',()=>{
 const storage=new MemoryStorage();
 const active=workspace();
 const recovery={...workspace(),updated_at:'2026-09-16T17:55:00Z'};
 const activeRaw=JSON.stringify(active);
 const recoveryRaw=JSON.stringify(recovery);
 storage.setItem(WORKSPACE_ACTIVE_KEY,activeRaw);
 storage.setItem(WORKSPACE_RECOVERY_KEY,recoveryRaw);
 storage.setItem(WORKSPACE_IMPORT_ORIGINAL_KEY,'{"schema_version":"0","legacy":true}');

 const inspected=inspectLegacyWorkspaceStorage(storage,validate)!;
 assert.deepEqual(inspected.active,active);
 assert.deepEqual(inspected.recovery,recovery);
 assert.equal(inspected.active_raw,activeRaw);
 assert.equal(inspected.recovery_raw,recoveryRaw);
 assert.equal(inspected.import_original_raw,'{"schema_version":"0","legacy":true}');
 assert.equal(storage.getItem(WORKSPACE_ACTIVE_KEY),activeRaw);
 assert.equal(storage.getItem(WORKSPACE_RECOVERY_KEY),recoveryRaw);
});

test('R3 legacy inspection fails closed on corrupt active or recovery data',()=>{
 const storage=new MemoryStorage();
 storage.setItem(WORKSPACE_ACTIVE_KEY,'{broken');
 assert.throws(()=>inspectLegacyWorkspaceStorage(storage,validate),/invalid JSON/);

 storage.setItem(WORKSPACE_ACTIVE_KEY,JSON.stringify(workspace()));
 storage.setItem(WORKSPACE_RECOVERY_KEY,'{broken');
 assert.throws(()=>inspectLegacyWorkspaceStorage(storage,validate),/invalid JSON/);
});

test('R3 legacy inspection returns no migration candidate when no active workspace exists',()=>{
 const storage=new MemoryStorage();
 storage.setItem(WORKSPACE_RECOVERY_KEY,JSON.stringify(workspace()));
 assert.equal(inspectLegacyWorkspaceStorage(storage,validate),undefined);
});
