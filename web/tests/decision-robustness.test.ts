import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {analyzeDeclaredScenarios,type DeclaredScenario} from '../src/decision-robustness.ts';

type Bundle={mask:number;start:number;false_share:number;true_share:number};
type Data={
 levers:{bit:number}[];
 profiles:{id:string;bundles:Bundle[]}[];
};

const data=JSON.parse(await readFile(new URL('../public/model/interventions.json',import.meta.url),'utf8')) as Data;

function plannerScenarios(settings:{budget:number;weight:number;start:number;costs:number[];enabled:number}):DeclaredScenario[]{
 const cost=(mask:number)=>data.levers.reduce((sum,lever,index)=>sum+((mask&lever.bit)?settings.costs[index]:0),0);
 const score=(bundle:Bundle)=>100*(settings.weight/100*(1-bundle.false_share)+(1-settings.weight/100)*bundle.true_share);
 return data.profiles.map(profile=>{
  const rows=profile.bundles.filter(bundle=>bundle.start===settings.start);
  const baseline=rows.find(bundle=>bundle.mask===0)!;
  return {
   scenarioId:profile.id,
   outcomes:rows.map(bundle=>({
    alternativeId:bundle.mask,
    score:score(bundle),
    gain:score(bundle)-score(baseline),
    feasible:(bundle.mask&settings.enabled)===bundle.mask&&cost(bundle.mask)<=settings.budget
   }))
  };
 });
}

test('OA-6B preserves the current default planner top bundle across all three declared profiles',()=>{
 const audit=analyzeDeclaredScenarios(
  plannerScenarios({budget:3,weight:50,start:2,costs:[1,1,1,1],enabled:15}),
  {referenceScenarioId:'reference',acceptableGainThreshold:5}
 );
 assert.equal(audit.scenarioCount,3);
 assert.deepEqual(audit.scenarios.map(s=>[s.scenarioId,s.topAlternativeIds]),[
  ['low',[14]],['reference',[14]],['high',[14]]
 ]);
 assert.deepEqual(audit.decisionSwitch.changes,[]);
 const bundle14=audit.alternatives.find(a=>a.alternativeId===14)!;
 assert.equal(bundle14.topRankScenarioCount,3);
 assert.equal(bundle14.scenarioDenominator,3);
 assert.equal(bundle14.acceptableScenarioCount,3);
 assert.equal(bundle14.maxRegretAcrossFeasibleScenarios,0);
 assert.equal(audit.probabilityInterpretation,'NOT_APPLICABLE_FINITE_DECLARED_SCENARIOS');
});

test('OA-6B detects a real decision switch already present in the canonical planner table',()=>{
 const audit=analyzeDeclaredScenarios(
  plannerScenarios({budget:2,weight:50,start:2,costs:[1,1,1,1],enabled:15}),
  {referenceScenarioId:'reference'}
 );
 assert.deepEqual(audit.scenarios.map(s=>[s.scenarioId,s.topAlternativeIds]),[
  ['low',[10]],['reference',[6]],['high',[6]]
 ]);
 assert.deepEqual(audit.decisionSwitch,{
  referenceScenarioId:'reference',
  referenceTopAlternativeIds:[6],
  changes:[{scenarioId:'low',topAlternativeIds:[10]}]
 });
});

test('OA-6B regret is zero for every scenario-best alternative and non-negative everywhere feasible',()=>{
 const audit=analyzeDeclaredScenarios(
  plannerScenarios({budget:2,weight:50,start:2,costs:[1,1,1,1],enabled:15}),
  {referenceScenarioId:'reference'}
 );
 for(const scenario of audit.scenarios){
  for(const outcome of scenario.outcomes.filter(o=>o.feasible)){
   assert(outcome.regret!==null);
   assert(outcome.regret>=0);
   if(scenario.topAlternativeIds.includes(outcome.alternativeId))assert.equal(outcome.regret,0);
  }
 }
});

test('OA-6B gives equal scores equal rank without turning deterministic ID order into evidence',()=>{
 const scenarios:DeclaredScenario[]=[
  {scenarioId:'a',outcomes:[
   {alternativeId:1,score:10,gain:2,feasible:true},
   {alternativeId:2,score:10,gain:2,feasible:true},
   {alternativeId:3,score:9,gain:1,feasible:true}
  ]},
  {scenarioId:'b',outcomes:[
   {alternativeId:1,score:8,gain:1,feasible:true},
   {alternativeId:2,score:8,gain:1,feasible:true},
   {alternativeId:3,score:7,gain:0,feasible:true}
  ]}
 ];
 const audit=analyzeDeclaredScenarios(scenarios,{referenceScenarioId:'a'});
 for(const scenario of audit.scenarios){
  assert.deepEqual(scenario.topAlternativeIds,[1,2]);
  assert.equal(scenario.outcomes.find(o=>o.alternativeId===1)!.rank,1);
  assert.equal(scenario.outcomes.find(o=>o.alternativeId===2)!.rank,1);
  assert.equal(scenario.outcomes.find(o=>o.alternativeId===3)!.rank,3);
 }
 assert.deepEqual(audit.decisionSwitch.changes,[]);
});

test('OA-6B threshold coverage is a scenario count, not a probability',()=>{
 const audit=analyzeDeclaredScenarios(
  plannerScenarios({budget:3,weight:50,start:2,costs:[1,1,1,1],enabled:15}),
  {referenceScenarioId:'reference',acceptableGainThreshold:5}
 );
 const bundle11=audit.alternatives.find(a=>a.alternativeId===11)!;
 assert.equal(bundle11.acceptableScenarioCount,2);
 assert.equal(bundle11.scenarioDenominator,3);
 assert.equal('probability' in bundle11,false);
});

test('OA-6B fails closed on malformed scenario tables',()=>{
 assert.throws(()=>analyzeDeclaredScenarios([
  {scenarioId:'a',outcomes:[{alternativeId:1,score:1,gain:0,feasible:true}]},
  {scenarioId:'a',outcomes:[{alternativeId:1,score:1,gain:0,feasible:true}]}
 ],{referenceScenarioId:'a'}),/scenarioId values must be unique/);

 assert.throws(()=>analyzeDeclaredScenarios([
  {scenarioId:'a',outcomes:[{alternativeId:1,score:1,gain:0,feasible:true}]},
  {scenarioId:'b',outcomes:[{alternativeId:2,score:1,gain:0,feasible:true}]}
 ],{referenceScenarioId:'a'}),/same alternative IDs/);

 assert.throws(()=>analyzeDeclaredScenarios([
  {scenarioId:'a',outcomes:[{alternativeId:1,score:1,gain:0,feasible:false}]},
  {scenarioId:'b',outcomes:[{alternativeId:1,score:1,gain:0,feasible:true}]}
 ],{referenceScenarioId:'a'}),/at least one feasible alternative/);
});
