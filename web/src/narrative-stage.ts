type Lang='ro'|'en';

export type NarrativeFrame={
 time:number;
 familiarity:number;
 correction:number;
 reliability:number;
 belief:number;
 accuracy_weight:number;
 share_probability:number;
 share:boolean;
 events:{event_type:string}[];
};
export type NarrativeRun={id:string;frames:NarrativeFrame[]};

type FrameKey='familiarity'|'correction'|'reliability'|'belief'|'accuracy_weight'|'share_probability';
type Inspector={kind:'mechanism';id:string}|{kind:'variable';id:string};
type State={mechanismId:string;step:number;inspector:Inspector};
export type NarrativeController={setMechanism:(id:string,step?:number)=>void;setVariable:(id:string)=>void;selectStep:(step:number)=>void};

const defaultStep:Record<string,number>={repetition:4,correction:5,source:8,accuracy:5};

export function mountNarrativeStage(
 host:HTMLElement,
 lang:Lang,
 runs:NarrativeRun[],
 openRun:(id:string,step:number)=>void,
 openRegistry:()=>void
):NarrativeController{
 const t=(ro:string,en:string)=>lang==='ro'?ro:en;
 const runFor=(id:string)=>runs.find(r=>r.id===id)??runs[0];
 let state:State={mechanismId:'repetition',step:defaultStep.repetition,inspector:{kind:'mechanism',id:'repetition'}};

 const variableMeta=()=>{
  const m:Record<string,{label:string;definition:string;not:string;formula?:string;key?:FrameKey}>={
   Nexp:{label:t('Expuneri','Exposures'),definition:t('Numărul întâlnirilor cu afirmația până la pasul selectat.','Number of encounters with the claim up to the selected step.'),not:t('Nu este familiaritatea însăși și nu măsoară timpul scurs.','It is not familiarity itself and does not measure elapsed time.')},
   F:{label:t('Familiaritate','Familiarity'),definition:t('Starea de familiaritate acumulată prin expuneri în M0.','The familiarity state accumulated through exposures in M0.'),not:t('Nu este adevăr, dovadă sau fiabilitate a sursei.','It is not truth, evidence, or source reliability.'),formula:'F′ = F + αf × (1 − F)',key:'familiarity'},
   C:{label:t('Accesibilitatea corecției','Correction accessibility'),definition:t('Cât de disponibil rămâne contextul corectiv în pasul selectat.','How available corrective context remains at the selected step.'),not:t('Nu indică singură direcția corecției și nu garantează schimbarea convingerii.','It does not by itself encode correction direction or guarantee belief change.'),formula:'C(t + Δt) = C(t) × exp(−λc × Δt)',key:'correction'},
   T:{label:t('Fiabilitatea estimată a sursei','Estimated source reliability'),definition:t('Estimarea internă a agentului privind sursa în sarcina curentă.','The agent’s internal estimate of the source in the current task.'),not:t('Nu este o măsurare independentă a fiabilității reale.','It is not an independent measurement of actual reliability.'),formula:'T′ = T + αt × (feedback − T)',key:'reliability'},
   B:{label:t('Convingere','Belief'),definition:t('Propensiunea modelată de a judeca afirmația drept adevărată.','Modeled propensity to judge the claim as true.'),not:t('Nu reprezintă cunoaștere, ideologie sau identitate.','It does not represent knowledge, ideology, or identity.'),key:'belief'},
   W:{label:t('Ponderea acurateții','Accuracy weight'),definition:t('Câtă pondere primește judecata de adevăr în decizia de distribuire.','How much weight truth judgment receives in the sharing decision.'),not:t('Nu reprezintă raționalitatea generală sau activarea Sistemului 2.','It does not represent general rationality or System 2 activation.'),key:'accuracy_weight'},
   P:{label:t('Probabilitatea de distribuire','Sharing probability'),definition:t('Probabilitatea calculată pentru acțiunea de distribuire la pasul selectat.','Calculated probability of the sharing action at the selected step.'),not:t('Nu este acțiunea Share și nu este o frecvență observată în populație.','It is not the Share action and is not an observed population frequency.'),formula:'P(share) = logistic[bias + W × (2B − 1) + βreward × (1 − W) × reward]',key:'share_probability'},
   Share:{label:t('Distribuire','Sharing'),definition:t('Rezultatul stochastic înregistrat pentru rularea precalculată.','Recorded stochastic outcome for the precomputed run.'),not:t('Nu echivalează cu aprobarea conținutului sau cu nivelul convingerii.','It is not equivalent to endorsement or belief level.')}
  };
  return m;
 };

 const driver:Record<string,{key:FrameKey;symbol:string;label:string}>={
  repetition:{key:'familiarity',symbol:'F',label:t('Familiaritate','Familiarity')},
  correction:{key:'correction',symbol:'C',label:t('Accesibilitatea corecției','Correction accessibility')},
  source:{key:'reliability',symbol:'T',label:t('Fiabilitatea estimată','Estimated reliability')},
  accuracy:{key:'accuracy_weight',symbol:'W',label:t('Ponderea acurateții','Accuracy weight')}
 };
 const mechanismTitle:Record<string,string>={
  repetition:t('Repetiție și familiaritate','Repetition and familiarity'),
  correction:t('Corecție și diminuarea accesibilității','Correction and accessibility decay'),
  source:t('Sursă și interpretarea evidenței','Source and evidence interpretation'),
  accuracy:t('Acuratețe, recompensă și decizie','Accuracy, reward and decision')
 };
 const phases:Record<string,{from:number;to:number;label:string}[]>={
  repetition:[{from:1,to:4,label:t('Expuneri repetate','Repeated exposures')},{from:5,to:12,label:t('După expuneri','After exposures')}],
  correction:[{from:1,to:4,label:t('Expuneri repetate','Repeated exposures')},{from:5,to:5,label:t('Corecție','Correction')},{from:6,to:12,label:t('Diminuarea accesibilității','Accessibility decay')}],
  source:[{from:1,to:8,label:t('Feedback repetat despre sursă','Repeated source feedback')},{from:9,to:12,label:t('După feedback','After feedback')}],
  accuracy:[{from:1,to:4,label:t('Înainte de indiciu','Before cue')},{from:5,to:12,label:t('Indiciu de acuratețe activ','Accuracy cue active')}]
 };

 const specialEvent=(frame:NarrativeFrame)=>frame.events.find(e=>e.event_type!=='DecisionEvent')?.event_type;
 const eventLabel=(event?:string)=>event?({
  ExposureEvent:t('expunere','exposure'),
  CorrectionEvent:t('corecție','correction'),
  SourceFeedbackEvent:t('feedback despre sursă','source feedback'),
  AccuracyCueEvent:t('indiciu de acuratețe','accuracy cue')
 } as Record<string,string>)[event]??event:t('fără eveniment extern','no external event');

 const countExposures=(run:NarrativeRun,step:number)=>run.frames.slice(0,step+1).reduce((n,f)=>n+f.events.filter(e=>e.event_type==='ExposureEvent').length,0);
 const variableValue=(id:string,run:NarrativeRun,step:number)=>{
  const f=run.frames[step];
  if(id==='Nexp')return String(countExposures(run,step));
  if(id==='Share')return f.share?t('da','yes'):t('nu','no');
  const meta=variableMeta()[id];
  if(meta?.key)return Number(f[meta.key]).toLocaleString(lang==='ro'?'ro-RO':'en-GB',{minimumFractionDigits:3,maximumFractionDigits:3});
  return '—';
 };

 const chart=(run:NarrativeRun)=>{
  const d=driver[state.mechanismId]??driver.repetition;
  const width=680,height=255,left=42,right=18,top=20,bottom=38;
  const innerW=width-left-right,innerH=height-top-bottom;
  const x=(i:number)=>left+(run.frames.length<=1?0:i*innerW/(run.frames.length-1));
  const y=(v:number)=>top+(1-v)*innerH;
  const points=(key:FrameKey)=>run.frames.map((f,i)=>`${x(i)},${y(Number(f[key]))}`).join(' ');
  const current=run.frames[state.step];
  const line=(key:FrameKey,klass:string,dash='')=>`<polyline class="${klass}" fill="none" stroke-width="3" stroke-dasharray="${dash}" points="${points(key)}"/><circle class="${klass}" cx="${x(state.step)}" cy="${y(Number(current[key]))}" r="5"/>`;
  return `<svg viewBox="0 0 ${width} ${height}" role="img" aria-labelledby="narrativeChartTitle narrativeChartDesc"><title id="narrativeChartTitle">${mechanismTitle[state.mechanismId]}</title><desc id="narrativeChartDesc">${t('Traiectoriile complete ale variabilei mecanismului, convingerii și probabilității de distribuire. Valorile exacte ale pasului selectat sunt afișate sub grafic.','Full trajectories of the mechanism variable, belief, and sharing probability. Exact values for the selected step are shown below the chart.')}</desc>${[0,.25,.5,.75,1].map(v=>`<line class="narrative-gridline" x1="${left}" x2="${width-right}" y1="${y(v)}" y2="${y(v)}"/><text x="${left-7}" y="${y(v)+4}" text-anchor="end">${v}</text>`).join('')}<line class="narrative-playhead" x1="${x(state.step)}" x2="${x(state.step)}" y1="${top}" y2="${height-bottom}"/>${line(d.key,'narrative-driver')}${line('belief','narrative-belief')}${line('share_probability','narrative-sharing','8 4')}${run.frames.map((f,i)=>`<text x="${x(i)}" y="${height-12}" text-anchor="middle">${f.time}</text>`).join('')}</svg>`;
 };

 const bind=()=>{
  host.querySelectorAll<HTMLButtonElement>('[data-narrative-step]').forEach(b=>b.onclick=()=>selectStep(Number(b.dataset.narrativeStep)));
  host.querySelectorAll<HTMLButtonElement>('[data-narrative-variable]').forEach(b=>b.onclick=()=>setVariable(b.dataset.narrativeVariable!));
  host.querySelector<HTMLButtonElement>('#narrativeBack')?.addEventListener('click',()=>{state.inspector={kind:'mechanism',id:state.mechanismId};render();});
  host.querySelector<HTMLButtonElement>('#narrativeOpenRun')?.addEventListener('click',()=>openRun(state.mechanismId,state.step));
  host.querySelector<HTMLButtonElement>('#narrativeRegistry')?.addEventListener('click',openRegistry);
 };

 const renderMechanism=()=>{
  const run=runFor(state.mechanismId);
  state.step=Math.max(0,Math.min(state.step,run.frames.length-1));
  const d=driver[state.mechanismId]??driver.repetition;
  const f=run.frames[state.step];
  const special=specialEvent(f);
  host.innerHTML=`<div class="narrative-stage-heading"><div><p class="eyebrow">${t('SCENĂ DINAMICĂ','DYNAMIC STAGE')}</p><h3>${mechanismTitle[state.mechanismId]}</h3></div><button id="narrativeOpenRun">${t('Deschide scenariul complet','Open full scenario')}</button></div><p class="note">${t('Această scenă citește rularea Python precalculată. Selectarea unui pas schimbă numai explicația locală; nu recalculează modelul.','This stage reads the precomputed Python run. Selecting a step changes only the local explanation; it does not recalculate the model.')}</p><div class="narrative-chart">${chart(run)}</div><div class="narrative-legend"><button data-narrative-variable="${d.symbol}" class="driver"><span></span>${d.symbol} · ${d.label}</button><button data-narrative-variable="B" class="belief"><span></span>B · ${t('Convingere','Belief')}</button><button data-narrative-variable="P" class="sharing"><span></span>P · ${t('Distribuire','Sharing')}</button></div><div class="narrative-phases" style="grid-template-columns:repeat(${run.frames.length},minmax(0,1fr))">${phases[state.mechanismId].map(p=>`<span style="grid-column:${p.from+1}/${p.to+2}">${p.label}</span>`).join('')}</div><div class="narrative-timeline" role="group" aria-label="${t('Selectează pasul explicat','Select the explained step')}">${run.frames.map((frame,i)=>{const e=specialEvent(frame);return `<button data-narrative-step="${i}" aria-current="${i===state.step?'step':'false'}" class="${e?'has-event':''}" aria-label="${t('Pas','Step')} ${i}${e?' · '+eventLabel(e):''}">${i}</button>`;}).join('')}</div><dl class="narrative-values"><div><dt>${d.symbol}</dt><dd>${variableValue(d.symbol,run,state.step)}</dd></div><div><dt>B</dt><dd>${variableValue('B',run,state.step)}</dd></div><div><dt>P</dt><dd>${variableValue('P',run,state.step)}</dd></div></dl><p class="narrative-event"><strong>${t('Pasul','Step')} ${state.step}:</strong> ${eventLabel(special)}. ${t('Distribuire simulată','Simulated share')}: ${f.share?t('da','yes'):t('nu','no')}.</p><div class="boundary"><strong>${t('Delimitare','Boundary')}</strong><p>${t('Fazele și adnotările organizează o rulare demonstrativă; nu transformă pașii în timp calendaristic și nu certifică un mecanism psihologic unic.','Phases and annotations organize a demonstration run; they do not turn steps into calendar time or establish a unique psychological mechanism.')}</p></div>`;
  bind();
 };

 const renderVariable=(id:string)=>{
  const run=runFor(state.mechanismId);
  const meta=variableMeta()[id]??variableMeta().B;
  host.innerHTML=`<div class="narrative-stage-heading"><div><p class="eyebrow">${t('INSPECTOR CONTEXTUAL','CONTEXTUAL INSPECTOR')}</p><h3><span class="factor-symbol">${id}</span> ${meta.label}</h3></div><button id="narrativeBack">${t('Înapoi la mecanism','Back to mechanism')}</button></div><p>${meta.definition}</p><div class="narrative-current-value"><span>${t('Valoare la pasul','Value at step')} ${state.step}</span><strong>${variableValue(id,run,state.step)}</strong></div>${meta.formula?`<p class="equation">${meta.formula}</p>`:''}<div class="boundary"><strong>${t('Ce nu reprezintă','What this is not')}</strong><p>${meta.not}</p></div><p class="note">${t('Deschiderea acestui inspector nu modifică valoarea variabilei și nu schimbă rularea.','Opening this inspector does not modify the variable value or change the run.')}</p><div class="narrative-inspector-actions"><button id="narrativeRegistry">${t('Consultă Registrul de dovezi','Open Evidence Registry')}</button><button id="narrativeOpenRun">${t('Vezi pasul în scenariul complet','View step in full scenario')}</button></div>`;
  bind();
 };

 const render=()=>state.inspector.kind==='variable'?renderVariable(state.inspector.id):renderMechanism();

 const selectStep=(step:number)=>{
  const run=runFor(state.mechanismId);
  state.step=Math.max(0,Math.min(step,run.frames.length-1));
  render();
 };
 const setMechanism=(id:string,step=defaultStep[id]??0)=>{
  state={mechanismId:id,step,inspector:{kind:'mechanism',id}};
  render();
 };
 const setVariable=(id:string)=>{
  state.inspector={kind:'variable',id};
  render();
 };

 render();
 return {setMechanism,setVariable,selectStep};
}
