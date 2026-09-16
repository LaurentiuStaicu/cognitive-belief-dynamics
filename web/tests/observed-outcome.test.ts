import test from 'node:test';
import assert from 'node:assert/strict';
import {buildActionCanvasProjection} from '../src/action-canvas.ts';
import {buildIndicatorProjection} from '../src/indicator-objects.ts';
import {buildSignpostProjection,createTriggerDraft} from '../src/signposts-triggers.ts';
import {buildAdaptivePlanDraft} from '../src/adaptive-plan-runtime.ts';
import {materializeIllustrativeImplementationPlan} from '../src/implementation-plan.ts';
import {materializeObservedOutcome,validateObservedOutcomeReferences} from '../src/observed-outcome.ts';

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
 case_id:'CEM.CASE.observation-test',
 action_canvas:canvas,
 indicators,
 adaptive_plan:adaptive,
 now:()=> '2026-09-16T18:30:00Z',
 id:()=> 'observation-plan'
});

const validInput=()=>({
 plan,
 indicators,
 indicator_id:'CEM.INDICATOR.M0.FALSE_SHARING.MEAN13',
 population_label:'Cohortă demonstrativă',
 population_definition:'Participanți pentru o observație introdusă manual',
 setting:'Cadru demonstrativ',
 geography:'RO',
 time_horizon:'30 days',
 outcome_name:'Distribuire falsă observată',
 outcome_definition:'Măsurare retrospectivă declarată de utilizator',
 feature_of_interest:'declared participant cohort',
 procedure:'manual retrospective measurement protocol',
 phenomenon_time:'2026-09-16T17:00:00Z',
 result_time:'2026-09-16T18:00:00Z',
 result_value:0.31,
 quality_note:'illustrative manual entry',
 source_refs:['source:A','source:A','source:B'],
 now:()=> '2026-09-16T18:45:00Z',
 id:()=> 'outcome-test'
});

test('OA-7 materializes a retrospective append-only ObservedOutcome without copying simulation values',()=>{
 const record=materializeObservedOutcome(validInput());
 assert.equal(record.object_type,'ObservedOutcome');
 assert.equal(record.id,'CEM.OBSERVED.OUTCOME.outcome-test');
 assert.equal(record.implementation_plan_id,plan.id);
 assert.equal(record.prospective_snapshot_id,plan.prospective_snapshot.id);
 assert.equal(record.indicator_id,'CEM.INDICATOR.M0.FALSE_SHARING.MEAN13');
 assert.equal(record.observed_property,'M0.SIMULATED.FALSE_SHARING.PROBABILITY.MEAN13');
 assert.equal(record.outcome.stage,'PROXIMAL');
 assert.equal(record.result.value,0.31);
 assert.equal(record.result.unit,'probability');
 assert.deepEqual(record.source_refs,['source:A','source:B']);
 assert.equal(record.retrospective,true);
 assert.equal(record.mutation_policy,'APPEND_ONLY_NO_RETROACTIVE_PREDICTION_EDIT');
 assert.equal(record.recorded_at,'2026-09-16T18:45:00.000Z');
 assert.equal(record.population.label.ro,record.population.label.en);
 assert.notEqual(record.result.value,bundle.false_share,'manual observation must not be copied from simulation reading');
});

test('OA-7 fails closed when plan, snapshot or Indicator references do not match',()=>{
 const record=materializeObservedOutcome(validInput());
 assert.throws(()=>validateObservedOutcomeReferences({...record,implementation_plan_id:'CEM.IMPLEMENTATION.PLAN.other'},plan,indicators),/ImplementationPlan reference mismatch/);
 assert.throws(()=>validateObservedOutcomeReferences({...record,prospective_snapshot_id:'CEM.PROSPECTIVE.SNAPSHOT.other'},plan,indicators),/ProspectiveSnapshot reference mismatch/);
 assert.throws(()=>validateObservedOutcomeReferences({...record,indicator_id:'CEM.INDICATOR.other'},plan,indicators),/not frozen/);
});

test('OA-7 rejects missing sources, future results, reversed times and invalid probability values',()=>{
 assert.throws(()=>materializeObservedOutcome({...validInput(),source_refs:[]}),/source reference/);
 assert.throws(()=>materializeObservedOutcome({...validInput(),result_value:1.2}),/between 0 and 1/);
 assert.throws(()=>materializeObservedOutcome({...validInput(),phenomenon_time:'2026-09-16T18:10:00Z',result_time:'2026-09-16T18:00:00Z'}),/must not be after/);
 assert.throws(()=>materializeObservedOutcome({...validInput(),result_time:'2026-09-16T19:00:00Z'}),/future/);
});
