import type {ImplementationPlan} from './implementation-plan';
import type {ObservedOutcome} from './observed-outcome';

type Lang='ro'|'en';
type Copy={ro:string;en:string};

export type RevisionProposalTarget='MODEL_ASSUMPTION'|'DECISION_ANALYSIS'|'IMPLEMENTATION_PLAN'|'INDICATOR';
export type RevisionProposalStatus='PROPOSED'|'ACCEPTED'|'REJECTED';

export type RevisionProposal={
 target:RevisionProposalTarget;
 rationale:Copy;
 proposed_change:Copy;
 status:RevisionProposalStatus;
};

export type DecisionAutopsy={
 object_type:'DecisionAutopsy';
 id:string;
 case_id:string;
 implementation_plan_id:string;
 decision_analysis_id:string;
 observed_outcome_ids:string[];
 created_at:string;
 findings:Copy[];
 revision_proposals:RevisionProposal[];
 prior_prediction_mutated:false;
 revision_of_autopsy_id?:string;
};

export type DecisionAutopsyInput={
 plan:ImplementationPlan;
 outcomes:ObservedOutcome[];
 prior_autopsies:DecisionAutopsy[];
 observed_outcome_ids:string[];
 findings:string[];
 proposal:{
  target:RevisionProposalTarget;
  rationale:string;
  proposed_change:string;
  status:RevisionProposalStatus;
 };
 revision_of_autopsy_id?:string;
 now?:()=>string;
 id?:()=>string;
};

const clean=(value:string)=>value.trim();
const verbatim=(value:string):Copy=>({ro:clean(value),en:clean(value)});
const unique=(values:string[])=>[...new Set(values.map(clean).filter(Boolean))];
const defaultId=()=>crypto.randomUUID();

function required(value:string,name:string):string{
 const result=clean(value);
 if(!result)throw new Error(`${name} is required`);
 return result;
}

function parseTime(value:string,name:string):number{
 const parsed=Date.parse(value);
 if(!Number.isFinite(parsed))throw new Error(`${name} must be a valid date-time`);
 return parsed;
}

export function validateDecisionAutopsyReferences(
 record:DecisionAutopsy,
 plan:ImplementationPlan,
 outcomes:ObservedOutcome[],
 priorAutopsies:DecisionAutopsy[]
):void{
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
 for(const id of record.observed_outcome_ids){
  const observed=outcomes.find(item=>item.id===id);
  if(!observed)throw new Error(`ObservedOutcome is not present in persisted input set: ${id}`);
  if(observed.object_type!=='ObservedOutcome')throw new Error(`referenced record is not an ObservedOutcome: ${id}`);
  if(observed.case_id!==plan.case_id)throw new Error(`ObservedOutcome case mismatch: ${id}`);
  if(observed.implementation_plan_id!==plan.id)throw new Error(`ObservedOutcome plan mismatch: ${id}`);
  if(observed.prospective_snapshot_id!==plan.prospective_snapshot.id)throw new Error(`ObservedOutcome snapshot mismatch: ${id}`);
  if(parseTime(observed.recorded_at,'ObservedOutcome recorded_at')>created)throw new Error(`DecisionAutopsy cannot predate ObservedOutcome recording: ${id}`);
 }

 for(const proposal of record.revision_proposals){
  if(!['MODEL_ASSUMPTION','DECISION_ANALYSIS','IMPLEMENTATION_PLAN','INDICATOR'].includes(proposal.target))throw new Error('unsupported revision proposal target');
  if(!clean(proposal.rationale.ro)||!clean(proposal.rationale.en))throw new Error('revision proposal rationale is required');
  if(!clean(proposal.proposed_change.ro)||!clean(proposal.proposed_change.en))throw new Error('revision proposal change is required');
  if(!['PROPOSED','ACCEPTED','REJECTED'].includes(proposal.status))throw new Error('unsupported revision proposal status');
 }

 if(record.revision_of_autopsy_id){
  const parent=priorAutopsies.find(item=>item.id===record.revision_of_autopsy_id);
  if(!parent)throw new Error('revision parent DecisionAutopsy is not present in persisted input set');
  if(parent.id===record.id)throw new Error('DecisionAutopsy cannot revise itself');
  if(parent.case_id!==record.case_id||parent.implementation_plan_id!==record.implementation_plan_id||parent.decision_analysis_id!==record.decision_analysis_id){
   throw new Error('revision parent DecisionAutopsy provenance mismatch');
  }
  if(parseTime(parent.created_at,'revision parent created_at')>created)throw new Error('DecisionAutopsy revision cannot predate its parent');
 }
}

