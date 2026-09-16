import release from '../public/model/version.json';
import {semanticEntity,semanticIndex,semanticRelation} from './semantic';
import {WorkspaceStore,type WorkspaceDocument,type WorkspaceSeed} from './workspace-store';

export function validateWorkspaceRuntime(document:WorkspaceDocument):void{
 if(document.schema_version!=='1')throw new Error(`unsupported workspace schema ${document.schema_version}`);
 if(!document.workspace_id.startsWith('CEM.WORKSPACE.'))throw new Error('invalid workspace id');
 if(!document.case.id.startsWith('CEM.CASE.'))throw new Error('invalid case id');

 for(const id of document.case.entity_refs)if(!semanticEntity(id))throw new Error(`unknown semantic entity ${id}`);
 for(const id of document.case.relation_refs)if(!semanticRelation(id))throw new Error(`unknown semantic relation ${id}`);
 if(document.case.focus?.entity_id&&!semanticEntity(document.case.focus.entity_id))throw new Error(`unknown focus entity ${document.case.focus.entity_id}`);
 if(document.case.focus?.relation_id&&!semanticRelation(document.case.focus.relation_id))throw new Error(`unknown focus relation ${document.case.focus.relation_id}`);

 const generated=new Set(
  document.provenance.activities.flatMap(activity=>
   activity.generated.filter(ref=>ref.kind==='WORKSPACE_REVISION').map(ref=>ref.id)
  )
 );
 if(!generated.has(document.provenance.current_revision_id))throw new Error('workspace current revision is not generated');

 for(const activity of document.provenance.activities){
  for(const ref of [...activity.used,...activity.generated]){
   if(ref.kind==='SEMANTIC_ENTITY'&&!semanticEntity(ref.id))throw new Error(`unknown provenance semantic entity ${ref.id}`);
   if(ref.kind==='SEMANTIC_RELATION'&&!semanticRelation(ref.id))throw new Error(`unknown provenance semantic relation ${ref.id}`);
  }
  if(activity.revision_of&&!generated.has(activity.revision_of))throw new Error(`unknown provenance parent revision ${activity.revision_of}`);
 }
}

export function initializeWorkspaceSession(storage:Storage=localStorage):WorkspaceStore{
 const store=new WorkspaceStore(storage,{validate:validateWorkspaceRuntime});
 const seed:WorkspaceSeed={
  title:'Untitled CEM case',
  versions:{
   software_version:release.software_version,
   release_tag:release.release_tag,
   model_specification:release.model_specification,
   evidence_snapshot:release.evidence_snapshot,
   semantic_schema_version:semanticIndex.schema_version,
   semantic_baseline_contract:semanticIndex.baseline_contract
  }
 };
 store.loadOrCreate(seed);
 return store;
}
