import {createServer} from 'node:http';
import {mkdir,readFile} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
import assert from 'node:assert/strict';
import {chromium} from 'playwright';

const dist=fileURLToPath(new URL('../dist/',import.meta.url));
const prefix='/cognitive-epistemic-model/';
const screenshotDir=process.env.CEM_SCREENSHOTS||'';
if(screenshotDir)await mkdir(screenshotDir,{recursive:true});

const server=createServer(async(req,res)=>{
 try{
  const pathname=new URL(req.url,'http://localhost').pathname;
  if(!pathname.startsWith(prefix)){res.writeHead(404).end();return;}
  const file=path.resolve(dist,decodeURIComponent(pathname.slice(prefix.length))||'index.html');
  if(!file.startsWith(dist)){res.writeHead(403).end();return;}
  const data=await readFile(file);
  res.setHeader('Content-Type',({'.html':'text/html','.js':'text/javascript','.css':'text/css','.json':'application/json','.svg':'image/svg+xml','.md':'text/markdown'})[path.extname(file)]||'application/octet-stream');
  res.end(data);
 }catch{res.writeHead(404).end();}
});
await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
const address=server.address();assert(address&&typeof address!=='string');
const url=`http://127.0.0.1:${address.port}${prefix}`;

const banned=[/\bPwm\b/,/\bUwm\b/,/\bAissue\b/,/\bSobs\b/,/\bEngageIntent\b/,/\bPaccess\b/,/\bNexp\b/,/\bEedit\b/,/\bFpres\b/,/\bODD\./,/\bREF\./,/\bVAR\./,/\bLINK\./,/\.json\b/,/\.py\b/];
function assertNoInternalCodes(text,label){for(const pattern of banned)assert(!pattern.test(text),`${label}: leaked internal token ${pattern}`);}

