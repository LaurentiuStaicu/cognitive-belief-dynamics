import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {buildActionCanvasProjection} from '../src/core/action-canvas.ts';

type Planning={levers:{id:string;bit:number;label:{ro:string;en:string};factor:string;action:{ro:string;en:string}}[];profiles:{id:string;bundles:{mask:number;start:number;false_share:number;true_share:number}[]}[]};
const planning=JSON.parse(await readFile(new URL('../public/model/interventions.json',import.meta.url),'utf8')) as Planning;
const reference=planning.profiles.find(item=>item.id==='reference')!;
const baseline=reference.bundles.find(item=>item.mask===0&&item.start===2)!;
const bundle=reference.bundles.find(item=>item.mask===6&&item.start===2)!;

test('OA-7 Action Canvas preserves the roadmap six-stage chain',()=>{const canvas=buildActionCanvasProjection({bundle,baseline,levers:planning.levers});assert.deepEqual(canvas.nodes.map(item=>item.stage),['PROBLEM','TARGET_MECHANISM','INTERVENTION','PROXIMAL_RESULT','INTERMEDIATE_RESULT','FINAL_OUTCOME']);assert.equal(canvas.object_type,'ActionCanvasProjection');assert.equal(canvas.persistence,'READ_ONLY_NOT_IMPLEMENTATION_PLAN');assert.equal(canvas.scope,'ILLUSTRATIVE_UNCALIBRATED');});
test('OA-7 Action Canvas uses only selected canonical levers for mechanism and intervention',()=>{const canvas=buildActionCanvasProjection({bundle,baseline,levers:planning.levers});const target=canvas.nodes.find(item=>item.stage==='TARGET_MECHANISM')!;const intervention=canvas.nodes.find(item=>item.stage==='INTERVENTION')!;assert.match(target.detail.en,/Verified corrective context/);assert.match(target.detail.en,/Accuracy cue/);assert.doesNotMatch(target.detail.en,/Reduce repetition/);assert.doesNotMatch(target.detail.en,/Verifiable source feedback/);assert.deepEqual(target.refs.sort(),['intervention-lever:accuracy','intervention-lever:correction']);assert.equal(intervention.status,'CANONICAL_INPUT');});
test('OA-7 Action Canvas labels direct M0 output as simulated and refuses to invent later outcome stages',()=>{const canvas=buildActionCanvasProjection({bundle,baseline,levers:planning.levers});const proximal=canvas.nodes.find(item=>item.stage==='PROXIMAL_RESULT')!;const intermediate=canvas.nodes.find(item=>item.stage==='INTERMEDIATE_RESULT')!;const final=canvas.nodes.find(item=>item.stage==='FINAL_OUTCOME')!;assert.equal(proximal.status,'SIMULATED_OUTPUT');assert.match(proximal.detail.en,/simulation outputs, not observed population effects/i);assert.equal(intermediate.status,'NOT_OPERATIONALIZED');assert.equal(final.status,'NOT_OPERATIONALIZED');assert.deepEqual(intermediate.refs,[]);assert.deepEqual(final.refs,[]);assert.equal('indicator_ids' in intermediate,false);assert.equal('indicator_ids' in final,false);});
