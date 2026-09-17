import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {buildIndicatorProjection} from '../src/core/indicator-objects.ts';
import {buildSignpostProjection,createTriggerDraft} from '../src/core/signposts-triggers.ts';

type Planning={profiles:{id:string;bundles:{mask:number;start:number;false_share:number;true_share:number}[]}[]};
const planning=JSON.parse(await readFile(new URL('../public/model/interventions.json',import.meta.url),'utf8')) as Planning;
const bundle=planning.profiles.find(item=>item.id==='reference')!.bundles.find(item=>item.mask===6&&item.start===2)!;
const indicators=buildIndicatorProjection(bundle);

test('OA-7 signposts map one-to-one onto operational Indicator objects',()=>{const projection=buildSignpostProjection(indicators);assert.equal(projection.object_type,'SignpostTriggerProjection');assert.equal(projection.persistence,'EPHEMERAL_NOT_WORKSPACE');assert.equal(projection.automation,'NO_BACKGROUND_MONITORING');assert.equal(projection.signposts.length,2);assert.deepEqual(projection.signposts.map(item=>item.indicator_id).sort(),indicators.indicators.map(item=>item.definition.id).sort());assert(projection.signposts.every(item=>item.monitoring_role==='INDICATOR_TO_MONITOR'));});
test('OA-7 trigger draft is user-declared and cannot masquerade as an evaluated observation',()=>{const signpost=buildSignpostProjection(indicators).signposts[0];const draft=createTriggerDraft({signpost,comparator:'LTE',threshold:0.35});assert.equal(draft.origin,'USER_DECLARED');assert.equal(draft.evaluation_status,'NOT_EVALUATED_NO_OBSERVED_OUTCOME');assert.equal(draft.action_binding_status,'NOT_BOUND_TO_ADAPTIVE_ACTION');assert.equal(draft.threshold,0.35);assert.equal(draft.unit,'probability');assert.equal('observed_value' in draft,false);assert.equal('triggered' in draft,false);});
test('OA-7 trigger thresholds fail closed outside the probability domain',()=>{const signpost=buildSignpostProjection(indicators).signposts[0];for(const threshold of [-0.01,1.01,Number.NaN])assert.throws(()=>createTriggerDraft({signpost,comparator:'GTE',threshold}),/within \[0,1\]/);});
