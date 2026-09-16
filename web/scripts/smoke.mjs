import {createServer} from 'node:http';
import {readFile, mkdir} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
import assert from 'node:assert/strict';
import {chromium} from 'playwright';
const dist=fileURLToPath(new URL('../dist/',import.meta.url));
const prefix='/cognitive-epistemic-model/';
const server=createServer(async(req,res)=>{
 try {
  const pathname=new URL(req.url,'http://localhost').pathname;
  if(!pathname.startsWith(prefix)){res.writeHead(404).end();return;}
  const file=path.resolve(dist,decodeURIComponent(pathname.slice(prefix.length))||'index.html');
  if(!file.startsWith(dist)){res.writeHead(403).end();return;}
  const data=await readFile(file);
  res.setHeader('Content-Type',({'.html':'text/html','.js':'text/javascript','.css':'text/css','.json':'application/json','.svg':'image/svg+xml'})[path.extname(file)]||'application/octet-stream');res.end(data);
 }catch{res.writeHead(404).end();}
});
await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
const url=`http://127.0.0.1:${server.address().port}${prefix}`;
let browser;
try {
 browser=await chromium.launch({headless:true, ...(process.env.CEM_BROWSER_PATH ? {executablePath:process.env.CEM_BROWSER_PATH, args:['--no-sandbox','--disable-gpu']} : {})});
 const page=await browser.newPage({viewport:{width:1440,height:1050},reducedMotion:'reduce'});
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 const domainForView={learning:'understand',structure:'understand',process:'understand',runs:'analyze',comparison:'analyze',planning:'act',reference:'library'};
 const openView=async view=>{
  const domain=domainForView[view];
  assert(domain,`missing IA domain for view ${view}`);
  await page.locator(`[data-nav-group="${domain}"]`).click();
  await page.locator(`[data-view="${view}"]`).click();
 };
 const waitTheory=()=>page.waitForFunction(()=>document.querySelector('#theoryArticle')?.getAttribute('aria-busy')==='false');
 page.on('response',r=>{if(r.status()>=400)errors.push(`${r.status()} ${r.url()}`)});
 await page.goto(url);await waitTheory();
 const workspaceKey='cem.workspace.v1.active';
 const workspaceBeforeReload=await page.evaluate(key=>localStorage.getItem(key),workspaceKey);
 assert(workspaceBeforeReload);
 const initialWorkspace=JSON.parse(workspaceBeforeReload);
 assert.equal(initialWorkspace.schema_version,'1');
 assert.equal(initialWorkspace.versions.software_version,'0.4.2a0');
 assert.equal(initialWorkspace.versions.model_specification,'M1');
 assert.equal(initialWorkspace.versions.evidence_snapshot,'EVIDENCE.M1.2026-09-16.r1');
 assert.deepEqual(initialWorkspace.case.entity_refs,[]);
 assert.deepEqual(initialWorkspace.case.relation_refs,[]);
 assert.equal(initialWorkspace.provenance.activities.at(-1).type,'CREATE');
 await page.reload();await waitTheory();
 assert.equal(await page.evaluate(key=>localStorage.getItem(key),workspaceKey),workspaceBeforeReload);
 const version=JSON.parse(await readFile(path.join(dist,'model/version.json'),'utf8'));
 assert.match(await page.locator('#releaseVersion').textContent(),new RegExp(version.version.replaceAll('.', '\\.')));
 assert((await page.locator('#releaseVersion').getAttribute('href')).endsWith('/'+version.release_tag));
 assert.equal(await page.locator('search.global-search').count(),1);
 assert.equal(await page.locator('#semanticSearchInput').getAttribute('type'),'search');
 assert.equal(await page.locator('label[for="semanticSearchInput"]').count(),1);
 assert.equal(await page.locator('[role="combobox"],[role="listbox"],[role="option"]').count(),0);
 await page.locator('#semanticSearchInput').fill('familiaritate');
 await page.locator('#semanticSearchForm button[type="submit"]').click();
 await page.locator('[data-search-result-id="VAR.FAMILIARITY.CLAIM"]').waitFor();
 assert.match(await page.locator('#semanticSearchSummary').textContent(),/rezultate semantice/);
 await page.locator('[data-search-result-id="VAR.FAMILIARITY.CLAIM"] [data-search-inspect-id]').click();
 assert.equal(await page.locator('aside#semanticInspector').count(),1);
 assert.equal(await page.locator('#semanticInspector').getAttribute('data-inspector-kind'),'entity');
 assert.equal(await page.locator('#semanticInspector').getAttribute('data-inspector-id'),'VAR.FAMILIARITY.CLAIM');
 assert.equal(await page.evaluate(()=>document.activeElement?.id),'semanticInspector');
 assert.match(await page.locator('#semanticInspector').textContent(),/VAR\.FAMILIARITY\.CLAIM/);
 assert.equal(await page.locator('#semanticInspector [role="dialog"]').count(),0);
 const firstRelation=page.locator('#semanticInspector [data-inspect-id]').first();
 await firstRelation.click();
 assert.equal(await page.locator('#semanticInspector').getAttribute('data-inspector-kind'),'relation');
 assert.match(await page.locator('#semanticInspector .eyebrow').textContent(),/Relație|Dependență|documentație/i);
 const sourceButton=page.locator('#semanticInspector .inspector-endpoints [data-inspect-id]').first();
 await sourceButton.click();
 assert.equal(await page.locator('#semanticInspector').getAttribute('data-inspector-kind'),'entity');

 assert.doesNotMatch(await page.locator('#semanticSearchResults').textContent(),/retrievalScore|1000|950|900/);
 const searchValueBeforeNav=await page.locator('#semanticSearchInput').inputValue();
 await page.locator('[data-nav-group="analyze"]').click();
 assert.equal(await page.locator('#semanticSearchInput').inputValue(),searchValueBeforeNav);
 assert.equal(await page.locator('[data-search-result-id="VAR.FAMILIARITY.CLAIM"]').count(),1);
 assert.notEqual(await page.locator('#semanticInspector').getAttribute('data-inspector-id'),'');
 await page.locator('[data-nav-group="understand"]').click();
 await waitTheory();
 const visualTokens=await page.evaluate(()=>{
  const css=getComputedStyle(document.documentElement);
  return {
   unit:css.getPropertyValue('--vl-space-unit').trim(),
   margin:css.getPropertyValue('--vl-content-margin-min').trim(),
   reader:css.getPropertyValue('--vl-reader-max').trim(),
   target:css.getPropertyValue('--vl-target-min').trim()
  };
 });
 assert.deepEqual(visualTokens,{unit:'6px',margin:'12px',reader:'72ch',target:'44px'});
 const domainBox=await page.locator('[data-nav-group="understand"]').boundingBox();
 assert(domainBox&&domainBox.height>=44,'primary domain target must remain at least 44px high');
 await page.locator('[data-nav-group="understand"]').focus();
 assert(Number.parseFloat(await page.locator('[data-nav-group="understand"]').evaluate(el=>getComputedStyle(el).outlineWidth))>=3,'visible focus ring must be at least 3px');
 assert.equal(await page.locator('[data-nav-group]').count(),4);
 assert.equal(await page.locator('[data-nav-group="understand"]').getAttribute('aria-pressed'),'true');
 assert.equal(await page.locator('.views [data-view]').count(),3);
 assert.equal(await page.locator('[data-view="learning"]').getAttribute('aria-pressed'),'true');
 await page.locator('[data-nav-group="analyze"]').click();
 await page.locator('[data-view="runs"]').waitFor();
 assert.equal(await page.locator('[data-nav-group="analyze"]').getAttribute('aria-pressed'),'true');
 assert.equal(await page.locator('.views [data-view]').count(),2);
 assert.equal(await page.locator('[data-view="runs"]').getAttribute('aria-pressed'),'true');
 await page.locator('[data-nav-group="act"]').click();
 await page.locator('[data-view="planning"]').waitFor();
 assert.equal(await page.locator('.views [data-view]').count(),1);
 await page.locator('[data-nav-group="library"]').click();
 await page.locator('[data-view="reference"]').waitFor();
 assert.equal(await page.locator('.views [data-view]').count(),1);
 await page.locator('[data-nav-group="understand"]').click();
 await waitTheory();
 assert.equal(await page.locator('[data-understanding-mode]').count(),4);
 assert.equal(await page.locator('[data-understanding-mode="theory"]').getAttribute('aria-pressed'),'true');
 assert.equal(await page.locator('[data-theory-chapter]').count(),16);
 const theoryMeasure=await page.locator('#theoryArticle p').first().evaluate(el=>({
  maxWidth:getComputedStyle(el).maxWidth,
  width:el.getBoundingClientRect().width
 }));
 assert.notEqual(theoryMeasure.maxWidth,'none');
 assert(Number.parseFloat(theoryMeasure.maxWidth)<=800,'Theory reader max-width must remain constrained');
 assert(theoryMeasure.width<=800,'Theory prose must not expand beyond the reader measure');
 assert((await page.locator('.theory-statuses [data-status]').count())>0);
 assert.notEqual(await page.locator('.theory-statuses [data-status]').first().evaluate(el=>getComputedStyle(el,'::before').content),'none');
 assert.match(await page.locator('#theoryArticle').textContent(),/Ce este Cognitive Epistemic Model/);

 // OA-5B: explicit Predict -> Reveal -> Explain -> Boundary flow, local bounded history and skip.
 await page.evaluate(()=>{location.hash='#understanding/active/AU-1';});
 await page.locator('#activeUnderstandingTitle').getByText('Înțelegere activă',{exact:true}).waitFor();
 assert.equal(await page.locator('[data-au-challenge]').count(),3);
 assert.equal(await page.locator('[data-au-challenge="AU-1"]').getAttribute('aria-current'),'step');
 assert.equal(await page.locator('[data-au-stage="REVEAL"]').count(),0);
 await page.locator('[data-au-start]').click();
 await page.locator('input[name="auPrediction"][value="INCREASE"]').check();
 await page.selectOption('#activeConfidence','medium');
 await page.locator('[data-au-submit]').click();
 assert.equal(await page.locator('#activeChallengeStage').getAttribute('data-au-stage'),'REVEAL');
 assert.match(await page.locator('#activeChallengeStage').textContent(),/Crește/);
 assert.match(await page.locator('#activeChallengeStage').textContent(),/coincide/);
 const activeHistory=await page.evaluate(()=>JSON.parse(localStorage.getItem('cem.active-understanding.history.v1')??'{"records":[]}'));
 assert.equal(activeHistory.schema_version,'1');
 assert.equal(activeHistory.records.length,1);
 assert.deepEqual(Object.keys(activeHistory.records[0]).sort(),['canonical_target_refs','challenge_id','confidence','outcome_category','prediction_category','timestamp']);
 assert.equal(activeHistory.records[0].challenge_id,'AU-1');
 assert.equal(activeHistory.records[0].confidence,'medium');
 await page.locator('[data-au-explain]').click();
 assert.match(await page.locator('#activeChallengeStage').textContent(),/Expunerea este evenimentul/);
 await page.locator('[data-au-boundary]').click();
 assert.match(await page.locator('#activeChallengeStage').textContent(),/Familiaritatea nu este adevăr/);
 await page.locator('[data-au-complete]').click();
 assert.match(await page.locator('#activeChallengeStage').textContent(),/SECVENȚĂ COMPLETĂ/);
 await page.locator('[data-au-challenge="AU-2"]').click();
 await page.waitForURL(/#understanding\/active\/AU-2$/);
 await page.locator('[data-au-start]').click();
 await page.locator('[data-au-skip]').click();
 assert.match(await page.locator('#activeChallengeStage').textContent(),/fără a salva o predicție/);
 assert.equal((await page.evaluate(()=>JSON.parse(localStorage.getItem('cem.active-understanding.history.v1')).records.length)),1);

 // OA-5D: Theory, Search and Universal Inspector cross-links preserve semantic identity and explicit focus.
 assert.equal(await page.locator('[data-au-open-theory]').count(),1);
 assert.equal(await page.locator('[data-au-search-canonical]').count(),1);
 assert.equal(await page.locator('[data-au-inspect-canonical]').count(),1);
 await page.locator('[data-au-search-canonical]').click();
 assert.equal(await page.locator('#semanticSearchInput').inputValue(),'COMP.NODE.ACCURACY_CUE_INPUT');
 assert.equal(await page.locator('#semanticSearchInput').evaluate(el=>document.activeElement===el),true);
 assert.equal(await page.locator('[data-search-result-id="COMP.NODE.ACCURACY_CUE_INPUT"]').count(),1);
 assert.equal(await page.locator('#activeChallengeStage').getAttribute('data-au-stage'),'REVEAL');
 await page.locator('[data-au-inspect-canonical]').click();
 assert.equal(await page.locator('#semanticInspector').getAttribute('data-inspector-id'),'COMPDEP.ACCURACY_CUE.ACCURACY_SALIENCE');
 assert.equal(await page.locator('#semanticInspector').getAttribute('data-inspector-kind'),'relation');
 assert.equal(await page.locator('#semanticInspector').evaluate(el=>document.activeElement===el),true);
 assert.equal(await page.locator('#activeChallengeStage').getAttribute('data-au-stage'),'REVEAL');
 await page.locator('[data-au-open-theory]').click();
 await page.waitForURL(/#understanding\/theory\/belief-accuracy-action$/);
 await waitTheory();
 assert.equal(await page.locator('#theoryArticle').evaluate(el=>document.activeElement===el),true);
 assert.match(await page.locator('#theoryArticle').textContent(),/Convingere, atenție la acuratețe și acțiune/);
 await page.goBack();
 await page.waitForURL(/#understanding\/active\/AU-2$/);
 await page.locator('#activeUnderstandingTitle').waitFor();

 await page.evaluate(()=>{location.hash='#understanding/active/challenge-model';});
 await page.locator('[data-challenge-model="M1.E3"]').waitFor();
 await page.locator('[data-au-cm-search]').click();
 assert.equal(await page.locator('#semanticSearchInput').inputValue(),'VAR.HEADLINE.NEGATIVITY');
 assert.equal(await page.locator('#semanticSearchInput').evaluate(el=>document.activeElement===el),true);
 await page.locator('[data-au-cm-inspect]').click();
 assert.equal(await page.locator('#semanticInspector').getAttribute('data-inspector-id'),'VAR.ACCESS.PROBABILITY');
 assert.equal(await page.locator('#semanticInspector').evaluate(el=>document.activeElement===el),true);
 await page.locator('[data-au-cm-theory]').click();
 await page.waitForURL(/#understanding\/theory\/algorithms-social-feedback$/);
 await waitTheory();
 assert.equal(await page.locator('#theoryArticle').evaluate(el=>document.activeElement===el),true);
 await page.goBack();
 await page.waitForURL(/#understanding\/active\/challenge-model$/);
 await page.locator('[data-challenge-model="M1.E3"]').waitFor();

 await page.evaluate(()=>{location.hash='#understanding/active/AU-2';});
 await page.locator('#activeUnderstandingTitle').waitFor();
 await page.locator('[data-au-clear-history]').click();
 assert.equal(await page.evaluate(()=>localStorage.getItem('cem.active-understanding.history.v1')),null);
 assert.match(await page.locator('#activeHistory').textContent(),/Nicio predicție salvată/);
 await page.locator('#language').click();
 assert.equal(await page.locator('html').getAttribute('lang'),'en');
 await page.locator('#activeUnderstandingTitle').getByText('Active Understanding',{exact:true}).waitFor();
 assert.match(await page.locator('#activeChallengeStage').textContent(),/accuracy cue/i);
 await page.locator('#language').click();
 await page.locator('[data-understanding-mode="theory"]').click();
 await waitTheory();

 // Alpha 0.4.1a1 Phase D: guided journey is deep-linkable, bilingual and returns from real app surfaces.
 await page.evaluate(()=>{location.hash='#understanding/tour/orientation';});
 await page.locator('#guidedTourTitle').getByText('1. Începe cu întrebarea modelului',{exact:true}).waitFor();
 assert.equal(await page.locator('[data-tour-step]').count(),10);
 assert.equal(await page.locator('[data-tour-step="orientation"]').getAttribute('aria-current'),'step');
 assert.equal(await page.locator('.tour-progress progress').getAttribute('value'),'1');
 if(process.env.CEM_SCREENSHOTS){
  await mkdir(process.env.CEM_SCREENSHOTS,{recursive:true});
  await page.screenshot({path:path.join(process.env.CEM_SCREENSHOTS,'guided-tour-ro.png'),fullPage:true});
 }
 await page.locator('[data-tour-next]').click();
 await page.waitForURL(/#understanding\/tour\/causal-chain$/);
 assert.equal(await page.locator('.tour-progress progress').getAttribute('value'),'2');
 await page.locator('[data-tour-step="mechanism"]').click();
 await page.waitForURL(/#understanding\/tour\/mechanism$/);
 await page.locator('[data-tour-open]').click();
 await page.waitForURL(/#understanding\/mechanisms\/repetition$/);
 await page.locator('#mechanismReading').waitFor();
 await page.goBack();
 await page.waitForURL(/#understanding\/tour\/mechanism$/);
 await page.locator('#guidedTourTitle').getByText('3. Urmărește un mecanism executabil',{exact:true}).waitFor();
 await page.evaluate(()=>{location.hash='#understanding/tour/scenario';});
 await page.locator('#guidedTourTitle').getByText('5. Verifică mecanismul într-un scenariu',{exact:true}).waitFor();
 await page.locator('[data-tour-open]').click();
 await page.locator('#scenario').waitFor();
 assert.equal(await page.locator('#scenario').inputValue(),'repetition');
 assert.equal(await page.locator('#timeline').inputValue(),'4');
 await page.goBack();
 await page.waitForURL(/#understanding\/tour\/scenario$/);
 await page.locator('#guidedTourTitle').getByText('5. Verifică mecanismul într-un scenariu',{exact:true}).waitFor();
 await page.locator('#language').click();
 assert.equal(await page.locator('html').getAttribute('lang'),'en');
 await page.locator('#guidedTourTitle').getByText('5. Check the mechanism in a scenario',{exact:true}).waitFor();
 if(process.env.CEM_SCREENSHOTS)await page.screenshot({path:path.join(process.env.CEM_SCREENSHOTS,'guided-tour-en.png'),fullPage:true});
 await page.locator('#language').click();
 assert.equal(await page.locator('html').getAttribute('lang'),'ro');

 await page.evaluate(()=>{location.hash='#understanding/theory/repetition-familiarity-truth';});
 await waitTheory();
 await page.locator('[data-theory-chapter="repetition-familiarity-truth"]').click();
 await page.waitForURL(/#understanding\/theory\/repetition-familiarity-truth$/);
 await page.locator('#theoryArticle').getByText('Repetiție, familiaritate și adevăr perceput',{exact:true}).waitFor();
 if(process.env.CEM_SCREENSHOTS){
  await mkdir(process.env.CEM_SCREENSHOTS,{recursive:true});
  await page.screenshot({path:path.join(process.env.CEM_SCREENSHOTS,'theory-ro.png'),fullPage:true});
 }
 await page.locator('#language').click();
 await waitTheory();
 assert.equal(await page.locator('html').getAttribute('lang'),'en');
 await page.locator('#theoryArticle').getByText('Repetition, familiarity and judged truth',{exact:true}).waitFor();
 if(process.env.CEM_SCREENSHOTS)await page.screenshot({path:path.join(process.env.CEM_SCREENSHOTS,'theory-en.png'),fullPage:true});
 await page.locator('#language').click();
 await waitTheory();
 assert.equal(await page.locator('html').getAttribute('lang'),'ro');
 await page.locator('#theoryArticle').getByText('Repetiție, familiaritate și adevăr perceput',{exact:true}).waitFor();
 await page.locator('[data-theory-token-kind="VAR"][data-theory-token-value="F"]').first().click();
 assert.match(await page.locator('#theoryInspector').textContent(),/Familiaritatea afirmației/);
 await page.locator('#theoryInspector [data-theory-open-view^="reference:"]').click();
 const registryItem=page.locator('[data-registry-id="VAR.FAMILIARITY.CLAIM"]');
 await registryItem.waitFor();
 assert.equal(await registryItem.evaluate(el=>document.activeElement===el),true);
 await page.goBack();
 await waitTheory();
 assert.match(await page.locator('#theoryArticle').textContent(),/Repetiție, familiaritate și adevăr perceput/);
 await page.goForward();
 await registryItem.waitFor();
 assert.equal(await registryItem.evaluate(el=>document.activeElement===el),true);
 await page.goBack();
 await waitTheory();
 await page.locator('[data-theory-token-kind="MECH"][data-theory-token-value="repetition"]').first().click();
 await page.locator('#theoryInspector [data-theory-open-mechanism="repetition"]').click();
 await page.waitForURL(/#understanding\/mechanisms\/repetition$/);
 await page.locator('#mechanismReading').waitFor();
 assert.equal(await page.locator('.learning-factors article').count(),7);
 await page.evaluate(()=>{location.hash='#understanding/theory/algorithms-social-feedback';});
 await waitTheory();
 await page.locator('[data-theory-token-kind="MECH"][data-theory-token-value="access"]').first().click();
 await page.locator('#theoryInspector [data-theory-open-mechanism="access"]').click();
 await page.waitForURL(/#understanding\/mechanisms\/access$/);
 await page.locator('#m1AccessStage').waitFor();
 await page.waitForFunction(()=>document.activeElement?.id==='m1AccessStage');
 assert.equal(await page.locator('#m1AccessStage').evaluate(el=>document.activeElement===el),true);
 // Alpha 0.4 Narrative Laboratory: explanation state is local until the user explicitly opens the full scenario.
 await page.locator('#narrativeStage').waitFor();
 assert.match(await page.locator('#narrativeStage').textContent(),/Repetiție și familiaritate/);
 assert.equal(await page.locator('[data-narrative-step]').count(),13);
 await page.locator('[data-mechanism="correction"]').click();
 assert.match(await page.locator('#narrativeStage').textContent(),/Corecție și diminuarea accesibilității/);
 assert.equal(await page.locator('[data-narrative-step="5"]').getAttribute('aria-current'),'step');
 await page.locator('[data-narrative-step="7"]').click();
 assert.equal(await page.locator('[data-narrative-step="7"]').getAttribute('aria-current'),'step');
 await page.locator('[data-inspect-variable="C"]').click();
 assert.match(await page.locator('#narrativeStage').textContent(),/Valoare la pasul 7/);
 assert.match(await page.locator('#narrativeStage').textContent(),/nu garantează schimbarea convingerii/i);
 await page.locator('#narrativeBack').click();
 await page.locator('[data-narrative-step="7"]').click();
 await page.locator('#narrativeOpenRun').click();
 assert.equal(await page.locator('#scenario').inputValue(),'correction');
 assert.equal(await page.locator('#timeline').inputValue(),'7');
 await openView('learning');
 await page.locator('#m1EditorialStage').waitFor();
 assert.equal(await page.locator('[data-m1-condition]').count(),3);
 assert.match(await page.locator('#m1EditorialStage').textContent(),/Benchmark empiric|Empirical benchmark/);
 assert.match(await page.locator('#m1EditorialStage').textContent(),/2\.141|2,141/);
 await page.locator('[data-m1-condition="neutral"]').click();
 assert.equal(await page.locator('[data-m1-condition="neutral"]').getAttribute('aria-pressed'),'true');
 assert.match(await page.locator('#m1EditorialStage').textContent(),/Sobs/);
 await page.locator('#m1PresentationStage').waitFor();
 assert.equal(await page.locator('[data-m1e2-audience]').count(),2);
 assert.match(await page.locator('#m1PresentationStage').textContent(),/TRUE that p/);
 assert.match(await page.locator('#m1PresentationStage').textContent(),/FALSE that not-p/);
 assert.match(await page.locator('#m1PresentationStage').textContent(),/B · frame × congruență|B · frame × congruence/);
 const congruentText=await page.locator('#m1PresentationStage').textContent();
 await page.locator('[data-m1e2-audience="counter_attitudinal"]').click();
 assert.equal(await page.locator('[data-m1e2-audience="counter_attitudinal"]').getAttribute('aria-pressed'),'true');
 const counterText=await page.locator('#m1PresentationStage').textContent();
 assert.notEqual(congruentText,counterText);
 assert.match(counterText,/Gatt/);
 await page.locator('#m1AccessStage').waitFor();
 const accessText=await page.locator('#m1AccessStage').textContent();
 assert.match(accessText,/Hneg/);
 assert.match(accessText,/PreviewImpression/);
 assert.match(accessText,/0[.,]119203/);
 assert.match(accessText,/0[.,]141851/);
 assert.match(accessText,/12[.,\s]?448/);
 assert.match(accessText,/53[.,\s]?699/);
 assert.match(accessText,/PreviewImpression ≠ Access/);
 assert.match(accessText,/M1\.E3-NULL/);
 assert.match(accessText,/M1\.E3-A/);
 await page.locator('#language').click();
 await page.locator('#m1AccessStage').waitFor();
 const accessEnglish=await page.locator('#m1AccessStage').textContent();
 assert.match(accessEnglish,/Headline access gate: NULL vs Hneg/);
 assert.match(accessEnglish,/Limitations and provenance/);
 assert.match(accessEnglish,/historical Upworthy field experiments/);
 await page.locator('#language').click();
 await page.locator('#m1AccessStage').waitFor();
 assert.match(await page.locator('#m1AccessStage').textContent(),/Limitări și proveniență/);
 await page.locator('[data-mechanism="source"]').click();
 assert.match(await page.locator('#mechanismReading').textContent(),/2T − 1/);
 await page.locator('#exploreMechanism').click();assert.equal(await page.locator('#scenario').inputValue(),'source');
 await openView('planning');await page.locator('#bestBundle').waitFor();
 const plans=JSON.parse(await readFile(path.join(dist,'model/interventions.json'),'utf8'));
 const score=b=>50*(1-b.false_share+b.true_share);
 const expected=plans.profiles.find(p=>p.id==='reference').bundles.filter(b=>b.start===2&&b.mask.toString(2).replaceAll('0','').length<=3).sort((a,b)=>score(b)-score(a))[0];
 assert.equal(Number(await page.locator('#bestBundle').getAttribute('data-mask')),expected.mask);

 // OA-7 first implementation slice: read-only Action Canvas projection.
 assert.equal(await page.locator('#actionCanvas').count(),1);
 assert.equal(await page.locator('[data-action-stage]').count(),6);
 assert.equal(await page.locator('#actionCanvas').getAttribute('data-action-canvas-mask'),String(expected.mask));
 assert.equal(await page.locator('[data-action-stage="PROXIMAL_RESULT"]').getAttribute('data-action-status'),'SIMULATED_OUTPUT');
 assert.equal(await page.locator('[data-action-stage="INTERMEDIATE_RESULT"]').getAttribute('data-action-status'),'NOT_OPERATIONALIZED');
 assert.equal(await page.locator('[data-action-stage="FINAL_OUTCOME"]').getAttribute('data-action-status'),'NOT_OPERATIONALIZED');
 assert.match(await page.locator('#actionCanvas').textContent(),/read-only|read-only/i);
 await page.locator('[data-plan-mask="2"] [data-inspect="2"]').click();
 assert.equal(await page.locator('#actionCanvas').getAttribute('data-action-canvas-mask'),'2');
 assert.match(await page.locator('[data-action-stage="TARGET_MECHANISM"]').textContent(),/Context corectiv verificat|Verified corrective context/);
 assert.doesNotMatch(await page.locator('[data-action-stage="TARGET_MECHANISM"]').textContent(),/Indiciu de acuratețe|Accuracy cue/);
 await page.locator(`[data-plan-mask="${expected.mask}"] [data-inspect="${expected.mask}"]`).click();
 assert.equal(await page.locator('#actionCanvas').getAttribute('data-action-canvas-mask'),String(expected.mask));

 // OA-7 Indicator objects: simulation-derived definitions remain distinct from observations.
 assert.equal(await page.locator('#indicatorObjects').count(),1);
 assert.equal(await page.locator('[data-indicator-id]').count(),2);
 assert.equal(await page.locator('[data-indicator-stage="PROXIMAL"]').count(),2);
 assert.equal(await page.locator('[data-observation-status="NOT_OBSERVED"]').count(),2);
 assert.equal(await page.locator('[data-indicator-coverage="INTERMEDIATE"]').getAttribute('data-indicator-coverage-status'),'NOT_OPERATIONALIZED');
 assert.equal(await page.locator('[data-indicator-coverage="FINAL"]').getAttribute('data-indicator-coverage-status'),'NOT_OPERATIONALIZED');
 assert.match(await page.locator('#indicatorObjects').textContent(),/nu ObservedOutcome|not ObservedOutcome/i);
 assert.match(await page.locator('[data-indicator-id="CEM.INDICATOR.M0.FALSE_SHARING.MEAN13"]').textContent(),/SIMULATED|simulat/i);

 // OA-6C: explicit finite-scenario uncertainty UI, threshold coverage and canonical context.
 assert.equal(await page.locator('#decisionUncertainty').count(),1);
 assert.equal(await page.locator('[data-uncertainty-id]').count(),5);
 assert.equal(await page.locator('#uncertaintyScenarioMatrix tbody tr').count(),3);
 assert.match(await page.locator('#decisionUncertainty').textContent(),/scenarii declarate|declared scenarios/i);
 assert.match(await page.locator('#decisionUncertainty').textContent(),/nu probabilitate|not a probability/i);
 assert.equal(await page.locator('#selectedRobustness').getAttribute('data-selected-alternative'),'14');
 assert.match(await page.locator('#selectedTopCoverage').textContent(),/3 \/ 3/);
 await page.locator('#acceptabilityThreshold').fill('8');
 await page.locator('#acceptabilityThreshold').dispatchEvent('change');
 assert.match(await page.locator('#selectedAcceptableCoverage').textContent(),/1 \/ 3/);
 await page.locator('[data-uncertainty-search="VAR.FAMILIARITY.CLAIM"]').click();
 assert.equal(await page.locator('#semanticSearchInput').inputValue(),'VAR.FAMILIARITY.CLAIM');
 assert.equal(await page.locator('#semanticSearchInput').evaluate(el=>document.activeElement===el),true);
 await page.locator('[data-uncertainty-inspect="VAR.FAMILIARITY.CLAIM"]').click();
 assert.equal(await page.locator('#semanticInspector').getAttribute('data-inspector-id'),'VAR.FAMILIARITY.CLAIM');
 assert.equal(await page.locator('#semanticInspector').evaluate(el=>document.activeElement===el),true);
 assert.equal(await page.locator('#decisionUncertainty').count(),1);
 await page.locator('#budget').fill('2');await page.locator('#budget').dispatchEvent('change');
 assert.equal(await page.locator('[data-switch-scenario="low"]').getAttribute('data-switch-top-mask'),'10');
 assert.match(await page.locator('#decisionSwitch').textContent(),/Răspuns redus|Lower response/);
 assert.equal(await page.locator('[data-information-priority="UNC.PLANNER.RESPONSE.PROFILES"]').getAttribute('data-priority-class'),'DECISION_SENSITIVE_NOW');
 await page.locator('#budget').fill('3');await page.locator('#budget').dispatchEvent('change');

 // OA-6D: qualitative information priority and local-only reassessment triggers.
 assert.equal(await page.locator('[data-information-priority]').count(),5);
 assert.equal(await page.locator('[data-information-priority="UNC.PLANNER.RESPONSE.PROFILES"]').getAttribute('data-priority-class'),'RESEARCH_OR_MONITOR');
 assert.equal(await page.locator('[data-information-priority="UNC.PLANNER.OBJECTIVE.WEIGHT"]').getAttribute('data-priority-class'),'CLARIFY_USER_ASSUMPTION');
 assert.equal(await page.locator('[data-information-priority="UNC.PLANNER.STRUCTURAL.SCOPE"]').getAttribute('data-priority-class'),'CONTEXT_LIMITATION');
 assert.match(await page.locator('.information-priority').textContent(),/QUALITATIVE_TRIAGE_NO_NUMERIC_VOI/);
 assert.match(await page.locator('.adaptive-reassessment').textContent(),/nu observă automat|does not automatically observe/i);
 await page.locator('[data-priority-create-trigger="UNC.PLANNER.RESPONSE.PROFILES"]').click();
 assert.equal(await page.locator('#reassessmentUncertainty').inputValue(),'UNC.PLANNER.RESPONSE.PROFILES');
 assert.equal(await page.locator('#reassessmentIndicator').evaluate(el=>document.activeElement===el),true);
 await page.locator('#reassessmentIndicator').fill('New correction-access estimate');
 await page.locator('[name="trigger_condition"]').fill('Outside current declared range');
 await page.locator('[name="response_action"]').fill('Re-run robustness comparison');
 await page.locator('[name="basis"]').selectOption('EMPIRICAL');
 await page.locator('[name="source_note"]').fill('Future study');
 await page.locator('#reassessmentForm button[type="submit"]').click();
 assert.equal(await page.locator('[data-reassessment-record]').count(),1);
 assert.match(await page.locator('#reassessmentRecords').textContent(),/New correction-access estimate/);
 assert.equal(await page.evaluate(()=>JSON.parse(localStorage.getItem('cem.decision-reassessment.v1')).records.length),1);
 await page.locator('[data-remove-reassessment]').click();
 assert.equal(await page.locator('[data-reassessment-record]').count(),0);
 assert.equal(await page.evaluate(()=>JSON.parse(localStorage.getItem('cem.decision-reassessment.v1')).records.length),0);

 // OA-6E: keyboard, bilingual semantic parity, 320 CSS px and 200% text reflow.
 const priorityTrigger=page.locator('[data-priority-create-trigger="UNC.PLANNER.RESPONSE.PROFILES"]');
 await priorityTrigger.focus();
 assert.equal(await priorityTrigger.evaluate(el=>document.activeElement===el),true);
 await page.keyboard.press('Enter');
 assert.equal(await page.locator('#reassessmentIndicator').evaluate(el=>document.activeElement===el),true);
 const semanticCounts=async()=>({
  uncertainty:await page.locator('[data-uncertainty-id]').count(),
  priority:await page.locator('[data-information-priority]').count(),
  scenarios:await page.locator('[data-uncertainty-scenario]').count(),
  robustness:await page.locator('[data-robustness-alternative]').count(),
  reassessmentForms:await page.locator('#reassessmentForm').count()
 });
 const roSemantic=await semanticCounts();
 assert.match(await page.locator('#decisionUncertainty').textContent(),/Ce rămâne robust când schimbăm ipotezele/);
 assert.match(await page.locator('#decisionUncertainty').textContent(),/FĂRĂ PROBABILITĂȚI IMPLICITE/);
 await page.locator('#language').click();
 assert.equal(await page.locator('html').getAttribute('lang'),'en');
 await page.locator('#decisionUncertainty').waitFor();
 assert.deepEqual(await semanticCounts(),roSemantic);
 assert.match(await page.locator('#decisionUncertainty').textContent(),/What remains robust when assumptions change/);
 assert.match(await page.locator('#decisionUncertainty').textContent(),/NO IMPLIED PROBABILITIES/);
 await page.locator('#language').click();
 assert.equal(await page.locator('html').getAttribute('lang'),'ro');
 await page.locator('#decisionUncertainty').waitFor();
 await page.setViewportSize({width:320,height:844});
 assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'OA-6 planning 320 CSS px horizontal overflow');
 await page.setViewportSize({width:1440,height:1050});
 await page.evaluate(()=>document.documentElement.style.fontSize='200%');
 const oa6TextOverflow=await page.evaluate(()=>[...document.querySelectorAll('body *')].map(el=>{const r=el.getBoundingClientRect();return {tag:el.tagName,id:el.id,cls:typeof el.className==='string'?el.className:'',left:Math.round(r.left),right:Math.round(r.right),width:Math.round(r.width),text:(el.textContent??'').trim().slice(0,80)};}).filter(item=>item.right>innerWidth+1||item.left<-1).slice(0,20));
 assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'OA-6 planning 200% text horizontal overflow: '+JSON.stringify(oa6TextOverflow));
 await page.evaluate(()=>document.documentElement.style.fontSize='');
 // Verify exported score decomposition and profile gaps independently of rendered rounding.
 await page.locator('#budget').fill('4');await page.locator('#budget').dispatchEvent('change');
 for(const weight of [0,50,100]){
  await page.locator('#objective').fill(String(weight));
  await page.locator('[data-inspect="15"]').click();
  const pending=page.waitForEvent('download');await page.locator('#exportPlan').click();
  const saved=await pending;const analysis=JSON.parse(await readFile(await saved.path(),'utf8'));
  assert.deepEqual(analysis.schedule,plans.schedules.find(s=>s.mask===15&&s.start===2));
  const audit=analysis.decision_audit;
  assert(Math.abs(audit.criteria.false_score_contribution+audit.criteria.true_score_contribution-analysis.gain)<1e-10);
  const reference=plans.profiles.find(p=>p.id==='reference').bundles.filter(b=>b.start===2);
  const baseline=reference.find(b=>b.mask===0),bundle=reference.find(b=>b.mask===15);
  assert(Math.abs(audit.criteria.false_sharing_reduction-100*(baseline.false_share-bundle.false_share))<1e-10);
  const value=b=>weight*(1-b.false_share)+(100-weight)*b.true_share;
  for(const profile of plans.profiles){
   const rows=profile.bundles.filter(b=>b.start===2);
   const top=Math.max(...rows.map(value));
   const entry=audit.profiles.find(p=>p.id===profile.id);
   assert(Math.abs(entry.gap_to_best-(top-value(rows.find(b=>b.mask===15))))<1e-10);
  }
  for(const factor of audit.factors){
   const expected=value(bundle)-value(reference.find(b=>b.mask===(15&~factor.bit)));
   assert(Math.abs(factor.loss_if_removed-expected)<1e-10);
  }
  assert.equal(await page.locator('#factorAudit tbody tr').count(),4);
  assert.equal(await page.locator('#profileAudit tbody tr').count(),3);
 }
 if(process.env.CEM_SCREENSHOTS)await mkdir(process.env.CEM_SCREENSHOTS,{recursive:true});
 // Scheduling UI follows the inspected bundle and the activation time.
 for(const start of [2,5]){
  await page.selectOption('#timing',String(start));
  await page.locator('[data-inspect="15"]').click();
  assert.equal(await page.locator('#actionSchedule [data-action]').count(),4);
  assert.equal(await page.locator('#eventSchedule tbody tr').count(),13);
  assert.equal(await page.locator('#actionSchedule [data-action="8"] td').first().textContent(),start===2?'2, 4, 6, 8':'5, 7, 9, 11');
  assert.equal(await page.locator('#actionSchedule [data-action="1"] td').first().textContent(),start===2?'2, 3, 4':'Niciunul');
  if(start===5)assert.match(await page.locator('#actionSchedule [data-action="1"]').textContent(),/prea târzie/);
  await page.locator('#schedulePanel details summary').click();
  if(process.env.CEM_SCREENSHOTS)await page.locator('#schedulePanel').screenshot({path:path.join(process.env.CEM_SCREENSHOTS,'schedule-'+start+'.png')});
  const pending=page.waitForEvent('download');await page.locator('#exportPlan').click();
  const file=await pending;const exported=JSON.parse(await readFile(await file.path(),'utf8'));
  assert.deepEqual(exported.schedule,plans.schedules.find(s=>s.mask===15&&s.start===start));
 }
 await page.selectOption('#timing','2');
 await page.locator('#objective').fill('50');
 await page.locator('#budget').fill('0');await page.locator('#budget').dispatchEvent('change');
 assert.equal(await page.locator('#bestBundle').getAttribute('data-mask'),'0');
 assert.match(await page.locator('#inspectedRank').textContent(),/1 \/ 1/);
 assert.equal(await page.locator('#alternativeGap').count(),0);
 assert.equal(await page.locator('#actionSchedule [data-action]').count(),0);
 assert.match(await page.locator('#actionSchedule').textContent(),/Fără măsuri/);
 await page.locator('#budget').fill('3');await page.locator('#budget').dispatchEvent('change');
 await page.locator('[data-lever="1"]').uncheck();
 assert.equal(Number(await page.locator('#bestBundle').getAttribute('data-mask'))&2,0);
 await page.locator('[data-lever="1"]').check();
 await page.selectOption('#timing','5');await page.selectOption('#assumption','low');
 const planDownload=page.waitForEvent('download');await page.locator('#exportPlan').click();assert.equal((await planDownload).suggestedFilename(),'cem-intervention-plan.json');
 await page.selectOption('#timing','2');await page.selectOption('#assumption','reference');
 if(process.env.CEM_SCREENSHOTS){await mkdir(process.env.CEM_SCREENSHOTS,{recursive:true});await page.screenshot({path:path.join(process.env.CEM_SCREENSHOTS,'planning.png'),fullPage:true});}
 await openView('runs');await page.locator('#scenario').waitFor();
 const chartPatterns=await page.locator('#chart polyline').evaluateAll(lines=>lines.map(line=>line.getAttribute('stroke-dasharray')));
 assert.deepEqual(chartPatterns,['none','8 4','2 4']);
 const data=JSON.parse(await readFile(path.join(dist,'model/runs.json'),'utf8'));
 const explanations=JSON.parse(await readFile(path.join(dist,'model/explanations.json'),'utf8'));
 for(const run of data.runs){
  await page.selectOption('#scenario',run.id);
  await page.locator('#timeline').fill('12');
  const expected=run.frames[12].belief.toLocaleString('ro-RO',{minimumFractionDigits:3,maximumFractionDigits:3});
  assert.equal(await page.locator('#metrics strong').first().textContent(),expected);
  assert.equal(await page.locator('.results tbody tr').count(),13);
  const detail=explanations.runs.find(r=>r.id===run.id).frames[12];
  const formatted=Math.abs(detail.belief_logit).toLocaleString('ro-RO',{minimumFractionDigits:3,maximumFractionDigits:3});
  assert.match(await page.locator('#beliefLogit').textContent(),new RegExp(formatted.replace('.', '\\.')));
  assert.equal(await page.locator('#beliefTerms tbody tr').count(),4);
  assert.equal(await page.locator('#sharingTerms tbody tr').count(),3);
 }
 await openView('comparison');
 for(const comparison of data.runs){
  await page.selectOption('#comparisonScenario',comparison.id);await page.locator('#compareTimeline').fill('12');
  const baseline=data.runs.find(r=>r.id==='repetition');
  const delta=comparison.frames[12].belief-baseline.frames[12].belief;
  const formatted=(delta>0?'+':delta<0?'−':'')+Math.abs(delta).toLocaleString('ro-RO',{minimumFractionDigits:3,maximumFractionDigits:3});
  assert.equal(await page.locator('#deltaBelief').textContent(),'ΔB = '+formatted);
  assert.equal(await page.locator('#comparisonRows tr').count(),13);
 }
 await page.selectOption('#comparisonScenario','source');assert.match(await page.locator('#comparisonContext').textContent(),/două intrări/);
 const comparisonDownload=page.waitForEvent('download');await page.locator('#downloadComparison').click();assert.equal((await comparisonDownload).suggestedFilename(),'cem-scenario-comparison.json');
 await page.selectOption('#comparisonScenario','correction');await page.locator('#compareTimeline').fill('5');await page.locator('#inspectCompared').click();
 assert.equal(await page.locator('#scenario').inputValue(),'correction');assert.equal(await page.locator('#timeline').inputValue(),'5');
 await page.selectOption('#scenario','accuracy');await page.locator('#timeline').fill('5');
 assert.match(await page.locator('.step-story').textContent(),/Convingerea rămâne neschimbată/);
 await page.locator('#previous').click();assert.match(await page.locator('#stepBadge').textContent(),/4 \/ 12/);
 await page.selectOption('#scenario','correction');
 await page.locator('#next').click();assert.match(await page.locator('#stepBadge').textContent(),/1 \/ 12/);
 await page.locator('#play').click();await page.waitForFunction(()=>document.querySelector('#stepBadge').textContent.includes('2 / 12'));
 await page.locator('#play').click();await page.locator('#reset').click();
 const download=page.waitForEvent('download');await page.locator('#download').click();assert.equal((await download).suggestedFilename(),'cem-m0-correction.json');
 await page.locator('#language').click();assert.equal(await page.locator('html').getAttribute('lang'),'en');assert.match(await page.locator('h1').textContent(),/Mechanisms/);
 await openView('structure');await page.selectOption('#variable','VAR.CORRECTION.ACCESS');assert.match(await page.locator('#detail').textContent(),/Corrective-context/);
 assert.match(await page.locator('#graphCount').textContent(),/8 nodes · 7/);
 await page.selectOption('#dependency','c-b');assert.match(await page.locator('#detail').textContent(),/direction/);
 // M0 Visual Stage: exported events and stochastic outcomes, not time or a probability threshold.
 for(const reference of data.runs){
  await page.selectOption('#stageRun',reference.id);
  for(const index of [0,4,5,12]){
   await page.locator('#stageTime').fill(String(index));
   const count=reference.frames.slice(0,index+1).flatMap(f=>f.events).filter(e=>e.event_type==='ExposureEvent').length;
   const readout=await page.locator('#stageReadout').textContent();
   assert(readout.includes('Nexp: '+count+' ·'));
   assert(readout.endsWith('Share: '+Number(reference.frames[index].share)));
  }
 }
 await page.locator('#stageBands').check();assert.equal(await page.locator('.stage-bands rect').count(),4);
 await page.locator('#stageFocus').check();
 await page.selectOption('#stageTour','correction');await page.locator('#stageStart').click();
 assert.equal(await page.locator('#stageTime').inputValue(),'5');
 assert.match(await page.locator('#stageNeighbours').textContent(),/Outputs/);
 if(process.env.CEM_SCREENSHOTS)await page.locator('.graph-layout').screenshot({path:path.join(process.env.CEM_SCREENSHOTS,'stage-bands.png')});
 await page.locator('#stageNext').click();assert.match(await page.locator('#stageTourText').textContent(),/Selected factor: B/);
 await page.locator('#stageBack').click();assert.match(await page.locator('#stageTourText').textContent(),/Selected factor: C/);
 assert.equal(await page.locator('#stageBack').isDisabled(),true);
 assert.match(await page.locator('#stageReading').textContent(),/direction −1.000/);
 await page.locator('#stageTime').fill('12');assert.match(await page.locator('#stageReading').textContent(),/C = 0.400/);
 await page.locator('#stageTime').fill('5');
 await page.selectOption('#stageTour','source');await page.locator('#stageStart').click();
 assert.equal(await page.locator('#stageTime').inputValue(),'8');
 assert.match(await page.locator('#stageReading').textContent(),/changes both feedback and signal/);
 for(const reference of data.runs){
  await page.selectOption('#stageRun',reference.id);
  assert.equal(await page.locator('#stageNext').isDisabled(),true);
  for(const index of [0,5,12]){
   await page.locator('#stageTime').fill(String(index));
   await page.selectOption('#variable','VAR.CORRECTION.ACCESS');
   const term=explanations.runs.find(r=>r.id===reference.id).frames[index].belief_terms.correction;
   const formatted=(term<0?'−':term>0?'+':'')+Math.abs(term).toLocaleString('en-GB',{minimumFractionDigits:3,maximumFractionDigits:3});
   assert((await page.locator('#stageReading').textContent()).includes('Term in the belief score: '+formatted));
  }
 }
 await page.selectOption('#stageTour','correction');await page.locator('#stageStart').click();
 await page.selectOption('#variable','VAR.BELIEF.CLAIM');
 assert.equal(await page.locator('#stageNext').isDisabled(),true);
 assert.match(await page.locator('#stageReading').textContent(),/combines prior belief/);
 if(process.env.CEM_SCREENSHOTS)await page.locator('.visual-controls').screenshot({path:path.join(process.env.CEM_SCREENSHOTS,'graph-explanation.png')});
 await page.locator('#stageOpen').click();assert.equal(await page.locator('#scenario').inputValue(),'correction');assert.equal(await page.locator('#timeline').inputValue(),'5');
 await openView('structure');
 await page.selectOption('#graphMode','inputs');assert.equal(await page.locator('#dependency option').count(),18);
 await page.selectOption('#dependency','prior-b');assert.match(await page.locator('#detail').textContent(),/does not automatically replace/);
 await page.selectOption('#graphFocus','source');assert.match(await page.locator('#graphCount').textContent(),/6 nodes/);
 await page.selectOption('#dependency','t-b');assert.match(await page.locator('#detail').textContent(),/0.5/);
 const registryVariables=JSON.parse(await readFile(path.join(dist,'model/variables.json'),'utf8'));
 const registryLinks=JSON.parse(await readFile(path.join(dist,'model/links.json'),'utf8'));
 await page.selectOption('#graphMode','registered');assert.equal(await page.locator('#variable option').count(),registryVariables.length);assert.equal(await page.locator('#variable option[value="VAR.ISSUE.APPRAISAL"]').count(),1);assert.equal(await page.locator('#variable option[value="VAR.ATTITUDE.CONGRUENCE"]').count(),1);assert.equal(await page.locator('#variable option[value="VAR.ACCESS.PROBABILITY"]').count(),1);assert.equal(await page.locator('#variable option[value="VAR.PREVIEW.IMPRESSION"]').count(),1);
 await page.selectOption('#graphMode','core');
 await openView('reference');
 assert.equal(await page.locator('.reference-grid article').count(),registryVariables.length+registryLinks.length);
 assert.equal(await page.locator('.citation-link').count(),registryLinks.reduce((sum,link)=>sum+link.evidence_refs.length,0));
 for(const a of await page.locator('.citation-link').all()) assert.match(await a.getAttribute('href'),/^https:\/\/doi\.org\/10\./);
 assert.match(await page.locator('.reference-grid').last().textContent(),/Candidate mechanism/);
 assert((await page.locator('.epistemic-status[data-status]').count())>0);
 assert.notEqual(await page.locator('.epistemic-status[data-status]').first().evaluate(el=>getComputedStyle(el,'::before').content),'none');
 if(process.env.CEM_SCREENSHOTS){await mkdir(process.env.CEM_SCREENSHOTS,{recursive:true});await page.locator('.reference-grid').last().screenshot({path:path.join(process.env.CEM_SCREENSHOTS,'evidence.png')});}
 await openView('process');
 assert.equal(await page.locator('[data-odd-stage]').count(),4);
 assert.equal(await page.locator('.subsystem-grid article').count(),8);
 assert.match(await page.locator('[data-odd-stage="submodel"]').textContent(),/Belief update|Actualizarea convingerii/);
 assert.match(await page.locator('.vodd-extension').textContent(),/MOD\.14/);
 await openView('runs');await page.locator('#language').click();await page.locator('#timeline').fill('8');
 if(process.env.CEM_SCREENSHOTS){await mkdir(process.env.CEM_SCREENSHOTS,{recursive:true});await page.screenshot({path:path.join(process.env.CEM_SCREENSHOTS,'desktop.png'),fullPage:true});}
 await page.setViewportSize({width:600,height:844});
 assert.equal(await page.locator('.nav-groups').evaluate(el=>getComputedStyle(el).display),'grid');
 assert.equal((await page.locator('.nav-groups').evaluate(el=>getComputedStyle(el).gridTemplateColumns)).split(' ').length,2);
 await page.setViewportSize({width:390,height:844});
 assert.equal((await page.locator('.nav-groups').evaluate(el=>getComputedStyle(el).gridTemplateColumns)).split(' ').length,1);
 await page.evaluate(()=>{location.hash='#understanding/theory/repetition-familiarity-truth';});
 await waitTheory();
 assert.equal(await page.locator('#theoryChapterSelect').isVisible(),true);
 assert.equal(await page.locator('.theory-chapter-list').isVisible(),false);
 assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'Theory mobile horizontal overflow');
 await page.evaluate(()=>{location.hash='#understanding/tour/planning';});
 await page.locator('#guidedTourTitle').getByText('9. Planifică numai după ce ai înțeles mecanismele',{exact:true}).waitFor();
 assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'Guided Tour mobile horizontal overflow');
 assert.equal(await page.locator('.guided-tour-layout').evaluate(el=>getComputedStyle(el).gridTemplateColumns.split(' ').length),1);
 assert.equal(await page.locator('.guided-tour-select').isVisible(),true);
 assert.equal(await page.locator('.guided-tour-steps ol').isVisible(),false);
 assert.equal(await page.locator('#guidedTourSelect').inputValue(),'planning');
 if(process.env.CEM_SCREENSHOTS)await page.screenshot({path:path.join(process.env.CEM_SCREENSHOTS,'guided-tour-mobile.png'),fullPage:true});
 await page.evaluate(()=>{location.hash='#understanding/active/AU-3';});
 await page.locator('#activeUnderstandingTitle').waitFor();
 assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'Active Understanding mobile horizontal overflow');
 assert.equal((await page.locator('.active-understanding-layout').evaluate(el=>getComputedStyle(el).gridTemplateColumns)).split(' ').length,1);
 if(process.env.CEM_SCREENSHOTS)await page.screenshot({path:path.join(process.env.CEM_SCREENSHOTS,'active-understanding-mobile.png'),fullPage:true});
 await page.evaluate(()=>{location.hash='#understanding/active/challenge-model';});
 await page.locator('[data-challenge-model="M1.E3"]').waitFor();
 assert.equal(await page.locator('[data-model="null"] [data-delta]').textContent(),'0,000000');
 assert.equal(await page.locator('[data-model="headline-negativity"] [data-delta]').textContent(),'0,022648');
 assert.match(await page.locator('.challenge-model-status').textContent(),/MODEL_DISCRIMINATION_DEMONSTRATION/);
 assert.match(await page.locator('.challenge-model').textContent(),/VAL\.M1\.N04/);
 assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'Challenge Model mobile horizontal overflow');
 if(process.env.CEM_SCREENSHOTS)await page.screenshot({path:path.join(process.env.CEM_SCREENSHOTS,'challenge-model-mobile.png'),fullPage:true});
 await page.locator('[data-au-open-access]').click();
 await page.locator('#m1AccessStage').waitFor();
 assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'M1.E3 mobile horizontal overflow');
 if(process.env.CEM_SCREENSHOTS)await page.screenshot({path:path.join(process.env.CEM_SCREENSHOTS,'m1-access-mobile.png'),fullPage:true});
 assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'Mobile horizontal overflow');
 await page.evaluate(()=>{location.hash='#understanding/theory/repetition-familiarity-truth';});
 await waitTheory();
 if(process.env.CEM_SCREENSHOTS)await page.screenshot({path:path.join(process.env.CEM_SCREENSHOTS,'mobile.png'),fullPage:true});
 for(const v of ['structure','reference','process','planning','learning','comparison']){await openView(v);assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`${v}: mobile overflow`);}
 await openView('learning');
 await waitTheory();
 await page.evaluate(()=>document.documentElement.style.fontSize='200%');
 if(!(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth))) console.log(await page.evaluate(()=>[...document.querySelectorAll('body *')].filter(e=>e.getBoundingClientRect().right>innerWidth).map(e=>({tag:e.tagName,cls:e.className,w:e.getBoundingClientRect().width})).slice(0,15)));
 assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'Text enlargement overflow');
 await page.evaluate(()=>document.documentElement.style.fontSize='');
 await page.setViewportSize({width:1440,height:1050});
 for(const colorScheme of ['light','dark']){
  await page.emulateMedia({colorScheme});
  for(const v of ['learning','runs','structure','planning','comparison']){
   await openView(v);
   assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`${v}: ${colorScheme} overflow`);
   if(process.env.CEM_SCREENSHOTS)await page.screenshot({path:path.join(process.env.CEM_SCREENSHOTS,`${v}-${colorScheme}.png`),fullPage:true});
  }
 }
 assert.deepEqual(errors,[]);
 console.log('PASS: 4 Python reference runs, replay controls, JSON download, RO/EN, graph selection, registry, process, subpath assets, mobile and enlarged text; no browser errors.');
} finally {await browser?.close();await new Promise(resolve=>server.close(resolve));}
