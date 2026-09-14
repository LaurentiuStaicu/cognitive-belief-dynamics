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
  res.setHeader('Content-Type',({'.html':'text/html','.js':'text/javascript','.css':'text/css','.json':'application/json'})[path.extname(file)]||'application/octet-stream');res.end(data);
 }catch{res.writeHead(404).end();}
});
await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
const url=`http://127.0.0.1:${server.address().port}${prefix}`;
let browser;
try {
 browser=await chromium.launch({headless:true, ...(process.env.CEM_BROWSER_PATH ? {executablePath:process.env.CEM_BROWSER_PATH, args:['--no-sandbox','--disable-gpu']} : {})});
 const page=await browser.newPage({viewport:{width:1440,height:1050},reducedMotion:'reduce'});
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 page.on('response',r=>{if(r.status()>=400)errors.push(`${r.status()} ${r.url()}`)});
 await page.goto(url);await page.locator('#mechanismReading').waitFor();
 const version=JSON.parse(await readFile(path.join(dist,'model/version.json'),'utf8'));
 assert.match(await page.locator('#releaseVersion').textContent(),new RegExp(version.version.replaceAll('.', '\\.')));
 assert((await page.locator('#releaseVersion').getAttribute('href')).endsWith('/'+version.release_tag));
 assert.equal(await page.locator('[data-view="learning"]').getAttribute('aria-pressed'),'true');
 assert.equal(await page.locator('.learning-factors article').count(),7);
 await page.locator('[data-mechanism="source"]').click();
 assert.match(await page.locator('#mechanismReading').textContent(),/2T − 1/);
 await page.locator('#exploreMechanism').click();assert.equal(await page.locator('#scenario').inputValue(),'source');
 await page.locator('[data-view="planning"]').click();await page.locator('#bestBundle').waitFor();
 const plans=JSON.parse(await readFile(path.join(dist,'model/interventions.json'),'utf8'));
 const score=b=>50*(1-b.false_share+b.true_share);
 const expected=plans.profiles.find(p=>p.id==='reference').bundles.filter(b=>b.start===2&&b.mask.toString(2).replaceAll('0','').length<=3).sort((a,b)=>score(b)-score(a))[0];
 assert.equal(Number(await page.locator('#bestBundle').getAttribute('data-mask')),expected.mask);
 await page.locator('#budget').fill('0');await page.locator('#budget').dispatchEvent('change');
 assert.equal(await page.locator('#bestBundle').getAttribute('data-mask'),'0');
 await page.locator('#budget').fill('3');await page.locator('#budget').dispatchEvent('change');
 await page.locator('[data-lever="1"]').uncheck();
 assert.equal(Number(await page.locator('#bestBundle').getAttribute('data-mask'))&2,0);
 await page.locator('[data-lever="1"]').check();
 await page.selectOption('#timing','5');await page.selectOption('#assumption','low');
 const planDownload=page.waitForEvent('download');await page.locator('#exportPlan').click();assert.equal((await planDownload).suggestedFilename(),'cem-intervention-plan.json');
 await page.selectOption('#timing','2');await page.selectOption('#assumption','reference');
 if(process.env.CEM_SCREENSHOTS){await mkdir(process.env.CEM_SCREENSHOTS,{recursive:true});await page.screenshot({path:path.join(process.env.CEM_SCREENSHOTS,'planning.png'),fullPage:true});}
 await page.locator('[data-view="runs"]').click();await page.locator('#scenario').waitFor();
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
 await page.locator('[data-view="comparison"]').click();
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
 await page.locator('[data-view="structure"]').click();await page.selectOption('#variable','VAR.CORRECTION.ACCESS');assert.match(await page.locator('#detail').textContent(),/Corrective-context/);
 assert.match(await page.locator('#graphCount').textContent(),/8 nodes · 7/);
 await page.selectOption('#dependency','c-b');assert.match(await page.locator('#detail').textContent(),/direction/);
 await page.selectOption('#graphMode','inputs');assert.equal(await page.locator('#dependency option').count(),18);
 await page.selectOption('#dependency','prior-b');assert.match(await page.locator('#detail').textContent(),/does not automatically replace/);
 await page.selectOption('#graphFocus','source');assert.match(await page.locator('#graphCount').textContent(),/6 nodes/);
 await page.selectOption('#dependency','t-b');assert.match(await page.locator('#detail').textContent(),/0.5/);
 await page.selectOption('#graphMode','registered');assert.equal(await page.locator('#variable option').count(),7);
 await page.selectOption('#graphMode','core');
 await page.locator('[data-view="reference"]').click();assert.equal(await page.locator('.reference-grid article').count(),10);
 assert.equal(await page.locator('.citation-link').count(),3);
 for(const a of await page.locator('.citation-link').all()) assert.match(await a.getAttribute('href'),/^https:\/\/doi\.org\/10\./);
 assert.match(await page.locator('.reference-grid').last().textContent(),/Candidate mechanism/);
 if(process.env.CEM_SCREENSHOTS){await mkdir(process.env.CEM_SCREENSHOTS,{recursive:true});await page.locator('.reference-grid').last().screenshot({path:path.join(process.env.CEM_SCREENSHOTS,'evidence.png')});}
 await page.locator('[data-view="process"]').click();assert.equal(await page.locator('.process-list li').count(),5);
 await page.locator('[data-view="runs"]').click();await page.locator('#language').click();await page.locator('#timeline').fill('8');
 if(process.env.CEM_SCREENSHOTS){await mkdir(process.env.CEM_SCREENSHOTS,{recursive:true});await page.screenshot({path:path.join(process.env.CEM_SCREENSHOTS,'desktop.png'),fullPage:true});}
 await page.setViewportSize({width:390,height:844});
 assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'Mobile horizontal overflow');
 if(process.env.CEM_SCREENSHOTS)await page.screenshot({path:path.join(process.env.CEM_SCREENSHOTS,'mobile.png'),fullPage:true});
 for(const v of ['structure','reference','process','planning','learning','comparison']){await page.locator(`[data-view="${v}"]`).click();assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`${v}: mobile overflow`);}
 await page.evaluate(()=>document.documentElement.style.fontSize='200%');
 if(!(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth))) console.log(await page.evaluate(()=>[...document.querySelectorAll('body *')].filter(e=>e.getBoundingClientRect().right>innerWidth).map(e=>({tag:e.tagName,cls:e.className,w:e.getBoundingClientRect().width})).slice(0,15)));
 assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'Text enlargement overflow');
 await page.evaluate(()=>document.documentElement.style.fontSize='');
 await page.setViewportSize({width:1440,height:1050});
 for(const colorScheme of ['light','dark']){
  await page.emulateMedia({colorScheme});
  for(const v of ['learning','runs','structure','planning','comparison']){
   await page.locator(`[data-view="${v}"]`).click();
   assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`${v}: ${colorScheme} overflow`);
   if(process.env.CEM_SCREENSHOTS)await page.screenshot({path:path.join(process.env.CEM_SCREENSHOTS,`${v}-${colorScheme}.png`),fullPage:true});
  }
 }
 assert.deepEqual(errors,[]);
 console.log('PASS: 4 Python reference runs, replay controls, JSON download, RO/EN, graph selection, registry, process, subpath assets, mobile and enlarged text; no browser errors.');
} finally {await browser?.close();await new Promise(resolve=>server.close(resolve));}
