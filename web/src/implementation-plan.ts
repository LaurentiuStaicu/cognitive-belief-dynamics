import type {ActionCanvasProjection} from './action-canvas';
import type {AdaptivePlanDraft,AdaptivePlanStep} from './adaptive-plan-runtime';
import type {IndicatorProjection} from './indicator-objects';

type Copy={ro:string;en:string};

export type ProspectiveSnapshot={
 id:string;
 frozen_at:string;
 revision_policy:'APPEND_ONLY_NO_RETROACTIVE_EDIT';
};

export type ImplementationPlan={
 object_type:'ImplementationPlan';
 id:string;
 case_id:string;
 created_at:string;
 decision_analysis_id:string;
 prospective_snapshot:ProspectiveSnapshot;
 plan_scope:'ILLUSTRATIVE';
 action_canvas:{
  problem:{label:Copy;refs:string[]};
  target_mechanism:{label:Copy;refs:string[]};
  intervention:{label:Copy;refs:string[]};
  proximal_result:{label:Copy;refs:string[];indicator_ids:string[]};
  intermediate_result:{label:Copy;refs:string[];indicator_ids:string[]};
  final_outcome:{label:Copy;refs:string[];indicator_ids:string[]};
 };
 indicator_ids:string[];
 adaptive_plan:{
  id:string;
  phase:'NOW'|'WATCH'|'IF'|'THEN'|'STOP'|'REASSESS';
  statement:Copy;
  indicator_id?:string;
  trigger_condition?:Copy;
  action?:Copy;
 }[];
 status:'DRAFT';
};

type MaterializeInput={
 case_id:string;
 action_canvas:ActionCanvasProjection;
 indicators:IndicatorProjection;
 adaptive_plan:AdaptivePlanDraft;
 now?:()=>string;
 id?:()=>string;
};

const clone=<T>(value:T):T=>JSON.parse(JSON.stringify(value)) as T;
const defaultId=()=>crypto.randomUUID();

function requireCompleteAdaptivePlan(plan:AdaptivePlanDraft):void{
 const phases=['NOW','WATCH','IF','THEN','STOP','REASSESS'] as const;
 if(plan.steps.length!==phases.length)throw new Error('adaptive plan must contain exactly six phases');
 for(let i=0;i<phases.length;i++){
  const step=plan.steps[i];
  if(step.phase!==phases[i])throw new Error('adaptive plan phase order is invalid');
  if(step.readiness!=='DEFINED')throw new Error(`adaptive plan phase ${step.phase} is not defined`);
 }
}

function canonicalAdaptiveStep(step:AdaptivePlanStep):ImplementationPlan['adaptive_plan'][number]{
 return {
  id:step.id.replace('CEM.ADAPTIVE.RUNTIME.','CEM.ADAPTIVE.STEP.RUNTIME.'),
  phase:step.phase,
  statement:clone(step.statement),
  ...(step.indicator_id?{indicator_id:step.indicator_id}:{}),
  ...(step.trigger_condition?{trigger_condition:clone(step.trigger_condition)}:{}),
  ...(step.action?{action:clone(step.action)}:{})
 };
}

export function materializeIllustrativeImplementationPlan(input:MaterializeInput):ImplementationPlan{
 requireCompleteAdaptivePlan(input.adaptive_plan);
 if(!input.case_id.startsWith('CEM.CASE.'))throw new Error('invalid case id');
 if(input.action_canvas.scope!=='ILLUSTRATIVE_UNCALIBRATED')throw new Error('only illustrative Action Canvas projections can be materialized in this slice');
 if(input.indicators.observation_boundary!=='SIMULATION_RESULT_IS_NOT_OBSERVED_OUTCOME')throw new Error('indicator observation boundary mismatch');

 const node=(stage:ActionCanvasProjection['nodes'][number]['stage'])=>{
  const found=input.action_canvas.nodes.find(item=>item.stage===stage);
  if(!found)throw new Error(`missing Action Canvas stage ${stage}`);
  return found;
 };
 const operationalIds=input.indicators.indicators.map(item=>item.definition.id);
 if(operationalIds.length===0)throw new Error('ImplementationPlan requires at least one operational Indicator');
 if(input.indicators.coverage.find(item=>item.stage==='INTERMEDIATE')?.status!=='NOT_OPERATIONALIZED')throw new Error('intermediate stage unexpectedly operationalized');
 if(input.indicators.coverage.find(item=>item.stage==='FINAL')?.status!=='NOT_OPERATIONALIZED')throw new Error('final stage unexpectedly operationalized');

 const token=(input.id??defaultId)();
 const timestamp=(input.now??(()=>new Date().toISOString()))();
 const toStage=(stage:ActionCanvasProjection['nodes'][number]['stage'])=>{
  const item=node(stage);
  return {label:clone(item.title),refs:[...item.refs]};
 };

 return {
  object_type:'ImplementationPlan',
  id:`CEM.IMPLEMENTATION.PLAN.${token}`,
  case_id:input.case_id,
  created_at:timestamp,
  decision_analysis_id:`CEM.DECISION.ANALYSIS.RUNTIME.${token}`,
  prospective_snapshot:{
   id:`CEM.PROSPECTIVE.SNAPSHOT.${token}`,
   frozen_at:timestamp,
   revision_policy:'APPEND_ONLY_NO_RETROACTIVE_EDIT'
  },
  plan_scope:'ILLUSTRATIVE',
  action_canvas:{
   problem:toStage('PROBLEM'),
   target_mechanism:toStage('TARGET_MECHANISM'),
   intervention:toStage('INTERVENTION'),
   proximal_result:{...toStage('PROXIMAL_RESULT'),indicator_ids:[...operationalIds]},
   intermediate_result:{...toStage('INTERMEDIATE_RESULT'),indicator_ids:[]},
   final_outcome:{...toStage('FINAL_OUTCOME'),indicator_ids:[]}
  },
  indicator_ids:[...operationalIds],
  adaptive_plan:input.adaptive_plan.steps.map(canonicalAdaptiveStep),
  status:'DRAFT'
 };
}

export function isAdaptivePlanReadyForFreeze(plan:AdaptivePlanDraft):boolean{
 try{requireCompleteAdaptivePlan(plan);return true;}catch{return false;}
}
