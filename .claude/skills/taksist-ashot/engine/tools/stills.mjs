// node tools/stills.mjs prev/ 0.5 1.0,3.5,6.7  — кадры в нужные секунды (одна сборка бандла)
import {bundle} from '@remotion/bundler';
import {renderStill, selectComposition} from '@remotion/renderer';
import path from 'path';
const [out = 'prev', scale = '0.5', secs = ''] = process.argv.slice(2);
const chrome = process.env.REMOTION_CHROME || '/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell';
const serveUrl = await bundle({entryPoint: path.resolve('src/index.ts'), publicDir: path.resolve('public')});
const comp = await selectComposition({serveUrl, id: 'Ashot', browserExecutable: chrome});
const list = secs ? secs.split(',').map(Number) : Array.from({length: 12}, (_, i) => (i + 0.5) * comp.durationInFrames / 30 / 12);
for (const s of list) {
  const f = Math.min(comp.durationInFrames - 1, Math.round(s * 30));
  await renderStill({serveUrl, composition: comp, frame: f, output: path.resolve(`${out}/t${s.toFixed(2)}.png`), scale: Number(scale), browserExecutable: chrome, chromiumOptions: {gl: 'swangle'}});
  console.log('ok', s);
}
