import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {visualLanguage} from '../src/visual-language.ts';

const visualCss=readFileSync(new URL('../src/visual-language.css',import.meta.url),'utf8');
const mainSource=readFileSync(new URL('../src/main.ts',import.meta.url),'utf8');
const comparisonSource=readFileSync(new URL('../src/comparison.ts',import.meta.url),'utf8');
const narrativeSource=readFileSync(new URL('../src/narrative-stage.ts',import.meta.url),'utf8');

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

test('VP-2 selected navigation states keep non-color visual cues',()=>{
 assert.match(visualCss,/\.nav-groups button\[aria-pressed=true\]\{[^}]*font-weight:700;[^}]*box-shadow:inset 0 -3px 0 currentColor/s);
 assert.match(visualCss,/\.views button\[aria-pressed=true\]\{[^}]*border-bottom-color:var\(--accent\);[^}]*font-weight:700/s);
 assert.match(visualCss,/button\[aria-pressed=true\]\{font-weight:700\}/);
});

test('VP-2 disclosure and disabled controls retain explicit interaction treatment',()=>{
 assert.match(visualCss,/summary\{min-height:var\(--vl-target-min\);[^}]*cursor:pointer/s);
 assert.match(visualCss,/button:disabled,select:disabled,input\[type=number\]:disabled\{opacity:\.52;cursor:not-allowed\}/);
 assert.match(visualCss,/button:hover:not\(:disabled\),\.button-link:hover\{background:var\(--vl-control-hover\)\}/);
});

test('VP-3 chart surfaces are scroll-contained and dense tables remain readable',()=>{
 assert.match(visualCss,/\.chart-wrap,\.comparison-plot,\.narrative-chart\{[^}]*overflow-x:auto;[^}]*border:1px solid var\(--vl-border-soft\);[^}]*scrollbar-gutter:stable/s);
 assert.match(visualCss,/\.table-scroll\{[^}]*overflow:auto;[^}]*border:1px solid var\(--vl-border-soft\);[^}]*scrollbar-gutter:stable/s);
 assert.match(visualCss,/\.table-scroll thead th\{position:sticky;top:0;[^}]*background:var\(--vl-surface-inset\)/s);
 assert.match(visualCss,/font-variant-numeric:tabular-nums/);
});

test('VP-3 narrative trajectories use non-color line patterns',()=>{
 assert.match(visualCss,/polyline\.narrative-driver\{stroke-dasharray:none\}/);
 assert.match(visualCss,/polyline\.narrative-belief\{stroke-dasharray:10 4\}/);
 assert.match(visualCss,/polyline\.narrative-sharing\{stroke-dasharray:2 4\}/);
 assert.match(visualCss,/\.narrative-legend \.belief span\{border-top-style:dashed\}/);
 assert.match(visualCss,/\.narrative-legend \.sharing span\{border-top-style:dotted\}/);
});

test('VP-3 chart families retain accessible names, exact-value readouts and data alternatives',()=>{
 assert(mainSource.includes('role="img" aria-label="${tr('));
 assert(mainSource.includes('class="chart-readout" id="chartReadout"'));
 assert.match(mainSource,/class="results"[\s\S]*class="table-scroll"/);
 assert(comparisonSource.includes('role="img" aria-label="${title}. ${t('));
 assert.match(comparisonSource,/class="panel comparison-table"[\s\S]*class="table-scroll"/);
 assert(narrativeSource.includes('aria-labelledby="narrativeChartTitle narrativeChartDesc"'));
 assert(narrativeSource.includes('<desc id="narrativeChartDesc">'));
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
