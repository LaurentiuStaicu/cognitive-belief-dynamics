import test from 'node:test';
import assert from 'node:assert/strict';
import {
 WORKSPACE_ACTIVE_KEY,
 WORKSPACE_RECOVERY_KEY,
 type StorageLike,
 type WorkspaceDocument
} from '../src/workspace-store.ts';
import {
 MAX_WORKSPACE_IMPORT_BYTES,
 MAX_WORKSPACE_IMPORT_DEPTH,
 MAX_WORKSPACE_IMPORT_NODES,
 WORKSPACE_IMPORT_ORIGINAL_KEY,
 InvalidWorkspaceShapeError,
 UnsupportedWorkspaceSchemaError,
 WorkspaceImportError,
 WorkspaceImportLimitError,
 importWorkspaceText,
 installWorkspaceImport,
 serializeWorkspace,
 workspaceFileName,
 type LegacyWorkspaceV0
} from '../src/workspace-portable.ts';

class MemoryStorage implements StorageLike{
 readonly values=new Map<string,string>();
 getItem(key:string){return this.values.get(key)??null;}
 setItem(key:string,value:string){this.values.set(key,value);}
 removeItem(key:string){this.values.delete(key);}
}

function current():WorkspaceDocument{
 return {
  schema_version:'1',
  workspace_id:'CEM.WORKSPACE.portable',
  created_at:'2026-09-16T10:00:00Z',
  updated_at:'2026-09-16T10:00:00Z',
  versions:{
   software_version:'0.4.2a0',release_tag:'v0.4.2a0',model_specification:'M1',
   evidence_snapshot:'EVIDENCE.M1.2026-09-16.r1',semantic_schema_version:'1',
   semantic_baseline_contract:'OA0.BASELINE.2026-09-16'
  },
  case:{
   id:'CEM.CASE.portable',title:'Portable case',notes:'keep me',
   entity_refs:['VAR.FAMILIARITY.CLAIM'],relation_refs:['LINK.EXPOSURE.FAMILIARITY'],
   focus:{entity_id:'VAR.FAMILIARITY.CLAIM'}
  },
  provenance:{
   current_revision_id:'CEM.WORKSPACE.REV.portable-r0',
   activities:[{
    id:'CEM.ACTIVITY.portable.create',type:'CREATE',timestamp:'2026-09-16T10:00:00Z',
    agent:{kind:'SOFTWARE',id:'CEM.WEB',version:'0.4.2a0'},
    used:[{kind:'SEMANTIC_ENTITY',id:'VAR.FAMILIARITY.CLAIM'}],
    generated:[{kind:'WORKSPACE_REVISION',id:'CEM.WORKSPACE.REV.portable-r0'}]
   }]
  }
 };
}

function legacy():LegacyWorkspaceV0{
 const doc=current();
 return {
  schema_version:'0',workspace_id:doc.workspace_id,created_at:doc.created_at,updated_at:doc.updated_at,
  software_version:doc.versions.software_version,release_tag:doc.versions.release_tag,
  model_specification:doc.versions.model_specification,evidence_snapshot:doc.versions.evidence_snapshot,
  semantic_schema_version:doc.versions.semantic_schema_version,
  semantic_baseline_contract:doc.versions.semantic_baseline_contract,
  case:doc.case
 };
}

function options(){
 let tick=0;
 return {
  now:()=>`2026-09-16T11:${String(++tick).padStart(2,'0')}:00Z`,
  id:()=>`portable-${tick}`,
  validate:(document:WorkspaceDocument)=>{
   assert.equal(document.schema_version,'1');
   const generated=new Set(document.provenance.activities.flatMap(a=>a.generated.filter(r=>r.kind==='WORKSPACE_REVISION').map(r=>r.id)));
   assert(generated.has(document.provenance.current_revision_id));
  }
 };
}

test('export uses stable pretty JSON and .cem.json filename',()=>{
 const doc=current();
 const text=serializeWorkspace(doc);
 assert.equal(text,JSON.stringify(doc,null,2)+'\n');
 assert.equal(workspaceFileName(doc),'portable.cem.json');
});

