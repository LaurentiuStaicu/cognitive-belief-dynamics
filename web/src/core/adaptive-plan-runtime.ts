import type {SignpostDefinition,TriggerDraft} from './signposts-triggers';

type Lang='ro'|'en';
type Copy=Record<Lang,string>;
export type AdaptivePhase='NOW'|'WATCH'|'IF'|'THEN'|'STOP'|'REASSESS';
export type AdaptiveStepReadiness='DEFINED'|'MISSING_TRIGGER'|'MISSING_ACTION';
export type StructuredTriggerCondition={indicator_id:string;comparator:TriggerDraft['comparator'];threshold:number;unit:TriggerDraft['unit'];origin:TriggerDraft['origin']};
export type AdaptivePlanStep={id:string;phase:AdaptivePhase;statement:Copy;readiness:AdaptiveStepReadiness;indicator_id?:string;trigger_draft_id?:string;trigger_condition?:Copy;trigger?:StructuredTriggerCondition;action?:Copy};
export type AdaptivePlanDraft={object_type:'AdaptivePlanDraft';status:'DRAFT';persistence:'EPHEMERAL_NOT_WORKSPACE';execution_status:'DESIGN_ONLY_NO_OBSERVED_OUTCOME';automation:'NO_AUTOMATIC_ACTIONS';bundle_label:Copy;trigger_draft_id?:string;steps:AdaptivePlanStep[]};
export type AdaptiveActionInputs={then_action:Copy;stop_action:Copy;reassess_action:Copy};

const copy=(ro:string,en:string):Copy=>({ro,en});
const comparator=(value:TriggerDraft['comparator'])=>({LT:'<',LTE:'≤',GTE:'≥',GT:'>'}[value]);
const nonEmptyCopy=(value:Copy)=>value.ro.trim().length>0&&value.en.trim().length>0;

export function buildAdaptivePlanDraft(input:{bundle_label:Copy;signpost?:SignpostDefinition;trigger?:TriggerDraft;actions?:AdaptiveActionInputs}):AdaptivePlanDraft{
 const triggerCondition=input.trigger?copy(`${input.trigger.indicator_id} ${comparator(input.trigger.comparator)} ${input.trigger.threshold.toFixed(2)} (prag declarat de utilizator; de evaluat numai pe observații)`,`${input.trigger.indicator_id} ${comparator(input.trigger.comparator)} ${input.trigger.threshold.toFixed(2)} (user-declared threshold; evaluate only on observations)`):undefined;
 const actionReady=input.actions!==undefined&&nonEmptyCopy(input.actions.then_action)&&nonEmptyCopy(input.actions.stop_action)&&nonEmptyCopy(input.actions.reassess_action);
 const steps:AdaptivePlanStep[]=[
  {id:'CEM.ADAPTIVE.RUNTIME.NOW',phase:'NOW',statement:copy(`Acum: păstrează ca opțiune inspectată bundle-ul „${input.bundle_label.ro}”; aceasta este o proiecție de plan, nu implementare reală.`,`Now: retain inspected bundle “${input.bundle_label.en}” as the current option; this is a plan projection, not real-world implementation.`),readiness:'DEFINED'},
  {id:'CEM.ADAPTIVE.RUNTIME.WATCH',phase:'WATCH',statement:input.signpost?copy(`Urmărește indicatorul ${input.signpost.indicator_id}.`,`Watch indicator ${input.signpost.indicator_id}.`):copy('Niciun signpost selectat.','No signpost selected.'),readiness:input.signpost?'DEFINED':'MISSING_TRIGGER',...(input.signpost?{indicator_id:input.signpost.indicator_id}:{})},
  {id:'CEM.ADAPTIVE.RUNTIME.IF',phase:'IF',statement:triggerCondition??copy('Definește mai întâi un trigger draft.','Define a trigger draft first.'),readiness:input.trigger?'DEFINED':'MISSING_TRIGGER',...(input.trigger?{trigger_draft_id:input.trigger.id,trigger_condition:triggerCondition,trigger:{indicator_id:input.trigger.indicator_id,comparator:input.trigger.comparator,threshold:input.trigger.threshold,unit:input.trigger.unit,origin:input.trigger.origin}}:{})},
  {id:'CEM.ADAPTIVE.RUNTIME.THEN',phase:'THEN',statement:actionReady?input.actions!.then_action:copy('Declară acțiunea contingentă care ar trebui reconsiderată dacă trigger-ul este confirmat.','Declare the contingent action to reconsider if the trigger is confirmed.'),readiness:actionReady?'DEFINED':'MISSING_ACTION',...(actionReady?{action:input.actions!.then_action}:{})},
  {id:'CEM.ADAPTIVE.RUNTIME.STOP',phase:'STOP',statement:actionReady?input.actions!.stop_action:copy('Declară regula/acțiunea de oprire.','Declare the stop rule/action.'),readiness:actionReady?'DEFINED':'MISSING_ACTION',...(actionReady?{action:input.actions!.stop_action}:{})},
  {id:'CEM.ADAPTIVE.RUNTIME.REASSESS',phase:'REASSESS',statement:actionReady?input.actions!.reassess_action:copy('Declară cum ar trebui reevaluată decizia.','Declare how the decision should be reassessed.'),readiness:actionReady?'DEFINED':'MISSING_ACTION',...(actionReady?{action:input.actions!.reassess_action}:{})}
 ];
 return {object_type:'AdaptivePlanDraft',status:'DRAFT',persistence:'EPHEMERAL_NOT_WORKSPACE',execution_status:'DESIGN_ONLY_NO_OBSERVED_OUTCOME',automation:'NO_AUTOMATIC_ACTIONS',bundle_label:input.bundle_label,...(input.trigger?{trigger_draft_id:input.trigger.id}:{}),steps};
}
