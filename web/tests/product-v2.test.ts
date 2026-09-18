import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {pathways,mechanisms} from '../src/product-v2/pathways.ts';
import {interventions} from '../src/product-v2/interventions.ts';

const index=await readFile(new URL('../index.html',import.meta.url),'utf8');
const main=await readFile(new URL('../src/product-v2/main.ts',import.meta.url),'utf8');
const pathwaySource=await readFile(new URL('../src/product-v2/pathways.ts',import.meta.url),'utf8');
const interventionSource=await readFile(new URL('../src/product-v2/interventions.ts',import.meta.url),'utf8');
const theory=await readFile(new URL('../src/product-v2/theory.ts',import.meta.url),'utf8');
const atlas=await readFile(new URL('../src/product-v2/atlas.ts',import.meta.url),'utf8');
const style=await readFile(new URL('../src/product-v2/style.css',import.meta.url),'utf8');
const expandedStyle=await readFile(new URL('../src/product-v2/expanded.css',import.meta.url),'utf8');
const contract=await readFile(new URL('../../docs/product/CEM_FRONTEND_REBUILD_ZERO.md',import.meta.url),'utf8');

test('clean-slate entry point mounts only product-v2',()=>{
 assert(index.includes('/src/product-v2/main.ts'));
 assert(!index.includes('/src/main.ts'));
 for(const legacy of ['suite-overview','navigation-shell','cem-product-map','semanticInspector','semanticSearchInput'])assert(!main.includes(legacy),`new entry point must not depend on ${legacy}`);
 assert(!main.includes("from '../main'"));
});

test('question-first product now covers the approved mechanism families without becoming a registry browser',()=>{
 assert(pathways.length>=8&&pathways.length<=10,`expected a small curated question set, got ${pathways.length}`);
 const ids=new Set(mechanisms.map(item=>item.id));
 for(const pathway of pathways){
  assert(pathway.mechanismIds.length>=4&&pathway.mechanismIds.length<=5,`${pathway.id}: pathway should stay compact`);
  assert.equal(pathway.edges.length,pathway.mechanismIds.length-1,`${pathway.id}: every adjacent mechanism needs one edge status`);
  for(const id of pathway.mechanismIds)assert(ids.has(id),`${pathway.id}: missing mechanism ${id}`);
  assert(pathway.strongest.en.length>40&&pathway.uncertainty.en.length>30&&pathway.moderators.en.length>15&&pathway.cannot.en.length>20,`${pathway.id}: usefulness strip is incomplete`);
 }
 for(const required of ['repetition','source-credibility','framing','emotion-salience','memory-belief','correction-failure','world-model-update','social-norms','belief-to-action'])assert(pathways.some(path=>path.id===required),`missing question pathway ${required}`);
});

test('mechanism details expose the required explanatory and evidence fields',()=>{
 for(const mechanism of mechanisms){
  for(const field of ['what','why','evidence','conditions','competing','limitations','interventions'] as const)assert(mechanism[field].en.length>=20,`${mechanism.id}: ${field} is underdeveloped`);
  assert(mechanism.influencedBy.length>0&&mechanism.influences.length>0,`${mechanism.id}: influence directions missing`);
  assert(mechanism.theorySlug.length>4,`${mechanism.id}: no theory cross-link`);
 }
 const familiarity=mechanisms.find(item=>item.id==='familiarity')!;
 assert(pathwaySource.includes('182 studies'));
 assert(pathwaySource.includes('31,184'));
 assert(pathwaySource.includes('g = 0.37'));
 assert(familiarity.sources.some(source=>source.url.includes('s41467-026-70041-x')));
});

test('intervention explorer contains all nine evidence classes and remains non-prescriptive',()=>{
 assert.equal(interventions.length,9);
 for(const required of ['accuracy','debunking','friction','inoculation','lateral-reading','media-literacy','social-norms','source-labels','warning'])assert(interventions.some(item=>item.id===required),`missing intervention ${required}`);
 for(const item of interventions){for(const field of ['target','evidence','outcome','effect','context','moderators','duration','tradeoffs','limitations'] as const)assert(item[field].en.length>=20,`${item.id}: ${field} incomplete`);assert(item.sources.length>0,`${item.id}: no source`);}
 assert(main.includes('not normative recommendations'));
 assert(interventionSource.includes('42 independent studies'));
 assert(interventionSource.includes('160 media-literacy interventions'));
});

test('full Theory is a separate reader with corpus navigation, search, glossary, citations and code naturalization',()=>{
 for(const marker of ['theory_index','theory_glossary','theory-v2-search','data-theory-mode','chapterSources','naturalize'])assert(theory.includes(marker),`Theory reader missing ${marker}`);
 assert(theory.includes('Back to pathway'));
 assert(theory.includes('technical provenance'));
 assert(expandedStyle.includes('.theory-v2'));
});

test('Full Model Atlas is secondary, macro-only by default and progressive',()=>{
 assert(main.includes("nav('atlas'"));
 assert(atlas.includes('SECONDARY'));
 assert.equal((atlas.match(/id:'/g)??[]).length,9);
 for(const stage of ['Information environment','Exposure and selection','Attention and access','Memory and familiarity','Priors and world model','Appraisal and uncertainty','Belief and judgment','Social context','Action and sharing'])assert(atlas.includes(stage),`atlas missing ${stage}`);
 assert(atlas.includes('<details class="atlas-stage"'));
 assert(expandedStyle.includes('.atlas-viewport'));
});

test('normal pathway/intervention product copy contains no registry identifiers or implementation file paths',()=>{
 const publicCopy=`${pathwaySource}\n${interventionSource}`;
 const banned=[/\bPwm\b/,/\bUwm\b/,/\bAissue\b/,/\bSobs\b/,/\bEngageIntent\b/,/\bPaccess\b/,/\bNexp\b/,/\bEedit\b/,/\bFpres\b/,/\bODD\./,/\bREF\./,/\bVAR\./,/\bLINK\./,/\.(?:json|py|ts)\b/];
 for(const pattern of banned)assert(!pattern.test(publicCopy),`public copy leaks ${pattern}`);
});

test('World3 visual family is explicit but CBD does not copy the World3 layout',()=>{
 for(const token of ['#f5f6f8','#ffffff','#dfe3e8','0 8px 28px rgba(35, 45, 60, 0.08)','14px','1120px','620px'])assert(style.includes(token),`missing World3-aligned token ${token}`);
 assert(contract.includes('World3 → CBD design token mapping'));
 assert(contract.includes('does **not** copy World3\'s 2-column/2×2 product layout'));
});

test('pathway remains visually dominant and details stay on demand',()=>{
 assert(expandedStyle.includes('.pathway-row.path-count-5'));
 assert(main.includes('context-drawer'));
 for(const heading of ['WHAT IS IT?','WHY DOES IT MATTER?','WHAT INFLUENCES IT?','WHAT DOES IT INFLUENCE?','WHAT DOES THE EVIDENCE SAY?','WHEN DOES IT CHANGE?','WHAT ELSE COULD EXPLAIN IT?','WHAT ARE THE LIMITATIONS?','INTERVENTIONS STUDIED'])assert(main.includes(heading));
});

test('MOD.15, Flatpak, calibration upload and new scientific mechanics remain outside the product implementation',()=>{
 for(const forbidden of ['MOD.15','Flatpak','human calibration','input type="file"'])assert(!main.includes(forbidden));
});
