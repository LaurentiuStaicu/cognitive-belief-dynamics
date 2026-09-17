import test from 'node:test';
import assert from 'node:assert/strict';
import {buildActionCanvasProjection} from '../src/core/action-canvas.ts';
import {buildIndicatorProjection} from '../src/core/indicator-objects.ts';
import {buildSignpostProjection,createTriggerDraft} from '../src/core/signposts-triggers.ts';
import {buildAdaptivePlanDraft} from '../src/core/adaptive-plan-runtime.ts';
import {isAdaptivePlanReadyForFreeze,materializeIllustrativeImplementationPlan} from '../src/implementation-plan.ts';

const bundle={mask:2,false_share:0.30,true_share:0.70};
const baseline={mask:0,false_share:0.40,true_share:0.65};
const levers=[{id:'correction',bit:2,label:{ro:'Context corectiv verificat',en:'Verified corrective context'},factor:'C -> B',action:{ro:'Aplică context verificat',en:'Apply verified context'}}];
const canvas=buildActionCanvasProjection({bundle,baseline,levers});
const indicators=buildIndicatorProjection(bundle);
const signpost=buildSignpostProjection(indicators).signposts[0];
const trigger=createTriggerDraft({signpost,comparator:'LTE',threshold:0.35});
const completeAdaptive=buildAdaptivePlanDraft({bundle_label:{ro:'Context corectiv verificat',en:'Verified corrective context'},signpost,trigger,actions:{then_action:{ro:'Reanalizează opțiunea',en:'Reanalyse the option'},stop_action:{ro:'Oprește aplicarea',en:'Stop implementation'},reassess_action:{ro:'Creează o revizie nouă',en:'Create a new revision'}}});

test('OA-7 materializes a canonical illustrative ImplementationPlan with frozen snapshot',()=>{const plan=materializeIllustrativeImplementationPlan({case_id:'CEM.CASE.test',action_canvas:canvas,indicators,adaptive_plan:completeAdaptive,now:()=> '2026-09-16T18:30:00Z',id:()=> 'plan-test'});assert.equal(plan.object_type,'ImplementationPlan');assert.equal(plan.id,'CEM.IMPLEMENTATION.PLAN.plan-test');assert.equal(plan.decision_analysis_id,'CEM.DECISION.ANALYSIS.RUNTIME.plan-test');assert.deepEqual(plan.prospective_snapshot,{id:'CEM.PROSPECTIVE.SNAPSHOT.plan-test',frozen_at:'2026-09-16T18:30:00Z',revision_policy:'APPEND_ONLY_NO_RETROACTIVE_EDIT'});assert.equal(plan.plan_scope,'ILLUSTRATIVE');assert.equal(plan.status,'DRAFT');assert.deepEqual(plan.indicator_ids,['CEM.INDICATOR.M0.FALSE_SHARING.MEAN13','CEM.INDICATOR.M0.TRUE_SHARING.MEAN13']);assert.deepEqual(plan.action_canvas.proximal_result.indicator_ids,plan.indicator_ids);assert.deepEqual(plan.action_canvas.intermediate_result.indicator_ids,[]);assert.deepEqual(plan.action_canvas.final_outcome.indicator_ids,[]);assert.deepEqual(plan.adaptive_plan.map(item=>item.phase),['NOW','WATCH','IF','THEN','STOP','REASSESS']);assert.equal('readiness' in plan.adaptive_plan[0],false);assert.equal('trigger_draft_id' in plan.adaptive_plan[2],false);assert.deepEqual(plan.adaptive_plan[2].trigger,{indicator_id:'CEM.INDICATOR.M0.FALSE_SHARING.MEAN13',comparator:'LTE',threshold:0.35,unit:'probability',origin:'USER_DECLARED'});});
test('OA-7 refuses to freeze incomplete adaptive drafts',()=>{const incomplete=buildAdaptivePlanDraft({bundle_label:{ro:'x',en:'x'},signpost});assert.equal(isAdaptivePlanReadyForFreeze(incomplete),false);assert.throws(()=>materializeIllustrativeImplementationPlan({case_id:'CEM.CASE.test',action_canvas:canvas,indicators,adaptive_plan:incomplete,id:()=> 'x',now:()=> '2026-09-16T18:30:00Z'}),/not defined/);});
test('OA-7 freeze readiness becomes true only for the complete six-phase draft',()=>{assert.equal(isAdaptivePlanReadyForFreeze(completeAdaptive),true);});
