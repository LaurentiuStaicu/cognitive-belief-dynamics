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
 const errors=[];
 page.on('pageerror',e=>errors.push(e.message));
 page.on('response',r=>{if(r.status()>=400)errors.push(`${r.status()} ${r.url()}`);});
 await page.goto(url);
 const shell=page.locator('[data-suite-standard="InfoClar Model Suite Design Standard v1.1"]');
 await shell.waitFor();

 assert.equal(await page.locator('.suite-model-panel').count(),1);
 assert.equal(await page.locator('.suite-theory-panel').count(),1);
 assert.equal(await page.locator('.suite-dashboard-panel').count(),1);
 assert.equal(await page.locator('.suite-aux-panel').count(),1);
 assert.equal(await page.locator('[data-nav-group]').count(),0);
 assert.equal(await page.locator('.navigation-shell').count(),0);
 assert.equal(await page.locator('.intro').count(),0);
 assert.equal(await page.locator('#semanticInspector').count(),0,'Global Inspector must not be permanent chrome');
 assert.equal(await page.locator('#semanticSearchInput').count(),0,'Search must not be permanent chrome');
 assert.equal(await page.locator('input[type="file"]').count(),0,'calibration upload must remain dormant');

 assert.equal(await page.locator('html').getAttribute('lang'),'en');
 await page.locator('#language').click();
 assert.equal(await page.locator('html').getAttribute('lang'),'ro');
 await page.locator('#language').click();
 assert.equal(await page.locator('html').getAttribute('lang'),'en');

 const workspace=JSON.parse(await page.evaluate(()=>localStorage.getItem('cem.workspace.v1.active')));
 assert.equal(workspace.schema_version,'1');
 assert.equal(workspace.versions.software_version,'0.4.3a0');

 await page.locator('[data-suite-learn="theory"]').first().click();
 await page.locator('#suiteTheoryContext #theoryArticle').waitFor();
 await page.waitForFunction(()=>document.querySelector('#suiteTheoryContext #theoryArticle')?.getAttribute('aria-busy')!=='true');
 assert.match(await page.locator('#suiteTheoryContext').textContent(),/What is Cognitive Epistemic Model|World-model construction/i);

 await page.locator('[data-suite-learn="world-model"]').first().click();
 await page.locator('#suiteTheoryContext [data-world-model]').waitFor();
 const wmText=await page.locator('#suiteTheoryContext').textContent();
 for(const token of ['Pprior','LR','Pwm','Uwm'])assert(wmText.includes(token),`world-model context missing ${token}`);
 assert.match(wmText,/EMPIRICAL/i);
 assert.match(wmText,/EXECUTABLE/i);
 assert.match(wmText,/CONCEPTUAL/i);
 assert.match(wmText,/INTERPRETIVE/i);

 await page.locator('[data-suite-learn="mechanisms"]').first().click();
 await page.locator('#suiteTheoryContext').waitFor();
 assert.match(await page.locator('#suiteTheoryContext').textContent(),/Mechanism|Mecanism/i);

 await page.locator('[data-suite-tool="search"]').first().click();
 await page.locator('#semanticSearchInput').waitFor();
 await page.locator('#semanticSearchInput').fill('world model');
 await page.locator('#semanticSearchForm button[type="submit"]').click();
 assert((await page.locator('[data-search-result-id]').count())>0,'contextual semantic search must return results');

 await page.locator('[data-suite-tool="inspector"]').first().click();
 await page.locator('#semanticInspector').waitFor();
 assert.match(await page.locator('#suiteAuxContext').textContent(),/Inspector/i);

 for(const [selector,needle] of [
  ['[data-suite-view="runs"]',/Run|Simulation/i],
  ['[data-suite-view="comparison"]',/Compar/i],
  ['[data-suite-view="planning"]',/Plan|Robust/i],
  ['[data-suite-view="reference"]',/Registr|Reference/i],
  ['[data-suite-view="process"]',/Process|Mechanism/i]
 ]){
  await page.locator(selector).first().click();
  await page.waitForTimeout(30);
  assert.match(await page.locator('#suiteAuxContext').textContent(),needle,selector);
 }

 assert.equal(await page.locator('[data-nav-group]').count(),0,'contextual tools must not recreate legacy top-level navigation');
 assert.equal(await page.locator('input[type="file"]').count(),0,'contextual tools must not expose dormant calibration');
 assert.deepEqual(errors,[],'InfoClar smoke must not introduce runtime/resource errors');
 console.log('InfoClar primary/contextual browser smoke passed');
}finally{
 if(browser)await browser.close();
 await new Promise(resolve=>server.close(resolve));
}
