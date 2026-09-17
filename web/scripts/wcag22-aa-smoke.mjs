import {createServer} from 'node:http';
import {readFile} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
import assert from 'node:assert/strict';
import {chromium} from 'playwright';

const dist=fileURLToPath(new URL('../dist/',import.meta.url));
const prefix='/cognitive-epistemic-model/';
const server=createServer(async(req,res)=>{
 try{const pathname=new URL(req.url,'http://localhost').pathname;if(!pathname.startsWith(prefix)){res.writeHead(404).end();return;}const file=path.resolve(dist,decodeURIComponent(pathname.slice(prefix.length))||'index.html');if(!file.startsWith(dist)){res.writeHead(403).end();return;}const data=await readFile(file);res.setHeader('Content-Type',({'.html':'text/html','.js':'text/javascript','.css':'text/css','.json':'application/json','.svg':'image/svg+xml'})[path.extname(file)]||'application/octet-stream');res.end(data);}catch{res.writeHead(404).end();}
});
await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
const address=server.address();assert(address&&typeof address!=='string');const url=`http://127.0.0.1:${address.port}${prefix}`;

const contexts=[
 ['primary',null],['theory','[data-suite-learn="theory"]'],['world-model','[data-suite-learn="world-model"]'],['mechanisms','[data-suite-learn="mechanisms"]'],['runs','[data-suite-view="runs"]'],['comparison','[data-suite-view="comparison"]'],['planning','[data-suite-view="planning"]'],['reference','[data-suite-view="reference"]'],['process','[data-suite-view="process"]'],['search','[data-suite-tool="search"]'],['inspector','[data-suite-tool="inspector"]']
];

