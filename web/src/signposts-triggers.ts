import type {IndicatorProjection} from './indicator-objects';

type Lang='ro'|'en';
type Copy=Record<Lang,string>;

export type SignpostDefinition={
 object_type:'Signpost';
 id:string;
 indicator_id:string;
 label:Copy;
 monitoring_role:'INDICATOR_TO_MONITOR';
 timing_role:'EARLY_SIGNAL_OR_STATE_TRACKING';
 source:'OA7_INDICATOR_OBJECT';
};

export type TriggerDraft={
 object_type:'TriggerDraft';
 id:string;
 signpost_id:string;
 indicator_id:string;
 comparator:'LT'|'LTE'|'GTE'|'GT';
 threshold:number;
 unit:'probability';
 origin:'USER_DECLARED';
 evaluation_status:'NOT_EVALUATED_NO_OBSERVED_OUTCOME';
 action_binding_status:'NOT_BOUND_TO_ADAPTIVE_ACTION';
};

export type SignpostTriggerProjection={
 object_type:'SignpostTriggerProjection';
 persistence:'EPHEMERAL_NOT_WORKSPACE';
 automation:'NO_BACKGROUND_MONITORING';
 signposts:SignpostDefinition[];
};

const copy=(ro:string,en:string):Copy=>({ro,en});
const slug=(id:string)=>id.replace(/^CEM\.INDICATOR\./,'').replace(/[^A-Za-z0-9._-]/g,'-');

export function buildSignpostProjection(indicators:IndicatorProjection):SignpostTriggerProjection{
 return {
  object_type:'SignpostTriggerProjection',
  persistence:'EPHEMERAL_NOT_WORKSPACE',
  automation:'NO_BACKGROUND_MONITORING',
  signposts:indicators.indicators.map(({definition})=>({
   object_type:'Signpost',
   id:`CEM.SIGNPOST.${slug(definition.id)}`,
   indicator_id:definition.id,
   label:copy(
    `Urmărește: ${definition.label.ro}`,
    `Watch: ${definition.label.en}`
   ),
   monitoring_role:'INDICATOR_TO_MONITOR',
   timing_role:'EARLY_SIGNAL_OR_STATE_TRACKING',
   source:'OA7_INDICATOR_OBJECT'
  }))
 };
}

export function createTriggerDraft(input:{
 signpost:SignpostDefinition;
 comparator:TriggerDraft['comparator'];
 threshold:number;
}):TriggerDraft{
 if(!Number.isFinite(input.threshold)||input.threshold<0||input.threshold>1)throw new Error('trigger threshold must be within [0,1]');
 return {
  object_type:'TriggerDraft',
  id:`CEM.TRIGGER.DRAFT.${slug(input.signpost.indicator_id)}.${input.comparator}.${String(input.threshold).replace('.','_')}`,
  signpost_id:input.signpost.id,
  indicator_id:input.signpost.indicator_id,
  comparator:input.comparator,
  threshold:input.threshold,
  unit:'probability',
  origin:'USER_DECLARED',
  evaluation_status:'NOT_EVALUATED_NO_OBSERVED_OUTCOME',
  action_binding_status:'NOT_BOUND_TO_ADAPTIVE_ACTION'
 };
}

const esc=(value:string)=>value.replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]??c));
const comparatorLabel=(value:TriggerDraft['comparator'])=>({LT:'<',LTE:'≤',GTE:'≥',GT:'>'}[value]);

