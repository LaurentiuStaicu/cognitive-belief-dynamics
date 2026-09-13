import {copyFileSync, mkdirSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
const root = new URL('../../', import.meta.url);
const target = new URL('../public/model/', import.meta.url);
mkdirSync(target, {recursive:true});
for (const name of ['variables','links','modules','validation_tests']) {
  copyFileSync(fileURLToPath(new URL(`model/${name}.json`, root)), fileURLToPath(new URL(`${name}.json`, target)));
}
