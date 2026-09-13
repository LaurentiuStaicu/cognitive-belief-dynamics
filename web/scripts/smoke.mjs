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
 await page.goto(url);await page.locator('#scenario').waitFor();
 const data=JSON.parse(await readFile(path.join(dist,'model/runs.json'),'utf8'));
 for(const run of data.runs){
  await page.selectOption('#scenario',run.id);
  await page.locator('#timeline').fill('12');
  const expected=run.frames[12].belief.toLocaleString('ro-RO',{minimumFractionDigits:3,maximumFractionDigits:3});
  assert.equal(await page.locator('#metrics strong').first().textContent(),expected);
  assert.equal(await page.locator('tbody tr').count(),13);
 }
 await page.selectOption('#scenario','correction');
 await page.locator('#next').click();assert.match(await page.locator('#stepBadge').textContent(),/1 \/ 12/);
 await page.locator('#play').click();await page.waitForFunction(()=>document.querySelector('#stepBadge').textContent.includes('2 / 12'));
 await page.locator('#play').click();await page.locator('#reset').click();
 const download=page.waitForEvent('download');await page.locator('#download').click();assert.equal((await download).suggestedFilename(),'cem-m0-correction.json');
 await page.locator('#language').click();assert.equal(await page.locator('html').getAttribute('lang'),'en');assert.match(await page.locator('h1').textContent(),/From exposure/);
 await page.locator('[data-view="structure"]').click();await page.selectOption('#variable','VAR.CORRECTION.ACCESS');assert.match(await page.locator('#detail').textContent(),/Corrective-context/);
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
 for(const v of ['structure','reference','process']){await page.locator(`[data-view="${v}"]`).click();assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`${v}: mobile overflow`);}
 await page.evaluate(()=>document.documentElement.style.fontSize='200%');
 if(!(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth))) console.log(await page.evaluate(()=>[...document.querySelectorAll('body *')].filter(e=>e.getBoundingClientRect().right>innerWidth).map(e=>({tag:e.tagName,cls:e.className,w:e.getBoundingClientRect().width})).slice(0,15)));
 assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'Text enlargement overflow');
 assert.deepEqual(errors,[]);
 console.log('PASS: 4 Python reference runs, replay controls, JSON download, RO/EN, graph selection, registry, process, subpath assets, mobile and enlarged text; no browser errors.');
} finally {await browser?.close();await new Promise(resolve=>server.close(resolve));}
