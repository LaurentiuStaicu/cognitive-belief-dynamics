import {cemDiagnostics,cemProductEdges,cemProductNodes,nodeById,type EpistemicLevel,type ProductLang} from './cem-product-map';

type Lang=ProductLang;
type ContextView='structure'|'runs'|'comparison'|'planning'|'reference'|'process';
type LearnMode='theory'|'mechanisms'|'world-model'|'tour'|'active';
type AuxTool='search'|'inspector';

type SuiteOverviewOptions={
 lang:Lang;
 selectedFocus:string;
 openFocus:(id:string)=>void;
 openUnderstanding:(mode:LearnMode)=>void;
 openTheoryChapter:(slug:string)=>void;
 openReference:(id:string)=>void;
 openView:(view:ContextView)=>void;
 openTool:(tool:AuxTool)=>void;
};

const esc=(value:string)=>value.replace(/[&<>"']/g,char=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]??char));
const statusLabel=(status:EpistemicLevel,lang:Lang)=>({
 EMPIRICAL:{ro:'EMPIRIC',en:'EMPIRICAL'},
 EXECUTABLE:{ro:'EXECUTABIL',en:'EXECUTABLE'},
 CONCEPTUAL:{ro:'CONCEPTUAL',en:'CONCEPTUAL'},
 INTERPRETIVE:{ro:'INTERPRETATIV',en:'INTERPRETIVE'}
}[status][lang]);

export function mountSuiteOverview(host:HTMLElement,options:SuiteOverviewOptions){
 const {lang}=options;
 const t=(ro:string,en:string)=>lang==='ro'?ro:en;
 const selected=options.selectedFocus==='overview'?undefined:nodeById(options.selectedFocus);
 const selectedEdges=selected?cemProductEdges.filter(edge=>edge.source===selected.id||edge.target===selected.id):[];
 const neighbors=new Set(selectedEdges.flatMap(edge=>[edge.source,edge.target]));
 const selectedDiagnosticIds=new Set(selected?cemDiagnostics.filter(diagnostic=>diagnostic.mechanisms.includes(selected.id)||diagnostic.focus===selected.id).map(item=>item.id):[]);
 const orderedDiagnostics=[...cemDiagnostics].sort((a,b)=>Number(selectedDiagnosticIds.has(b.id))-Number(selectedDiagnosticIds.has(a.id)));
 const primaryDiagnostics=orderedDiagnostics.slice(0,4);
 const secondaryDiagnostics=orderedDiagnostics.slice(4);
 const nodeName=(id:string)=>nodeById(id)?.label[lang]??id;
 const statusBadges=(statuses:EpistemicLevel[])=>statuses.map(status=>`<span class="epistemic-status" data-status="${status}">${statusLabel(status,lang)}</span>`).join('');
 const nodeClass=(id:string)=>{
  if(!selected)return 'cem-system-node';
  if(id===selected.id)return 'cem-system-node is-selected';
  if(neighbors.has(id))return 'cem-system-node is-related';
  return 'cem-system-node is-dimmed';
 };
 const edgeClass=(source:string,target:string,level:string)=>{
  const classes=['cem-system-edge',level==='CONCEPTUAL'?'is-conceptual':'is-executable'];
  if(selected&&source!==selected.id&&target!==selected.id)classes.push('is-dimmed');
  else if(selected)classes.push('is-related');
  return classes.join(' ');
 };
 const mapEdges=cemProductEdges.map(edge=>{
  const source=nodeById(edge.source)!;const target=nodeById(edge.target)!;
  return `<line class="${edgeClass(edge.source,edge.target,edge.level)}" data-suite-edge="${edge.id}" x1="${source.x*10}" y1="${source.y*6.2}" x2="${target.x*10}" y2="${target.y*6.2}" marker-end="url(#cemArrow)"/>`;
 }).join('');
 const mapNodes=cemProductNodes.map(node=>`<button type="button" class="${nodeClass(node.id)}" data-suite-focus="${node.id}" aria-pressed="${selected?.id===node.id}" style="--node-x:${node.x}%;--node-y:${node.y}%" aria-label="${esc(node.label[lang])}: ${esc(node.summary[lang])}"><strong>${esc(node.label[lang])}</strong><small>${esc(node.identifiers.join(' · '))}</small></button>`).join('');
 const relevantPaths=selected?`<section class="cem-path-detail" aria-labelledby="cemPathTitle"><div class="cem-path-detail-heading"><div><p class="eyebrow">${t('MECANISM SELECTAT','SELECTED MECHANISM')}</p><h3 id="cemPathTitle">${esc(selected.label[lang])}</h3></div><button type="button" data-suite-focus="overview">${t('Vezi din nou ansamblul','Restore overview')}</button></div><p>${esc(selected.summary[lang])}</p><div class="cem-relevant-paths">${selectedEdges.map(edge=>{const other=edge.source===selected.id?edge.target:edge.source;return `<button type="button" data-suite-focus="${other}" class="cem-path-card"><span>${esc(nodeName(edge.source))} → ${esc(nodeName(edge.target))}</span><small>${esc(edge.label[lang])} · ${edge.level}</small></button>`;}).join('')}</div></section>`:`<section class="cem-map-guide"><strong>${t('Cum citești harta','How to read the map')}</strong><p>${t('Harta păstrează întregul traseu de la informație la acțiune. Selectează orice mecanism pentru a evidenția vecinii și relațiile lui; liniile continue reprezintă trasee executabile de referință, iar cele întrerupte relații conceptuale sau bridge-uri care necesită măsurare specifică.','The map keeps the full path from information to action visible. Select any mechanism to highlight its neighbors and relationships; solid lines show executable reference paths, while dashed lines show conceptual relations or bridges requiring task-specific measurement.')}</p></section>`;
 const theoryNode=selected??nodeById('available-information')!;
 const diagnosticCard=(diagnostic:typeof cemDiagnostics[number])=>`<article class="suite-diagnostic ${selectedDiagnosticIds.has(diagnostic.id)?'is-relevant':''}" data-diagnostic-id="${diagnostic.id}"><div class="suite-diagnostic-heading"><h3>${esc(diagnostic.title[lang])}</h3><div class="suite-diagnostic-statuses">${statusBadges(diagnostic.statuses)}</div></div><p>${esc(diagnostic.why[lang])}</p><dl><dt>${t('Mecanisme','Mechanisms')}</dt><dd>${diagnostic.mechanisms.map(nodeName).map(esc).join(' · ')}</dd><dt>${t('Dovezi','Evidence')}</dt><dd>${esc(diagnostic.evidence[lang])}</dd><dt>${t('Incertitudine','Uncertainty')}</dt><dd>${esc(diagnostic.uncertainty[lang])}</dd></dl><button type="button" data-suite-diagnostic-focus="${diagnostic.focus}">${t('Localizează pe hartă','Locate on map')}</button></article>`;
 const evidenceRefs=selected?.evidenceRefs??[];
 host.innerHTML=`<section class="suite-overview infoclar-primary-shell" data-suite-standard="InfoClar Model Suite Design Standard v1.1" aria-label="${t('Suprafața principală Cognitive Epistemic Model','Cognitive Epistemic Model primary surface')}">
  <div class="suite-grid">
   <section class="panel suite-panel suite-model-panel" aria-labelledby="suiteModelTitle">
    <div class="suite-panel-heading"><div><p class="eyebrow">${t('HARTA SISTEMULUI','SYSTEM MAP')}</p><h1 id="suiteModelTitle">${t('Cum informația devine reprezentare, judecată și acțiune','How information becomes representation, judgment and action')}</h1></div><span class="suite-priority-badge">${t('SUPRAFAȚĂ DOMINANTĂ','DOMINANT SURFACE')}</span></div>
    <p class="suite-panel-intro">${t('Explorează arhitectura CEM fără a pierde complexitatea ei. Denumirile în limbaj natural sunt primare; identificatorii modelului apar secundar.','Explore the CEM architecture without collapsing its complexity. Natural-language names are primary; model identifiers remain secondary.')}</p>
    <div class="cem-system-map" aria-label="${t('Hartă explorabilă a mecanismelor Cognitive Epistemic Model','Explorable map of Cognitive Epistemic Model mechanisms')}">
     <div class="cem-map-stage-label stage-information">${t('INFORMAȚIE','INFORMATION')}</div><div class="cem-map-stage-label stage-representation">${t('ACCES & REPREZENTARE','ACCESS & REPRESENTATION')}</div><div class="cem-map-stage-label stage-integration">${t('INTEGRARE','INTEGRATION')}</div><div class="cem-map-stage-label stage-judgment">${t('JUDECATĂ & ACȚIUNE','JUDGMENT & ACTION')}</div>
     <svg class="cem-system-links" viewBox="0 0 1000 620" aria-hidden="true" preserveAspectRatio="none"><defs><marker id="cemArrow" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 z"/></marker></defs>${mapEdges}</svg>${mapNodes}
    </div>
    ${relevantPaths}
    <div class="suite-inline-actions"><button type="button" data-suite-view="structure">${t('Dependențe tehnice','Technical dependencies')}</button><button type="button" data-suite-view="runs">${t('Rulări de referință','Reference runs')}</button><button type="button" data-suite-view="comparison">${t('Compară scenarii','Compare scenarios')}</button></div>
   </section>

   <section class="panel suite-panel suite-theory-panel" aria-labelledby="suiteTheoryTitle">
    <p class="eyebrow">THEORY / LEARN</p><h2 id="suiteTheoryTitle">${selected?esc(selected.label[lang]):t('Teoria completă a Cognitive Epistemic Model','The complete Cognitive Epistemic Model theory')}</h2>
    <p>${selected?esc(selected.theory[lang]):t('Corpusul bilingv leagă fundamentele cognitive și epistemice de mecanisme, module, literatură, statut epistemic, ipoteze alternative și limite. Selectarea unui nod din hartă aduce aici secțiunea relevantă, iar capitolul complet rămâne la un click distanță.','The bilingual corpus connects cognitive and epistemic foundations to mechanisms, modules, literature, epistemic status, alternative hypotheses and boundaries. Selecting a map node brings the relevant section here, while the complete chapter remains one click away.')}</p>
    <div class="theory-statuses suite-theory-statuses">${statusBadges(theoryNode.statuses)}</div>
    ${selected?`<div class="suite-theory-context-card"><strong>${t('Legătura teoretică','Theory connection')}</strong><p>${esc(selected.summary[lang])}</p><p class="note">${t('Identificatori','Identifiers')}: ${esc(selected.identifiers.join(' · '))}</p></div>`:''}
    <div class="suite-learning-actions"><button type="button" class="primary" data-suite-theory-chapter="${selected?esc(selected.chapterSlug):'what-is-cem'}">${selected?t('Deschide capitolul complet','Open full chapter'):t('Începe cu teoria CEM','Start with CEM theory')}</button><button type="button" data-suite-learn="theory">${t('Răsfoiește corpusul complet','Browse full corpus')}</button><button type="button" data-suite-learn="mechanisms">${t('Mecanisme detaliate','Detailed mechanisms')}</button><button type="button" data-suite-learn="world-model">MOD.14</button></div>
    <details class="suite-learning-more"><summary>${t('Alte instrumente de învățare','More learning tools')}</summary><div class="suite-learning-actions"><button type="button" data-suite-learn="tour">${t('Tur ghidat','Guided tour')}</button><button type="button" data-suite-learn="active">${t('Învățare activă','Active learning')}</button></div></details>
    <div id="suiteTheoryContext" class="suite-context-slot suite-theory-context" aria-live="polite"></div>
   </section>

   <section class="panel suite-panel suite-dashboard-panel" aria-labelledby="suiteDashboardTitle">
    <p class="eyebrow">DASHBOARD</p><h2 id="suiteDashboardTitle">${t('Puncte de presiune epistemică','Epistemic pressure points')}</h2>
    <p class="suite-panel-intro">${t('Dashboard-ul prioritizează problemele pe care utilizatorul trebuie să le înțeleagă în sistem, nu metadatele software-ului. Fiecare diagnostic leagă problema de mecanisme, dovezi, incertitudine și hartă.','The dashboard prioritizes system problems the user needs to understand, not software metadata. Each diagnostic links the issue to mechanisms, evidence, uncertainty and the map.')}</p>
    <div class="suite-diagnostics">${primaryDiagnostics.map(diagnosticCard).join('')}</div>
    ${secondaryDiagnostics.length?`<details class="suite-more-diagnostics"><summary>${t('Alte tensiuni relevante','Other relevant tensions')}</summary><div class="suite-diagnostics">${secondaryDiagnostics.map(diagnosticCard).join('')}</div></details>`:''}
   </section>

   <section class="panel suite-panel suite-aux-panel" aria-labelledby="suiteAuxTitle">
    <p class="eyebrow">${t('DOVEZI / CONTEXT','EVIDENCE / CONTEXT')}</p><h2 id="suiteAuxTitle">${selected?esc(selected.label[lang]):t('Dovezi, proveniență, incertitudine și limite','Evidence, provenance, uncertainty and limitations')}</h2>
    ${selected?`<div class="suite-aux-context-card"><div><strong>${t('Statut epistemic','Epistemic status')}</strong><div class="suite-diagnostic-statuses">${statusBadges(selected.statuses)}</div></div><div><strong>${t('Proveniență','Provenance')}</strong><p>${esc(selected.provenance[lang])}</p></div><div><strong>${t('Incertitudine','Uncertainty')}</strong><p>${esc(selected.uncertainty[lang])}</p></div><div><strong>${t('Limită','Boundary')}</strong><p>${esc(selected.limitation[lang])}</p></div><div><strong>${t('Surse relevante','Relevant sources')}</strong>${evidenceRefs.length?`<div class="suite-source-links">${evidenceRefs.map(ref=>`<button type="button" data-suite-reference="${esc(ref)}"><code>${esc(ref)}</code></button>`).join('')}</div>`:`<p>${t('Acest nod este o distincție arhitecturală; verifică teoria completă și relațiile înregistrate înainte de orice interpretare empirică.','This node is an architectural distinction; inspect the full theory and registered relations before making an empirical interpretation.')}</p>`}</div></div>`:`<div class="suite-aux-overview"><p>${t('Selectează un mecanism din hartă pentru a vedea aici statutul epistemic, proveniența necesară, sursele relevante, incertitudinea și limitele lui. Instrumentele aprofundate rămân disponibile contextual, fără a concura cu harta principală.','Select a mechanism on the map to see its epistemic status, required provenance, relevant sources, uncertainty and boundaries here. Deep tools remain contextually available without competing with the primary map.')}</p><div class="boundary"><strong>${t('Regulă de interpretare','Interpretation rule')}</strong><p>${t('EMPIRICAL, EXECUTABLE, CONCEPTUAL și INTERPRETIVE sunt niveluri diferite. Un rezultat executabil nu devine automat o estimare populațională sau o explicație cauzală validată.','EMPIRICAL, EXECUTABLE, CONCEPTUAL and INTERPRETIVE are distinct levels. An executable result does not automatically become a population estimate or a validated causal explanation.')}</p></div></div>`}
    <div class="suite-inline-actions"><button type="button" data-suite-view="reference">${t('Registru științific','Scientific registry')}</button><button type="button" data-suite-view="process">${t('Metodologie / Visual ODD','Methodology / Visual ODD')}</button><button type="button" data-suite-view="planning">${t('Implicații și planificare','Implications & planning')}</button><button type="button" data-suite-tool="search">${t('Caută în Semantic Spine','Search Semantic Spine')}</button><button type="button" data-suite-tool="inspector">${t('Inspector contextual','Contextual inspector')}</button></div>
    <div id="suiteAuxContext" class="suite-context-slot suite-aux-context" aria-live="polite"></div>
   </section>
  </div>
 </section>`;
 host.querySelectorAll<HTMLButtonElement>('[data-suite-focus]').forEach(button=>button.onclick=()=>options.openFocus(button.dataset.suiteFocus!));
 host.querySelectorAll<HTMLButtonElement>('[data-suite-diagnostic-focus]').forEach(button=>button.onclick=()=>options.openFocus(button.dataset.suiteDiagnosticFocus!));
 host.querySelectorAll<HTMLButtonElement>('[data-suite-learn]').forEach(button=>button.onclick=()=>options.openUnderstanding(button.dataset.suiteLearn as LearnMode));
 host.querySelectorAll<HTMLButtonElement>('[data-suite-theory-chapter]').forEach(button=>button.onclick=()=>options.openTheoryChapter(button.dataset.suiteTheoryChapter!));
 host.querySelectorAll<HTMLButtonElement>('[data-suite-reference]').forEach(button=>button.onclick=()=>options.openReference(button.dataset.suiteReference!));
 host.querySelectorAll<HTMLButtonElement>('[data-suite-view]').forEach(button=>button.onclick=()=>options.openView(button.dataset.suiteView as ContextView));
 host.querySelectorAll<HTMLButtonElement>('[data-suite-tool]').forEach(button=>button.onclick=()=>options.openTool(button.dataset.suiteTool as AuxTool));
}
