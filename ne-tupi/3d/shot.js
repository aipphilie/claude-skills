const { chromium } = require('playwright');
const poses = JSON.parse(process.argv[2]);
const [w,h] = [Number(process.argv[3]||540), Number(process.argv[4]||960)];
(async () => {
  const b = await chromium.launch({args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
  const pg = await b.newPage({viewport:{width:w,height:h}});
  pg.on('console', m => console.log('console:', m.text()));
  pg.on('pageerror', e => console.log('err:', e.message));
  await pg.goto('http://localhost:8777/3d/index.html');
  await pg.waitForFunction(() => window.ready);
  for (const [name, p] of Object.entries(poses)) {
    await pg.evaluate(p => { if (p.style) window.setStyle(p.style); return window.pose(p); }, p);
    await pg.screenshot({path: `3d/out/${name}.png`});
  }
  await b.close();
})();
