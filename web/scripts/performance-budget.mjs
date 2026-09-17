import {readdir,stat} from 'node:fs/promises';
import {extname,join,relative} from 'node:path';

const ROOT=new URL('../dist/',import.meta.url);
const budgets={
 largestJavaScriptBytes:1_000_000,
 totalJavaScriptBytes:1_200_000,
 totalCssBytes:100_000,
 totalDistBytes:8*1024*1024,
 totalFileCount:120
};

async function filesRecursively(directory){
 const entries=await readdir(directory,{withFileTypes:true});
 const files=[];
 for(const entry of entries){
  const path=join(directory,entry.name);
  if(entry.isDirectory())files.push(...await filesRecursively(path));
  else if(entry.isFile())files.push(path);
 }
 return files;
}

const root=ROOT.pathname;
const files=await filesRecursively(root);
const inventory=[];
for(const path of files){
 const info=await stat(path);
 inventory.push({path:relative(root,path),bytes:info.size,ext:extname(path).toLowerCase()});
}

const js=inventory.filter(item=>item.ext==='.js');
const css=inventory.filter(item=>item.ext==='.css');
const sum=items=>items.reduce((total,item)=>total+item.bytes,0);
const largest=(items)=>items.reduce((max,item)=>Math.max(max,item.bytes),0);
const metrics={
 largestJavaScriptBytes:largest(js),
 totalJavaScriptBytes:sum(js),
 totalCssBytes:sum(css),
 totalDistBytes:sum(inventory),
 totalFileCount:inventory.length
};

let failed=false;
for(const [name,budget] of Object.entries(budgets)){
 const actual=metrics[name];
 const ok=actual<=budget;
 console.log(`${ok?'PASS':'FAIL'} ${name}: ${actual} <= ${budget}`);
 if(!ok)failed=true;
}

const largestJs=js.toSorted((a,b)=>b.bytes-a.bytes)[0];
if(largestJs)console.log(`Largest JS asset: ${largestJs.path} (${largestJs.bytes} bytes)`);
console.log(`Built files: ${inventory.length}`);

if(failed){
 console.error('OA-8 performance budget exceeded. Treat budget changes as explicit architectural decisions, not silent CI relaxation.');
 process.exit(1);
}