export function materializeDecisionAutopsy(input:DecisionAutopsyInput):DecisionAutopsy{
 if(input.plan.plan_scope!=='ILLUSTRATIVE')throw new Error('this DecisionAutopsy slice accepts only the current illustrative ImplementationPlan');
 const observedIds=unique(input.observed_outcome_ids);
 if(observedIds.length===0)throw new Error('select at least one ObservedOutcome');
 const findings=input.findings.map(clean).filter(Boolean).map(verbatim);
 if(findings.length===0)throw new Error('at least one finding is required');
 const rationale=required(input.proposal.rationale,'revision proposal rationale');
 const proposedChange=required(input.proposal.proposed_change,'revision proposal change');
 const createdAt=(input.now??(()=>new Date().toISOString()))();
 const token=(input.id??defaultId)();
 const record:DecisionAutopsy={
  object_type:'DecisionAutopsy',
  id:`CEM.DECISION.AUTOPSY.${token}`,
  case_id:input.plan.case_id,
  implementation_plan_id:input.plan.id,
  decision_analysis_id:input.plan.decision_analysis_id,
  observed_outcome_ids:observedIds,
  created_at:new Date(parseTime(createdAt,'created_at')).toISOString(),
  findings,
  revision_proposals:[{
   target:input.proposal.target,
   rationale:verbatim(rationale),
   proposed_change:verbatim(proposedChange),
   status:input.proposal.status
  }],
  prior_prediction_mutated:false,
  ...(clean(input.revision_of_autopsy_id??'')?{revision_of_autopsy_id:clean(input.revision_of_autopsy_id!)}:{})
 };
 validateDecisionAutopsyReferences(record,input.plan,input.outcomes,input.prior_autopsies);
 return record;
}

const esc=(value:string)=>value.replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]??c));

