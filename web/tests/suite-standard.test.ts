import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {calibrationExtension} from '../src/calibration-extension-contract.ts';

const overviewSource=readFileSync(new URL('../src/suite-overview.ts',import.meta.url),'utf8');
const overviewCss=readFileSync(new URL('../src/suite-overview.css',import.meta.url),'utf8');
const understandingSource=readFileSync(new URL('../src/understanding.ts',import.meta.url),'utf8');
const mainSource=readFileSync(new URL('../src/main.ts',import.meta.url),'utf8');
const indexSource=readFileSync(new URL('../index.html',import.meta.url),'utf8');

test('InfoClar v1.1 keeps one simplified application with four common surfaces',()=>{
 assert.match(overviewSource,/data-suite-standard="InfoClar Model Suite Design Standard v1\.1"/);
 assert.match(overviewSource,/suite-model-panel/);
 assert.match(overviewSource,/suite-theory-panel/);
 assert.match(overviewSource,/suite-dashboard-panel/);
 assert.match(overviewSource,/suite-aux-panel/);
 assert.match(overviewCss,/grid-template-areas:'model theory' 'dashboard aux'/);
 assert.match(overviewCss,/@media\(max-width:760px\)[\s\S]*grid-template-areas:'model' 'theory' 'dashboard' 'aux'/);
});

test('cognitive diagram stays model-specific instead of imposing a suite-generic chart',()=>{
 for(const token of ['Nexp','F','B','W','Aissue','Paccess','Pengage','Share','EngageIntent','Access'])assert(overviewSource.includes(token),token);
 assert.match(overviewSource,/cem-mechanism-map/);
});

test('English is the first-run default and the bilingual choice persists locally',()=>{
 assert.match(indexSource,/<html lang="en">/);
 assert.match(mainSource,/cem\.ui\.language/);
 assert.match(mainSource,/savedLanguage==='ro'\|\|savedLanguage==='en'\?savedLanguage:'en'/);
 assert.match(mainSource,/localStorage\.setItem\('cem\.ui\.language',lang\)/);
 assert.match(mainSource,/lang==='ro'\?'EN':'RO'/);
});

test('overview is the default learning mode while deeper learning remains in the same app',()=>{
 assert.match(understandingSource,/type Mode='overview'\|'theory'\|'mechanisms'\|'world-model'\|'tour'\|'active'/);
 assert.match(understandingSource,/saved:'overview'/);
 assert.match(understandingSource,/mountSuiteOverview/);
});

test('calibration is a dormant post-v1 extension seam rather than an Advanced app',()=>{
 assert.equal(calibrationExtension.status,'PLANNED_POST_V1');
 assert.equal(calibrationExtension.mounted,false);
 assert.equal(calibrationExtension.uploadControlAvailable,false);
 assert.deepEqual([...calibrationExtension.acceptedExtensions],['.txt','.md','.csv','.tsv','.json','.xlsx','.ods']);
 assert(!mainSource.includes("./calibration-extension-contract"));
 assert(!overviewSource.includes('type="file"'));
 assert(!overviewSource.toLowerCase().includes('advanced mode'));
});
