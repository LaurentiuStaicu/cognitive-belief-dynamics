import test from 'node:test';
import assert from 'node:assert/strict';
import {collectLocalDiagnostics,serializeLocalDiagnostics} from '../src/local-diagnostics.ts';

const input={
 software_version:'0.4.2a0',release_tag:'v0.4.2a0',model_specification:'M1',
 evidence_snapshot:'EVIDENCE.M1.2026-09-16.r1',evidence_as_of:'2026-09-16',
 online:true,local_storage_available:true,indexed_db_available:true,service_worker_controlled:false
};

test('local diagnostics contains only the declared non-personal trust fields',()=>{
 const record=collectLocalDiagnostics(input,()=> '2026-09-17T07:00:00.000Z');
 assert.deepEqual(Object.keys(record).sort(),['generated_at','schema_version','scope','software','evidence','runtime','telemetry'].sort());
 assert.equal(record.scope,'LOCAL_RUNTIME_ONLY');
 assert.equal(record.telemetry,'NONE');
 assert.deepEqual(record.software,{version:'0.4.2a0',release_tag:'v0.4.2a0',model_specification:'M1'});
 assert.deepEqual(record.evidence,{snapshot:'EVIDENCE.M1.2026-09-16.r1',as_of:'2026-09-16'});
 assert.deepEqual(record.runtime,{network:'ONLINE',local_storage:'AVAILABLE',indexed_db:'AVAILABLE',service_worker:'NOT_CONTROLLED'});
 const text=serializeLocalDiagnostics(record);
 for(const forbidden of ['userAgent','location','workspace','case','notes','query','history','email','ip_address']){
  assert.equal(text.includes(forbidden),false,`diagnostics must not contain ${forbidden}`);
 }
});

test('offline and unavailable capabilities are represented without error or upload semantics',()=>{
 const record=collectLocalDiagnostics({...input,online:false,local_storage_available:false,indexed_db_available:false},()=> '2026-09-17T07:00:00.000Z');
 assert.equal(record.runtime.network,'OFFLINE');
 assert.equal(record.runtime.local_storage,'UNAVAILABLE');
 assert.equal(record.runtime.indexed_db,'UNAVAILABLE');
 assert.equal(record.telemetry,'NONE');
});