export function mountDecisionAutopsy(
 host:HTMLElement,
 input:{
  plan:ImplementationPlan;
  outcomes:ObservedOutcome[];
  autopsies:DecisionAutopsy[];
  lang:Lang;
  persist:(record:DecisionAutopsy)=>Promise<DecisionAutopsy>;
  afterPersist?:()=>Promise<void>|void;
 }
):void{
 const {plan,lang}=input;
 const t=(ro:string,en:string)=>lang==='ro'?ro:en;
 const outcomes=[...input.outcomes].sort((a,b)=>a.recorded_at.localeCompare(b.recorded_at)||a.id.localeCompare(b.id));
 const autopsies=[...input.autopsies].sort((a,b)=>a.created_at.localeCompare(b.created_at)||a.id.localeCompare(b.id));
 const outcomeChoices=outcomes.map(item=>`<label><input type="checkbox" name="observed_outcome_id" value="${esc(item.id)}"> <code>${esc(item.id)}</code> · ${esc(item.indicator_id)} · ${item.result.value}</label>`).join('');
 const parentOptions=autopsies.map(item=>`<option value="${esc(item.id)}">${esc(item.id)} · ${esc(item.created_at)}</option>`).join('');
 const trail=autopsies.map(item=>`<li data-autopsy-id="${esc(item.id)}" data-revision-of="${esc(item.revision_of_autopsy_id??'')}"><code>${esc(item.id)}</code>${item.revision_of_autopsy_id?` ← ${esc(item.revision_of_autopsy_id)}`:''}<br><small>${esc(item.created_at)} · ${item.observed_outcome_ids.length} ObservedOutcome · ${item.revision_proposals[0]?.status??'NO_PROPOSAL'}</small></li>`).join('');
 host.innerHTML=`<section id="decisionAutopsy" data-plan-id="${esc(plan.id)}" data-mutation-policy="APPEND_ONLY_NO_RETROACTIVE_EDIT">
  <div class="section-heading"><div><p class="eyebrow">OA-7 · DECISION AUTOPSY</p><h4>${t('Autopsie decizională și traseu de revizie','Decision autopsy and revision trail')}</h4><p>${t('Leagă manual observațiile de constatări și de o propunere de revizie. Fiecare revizie este un obiect nou; predicția, planul și autopsiile anterioare rămân nemodificate.','Manually link observations to findings and a revision proposal. Every revision is a new object; the prediction, plan and prior autopsies remain unchanged.')}</p></div><span class="planner-badge">APPEND-ONLY · HUMAN REVIEW</span></div>
  <div><strong>${t('Traseu existent','Existing trail')}</strong>${trail?`<ol id="decisionAutopsyTrail">${trail}</ol>`:`<p class="note" data-autopsy-empty="true">${t('Nu există încă nicio autopsie pentru acest plan.','No autopsy exists for this plan yet.')}</p>`}</div>
  <form id="decisionAutopsyForm">
   <fieldset ${outcomes.length?'':'disabled'}><legend>${t('ObservedOutcome persistate folosite','Persisted ObservedOutcome records used')}</legend>${outcomeChoices||`<p>${t('Înregistrează mai întâi cel puțin un ObservedOutcome.','Record at least one ObservedOutcome first.')}</p>`}</fieldset>
   <label>${t('Revizuiește o autopsie anterioară (opțional)','Revision of prior autopsy (optional)')}<select name="revision_of_autopsy_id"><option value="">${t('Autopsie nouă, fără părinte','New autopsy, no parent')}</option>${parentOptions}</select></label>
   <label>${t('Constatări — câte una pe rând','Findings — one per line')}<textarea name="findings" required ${outcomes.length?'':'disabled'}></textarea></label>
   <label>${t('Ținta propunerii','Proposal target')}<select name="proposal_target" ${outcomes.length?'':'disabled'}><option value="MODEL_ASSUMPTION">MODEL_ASSUMPTION</option><option value="DECISION_ANALYSIS">DECISION_ANALYSIS</option><option value="IMPLEMENTATION_PLAN">IMPLEMENTATION_PLAN</option><option value="INDICATOR">INDICATOR</option></select></label>
   <label>${t('Raționamentul propunerii','Proposal rationale')}<textarea name="proposal_rationale" required ${outcomes.length?'':'disabled'}></textarea></label>
   <label>${t('Schimbarea propusă','Proposed change')}<textarea name="proposed_change" required ${outcomes.length?'':'disabled'}></textarea></label>
   <label>${t('Status declarat de utilizator','User-declared status')}<select name="proposal_status" ${outcomes.length?'':'disabled'}><option value="PROPOSED">PROPOSED</option><option value="ACCEPTED">ACCEPTED</option><option value="REJECTED">REJECTED</option></select></label>
   <button type="submit" class="primary" ${outcomes.length?'':'disabled'}>${t('Adaugă DecisionAutopsy','Append DecisionAutopsy')}</button>
  </form>
  <p class="note">${t('Textele sunt păstrate verbatim în câmpurile RO/EN; aplicația nu inventează explicații, traduceri sau revizii. ACCEPTED/REJECTED reprezintă doar statusul declarat de utilizator și nu modifică automat modelul sau planul.','Free text is preserved verbatim in RO/EN fields; the app does not invent explanations, translations or revisions. ACCEPTED/REJECTED is only the user-declared status and never changes the model or plan automatically.')}</p>
  <p id="decisionAutopsyStatus" class="note" aria-live="polite"></p>
 </section>`;

 const form=host.querySelector<HTMLFormElement>('#decisionAutopsyForm')!;
 const status=host.querySelector<HTMLElement>('#decisionAutopsyStatus')!;
 form.onsubmit=async event=>{
  event.preventDefault();
  if(!form.reportValidity())return;
  const selected=[...form.querySelectorAll<HTMLInputElement>('input[name="observed_outcome_id"]:checked')].map(item=>item.value);
  if(selected.length===0){status.textContent=t('Selectează cel puțin un ObservedOutcome.','Select at least one ObservedOutcome.');return;}
  const submit=form.querySelector<HTMLButtonElement>('button[type="submit"]')!;
  submit.disabled=true;
  status.textContent=t('Se validează proveniența și se adaugă autopsia…','Validating provenance and appending autopsy…');
  try{
   const data=new FormData(form);
   const record=materializeDecisionAutopsy({
    plan,
    outcomes,
    prior_autopsies:autopsies,
    observed_outcome_ids:selected,
    findings:String(data.get('findings')??'').split(/\r?\n/),
    proposal:{
     target:String(data.get('proposal_target')) as RevisionProposalTarget,
     rationale:String(data.get('proposal_rationale')??''),
     proposed_change:String(data.get('proposed_change')??''),
     status:String(data.get('proposal_status')) as RevisionProposalStatus
    },
    revision_of_autopsy_id:String(data.get('revision_of_autopsy_id')??'')
   });
   const stored=await input.persist(record);
   host.dataset.decisionAutopsyId=stored.id;
   status.textContent=t(`DecisionAutopsy adăugată append-only: ${stored.id}`,`Append-only DecisionAutopsy saved: ${stored.id}`);
   await input.afterPersist?.();
  }catch(error){
   status.textContent=t(`Autopsia a eșuat: ${String(error)}`,`Autopsy failed: ${String(error)}`);
  }finally{submit.disabled=false;}
 };
}
