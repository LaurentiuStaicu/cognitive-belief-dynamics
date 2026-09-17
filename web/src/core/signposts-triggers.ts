import type {IndicatorProjection} from './indicator-objects';

type Lang='ro'|'en';
type Copy=Record<Lang,string>;
export type SignpostDefinition={object_type:'Signpost';id:string;indicator_id:string;label:Copy;monitoring_role:'INDICATOR_TO_MONITOR';timing_role:'EARLY_SIGNAL_OR_STATE_TRACKING';source:'OA7_INDICATOR_OBJECT'};
export type TriggerDraft={object_type:'TriggerDraft';id:string;signpost_id:string;indicator_id:string;comparator:'LT'|'LTE'|'GTE'|'GT';threshold:number;unit:'probability';origin:'USER_DECLARED';evaluation_status:'NOT_EVALUATED_NO_OBSERVED_OUTCOME';action_binding_status:'NOT_BOUND_TO_ADAPTIVE_ACTION'};
export type SignpostTriggerProjection={object_type:'SignpostTriggerProjection';persistence:'EPHEMERAL_NOT_WORKSPACE';automation:'NO_BACKGROUND_MONITORING';signposts:SignpostDefinition[]};

const copy=(ro:string,en:string):Copy=>({ro,en});
const slug=(id:string)=>id.replace(/^CEM\.INDICATOR\./,'').replace(/[^A-Za-z0-9._-]/g,'-');

export function buildSignpostProjection(indicators:IndicatorProjection):SignpostTriggerProjection{
 return {object_type:'SignpostTriggerProjection',persistence:'EPHEMERAL_NOT_WORKSPACE',automation:'NO_BACKGROUND_MONITORING',signposts:indicators.indicators.map(({definition})=>({object_type:'Signpost',id:`CEM.SIGNPOST.${slug(definition.id)}`,indicator_id:definition.id,label:copy(`Urmărește: ${definition.label.ro}`,`Watch: ${definition.label.en}`),monitoring_role:'INDICATOR_TO_MONITOR',timing_role:'EARLY_SIGNAL_OR_STATE_TRACKING',source:'OA7_INDICATOR_OBJECT'}))};
}

export function createTriggerDraft(input:{signpost:SignpostDefinition;comparator:TriggerDraft['comparator'];threshold:number}):TriggerDraft{
 if(!Number.isFinite(input.threshold)||input.threshold<0||input.threshold>1)throw new Error('trigger threshold must be within [0,1]');
 return {object_type:'TriggerDraft',id:`CEM.TRIGGER.DRAFT.${slug(input.signpost.indicator_id)}.${input.comparator}.${String(input.threshold).replace('.','_')}`,signpost_id:input.signpost.id,indicator_id:input.signpost.indicator_id,comparator:input.comparator,threshold:input.threshold,unit:'probability',origin:'USER_DECLARED',evaluation_status:'NOT_EVALUATED_NO_OBSERVED_OUTCOME',action_binding_status:'NOT_BOUND_TO_ADAPTIVE_ACTION'};
}
