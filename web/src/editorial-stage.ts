type Lang='ro'|'en';

export type M1EditorialCondition={
 emphasis:number;
 selected_unit_ids:string[];
 all_selected_fact_compatible:boolean;
 observed_balance:number;
 issue_appraisal:number;
};

export type EmpiricalTarget={
 id:string;
 pattern_id:string;
 evidence_ref:string;
 use:string;
 study:{randomized:boolean;preregistered:boolean;n_recruited:number;n_analyzed:number;event_count:number};
 effects:{outcome:string;comparison:string;estimate_pp:number;ci95?:number[];cohens_d?:number}[];
 model_match:string;
 limitations:string;
};

export type M1EditorialData={
 model_version:string;
 model_specification:string;
 baseline_model_specification:string;
 experiment:{
  id:string;
  purpose:string;
  information_pool:{unit_id:string;event_id:string;valence:number;compatible_with_facts:boolean}[];
  selection_budget:number;
  appraisal_gain:number;
  conditions:Record<'negative'|'neutral'|'positive',M1EditorialCondition>;
  nested_null:{selected_unit_ids:string[];observed_balance:number;issue_appraisal:number};
  empirical_target_id:string;
  interpretation_boundary:string;
 };
};

export function mountEditorialStage(
 host:HTMLElement,
 lang:Lang,
 data:M1EditorialData,
 target:EmpiricalTarget,
 openRegistry:()=>void
){
 const t=(ro:string,en:string)=>lang==='ro'?ro:en;
 let condition:'negative'|'neutral'|'positive'='negative';
 const fmt=(n:number)=>n.toLocaleString(lang==='ro'?'ro-RO':'en-GB',{minimumFractionDigits:3,maximumFractionDigits:3});
 const label=(id:string)=>({negative:t('Accent negativ','Negative emphasis'),neutral:t('Selecție neutră','Neutral selection'),positive:t('Accent pozitiv','Positive emphasis')} as Record<string,string>)[id];

 const render=()=>{
  const c=data.experiment.conditions[condition];
  const selected=new Set(c.selected_unit_ids);
  host.innerHTML=`<div class="narrative-stage-heading"><div><p class="eyebrow">M1 · ${data.experiment.id}</p><h3>${t('Accent editorial și informația observată','Editorial emphasis and observed information')}</h3></div><button id="m1Registry">${t('Registrul dovezilor','Evidence Registry')}</button></div>
  <p class="note">${t('Aceeași lume factuală de bază este păstrată. Se schimbă numai ce unități compatibile cu faptele intră în eșantionul observat.','The same underlying factual world is held fixed. Only which fact-compatible units enter the observed sample changes.')}</p>
  <div class="stage-options m1-condition-switch" role="group" aria-label="${t('Condiția editorială','Editorial condition')}">${(['negative','neutral','positive'] as const).map(id=>`<button data-m1-condition="${id}" aria-pressed="${id===condition}">${label(id)}</button>`).join('')}</div>
  <div class="m1-pool" aria-label="${t('Pool-ul informațional și selecția curentă','Information pool and current selection')}">${data.experiment.information_pool.map(u=>`<div class="m1-unit ${selected.has(u.unit_id)?'selected':''}" data-valence="${u.valence<0?'negative':u.valence>0?'positive':'neutral'}"><span>${u.unit_id}</span><strong>${fmt(u.valence)}</strong><small>${u.compatible_with_facts?t('compatibil factual','fact-compatible'):t('neverificat','unchecked')}</small></div>`).join('')}</div>
  <dl class="narrative-values m1-values"><div><dt>Eedit</dt><dd>${fmt(c.emphasis)}</dd></div><div><dt>Sobs</dt><dd>${fmt(c.observed_balance)}</dd></div><div><dt>Aissue</dt><dd>${fmt(c.issue_appraisal)}</dd></div></dl>
  <p class="narrative-event"><strong>${label(condition)}:</strong> ${t('sunt selectate','selects')} ${c.selected_unit_ids.join(', ')}.</p>
  <details><summary>${t('Compară cu modelul-null','Compare with nested null model')}</summary><p>${t('Cu selecția editorială dezactivată, toate condițiile văd întregul pool, Sobs =','With editorial selection disabled, all conditions see the full pool, Sobs =')} ${fmt(data.experiment.nested_null.observed_balance)}, Aissue = ${fmt(data.experiment.nested_null.issue_appraisal)}.</p></details>
  <section class="m1-benchmark"><h4>${t('Benchmark empiric, nu parametru','Empirical benchmark, not a parameter')}</h4><p>${t('Studiu randomizat, preregistrat:','Randomized, preregistered study:')} N=${target.study.n_recruited.toLocaleString(lang==='ro'?'ro-RO':'en-GB')}, ${t('analiza principală','main analysis')} n=${target.study.n_analyzed.toLocaleString(lang==='ro'?'ro-RO':'en-GB')}, ${target.study.event_count} ${t('evenimente','events')}.</p><ul>${target.effects.filter(e=>e.comparison==='negative_vs_neutral').map(e=>`<li>${e.outcome}: ${e.estimate_pp.toLocaleString(lang==='ro'?'ro-RO':'en-GB',{maximumFractionDigits:2})} pp${e.ci95?` · 95% CI [${e.ci95[0]}, ${e.ci95[1]}]`:''}</li>`).join('')}</ul><p class="note">${t('M1 validează numai direcția și contrastul cu modelul-null; nu ajustează gain-ul pentru a reproduce aceste procente.','M1 validates only direction and the nested-null contrast; it does not tune the gain to reproduce these percentages.')}</p></section>
  <div class="boundary"><strong>${t('Delimitare științifică','Scientific boundary')}</strong><p>${t('Experimentul publicat susține faptul că prezentări factual corecte cu accente diferite pot schimba evaluările și opiniile. Nu identifică însă Eedit, Sobs, Aissue sau câștigul de 0,25 din această implementare; acestea sunt construcții M1 de referință și nu sunt calibrate la efectul publicat.','The published experiment supports that factually accurate presentations with different emphases can shift evaluations and opinions. It does not identify Eedit, Sobs, Aissue, or the 0.25 gain used here; these are M1 reference constructs and are not calibrated to the published effect.')}</p></div>`;
  host.querySelectorAll<HTMLButtonElement>('[data-m1-condition]').forEach(b=>b.onclick=()=>{condition=b.dataset.m1Condition as typeof condition;render();});
  host.querySelector<HTMLButtonElement>('#m1Registry')!.onclick=openRegistry;
 };
 render();
}
