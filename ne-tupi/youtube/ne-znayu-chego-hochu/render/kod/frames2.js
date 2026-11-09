// node frames2.js track.json start end outdir [w h]
const { chromium } = require('playwright'); const fs = require('fs');
const [file, a, b, out, w = 720, h = 1280, port = 8777] = process.argv.slice(2);
const frames = JSON.parse(fs.readFileSync(file)); fs.mkdirSync(out, {recursive: true});
(async () => {
  const br = await chromium.launch({args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader']});
  const pg = await br.newPage({viewport: {width: +w, height: +h}});
  await pg.goto(`http://localhost:${port}/3d/index.html`); await pg.waitForFunction(() => window.ready);
  await pg.evaluate(s => window.setStyle(s), 'flat');
  for (let i = +a; i < Math.min(+b, frames.length); i++) {
    const f = `${out}/${String(i).padStart(5, '0')}.png`;
    if (fs.existsSync(f)) continue;
    await pg.evaluate(p => window.pose(p), frames[i]);
    await pg.screenshot({path: f});
    if (i % 500 == 0) console.log(i);
  }
  await br.close();
})();
