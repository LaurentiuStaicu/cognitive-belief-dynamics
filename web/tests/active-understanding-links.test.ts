import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {challengeModelLearningLinks,deriveActiveLearningLinks,type ActiveTheoryChapter} from '../src/active-understanding-links.ts';

const contract=JSON.parse(await readFile(new URL('../../model/contracts/active_understanding_v1.json',import.meta.url),'utf8')) as {challenges:{id:string;worked_example_refs:string[];canonical_target_refs:string[];canonical_relation_refs:string[]}[]};
const theory=JSON.parse(await readFile(new URL('../../model/theory_index.json',import.meta.url),'utf8')) as ActiveTheoryChapter[];

test('OA-5D derives Theory/Search/Inspector links for all three required foundation families',()=>{
 const links=Object.fromEntries(contract.challenges.map(challenge=>[challenge.id,deriveActiveLearningLinks(challenge,theory)]));
 assert.deepEqual(Object.keys(links),['AU-1','AU-2','AU-3']);
 assert.deepEqual(links['AU-1'],{theorySlug:'repetition-familiarity-truth',searchQuery:'VAR.EXPOSURE.COUNT',inspectorId:'COMPDEP.EXPOSURE.FAMILIARITY'});
 assert.deepEqual(links['AU-2'],{theorySlug:'belief-accuracy-action',searchQuery:'COMP.NODE.ACCURACY_CUE_INPUT',inspectorId:'COMPDEP.ACCURACY_CUE.ACCURACY_SALIENCE'});
 assert.deepEqual(links['AU-3'],{theorySlug:'repetition-familiarity-truth',searchQuery:'VAR.EXPOSURE.COUNT',inspectorId:'COMPDEP.EXPOSURE.FAMILIARITY'});
});

test('OA-5D Challenge Model links stay on the registered M1.E3 semantic objects',()=>{
 assert.deepEqual(challengeModelLearningLinks,{theorySlug:'algorithms-social-feedback',searchQuery:'VAR.HEADLINE.NEGATIVITY',inspectorId:'VAR.ACCESS.PROBABILITY'});
});
