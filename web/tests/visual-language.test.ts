import test from 'node:test';
import assert from 'node:assert/strict';
import {visualLanguage} from '../src/visual-language.ts';

test('visual spacing uses the documented six-pixel rhythm and safe content margin',()=>{
 assert.equal(visualLanguage.spacing.unitPx,6);
 assert.deepEqual(visualLanguage.spacing.scalePx,[6,12,18,24,36,48]);
 assert(visualLanguage.spacing.contentMarginMinPx>=12);
 for(const value of visualLanguage.spacing.scalePx)assert.equal(value%visualLanguage.spacing.unitPx,0);
});

test('typography is system-first and reader width remains restrained',()=>{
 assert.match(visualLanguage.typography.fontStack,/^system-ui/);
 assert(!visualLanguage.typography.fontStack.includes('http'));
 assert(visualLanguage.typography.readerMaxCh>=60&&visualLanguage.typography.readerMaxCh<=80);
 assert(visualLanguage.typography.bodyLineHeight>=1.5);
});

test('interaction targets and focus indicators exceed project minimums',()=>{
 assert(visualLanguage.interaction.targetMinPx>=44);
 assert(visualLanguage.interaction.focusRingPx>=2);
 assert(visualLanguage.interaction.focusOffsetPx>=2);
});

test('adaptive breakpoints are ordered and preserve existing shell thresholds',()=>{
 assert.equal(visualLanguage.breakpointsPx.compact,760);
 assert.equal(visualLanguage.breakpointsPx.medium,1050);
 assert(visualLanguage.breakpointsPx.compact<visualLanguage.breakpointsPx.medium);
});

test('chart series are not distinguished by color alone',()=>{
 const series=Object.values(visualLanguage.chartSeries);
 assert.equal(new Set(series.map(item=>item.dash)).size,series.length);
 assert.deepEqual(series.map(item=>item.dash),['none','8 4','2 4']);
 assert(series.every(item=>item.cssVar.startsWith('--series-')));
});

test('epistemic statuses have textual-category markers independent of color',()=>{
 const entries=Object.entries(visualLanguage.epistemicMarkers);
 assert.equal(entries.length,8);
 assert.equal(new Set(entries.map(([,marker])=>marker)).size,entries.length);
 assert(entries.every(([,marker])=>marker.length>0));
});
