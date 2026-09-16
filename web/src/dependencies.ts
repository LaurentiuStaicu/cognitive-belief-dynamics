/** Computational dependencies, separate from the empirical evidence registry. */
import canonical from './generated/computational_dependencies.json';

export type Dependency={id:string;source:string;target:string;ro:string;en:string;formula:string;file:string;registered?:string};
export type ExtraNode={id:string;ro:string;en:string;kind:'input'|'output'};

type CanonicalData={
 extra_nodes:Array<{graph_id:string;semantic_id:string;kind:'input'|'output';label:{ro:string;en:string}}>;
 dependencies:Array<{
  id:string;graph_id:string;source_graph_id:string;target_graph_id:string;
  source_semantic_id:string;target_semantic_id:string;
  description:{ro:string;en:string};formula:string;code_file:string;registered_relation_id?:string
 }>;
};

const data=canonical as CanonicalData;

export const extraNodes:ExtraNode[]=data.extra_nodes.map(node=>({
 id:node.graph_id,
 ro:node.label.ro,
 en:node.label.en,
 kind:node.kind
}));

export const dependencies:Dependency[]=data.dependencies.map(item=>({
 id:item.graph_id,
 source:item.source_graph_id,
 target:item.target_graph_id,
 ro:item.description.ro,
 en:item.description.en,
 formula:item.formula,
 file:item.code_file,
 ...(item.registered_relation_id?{registered:item.registered_relation_id}:{})
}));
