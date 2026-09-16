import test from 'node:test';
import assert from 'node:assert/strict';
import {
 WORKSPACE_ACTIVE_KEY,
 WORKSPACE_RECOVERY_KEY,
 WorkspaceStore,
 type StorageLike,
 type WorkspaceCase,
 type WorkspaceDocument,
 type WorkspaceSeed
} from '../src/workspace-store.ts';

class MemoryStorage implements StorageLike{
 readonly values=new Map<string,string>();
 getItem(key:string){return this.values.get(key)??null;}
 setItem(key:string,value:string){this.values.set(key,value);}
 removeItem(key:string){this.values.delete(key);}
}

function harness(){
 const storage=new MemoryStorage();
 let tick=0;
 const ids=()=>`test-${++tick}`;
 const now=()=>`2026-09-16T11:${String(tick).padStart(2,'0')}:00Z`;
 const validate=(document:WorkspaceDocument)=>{
  assert.equal(document.schema_version,'1');
  assert(document.provenance.activities.some(activity=>
   activity.generated.some(ref=>ref.kind==='WORKSPACE_REVISION'&&ref.id===document.provenance.current_revision_id)
  ));
 };
 const seed:WorkspaceSeed={
  title:'Initial case',
  versions:{
   software_version:'0.4.2a0',
   release_tag:'v0.4.2a0',
   model_specification:'M1',
   evidence_snapshot:'EVIDENCE.M1.2026-09-16.r1',
   semantic_schema_version:'1',
   semantic_baseline_contract:'OA0.BASELINE.2026-09-16'
  },
  entity_refs:['VAR.FAMILIARITY.CLAIM'],
  relation_refs:['LINK.EXPOSURE.FAMILIARITY']
 };
 return {storage,ids,now,validate,seed};
}

const renamed=(document:WorkspaceDocument,title:string):WorkspaceCase=>({...document.case,title});

test('save close load preserves the exact active workspace document',()=>{
 const h=harness();
 const first=new WorkspaceStore(h.storage,{id:h.ids,now:h.now,validate:h.validate});
 const created=first.loadOrCreate(h.seed);
 first.autosave(renamed(created,'Saved case'));
 const raw=h.storage.getItem(WORKSPACE_ACTIVE_KEY);
 assert(raw);

 const second=new WorkspaceStore(h.storage,{id:h.ids,now:h.now,validate:h.validate});
 const loaded=second.loadOrCreate(h.seed);
 assert.deepEqual(loaded,JSON.parse(raw!));
 assert.equal(h.storage.getItem(WORKSPACE_ACTIVE_KEY),raw);
});

test('autosave keeps the previous valid document as a recovery snapshot',()=>{
 const h=harness();
 const store=new WorkspaceStore(h.storage,{id:h.ids,now:h.now,validate:h.validate});
 const initial=store.loadOrCreate(h.seed);
 store.autosave(renamed(initial,'Autosaved case'));

 const recovery=JSON.parse(h.storage.getItem(WORKSPACE_RECOVERY_KEY)!);
 assert.equal(recovery.case.title,'Initial case');
 assert.equal(store.current().case.title,'Autosaved case');
 assert.equal(store.current().provenance.activities.at(-1)?.type,'AUTOSAVE');
});

test('undo and redo restore case snapshots while generating new revisions',()=>{
 const h=harness();
 const store=new WorkspaceStore(h.storage,{id:h.ids,now:h.now,validate:h.validate});
 const initial=store.loadOrCreate(h.seed);
 const first=store.autosave(renamed(initial,'First edit'));
 store.autosave(renamed(first,'Second edit'));

 assert.equal(store.undo()?.case.title,'First edit');
 assert.equal(store.current().provenance.activities.at(-1)?.type,'UNDO');
 assert.equal(store.redo()?.case.title,'Second edit');
 assert.equal(store.current().provenance.activities.at(-1)?.type,'REDO');
});

test('a corrupted active snapshot recovers from the last valid recovery document',()=>{
 const h=harness();
 const first=new WorkspaceStore(h.storage,{id:h.ids,now:h.now,validate:h.validate});
 const initial=first.loadOrCreate(h.seed);
 first.autosave(renamed(initial,'New edit'));
 h.storage.setItem(WORKSPACE_ACTIVE_KEY,'{corrupt');

 const second=new WorkspaceStore(h.storage,{id:h.ids,now:h.now,validate:h.validate});
 const recovered=second.loadOrCreate(h.seed);
 assert.equal(recovered.case.title,'Initial case');
 assert.equal(recovered.provenance.activities.at(-1)?.type,'RECOVER');
 assert.doesNotThrow(()=>JSON.parse(h.storage.getItem(WORKSPACE_ACTIVE_KEY)!));
});

test('explicit recovery never promotes a corrupted recovery snapshot',()=>{
 const h=harness();
 const store=new WorkspaceStore(h.storage,{id:h.ids,now:h.now,validate:h.validate});
 store.loadOrCreate(h.seed);
 h.storage.setItem(WORKSPACE_RECOVERY_KEY,'not-json');
 assert.equal(store.recover(),undefined);
});
