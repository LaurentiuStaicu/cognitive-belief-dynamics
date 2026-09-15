type Lang='ro'|'en';

export type M1AccessModelResult={
 p_access:number;
 access:boolean;
};

export type M1AccessCondition={
 headline_id:string;
 story_id:string;
 source_id:string;
 image_id:string|null;
 fact_compatible:boolean;
 preview_impression:boolean;
 hneg:number;
 models:Record<'null'|'headline_negativity',M1AccessModelResult>;
};

export type M1AccessData={
 model_version:string;
 model_specification:string;
 baseline_model_specification:string;
 experiment:{
  id:string;
  purpose:string;
  selected_cue:string;
  cue_encoding:{
   type:string;
   control:number;
   treatment:number;
   runtime_sentiment_analysis:boolean;
  };
  parameters:{
   intercept:number;
   beta_hneg:number;
   calibrated:boolean;
  };
  illustrative_access_draw:number;
  conditions:Record<'lower_negativity'|'higher_negativity',M1AccessCondition>;
  empirical_target_id:string;
  validation_pattern_ids:string[];
  interpretation_boundary:string;
 };
};

export type M1AccessTarget={
 id:string;
 pattern_id:string;
 evidence_ref:string;
 provenance_refs:string[];
 integrity_refs:string[];
 counterevidence_refs:string[];
 use:string;
 study:{
  design_family:string;
  randomized_assignment:boolean;
  preregistered_analysis:boolean;
  n_experiments:number;
  n_variants:number;
  n_impressions_min:number;
  n_clicks:number;
  count_note:string;
 };
 effects:{
  outcome:string;
  comparison:string;
  metric:string;
  estimate:number;
  ci?:number[];
  scale_note:string;
  magnitude_use:string;
 }[];
 model_match:string;
 limitations:string;
};

