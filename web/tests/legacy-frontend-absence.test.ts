import test from 'node:test';
import assert from 'node:assert/strict';
import {access,readdir,readFile} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import path from 'node:path';

type Contract={authoritative_entrypoint:string;authoritative_frontend_root:string;deleted_files:string[];removed_shell_identifiers:string[];forbidden_legacy_imports:string[]};
const repoRoot=fileURLToPath(new URL('../../',import.meta.url));
const webRoot=path.join(repoRoot,'web');
const contract=JSON.parse(await readFile(path.join(webRoot,'legacy-frontend-removal-contract.json'),'utf8')) as Contract;

async function exists(file:string){try{await access(file);return true;}catch{return false;}}
async function walk(dir:string):Promise<string[]>{const entries=await readdir(dir,{withFileTypes:true});const result:string[]=[];for(const entry of entries){const target=path.join(dir,entry.name);if(entry.isDirectory())result.push(...await walk(target));else result.push(target);}return result;}
const rel=(file:string)=>path.relative(repoRoot,file).split(path.sep).join('/');

test('all files declared legacy are physically absent',async()=>{for(const file of contract.deleted_files)assert.equal(await exists(path.join(repoRoot,file)),false,`${file} must stay deleted; git history is the archive`);});

test('index has exactly one authoritative frontend entrypoint',async()=>{const index=await readFile(path.join(webRoot,'index.html'),'utf8');const moduleScripts=[...index.matchAll(/<script\s+type=["']module["'][^>]*src=["']([^"']+)["']/g)].map(match=>match[1]);assert.deepEqual(moduleScripts,['/src/product-v2/main.ts']);assert(!index.includes('/src/main.ts'));});

test('all active CSS belongs to the authoritative product frontend',async()=>{const css=(await walk(path.join(webRoot,'src'))).filter(file=>file.endsWith('.css')).map(rel);assert(css.length>0);for(const file of css)assert(file.startsWith('web/src/product-v2/'),`non-authoritative stylesheet found: ${file}`);});

test('authoritative frontend does not import or identify the removed shell',async()=>{const root=path.join(repoRoot,contract.authoritative_frontend_root);const files=(await walk(root)).filter(file=>/\.(?:ts|css)$/.test(file));const source=(await Promise.all(files.map(file=>readFile(file,'utf8')))).join('\n');for(const token of contract.forbidden_legacy_imports)assert(!source.includes(token),`legacy import returned: ${token}`);for(const token of contract.removed_shell_identifiers)assert(!source.includes(token),`legacy shell identifier returned: ${token}`);assert(!source.includes("from '../main'"));assert(!source.includes('data-domain="understand"'));assert(!source.includes('data-domain="analyze"'));assert(!source.includes('data-domain="act"'));assert(!source.includes('data-domain="library"'));});

test('headless domain modules do not reintroduce presentation styles',async()=>{const coreRoot=path.join(webRoot,'src','core');const files=await walk(coreRoot);assert(files.length>=7);assert(files.every(file=>file.endsWith('.ts')));const source=(await Promise.all(files.map(file=>readFile(file,'utf8')))).join('\n');for(const marker of ['innerHTML','querySelector','HTMLElement','document.','<section','<button'])assert(!source.includes(marker),`presentation leaked into headless core: ${marker}`);});
