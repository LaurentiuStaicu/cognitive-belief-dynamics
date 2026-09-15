type Lang='ro'|'en';

export type OddProcess={
 id:string;
 stage:'initialisation'|'submodel'|'observation'|'scale';
 label:Record<Lang,string>;
 description:Record<Lang,string>;
 code_ref:string;
 status:'implemented_m0'|'candidate'|'future';
};

export type Subsystem={
 id:string;
 label:Record<Lang,string>;
 description:Record<Lang,string>;
 implementation_status:'active'|'partial'|'planned_0_4'|'future';
};

export function mountVisualOdd(host:HTMLElement,lang:Lang,processes:OddProcess[],subsystems:Subsystem[]){
 const t=(ro:string,en:string)=>lang==='ro'?ro:en;
 const groups:[OddProcess['stage'],string,string][]=[
  ['initialisation',t('Inițializare','Initialisation'),t('Ce există și cu ce stare pornește rularea.','What exists and what state the run starts with.')],
  ['submodel',t('Submodele / procese','Submodels / processes'),t('Ordinea operațiilor care actualizează starea și produc decizia.','The operations that update state and produce the decision.')],
  ['observation',t('Observație','Observation'),t('Ce este înregistrat și ce patternuri sunt testate.','What is recorded and which patterns are tested.')],
  ['scale',t('Scări','Scales'),t('Rezoluția temporală și nivelurile entităților din M0.','Temporal resolution and entity levels in M0.')]
 ];
 const status=(s:Subsystem['implementation_status'])=>({
  active:t('activ','active'),
  partial:t('parțial','partial'),
  planned_0_4:t('vizat în 0.4','targeted in 0.4'),
  future:t('viitor','future')
 }[s]);
 host.innerHTML=`<div class="section-heading"><div><h2>${t('Visual ODD · cum rulează modelul','Visual ODD · how the model runs')}</h2><p>${t('Această vedere este generată din registry-urile modelului. Completează harta de sistem: harta arată dependențele, iar Visual ODD arată ciclul simulatorului.','This view is generated from model registries. It complements the system map: the map shows dependencies, while Visual ODD shows the simulator cycle.')}</p></div></div>
 <div class="vodd-boundary boundary"><strong>${t('Statut','Status')}</strong><p>${t('M0 este un model demonstrativ necalibrat. Visual ODD documentează implementarea; nu validează mecanismele psihologice și nu transformă pașii abstracți în timp calendaristic.','M0 is an uncalibrated demonstration model. Visual ODD documents implementation; it does not validate psychological mechanisms or turn abstract steps into calendar time.')}</p></div>
 <div class="vodd-flow" aria-label="${t('Ciclul Visual ODD','Visual ODD cycle')}">${groups.map(([key,title,desc],i)=>`<section class="panel vodd-stage" data-odd-stage="${key}"><div class="vodd-stage-number">${String(i+1).padStart(2,'0')}</div><h3>${title}</h3><p class="note">${desc}</p><ol>${processes.filter(p=>p.stage===key).map(p=>`<li><details><summary>${p.label[lang]}</summary><p>${p.description[lang]}</p><p class="meta"><code>${p.id}</code> · <code>${p.code_ref}</code></p></details></li>`).join('')}</ol></section>`).join('')}</div>
 <section class="panel vodd-subsystems"><div class="section-heading"><div><h2>${t('Opt subsisteme executabile','Eight executable subsystems')}</h2><p>${t('Cele 20 de module conceptuale sunt harta științifică; nu devin 20 de motoare software independente.','The 20 conceptual modules are the scientific map; they do not become 20 independent software engines.')}</p></div></div><div class="subsystem-grid">${subsystems.map(s=>`<article><div><h3>${s.label[lang]}</h3><span class="planner-badge">${status(s.implementation_status)}</span></div><p>${s.description[lang]}</p><code>${s.id}</code></article>`).join('')}</div></section>
 <section class="panel vodd-extension"><h2>${t('Contractul științific Alpha 0.4','Alpha 0.4 scientific contract')}</h2><p>${t('World-model construction (MOD.14), heuristic policy selection (MOD.15) și editorial media (MOD.16) sunt extensiile științifice vizate. Ele nu primesc parametri numerici doar pentru a completa diagrama. Fiecare extensie executabilă trebuie să aibă fenomen observabil, operaționalizare, predicție diferențială și criteriu de respingere, apoi să păstreze patternurile M0.','World-model construction (MOD.14), heuristic policy selection (MOD.15), and editorial media (MOD.16) are the targeted scientific extensions. They do not receive numerical parameters merely to complete the diagram. Each executable extension must have an observable phenomenon, operationalisation, a differential prediction, and a rejection criterion, then retain the M0 patterns.')}</p></section>`;
}
