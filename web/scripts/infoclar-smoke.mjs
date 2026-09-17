import {createServer} from 'node:http';
import {readFile,mkdir,writeFile} from 'node:fs/promises';
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
const address=server.address();assert(address&&typeof address!=='string');
const url=`http://127.0.0.1:${address.port}${prefix}`;
const screenshotDir=process.env.CEM_SCREENSHOTS;
const forbiddenNormal=/\b(?:Pwm|Uwm|Pprior|Aissue|Sobs|EngageIntent|Pengage|Paccess|Nexp|Eedit|Vcontent|Fpres|Gatt|Hneg|LR)\b|\b(?:REF|VAR|LINK|ODD)\.[A-Z0-9._-]+|(?:src\/|web\/src\/|\.tsx?\b|\.mjs\b|\.json\b)/i;

let browser;let checkpoint='launch';let currentPage;
const saveFailure=async(error)=>{
 if(!screenshotDir)return;
 await mkdir(screenshotDir,{recursive:true});
 const diagnostic=`checkpoint=${checkpoint}\nurl=${currentPage?.url()??url}\nerror=${error instanceof Error?error.stack??error.message:String(error)}\n`;
 await writeFile(path.join(screenshotDir,'product-concept-failure.txt'),diagnostic,'utf8').catch(()=>{});
 if(currentPage)await currentPage.screenshot({path:path.join(screenshotDir,'product-concept-failure.png'),fullPage:true}).catch(()=>{});
};
const visibleProductText=page=>page.locator('[data-product-surface]:visible, .context-drawer:visible').allTextContents().then(parts=>parts.join('\n'));
const assertNoInternalCodes=async(page,label)=>{
 const text=await visibleProductText(page);
 assert.equal(forbiddenNormal.test(text),false,`${label}: normal product surface leaks an internal identifier: ${text.match(forbiddenNormal)?.[0]??''}`);
 assert.equal(await page.locator('[data-product-surface]:visible code, .context-drawer:visible code').count(),0,`${label}: normal product surface must not render code tags`);
};
const assertOuterReflow=async(page,label)=>{
 const result=await page.evaluate(()=>({scrollWidth:document.documentElement.scrollWidth,innerWidth:window.innerWidth}));
 assert(result.scrollWidth<=result.innerWidth+2,`${label}: outer horizontal overflow ${result.scrollWidth}>${result.innerWidth}`);
};
const assertPathTraceability=async(page,label,mobile=false)=>{
 const steps=page.locator('.pathway-step');
 const connectors=page.locator('.pathway-connector');
 const n=await steps.count();assert(n>=4&&n<=8,`${label}: expected 4–8 primary mechanisms, got ${n}`);assert.equal(await connectors.count(),n-1,`${label}: connectors must join every consecutive mechanism`);
 const boxes=await steps.evaluateAll(items=>items.map(item=>{const r=item.getBoundingClientRect();return {left:r.left,right:r.right,top:r.top,bottom:r.bottom,width:r.width,height:r.height,scrollWidth:item.scrollWidth,clientWidth:item.clientWidth};}));
 for(const [index,box] of boxes.entries())assert(box.scrollWidth<=box.clientWidth+2,`${label}: step ${index+1} text overflows its card`);
 if(mobile){
  for(let i=1;i<boxes.length;i++)assert(boxes[i].top>boxes[i-1].bottom,`${label}: mobile pathway is not a clean top-to-bottom sequence at step ${i+1}`);
 }else{
  const viewport=await page.evaluate(()=>innerWidth);
  const first=boxes[0],last=boxes[boxes.length-1];
  assert(first.left>=0&&last.right<=viewport+2,`${label}: complete pathway is not visible in the desktop viewport (${first.left}…${last.right} vs ${viewport})`);
  for(let i=1;i<boxes.length;i++)assert(boxes[i].left>boxes[i-1].right,`${label}: mechanism cards overlap or reverse at ${i+1}`);
 }
};

