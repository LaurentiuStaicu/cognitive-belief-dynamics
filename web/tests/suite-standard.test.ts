import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {calibrationExtension} from '../src/calibration-extension-contract.ts';
import {cemDiagnostics,cemProductEdges,cemProductNodes} from '../src/cem-product-map.ts';
import {interventionEvidence,mechanismEvidence,questionPathways,semanticFamilies,theoryTopics} from '../src/product-usefulness.ts';
const shellSource=readFileSync(new URL('../src/suite-overview.ts',import.meta.url),'utf8');
const shellCss=readFileSync(new URL('../src/suite-overview.css',import.meta.url),'utf8');
const understandingSource=readFileSync(new URL('../src/understanding.ts',import.meta.url),'utf8');
const mainSource=readFileSync(new URL('../src/main.ts',import.meta.url),'utf8');
const indexSource=readFileSync(new URL('../index.html',import.meta.url),'utf8');
const nodeIds=new Set(cemProductNodes.map(node=>node.id));
const edgeIds=new Set(cemProductEdges.map(edge=>edge.id));

test('InfoClar v1.1 remains the four-region shell but usefulness is primary',()=>{
 assert.match(mainSource,/mountSuiteOverview\(suiteRoot/);
 for(const token of ['suite-model-panel','suite-theory-panel','suite-dashboard-panel','suite-aux-panel'])assert(shellSource.includes(token),token);
 assert.match(shellCss,/grid-template-areas:'model theory' 'dashboard aux'/);
 assert.match(shellCss,/@media\(max-width:980px\)[\s\S]*grid-template-areas:'model' 'theory' 'dashboard' 'aux'/);
 assert.match(shellSource,/MECHANISM EXPLORER/);
 assert.match(shellSource,/What does CEM try to explain|Ce încearcă să explice CEM/);
});

test('Usefulness Gate 1-3: real mechanism architecture plus question pathways',()=>{
 assert(cemProductNodes.length>=20);
 assert(cemProductEdges.length>=23);
 for(const edge of cemProductEdges){assert(nodeIds.has(edge.source));assert(nodeIds.has(edge.target));}
 assert(questionPathways.length>=9);
 for(const question of questionPathways){assert(question.question.en.length>20);assert(question.nodes.length>=3);assert(question.nodes.every(id=>nodeIds.has(id)),question.id);assert(question.edgeIds.every(id=>edgeIds.has(id)),question.id);assert(question.boundary.en.length>30);}
 for(const token of ['SYSTEM OVERVIEW','QUESTION / PATHWAY EXPLORER','data-pathway-question','is-path'])assert(shellSource.includes(token),token);
 assert(semanticFamilies.length>=16);
 for(const family of semanticFamilies){assert(family.nodes.every(id=>nodeIds.has(id)),family.id);assert(family.modules.length>0);}
});

test('Usefulness Gate 4-5: evidence status, uncertainty and effect-size discipline',()=>{
 for(const node of cemProductNodes){assert(node.statuses.length>0);assert(node.summary.en.length>20);assert(node.limitation.en.length>20);}
 assert(mechanismEvidence.length>=5);
 for(const evidence of mechanismEvidence){assert(nodeIds.has(evidence.nodeId));assert(evidence.evidenceLevel.en.length>20);assert(evidence.evidenceType.en.length>10);assert(evidence.heterogeneity.en.length>20);assert(evidence.competing.en.length>20);assert(evidence.limitations.en.length>20);assert(evidence.sources.length>0);}
 assert.match(shellSource,/Effect size|Dimensiunea efectului/);
 assert.match(shellSource,/Not shown|Nu este afișată/);
 assert.match(shellSource,/Heterogeneity|Eterogenitate/);
 assert.match(shellSource,/Competing explanations|Explicații concurente/);
});

test('Usefulness Gate 6: intervention evidence is empirical and never automatic recommendation',()=>{
 const expected=['accuracy-prompts','debunking','friction','inoculation','lateral-reading','media-literacy','social-norms','source-labels','warning-labels'];
 assert.deepEqual(new Set(interventionEvidence.map(item=>item.id)),new Set(expected));
 for(const item of interventionEvidence){assert(item.targetNodes.every(id=>nodeIds.has(id)),item.id);assert(item.population.en.length>20);assert(item.outcome.en.length>10);assert(item.effect.en.length>20);assert(item.uncertainty.en.length>20);assert(item.heterogeneity.en.length>20);assert(item.duration.en.length>20);assert(item.moderators.en.length>20);assert(item.adverse.en.length>20);assert(item.directness.en.length>20);assert(item.sources.every(source=>source.url.startsWith('https://')),item.id);}
 assert.match(shellSource,/INTERVENTION EVIDENCE EXPLORER/);
 assert.match(shellSource,/does not mean “CEM automatically recommends this action”|nu înseamnă „CEM recomandă automat această acțiune”/i);
});

test('Usefulness Gate 7: mechanism selection reaches full contextual theory and source corpus',()=>{
 assert(theoryTopics.length>=12);
 const joined=theoryTopics.map(topic=>`${topic.label.en} ${topic.scope.en}`).join(' ');
 for(const concept of ['epistemology','Perception','attention','Memory','familiarity','source','Priors','Bayesian','world-model','Uncertainty','heuristics','Framing','emotion','Social','norms','Misinformation','correction','Belief','judgment','sharing','Evidence hierarchy','EXECUTABLE','CONCEPTUAL','cannot predict'])assert.match(joined,new RegExp(concept,'i'),concept);
 assert.match(shellSource,/data-suite-theory-chapter/);
 assert.match(shellSource,/Complete CEM corpus|Corpus complet CEM/);
 assert.match(understandingSource,/type Mode='theory'\|'mechanisms'\|'world-model'\|'tour'\|'active'/);
});

test('Usefulness Gate 8-9: no personal vulnerability prediction and dashboard is epistemic',()=>{
 assert.match(shellSource,/EPISTEMIC MECHANISMS & VULNERABILITIES/);
 assert.match(shellSource,/not a user profile|Nu este un profil al utilizatorului/i);
 assert.match(shellSource,/does not assign an individual vulnerability|nu atribuie vulnerabilitate/i);
 for(const forbidden of ['softwareVersion','modelSpecification','variableCount','moduleCount','referenceCount','validationCount','Model state & maturity','Starea și maturitatea modelului'])assert.equal(shellSource.includes(forbidden),false,forbidden);
 assert(cemDiagnostics.length>=6);
});

test('internal identifiers remain secondary and infrastructure stays contextual',()=>{
 assert.match(shellSource,/Secondary technical details|Detalii tehnice secundare/);
 assert.match(shellSource,/data-suite-tool="search"/);
 assert.match(shellSource,/data-suite-tool="inspector"/);
 for(const view of ['structure','runs','reference','process'])assert(shellSource.includes(`data-suite-view="${view}"`),view);
 for(const forbidden of ['navigation-shell','data-nav-group','semantic-inspector-global','class="intro"'])assert.equal(mainSource.includes(forbidden),false,forbidden);
});

test('English remains first-run default and bilingual choice persists locally',()=>{
 assert.match(indexSource,/<html lang="en">/);assert.match(mainSource,/cem\.ui\.language/);assert.match(mainSource,/savedLanguage==='ro'\|\|savedLanguage==='en'\?savedLanguage:'en'/);assert.match(mainSource,/localStorage\.setItem\('cem\.ui\.language',lang\)/);
});

test('frozen boundaries stay frozen: no Advanced mode, calibration upload or Flatpak work',()=>{
 assert.equal(calibrationExtension.status,'PLANNED_POST_V1');assert.equal(calibrationExtension.mounted,false);assert.equal(calibrationExtension.uploadControlAvailable,false);
 assert(!mainSource.includes("./calibration-extension-contract"));assert(!shellSource.includes('type="file"'));
 assert.equal(/data-(?:mode|view)=\"advanced\"/i.test(shellSource),false);assert.equal(/advanced-mode/i.test(shellSource),false);assert.equal(/Flatpak|Web-first|web-first|Alpha\s+0\./.test(shellSource),false);
 assert.equal(mainSource.includes('id="releaseVersion"'),false);assert.match(mainSource,/EMPIRICAL · EXECUTABLE · CONCEPTUAL · INTERPRETIVE/);
});
