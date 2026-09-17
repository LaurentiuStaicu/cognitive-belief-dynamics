type Lang='ro'|'en';
type Copy=Record<Lang,string>;

export type ActionCanvasStatus='CANONICAL_INPUT'|'SIMULATED_OUTPUT'|'NOT_OPERATIONALIZED';
export type ActionCanvasStage='PROBLEM'|'TARGET_MECHANISM'|'INTERVENTION'|'PROXIMAL_RESULT'|'INTERMEDIATE_RESULT'|'FINAL_OUTCOME';

export type ActionCanvasLever={id:string;bit:number;label:Copy;factor:string;action:Copy};
export type ActionCanvasBundle={mask:number;false_share:number;true_share:number};
export type ActionCanvasNode={stage:ActionCanvasStage;status:ActionCanvasStatus;title:Copy;detail:Copy;refs:string[]};
export type ActionCanvasProjection={object_type:'ActionCanvasProjection';scope:'ILLUSTRATIVE_UNCALIBRATED';persistence:'READ_ONLY_NOT_IMPLEMENTATION_PLAN';bundle_mask:number;nodes:ActionCanvasNode[]};

const copy=(ro:string,en:string):Copy=>({ro,en});
const signed=(value:number)=>value>0?`+${value.toFixed(4)}`:value.toFixed(4);

export function buildActionCanvasProjection(input:{bundle:ActionCanvasBundle;baseline:ActionCanvasBundle;levers:ActionCanvasLever[]}):ActionCanvasProjection{
 const selected=input.levers.filter(lever=>(input.bundle.mask&lever.bit)!==0);
 const mechanism=selected.length?selected.map(lever=>`${lever.label.ro}: ${lever.factor}`).join(' · '):'Nicio măsură activă; nu este selectată o cale mecanistică de intervenție.';
 const mechanismEn=selected.length?selected.map(lever=>`${lever.label.en}: ${lever.factor}`).join(' · '):'No active measure; no intervention mechanism path is selected.';
 const interventionRo=selected.length?selected.map(lever=>lever.action.ro).join(' · '):'Fără măsuri; rulează numai condițiile de bază ale simulării.';
 const interventionEn=selected.length?selected.map(lever=>lever.action.en).join(' · '):'No measures; only the simulation baseline conditions run.';
 const falseDelta=input.bundle.false_share-input.baseline.false_share;
 const trueDelta=input.bundle.true_share-input.baseline.true_share;
 return {object_type:'ActionCanvasProjection',scope:'ILLUSTRATIVE_UNCALIBRATED',persistence:'READ_ONLY_NOT_IMPLEMENTATION_PLAN',bundle_mask:input.bundle.mask,nodes:[
  {stage:'PROBLEM',status:'CANONICAL_INPUT',title:copy('Problemă','Problem'),detail:copy('Problemă decizională sintetică M0: reducerea probabilității simulate de distribuire a afirmației false, păstrând pe cât posibil distribuirea afirmației adevărate.','Synthetic M0 decision problem: reduce simulated false-claim sharing probability while preserving true-claim sharing where possible.'),refs:['web/public/model/interventions.json']},
  {stage:'TARGET_MECHANISM',status:'CANONICAL_INPUT',title:copy('Mecanism țintă','Target mechanism'),detail:{ro:mechanism,en:mechanismEn},refs:selected.map(lever=>`intervention-lever:${lever.id}`)},
  {stage:'INTERVENTION',status:'CANONICAL_INPUT',title:copy('Intervenție','Intervention'),detail:{ro:interventionRo,en:interventionEn},refs:selected.map(lever=>`intervention-lever:${lever.id}`)},
  {stage:'PROXIMAL_RESULT',status:'SIMULATED_OUTPUT',title:copy('Rezultat proximal simulat','Simulated proximal result'),detail:copy(`Schimbare directă față de baseline în media pe 13 pași: ΔP(distribuire falsă) ${signed(falseDelta)}; ΔP(distribuire adevărată) ${signed(trueDelta)}. Acestea sunt outputuri ale simulării, nu efecte observate într-o populație.`,`Direct change versus baseline in the 13-step mean: ΔP(false sharing) ${signed(falseDelta)}; ΔP(true sharing) ${signed(trueDelta)}. These are simulation outputs, not observed population effects.`),refs:['web/public/model/interventions.json']},
  {stage:'INTERMEDIATE_RESULT',status:'NOT_OPERATIONALIZED',title:copy('Rezultat intermediar','Intermediate result'),detail:copy('Nu este reprezentat ca etapă distinctă executabilă sau observată în M0. Va necesita un Indicator explicit înainte de utilizarea în Reality Loop.','Not represented as a distinct executable or observed stage in M0. It requires an explicit Indicator before use in the Reality Loop.'),refs:[]},
  {stage:'FINAL_OUTCOME',status:'NOT_OPERATIONALIZED',title:copy('Rezultat final','Final outcome'),detail:copy('Nu este definit ca outcome real-world. Un ImplementationPlan real va necesita populație, context, outcome și Indicator înainte de înregistrarea observațiilor.','Not defined as a real-world outcome. A real ImplementationPlan will require population, context, outcome and an Indicator before observations can be recorded.'),refs:[]}
 ]};
}
