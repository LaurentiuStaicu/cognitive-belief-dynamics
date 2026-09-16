export const WORKSPACE_SCHEMA_VERSION='1';
export const WORKSPACE_ACTIVE_KEY='cem.workspace.v1.active';
export const WORKSPACE_RECOVERY_KEY='cem.workspace.v1.recovery';

export type WorkspaceActivityType='CREATE'|'SAVE'|'AUTOSAVE'|'IMPORT'|'EXPORT'|'MIGRATE'|'RECOVER'|'UNDO'|'REDO';
export type WorkspaceRefKind='SEMANTIC_ENTITY'|'SEMANTIC_RELATION'|'WORKSPACE_REVISION'|'EVIDENCE_SNAPSHOT'|'MODEL_SPECIFICATION'|'SOFTWARE_VERSION';

export type WorkspaceVersions={
 software_version:string;
 release_tag?:string;
 model_specification:string;
 evidence_snapshot:string;
 semantic_schema_version:string;
 semantic_baseline_contract:string;
};

export type WorkspaceCase={
 id:string;
 title:string;
 notes?:string;
 entity_refs:string[];
 relation_refs:string[];
 focus?:{entity_id?:string;relation_id?:string};
};

export type WorkspaceRef={kind:WorkspaceRefKind;id:string};
export type WorkspaceActivity={
 id:string;
 type:WorkspaceActivityType;
 timestamp:string;
 agent:{kind:'SOFTWARE'|'USER_ACTION'|'SYSTEM';id:string;version?:string};
 used:WorkspaceRef[];
 generated:WorkspaceRef[];
 revision_of?:string;
};

export type WorkspaceDocument={
 schema_version:'1';
 workspace_id:string;
 created_at:string;
 updated_at:string;
 versions:WorkspaceVersions;
 case:WorkspaceCase;
 provenance:{current_revision_id:string;activities:WorkspaceActivity[]};
};

export type WorkspaceSeed={
 versions:WorkspaceVersions;
 title:string;
 notes?:string;
 entity_refs?:string[];
 relation_refs?:string[];
 focus?:WorkspaceCase['focus'];
};

export type StorageLike={
 getItem(key:string):string|null;
 setItem(key:string,value:string):void;
 removeItem(key:string):void;
};

type StoreOptions={
 now?:()=>string;
 id?:()=>string;
 validate?:(document:WorkspaceDocument)=>void;
};

const clone=<T>(value:T):T=>JSON.parse(JSON.stringify(value)) as T;
const defaultId=()=>crypto.randomUUID();
const defaultNow=()=>new Date().toISOString();

function canonicalRefs(document:WorkspaceDocument):WorkspaceRef[]{
 const refs:WorkspaceRef[]=[
  ...document.case.entity_refs.map(id=>({kind:'SEMANTIC_ENTITY' as const,id})),
  ...document.case.relation_refs.map(id=>({kind:'SEMANTIC_RELATION' as const,id})),
  {kind:'EVIDENCE_SNAPSHOT',id:document.versions.evidence_snapshot},
  {kind:'MODEL_SPECIFICATION',id:document.versions.model_specification},
  {kind:'SOFTWARE_VERSION',id:document.versions.software_version}
 ];
 return refs;
}

export class WorkspaceStore {
 private document?:WorkspaceDocument;
 private undoStack:WorkspaceCase[]=[];
 private redoStack:WorkspaceCase[]=[];
 private readonly now:()=>string;
 private readonly id:()=>string;
 private readonly validate:(document:WorkspaceDocument)=>void;

 constructor(private readonly storage:StorageLike,options:StoreOptions={}){
  this.now=options.now??defaultNow;
  this.id=options.id??defaultId;
  this.validate=options.validate??(()=>{});
 }

 current():WorkspaceDocument{
  if(!this.document)throw new Error('workspace not initialized');
  return clone(this.document);
 }

 canUndo():boolean{return this.undoStack.length>0;}
 canRedo():boolean{return this.redoStack.length>0;}

 loadOrCreate(seed:WorkspaceSeed):WorkspaceDocument{
  const activeRaw=this.storage.getItem(WORKSPACE_ACTIVE_KEY);
  const active=this.parseValid(activeRaw);
  if(active){
   this.document=active;
   this.undoStack=[];
   this.redoStack=[];
   return this.current();
  }

  const recovery=this.parseValid(this.storage.getItem(WORKSPACE_RECOVERY_KEY));
  if(recovery){
   this.document=this.recoveredDocument(recovery);
   this.undoStack=[];
   this.redoStack=[];
   this.persist(false);
   return this.current();
  }

  this.document=this.create(seed);
  this.undoStack=[];
  this.redoStack=[];
  this.persist(false);
  return this.current();
 }

 autosave(nextCase:WorkspaceCase):WorkspaceDocument{
  this.requireDocument();
  this.undoStack.push(clone(this.document!.case));
  this.redoStack=[];
  return this.commitCase(nextCase,'AUTOSAVE');
 }

 save():WorkspaceDocument{
  this.requireDocument();
  return this.commitCase(this.document!.case,'SAVE');
 }

 undo():WorkspaceDocument|undefined{
  this.requireDocument();
  const previous=this.undoStack.pop();
  if(!previous)return undefined;
  this.redoStack.push(clone(this.document!.case));
  return this.commitCase(previous,'UNDO');
 }

