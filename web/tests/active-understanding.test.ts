import test from 'node:test';
import assert from 'node:assert/strict';
import {
 ACTIVE_HISTORY_MAX_RECORDS,
 LearningHistoryStore,
 createActiveSession,
 reduceActiveSession,
 type StorageLike
} from '../src/active-understanding.ts';

class MemoryStorage implements StorageLike{
 private data=new Map<string,string>();
 getItem(key:string){return this.data.get(key)??null;}
 setItem(key:string,value:string){this.data.set(key,value);}
 removeItem(key:string){this.data.delete(key);}
}

test('OA-5A state machine requires predict before reveal but permits an explicit skip',()=>{
 let state=createActiveSession('AU-1','INCREASE');
 assert.equal(state.stage,'WORKED_EXAMPLE');
 state=reduceActiveSession(state,{type:'START_PREDICTION'});
 assert.equal(state.stage,'PREDICT');
 state=reduceActiveSession(state,{type:'SKIP_PREDICTION'});
 assert.equal(state.stage,'REVEAL');
 assert.equal(state.predictionCategory,undefined);
});

test('submitted prediction records outcome and optional learner confidence without changing the target result',()=>{
 let state=createActiveSession('AU-2','ACCURACY_SALIENCE');
 state=reduceActiveSession(state,{type:'START_PREDICTION'});
 state=reduceActiveSession(state,{
  type:'SUBMIT_PREDICTION',
  predictionCategory:'ACCURACY_SALIENCE',
  confidence:'medium'
 });
 assert.equal(state.stage,'REVEAL');
 assert.equal(state.outcome,'correct');
 assert.equal(state.confidence,'medium');
 assert.equal(state.predictionCategory,'ACCURACY_SALIENCE');
});

test('reveal must precede explanation, boundary and completion',()=>{
 let state=createActiveSession('AU-3','COMPUTATIONAL_DEPENDENCY');
 state=reduceActiveSession(state,{type:'START_PREDICTION'});
 state=reduceActiveSession(state,{
  type:'SUBMIT_PREDICTION',
  predictionCategory:'REGISTERED_EVIDENCE_RELATION'
 });
 assert.equal(state.outcome,'incorrect');
 state=reduceActiveSession(state,{type:'SHOW_EXPLANATION'});
 assert.equal(state.stage,'EXPLAIN');
 state=reduceActiveSession(state,{type:'SHOW_BOUNDARY'});
 assert.equal(state.stage,'BOUNDARY');
 state=reduceActiveSession(state,{type:'COMPLETE'});
 assert.equal(state.stage,'COMPLETE');
});

test('illegal state transitions fail closed',()=>{
 const state=createActiveSession('AU-1','INCREASE');
 assert.throws(()=>reduceActiveSession(state,{type:'SHOW_EXPLANATION'}));
 assert.throws(()=>reduceActiveSession(state,{
  type:'SUBMIT_PREDICTION',
  predictionCategory:'INCREASE'
 }));
});

test('learning history is local, bounded and clearable',()=>{
 const storage=new MemoryStorage();
 let tick=0;
 const store=new LearningHistoryStore(storage,{maxRecords:3,now:()=>`2026-09-16T13:00:0${tick++}Z`});
 for(let i=0;i<5;i++){
  store.record({
   challenge_id:'AU-1',
   canonical_target_refs:['VAR.FAMILIARITY.CLAIM'],
   prediction_category:i%2===0?'INCREASE':'UNCHANGED',
   outcome_category:i%2===0?'correct':'incorrect'
  });
 }
 const records=store.all();
 assert.equal(records.length,3);
 assert.equal(records[0].prediction_category,'INCREASE');
 assert.equal(records[2].prediction_category,'INCREASE');
 store.clear();
 assert.deepEqual(store.all(),[]);
 assert.equal(ACTIVE_HISTORY_MAX_RECORDS,100);
});

test('corrupt or future history fails closed to an empty local history',()=>{
 const storage=new MemoryStorage();
 storage.setItem('cem.active-understanding.history.v1','{"schema_version":"2","records":[{"free_text":"not allowed"}]}');
 const store=new LearningHistoryStore(storage);
 assert.deepEqual(store.all(),[]);
});
