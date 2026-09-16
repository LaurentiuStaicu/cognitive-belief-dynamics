import type {SignpostDefinition,TriggerDraft} from './signposts-triggers';

type Lang='ro'|'en';
type Copy=Record<Lang,string>;

export type AdaptivePhase='NOW'|'WATCH'|'IF'|'THEN'|'STOP'|'REASSESS';
export type AdaptiveStepReadiness='DEFINED'|'MISSING_TRIGGER'|'MISSING_ACTION';

export type AdaptivePlanStep={
 id:string;
 phase:AdaptivePhase;
 statement:Copy;
 readiness:AdaptiveStepReadiness;
 indicator_id?:string;
 trigger_draft_id?:string;
 trigger_condition?:Copy;
 action?:Copy;
};

export type AdaptivePlanDraft={
 object_type:'AdaptivePlanDraft';
 status:'DRAFT';
 persistence:'EPHEMERAL_NOT_WORKSPACE';
 execution_status:'DESIGN_ONLY_NO_OBSERVED_OUTCOME';
 automation:'NO_AUTOMATIC_ACTIONS';
 bundle_label:Copy;
 trigger_draft_id?:string;
 steps:AdaptivePlanStep[];
};

export type AdaptiveActionInputs={
 then_action:Copy;
 stop_action:Copy;
 reassess_action:Copy;
};

const copy=(ro:string,en:string):Copy=>({ro,en});
const comparator=(value:TriggerDraft['comparator'])=>({LT:'<',LTE:'≤',GTE:'≥',GT:'>'}[value]);
const nonEmptyCopy=(value:Copy)=>value.ro.trim().length>0&&value.en.trim().length>0;

export function buildAdaptivePlanDraft(input:{
 bundle_label:Copy;
 signpost?:SignpostDefinition;
 trigger?:TriggerDraft;
 actions?:AdaptiveActionInputs;
}):AdaptivePlanDraft{
 const triggerCondition=input.trigger
  ?copy(
    `${input.trigger.indicator_id} ${comparator(input.trigger.comparator)} ${input.trigger.threshold.toFixed(2)} (prag declarat de utilizator; de evaluat numai pe observații)`,
    `${input.trigger.indicator_id} ${comparator(input.trigger.comparator)} ${input.trigger.threshold.toFixed(2)} (user-declared threshold; evaluate only on observations)`
   )
  :undefined;
 const actionReady=input.actions!==undefined&&nonEmptyCopy(input.actions.then_action)&&nonEmptyCopy(input.actions.stop_action)&&nonEmptyCopy(input.actions.reassess_action);
 const steps:AdaptivePlanStep[]=[
  {
   id:'CEM.ADAPTIVE.RUNTIME.NOW',
   phase:'NOW',
   statement:copy(
    `Acum: păstrează ca opțiune inspectată bundle-ul „${input.bundle_label.ro}”; aceasta este o proiecție de plan, nu implementare reală.`,
    `Now: retain inspected bundle “${input.bundle_label.en}” as the current option; this is a plan projection, not real-world implementation.`
   ),
   readiness:'DEFINED'
  },
  {
   id:'CEM.ADAPTIVE.RUNTIME.WATCH',
   phase:'WATCH',
   statement:input.signpost
    ?copy(`Urmărește indicatorul ${input.signpost.indicator_id}.`,`Watch indicator ${input.signpost.indicator_id}.`)
    :copy('Niciun signpost selectat.','No signpost selected.'),
   readiness:input.signpost?'DEFINED':'MISSING_TRIGGER',
   ...(input.signpost?{indicator_id:input.signpost.indicator_id}: {})
  },
  {
   id:'CEM.ADAPTIVE.RUNTIME.IF',
   phase:'IF',
   statement:triggerCondition??copy('Definește mai întâi un trigger draft.','Define a trigger draft first.'),
   readiness:input.trigger?'DEFINED':'MISSING_TRIGGER',
   ...(input.trigger?{trigger_draft_id:input.trigger.id,trigger_condition:triggerCondition}: {})
  },
  {
   id:'CEM.ADAPTIVE.RUNTIME.THEN',
   phase:'THEN',
   statement:actionReady?input.actions!.then_action:copy('Declară acțiunea contingentă care ar trebui reconsiderată dacă trigger-ul este confirmat.','Declare the contingent action to reconsider if the trigger is confirmed.'),
   readiness:actionReady?'DEFINED':'MISSING_ACTION',
   ...(actionReady?{action:input.actions!.then_action}: {})
  },
  {
   id:'CEM.ADAPTIVE.RUNTIME.STOP',
   phase:'STOP',
   statement:actionReady?input.actions!.stop_action:copy('Declară regula/acțiunea de oprire.','Declare the stop rule/action.'),
   readiness:actionReady?'DEFINED':'MISSING_ACTION',
   ...(actionReady?{action:input.actions!.stop_action}: {})
  },
  {
   id:'CEM.ADAPTIVE.RUNTIME.REASSESS',
   phase:'REASSESS',
   statement:actionReady?input.actions!.reassess_action:copy('Declară cum ar trebui reevaluată decizia.','Declare how the decision should be reassessed.'),
   readiness:actionReady?'DEFINED':'MISSING_ACTION',
   ...(actionReady?{action:input.actions!.reassess_action}: {})
  }
 ];
 return {
  object_type:'AdaptivePlanDraft',
  status:'DRAFT',
  persistence:'EPHEMERAL_NOT_WORKSPACE',
  execution_status:'DESIGN_ONLY_NO_OBSERVED_OUTCOME',
  automation:'NO_AUTOMATIC_ACTIONS',
  bundle_label:input.bundle_label,
  ...(input.trigger?{trigger_draft_id:input.trigger.id}:{}),
  steps
 };
}

