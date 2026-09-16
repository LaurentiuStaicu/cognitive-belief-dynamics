import test from 'node:test';
import assert from 'node:assert/strict';
import {isAppView,navigationGroupForView,navigationGroups,navigationItem,requiredExistingViews,type AppView} from '../src/navigation.ts';

test('OA-3 has exactly four ordered user-purpose domains',()=>{
 assert.deepEqual(navigationGroups.map(group=>group.id),['understand','analyze','act','library']);
 assert.deepEqual(navigationGroups.map(group=>group.label.ro),['Înțelege','Analizează','Acționează','Bibliotecă']);
 assert.deepEqual(navigationGroups.map(group=>group.label.en),['Understand','Analyze','Act','Library']);
});

test('every pre-OA-3 view remains discoverable exactly once',()=>{
 const mapped=navigationGroups.flatMap(group=>group.items.map(item=>item.view));
 assert.deepEqual([...mapped].sort(),[...requiredExistingViews].sort());
 assert.equal(new Set(mapped).size,mapped.length);
});

test('each group default is a child of that group',()=>{
 for(const group of navigationGroups)assert(group.items.some(item=>item.view===group.defaultView),group.id+' default missing from group');
});

test('purpose mapping preserves project priority order',()=>{
 assert.equal(navigationGroupForView('learning').id,'understand');
 assert.equal(navigationGroupForView('structure').id,'understand');
 assert.equal(navigationGroupForView('process').id,'understand');
 assert.equal(navigationGroupForView('runs').id,'analyze');
 assert.equal(navigationGroupForView('comparison').id,'analyze');
 assert.equal(navigationGroupForView('planning').id,'act');
 assert.equal(navigationGroupForView('reference').id,'library');
});

test('navigation labels remain bilingual and non-empty',()=>{
 for(const view of requiredExistingViews as readonly AppView[]){
  const item=navigationItem(view);
  assert(item.label.ro.trim());assert(item.label.en.trim());assert(item.description.ro.trim());assert(item.description.en.trim());
 }
});

test('OA-3A does not introduce search or inspector destinations',()=>{
 const haystack=JSON.stringify(navigationGroups).toLowerCase();
 assert(!haystack.includes('search'));assert(!haystack.includes('căut'));assert(!haystack.includes('inspector'));
});

test('runtime view guard accepts only mapped application views',()=>{
 assert.equal(isAppView('learning'),true);
 assert.equal(isAppView('reference'),true);
 assert.equal(isAppView('search'),false);
 assert.equal(isAppView(''),false);
});
