type Lang='ro'|'en';

type ContextView='structure'|'runs'|'comparison'|'planning'|'reference'|'process';
type LearnMode='theory'|'mechanisms'|'world-model'|'tour'|'active';
type AuxTool='search'|'inspector';

type SuiteOverviewOptions={
 lang:Lang;
 softwareVersion:string;
 modelSpecification:string;
 variableCount:number;
 moduleCount:number;
 referenceCount:number;
 validationCount:number;
 openUnderstanding:(mode:LearnMode)=>void;
 openView:(view:ContextView)=>void;
 openTool:(tool:AuxTool)=>void;
};

const esc=(value:string)=>value.replace(/[&<>"']/g,char=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot',"'":'&#39;'}[char]??char));

export function mountSuiteOverview(host:HTMLElement,options:SuiteOverviewOptions){
 const {lang}=options;
 const t=(ro:string,en:string)=>lang==='ro'?ro:en;
 host.innerHTML=`<section class="suite-overview infoclar-primary-shell" data-suite-standard="InfoClar Model Suite Design Standard v1.1" aria-label="${t('Suprafața principală Cognitive Epistemic Model','Cognitive Epistemic Model primary surface')}">
  <div class="suite-grid">
   <section class="panel suite-panel suite-model-panel" aria-labelledby="suiteModelTitle">
    <div class="suite-panel-heading"><div><p class="eyebrow">${t('VIZUALIZAREA MODELULUI','MODEL VISUALIZATION')}</p><h2 id="suiteModelTitle">${t('Cum se construiește și se actualizează reprezentarea','How the representation is constructed and updated')}</h2></div><span class="suite-priority-badge">${t('SUPRAFAȚĂ DOMINANTĂ','DOMINANT SURFACE')}</span></div>
    <p class="suite-panel-intro">${t('Urmează fluxul de la informația disponibilă la informația observată, stări cognitive, model intern, judecată și acțiune. Selectează un mecanism pentru explicația lui, nu doar pentru o valoare.','Follow the flow from available information to observed information, cognitive states, the internal model, judgment and action. Select a mechanism for its explanation, not merely a value.')}</p>
    <div class="cem-mechanism-map" aria-label="${t('Hartă conceptuală a principalelor mecanisme Cognitive Epistemic Model','Conceptual map of the main Cognitive Epistemic Model mechanisms')}">
     <div class="cem-map-column cem-map-inputs"><span class="cem-map-label">${t('Informație și context','Information & context')}</span>
      <button type="button" class="cem-node" data-suite-learn="mechanisms"><strong>${t('Expunere și selecție','Exposure & selection')}</strong><small>Nexp · Vcontent · Eedit · Hneg</small></button>
      <button type="button" class="cem-node" data-suite-learn="mechanisms"><strong>${t('Sursă și prezentare','Source & presentation')}</strong><small>T · Fpres · PreviewImpression</small></button>
     </div><div class="cem-map-flow" aria-hidden="true">→</div>
     <div class="cem-map-column cem-map-states"><span class="cem-map-label">${t('Procesare și reprezentare','Processing & representation')}</span>
      <button type="button" class="cem-node" data-suite-learn="mechanisms"><strong>${t('Familiaritate și corecție','Familiarity & correction')}</strong><small>F · C</small></button>
      <button type="button" class="cem-node cem-node-world" data-suite-learn="world-model"><strong>${t('MOD.14 · Modelul realității','MOD.14 · World model')}</strong><small>Pprior · LR → Pwm · Uwm</small></button>
      <button type="button" class="cem-node" data-suite-learn="mechanisms"><strong>${t('Evaluare, convingere, acuratețe','Appraisal, belief, accuracy')}</strong><small>Aissue · B · W</small></button>
     </div><div class="cem-map-flow" aria-hidden="true">→</div>
     <div class="cem-map-column cem-map-outcomes"><span class="cem-map-label">${t('Rezultate observabile','Observable outcomes')}</span>
      <button type="button" class="cem-node" data-suite-view="runs"><strong>${t('Judecată și traiectorii','Judgment & trajectories')}</strong><small>${t('scenarii de referință','reference scenarios')}</small></button>
      <button type="button" class="cem-node" data-suite-view="planning"><strong>${t('Acțiune','Action')}</strong><small>Share · EngageIntent · Access</small></button>
     </div>
    </div>
    <div class="suite-inline-actions"><button type="button" class="primary" data-suite-learn="world-model">${t('Explorează MOD.14','Explore MOD.14')}</button><button type="button" data-suite-learn="mechanisms">${t('Explică mecanismele','Explain mechanisms')}</button><button type="button" data-suite-view="structure">${t('Hartă tehnică','Technical map')}</button><button type="button" data-suite-view="comparison">${t('Compară scenarii','Compare scenarios')}</button></div>
   </section>

   <section class="panel suite-panel suite-theory-panel" aria-labelledby="suiteTheoryTitle">
    <p class="eyebrow">THEORY / LEARN</p><h2 id="suiteTheoryTitle">${t('Teorie legată direct de mecanisme','Theory linked directly to mechanisms')}</h2>
    <p>${t('Aprofundează definițiile, dovezile, ipotezele și limitele fără a părăsi suprafața principală. Nivelurile EMPIRICAL, EXECUTABLE, CONCEPTUAL și INTERPRETIVE rămân vizibile.','Open definitions, evidence, hypotheses and boundaries without leaving the primary surface. EMPIRICAL, EXECUTABLE, CONCEPTUAL and INTERPRETIVE levels remain visible.')}</p>
    <div class="suite-learning-actions"><button type="button" class="primary" data-suite-learn="theory">${t('Teorie','Theory')}</button><button type="button" data-suite-learn="world-model">MOD.14</button><button type="button" data-suite-learn="tour">${t('Tur ghidat','Guided tour')}</button><button type="button" data-suite-learn="active">${t('Învățare activă','Active learning')}</button></div>
    <div id="suiteTheoryContext" class="suite-context-slot suite-theory-context" aria-live="polite"></div>
   </section>

   <section class="panel suite-panel suite-dashboard-panel" aria-labelledby="suiteDashboardTitle">
    <p class="eyebrow">DASHBOARD</p><h2 id="suiteDashboardTitle">${t('Starea și maturitatea modelului','Model state & maturity')}</h2>
    <div class="suite-metrics"><div><span>${t('Specificație','Specification')}</span><strong>${esc(options.modelSpecification)}</strong></div><div><span>${t('Versiune','Version')}</span><strong>${esc(options.softwareVersion)}</strong></div><div><span>${t('Variabile canonice','Canonical variables')}</span><strong>${options.variableCount}</strong></div><div><span>${t('Module conceptuale','Conceptual modules')}</span><strong>${options.moduleCount}</strong></div><div><span>${t('Referințe','References')}</span><strong>${options.referenceCount}</strong></div><div><span>${t('Validări','Validations')}</span><strong>${options.validationCount}</strong></div></div>
    <div class="suite-status-row"><span class="epistemic-status" data-status="EXECUTABLE">${t('M1.E1–E3 executabile','M1.E1–E3 executable')}</span><span class="epistemic-status" data-status="CONCEPTUAL">${t('MOD.14 mixt: empiric / executabil / conceptual / interpretativ','MOD.14 mixed: empirical / executable / conceptual / interpretive')}</span></div>
    <p class="suite-panel-intro">${t('Phase M rămâne neschimbată. M1.E4, Pencode și validarea populațională nu sunt reactivate.','Phase M remains unchanged. M1.E4, Pencode and population validation are not reactivated.')}</p>
   </section>

   <section class="panel suite-panel suite-aux-panel" aria-labelledby="suiteAuxTitle">
    <p class="eyebrow">${t('CONTEXT / AUXILIAR','CONTEXT / AUXILIARY')}</p><h2 id="suiteAuxTitle">${t('Dovezi, limite și instrumente contextuale','Evidence, boundaries & contextual tools')}</h2>
    <div class="suite-aux-list"><article><strong>${t('Calibrare','Calibration')}</strong><p>${t('Dormantă până după v1; nu există Advanced mode.','Dormant until after v1; there is no Advanced mode.')}</p></article><article><strong>${t('Dezvoltare','Development')}</strong><p>${t('Web-first. Varianta Flatpak este amânată până la v1 sau aproape de v1.','Web-first. Flatpak is deferred until v1 or near-v1.')}</p></article><article><strong>${t('Limită epistemică','Epistemic boundary')}</strong><p>${t('Instrumentele auxiliare nu transformă un construct conceptual într-un rezultat calibrat.','Auxiliary tools do not turn a conceptual construct into a calibrated result.')}</p></article></div>
    <div class="suite-inline-actions"><button type="button" data-suite-view="reference">${t('Registru științific','Scientific registry')}</button><button type="button" data-suite-view="process">${t('Metodologie','Methodology')}</button><button type="button" data-suite-view="planning">${t('Planificare','Planning')}</button><button type="button" data-suite-tool="search">${t('Caută în Semantic Spine','Search Semantic Spine')}</button><button type="button" data-suite-tool="inspector">${t('Inspector contextual','Contextual inspector')}</button></div>
    <div id="suiteAuxContext" class="suite-context-slot suite-aux-context" aria-live="polite"></div>
   </section>
  </div>
 </section>`;
 host.querySelectorAll<HTMLButtonElement>('[data-suite-learn]').forEach(button=>button.onclick=()=>options.openUnderstanding(button.dataset.suiteLearn as LearnMode));
 host.querySelectorAll<HTMLButtonElement>('[data-suite-view]').forEach(button=>button.onclick=()=>options.openView(button.dataset.suiteView as ContextView));
 host.querySelectorAll<HTMLButtonElement>('[data-suite-tool]').forEach(button=>button.onclick=()=>options.openTool(button.dataset.suiteTool as AuxTool));
}
