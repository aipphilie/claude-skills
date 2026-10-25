// Living handwriting: per-letter jitter that grows with `mess` (0 tidy … 1 barely holding the pencil)
function scrawl(g,text,x,y,size,mess,seed,o={}){
  const R=rng(seed);let cx=x,cy=y;const slant=-.22-mess*.12+(R()-.5)*.06,drift=(R()-.5)*mess*.08;
  for(const ch of text){
    if(ch===' '){cx+=size*(.28+R()*.12+mess*.15);continue}
    const sz=size*(1+(R()-.5)*(.08+mess*.35)),rot=(R()-.5)*(.05+mess*.32),dy=(R()-.5)*(2+mess*14);
    const ink=o.ink||[34,36,52],a=(.78+R()*.2)*(1-mess*.12);
    g.save();g.translate(cx,cy+dy+(cx-x)*drift);g.rotate(rot);g.transform(1,0,slant,1,0,0);
    g.font=`700 ${sz}px Hand`;g.fillStyle=`rgba(${ink[0]},${ink[1]},${ink[2]},${a})`;g.fillText(ch,0,0);
    if(mess>.45){g.globalAlpha=.35*mess;g.fillText(ch,1.5+R()*mess*3,R()*mess*3)} // tremor: shaky double stroke
    g.restore();cx+=g.measureText?(()=>{g.font=`700 ${sz}px Hand`;return g.measureText(ch).width})()*(.92+(R()-.5)*mess*.3):sz*.5;
  }
  if(o.strike){g.strokeStyle=`rgba(34,36,52,.8)`;g.lineWidth=3+mess*3;g.beginPath();g.moveTo(x-6,y-size*.3);for(let k=0;k<=8;k++)g.lineTo(x+(cx-x)*k/8,y-size*.3+(R()-.5)*8);g.stroke()}
  if(o.blot){g.fillStyle='rgba(30,30,45,.75)';g.beginPath();const bx=x+(cx-x)*(.3+R()*.5),by=y-size*.2;for(let k=0;k<14;k++){const a=k/14*Math.PI*2,r=size*(.12+R()*.14);k?g.lineTo(bx+Math.cos(a)*r,by+Math.sin(a)*r):g.moveTo(bx+r,by)}g.fill()}
  return cx;
}
window.renderFrame=function(){
  ctx.setTransform(1,0,0,1,0,0);ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
  const pg=ctx.createLinearGradient(0,0,W,1500);pg.addColorStop(0,'#d6cab0');pg.addColorStop(1,'#b3a68b');ctx.fillStyle=pg;ctx.fillRect(0,0,W,1500);
  const R=rng(5);for(let i=0;i<1500;i++){ctx.fillStyle=R()<.5?'rgba(255,255,255,.05)':'rgba(80,60,40,.05)';ctx.fillRect(R()*W,R()*1500,20+R()*60,2+R()*4)}
  ctx.strokeStyle='rgba(80,60,40,.35)';ctx.lineWidth=2;for(let y=250;y<1480;y+=110){ctx.beginPath();ctx.moveTo(40,y);ctx.lineTo(W-40,y);ctx.stroke()}
  scrawl(ctx,'Журнал наблюдений · ст. «Северная»',70,150,54,.05,1);
  const rows=[['День 12: пробовал узнать позывной. Молчат.',.0],['День 23: печь дымит — прочистил колено трубы',.12],['День 31: порвалась верёвка. Узел у 3-го столба',.25],
    ['День 49: −52. Генератор встал. Фильтр над печью',.4],['День 55: гудки. опять. не отвечаю',.55,{strike:true}],['День 60: диспетчер кашлянул на том же слове',.68],
    ['День 64: правая не держит карандаш',.82,{blot:true}],['День 70: они не прекратятся',.95]];
  rows.forEach(([t,m,o],i)=>{scrawl(ctx,t,70,235+i*110+90,48+m*14,m,10+i,o||{});ctx.font='700 22px '+MONO;ctx.fillStyle='rgba(181,69,47,.9)';ctx.fillText('mess '+m.toFixed(2),900,235+i*110+40)});
  finish(0);
};
window.ready=document.fonts.load('700 70px Hand').then(()=>true);
