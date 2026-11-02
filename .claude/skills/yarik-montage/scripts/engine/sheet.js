const {chromium}=require('playwright');const fs=require('fs');const dir=__dirname;
(async()=>{const b=await chromium.launch();const p=await b.newPage();p.on('pageerror',e=>console.log('ERR',e.message));
await p.setContent(`<html><body style="margin:0"><canvas id=c width=1080 height=1920></canvas><script>${process.env.TIMING?'const TIMING='+fs.readFileSync(process.env.TIMING,'utf8')+';':''}\n${fs.readFileSync(dir+'/yarik.js','utf8')}\n${fs.readFileSync(dir+'/scenes.js','utf8')}\n${fs.readFileSync(dir+'/lie.js','utf8')}\nwindow.g=document.getElementById('c').getContext('2d');</script></body></html>`);
await p.evaluate(()=>document.fonts.load('900 50px Inter'));
const ts=JSON.parse(process.argv[3]);fs.mkdirSync(process.argv[2],{recursive:true});
for(let i=0;i<ts.length;i++){const d=await p.evaluate(t=>{render(g,t);return document.getElementById('c').toDataURL('image/jpeg',.8)},ts[i]);fs.writeFileSync(`${process.argv[2]}/f${String(i).padStart(3,'0')}.jpg`,Buffer.from(d.split(',')[1],'base64'))}
await b.close()})();
