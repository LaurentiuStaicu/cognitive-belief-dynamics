import type {ImplementationPlan} from './implementation-plan';
import type {IndicatorDefinition,IndicatorProjection} from './indicator-objects';
import {addRealityLoopObject,readRealityLoopObject} from './workspace-indexeddb';

type Lang='ro'|'en';
type Copy={ro:string;en:string};

export type ObservedOutcome={
 object_type:'ObservedOutcome';
 id:string;
 case_id:string;
 implementation_plan_id:string;
 prospective_snapshot_id:string;
 indicator_id:string;
 population:{
  label:Copy;
  definition:Copy;
  inclusion?:string;
  exclusion?:string;
 };
 context:{
  setting:Copy;
  geography?:string;
  time_horizon:string;
 };
 outcome:{
  name:Copy;
  definition:Copy;
  stage:'PROXIMAL'|'INTERMEDIATE'|'FINAL';
 };
 feature_of_interest:string;
 observed_property:string;
 procedure:string;
 phenomenon_time:string;
 result_time:string;
 result:{
  value:number;
  unit?:string;
  quality_note?:string;
 };
 source_refs:string[];
 recorded_at:string;
 retrospective:true;
 mutation_policy:'APPEND_ONLY_NO_RETROACTIVE_PREDICTION_EDIT';
};

export type ObservedOutcomeInput={
 plan:ImplementationPlan;
 indicators:IndicatorProjection;
 indicator_id:string;
 population_label:string;
 population_definition:string;
 population_inclusion?:string;
 population_exclusion?:string;
 setting:string;
 geography?:string;
 time_horizon:string;
 outcome_name:string;
 outcome_definition:string;
 feature_of_interest:string;
 procedure:string;
 phenomenon_time:string;
 result_time:string;
 result_value:number;
 quality_note?:string;
 source_refs:string[];
 now?:()=>string;
 id?:()=>string;
};

const defaultId=()=>crypto.randomUUID();
const clean=(value:string)=>value.trim();
const verbatim=(value:string):Copy=>({ro:clean(value),en:clean(value)});
const required=(value:string,name:string)=>{
 const result=clean(value);
 if(!result)throw new Error(`${name} is required`);
 return result;
};
const uniqueRefs=(values:string[])=>[...new Set(values.map(clean).filter(Boolean))];

function indicatorFor(indicators:IndicatorProjection,id:string):IndicatorDefinition{
 const definition=indicators.indicators.find(item=>item.definition.id===id)?.definition;
 if(!definition)throw new Error('indicator reference is not available in the current IndicatorProjection');
 return definition;
}

function parseTime(value:string,name:string):number{
 const parsed=Date.parse(value);
 if(!Number.isFinite(parsed))throw new Error(`${name} must be a valid date-time`);
 return parsed;
}

export function validateObservedOutcomeReferences(
 record:ObservedOutcome,
 plan:ImplementationPlan,
 indicators:IndicatorProjection
):void{
 if(plan.object_type!=='ImplementationPlan')throw new Error('referenced record is not an ImplementationPlan');
 if(record.case_id!==plan.case_id)throw new Error('ObservedOutcome case_id does not match ImplementationPlan');
 if(record.implementation_plan_id!==plan.id)throw new Error('ObservedOutcome ImplementationPlan reference mismatch');
 if(record.prospective_snapshot_id!==plan.prospective_snapshot.id)throw new Error('ObservedOutcome ProspectiveSnapshot reference mismatch');
 if(!plan.indicator_ids.includes(record.indicator_id))throw new Error('ObservedOutcome Indicator is not frozen into the ImplementationPlan');
 const definition=indicatorFor(indicators,record.indicator_id);
 if(record.observed_property!==definition.observed_property)throw new Error('ObservedOutcome observed_property does not match Indicator definition');
 if(record.outcome.stage!==definition.target_stage)throw new Error('ObservedOutcome outcome stage does not match Indicator definition');
 if(definition.unit&&record.result.unit!==definition.unit)throw new Error('ObservedOutcome result unit does not match Indicator definition');
 if(definition.target_stage==='PROXIMAL'&&!plan.action_canvas.proximal_result.indicator_ids.includes(record.indicator_id)){
  throw new Error('ObservedOutcome Indicator is not linked to the frozen proximal Action Canvas stage');
 }
 if(definition.target_stage==='INTERMEDIATE'&&!plan.action_canvas.intermediate_result.indicator_ids.includes(record.indicator_id)){
  throw new Error('ObservedOutcome Indicator is not linked to the frozen intermediate Action Canvas stage');
 }
 if(definition.target_stage==='FINAL'&&!plan.action_canvas.final_outcome.indicator_ids.includes(record.indicator_id)){
  throw new Error('ObservedOutcome Indicator is not linked to the frozen final Action Canvas stage');
 }
}

