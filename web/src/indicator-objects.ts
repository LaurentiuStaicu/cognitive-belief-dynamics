type Lang='ro'|'en';
type Copy=Record<Lang,string>;

export type IndicatorDefinition={
 object_type:'Indicator';
 id:string;
 label:Copy;
 observed_property:string;
 target_stage:'PROXIMAL'|'INTERMEDIATE'|'FINAL';
 result_type:'NUMBER'|'BOOLEAN'|'TEXT'|'CATEGORY';
 unit?:string;
 direction:'INCREASE'|'DECREASE'|'STAY_WITHIN_RANGE'|'NONE';
 measurement_procedure:string;
 source_refs:string[];
 limitations:Copy;
};

export type SimulationIndicatorReading={
 reading_kind:'SIMULATION_RESULT';
 indicator_id:string;
 value:number;
 unit:'probability';
 source_ref:'web/public/model/interventions.json';
 observation_status:'NOT_OBSERVED';
};

export type IndicatorRuntimeObject={
 definition:IndicatorDefinition;
 reading:SimulationIndicatorReading;
};

export type IndicatorCoverage={
 stage:'PROXIMAL'|'INTERMEDIATE'|'FINAL';
 status:'AVAILABLE_SIMULATION_INDICATORS'|'NOT_OPERATIONALIZED';
 indicator_ids:string[];
};

export type IndicatorProjection={
 object_type:'IndicatorProjection';
 persistence:'READ_ONLY_NOT_WORKSPACE';
 observation_boundary:'SIMULATION_RESULT_IS_NOT_OBSERVED_OUTCOME';
 indicators:IndicatorRuntimeObject[];
 coverage:IndicatorCoverage[];
};

const copy=(ro:string,en:string):Copy=>({ro,en});

const DEFINITIONS:IndicatorDefinition[]=[
 {
  object_type:'Indicator',
  id:'CEM.INDICATOR.M0.FALSE_SHARING.MEAN13',
  label:copy('Probabilitatea medie simulată de distribuire a afirmației false','Mean simulated false-claim sharing probability'),
  observed_property:'M0.SIMULATED.FALSE_SHARING.PROBABILITY.MEAN13',
  target_stage:'PROXIMAL',
  result_type:'NUMBER',
  unit:'probability',
  direction:'DECREASE',
  measurement_procedure:'COMPUTED_FROM_M0_FALSE_SHARE_13_STEP_MEAN',
  source_refs:['web/public/model/interventions.json'],
  limitations:copy(
   'Output de simulare pentru o afirmație sintetică falsă. Nu este prevalență, rată populațională sau observație empirică.',
   'Simulation output for one synthetic false claim. It is not prevalence, a population rate, or an empirical observation.'
  )
 },
 {
  object_type:'Indicator',
  id:'CEM.INDICATOR.M0.TRUE_SHARING.MEAN13',
  label:copy('Probabilitatea medie simulată de distribuire a afirmației adevărate','Mean simulated true-claim sharing probability'),
  observed_property:'M0.SIMULATED.TRUE_SHARING.PROBABILITY.MEAN13',
  target_stage:'PROXIMAL',
  result_type:'NUMBER',
  unit:'probability',
  direction:'INCREASE',
  measurement_procedure:'COMPUTED_FROM_M0_TRUE_SHARE_13_STEP_MEAN',
  source_refs:['web/public/model/interventions.json'],
  limitations:copy(
   'Output de simulare pentru o afirmație sintetică adevărată. Nu este prevalență, rată populațională sau observație empirică.',
   'Simulation output for one synthetic true claim. It is not prevalence, a population rate, or an empirical observation.'
  )
 }
];

