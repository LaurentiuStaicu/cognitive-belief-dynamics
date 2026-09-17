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
const contexts=[['primary',null,null],['theory','[data-suite-learn="theory"]','corpus'],['world-model','[data-suite-learn="world-model"]','corpus'],['planning','[data-suite-view="planning"]','infra'],['reference','[data-suite-view="reference"]','infra'],['search','[data-suite-tool="search"]','infra'],['inspector','[data-suite-tool="inspector"]','infra']];
let browser;
try{
 browser=await chromium.launch({headless:true,...(process.env.CEM_BROWSER_PATH?{executablePath:process.env.CEM_BROWSER_PATH,args:['--no-sandbox','--disable-gpu']}: {})});
 const page=await browser.newPage({viewport:{width:1440,height:1050},reducedMotion:'reduce'});
 const errors=[];page.on('pageerror',e=>errors.push(e.message));page.on('response',r=>{if(r.status()>=400)errors.push(`${r.status()} ${r.url()}`);});
 const settle=async()=>{await page.locator('[data-suite-standard="InfoClar Model Suite Design Standard v1.1"]').waitFor();await page.waitForTimeout(25);};
 const reveal=async disclosure=>{if(disclosure==='corpus'){const d=page.locator('.corpus-navigator');if(!await d.evaluate(el=>el.open))await d.locator(':scope > summary').click();}if(disclosure==='infra'){const d=page.locator('.infrastructure-tools');if(!await d.evaluate(el=>el.open))await d.locator(':scope > summary').click();}};
 const openContext=async(selector,disclosure)=>{await page.goto(url);await settle();if(disclosure)await reveal(disclosure);if(selector){const b=page.locator(selector).first();await b.waitFor({state:'visible'});await b.click();await settle();}};
 const prepare=async()=>page.evaluate(()=>{document.querySelectorAll('[data-oa8-tab-audit]').forEach(e=>e.removeAttribute('data-oa8-tab-audit'));const q='a[href],button,input:not([type="hidden"]),select,textarea,summary,[tabindex],audio[controls],video[controls],[contenteditable="true"]';const visible=e=>{const s=getComputedStyle(e),r=e.getBoundingClientRect();return s.display!=='none'&&s.visibility!=='hidden'&&r.width>0&&r.height>0;};const disabled=e=>e.hasAttribute('disabled')||e.getAttribute('aria-disabled')==='true';const blocked=e=>{if(e.closest('[aria-hidden="true"],[inert]'))return true;const closed=e.closest('details:not([open])');if(!closed)return false;const summary=closed.querySelector(':scope > summary');return !(summary&&(e===summary||summary.contains(e)));};const radios=e=>{if(!(e instanceof HTMLInputElement)||e.type!=='radio'||!e.name)return true;const group=[...document.querySelectorAll(`input[type="radio"][name="${CSS.escape(e.name)}"]`)].filter(x=>visible(x)&&!disabled(x)&&!blocked(x));const checked=group.find(x=>x.checked);return checked?checked===e:group[0]===e;};return [...document.querySelectorAll(q)].filter(e=>e.tabIndex>=0&&visible(e)&&!disabled(e)&&!blocked(e)&&radios(e)).map((e,i)=>{const id=String(i);e.setAttribute('data-oa8-tab-audit',id);return {id,tag:e.tagName,domId:e.id||'',text:(e.getAttribute('aria-label')||e.textContent||'').trim().replace(/\s+/g,' ').slice(0,80)};});});
 const traverse=async label=>{const expected=await prepare();assert(expected.length>0,`${label}: no sequential keyboard targets`);await page.evaluate(()=>{document.body.setAttribute('tabindex','-1');document.body.focus();});const seen=new Set();for(let i=0;i<expected.length+16&&seen.size<expected.length;i++){await page.keyboard.press('Tab');const id=await page.evaluate(()=>document.activeElement?.getAttribute('data-oa8-tab-audit')??null);if(id!==null)seen.add(id);}const missing=expected.filter(x=>!seen.has(x.id));assert.deepEqual(missing,[],`${label}: Tab did not reach ${JSON.stringify(missing)}`);await page.evaluate(()=>{document.body.removeAttribute('tabindex');document.querySelectorAll('[data-oa8-tab-audit]').forEach(e=>e.removeAttribute('data-oa8-tab-audit'));});};
 for(const [name,selector,disclosure] of contexts){await openContext(selector,disclosure);await traverse(name);}

 // Closed <details> content is intentionally absent from the sequential focus order.
 // Verify the stronger MOD.14 requirement separately: keyboard-open Primary evidence,
 // then traverse every source link in source order.
 await openContext('[data-suite-learn="world-model"]','corpus');
 const evidence=page.locator('#suiteTheoryContext .wm-context-panel details').filter({hasText:/Primary evidence|Dovezi primare/}).first();
 const evidenceSummary=evidence.locator(':scope > summary');
 await evidenceSummary.waitFor({state:'visible'});
 assert.equal(await evidence.evaluate(el=>el.open),false,'world-model: primary evidence disclosure should start closed');
 await evidenceSummary.focus();
 await page.keyboard.press('Space');
 assert.equal(await evidence.evaluate(el=>el.open),true,'world-model: Space must open primary evidence disclosure');
 const sourceLinks=evidence.locator('a[href]');
 const sourceCount=await sourceLinks.count();
 assert(sourceCount>0,'world-model: primary evidence must expose source links after keyboard opening');
 await evidenceSummary.focus();
 for(let i=0;i<sourceCount;i++){
  await page.keyboard.press('Tab');
  const reached=await sourceLinks.nth(i).evaluate(el=>document.activeElement===el);
  assert.equal(reached,true,`world-model: Tab must reach primary evidence source ${i+1}/${sourceCount}`);
 }

 assert.deepEqual(errors,[],'keyboard traversal audit must not introduce runtime/resource errors');
 console.log('OA-8 keyboard traversal regression passed for InfoClar primary/contextual surfaces, including keyboard-open MOD.14 evidence links.');
}finally{if(browser)await browser.close();await new Promise(resolve=>server.close(resolve));}