 redo():WorkspaceDocument|undefined{
  this.requireDocument();
  const next=this.redoStack.pop();
  if(!next)return undefined;
  this.undoStack.push(clone(this.document!.case));
  return this.commitCase(next,'REDO');
 }

 recover():WorkspaceDocument|undefined{
  const recovery=this.parseValid(this.storage.getItem(WORKSPACE_RECOVERY_KEY));
  if(!recovery)return undefined;
  this.document=this.recoveredDocument(recovery);
  this.undoStack=[];
  this.redoStack=[];
  this.persist(false);
  return this.current();
 }

 clear():void{
  this.document=undefined;
  this.undoStack=[];
  this.redoStack=[];
  this.storage.removeItem(WORKSPACE_ACTIVE_KEY);
  this.storage.removeItem(WORKSPACE_RECOVERY_KEY);
 }

 private requireDocument():void{
  if(!this.document)throw new Error('workspace not initialized');
 }

 private create(seed:WorkspaceSeed):WorkspaceDocument{
  const timestamp=this.now();
  const token=this.id();
  const revisionId=`CEM.WORKSPACE.REV.${token}`;
  const document:WorkspaceDocument={
   schema_version:'1',
   workspace_id:`CEM.WORKSPACE.${token}`,
   created_at:timestamp,
   updated_at:timestamp,
   versions:clone(seed.versions),
   case:{
    id:`CEM.CASE.${token}`,
    title:seed.title,
    ...(seed.notes!==undefined?{notes:seed.notes}:{}),
    entity_refs:[...(seed.entity_refs??[])],
    relation_refs:[...(seed.relation_refs??[])],
    ...(seed.focus?{focus:clone(seed.focus)}:{})
   },
   provenance:{current_revision_id:revisionId,activities:[]}
  };
  document.provenance.activities.push({
   id:`CEM.ACTIVITY.${token}.create`,
   type:'CREATE',
   timestamp,
   agent:{kind:'SOFTWARE',id:'CEM.WEB',version:document.versions.software_version},
   used:canonicalRefs(document),
   generated:[{kind:'WORKSPACE_REVISION',id:revisionId}]
  });
  this.validate(document);
  return document;
 }

 private commitCase(nextCase:WorkspaceCase,type:WorkspaceActivityType):WorkspaceDocument{
  const previous=this.current();
  const token=this.id();
  const timestamp=this.now();
  const revisionId=`CEM.WORKSPACE.REV.${token}`;
  const document:WorkspaceDocument={
   ...previous,
   updated_at:timestamp,
   case:clone(nextCase),
   provenance:{
    current_revision_id:revisionId,
    activities:[
     ...previous.provenance.activities,
     {
      id:`CEM.ACTIVITY.${token}.${type.toLowerCase()}`,
      type,
      timestamp,
      agent:{kind:type==='AUTOSAVE'?'SYSTEM':'USER_ACTION',id:type==='AUTOSAVE'?'CEM.AUTOSAVE':'CEM.WEB',version:previous.versions.software_version},
      used:[
       {kind:'WORKSPACE_REVISION',id:previous.provenance.current_revision_id},
       ...canonicalRefs({...previous,case:clone(nextCase)})
      ],
      generated:[{kind:'WORKSPACE_REVISION',id:revisionId}],
      revision_of:previous.provenance.current_revision_id
     }
    ]
   }
  };
  this.validate(document);
  this.document=document;
  this.persist(true);
  return this.current();
 }

 private recoveredDocument(source:WorkspaceDocument):WorkspaceDocument{
  const token=this.id();
  const timestamp=this.now();
  const revisionId=`CEM.WORKSPACE.REV.${token}`;
  const recovered:WorkspaceDocument={
   ...clone(source),
   updated_at:timestamp,
   provenance:{
    current_revision_id:revisionId,
    activities:[
     ...source.provenance.activities,
     {
      id:`CEM.ACTIVITY.${token}.recover`,
      type:'RECOVER',
      timestamp,
      agent:{kind:'SYSTEM',id:'CEM.RECOVERY',version:source.versions.software_version},
      used:[
       {kind:'WORKSPACE_REVISION',id:source.provenance.current_revision_id},
       ...canonicalRefs(source)
      ],
      generated:[{kind:'WORKSPACE_REVISION',id:revisionId}],
      revision_of:source.provenance.current_revision_id
     }
    ]
   }
  };
  this.validate(recovered);
  return recovered;
 }

 private parseValid(raw:string|null):WorkspaceDocument|undefined{
  if(!raw)return undefined;
  try{
   const parsed=JSON.parse(raw) as WorkspaceDocument;
   if(parsed?.schema_version!==WORKSPACE_SCHEMA_VERSION)return undefined;
   this.validate(parsed);
   return parsed;
  }catch{return undefined;}
 }

 private persist(updateRecovery:boolean):void{
  this.requireDocument();
  this.validate(this.document!);
  if(updateRecovery){
   const existing=this.parseValid(this.storage.getItem(WORKSPACE_ACTIVE_KEY));
   if(existing)this.storage.setItem(WORKSPACE_RECOVERY_KEY,JSON.stringify(existing));
  }
  this.storage.setItem(WORKSPACE_ACTIVE_KEY,JSON.stringify(this.document));
 }
}
