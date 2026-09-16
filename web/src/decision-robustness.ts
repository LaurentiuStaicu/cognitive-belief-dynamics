export type AlternativeId=number;

export type ScenarioOutcome={
 alternativeId:AlternativeId;
 score:number;
 gain:number;
 feasible:boolean;
};

export type DeclaredScenario={
 scenarioId:string;
 outcomes:ScenarioOutcome[];
};

export type RobustnessOptions={
 referenceScenarioId:string;
 acceptableGainThreshold?:number;
 tolerance?:number;
};

export type ScenarioOutcomeAudit={
 alternativeId:AlternativeId;
 feasible:boolean;
 score:number;
 gain:number;
 rank:number|null;
 regret:number|null;
 acceptable:boolean;
};

export type ScenarioAudit={
 scenarioId:string;
 bestScore:number;
 topAlternativeIds:AlternativeId[];
 outcomes:ScenarioOutcomeAudit[];
};

export type AlternativeRobustness={
 alternativeId:AlternativeId;
 feasibleScenarioCount:number;
 scenarioDenominator:number;
 topRankScenarioCount:number;
 acceptableScenarioCount:number|null;
 rankRange:[number,number]|null;
 scoreRange:[number,number]|null;
 gainRange:[number,number]|null;
 maxRegretAcrossFeasibleScenarios:number|null;
};

export type DecisionSwitchAudit={
 referenceScenarioId:string;
 referenceTopAlternativeIds:AlternativeId[];
 changes:{scenarioId:string;topAlternativeIds:AlternativeId[]}[];
};

export type RobustnessAudit={
 scenarioCount:number;
 scenarios:ScenarioAudit[];
 alternatives:AlternativeRobustness[];
 decisionSwitch:DecisionSwitchAudit;
 probabilityInterpretation:'NOT_APPLICABLE_FINITE_DECLARED_SCENARIOS';
};

const finite=(value:number,label:string)=>{
 if(!Number.isFinite(value))throw new Error(label+' must be finite');
 return value;
};

const sameIds=(left:AlternativeId[],right:AlternativeId[])=>{
 if(left.length!==right.length)return false;
 for(let i=0;i<left.length;i++)if(left[i]!==right[i])return false;
 return true;
};

export function analyzeDeclaredScenarios(
 declaredScenarios:readonly DeclaredScenario[],
 options:RobustnessOptions
):RobustnessAudit{
 if(declaredScenarios.length<2)throw new Error('at least two declared scenarios are required');
 const tolerance=options.tolerance??1e-12;
 if(!Number.isFinite(tolerance)||tolerance<0)throw new Error('tolerance must be a finite non-negative number');
 if(options.acceptableGainThreshold!==undefined)finite(options.acceptableGainThreshold,'acceptableGainThreshold');

 const scenarioIds=new Set<string>();
 const canonicalIds:number[]=[];
 const scenarioAudits:ScenarioAudit[]=[];

 for(const [index,scenario] of declaredScenarios.entries()){
  if(!scenario.scenarioId)throw new Error('scenarioId must be non-empty');
  if(scenarioIds.has(scenario.scenarioId))throw new Error('scenarioId values must be unique');
  scenarioIds.add(scenario.scenarioId);
  if(scenario.outcomes.length<1)throw new Error('each scenario must contain alternatives');

  const seen=new Set<number>();
  const ids:number[]=[];
  for(const outcome of scenario.outcomes){
   if(!Number.isInteger(outcome.alternativeId)||outcome.alternativeId<0)throw new Error('alternativeId must be a non-negative integer');
   if(seen.has(outcome.alternativeId))throw new Error('alternativeId values must be unique within each scenario');
   seen.add(outcome.alternativeId);
   ids.push(outcome.alternativeId);
   finite(outcome.score,'score');
   finite(outcome.gain,'gain');
  }
  ids.sort((a,b)=>a-b);
  if(index===0)canonicalIds.push(...ids);
  else if(!sameIds(ids,canonicalIds))throw new Error('all declared scenarios must contain the same alternative IDs');

  const feasible=scenario.outcomes.filter(item=>item.feasible);
  if(feasible.length<1)throw new Error('each scenario must contain at least one feasible alternative');
  const bestScore=Math.max(...feasible.map(item=>item.score));
  const topAlternativeIds=feasible
   .filter(item=>Math.abs(bestScore-item.score)<=tolerance)
   .map(item=>item.alternativeId)
   .sort((a,b)=>a-b);

  const audited=scenario.outcomes
   .map(item=>{
    if(!item.feasible){
     return {
      alternativeId:item.alternativeId,
      feasible:false,
      score:item.score,
      gain:item.gain,
      rank:null,
      regret:null,
      acceptable:false
     };
    }
    const rank=1+feasible.filter(other=>other.score>item.score+tolerance).length;
    const rawRegret=bestScore-item.score;
    const regret=rawRegret<=tolerance?0:rawRegret;
    return {
     alternativeId:item.alternativeId,
     feasible:true,
     score:item.score,
     gain:item.gain,
     rank,
     regret,
     acceptable:options.acceptableGainThreshold===undefined?false:item.gain+ tolerance>=options.acceptableGainThreshold
    };
   })
   .sort((a,b)=>a.alternativeId-b.alternativeId);

  scenarioAudits.push({scenarioId:scenario.scenarioId,bestScore,topAlternativeIds,outcomes:audited});
 }

 if(!scenarioIds.has(options.referenceScenarioId))throw new Error('referenceScenarioId must identify a declared scenario');

 const alternatives=canonicalIds.map(alternativeId=>{
  const outcomes=scenarioAudits.map(s=>s.outcomes.find(o=>o.alternativeId===alternativeId)!);
  const feasible=outcomes.filter(o=>o.feasible);
  const ranks=feasible.map(o=>o.rank as number);
  const scores=feasible.map(o=>o.score);
  const gains=feasible.map(o=>o.gain);
  const regrets=feasible.map(o=>o.regret as number);
  return {
   alternativeId,
   feasibleScenarioCount:feasible.length,
   scenarioDenominator:scenarioAudits.length,
   topRankScenarioCount:feasible.filter(o=>o.rank===1).length,
   acceptableScenarioCount:options.acceptableGainThreshold===undefined?null:feasible.filter(o=>o.acceptable).length,
   rankRange:ranks.length?[Math.min(...ranks),Math.max(...ranks)] as [number,number]:null,
   scoreRange:scores.length?[Math.min(...scores),Math.max(...scores)] as [number,number]:null,
   gainRange:gains.length?[Math.min(...gains),Math.max(...gains)] as [number,number]:null,
   maxRegretAcrossFeasibleScenarios:regrets.length?Math.max(...regrets):null
  };
 });

 const reference=scenarioAudits.find(s=>s.scenarioId===options.referenceScenarioId)!;
 const changes=scenarioAudits
  .filter(s=>s.scenarioId!==reference.scenarioId&&!sameIds(s.topAlternativeIds,reference.topAlternativeIds))
  .map(s=>({scenarioId:s.scenarioId,topAlternativeIds:[...s.topAlternativeIds]}));

 return {
  scenarioCount:scenarioAudits.length,
  scenarios:scenarioAudits,
  alternatives,
  decisionSwitch:{
   referenceScenarioId:reference.scenarioId,
   referenceTopAlternativeIds:[...reference.topAlternativeIds],
   changes
  },
  probabilityInterpretation:'NOT_APPLICABLE_FINITE_DECLARED_SCENARIOS'
 };
}
