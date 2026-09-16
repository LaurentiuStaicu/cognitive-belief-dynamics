import release from '../public/model/version.json';
import cytoscape, {type Core} from 'cytoscape';
import './style.css';
import './elementary.css';
import './visual-language.css';
import './search-ui.css';
import './inspector-ui.css';
import './active-understanding-ui.css';
import './decision-uncertainty-ui.css';
import './action-canvas.css';
import './indicator-objects.css';
import './signposts-triggers.css';
import './adaptive-plan-runtime.css';
import {chartSeries} from './visual-language';
import {mountSemanticSearch} from './search-ui';
import {mountSemanticInspector} from './inspector-ui';
import {mountUnderstanding} from './understanding';
import {type TheoryChapter,type TheoryGlossaryEntry,type TheoryValidation} from './theory-reader';
import {type M1EditorialData,type EmpiricalTarget} from './editorial-stage';
import {type M1PresentationData} from './presentation-stage';
import {type M1AccessData} from './access-stage';
import {mountComparison} from './comparison';
import {renderExplanation,type ExplanationData} from './explanation';
let explanations:ExplanationData;
import {mountVisualStage} from './visual-stage';
import {dependencies,extraNodes} from './dependencies';
import {assertSemanticCoverage,semanticLabel} from './semantic';
import {initializeWorkspaceSession,validateWorkspaceRuntime} from './workspace-session';
import {migrateLegacyWorkspaceToIndexedDb} from './workspace-indexeddb';
import {isAppView,navigationGroupForView,navigationGroups,type AppView} from './navigation';
let graphMode='core';
let graphFocus='all';
import {mountPlanner,type PlanningData} from './planner';
import {type DecisionUncertaintyRegistry} from './decision-uncertainty-contract';
import {scenarioName} from './labels';
import {mountVisualOdd,type OddProcess,type Subsystem} from './odd';

type Lang = 'ro' | 'en';
type Variable = {id:string; short_name:string; label:Record<Lang,string>; definition:string; what_it_is_not:string; conceptual_module:string; ontology_type:string};
type Link = {id:string; source:string; target:string; relation_type:string; polarity:string; mechanism_evidence_status:string; functional_form_status:string; phenomenon_evidence_status:string; evidence_refs:string[]; evidence_summary:Record<Lang,string>; evidence_limitations:Record<Lang,string>};
type Frame = {time:number; familiarity:number; correction:number; reliability:number; belief:number; accuracy_weight:number; share_probability:number; share:boolean; events:{event_type:string}[]};
type Run = {id:string; seed:number; prior:number; parameters:Record<string,number>; frames:Frame[]};
type Reference = {id:string; citation:string; url:string; access_url:string; checked_on:string; review_scope:string};
type Module = {id:string;label:Record<Lang,string>};
let lang:Lang = 'ro';
let view:AppView = 'learning';
let planning:PlanningData;
let decisionUncertainty:DecisionUncertaintyRegistry;
let selected = 'correction';
let step = 0;
let playing:ReturnType<typeof setInterval> | undefined;
let graph:Core | undefined;
let variables:Variable[] = [];
let links:Link[] = [];
let modules:Module[] = [];
let runs:Run[] = [];
let references:Reference[] = [];
let oddProcesses:OddProcess[] = [];
let subsystems:Subsystem[] = [];
let m1Editorial:M1EditorialData;
let m1Presentation:M1PresentationData;
let m1Access:M1AccessData;
let m1Targets:EmpiricalTarget[] = [];
let theoryIndex:TheoryChapter[] = [];
let theoryGlossary:TheoryGlossaryEntry[] = [];
let validationTests:TheoryValidation[] = [];
let registryFocus = '';
let semanticSearchQuery = '';
let semanticInspectorId = '';
const app = document.getElementById('app')!;
const tr = (ro:string,en:string) => lang === 'ro' ? ro : en;
const num = (n:number) => n.toLocaleString(lang === 'ro' ? 'ro-RO' : 'en-GB', {minimumFractionDigits:3,maximumFractionDigits:3});
const escape = (s:string) => s.replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]!));
const text = (s:string) => escape(s);
const runName = (id:string) => scenarioName(id, lang);
const definitions:Record<string,[string,string]> = {
 F:['Familiaritatea unei afirmații după expuneri repetate.','Nu măsoară adevărul, fiabilitatea sursei sau dovezile factuale.'],
 C:['Accesibilitatea curentă a informației corective despre afirmație.','Nu garantează corectarea convingerii.'],
 T:['Estimarea făcută de agent privind fiabilitatea sursei în sarcina curentă.','Nu este fiabilitatea reală a sursei.'],
 B:['Propensiunea latentă de a judeca afirmația drept adevărată la un moment dat.','Nu reprezintă cunoaștere, ideologie sau angajament identitar.'],
 W:['Ponderea contextuală acordată acurateții în decizia de distribuire.','Nu reprezintă raționalitatea generală sau activarea Sistemului 2.'],
 Nexp:['Numărul expunerilor agentului la o informație.','Nu este familiaritatea în sine.'],
 Share:['Acțiunea observată sau simulată de distribuire.','Nu echivalează cu o convingere sau cu aprobarea conținutului.'],
 Vcontent:['Valența semnată atribuită unei unități informaționale relevante pentru eveniment în sarcina M1.','Nu este valoarea de adevăr, factualitatea, ideologia politică sau starea emoțională a unei persoane.'],
 Eedit:['Politica de referință care controlează ce unități informaționale sunt selectate preferențial dintr-un pool factual fix.','Nu este un scor măsurat de bias al unei redacții, o rată de dezinformare sau un parametru de ranking al platformei.'],
 Sobs:['Media valenței semnate a unităților informaționale efectiv observate după selecția editorială.','Nu este adevărul evenimentului, valența totală a lumii sau opinia unei persoane.'],
 Aissue:['Starea M1 mărginită care reprezintă evaluarea curentă a unui eveniment sau subiect după eșantionul informațional observat.','Nu este convingerea B despre adevărul unei afirmații, cunoaștere, ideologie sau diagnostic afectiv.'],
 Fpres:['Codarea de referință a cadrului de prezentare confirmation versus refutation pentru același sens semantic.','Nu este valoare de adevăr, factualitate, selecție editorială sau valență emoțională.'],
 Gatt:['Relația task-specifică dintre atitudinea anterioară relevantă și poziția semantică a mesajului curent.','Nu este ideologie stabilă, identitate de partid, personalitate sau scor global de confirmation bias.'],
 Pengage:['Probabilitatea latentă M1.E2 a unui răspuns de engagement activ în sarcina de referință.','Nu este probabilitatea M0 Share, CTR observat, endorsement sau rată populațională calibrată.'],
 EngageIntent:['Outcome observabil de referință pentru un răspuns activ declarat versus ignore.','Nu este M0 Share, comportament real pe platformă sau endorsement.'],
 Hneg:['Indiciu binar precomputat care separă condiția de titlu cu negativitate mai redusă de cea cu negativitate mai ridicată în M1.E3.','Nu este scor de sentiment calculat la runtime, proporție LIWC, adevăr, etichetă de dezinformare sau mărime de efect calibrată.'],
 PreviewImpression:['Eveniment înregistrat că preview-ul titlului a fost randat sau disponibil în sarcina M1.E3.','Nu dovedește fixație vizuală, lectură, encodare, reamintire sau acces la conținutul complet.'],
 Paccess:['Probabilitatea latentă M1.E3 de click/deschidere a conținutului complet, condiționată de o impresie de preview.','Nu este CTR populațional observat, atenție, durată de lectură, convingere, Pengage sau probabilitatea M0 Share.'],
 Access:['Rezultatul binar M1.E3 care indică dacă elementul complet este deschis după impresia preview-ului.','Nu este atenție, finalizarea lecturii, endorsement, convingere, EngageIntent sau distribuire.']
};
const scenarioDescription = () => ({
 repetition:tr('Patru expuneri la pașii 1–4 cresc familiaritatea. Nu se adaugă dovezi sau corecții.','Four exposures at steps 1–4 increase familiarity. No evidence or corrections are added.'),
 correction:tr('După cele patru expuneri, o corecție apare la pasul 5. Accesibilitatea ei scade apoi exponențial.','After four exposures, a correction arrives at step 5. Its accessibility then decays exponentially.'),
 source:tr('La pașii 2, 4, 6 și 8, feedbackul negativ scade fiabilitatea estimată a sursei. Semnalul de evidență rămâne +0,6.','Negative feedback at steps 2, 4, 6 and 8 reduces estimated source reliability. The evidence signal remains +0.6.'),
 accuracy:tr('De la pasul 5, un indiciu pune mai mult accent pe acuratețe în decizia de distribuire. Nu modifică direct convingerea.','From step 5, a cue gives accuracy more weight in the sharing decision. It does not directly change belief.')
}[selected]!);
const eventName = (s:string) => ({ExposureEvent:tr('Expunere','Exposure'),CorrectionEvent:tr('Corecție','Correction'),SourceFeedbackEvent:tr('Feedback despre sursă','Source feedback'),DecisionEvent:tr('Judecată și decizie','Judgment and decision')}[s] ?? s);
const run = () => runs.find(r=>r.id===selected)!;
const stop = () => { if(playing!==undefined) clearInterval(playing); playing=undefined; };

