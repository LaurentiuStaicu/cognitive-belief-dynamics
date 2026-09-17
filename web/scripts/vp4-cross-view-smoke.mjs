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

const domainForView={
 learning:'understand',
 structure:'understand',
 process:'understand',
 runs:'analyze',
 comparison:'analyze',
 planning:'act',
 reference:'library'
};
const views=Object.keys(domainForView);

const overflowDiagnostic=page=>page.evaluate(()=>[...document.querySelectorAll('body *')]
 .map(el=>{const r=el.getBoundingClientRect();return {tag:el.tagName,id:el.id,cls:typeof el.className==='string'?el.className:'',left:Math.round(r.left),right:Math.round(r.right),width:Math.round(r.width),text:(el.textContent??'').trim().slice(0,70)};})
 .filter(item=>item.right>innerWidth+1||item.left<-1)
 .slice(0,12));

let browser;
try{
 browser=await chromium.launch({headless:true,...(process.env.CEM_BROWSER_PATH?{executablePath:process.env.CEM_BROWSER_PATH,args:['--no-sandbox','--disable-gpu']}: {})});

 const exerciseViews=async(page,label)=>{
  for(const view of views){
   const domain=domainForView[view];
   await page.locator(`[data-nav-group="${domain}"]`).click();
   const viewButton=page.locator(`[data-view="${view}"]`);
   await viewButton.waitFor({state:'visible'});
   await viewButton.click();
   if(view==='learning'){
    await page.waitForFunction(()=>{const article=document.querySelector('#theoryArticle');return !article||article.getAttribute('aria-busy')==='false';});
   }
   await page.evaluate(()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve))));
   const fits=await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1&&document.body.scrollWidth<=innerWidth+1);
   if(!fits){
    const diagnostic=await overflowDiagnostic(page);
    assert.fail(`${label} ${view}: document-level horizontal overflow: ${JSON.stringify(diagnostic)}`);
   }
   const workspace=await page.locator('.workspace').boundingBox();
   assert(workspace,`${label} ${view}: workspace missing`);
   assert(workspace.x>=-1,`${label} ${view}: workspace crosses left viewport edge`);
   assert(workspace.x+workspace.width<=await page.evaluate(()=>innerWidth)+1,`${label} ${view}: workspace crosses right viewport edge`);
  }
 };

 for(const colorScheme of ['light','dark']){
  const page=await browser.newPage({viewport:{width:320,height:844},colorScheme,reducedMotion:'reduce'});
  const errors=[];
  page.on('pageerror',error=>errors.push(error.message));
  page.on('response',response=>{if(response.status()>=400)errors.push(`${response.status()} ${response.url()}`);});
  await page.goto(url);
  await page.waitForFunction(()=>document.querySelector('[data-nav-group="understand"]'));
  await exerciseViews(page,`320px/${colorScheme}`);
  const compactColumns=await page.locator('.nav-groups').evaluate(el=>getComputedStyle(el).gridTemplateColumns.split(' ').filter(Boolean).length);
  assert.equal(compactColumns,1,`320px/${colorScheme}: primary navigation must collapse to one column`);
  const minMargin=await page.locator('.workspace').evaluate(el=>Math.min(Number.parseFloat(getComputedStyle(el).paddingLeft),Number.parseFloat(getComputedStyle(el).paddingRight)));
  assert(minMargin>=12,`320px/${colorScheme}: workspace content margin must remain at least 12px`);
  assert.deepEqual(errors,[],`320px/${colorScheme}: browser errors`);
  await page.close();
 }

 const zoomPage=await browser.newPage({viewport:{width:1440,height:1050},colorScheme:'light',reducedMotion:'reduce'});
 const zoomErrors=[];
 zoomPage.on('pageerror',error=>zoomErrors.push(error.message));
 zoomPage.on('response',response=>{if(response.status()>=400)zoomErrors.push(`${response.status()} ${response.url()}`);});
 await zoomPage.goto(url);
 await zoomPage.waitForFunction(()=>document.querySelector('[data-nav-group="understand"]'));
 await zoomPage.evaluate(()=>{document.documentElement.style.fontSize='200%';});
 await exerciseViews(zoomPage,'200%-text');
 assert.deepEqual(zoomErrors,[],'200%-text: browser errors');
 await zoomPage.close();
}finally{
 if(browser)await browser.close();
 await new Promise(resolve=>server.close(resolve));
}

console.log('VP-4 cross-view responsive closure passed');
