import {
 WORKSPACE_ACTIVE_KEY,
 WORKSPACE_RECOVERY_KEY,
 type StorageLike,
 type WorkspaceDocument
} from './workspace-store';
import {WORKSPACE_IMPORT_ORIGINAL_KEY} from './workspace-portable';

export const CEM_STORAGE_DB_NAME='cem-reality-loop';
export const CEM_STORAGE_DB_VERSION=1;
export const CEM_STORAGE_STORES={
 workspace_documents:'workspace_documents',
 reality_loop_objects:'reality_loop_objects',
 workspace_recovery:'workspace_recovery',
 import_originals:'import_originals',
 storage_meta:'storage_meta'
} as const;
export const LEGACY_MIGRATION_META_KEY='legacy_workspace_v1_migration';

export type LegacyWorkspaceSnapshot={
 active_raw:string;
 active:WorkspaceDocument;
 recovery_raw?:string;
 recovery?:WorkspaceDocument;
 import_original_raw?:string;
};

export type LegacyMigrationStatus='MIGRATED'|'REFRESHED'|'NO_ACTIVE_WORKSPACE';

export type LegacyMigrationResult={
 status:LegacyMigrationStatus;
 workspace_id?:string;
 legacy_keys_preserved:true;
 database_name:string;
 database_version:number;
};

type ValidateWorkspace=(document:WorkspaceDocument)=>void;

type OpenOptions={
 factory?:IDBFactory;
 now?:()=>string;
};

const clone=<T>(value:T):T=>JSON.parse(JSON.stringify(value)) as T;

function parseWorkspace(raw:string,key:string,validate:ValidateWorkspace):WorkspaceDocument{
 let parsed:WorkspaceDocument;
 try{parsed=JSON.parse(raw) as WorkspaceDocument;}catch{throw new Error(`${key}: invalid JSON`);}
 if(parsed?.schema_version!=='1')throw new Error(`${key}: unsupported workspace schema ${String(parsed?.schema_version)}`);
 validate(parsed);
 return parsed;
}

export function inspectLegacyWorkspaceStorage(storage:StorageLike,validate:ValidateWorkspace):LegacyWorkspaceSnapshot|undefined{
 const activeRaw=storage.getItem(WORKSPACE_ACTIVE_KEY);
 if(activeRaw===null)return undefined;
 const active=parseWorkspace(activeRaw,WORKSPACE_ACTIVE_KEY,validate);
 const recoveryRaw=storage.getItem(WORKSPACE_RECOVERY_KEY);
 const recovery=recoveryRaw===null?undefined:parseWorkspace(recoveryRaw,WORKSPACE_RECOVERY_KEY,validate);
 const importOriginalRaw=storage.getItem(WORKSPACE_IMPORT_ORIGINAL_KEY)??undefined;
 return {
  active_raw:activeRaw,
  active:clone(active),
  ...(recoveryRaw!==null?{recovery_raw:recoveryRaw,recovery:clone(recovery!)}:{}),
  ...(importOriginalRaw!==undefined?{import_original_raw:importOriginalRaw}:{})
 };
}

function requestResult<T>(request:IDBRequest<T>):Promise<T>{
 return new Promise((resolve,reject)=>{
  request.onsuccess=()=>resolve(request.result);
  request.onerror=()=>reject(request.error??new Error('IndexedDB request failed'));
 });
}

function transactionDone(transaction:IDBTransaction):Promise<void>{
 return new Promise((resolve,reject)=>{
  transaction.oncomplete=()=>resolve();
  transaction.onabort=()=>reject(transaction.error??new Error('IndexedDB transaction aborted'));
  transaction.onerror=()=>{};
 });
}

function ensureIndex(store:IDBObjectStore,name:string,keyPath:string){
 if(!store.indexNames.contains(name))store.createIndex(name,keyPath,{unique:false});
}

export function openCemStorage(options:OpenOptions={}):Promise<IDBDatabase>{
 const factory=options.factory??indexedDB;
 return new Promise((resolve,reject)=>{
  const request=factory.open(CEM_STORAGE_DB_NAME,CEM_STORAGE_DB_VERSION);
  request.onupgradeneeded=()=>{
   const db=request.result;
   if(!db.objectStoreNames.contains(CEM_STORAGE_STORES.workspace_documents)){
    db.createObjectStore(CEM_STORAGE_STORES.workspace_documents,{keyPath:'workspace_id'});
   }
   if(!db.objectStoreNames.contains(CEM_STORAGE_STORES.workspace_recovery)){
    db.createObjectStore(CEM_STORAGE_STORES.workspace_recovery,{keyPath:'workspace_id'});
   }
   if(!db.objectStoreNames.contains(CEM_STORAGE_STORES.import_originals)){
    db.createObjectStore(CEM_STORAGE_STORES.import_originals,{keyPath:'id'});
   }
   if(!db.objectStoreNames.contains(CEM_STORAGE_STORES.storage_meta)){
    db.createObjectStore(CEM_STORAGE_STORES.storage_meta,{keyPath:'key'});
   }
   let reality:IDBObjectStore;
   if(!db.objectStoreNames.contains(CEM_STORAGE_STORES.reality_loop_objects)){
    reality=db.createObjectStore(CEM_STORAGE_STORES.reality_loop_objects,{keyPath:'id'});
   }else{
    reality=request.transaction!.objectStore(CEM_STORAGE_STORES.reality_loop_objects);
   }
   ensureIndex(reality,'object_type','object_type');
   ensureIndex(reality,'case_id','case_id');
   ensureIndex(reality,'implementation_plan_id','implementation_plan_id');
   ensureIndex(reality,'indicator_id','indicator_id');
   ensureIndex(reality,'created_at','created_at');
  };
  request.onblocked=()=>reject(new Error('IndexedDB upgrade blocked by another open CEM tab'));
  request.onerror=()=>reject(request.error??new Error('failed to open CEM IndexedDB'));
  request.onsuccess=()=>{
   const db=request.result;
   db.onversionchange=()=>db.close();
   resolve(db);
  };
 });
}

