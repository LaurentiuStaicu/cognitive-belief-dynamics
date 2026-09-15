import {copyFileSync, mkdirSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
const root = new URL('../../', import.meta.url);
const target = new URL('../public/model/', import.meta.url);
mkdirSync(target, {recursive:true});
for (const name of ['variables','links','modules','validation_tests','references','subsystems','processes','evidence_snapshot','empirical_targets']) {
  copyFileSync(fileURLToPath(new URL(`model/${name}.json`, root)), fileURLToPath(new URL(`${name}.json`, target)));
}

const licenses=new URL('../public/licenses/',import.meta.url);
mkdirSync(licenses,{recursive:true});
for(const [source,dest] of [['LICENSE','MIT.txt'],['LICENSES/CC-BY-4.0.txt','CC-BY-4.0.txt'],['LICENSING.md','LICENSING.md']])copyFileSync(new URL(source,root),new URL(dest,licenses));
