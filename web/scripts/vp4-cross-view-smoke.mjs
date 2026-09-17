import {createServer} from 'node:http';
import {readFile} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
import assert from 'node:assert/strict';
import {chromium} from 'playwright';

const dist=fileURLToPath(new URL('../dist/',import.meta.url));
const prefix='/cognitive-epistemic-model/';
const server=createServer(async(req,res)=>{try{const pathname=new URL(req.url,'http://localhost').pathname;if(!pathname.startsWith(prefix)){res.writeHead(404).end();return;}const file=path.resolve(dist,decodeURIComponent(pathname.slice(prefix.length))||'index.html');if(!file.startsWith(dist)){res.writeHead(403).end();return;}const data=await readFile(file);res.setHeader('Content-Type',({'.html':'text/html','.js':'text/javascript','.css':'text/css','.json':'application/json','.svg':'image/svg+xml'})[path.extname(file)]||'application/octet-stream');res.end(data);}catch{res.writeHead(404).end();}});
await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));const address=server.address();assert(address&&typeof address!=='string');const url=`http://127.0.0.1:${address.port}${prefix}`;
const overflowDiagnostic=page=>page.evaluate(()=>[...document.querySelectorAll('body *')].map(el=>{const r=el.getBoundingClientRect();return {tag:el.tagName,id:el.id,cls:typeof el.className==='string'?el.className:'',left:Math.round(r.left),right:Math.round(r.right),width:Math.round(r.width),text:(el.textContent??'').trim().slice(0,70)};}).filter(item=>item.right>innerWidth+1||item.left<-1).slice(0,12));
const settle=async page=>{await page.locator('[data-suite-standard="InfoClar Model Suite Design Standard v1.1"]').waitFor();await page.waitForTimeout(25);const article=page.locator('#suiteTheoryContext #theoryArticle:visible');if(await article.count())await page.waitForFunction(()=>[...document.querySelectorAll('#suiteTheoryContext #theoryArticle')].filter(el=>getComputedStyle(el).display!=='none').every(el=>el.getAttribute('aria-busy')!=='true'));await page.evaluate(()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve))));};
const fits=async(page,label)=>{const okay=await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+2&&document.body.scrollWidth<=innerWidth+2);if(!okay)assert.fail(`${label}: horizontal overflow ${JSON.stringify(await overflowDiagnostic(page))}`);};
const openTechnical=async page=>{await page.getByRole('button',{name:/Research \/ Provenance|Research \/ Proveniență/i}).click();await page.locator('[data-product-surface="technical"]').waitFor();};
const exercise=async(page,label)=>{
 const reset=async()=>{await page.goto(url);await settle(page);};
 await reset();await fits(page,`${label}/home`);
 await page.getByRole('button',{name:/How can repetition make a claim seem more true/i}).click();await settle(page);await fits(page,`${label}/pathway`);
 await page.locator('[data-suite-focus="familiarity"]').click();await settle(page);await fits(page,`${label}/mechanism-drawer`);
 await page.locator('[data-close-mechanism]').click();
 await page.getByRole('button',{name:'Interventions'}).click();await settle(page);await fits(page,`${label}/interventions`);
 await page.getByRole('button',{name:'Full Model Atlas'}).click();await settle(page);await fits(page,`${label}/atlas-major`);
 await page.locator('#atlasFilter').selectOption('memory-familiarity');await settle(page);await fits(page,`${label}/atlas-expanded`);
 await page.getByRole('button',{name:'Theory / Learn'}).click();await page.getByRole('button',{name:/Open full reader|Deschide reader-ul complet/i}).click();await settle(page);await fits(page,`${label}/theory`);
 await reset();await openTechnical(page);await fits(page,`${label}/technical`);
 for(const [name,selector] of [['runs','[data-suite-view="runs"]'],['comparison','[data-suite-view="comparison"]'],['planning','[data-suite-view="planning"]'],['reference','[data-suite-view="reference"]'],['process','[data-suite-view="process"]'],['search','[data-suite-tool="search"]'],['inspector','[data-suite-tool="inspector"]']]){await reset();await openTechnical(page);const control=page.locator(selector).first();await control.waitFor({state:'visible'});await control.click();await settle(page);await fits(page,`${label}/${name}`);}
};
let browser;
try{browser=await chromium.launch({headless:true,...(process.env.CEM_BROWSER_PATH?{executablePath:process.env.CEM_BROWSER_PATH,args:['--no-sandbox','--disable-gpu']}:{})});for(const colorScheme of ['light','dark']){const page=await browser.newPage({viewport:{width:320,height:844},colorScheme,reducedMotion:'reduce'});const errors=[];page.on('pageerror',e=>errors.push(e.message));page.on('response',r=>{if(r.status()>=400)errors.push(`${r.status()} ${r.url()}`);});await exercise(page,`320px/${colorScheme}`);const margin=await page.locator('.workspace').first().evaluate(el=>Math.min(Number.parseFloat(getComputedStyle(el).paddingLeft),Number.parseFloat(getComputedStyle(el).paddingRight)));assert(margin>=12,`320px/${colorScheme}: workspace margin must remain >=12px`);assert.deepEqual(errors,[],`320px/${colorScheme}: browser errors`);await page.close();}const page=await browser.newPage({viewport:{width:1440,height:1050},reducedMotion:'reduce'});const errors=[];page.on('pageerror',e=>errors.push(e.message));page.on('response',r=>{if(r.status()>=400)errors.push(`${r.status()} ${r.url()}`);});await page.goto(url);await page.evaluate(()=>{document.documentElement.style.fontSize='200%';});await exercise(page,'200%-text');assert.deepEqual(errors,[],'200%-text: browser errors');await page.close();}finally{if(browser)await browser.close();await new Promise(resolve=>server.close(resolve));}
console.log('VP-4 product-concept responsive closure passed');
