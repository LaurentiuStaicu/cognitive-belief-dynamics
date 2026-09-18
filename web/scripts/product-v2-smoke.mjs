import {createServer} from 'node:http';
import {mkdir,readFile} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
import assert from 'node:assert/strict';
import {chromium} from 'playwright';

const dist=fileURLToPath(new URL('../dist/',import.meta.url));
const prefix='/cognitive-belief-dynamics/';
const screenshotDir=process.env.CEM_SCREENSHOTS||'';
if(screenshotDir)await mkdir(screenshotDir,{recursive:true});
const server=createServer(async(req,res)=>{try{const pathname=new URL(req.url,'http://localhost').pathname;if(!pathname.startsWith(prefix)){res.writeHead(404).end();return;}const file=path.resolve(dist,decodeURIComponent(pathname.slice(prefix.length))||'index.html');if(!file.startsWith(dist)){res.writeHead(403).end();return;}const data=await readFile(file);res.setHeader('Content-Type',({'.html':'text/html','.js':'text/javascript','.css':'text/css','.json':'application/json','.svg':'image/svg+xml','.md':'text/markdown'})[path.extname(file)]||'application/octet-stream');res.end(data);}catch{res.writeHead(404).end();}});
await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));const address=server.address();assert(address&&typeof address!=='string');const url=`http://127.0.0.1:${address.port}${prefix}`;

const banned=[/\bPwm\b/,/\bUwm\b/,/\bAissue\b/,/\bSobs\b/,/\bEngageIntent\b/,/\bPaccess\b/,/\bNexp\b/,/\bEedit\b/,/\bFpres\b/,/\bODD\./,/\bREF\./,/\bVAR\./,/\bLINK\./,/\bMOD\.\d+/i,/\bM1\.[A-Za-z0-9.]+/i,/\.(?:json|py|ts)\b/];
const questionIds=['repetition','source-credibility','framing','emotion-salience','memory-belief','correction-failure','world-model-update','social-norms','belief-to-action'];
function assertNoInternalCodes(text,label){for(const pattern of banned)assert(!pattern.test(text),`${label}: leaked internal token ${pattern}`);}

async function selectPathway(page,id){
 if(id!=='repetition'){
  const details=page.locator('.future-questions');
  if(!(await details.evaluate(element=>element.open)))await details.locator('summary').click();
 }
 await page.locator(`[data-question="${id}"]`).click();
 await page.locator(`[data-pathway="${id}"]`).waitFor();
}

async function assertPathway(page,viewport,id){
 await selectPathway(page,id);const pathway=page.locator(`[data-pathway="${id}"]`);
 const text=await pathway.innerText();assertNoInternalCodes(text,`${viewport.name} ${id}`);
 const nodeLocator=pathway.locator('.path-node');const nodes=await nodeLocator.evaluateAll(items=>items.map(item=>{const rect=item.getBoundingClientRect();return {top:rect.top,left:rect.left,right:rect.right,bottom:rect.bottom,width:rect.width};}));
 assert(nodes.length>=4&&nodes.length<=5,`${viewport.name} ${id}: pathway must contain four or five primary steps`);
 assert.equal(await pathway.locator('.path-edge').count(),nodes.length-1,`${viewport.name} ${id}: every adjacent step needs one relationship`);
 assert.equal(await pathway.locator('.edge-status').count(),0,`${viewport.name} ${id}: long relationship labels must not fragment the pathway`);
 assert((await page.locator('.pathway-panel .relation-key').count())>=1,`${viewport.name} ${id}: compact relationship legend missing`);
 const dimensions=await pathway.evaluate(element=>{const rect=element.getBoundingClientRect();return {left:rect.left,right:rect.right,scrollWidth:document.documentElement.scrollWidth,innerWidth:window.innerWidth};});
 assert(dimensions.left>=-1,`${viewport.name} ${id}: pathway begins outside viewport`);assert(dimensions.right<=viewport.width+1,`${viewport.name} ${id}: pathway exceeds viewport (${dimensions.right} > ${viewport.width})`);assert(dimensions.scrollWidth<=dimensions.innerWidth+1,`${viewport.name} ${id}: document overflow ${dimensions.scrollWidth} > ${dimensions.innerWidth}`);
 if(viewport.width<=760){for(let i=1;i<nodes.length;i++)assert(nodes[i].top>nodes[i-1].bottom,`${viewport.name} ${id}: pathway is not a clear vertical sequence`);}else{for(let i=1;i<nodes.length;i++)assert(nodes[i].left>nodes[i-1].right,`${viewport.name} ${id}: pathway is not a clear left-to-right sequence`);}
}

