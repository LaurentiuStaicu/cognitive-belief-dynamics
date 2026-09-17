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
 }catch{
  res.writeHead(404).end();
 }
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
  if(await theory.count()){
   await page.waitForFunction(()=>document.querySelector('#theoryArticle')?.getAttribute('aria-busy')!=='true');
  }
 };

 const auditCurrentSurface=async label=>{
  const result=await page.evaluate(()=>{
   const isVisible=element=>{
    const style=getComputedStyle(element);
    const rect=element.getBoundingClientRect();
    return style.display!=='none'&&style.visibility!=='hidden'&&rect.width>0&&rect.height>0;
   };
   const textForIds=value=>(value??'').split(/\s+/).filter(Boolean).map(id=>document.getElementById(id)?.textContent?.trim()??'').filter(Boolean).join(' ').trim();
   const accessibleName=element=>{
    const ariaLabel=element.getAttribute('aria-label')?.trim();
    if(ariaLabel)return ariaLabel;
    const labelledBy=textForIds(element.getAttribute('aria-labelledby'));
    if(labelledBy)return labelledBy;
    if('labels' in element&&element.labels?.length){
     const labelText=[...element.labels].map(label=>label.textContent?.trim()??'').filter(Boolean).join(' ').trim();
     if(labelText)return labelText;
    }
    if(element instanceof HTMLInputElement&&['button','submit','reset'].includes(element.type)&&element.value.trim())return element.value.trim();
    const text=element.textContent?.trim();
    if(text)return text;
    return element.getAttribute('title')?.trim()??'';
   };
   const interactiveSelector='button,a[href],input:not([type="hidden"]),select,textarea,summary,[role="button"],[role="link"],[role="tab"],[role="switch"],[role="checkbox"],[role="radio"]';
   const interactives=[...document.querySelectorAll(interactiveSelector)].filter(element=>isVisible(element)&&!element.hasAttribute('disabled')&&element.getAttribute('aria-disabled')!=='true');
   const missingNames=interactives.filter(element=>!accessibleName(element)).map(element=>({tag:element.tagName,id:element.id,cls:typeof element.className==='string'?element.className:''})).slice(0,20);

   const targetSelector='button,input:not([type="hidden"]):not([type="checkbox"]):not([type="radio"]):not([type="range"]),select,textarea,summary,[role="button"],[role="tab"],[role="switch"]';
   const targetIssues=[...document.querySelectorAll(targetSelector)]
    .filter(element=>isVisible(element)&&!element.hasAttribute('disabled')&&element.getAttribute('aria-disabled')!=='true')
    .map(element=>{const rect=element.getBoundingClientRect();return {element,width:rect.width,height:rect.height};})
    .filter(item=>item.width<24||item.height<24)
    .map(item=>({tag:item.element.tagName,id:item.element.id,cls:typeof item.element.className==='string'?item.element.className:'',width:Math.round(item.width*10)/10,height:Math.round(item.height*10)/10}))
    .slice(0,20);

   const focusables=interactives.filter(element=>element.tabIndex>=0).slice(0,80);
   const focusObscured=[];
   for(const element of focusables){
    element.focus({preventScroll:false});
    const rect=element.getBoundingClientRect();
    const left=Math.max(0,rect.left);
    const right=Math.min(innerWidth,rect.right);
    const top=Math.max(0,rect.top);
    const bottom=Math.min(innerHeight,rect.bottom);
    if(right<=left||bottom<=top){
     focusObscured.push({tag:element.tagName,id:element.id,reason:'outside-viewport'});
     continue;
    }
    const points=[
     [(left+right)/2,(top+bottom)/2],
     [left+Math.min(2,(right-left)/2),(top+bottom)/2],
     [right-Math.min(2,(right-left)/2),(top+bottom)/2],
     [(left+right)/2,top+Math.min(2,(bottom-top)/2)],
     [(left+right)/2,bottom-Math.min(2,(bottom-top)/2)]
    ];
    const exposed=points.some(([x,y])=>{
     const hit=document.elementFromPoint(x,y);
     return !!hit&&(hit===element||element.contains(hit));
    });
    if(!exposed)focusObscured.push({tag:element.tagName,id:element.id,reason:'author-content-obscures-focus'});
   }

   const hiddenFocusable=[...document.querySelectorAll('[aria-hidden="true"]')]
    .flatMap(root=>[root,...root.querySelectorAll(interactiveSelector)])
    .filter(element=>element.tabIndex>=0&&isVisible(element))
    .map(element=>({tag:element.tagName,id:element.id}))
    .slice(0,20);

   return {missingNames,targetIssues,focusObscured,hiddenFocusable};
  });
  assert.deepEqual(result.missingNames,[],`${label}: visible interactive controls without an accessible name: ${JSON.stringify(result.missingNames)}`);
  assert.deepEqual(result.targetIssues,[],`${label}: non-inline control targets below 24x24 CSS px: ${JSON.stringify(result.targetIssues)}`);
  assert.deepEqual(result.focusObscured,[],`${label}: focused controls fully obscured or outside viewport: ${JSON.stringify(result.focusObscured)}`);
  assert.deepEqual(result.hiddenFocusable,[],`${label}: aria-hidden content contains visible focusable controls: ${JSON.stringify(result.hiddenFocusable)}`);
 };

 await page.goto(url);
 await waitForSettledUi();
 assert.equal(await page.locator('html').getAttribute('lang'),'en','document language must start in English');
 assert.match(await page.title(),/Cognitive Epistemic Model/i,'page title must describe the application');

 const duplicateIds=await page.evaluate(()=>{
  const counts=new Map();
  for(const element of document.querySelectorAll('[id]'))counts.set(element.id,(counts.get(element.id)??0)+1);
  return [...counts.entries()].filter(([,count])=>count>1).map(([id,count])=>({id,count}));
 });
 assert.deepEqual(duplicateIds,[],'DOM IDs must remain unique');

 // Primary navigation must be keyboard-operable and expose state without color alone.
 for(const domain of Object.keys(domains)){
  const control=page.locator(`[data-nav-group="${domain}"]`);
  await control.focus();
  assert.equal(await control.evaluate(element=>document.activeElement===element),true,`${domain}: primary navigation must receive focus`);
  await page.keyboard.press('Enter');
  await page.waitForTimeout(20);
  assert.equal(await control.getAttribute('aria-pressed'),'true',`${domain}: Enter must activate primary navigation`);
 }

 // EN/RO language state must update the page language metadata.
 await page.locator('#language').click();
 assert.equal(await page.locator('html').getAttribute('lang'),'ro');
 await page.locator('#language').click();
 assert.equal(await page.locator('html').getAttribute('lang'),'en');

 // Audit every currently exposed primary/secondary surface at the normal desktop viewport.
 for(const [domain,views] of Object.entries(domains)){
  await page.locator(`[data-nav-group="${domain}"]`).click();
  for(const view of views){
   const viewControl=page.locator(`[data-view="${view}"]`);
   await viewControl.click();
   await waitForSettledUi();
   await auditCurrentSurface(`${domain}/${view}`);
  }
 }

 // WCAG 1.4.10: no two-dimensional scrolling at the 320 CSS px reflow target.
 await page.setViewportSize({width:320,height:844});
 for(const [domain,views] of Object.entries(domains)){
  await page.locator(`[data-nav-group="${domain}"]`).click();
  for(const view of views){
   await page.locator(`[data-view="${view}"]`).click();
   await waitForSettledUi();
   const overflow=await page.evaluate(()=>({scrollWidth:document.documentElement.scrollWidth,innerWidth}));
   assert(overflow.scrollWidth<=overflow.innerWidth+1,`${domain}/${view}: horizontal overflow at 320 CSS px (${overflow.scrollWidth}>${overflow.innerWidth})`);
  }
 }

 // WCAG 1.4.4: 200% text scaling must not introduce horizontal page overflow.
 await page.setViewportSize({width:1440,height:1050});
 await page.evaluate(()=>{document.documentElement.style.fontSize='200%';});
 for(const [domain,views] of Object.entries(domains)){
  await page.locator(`[data-nav-group="${domain}"]`).click();
  for(const view of views){
   await page.locator(`[data-view="${view}"]`).click();
   await waitForSettledUi();
   const overflow=await page.evaluate(()=>({scrollWidth:document.documentElement.scrollWidth,innerWidth}));
   assert(overflow.scrollWidth<=overflow.innerWidth+1,`${domain}/${view}: horizontal overflow with 200% text (${overflow.scrollWidth}>${overflow.innerWidth})`);
  }
 }
 await page.evaluate(()=>{document.documentElement.style.fontSize='';});

 // Existing visual language promises a target larger than WCAG 2.5.8's 24 CSS px minimum.
 const targetToken=await page.evaluate(()=>getComputedStyle(document.documentElement).getPropertyValue('--vl-target-min').trim());
 assert.equal(targetToken,'44px');

 assert.deepEqual(errors,[],'WCAG smoke must not introduce page/runtime resource errors');
 console.log('WCAG 2.2 AA automated baseline passed; manual audit remains required for full conformance.');
}finally{
 if(browser)await browser.close();
 await new Promise(resolve=>server.close(resolve));
}
