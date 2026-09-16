import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {projectAccessChallenge} from '../src/challenge-model.ts';
import type {M1AccessData} from '../src/access-stage.ts';

const data=JSON.parse(await readFile(new URL('../public/model/m1_access.json',import.meta.url),'utf8')) as M1AccessData;

test('OA-5C projects only the existing M1.E3 NULL versus Hneg comparator',()=>{
 const projection=projectAccessChallenge(data);
 assert.equal(projection.experimentId,'M1.E3');
 assert.equal(projection.purpose,'MODEL_DISCRIMINATION_DEMONSTRATION');
 assert.equal(projection.storyId,data.experiment.conditions.higher_negativity.story_id);
 assert.equal(projection.sourceId,data.experiment.conditions.higher_negativity.source_id);
 assert.equal(projection.imageId,data.experiment.conditions.higher_negativity.image_id);
 assert.equal(projection.previewImpression,true);
 assert.equal(projection.nullModel.lower,projection.nullModel.higher);
 assert.equal(projection.nullModel.delta,0);
 assert(projection.alternativeModel.higher>projection.alternativeModel.lower);
 assert(Math.abs(projection.alternativeModel.delta-0.02264814287837025)<1e-15);
 assert.equal(projection.betaHneg,0.2);
 assert.equal(projection.calibrated,false);
 assert.equal(projection.empiricalTargetId,'TARGET.M1.E3.ROBERTSON_2023');
 assert(projection.validationPatternIds.includes('VAL.M1.004'));
 assert(projection.validationPatternIds.includes('VAL.M1.N04'));
});

test('OA-5C fails closed if the held-fixed context is no longer held fixed',()=>{
 const changed=structuredClone(data);
 changed.experiment.conditions.higher_negativity.story_id='STORY.DIFFERENT';
 assert.throws(()=>projectAccessChallenge(changed),/invariant failed: story_id/);
});

test('OA-5C fails closed if the registered NULL starts responding to Hneg',()=>{
 const changed=structuredClone(data);
 changed.experiment.conditions.higher_negativity.models.null.p_access+=0.01;
 assert.throws(()=>projectAccessChallenge(changed),/NULL comparator/);
});
