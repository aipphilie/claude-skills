// node events.js [timing.json] > ev.json — времена склеек кадров (для звуков монтажа)
const fs=require('fs');const dir=__dirname;
const H={get:(o,k)=>k==='width'?100:(typeof k==='symbol'?undefined:F),set:()=>true};const F=new Proxy(function(){},{get:H.get,apply:()=>F,set:()=>true});
global.document={fonts:{load:()=>0}};
let code=fs.readFileSync(dir+'/yarik.js','utf8')+'\n'+fs.readFileSync(dir+'/scenes.js','utf8')+'\n;return {SC,TOTAL};';
if(process.argv[2])code='const TIMING='+fs.readFileSync(process.argv[2],'utf8')+';\n'+code;
let cur=-1;const {SC,TOTAL}=new Function('SHOT_LOG',code)(i=>{cur=i});
const ev=[];let last='';
for(let f=0;f<TOTAL*60;f++){const t=f/60;let si=SC.findIndex(s=>t>=s.t0&&t<s.t0+s.d);if(si<0)continue;const s=SC[si];cur=-1;try{s.draw(F,t-s.t0,s.d)}catch(e){}
  const key=si+':'+cur;if(key!==last){ev.push({t:+t.toFixed(3),scene:si,shot:cur});last=key}}
console.log(JSON.stringify({total:TOTAL,ev}));
