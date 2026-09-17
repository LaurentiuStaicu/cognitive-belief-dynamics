export type LocalDiagnosticsInput={
 software_version:string;
 release_tag?:string;
 model_specification:string;
 evidence_snapshot:string;
 evidence_as_of:string;
 online:boolean;
 local_storage_available:boolean;
 indexed_db_available:boolean;
 service_worker_controlled:boolean;
};

export type LocalDiagnostics={
 schema_version:'1';
 generated_at:string;
 scope:'LOCAL_RUNTIME_ONLY';
 telemetry:'NONE';
 software:{version:string;release_tag?:string;model_specification:string};
 evidence:{snapshot:string;as_of:string};
 runtime:{
  network:'ONLINE'|'OFFLINE';
  local_storage:'AVAILABLE'|'UNAVAILABLE';
  indexed_db:'AVAILABLE'|'UNAVAILABLE';
  service_worker:'CONTROLLED'|'NOT_CONTROLLED';
 };
};

export function collectLocalDiagnostics(
 input:LocalDiagnosticsInput,
 now:()=>string=()=>new Date().toISOString()
):LocalDiagnostics{
 return {
  schema_version:'1',
  generated_at:now(),
  scope:'LOCAL_RUNTIME_ONLY',
  telemetry:'NONE',
  software:{
   version:input.software_version,
   ...(input.release_tag?{release_tag:input.release_tag}:{}),
   model_specification:input.model_specification
  },
  evidence:{snapshot:input.evidence_snapshot,as_of:input.evidence_as_of},
  runtime:{
   network:input.online?'ONLINE':'OFFLINE',
   local_storage:input.local_storage_available?'AVAILABLE':'UNAVAILABLE',
   indexed_db:input.indexed_db_available?'AVAILABLE':'UNAVAILABLE',
   service_worker:input.service_worker_controlled?'CONTROLLED':'NOT_CONTROLLED'
  }
 };
}

export function serializeLocalDiagnostics(record:LocalDiagnostics):string{
 return JSON.stringify(record,null,2)+'\n';
}

export function downloadLocalDiagnostics(record:LocalDiagnostics):void{
 const blob=new Blob([serializeLocalDiagnostics(record)],{type:'application/json'});
 const url=URL.createObjectURL(blob);
 const anchor=globalThis.document.createElement('a');
 anchor.href=url;
 anchor.download='cem-local-diagnostics.json';
 anchor.click();
 setTimeout(()=>URL.revokeObjectURL(url),1000);
}