let browser;
try{
 browser=await chromium.launch({headless:true,...(process.env.CEM_BROWSER_PATH?{executablePath:process.env.CEM_BROWSER_PATH,args:['--no-sandbox','--disable-gpu']}: {})});
 const viewports=[{width:1440,height:900,name:'1440x900'},{width:1366,height:768,name:'1366x768'},{width:390,height:844,name:'mobile-390x844'}];
 for(const viewport of viewports){
  const page=await browser.newPage({viewport:{width:viewport.width,height:viewport.height},reducedMotion:'reduce'});const errors=[];page.on('pageerror',e=>errors.push(e.message));page.on('response',r=>{if(r.status()>=400)errors.push(`${r.status()} ${r.url()}`);});
  await page.goto(url);await page.locator('.product-header').waitFor();assert.equal(await page.locator('.suite-header,.navigation-shell,.suite-model-panel,#semanticInspector,#semanticSearchInput').count(),0,`${viewport.name}: legacy chrome mounted`);assert.equal(await page.locator('html').getAttribute('lang'),'en');
  const homeText=await page.locator('body').innerText();assertNoInternalCodes(homeText,`${viewport.name} home`);assert.match(homeText,/How can information influence what we believe and do\?/);assert.equal(await page.locator('[data-question]').count(),9,`${viewport.name}: all curated evidence-grounded questions must be selectable after the prototype gate`);assert.equal(await page.locator('[data-question="repetition"]').count(),1);assert.equal(await page.locator('.future-question-button').count(),8,`${viewport.name}: expanded question set incomplete`);
  if(screenshotDir)await page.screenshot({path:path.join(screenshotDir,`product-v2-home-${viewport.name}.png`),fullPage:true});
  if(viewport.name==='1440x900'&&screenshotDir){await page.locator('.future-questions summary').click();await page.screenshot({path:path.join(screenshotDir,'product-v2-question-catalog-1440x900.png'),fullPage:true});await page.locator('.future-questions summary').click();}

  for(const id of questionIds)await assertPathway(page,viewport,id);
  await selectPathway(page,'repetition');if(screenshotDir)await page.screenshot({path:path.join(screenshotDir,`product-v2-repetition-${viewport.name}.png`),fullPage:true});
  if(viewport.name==='1440x900'&&screenshotDir){await selectPathway(page,'source-credibility');await page.screenshot({path:path.join(screenshotDir,'product-v2-source-credibility-1440x900.png'),fullPage:true});await selectPathway(page,'world-model-update');await page.screenshot({path:path.join(screenshotDir,'product-v2-world-model-update-1440x900.png'),fullPage:true});await selectPathway(page,'repetition');}

  await page.locator('[data-mechanism="exposure"]').click();let drawer=page.locator('#context-drawer[data-open="true"]');await drawer.waitFor();let drawerText=await drawer.innerText();for(const label of ['WHAT IS IT?','WHY DOES IT MATTER?','WHAT INFLUENCES IT?','WHAT DOES IT INFLUENCE?','WHAT DOES THE EVIDENCE SAY?','HOW LARGE IS THE EFFECT?','WHEN DOES IT CHANGE?','WHAT ELSE COULD EXPLAIN IT?','WHAT ARE THE LIMITATIONS?','INTERVENTIONS STUDIED'])assert(drawerText.includes(label),`${viewport.name}: exposure drawer missing ${label}`);for(const evidence of ['182 studies','366 effect sizes','31,184 participants','g = 0.37','95% CI 0.30–0.44'])assert(drawerText.includes(evidence),`${viewport.name}: endpoint evidence missing ${evidence}`);assertNoInternalCodes(drawerText,`${viewport.name} exposure drawer`);let drawerBox=await drawer.boundingBox();assert(drawerBox);if(viewport.width>760)assert(drawerBox.width>=430,`${viewport.name}: drawer too narrow`);else assert(drawerBox.width>=viewport.width-2,`${viewport.name}: mobile drawer not full width`);await page.locator('[data-close-drawer]').click();

  await page.locator('[data-mechanism="familiarity"]').click();drawer=page.locator('#context-drawer[data-open="true"]');await drawer.waitFor();drawerText=await drawer.innerText();assert(drawerText.includes('A subjective memory signal'));assert(drawerText.includes('prominent explanations of illusory truth'));assert(!drawerText.includes('HOW LARGE IS THE EFFECT?'),`${viewport.name}: endpoint repetition effect must not be presented as a familiarity mediator coefficient`);assertNoInternalCodes(drawerText,`${viewport.name} familiarity drawer`);if(viewport.name==='1440x900'&&screenshotDir)await page.screenshot({path:path.join(screenshotDir,'product-v2-familiarity-drawer-1440x900.png'),fullPage:false});await page.keyboard.press('Escape');assert.equal(await page.locator('#context-drawer[data-open="true"]').count(),0,`${viewport.name}: Escape must dismiss the drawer`);

  if(viewport.name==='1440x900'){
   await page.locator('[data-view="theory"]').click();await page.locator('.theory-v2-reader h1').waitFor();assert((await page.locator('[data-theory-chapter]').count())>=15,'Theory must expose the full chapter corpus');let theoryText=await page.locator('[data-product-view="theory"]').innerText();assertNoInternalCodes(theoryText,'Theory default chapter');assert(theoryText.includes('Sources and further reading')||theoryText.includes('What this chapter does not claim'));
   const worldButton=page.locator('[data-theory-chapter="world-model-construction"]');if(await worldButton.count()){await worldButton.click();await page.locator('.theory-v2-reader h1').waitFor();theoryText=await page.locator('.theory-v2-reader').innerText();assertNoInternalCodes(theoryText,'Theory world-model chapter');assert.match(theoryText,/world model|internal model/i);}
   await page.locator('[data-theory-mode="glossary"]').click();assert((await page.locator('[data-glossary]').count())>=10,'Theory glossary unexpectedly small');if(screenshotDir)await page.screenshot({path:path.join(screenshotDir,'product-v2-theory-1440x900.png'),fullPage:false});

   await page.locator('.header-nav [data-view="explore"]').click();await selectPathway(page,'repetition');await page.locator('.header-nav [data-view="interventions"]').click();await page.locator('[data-product-view="interventions"]').waitFor();assert.equal(await page.locator('[data-intervention]').count(),3,'Only interventions relevant to the selected repetition pathway should be rendered');const interventionText=await page.locator('[data-product-view="interventions"]').innerText();for(const phrase of ['Accuracy prompts','Warning / fact-check labels','Debunking / rebuttal'])assert(interventionText.includes(phrase),`Repetition interventions missing ${phrase}`);for(const unrelated of ['Friction','Psychological inoculation / prebunking','Lateral reading','Media literacy','Social norms','Source credibility labels'])assert(!interventionText.includes(unrelated),`Unrelated intervention leaked into repetition slice: ${unrelated}`);assertNoInternalCodes(interventionText,'Interventions');assert.match(interventionText,/not normative recommendations/i);if(screenshotDir)await page.screenshot({path:path.join(screenshotDir,'product-v2-interventions-1440x900.png'),fullPage:false});

   await page.locator('.header-nav [data-view="atlas"]').click();await page.locator('#atlas-track').waitFor();assert.equal(await page.locator('.atlas-stage').count(),9);assert.equal(await page.locator('.atlas-stage[open]').count(),0,'Atlas must start macro-only/collapsed');const atlasText=await page.locator('[data-product-view="atlas"]').innerText();assertNoInternalCodes(atlasText,'Atlas');await page.locator('.atlas-stage').first().locator('summary').click();assert.equal(await page.locator('.atlas-stage[open]').count(),1);if(screenshotDir)await page.screenshot({path:path.join(screenshotDir,'product-v2-atlas-1440x900.png'),fullPage:false});

   await page.locator('[data-lang="ro"]').click();assert.equal(await page.locator('html').getAttribute('lang'),'ro');assertNoInternalCodes(await page.locator('body').innerText(),'Romanian Atlas');await page.locator('[data-lang="en"]').click();
   await page.goto(url);await page.keyboard.press('Tab');assert.equal(await page.evaluate(()=>document.activeElement?.classList.contains('skip-link')),true,'keyboard traversal must start with skip link');
  }
  assert.deepEqual(errors,[],`${viewport.name}: runtime/resource errors`);await page.close();
 }
 console.log('CBD product-v2 curated pathway expansion, usefulness, responsive and code-hygiene gate passed');
}finally{if(browser)await browser.close();await new Promise(resolve=>server.close(resolve));}