try{
 browser=await chromium.launch({headless:true,...(process.env.CEM_BROWSER_PATH?{executablePath:process.env.CEM_BROWSER_PATH,args:['--no-sandbox','--disable-gpu']}:{})});
 const scenarios=[
  {name:'1440x900',width:1440,height:900,mobile:false},
  {name:'1366x768',width:1366,height:768,mobile:false},
  {name:'mobile-390x844',width:390,height:844,mobile:true}
 ];
 for(const scenario of scenarios){
  checkpoint=`${scenario.name}: open home`;
  const page=await browser.newPage({viewport:{width:scenario.width,height:scenario.height},reducedMotion:'reduce'});currentPage=page;page.setDefaultTimeout(10000);
  const errors=[];page.on('pageerror',e=>errors.push(e.message));page.on('response',r=>{if(r.status()>=400)errors.push(`${r.status()} ${r.url()}`);});
  await page.goto(url);await page.locator('[data-suite-standard="InfoClar Model Suite Design Standard v1.1"]').waitFor();
  assert.equal(await page.locator('[data-product-surface="home"]').count(),1,`${scenario.name}: first screen must be Questions/Home`);
  assert((await page.locator('[data-pathway-question]').count())>=11,`${scenario.name}: question library incomplete`);
  assert.equal(await page.locator('.atlas-map:visible').count(),0,`${scenario.name}: full model atlas must not be first screen`);
  assert.match(await page.locator('[data-product-surface="home"]').textContent(),/Choose a human question|Alege o întrebare umană/i);
  await assertNoInternalCodes(page,`${scenario.name} home`);await assertOuterReflow(page,`${scenario.name} home`);
  if(screenshotDir){await mkdir(screenshotDir,{recursive:true});await page.screenshot({path:path.join(screenshotDir,`product-home-${scenario.name}.png`),fullPage:true});}

  checkpoint=`${scenario.name}: repetition pathway`;
  await page.getByRole('button',{name:/How can repetition make a claim seem more true/i}).click();
  await page.locator('[data-product-surface="pathway"]').waitFor();
  assert.match(await page.locator('.pathway-title-row').textContent(),/repetition/i);
  for(const token of ['Empirical causal support','Empirical association','Executable model relation','Conceptual hypothesis','Interpretive link','Normative operator'])assert((await page.locator('.relation-legend').textContent()).includes(token),`${scenario.name}: relation legend missing ${token}`);
  await assertPathTraceability(page,`${scenario.name} repetition pathway`,scenario.mobile);await assertNoInternalCodes(page,`${scenario.name} pathway`);await assertOuterReflow(page,`${scenario.name} pathway`);
  if(screenshotDir)await page.screenshot({path:path.join(screenshotDir,`product-pathway-${scenario.name}.png`),fullPage:true});

  checkpoint=`${scenario.name}: familiarity evidence drawer`;
  await page.locator('[data-suite-focus="familiarity"]').click();await page.locator('.context-drawer').waitFor();
  const drawerText=await page.locator('.context-drawer').textContent();
  for(const token of ['WHAT IS IT?','WHAT INFLUENCES IT?','WHAT DOES IT INFLUENCE?','WHAT EVIDENCE SUPPORTS IT?','HOW LARGE IS THE EFFECT?','UNDER WHAT CONDITIONS?','WHAT COMPETING EXPLANATIONS EXIST?','WHAT ARE THE LIMITATIONS?'])assert(drawerText.includes(token),`${scenario.name}: drawer missing ${token}`);
  assert.match(drawerText,/182 studies/);assert.match(drawerText,/31,184/);assert.match(drawerText,/g=0\.37/);assert.match(drawerText,/risk.of.bias/i);
  await assertNoInternalCodes(page,`${scenario.name} mechanism drawer`);
  if(screenshotDir)await page.screenshot({path:path.join(screenshotDir,`product-mechanism-${scenario.name}.png`),fullPage:true});
  await page.locator('[data-close-mechanism]').click();

  checkpoint=`${scenario.name}: dashboard`;
  const dashboardText=await page.locator('.pathway-dashboard').textContent();
  for(const token of ['STRONGEST EVIDENCE','MAIN UNCERTAINTIES','IMPORTANT MODERATORS','COMPETING EXPLANATIONS','INTERVENTIONS STUDIED','WHAT CEM CANNOT CLAIM'])assert(dashboardText.includes(token),`${scenario.name}: dashboard missing ${token}`);

  if(scenario.name==='1440x900'){
   checkpoint='intervention evidence';await page.getByRole('button',{name:'Interventions'}).click();await page.locator('#interventionEvidenceSelect').selectOption('warning-labels');
   const interventionText=await page.locator('.intervention-detail').textContent();
   for(const token of ['Target mechanism','Study type','Population / context','Outcome','Effect estimate','Uncertainty','Heterogeneity','Durability','Moderators','Possible harms / trade-offs','Directness to CEM'])assert(interventionText.includes(token),`intervention missing ${token}`);
   assert.match(interventionText,/27\.6%/);assert.match(interventionText,/24\.7%/);assert.match(interventionText,/does not imply|does not.*recommend|CEM recommends/i);
   await assertNoInternalCodes(page,'intervention explorer');

   checkpoint='full model atlas';await page.getByRole('button',{name:'Full Model Atlas'}).click();assert.equal(await page.locator('.atlas-major-group').count()>=9,true);assert.equal(await page.locator('.atlas-map:visible').count(),0,'atlas must default to major levels');await page.locator('#atlasFilter').selectOption('memory-familiarity');await page.locator('.atlas-map').waitFor();assert((await page.locator('.atlas-node').count())>=3);assert.equal(await page.locator('.atlas-edge').count(),0,'atlas shows no spaghetti edges before selecting a mechanism');await page.locator('.atlas-node').first().click();assert((await page.locator('.atlas-edge').count())<=6,'atlas progressive disclosure must limit simultaneous edges');await assertNoInternalCodes(page,'full model atlas');

   checkpoint='theory public reader';await page.getByRole('button',{name:'Theory / Learn'}).click();await page.getByRole('button',{name:/Open full reader/i}).click();await page.locator('#suiteTheoryContext #theoryArticle').waitFor();await page.waitForFunction(()=>document.querySelector('#suiteTheoryContext #theoryArticle')?.getAttribute('aria-busy')!=='true');await page.waitForTimeout(50);await assertNoInternalCodes(page,'theory reader');

   checkpoint='technical provenance';await page.getByRole('button',{name:/Research \/ Provenance/i}).click();assert.match(await page.locator('[data-product-surface="technical"]').textContent(),/Identifiers|Evidence registry|Mechanism register/i);assert((await page.locator('[data-product-surface="technical"] code').count())>0,'technical provenance should retain research identifiers');
   checkpoint='workspace persistence';const workspace=JSON.parse(await page.evaluate(()=>localStorage.getItem('cem.workspace.v1.active')));assert.equal(workspace.schema_version,'1');
  }
  assert.deepEqual(errors,[],`${scenario.name}: runtime/resource errors`);
  await page.close();
 }
 console.log('CEM Product Concept Usefulness Gate and mandatory visual-audit capture passed');
}catch(error){await saveFailure(error);throw error;}finally{if(browser)await browser.close();await new Promise(resolve=>server.close(resolve));}