export async function readIndexedWorkspace(workspaceId:string,options:OpenOptions={}):Promise<WorkspaceDocument|undefined>{
 const db=await openCemStorage(options);
 try{
  const tx=db.transaction(CEM_STORAGE_STORES.workspace_documents,'readonly');
  const value=await requestResult(tx.objectStore(CEM_STORAGE_STORES.workspace_documents).get(workspaceId));
  await transactionDone(tx);
  return value===undefined?undefined:clone(value as WorkspaceDocument);
 }finally{db.close();}
}

export async function readStorageMeta(key:string,options:OpenOptions={}):Promise<unknown>{
 const db=await openCemStorage(options);
 try{
  const tx=db.transaction(CEM_STORAGE_STORES.storage_meta,'readonly');
  const value=await requestResult(tx.objectStore(CEM_STORAGE_STORES.storage_meta).get(key));
  await transactionDone(tx);
  return value===undefined?undefined:clone((value as {value:unknown}).value);
 }finally{db.close();}
}

export async function migrateLegacyWorkspaceToIndexedDb(
 storage:StorageLike,
 validate:ValidateWorkspace,
 options:OpenOptions={}
):Promise<LegacyMigrationResult>{
 const snapshot=inspectLegacyWorkspaceStorage(storage,validate);
 if(!snapshot){
  return {status:'NO_ACTIVE_WORKSPACE',legacy_keys_preserved:true,database_name:CEM_STORAGE_DB_NAME,database_version:CEM_STORAGE_DB_VERSION};
 }
 const now=options.now??(()=>new Date().toISOString());
 const db=await openCemStorage(options);
 try{
  const priorTx=db.transaction(CEM_STORAGE_STORES.storage_meta,'readonly');
  const priorRecord=await requestResult(priorTx.objectStore(CEM_STORAGE_STORES.storage_meta).get(LEGACY_MIGRATION_META_KEY)) as {value?:{workspace_id?:string;active_raw?:string}}|undefined;
  await transactionDone(priorTx);
  const refreshed=Boolean(priorRecord?.value?.workspace_id===snapshot.active.workspace_id&&priorRecord.value.active_raw!==undefined);

  const stores=[
   CEM_STORAGE_STORES.workspace_documents,
   CEM_STORAGE_STORES.workspace_recovery,
   CEM_STORAGE_STORES.import_originals,
   CEM_STORAGE_STORES.storage_meta
  ];
  let tx:IDBTransaction;
  try{
   tx=db.transaction(stores,'readwrite',{durability:'strict'});
  }catch{
   tx=db.transaction(stores,'readwrite');
  }
  tx.objectStore(CEM_STORAGE_STORES.workspace_documents).put(clone(snapshot.active));
  if(snapshot.recovery){
   tx.objectStore(CEM_STORAGE_STORES.workspace_recovery).put({
    workspace_id:snapshot.active.workspace_id,
    document:clone(snapshot.recovery),
    original_raw:snapshot.recovery_raw
   });
  }
  if(snapshot.import_original_raw!==undefined){
   tx.objectStore(CEM_STORAGE_STORES.import_originals).put({
    id:`legacy-import-original:${snapshot.active.workspace_id}`,
    workspace_id:snapshot.active.workspace_id,
    original_text:snapshot.import_original_raw
   });
  }
  tx.objectStore(CEM_STORAGE_STORES.storage_meta).put({
   key:LEGACY_MIGRATION_META_KEY,
   value:{
    workspace_id:snapshot.active.workspace_id,
    active_raw:snapshot.active_raw,
    migrated_at:now(),
    source:'localStorage',
    legacy_keys_preserved:true
   }
  });
  await transactionDone(tx);

  const verifyTx=db.transaction(CEM_STORAGE_STORES.workspace_documents,'readonly');
  const written=await requestResult(verifyTx.objectStore(CEM_STORAGE_STORES.workspace_documents).get(snapshot.active.workspace_id)) as WorkspaceDocument|undefined;
  await transactionDone(verifyTx);
  if(!written)throw new Error('IndexedDB migration verification failed: active workspace missing');
  validate(written);
  if(JSON.stringify(written)!==JSON.stringify(snapshot.active))throw new Error('IndexedDB migration verification failed: active workspace mismatch');

  return {
   status:refreshed?'REFRESHED':'MIGRATED',
   workspace_id:snapshot.active.workspace_id,
   legacy_keys_preserved:true,
   database_name:CEM_STORAGE_DB_NAME,
   database_version:CEM_STORAGE_DB_VERSION
  };
 }finally{db.close();}
}