export function mountAccessStage(
 host:HTMLElement,
 lang:Lang,
 data:M1AccessData,
 target:M1AccessTarget,
 openRegistry:()=>void
){
 const t=(ro:string,en:string)=>lang==='ro'?ro:en;
 const locale=lang==='ro'?'ro-RO':'en-GB';
 const p=(n:number)=>n.toLocaleString(locale,{minimumFractionDigits:6,maximumFractionDigits:6});
 const integer=(n:number)=>n.toLocaleString(locale);
 const lower=data.experiment.conditions.lower_negativity;
 const higher=data.experiment.conditions.higher_negativity;
 const delta=higher.models.headline_negativity.p_access-lower.models.headline_negativity.p_access;
 const logOdds=target.effects.find(effect=>effect.metric==='LOG_ODDS_COEFFICIENT');
 const relative=target.effects.find(effect=>effect.metric==='RELATIVE_CHANGE_PERCENT');
 const registeredLimitations=t(
  'Dovezile cauzale principale provin din experimentele istorice Upworthy. O corecție a arhivei din 2024 identifică o perioadă cu probleme probabile de randomizare; administratorii arhivei raportează că rezultatele Robertson rămân aproape identice când analiza este restrânsă la testele fiabile. Cercetări experimentale preliminare recente nu găsesc efectul așteptat al negativității într-un alt context, astfel că CEM tratează direcția ca mecanism candidat delimitat, nu ca o constantă universală.',
  target.limitations
 );
 const registeredCountNote=t(
  'Textul principal al secțiunii Results raportează 53.699 de titluri în eșantionul confirmator filtrat, în timp ce două legende de figură raportează 53.669. CEM păstrează cifra din textul principal și documentează explicit discrepanța de 30 de titluri ca informație de proveniență.',
  target.study.count_note
 );
 const ci=(values:number[])=>values.map(value=>value.toLocaleString(locale,{minimumFractionDigits:3,maximumFractionDigits:3})).join(', ');

 host.innerHTML=`<div class="narrative-stage-heading">
  <div><p class="eyebrow">M1 · ${data.experiment.id}</p><h3>${t('Poarta de acces la titlu: NULL vs Hneg','Headline access gate: NULL vs Hneg')}</h3></div>
  <button id="m1e3Registry">${t('Registrul dovezilor','Evidence Registry')}</button>
 </div>
 <p class="note">${t(
  'Comparator între condiții, fără axă temporală. Povestea, sursa, imaginea și oportunitatea de impresie sunt identice; se schimbă numai indiciul binar Hneg precomputat.',
  'Between-condition comparator with no temporal axis. Story, source, image and impression opportunity are identical; only the precomputed binary Hneg cue changes.'
 )}</p>

 <section class="m1-access-flow" aria-label="${t('Etapele mecanismului de acces','Access mechanism stages')}">
  <span>${t('Preview afișat','Preview rendered')}</span><strong>→</strong><span>Hneg ∈ {0,1}</span><strong>→</strong><span>Paccess</span><strong>→</strong><span>Access</span>
 </section>

 <div class="m1-fixed-invariants">
  <article class="panel"><span>${t('Poveste fixă','Fixed story')}</span><code>${lower.story_id}</code></article>
  <article class="panel"><span>${t('Sursă fixă','Fixed source')}</span><code>${lower.source_id}</code></article>
  <article class="panel"><span>${t('Imagine fixă','Fixed image')}</span><code>${lower.image_id??'NONE'}</code></article>
 </div>

 <div class="m1-access-headlines">
  <article class="panel">
   <p class="eyebrow">${t('CONTROL · NEGATIVITATE MAI REDUSĂ','CONTROL · LOWER NEGATIVITY')}</p>
   <h4>${lower.headline_id}</h4>
   <dl class="narrative-values"><div><dt>Hneg</dt><dd>${lower.hneg}</dd></div><div><dt>PreviewImpression</dt><dd>${lower.preview_impression?t('da','yes'):t('nu','no')}</dd></div><div><dt>${t('Compatibil factual','Fact-compatible')}</dt><dd>${lower.fact_compatible?t('da','yes'):t('nu','no')}</dd></div></dl>
  </article>
  <article class="panel">
   <p class="eyebrow">${t('TRATAMENT · NEGATIVITATE MAI RIDICATĂ','TREATMENT · HIGHER NEGATIVITY')}</p>
   <h4>${higher.headline_id}</h4>
   <dl class="narrative-values"><div><dt>Hneg</dt><dd>${higher.hneg}</dd></div><div><dt>PreviewImpression</dt><dd>${higher.preview_impression?t('da','yes'):t('nu','no')}</dd></div><div><dt>${t('Compatibil factual','Fact-compatible')}</dt><dd>${higher.fact_compatible?t('da','yes'):t('nu','no')}</dd></div></dl>
  </article>
 </div>

 <div class="table-scroll m1-access-table"><table>
  <caption>${t('Comparație exactă între modelul NULL și poarta sensibilă la Hneg','Exact comparison of the NULL model and the Hneg-sensitive gate')}</caption>
  <thead><tr><th>${t('Condiție','Condition')}</th><th>Hneg</th><th>NULL · Paccess</th><th>${t('Poartă Hneg · Paccess','Hneg gate · Paccess')}</th><th>${t('Access ilustrativ','Illustrative Access')}</th></tr></thead>
  <tbody>
   <tr><td>${t('Negativitate mai redusă','Lower negativity')}</td><td>${lower.hneg}</td><td>${p(lower.models.null.p_access)}</td><td>${p(lower.models.headline_negativity.p_access)}</td><td>${lower.models.headline_negativity.access?t('da','yes'):t('nu','no')}</td></tr>
   <tr><td>${t('Negativitate mai ridicată','Higher negativity')}</td><td>${higher.hneg}</td><td>${p(higher.models.null.p_access)}</td><td>${p(higher.models.headline_negativity.p_access)}</td><td>${higher.models.headline_negativity.access?t('da','yes'):t('nu','no')}</td></tr>
  </tbody>
 </table></div>

 <div class="m1-model-grid">
  <article class="panel"><p class="eyebrow">M1.E3-NULL</p><h4>${t('Poartă insensibilă la indiciu','Cue-insensitive gate')}</h4><p class="equation">logit(Paccess) = b0</p><p>${t('Cele două condiții converg:','The two conditions converge:')} <strong>${p(lower.models.null.p_access)}</strong>.</p></article>
  <article class="panel"><p class="eyebrow">M1.E3-A</p><h4>${t('Poartă sensibilă la Hneg','Hneg-sensitive gate')}</h4><p class="equation">logit(Paccess) = b0 + beta_hneg × Hneg</p><p>ΔPaccess = <strong>${p(delta)}</strong></p></article>
 </div>

 <p class="note">${t(
  'Coeficienții CEM sunt demonstrativi: b0=' + data.experiment.parameters.intercept + ', beta_hneg=' + data.experiment.parameters.beta_hneg + '. Access-ul binar folosește aceeași tragere ilustrativă ' + data.experiment.illustrative_access_draw + ' în ambele condiții; validarea se bazează pe contrastul Paccess, nu pe un singur draw.',
  'CEM coefficients are demonstrative: b0=' + data.experiment.parameters.intercept + ', beta_hneg=' + data.experiment.parameters.beta_hneg + '. Binary Access uses the same illustrative draw ' + data.experiment.illustrative_access_draw + ' in both conditions; validation is based on the Paccess contrast, not on one draw.'
 )}</p>

 <section class="m1-benchmark">
  <h4>${t('Țintă empirică pentru direcție, nu calibrare','Empirical target for direction, not calibration')}</h4>
  <p><strong>${target.id}</strong> · ${integer(target.study.n_experiments)} ${t('experimente','experiments')} · ${integer(target.study.n_variants)} ${t('variante de titlu','headline variants')} · &gt;${integer(target.study.n_impressions_min)} ${t('impresii','impressions')} · ${integer(target.study.n_clicks)} ${t('clickuri','clicks')}.</p>
  <ul>
   ${logOdds?`<li>${t('Coeficient publicat pentru proporția standardizată de cuvinte negative','Published coefficient for standardized negative-word proportion')}: β=${logOdds.estimate.toLocaleString(locale,{maximumFractionDigits:3})}${logOdds.ci?` · 99% CI [${ci(logOdds.ci)}]`:''}.</li>`:''}
   ${relative?`<li>${t('Context de magnitudine raportat de autori pentru un cuvânt negativ suplimentar într-un titlu de lungime medie','Source-reported magnitude context for one additional negative word in an average-length headline')}: ~${relative.estimate.toLocaleString(locale,{maximumFractionDigits:1})}% ${t('creștere relativă a CTR','relative CTR increase')}.</li>`:''}
  </ul>
  <p class="note">${t(
   'Aceste valori nu sunt copiate în beta_hneg. CEM verifică numai predicția direcțională higher Hneg → higher Paccess și contrastul cu NULL.',
   'These values are not copied into beta_hneg. CEM checks only the directional higher Hneg → higher Paccess prediction and the contrast with NULL.'
  )}</p>
  <details><summary>${t('Limitări și proveniență','Limitations and provenance')}</summary><p>${registeredLimitations}</p><p class="note">${registeredCountNote}</p></details>
 </section>

 <div class="boundary"><strong>${t('Delimitare științifică','Scientific boundary')}</strong><p>${t(
  'PreviewImpression ≠ Access ≠ atenție ≠ encodare ≠ convingere ≠ EngageIntent ≠ Share. Un non-click păstrează impresia preview-ului. M1.E3 nu propagă Access în stările M0, M1.E1 sau M1.E2.',
  'PreviewImpression ≠ Access ≠ attention ≠ encoding ≠ belief ≠ EngageIntent ≠ Share. A non-click preserves the preview impression. M1.E3 does not propagate Access into M0, M1.E1 or M1.E2 states.'
 )}</p></div>`;

 host.querySelector<HTMLButtonElement>('#m1e3Registry')!.onclick=openRegistry;
}
