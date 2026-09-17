type Lang='ro'|'en';
type EpistemicLevel='EMPIRICAL'|'EXECUTABLE'|'CONCEPTUAL'|'INTERPRETIVE';

type Bilingual={en:string;ro:string};
type WorldVariable={id:string;short_name:string;label:Bilingual;status:EpistemicLevel[];definition:string;not_equivalent_to:string[];range?:[number|null,number|null]};
type WorldMechanism={id:string;label:Bilingual;status:EpistemicLevel[];description:string};
type WorldRelation={id:string;source:string;target:string;kind:string;sign:string;status:EpistemicLevel[]};
type WorldReference={id:string;citation:string;doi:string;url:string;supports:string[]};
type WorldContract={
 contract_id:string;
 module_id:string;
 title:Bilingual;
 purpose:Bilingual;
 scope_boundary:Bilingual;
 epistemic_levels:{level:EpistemicLevel;claims:string[]}[];
 variables:WorldVariable[];
 mechanisms:WorldMechanism[];
 relations:WorldRelation[];
 temporal_model:{unit:string;sequence:string[];warning:string};
 executable_specification:{posterior_formula:string;odds_formula:string;uncertainty_formula:string;preconditions:string[];failure_mode:string};
 cross_links:{target:string;role:string}[];
 falsification_and_tests:{claim:string;weakening_condition:string;scope:string}[];
 limitations:string[];
 references:WorldReference[];
};

