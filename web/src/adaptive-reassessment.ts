export const REASSESSMENT_SCHEMA_VERSION='1';
export const REASSESSMENT_STORAGE_KEY='cem.decision-reassessment.v1';
export const REASSESSMENT_MAX_RECORDS=50;

export type ReassessmentBasis='USER_DEFINED'|'EMPIRICAL'|'CONCEPTUAL'|'EXECUTABLE';
export type SignpostKind='METRIC'|'EVENT'|'EVIDENCE_UPDATE'|'SCHEDULED_REVIEW'|'OTHER';

export type ReassessmentRecord={
 id:string;
 uncertainty_id:string;
 signpost_kind:SignpostKind;
 indicator:string;
 trigger_condition:string;
 response_action:string;
 basis:ReassessmentBasis;
 rationale:string;
 source_note:string;
 earliest_reassessment:string;
 latest_reassessment:string;
 created_at:string;
};

export type ReassessmentDocument={
 schema_version:'1';
 records:ReassessmentRecord[];
};

export type StorageLike={
 getItem(key:string):string|null;
 setItem(key:string,value:string):void;
 removeItem(key:string):void;
};

type Options={
 storageKey?:string;
 maxRecords?:number;
 now?:()=>string;
 idFactory?:()=>string;
};

const clone=<T>(value:T):T=>JSON.parse(JSON.stringify(value)) as T;
const nonEmpty=(value:unknown):value is string=>typeof value==='string'&&value.trim().length>0;

function validRecord(value:unknown):value is ReassessmentRecord{
 if(!value||typeof value!=='object')return false;
 const item=value as Partial<ReassessmentRecord>;
 if(!nonEmpty(item.id)||!nonEmpty(item.uncertainty_id)||!nonEmpty(item.indicator)||!nonEmpty(item.trigger_condition)||!nonEmpty(item.response_action)||!nonEmpty(item.created_at))return false;
 if(!['METRIC','EVENT','EVIDENCE_UPDATE','SCHEDULED_REVIEW','OTHER'].includes(item.signpost_kind??''))return false;
 if(!['USER_DEFINED','EMPIRICAL','CONCEPTUAL','EXECUTABLE'].includes(item.basis??''))return false;
 for(const field of ['rationale','source_note','earliest_reassessment','latest_reassessment'] as const){if(typeof item[field]!=='string')return false;}
 return true;
}

export class ReassessmentStore{
 private readonly storage:StorageLike;
 private readonly storageKey:string;
 private readonly maxRecords:number;
 private readonly now:()=>string;
 private readonly idFactory:()=>string;

 constructor(storage:StorageLike,options:Options={}){
  this.storage=storage;
  this.storageKey=options.storageKey??REASSESSMENT_STORAGE_KEY;
  this.maxRecords=Math.max(1,Math.min(options.maxRecords??REASSESSMENT_MAX_RECORDS,REASSESSMENT_MAX_RECORDS));
  this.now=options.now??(()=>new Date().toISOString());
  this.idFactory=options.idFactory??(()=>`trigger-${Date.now()}-${Math.random().toString(36).slice(2,8)}`);
 }

 all():ReassessmentRecord[]{return clone(this.read().records);}

 add(input:Omit<ReassessmentRecord,'id'|'created_at'>):ReassessmentRecord{
  const record:ReassessmentRecord={...clone(input),id:this.idFactory(),created_at:this.now()};
  if(!validRecord(record))throw new Error('invalid reassessment record');
  const document=this.read();
  document.records=[...document.records,record].slice(-this.maxRecords);
  this.write(document);
  return clone(record);
 }

 remove(id:string):void{
  if(!nonEmpty(id))throw new Error('record id required');
  const document=this.read();
  document.records=document.records.filter(item=>item.id!==id);
  this.write(document);
 }

 clear():void{this.storage.removeItem(this.storageKey);}

 private read():ReassessmentDocument{
  const raw=this.storage.getItem(this.storageKey);
  if(raw===null)return {schema_version:REASSESSMENT_SCHEMA_VERSION,records:[]};
  try{
   const parsed=JSON.parse(raw) as Partial<ReassessmentDocument>;
   if(parsed.schema_version!==REASSESSMENT_SCHEMA_VERSION||!Array.isArray(parsed.records)||!parsed.records.every(validRecord)){
    return {schema_version:REASSESSMENT_SCHEMA_VERSION,records:[]};
   }
   return {schema_version:REASSESSMENT_SCHEMA_VERSION,records:parsed.records.slice(-this.maxRecords)};
  }catch{return {schema_version:REASSESSMENT_SCHEMA_VERSION,records:[]};}
 }

 private write(document:ReassessmentDocument):void{this.storage.setItem(this.storageKey,JSON.stringify(document));}
}
