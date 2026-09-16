import type {StructuredTriggerCondition} from './adaptive-plan-runtime';
import type {ImplementationPlan} from './implementation-plan';
import type {IndicatorProjection} from './indicator-objects';
import type {ObservedOutcome} from './observed-outcome';

type Lang='ro'|'en';

export type TriggerEvaluationStatus='TRIGGER_MET'|'TRIGGER_NOT_MET'|'NOT_EVALUABLE';
export type TriggerEvaluationReason=
 'COMPARISON_TRUE'|
 'COMPARISON_FALSE'|
 'INDICATOR_MISMATCH'|
 'UNIT_MISMATCH'|
 'PRE_SNAPSHOT_PHENOMENON'|
 'INVALID_TIME'|
 'REFERENCE_VALIDATION_FAILED';

export type TriggerEvaluation={
 object_type:'TriggerEvaluation';
 persistence:'DERIVED_NOT_STORED';
 automation:'NO_AUTOMATIC_ACTIONS';
 implementation_plan_id:string;
 prospective_snapshot_id:string;
 observed_outcome_id:string;
 indicator_id:string;
 comparator:StructuredTriggerCondition['comparator'];
 threshold:number;
 unit:string;
 observed_value:number;
 phenomenon_time:string;
 result_time:string;
 status:TriggerEvaluationStatus;
 reason:TriggerEvaluationReason;
};

export type TriggerEvaluationProjection={
 object_type:'TriggerEvaluationProjection';
 source:'PERSISTED_OBSERVED_OUTCOME_ONLY';
 persistence:'DERIVED_NOT_STORED';
 automation:'NO_AUTOMATIC_ACTIONS';
 implementation_plan_id:string;
 prospective_snapshot_id:string;
 trigger:StructuredTriggerCondition;
 evaluations:TriggerEvaluation[];
};

function frozenTrigger(plan:ImplementationPlan):StructuredTriggerCondition{
 const iff=plan.adaptive_plan.find(step=>step.phase==='IF');
 if(!iff?.trigger)throw new Error('ImplementationPlan has no frozen structured trigger');
 return iff.trigger;
}

function compare(value:number,trigger:StructuredTriggerCondition):boolean{
 switch(trigger.comparator){
  case 'LT': return value<trigger.threshold;
  case 'LTE': return value<=trigger.threshold;
  case 'GTE': return value>=trigger.threshold;
  case 'GT': return value>trigger.threshold;
 }
 throw new Error('unsupported trigger comparator');
}

function referencesValid(plan:ImplementationPlan,outcome:ObservedOutcome,indicators:IndicatorProjection):boolean{
 if(plan.object_type!=='ImplementationPlan')return false;
 if(outcome.case_id!==plan.case_id)return false;
 if(outcome.implementation_plan_id!==plan.id)return false;
 if(outcome.prospective_snapshot_id!==plan.prospective_snapshot.id)return false;
 if(!plan.indicator_ids.includes(outcome.indicator_id))return false;
 const definition=indicators.indicators.find(item=>item.definition.id===outcome.indicator_id)?.definition;
 if(!definition)return false;
 if(outcome.observed_property!==definition.observed_property)return false;
 if(outcome.outcome.stage!==definition.target_stage)return false;
 if(definition.unit&&outcome.result.unit!==definition.unit)return false;
 if(definition.target_stage==='PROXIMAL'&&!plan.action_canvas.proximal_result.indicator_ids.includes(outcome.indicator_id))return false;
 if(definition.target_stage==='INTERMEDIATE'&&!plan.action_canvas.intermediate_result.indicator_ids.includes(outcome.indicator_id))return false;
 if(definition.target_stage==='FINAL'&&!plan.action_canvas.final_outcome.indicator_ids.includes(outcome.indicator_id))return false;
 return true;
}

function notEvaluable(
 plan:ImplementationPlan,
 outcome:ObservedOutcome,
 trigger:StructuredTriggerCondition,
 reason:Exclude<TriggerEvaluationReason,'COMPARISON_TRUE'|'COMPARISON_FALSE'>
):TriggerEvaluation{
 return {
  object_type:'TriggerEvaluation',
  persistence:'DERIVED_NOT_STORED',
  automation:'NO_AUTOMATIC_ACTIONS',
  implementation_plan_id:plan.id,
  prospective_snapshot_id:plan.prospective_snapshot.id,
  observed_outcome_id:outcome.id,
  indicator_id:outcome.indicator_id,
  comparator:trigger.comparator,
  threshold:trigger.threshold,
  unit:trigger.unit,
  observed_value:outcome.result.value,
  phenomenon_time:outcome.phenomenon_time,
  result_time:outcome.result_time,
  status:'NOT_EVALUABLE',
  reason
 };
}

