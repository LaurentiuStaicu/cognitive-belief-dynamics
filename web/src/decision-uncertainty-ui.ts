import type {RobustnessAudit} from './decision-robustness';

type Lang='ro'|'en';
type Copy=Record<Lang,string>;

export type DecisionUncertaintyItem={
 id:string;
 label:Copy;
 role:'SCIENTIFIC_UNCERTAINTY'|'DECISION_ASSUMPTION';
 uncertainty_type:'PARAMETER'|'STRUCTURAL'|'EVIDENCE'|'SCENARIO'|'PREFERENCE'|'IMPLEMENTATION'|'MEASUREMENT';
 target_ids:string[];
 source_kind:string;
 source_refs:string[];
 quantification_status:'QUALITATIVE'|'BOUNDED_RANGE'|'FINITE_SCENARIOS'|'PROBABILITY_DISTRIBUTION';
 probability_status:'NOT_AVAILABLE'|'USER_DECLARED'|'EMPIRICALLY_ESTIMATED'|'MODEL_DERIVED';
 reducibility:string;
 decision_relevance:string[];
 limitations:Copy;
 finite_scenarios?:{id:string;label:Copy;value:number}[];
 bounded_range?:{minimum:number;maximum:number;unit:string};
};

export type DecisionUncertaintyRegistry={
 schema_version:string;
 registry_id:string;
 baseline_artifact:string;
 probability_policy:{
  finite_scenarios_default:'NOT_AVAILABLE';
  infer_probabilities:false;
  expected_value_requires_explicit_probabilities:true;
 };
 uncertainties:DecisionUncertaintyItem[];
};

export const uncertaintyCanonicalContext={
 theorySlug:'interventions',
 semanticIds:[
  'VAR.FAMILIARITY.CLAIM',
  'VAR.CORRECTION.ACCESS',
  'VAR.ACCURACY.SALIENCE',
  'VAR.ACTION.SHARE'
 ]
} as const;

type Options={
 lang:Lang;
 registry:DecisionUncertaintyRegistry;
 audit:RobustnessAudit;
 selectedAlternativeId:number;
 acceptableGainThreshold:number;
 scenarioLabel:(id:string)=>string;
 alternativeLabel:(id:number)=>string;
 number:(value:number)=>string;
 onThresholdChange:(value:number)=>void;
 navigate:(target:string)=>void;
};

const esc=(value:string)=>value.replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]!));
const labelRole=(role:DecisionUncertaintyItem['role'],lang:Lang)=>role==='SCIENTIFIC_UNCERTAINTY'?(lang==='ro'?'incertitudine științifică':'scientific uncertainty'):(lang==='ro'?'ipoteză de decizie':'decision assumption');
const labelQuant=(value:DecisionUncertaintyItem['quantification_status'],lang:Lang)=>({
 QUALITATIVE:lang==='ro'?'calitativă':'qualitative',
 BOUNDED_RANGE:lang==='ro'?'interval mărginit':'bounded range',
 FINITE_SCENARIOS:lang==='ro'?'scenarii finite':'finite scenarios',
 PROBABILITY_DISTRIBUTION:lang==='ro'?'distribuție probabilistică':'probability distribution'
}[value]);