const esc=(value:string)=>value.replace(/[&<>"']/g,char=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]!));
const clamp=(value:number,min:number,max:number)=>Math.min(max,Math.max(min,value));

function posterior(prior:number,lr:number){
 if(!Number.isFinite(prior)||prior<0||prior>1)throw new Error('prior');
 if(!Number.isFinite(lr)||lr<=0)throw new Error('lr');
 if(prior===0||prior===1)return prior;
 return (prior*lr)/(prior*lr+(1-prior));
}
function entropy(p:number){
 if(p===0||p===1)return 0;
 return -(p*Math.log2(p)+(1-p)*Math.log2(1-p));
}

const levelExplanation=(level:EpistemicLevel,lang:Lang)=>({
 EMPIRICAL:lang==='ro'?'Fenomen susținut de studii; forma și magnitudinea depind de sarcină.':'Phenomenon supported by studies; form and magnitude remain task-dependent.',
 EXECUTABLE:lang==='ro'?'Calcul implementat și testabil în software; nu implică automat validitate descriptivă populațională.':'Implemented and software-testable computation; it does not automatically imply population-level descriptive validity.',
 CONCEPTUAL:lang==='ro'?'Mecanism organizatoric fără ecuație universală justificată.':'Organizing mechanism without a justified universal equation.',
 INTERPRETIVE:lang==='ro'?'Cadru explicativ util, păstrat separat de afirmațiile executabile.':'Useful explanatory frame kept separate from executable claims.'
}[level]);

export async function mountWorldModel(host:HTMLElement,lang:Lang,navigate:(target:string)=>void){
 const t=(ro:string,en:string)=>lang==='ro'?ro:en;
 const response=await fetch('model/world_model_v1.json');
 if(!response.ok)throw new Error(`MOD.14 contract HTTP ${response.status}`);
 const contract=await response.json() as WorldContract;
 const mechanismById=new Map(contract.mechanisms.map(item=>[item.id,item]));
 const variableById=new Map(contract.variables.map(item=>[item.id,item]));
 const label=(id:string)=>{
  const item=mechanismById.get(id)??variableById.get(id);
  return item?item.label[lang]:id;
 };
 const statusBadges=(levels:EpistemicLevel[])=>levels.map(level=>`<span class="epistemic-status wm-status" data-status="${level}" title="${esc(levelExplanation(level,lang))}">${level}</span>`).join('');
 const mechanisms=contract.mechanisms.map((item,index)=>`<article class="wm-node" data-wm-mechanism="${esc(item.id)}"><span class="wm-step">${index+1}</span><div><strong>${esc(item.label[lang])}</strong><p>${esc(item.description)}</p><div class="wm-status-row">${statusBadges(item.status)}</div></div></article>`).join('<span class="wm-arrow" aria-hidden="true">→</span>');
 const relations=contract.relations.map(item=>`<tr><td>${esc(label(item.source))}</td><td>${esc(item.kind)}</td><td>${esc(label(item.target))}</td><td>${esc(item.sign)}</td><td>${statusBadges(item.status)}</td></tr>`).join('');
 const refs=contract.references.map(item=>`<li><a href="${esc(item.url)}" target="_blank" rel="noreferrer">${esc(item.citation)}</a></li>`).join('');
 const limits=contract.limitations.map(item=>`<li>${esc(item)}</li>`).join('');
 const crossLinks=contract.cross_links.map(item=>`<button type="button" class="wm-crosslink" data-semantic-id="${esc(item.target)}"><strong>${esc(item.target)}</strong><span>${esc(item.role)}</span></button>`).join('');
 const evidenceLevels=contract.epistemic_levels.map(item=>`<article><div class="wm-level-title">${statusBadges([item.level])}</div><ul>${item.claims.map(claim=>`<li>${esc(claim)}</li>`).join('')}</ul></article>`).join('');
 const falsification=contract.falsification_and_tests.map(item=>`<article><strong>${esc(item.claim)}</strong><p>${esc(item.weakening_condition)}</p><small>${esc(item.scope)}</small></article>`).join('');

 host.innerHTML=`<section class="world-model-shell" data-world-model-contract="${esc(contract.contract_id)}" aria-labelledby="worldModelTitle">
  <div class="wm-heading"><div><p class="eyebrow">MOD.14 · WORLD-MODEL CONSTRUCTION</p><h2 id="worldModelTitle">${esc(contract.title[lang])}</h2><p>${esc(contract.purpose[lang])}</p></div><button type="button" data-wm-action="registry">${t('Registru științific','Scientific registry')}</button></div>
  <div class="wm-boundary"><strong>${t('Limita centrală','Central boundary')}</strong><p>${esc(contract.scope_boundary[lang])}</p></div>

  <div class="wm-grid">
   <section class="panel wm-panel wm-mechanism-panel" aria-labelledby="wmMechanismTitle">
    <p class="eyebrow">${t('VIZUALIZAREA MECANISMULUI','MECHANISM VISUALIZATION')}</p><h3 id="wmMechanismTitle">${t('Cum se construiește și se revizuiește reprezentarea','How the representation is constructed and revised')}</h3>
    <p>${t('Traseul este conceptual acolo unde nu există o punte de măsurare validată. Numai actualizarea probabilistică și incertitudinea derivată sunt executabile.','The path remains conceptual where no validated measurement bridge exists. Only the probabilistic update and derived uncertainty are executable.')}</p>
    <div class="wm-flow">${mechanisms}</div>
    <details class="wm-relations"><summary>${t('Vezi relațiile, semnele și statutul','See relations, signs and status')}</summary><div class="table-scroll"><table><thead><tr><th>${t('Sursă','Source')}</th><th>${t('Relație','Relation')}</th><th>${t('Țintă','Target')}</th><th>${t('Semn','Sign')}</th><th>${t('Statut','Status')}</th></tr></thead><tbody>${relations}</tbody></table></div></details>
   </section>

   <section class="panel wm-panel wm-theory-panel" aria-labelledby="wmTheoryTitle">
    <p class="eyebrow">THEORY / LEARN</p><h3 id="wmTheoryTitle">${t('Patru niveluri epistemice, fără amestecarea lor','Four epistemic levels, kept separate')}</h3>
    <div class="wm-levels">${evidenceLevels}</div>
    <button type="button" data-wm-action="theory">${t('Deschide capitolul teoretic complet','Open the full theory chapter')}</button>
   </section>

   <section class="panel wm-panel wm-dashboard-panel" aria-labelledby="wmDashboardTitle">
    <p class="eyebrow">DASHBOARD · EXECUTABLE REFERENCE</p><h3 id="wmDashboardTitle">${t('Actualizare normativă transparentă','Transparent normative update')}</h3>
    <p>${t('Calculatorul nu estimează convingerea unei persoane. Arată numai ce produce regula Bayes pentru un prior și un LR furnizate explicit.','The calculator does not estimate a person’s belief. It only shows what Bayes’ rule produces from an explicitly supplied prior and LR.')}</p>
    <div class="wm-calculator">
     <label>${t('Prior Pprior','Prior Pprior')} <input id="wmPrior" type="number" min="0" max="1" step="0.01" value="0.30"></label>
     <label>${t('Raport diagnostic LR','Diagnostic LR')} <input id="wmLr" type="number" min="0.0001" step="0.1" value="3"></label>
     <div class="wm-metrics"><div><span>Pwm</span><strong id="wmPosterior">—</strong></div><div><span>Uwm</span><strong id="wmUncertainty">—</strong></div><div><span>${t('Direcție','Direction')}</span><strong id="wmDirection">—</strong></div></div>
     <p id="wmCalcNote" class="wm-calc-note"></p>
    </div>
    <details><summary>${t('Precondiții și formule','Preconditions and formulas')}</summary><code>${esc(contract.executable_specification.posterior_formula)}</code><code>${esc(contract.executable_specification.uncertainty_formula)}</code><ul>${contract.executable_specification.preconditions.map(item=>`<li>${esc(item)}</li>`).join('')}</ul><p>${esc(contract.executable_specification.failure_mode)}</p></details>
   </section>

   <section class="panel wm-panel wm-context-panel" aria-labelledby="wmContextTitle">
    <p class="eyebrow">${t('DOVEZI · LIMITE · LEGĂTURI','EVIDENCE · LIMITS · CROSS-LINKS')}</p><h3 id="wmContextTitle">${t('Ce știm și unde se oprește modelul','What we know and where the model stops')}</h3>
    <details open><summary>${t('Condiții de falsificare/slăbire','Falsification / weakening conditions')}</summary><div class="wm-falsification">${falsification}</div></details>
    <details><summary>${t('Limitări explicite','Explicit limitations')}</summary><ul>${limits}</ul></details>
    <details><summary>${t('Dovezi primare','Primary evidence')}</summary><ol>${refs}</ol></details>
    <div class="wm-crosslinks"><h4>${t('Legături către constructele CEM existente','Links to existing CEM constructs')}</h4>${crossLinks}</div>
   </section>
  </div>
 </section>`;

 const priorInput=host.querySelector<HTMLInputElement>('#wmPrior')!;
 const lrInput=host.querySelector<HTMLInputElement>('#wmLr')!;
 const posteriorEl=host.querySelector<HTMLElement>('#wmPosterior')!;
 const uncertaintyEl=host.querySelector<HTMLElement>('#wmUncertainty')!;
 const directionEl=host.querySelector<HTMLElement>('#wmDirection')!;
 const noteEl=host.querySelector<HTMLElement>('#wmCalcNote')!;
 const update=()=>{
  try{
   const p=clamp(Number(priorInput.value),0,1);
   const lr=Number(lrInput.value);
   const next=posterior(p,lr);
   posteriorEl.textContent=next.toFixed(3);
   uncertaintyEl.textContent=entropy(next).toFixed(3);
   directionEl.textContent=lr>1?t('sus','up'):lr<1?t('jos','down'):t('neschimbat','unchanged');
   noteEl.textContent=t('Referință normativă, nu estimare a lui B și nu validare populațională.','Normative reference, not an estimate of B and not population validation.');
   noteEl.dataset.state='ok';
  }catch{
   posteriorEl.textContent='—';uncertaintyEl.textContent='—';directionEl.textContent='—';
   noteEl.textContent=t('LR trebuie să fie finit și strict pozitiv. Operatorul eșuează închis.','LR must be finite and strictly positive. The operator fails closed.');
   noteEl.dataset.state='error';
  }
 };
 priorInput.addEventListener('input',update);lrInput.addEventListener('input',update);update();
 host.querySelector<HTMLButtonElement>('[data-wm-action="registry"]')!.onclick=()=>navigate('reference');
 host.querySelector<HTMLButtonElement>('[data-wm-action="theory"]')!.onclick=()=>{location.hash='#understanding/theory/world-model-construction';};
 host.querySelectorAll<HTMLButtonElement>('[data-semantic-id]').forEach(button=>button.onclick=()=>navigate('reference'));
}