const esc=(value:string)=>value.replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]??c));

export function mountAdaptivePlanRuntime(host:HTMLElement,input:{
 lang:Lang;
 bundle_label:Copy;
 signposts:SignpostDefinition[];
 trigger_drafts:TriggerDraft[];
}){
 const {lang}=input;
 const t=(ro:string,en:string)=>lang==='ro'?ro:en;
 let selectedTriggerId=input.trigger_drafts[0]?.id??'';
 let actions:AdaptiveActionInputs|undefined;
 const render=()=>{
  const trigger=input.trigger_drafts.find(item=>item.id===selectedTriggerId);
  const signpost=trigger?input.signposts.find(item=>item.id===trigger.signpost_id):input.signposts[0];
  const plan=buildAdaptivePlanDraft({bundle_label:input.bundle_label,signpost,trigger,actions});
  host.innerHTML=`<section id="adaptivePlanRuntime" class="adaptive-plan-runtime" data-execution-status="${plan.execution_status}">
   <div class="section-heading"><div><p class="eyebrow">OA-7 · ADAPTIVE PLAN</p><h4>${t('NOW / WATCH / IF / THEN / STOP / REASSESS','NOW / WATCH / IF / THEN / STOP / REASSESS')}</h4><p>${t('Acesta este un plan draft prospectiv. Definește ce am face dacă un trigger ar fi confirmat ulterior prin observații; nu execută și nu evaluează acțiuni.','This is a prospective plan draft. It defines what we would do if a trigger were later confirmed by observations; it does not execute or evaluate actions.')}</p></div><span class="adaptive-plan-boundary">${plan.execution_status}</span></div>
   <div class="adaptive-step-grid">${plan.steps.map(step=>`<article data-adaptive-phase="${step.phase}" data-adaptive-readiness="${step.readiness}"><div><strong>${step.phase}</strong><code>${step.readiness}</code></div><p>${esc(step.statement[lang])}</p>${step.indicator_id?`<small>Indicator: ${esc(step.indicator_id)}</small>`:''}${step.trigger_draft_id?`<small>Trigger: ${esc(step.trigger_draft_id)}</small>`:''}</article>`).join('')}</div>
   <form id="adaptivePlanForm">
    <label>${t('Trigger draft','Trigger draft')}<select name="trigger_id" ${input.trigger_drafts.length?'':'disabled'}>${input.trigger_drafts.length?input.trigger_drafts.map(item=>`<option value="${esc(item.id)}" ${item.id===selectedTriggerId?'selected':''}>${esc(item.indicator_id)} ${comparator(item.comparator)} ${item.threshold.toFixed(2)}</option>`).join(''):`<option>${t('Definește mai întâi un trigger draft','Define a trigger draft first')}</option>`}</select></label>
    <label>${t('THEN — acțiune contingentă','THEN — contingent action')}<textarea name="then_action" rows="2" required maxlength="300" ${input.trigger_drafts.length?'':'disabled'}>${actions?esc(actions.then_action[lang]):''}</textarea></label>
    <label>${t('STOP — regulă/acțiune de oprire','STOP — stop rule/action')}<textarea name="stop_action" rows="2" required maxlength="300" ${input.trigger_drafts.length?'':'disabled'}>${actions?esc(actions.stop_action[lang]):''}</textarea></label>
    <label>${t('REASSESS — cum reevaluăm','REASSESS — how to reassess')}<textarea name="reassess_action" rows="2" required maxlength="300" ${input.trigger_drafts.length?'':'disabled'}>${actions?esc(actions.reassess_action[lang]):''}</textarea></label>
    <button type="submit" class="primary" ${input.trigger_drafts.length?'':'disabled'}>${t('Actualizează plan draft','Update plan draft')}</button>
   </form>
   <div class="boundary"><strong>${t('Limită de execuție','Execution boundary')}</strong><p>${t('Nici THEN, STOP, nici REASSESS nu se execută automat. Fără ObservedOutcome, trigger-ul rămâne neevaluat, iar planul este doar o pregătire prospectivă.','THEN, STOP, and REASSESS are never executed automatically. Without ObservedOutcome, the trigger remains unevaluated and the plan is only prospective preparation.')}</p></div>
  </section>`;
  const select=host.querySelector<HTMLSelectElement>('#adaptivePlanForm select[name="trigger_id"]');
  if(select)select.onchange=()=>{selectedTriggerId=select.value;actions=undefined;render();};
  const form=host.querySelector<HTMLFormElement>('#adaptivePlanForm')!;
  form.onsubmit=event=>{
   event.preventDefault();
   if(!form.reportValidity())return;
   const data=new FormData(form);
   const c=(value:string)=>copy(value,value);
   actions={
    then_action:c(String(data.get('then_action')??'').trim()),
    stop_action:c(String(data.get('stop_action')??'').trim()),
    reassess_action:c(String(data.get('reassess_action')??'').trim())
   };
   render();
  };
 };
 render();
}
