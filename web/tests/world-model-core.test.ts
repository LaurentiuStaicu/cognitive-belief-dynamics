import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {worldModelPosterior,binaryEntropy} from '../src/core/world-model.ts';

const contract=JSON.parse(await readFile(new URL('../../model/contracts/world_model_v1.json',import.meta.url),'utf8'));

test('MOD.14 contract preserves all four epistemic levels',()=>{const levels=new Set(contract.epistemic_levels.map((item:{level:string})=>item.level));assert.deepEqual(levels,new Set(['EMPIRICAL','EXECUTABLE','CONCEPTUAL','INTERPRETIVE']));});
test('MOD.14 executable posterior remains a normative Bayes calculation',()=>{assert.equal(worldModelPosterior(0,3),0);assert.equal(worldModelPosterior(1,3),1);assert(Math.abs(worldModelPosterior(0.3,3)-0.5625)<1e-12);assert.throws(()=>worldModelPosterior(-0.1,3),/prior/);assert.throws(()=>worldModelPosterior(0.3,0),/likelihood ratio/);});
test('MOD.14 binary entropy remains bounded at the probability endpoints',()=>{assert.equal(binaryEntropy(0),0);assert.equal(binaryEntropy(1),0);assert(Math.abs(binaryEntropy(0.5)-1)<1e-12);assert.throws(()=>binaryEntropy(1.1),/probability/);});
test('MOD.14 contract preserves Phase M and blocked human work boundary',()=>{const limits=contract.limitations.join(' ').toLowerCase();assert(limits.includes('m1.e4'));assert(limits.includes('pencode'));assert(limits.includes('human recruitment'));assert(limits.includes('phase m remains unchanged'));});
