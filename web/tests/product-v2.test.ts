import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';

const index=await readFile(new URL('../index.html',import.meta.url),'utf8');
const main=await readFile(new URL('../src/product-v2/main.ts',import.meta.url),'utf8');
const content=await readFile(new URL('../src/product-v2/content.ts',import.meta.url),'utf8');
const style=await readFile(new URL('../src/product-v2/style.css',import.meta.url),'utf8');
const contract=await readFile(new URL('../../docs/product/CEM_FRONTEND_REBUILD_ZERO.md',import.meta.url),'utf8');

test('clean-slate entry point mounts only product-v2',()=>{
 assert(index.includes('/src/product-v2/main.ts'));
 assert(!index.includes('/src/main.ts'));
 for(const legacy of ['suite-overview','navigation-shell','cem-product-map','semanticInspector','semanticSearchInput'])assert(!main.includes(legacy),`new entry point must not depend on ${legacy}`);
 assert(!main.includes("from '../main'"));
});

test('prototype contains exactly one enabled vertical slice before expansion',()=>{
 const enabled=(content.match(/enabled:true/g)??[]).length;
 assert.equal(enabled,1);
 for(const step of ['Repeated exposure','Familiarity','Belief judgment','Sharing / action'])assert(content.includes(step));
 assert(content.includes('182 studies'));
 assert(content.includes('31,184'));
 assert(content.includes('g = 0.37'));
});

test('normal product source contains no internal CEM registry identifiers or implementation paths',()=>{
 const publicSource=`${main}\n${content}`;
 const banned=[/\bPwm\b/,/\bUwm\b/,/\bAissue\b/,/\bSobs\b/,/\bEngageIntent\b/,/\bPaccess\b/,/\bNexp\b/,/\bEedit\b/,/\bFpres\b/,/\bODD\./,/\bREF\./,/\bVAR\./,/\bLINK\./,/\.json\b/,/\.py\b/];
 for(const pattern of banned)assert(!pattern.test(publicSource),`public product source leaks ${pattern}`);
});

test('World3 visual family is explicit but CEM does not copy the World3 layout',()=>{
 for(const token of ['#f5f6f8','#ffffff','#dfe3e8','0 8px 28px rgba(35, 45, 60, 0.08)','14px','1120px','620px'])assert(style.includes(token),`missing World3-aligned token ${token}`);
 assert(contract.includes('World3 → CEM design token mapping'));
 assert(contract.includes('does **not** copy World3\'s 2-column/2×2 product layout'));
});

test('pathway is compact and details are on demand',()=>{
 assert(style.includes('grid-template-columns: minmax(170px,1fr)'));
 assert(main.includes('context-drawer'));
 assert(main.includes('WHAT DOES THE EVIDENCE SAY?'));
 assert(main.includes('HOW LARGE IS THE EFFECT?'));
 assert(main.includes('WHAT ELSE COULD EXPLAIN IT?'));
 assert(main.includes('INTERVENTIONS STUDIED'));
});

test('MOD.15, Flatpak and human calibration remain outside the new product implementation',()=>{
 for(const forbidden of ['MOD.15','Flatpak','human calibration','input type="file"'])assert(!main.includes(forbidden));
});