function shell() {
 graph?.destroy(); graph=undefined;
 document.documentElement.lang=lang;
 app.innerHTML=`<header class="topbar"><a class="brand" href="#" aria-label="Cognitive Epistemic Model"><img class="brand-icon" src="./icon.svg" width="42" height="42" alt=""><span>Cognitive Epistemic Model<small>${tr('Laborator de explorare','Exploration lab')}</small></span></a><div class="top-actions"><a class="version" id="releaseVersion" href="https://github.com/LaurentiuStaicu/cognitive-epistemic-model/releases/tag/${release.release_tag}" target="_blank" rel="noopener">${release.channel} ${release.version} · ${release.model}</a><button id="language" aria-label="${tr('Schimbă limba interfeței în engleză','Switch the interface language to Romanian')}">${lang==='ro'?'EN':'RO'}</button><a href="https://github.com/LaurentiuStaicu/cognitive-epistemic-model" target="_blank" rel="noopener">GitHub ↗</a></div></header>
 <div class="workspace"><div class="intro"><div><p class="eyebrow">${tr('FORMAREA CONVINGERILOR','BELIEF FORMATION')}</p><h1>${tr('Mecanisme, intervenții, priorități.','Mechanisms, interventions, priorities.')}</h1><p>${tr('Înțelege relațiile dintre factori și compară efectele măsurilor, separat și împreună.','Understand relationships between factors and compare measures, individually and together.')}</p></div><div class="scope"><strong>${variables.length}</strong><span>${tr('variabile înregistrate','registered variables')}</span><strong>04</strong><span>${tr('scenarii de referință','reference scenarios')}</span></div></div>
 <div id="semanticSearch"></div>
 <div class="navigation-shell">${(()=>{const active=navigationGroupForView(view);return `<nav class="nav-groups" aria-label="${tr('Domeniile aplicației','Application domains')}">${navigationGroups.map(group=>`<button data-nav-group="${group.id}" aria-pressed="${active.id===group.id}" title="${group.description[lang]}">${group.label[lang]}</button>`).join('')}</nav><nav class="views" aria-label="${tr('Vederile din domeniul curent','Views in current domain')}">${active.items.map(item=>`<button data-view="${item.view}" aria-pressed="${view===item.view}" title="${item.description[lang]}">${item.label[lang]}</button>`).join('')}</nav>`;})()}</div>
 <div class="app-content-shell"><main id="content"></main><aside id="semanticInspector" class="panel semantic-inspector-global" aria-labelledby="semanticInspectorTitle" tabindex="-1"></aside></div><footer><span>${tr('Model demonstrativ · coeficienți necalibrați','Demonstration model · uncalibrated coefficients')}</span><span>${tr('Nu estimează proporții Track A/B sau diagnostice individuale.','Does not estimate Track A/B prevalence or individual diagnoses.')}</span></footer></div>`;
 const remountInspector=(focus=false)=>{const host=document.getElementById('semanticInspector')!;mountSemanticInspector(host,{lang,id:semanticInspectorId,onSelect:id=>{semanticInspectorId=id;remountInspector(true);}});if(focus)host.focus({preventScroll:false});};
 const remountSearch=(focus=false)=>{const host=document.getElementById('semanticSearch')!;mountSemanticSearch(host,{lang,initialQuery:semanticSearchQuery,onQueryChange:query=>{semanticSearchQuery=query;},onSelect:id=>{semanticInspectorId=id;remountInspector(true);}});if(focus)host.querySelector<HTMLInputElement>('#semanticSearchInput')?.focus({preventScroll:false});};
 remountSearch();
 remountInspector();
 document.getElementById('language')!.onclick=()=>{stop();lang=lang==='ro'?'en':'ro';shell();};
 document.querySelectorAll<HTMLButtonElement>('[data-nav-group]').forEach(b=>b.onclick=()=>{stop();const group=navigationGroups.find(candidate=>candidate.id===b.dataset.navGroup);if(!group)return;view=group.defaultView;if(view==='reference')registryFocus='';shell();document.getElementById('content')!.scrollIntoView({block:'start'});});
 document.querySelectorAll<HTMLButtonElement>('[data-view]').forEach(b=>b.onclick=()=>{stop();const next=b.dataset.view;if(!next||!isAppView(next))return;if(next==='reference')registryFocus='';view=next;shell();});
 if(view==='learning') mountUnderstanding(document.getElementById('content')!,lang,runs,m1Editorial,m1Presentation,m1Access,m1Targets,{chapters:theoryIndex,glossary:theoryGlossary,variables,modules,references,validations:validationTests,releaseTag:release.release_tag},target=>{stop();const [nextRaw,...parts]=target.split(':');const payload=parts.join(':');if(nextRaw==='search'){semanticSearchQuery=payload;remountSearch(true);return;}if(nextRaw==='inspect'){semanticInspectorId=payload;remountInspector(true);return;}const [id,time]=parts;if(!isAppView(nextRaw))throw new Error(`unknown application view: ${nextRaw}`);const next=nextRaw;if(location.hash.startsWith('#understanding/')&&!target.startsWith('learning'))history.pushState({cemView:next,cemId:id??null,cemTime:time??null},'',location.href);view=next;if(next==='reference'){registryFocus=id??'';}else if(id){selected=id;step=time===undefined?0:Number(time);}shell();document.getElementById('content')!.scrollIntoView({block:'start'});});
 if(view==='planning') mountPlanner(document.getElementById('content')!,planning,decisionUncertainty,lang,target=>{const [kind,...parts]=target.split(':');const payload=parts.join(':');if(kind==='search'){semanticSearchQuery=payload;remountSearch(true);return;}if(kind==='inspect'){semanticInspectorId=payload;remountInspector(true);return;}if(kind==='reference'){history.pushState({cemView:'reference',cemId:payload,cemTime:null},'',location.href);registryFocus=payload;view='reference';shell();document.getElementById('content')!.scrollIntoView({block:'start'});return;}throw new Error(`unknown planner navigation target: ${target}`);});
 if(view==='runs') renderRuns();
 if(view==='comparison') mountComparison(document.getElementById('content')!,runs,lang,(id,time)=>{selected=id;step=time;view='runs';shell();document.getElementById('content')!.scrollIntoView({block:'start'});});
 if(view==='structure') renderStructure();
 if(view==='process') renderProcess();
 if(view==='reference') renderReference();
}
function content(html:string) { document.getElementById('content')!.innerHTML=html; }
function renderRuns() {
 content(`<div class="run-layout"><aside class="panel settings"><p class="eyebrow">${tr('SCENARIU','SCENARIO')}</p><label for="scenario">${tr('Ce mecanism explorăm?','Which mechanism?')}</label><select id="scenario">${runs.map(r=>`<option value="${r.id}" ${r.id===selected?'selected':''}>${runName(r.id)}</option>`).join('')}</select><p class="description">${scenarioDescription()}</p><div class="assumptions"><div><span>${tr('Convingere inițială','Prior belief')}</span><b>0.300</b></div><div><span>${tr('Agent / afirmație','Agent / claim')}</span><b>A1 / C1</b></div><div><span>Seed</span><b>7</b></div></div><p class="note">${tr('Redare a unei rulări precalculate de nucleul Python. Pașii sunt unități abstracte, nu ani sau zile.','Replay of a run precomputed by the Python core. Steps are abstract units, not years or days.')}</p><details><summary>${tr('Parametrii acestei rulări','Run parameters')}</summary><dl class="parameters">${Object.entries(run().parameters).map(([k,v])=>`<dt>${k}</dt><dd>${v}</dd>`).join('')}</dl></details><button class="download" id="download">${tr('Descarcă rularea JSON ↓','Download run JSON ↓')}</button></aside>
 <section class="panel experiment"><div class="section-heading"><div><p class="eyebrow">${tr('RULARE DE REFERINȚĂ','REFERENCE RUN')}</p><h2>${runName(selected)}</h2></div><span class="step-badge" id="stepBadge"></span></div><div class="metrics" id="metrics"></div><div class="chart-wrap" id="chart"></div><div class="legend"><span class="belief">${tr('Convingere','Belief')}</span><span class="sharing">${tr('Probabilitate de distribuire','Sharing probability')}</span><span class="corrective">${tr('Accesibilitatea corecției','Correction accessibility')}</span></div><p class="chart-readout" id="chartReadout"></p><div class="transport"><button id="previous">${tr('Pasul anterior','Previous step')}</button><button class="primary" id="play"></button><button id="next">${tr('Pasul următor','Next step')}</button><button id="reset">↺ ${tr('De la început','Reset')}</button><label class="sr-only" for="timeline">${tr('Pasul rulării','Run step')}</label><input id="timeline" type="range" min="0" max="12" step="1" value="${step}"></div><div class="event-strip" id="events" role="status" aria-live="polite"></div><section id="stepExplanation" class="step-explanation"></section><details class="results"><summary>${tr('Vezi valorile într-un tabel','View values in a table')}</summary><div class="table-scroll"><table><caption>${tr('Toți pașii rulării selectate','All steps of the selected run')}</caption><thead><tr><th>${tr('Pas','Step')}</th><th>B</th><th>P(${tr('distribuire','share')})</th><th>F</th><th>C</th><th>T</th><th>W</th><th>${tr('Distribuit','Shared')}</th></tr></thead><tbody>${run().frames.map(f=>`<tr><td>${f.time}</td>${[f.belief,f.share_probability,f.familiarity,f.correction,f.reliability,f.accuracy_weight].map(v=>`<td>${num(v)}</td>`).join('')}<td>${f.share?tr('Da','Yes'):tr('Nu','No')}</td></tr>`).join('')}</tbody></table></div></details></section></div>`);
 document.getElementById('scenario')!.onchange=e=>{stop();selected=(e.target as HTMLSelectElement).value;step=0;renderRuns();};
 document.getElementById('play')!.onclick=()=>{if(playing!==undefined){stop();updateFrame();return;} if(step===12)step=0;playing=setInterval(()=>{step++;if(step>=12)stop();updateFrame();},850);updateFrame();};
 document.getElementById('previous')!.onclick=()=>{stop();step=Math.max(0,step-1);updateFrame();};
 document.getElementById('next')!.onclick=()=>{stop();step=Math.min(12,step+1);updateFrame();};
 document.getElementById('reset')!.onclick=()=>{stop();step=0;updateFrame();};
 document.getElementById('timeline')!.oninput=e=>{stop();step=Number((e.target as HTMLInputElement).value);updateFrame();};
 document.getElementById('download')!.onclick=()=>{const url=URL.createObjectURL(new Blob([JSON.stringify({model_version:release.version,...run(),explanation:explanations.runs.find(r=>r.id===selected)},null,2)],{type:'application/json'}));const a=document.createElement('a');a.href=url;a.download=`cem-m0-${selected}.json`;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);};
 updateFrame();
}
function updateFrame(){
 const f=run().frames[step];
 document.getElementById('stepBadge')!.textContent=`${tr('Pas','Step')} ${step} / 12`;
 document.getElementById('metrics')!.innerHTML=[[tr('Convingere · B','Belief · B'),f.belief,'belief'],[tr('P(distribuire)','P(share)'),f.share_probability,'sharing'],[tr('Corecție · C','Correction · C'),f.correction,'corrective']].map(([label,value,color])=>`<div><span>${label}</span><strong class="${color}">${num(Number(value))}</strong></div>`).join('');
 const px=(i:number)=>50+i*55; const py=(v:number)=>242-v*212;
 const line=(key:keyof Frame,color:string,dash:string)=>`<polyline fill="none" stroke="${color}" stroke-width="3" stroke-dasharray="${dash}" points="${run().frames.slice(0,step+1).map(f=>`${px(f.time)},${py(Number(f[key]))}`).join(' ')}"/><circle cx="${px(step)}" cy="${py(Number(f[key]))}" r="5" fill="${color}"/>`;
 document.getElementById('chart')!.innerHTML=`<svg viewBox="0 0 748 290" role="img" aria-label="${tr('Evoluția convingerii, distribuirii și corecției; valorile exacte sunt în tabelul de mai jos.','Belief, sharing and correction trajectories; exact values are in the table below.')}"><title>${runName(selected)}</title>${[0,.25,.5,.75,1].map(v=>`<line x1="50" x2="710" y1="${py(v)}" y2="${py(v)}" stroke="var(--border)"/><text x="36" y="${py(v)+5}" text-anchor="end">${v}</text>`).join('')}${run().frames.map(f=>`<text x="${px(f.time)}" y="270" text-anchor="middle">${f.time}</text>`).join('')}<line x1="${px(step)}" x2="${px(step)}" y1="24" y2="242" stroke="var(--muted)" stroke-dasharray="4 5"/>${line('belief',`var(${chartSeries.belief.cssVar})`,chartSeries.belief.dash)}${line('share_probability',`var(${chartSeries.sharing.cssVar})`,chartSeries.sharing.dash)}${line('correction',`var(${chartSeries.correction.cssVar})`,chartSeries.correction.dash)}</svg>`;
 document.getElementById('events')!.textContent=`${tr('La acest pas','At this step')}: ${f.events.map(e=>eventName(e.event_type)).join(' → ')}. ${tr('Distribuire simulată','Simulated share')}: ${f.share?tr('da','yes'):tr('nu','no')}.`;
 document.getElementById('play')!.textContent=playing!==undefined?tr('⏸ Pauză','⏸ Pause'):tr('▶ Redă','▶ Play');
 (document.getElementById('timeline') as HTMLInputElement).value=String(step);
 (document.getElementById('next') as HTMLButtonElement).disabled=step===12;
 (document.getElementById('previous') as HTMLButtonElement).disabled=step===0;
 const explained=explanations.runs.find(r=>r.id===selected)!;
 renderExplanation(document.getElementById('stepExplanation')!,explained.frames[step],explained.frames,f,lang);
 const readout=(index:number)=>{const point=run().frames[index];document.getElementById('chartReadout')!.textContent=`${tr('Pas','Step')} ${index} · B: ${num(point.belief)} · P: ${num(point.share_probability)} · C: ${num(point.correction)}. ${tr('Folosește cursorul pe grafic sau selectorul de pas pentru valorile exacte.','Use the chart pointer or step slider for exact values.')}`;};
 readout(step);
 const svg=document.querySelector<SVGSVGElement>('#chart svg')!;
 svg.onpointermove=e=>{const point=new DOMPoint(e.clientX,e.clientY).matrixTransform(svg.getScreenCTM()!.inverse());readout(Math.max(0,Math.min(step,Math.round((point.x-50)/55))));};
 svg.onpointerleave=()=>readout(step);
}
function variableDetail(v:Variable){const localized=definitions[v.short_name];const definition=lang==='ro'&&localized?localized[0]:v.definition;const not=lang==='ro'&&localized?localized[1]:v.what_it_is_not;return `<p class="eyebrow">${text(v.short_name)} · ${text(v.ontology_type)}</p><h2>${text(semanticLabel(v.id,lang,v.label[lang]))}</h2><p>${text(definition)}</p><div class="boundary"><strong>${tr('Ce nu reprezintă','What this is not')}</strong><p>${text(not)}</p></div><p class="meta">${text(v.conceptual_module)} · ${text(semanticLabel(v.conceptual_module,lang,modules.find(m=>m.id===v.conceptual_module)!.label[lang]))}</p><code>${text(v.id)}</code>`;}
function renderStructure(){
 if(graphMode==='registered')renderRegisteredStructure();else renderComputationalStructure();
 const host=document.getElementById('content')!;
 host.insertAdjacentHTML('afterbegin',`<div class="graph-controls panel"><label for="graphMode">${tr('Ce hartă explorezi?','Which map?')}</label><select id="graphMode"><option value="core">${tr('Dependențe M0 · nucleu','M0 dependencies · core')}</option><option value="inputs">${tr('Dependențe M0 · cu intrări contextuale','M0 dependencies · including context inputs')}</option><option value="registered">${tr('Relațiile din registrul de dovezi','Evidence-registry relationships')}</option></select></div>`);
 const mode=host.querySelector<HTMLSelectElement>('#graphMode')!;mode.value=graphMode;mode.onchange=()=>{graphMode=mode.value;graphFocus='all';shell();};
}
function renderComputationalStructure(){
 const core=['Nexp','F','C','T','B','W','Share','P'];
 const focusNodes:Record<string,string[]>={all:[],repetition:['Nexp','F','B','P','Share','Prior'],correction:['Correction','Time','C','Direction','B','F','P','Share'],source:['Feedback','T','Evidence','B','P','Share'],decision:['B','W','P','Share','Cue','Baseline','Reward','Random']};
 const visible=(id:string)=>(graphMode==='inputs'||core.includes(id))&&(graphFocus==='all'||focusNodes[graphFocus].includes(id));
 const nodes=[...variables.map(v=>({id:v.short_name,label:v.short_name,name:semanticLabel(v.id,lang,v.label[lang]),kind:'variable'})),...extraNodes.map(v=>({id:v.id,label:v.id==='P'?tr('P(distribuire)','P(share)'):v[lang],name:v[lang],kind:v.kind}))].filter(v=>visible(v.id));
 const edges=dependencies.filter(e=>visible(e.source)&&visible(e.target));
 const label=(id:string)=>nodes.find(n=>n.id===id)?.name??id;
 content(`<div class="section-heading"><div><h2>${tr('Cum calculează M0 rezultatele','How M0 computes outcomes')}</h2><p>${tr('Săgețile arată dependențe de calcul. Liniile continue au o corespondență în registru; cele întrerupte sunt explicate din cod, fără o evaluare bibliografică proprie. Niciuna nu certifică validarea mecanismului.','Arrows show computational dependencies. Solid lines have a registry correspondence; dashed lines are explained from code without their own evidence assessment. Neither certifies mechanism validity.')}</p></div><button id="fit">${tr('Încadrează harta','Fit graph')}</button></div><div class="graph-controls"><label for="graphFocus">${tr('Concentrează harta pe un mecanism','Focus on a mechanism')}</label><select id="graphFocus">${[['all',tr('Ansamblu','Overview')],['repetition',tr('Repetiție','Repetition')],['correction',tr('Corecție','Correction')],['source',tr('Sursă și evidență','Source and evidence')],['decision',tr('Decizie','Decision')]].map(([id,name])=>`<option value="${id}" ${graphFocus===id?'selected':''}>${name}</option>`).join('')}</select><p class="note" id="graphCount">${nodes.length} ${tr('noduri','nodes')} · ${edges.length} ${tr('dependențe vizibile','visible dependencies')}. ${tr('Cercuri: variabile înregistrate. Dreptunghi: probabilitate calculată. Capsule: intrări. Coeficienții sunt explicați în detalii.','Circles: registered variables. Rectangle: calculated probability. Capsules: inputs. Coefficients are explained in details.')}</p></div><div class="graph-layout"><div class="panel graph-panel"><div id="cy" role="img" aria-label="${tr('Hartă de calcul; toate nodurile și relațiile sunt accesibile prin selectoarele alăturate.','Computational map; all nodes and links are accessible through adjacent selectors.')}"></div><p class="graph-hint">${tr('Selectează un nod sau o săgeată. Nu există în M0 o buclă automată de la distribuire la expuneri viitoare.','Select a node or arrow. M0 has no automatic feedback loop from sharing to future exposures.')}</p></div><aside class="panel detail-panel"><label for="variable">${tr('Inspectează un factor','Inspect a factor')}</label><select id="variable">${nodes.map(n=>`<option value="${variables.find(v=>v.short_name===n.id)?.id??n.id}">${text(n.name)}</option>`).join('')}</select><label for="dependency">${tr('Inspectează o interacțiune','Inspect an interaction')}</label><select id="dependency"><option value="">${tr('Alege o săgeată','Choose an arrow')}</option>${edges.map(e=>`<option value="${e.id}">${text(label(e.source))} → ${text(label(e.target))}</option>`).join('')}</select><div id="detail" aria-live="polite"></div></aside></div>`);
 const css=getComputedStyle(document.documentElement),token=(n:string)=>css.getPropertyValue(n).trim();
 const positions:Record<string,{x:number;y:number}>={Nexp:{x:20,y:30},F:{x:250,y:30},C:{x:250,y:190},T:{x:250,y:350},B:{x:520,y:190},W:{x:520,y:440},P:{x:780,y:190},Share:{x:1010,y:190},Prior:{x:520,y:-130},Evidence:{x:520,y:20},Direction:{x:250,y:-130},Cue:{x:250,y:580},Baseline:{x:520,y:580},Reward:{x:780,y:440},Feedback:{x:20,y:350},Correction:{x:20,y:190},Time:{x:20,y:580},Random:{x:1010,y:440}};
 graph=cytoscape({container:document.getElementById('cy'),elements:[...nodes.map(n=>({data:n,position:positions[n.id]})),...edges.map(e=>({data:{id:e.id,source:e.source,target:e.target,registered:e.registered?'yes':'no'}}))],style:[{selector:'node',style:{label:'data(label)','width':72,'height':72,'background-color':token('--soft'),'border-width':2,'border-color':token('--accent'),'color':token('--text'),'text-valign':'center','font-family':css.fontFamily,'font-size':18,'text-wrap':'wrap','text-max-width':'120px'}},{selector:'node[kind="input"]',style:{shape:'round-rectangle',width:145,height:62,'font-size':16}},{selector:'node[kind="output"]',style:{shape:'rectangle',width:145,height:68,'font-size':17}},{selector:'edge',style:{'curve-style':'bezier','target-arrow-shape':'triangle','line-color':token('--muted'),'target-arrow-color':token('--muted'),'width':2,'line-style':'dashed'}},{selector:'edge[registered="yes"]',style:{'line-style':'solid'}},{selector:'.related',style:{'line-color':token('--accent'),'target-arrow-color':token('--accent'),'width':4}},{selector:':selected',style:{'border-width':5,'line-color':token('--accent'),'target-arrow-color':token('--accent')}}],layout:{name:'preset',padding:45},minZoom:.2,maxZoom:3,wheelSensitivity:.2});
 const edgeDetail=(id:string)=>{const e=edges.find(e=>e.id===id)!;graph!.elements().unselect().removeClass('related');graph!.getElementById(id).select();(document.getElementById('dependency') as HTMLSelectElement).value=id;document.getElementById('detail')!.innerHTML=`<h2>${text(label(e.source))} → ${text(label(e.target))}</h2><p>${text(e[lang])}</p><p class="equation">${text(e.formula)}</p><p class="note">${tr('Relația este descrisă din implementarea M0, nu estimată din date populaționale.','This relationship is described from M0 implementation, not estimated from population data.')}</p><a href="https://github.com/LaurentiuStaicu/cognitive-epistemic-model/blob/main/src/cognitive_epistemic_model/${e.file}" target="_blank" rel="noopener">${tr('Vezi implementarea','View implementation')} · ${e.file}</a>${e.registered?`<details class="dependency-evidence"><summary>${tr('Corespondență și limite în registrul de dovezi','Correspondence and limits in the evidence registry')}</summary>${linkDetail(links.find(l=>l.id===e.registered)!)}</details>`:`<p class="boundary">${tr('Fără evaluare bibliografică proprie pentru această dependență. Formula este o alegere necalibrată a modelului.','No dedicated evidence assessment for this dependency. The formula is an uncalibrated model choice.')}</p>`}`;};
 const show=(id:string)=>{const v=variables.find(v=>v.id===id||v.short_name===id),key=v?.short_name??id;graph!.elements().unselect().removeClass('related');graph!.getElementById(key).select().connectedEdges().addClass('related');(document.getElementById('variable') as HTMLSelectElement).value=v?.id??id;(document.getElementById('dependency') as HTMLSelectElement).value='';const connected=edges.filter(e=>e.source===key||e.target===key);document.getElementById('detail')!.innerHTML=(v?variableDetail(v):`<h2>${text(label(key))}</h2><p>${key==='P'?tr('Probabilitatea este rezultatul politicii de distribuire și precede extragerea acțiunii. Nu este o a opta variabilă înregistrată.','Probability is the sharing policy output, preceding action sampling. It is not an eighth registered variable.'):tr('Intrare contextuală sau proprietate a agentului. Selectează o dependență pentru rolul, ecuația și limitele acesteia.','Contextual input or agent property. Select a dependency for its role, equation and limitations.')}</p>`)+`<h3>${tr('Dependențe vizibile','Visible dependencies')}</h3><div class="dependency-buttons">${connected.map(e=>`<button data-edge="${e.id}">${text(label(e.source))} → ${text(label(e.target))}</button>`).join('')}</div>`;document.querySelectorAll<HTMLButtonElement>('[data-edge]').forEach(b=>b.onclick=()=>edgeDetail(b.dataset.edge!));};
 graph.on('tap','node',e=>show(e.target.id()));graph.on('tap','edge',e=>edgeDetail(e.target.id()));
 document.getElementById('variable')!.onchange=e=>show((e.target as HTMLSelectElement).value);
 document.getElementById('dependency')!.onchange=e=>{const id=(e.target as HTMLSelectElement).value;if(id)edgeDetail(id);};
 document.getElementById('graphFocus')!.onchange=e=>{graphFocus=(e.target as HTMLSelectElement).value;shell();};
 document.getElementById('fit')!.onclick=()=>graph!.fit(undefined,45);show(nodes[0].id);
 mountVisualStage(graph!,lang,runs,explanations,selected,step,show,edgeDetail,(id,time)=>{selected=id;step=time;view='runs';shell();},(id,time)=>{selected=id;step=time;});
}

