import test from 'node:test';
import assert from 'node:assert/strict';
import {buildIndicatorProjection} from '../src/indicator-objects.ts';
import {buildSignpostProjection,createTriggerDraft} from '../src/signposts-triggers.ts';
import {buildAdaptivePlanDraft} from '../src/adaptive-plan-runtime.ts';

const indicators=buildIndicatorProjection({false_share:0.3,true_share:0.7});
const signposts=buildSignpostProjection(indicators);
const trigger=createTriggerDraft({signpost:signposts.signposts[0],comparator:'LTE',threshold:0.35});
const bundle_label={ro:'Context corectiv verificat',en:'Verified corrective context'};

test('OA-7 adaptive plan exposes exactly the canonical six phases',()=>{
 const plan=buildAdaptivePlanDraft({bundle_label,signpost:signposts.signposts[0],trigger,actions:{
  then_action:{ro:'Aplică acțiunea contingentă',en:'Apply contingent action'},
  stop_action:{ro:'Oprește intervenția',en:'Stop the intervention'},
  reassess_action:{ro:'Reevaluează decizia',en:'Reassess the decision'}
 }});
 assert.deepEqual(plan.steps.map(item=>item.phase),['NOW','WATCH','IF','THEN','STOP','REASSESS']);
 assert.equal(plan.persistence,'EPHEMERAL_NOT_WORKSPACE');
 assert.equal(plan.execution_status,'DESIGN_ONLY_NO_OBSERVED_OUTCOME');
 assert.equal(plan.automation,'NO_AUTOMATIC_ACTIONS');
});

test('OA-7 WATCH and IF bind to signpost/trigger while actions remain user declarations',()=>{
 const plan=buildAdaptivePlanDraft({bundle_label,signpost:signposts.signposts[0],trigger,actions:{
  then_action:{ro:'A',en:'A'},stop_action:{ro:'B',en:'B'},reassess_action:{ro:'C',en:'C'}
 }});
 const watch=plan.steps.find(item=>item.phase==='WATCH')!;
 const iff=plan.steps.find(item=>item.phase==='IF')!;
 assert.equal(watch.indicator_id,trigger.indicator_id);
 assert.equal(iff.trigger_draft_id,trigger.id);
 assert.match(iff.trigger_condition!.en,/user-declared threshold/i);
 for(const phase of ['THEN','STOP','REASSESS'] as const){
  assert.equal(plan.steps.find(item=>item.phase===phase)!.readiness,'DEFINED');
 }
});

test('OA-7 adaptive plan fails incomplete rather than inventing trigger or contingent actions',()=>{
 const plan=buildAdaptivePlanDraft({bundle_label,signpost:signposts.signposts[0]});
 assert.equal(plan.steps.find(item=>item.phase==='IF')!.readiness,'MISSING_TRIGGER');
 assert.equal(plan.steps.find(item=>item.phase==='THEN')!.readiness,'MISSING_ACTION');
 assert.equal(plan.steps.find(item=>item.phase==='STOP')!.readiness,'MISSING_ACTION');
 assert.equal(plan.steps.find(item=>item.phase==='REASSESS')!.readiness,'MISSING_ACTION');
 assert.equal('executed' in plan,false);
 assert.equal('observed_outcome_id' in plan,false);
});
