type Lang='ro'|'en';
type Copy=Record<Lang,string>;

export type ActionCanvasStatus='CANONICAL_INPUT'|'SIMULATED_OUTPUT'|'NOT_OPERATIONALIZED';
export type ActionCanvasStage='PROBLEM'|'TARGET_MECHANISM'|'INTERVENTION'|'PROXIMAL_RESULT'|'INTERMEDIATE_RESULT'|'FINAL_OUTCOME';

export type ActionCanvasLever={
 id:string;
 bit:number;
 label:Copy;
 factor:string;
 action:Copy;
};

export type ActionCanvasBundle={
 mask:number;
 false_share:number;
 true_share:number;
};

export type ActionCanvasNode={
 stage:ActionCanvasStage;
 status:ActionCanvasStatus;
 title:Copy;
 detail:Copy;
 refs:string[];
};

export type ActionCanvasProjection={
 object_type:'ActionCanvasProjection';
 scope:'ILLUSTRATIVE_UNCALIBRATED';
 persistence:'READ_ONLY_NOT_IMPLEMENTATION_PLAN';
 bundle_mask:number;
 nodes:ActionCanvasNode[];
};

const copy=(ro:string,en:string):Copy=>({ro,en});
const signed=(value:number)=>value>0?`+${value.toFixed(4)}`:value.toFixed(4);

export function buildActionCanvasProjection(input:{
 bundle:ActionCanvasBundle;
 baseline:ActionCanvasBundle;
 levers:ActionCanvasLever[];
}):ActionCanvasProjection{
 const selected=input.levers.filter(lever=>(input.bundle.mask&lever.bit)!==0);
 const mechanism=selected.length
  ?selected.map(lever=>`${lever.label.ro}: ${lever.factor}`).join(' · ')
  :'Nicio măsură activă; nu este selectată o cale mecanistică de intervenție.';
 const mechanismEn=selected.length
  ?selected.map(lever=>`${lever.label.en}: ${lever.factor}`).join(' · ')
  :'No active measure; no intervention mechanism path is selected.';
 const interventionRo=selected.length?selected.map(lever=>lever.action.ro).join(' · '):'Fără măsuri; rulează numai condițiile de bază ale simulării.';
 const interventionEn=selected.length?selected.map(lever=>lever.action.en).join(' · '):'No measures; only the simulation baseline conditions run.';
 const falseDelta=input.bundle.false_share-input.baseline.false_share;
 const trueDelta=input.bundle.true_share-input.baseline.true_share;
 return {
  object_type:'ActionCanvasProjection',
  scope:'ILLUSTRATIVE_UNCALIBRATED',
  persistence:'READ_ONLY_NOT_IMPLEMENTATION_PLAN',
  bundle_mask:input.bundle.mask,
  nodes:[
   {
    stage:'PROBLEM',status:'CANONICAL_INPUT',
    title:copy('Problemă','Problem'),
    detail:copy(
     'Problemă decizională sintetică M0: reducerea probabilității simulate de distribuire a afirmației false, păstrând pe cât posibil distribuirea afirmației adevărate.',
     'Synthetic M0 decision problem: reduce simulated false-claim sharing probability while preserving true-claim sharing where possible.'
    ),
    refs:['web/public/model/interventions.json']
   },
   {
    stage:'TARGET_MECHANISM',status:'CANONICAL_INPUT',
    title:copy('Mecanism țintă','Target mechanism'),
    detail:{ro:mechanism,en:mechanismEn},
    refs:selected.map(lever=>`intervention-lever:${lever.id}`)
   },
   {
    stage:'INTERVENTION',status:'CANONICAL_INPUT',
    title:copy('Intervenție','Intervention'),
    detail:{ro:interventionRo,en:interventionEn},
    refs:selected.map(lever=>`intervention-lever:${lever.id}`)
   },
   {
    stage:'PROXIMAL_RESULT',status:'SIMULATED_OUTPUT',
    title:copy('Rezultat proximal simulat','Simulated proximal result'),
    detail:copy(
     `Schimbare directă față de baseline în media pe 13 pași: ΔP(distribuire falsă) ${signed(falseDelta)}; ΔP(distribuire adevărată) ${signed(trueDelta)}. Acestea sunt outputuri ale simulării, nu efecte observate într-o populație.`,
     `Direct change versus baseline in the 13-step mean: ΔP(false sharing) ${signed(falseDelta)}; ΔP(true sharing) ${signed(trueDelta)}. These are simulation outputs, not observed population effects.`
    ),
    refs:['web/public/model/interventions.json']
   },
   {
    stage:'INTERMEDIATE_RESULT',status:'NOT_OPERATIONALIZED',
    title:copy('Rezultat intermediar','Intermediate result'),
    detail:copy(
     'Nu este reprezentat ca etapă distinctă executabilă sau observată în M0. Va necesita un Indicator explicit înainte de utilizarea în Reality Loop.',
     'Not represented as a distinct executable or observed stage in M0. It requires an explicit Indicator before use in the Reality Loop.'
    ),
    refs:[]
   },
   {
    stage:'FINAL_OUTCOME',status:'NOT_OPERATIONALIZED',
    title:copy('Rezultat final','Final outcome'),
    detail:copy(
     'Nu este definit ca outcome real-world. Un ImplementationPlan real va necesita populație, context, outcome și Indicator înainte de înregistrarea observațiilor.',
     'Not defined as a real-world outcome. A real ImplementationPlan will require population, context, outcome and an Indicator before observations can be recorded.'
    ),
    refs:[]
   }
  ]
 };
}

const esc=(value:string)=>value.replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot',"'":'&#39;'}[c]??c));

export function renderActionCanvas(canvas:ActionCanvasProjection,lang:Lang):string{
 const t=(ro:string,en:string)=>lang==='ro'?ro:en;
 return `<section class="action-canvas" id="actionCanvas" data-action-canvas-mask="${canvas.bundle_mask}">
  <div class="section-heading"><div><p class="eyebrow">OA-7 · ACTION CANVAS</p><h4>${t('De la problemă la outcome — fără a inventa verigi lipsă','From problem to outcome — without inventing missing links')}</h4><p>${t('Aceasta este o proiecție read-only a bundle-ului inspectat. Nu este încă un ImplementationPlan și nu este salvată în Workspace.','This is a read-only projection of the inspected bundle. It is not yet an ImplementationPlan and is not stored in Workspace.')}</p></div><span class="action-canvas-scope">${canvas.scope}</span></div>
  <ol class="action-canvas-chain">${canvas.nodes.map(node=>`<li data-action-stage="${node.stage}" data-action-status="${node.status}"><div class="action-canvas-stage"><span>${esc(node.title[lang])}</span><code>${node.status}</code></div><p>${esc(node.detail[lang])}</p></li>`).join('')}</ol>
  <div class="boundary"><strong>${t('Limită Reality Loop','Reality Loop boundary')}</strong><p>${t('Numai rezultatul proximal este derivat direct din outputul M0. Rezultatul intermediar și outcome-ul final rămân neoperationalizate până când Indicator objects sunt definite într-un slice separat.','Only the proximal result is derived directly from M0 output. The intermediate result and final outcome remain unoperationalized until Indicator objects are defined in a separate slice.')}</p></div>
 </section>`;
}