function renderRegisteredStructure(){
 content(`<div class="section-heading"><div><h2>${tr('Structura înregistrată','Registered structure')}</h2><p>${tr('Șapte variabile și trei relații documentate. Harta nu reprezintă încă toate dependențele din ecuații.','Seven variables and three documented links. The map does not yet represent every dependency in the equations.')}</p></div><button id="fit">${tr('Încadrează harta','Fit graph')}</button></div><div class="graph-layout"><div class="panel graph-panel"><div id="cy" role="img" aria-label="${tr('Hartă interactivă; pentru navigare cu tastatura folosiți selectorul alăturat.','Interactive graph; use the adjacent selector for keyboard access.')}"></div><p class="graph-hint">${tr('Selectează un nod sau o relație pentru detalii. Trage pentru deplasare.','Select a node or link for details. Drag to pan.')}</p></div><aside class="panel detail-panel"><label for="variable">${tr('Inspectează o variabilă','Inspect a variable')}</label><select id="variable">${variables.map(v=>`<option value="${v.id}">${text(semanticLabel(v.id,lang,v.label[lang]))}</option>`).join('')}</select><div id="detail"></div></aside></div>`);
 const positions:Record<string,{x:number;y:number}>={Nexp:{x:100,y:90},F:{x:300,y:90},B:{x:500,y:90},W:{x:300,y:280},Share:{x:500,y:280},C:{x:100,y:280},T:{x:100,y:460}};
 const css=getComputedStyle(document.documentElement);const token=(name:string)=>css.getPropertyValue(name).trim();
 graph=cytoscape({container:document.getElementById('cy'),elements:[...variables.map(v=>({data:{id:v.id,label:v.short_name,full:semanticLabel(v.id,lang,v.label[lang])},position:positions[v.short_name]})),...links.map(l=>({data:{id:l.id,source:l.source,target:l.target,label:l.relation_type==='MODERATING'?tr('moderează','moderates'):tr('influențează','influences')}}))],style:[{selector:'node',style:{'label':'data(label)','width':64,'height':64,'background-color':token('--soft'),'border-width':2,'border-color':token('--accent'),'color':token('--text'),'font-family':css.fontFamily,'text-valign':'center','font-size':20}},{selector:'edge',style:{'curve-style':'bezier','target-arrow-shape':'triangle','line-color':token('--muted'),'target-arrow-color':token('--muted'),'label':'data(label)','color':token('--text'),'font-size':12,'text-margin-y':-12,'width':2}},{selector:':selected',style:{'border-color':token('--accent'),'line-color':token('--accent'),'target-arrow-color':token('--accent')}}],layout:{name:'preset',padding:50},minZoom:0.4,maxZoom:2,wheelSensitivity:0.2});
 const show=(id:string)=>{const v=variables.find(v=>v.id===id)!;document.getElementById('detail')!.innerHTML=variableDetail(v);(document.getElementById('variable') as HTMLSelectElement).value=id;graph!.$('node').unselect();graph!.getElementById(id).select();};
 graph.on('tap','node',e=>show(e.target.id()));
 graph.on('tap','edge',e=>{const l=links.find(l=>l.id===e.target.id())!;document.getElementById('detail')!.innerHTML=linkDetail(l);});
 document.getElementById('variable')!.onchange=e=>show((e.target as HTMLSelectElement).value);
 document.getElementById('fit')!.onclick=()=>graph!.fit(undefined,50);
 show(variables[0].id);
}
function evidenceStatus(status:string):string {
 return ({EXPERIMENTAL:tr('Experimental','Experimental'),META_ANALYTIC:tr('Meta-analiză','Meta-analysis'),CANDIDATE:tr('Mecanism candidat','Candidate mechanism'),REFERENCE_CANDIDATE:tr('Formă de referință, necalibrată','Uncalibrated reference form')}[status]??status);
}
function evidenceBadge(status:string):string {
 return `<span class="epistemic-status" data-status="${escape(status)}">${text(evidenceStatus(status))}</span>`;
}
function safeSource(url:string):string {try{return new URL(url).protocol==='https:'?escape(url):'#';}catch{return '#';}}
function linkDetail(l:Link){return `<p class="eyebrow">${tr('RELAȚIE ÎN REGISTRU','REGISTERED LINK')}</p><h3>${text(semanticLabel(l.source,lang,variables.find(v=>v.id===l.source)!.label[lang]))} → ${text(semanticLabel(l.target,lang,variables.find(v=>v.id===l.target)!.label[lang]))}</h3><dl class="link-data"><dt>${tr('Tip','Type')}</dt><dd>${text(l.relation_type)}</dd><dt>${tr('Polaritate','Polarity')}</dt><dd>${text(l.polarity)}</dd><dt>${tr('Dovezi despre fenomen','Evidence for the phenomenon')}</dt><dd>${evidenceBadge(l.phenomenon_evidence_status)}</dd><dt>${tr('Mecanismul exact din model','Exact model mechanism')}</dt><dd>${evidenceBadge(l.mechanism_evidence_status)}</dd><dt>${tr('Formă funcțională','Functional form')}</dt><dd>${evidenceBadge(l.functional_form_status)}</dd></dl><div class="evidence-assessment"><h4>${tr('Ce susține sursa','What the source supports')}</h4><p>${text(l.evidence_summary[lang])}</p><h4>${tr('Limita pentru acest model','Limit for this model')}</h4><p>${text(l.evidence_limitations[lang])}</p></div><h4>${tr('Surse și nivel de verificare','Sources and review scope')}</h4><ul class="sources">${l.evidence_refs.map(id=>{const ref=references.find(r=>r.id===id)!;return `<li><a class="citation-link" href="${safeSource(ref.url)}" target="_blank" rel="noopener noreferrer">${text(ref.citation)}</a><div><a href="${safeSource(ref.access_url)}" target="_blank" rel="noopener noreferrer">${tr('Pagina consultată ↗','Consulted source ↗')}</a></div><p class="meta">${ref.checked_on} · ${ref.review_scope==='ABSTRACT'?tr('Rezumat consultat','Abstract consulted'):ref.review_scope==='ABSTRACT_AND_SELECTED_SECTIONS'?tr('Rezumat și secțiuni selectate','Abstract and selected sections'):tr('Text integral','Full text')}</p></li>`;}).join('')}</ul><p class="note">${tr('Verificare bibliografică inițială, nu revizuire sistematică sau replicare independentă. Coeficienții nu au fost calibrați din aceste surse.','Initial bibliographic check, not a systematic review or independent replication. Coefficients were not calibrated from these sources.')}</p>`;}
function renderReference(){
 content(`<div class="section-heading"><div><h2>${tr('Registrul variabilelor și relațiilor','Variable and link registry')}</h2><p>${tr('Aceleași date ca în hartă, într-o formă navigabilă cu tastatura.','The same data as the graph, in a keyboard-accessible form.')}</p></div></div><div class="reference-grid">${variables.map(v=>`<article class="panel" data-registry-id="${v.id}">${variableDetail(v)}</article>`).join('')}</div><h2 class="section-title">${tr('Relații și statutul dovezilor','Links and evidence status')}</h2><div class="reference-grid">${links.map(l=>`<article class="panel" data-registry-id="${l.id}">${linkDetail(l)}</article>`).join('')}</div><details class="panel modules"><summary>${tr('Cele 20 de module conceptuale','The 20 conceptual modules')}</summary><p>${tr('Inventar conceptual, nu 20 de module executabile validate.','Conceptual inventory, not 20 validated executable modules.')}</p><ol>${modules.map(m=>`<li><code>${m.id}</code> ${text(semanticLabel(m.id,lang,m.label[lang]))}</li>`).join('')}</ol></details>`);
 if(registryFocus){
  const target=document.querySelector<HTMLElement>(`[data-registry-id="${CSS.escape(registryFocus)}"]`);
  if(target){target.tabIndex=-1;target.focus({preventScroll:true});target.scrollIntoView({block:'center'});}
 }
}
function renderProcess(){
 mountVisualOdd(document.getElementById('content')!,lang,oddProcesses,subsystems);
}
async function load<T>(name:string):Promise<T>{const r=await fetch(`./model/${name}.json`);if(!r.ok)throw new Error(`${name}: HTTP ${r.status}`);return r.json();}
async function init(){[variables,links,modules,references,oddProcesses,subsystems,m1Targets,m1Editorial,m1Presentation,m1Access,theoryIndex,theoryGlossary,validationTests]=await Promise.all([load<Variable[]>('variables'),load<Link[]>('links'),load<Module[]>('modules'),load<Reference[]>('references'),load<OddProcess[]>('processes'),load<Subsystem[]>('subsystems'),load<EmpiricalTarget[]>('empirical_targets'),load<M1EditorialData>('m1_editorial'),load<M1PresentationData>('m1_presentation'),load<M1AccessData>('m1_access'),load<TheoryChapter[]>('theory_index'),load<TheoryGlossaryEntry[]>('theory_glossary'),load<TheoryValidation[]>('validation_tests')]);assertSemanticCoverage([...variables.map(v=>v.id),...modules.map(m=>m.id),...references.map(r=>r.id),...validationTests.map(v=>v.id),...theoryIndex.map(c=>c.id),...theoryGlossary.map(g=>g.id)],links.map(l=>l.id));initializeWorkspaceSession();try{await migrateLegacyWorkspaceToIndexedDb(localStorage,validateWorkspaceRuntime);}catch(error){console.error('R3 IndexedDB migration failed; localStorage remains authoritative',error);}runs=(await load<{runs:Run[]}>('runs')).runs;planning=await load<PlanningData>('interventions');decisionUncertainty=await load<DecisionUncertaintyRegistry>('decision_uncertainty');explanations=await load<ExplanationData>('explanations');shell();}
matchMedia('(prefers-color-scheme: dark)').addEventListener('change',()=>{if(view==='structure'){stop();shell();}});
let understandingRouteRefresh=false;
const refreshUnderstandingRoute=()=>{
 if(understandingRouteRefresh)return;
 understandingRouteRefresh=true;
 queueMicrotask(()=>{
  understandingRouteRefresh=false;
  if(location.hash.startsWith('#understanding/')){stop();view='learning';shell();}
 });
};
addEventListener('hashchange',refreshUnderstandingRoute);
addEventListener('popstate',event=>{
 const state=event.state as {cemView?:string;cemId?:string|null;cemTime?:string|null}|null;
 if(state?.cemView&&isAppView(state.cemView)){
  stop();
  view=state.cemView;
  if(view==='reference')registryFocus=state.cemId??'';
  else if(state.cemId){selected=state.cemId;step=state.cemTime===null||state.cemTime===undefined?0:Number(state.cemTime);}
  shell();
  return;
 }
 refreshUnderstandingRoute();
});
init().catch(e=>{app.replaceChildren();const p=document.createElement('p');p.className='loading';p.textContent=`Nu se poate încărca modelul / Unable to load model: ${String(e)}`;app.append(p);});
