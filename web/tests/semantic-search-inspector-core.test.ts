import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import type {SemanticIndex} from '../src/semantic.ts';
import {normalizeSearchText,searchSemanticIndex} from '../src/semantic-search.ts';
import {inspectSemanticIndex} from '../src/semantic-inspector.ts';

const semanticIndex=JSON.parse(readFileSync(new URL('../src/generated/semantic_index.json',import.meta.url),'utf8')) as SemanticIndex;

test('search normalization is case and Romanian-diacritic tolerant',()=>{assert.equal(normalizeSearchText('Înțelegere și ACURATEȚE'),'intelegere si acuratete');});
test('exact canonical IDs outrank lexical label matches deterministically',()=>{const result=searchSemanticIndex(semanticIndex,'VAR.FAMILIARITY.CLAIM',{lang:'en',limit:10});assert(result.length>0);assert.equal(result[0].id,'VAR.FAMILIARITY.CLAIM');assert.equal(result[0].match,'ID_EXACT');assert.equal(result[0].retrievalScore,1000);});
test('Romanian preferred labels and English alternatives are both searchable',()=>{const ro=searchSemanticIndex(semanticIndex,'familiaritate',{lang:'ro',limit:20});assert(ro.some(item=>item.id==='VAR.FAMILIARITY.CLAIM'));const en=searchSemanticIndex(semanticIndex,'familiarity',{lang:'en',limit:20});assert(en.some(item=>item.id==='VAR.FAMILIARITY.CLAIM'));});
test('semantic-type filter constrains retrieval without changing index',()=>{const items=searchSemanticIndex(semanticIndex,'accuracy',{lang:'en',semanticTypes:['COMPUTATIONAL_NODE'],limit:100});assert(items.length>0);assert(items.every(item=>item.semanticType==='COMPUTATIONAL_NODE'));});
test('empty search never returns a browse-all dump',()=>{assert.deepEqual(searchSemanticIndex(semanticIndex,'   ',{lang:'en'}),[]);});
test('retrieval ordering is deterministic for the same query',()=>{const a=searchSemanticIndex(semanticIndex,'evidence',{lang:'en',limit:100});const b=searchSemanticIndex(semanticIndex,'evidence',{lang:'en',limit:100});assert.deepEqual(a,b);});
test('inspector preserves entity status facets and relation layers',()=>{const item=inspectSemanticIndex(semanticIndex,'VAR.FAMILIARITY.CLAIM','en');assert(item&&item.kind==='entity');assert.equal(item.id,'VAR.FAMILIARITY.CLAIM');assert(item.related.length>0);assert(item.related.every(relation=>['REGISTERED_EVIDENCE_RELATION','COMPUTATIONAL_DEPENDENCY','DOCUMENTATION_RELATION'].includes(relation.layer)));});
test('relation inspector preserves scientific facets instead of flattening to a generic edge',()=>{const relation=semanticIndex.relations.find(item=>item.layer==='REGISTERED_EVIDENCE_RELATION');assert(relation);const inspected=inspectSemanticIndex(semanticIndex,relation.id,'en');assert(inspected&&inspected.kind==='relation');assert.equal(inspected.layer,'REGISTERED_EVIDENCE_RELATION');assert.deepEqual(inspected.statusFacets,relation.status_facets);assert.deepEqual(inspected.evidenceRefs,relation.evidence_refs);});
test('unknown inspector IDs fail closed',()=>{assert.equal(inspectSemanticIndex(semanticIndex,'DOES.NOT.EXIST','en'),undefined);});