export function evaluateObservedOutcomeAgainstFrozenTrigger(input:{
 plan:ImplementationPlan;
 outcome:ObservedOutcome;
 indicators:IndicatorProjection;
}):TriggerEvaluation{
 const {plan,outcome,indicators}=input;
 const trigger=frozenTrigger(plan);
 if(!referencesValid(plan,outcome,indicators)){
  return notEvaluable(plan,outcome,trigger,'REFERENCE_VALIDATION_FAILED');
 }
 if(outcome.indicator_id!==trigger.indicator_id)return notEvaluable(plan,outcome,trigger,'INDICATOR_MISMATCH');
 if(outcome.result.unit!==trigger.unit)return notEvaluable(plan,outcome,trigger,'UNIT_MISMATCH');
 const frozenAt=Date.parse(plan.prospective_snapshot.frozen_at);
 const phenomenon=Date.parse(outcome.phenomenon_time);
 const resultTime=Date.parse(outcome.result_time);
 if(!Number.isFinite(frozenAt)||!Number.isFinite(phenomenon)||!Number.isFinite(resultTime)){
  return notEvaluable(plan,outcome,trigger,'INVALID_TIME');
 }
 if(phenomenon<frozenAt)return notEvaluable(plan,outcome,trigger,'PRE_SNAPSHOT_PHENOMENON');
 const met=compare(outcome.result.value,trigger);
 return {
  object_type:'TriggerEvaluation',
  persistence:'DERIVED_NOT_STORED',
  automation:'NO_AUTOMATIC_ACTIONS',
  implementation_plan_id:plan.id,
  prospective_snapshot_id:plan.prospective_snapshot.id,
  observed_outcome_id:outcome.id,
  indicator_id:outcome.indicator_id,
  comparator:trigger.comparator,
  threshold:trigger.threshold,
  unit:trigger.unit,
  observed_value:outcome.result.value,
  phenomenon_time:outcome.phenomenon_time,
  result_time:outcome.result_time,
  status:met?'TRIGGER_MET':'TRIGGER_NOT_MET',
  reason:met?'COMPARISON_TRUE':'COMPARISON_FALSE'
 };
}

export function buildTriggerEvaluationProjection(input:{
 plan:ImplementationPlan;
 outcomes:ObservedOutcome[];
 indicators:IndicatorProjection;
}):TriggerEvaluationProjection{
 const trigger=frozenTrigger(input.plan);
 const outcomes=[...input.outcomes]
  .filter(item=>item.object_type==='ObservedOutcome'&&item.implementation_plan_id===input.plan.id)
  .sort((a,b)=>a.result_time.localeCompare(b.result_time)||a.id.localeCompare(b.id));
 return {
  object_type:'TriggerEvaluationProjection',
  source:'PERSISTED_OBSERVED_OUTCOME_ONLY',
  persistence:'DERIVED_NOT_STORED',
  automation:'NO_AUTOMATIC_ACTIONS',
  implementation_plan_id:input.plan.id,
  prospective_snapshot_id:input.plan.prospective_snapshot.id,
  trigger:{...trigger},
  evaluations:outcomes.map(outcome=>evaluateObservedOutcomeAgainstFrozenTrigger({
   plan:input.plan,outcome,indicators:input.indicators
  }))
 };
}

const esc=(value:string)=>value.replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]??c));
const symbol=(value:StructuredTriggerCondition['comparator'])=>({LT:'<',LTE:'≤',GTE:'≥',GT:'>'}[value]);

export function mountTriggerEvaluation(
 host:HTMLElement,
 input:{plan:ImplementationPlan;outcomes:ObservedOutcome[];indicators:IndicatorProjection;lang:Lang}
):TriggerEvaluationProjection{
 const projection=buildTriggerEvaluationProjection(input);
 const t=(ro:string,en:string)=>input.lang==='ro'?ro:en;
 const rows=projection.evaluations.map(item=>`<tr data-trigger-evaluation="${esc(item.observed_outcome_id)}" data-trigger-status="${item.status}">
  <td><code>${esc(item.observed_outcome_id)}</code></td>
  <td>${esc(item.indicator_id)}</td>
  <td>${item.observed_value}</td>
  <td>${symbol(item.comparator)} ${item.threshold}</td>
  <td><strong>${item.status}</strong><br><small>${item.reason}</small></td>
 </tr>`).join('');
 host.innerHTML=`<section id="triggerEvaluation" data-plan-id="${esc(projection.implementation_plan_id)}" data-automation="${projection.automation}">
  <div class="section-heading"><div><p class="eyebrow">OA-7 · OBSERVED TRIGGER EVALUATION</p><h4>${t('Evaluează trigger-ul pe observații persistate','Evaluate the trigger on persisted observations')}</h4><p>${t('Comparația este read-only și folosește numai ObservedOutcome din IndexedDB. Nu execută THEN / STOP / REASSESS și nu modifică planul prospectiv.','The comparison is read-only and uses only ObservedOutcome records from IndexedDB. It does not execute THEN / STOP / REASSESS and does not modify the prospective plan.')}</p></div><span class="planner-badge">DERIVED · NO AUTOMATION</span></div>
  <p><strong>${t('Trigger înghețat','Frozen trigger')}:</strong> ${esc(projection.trigger.indicator_id)} ${symbol(projection.trigger.comparator)} ${projection.trigger.threshold} ${esc(projection.trigger.unit)}</p>
  ${rows?`<div class="table-scroll"><table><thead><tr><th>ObservedOutcome</th><th>Indicator</th><th>${t('Valoare','Value')}</th><th>IF</th><th>${t('Evaluare','Evaluation')}</th></tr></thead><tbody>${rows}</tbody></table></div>`:`<p class="note" data-trigger-empty="true">${t('Nu există încă ObservedOutcome persistat pentru acest plan. Trigger-ul rămâne neevaluat.','No persisted ObservedOutcome exists for this plan yet. The trigger remains unevaluated.')}</p>`}
  <div class="boundary"><strong>${projection.automation}</strong><p>${t('TRIGGER_MET înseamnă doar că observația satisface condiția IF declarată prospectiv. Este un semnal pentru revizuire umană, nu o comandă de executare. Observațiile al căror phenomenon_time precede snapshotul sunt NOT_EVALUABLE.','TRIGGER_MET only means that the observation satisfies the prospectively declared IF condition. It is a signal for human review, not an execution command. Observations whose phenomenon_time predates the snapshot are NOT_EVALUABLE.')}</p></div>
 </section>`;
 return projection;
}
