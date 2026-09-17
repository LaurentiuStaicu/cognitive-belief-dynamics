import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {uncertaintyCanonicalContext,type DecisionUncertaintyRegistry} from '../src/decision-uncertainty-contract.ts';

const variables=JSON.parse(await readFile(new URL('../../model/variables.json',import.meta.url),'utf8')) as {id:string}[];
const theory=JSON.parse(await readFile(new URL('../../model/theory_index.json',import.meta.url),'utf8')) as {source_paths:{en:string}}[];
const registry=JSON.parse(await readFile(new URL('../../model/contracts/decision_uncertainty_v1.json',import.meta.url),'utf8')) as DecisionUncertaintyRegistry;

test('OA-6C canonical context links only to existing Semantic Spine entities and a real Theory chapter',()=>{const ids=new Set(variables.map(item=>item.id));for(const id of uncertaintyCanonicalContext.semanticIds)assert(ids.has(id),id);assert(theory.some(item=>item.source_paths.en.endsWith('/12-interventions.md')));assert.equal(uncertaintyCanonicalContext.theorySlug,'interventions');});
test('OA-6C registry remains explicitly non-probabilistic for all initial uncertainty objects',()=>{assert.equal(registry.probability_policy.infer_probabilities,false);assert.equal(registry.probability_policy.expected_value_requires_explicit_probabilities,true);assert(registry.uncertainties.every(item=>item.probability_status==='NOT_AVAILABLE'));assert.equal(registry.uncertainties.filter(item=>item.quantification_status==='FINITE_SCENARIOS').length,2);});
