import type {ImplementationPlan} from '../implementation-plan';
import type {ObservedOutcome} from './observed-outcome';

type Copy={ro:string;en:string};
export type RevisionProposalTarget='MODEL_ASSUMPTION'|'DECISION_ANALYSIS'|'IMPLEMENTATION_PLAN'|'INDICATOR';
export type RevisionProposalStatus='PROPOSED'|'ACCEPTED'|'REJECTED';
export type RevisionProposal={target:RevisionProposalTarget;rationale:Copy;proposed_change:Copy;status:RevisionProposalStatus};
export type DecisionAutopsy={object_type:'DecisionAutopsy';id:string;case_id:string;implementation_plan_id:string;decision_analysis_id:string;observed_outcome_ids:string[];created_at:string;findings:Copy[];revision_proposals:RevisionProposal[];prior_prediction_mutated:false;revision_of_autopsy_id?:string};
export type DecisionAutopsyInput={plan:ImplementationPlan;outcomes:ObservedOutcome[];prior_autopsies:DecisionAutopsy[];observed_outcome_ids:string[];findings:string[];proposal:{target:RevisionProposalTarget;rationale:string;proposed_change:string;status:RevisionProposalStatus};revision_of_autopsy_id?:string;now?:()=>string;id?:()=>string};

const clean=(value:string)=>value.trim();
const verbatim=(value:string):Copy=>({ro:clean(value),en:clean(value)});
const unique=(values:string[])=>[...new Set(values.map(clean).filter(Boolean))];
const defaultId=()=>crypto.randomUUID();
function required(value:string,name:string):string{const result=clean(value);if(!result)throw new Error(`${name} is required`);return result;}
function parseTime(value:string,name:string):number{const parsed=Date.parse(value);if(!Number.isFinite(parsed))throw new Error(`${name} must be a valid date-time`);return parsed;}

export function validateDecisionAutopsyReferences(record:DecisionAutopsy,plan:ImplementationPlan,outcomes:ObservedOutcome[],priorAutopsies:DecisionAutopsy[]):void{
 if(plan.object_type!=='ImplementationPlan')throw new Error('referenced record is not an ImplementationPlan');
 if(record.case_id!==plan.case_id)throw new Error('DecisionAutopsy case_id does not match ImplementationPlan');
 if(record.implementation_plan_id!==plan.id)throw new Error('DecisionAutopsy ImplementationPlan reference mismatch');
 if(record.decision_analysis_id!==plan.decision_analysis_id)throw new Error('DecisionAutopsy DecisionAnalysis reference mismatch');
 if(record.prior_prediction_mutated!==false)throw new Error('DecisionAutopsy must not mutate the prior prediction');
 if(record.observed_outcome_ids.length===0)throw new Error('DecisionAutopsy requires at least one ObservedOutcome');
 if(new Set(record.observed_outcome_ids).size!==record.observed_outcome_ids.length)throw new Error('DecisionAutopsy ObservedOutcome references must be unique');
 if(record.findings.length===0||record.findings.some(item=>!clean(item.ro)||!clean(item.en)))throw new Error('DecisionAutopsy requires non-empty findings');
 if(record.revision_proposals.length===0)throw new Error('DecisionAutopsy current slice requires at least one revision proposal');
 const created=parseTime(record.created_at,'created_at');
 for(const id of record.observed_outcome_ids){const observed=outcomes.find(item=>item.id===id);if(!observed)throw new Error(`ObservedOutcome is not present in persisted input set: ${id}`);if(observed.object_type!=='ObservedOutcome')throw new Error(`referenced record is not an ObservedOutcome: ${id}`);if(observed.case_id!==plan.case_id)throw new Error(`ObservedOutcome case mismatch: ${id}`);if(observed.implementation_plan_id!==plan.id)throw new Error(`ObservedOutcome plan mismatch: ${id}`);if(observed.prospective_snapshot_id!==plan.prospective_snapshot.id)throw new Error(`ObservedOutcome snapshot mismatch: ${id}`);if(parseTime(observed.recorded_at,'ObservedOutcome recorded_at')>created)throw new Error(`DecisionAutopsy cannot predate ObservedOutcome recording: ${id}`);}
 for(const proposal of record.revision_proposals){if(!['MODEL_ASSUMPTION','DECISION_ANALYSIS','IMPLEMENTATION_PLAN','INDICATOR'].includes(proposal.target))throw new Error('unsupported revision proposal target');if(!clean(proposal.rationale.ro)||!clean(proposal.rationale.en))throw new Error('revision proposal rationale is required');if(!clean(proposal.proposed_change.ro)||!clean(proposal.proposed_change.en))throw new Error('revision proposal change is required');if(!['PROPOSED','ACCEPTED','REJECTED'].includes(proposal.status))throw new Error('unsupported revision proposal status');}
 if(record.revision_of_autopsy_id){const parent=priorAutopsies.find(item=>item.id===record.revision_of_autopsy_id);if(!parent)throw new Error('revision parent DecisionAutopsy is not present in persisted input set');if(parent.id===record.id)throw new Error('DecisionAutopsy cannot revise itself');if(parent.case_id!==record.case_id||parent.implementation_plan_id!==record.implementation_plan_id||parent.decision_analysis_id!==record.decision_analysis_id)throw new Error('revision parent DecisionAutopsy provenance mismatch');if(parseTime(parent.created_at,'revision parent created_at')>created)throw new Error('DecisionAutopsy revision cannot predate its parent');}
}

export function materializeDecisionAutopsy(input:DecisionAutopsyInput):DecisionAutopsy{
 if(input.plan.plan_scope!=='ILLUSTRATIVE')throw new Error('this DecisionAutopsy slice accepts only the current illustrative ImplementationPlan');const observedIds=unique(input.observed_outcome_ids);if(observedIds.length===0)throw new Error('select at least one ObservedOutcome');const findings=input.findings.map(clean).filter(Boolean).map(verbatim);if(findings.length===0)throw new Error('at least one finding is required');const rationale=required(input.proposal.rationale,'revision proposal rationale');const proposedChange=required(input.proposal.proposed_change,'revision proposal change');const createdAt=(input.now??(()=>new Date().toISOString()))();const token=(input.id??defaultId)();const record:DecisionAutopsy={object_type:'DecisionAutopsy',id:`CEM.DECISION.AUTOPSY.${token}`,case_id:input.plan.case_id,implementation_plan_id:input.plan.id,decision_analysis_id:input.plan.decision_analysis_id,observed_outcome_ids:observedIds,created_at:new Date(parseTime(createdAt,'created_at')).toISOString(),findings,revision_proposals:[{target:input.proposal.target,rationale:verbatim(rationale),proposed_change:verbatim(proposedChange),status:input.proposal.status}],prior_prediction_mutated:false,...(clean(input.revision_of_autopsy_id??'')?{revision_of_autopsy_id:clean(input.revision_of_autopsy_id!)}:{})};validateDecisionAutopsyReferences(record,input.plan,input.outcomes,input.prior_autopsies);return record;
}