export function renderDecisionUncertainty(host:HTMLElement,options:Options){
 const {lang,registry,audit,selectedAlternativeId,acceptableGainThreshold,scenarioLabel,alternativeLabel,number}=options;
 const tr=(ro:string,en:string)=>lang==='ro'?ro:en;
 const selected=audit.alternatives.find(item=>item.alternativeId===selectedAlternativeId);
 if(!selected)throw new Error('selected alternative is missing from robustness audit');
 const selectedScenarioRows=audit.scenarios.map(scenario=>({scenario,outcome:scenario.outcomes.find(item=>item.alternativeId===selectedAlternativeId)!}));
 const coverage=(count:number|null)=>count===null?tr('necalculat','not calculated'):`${count} / ${audit.scenarioCount}`;
 const range=(value:[number,number]|null)=>value?`${number(value[0])} – ${number(value[1])}`:tr('n/a','n/a');
 const rankRange=selected.rankRange?`${selected.rankRange[0]} – ${selected.rankRange[1]}`:tr('n/a','n/a');
 const regret=selected.maxRegretAcrossFeasibleScenarios===null?tr('n/a','n/a'):number(selected.maxRegretAcrossFeasibleScenarios);
 const changes=audit.decisionSwitch.changes;
 host.innerHTML=`<div class="section-heading uncertainty-heading"><div><p class="eyebrow">OA-6 · DECISION UNDER UNCERTAINTY</p><h3>${tr('Ce rămâne robust când schimbăm ipotezele?','What remains robust when assumptions change?')}</h3><p>${tr('Compară aceleași opțiuni fezabile în cele trei profiluri declarate. Frecvența unui rezultat în aceste profiluri este acoperire de scenarii, nu probabilitate.','Compare the same feasible options across the three declared profiles. Frequency across these profiles is scenario coverage, not probability.')}</p></div><span class="uncertainty-badge">${tr('FĂRĂ PROBABILITĂȚI IMPLICITE','NO IMPLIED PROBABILITIES')}</span></div>
 <details class="uncertainty-ledger" open>
  <summary>${tr('Ce este incert? Registrul OA-6A','What is uncertain? OA-6A registry')}</summary>
  <div class="uncertainty-ledger-grid">${registry.uncertainties.map(item=>`<article data-uncertainty-id="${esc(item.id)}"><div class="uncertainty-tags"><span>${esc(labelRole(item.role,lang))}</span><span>${esc(item.uncertainty_type)}</span><span>${esc(labelQuant(item.quantification_status,lang))}</span></div><h4>${esc(item.label[lang])}</h4><p>${esc(item.limitations[lang])}</p><dl><dt>${tr('Probabilitate','Probability')}</dt><dd><code>${esc(item.probability_status)}</code></dd><dt>${tr('Reducibilitate','Reducibility')}</dt><dd><code>${esc(item.reducibility)}</code></dd></dl></article>`).join('')}</div>
 </details>
 <div class="uncertainty-threshold"><div><label for="acceptabilityThreshold">${tr('Prag de acceptabilitate ales de utilizator · câștig minim','User-declared acceptability threshold · minimum gain')}</label><p class="note">${tr('Pragul este o preferință de decizie, nu un parametru științific și nu modifică scorurile modelului.','The threshold is a decision preference, not a scientific parameter, and does not modify model scores.')}</p></div><input id="acceptabilityThreshold" type="number" min="0" max="100" step="0.5" value="${acceptableGainThreshold}"></div>
 <section id="selectedRobustness" data-selected-alternative="${selectedAlternativeId}" aria-live="polite">
  <h4>${tr('Robustețea combinației selectate','Robustness of the selected bundle')}: ${esc(alternativeLabel(selectedAlternativeId))}</h4>
  <div class="uncertainty-metrics">
   <div><span>${tr('Prima alegere în','Top-ranked in')}</span><strong id="selectedTopCoverage">${coverage(selected.topRankScenarioCount)}</strong><small>${tr('scenarii declarate','declared scenarios')}</small></div>
   <div><span>${tr('Acceptabilă peste prag în','Acceptable above threshold in')}</span><strong id="selectedAcceptableCoverage">${coverage(selected.acceptableScenarioCount)}</strong><small>${tr('scenarii declarate','declared scenarios')}</small></div>
   <div><span>${tr('Interval rang','Rank range')}</span><strong>${rankRange}</strong><small>${tr('rang, nu probabilitate','rank, not probability')}</small></div>
   <div><span>${tr('Regret maxim','Maximum regret')}</span><strong>${regret}</strong><small>${tr('puncte de scor în setul declarat','score points in declared set')}</small></div>
  </div>
 </section>
 <div class="table-scroll uncertainty-matrix"><table id="uncertaintyScenarioMatrix"><caption>${tr('Aceleași restricții, costuri, ponderi și moment de activare; se schimbă numai profilul de răspuns declarat.','Same constraints, costs, weights and activation timing; only the declared response profile changes.')}</caption><thead><tr><th scope="col">${tr('Scenariu','Scenario')}</th><th scope="col">${tr('Prima alegere fezabilă','Top feasible choice')}</th><th scope="col">${tr('Rangul combinației selectate','Selected rank')}</th><th scope="col">${tr('Câștig selectat','Selected gain')}</th><th scope="col">${tr('Regret selectat','Selected regret')}</th></tr></thead><tbody>${selectedScenarioRows.map(({scenario,outcome})=>`<tr data-uncertainty-scenario="${esc(scenario.scenarioId)}"><th scope="row">${esc(scenarioLabel(scenario.scenarioId))}</th><td>${scenario.topAlternativeIds.map(alternativeLabel).map(esc).join(' = ')}</td><td>${outcome.rank??tr('nefezabil','infeasible')}</td><td>${number(outcome.gain)}</td><td>${outcome.regret===null?tr('n/a','n/a'):number(outcome.regret)}</td></tr>`).join('')}</tbody></table></div>
 <section id="decisionSwitch" class="uncertainty-switch"><h4>${tr('De ce se schimbă decizia?','Why does the decision switch?')}</h4>${changes.length?`<p>${tr('Față de profilul de referință selectat, prima alegere se schimbă în condițiile de mai jos. Aceasta este sensibilitate la scenariu, nu probabilitate de schimbare.','Relative to the selected reference profile, the top choice changes under the conditions below. This is scenario sensitivity, not a probability of switching.')}</p><ul>${changes.map(change=>`<li data-switch-scenario="${esc(change.scenarioId)}" data-switch-top-mask="${change.topAlternativeIds.join(',')}"><strong>${esc(scenarioLabel(change.scenarioId))}</strong>: ${change.topAlternativeIds.map(alternativeLabel).map(esc).join(' = ')}</li>`).join('')}</ul>`:`<p>${tr('Nu apare o schimbare a primei alegeri între cele trei profiluri declarate pentru setările curente. Aceasta nu demonstrează robustețe în afara acestor trei scenarii.','No top-choice switch appears across the three declared profiles under the current settings. This does not establish robustness beyond these three scenarios.')}</p>`}</section>
 <details class="uncertainty-robustness-table"><summary>${tr('Compară robustețea tuturor combinațiilor','Compare robustness across all bundles')}</summary><div class="table-scroll"><table><thead><tr><th scope="col">${tr('Combinație','Bundle')}</th><th scope="col">${tr('Fezabilă','Feasible')}</th><th scope="col">${tr('Prima alegere','Top-ranked')}</th><th scope="col">${tr('Acceptabilă','Acceptable')}</th><th scope="col">${tr('Rang','Rank')}</th><th scope="col">${tr('Câștig','Gain')}</th><th scope="col">${tr('Regret maxim','Max regret')}</th></tr></thead><tbody>${audit.alternatives.filter(item=>item.feasibleScenarioCount>0).map(item=>`<tr data-robustness-alternative="${item.alternativeId}"><th scope="row">${esc(alternativeLabel(item.alternativeId))}</th><td>${item.feasibleScenarioCount} / ${item.scenarioDenominator}</td><td>${item.topRankScenarioCount} / ${item.scenarioDenominator}</td><td>${coverage(item.acceptableScenarioCount)}</td><td>${item.rankRange?item.rankRange.join(' – '):tr('n/a','n/a')}</td><td>${range(item.gainRange)}</td><td>${item.maxRegretAcrossFeasibleScenarios===null?tr('n/a','n/a'):number(item.maxRegretAcrossFeasibleScenarios)}</td></tr>`).join('')}</tbody></table></div></details>
 <div class="boundary uncertainty-boundary"><strong>${tr('Limită epistemică','Epistemic boundary')}</strong><p>${tr('Profilurile low/reference/high sunt scenarii finite de sensibilitate cu probability_status = NOT_AVAILABLE. Nici raportul 3/3, nici regretul, nici intervalele de rang nu sunt probabilități, intervale de încredere sau recomandări validate pentru populație.','The low/reference/high profiles are finite sensitivity scenarios with probability_status = NOT_AVAILABLE. Neither 3/3 coverage, regret, nor rank ranges are probabilities, confidence intervals, or validated population recommendations.')}</p></div>
 <div class="uncertainty-context"><h4>${tr('Context canonic asociat','Related canonical context')}</h4><p class="note">${tr('Aceste legături navighează către obiecte deja înregistrate; nu adaugă relații științifice noi.','These links navigate to already-registered objects; they do not add new scientific relations.')}</p><div><button type="button" data-uncertainty-theory>${tr('Teorie · intervenții','Theory · interventions')}</button>${uncertaintyCanonicalContext.semanticIds.map(id=>`<span class="uncertainty-context-item"><code>${id}</code><button type="button" data-uncertainty-search="${id}">${tr('Caută','Search')}</button><button type="button" data-uncertainty-inspect="${id}">${tr('Inspector','Inspector')}</button></span>`).join('')}<button type="button" data-uncertainty-reference="VAR.ACTION.SHARE">${tr('Registru · Share','Registry · Share')}</button></div></div>`;

 host.querySelector<HTMLInputElement>('#acceptabilityThreshold')!.onchange=event=>{
  const input=event.currentTarget;
  if(!input.reportValidity())return;
  options.onThresholdChange(Number(input.value));
 };
 host.querySelector<HTMLButtonElement>('[data-uncertainty-theory]')!.onclick=()=>{location.hash='#understanding/theory/'+uncertaintyCanonicalContext.theorySlug;};
 host.querySelectorAll<HTMLButtonElement>('[data-uncertainty-search]').forEach(button=>button.onclick=()=>options.navigate('search:'+button.dataset.uncertaintySearch));
 host.querySelectorAll<HTMLButtonElement>('[data-uncertainty-inspect]').forEach(button=>button.onclick=()=>options.navigate('inspect:'+button.dataset.uncertaintyInspect));
 const reference=host.querySelector<HTMLButtonElement>('[data-uncertainty-reference]')!;
 reference.onclick=()=>options.navigate('reference:'+reference.dataset.uncertaintyReference);
}
