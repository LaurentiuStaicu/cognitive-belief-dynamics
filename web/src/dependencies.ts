/** Computational dependency view hydrated from canonical model data. */
export type Dependency={
 id:string;
 source:string;
 target:string;
 ro:string;
 en:string;
 formula:string;
 file:string;
 registered?:string;
};

export type ExtraNode={
 id:string;
 ro:string;
 en:string;
 kind:'input'|'output';
};

export type ComputationalDependencyRegistry={
 schema_version:string;
 model_specification:'M0';
 nodes:{
  id:string;
  semantic_id:string;
  label:{ro:string;en:string};
  kind:'input'|'output';
 }[];
 dependencies:{
  id:string;
  source:string;
  target:string;
  source_semantic_id:string;
  target_semantic_id:string;
  explanation:{ro:string;en:string};
  formula:string;
  code_file:string;
  registered_relation_id?:string;
 }[];
};

export const dependencies:Dependency[]=[];
export const extraNodes:ExtraNode[]=[];

export function hydrateComputationalDependencies(data:ComputationalDependencyRegistry){
 if(data.model_specification!=='M0')throw new Error('computational_dependencies: expected M0');
 dependencies.splice(0,dependencies.length,...data.dependencies.map(item=>({
  id:item.id,
  source:item.source,
  target:item.target,
  ro:item.explanation.ro,
  en:item.explanation.en,
  formula:item.formula,
  file:item.code_file,
  ...(item.registered_relation_id?{registered:item.registered_relation_id}:{})
 })));
 extraNodes.splice(0,extraNodes.length,...data.nodes.map(item=>({
  id:item.id,
  ro:item.label.ro,
  en:item.label.en,
  kind:item.kind
 })));
}
