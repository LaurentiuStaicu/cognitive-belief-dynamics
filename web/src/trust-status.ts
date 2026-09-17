export type EvidenceSnapshotTrustInput={
 id:string;
 as_of:string;
 model_specification:string;
};

export type TrustStatus={
 network:'ONLINE'|'OFFLINE';
 delivery_mode:'STATIC_BUNDLED_ARTIFACTS';
 offline_guarantee:'NONE_WITHOUT_PRIOR_BROWSER_CACHE';
 evidence:{
  id:string;
  as_of:string;
  model_specification:string;
  mode:'PINNED_BUNDLED_SNAPSHOT';
  freshness:'NOT_LIVE_VERIFIED';
  age_days:number;
 };
};

const DAY_MS=24*60*60*1000;

function parseAsOf(value:string):number{
 if(!/^\d{4}-\d{2}-\d{2}$/.test(value))throw new Error(`invalid evidence as_of date: ${value}`);
 const timestamp=Date.parse(`${value}T00:00:00Z`);
 if(!Number.isFinite(timestamp))throw new Error(`invalid evidence as_of date: ${value}`);
 return timestamp;
}

export function deriveTrustStatus(
 snapshot:EvidenceSnapshotTrustInput,
 options:{online:boolean;now?:Date}={online:true}
):TrustStatus{
 const now=options.now??new Date();
 const asOf=parseAsOf(snapshot.as_of);
 const ageDays=Math.floor((now.getTime()-asOf)/DAY_MS);
 if(ageDays<0)throw new Error('evidence snapshot as_of cannot be in the future');
 return {
  network:options.online?'ONLINE':'OFFLINE',
  delivery_mode:'STATIC_BUNDLED_ARTIFACTS',
  offline_guarantee:'NONE_WITHOUT_PRIOR_BROWSER_CACHE',
  evidence:{
   id:snapshot.id,
   as_of:snapshot.as_of,
   model_specification:snapshot.model_specification,
   mode:'PINNED_BUNDLED_SNAPSHOT',
   freshness:'NOT_LIVE_VERIFIED',
   age_days:ageDays
  }
 };
}
