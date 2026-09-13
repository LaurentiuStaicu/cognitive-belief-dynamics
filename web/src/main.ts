import cytoscape, {type Core} from 'cytoscape';
import './style.css';
import './elementary.css';
import {mountLearning} from './learning';
import {mountPlanner,type PlanningData} from './planner';

type Lang = 'ro' | 'en';
type Variable = {id:string; short_name:string; label:Record<Lang,string>; definition:string; what_it_is_not:string; conceptual_module:string; ontology_type:string};
type Link = {id:string; source:string; target:string; relation_type:string; polarity:string; mechanism_evidence_status:string; functional_form_status:string; phenomenon_evidence_status:string; evidence_refs:string[]; evidence_summary:Record<Lang,string>; evidence_limitations:Record<Lang,string>};
type Frame = {time:number; familiarity:number; correction:number; reliability:number; belief:number; accuracy_weight:number; share_probability:number; share:boolean; events:{event_type:string}[]};
type Run = {id:string; seed:number; prior:number; parameters:Record<string,number>; frames:Frame[]};
type Reference = {id:string; citation:string; url:string; access_url:string; checked_on:string; review_scope:string};
type Module = {id:string;label:Record<Lang,string>};
let lang:Lang = 'ro';
let view = 'learning';
let planning:PlanningData;
let selected = 'correction';
let step = 0;
let playing:ReturnType<typeof setInterval> | undefined;
let graph:Core | undefined;
let variables:Variable[] = [];
let links:Link[] = [];
let modules:Module[] = [];
let runs:Run[] = [];
let references:Reference[] = [];
const app = document.getElementById('app')!;
const tr = (ro:string,en:string) => lang === 'ro' ? ro : en;
const num = (n:number) => n.toLocaleString(lang === 'ro' ? 'ro-RO' : 'en-GB', {minimumFractionDigits:3,maximumFractionDigits:3});
const escape = (s:string) => s.replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]!));
const text = (s:string) => escape(s);
const names:Record<string,[string,string]> = {
 repetition:['Repetiție','Repetition'],correction:['Corecție și uitare','Correction and decay'],source:['Feedback despre sursă','Source feedback'],accuracy:['Atenție la acuratețe','Accuracy cue']
};
const runName = (id:string) => names[id][lang==='ro'?0:1];
const definitions:Record<string,[string,string]> = {
 F:['Familiaritatea unei afirmații după expuneri repetate.','Nu măsoară adevărul, fiabilitatea sursei sau dovezile factuale.'],
 C:['Accesibilitatea curentă a informației corective despre afirmație.','Nu garantează corectarea convingerii.'],
 T:['Estimarea făcută de agent privind fiabilitatea sursei în sarcina curentă.','Nu este fiabilitatea reală a sursei.'],
 B:['Propensiunea latentă de a judeca afirmația drept adevărată la un moment dat.','Nu reprezintă cunoaștere, ideologie sau angajament identitar.'],
 W:['Ponderea contextuală acordată acurateții în decizia de distribuire.','Nu reprezintă raționalitatea generală sau activarea Sistemului 2.'],
 Nexp:['Numărul expunerilor agentului la o informație.','Nu este familiaritatea în sine.'],
 Share:['Acțiunea observată sau simulată de distribuire.','Nu echivalează cu o convingere sau cu aprobarea conținutului.']
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
 app.innerHTML=`<header class="topbar"><a class="brand" href="#" aria-label="Cognitive Epistemic Model"><span class="brand-mark">CE</span><span>Cognitive Epistemic Model<small>${tr('Laborator de explorare','Exploration lab')}</small></span></a><div class="top-actions"><span class="version">M0 · ALPHA</span><button id="language" aria-label="${tr('Switch to English','Schimbă în română')}">${lang==='ro'?'EN':'RO'}</button><a href="https://github.com/LaurentiuStaicu/cognitive-epistemic-model" target="_blank" rel="noopener">GitHub ↗</a></div></header>
 <div class="workspace"><div class="intro"><div><p class="eyebrow">${tr('FORMAREA CONVINGERILOR','BELIEF FORMATION')}</p><h1>${tr('Mecanisme, intervenții, priorități.','Mechanisms, interventions, priorities.')}</h1><p>${tr('Înțelege relațiile dintre factori și compară efectele măsurilor, separat și împreună.','Understand relationships between factors and compare measures, individually and together.')}</p></div><div class="scope"><strong>07</strong><span>${tr('variabile înregistrate','registered variables')}</span><strong>04</strong><span>${tr('scenarii de referință','reference scenarios')}</span></div></div>
 <nav class="views" aria-label="${tr('Vederile modelului','Model views')}">${[['learning',tr('1 · Înțelegere','1 · Understanding')],['planning',tr('2–3 · Priorități și acțiuni','2–3 · Priorities and actions')],['structure',tr('Hartă','Graph')],['runs',tr('Scenarii','Scenarios')],['process',tr('Proces','Process')],['reference',tr('Registru','Registry')]].map(([id,label])=>`<button data-view="${id}" aria-pressed="${view===id}">${label}</button>`).join('')}</nav>
 <main id="content"></main><footer><span>${tr('Model demonstrativ · coeficienți necalibrați','Demonstration model · uncalibrated coefficients')}</span><span>${tr('Nu estimează proporții Track A/B sau diagnostice individuale.','Does not estimate Track A/B prevalence or individual diagnoses.')}</span></footer></div>`;
 document.getElementById('language')!.onclick=()=>{stop();lang=lang==='ro'?'en':'ro';shell();};
 document.querySelectorAll<HTMLButtonElement>('[data-view]').forEach(b=>b.onclick=()=>{stop();view=b.dataset.view!;shell();});
 if(view==='learning') mountLearning(document.getElementById('content')!,lang,target=>{stop();const [next,id]=target.split(':');view=next;if(id){selected=id;step=0;}shell();document.getElementById('content')!.scrollIntoView({block:'start'});});
 if(view==='planning') mountPlanner(document.getElementById('content')!,planning,lang);
 if(view==='runs') renderRuns();
 if(view==='structure') renderStructure();
 if(view==='process') renderProcess();
 if(view==='reference') renderReference();
}
function content(html:string) { document.getElementById('content')!.innerHTML=html; }
function renderRuns() {
 content(`<div class="run-layout"><aside class="panel settings"><p class="eyebrow">${tr('SCENARIU','SCENARIO')}</p><label for="scenario">${tr('Ce mecanism explorăm?','Which mechanism?')}</label><select id="scenario">${runs.map(r=>`<option value="${r.id}" ${r.id===selected?'selected':''}>${runName(r.id)}</option>`).join('')}</select><p class="description">${scenarioDescription()}</p><div class="assumptions"><div><span>${tr('Convingere inițială','Initial belief')}</span><b>0.300</b></div><div><span>${tr('Agent / afirmație','Agent / claim')}</span><b>A1 / C1</b></div><div><span>Seed</span><b>7</b></div></div><p class="note">${tr('Redare a unei rulări precalculate de nucleul Python. Pașii sunt unități abstracte, nu ani sau zile.','Replay of a run precomputed by the Python core. Steps are abstract units, not years or days.')}</p><details><summary>${tr('Parametrii acestei rulări','Run parameters')}</summary><dl class="parameters">${Object.entries(run().parameters).map(([k,v])=>`<dt>${k}</dt><dd>${v}</dd>`).join('')}</dl></details><button class="download" id="download">${tr('Descarcă rularea JSON ↓','Download run JSON ↓')}</button></aside>
 <section class="panel experiment"><div class="section-heading"><div><p class="eyebrow">${tr('RULARE DE REFERINȚĂ','REFERENCE RUN')}</p><h2>${runName(selected)}</h2></div><span class="step-badge" id="stepBadge"></span></div><div class="metrics" id="metrics"></div><div class="chart-wrap" id="chart"></div><div class="legend"><span class="belief">${tr('Convingere','Belief')}</span><span class="sharing">${tr('Probabilitate de distribuire','Sharing probability')}</span><span class="corrective">${tr('Accesibilitatea corecției','Correction accessibility')}</span></div><div class="transport"><button class="primary" id="play"></button><button id="next">${tr('Pasul următor','Next step')}</button><button id="reset">↺ ${tr('De la început','Reset')}</button><label class="sr-only" for="timeline">${tr('Pasul rulării','Run step')}</label><input id="timeline" type="range" min="0" max="12" step="1" value="${step}"></div><div class="event-strip" id="events" role="status" aria-live="polite"></div><details class="results"><summary>${tr('Vezi valorile într-un tabel','View values in a table')}</summary><div class="table-scroll"><table><caption>${tr('Toți pașii rulării selectate','All steps of the selected run')}</caption><thead><tr><th>${tr('Pas','Step')}</th><th>B</th><th>P(${tr('distribuire','share')})</th><th>F</th><th>C</th><th>T</th><th>W</th><th>${tr('Distribuit','Shared')}</th></tr></thead><tbody>${run().frames.map(f=>`<tr><td>${f.time}</td>${[f.belief,f.share_probability,f.familiarity,f.correction,f.reliability,f.accuracy_weight].map(v=>`<td>${num(v)}</td>`).join('')}<td>${f.share?tr('Da','Yes'):tr('Nu','No')}</td></tr>`).join('')}</tbody></table></div></details></section></div>`);
 document.getElementById('scenario')!.onchange=e=>{stop();selected=(e.target as HTMLSelectElement).value;step=0;renderRuns();};
 document.getElementById('play')!.onclick=()=>{if(playing!==undefined){stop();updateFrame();return;} if(step===12)step=0;playing=setInterval(()=>{step++;if(step>=12)stop();updateFrame();},850);updateFrame();};
 document.getElementById('next')!.onclick=()=>{stop();step=Math.min(12,step+1);updateFrame();};
 document.getElementById('reset')!.onclick=()=>{stop();step=0;updateFrame();};
 document.getElementById('timeline')!.oninput=e=>{stop();step=Number((e.target as HTMLInputElement).value);updateFrame();};
 document.getElementById('download')!.onclick=()=>{const url=URL.createObjectURL(new Blob([JSON.stringify({model_version:'0.2.0a0',...run()},null,2)],{type:'application/json'}));const a=document.createElement('a');a.href=url;a.download=`cem-m0-${selected}.json`;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);};
 updateFrame();
}
function updateFrame(){
 const f=run().frames[step];
 document.getElementById('stepBadge')!.textContent=`${tr('Pas','Step')} ${step} / 12`;
 document.getElementById('metrics')!.innerHTML=[[tr('Convingere · B','Belief · B'),f.belief,'belief'],[tr('P(distribuire)','P(share)'),f.share_probability,'sharing'],[tr('Corecție · C','Correction · C'),f.correction,'corrective']].map(([label,value,color])=>`<div><span>${label}</span><strong class="${color}">${num(Number(value))}</strong></div>`).join('');
 const px=(i:number)=>50+i*55; const py=(v:number)=>242-v*212;
 const line=(key:keyof Frame,color:string,dash:string)=>`<polyline fill="none" stroke="${color}" stroke-width="3" stroke-dasharray="${dash}" points="${run().frames.slice(0,step+1).map(f=>`${px(f.time)},${py(Number(f[key]))}`).join(' ')}"/><circle cx="${px(step)}" cy="${py(Number(f[key]))}" r="5" fill="${color}"/>`;
 document.getElementById('chart')!.innerHTML=`<svg viewBox="0 0 748 290" role="img" aria-label="${tr('Evoluția convingerii, distribuirii și corecției; valorile exacte sunt în tabelul de mai jos.','Belief, sharing and correction trajectories; exact values are in the table below.')}"><title>${runName(selected)}</title>${[0,.25,.5,.75,1].map(v=>`<line x1="50" x2="710" y1="${py(v)}" y2="${py(v)}" stroke="var(--border)"/><text x="36" y="${py(v)+5}" text-anchor="end">${v}</text>`).join('')}${run().frames.map(f=>`<text x="${px(f.time)}" y="270" text-anchor="middle">${f.time}</text>`).join('')}<line x1="${px(step)}" x2="${px(step)}" y1="24" y2="242" stroke="var(--muted)" stroke-dasharray="4 5"/>${line('belief','var(--series-belief)','none')}${line('share_probability','var(--series-sharing)','8 4')}${line('correction','var(--series-correction)','2 4')}</svg>`;
 document.getElementById('events')!.textContent=`${tr('La acest pas','At this step')}: ${f.events.map(e=>eventName(e.event_type)).join(' → ')}. ${tr('Distribuire simulată','Simulated share')}: ${f.share?tr('da','yes'):tr('nu','no')}.`;
 document.getElementById('play')!.textContent=playing!==undefined?tr('Ⅱ Pauză','Ⅱ Pause'):tr('▶ Redă','▶ Play');
 (document.getElementById('timeline') as HTMLInputElement).value=String(step);
 (document.getElementById('next') as HTMLButtonElement).disabled=step===12;
}
function variableDetail(v:Variable){return `<p class="eyebrow">${text(v.short_name)} · ${text(v.ontology_type)}</p><h2>${text(v.label[lang])}</h2><p>${text(lang==='ro'?definitions[v.short_name][0]:v.definition)}</p><div class="boundary"><strong>${tr('Delimitare','Boundary')}</strong><p>${text(lang==='ro'?definitions[v.short_name][1]:v.what_it_is_not)}</p></div><p class="meta">${text(v.conceptual_module)} · ${text(modules.find(m=>m.id===v.conceptual_module)!.label[lang])}</p><code>${text(v.id)}</code>`;}
function renderStructure(){
 content(`<div class="section-heading"><div><h2>${tr('Structura înregistrată','Registered structure')}</h2><p>${tr('7 variabile și 3 relații documentate. Harta nu reprezintă încă toate dependențele din ecuații.','7 variables and 3 documented links. The map does not yet represent every dependency in the equations.')}</p></div><button id="fit">${tr('Încadrează harta','Fit graph')}</button></div><div class="graph-layout"><div class="panel graph-panel"><div id="cy" role="img" aria-label="${tr('Hartă interactivă; pentru navigare cu tastatura folosiți selectorul alăturat.','Interactive graph; use the adjacent selector for keyboard access.')}"></div><p class="graph-hint">${tr('Selectează un nod sau o relație pentru detalii. Trage pentru deplasare.','Select a node or link for details. Drag to pan.')}</p></div><aside class="panel detail-panel"><label for="variable">${tr('Inspectează o variabilă','Inspect a variable')}</label><select id="variable">${variables.map(v=>`<option value="${v.id}">${text(v.label[lang])}</option>`).join('')}</select><div id="detail"></div></aside></div>`);
 const positions:Record<string,{x:number;y:number}>={Nexp:{x:100,y:90},F:{x:300,y:90},B:{x:500,y:90},W:{x:300,y:280},Share:{x:500,y:280},C:{x:100,y:280},T:{x:100,y:460}};
 const css=getComputedStyle(document.documentElement);const token=(name:string)=>css.getPropertyValue(name).trim();
 graph=cytoscape({container:document.getElementById('cy'),elements:[...variables.map(v=>({data:{id:v.id,label:v.short_name,full:v.label[lang]},position:positions[v.short_name]})),...links.map(l=>({data:{id:l.id,source:l.source,target:l.target,label:l.relation_type==='MODERATING'?tr('moderează','moderates'):tr('influențează','influences')}}))],style:[{selector:'node',style:{'label':'data(label)','width':64,'height':64,'background-color':token('--soft'),'border-width':2,'border-color':token('--accent'),'color':token('--text'),'font-family':css.fontFamily,'text-valign':'center','font-size':20}},{selector:'edge',style:{'curve-style':'bezier','target-arrow-shape':'triangle','line-color':token('--muted'),'target-arrow-color':token('--muted'),'label':'data(label)','color':token('--text'),'font-size':12,'text-margin-y':-12,'width':2}},{selector:':selected',style:{'border-color':token('--accent'),'line-color':token('--accent'),'target-arrow-color':token('--accent')}}],layout:{name:'preset',padding:50},minZoom:0.4,maxZoom:2,wheelSensitivity:0.2});
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
function safeSource(url:string):string {try{return new URL(url).protocol==='https:'?escape(url):'#';}catch{return '#';}}
function linkDetail(l:Link){return `<p class="eyebrow">${tr('RELAȚIE ÎN REGISTRU','REGISTERED LINK')}</p><h3>${text(variables.find(v=>v.id===l.source)!.label[lang])} → ${text(variables.find(v=>v.id===l.target)!.label[lang])}</h3><dl class="link-data"><dt>${tr('Tip','Type')}</dt><dd>${text(l.relation_type)}</dd><dt>${tr('Polaritate','Polarity')}</dt><dd>${text(l.polarity)}</dd><dt>${tr('Dovezi despre fenomen','Evidence for the phenomenon')}</dt><dd>${text(evidenceStatus(l.phenomenon_evidence_status))}</dd><dt>${tr('Mecanismul exact din M0','Exact M0 mechanism')}</dt><dd>${text(evidenceStatus(l.mechanism_evidence_status))}</dd><dt>${tr('Formă funcțională','Functional form')}</dt><dd>${text(evidenceStatus(l.functional_form_status))}</dd></dl><div class="evidence-assessment"><h4>${tr('Ce susține sursa','What the source supports')}</h4><p>${text(l.evidence_summary[lang])}</p><h4>${tr('Limita pentru acest model','Limit for this model')}</h4><p>${text(l.evidence_limitations[lang])}</p></div><h4>${tr('Surse și nivel de verificare','Sources and review scope')}</h4><ul class="sources">${l.evidence_refs.map(id=>{const ref=references.find(r=>r.id===id)!;return `<li><a class="citation-link" href="${safeSource(ref.url)}" target="_blank" rel="noopener noreferrer">${text(ref.citation)}</a><div><a href="${safeSource(ref.access_url)}" target="_blank" rel="noopener noreferrer">${tr('Pagina consultată ↗','Consulted source ↗')}</a></div><p class="meta">${ref.checked_on} · ${ref.review_scope==='ABSTRACT'?tr('Rezumat consultat','Abstract consulted'):ref.review_scope==='ABSTRACT_AND_SELECTED_SECTIONS'?tr('Rezumat și secțiuni selectate','Abstract and selected sections'):tr('Text integral','Full text')}</p></li>`;}).join('')}</ul><p class="note">${tr('Verificare bibliografică inițială, nu revizuire sistematică sau replicare independentă. Coeficienții nu au fost calibrați din aceste surse.','Initial bibliographic check, not a systematic review or independent replication. Coefficients were not calibrated from these sources.')}</p>`;}
function renderReference(){
 content(`<div class="section-heading"><div><h2>${tr('Registrul variabilelor și relațiilor','Variable and link registry')}</h2><p>${tr('Aceleași date ca în hartă, într-o formă navigabilă cu tastatura.','The same data as the graph, in a keyboard-accessible form.')}</p></div></div><div class="reference-grid">${variables.map(v=>`<article class="panel">${variableDetail(v)}</article>`).join('')}</div><h2 class="section-title">${tr('Relații și statutul dovezilor','Links and evidence status')}</h2><div class="reference-grid">${links.map(l=>`<article class="panel">${linkDetail(l)}</article>`).join('')}</div><details class="panel modules"><summary>${tr('Cele 20 de module conceptuale','The 20 conceptual modules')}</summary><p>${tr('Inventar conceptual, nu 20 de module executabile validate.','Conceptual inventory, not 20 validated executable modules.')}</p><ol>${modules.map(m=>`<li><code>${m.id}</code> ${text(m.label[lang])}</li>`).join('')}</ol></details>`);
}
function renderProcess(){
 const steps=[
 [tr('Entități și stare','Entities and state'),tr('Un agent, o afirmație și o sursă. Familiaritatea, corecția și fiabilitatea estimată persistă între evenimente.','One agent, one claim and one source. Familiarity, correction accessibility and estimated reliability persist between events.')],
 [tr('Programarea evenimentelor','Event scheduling'),tr('Evenimentele se ordonează după timp. La același moment, se păstrează ordinea de intrare.','Events are sorted by time. Input order is preserved for simultaneous events.')],
 [tr('Actualizarea stării','State update'),tr('Expunerea crește familiaritatea; corecția adaugă context corectiv; feedbackul schimbă estimarea sursei. Accesibilitatea corecției se diminuează cu timpul.','Exposure increases familiarity; correction encodes corrective context; feedback updates source estimates. Correction accessibility decays with time.')],
 [tr('Formarea judecății','Judgment formation'),tr('Convingerea inițială, familiaritatea, semnalul de evidență ponderat de sursă și corecția intră într-o transformare logistică. Adevărul din lumea simulată nu intră direct în ecuație.','Prior belief, familiarity, source-weighted evidence and correction enter a logistic transform. Simulated ground truth is not passed directly to this equation.')],
 [tr('Decizie și jurnal','Decision and log'),tr('Ponderea acurateții și recompensa contextuală determină probabilitatea de distribuire. O extragere aleatoare generează acțiunea, iar jurnalul păstrează rezultatul.','Accuracy weight and contextual reward determine sharing probability. A random draw generates the action, and the log records the outcome.')]
 ];
 content(`<div class="section-heading"><div><h2>${tr('Procesul executabil M0','The executable M0 process')}</h2><p>${tr('O vedere de ansamblu a procesului, inspirată de ODD. Nu reprezintă încă o specificație ODD completă.','An ODD-inspired process overview. This is not yet a complete ODD specification.')}</p></div></div><div class="process-layout"><ol class="process-list">${steps.map(([title,body],i)=>`<li><span class="process-number">0${i+1}</span><div><h3>${title}</h3><p>${body}</p></div></li>`).join('')}</ol><aside class="panel interpretive"><p class="eyebrow">${tr('NIVELURI DE INTERPRETARE','LEVELS OF INTERPRETATION')}</p><h2>${tr('Ce nu codifică M0','What M0 does not encode')}</h2><h3>Track A / Track B</h3><p>${tr('Descrieri conceptuale ale procesării reactive și adaptive. Nu sunt clase fixe de persoane sau stări impuse agenților.','Conceptual descriptions of reactive and adaptive processing. They are not fixed classes of people or hard-coded agent states.')}</p><h3>${tr('Extensia jungiană','Jungian extension')}</h3><p>${tr('Individuația și Axa Eu–Sine rămân un nivel interpretativ distinct. Creația poate fi o consecință posibilă, nu un rezultat garantat sau o variabilă calculată de M0.','Individuation and the ego–Self axis remain a separate interpretive layer. Creativity is a possible consequence, not a guaranteed result or a variable computed by M0.')}</p><div class="boundary"><strong>${tr('Limita inferenței','Inference boundary')}</strong><p>${tr('Reproducerea unui tipar nu demonstrează un mecanism psihologic unic. Testele de software nu constituie validare empirică.','Reproducing a pattern does not establish a unique psychological mechanism. Software tests do not constitute empirical validation.')}</p></div></aside></div>`);
}
async function load<T>(name:string):Promise<T>{const r=await fetch(`./model/${name}.json`);if(!r.ok)throw new Error(`${name}: HTTP ${r.status}`);return r.json();}
async function init(){[variables,links,modules,references]=await Promise.all([load<Variable[]>('variables'),load<Link[]>('links'),load<Module[]>('modules'),load<Reference[]>('references')]);runs=(await load<{runs:Run[]}>('runs')).runs;planning=await load<PlanningData>('interventions');shell();}
matchMedia('(prefers-color-scheme: dark)').addEventListener('change',()=>{if(view==='structure'){stop();shell();}});
init().catch(e=>{app.replaceChildren();const p=document.createElement('p');p.className='loading';p.textContent=`Nu se poate încărca modelul / Unable to load model: ${String(e)}`;app.append(p);});