export function mountSignpostsTriggers(host:HTMLElement,projection:SignpostTriggerProjection,lang:Lang){
 const t=(ro:string,en:string)=>lang==='ro'?ro:en;
 let drafts:TriggerDraft[]=[];
 const render=()=>{
  host.innerHTML=`<section class="signposts-triggers" id="signpostsTriggers">
   <div class="section-heading"><div><p class="eyebrow">OA-7 · SIGNPOSTS / TRIGGERS</p><h4>${t('Ce urmărim și ce condiție ar cere reevaluare?','What do we watch and what condition would require reassessment?')}</h4><p>${t('Signpost-ul identifică indicatorul de urmărit. Trigger-ul este o condiție prospectivă declarată de utilizator; nu este derivată din model și nu este evaluată automat fără ObservedOutcome.','A signpost identifies the indicator to monitor. A trigger is a prospective user-declared condition; it is not derived from the model and is not automatically evaluated without an ObservedOutcome.')}</p></div><span class="signpost-boundary">${projection.automation}</span></div>
   <div class="signpost-grid">${projection.signposts.map(item=>`<article data-signpost-id="${esc(item.id)}" data-signpost-indicator="${esc(item.indicator_id)}"><h5>${esc(item.label[lang])}</h5><code>${esc(item.id)}</code><dl><dt>Indicator</dt><dd>${esc(item.indicator_id)}</dd><dt>${t('Rol','Role')}</dt><dd>${item.monitoring_role}</dd><dt>${t('Timp','Timing')}</dt><dd>${item.timing_role}</dd></dl></article>`).join('')}</div>
   <form id="triggerDraftForm">
    <label>${t('Signpost','Signpost')}<select name="signpost_id" required>${projection.signposts.map(item=>`<option value="${esc(item.id)}">${esc(item.label[lang])}</option>`).join('')}</select></label>
    <label>${t('Comparator','Comparator')}<select name="comparator"><option value="LTE">≤</option><option value="LT">&lt;</option><option value="GTE">≥</option><option value="GT">&gt;</option></select></label>
    <label>${t('Prag declarat de utilizator','User-declared threshold')}<input name="threshold" type="number" min="0" max="1" step="0.01" required value="0.50"></label>
    <button type="submit" class="primary">${t('Definește trigger draft','Define trigger draft')}</button>
   </form>
   <div id="triggerDrafts" aria-live="polite">${drafts.length?`<div class="trigger-draft-list">${drafts.map(item=>`<article data-trigger-draft="${esc(item.id)}"><strong>${esc(item.indicator_id)} ${comparatorLabel(item.comparator)} ${item.threshold.toFixed(2)}</strong><code>${item.origin}</code><small>${item.evaluation_status}</small><small>${item.action_binding_status}</small><button type="button" data-remove-trigger="${esc(item.id)}">${t('Șterge','Remove')}</button></article>`).join('')}</div>`:`<p class="note">${t('Nu există trigger drafts în această vizualizare.','No trigger drafts exist in this view.')}</p>`}</div>
   <div class="boundary"><strong>${t('Limită de monitorizare','Monitoring boundary')}</strong><p>${t('CEM nu monitorizează surse externe în fundal și nu tratează valoarea simulată curentă drept semnal observat. Trigger-ul va putea fi evaluat numai după introducerea explicită a ObservedOutcome într-un slice ulterior. Acțiunea contingentă nu este definită aici.','CEM does not monitor external sources in the background and does not treat the current simulated value as an observed signal. A trigger can be evaluated only after ObservedOutcome is explicitly introduced in a later slice. The contingent action is not defined here.')}</p></div>
  </section>`;
  const form=host.querySelector<HTMLFormElement>('#triggerDraftForm')!;
  form.onsubmit=event=>{
   event.preventDefault();
   if(!form.reportValidity())return;
   const data=new FormData(form);
   const signpost=projection.signposts.find(item=>item.id===String(data.get('signpost_id')))!;
   const draft=createTriggerDraft({signpost,comparator:String(data.get('comparator')) as TriggerDraft['comparator'],threshold:Number(data.get('threshold'))});
   drafts=[...drafts.filter(item=>item.signpost_id!==draft.signpost_id),draft];
   render();
  };
  host.querySelectorAll<HTMLButtonElement>('[data-remove-trigger]').forEach(button=>button.onclick=()=>{
   drafts=drafts.filter(item=>item.id!==button.dataset.removeTrigger);
   render();
  });
 };
 render();
}
