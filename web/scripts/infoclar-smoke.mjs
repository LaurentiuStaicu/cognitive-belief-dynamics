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
const address=server.address();assert(address&&typeof address!=='string');
const url=`http://127.0.0.1:${address.port}${prefix}`;

let browser;
try{
 browser=await chromium.launch({headless:true,...(process.env.CEM_BROWSER_PATH?{executablePath:process.env.CEM_BROWSER_PATH,args:['--no-sandbox','--disable-gpu']}: {})});
 const page=await browser.newPage({viewport:{width:1440,height:1050},reducedMotion:'reduce'});
 const errors=[];page.on('pageerror',e=>errors.push(e.message));page.on('response',r=>{if(r.status()>=400)errors.push(`${r.status()} ${r.url()}`);});
 await page.goto(url);
 const shell=page.locator('[data-suite-standard="InfoClar Model Suite Design Standard v1.1"]');await shell.waitFor();
 for(const selector of ['.suite-model-panel','.suite-theory-panel','.suite-dashboard-panel','.suite-aux-panel'])assert.equal(await page.locator(selector).count(),1,selector);
 assert.equal(await page.locator('[data-nav-group]').count(),0);assert.equal(await page.locator('.navigation-shell').count(),0);assert.equal(await page.locator('#semanticInspector').count(),0);assert.equal(await page.locator('#semanticSearchInput').count(),0);assert.equal(await page.locator('input[type="file"]').count(),0);
 assert.match(await page.locator('.usefulness-orientation').textContent(),/What does CEM try to explain/i);
 assert.match(await page.locator('.suite-model-panel').textContent(),/MECHANISM EXPLORER/i);
 assert.match(await page.locator('.suite-dashboard-panel').textContent(),/EPISTEMIC MECHANISMS & VULNERABILITIES/i);
 assert.match(await page.locator('.suite-aux-panel').textContent(),/INTERVENTION EVIDENCE EXPLORER/i);

 assert.equal(await page.locator('html').getAttribute('lang'),'en');await page.locator('#language').click();assert.equal(await page.locator('html').getAttribute('lang'),'ro');await page.locator('#language').click();assert.equal(await page.locator('html').getAttribute('lang'),'en');

 await page.getByRole('button',{name:'QUESTION / PATHWAY EXPLORER'}).click();
 const questions=page.locator('[data-pathway-question]');assert((await questions.count())>=9,'question library must expose at least nine pathways');
 await page.getByRole('button',{name:/Why can a repeated claim seem more true/i}).click();
 assert((await page.locator('.cem-system-node.is-path').count())>=3,'pathway must highlight real mechanism nodes');
 assert((await page.locator('.cem-system-edge.is-path').count())>=2,'pathway must highlight registered edges');
 assert.match(await page.locator('.active-path-readout').textContent(),/Exposure|Familiarity|Belief/i);

 await page.locator('[data-suite-focus="familiarity"]').click();
 await page.locator('.mechanism-inspector').waitFor();
 const mechanismText=await page.locator('.mechanism-inspector').textContent();
 for(const token of ['Inputs','Outputs','Neighbours','Evidence level','Effect size','Heterogeneity','Competing explanations','Limitations','Sources'])assert(mechanismText.includes(token),token);
 assert.match(mechanismText,/g=0.37/i);
 assert.match(await page.locator('.no-personal-score').textContent(),/not a user profile|not.*vulnerability score/i);

 const interventionSelect=page.locator('#interventionEvidenceSelect');await interventionSelect.selectOption('warning-labels');
 const interventionText=await page.locator('.intervention-card').textContent();
 for(const token of ['Target mechanism','Population / context','Outcome','Effect estimate','Uncertainty','Heterogeneity','Duration','Conditions / moderators','Possible adverse effects','Directness to CEM'])assert(interventionText.includes(token),token);
 assert.match(interventionText,/27.6%/);assert.match(await page.locator('.suite-aux-panel').textContent(),/does not mean “CEM automatically recommends this action”/i);

 await page.locator('.corpus-navigator summary').click();
 assert((await page.locator('.corpus-topic').count())>=12,'complete corpus navigator');
 await page.locator('[data-suite-theory-chapter="repetition-familiarity-truth"]').first().click();
 await page.locator('#suiteTheoryContext #theoryArticle').waitFor();
 await page.waitForFunction(()=>document.querySelector('#suiteTheoryContext #theoryArticle')?.getAttribute('aria-busy')!=='true');
 assert.match(await page.locator('#suiteTheoryContext').textContent(),/familiar|truth|repet/i);

 await page.locator('.infrastructure-tools summary').click();
 await page.locator('[data-suite-tool="search"]').first().click();await page.locator('#semanticSearchInput').waitFor();await page.locator('#semanticSearchInput').fill('world model');await page.locator('#semanticSearchForm button[type="submit"]').click();assert((await page.locator('[data-search-result-id]').count())>0);
 await page.locator('[data-suite-tool="inspector"]').first().click();await page.locator('#semanticInspector').waitFor();

 const workspace=JSON.parse(await page.evaluate(()=>localStorage.getItem('cem.workspace.v1.active')));assert.equal(workspace.schema_version,'1');
 assert.deepEqual(errors,[],'Product usefulness browser smoke must not introduce runtime/resource errors');
 console.log('Product Usefulness Gate browser smoke passed');
}finally{if(browser)await browser.close();await new Promise(resolve=>server.close(resolve));}
