import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {analyzeDeclaredScenarios,type DeclaredScenario} from '../src/decision-robustness.ts';
import {deriveInformationPriority} from '../src/information-priority.ts';

type Bundle={mask:number;start:number;false_share:number;true_share:number};
type Planning={levers:{bit:number}[];profiles:{id:string;bundles:Bundle[]}[]};
type Registry={uncertainties:{id:string;role:'SCIENTIFIC_UNCERTAINTY'|'DECISION_ASSUMPTION';uncertainty_type:string;reducibility:string}[]};
const planning=JSON.parse(await readFile(new URL('../public/model/interventions.json',import.meta.url),'utf8')) as Planning;
const registry=JSON.parse(await readFile(new URL('../../model/contracts/decision_uncertainty_v1.json',import.meta.url),'utf8')) as Registry;

function scenarios(settings:{budget:number;weight:number;start:number}):DeclaredScenario[]{
 const costs=[1,1,1,1],enabled=15;
 const cost=(mask:number)=>planning.levers.reduce((sum,lever,index)=>sum+((mask&lever.bit)?costs[index]:0),0);
 const score=(bundle:Bundle)=>100*(settings.weight/100*(1-bundle.false_share)+(1-settings.weight/100)*bundle.true_share);
 return planning.profiles.map(profile=>{
  const rows=profile.bundles.filter(bundle=>bundle.start===settings.start);
  const baseline=rows.find(bundle=>bundle.mask===0)!;
  return {scenarioId:profile.id,outcomes:rows.map(bundle=>({alternativeId:bundle.mask,score:score(bundle),gain:score(bundle)-score(baseline),feasible:cost(bundle.mask)<=settings.budget&&(bundle.mask&enabled)===bundle.mask}))};
 });
}

test('OA-6D uses qualitative triage and keeps stable response profiles out of numeric VOI',()=>{
 const audit=analyzeDeclaredScenarios(scenarios({budget:3,weight:50,start:2}),{referenceScenarioId:'reference'});
 const triage=deriveInformationPriority(registry.uncertainties,audit,14);
 assert.equal(triage.triagePolicy,'QUALITATIVE_TRIAGE_NO_NUMERIC_VOI');
 const response=triage.entries.find(item=>item.uncertaintyId==='UNC.PLANNER.RESPONSE.PROFILES')!;
 assert.equal(response.priorityClass,'RESEARCH_OR_MONITOR');
 assert.equal(response.decisionSensitive,false);
 for(const id of ['UNC.PLANNER.OBJECTIVE.WEIGHT','UNC.PLANNER.EFFORT.COSTS','UNC.PLANNER.ACTIVATION.TIMING']){
  assert.equal(triage.entries.find(item=>item.uncertaintyId===id)!.priorityClass,'CLARIFY_USER_ASSUMPTION');
 }
 assert.equal(triage.entries.find(item=>item.uncertaintyId==='UNC.PLANNER.STRUCTURAL.SCOPE')!.priorityClass,'CONTEXT_LIMITATION');
 assert.equal('score' in triage.entries[0],false);
 assert.equal('voi' in triage.entries[0],false);
});

test('OA-6D marks response-profile uncertainty decision-sensitive when the canonical planner actually switches top bundle',()=>{
 const audit=analyzeDeclaredScenarios(scenarios({budget:2,weight:50,start:2}),{referenceScenarioId:'reference'});
 const triage=deriveInformationPriority(registry.uncertainties,audit,6);
 const response=triage.entries.find(item=>item.uncertaintyId==='UNC.PLANNER.RESPONSE.PROFILES')!;
 assert.equal(response.priorityClass,'DECISION_SENSITIVE_NOW');
 assert.equal(response.reason,'DIRECT_DECISION_SWITCH');
 assert.equal(response.decisionSensitive,true);
});
