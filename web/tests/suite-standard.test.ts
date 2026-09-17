import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {calibrationExtension} from '../src/calibration-extension-contract.ts';
import {cemProductEdges,cemProductNodes} from '../src/cem-product-map.ts';
import {atlasGroups,edgeEvidence,interventionEvidence,mechanismEvidence,questionPathways,theoryTopics} from '../src/product-usefulness.ts';
const shellSource=readFileSync(new URL('../src/suite-overview.ts',import.meta.url),'utf8');
const shellCss=readFileSync(new URL('../src/suite-overview.css',import.meta.url),'utf8');
const understandingSource=readFileSync(new URL('../src/understanding.ts',import.meta.url),'utf8');
const mainSource=readFileSync(new URL('../src/main.ts',import.meta.url),'utf8');
const indexSource=readFileSync(new URL('../index.html',import.meta.url),'utf8');
const nodeIds=new Set(cemProductNodes.map(node=>node.id));
const edgeIds=new Set(cemProductEdges.map(edge=>edge.id));

test('Product Concept Recovery is questions-first, not a full-map landing page',()=>{
 assert.match(mainSource,/mountSuiteOverview\(suiteRoot/);
 assert.match(shellSource,/START WITH A PHENOMENON|ÎNCEPE CU UN FENOMEN/);
 assert.match(shellSource,/Choose a human question, not a model variable|Alege o întrebare umană, nu o variabilă a modelului/);
 assert.match(shellSource,/data-product-surface="home"/);
 assert.match(shellSource,/nav\('atlas'/);
 assert.equal(/grid-template-areas:'model theory' 'dashboard aux'/.test(shellCss),false);
 assert.equal(shellSource.includes('suite-model-panel'),false);
});

test('Usefulness Gate 1-2: human questions resolve to compact registered pathways',()=>{
 assert(questionPathways.length>=11);
 for(const question of questionPathways){
  assert(question.question.en.length>20,question.id);
  assert(question.nodes.length>=4&&question.nodes.length<=8,`${question.id}: ${question.nodes.length}`);
  assert.equal(question.edgeIds.length,question.nodes.length-1,question.id);
  assert(question.nodes.every(id=>nodeIds.has(id)),question.id);
  assert(question.edgeIds.every(id=>edgeIds.has(id)),question.id);
  assert(question.secondary.length>=1,question.id);
  for(const branch of question.secondary)assert(branch.nodes.every(id=>nodeIds.has(id)),question.id);
  assert(question.boundary.en.length>35,question.id);
 }
 assert.match(shellSource,/PATHWAY EXPLORER/);
 assert.match(shellSource,/secondary-branch/);
 assert.match(shellCss,/\.pathway-flow\{display:flex/);
 assert.match(shellCss,/@media\(max-width:640px\)[\s\S]*\.pathway-flow\{display:grid/);
});

test('Usefulness Gate 3-4: every registered product edge has an intelligible evidence relation status',()=>{
 assert.equal(edgeEvidence.length,cemProductEdges.length);
 assert.deepEqual(new Set(edgeEvidence.map(item=>item.edgeId)),edgeIds);
 const required=new Set(['EMPIRICAL_CAUSAL_SUPPORT','EMPIRICAL_ASSOCIATION','EXECUTABLE_MODEL_RELATION','CONCEPTUAL_HYPOTHESIS','INTERPRETIVE_LINK','NORMATIVE_OPERATOR']);
 assert.deepEqual(new Set(edgeEvidence.map(item=>item.status)),required);
 for(const relation of edgeEvidence){assert(relation.label.en.length>5);assert(relation.explanation.en.length>35);}
 for(const label of ['Empirical causal support','Empirical association','Executable model relation','Conceptual hypothesis','Interpretive link','Normative operator'])assert(shellSource.includes(label),label);
 assert.match(shellCss,/data-edge-status=EMPIRICAL_CAUSAL_SUPPORT/);
 assert.match(shellCss,/data-edge-status=EMPIRICAL_ASSOCIATION/);
 assert.match(shellCss,/data-edge-status=CONCEPTUAL_HYPOTHESIS/);
});

test('Usefulness Gate 3: internal codes are confined to Research / Technical provenance',()=>{
 const split=shellSource.split('RESEARCH / TECHNICAL PROVENANCE');assert(split.length>=2);const publicTemplate=split[0];
 for(const forbidden of ['<code>${esc(selected.identifiers','Evidence registry:</strong> <code>','theory slug:</strong> <code>'])assert.equal(publicTemplate.includes(forbidden),false,forbidden);
 assert.match(shellSource,/Research \/ Provenance|Research \/ Proveniență/);assert.match(shellSource,/technical-node-register/);assert.match(understandingSource,/scrubTheoryTechnicalIdentifiers/);assert.match(understandingSource,/technical file — see Research \/ Provenance/);
});

test('Usefulness Gate 5-6: mechanism evidence cards expose synthesis quality and effect sizes only conditionally',()=>{
 assert(mechanismEvidence.length>=5);
 for(const evidence of mechanismEvidence){
  assert(nodeIds.has(evidence.nodeId),evidence.nodeId);
  for(const field of [evidence.strength.en,evidence.studyType.en,evidence.studies.en,evidence.populations.en,evidence.uncertainty.en,evidence.heterogeneity.en,evidence.moderators.en,evidence.quality.en,evidence.replication.en,evidence.competing.en,evidence.limitations.en])assert(field.trim().length>=8,`${evidence.nodeId}: ${field}`);
  assert(evidence.sources.length>0,evidence.nodeId);
 }
 const familiarity=mechanismEvidence.find(item=>item.nodeId==='familiarity')!;
 assert.match(familiarity.studies.en,/182 studies/);assert.match(familiarity.populations.en,/31,184/);assert.match(familiarity.effectSize!.en,/g=0\.37/);assert.match(familiarity.quality.en,/risk-of-bias|Risk-of-bias/i);
 assert.match(shellSource,/WHAT EVIDENCE SUPPORTS IT/);assert.match(shellSource,/HOW LARGE IS THE EFFECT/);assert.match(shellSource,/evidence\.effectSize\?/);
});

test('Usefulness Gate 7: Intervention Explorer covers the nine empirical classes without becoming a recommender',()=>{
 const expected=['accuracy-prompts','debunking','friction','inoculation','lateral-reading','media-literacy','social-norms','source-labels','warning-labels'];assert.deepEqual(new Set(interventionEvidence.map(item=>item.id)),new Set(expected));
 for(const item of interventionEvidence){assert(item.targetNodes.every(id=>nodeIds.has(id)),item.id);for(const field of [item.targetMechanism.en,item.studyType.en,item.population.en,item.outcome.en,item.effect.en,item.uncertainty.en,item.heterogeneity.en,item.duration.en,item.moderators.en,item.adverse.en,item.directness.en])assert(field.length>15,item.id);assert(item.sources.every(source=>source.url.startsWith('https://')),item.id);}
 assert.match(shellSource,/INTERVENTION EVIDENCE EXPLORER/);assert.match(shellSource,/Intervention Evidence ≠ “CEM recommends this action”/);
});

test('Usefulness Gate 8: Theory/Learn is a broad manual and technical identifiers are not its public language',()=>{
 assert(theoryTopics.length>=20);const joined=theoryTopics.map(topic=>`${topic.label.en} ${topic.scope.en}`).join(' ');
 for(const concept of ['Purpose','Epistemology','Perception','Attention','Memory','familiarity','Source monitoring','Priors','Bayesian','World-model','Uncertainty','Heuristics','Framing','Emotion','Social cognition','Misinformation','Correction','Belief','Judgment','Action','Evidence hierarchy','cannot predict'])assert.match(joined,new RegExp(concept,'i'),concept);
 assert.match(shellSource,/The complete CEM manual|Manualul complet al CEM/);assert.match(shellSource,/data-suite-theory-chapter/);assert.match(understandingSource,/public reader explains the theory in natural language/);
});

test('Full Model Atlas is secondary, filtered and progressive rather than a spaghetti graph',()=>{
 assert(atlasGroups.length>=9);for(const group of atlasGroups)assert(group.nodes.every(id=>nodeIds.has(id)),group.id);
 assert.match(shellSource,/FULL MODEL ATLAS/);assert.match(shellSource,/atlasFilter/);assert.match(shellSource,/atlasZoom/);assert.match(shellSource,/relations appear only around the selected mechanism/);assert.match(shellSource,/relatedEdges=selected\?/);
});

test('Usefulness Gate 9 dashboard contains only pathway-relevant epistemic questions',()=>{
 for(const token of ['STRONGEST EVIDENCE','MAIN UNCERTAINTIES','IMPORTANT MODERATORS','COMPETING EXPLANATIONS','INTERVENTIONS STUDIED','WHAT CEM CANNOT CLAIM'])assert(shellSource.includes(token),token);
 for(const forbidden of ['softwareVersion','variableCount','moduleCount','referenceCount','validationCount','Model state & maturity','Starea și maturitatea modelului'])assert.equal(shellSource.includes(forbidden),false,forbidden);
 assert.match(shellSource,/does not predict an individual person’s behavior|nu prezice comportamentul unei persoane/);
});

test('responsive product layout gives the pathway the dominant surface and the mechanism context is dismissible',()=>{
 assert.match(shellCss,/\.pathway-workspace\{width:min\(100%,calc\(100vw - 2\.4rem\)\);min-height:72vh/);assert.match(shellSource,/data-close-mechanism/);assert.match(shellCss,/\.context-drawer\{position:fixed/);assert.match(shellCss,/@media\(max-width:900px\)[\s\S]*\.context-drawer\{position:static/);
});

test('English remains first-run default and bilingual choice persists locally',()=>{assert.match(indexSource,/<html lang="en">/);assert.match(mainSource,/cem\.ui\.language/);assert.match(mainSource,/savedLanguage==='ro'\|\|savedLanguage==='en'\?savedLanguage:'en'/);assert.match(mainSource,/localStorage\.setItem\('cem\.ui\.language',lang\)/);});

test('frozen boundaries remain frozen: no MOD.15 implementation, Advanced mode, calibration upload or Flatpak work',()=>{
 assert.equal(calibrationExtension.status,'PLANNED_POST_V1');assert.equal(calibrationExtension.mounted,false);assert.equal(calibrationExtension.uploadControlAvailable,false);assert(!mainSource.includes("./calibration-extension-contract"));assert(!shellSource.includes('type="file"'));assert.equal(/data-(?:mode|view)=\"advanced\"/i.test(shellSource),false);assert.equal(/advanced-mode/i.test(shellSource),false);assert.equal(/Flatpak|Web-first|web-first|Alpha\s+0\./.test(shellSource),false);assert.equal(mainSource.includes('id="releaseVersion"'),false);
});
