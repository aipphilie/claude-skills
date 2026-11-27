const {chromium}=require('playwright');
const fs=require('node:fs/promises');
const path=require('node:path');

(async () => {
  const out=process.env.NETUPI_WORK || __dirname;
  const browser=await chromium.launch({executablePath:process.env.CHROMIUM_BIN || '/usr/bin/chromium',args:['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
  try {
    const page=await browser.newPage({viewport:{width:1080,height:1920}});
    const scene=await fs.readFile(path.join(out,'model.html'),'utf8');
    const poses=JSON.parse(await fs.readFile(path.join(out,'clips.json'),'utf8'));
    await page.route('http://netupi.test/**',r=>r.fulfill({contentType:'text/html',body:scene}));
    await page.route('https://cdn.jsdelivr.net/**',r=>r.fulfill({path:path.join(out,'three.module.js'),contentType:'text/javascript',headers:{'access-control-allow-origin':'*'}}));
    await page.goto('http://netupi.test/');
    await page.waitForFunction(()=>window.ready,null,{timeout:20000});
    await page.evaluate(()=>window.setStyle('flat'));
    for(const [name,frames] of Object.entries(poses)){
      const dir=path.join(out,'kadry',name);
      await fs.mkdir(dir,{recursive:true});
      for(const [i,pose] of frames.entries()){
        const png=await page.evaluate(p=>{window.pose(p);return document.querySelector('canvas').toDataURL('image/png').split(',')[1]},pose);
        await fs.writeFile(path.join(dir,String(i).padStart(3,'0')+'.png'),Buffer.from(png,'base64'));
      }
      console.log(name,frames.length);
    }
  } finally {await browser.close()}
})().catch(error=>{console.error(error);process.exitCode=1});