test('v1 import preserves the exact original text and object while adding IMPORT provenance to a clone',()=>{
 const source=current();
 const text=serializeWorkspace(source);
 const sourceBefore=structuredClone(source);
 const result=importWorkspaceText(text,options());
 assert.equal(result.original_text,text);
 assert.deepEqual(result.original,sourceBefore);
 assert.deepEqual(source,sourceBefore);
 assert.equal(result.migrated_from,undefined);
 assert.equal(result.document.case.title,source.case.title);
 assert.deepEqual(result.document.case.entity_refs,source.case.entity_refs);
 assert.equal(result.document.provenance.activities.at(-1)?.type,'IMPORT');
 assert.notEqual(result.document.provenance.current_revision_id,source.provenance.current_revision_id);
});

test('v0 migration preserves case semantics and records MIGRATE then IMPORT',()=>{
 const source=legacy();
 const before=structuredClone(source);
 const text=JSON.stringify(source);
 const result=importWorkspaceText(text,options());
 assert.deepEqual(source,before);
 assert.equal(result.migrated_from,'0');
 assert.equal(result.document.schema_version,'1');
 assert.equal(result.document.workspace_id,source.workspace_id);
 assert.deepEqual(result.document.case,source.case);
 assert.equal(result.document.versions.software_version,source.software_version);
 assert.equal(result.document.versions.model_specification,source.model_specification);
 assert.equal(result.document.versions.evidence_snapshot,source.evidence_snapshot);
 assert.deepEqual(result.document.provenance.activities.slice(-2).map(a=>a.type),['MIGRATE','IMPORT']);
});

test('install archives exact original text and keeps prior active document as recovery',()=>{
 const storage=new MemoryStorage();
 storage.setItem(WORKSPACE_ACTIVE_KEY,'{"previous":true}');
 const text=serializeWorkspace(current());
 const result=importWorkspaceText(text,options());
 installWorkspaceImport(storage,result);
 assert.equal(storage.getItem(WORKSPACE_IMPORT_ORIGINAL_KEY),text);
 assert.equal(storage.getItem(WORKSPACE_RECOVERY_KEY),'{"previous":true}');
 assert.deepEqual(JSON.parse(storage.getItem(WORKSPACE_ACTIVE_KEY)!),result.document);
});

test('unknown future schema fails closed and storage remains untouched',()=>{
 const storage=new MemoryStorage();
 storage.setItem(WORKSPACE_ACTIVE_KEY,'sentinel');
 const future=JSON.stringify({...current(),schema_version:'2'});
 assert.throws(()=>importWorkspaceText(future,options()),UnsupportedWorkspaceSchemaError);
 assert.equal(storage.getItem(WORKSPACE_ACTIVE_KEY),'sentinel');
 assert.equal(storage.getItem(WORKSPACE_IMPORT_ORIGINAL_KEY),null);
});

test('corrupt JSON fails closed',()=>{
 assert.throws(()=>importWorkspaceText('{broken',options()),WorkspaceImportError);
});

test('oversized text is rejected before parse or install',()=>{
 const text=`{"padding":"${'x'.repeat(MAX_WORKSPACE_IMPORT_BYTES)}"}`;
 assert.throws(()=>importWorkspaceText(text,options()),WorkspaceImportLimitError);
});

test('top-level primitive and array inputs are rejected before schema migration',()=>{
 assert.throws(()=>importWorkspaceText('null',options()),InvalidWorkspaceShapeError);
 assert.throws(()=>importWorkspaceText('[]',options()),InvalidWorkspaceShapeError);
});

test('excessive nesting is rejected before clone and provenance work',()=>{
 let nested:unknown='leaf';
 for(let i=0;i<MAX_WORKSPACE_IMPORT_DEPTH+1;i++)nested={child:nested};
 const text=JSON.stringify({schema_version:'1',nested});
 assert.throws(()=>importWorkspaceText(text,options()),WorkspaceImportLimitError);
});

test('excessive node count is rejected before validation',()=>{
 const text=JSON.stringify({schema_version:'1',items:Array.from({length:MAX_WORKSPACE_IMPORT_NODES},()=>0)});
 assert.throws(()=>importWorkspaceText(text,options()),WorkspaceImportLimitError);
});
