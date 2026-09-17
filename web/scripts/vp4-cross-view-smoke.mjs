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

const contexts=[
 ['primary',null],
 ['theory','[data-suite-learn="theory"]'],
 ['world-model','[data-suite-learn="world-model"]'],
 ['mechanisms','[data-suite-learn="mechanisms"]'],
 ['runs','[data-suite-view="runs"]'],
 ['comparison','[data-suite-view="comparison"]'],
 ['planning','[data-suite-view="planning"]'],
 ['reference','[data-suite-view="reference"]'],
 ['process','[data-suite-view="process"]'],
 ['search','[data-suite-tool="search"]'],
 ['inspector','[data-suite-tool="inspector"]']
];

const overflowDiagnostic=page=>page.evaluate(()=>[...document.querySelectorAll('body *')]
 .map(el=>{const r=el.getBoundingClientRect();return {tag:el.tagName,id:el.id,cls:typeof el.className==='string'?el.className:'',left:Math.round(r.left),right:Math.round(r.right),width:Math.round(r.width),text:(el.textContent??'').trim().slice(0,70)};})
 .filter(item=>item.right>innerWidth+1||item.left<-1)
 .slice(0,12));

const settle=async page=>{
 await page.locator('[data-suite-standard="InfoClar Model Suite Design Standard v1.1"]').waitFor();
 await page.waitForTimeout(30);
 const visibleTheory=page.locator('#suiteTheoryContext #theoryArticle:visible');
 if(await visibleTheory.count())await page.waitForFunction(()=>[...document.querySelectorAll('#suiteTheoryContext #theoryArticle')].filter(el=>getComputedStyle(el).display!=='none').every(el=>el.getAttribute('aria-busy')!=='true'));
 await page.evaluate(()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve))));
};

const exercise=async(page,label)=>{
 for(const [name,selector] of contexts){
  await page.goto(url);
  await settle(page);
  if(selector){const control=page.locator(selector).first();await control.waitFor({state:'visible'});await control.click();await settle(page);}
  const fits=await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1&&document.body.scrollWidth<=innerWidth+1);
  if(!fits)assert.fail(`${label}/${name}: horizontal overflow ${JSON.stringify(await overflowDiagnostic(page))}`);
  const shell=await page.locator('[data-suite-standard]').boundingBox();
  assert(shell,`${label}/${name}: InfoClar shell missing`);
  assert(shell.x>=-1,`${label}/${name}: shell crosses left edge`);
  assert(shell.x+shell.width<=await page.evaluate(()=>innerWidth)+1,`${label}/${name}: shell crosses right edge`);
 }
};

let browser;
try{
 browser=await chromium.launch({headless:true,...(process.env.CEM_BROWSER_PATH?{executablePath:process.env.CEM_BROWSER_PATH,args:['--no-sandbox','--disable-gpu']}: {})});
 for(const colorScheme of ['light','dark']){
  const page=await browser.newPage({viewport:{width:320,height:844},colorScheme,reducedMotion:'reduce'});
  const errors=[];page.on('pageerror',e=>errors.push(e.message));page.on('response',r=>{if(r.status()>=400)errors.push(`${r.status()} ${r.url()}`);});
  await exercise(page,`320px/${colorScheme}`);
  const margin=await page.locator('.workspace').first().evaluate(el=>Math.min(Number.parseFloat(getComputedStyle(el).paddingLeft),Number.parseFloat(getComputedStyle(el).paddingRight)));
  assert(margin>=12,`320px/${colorScheme}: workspace margin must remain >=12px`);
  assert.deepEqual(errors,[],`320px/${colorScheme}: browser errors`);
  await page.close();
 }
 const page=await browser.newPage({viewport:{width:1440,height:1050},reducedMotion:'reduce'});
 const errors=[];page.on('pageerror',e=>errors.push(e.message));page.on('response',r=>{if(r.status()>=400)errors.push(`${r.status()} ${r.url()}`);});
 await page.goto(url);await settle(page);await page.evaluate(()=>{document.documentElement.style.fontSize='200%';});
 await exercise(page,'200%-text');
 assert.deepEqual(errors,[],'200%-text: browser errors');
 await page.close();
}finally{if(browser)await browser.close();await new Promise(resolve=>server.close(resolve));}
console.log('VP-4 InfoClar contextual responsive closure passed');