let browser;
try{
 browser=await chromium.launch({headless:true,...(process.env.CEM_BROWSER_PATH?{executablePath:process.env.CEM_BROWSER_PATH,args:['--no-sandbox','--disable-gpu']}: {})});
 const viewports=[
  {width:1440,height:900,name:'1440x900'},
  {width:1366,height:768,name:'1366x768'},
  {width:390,height:844,name:'mobile-390x844'},
 ];
 for(const viewport of viewports){
  const page=await browser.newPage({viewport:{width:viewport.width,height:viewport.height},reducedMotion:'reduce'});
  const errors=[];page.on('pageerror',e=>errors.push(e.message));page.on('response',r=>{if(r.status()>=400)errors.push(`${r.status()} ${r.url()}`);});
  await page.goto(url);
  await page.locator('.product-header').waitFor();
  assert.equal(await page.locator('.suite-header,.navigation-shell,.suite-model-panel,#semanticInspector,#semanticSearchInput').count(),0,`${viewport.name}: legacy product chrome must not mount`);
  assert.equal(await page.locator('html').getAttribute('lang'),'en');
  const homeText=await page.locator('body').innerText();assertNoInternalCodes(homeText,`${viewport.name} home`);
  assert.match(homeText,/How can information end up changing what we believe and do\?/);
  assert.equal(await page.locator('[data-question="repetition"]').count(),1);

  await page.locator('[data-question="repetition"]').click();
  await page.locator('[data-pathway="repetition"]').waitFor();
  const pathwayText=await page.locator('[data-pathway="repetition"]').innerText();
  for(const label of ['Repeated exposure','Familiarity','Belief judgment','Sharing / action'])assert(pathwayText.includes(label),`${viewport.name}: missing ${label}`);
  assertNoInternalCodes(await page.locator('body').innerText(),`${viewport.name} pathway`);
  const dimensions=await page.locator('[data-pathway="repetition"]').evaluate(element=>{const rect=element.getBoundingClientRect();return {left:rect.left,right:rect.right,width:rect.width,scrollWidth:document.documentElement.scrollWidth,innerWidth:window.innerWidth};});
  assert(dimensions.left>=-1,`${viewport.name}: pathway begins outside viewport`);
  assert(dimensions.right<=viewport.width+1,`${viewport.name}: pathway exceeds viewport (${dimensions.right} > ${viewport.width})`);
  assert(dimensions.scrollWidth<=dimensions.innerWidth+1,`${viewport.name}: horizontal document overflow ${dimensions.scrollWidth} > ${dimensions.innerWidth}`);

  const nodes=await page.locator('.path-node').evaluateAll(items=>items.map(item=>{const rect=item.getBoundingClientRect();return {top:rect.top,left:rect.left,right:rect.right,bottom:rect.bottom,width:rect.width};}));
  assert.equal(nodes.length,4,`${viewport.name}: expected four primary mechanisms`);
  if(viewport.width<=760){for(let i=1;i<nodes.length;i++)assert(nodes[i].top>nodes[i-1].bottom,`${viewport.name}: mobile pathway is not a vertical sequence`);}else{for(let i=1;i<nodes.length;i++)assert(nodes[i].left>nodes[i-1].right,`${viewport.name}: desktop pathway order is not visually left-to-right`);}

  const statusCount=await page.locator('.edge-status').count();assert.equal(statusCount,3,`${viewport.name}: each visible edge needs a status`);
  if(screenshotDir)await page.screenshot({path:path.join(screenshotDir,`product-v2-pathway-${viewport.name}.png`),fullPage:true});

  await page.locator('[data-mechanism="familiarity"]').click();
  const drawer=page.locator('#context-drawer[data-open="true"]');await drawer.waitFor();
  const drawerText=await drawer.innerText();
  for(const label of ['WHAT IS IT?','WHAT DOES THE EVIDENCE SAY?','HOW LARGE IS THE EFFECT?','WHAT ELSE COULD EXPLAIN IT?','INTERVENTIONS STUDIED'])assert(drawerText.includes(label),`${viewport.name}: drawer missing ${label}`);
  assert(drawerText.includes('182 studies'));assert(drawerText.includes('31,184'));assert(drawerText.includes('0.37'));
  assertNoInternalCodes(drawerText,`${viewport.name} mechanism drawer`);
  const drawerBox=await drawer.boundingBox();assert(drawerBox,`${viewport.name}: drawer bounding box unavailable`);
  if(viewport.width>760)assert(drawerBox.width>=430,`${viewport.name}: context drawer is too narrow (${drawerBox.width})`);else assert(drawerBox.width>=viewport.width-2,`${viewport.name}: mobile drawer should use the viewport width`);
  await page.locator('[data-close-drawer]').click();

  if(viewport.name==='1440x900'){
   await page.locator('[data-view="theory"]').first().click();
   await page.locator('[data-product-view="theory"]').waitFor();
   const theoryText=await page.locator('[data-product-view="theory"]').innerText();
   assert.match(theoryText,/Repetition, familiarity and judged truth/);assert(theoryText.includes('g = 0.37'));assertNoInternalCodes(theoryText,'theory');
   await page.locator('#theory-search').fill('heterogeneity');
   assert((await page.locator('[data-theory-section]:visible').count())>=1,'theory search should leave at least one matching section');
   await page.locator('[data-view="interventions"]').first().click();
   await page.locator('[data-product-view="interventions"]').waitFor();
   const interventionText=await page.locator('[data-product-view="interventions"]').innerText();
   assert(interventionText.includes('21 randomized experiments'));assert(interventionText.includes('20 experiments'));assert.match(interventionText,/not normative CEM recommendations/i);assertNoInternalCodes(interventionText,'interventions');
   await page.locator('[data-lang="ro"]').click();assert.equal(await page.locator('html').getAttribute('lang'),'ro');
   assert.match(await page.locator('body').innerText(),/Intervenții studiate/);
   await page.locator('[data-lang="en"]').click();
   await page.goto(url);
   await page.keyboard.press('Tab');
   assert.equal(await page.evaluate(()=>document.activeElement?.classList.contains('skip-link')),true,'keyboard traversal should begin with skip link');
  }
  assert.deepEqual(errors,[],`${viewport.name}: runtime/resource errors`);
  await page.close();
 }
 console.log('CEM product-v2 vertical-slice visual usefulness gate passed');
}finally{
 if(browser)await browser.close();
 await new Promise(resolve=>server.close(resolve));
}
