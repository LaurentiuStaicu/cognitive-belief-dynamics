import {addRealityLoopObject,readRealityLoopObject,readRealityLoopObjectsByIndex} from './workspace-indexeddb';
import {mountDecisionAutopsy,validateDecisionAutopsyReferences,type DecisionAutopsy} from './decision-autopsy';
import type {ImplementationPlan} from './implementation-plan';
import type {ObservedOutcome} from './observed-outcome';

type Lang='ro'|'en';
type RealityLoopRecord=ObservedOutcome|DecisionAutopsy;

function partition(records:RealityLoopRecord[]){
 return {
  outcomes:records.filter((item):item is ObservedOutcome=>item.object_type==='ObservedOutcome'),
  autopsies:records.filter((item):item is DecisionAutopsy=>item.object_type==='DecisionAutopsy')
 };
}

export async function mountPersistedDecisionAutopsy(
 host:HTMLElement,
 input:{plan:ImplementationPlan;lang:Lang}
):Promise<()=>Promise<void>>{
 const refresh=async()=>{
  const records=await readRealityLoopObjectsByIndex<RealityLoopRecord>('implementation_plan_id',input.plan.id);
  const {outcomes,autopsies}=partition(records);
  mountDecisionAutopsy(host,{
   plan:input.plan,
   outcomes,
   autopsies,
   lang:input.lang,
   persist:async record=>{
    const persistedPlan=await readRealityLoopObject<ImplementationPlan>(record.implementation_plan_id);
    if(!persistedPlan)throw new Error('referenced ImplementationPlan is not present in canonical IndexedDB storage');
    const fresh=partition(await readRealityLoopObjectsByIndex<RealityLoopRecord>('implementation_plan_id',record.implementation_plan_id));
    validateDecisionAutopsyReferences(record,persistedPlan,fresh.outcomes,fresh.autopsies);
    return addRealityLoopObject(record);
   },
   afterPersist:refresh
  });
 };
 await refresh();
 return refresh;
}
