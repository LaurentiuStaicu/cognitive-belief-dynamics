import test from 'node:test';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {readFile} from 'node:fs/promises';

const gitBlobSha=(content:Buffer)=>{
 const header=Buffer.from(`blob ${content.length}\0`);
 return createHash('sha1').update(Buffer.concat([header,content])).digest('hex');
};

const scientificBaseline={
 '../public/model/interventions.json':'90092a231d6fe6bb341efd02d381473af2ecd235',
 '../public/model/runs.json':'4fbd9656f4c006644e151c31e47fc78683b99f90',
 '../public/model/explanations.json':'1ae3bc4b580f39160f7574c5626f63bffdd59322',
 '../../model/variables.json':'0aa7f4482634f2f8f733ca42d996d2d6fda39ae4',
 '../../model/links.json':'d81ba2c8c07a3ad5165feaa7be55397b74a366ed'
} as const;

const releaseVersionedArtifacts=new Set([
 '../public/model/interventions.json',
 '../public/model/runs.json',
 '../public/model/explanations.json'
]);

const normalizeReleaseMetadata=(relative:string,content:Buffer)=>{
 if(!releaseVersionedArtifacts.has(relative))return content;
 const current=content.toString('utf8');
 assert(current.includes('0.4.3a0'),`${relative}: current release metadata missing`);
 const normalized=current.replaceAll('0.4.3a0','0.4.2a0');
 assert.equal(normalized.includes('0.4.3a0'),false,`${relative}: unexpected additional current-version payload`);
 return Buffer.from(normalized);
};

test('OA-6E preserves the R7 baseline scientific artifacts byte-for-byte modulo release metadata',async()=>{
 for(const [relative,expected] of Object.entries(scientificBaseline)){
  const content=await readFile(new URL(relative,import.meta.url));
  assert.equal(gitBlobSha(normalizeReleaseMetadata(relative,content)),expected,relative);
 }
});

test('OA-6E keeps the uncertainty registry bilingual and semantically complete',async()=>{
 const registry=JSON.parse(await readFile(new URL('../../model/contracts/decision_uncertainty_v1.json',import.meta.url),'utf8')) as {
  probability_policy:{infer_probabilities:boolean;expected_value_requires_explicit_probabilities:boolean};
  uncertainties:{label:{ro:string;en:string};limitations:{ro:string;en:string};finite_scenarios?:{label:{ro:string;en:string}}[]}[];
 };
 assert.equal(registry.probability_policy.infer_probabilities,false);
 assert.equal(registry.probability_policy.expected_value_requires_explicit_probabilities,true);
 for(const item of registry.uncertainties){
  assert(item.label.ro.trim()&&item.label.en.trim());
  assert(item.limitations.ro.trim()&&item.limitations.en.trim());
  for(const scenario of item.finite_scenarios??[])assert(scenario.label.ro.trim()&&scenario.label.en.trim());
 }
});

test('OA-6E rejects unjustified positive probability/expected-value language in executable OA-6 surfaces',async()=>{
 const sources=await Promise.all([
  '../src/decision-uncertainty-ui.ts',
  '../src/decision-uncertainty-contract.ts',
  '../src/decision-robustness.ts',
  '../src/information-priority.ts',
  '../src/adaptive-reassessment.ts',
  '../src/planner.ts'
 ].map(async path=>[path,await readFile(new URL(path,import.meta.url),'utf8')] as const));
 const forbidden=[
  /95%\s+confidence/i,
  /probability\s+(?:this|that)\s+.*best/i,
  /probability\s+of\s+.*best/i,
  /expected\s+outcome/i,
  /recommended\s+policy/i,
  /\bEVPI\b/,
  /\bEVSI\b/
 ];
 for(const [path,source] of sources){
  for(const pattern of forbidden)assert.equal(pattern.test(source),false,`${path}: ${pattern}`);
 }
 const ui=sources.find(([path])=>path.endsWith('decision-uncertainty-ui.ts'))![1];
 for(const required of [
  'nu probabilitate','not probability',
  'FĂRĂ PROBABILITĂȚI IMPLICITE','NO IMPLIED PROBABILITIES',
  'Nu este VOI numeric','It is not numeric VOI',
  'ÎNREGISTRARE, NU AUTOMATIZARE','RECORDING, NOT AUTOMATION'
 ])assert(ui.includes(required),required);
});

test('OA-6E keeps scientific, decision and learner confidence vocabularies separated',async()=>{
 const uncertainty=await readFile(new URL('../src/decision-uncertainty-ui.ts',import.meta.url),'utf8');
 const learning=await readFile(new URL('../src/active-understanding.ts',import.meta.url),'utf8');
 assert.equal(/learner confidence/i.test(uncertainty),false);
 assert.equal(/ActiveConfidence/.test(uncertainty),false);
 assert(/ActiveConfidence/.test(learning));
 assert(/Robustness/.test(uncertainty));
});
