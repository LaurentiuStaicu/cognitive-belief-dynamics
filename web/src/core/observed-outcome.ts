import type {ImplementationPlan} from '../implementation-plan';
import type {IndicatorDefinition,IndicatorProjection} from './indicator-objects';

type Copy={ro:string;en:string};
export type ObservedOutcome={object_type:'ObservedOutcome';id:string;case_id:string;implementation_plan_id:string;prospective_snapshot_id:string;indicator_id:string;population:{label:Copy;definition:Copy;inclusion?:string;exclusion?:string};context:{setting:Copy;geography?:string;time_horizon:string};outcome:{name:Copy;definition:Copy;stage:'PROXIMAL'|'INTERMEDIATE'|'FINAL'};feature_of_interest:string;observed_property:string;procedure:string;phenomenon_time:string;result_time:string;result:{value:number;unit?:string;quality_note?:string};source_refs:string[];recorded_at:string;retrospective:true;mutation_policy:'APPEND_ONLY_NO_RETROACTIVE_PREDICTION_EDIT'};
export type ObservedOutcomeInput={plan:ImplementationPlan;indicators:IndicatorProjection;indicator_id:string;population_label:string;population_definition:string;population_inclusion?:string;population_exclusion?:string;setting:string;geography?:string;time_horizon:string;outcome_name:string;outcome_definition:string;feature_of_interest:string;procedure:string;phenomenon_time:string;result_time:string;result_value:number;quality_note?:string;source_refs:string[];now?:()=>string;id?:()=>string};

const defaultId=()=>crypto.randomUUID();
const clean=(value:string)=>value.trim();
const verbatim=(value:string):Copy=>({ro:clean(value),en:clean(value)});
const required=(value:string,name:string)=>{const result=clean(value);if(!result)throw new Error(`${name} is required`);return result;};
const uniqueRefs=(values:string[])=>[...new Set(values.map(clean).filter(Boolean))];
function indicatorFor(indicators:IndicatorProjection,id:string):IndicatorDefinition{const definition=indicators.indicators.find(item=>item.definition.id===id)?.definition;if(!definition)throw new Error('indicator reference is not available in the current IndicatorProjection');return definition;}
function parseTime(value:string,name:string):number{const parsed=Date.parse(value);if(!Number.isFinite(parsed))throw new Error(`${name} must be a valid date-time`);return parsed;}

export function validateObservedOutcomeReferences(record:ObservedOutcome,plan:ImplementationPlan,indicators:IndicatorProjection):void{
 if(plan.object_type!=='ImplementationPlan')throw new Error('referenced record is not an ImplementationPlan');
 if(record.case_id!==plan.case_id)throw new Error('ObservedOutcome case_id does not match ImplementationPlan');
 if(record.implementation_plan_id!==plan.id)throw new Error('ObservedOutcome ImplementationPlan reference mismatch');
 if(record.prospective_snapshot_id!==plan.prospective_snapshot.id)throw new Error('ObservedOutcome ProspectiveSnapshot reference mismatch');
 if(!plan.indicator_ids.includes(record.indicator_id))throw new Error('ObservedOutcome Indicator is not frozen into the ImplementationPlan');
 const definition=indicatorFor(indicators,record.indicator_id);
 if(record.observed_property!==definition.observed_property)throw new Error('ObservedOutcome observed_property does not match Indicator definition');
 if(record.outcome.stage!==definition.target_stage)throw new Error('ObservedOutcome outcome stage does not match Indicator definition');
 if(definition.unit&&record.result.unit!==definition.unit)throw new Error('ObservedOutcome result unit does not match Indicator definition');
 if(definition.target_stage==='PROXIMAL'&&!plan.action_canvas.proximal_result.indicator_ids.includes(record.indicator_id))throw new Error('ObservedOutcome Indicator is not linked to the frozen proximal Action Canvas stage');
 if(definition.target_stage==='INTERMEDIATE'&&!plan.action_canvas.intermediate_result.indicator_ids.includes(record.indicator_id))throw new Error('ObservedOutcome Indicator is not linked to the frozen intermediate Action Canvas stage');
 if(definition.target_stage==='FINAL'&&!plan.action_canvas.final_outcome.indicator_ids.includes(record.indicator_id))throw new Error('ObservedOutcome Indicator is not linked to the frozen final Action Canvas stage');
}

export function materializeObservedOutcome(input:ObservedOutcomeInput):ObservedOutcome{
 const definition=indicatorFor(input.indicators,input.indicator_id);
 if(input.plan.plan_scope!=='ILLUSTRATIVE')throw new Error('this recorder slice accepts only the current illustrative ImplementationPlan');
 if(!input.plan.indicator_ids.includes(definition.id))throw new Error('selected Indicator is not part of the frozen ImplementationPlan');
 const populationLabel=required(input.population_label,'population label');const populationDefinition=required(input.population_definition,'population definition');const setting=required(input.setting,'context setting');const timeHorizon=required(input.time_horizon,'time horizon');const outcomeName=required(input.outcome_name,'outcome name');const outcomeDefinition=required(input.outcome_definition,'outcome definition');const feature=required(input.feature_of_interest,'feature of interest');const procedure=required(input.procedure,'procedure');
 const sourceRefs=uniqueRefs(input.source_refs);if(sourceRefs.length===0)throw new Error('at least one source reference is required');if(!Number.isFinite(input.result_value))throw new Error('result value must be finite');if(definition.unit==='probability'&&(input.result_value<0||input.result_value>1))throw new Error('probability result must be between 0 and 1');
 const phenomenonMs=parseTime(input.phenomenon_time,'phenomenon_time');const resultMs=parseTime(input.result_time,'result_time');const recordedAt=(input.now??(()=>new Date().toISOString()))();const recordedMs=parseTime(recordedAt,'recorded_at');if(phenomenonMs>resultMs)throw new Error('phenomenon_time must not be after result_time');if(resultMs>recordedMs)throw new Error('result_time must not be in the future relative to recorded_at');
 const token=(input.id??defaultId)();
 const record:ObservedOutcome={object_type:'ObservedOutcome',id:`CEM.OBSERVED.OUTCOME.${token}`,case_id:input.plan.case_id,implementation_plan_id:input.plan.id,prospective_snapshot_id:input.plan.prospective_snapshot.id,indicator_id:definition.id,population:{label:verbatim(populationLabel),definition:verbatim(populationDefinition),...(clean(input.population_inclusion??'')?{inclusion:clean(input.population_inclusion!)}:{}),...(clean(input.population_exclusion??'')?{exclusion:clean(input.population_exclusion!)}:{})},context:{setting:verbatim(setting),...(clean(input.geography??'')?{geography:clean(input.geography!)}:{}),time_horizon:timeHorizon},outcome:{name:verbatim(outcomeName),definition:verbatim(outcomeDefinition),stage:definition.target_stage},feature_of_interest:feature,observed_property:definition.observed_property,procedure,phenomenon_time:new Date(phenomenonMs).toISOString(),result_time:new Date(resultMs).toISOString(),result:{value:input.result_value,...(definition.unit?{unit:definition.unit}:{}),...(clean(input.quality_note??'')?{quality_note:clean(input.quality_note!)}:{})},source_refs:sourceRefs,recorded_at:new Date(recordedMs).toISOString(),retrospective:true,mutation_policy:'APPEND_ONLY_NO_RETROACTIVE_PREDICTION_EDIT'};
 validateObservedOutcomeReferences(record,input.plan,input.indicators);return record;
}
