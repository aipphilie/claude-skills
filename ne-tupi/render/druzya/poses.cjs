const { chromium } = require('playwright');
const fs = require('node:fs/promises');
const path = require('node:path');

const work = process.env.NETUPI_WORK;
const sourcePath = path.resolve(__dirname,'../divan/kod/3d/index.html');

(async () => {
  const browser = await chromium.launch({executablePath:process.env.CHROMIUM_BIN || undefined,args:['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
  try {
    const page = await browser.newPage({viewport:{width:720,height:1280}});
    const source = await fs.readFile(sourcePath,'utf8');
    const jobs = JSON.parse(await fs.readFile(path.join(work,'poses.json'),'utf8'));
    await page.route('http://netupi.test/**', route => route.fulfill({contentType:'text/html',body:source}));
    await page.route('https://cdn.jsdelivr.net/**', route => route.fulfill({path:path.join(work,'three.module.js'),contentType:'text/javascript',headers:{'access-control-allow-origin':'*'}}));
    await page.goto('http://netupi.test/');
    await page.waitForFunction(() => window.ready, null, {timeout:15000});
    await page.evaluate(() => window.setStyle('flat'));
    for (const [name, poses] of Object.entries(jobs)) {
      const folder = path.join(work,'poses',name);
      await fs.mkdir(folder,{recursive:true});
      for (const [i, pose] of poses.entries()) {
        const png = await page.evaluate(p => {
          window.pose(p);
          return document.querySelector('canvas').toDataURL('image/png').split(',')[1];
        }, pose);
        await fs.writeFile(path.join(folder,String(i).padStart(3,'0')+'.png'),Buffer.from(png,'base64'));
      }
      console.log(name,poses.length);
    }
  } finally {
    await browser.close();
  }
})().catch(e => { console.error(e); process.exitCode=1; });
