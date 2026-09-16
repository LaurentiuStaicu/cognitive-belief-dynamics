import {copyFileSync, cpSync, mkdirSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
const root = new URL('../../', import.meta.url);
const target = new URL('../public/model/', import.meta.url);
mkdirSync(target, {recursive:true});
for (const name of ['variables','links','modules','validation_tests','references','subsystems','processes','evidence_snapshot','empirical_targets','theory_index','theory_glossary']) {
  copyFileSync(fileURLToPath(new URL(`model/${name}.json`, root)), fileURLToPath(new URL(`${name}.json`, target)));
}

const generated=new URL('../src/generated/',import.meta.url);
mkdirSync(generated,{recursive:true});
copyFileSync(
 fileURLToPath(new URL('model/computational_dependencies.json',root)),
 fileURLToPath(new URL('computational_dependencies.json',generated))
);

const licenses=new URL('../public/licenses/',import.meta.url);
mkdirSync(licenses,{recursive:true});
for(const [source,dest] of [['LICENSE','MIT.txt'],['LICENSES/CC-BY-4.0.txt','CC-BY-4.0.txt'],['LICENSING.md','LICENSING.md']])copyFileSync(new URL(source,root),new URL(dest,licenses));

const theorySource=new URL('../../docs/theory/',import.meta.url);
const theoryTarget=new URL('../public/theory/',import.meta.url);
mkdirSync(theoryTarget,{recursive:true});
cpSync(theorySource,theoryTarget,{recursive:true,force:true});
