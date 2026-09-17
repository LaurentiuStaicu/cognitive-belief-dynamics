type Lang='ro'|'en';
type Copy=Record<Lang,string>;

export type IndicatorDefinition={object_type:'Indicator';id:string;label:Copy;observed_property:string;target_stage:'PROXIMAL'|'INTERMEDIATE'|'FINAL';result_type:'NUMBER'|'BOOLEAN'|'TEXT'|'CATEGORY';unit?:string;direction:'INCREASE'|'DECREASE'|'STAY_WITHIN_RANGE'|'NONE';measurement_procedure:string;source_refs:string[];limitations:Copy};
export type SimulationIndicatorReading={reading_kind:'SIMULATION_RESULT';indicator_id:string;value:number;unit:'probability';source_ref:'web/public/model/interventions.json';observation_status:'NOT_OBSERVED'};
export type IndicatorRuntimeObject={definition:IndicatorDefinition;reading:SimulationIndicatorReading};
export type IndicatorCoverage={stage:'PROXIMAL'|'INTERMEDIATE'|'FINAL';status:'AVAILABLE_SIMULATION_INDICATORS'|'NOT_OPERATIONALIZED';indicator_ids:string[]};
export type IndicatorProjection={object_type:'IndicatorProjection';persistence:'READ_ONLY_NOT_WORKSPACE';observation_boundary:'SIMULATION_RESULT_IS_NOT_OBSERVED_OUTCOME';indicators:IndicatorRuntimeObject[];coverage:IndicatorCoverage[]};

const copy=(ro:string,en:string):Copy=>({ro,en});
const DEFINITIONS:IndicatorDefinition[]=[
 {object_type:'Indicator',id:'CEM.INDICATOR.M0.FALSE_SHARING.MEAN13',label:copy('Probabilitatea medie simulată de distribuire a afirmației false','Mean simulated false-claim sharing probability'),observed_property:'M0.SIMULATED.FALSE_SHARING.PROBABILITY.MEAN13',target_stage:'PROXIMAL',result_type:'NUMBER',unit:'probability',direction:'DECREASE',measurement_procedure:'COMPUTED_FROM_M0_FALSE_SHARE_13_STEP_MEAN',source_refs:['web/public/model/interventions.json'],limitations:copy('Output de simulare pentru o afirmație sintetică falsă. Nu este prevalență, rată populațională sau observație empirică.','Simulation output for one synthetic false claim. It is not prevalence, a population rate, or an empirical observation.')},
 {object_type:'Indicator',id:'CEM.INDICATOR.M0.TRUE_SHARING.MEAN13',label:copy('Probabilitatea medie simulată de distribuire a afirmației adevărate','Mean simulated true-claim sharing probability'),observed_property:'M0.SIMULATED.TRUE_SHARING.PROBABILITY.MEAN13',target_stage:'PROXIMAL',result_type:'NUMBER',unit:'probability',direction:'INCREASE',measurement_procedure:'COMPUTED_FROM_M0_TRUE_SHARE_13_STEP_MEAN',source_refs:['web/public/model/interventions.json'],limitations:copy('Output de simulare pentru o afirmație sintetică adevărată. Nu este prevalență, rată populațională sau observație empirică.','Simulation output for one synthetic true claim. It is not prevalence, a population rate, or an empirical observation.')}
];

export function buildIndicatorProjection(bundle:{false_share:number;true_share:number}):IndicatorProjection{
 const values:Record<string,number>={'CEM.INDICATOR.M0.FALSE_SHARING.MEAN13':bundle.false_share,'CEM.INDICATOR.M0.TRUE_SHARING.MEAN13':bundle.true_share};
 const indicators=DEFINITIONS.map(definition=>({definition,reading:{reading_kind:'SIMULATION_RESULT' as const,indicator_id:definition.id,value:values[definition.id],unit:'probability' as const,source_ref:'web/public/model/interventions.json' as const,observation_status:'NOT_OBSERVED' as const}}));
 return {object_type:'IndicatorProjection',persistence:'READ_ONLY_NOT_WORKSPACE',observation_boundary:'SIMULATION_RESULT_IS_NOT_OBSERVED_OUTCOME',indicators,coverage:[{stage:'PROXIMAL',status:'AVAILABLE_SIMULATION_INDICATORS',indicator_ids:indicators.map(item=>item.definition.id)},{stage:'INTERMEDIATE',status:'NOT_OPERATIONALIZED',indicator_ids:[]},{stage:'FINAL',status:'NOT_OPERATIONALIZED',indicator_ids:[]}]};
}
