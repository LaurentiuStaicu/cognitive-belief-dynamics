import {cemProductEdges,cemProductNodes,nodeById,type EpistemicLevel,type ProductLang} from './cem-product-map';
import {atlasGroups,edgeEvidenceFor,evidenceForNode,intersections,interventionEvidence,pathwayById,questionPathways,theoryTopics} from './product-usefulness';

type Lang=ProductLang;
type ContextView='structure'|'runs'|'comparison'|'planning'|'reference'|'process';
type LearnMode='theory'|'mechanisms'|'world-model'|'tour'|'active';
type AuxTool='search'|'inspector';
type ProductView='home'|'pathway'|'interventions'|'atlas'|'theory'|'technical';

type SuiteOverviewOptions={lang:Lang;selectedFocus:string;openFocus:(id:string)=>void;openUnderstanding:(mode:LearnMode)=>void;openTheoryChapter:(slug:string)=>void;openReference:(id:string)=>void;openView:(view:ContextView)=>void;openTool:(tool:AuxTool)=>void;};

let productView:ProductView='home';
let activeQuestionId:string|undefined;
let activeInterventionId='accuracy-prompts';
let atlasFilter='major';
let atlasZoom=1;

const esc=(value:string)=>value.replace(/[&<>"']/g,char=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]??char));
const clean=(value:string)=>value
 .replace(/\bPwm\b/g,'normative proposition probability')
 .replace(/\bUwm\b/g,'explicit uncertainty')
 .replace(/\bPprior\b/g,'prior probability')
 .replace(/\bLR\b/g,'likelihood ratio')
 .replace(/\bAissue\b/g,'issue appraisal')
 .replace(/\bSobs\b/g,'observed information balance')
 .replace(/\bNexp\b/g,'exposure count')
 .replace(/\bPengage\b/g,'engagement probability')
 .replace(/\bEngageIntent\b/g,'engagement intention')
 .replace(/\bPaccess\b/g,'access probability')
 .replace(/\bPreviewImpression\b/g,'preview impression')
 .replace(/\bHneg\b/g,'headline-negativity condition')
 .replace(/\bEedit\b/g,'editorial selection policy')
 .replace(/\bVcontent\b/g,'content valence')
 .replace(/\bFpres\b/g,'presentation frame')
 .replace(/\bGatt\b/g,'prior-attitude congruence')
 .replace(/\bShare\b/g,'sharing outcome')
 .replace(/\bDecisionEvent\b/g,'decision event')
 .replace(/\bF\b/g,'familiarity state')
 .replace(/\bB\b/g,'belief state')
 .replace(/\bW\b/g,'accuracy weighting')
 .replace(/\bC\b/g,'corrective accessibility')
 .replace(/\bT\b/g,'estimated source reliability')
 .replace(/\bProv\b/g,'provenance')
 .replace(/\bMOD\.\d+\b/g,'the relevant CEM module')
 .replace(/\b(?:REF|VAR|LINK|ODD)\.[A-Z0-9._-]+\b/gi,'technical record');
const externalLink=(url:string,label:string)=>`<a class="evidence-source" href="${esc(url)}" target="_blank" rel="noreferrer">${esc(label)} ↗</a>`;
const nodeName=(id:string,lang:Lang)=>clean(nodeById(id)?.label[lang]??id);
const naturalStatus=(status:EpistemicLevel,lang:Lang)=>({EMPIRICAL:{en:'Empirical',ro:'Empiric'},EXECUTABLE:{en:'Executable in the reference model',ro:'Executabil în modelul de referință'},CONCEPTUAL:{en:'Conceptual',ro:'Conceptual'},INTERPRETIVE:{en:'Interpretive',ro:'Interpretativ'}}[status][lang]);

export function mountSuiteOverview(host:HTMLElement,options:SuiteOverviewOptions){
 const {lang}=options;
 const t=(ro:string,en:string)=>lang==='ro'?ro:en;
 const selected=options.selectedFocus==='overview'?undefined:nodeById(options.selectedFocus);
 const activePath=pathwayById(activeQuestionId);
 const selectedEdges=selected?cemProductEdges.filter(edge=>edge.source===selected.id||edge.target===selected.id):[];
 const upstream=selectedEdges.filter(edge=>edge.target===selected?.id).map(edge=>nodeName(edge.source,lang));
 const downstream=selectedEdges.filter(edge=>edge.source===selected?.id).map(edge=>nodeName(edge.target,lang));
 const evidence=selected?evidenceForNode(selected.id):undefined;
 const relevantInterventions=activePath?interventionEvidence.filter(item=>intersections(item.targetNodes,[...new Set(activePath.nodes)])):interventionEvidence;
 if(!relevantInterventions.some(item=>item.id===activeInterventionId))activeInterventionId=relevantInterventions[0]?.id??interventionEvidence[0].id;
 const intervention=interventionEvidence.find(item=>item.id===activeInterventionId)??interventionEvidence[0];

 const nav=(view:ProductView,label:string)=>`<button type="button" class="product-nav-button" data-product-view="${view}" aria-current="${productView===view?'page':'false'}">${label}</button>`;
 const chrome=`<div class="product-shell-header"><div><p class="eyebrow">COGNITIVE EPISTEMIC MODEL</p><h1>${t('Cum poate informația influența ceea ce percepem, reținem, credem, judecăm și facem?','How can information influence what we perceive, remember, believe, judge and do?')}</h1><p>${t('Explorează mecanismele, dovezile și intervențiile studiate. CEM explică relații și limite; nu prezice comportamentul unei persoane.','Explore mechanisms, evidence and studied interventions. CEM explains relations and limits; it does not predict an individual person’s behavior.')}</p></div><nav class="product-nav" aria-label="${t('Navigare produs','Product navigation')}">${nav('home',t('Întrebări','Questions'))}${nav('pathway',t('Pathway','Pathway'))}${nav('interventions',t('Intervenții','Interventions'))}${nav('atlas',t('Atlas complet','Full Model Atlas'))}${nav('theory',t('Theory / Learn','Theory / Learn'))}${nav('technical',t('Research / Proveniență','Research / Provenance'))}</nav></div>`;

 const home=()=>`<main class="questions-home" data-product-surface="home"><section class="home-intro"><p class="eyebrow">${t('ÎNCEPE CU UN FENOMEN','START WITH A PHENOMENON')}</p><h2>${t('Alege o întrebare umană, nu o variabilă a modelului','Choose a human question, not a model variable')}</h2><p>${t('Fiecare întrebare de mai jos este legată de mecanisme și relații deja existente în CEM și de literatura atașată acestora.','Each question below is tied to mechanisms and relations already present in CEM and to the literature attached to them.')}</p></section><div class="question-card-grid">${questionPathways.map(question=>`<button type="button" class="question-card" data-pathway-question="${question.id}"><span class="question-arrow" aria-hidden="true">→</span><strong>${esc(question.question[lang])}</strong><small>${esc(question.why[lang])}</small></button>`).join('')}</div><aside class="home-boundary"><strong>${t('Ce nu face această pagină','What this page does not do')}</strong><span>${t('Nu începe cu harta completă, nu afișează coduri interne și nu atribuie unui utilizator un scor de vulnerabilitate.','It does not start with the full model map, show internal codes, or assign the user a vulnerability score.')}</span></aside></main>`;

 const pathwayFlow=()=>{
  if(!activePath)return `<section class="empty-pathway"><h2>${t('Alege mai întâi o întrebare','Choose a question first')}</h2><p>${t('Pathway Explorer afișează numai mecanismele necesare pentru fenomenul selectat.','Pathway Explorer shows only the mechanisms needed for the selected phenomenon.')}</p><button type="button" class="primary" data-product-view="home">${t('Vezi întrebările','See questions')}</button></section>`;
  const pieces:string[]=[];
  activePath.nodes.forEach((nodeId,index)=>{
   const node=nodeById(nodeId);if(!node)return;
   pieces.push(`<button type="button" class="pathway-step ${selected?.id===nodeId?'is-selected':''}" data-suite-focus="${nodeId}" aria-label="${esc(clean(node.label[lang]))}"><span class="step-number">${index+1}</span><strong>${esc(clean(node.label[lang]))}</strong><small>${esc(clean(node.summary[lang]))}</small></button>`);
   const edgeId=activePath.edgeIds[index];
   if(edgeId){const relation=edgeEvidenceFor(edgeId);pieces.push(`<div class="pathway-connector" data-edge-status="${relation?.status??'CONCEPTUAL_HYPOTHESIS'}"><span class="connector-line" aria-hidden="true">→</span><span class="edge-status-badge">${esc(relation?.label[lang]??t('Relație înregistrată','Registered relation'))}</span><small>${esc(clean(relation?.explanation[lang]??t('Relație existentă în model.','Existing model relation.')))}</small></div>`);}
  });
  const secondary=activePath.secondary.map(branch=>`<details class="secondary-branch"><summary>+ ${esc(branch.label[lang])}</summary><p>${esc(branch.note[lang])}</p><div class="secondary-node-row">${branch.nodes.map(id=>`<button type="button" data-suite-focus="${id}">${esc(nodeName(id,lang))}</button>`).join('')}</div></details>`).join('');
  return `<section class="pathway-workspace" data-product-surface="pathway"><div class="pathway-title-row"><div><p class="eyebrow">PATHWAY EXPLORER</p><h2>${esc(activePath.question[lang])}</h2><p>${esc(activePath.why[lang])}</p></div><button type="button" data-product-view="home">${t('Schimbă întrebarea','Change question')}</button></div><div class="relation-legend" aria-label="${t('Statutul legăturilor','Relation status legend')}">${['EMPIRICAL_CAUSAL_SUPPORT','EMPIRICAL_ASSOCIATION','EXECUTABLE_MODEL_RELATION','CONCEPTUAL_HYPOTHESIS','INTERPRETIVE_LINK','NORMATIVE_OPERATOR'].map(status=>`<span data-edge-status="${status}">${({EMPIRICAL_CAUSAL_SUPPORT:t('Suport cauzal empiric','Empirical causal support'),EMPIRICAL_ASSOCIATION:t('Asociere empirică','Empirical association'),EXECUTABLE_MODEL_RELATION:t('Relație executabilă','Executable model relation'),CONCEPTUAL_HYPOTHESIS:t('Ipoteză conceptuală','Conceptual hypothesis'),INTERPRETIVE_LINK:t('Legătură interpretativă','Interpretive link'),NORMATIVE_OPERATOR:t('Operator normativ','Normative operator')} as Record<string,string>)[status]}</span>`).join('')}</div><div class="pathway-scroll"><div class="pathway-flow">${pieces.join('')}</div></div><div class="secondary-branches"><h3>${t('Ramuri secundare','Secondary branches')}</h3>${secondary}</div><p class="pathway-boundary"><strong>${t('Limită a interpretării','Interpretation boundary')}:</strong> ${esc(activePath.boundary[lang])}</p>${pathwayDashboard()}</section>`;
 };

 const pathwayDashboard=()=>{
  if(!activePath)return '';
  const uniqueNodes=[...new Set(activePath.nodes)];
  const evidenceItems=uniqueNodes.map(id=>evidenceForNode(id)).filter(Boolean);
  const strongest=evidenceItems[0];
  const moderatorText=evidenceItems.map(item=>item?.moderators[lang]).filter(Boolean).slice(0,2).join(' ');
  const competing=evidenceItems.map(item=>item?.competing[lang]).filter(Boolean).slice(0,2).join(' ');
  const uncertainty=evidenceItems.map(item=>item?.uncertainty[lang]).filter(Boolean).slice(0,2).join(' ');
  const studied=relevantInterventions.slice(0,4).map(item=>item.label[lang]).join(' · ');
  return `<section class="pathway-dashboard" aria-labelledby="dashboardTitle"><h3 id="dashboardTitle">${t('Ce știm despre acest pathway','What we know about this pathway')}</h3><div class="pathway-dashboard-grid"><article><span>${t('CELE MAI PUTERNICE DOVEZI','STRONGEST EVIDENCE')}</span><p>${esc(strongest?.strength[lang]??t('Nu există o sinteză cantitativă comparabilă pentru acest pathway.','No comparable quantitative synthesis is attached to this pathway.'))}</p></article><article><span>${t('INCERTITUDINI PRINCIPALE','MAIN UNCERTAINTIES')}</span><p>${esc(uncertainty||activePath.boundary[lang])}</p></article><article><span>${t('MODERATORI IMPORTANȚI','IMPORTANT MODERATORS')}</span><p>${esc(moderatorText||t('Dependența de sarcină, populație și context rămâne importantă.','Task, population and context dependence remain important.'))}</p></article><article><span>${t('EXPLICAȚII CONCURENTE','COMPETING EXPLANATIONS')}</span><p>${esc(competing||t('Pathway-ul nu exclude mecanisme alternative neidentificate de datele curente.','The pathway does not exclude alternative mechanisms not identified by current data.'))}</p></article><article><span>${t('INTERVENȚII STUDIATE','INTERVENTIONS STUDIED')}</span><p>${esc(studied||t('Nicio clasă de intervenție nu este legată direct de toate etapele acestui pathway.','No intervention class is directly linked to all stages of this pathway.'))}</p><button type="button" data-product-view="interventions">${t('Deschide Intervention Explorer','Open Intervention Explorer')}</button></article><article><span>${t('CE NU POATE AFIRMA CEM','WHAT CEM CANNOT CLAIM')}</span><p>${esc(activePath.boundary[lang])}</p></article></div></section>`;
 };

 const evidenceCard=()=>{
  if(!selected)return '';
  if(!evidence)return `<article class="evidence-card"><h3>${t('Dovezi pentru acest mecanism','Evidence for this mechanism')}</h3><p>${t('CEM înregistrează acest mecanism, dar nu atașează aici o sinteză cantitativă comparabilă. Deschide capitolul Theory pentru argumentare, surse și limitări.','CEM registers this mechanism, but no comparable quantitative synthesis is attached here. Open the Theory chapter for rationale, sources and limitations.')}</p></article>`;
  return `<article class="evidence-card"><div class="evidence-card-heading"><div><p class="eyebrow">EVIDENCE CARD</p><h3>${esc(evidence.strength[lang])}</h3></div></div><dl><dt>${t('Tipul studiilor','Study type')}</dt><dd>${esc(evidence.studyType[lang])}</dd><dt>${t('Număr de studii','Number of studies')}</dt><dd>${esc(evidence.studies[lang])}</dd><dt>${t('Populații / contexte','Populations / settings')}</dt><dd>${esc(evidence.populations[lang])}</dd>${evidence.effectSize?`<dt>${t('Estimare a efectului','Effect estimate')}</dt><dd class="effect-estimate">${esc(evidence.effectSize[lang])}</dd>`:''}<dt>${t('Incertitudine','Uncertainty')}</dt><dd>${esc(evidence.uncertainty[lang])}</dd><dt>${t('Eterogenitate','Heterogeneity')}</dt><dd>${esc(evidence.heterogeneity[lang])}</dd><dt>${t('Moderatori','Moderators')}</dt><dd>${esc(evidence.moderators[lang])}</dd><dt>${t('Calitate / risk of bias','Quality / risk of bias')}</dt><dd>${esc(evidence.quality[lang])}</dd><dt>${t('Replicare','Replication')}</dt><dd>${esc(evidence.replication[lang])}</dd></dl><div class="evidence-sources">${evidence.sources.map(source=>externalLink(source.url,source.label)).join('')}</div></article>`;
 };

 const mechanismDrawer=()=>selected?`<aside class="context-drawer" aria-label="${t('Detalii mecanism','Mechanism details')}"><div class="drawer-heading"><div><p class="eyebrow">${t('MECANISM SELECTAT','SELECTED MECHANISM')}</p><h2>${esc(clean(selected.label[lang]))}</h2></div><button type="button" class="drawer-close" data-close-mechanism aria-label="${t('Închide','Close')}">×</button></div><div class="mechanism-levels">${selected.statuses.map(status=>`<span>${esc(naturalStatus(status,lang))}</span>`).join('')}</div><section><h3>${t('CE ESTE?','WHAT IS IT?')}</h3><p>${esc(clean(selected.summary[lang]))}</p></section><section><h3>${t('CE ÎL INFLUENȚEAZĂ?','WHAT INFLUENCES IT?')}</h3><p>${esc(upstream.join(' · ')||t('Nu există o intrare directă în harta actuală.','No direct upstream relation is registered in the current product map.'))}</p></section><section><h3>${t('CE INFLUENȚEAZĂ?','WHAT DOES IT INFLUENCE?')}</h3><p>${esc(downstream.join(' · ')||t('Nu există o ieșire directă în harta actuală.','No direct downstream relation is registered in the current product map.'))}</p></section><section><h3>${t('CE DOVEZI ÎL SUSȚIN?','WHAT EVIDENCE SUPPORTS IT?')}</h3>${evidenceCard()}</section>${evidence?.effectSize?`<section><h3>${t('CÂT DE MARE ESTE EFECTUL?','HOW LARGE IS THE EFFECT?')}</h3><p class="effect-callout">${esc(evidence.effectSize[lang])}</p></section>`:''}<section><h3>${t('ÎN CE CONDIȚII?','UNDER WHAT CONDITIONS?')}</h3><p>${esc(evidence?.moderators[lang]??clean(selected.uncertainty[lang]))}</p></section><section><h3>${t('CE EXPLICAȚII CONCURENTE EXISTĂ?','WHAT COMPETING EXPLANATIONS EXIST?')}</h3><p>${esc(evidence?.competing[lang]??t('Modelul nu identifică o singură explicație cauzală pentru această relație. Vezi Theory pentru alternativele relevante.','The model does not identify a single causal explanation for this relation. See Theory for relevant alternatives.'))}</p></section><section><h3>${t('CARE SUNT LIMITĂRILE?','WHAT ARE THE LIMITATIONS?')}</h3><p>${esc(evidence?.limitations[lang]??clean(selected.limitation[lang]))}</p></section><div class="drawer-actions"><button type="button" class="primary" data-suite-theory-chapter="${esc(selected.chapterSlug)}">${t('Deschide teoria completă','Open full theory')}</button><button type="button" data-product-view="technical">${t('Proveniență tehnică','Technical provenance')}</button></div></aside>`:'';

 const interventionsView=()=>`<main class="interventions-view" data-product-surface="interventions"><div class="section-heading"><div><p class="eyebrow">INTERVENTION EVIDENCE EXPLORER</p><h2>${t('Intervenții investigate empiric','Empirically studied interventions')}</h2><p>${t('Aceste carduri descriu ce a fost testat și cu ce rezultate. Nu reprezintă recomandări automate ale CEM.','These cards describe what has been tested and with what outcomes. They are not automatic CEM recommendations.')}</p></div></div><label class="intervention-select"><span>${t('Clasa de intervenție','Intervention class')}</span><select id="interventionEvidenceSelect">${interventionEvidence.map(item=>`<option value="${item.id}" ${item.id===intervention.id?'selected':''}>${esc(item.label[lang])}</option>`).join('')}</select></label><article class="intervention-detail"><h3>${esc(intervention.label[lang])}</h3><dl><dt>${t('Mecanism vizat','Target mechanism')}</dt><dd>${esc(intervention.targetMechanism[lang])}</dd><dt>${t('Tipul studiilor','Study type')}</dt><dd>${esc(intervention.studyType[lang])}</dd><dt>${t('Populație / context','Population / context')}</dt><dd>${esc(intervention.population[lang])}</dd><dt>Outcome</dt><dd>${esc(intervention.outcome[lang])}</dd><dt>${t('Estimare a efectului','Effect estimate')}</dt><dd>${esc(intervention.effect[lang])}</dd><dt>${t('Incertitudine','Uncertainty')}</dt><dd>${esc(intervention.uncertainty[lang])}</dd><dt>${t('Eterogenitate','Heterogeneity')}</dt><dd>${esc(intervention.heterogeneity[lang])}</dd><dt>${t('Durata efectului','Durability')}</dt><dd>${esc(intervention.duration[lang])}</dd><dt>${t('Moderatori','Moderators')}</dt><dd>${esc(intervention.moderators[lang])}</dd><dt>${t('Posibile efecte adverse / trade-offs','Possible harms / trade-offs')}</dt><dd>${esc(intervention.adverse[lang])}</dd><dt>${t('Cât de direct susține CEM','Directness to CEM')}</dt><dd>${esc(intervention.directness[lang])}</dd></dl><div class="evidence-sources">${intervention.sources.map(source=>externalLink(source.url,source.label)).join('')}</div><p class="nonrecommendation">${t('Intervention Evidence ≠ „CEM recomandă această acțiune”.','Intervention Evidence ≠ “CEM recommends this action”.')}</p></article></main>`;

 const atlasView=()=>{
  const visibleIds=atlasFilter==='major'?[]:atlasFilter==='all'?cemProductNodes.map(node=>node.id):(atlasGroups.find(group=>group.id===atlasFilter)?.nodes??[]);
  const visible=new Set(visibleIds);
  const relatedEdges=selected?cemProductEdges.filter(edge=>(edge.source===selected.id||edge.target===selected.id)&&visible.has(edge.source)&&visible.has(edge.target)):[];
  const atlasNodes=cemProductNodes.filter(node=>visible.has(node.id)).map(node=>`<button type="button" class="atlas-node ${selected?.id===node.id?'is-selected':''}" data-suite-focus="${node.id}" style="--node-x:${node.x}%;--node-y:${node.y}%"><strong>${esc(clean(node.label[lang]))}</strong></button>`).join('');
  const atlasEdges=relatedEdges.map(edge=>{const a=nodeById(edge.source)!;const b=nodeById(edge.target)!;const relation=edgeEvidenceFor(edge.id);return `<line x1="${a.x}" y1="${a.y}" x2="${b.x}" y2="${b.y}" class="atlas-edge" data-edge-status="${relation?.status??'CONCEPTUAL_HYPOTHESIS'}" marker-end="url(#atlasArrow)"/>`;}).join('');
  const major=atlasGroups.map(group=>`<article class="atlas-major-group"><h3>${esc(group.label[lang])}</h3><p>${group.nodes.map(id=>nodeName(id,lang)).filter((value,index,array)=>array.indexOf(value)===index).join(' · ')}</p><button type="button" data-atlas-filter="${group.id}">${t('Extinde mecanismele','Expand mechanisms')}</button></article>`).join('');
  return `<main class="atlas-view" data-product-surface="atlas"><div class="section-heading"><div><p class="eyebrow">FULL MODEL ATLAS</p><h2>${t('Harta completă este secundară și progresivă','The full model map is secondary and progressive')}</h2><p>${t('Implicit vezi doar nivelurile majore. Extinde o familie sau toate mecanismele; relațiile apar numai în jurul mecanismului selectat pentru a evita spaghetti graph.','By default you see only major levels. Expand a family or all mechanisms; relations appear only around the selected mechanism to avoid a spaghetti graph.')}</p></div></div><div class="atlas-controls"><label>${t('Filtru','Filter')}<select id="atlasFilter"><option value="major" ${atlasFilter==='major'?'selected':''}>${t('Niveluri majore','Major levels')}</option><option value="all" ${atlasFilter==='all'?'selected':''}>${t('Toate mecanismele','All mechanisms')}</option>${atlasGroups.map(group=>`<option value="${group.id}" ${atlasFilter===group.id?'selected':''}>${esc(group.label[lang])}</option>`).join('')}</select></label><label>${t('Zoom','Zoom')}<input id="atlasZoom" type="range" min="0.75" max="1.5" step="0.05" value="${atlasZoom}"></label></div>${atlasFilter==='major'?`<div class="atlas-major-grid">${major}</div>`:`<div class="atlas-scroll"><div class="atlas-map" style="--atlas-zoom:${atlasZoom}"><svg class="atlas-links" viewBox="0 0 100 100" aria-hidden="true"><defs><marker id="atlasArrow" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 z"/></marker></defs>${atlasEdges}</svg>${atlasNodes}</div></div>`}<p class="atlas-note">${t('Selectarea unui mecanism arată numai relațiile directe înregistrate. Grosimea sau poziția nu reprezintă mărimea efectului.','Selecting a mechanism reveals only its directly registered relations. Thickness or position does not represent effect size.')}</p></main>`;
 };

 const theoryView=()=>`<main class="theory-view" data-product-surface="theory"><div class="section-heading"><div><p class="eyebrow">THEORY / LEARN</p><h2>${t('Manualul complet al CEM','The complete CEM manual')}</h2><p>${t('Poți parcurge manualul independent sau poți deschide direct capitolul relevant dintr-un pathway ori mecanism. Limbajul principal este conceptual și natural; identificatorii tehnici rămân în Research / Provenance.','Read the manual independently or open the relevant chapter directly from a pathway or mechanism. The primary language is conceptual and natural; technical identifiers remain in Research / Provenance.')}</p></div><button type="button" class="primary" data-suite-understanding="theory">${t('Deschide reader-ul complet','Open full reader')}</button></div><div class="theory-topic-grid">${theoryTopics.map(topic=>`<button type="button" class="theory-topic" data-suite-theory-chapter="${esc(topic.chapterSlug)}"><strong>${esc(topic.label[lang])}</strong><small>${esc(topic.scope[lang])}</small></button>`).join('')}</div><div id="suiteTheoryContext" class="suite-context-slot theory-context"></div></main>`;

 const technicalView=()=>`<main class="technical-view" data-product-surface="technical"><div class="section-heading"><div><p class="eyebrow">RESEARCH / TECHNICAL PROVENANCE</p><h2>${t('Identificatori, registry și instrumente de audit','Identifiers, registry and audit tools')}</h2><p>${t('Această zonă este separată intenționat de experiența normală. Aici pot apărea codurile interne necesare cercetării și reproducerii.','This area is intentionally separated from the normal experience. Internal codes needed for research and reproducibility may appear here.')}</p></div></div>${selected?`<article class="technical-selected"><h3>${esc(selected.label[lang])}</h3><p><strong>Identifiers:</strong> <code>${esc(selected.identifiers.join(' · '))}</code></p><p><strong>Evidence registry:</strong> <code>${esc(selected.evidenceRefs.join(' · ')||'—')}</code></p><p><strong>Theory slug:</strong> <code>${esc(selected.chapterSlug)}</code></p><p><strong>Required provenance:</strong> ${esc(selected.provenance[lang])}</p></article>`:''}<div class="technical-actions"><button type="button" data-suite-tool="search">Semantic Search</button><button type="button" data-suite-tool="inspector">Semantic Inspector</button><button type="button" data-suite-view="structure">Structure</button><button type="button" data-suite-view="runs">Runs</button><button type="button" data-suite-view="comparison">Comparison</button><button type="button" data-suite-view="planning">Planning</button><button type="button" data-suite-view="reference">Reference registry</button><button type="button" data-suite-view="process">Process / ODD</button></div><details class="technical-node-register"><summary>${t('Registrul mecanismelor','Mechanism register')}</summary><div>${cemProductNodes.map(node=>`<p><strong>${esc(node.label[lang])}</strong> <code>${esc(node.id)} · ${esc(node.identifiers.join(' · '))}</code></p>`).join('')}</div></details><div id="suiteAuxContext" class="suite-context-slot"></div></main>`;

 let content='';
 if(productView==='home')content=home();
 else if(productView==='pathway')content=pathwayFlow();
 else if(productView==='interventions')content=interventionsView();
 else if(productView==='atlas')content=atlasView();
 else if(productView==='theory')content=theoryView();
 else content=technicalView();
 const hiddenTheory=productView==='theory'?'':`<div id="suiteTheoryContext" class="suite-context-slot" hidden></div>`;
 const hiddenAux=productView==='technical'?'':`<div id="suiteAuxContext" class="suite-context-slot" hidden></div>`;
 host.innerHTML=`<section class="suite-overview product-concept-shell" data-suite-standard="InfoClar Model Suite Design Standard v1.1">${chrome}${content}${hiddenTheory}${hiddenAux}${productView==='pathway'?mechanismDrawer():''}</section>`;

 host.querySelectorAll<HTMLButtonElement>('[data-product-view]').forEach(button=>button.onclick=()=>{productView=button.dataset.productView as ProductView;if(productView==='pathway'&&!activeQuestionId)productView='home';mountSuiteOverview(host,options);});
 host.querySelectorAll<HTMLButtonElement>('[data-pathway-question]').forEach(button=>button.onclick=()=>{activeQuestionId=button.dataset.pathwayQuestion;productView='pathway';options.openFocus('overview');});
 host.querySelectorAll<HTMLButtonElement>('[data-suite-focus]').forEach(button=>button.onclick=()=>options.openFocus(button.dataset.suiteFocus!));
 host.querySelectorAll<HTMLButtonElement>('[data-close-mechanism]').forEach(button=>button.onclick=()=>options.openFocus('overview'));
 host.querySelectorAll<HTMLButtonElement>('[data-suite-theory-chapter]').forEach(button=>button.onclick=()=>{productView='theory';options.openTheoryChapter(button.dataset.suiteTheoryChapter!);});
 host.querySelectorAll<HTMLButtonElement>('[data-suite-understanding]').forEach(button=>button.onclick=()=>{productView='theory';options.openUnderstanding(button.dataset.suiteUnderstanding as LearnMode);});
 host.querySelectorAll<HTMLButtonElement>('[data-suite-view]').forEach(button=>button.onclick=()=>{productView='technical';options.openView(button.dataset.suiteView as ContextView);});
 host.querySelectorAll<HTMLButtonElement>('[data-suite-tool]').forEach(button=>button.onclick=()=>{productView='technical';options.openTool(button.dataset.suiteTool as AuxTool);});
 host.querySelectorAll<HTMLButtonElement>('[data-atlas-filter]').forEach(button=>button.onclick=()=>{atlasFilter=button.dataset.atlasFilter!;mountSuiteOverview(host,options);});
 const interventionSelect=host.querySelector<HTMLSelectElement>('#interventionEvidenceSelect');if(interventionSelect)interventionSelect.onchange=()=>{activeInterventionId=interventionSelect.value;mountSuiteOverview(host,options);};
 const atlasSelect=host.querySelector<HTMLSelectElement>('#atlasFilter');if(atlasSelect)atlasSelect.onchange=()=>{atlasFilter=atlasSelect.value;options.openFocus('overview');};
 const atlasZoomInput=host.querySelector<HTMLInputElement>('#atlasZoom');if(atlasZoomInput)atlasZoomInput.oninput=()=>{atlasZoom=Number(atlasZoomInput.value);host.querySelector<HTMLElement>('.atlas-map')?.style.setProperty('--atlas-zoom',String(atlasZoom));};
}
