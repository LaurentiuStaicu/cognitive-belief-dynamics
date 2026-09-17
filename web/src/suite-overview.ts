type Lang='ro'|'en';

type SuiteOverviewOptions={
 lang:Lang;
 softwareVersion:string;
 modelSpecification:string;
 variableCount:number;
 moduleCount:number;
 referenceCount:number;
 validationCount:number;
 openUnderstanding:(mode:'theory'|'mechanisms'|'tour'|'active')=>void;
 openView:(view:'structure'|'runs'|'comparison'|'planning'|'reference'|'process')=>void;
};

const esc=(value:string)=>value.replace(/[&<>"']/g,char=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]!));

export function mountSuiteOverview(host:HTMLElement,options:SuiteOverviewOptions){
 const {lang}=options;
 const t=(ro:string,en:string)=>lang==='ro'?ro:en;
 host.innerHTML=`<section class="suite-overview" data-suite-standard="InfoClar Model Suite Design Standard v1.1" aria-labelledby="suiteOverviewTitle">
  <div class="suite-overview-heading">
   <div>
    <p class="eyebrow">INFOCLAR MODEL SUITE · v1.1</p>
    <h2 id="suiteOverviewTitle">${t('Model cognitiv epistemic','Cognitive Epistemic Model')}</h2>
    <p>${t('O singură suprafață simplificată pentru a vedea mecanismele, a învăța teoria, a urmări starea modelului și a accesa instrumentele auxiliare.','One simplified surface for seeing the mechanisms, learning the theory, tracking model state and reaching supporting tools.')}</p>
   </div>
  </div>

  <div class="suite-grid">
   <section class="panel suite-panel suite-model-panel" aria-labelledby="suiteModelTitle">
    <div class="suite-panel-heading"><div><p class="eyebrow">${t('VIZUALIZAREA MODELULUI','MODEL VISUALIZATION')}</p><h3 id="suiteModelTitle">${t('Cum circulă informația prin model','How information moves through the model')}</h3></div><button type="button" data-suite-view="structure">${t('Deschide harta completă','Open full map')}</button></div>
    <p class="suite-panel-intro">${t('Diagrama păstrează forma specifică modelului cognitiv: expunerea și proprietățile mesajului modifică stări interne, iar aceste stări influențează judecata și acțiunea.','The diagram keeps the cognitive model’s own form: exposure and message properties change internal states, which then influence judgment and action.')}</p>
    <div class="cem-mechanism-map" role="img" aria-label="${t('Hartă conceptuală a principalelor mecanisme Cognitive Epistemic Model','Conceptual map of the main Cognitive Epistemic Model mechanisms')}">
     <div class="cem-map-column cem-map-inputs">
      <span class="cem-map-label">${t('Intrări','Inputs')}</span>
      <button type="button" class="cem-node" data-suite-learn="mechanisms"><strong>${t('Expunere','Exposure')}</strong><small>Nexp · Vcontent · Hneg</small></button>
      <button type="button" class="cem-node" data-suite-learn="mechanisms"><strong>${t('Sursă și prezentare','Source & presentation')}</strong><small>T · Eedit · Fpres</small></button>
     </div>
     <div class="cem-map-flow" aria-hidden="true">→</div>
     <div class="cem-map-column cem-map-states">
      <span class="cem-map-label">${t('Stări cognitive','Cognitive states')}</span>
      <button type="button" class="cem-node" data-suite-learn="mechanisms"><strong>${t('Familiaritate','Familiarity')}</strong><small>F</small></button>
      <button type="button" class="cem-node" data-suite-learn="mechanisms"><strong>${t('Evaluare și acces','Evaluation & access')}</strong><small>Aissue · Paccess · Pengage</small></button>
      <button type="button" class="cem-node" data-suite-learn="mechanisms"><strong>${t('Convingere și acuratețe','Belief & accuracy')}</strong><small>B · W</small></button>
     </div>
     <div class="cem-map-flow" aria-hidden="true">→</div>
     <div class="cem-map-column cem-map-outcomes">
      <span class="cem-map-label">${t('Rezultate','Outcomes')}</span>
      <button type="button" class="cem-node" data-suite-view="runs"><strong>${t('Judecată','Judgment')}</strong><small>${t('scenarii și traiectorii','scenarios & trajectories')}</small></button>
      <button type="button" class="cem-node" data-suite-view="planning"><strong>${t('Acțiune','Action')}</strong><small>Share · EngageIntent · Access</small></button>
     </div>
    </div>
    <div class="suite-inline-actions"><button type="button" class="primary" data-suite-learn="mechanisms">${t('Explorează mecanismele','Explore mechanisms')}</button><button type="button" data-suite-view="comparison">${t('Compară scenarii','Compare scenarios')}</button></div>
   </section>

   <section class="panel suite-panel suite-theory-panel" aria-labelledby="suiteTheoryTitle">
    <p class="eyebrow">THEORY / LEARN</p>
    <h3 id="suiteTheoryTitle">${t('Înțelege înainte să interpretezi','Understand before interpreting')}</h3>
    <p>${t('Teoria explică ce reprezintă fiecare variabilă, ce relații sunt executabile, ce este doar conceptual și unde sunt limitele de interpretare.','Theory explains what each variable represents, which relations are executable, what remains conceptual and where interpretation must stop.')}</p>
    <div class="suite-learning-actions">
     <button type="button" class="primary" data-suite-learn="theory">${t('Deschide teoria','Open theory')}</button>
     <button type="button" data-suite-learn="tour">${t('Tur ghidat','Guided tour')}</button>
     <button type="button" data-suite-learn="active">${t('Învățare activă','Active learning')}</button>
     <button type="button" data-suite-view="process">${t('Metodologie','Methodology')}</button>
    </div>
    <div class="suite-boundary-card"><strong>${t('Principiu de utilizare','Use principle')}</strong><p>${t('Culorile, scorurile sau traseele nu înlocuiesc statutul epistemic și explicațiile textuale.','Colors, scores and paths never replace epistemic status and textual explanation.')}</p></div>
   </section>

   <section class="panel suite-panel suite-dashboard-panel" aria-labelledby="suiteDashboardTitle">
    <p class="eyebrow">DASHBOARD</p>
    <h3 id="suiteDashboardTitle">${t('Starea modelului','Model state')}</h3>
    <div class="suite-metrics">
     <div><span>${t('Specificație activă','Active specification')}</span><strong>${esc(options.modelSpecification)}</strong></div>
     <div><span>${t('Versiune software','Software version')}</span><strong>${esc(options.softwareVersion)}</strong></div>
     <div><span>${t('Variabile înregistrate','Registered variables')}</span><strong>${options.variableCount}</strong></div>
     <div><span>${t('Module conceptuale','Conceptual modules')}</span><strong>${options.moduleCount}</strong></div>
     <div><span>${t('Referințe','References')}</span><strong>${options.referenceCount}</strong></div>
     <div><span>${t('Validări înregistrate','Registered validations')}</span><strong>${options.validationCount}</strong></div>
    </div>
    <div class="suite-status-row"><span class="epistemic-status" data-status="EXECUTABLE">${t('M1.E1–E3 executabile','M1.E1–E3 executable')}</span><span class="epistemic-status" data-status="CANDIDATE">${t('M1.E4 pre-human','M1.E4 pre-human')}</span></div>
   </section>

   <section class="panel suite-panel suite-aux-panel" aria-labelledby="suiteAuxTitle">
    <p class="eyebrow">${t('PANOU AUXILIAR','AUXILIARY')}</p>
    <h3 id="suiteAuxTitle">${t('Context, limite și extensii','Context, boundaries & extensions')}</h3>
    <div class="suite-aux-list">
     <article><strong>${t('Calibrare','Calibration')}</strong><p>${t('Nu este activă înainte de v1. Arhitectura păstrează un punct de extensie pentru un modul post-v1 cu încărcare de fișiere de date.','Not active before v1. The architecture keeps an extension point for a post-v1 module with data-file upload.')}</p></article>
     <article><strong>Pencode</strong><p>${t('Rămâne neidentificat și blocat; nu este înlocuit de proxy-uri UI.','Remains unidentified and blocked; it is not replaced by UI proxies.')}</p></article>
     <article><strong>${t('Validare umană','Human validation')}</strong><p>${t('Rămâne un program extern viitor; aplicația curentă nu este o interfață de recrutare sau calibrare populațională.','Remains a future external program; the current app is not a recruitment or population-calibration interface.')}</p></article>
    </div>
    <div class="suite-inline-actions"><button type="button" data-suite-view="reference">${t('Registru științific','Scientific registry')}</button><button type="button" data-suite-view="planning">${t('Planificare','Planning')}</button></div>
   </section>
  </div>
 </section>`;

 host.querySelectorAll<HTMLButtonElement>('[data-suite-learn]').forEach(button=>button.onclick=()=>options.openUnderstanding(button.dataset.suiteLearn as 'theory'|'mechanisms'|'tour'|'active'));
 host.querySelectorAll<HTMLButtonElement>('[data-suite-view]').forEach(button=>button.onclick=()=>options.openView(button.dataset.suiteView as 'structure'|'runs'|'comparison'|'planning'|'reference'|'process'));
}
