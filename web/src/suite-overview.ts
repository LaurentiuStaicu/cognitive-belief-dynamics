import {cemDiagnostics,cemProductEdges,cemProductNodes,nodeById,type EpistemicLevel,type ProductLang} from './cem-product-map';
import {evidenceForNode,intersections,interventionEvidence,pathwayById,questionPathways,semanticFamilies,theoryTopics} from './product-usefulness';

type Lang=ProductLang;
type ContextView='structure'|'runs'|'comparison'|'planning'|'reference'|'process';
type LearnMode='theory'|'mechanisms'|'world-model'|'tour'|'active';
type AuxTool='search'|'inspector';
type ExplorerMode='overview'|'question';

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

let explorerMode:ExplorerMode='overview';
let activeQuestionId:string|undefined;
let activeInterventionId='accuracy-prompts';

const esc=(value:string)=>value.replace(/[&<>"']/g,char=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]??char));
const statusLabel=(status:EpistemicLevel,lang:Lang)=>({EMPIRICAL:{ro:'EMPIRIC',en:'EMPIRICAL'},EXECUTABLE:{ro:'EXECUTABIL',en:'EXECUTABLE'},CONCEPTUAL:{ro:'CONCEPTUAL',en:'CONCEPTUAL'},INTERPRETIVE:{ro:'INTERPRETATIV',en:'INTERPRETIVE'}}[status][lang]);
const externalLink=(url:string,label:string)=>`<a class="suite-evidence-link" href="${esc(url)}" target="_blank" rel="noreferrer">${esc(label)}</a>`;

export function mountSuiteOverview(host:HTMLElement,options:SuiteOverviewOptions){
 const {lang}=options;
 const t=(ro:string,en:string)=>lang==='ro'?ro:en;
 const selected=options.selectedFocus==='overview'?undefined:nodeById(options.selectedFocus);
 const activePath=explorerMode==='question'?pathwayById(activeQuestionId):undefined;
 const pathNodes=new Set(activePath?.nodes??[]);
 const pathEdges=new Set(activePath?.edgeIds??[]);
 const selectedEdges=selected?cemProductEdges.filter(edge=>edge.source===selected.id||edge.target===selected.id):[];
 const neighborIds=new Set(selectedEdges.flatMap(edge=>[edge.source,edge.target]));
 const nodeName=(id:string)=>nodeById(id)?.label[lang]??id;
 const statusBadges=(statuses:EpistemicLevel[])=>statuses.map(status=>`<span class="epistemic-status" data-status="${status}">${statusLabel(status,lang)}</span>`).join('');

 const nodeClass=(id:string)=>{
  const classes=['cem-system-node'];
  if(selected?.id===id)classes.push('is-selected');
  if(activePath){
   if(pathNodes.has(id))classes.push('is-path');else classes.push('is-dimmed');
  }else if(selected){
   if(neighborIds.has(id))classes.push('is-related');else classes.push('is-dimmed');
  }
  return classes.join(' ');
 };
 const edgeClass=(id:string,source:string,target:string,level:string)=>{
  const classes=['cem-system-edge',level==='CONCEPTUAL'?'is-conceptual':'is-executable'];
  if(activePath){if(pathEdges.has(id))classes.push('is-path');else classes.push('is-dimmed');}
  else if(selected){if(source===selected.id||target===selected.id)classes.push('is-related');else classes.push('is-dimmed');}
  return classes.join(' ');
 };
 const mapEdges=cemProductEdges.map(edge=>{
  const source=nodeById(edge.source)!;const target=nodeById(edge.target)!;
  return `<line class="${edgeClass(edge.id,edge.source,edge.target,edge.level)}" data-suite-edge="${edge.id}" x1="${source.x*10}" y1="${source.y*6.2}" x2="${target.x*10}" y2="${target.y*6.2}" marker-end="url(#cemArrow)"/>`;
 }).join('');
 const mapNodes=cemProductNodes.map(node=>`<button type="button" class="${nodeClass(node.id)}" data-suite-focus="${node.id}" aria-pressed="${selected?.id===node.id}" style="--node-x:${node.x}%;--node-y:${node.y}%" aria-label="${esc(node.label[lang])}: ${esc(node.summary[lang])}"><strong>${esc(node.label[lang])}</strong><small>${esc(node.identifiers.join(' · '))}</small></button>`).join('');

 const questionButtons=questionPathways.map(question=>`<button type="button" class="pathway-question ${activeQuestionId===question.id&&explorerMode==='question'?'is-active':''}" data-pathway-question="${question.id}" aria-pressed="${activeQuestionId===question.id&&explorerMode==='question'}">${esc(question.question[lang])}</button>`).join('');
 const familyChips=semanticFamilies.map(family=>`<span class="mechanism-family ${activePath&&intersections(family.nodes,activePath.nodes)?'is-active':''}" title="${esc(family.modules.join(' · '))}">${esc(family.label[lang])}</span>`).join('');

 const selectedEvidence=selected?evidenceForNode(selected.id):undefined;
 const upstream=selectedEdges.filter(edge=>edge.target===selected?.id).map(edge=>nodeName(edge.source));
 const downstream=selectedEdges.filter(edge=>edge.source===selected?.id).map(edge=>nodeName(edge.target));
 const neighbors=[...new Set(selectedEdges.flatMap(edge=>[edge.source,edge.target]).filter(id=>id!==selected?.id))].map(nodeName);
 const inputs=upstream.length?upstream.join(' · '):t('Nicio intrare explicită în harta de produs','No explicit upstream input in the product map');
 const outputs=downstream.length?downstream.join(' · '):t('Nicio ieșire explicită în harta de produs','No explicit downstream output in the product map');
 const evidenceSources=selectedEvidence?.sources??selected?.evidenceRefs.map(ref=>({label:ref,ref}))??[];
 const sourceMarkup=evidenceSources.length?evidenceSources.map(source=>'url' in source&&source.url?externalLink(source.url,source.label):`<button type="button" class="suite-reference-button" data-suite-reference="${esc('ref' in source&&source.ref?source.ref:source.label)}">${esc(source.label)}</button>`).join(''):`<span class="note">${t('Nu există o sinteză cantitativă legată direct de acest nod în catalogul de produs.','No quantitative synthesis is directly attached to this product node.')}</span>`;

 const mechanismPanel=selected?`<div class="mechanism-inspector">
   <div class="mechanism-title-row"><div><p class="eyebrow">${t('MECANISM SELECTAT','SELECTED MECHANISM')}</p><h2>${esc(selected.label[lang])}</h2></div><div class="suite-diagnostic-statuses">${statusBadges(selected.statuses)}</div></div>
   <p class="mechanism-definition">${esc(selected.summary[lang])}</p>
   <dl class="mechanism-facts">
    <dt>${t('Inputuri','Inputs')}</dt><dd>${esc(inputs)}</dd>
    <dt>${t('Outputuri','Outputs')}</dt><dd>${esc(outputs)}</dd>
    <dt>${t('Vecini','Neighbours')}</dt><dd>${esc(neighbors.join(' · ')||t('Niciunul în harta curentă','None in current map'))}</dd>
    <dt>${t('Upstream','Upstream')}</dt><dd>${esc(upstream.join(' · ')||'—')}</dd>
    <dt>${t('Downstream','Downstream')}</dt><dd>${esc(downstream.join(' · ')||'—')}</dd>
    <dt>${t('Nivel de dovadă','Evidence level')}</dt><dd>${esc(selectedEvidence?.evidenceLevel[lang]??t('Vezi statutul epistemic și registrul de dovezi; nu există o sinteză de efect atașată.','See epistemic status and evidence registry; no effect synthesis is attached.'))}</dd>
    <dt>${t('Tipul dovezii','Evidence type')}</dt><dd>${esc(selectedEvidence?.evidenceType[lang]??t('Registry / mechanism-specific evidence','Registry / mechanism-specific evidence'))}</dd>
    <dt>${t('Dimensiunea efectului','Effect size')}</dt><dd>${esc(selectedEvidence?.effectSize?.[lang]??t('Nu este afișată: literatura auditată nu justifică o sinteză comparabilă direct pentru acest nod.','Not shown: the audited literature does not justify a directly comparable synthesis for this node.'))}</dd>
    <dt>${t('Eterogenitate','Heterogeneity')}</dt><dd>${esc(selectedEvidence?.heterogeneity[lang]??selected.uncertainty[lang])}</dd>
    <dt>${t('Explicații concurente','Competing explanations')}</dt><dd>${esc(selectedEvidence?.competing[lang]??t('Vezi teoria completă; harta nu transformă o asociere într-o singură explicație cauzală.','See the full theory; the map does not turn an association into one causal explanation.'))}</dd>
    <dt>${t('Limitări','Limitations')}</dt><dd>${esc(selectedEvidence?.limitations[lang]??selected.limitation[lang])}</dd>
   </dl>
   <div class="mechanism-sources"><strong>${t('Surse','Sources')}</strong><div>${sourceMarkup}</div></div>
   <details class="technical-identifiers"><summary>${t('Detalii tehnice secundare','Secondary technical details')}</summary><p><strong>${t('Identificatori','Identifiers')}:</strong> <code>${esc(selected.identifiers.join(' · '))}</code></p><p><strong>${t('Proveniență necesară','Required provenance')}:</strong> ${esc(selected.provenance[lang])}</p></details>
   <button type="button" class="primary" data-suite-theory-chapter="${esc(selected.chapterSlug)}">${t('Deschide teoria completă a acestui mecanism','Open the full theory for this mechanism')}</button>
  </div>`:`<div class="mechanism-inspector empty-mechanism"><p class="eyebrow">THEORY / LEARN</p><h2>${t('De la mecanism la teorie și surse','From mechanism to theory and sources')}</h2><p>${t('Selectează orice mecanism din hartă. Panoul va arăta definiția, intrările, ieșirile, vecinii, traseul upstream/downstream, statutul epistemic, dovezile, efectul numai când este comparabil, heterogenitatea, explicațiile concurente, limitele și sursele.','Select any mechanism in the map. This panel will show definition, inputs, outputs, neighbours, upstream/downstream path, epistemic status, evidence, effect only when comparable, heterogeneity, competing explanations, limitations and sources.')}</p><p class="boundary">${t('CEM nu atribuie vulnerabilitate sau probabilitate comportamentală unei persoane fără date și validare dedicate.','CEM does not assign an individual vulnerability or behavioral probability without dedicated data and validation.')}</p></div>`;

 const pathEvidenceNodes=(activePath?.nodes??cemProductNodes.map(node=>node.id)).map(id=>evidenceForNode(id)).filter(Boolean);
 const empiricalCount=(activePath?.nodes??cemProductNodes.map(node=>node.id)).map(id=>nodeById(id)).filter(node=>node?.statuses.includes('EMPIRICAL')).length;
 const conceptualCount=(activePath?.nodes??cemProductNodes.map(node=>node.id)).map(id=>nodeById(id)).filter(node=>node?.statuses.includes('CONCEPTUAL')&&!node?.statuses.includes('EMPIRICAL')).length;
 const effectCount=pathEvidenceNodes.filter(item=>item?.effectSize).length;
 const relevantDiagnostics=activePath?cemDiagnostics.filter(diag=>intersections(diag.mechanisms,activePath.nodes)):cemDiagnostics.slice(0,4);
 const dashboardDiagnostics=relevantDiagnostics.slice(0,3).map(diag=>`<article class="vulnerability-card"><div class="suite-diagnostic-statuses">${statusBadges(diag.statuses)}</div><h3>${esc(diag.title[lang])}</h3><p>${esc(diag.why[lang])}</p><p class="note"><strong>${t('Dovezi','Evidence')}:</strong> ${esc(diag.evidence[lang])}</p><p class="note"><strong>${t('Incertitudine','Uncertainty')}:</strong> ${esc(diag.uncertainty[lang])}</p><button type="button" data-suite-diagnostic-focus="${esc(diag.focus)}">${t('Vezi mecanismul','Inspect mechanism')}</button></article>`).join('');
 const pathwaySummary=activePath?`<div class="pathway-summary"><p class="eyebrow">${t('ÎNTREBARE ACTIVĂ','ACTIVE QUESTION')}</p><h3>${esc(activePath.question[lang])}</h3><p>${esc(activePath.why[lang])}</p><p class="boundary"><strong>${t('Limită','Boundary')}:</strong> ${esc(activePath.boundary[lang])}</p></div>`:`<div class="pathway-summary"><p class="eyebrow">SYSTEM OVERVIEW</p><h3>${t('Unde sunt mecanismele mai solide și unde sunt limitele?','Where are mechanisms stronger, and where are the boundaries?')}</h3><p>${t('Dashboard-ul descrie structura dovezilor și punctele de incertitudine ale modelului, nu un scor al utilizatorului. Alege o întrebare pentru a restrânge diagnosticul la pathway-ul relevant.','The dashboard describes the model evidence structure and uncertainty points, not a user score. Choose a question to narrow the diagnostics to the relevant pathway.')}</p></div>`;

 const relevantInterventions=activePath?interventionEvidence.filter(item=>intersections(item.targetNodes,activePath.nodes)):selected?interventionEvidence.filter(item=>item.targetNodes.includes(selected.id)):interventionEvidence;
 if(!relevantInterventions.some(item=>item.id===activeInterventionId))activeInterventionId=relevantInterventions[0]?.id??interventionEvidence[0].id;
 const activeIntervention=interventionEvidence.find(item=>item.id===activeInterventionId)??interventionEvidence[0];
 const interventionOptions=relevantInterventions.map(item=>`<option value="${item.id}" ${item.id===activeIntervention.id?'selected':''}>${esc(item.label[lang])}</option>`).join('');
 const interventionSources=activeIntervention.sources.map(source=>externalLink(source.url,source.label)).join('');

 const corpusTopics=theoryTopics.map(topic=>`<button type="button" class="corpus-topic" data-suite-theory-chapter="${esc(topic.chapterSlug)}"><strong>${esc(topic.label[lang])}</strong><small>${esc(topic.scope[lang])}</small><span>${esc(topic.modules.join(' · '))}</span></button>`).join('');

 host.innerHTML=`<section class="suite-overview infoclar-primary-shell" data-suite-standard="InfoClar Model Suite Design Standard v1.1" aria-label="${t('Cognitive Epistemic Model — explorer de mecanisme','Cognitive Epistemic Model — mechanism explorer')}">
  <div class="usefulness-orientation" role="note"><strong>${t('Ce încearcă să explice CEM?','What does CEM try to explain?')}</strong><span>${t('Cum informația disponibilă poate trece prin selecție, sursă, framing, atenție, familiaritate, memorie, priors, context social și incertitudine pentru a contribui la reprezentare, convingere, judecată și acțiune — și ce dovezi susțin fiecare legătură.','How available information can pass through selection, source, framing, attention, familiarity, memory, priors, social context and uncertainty to contribute to representation, belief, judgment and action — and what evidence supports each link.')}</span></div>
  <div class="suite-grid">
   <section class="panel suite-panel suite-model-panel" aria-labelledby="suiteModelTitle">
    <div class="suite-panel-heading"><div><p class="eyebrow">MECHANISM EXPLORER</p><h1 id="suiteModelTitle">${t('Cum poate informația deveni percepție, memorie, convingere, judecată și acțiune','How information can become perception, memory, belief, judgment and action')}</h1></div></div>
    <div class="explorer-mode-tabs" role="group" aria-label="${t('Mod de explorare','Explorer mode')}"><button type="button" data-explorer-mode="overview" aria-pressed="${explorerMode==='overview'}">SYSTEM OVERVIEW</button><button type="button" data-explorer-mode="question" aria-pressed="${explorerMode==='question'}">QUESTION / PATHWAY EXPLORER</button></div>
    ${explorerMode==='question'?`<div class="question-library" aria-label="${t('Bibliotecă de întrebări','Question library')}">${questionButtons}</div>`:''}
    <div class="mechanism-families" aria-label="${t('Familii semantice','Semantic families')}">${familyChips}</div>
    <div class="cem-system-map" aria-label="${t('Hartă explorabilă a mecanismelor CEM','Explorable CEM mechanism map')}">
     <div class="cem-map-stage-label stage-information">${t('INFORMAȚIE & ACCES','INFORMATION & ACCESS')}</div><div class="cem-map-stage-label stage-representation">${t('REPREZENTARE & MEMORIE','REPRESENTATION & MEMORY')}</div><div class="cem-map-stage-label stage-integration">${t('INTEGRARE & INCERTITUDINE','INTEGRATION & UNCERTAINTY')}</div><div class="cem-map-stage-label stage-judgment">${t('JUDECATĂ & ACȚIUNE','JUDGMENT & ACTION')}</div>
     <svg class="cem-system-links" viewBox="0 0 1000 620" aria-hidden="true" preserveAspectRatio="none"><defs><marker id="cemArrow" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 z"/></marker></defs>${mapEdges}</svg>${mapNodes}
    </div>
    ${activePath?`<div class="active-path-readout"><strong>${esc(activePath.question[lang])}</strong><span>${activePath.nodes.map(nodeName).map(esc).join(' → ')}</span><small>${esc(activePath.boundary[lang])}</small></div>`:`<div class="cem-map-guide"><strong>${t('Cum citești harta','How to read the map')}</strong><p>${t('Nodurile sunt mecanisme sau stări reale deja reprezentate în produs; liniile continue indică trasee executabile de referință, iar liniile întrerupte bridge-uri conceptuale. Nu sunt adăugate relații pentru densitate vizuală.','Nodes are real mechanisms or states already represented in the product; solid lines are executable reference paths and dashed lines are conceptual bridges. No relations are added for visual density.')}</p></div>`}
   </section>

   <section class="panel suite-panel suite-theory-panel" aria-labelledby="suiteTheoryTitle">
    ${mechanismPanel}
    <details class="corpus-navigator"><summary>${t('Corpus complet CEM — navigare progresivă EN/RO','Complete CEM corpus — progressive EN/RO navigation')}</summary><div class="corpus-topic-grid">${corpusTopics}</div><div class="suite-learning-actions"><button type="button" data-suite-learn="theory">${t('Deschide reader-ul complet','Open full reader')}</button><button type="button" data-suite-learn="mechanisms">${t('Mecanisme detaliate','Detailed mechanisms')}</button><button type="button" data-suite-learn="world-model">MOD.14</button><button type="button" data-suite-learn="tour">${t('Tur ghidat','Guided tour')}</button><button type="button" data-suite-learn="active">${t('Înțelegere activă','Active understanding')}</button></div></details>
    <div id="suiteTheoryContext" class="suite-context-slot suite-theory-context" aria-live="polite"></div>
   </section>

   <section class="panel suite-panel suite-dashboard-panel" aria-labelledby="suiteDashboardTitle">
    <p class="eyebrow">EPISTEMIC MECHANISMS & VULNERABILITIES</p><h2 id="suiteDashboardTitle">${activePath?esc(activePath.question[lang]):t('Structura dovezilor și punctele de vulnerabilitate ale mecanismelor','Evidence structure and mechanism vulnerability points')}</h2>
    ${pathwaySummary}
    <div class="evidence-metrics"><div><strong>${empiricalCount}</strong><span>${t('noduri din selecție cu suport EMPIRICAL declarat','selected nodes with declared EMPIRICAL support')}</span></div><div><strong>${conceptualCount}</strong><span>${t('noduri conceptuale fără suport EMPIRICAL declarat','conceptual nodes without declared EMPIRICAL support')}</span></div><div><strong>${effectCount}</strong><span>${t('sinteze cu efect comparabil afișabil','comparable effect syntheses displayable')}</span></div></div>
    <div class="suite-diagnostics">${dashboardDiagnostics||`<article class="vulnerability-card"><h3>${t('Modelul nu poate face aici o afirmație mai puternică','The model cannot make a stronger claim here')}</h3><p>${t('Pathway-ul selectat nu are un diagnostic validat suplimentar în registry. Absența unui card nu este dovadă de absență a mecanismului.','The selected pathway has no additional validated diagnostic in the registry. Absence of a card is not evidence that the mechanism is absent.')}</p></article>`}</div>
    <div class="boundary no-personal-score"><strong>${t('Ce NU este acest dashboard','What this dashboard is NOT')}</strong><p>${t('Nu este un profil al utilizatorului, un scor de vulnerabilitate, o probabilitate personală de a crede misinformation sau o predicție de comportament individual.','It is not a user profile, vulnerability score, personal probability of believing misinformation, or individual behavioral prediction.')}</p></div>
   </section>

   <section class="panel suite-panel suite-aux-panel" aria-labelledby="suiteAuxTitle">
    <p class="eyebrow">INTERVENTION EVIDENCE EXPLORER</p><h2 id="suiteAuxTitle">${t('Intervenții studiate empiric și mecanismele vizate','Empirically studied interventions and their target mechanisms')}</h2>
    <p class="suite-panel-intro">${t('Acest panou organizează literatura; nu înseamnă „CEM recomandă automat această acțiune”. Contextul, populația, outcome-ul și heterogenitatea rămân parte din rezultat.','This panel organizes the literature; it does not mean “CEM automatically recommends this action”. Context, population, outcome and heterogeneity remain part of the result.')}</p>
    <label class="intervention-picker"><span>${t('Intervenție','Intervention')}</span><select id="interventionEvidenceSelect">${interventionOptions}</select></label>
    <article class="intervention-card">
     <div class="intervention-heading"><h3>${esc(activeIntervention.label[lang])}</h3><span>${esc(activeIntervention.targetNodes.map(nodeName).join(' · '))}</span></div>
     <dl class="mechanism-facts intervention-facts">
      <dt>${t('Mecanism vizat','Target mechanism')}</dt><dd>${esc(activeIntervention.targetMechanism[lang])}</dd>
      <dt>${t('Populație / context','Population / context')}</dt><dd>${esc(activeIntervention.population[lang])}</dd>
      <dt>Outcome</dt><dd>${esc(activeIntervention.outcome[lang])}</dd>
      <dt>${t('Efect','Effect estimate')}</dt><dd>${esc(activeIntervention.effect[lang])}</dd>
      <dt>${t('Incertitudine','Uncertainty')}</dt><dd>${esc(activeIntervention.uncertainty[lang])}</dd>
      <dt>${t('Eterogenitate','Heterogeneity')}</dt><dd>${esc(activeIntervention.heterogeneity[lang])}</dd>
      <dt>${t('Durată','Duration')}</dt><dd>${esc(activeIntervention.duration[lang])}</dd>
      <dt>${t('Condiții / moderatori','Conditions / moderators')}</dt><dd>${esc(activeIntervention.moderators[lang])}</dd>
      <dt>${t('Posibile efecte adverse','Possible adverse effects')}</dt><dd>${esc(activeIntervention.adverse[lang])}</dd>
      <dt>${t('Cât de direct susține CEM','Directness to CEM')}</dt><dd>${esc(activeIntervention.directness[lang])}</dd>
     </dl>
     <div class="mechanism-sources"><strong>${t('Surse auditate','Audited sources')}</strong><div>${interventionSources}</div></div>
    </article>
    <details class="infrastructure-tools"><summary>${t('Infrastructură și instrumente avansate păstrate contextual','Infrastructure and advanced tools kept contextual')}</summary><div class="suite-inline-actions"><button type="button" data-suite-view="reference">${t('Registru științific','Scientific registry')}</button><button type="button" data-suite-view="process">${t('Metodologie / Visual ODD','Methodology / Visual ODD')}</button><button type="button" data-suite-view="structure">${t('Dependențe tehnice','Technical dependencies')}</button><button type="button" data-suite-view="runs">${t('Rulări de referință','Reference runs')}</button><button type="button" data-suite-view="comparison">${t('Comparație','Comparison')}</button><button type="button" data-suite-view="planning">${t('Planificare','Planning')}</button><button type="button" data-suite-tool="search">${t('Semantic Spine Search','Semantic Spine Search')}</button><button type="button" data-suite-tool="inspector">${t('Inspector contextual','Contextual inspector')}</button></div></details>
    <div id="suiteAuxContext" class="suite-context-slot suite-aux-context" aria-live="polite"></div>
   </section>
  </div>
 </section>`;

 host.querySelectorAll<HTMLButtonElement>('[data-explorer-mode]').forEach(button=>button.onclick=()=>{explorerMode=button.dataset.explorerMode as ExplorerMode;if(explorerMode==='question'&&!activeQuestionId)activeQuestionId=questionPathways[0].id;mountSuiteOverview(host,options);});
 host.querySelectorAll<HTMLButtonElement>('[data-pathway-question]').forEach(button=>button.onclick=()=>{explorerMode='question';activeQuestionId=button.dataset.pathwayQuestion;mountSuiteOverview(host,options);});
 host.querySelectorAll<HTMLButtonElement>('[data-suite-focus]').forEach(button=>button.onclick=()=>options.openFocus(button.dataset.suiteFocus!));
 host.querySelectorAll<HTMLButtonElement>('[data-suite-diagnostic-focus]').forEach(button=>button.onclick=()=>options.openFocus(button.dataset.suiteDiagnosticFocus!));
 host.querySelectorAll<HTMLButtonElement>('[data-suite-learn]').forEach(button=>button.onclick=()=>options.openUnderstanding(button.dataset.suiteLearn as LearnMode));
 host.querySelectorAll<HTMLButtonElement>('[data-suite-theory-chapter]').forEach(button=>button.onclick=()=>options.openTheoryChapter(button.dataset.suiteTheoryChapter!));
 host.querySelectorAll<HTMLButtonElement>('[data-suite-reference]').forEach(button=>button.onclick=()=>options.openReference(button.dataset.suiteReference!));
 host.querySelectorAll<HTMLButtonElement>('[data-suite-view]').forEach(button=>button.onclick=()=>options.openView(button.dataset.suiteView as ContextView));
 host.querySelectorAll<HTMLButtonElement>('[data-suite-tool]').forEach(button=>button.onclick=()=>options.openTool(button.dataset.suiteTool as AuxTool));
 const interventionSelect=host.querySelector<HTMLSelectElement>('#interventionEvidenceSelect');
 if(interventionSelect)interventionSelect.onchange=()=>{activeInterventionId=interventionSelect.value;mountSuiteOverview(host,options);};
}