export function materializeObservedOutcome(input:ObservedOutcomeInput):ObservedOutcome{
 const definition=indicatorFor(input.indicators,input.indicator_id);
 if(input.plan.plan_scope!=='ILLUSTRATIVE')throw new Error('this recorder slice accepts only the current illustrative ImplementationPlan');
 if(!input.plan.indicator_ids.includes(definition.id))throw new Error('selected Indicator is not part of the frozen ImplementationPlan');

 const populationLabel=required(input.population_label,'population label');
 const populationDefinition=required(input.population_definition,'population definition');
 const setting=required(input.setting,'context setting');
 const timeHorizon=required(input.time_horizon,'time horizon');
 const outcomeName=required(input.outcome_name,'outcome name');
 const outcomeDefinition=required(input.outcome_definition,'outcome definition');
 const feature=required(input.feature_of_interest,'feature of interest');
 const procedure=required(input.procedure,'procedure');
 const sourceRefs=uniqueRefs(input.source_refs);
 if(sourceRefs.length===0)throw new Error('at least one source reference is required');
 if(!Number.isFinite(input.result_value))throw new Error('result value must be finite');
 if(definition.unit==='probability'&&(input.result_value<0||input.result_value>1))throw new Error('probability result must be between 0 and 1');

 const phenomenonMs=parseTime(input.phenomenon_time,'phenomenon_time');
 const resultMs=parseTime(input.result_time,'result_time');
 const recordedAt=(input.now??(()=>new Date().toISOString()))();
 const recordedMs=parseTime(recordedAt,'recorded_at');
 if(phenomenonMs>resultMs)throw new Error('phenomenon_time must not be after result_time');
 if(resultMs>recordedMs)throw new Error('result_time must not be in the future relative to recorded_at');

 const token=(input.id??defaultId)();
 const record:ObservedOutcome={
  object_type:'ObservedOutcome',
  id:`CEM.OBSERVED.OUTCOME.${token}`,
  case_id:input.plan.case_id,
  implementation_plan_id:input.plan.id,
  prospective_snapshot_id:input.plan.prospective_snapshot.id,
  indicator_id:definition.id,
  population:{
   label:verbatim(populationLabel),
   definition:verbatim(populationDefinition),
   ...(clean(input.population_inclusion??'')?{inclusion:clean(input.population_inclusion!)}:{}),
   ...(clean(input.population_exclusion??'')?{exclusion:clean(input.population_exclusion!)}:{})
  },
  context:{
   setting:verbatim(setting),
   ...(clean(input.geography??'')?{geography:clean(input.geography!)}:{}),
   time_horizon:timeHorizon
  },
  outcome:{
   name:verbatim(outcomeName),
   definition:verbatim(outcomeDefinition),
   stage:definition.target_stage
  },
  feature_of_interest:feature,
  observed_property:definition.observed_property,
  procedure,
  phenomenon_time:new Date(phenomenonMs).toISOString(),
  result_time:new Date(resultMs).toISOString(),
  result:{
   value:input.result_value,
   ...(definition.unit?{unit:definition.unit}:{}),
   ...(clean(input.quality_note??'')?{quality_note:clean(input.quality_note!)}:{})
  },
  source_refs:sourceRefs,
  recorded_at:new Date(recordedMs).toISOString(),
  retrospective:true,
  mutation_policy:'APPEND_ONLY_NO_RETROACTIVE_PREDICTION_EDIT'
 };
 validateObservedOutcomeReferences(record,input.plan,input.indicators);
 return record;
}

export async function persistObservedOutcome(
 record:ObservedOutcome,
 indicators:IndicatorProjection
):Promise<ObservedOutcome>{
 const persistedPlan=await readRealityLoopObject<ImplementationPlan>(record.implementation_plan_id);
 if(!persistedPlan)throw new Error('referenced ImplementationPlan is not present in canonical IndexedDB storage');
 validateObservedOutcomeReferences(record,persistedPlan,indicators);
 return addRealityLoopObject(record);
}

const esc=(value:string)=>value.replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]??c));
const localDefault=()=>new Date(Date.now()-60_000).toISOString().slice(0,16);

