import type {
 StorageLike,
 WorkspaceActivity,
 WorkspaceDocument,
 WorkspaceRef,
 WorkspaceVersions
} from './workspace-store';

const WORKSPACE_ACTIVE_KEY='cem.workspace.v1.active';
const WORKSPACE_RECOVERY_KEY='cem.workspace.v1.recovery';
export const WORKSPACE_IMPORT_ORIGINAL_KEY='cem.workspace.v1.import.original';

export class WorkspaceImportError extends Error{}
export class UnsupportedWorkspaceSchemaError extends WorkspaceImportError{}

export type LegacyWorkspaceV0={
 schema_version:'0';
 workspace_id:string;
 created_at:string;
 updated_at:string;
 software_version:string;
 release_tag?:string;
 model_specification:string;
 evidence_snapshot:string;
 semantic_schema_version:string;
 semantic_baseline_contract:string;
 case:WorkspaceDocument['case'];
};

type ImportOptions={
 now?:()=>string;
 id?:()=>string;
 validate:(document:WorkspaceDocument)=>void;
};

export type WorkspaceImportResult={
 original_text:string;
 original:unknown;
 document:WorkspaceDocument;
 migrated_from?:'0';
};

const clone=<T>(value:T):T=>JSON.parse(JSON.stringify(value)) as T;
const nowDefault=()=>new Date().toISOString();
const idDefault=()=>crypto.randomUUID();

function refs(document:WorkspaceDocument):WorkspaceRef[]{
 return [
  ...document.case.entity_refs.map(id=>({kind:'SEMANTIC_ENTITY' as const,id})),
  ...document.case.relation_refs.map(id=>({kind:'SEMANTIC_RELATION' as const,id})),
  {kind:'EVIDENCE_SNAPSHOT',id:document.versions.evidence_snapshot},
  {kind:'MODEL_SPECIFICATION',id:document.versions.model_specification},
  {kind:'SOFTWARE_VERSION',id:document.versions.software_version}
 ];
}

function appendActivity(
 source:WorkspaceDocument,
 type:'MIGRATE'|'IMPORT',
 now:()=>string,
 id:()=>string
):WorkspaceDocument{
 const timestamp=now();
 const token=id();
 const revisionId=`CEM.WORKSPACE.REV.${token}`;
 const activity:WorkspaceActivity={
  id:`CEM.ACTIVITY.${token}.${type.toLowerCase()}`,
  type,
  timestamp,
  agent:{kind:'SOFTWARE',id:type==='MIGRATE'?'CEM.MIGRATION':'CEM.IMPORT',version:source.versions.software_version},
  used:[
   {kind:'WORKSPACE_REVISION',id:source.provenance.current_revision_id},
   ...refs(source)
  ],
  generated:[{kind:'WORKSPACE_REVISION',id:revisionId}],
  revision_of:source.provenance.current_revision_id
 };
 return {
  ...clone(source),
  updated_at:timestamp,
  provenance:{
   current_revision_id:revisionId,
   activities:[...clone(source.provenance.activities),activity]
  }
 };
}

function migrateV0(source:LegacyWorkspaceV0,now:()=>string,id:()=>string):WorkspaceDocument{
 const token=id();
 const initialRevision=`CEM.WORKSPACE.REV.${token}.legacy`;
 const versions:WorkspaceVersions={
  software_version:source.software_version,
  ...(source.release_tag?{release_tag:source.release_tag}:{}),
  model_specification:source.model_specification,
  evidence_snapshot:source.evidence_snapshot,
  semantic_schema_version:source.semantic_schema_version,
  semantic_baseline_contract:source.semantic_baseline_contract
 };
 const base:WorkspaceDocument={
  schema_version:'1',
  workspace_id:source.workspace_id,
  created_at:source.created_at,
  updated_at:source.updated_at,
  versions,
  case:clone(source.case),
  provenance:{
   current_revision_id:initialRevision,
   activities:[{
    id:`CEM.ACTIVITY.${token}.legacy`,
    type:'CREATE',
    timestamp:source.created_at,
    agent:{kind:'SYSTEM',id:'CEM.LEGACY.V0',version:source.software_version},
    used:refs({
     schema_version:'1',workspace_id:source.workspace_id,created_at:source.created_at,
     updated_at:source.updated_at,versions,case:clone(source.case),
     provenance:{current_revision_id:initialRevision,activities:[]}
    }),
    generated:[{kind:'WORKSPACE_REVISION',id:initialRevision}]
   }]
  }
 };
 return appendActivity(base,'MIGRATE',now,id);
}

export function workspaceFileName(document:WorkspaceDocument):string{
 const stem=document.case.id.replace(/^CEM\.CASE\./,'')||'workspace';
 return `${stem}.cem.json`;
}

export function serializeWorkspace(document:WorkspaceDocument):string{
 return JSON.stringify(document,null,2)+'\n';
}

export function importWorkspaceText(text:string,options:ImportOptions):WorkspaceImportResult{
 const now=options.now??nowDefault;
 const id=options.id??idDefault;
 let parsed:unknown;
 try{parsed=JSON.parse(text);}catch(error){throw new WorkspaceImportError(`invalid workspace JSON: ${String(error)}`);}
 const original=clone(parsed);
 const version=(parsed as {schema_version?:unknown})?.schema_version;
 let document:WorkspaceDocument;
 let migrated_from:WorkspaceImportResult['migrated_from'];
 if(version==='1'){
  document=clone(parsed as WorkspaceDocument);
 }else if(version==='0'){
  document=migrateV0(clone(parsed as LegacyWorkspaceV0),now,id);
  migrated_from='0';
 }else{
  throw new UnsupportedWorkspaceSchemaError(`unsupported workspace schema: ${String(version)}`);
 }
 options.validate(document);
 document=appendActivity(document,'IMPORT',now,id);
 options.validate(document);
 return {original_text:text,original,document,...(migrated_from?{migrated_from}:{})};
}

export function installWorkspaceImport(storage:StorageLike,result:WorkspaceImportResult):void{
 const active=storage.getItem(WORKSPACE_ACTIVE_KEY);
 if(active!==null)storage.setItem(WORKSPACE_RECOVERY_KEY,active);
 storage.setItem(WORKSPACE_IMPORT_ORIGINAL_KEY,result.original_text);
 storage.setItem(WORKSPACE_ACTIVE_KEY,JSON.stringify(result.document));
}

export function downloadWorkspace(document:WorkspaceDocument):void{
 const blob=new Blob([serializeWorkspace(document)],{type:'application/json'});
 const url=URL.createObjectURL(blob);
 const anchor=documentGlobal().createElement('a');
 anchor.href=url;
 anchor.download=workspaceFileName(document);
 anchor.click();
 setTimeout(()=>URL.revokeObjectURL(url),1000);
}

export async function readWorkspaceFile(file:File):Promise<string>{return file.text();}

function documentGlobal():Document{return globalThis.document;}
