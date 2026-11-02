// node cover_render.js <outdir> — рендер обложек A/B/C в PNG
const {chromium}=require('playwright');const fs=require('fs');const dir=__dirname;const out=process.argv[2];
(async()=>{const b=await chromium.launch();const p=await b.newPage();
 const js=['yarik.js','scenes.js','lie.js','cover.js'].map(f=>fs.readFileSync(dir+'/'+f,'utf8')).join('\n');
 await p.setContent(`<canvas id=c width=1080 height=1920></canvas><script>${js}\nwindow.g=document.getElementById('c').getContext('2d');</script>`);
 await p.evaluate(()=>document.fonts.load('900 50px Inter'));fs.mkdirSync(out,{recursive:true});
 for(const k of ['A']){const d=await p.evaluate(k=>{g.setTransform(1,0,0,1,0,0);g.globalAlpha=1;COVERS[k](g);return document.getElementById('c').toDataURL('image/png')},k);
  fs.writeFileSync(`${out}/cover-${k}.png`,Buffer.from(d.split(',')[1],'base64'))}
 await b.close()})();
