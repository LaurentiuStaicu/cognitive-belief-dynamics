import type {SemanticEntity,SemanticIndex,SemanticLang,SemanticRelation} from './semantic';

export type SemanticInspectorRelation={
 id:string;
 layer:SemanticRelation['layer'];
 direction:'incoming'|'outgoing';
 counterpartId:string;
 counterpartLabel:string;
 relationType?:string;
 polarity?:string;
 statusFacets?:SemanticRelation['status_facets'];
};

export type SemanticInspectorEntity={
 kind:'entity';id:string;semanticType:string;title:string;shortName?:string;
 summary?:string;statusFacets?:SemanticEntity['status_facets'];
 source:SemanticEntity['source'];related:SemanticInspectorRelation[];
};

export type SemanticInspectorRelationModel={
 kind:'relation';id:string;layer:SemanticRelation['layer'];title:string;
 sourceId:string;sourceLabel:string;targetId:string;targetLabel:string;
 relationType?:string;polarity?:string;statusFacets?:SemanticRelation['status_facets'];
 evidenceRefs?:string[];formula?:string;codeFile?:string;registeredRelationId?:string;
 sourceRecord:SemanticRelation['source_record'];
};

export type SemanticInspectorModel=SemanticInspectorEntity|SemanticInspectorRelationModel;

function label(entity:SemanticEntity|undefined,lang:SemanticLang,fallback:string):string{
 if(!entity)return fallback;const p=entity.labels.preferred;return p[lang]??p.und??p.en??p.ro??fallback;
}
function summary(entity:SemanticEntity,lang:SemanticLang):string|undefined{
 const s=entity.summary;return s?.[lang]??s?.und??s?.en??s?.ro;
}

export function inspectSemanticIndex(index:SemanticIndex,id:string,lang:SemanticLang):SemanticInspectorModel|undefined{
 const entities=new Map(index.entities.map(entity=>[entity.id,entity]));
 const entity=entities.get(id);
 if(entity){
  const related=index.relations.flatMap(relation=>{
   if(relation.source===id){const counterpart=entities.get(relation.target);return [{
    id:relation.id,layer:relation.layer,direction:'outgoing' as const,counterpartId:relation.target,
    counterpartLabel:label(counterpart,lang,relation.target),relationType:relation.relation_type,
    polarity:relation.polarity,statusFacets:relation.status_facets
   }];}
   if(relation.target===id){const counterpart=entities.get(relation.source);return [{
    id:relation.id,layer:relation.layer,direction:'incoming' as const,counterpartId:relation.source,
    counterpartLabel:label(counterpart,lang,relation.source),relationType:relation.relation_type,
    polarity:relation.polarity,statusFacets:relation.status_facets
   }];}
   return [];
  }).sort((a,b)=>a.layer.localeCompare(b.layer,'en')||a.id.localeCompare(b.id,'en'));
  return {kind:'entity',id:entity.id,semanticType:entity.semantic_type,title:label(entity,lang,entity.id),
   shortName:entity.short_name,summary:summary(entity,lang),statusFacets:entity.status_facets,source:entity.source,related};
 }
 const relation=index.relations.find(item=>item.id===id);if(!relation)return undefined;
 const source=entities.get(relation.source),target=entities.get(relation.target);
 const sourceLabel=label(source,lang,relation.source),targetLabel=label(target,lang,relation.target);
 return {kind:'relation',id:relation.id,layer:relation.layer,title:sourceLabel+' → '+targetLabel,
  sourceId:relation.source,sourceLabel,targetId:relation.target,targetLabel,relationType:relation.relation_type,
  polarity:relation.polarity,statusFacets:relation.status_facets,evidenceRefs:relation.evidence_refs,
  formula:relation.formula,codeFile:relation.code_file,registeredRelationId:relation.registered_relation_id,sourceRecord:relation.source_record};
}