let browser;
try{
 browser=await chromium.launch({headless:true,...(process.env.CEM_BROWSER_PATH?{executablePath:process.env.CEM_BROWSER_PATH,args:['--no-sandbox','--disable-gpu']}: {})});
 const page=await browser.newPage({viewport:{width:1440,height:1050},reducedMotion:'reduce'});
 const errors=[];page.on('pageerror',e=>errors.push(e.message));page.on('response',r=>{if(r.status()>=400)errors.push(`${r.status()} ${r.url()}`);});

 const settle=async()=>{await page.locator('[data-suite-standard="InfoClar Model Suite Design Standard v1.1"]').waitFor();await page.waitForTimeout(25);const theory=page.locator('#suiteTheoryContext #theoryArticle:visible');if(await theory.count())await page.waitForFunction(()=>[...document.querySelectorAll('#suiteTheoryContext #theoryArticle')].filter(el=>getComputedStyle(el).display!=='none').every(el=>el.getAttribute('aria-busy')!=='true'));};
 const openContext=async selector=>{await page.goto(url);await settle();if(selector){const control=page.locator(selector).first();await control.waitFor({state:'visible'});await control.click();await settle();}};
 const auditCurrentSurface=async label=>{
  const result=await page.evaluate(()=>{
   const visible=e=>{const s=getComputedStyle(e),r=e.getBoundingClientRect();return s.display!=='none'&&s.visibility!=='hidden'&&r.width>0&&r.height>0;};
   const ids=value=>(value??'').split(/\s+/).filter(Boolean).map(id=>document.getElementById(id)?.textContent?.trim()??'').filter(Boolean).join(' ').trim();
   const name=e=>{const a=e.getAttribute('aria-label')?.trim();if(a)return a;const l=ids(e.getAttribute('aria-labelledby'));if(l)return l;if('labels' in e&&e.labels?.length){const x=[...e.labels].map(v=>v.textContent?.trim()??'').filter(Boolean).join(' ').trim();if(x)return x;}if(e instanceof HTMLInputElement&&['button','submit','reset'].includes(e.type)&&e.value.trim())return e.value.trim();return e.textContent?.trim()||e.getAttribute('title')?.trim()||'';};
   const interactive='button,a[href],input:not([type="hidden"]),select,textarea,summary,[role="button"],[role="link"],[role="tab"],[role="switch"],[role="checkbox"],[role="radio"]';
   const items=[...document.querySelectorAll(interactive)].filter(e=>visible(e)&&!e.hasAttribute('disabled')&&e.getAttribute('aria-disabled')!=='true');
   const missingNames=items.filter(e=>!name(e)).map(e=>({tag:e.tagName,id:e.id})).slice(0,20);
   const targetIssues=[...document.querySelectorAll('button,input:not([type="hidden"]):not([type="checkbox"]):not([type="radio"]):not([type="range"]),select,textarea,summary,[role="button"],[role="tab"],[role="switch"]')].filter(e=>visible(e)&&!e.hasAttribute('disabled')&&e.getAttribute('aria-disabled')!=='true').map(e=>{const r=e.getBoundingClientRect();return {e,w:r.width,h:r.height};}).filter(x=>x.w<24||x.h<24).map(x=>({tag:x.e.tagName,id:x.e.id,w:Math.round(x.w),h:Math.round(x.h)})).slice(0,20);
   const hiddenFocusable=[...document.querySelectorAll('[aria-hidden="true"]')].flatMap(root=>[root,...root.querySelectorAll(interactive)]).filter(e=>e.tabIndex>=0&&visible(e)).map(e=>({tag:e.tagName,id:e.id})).slice(0,20);
   const duplicates=[...document.querySelectorAll('[id]')].reduce((m,e)=>(m.set(e.id,(m.get(e.id)??0)+1),m),new Map());
   return {missingNames,targetIssues,hiddenFocusable,duplicateIds:[...duplicates].filter(([,n])=>n>1).map(([id,count])=>({id,count}))};
  });
  assert.deepEqual(result.missingNames,[],`${label}: unnamed controls ${JSON.stringify(result.missingNames)}`);
  assert.deepEqual(result.targetIssues,[],`${label}: targets below 24px ${JSON.stringify(result.targetIssues)}`);
  assert.deepEqual(result.hiddenFocusable,[],`${label}: aria-hidden focusables ${JSON.stringify(result.hiddenFocusable)}`);
  assert.deepEqual(result.duplicateIds,[],`${label}: duplicate DOM IDs ${JSON.stringify(result.duplicateIds)}`);
 };

 await openContext(null);
 assert.equal(await page.locator('html').getAttribute('lang'),'en');
 assert.match(await page.title(),/Cognitive Epistemic Model/i);
 assert.equal(await page.locator('.suite-model-panel').count(),1);
 assert.equal(await page.locator('.suite-theory-panel').count(),1);
 assert.equal(await page.locator('.suite-dashboard-panel').count(),1);
 assert.equal(await page.locator('.suite-aux-panel').count(),1);
 assert.equal(await page.locator('[data-nav-group]').count(),0,'retired top-level navigation must not return');
 await page.locator('#language').click();assert.equal(await page.locator('html').getAttribute('lang'),'ro');await page.locator('#language').click();assert.equal(await page.locator('html').getAttribute('lang'),'en');

 for(const [name,selector] of contexts){await openContext(selector);await auditCurrentSurface(name);}

 await page.setViewportSize({width:320,height:844});
 for(const [name,selector] of contexts){await openContext(selector);const o=await page.evaluate(()=>({sw:document.documentElement.scrollWidth,w:innerWidth}));assert(o.sw<=o.w+1,`${name}: horizontal overflow at 320px (${o.sw}>${o.w})`);}

 await page.setViewportSize({width:1440,height:1050});
 for(const [name,selector] of contexts){await openContext(selector);await page.evaluate(()=>{document.documentElement.style.fontSize='200%';});const o=await page.evaluate(()=>({sw:document.documentElement.scrollWidth,w:innerWidth}));assert(o.sw<=o.w+1,`${name}: overflow at 200% text (${o.sw}>${o.w})`);}
 const targetToken=await page.evaluate(()=>getComputedStyle(document.documentElement).getPropertyValue('--vl-target-min').trim());assert.equal(targetToken,'44px');
 assert.deepEqual(errors,[],'WCAG smoke must not introduce runtime/resource errors');
 console.log('WCAG 2.2 AA automated baseline passed for InfoClar primary/contextual surfaces; manual audit remains required.');
}finally{if(browser)await browser.close();await new Promise(resolve=>server.close(resolve));}