import type {RobustnessAudit} from './decision-robustness';

export type InformationPriorityClass=
 |'DECISION_SENSITIVE_NOW'
 |'CLARIFY_USER_ASSUMPTION'
 |'RESEARCH_OR_MONITOR'
 |'CONTEXT_LIMITATION';

export type InformationPriorityReason=
 |'DIRECT_DECISION_SWITCH'
 |'STABLE_WITHIN_DECLARED_SCENARIOS'
 |'USER_CONTROLLED_ASSUMPTION'
 |'REDUCIBLE_EVIDENCE_GAP'
 |'OMITTED_MODEL_SCOPE';

export type PriorityUncertainty={
 id:string;
 role:'SCIENTIFIC_UNCERTAINTY'|'DECISION_ASSUMPTION';
 uncertainty_type:string;
 reducibility:string;
};

export type InformationPriorityEntry={
 uncertaintyId:string;
 priorityClass:InformationPriorityClass;
 reason:InformationPriorityReason;
 reducibility:string;
 decisionSensitive:boolean;
};

export type InformationPriorityAudit={
 triagePolicy:'QUALITATIVE_TRIAGE_NO_NUMERIC_VOI';
 entries:InformationPriorityEntry[];
};

export function deriveInformationPriority(
 uncertainties:readonly PriorityUncertainty[],
 robustness:RobustnessAudit,
 selectedAlternativeId:number
):InformationPriorityAudit{
 const selected=robustness.alternatives.find(item=>item.alternativeId===selectedAlternativeId);
 if(!selected)throw new Error('selected alternative is missing from robustness audit');
 const responseSensitive=robustness.decisionSwitch.changes.length>0||selected.topRankScenarioCount<selected.feasibleScenarioCount;
 const entries=uncertainties.map(item=>{
  if(item.id==='UNC.PLANNER.RESPONSE.PROFILES'){
   return responseSensitive
    ?{uncertaintyId:item.id,priorityClass:'DECISION_SENSITIVE_NOW' as const,reason:'DIRECT_DECISION_SWITCH' as const,reducibility:item.reducibility,decisionSensitive:true}
    :{uncertaintyId:item.id,priorityClass:'RESEARCH_OR_MONITOR' as const,reason:'STABLE_WITHIN_DECLARED_SCENARIOS' as const,reducibility:item.reducibility,decisionSensitive:false};
  }
  if(item.reducibility==='USER_CONTROLLED'){
   return {uncertaintyId:item.id,priorityClass:'CLARIFY_USER_ASSUMPTION' as const,reason:'USER_CONTROLLED_ASSUMPTION' as const,reducibility:item.reducibility,decisionSensitive:false};
  }
  if(item.uncertainty_type==='STRUCTURAL'){
   return {uncertaintyId:item.id,priorityClass:'CONTEXT_LIMITATION' as const,reason:'OMITTED_MODEL_SCOPE' as const,reducibility:item.reducibility,decisionSensitive:false};
  }
  return {uncertaintyId:item.id,priorityClass:'RESEARCH_OR_MONITOR' as const,reason:'REDUCIBLE_EVIDENCE_GAP' as const,reducibility:item.reducibility,decisionSensitive:false};
 });
 return {triagePolicy:'QUALITATIVE_TRIAGE_NO_NUMERIC_VOI',entries};
}
