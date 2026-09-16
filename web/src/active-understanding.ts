export type ActiveStage='WORKED_EXAMPLE'|'PREDICT'|'REVEAL'|'EXPLAIN'|'BOUNDARY'|'COMPLETE';
export type ActiveConfidence='low'|'medium'|'high';
export type PredictionOutcome='correct'|'incorrect';

export type ActiveSession={
 challengeId:string;
 stage:ActiveStage;
 predictionCategory?:string;
 confidence?:ActiveConfidence;
 outcome?:PredictionOutcome;
};

export type ActiveAction=
 |{type:'START_PREDICTION'}
 |{type:'SUBMIT_PREDICTION';predictionCategory:string;correctChoiceId:string;confidence?:ActiveConfidence}
 |{type:'SKIP_PREDICTION'}
 |{type:'SHOW_EXPLANATION'}
 |{type:'SHOW_BOUNDARY'}
 |{type:'COMPLETE'}
 |{type:'RESET'};

export function createActiveSession(challengeId:string):ActiveSession{
 if(!challengeId.trim())throw new Error('challenge id required');
 return {challengeId,stage:'WORKED_EXAMPLE'};
}

export function reduceActiveSession(state:ActiveSession,action:ActiveAction):ActiveSession{
 switch(action.type){
  case 'START_PREDICTION':
   if(state.stage!=='WORKED_EXAMPLE')throw new Error('prediction can start only after worked example');
   return {...state,stage:'PREDICT'};
  case 'SUBMIT_PREDICTION':
   if(state.stage!=='PREDICT')throw new Error('prediction can be submitted only in PREDICT stage');
   if(!action.predictionCategory.trim())throw new Error('prediction category required');
   return {
    ...state,
    stage:'REVEAL',
    predictionCategory:action.predictionCategory,
    ...(action.confidence?{confidence:action.confidence}:{}),
    outcome:action.predictionCategory===action.correctChoiceId?'correct':'incorrect'
   };
  case 'SKIP_PREDICTION':
   if(state.stage!=='PREDICT')throw new Error('prediction can be skipped only in PREDICT stage');
   return {challengeId:state.challengeId,stage:'REVEAL'};
  case 'SHOW_EXPLANATION':
   if(state.stage!=='REVEAL')throw new Error('explanation follows reveal');
   return {...state,stage:'EXPLAIN'};
  case 'SHOW_BOUNDARY':
   if(state.stage!=='EXPLAIN')throw new Error('epistemic boundary follows explanation');
   return {...state,stage:'BOUNDARY'};
  case 'COMPLETE':
   if(state.stage!=='BOUNDARY')throw new Error('completion follows epistemic boundary');
   return {...state,stage:'COMPLETE'};
  case 'RESET':
   return createActiveSession(state.challengeId);
 }
}

export const ACTIVE_HISTORY_SCHEMA_VERSION='1';
export const ACTIVE_HISTORY_STORAGE_KEY='cem.active-understanding.history.v1';
export const ACTIVE_HISTORY_MAX_RECORDS=100;

export type LearningHistoryRecord={
 challenge_id:string;
 canonical_target_refs:string[];
 prediction_category:string;
 confidence?:ActiveConfidence;
 outcome_category:PredictionOutcome;
 timestamp:string;
};

export type LearningHistoryDocument={
 schema_version:'1';
 records:LearningHistoryRecord[];
};

export type StorageLike={
 getItem(key:string):string|null;
 setItem(key:string,value:string):void;
 removeItem(key:string):void;
};

type LearningHistoryOptions={
 maxRecords?:number;
 now?:()=>string;
 storageKey?:string;
};

const clone=<T>(value:T):T=>JSON.parse(JSON.stringify(value)) as T;

function validRecord(record:unknown):record is LearningHistoryRecord{
 if(!record||typeof record!=='object')return false;
 const item=record as Partial<LearningHistoryRecord>;
 if(typeof item.challenge_id!=='string'||!item.challenge_id)return false;
 if(!Array.isArray(item.canonical_target_refs)||item.canonical_target_refs.some(ref=>typeof ref!=='string'||!ref))return false;
 if(typeof item.prediction_category!=='string'||!item.prediction_category)return false;
 if(item.confidence!==undefined&&!['low','medium','high'].includes(item.confidence))return false;
 if(item.outcome_category!=='correct'&&item.outcome_category!=='incorrect')return false;
 if(typeof item.timestamp!=='string'||!item.timestamp)return false;
 return true;
}

export class LearningHistoryStore{
 private readonly storage:StorageLike;
 private readonly storageKey:string;
 private readonly maxRecords:number;
 private readonly now:()=>string;

 constructor(storage:StorageLike,options:LearningHistoryOptions={}){
  this.storage=storage;
  this.storageKey=options.storageKey??ACTIVE_HISTORY_STORAGE_KEY;
  this.maxRecords=Math.max(1,Math.min(options.maxRecords??ACTIVE_HISTORY_MAX_RECORDS,ACTIVE_HISTORY_MAX_RECORDS));
  this.now=options.now??(()=>new Date().toISOString());
 }

 all():LearningHistoryRecord[]{
  return clone(this.read().records);
 }

 record(input:Omit<LearningHistoryRecord,'timestamp'>):LearningHistoryDocument{
  if(!validRecord({...input,timestamp:this.now()}))throw new Error('invalid learning-history record');
  const document=this.read();
  const next:LearningHistoryRecord={...clone(input),timestamp:this.now()};
  document.records=[...document.records,next].slice(-this.maxRecords);
  this.write(document);
  return clone(document);
 }

 clear():void{
  this.storage.removeItem(this.storageKey);
 }

 private read():LearningHistoryDocument{
  const raw=this.storage.getItem(this.storageKey);
  if(raw===null)return {schema_version:ACTIVE_HISTORY_SCHEMA_VERSION,records:[]};
  try{
   const parsed=JSON.parse(raw) as Partial<LearningHistoryDocument>;
   if(parsed.schema_version!==ACTIVE_HISTORY_SCHEMA_VERSION||!Array.isArray(parsed.records)||!parsed.records.every(validRecord)){
    return {schema_version:ACTIVE_HISTORY_SCHEMA_VERSION,records:[]};
   }
   return {schema_version:ACTIVE_HISTORY_SCHEMA_VERSION,records:parsed.records.slice(-this.maxRecords)};
  }catch{
   return {schema_version:ACTIVE_HISTORY_SCHEMA_VERSION,records:[]};
  }
 }

 private write(document:LearningHistoryDocument):void{
  this.storage.setItem(this.storageKey,JSON.stringify(document));
 }
}
