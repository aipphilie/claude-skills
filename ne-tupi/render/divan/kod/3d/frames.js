// рендер списка кадров: node frames.js frames.json outdir [w h]
const { chromium } = require('playwright');
const fs = require('fs');
const [file, out, style = 'flat', w = 1080, h = 1920, port = 8777] = process.argv.slice(2);
const jobs = JSON.parse(fs.readFileSync(file));
(async () => {
  const b = await chromium.launch({args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader']});
  const pg = await b.newPage({viewport: {width: +w, height: +h}});
  pg.on('pageerror', e => console.log('err:', e.message));
  const path = require('path'); const ROOT = path.resolve(__dirname, '..');
  await pg.route('http://local.test/**', r => { const p = path.join(ROOT, new URL(r.request().url()).pathname); r.fulfill({path: p}); });
  await pg.goto(`http://local.test/3d/index.html`);
  await pg.waitForFunction(() => window.ready);
  await pg.evaluate(s => window.setStyle(s), style);
  for (const [name, frames] of Object.entries(jobs)) {
    fs.mkdirSync(`${out}/${name}`, {recursive: true});
    for (let i = 0; i < frames.length; i++) {
      await pg.evaluate(p => window.pose(p), frames[i]);
      await pg.screenshot({omitBackground: true, path: `${out}/${name}/${String(i).padStart(3, '0')}.png`});
    }
    console.log(name, frames.length);
  }
  await b.close();
})();
