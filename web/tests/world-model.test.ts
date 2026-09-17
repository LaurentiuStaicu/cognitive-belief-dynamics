import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';

const contract=JSON.parse(await readFile(new URL('../../model/contracts/world_model_v1.json',import.meta.url),'utf8'));
const source=await readFile(new URL('../src/world-model.ts',import.meta.url),'utf8');
const understanding=await readFile(new URL('../src/understanding.ts',import.meta.url),'utf8');
const overview=await readFile(new URL('../src/suite-overview.ts',import.meta.url),'utf8');

test('MOD.14 UI exposes all epistemic levels and a mechanism-first InfoClar surface',()=>{
 const levels=new Set(contract.epistemic_levels.map((item:{level:string})=>item.level));
 assert.deepEqual(levels,new Set(['EMPIRICAL','EXECUTABLE','CONCEPTUAL','INTERPRETIVE']));
 assert(source.includes('MECHANISM VISUALIZATION'));
 assert(source.includes('THEORY / LEARN'));
 assert(source.includes('DASHBOARD · EXECUTABLE REFERENCE'));
 assert(source.includes('EVIDENCE · LIMITS · CROSS-LINKS'));
});

test('MOD.14 is reachable from the shared Theory/Learn architecture',()=>{
 assert(understanding.includes("'world-model'"));
 assert(understanding.includes('mountWorldModel'));
 assert(overview.includes('data-suite-learn="world-model"'));
});

test('MOD.14 browser calculator keeps normative posterior distinct from belief B',()=>{
 assert(source.includes('not an estimate of B'));
 assert(source.includes('fails closed'));
 assert(source.includes('likelihood ratio'));
 assert(!source.includes('Pencode='));
});

test('MOD.14 contract preserves Phase M and blocked human work boundary',()=>{
 const limits=contract.limitations.join(' ').toLowerCase();
 assert(limits.includes('m1.e4'));
 assert(limits.includes('pencode'));
 assert(limits.includes('human recruitment'));
 assert(limits.includes('phase m remains unchanged'));
});