export function mountObservedOutcomeRecorder(
 host:HTMLElement,
 input:{plan:ImplementationPlan;indicators:IndicatorProjection;lang:Lang}
):void{
 const {plan,indicators,lang}=input;
 const t=(ro:string,en:string)=>lang==='ro'?ro:en;
 const options=plan.indicator_ids.map(id=>{
  const definition=indicatorFor(indicators,id);
  return `<option value="${esc(id)}">${esc(definition.label[lang])} · ${esc(id)}</option>`;
 }).join('');
 host.innerHTML=`<section id="observedOutcomeRecorder" data-plan-id="${esc(plan.id)}" data-snapshot-id="${esc(plan.prospective_snapshot.id)}">
  <div class="section-heading"><div><p class="eyebrow">OA-7 · RETROSPECTIVE OBSERVATION</p><h4>${t('Înregistrează un rezultat observat','Record an observed outcome')}</h4><p>${t('Înregistrarea este manuală, retrospectivă și append-only. Nu copiază automat valorile simulării și nu modifică planul sau snapshotul prospectiv.','The record is manual, retrospective and append-only. It never copies simulation values automatically and does not modify the plan or prospective snapshot.')}</p></div><span class="planner-badge">ILLUSTRATIVE · MANUAL</span></div>
  <form id="observedOutcomeForm">
   <label>${t('Indicator din planul înghețat','Indicator from frozen plan')}<select name="indicator_id" required>${options}</select></label>
   <label>${t('Eticheta populației','Population label')}<input name="population_label" required></label>
   <label>${t('Definiția populației','Population definition')}<textarea name="population_definition" required></textarea></label>
   <label>${t('Criterii de includere (opțional)','Inclusion criteria (optional)')}<input name="population_inclusion"></label>
   <label>${t('Criterii de excludere (opțional)','Exclusion criteria (optional)')}<input name="population_exclusion"></label>
   <label>${t('Cadru / setting','Setting')}<input name="setting" required></label>
   <label>${t('Geografie (opțional)','Geography (optional)')}<input name="geography"></label>
   <label>${t('Orizont temporal','Time horizon')}<input name="time_horizon" required placeholder="${t('ex. 30 zile','e.g. 30 days')}"></label>
   <label>${t('Numele rezultatului','Outcome name')}<input name="outcome_name" required></label>
   <label>${t('Definiția rezultatului','Outcome definition')}<textarea name="outcome_definition" required></textarea></label>
   <label>${t('Entitatea / caracteristica observată','Feature of interest')}<input name="feature_of_interest" required></label>
   <label>${t('Procedura de măsurare','Measurement procedure')}<textarea name="procedure" required></textarea></label>
   <label>${t('Momentul fenomenului','Phenomenon time')}<input name="phenomenon_time" type="datetime-local" required value="${localDefault()}"></label>
   <label>${t('Momentul rezultatului','Result time')}<input name="result_time" type="datetime-local" required value="${localDefault()}"></label>
   <label>${t('Valoare observată','Observed value')}<input name="result_value" type="number" min="0" max="1" step="0.0001" required></label>
   <label>${t('Notă de calitate (opțional)','Quality note (optional)')}<textarea name="quality_note"></textarea></label>
   <label>${t('Surse — câte una pe rând','Sources — one per line')}<textarea name="source_refs" required></textarea></label>
   <button type="submit" class="primary">${t('Adaugă ObservedOutcome','Append ObservedOutcome')}</button>
  </form>
  <p class="note">${t('Textele libere sunt păstrate verbatim în ambele câmpuri bilingve; recorderul nu inventează traduceri. Pentru indicatorii M0, unitatea este probability și sunt acceptate numai valori 0–1.','Free text is preserved verbatim in both bilingual fields; the recorder does not invent translations. For the current M0 indicators, the unit is probability and only values from 0 to 1 are accepted.')}</p>
  <p id="observedOutcomeStatus" class="note" aria-live="polite"></p>
 </section>`;

 const form=host.querySelector<HTMLFormElement>('#observedOutcomeForm')!;
 const status=host.querySelector<HTMLElement>('#observedOutcomeStatus')!;
 form.onsubmit=async event=>{
  event.preventDefault();
  const submit=form.querySelector<HTMLButtonElement>('button[type="submit"]')!;
  if(!form.reportValidity())return;
  submit.disabled=true;
  status.textContent=t('Se validează referințele și se adaugă observația…','Validating references and appending observation…');
  try{
   const data=new FormData(form);
   const dt=(name:string)=>new Date(String(data.get(name))).toISOString();
   const record=materializeObservedOutcome({
    plan,
    indicators,
    indicator_id:String(data.get('indicator_id')),
    population_label:String(data.get('population_label')),
    population_definition:String(data.get('population_definition')),
    population_inclusion:String(data.get('population_inclusion')??''),
    population_exclusion:String(data.get('population_exclusion')??''),
    setting:String(data.get('setting')),
    geography:String(data.get('geography')??''),
    time_horizon:String(data.get('time_horizon')),
    outcome_name:String(data.get('outcome_name')),
    outcome_definition:String(data.get('outcome_definition')),
    feature_of_interest:String(data.get('feature_of_interest')),
    procedure:String(data.get('procedure')),
    phenomenon_time:dt('phenomenon_time'),
    result_time:dt('result_time'),
    result_value:Number(data.get('result_value')),
    quality_note:String(data.get('quality_note')??''),
    source_refs:String(data.get('source_refs')).split(/\r?\n/)
   });
   const stored=await persistObservedOutcome(record,indicators);
   host.dataset.observedOutcomeId=stored.id;
   status.textContent=t(`Observație adăugată append-only: ${stored.id}`,`Append-only observation saved: ${stored.id}`);
  }catch(error){
   status.textContent=t(`Înregistrarea a eșuat: ${String(error)}`,`Observation failed: ${String(error)}`);
  }finally{submit.disabled=false;}
 };
}
