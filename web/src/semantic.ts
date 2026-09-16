import raw from './generated/semantic_index.json';

export type SemanticLang='ro'|'en';
export type SemanticStatusFacets={
 source_tags?:string[];
 phenomenon_evidence?:string;
 mechanism_evidence?:string;
 functional_form?:string;
};
export type SemanticLabels={
 preferred:Partial<Record<SemanticLang|'und',string>>;
 alternative?:Partial<Record<SemanticLang|'und',string[]>>;
};
export type SemanticEntity={
 id:string;
 semantic_type:string;
 semantic_roles?:string[];
 labels:SemanticLabels;
 source:{path:string;source_id:string};
 status_facets?:SemanticStatusFacets;
 short_name?:string;
 summary?:Partial<Record<SemanticLang|'und',string>>;
 related_ids?:string[];
};
export type SemanticRelation={
 id:string;
 layer:'REGISTERED_EVIDENCE_RELATION'|'COMPUTATIONAL_DEPENDENCY'|'DOCUMENTATION_RELATION';
 source:string;
 target:string;
 source_record:{path:string;source_id:string};
 relation_type?:string;
 polarity?:string;
 status_facets?:SemanticStatusFacets;
 evidence_refs?:string[];
 formula?:string;
 code_file?:string;
 registered_relation_id?:string;
};
export type SemanticIndex={
 schema_version:string;
 baseline_contract:string;
 source_paths:string[];
 entities:SemanticEntity[];
 relations:SemanticRelation[];
};

export const semanticIndex=raw as unknown as SemanticIndex;
const entitiesById=new Map(semanticIndex.entities.map(entity=>[entity.id,entity]));
const relationsById=new Map(semanticIndex.relations.map(relation=>[relation.id,relation]));
const outgoingById=new Map<string,SemanticRelation[]>();
const incomingById=new Map<string,SemanticRelation[]>();

for(const relation of semanticIndex.relations){
 const outgoing=outgoingById.get(relation.source)??[];
 outgoing.push(relation);outgoingById.set(relation.source,outgoing);
 const incoming=incomingById.get(relation.target)??[];
 incoming.push(relation);incomingById.set(relation.target,incoming);
}

export function semanticEntity(id:string):SemanticEntity|undefined{return entitiesById.get(id);}
export function semanticRelation(id:string):SemanticRelation|undefined{return relationsById.get(id);}

export function semanticLabel(id:string,lang:SemanticLang,fallback?:string):string{
 const preferred=semanticEntity(id)?.labels.preferred;
 return preferred?.[lang]??preferred?.und??preferred?.en??preferred?.ro??fallback??id;
}

export function semanticRelationsFor(
 id:string,
 direction:'incoming'|'outgoing'|'both'='both'
):SemanticRelation[]{
 if(direction==='incoming')return [...(incomingById.get(id)??[])];
 if(direction==='outgoing')return [...(outgoingById.get(id)??[])];
 return [...(incomingById.get(id)??[]),...(outgoingById.get(id)??[])];
}

export function assertSemanticCoverage(entityIds:Iterable<string>,relationIds:Iterable<string>=[]):void{
 const missingEntities=[...entityIds].filter(id=>!entitiesById.has(id));
 const missingRelations=[...relationIds].filter(id=>!relationsById.has(id));
 if(missingEntities.length||missingRelations.length){
  throw new Error(
   `Semantic Spine coverage error: entities=[${missingEntities.join(', ')}] relations=[${missingRelations.join(', ')}]`
  );
 }
}