export function buildIndicatorProjection(bundle:{false_share:number;true_share:number}):IndicatorProjection{
 const values:Record<string,number>={
  'CEM.INDICATOR.M0.FALSE_SHARING.MEAN13':bundle.false_share,
  'CEM.INDICATOR.M0.TRUE_SHARING.MEAN13':bundle.true_share
 };
 const indicators=DEFINITIONS.map(definition=>({
  definition,
  reading:{
   reading_kind:'SIMULATION_RESULT' as const,
   indicator_id:definition.id,
   value:values[definition.id],
   unit:'probability' as const,
   source_ref:'web/public/model/interventions.json' as const,
   observation_status:'NOT_OBSERVED' as const
  }
 }));
 return {
  object_type:'IndicatorProjection',
  persistence:'READ_ONLY_NOT_WORKSPACE',
  observation_boundary:'SIMULATION_RESULT_IS_NOT_OBSERVED_OUTCOME',
  indicators,
  coverage:[
   {stage:'PROXIMAL',status:'AVAILABLE_SIMULATION_INDICATORS',indicator_ids:indicators.map(item=>item.definition.id)},
   {stage:'INTERMEDIATE',status:'NOT_OPERATIONALIZED',indicator_ids:[]},
   {stage:'FINAL',status:'NOT_OPERATIONALIZED',indicator_ids:[]}
  ]
 };
}

const esc=(value:string)=>value.replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]??c));
const n=(value:number,lang:Lang)=>value.toLocaleString(lang==='ro'?'ro-RO':'en-GB',{minimumFractionDigits:4,maximumFractionDigits:4});

export function renderIndicatorObjects(projection:IndicatorProjection,lang:Lang):string{
 const t=(ro:string,en:string)=>lang==='ro'?ro:en;
 return `<section id="indicatorObjects" class="indicator-objects">
  <div class="section-heading"><div><p class="eyebrow">OA-7 · INDICATOR OBJECTS</p><h4>${t('Ce putem măsura acum — și ce nu','What can be measured now — and what cannot')}</h4><p>${t('Indicatorii disponibili acum sunt definiții read-only legate de outputurile M0. Valorile afișate sunt rezultate de simulare, nu ObservedOutcome.','The currently available indicators are read-only definitions tied to M0 outputs. Displayed values are simulation results, not ObservedOutcome records.')}</p></div><span class="indicator-boundary">${projection.observation_boundary}</span></div>
  <div class="indicator-grid">${projection.indicators.map(item=>`<article data-indicator-id="${esc(item.definition.id)}" data-indicator-stage="${item.definition.target_stage}" data-observation-status="${item.reading.observation_status}">
   <div class="indicator-title"><h5>${esc(item.definition.label[lang])}</h5><code>${esc(item.definition.id)}</code></div>
   <dl><dt>${t('Proprietate','Property')}</dt><dd>${esc(item.definition.observed_property)}</dd><dt>${t('Procedură','Procedure')}</dt><dd>${esc(item.definition.measurement_procedure)}</dd><dt>${t('Direcție dorită','Desired direction')}</dt><dd>${item.definition.direction}</dd><dt>${t('Valoare simulată curentă','Current simulated value')}</dt><dd><strong>${n(item.reading.value,lang)}</strong> ${item.reading.unit}</dd><dt>${t('Status observație','Observation status')}</dt><dd><strong>${item.reading.observation_status}</strong></dd></dl>
   <p class="note">${esc(item.definition.limitations[lang])}</p>
  </article>`).join('')}</div>
  <div class="indicator-coverage">${projection.coverage.map(item=>`<article data-indicator-coverage="${item.stage}" data-indicator-coverage-status="${item.status}"><strong>${item.stage}</strong><span>${item.status}</span><small>${item.indicator_ids.length?item.indicator_ids.map(esc).join(' · '):t('Niciun Indicator operațional definit încă.','No operational Indicator defined yet.')}</small></article>`).join('')}</div>
  <div class="boundary"><strong>${t('Limită observațională','Observation boundary')}</strong><p>${t('Un Indicator definește ce ar trebui urmărit și cum este calculat aici. Nu creează o observație retrospectivă. ObservedOutcome va fi introdus numai într-un slice ulterior, cu populație, context, procedură și timp de observație explicit.','An Indicator defines what should be tracked and how it is calculated here. It does not create a retrospective observation. ObservedOutcome will be introduced only in a later slice with explicit population, context, procedure, and observation time.')}</p></div>
 </section>`;
}
