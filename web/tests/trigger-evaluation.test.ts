import test from 'node:test';
import assert from 'node:assert/strict';
import {buildActionCanvasProjection} from '../src/action-canvas.ts';
import {buildIndicatorProjection} from '../src/indicator-objects.ts';
import {buildSignpostProjection,createTriggerDraft} from '../src/signposts-triggers.ts';
import {buildAdaptivePlanDraft} from '../src/adaptive-plan-runtime.ts';
import {materializeIllustrativeImplementationPlan} from '../src/implementation-plan.ts';
import {materializeObservedOutcome} from '../src/observed-outcome.ts';
import {buildTriggerEvaluationProjection,evaluateObservedOutcomeAgainstFrozenTrigger} from '../src/trigger-evaluation.ts';

const bundle={mask:2,false_share:0.30,true_share:0.70};
const baseline={mask:0,false_share:0.40,true_share:0.65};
const levers=[{id:'correction',bit:2,label:{ro:'Context corectiv verificat',en:'Verified corrective context'},factor:'C -> B',action:{ro:'Aplică context verificat',en:'Apply verified context'}}];
const canvas=buildActionCanvasProjection({bundle,baseline,levers});
const indicators=buildIndicatorProjection(bundle);
const signpost=buildSignpostProjection(indicators).signposts[0];
const trigger=createTriggerDraft({signpost,comparator:'LTE',threshold:0.35});
const adaptive=buildAdaptivePlanDraft({
 bundle_label:{ro:'Context corectiv verificat',en:'Verified corrective context'},
 signpost,
 trigger,
 actions:{
  then_action:{ro:'Reanalizează',en:'Reanalyse'},
  stop_action:{ro:'Oprește',en:'Stop'},
  reassess_action:{ro:'Revizuiește',en:'Revise'}
 }
});
const plan=materializeIllustrativeImplementationPlan({
 case_id:'CEM.CASE.trigger-evaluation',
 action_canvas:canvas,
 indicators,
 adaptive_plan:adaptive,
 now:()=> '2026-09-16T18:30:00Z',
 id:()=> 'trigger-evaluation-plan'
});

function outcome(input:{
 id:string;
 indicator_id?:string;
 value:number;
 phenomenon_time?:string;
 result_time?:string;
}){
 return materializeObservedOutcome({
  plan,
  indicators,
  indicator_id:input.indicator_id??'CEM.INDICATOR.M0.FALSE_SHARING.MEAN13',
  population_label:'Cohort',
  population_definition:'Manual retrospective cohort',
  setting:'Illustrative setting',
  geography:'RO',
  time_horizon:'30 days',
  outcome_name:'Observed result',
  outcome_definition:'Retrospective manual measurement',
  feature_of_interest:'declared cohort',
  procedure:'manual measurement protocol',
  phenomenon_time:input.phenomenon_time??'2026-09-16T18:31:00Z',
  result_time:input.result_time??'2026-09-16T18:32:00Z',
  result_value:input.value,
  source_refs:['source:manual'],
  now:()=> '2026-09-16T18:45:00Z',
  id:()=> input.id
 });
}

test('OA-7 evaluates a persisted-compatible post-snapshot observation against the frozen structured trigger',()=>{
 const evaluation=evaluateObservedOutcomeAgainstFrozenTrigger({plan,outcome:outcome({id:'met',value:0.31}),indicators});
 assert.equal(evaluation.status,'TRIGGER_MET');
 assert.equal(evaluation.reason,'COMPARISON_TRUE');
 assert.equal(evaluation.comparator,'LTE');
 assert.equal(evaluation.threshold,0.35);
 assert.equal(evaluation.observed_value,0.31);
 assert.equal(evaluation.persistence,'DERIVED_NOT_STORED');
 assert.equal(evaluation.automation,'NO_AUTOMATIC_ACTIONS');

 const notMet=evaluateObservedOutcomeAgainstFrozenTrigger({plan,outcome:outcome({id:'not-met',value:0.40}),indicators});
 assert.equal(notMet.status,'TRIGGER_NOT_MET');
 assert.equal(notMet.reason,'COMPARISON_FALSE');
});

test('OA-7 refuses to confirm a prospective trigger from a pre-snapshot phenomenon',()=>{
 const evaluation=evaluateObservedOutcomeAgainstFrozenTrigger({
  plan,
  outcome:outcome({id:'pre-snapshot',value:0.31,phenomenon_time:'2026-09-16T18:00:00Z',result_time:'2026-09-16T18:10:00Z'}),
  indicators
 });
 assert.equal(evaluation.status,'NOT_EVALUABLE');
 assert.equal(evaluation.reason,'PRE_SNAPSHOT_PHENOMENON');
});

test('OA-7 keeps observations for other plan Indicators non-evaluable for this trigger',()=>{
 const evaluation=evaluateObservedOutcomeAgainstFrozenTrigger({
  plan,
  outcome:outcome({id:'other-indicator',indicator_id:'CEM.INDICATOR.M0.TRUE_SHARING.MEAN13',value:0.72}),
  indicators
 });
 assert.equal(evaluation.status,'NOT_EVALUABLE');
 assert.equal(evaluation.reason,'INDICATOR_MISMATCH');
});

test('OA-7 projection is read-only, deterministic and contains only observations linked to the frozen plan',()=>{
 const matching=outcome({id:'matching',value:0.34,result_time:'2026-09-16T18:34:00Z'});
 const otherPlan={...outcome({id:'other-plan',value:0.34,result_time:'2026-09-16T18:33:00Z'}),implementation_plan_id:'CEM.IMPLEMENTATION.PLAN.other'};
 const projection=buildTriggerEvaluationProjection({plan,outcomes:[otherPlan,matching],indicators});
 assert.equal(projection.source,'PERSISTED_OBSERVED_OUTCOME_ONLY');
 assert.equal(projection.persistence,'DERIVED_NOT_STORED');
 assert.equal(projection.automation,'NO_AUTOMATIC_ACTIONS');
 assert.deepEqual(projection.evaluations.map(item=>item.observed_outcome_id),['CEM.OBSERVED.OUTCOME.matching']);
 assert.equal(projection.evaluations[0].status,'TRIGGER_MET');
 assert.equal('action' in projection.evaluations[0],false);
});
