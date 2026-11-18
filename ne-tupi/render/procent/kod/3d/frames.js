// рендер списка кадров: node frames.js frames.json outdir [w h]
const { chromium } = require('playwright');
const fs = require('fs');
const [file, out, style = 'flat', w = 1080, h = 1920, port = 8777] = process.argv.slice(2);
const jobs = JSON.parse(fs.readFileSync(file));
(async () => {
  const b = await chromium.launch({args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader']});
  const pg = await b.newPage({viewport: {width: +w, height: +h}});
  pg.on('pageerror', e => console.log('err:', e.message));
  await pg.goto(`http://localhost:${port}/3d/index.html`);
  await pg.waitForFunction(() => window.ready);
  await pg.evaluate(s => window.setStyle(s), style);
  for (const [name, frames] of Object.entries(jobs)) {
    fs.mkdirSync(`${out}/${name}`, {recursive: true});
    const anchors = [];
    for (let i = 0; i < frames.length; i++) {
      anchors.push(await pg.evaluate(p => window.pose(p), frames[i]));
      await pg.screenshot({path: `${out}/${name}/${String(i).padStart(3, '0')}.png`});
    }
    fs.writeFileSync(`${out}/${name}/anchors.json`, JSON.stringify(anchors));
    console.log(name, frames.length);
  }
  await b.close();
})();
