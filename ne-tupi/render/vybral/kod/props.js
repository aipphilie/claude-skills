// node props.js props.json outdir — рендер 3D-предметов кадрами 600x600 с прозрачным фоном
const { chromium } = require('playwright'); const fs = require('fs');
const [file, out, port = 8790] = process.argv.slice(2); const jobs = JSON.parse(fs.readFileSync(file));
(async () => {
  const b = await chromium.launch({args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader']});
  const pg = await b.newPage({viewport: {width: 600, height: 600}}); pg.on('pageerror', e => console.log('err:', e.message));
  await pg.goto(`http://localhost:${port}/3d/props.html`); await pg.waitForFunction(() => window.ready);
  for (const [name, frames] of Object.entries(jobs)) {
    fs.mkdirSync(`${out}/${name}`, {recursive: true});
    for (let i = 0; i < frames.length; i++) { await pg.evaluate(p => window.prop(p), frames[i]); await pg.screenshot({omitBackground: true, path: `${out}/${name}/${String(i).padStart(3, '0')}.png`}); }
    console.log(name, frames.length);
  }
  await b.close();
})();
