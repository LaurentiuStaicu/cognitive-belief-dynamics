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
