import test from 'node:test';
import assert from 'node:assert/strict';
import {ReassessmentStore,type StorageLike} from '../src/adaptive-reassessment.ts';

class MemoryStorage implements StorageLike{
 data=new Map<string,string>();
 getItem(key:string){return this.data.get(key)??null;}
 setItem(key:string,value:string){this.data.set(key,value);}
 removeItem(key:string){this.data.delete(key);}
}

const input={
 uncertainty_id:'UNC.PLANNER.RESPONSE.PROFILES',
 signpost_kind:'METRIC' as const,
 indicator:'Observed correction-access estimate',
 trigger_condition:'Outside the current declared sensitivity range',
 response_action:'Re-run robustness comparison',
 basis:'EMPIRICAL' as const,
 rationale:'Could change the top bundle',
 source_note:'Future study',
 earliest_reassessment:'after step 4',
 latest_reassessment:'before step 8'
};

test('OA-6D stores reassessment triggers locally with explicit provenance fields',()=>{
 const storage=new MemoryStorage();
 const store=new ReassessmentStore(storage,{now:()=> '2026-09-16T16:00:00Z',idFactory:()=> 'trigger-1'});
 const saved=store.add(input);
 assert.equal(saved.id,'trigger-1');
 assert.equal(saved.created_at,'2026-09-16T16:00:00Z');
 assert.deepEqual(store.all(),[saved]);
 store.remove('trigger-1');
 assert.deepEqual(store.all(),[]);
});

test('OA-6D caps local records and can clear them without touching model data',()=>{
 const storage=new MemoryStorage();
 let id=0;
 const store=new ReassessmentStore(storage,{maxRecords:2,idFactory:()=>`trigger-${++id}`,now:()=> '2026-09-16T16:00:00Z'});
 store.add({...input,indicator:'one'});store.add({...input,indicator:'two'});store.add({...input,indicator:'three'});
 assert.deepEqual(store.all().map(item=>item.indicator),['two','three']);
 store.clear();
 assert.deepEqual(store.all(),[]);
});

test('OA-6D fails closed on corrupt or future local documents',()=>{
 const storage=new MemoryStorage();
 storage.setItem('cem.decision-reassessment.v1','not-json');
 assert.deepEqual(new ReassessmentStore(storage).all(),[]);
 storage.setItem('cem.decision-reassessment.v1',JSON.stringify({schema_version:'2',records:[]}));
 assert.deepEqual(new ReassessmentStore(storage).all(),[]);
});

test('OA-6D rejects incomplete trigger records',()=>{
 const storage=new MemoryStorage();
 const store=new ReassessmentStore(storage,{idFactory:()=> 'x',now:()=> '2026-09-16T16:00:00Z'});
 assert.throws(()=>store.add({...input,indicator:''}),/invalid reassessment record/);
});
