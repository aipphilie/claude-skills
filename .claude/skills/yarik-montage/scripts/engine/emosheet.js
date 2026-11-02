// node emosheet.js <engineDir> <out.png> <which: faces|poses>
const {chromium}=require('playwright');const fs=require('fs');const [dir,out,which]=process.argv.slice(2);
(async()=>{const b=await chromium.launch();const p=await b.newPage();p.on('pageerror',e=>console.log('ERR',e.message));p.on('console',m=>console.log(m.text()));
await p.setContent(`<html><body style="margin:0"><canvas id=c></canvas><script>${fs.readFileSync(dir+'/yarik.js','utf8')}\n${fs.readFileSync(dir+'/scenes.js','utf8')}\n${fs.readFileSync(dir+'/lie.js','utf8')}</script></body></html>`);
await p.evaluate(()=>document.fonts.load('900 50px Inter'));
const d=await p.evaluate(which=>{const c=document.getElementById('c'),g=c.getContext('2d');const t=1.0;
 const W=400,H=which==='poses'?560:470,COLS=4;
 const face=(fn)=>(x,y)=>{fn(x,y)};
 const Y=(o)=>(cx,cy)=>at(g,cx,cy,.36,()=>drawYarik(g,Object.assign({cap:true},o)));
 const faces=[
  ['norm — обычный','emo:norm',Y({emo:'norm'})],['smile — доволен','emo:smile',Y({emo:'smile'})],['laugh — ржёт','emo:laugh',Y({emo:'laugh'})],['shock — шок','emo:shock',Y({emo:'shock'})],
  ['bad — плохо','emo:bad',Y({emo:'bad'})],['cry — плачет','emo:cry',Y({emo:'cry'})],['hold — сдерживается','emo:hold, puff:1',Y({emo:'hold',puff:1})],['hold + tears','emo:hold, tears:1, flush:.6',Y({emo:'hold',tears:1,flush:.6})],
  ['angry — злой','emo:angry',Y({emo:'angry'})],['firm — решительный','emo:firm',Y({emo:'firm'})],['flush — покраснел','emo:smile, flush:.8',Y({emo:'smile',flush:.8})],['wink — подмигнул','emo:smile, wink:1',Y({emo:'smile',wink:1})],
  ['без кепки','cap:false',Y({emo:'norm',cap:false})],['моргнул / глаза закрыты','blink:1',Y({emo:'norm',blink:1})],['смотрит в сторону','look:-1 / look:1',(x,y)=>{at(g,x,y,.36,()=>drawYarik(g,{emo:'norm',cap:true,look:1}))}],['laugh без слёз','emo:laugh, tears:0',Y({emo:'laugh',tears:0})],
  ['в наушниках','ykp(...,{phones})',(x,y)=>ykp(g,x,y,.36,'smile',t,{})],['кайфует, глаза закрыты','ykp {closed:1, nod:1}',(x,y)=>ykp(g,x,y,.36,'smile',t,{closed:1,nod:1})],['мурашки','ykp {fur:1, phones:0}',(x,y)=>ykp(g,x,y,.36,'shock',t,{fur:1,phones:0})],['влюблён','yarikLove(...)',(x,y)=>yarikLove(g,x,y,.36,t,1)],
  ['глаза-звёзды','yk + starEyes',(x,y)=>{at(g,x,y,.36,()=>{drawYarik(g,{emo:'laugh',cap:true,tears:0});starEyes(g,t)})}],['плохо + эффекты','yarik(bad) + badFx',(x,y)=>{yarik(g,x,y,.36,'bad',t);badFx(g,x,y,.36,t)}],['друг (зеркальный)','friend(...)',(x,y)=>friend(g,x,y,.36,'laugh',t)],['она','girl(...)',(x,y)=>girl(g,x,y,.36,t)],
 ];
 const poses=[
  ['лежит на диване (В2)',"LIE[LIE_VAR](g,t)  // C2",fx=>LIE[LIE_VAR](g,t)],['на полу','yarikFloor(g,t,emo)',fx=>yarikFloor(g,t,'bad')],['за столом','yarikDesk(g,t,emo)',fx=>yarikDesk(g,t,'norm')],['ночь, не спит','bedAwake(g,t)',fx=>bedAwake(g,t)],
  ['кровать ночью','nightBed(g,t)',fx=>nightBed(g,t)],['сбоку','yarikSide(g,t)',fx=>yarikSide(g,t)],['идёт (шарф)','yarikWalk(...)',fx=>{bgFill(g,P.sage);yarikWalk(g,420,420,.6,'norm',t)}],['коллеги','person(g,x,y,s,{shirt,tie})',fx=>{bgFill(g,P.cream);person(g,230,470,1.1,{shirt:P.sage});person(g,610,470,1.1,{shirt:P.terra,hair:P.dark,tie:1})}],
  ['офис мозга (органы)','brainOffice(g,t)',fx=>brainOffice(g,t)],['мозг-персонаж','brain(g) + brainEyes(g,t)',fx=>{bgFill(g,P.beige);at(g,420,480,2.6,()=>{brain(g);brainEyes(g,t)})}],
 ];
 const L=which==='poses'?poses:faces;const rows=Math.ceil(L.length/COLS);c.width=W*COLS;c.height=H*rows+90;
 g.fillStyle=P.beige;g.fillRect(0,0,c.width,c.height);txt(g,which==='poses'?'Ярик — позы и сцены (в координатах карточки 840×990)':'Ярик — все эмоции и флаги drawYarik',c.width/2,52,40,P.choc);
 L.forEach(([name,code,fn],i)=>{const x=(i%COLS)*W,y=90+Math.floor(i/COLS)*H;g.save();rr(g,x+12,y+8,W-24,H-20,26);g.fillStyle=P.cream;g.fill();g.lineWidth=4;g.strokeStyle=P.choc;g.stroke();g.clip();
  if(which==='poses'){g.save();const k=Math.min((W-24)/840,(H-112)/990);g.translate(x+W/2-420*k,y+8);g.scale(k,k);g.beginPath();g.rect(0,0,840,990);g.clip();fn();g.restore()}else{fn(x+W/2,y+130)}
  g.restore();g.fillStyle=P.cream;g.fillRect(x+14,y+H-104,W-28,80);txt(g,name,x+W/2,y+H-72,28,P.choc);g.font='600 22px monospace';g.fillStyle=P.terra;g.textAlign='center';g.fillText(code,x+W/2,y+H-36)});
 return c.toDataURL('image/png')},which);
fs.writeFileSync(out,Buffer.from(d.split(',')[1],'base64'));await b.close()})();
