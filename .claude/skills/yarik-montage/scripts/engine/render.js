// node render.js preview <outdir>  — PNG по кадру из каждой сцены
// node render.js video <out.mp4>   — полный рендер через ffmpeg
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');const {spawn}=require('child_process');
const dir=__dirname;const [mode,out]=process.argv.slice(2);const LV=process.env.LIE_VAR||null;
(async()=>{
  const b=await chromium.launch();const p=await b.newPage();
  await p.setContent(`<html><body style="margin:0"><canvas id=c width=1080 height=1920></canvas><script>${process.env.TIMING?'const TIMING='+fs.readFileSync(process.env.TIMING,'utf8')+';':''}\n${fs.readFileSync(dir+'/yarik.js','utf8')}\n${fs.readFileSync(dir+'/scenes.js','utf8')}\n${fs.readFileSync(dir+'/lie.js','utf8')}\nwindow.g=document.getElementById('c').getContext('2d');window.info={total:TOTAL,sc:SC.map(s=>({t0:s.t0,d:s.d,clean:s.clean}))};</script></body></html>`);
  await p.evaluate(()=>document.fonts.load('900 50px Inter'));await p.evaluate(()=>document.fonts.load('800 50px Inter'));
  if(LV&&LV!=='x')await p.evaluate(v=>{LIE_VAR=v},LV);const info=await p.evaluate(()=>window.info);console.log('total',info.total.toFixed(1),'s');
  const grab=async t=>Buffer.from((await p.evaluate(t=>{render(g,t);return document.getElementById('c').toDataURL('image/jpeg',.93)},t)).split(',')[1],'base64');
  if(mode==='frames'){const spec=JSON.parse(process.argv[4]);fs.mkdirSync(out,{recursive:true});for(const [name,v,t,ss] of spec){await p.evaluate(([v,ss])=>{LIE_VAR=v;if(ss)SUB_STYLE=ss},[v,ss]);fs.writeFileSync(path.join(out,name+'.jpg'),await grab(t))}}
  else if(mode==='preview'){fs.mkdirSync(out,{recursive:true});
    for(let i=0;i<info.sc.length;i++){const s=info.sc[i];fs.writeFileSync(path.join(out,`s${String(i+1).padStart(2,'0')}.jpg`),await grab(s.t0+s.d*.85))}}
  else{const n=Math.ceil(info.total*30);
    const ff=spawn('ffmpeg',['-y','-loglevel','error','-f','image2pipe','-framerate','30','-c:v','mjpeg','-i','-',...(process.env.AUDIO?['-i',process.env.AUDIO,'-af','apad','-t',String(info.total)]:['-f','lavfi','-i','anullsrc=r=48000:cl=stereo','-shortest']),'-c:v','libx264','-pix_fmt','yuv420p','-crf','20','-preset','medium','-r','30','-c:a','aac','-b:a','128k','-movflags','+faststart',out],{stdio:['pipe','inherit','inherit']});
    for(let f=0;f<n;f++){const buf=await grab(f/30);if(!ff.stdin.write(buf))await new Promise(r=>ff.stdin.once('drain',r));if(f%300===0)console.log('frame',f,'/',n)}
    ff.stdin.end();await new Promise(r=>ff.on('close',r));
    fs.writeFileSync(out.replace(/\.mp4$/,'.timings.json'),JSON.stringify(info,null,1));}
  await b.close();
})();
