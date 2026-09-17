import {createServer} from 'node:http';
import {readFile} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
import assert from 'node:assert/strict';
import {chromium} from 'playwright';

const dist=fileURLToPath(new URL('../dist/',import.meta.url));
const prefix='/cognitive-epistemic-model/';
const server=createServer(async(req,res)=>{try{const pathname=new URL(req.url,'http://localhost').pathname;if(!pathname.startsWith(prefix)){res.writeHead(404).end();return;}const file=path.resolve(dist,decodeURIComponent(pathname.slice(prefix.length))||'index.html');if(!file.startsWith(dist)){res.writeHead(403).end();return;}const data=await readFile(file);res.setHeader('Content-Type',({'.html':'text/html','.js':'text/javascript','.css':'text/css','.json':'application/json','.svg':'image/svg+xml'})[path.extname(file)]||'application/octet-stream');res.end(data);}catch{res.writeHead(404).end();}});
await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
const address=server.address();assert(address&&typeof address!=='string');const url=`http://127.0.0.1:${address.port}${prefix}`;
const contexts=[['primary',null],['theory','[data-suite-learn="theory"]'],['world-model','[data-suite-learn="world-model"]'],['planning','[data-suite-view="planning"]'],['reference','[data-suite-view="reference"]'],['search','[data-suite-tool="search"]'],['inspector','[data-suite-tool="inspector"]']];
let browser;
try{
 browser=await chromium.launch({headless:true,...(process.env.CEM_BROWSER_PATH?{executablePath:process.env.CEM_BROWSER_PATH,args:['--no-sandbox','--disable-gpu']}: {})});
 const page=await browser.newPage({viewport:{width:1440,height:1050},reducedMotion:'reduce'});
 const errors=[];page.on('pageerror',e=>errors.push(e.message));page.on('response',r=>{if(r.status()>=400)errors.push(`${r.status()} ${r.url()}`);});
 const settle=async()=>{await page.locator('[data-suite-standard="InfoClar Model Suite Design Standard v1.1"]').waitFor();await page.waitForTimeout(25);};
 const openContext=async selector=>{await page.goto(url);await settle();if(selector){const b=page.locator(selector).first();await b.waitFor({state:'visible'});await b.click();await settle();}};
 const prepare=async()=>page.evaluate(()=>{document.querySelectorAll('[data-oa8-tab-audit]').forEach(e=>e.removeAttribute('data-oa8-tab-audit'));const q='a[href],button,input:not([type="hidden"]),select,textarea,summary,[tabindex],audio[controls],video[controls],[contenteditable="true"]';const visible=e=>{const s=getComputedStyle(e),r=e.getBoundingClientRect();return s.display!=='none'&&s.visibility!=='hidden'&&r.width>0&&r.height>0;};const disabled=e=>e.hasAttribute('disabled')||e.getAttribute('aria-disabled')==='true';const blocked=e=>!!e.closest('[aria-hidden="true"],[inert]');const radios=e=>{if(!(e instanceof HTMLInputElement)||e.type!=='radio'||!e.name)return true;const group=[...document.querySelectorAll(`input[type="radio"][name="${CSS.escape(e.name)}"]`)].filter(x=>visible(x)&&!disabled(x)&&!blocked(x));const checked=group.find(x=>x.checked);return checked?checked===e:group[0]===e;};return [...document.querySelectorAll(q)].filter(e=>e.tabIndex>=0&&visible(e)&&!disabled(e)&&!blocked(e)&&radios(e)).map((e,i)=>{const id=String(i);e.setAttribute('data-oa8-tab-audit',id);return {id,tag:e.tagName,domId:e.id||'',text:(e.getAttribute('aria-label')||e.textContent||'').trim().replace(/\s+/g,' ').slice(0,80)};});});
 const traverse=async label=>{const expected=await prepare();assert(expected.length>0,`${label}: no sequential keyboard targets`);await page.evaluate(()=>{document.body.setAttribute('tabindex','-1');document.body.focus();});const seen=new Set();for(let i=0;i<expected.length+16&&seen.size<expected.length;i++){await page.keyboard.press('Tab');const id=await page.evaluate(()=>document.activeElement?.getAttribute('data-oa8-tab-audit')??null);if(id!==null)seen.add(id);}const missing=expected.filter(x=>!seen.has(x.id));assert.deepEqual(missing,[],`${label}: Tab did not reach ${JSON.stringify(missing)}`);await page.evaluate(()=>{document.body.removeAttribute('tabindex');document.querySelectorAll('[data-oa8-tab-audit]').forEach(e=>e.removeAttribute('data-oa8-tab-audit'));});};
 for(const [name,selector] of contexts){await openContext(selector);await traverse(name);}
 assert.deepEqual(errors,[],'keyboard traversal audit must not introduce runtime/resource errors');
 console.log('OA-8 keyboard traversal regression passed for InfoClar primary/contextual surfaces.');
}finally{if(browser)await browser.close();await new Promise(resolve=>server.close(resolve));}