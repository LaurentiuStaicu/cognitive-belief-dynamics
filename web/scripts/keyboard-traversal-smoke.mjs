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
const address=server.address();
assert(address&&typeof address!=='string');
const url=`http://127.0.0.1:${address.port}${prefix}`;

const domains={
 understand:['learning','structure','process'],
 analyze:['runs','comparison'],
 act:['planning'],
 library:['reference']
};

let browser;
try{
 browser=await chromium.launch({
  headless:true,
  ...(process.env.CEM_BROWSER_PATH?{executablePath:process.env.CEM_BROWSER_PATH,args:['--no-sandbox','--disable-gpu']}: {})
 });
 const page=await browser.newPage({viewport:{width:1440,height:1050},reducedMotion:'reduce'});
 const errors=[];
 page.on('pageerror',error=>errors.push(error.message));
 page.on('response',response=>{if(response.status()>=400)errors.push(`${response.status()} ${response.url()}`);});

 const waitForSettledUi=async()=>{
  await page.waitForFunction(()=>document.querySelector('#app')?.children.length>0);
  const theory=page.locator('#theoryArticle');
  if(await theory.count())await page.waitForFunction(()=>document.querySelector('#theoryArticle')?.getAttribute('aria-busy')!=='true');
 };

 const prepareTabCandidates=async()=>page.evaluate(()=>{
  document.querySelectorAll('[data-oa8-tab-audit]').forEach(element=>element.removeAttribute('data-oa8-tab-audit'));
  const selector='a[href],button,input:not([type="hidden"]),select,textarea,summary,[tabindex],audio[controls],video[controls],[contenteditable="true"]';
  const isVisible=element=>{
   const style=getComputedStyle(element);
   const rect=element.getBoundingClientRect();
   return style.display!=='none'&&style.visibility!=='hidden'&&rect.width>0&&rect.height>0;
  };
  const isDisabled=element=>element.hasAttribute('disabled')||element.getAttribute('aria-disabled')==='true';
  const blockedByAncestor=element=>!!element.closest('[aria-hidden="true"],[inert]');
  const radioIsSequential=element=>{
   if(!(element instanceof HTMLInputElement)||element.type!=='radio'||!element.name)return true;
   const escaped=CSS.escape(element.name);
   const group=[...document.querySelectorAll(`input[type="radio"][name="${escaped}"]`)].filter(candidate=>isVisible(candidate)&&!isDisabled(candidate)&&!blockedByAncestor(candidate));
   const checked=group.find(candidate=>candidate.checked);
   return checked?checked===element:group[0]===element;
  };
  const candidates=[...document.querySelectorAll(selector)]
   .filter(element=>element.tabIndex>=0&&isVisible(element)&&!isDisabled(element)&&!blockedByAncestor(element)&&radioIsSequential(element));
  return candidates.map((element,index)=>{
   const id=String(index);
   element.setAttribute('data-oa8-tab-audit',id);
   return {
    id,
    tag:element.tagName,
    domId:element.id||'',
    role:element.getAttribute('role')||'',
    text:(element.getAttribute('aria-label')||element.textContent||'').trim().replace(/\s+/g,' ').slice(0,80)
   };
  });
 });

 const traverseSurface=async label=>{
  const expected=await prepareTabCandidates();
  assert(expected.length>0,`${label}: surface exposes no sequential keyboard focus targets`);
  await page.evaluate(()=>{
   document.body.setAttribute('tabindex','-1');
   document.body.focus();
  });
  assert.equal(await page.evaluate(()=>document.activeElement===document.body),true,`${label}: audit must start from body focus sentinel`);

  const seen=[];
  const seenSet=new Set();
  const maxSteps=expected.length+12;
  for(let step=0;step<maxSteps&&seenSet.size<expected.length;step++){
   await page.keyboard.press('Tab');
   const active=await page.evaluate(()=>{
    const element=document.activeElement;
    if(!(element instanceof HTMLElement))return null;
    return {
     auditId:element.getAttribute('data-oa8-tab-audit'),
     tag:element.tagName,
     domId:element.id||'',
     role:element.getAttribute('role')||''
    };
   });
   if(active?.auditId!==null&&active?.auditId!==undefined){
    seen.push(active.auditId);
    seenSet.add(active.auditId);
   }
  }

  const missing=expected.filter(item=>!seenSet.has(item.id));
  assert.deepEqual(missing,[],`${label}: visible sequential focus targets not reached by real Tab traversal: ${JSON.stringify({missing,seen})}`);
  assert.equal(new Set(seen).size,expected.length,`${label}: traversal must reach every expected focus target before the audit limit`);

  await page.evaluate(()=>{
   document.body.removeAttribute('tabindex');
   document.querySelectorAll('[data-oa8-tab-audit]').forEach(element=>element.removeAttribute('data-oa8-tab-audit'));
  });
 };

 await page.goto(url);
 await waitForSettledUi();

 for(const [domain,views] of Object.entries(domains)){
  await page.locator(`[data-nav-group="${domain}"]`).click();
  for(const view of views){
   await page.locator(`[data-view="${view}"]`).click();
   await waitForSettledUi();
   await traverseSurface(`${domain}/${view}`);
  }
 }

 assert.deepEqual(errors,[],'keyboard traversal audit must not introduce runtime/resource errors');
 console.log('OA-8 keyboard traversal regression passed for all exposed primary/secondary surfaces.');
}finally{
 if(browser)await browser.close();
 await new Promise(resolve=>server.close(resolve));
}
