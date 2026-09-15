type Lang='ro'|'en';

export type PresentationModelResult={
 confirmation:number;
 refutation:number;
 contrast:number;
 confirmation_engage_intent?:boolean;
 refutation_engage_intent?:boolean;
};

export type M1PresentationData={
 model_version:string;
 model_specification:string;
 baseline_model_specification:string;
 experiment:{
  id:string;
  purpose:string;
  semantic_proposition_id:string;
  semantic_signature:string;
  fact_compatible:boolean;
  frames:string[];
  illustrative_engage_intent_draw:number;
  parameters:Record<string,number>;
  conditions:Record<'congruent'|'counter_attitudinal',{
   prior_stance:number;
   message_stance:number;
   congruence:number;
   models:Record<'null'|'frame_only'|'frame_congruence',PresentationModelResult>;
  }>;
  empirical_target_ids:string[];
  interpretation_boundary:string;
 };
};

type EmpiricalTarget={
 id:string;
 study:{n_recruited:number;n_analyzed:number;event_count:number};
 effects:{outcome:string;comparison:string;estimate_pp:number}[];
 limitations:string;
};

export function mountPresentationStage(
 host:HTMLElement,
 lang:Lang,
 data:M1PresentationData,
 targets:EmpiricalTarget[],
 openRegistry:()=>void
){
 const t=(ro:string,en:string)=>lang==='ro'?ro:en;
 const fmt=(n:number)=>n.toLocaleString(lang==='ro'?'ro-RO':'en-GB',{minimumFractionDigits:3,maximumFractionDigits:3});
 let audience:'congruent'|'counter_attitudinal'='congruent';

 const modelLabel=(id:string)=>({
  null:t('NULL · fără variație de frame','NULL · presentation normalized'),
  frame_only:t('A · numai frame','A · frame only'),
  frame_congruence:t('B · frame × congruență','B · frame × congruence')
 } as Record<string,string>)[id];

 const render=()=>{
  const c=data.experiment.conditions[audience];
  host.innerHTML=`<div class="narrative-stage-heading"><div><p class="eyebrow">M1 · ${data.experiment.id}</p><h3>${t('Framing semantic echivalent × congruență','Semantic-equivalent framing × congruence')}</h3></div><button id="m1e2Registry">${t('Registrul dovezilor','Evidence Registry')}</button></div>
  <p class="note">${t('Sensul propoziției și compatibilitatea factuală rămân identice. Se schimbă numai prezentarea confirmation/refutation și relația dintre mesaj și atitudinea anterioară relevantă sarcinii.','Proposition meaning and factual compatibility remain identical. Only confirmation/refutation presentation and the message–prior-attitude relation change.')}</p>
  <div class="m1-semantic-pair"><article><p class="eyebrow">confirmation</p><strong>TRUE that p</strong><small>${data.experiment.semantic_signature}</small></article><article><p class="eyebrow">refutation</p><strong>FALSE that not-p</strong><small>${data.experiment.semantic_signature}</small></article></div>
  <div class="stage-options m1-condition-switch" role="group" aria-label="${t('Congruența mesajului','Message congruence')}"><button data-m1e2-audience="congruent" aria-pressed="${audience==='congruent'}">${t('Congruent','Congruent')}</button><button data-m1e2-audience="counter_attitudinal" aria-pressed="${audience==='counter_attitudinal'}">${t('Counter-attitudinal','Counter-attitudinal')}</button></div>
  <dl class="narrative-values"><div><dt>Fpres</dt><dd>±1</dd></div><div><dt>Gatt</dt><dd>${fmt(c.congruence)}</dd></div><div><dt>${t('Compatibil factual','Fact-compatible')}</dt><dd>${data.experiment.fact_compatible?t('da','yes'):t('nu','no')}</dd></div></dl>
  <div class="m1-model-grid">${(['null','frame_only','frame_congruence'] as const).map(id=>{const m=c.models[id];return `<article class="panel"><h4>${modelLabel(id)}</h4><div class="m1-model-bars"><div><span>confirmation</span><progress max="1" value="${m.confirmation}"></progress><strong>${fmt(m.confirmation)}</strong></div><div><span>refutation</span><progress max="1" value="${m.refutation}"></progress><strong>${fmt(m.refutation)}</strong></div></div><p>Δ = ${fmt(m.contrast)}</p></article>`;}).join('')}</div>
  <section class="m1-benchmark"><h4>${t('Ținte empirice de discriminare','Empirical discrimination targets')}</h4><ul>${targets.map(target=>`<li><strong>${target.id}</strong> · N=${target.study.n_recruited.toLocaleString(lang==='ro'?'ro-RO':'en-GB')} · ${target.effects.map(e=>`${e.comparison}: ${e.estimate_pp.toLocaleString(lang==='ro'?'ro-RO':'en-GB',{maximumFractionDigits:1})} pp`).join('; ')}</li>`).join('')}</ul><p class="note">${t('Valorile publicate sunt benchmarkuri, nu coeficienții modelului. B este păstrat numai dacă reproduce predicția suplimentară de moderare pe care A nu o poate reproduce.','Published values are benchmarks, not model coefficients. B is retained only if it reproduces the additional moderation prediction that A cannot reproduce.')}</p></section>
  <div class="boundary"><strong>${t('Delimitare științifică','Scientific boundary')}</strong><p>${t('Gatt este o relație task-specifică, nu ideologie sau partid. Pengage este probabilitate de engagement activ în sarcina de referință, iar EngageIntent este distinct de M0 Share. Nici dificultatea cognitivă, nici afectul negativ nu sunt mediatori obligatorii în această versiune.','Gatt is a task-specific relation, not ideology or party. Pengage is active-engagement probability in the reference task, and EngageIntent is distinct from M0 Share. Neither cognitive difficulty nor negative affect is a required mediator in this version.')}</p></div>`;
  host.querySelectorAll<HTMLButtonElement>('[data-m1e2-audience]').forEach(b=>b.onclick=()=>{audience=b.dataset.m1e2Audience as typeof audience;render();});
  host.querySelector<HTMLButtonElement>('#m1e2Registry')!.onclick=openRegistry;
 };
 render();
}
