import {createServer} from 'node:http';
import {readFile} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
import assert from 'node:assert/strict';
import {chromium} from 'playwright';

const dist=fileURLToPath(new URL('../dist/',import.meta.url));
const prefix='/cognitive-epistemic-model/';
const server=createServer(async(req,res)=>{
 try{
  const pathname=new URL(req.url,'http://localhost').pathname;
  if(!pathname.startsWith(prefix)){res.writeHead(404).end();return;}
  const file=path.resolve(dist,decodeURIComponent(pathname.slice(prefix.length))||'index.html');
  if(!file.startsWith(dist)){res.writeHead(403).end();return;}
  const data=await readFile(file);
  res.setHeader('Content-Type',({'.html':'text/html','.js':'text/javascript','.css':'text/css','.json':'application/json','.svg':'image/svg+xml'})[path.extname(file)]||'application/octet-stream');
  res.end(data);
 }catch{res.writeHead(404).end();}
});
await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
const url=`http://127.0.0.1:${server.address().port}${prefix}`;
let browser;
try{
 browser=await chromium.launch({headless:true,...(process.env.CEM_BROWSER_PATH?{executablePath:process.env.CEM_BROWSER_PATH,args:['--no-sandbox','--disable-gpu']}:{})});
 const page=await browser.newPage({viewport:{width:1440,height:1050},reducedMotion:'reduce'});
 const errors=[];
 page.on('pageerror',error=>errors.push(error.message));
 page.on('response',response=>{if(response.status()>=400)errors.push(`${response.status()} ${response.url()}`);});
 await page.goto(url);
 await page.locator('[data-suite-standard="InfoClar Model Suite Design Standard v1.1"]').waitFor();
 const initialWorkspace=JSON.parse(await page.evaluate(()=>localStorage.getItem('cem.workspace.v1.active')));
 const readIdbRecord=async(store,key)=>page.evaluate(async({store,key})=>{
  const db=await new Promise((resolve,reject)=>{const req=indexedDB.open('cem-reality-loop',1);req.onsuccess=()=>resolve(req.result);req.onerror=()=>reject(req.error);});
  try{return await new Promise((resolve,reject)=>{const tx=db.transaction(store,'readonly');const req=tx.objectStore(store).get(key);req.onsuccess=()=>resolve(req.result??null);req.onerror=()=>reject(req.error);});}
  finally{db.close();}
 },{store,key});

 await page.locator('[data-nav-group="act"]').click();
 await page.locator('[data-view="planning"]').click();
 await page.locator('#bestBundle').waitFor();
 await page.locator('[data-plan-mask="2"] [data-inspect="2"]').click();

 await page.locator('#triggerDraftForm select[name="signpost_id"]').selectOption('CEM.SIGNPOST.M0.FALSE_SHARING.MEAN13');
 await page.locator('#triggerDraftForm select[name="comparator"]').selectOption('LTE');
 await page.locator('#triggerDraftForm input[name="threshold"]').fill('0.35');
 await page.locator('#triggerDraftForm button[type="submit"]').click();
 await page.locator('#adaptivePlanForm textarea[name="then_action"]').fill('Human review of the contingent option');
 await page.locator('#adaptivePlanForm textarea[name="stop_action"]').fill('Human review before any stop decision');
 await page.locator('#adaptivePlanForm textarea[name="reassess_action"]').fill('Create a new prospective revision');
 await page.locator('#adaptivePlanForm button[type="submit"]').click();
 await page.locator('#freezeImplementationPlan').click();
 await page.waitForFunction(()=>Boolean(document.querySelector('#implementationPlanPersistenceHost')?.getAttribute('data-implementation-plan-id')));
 const planId=await page.locator('#implementationPlanPersistenceHost').getAttribute('data-implementation-plan-id');
 assert(planId?.startsWith('CEM.IMPLEMENTATION.PLAN.'));
 const frozenPlan=await readIdbRecord('reality_loop_objects',planId);
 const frozenPlanBefore=JSON.stringify(frozenPlan);

 await page.locator('#decisionAutopsy').waitFor();
 assert.equal(await page.locator('#decisionAutopsy').getAttribute('data-plan-id'),planId);
 assert.equal(await page.locator('#decisionAutopsy').getAttribute('data-mutation-policy'),'APPEND_ONLY_NO_RETROACTIVE_EDIT');
 assert.equal(await page.locator('[data-autopsy-empty]').count(),1);
 assert.equal(await page.locator('#decisionAutopsyForm button[type="submit"]').isDisabled(),true);

 await page.locator('#observedOutcomeForm [name="indicator_id"]').selectOption('CEM.INDICATOR.M0.FALSE_SHARING.MEAN13');
 await page.locator('#observedOutcomeForm [name="population_label"]').fill('Autopsy regression cohort');
 await page.locator('#observedOutcomeForm [name="population_definition"]').fill('Manual illustrative cohort for DecisionAutopsy regression');
 await page.locator('#observedOutcomeForm [name="setting"]').fill('DecisionAutopsy browser regression');
 await page.locator('#observedOutcomeForm [name="geography"]').fill('RO');
 await page.locator('#observedOutcomeForm [name="time_horizon"]').fill('30 days');
 await page.locator('#observedOutcomeForm [name="outcome_name"]').fill('Observed false-sharing probability');
 await page.locator('#observedOutcomeForm [name="outcome_definition"]').fill('Manual retrospective measurement for autopsy regression');
 await page.locator('#observedOutcomeForm [name="feature_of_interest"]').fill('autopsy regression cohort');
 await page.locator('#observedOutcomeForm [name="procedure"]').fill('manual autopsy regression measurement');
 await page.locator('#observedOutcomeForm [name="phenomenon_time"]').fill('2026-01-01T10:00');
 await page.locator('#observedOutcomeForm [name="result_time"]').fill('2026-01-01T11:00');
 await page.locator('#observedOutcomeForm [name="result_value"]').fill('0.3142');
 await page.locator('#observedOutcomeForm [name="source_refs"]').fill('source:decision-autopsy-regression');
 await page.locator('#observedOutcomeForm button[type="submit"]').click();
 await page.waitForFunction(()=>Boolean(document.querySelector('#observedOutcomeHost')?.getAttribute('data-observed-outcome-id')));
 const outcomeId=await page.locator('#observedOutcomeHost').getAttribute('data-observed-outcome-id');
 assert(outcomeId?.startsWith('CEM.OBSERVED.OUTCOME.'));
 await page.waitForFunction(id=>Boolean(document.querySelector(`#decisionAutopsyForm input[value="${id}"]`)),outcomeId);

 await page.locator(`#decisionAutopsyForm input[value="${outcomeId}"]`).check();
 await page.locator('#decisionAutopsyForm textarea[name="findings"]').fill('Manual finding based on the persisted observation');
 await page.locator('#decisionAutopsyForm select[name="proposal_target"]').selectOption('MODEL_ASSUMPTION');
 await page.locator('#decisionAutopsyForm textarea[name="proposal_rationale"]').fill('Manual rationale from retrospective review');
 await page.locator('#decisionAutopsyForm textarea[name="proposed_change"]').fill('Review the assumption in a new prospective revision');
 await page.locator('#decisionAutopsyForm select[name="proposal_status"]').selectOption('PROPOSED');
 await page.locator('#decisionAutopsyForm button[type="submit"]').click();
 await page.waitForFunction(()=>Boolean(document.querySelector('#decisionAutopsyHost')?.getAttribute('data-decision-autopsy-id')));
 const firstAutopsyId=await page.locator('#decisionAutopsyHost').getAttribute('data-decision-autopsy-id');
 assert(firstAutopsyId?.startsWith('CEM.DECISION.AUTOPSY.'));
 const firstAutopsy=await readIdbRecord('reality_loop_objects',firstAutopsyId);
 const firstAutopsyBeforeRevision=JSON.stringify(firstAutopsy);
 assert.equal(firstAutopsy.object_type,'DecisionAutopsy');
 assert.equal(firstAutopsy.case_id,initialWorkspace.case.id);
 assert.equal(firstAutopsy.implementation_plan_id,planId);
 assert.equal(firstAutopsy.decision_analysis_id,frozenPlan.decision_analysis_id);
 assert.deepEqual(firstAutopsy.observed_outcome_ids,[outcomeId]);
 assert.equal(firstAutopsy.revision_proposals[0].status,'PROPOSED');
 assert.equal(firstAutopsy.prior_prediction_mutated,false);
 assert.equal('revision_of_autopsy_id' in firstAutopsy,false);

 await page.waitForFunction(id=>Boolean(document.querySelector(`#decisionAutopsyTrail [data-autopsy-id="${id}"]`)),firstAutopsyId);
 await page.locator(`#decisionAutopsyForm input[value="${outcomeId}"]`).check();
 await page.locator('#decisionAutopsyForm select[name="revision_of_autopsy_id"]').selectOption(firstAutopsyId);
 await page.locator('#decisionAutopsyForm textarea[name="findings"]').fill('Second manual review creates a new autopsy entity');
 await page.locator('#decisionAutopsyForm select[name="proposal_target"]').selectOption('IMPLEMENTATION_PLAN');
 await page.locator('#decisionAutopsyForm textarea[name="proposal_rationale"]').fill('Manual decision to revise the prospective plan');
 await page.locator('#decisionAutopsyForm textarea[name="proposed_change"]').fill('Create a separate ImplementationPlan revision later');
 await page.locator('#decisionAutopsyForm select[name="proposal_status"]').selectOption('ACCEPTED');
 await page.locator('#decisionAutopsyForm button[type="submit"]').click();
 await page.waitForFunction(old=>{const value=document.querySelector('#decisionAutopsyHost')?.getAttribute('data-decision-autopsy-id');return Boolean(value&&value!==old);},firstAutopsyId);
 const secondAutopsyId=await page.locator('#decisionAutopsyHost').getAttribute('data-decision-autopsy-id');
 const secondAutopsy=await readIdbRecord('reality_loop_objects',secondAutopsyId);
 assert.equal(secondAutopsy.revision_of_autopsy_id,firstAutopsyId);
 assert.equal(secondAutopsy.revision_proposals[0].status,'ACCEPTED');
 assert.equal(secondAutopsy.prior_prediction_mutated,false);
 assert.equal(JSON.stringify(await readIdbRecord('reality_loop_objects',firstAutopsyId)),firstAutopsyBeforeRevision);
 assert.equal(JSON.stringify(await readIdbRecord('reality_loop_objects',planId)),frozenPlanBefore);
 assert.equal(errors.length,0,errors.join('\n'));
}finally{
 if(browser)await browser.close();
 await new Promise(resolve=>server.close(resolve));
}
