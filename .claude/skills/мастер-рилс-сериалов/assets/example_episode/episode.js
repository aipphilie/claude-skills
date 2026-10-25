// ============ Episode 1 «Сигнал» — shots synced to the voice timeline ============
const ph=id=>PH[id], ps=id=>PH[id].s, pe=id=>PH[id].e;
const wt=(id,k)=>PH[id].w[k][1];                       // time of k-th word of a phrase
const BEEPS=[.15,.42,.69, 6.75,7.0,7.25, 50.5,50.78,51.06, 64.85,65.12,65.39, 83.5,83.78,84.06];
const beepOn=t=>BEEPS.some(b=>t>=b&&t<b+.13);
const sinceBeep=t=>{let d=99;for(const b of BEEPS)if(t>=b)d=Math.min(d,t-b);return d};
function keys(t,K){let k=0;while(k<K.length-2&&t>K[k+1][0])k++;const a=K[k],b=K[k+1],p=easeInOut((t-a[0])/(b[0]-a[0]||1));return a.slice(1).map((v,i)=>lerp(v,b[i+1],p))}
function shakeAt(t,list,amp=8,d=.2){let s=0;for(const b of list)if(t>=b&&t<b+d)s=Math.max(s,amp*(1-(t-b)/d));return s}
function dark(g,a){g.fillStyle=`rgba(0,0,0,${a})`;g.fillRect(0,0,W,H)}

// ---------------- radio close-up ----------------
function cord(g,p){ // p: 0 plugged in the wall, 1 lying on the table
  const A=[[230,1090],[205,1140],[185,1160],[160,1160],[135,1160],[116,1120],[116,1075]];
  const B=[[230,1090],[180,1180],[170,1340],[330,1420],[420,1465],[430,1520],[370,1560]];
  const P=A.map((a,i)=>[lerp(a[0],B[i][0],p),lerp(a[1],B[i][1],p)]);
  g.strokeStyle='#0a0e0f';g.lineWidth=13;g.lineCap='round';g.beginPath();g.moveTo(...P[0]);g.bezierCurveTo(...P[1],...P[2],...P[3]);g.bezierCurveTo(...P[4],...P[5],...P[6]);g.stroke();
  const px=lerp(116,370,p),py=lerp(1045,1560,p);
  g.save();g.translate(px,py);g.rotate(lerp(0,-2.4,p));poly(g,[[-26,-22],[26,-22],[26,26],[-26,26]],'#1c2324');
  if(p>.05){g.fillStyle='#9a9a8e';g.fillRect(-14,26,7,28);g.fillRect(7,26,7,28)}g.restore();
  return [px,py];
}
function radio(g,t,o){
  const [cx,cy,z]=keys(t,o.K);const sh=shakeAt(t,BEEPS.filter(b=>b>o.t0&&b<o.t1),7)+shakeAt(t,o.hits||[],12,.25);
  g.save();cam(g,cx+Math.sin(t*90)*sh,cy+Math.cos(t*77)*sh,z);g.drawImage(S1,0,0);
  const fl=(.85+.15*Math.sin(t*13)*Math.sin(t*7.3))*(o.lamp??1);
  g.globalCompositeOperation='lighter';glow(g,960,1010,520*fl,'rgba(232,150,60,A)',.30*fl);glow(g,960,1010,110,'rgba(255,190,100,A)',.55*fl);g.globalCompositeOperation='source-over';
  poly(g,[[960,1060],[972,1030],[960,995],[948,1030]],'#ffd27a');
  // dial: lit only when powered — or for a moment on each beep
  const on=typeof o.on==='function'?o.on(t):o.on,flash=beepOn(t)?1:Math.max(0,1-sinceBeep(t)/.35)*.6;
  if(!on){g.fillStyle=`rgba(22,17,12,${.88*(1-flash)})`;g.fillRect(292,737,261,121)}
  g.fillStyle='#121918';g.fillRect(540,935,46,70);g.fillStyle='#8a948f';g.fillRect(554,on?928:972,18,40);
  let nx=402+Math.sin(t*2.1)*2;if(beepOn(t))nx+=46;g.fillStyle='#c0261b';g.fillRect(nx,738,4,118);
  for(const b of BEEPS){const d=t-b;if(d>0&&d<.6){g.strokeStyle=`rgba(255,226,160,${(1-d/.6)*.75})`;g.lineWidth=5;g.beginPath();g.arc(705,805,112+d*420,0,7);g.stroke()}}
  if(o.clock)clockObj(g,560,1225,70,o.clock(t));
  const pl=cord(g,o.plug?o.plug(t):(on?0:1));
  g.fillStyle='#ffd9a0';for(const m of MOTES){g.globalAlpha=.25+.25*Math.sin(t*2+m.s*20);g.fillRect(m.x+Math.sin(t*.4+m.s*9)*30,m.y-((t*14+m.s*400)%400),3,3)}g.globalAlpha=1;
  const T=g.getTransform();g.restore();
  if(o.dim)dark(g,o.dim);
  return {T,pl};
}
function clockObj(g,x,y,r,min){ // min = minutes after midnight
  g.save();g.translate(x,y);
  for(const s of [-1,1]){g.fillStyle='#4a524c';g.beginPath();g.arc(s*r*.62,-r*.92,r*.36,Math.PI,0);g.fill()}
  g.fillStyle='#2b322f';g.fillRect(-r*.7,r*.85,r*.18,r*.3);g.fillRect(r*.52,r*.85,r*.18,r*.3);
  g.fillStyle='#3b4440';g.beginPath();g.arc(0,0,r,0,7);g.fill();g.fillStyle='#d8cfb8';g.beginPath();g.arc(0,0,r*.84,0,7);g.fill();
  g.fillStyle='#2a2420';for(let i=0;i<12;i++){g.save();g.rotate(i*Math.PI/6);g.fillRect(-r*.025,-r*.8,r*.05,i%3?r*.09:r*.16);g.restore()}
  const hA=(min/60%12)/12*Math.PI*2,mA=(min%60)/60*Math.PI*2;
  g.strokeStyle='#15110e';g.lineCap='round';g.lineWidth=r*.07;g.beginPath();g.moveTo(0,0);g.lineTo(Math.sin(hA)*r*.45,-Math.cos(hA)*r*.45);g.stroke();
  g.lineWidth=r*.045;g.beginPath();g.moveTo(0,0);g.lineTo(Math.sin(mA)*r*.7,-Math.cos(mA)*r*.7);g.stroke();
  const sA=(min*60%60)/60*Math.PI*2;g.strokeStyle='#b5452f';g.lineWidth=r*.02;g.beginPath();g.moveTo(0,0);g.lineTo(Math.sin(sA)*r*.74,-Math.cos(sA)*r*.74);g.stroke();
  g.fillStyle='#15110e';g.beginPath();g.arc(0,0,r*.06,0,7);g.fill();g.restore();
}

// ---------------- portrait ----------------
const PBG=mk();{const g=PBG.getContext('2d'),R=rng(13);g.fillStyle='#0f171b';g.fillRect(0,0,W,H);
  for(let x=-20;x<W;x+=110)poly(g,jag([[x,0],[x+106,0],[x+106,H],[x,H]],R,3,10),R()<.5?'#121c21':'#0e161a');}
function portrait(g,t,o){
  g.drawImage(PBG,0,0);
  const lamp=typeof o.lamp==='function'?o.lamp(t):(o.lamp??1),fl=(.85+.15*Math.sin(t*11)*Math.sin(t*4.3))*lamp;
  g.globalCompositeOperation='lighter';glow(g,120,760,1000,'rgba(232,150,60,A)',.34*fl);
  if(o.radioGlow)glow(g,540,1900,900,'rgba(240,170,80,A)',.28*o.radioGlow*(beepOn(t)?1.6:1));g.globalCompositeOperation='source-over';
  const [fx,fy,z]=keys(t,o.K||[[0,540,900,1],[1,540,900,1]]);const sh=shakeAt(t,o.hits||[],14,.3);
  g.save();g.translate(540+Math.sin(t*80)*sh,900+Math.cos(t*70)*sh);g.scale(z,z);g.translate(-fx,-fy);
  g.translate(540,900);g.scale(1.25,1.25);
  const blink=((t+(o.bo||0))%3.6<.13)?1:0;
  drawAndrey(g,{look:typeof o.look==='function'?o.look(t):(o.look||0),blink:o.wide?-.35:blink});
  if(o.mic){g.save();g.translate(-40,150);g.rotate(-.35);poly(g,[[-34,-70],[34,-70],[40,70],[-40,70]],'#15191b');g.fillStyle='#2e3639';for(let y=-60;y<60;y+=14)g.fillRect(-28,y,56,6);
    g.fillStyle='#0c0e0f';g.fillRect(-10,70,20,120);g.restore();
    poly(g,jag([[-140,250],[-70,190],[10,230],[0,320],[-120,330]],rng(3),6,3),'#7a5a44')}
  g.restore();
  if(lamp<1)dark(g,(1-lamp)*.75);
  if(o.radioGlow){g.fillStyle='#0b1012';g.fillRect(0,1720,W,200);g.fillStyle='rgba(240,170,80,.5)';g.fillRect(380,1736,320,10)}
}

// ---------------- map with rings, timed to words ----------------
function mapScene2(g,t,t0,t1,rt,ml){
  const s=lerp(1.5,.8,easeOut((t-t0)/(t1-t0))),sx=540,sy=820;
  g.fillStyle='#000';g.fillRect(0,0,W,H);
  g.save();g.setTransform(s,0,0,s,sx-MCX*s,sy-MCY*s);g.drawImage(MAP,0,0);g.restore();
  const fog=g.createRadialGradient(sx,sy,200,sx,sy,1100);fog.addColorStop(0,'rgba(5,10,13,0)');fog.addColorStop(1,'rgba(5,10,13,.75)');g.fillStyle=fog;g.fillRect(0,0,W,H);
  for(let k=0;k<4;k++){const p=((((t-t0)*.7+k/4)%1)+1)%1;g.strokeStyle=`rgba(232,162,74,${(1-p)*.35})`;g.lineWidth=2;g.beginPath();g.arc(sx,sy,p*720*s,0,7);g.stroke()}
  for(const [d,r,lab] of [[0,217,'100 КМ'],[.5,433,'200 КМ'],[1.05,650,'300 КМ — НИ ДУШИ']]){const a0=rt+d;if(t<a0)continue;const p=easeOut((t-a0)/.7),rr=r*s*p;
    g.setLineDash([16,12]);g.lineDashOffset=-t*20;g.strokeStyle='rgba(232,162,74,.9)';g.lineWidth=3;g.beginPath();g.arc(sx,sy,rr,0,7);g.stroke();g.setLineDash([]);
    g.fillStyle='rgba(232,162,74,.05)';g.beginPath();g.arc(sx,sy,rr,0,7);g.fill();
    if(p>.6){const lx=sx+Math.cos(-.75)*rr,ly=sy+Math.sin(-.75)*rr,last=r===650;g.globalAlpha=ease((p-.6)/.4);tag(g,Math.min(lx+8,W-30-(last?470:190)),ly,lab,'#e8a24a',last?'#e8a24a':null);g.globalAlpha=1}}
  if(t>ml){const p=easeOut((t-ml)/.7),ex=sx+760*p,ey=sy-900*p;
    g.setLineDash([6,10]);g.strokeStyle='#cfe3e8';g.lineWidth=3;g.beginPath();g.moveTo(sx,sy);g.lineTo(ex,ey);g.stroke();g.setLineDash([]);
    if(p>.8){g.globalAlpha=ease((p-.8)/.2);tag(g,520,330,'МАТЕРИК ↗  СВЯЗЬ 08:00 / 20:00','#cfe3e8');g.globalAlpha=1}}
  const fl=.85+.15*Math.sin(t*9);g.globalCompositeOperation='lighter';glow(g,sx,sy,140,'rgba(232,150,60,A)',.55*fl);g.globalCompositeOperation='source-over';
  g.fillStyle='#ffb447';g.fillRect(sx-9,sy-9,18,18);g.strokeStyle='#0b1418';g.lineWidth=3;g.strokeRect(sx-9,sy-9,18,18);
  g.globalAlpha=clamp((t-t0-.2)/.3,0,1);tag(g,sx+28,sy+44,'СТ. «СЕВЕРНАЯ»','#e8a24a');g.globalAlpha=1;
  drawSnow(g,t,.6,.5);
}

// ---------------- days flipping in the log ----------------
const TABLE=mk();{const g=TABLE.getContext('2d'),R=rng(17);g.fillStyle='#22190f';g.fillRect(0,0,W,H);
  for(let i=0;i<40;i++){const y=R()*H;g.strokeStyle='rgba(0,0,0,.3)';g.lineWidth=2+R()*4;g.beginPath();g.moveTo(0,y);g.lineTo(W,y+(R()-.5)*60);g.stroke()}}
function paperPage(g,x,y,w,h,col){poly(g,jag([[x,y],[x+w,y],[x+w,y+h],[x,y+h]],rng(x|0),2,5),col);g.strokeStyle='rgba(70,60,45,.35)';g.lineWidth=2;for(let yy=y+90;yy<y+h-30;yy+=52){g.beginPath();g.moveTo(x+30,yy);g.lineTo(x+w-30,yy);g.stroke()}}
function days(g,t,t0,c0,c1){
  g.drawImage(TABLE,0,0);g.globalCompositeOperation='lighter';glow(g,200,500,1100,'rgba(232,150,60,A)',.25);g.globalCompositeOperation='source-over';
  const z=lerp(1,1.08,(t-t0)/2.5);g.save();g.translate(540,900);g.scale(z,z);g.translate(-540,-900);
  poly(g,[[110,430],[970,430],[990,1430],[90,1430]],'#100b07');
  paperPage(g,120,450,420,960,'#b9ad92');paperPage(g,540,450,420,960,'#c8bc9f');
  const n=Math.round(lerp(1,47,ease((t-c0)/(c1-c0))));
  g.fillStyle='#3a2e24';g.font='700 46px Hand';g.fillText('День '+Math.max(1,n-1),170,560);g.fillText('День '+n,590,560);
  g.font='700 34px Hand';g.fillStyle='rgba(58,46,36,.75)';for(let i=0;i<6;i++){g.fillText('−3'+((n+i)%9)+'°   ветер '+(8+(n*3+i)%9)+' м/с',170,660+i*104);g.fillText('−3'+((n+i+4)%9)+'°   давл. 74'+((n+i)%9),590,660+i*104)}
  if(t>c0&&t<c1){const f=((t-c0)*14)%1,wdt=420*Math.cos(f*Math.PI);poly(g,[[540,450],[540+wdt,440+Math.sin(f*Math.PI)*30],[540+wdt,1420],[540,1410]],wdt>0?'#d4c8ab':'#a99d84')}
  g.restore();
  g.save();g.textAlign='center';g.font='900 150px Mont';g.fillStyle='#f5b83d';g.shadowColor='rgba(0,0,0,.8)';g.shadowBlur=30;g.fillText(String(n),540,330);g.font='700 30px '+MONO;g.fillStyle='#e7ddc4';g.fillText('ДЕНЬ НА СТАНЦИИ',540,380);g.restore();
}

// ---------------- full figure (side view, facing right) ----------------
function figure(g,x,y,s,ph,o={}){
  g.save();g.translate(x,y);g.scale(o.flip?-s:s,s);
  const sw=Math.sin(ph)*.38,bob=Math.abs(Math.sin(ph))*6;g.translate(0,-bob);
  for(const k of [-1,1]){g.save();g.translate(0,-135);g.rotate(sw*k);poly(g,[[-17,0],[17,0],[14,120],[-14,120]],k<0?'#161c1c':'#1e2626');poly(g,[[-16,112],[28,112],[30,136],[-16,136]],'#0e1111');g.restore()}
  poly(g,[[-48,-140],[46,-140],[40,-250],[-36,-252]],'#34423a');poly(g,[[-48,-140],[0,-140],[2,-252],[-36,-252]],'#475a4b');
  g.save();g.translate(18,-232);g.rotate(o.reach??(-.25+Math.sin(ph+1)*.25));poly(g,[[-14,-10],[86,-8],[86,16],[-14,18]],'#3d4d42');poly(g,jag([[80,-14],[112,-12],[116,16],[80,20]],rng(5),3,2),'#5a4332');g.restore();
  // scarf tail flapping in the wind
  const f=Math.sin((o.t||0)*14),f2=Math.sin((o.t||0)*11+1);
  poly(g,[[-30,-262],[30,-262],[32,-244],[-32,-244]],'#8a3b2a');poly(g,[[-28,-258],[-70,-262+f*8],[-110,-250+f2*14],[-96,-238+f2*10],[-60,-244+f*6],[-28,-246]],'#a8503a');
  poly(g,jag([[-24,-300],[26,-300],[30,-262],[-22,-260]],rng(9),3,2),'#9c7660');poly(g,[[6,-286],[30,-284],[30,-262],[0,-260]],'#36291f');
  poly(g,jag([[-38,-300],[-34,-335],[0,-346],[30,-336],[38,-300],[30,-288],[-30,-286]],rng(7),4,3),'#5c4838');
  poly(g,jag([[-40,-300],[40,-300],[38,-288],[-44,-284]],rng(8),3,3),'#8c7558');poly(g,jag([[-40,-300],[-30,-262],[-44,-258],[-50,-292]],rng(4),3,2),'#6e5a46');
  g.fillStyle='rgba(225,236,240,.85)';g.fillRect(-30,-346,40,6);g.fillRect(-40,-256,18,4);
  g.restore();
}
function streaks(g,t,amt=1,ang=.35){g.strokeStyle='rgba(225,236,240,.55)';g.lineWidth=2;
  for(const p of SNOW){const sp=500+p.z*700;const x=((p.x+t*sp)%(W*1.4))-W*.2,y=((p.y+t*sp*ang)%H);g.globalAlpha=Math.min(1,.2+p.z*.4)*amt;g.beginPath();g.moveTo(x,y);g.lineTo(x-30-p.z*30,y-(30+p.z*30)*ang);g.stroke()}g.globalAlpha=1}
function stormBg(g,t,fogA=.35){
  const sg=g.createLinearGradient(0,0,0,H);sg.addColorStop(0,'#0b161c');sg.addColorStop(.6,'#1d3640');sg.addColorStop(1,'#2a4752');g.fillStyle=sg;g.fillRect(0,0,W,H);
  g.globalAlpha=.5;g.drawImage(L1,0,120);g.globalAlpha=1;g.fillStyle=`rgba(120,150,160,${fogA})`;g.fillRect(0,0,W,H);
}

// door + first steps into the storm
function exitScene(g,t,t0){
  stormBg(g,t,.25);
  poly(g,[[0,1350],[W,1330],[W,H],[0,H]],'#2f4d57');poly(g,[[0,1350],[W,1330],[W,1352],[0,1372]],'#6a8a93');
  poly(g,[[-40,420],[360,440],[360,1360],[-40,1360]],'#1a2a30');for(let y=470;y<1350;y+=46){g.fillStyle='rgba(0,0,0,.25)';g.fillRect(-40,y,400,4)}
  const op=easeOut((t-t0-.2)/.6);poly(g,[[170,780],[330,780],[330,1352],[170,1352]],'#2a1a10');
  g.globalCompositeOperation='lighter';poly(g,[[170+160*(1-op),780],[330,780],[330,1352],[170+160*(1-op),1352]],'rgba(255,170,80,.75)');
  poly(g,[[330,1352],[330,780],[330+420*op,1500],[330+260*op,1700]],'rgba(255,170,80,.18)');glow(g,300,1100,500,'rgba(255,170,80,A)',.25*op);g.globalCompositeOperation='source-over';
  poly(g,[[170,780],[170+160*(1-op)*0+20,760],[170+40,1360],[170,1352]],'#120c08');
  const wx=lerp(260,560,ease((t-t0-.6)/2.6));figure(g,wx,1395,1.25,(t-t0)*6,{t});
  streaks(g,t,1);drawSnow(g,t,1,2);
  // 6-hour dial
  const cx=540,cy=430,r=118,a=clamp((t-t0)/2.8,0,1);g.save();g.globalAlpha=clamp((t-t0)/.3,0,1);
  g.fillStyle='rgba(6,14,20,.8)';g.beginPath();g.arc(cx,cy,r+16,0,7);g.fill();g.strokeStyle='#6fc3ff';g.lineWidth=3;g.beginPath();g.arc(cx,cy,r+16,0,7);g.stroke();
  g.font='700 26px '+MONO;g.textAlign='center';g.textBaseline='middle';
  ['00','06','12','18'].forEach((l,i)=>{const an=i*Math.PI/2-Math.PI/2,lit=a*4>i;g.fillStyle=lit?'#f5b83d':'#4e6f80';g.beginPath();g.arc(cx+Math.cos(an)*r*.78,cy+Math.sin(an)*r*.78,12,0,7);g.fill();g.fillText(l,cx+Math.cos(an)*r*.42,cy+Math.sin(an)*r*.42)});
  const ha=a*Math.PI*2-Math.PI/2;g.strokeStyle='#d6efff';g.lineWidth=5;g.beginPath();g.moveTo(cx,cy);g.lineTo(cx+Math.cos(ha)*r*.7,cy+Math.sin(ha)*r*.7);g.stroke();
  g.fillStyle='#9fd4f5';g.font='700 24px '+MONO;g.fillText('КАЖДЫЕ 6 Ч',cx,cy+r+48);g.restore();
}
// side view: rope with three poles, ruler 40 m
function ropeScene(g,t,t0,ruler0){
  stormBg(g,t,.3);
  const gy=1350;poly(g,jag([[0,gy],[W,gy-10],[W,H],[0,H]],rng(2),5,8),'#2c4954');poly(g,jag([[0,gy],[W,gy-10],[W,gy+16],[0,gy+22]],rng(3),3,8),'#6a8a93');
  poly(g,[[-60,760],[130,760],[130,gy+4],[-60,gy+4]],'#1a2a30');poly(g,[[60,1000],[120,1000],[120,gy],[60,gy]],'#2a1a10');g.fillStyle='#ffb447';g.fillRect(-20,880,50,40);
  g.globalCompositeOperation='lighter';glow(g,10,900,220,'rgba(255,170,80,A)',.35);g.globalCompositeOperation='source-over';
  poly(g,[[925,1170],[1010,1170],[1010,1250],[925,1250]],'#a9bcc1');poly(g,[[915,1160],[1020,1160],[1010,1146],[925,1146]],'#d2dde0');g.fillStyle='#0e1a1f';g.fillRect(935,1250,8,100);g.fillRect(992,1250,8,100);
  const poles=[340,560,780];g.fillStyle='#0e1a1f';for(const x of poles)g.fillRect(x-4,1160,8,gy-1160);
  const pts=[[125,1150],...poles.map(x=>[x,1166]),[925,1180]];g.strokeStyle='#8c7a5a';g.lineWidth=5;g.beginPath();g.moveTo(...pts[0]);
  for(let i=1;i<pts.length;i++){const a=pts[i-1],b=pts[i];g.quadraticCurveTo((a[0]+b[0])/2,Math.max(a[1],b[1])+26,b[0],b[1])}g.stroke();
  g.fillStyle='#5a4a33';g.beginPath();g.arc(780,1166,9,0,7);g.fill(); // the knot at the third pole
  const wx=lerp(170,640,clamp((t-t0)/4.8,0,1));figure(g,wx,gy+6,1.0,(t-t0)*5,{t,reach:-.62});
  // ruler
  const p=easeOut((t-ruler0)/1.2);if(t>ruler0){g.save();const x0=125,x1=925,xr=lerp(x0,x1,p),y=1060;g.strokeStyle='#f5b83d';g.lineWidth=4;g.beginPath();g.moveTo(x0,y);g.lineTo(xr,y);g.stroke();
    g.font='700 26px '+MONO;g.textAlign='center';g.fillStyle='#f5b83d';for(let m=0;m<=40;m+=10){const x=lerp(x0,x1,m/40);if(x>xr+1)break;g.fillRect(x-2,y-14,4,28);g.fillText(m+(m===40?' М':''),x,y-28)}g.restore()}
  streaks(g,t,1.3,.25);drawSnow(g,t,1,2.5);
}
// mitten lets go of the rope
function mittenScene(g,t,t0,rel){
  stormBg(g,t,.4);streaks(g,t,.8,.2);
  const ry=980;g.strokeStyle='#8c7a5a';g.lineWidth=34;g.beginPath();g.moveTo(-50,ry+30);g.quadraticCurveTo(540,ry+70,W+50,ry+10);g.stroke();
  g.strokeStyle='rgba(40,30,20,.6)';g.lineWidth=6;for(let x=-40;x<W+40;x+=34){const y=ry+30+Math.sin(x/W*Math.PI)*36;g.beginPath();g.moveTo(x,y-14);g.lineTo(x+18,y+14);g.stroke()}
  const r=easeOut((t-rel)/.45);g.save();g.translate(520+r*-60,ry+40-r*260);g.rotate(-r*.6);
  poly(g,jag([[-150,40],[-120,-90],[60,-110],[140,-40],[150,60],[40,120],[-110,110]],rng(31),6,4),'#5a4332');
  poly(g,jag([[-150,40],[-120,-90],[0,-104],[-20,110],[-110,110]],rng(32),6,3),'#6e5440');
  poly(g,jag([[-130,-20],[-260,-60],[-280,40],[-150,80]],rng(33),6,3),'#34423a');
  const th=lerp(0,70,r);poly(g,jag([[60,60],[150,60+th*.2],[170,120+th],[90,140+th]],rng(34),5,3),'#4e3a2b');
  g.fillStyle='rgba(225,236,240,.8)';for(let i=0;i<30;i++)g.fillRect(-140+(i*37%280),-90+(i*53%180),4,4);g.restore();
  drawSnow(g,t,1.2,3);
}
// white-out: five steps and the door is gone
function whiteout(g,t,t0,t1){
  const k=clamp((t-t0)/(t1-t0),0,1);stormBg(g,t,.35+k*.3);
  const gy=1380;poly(g,[[0,gy],[W,gy],[W,H],[0,H]],'#4a6a74');
  const lightA=Math.max(0,1-k*1.4);g.globalCompositeOperation='lighter';glow(g,90,1250,180,'rgba(255,170,80,A)',.5*lightA);g.globalCompositeOperation='source-over';g.fillStyle=`rgba(255,180,90,${lightA})`;g.fillRect(78,1238,26,20);
  const steps=[0,1,2,3,4].map(i=>lerp(t0+.15,t1-.2,i/4));const n=steps.filter(s=>t>=s).length,fx=380+n*70;
  for(let i=0;i<n;i++){g.fillStyle='rgba(20,35,42,.55)';g.beginPath();g.ellipse(360+i*70,gy+40+(i%2)*26,24,10,0,0,7);g.fill();
    g.save();g.globalAlpha=clamp((t-steps[i])/.15,0,1);g.font='900 70px Mont';g.textAlign='center';g.fillStyle='#f5b83d';g.shadowColor='rgba(0,0,0,.6)';g.shadowBlur=14;g.fillText(String(i+1),360+i*70,gy-260);g.restore()}
  figure(g,fx,gy+10,1.15,n*Math.PI/2+(t-t0)*2,{t,reach:.6});
  g.fillStyle=`rgba(215,226,230,${.15+k*.62})`;g.fillRect(0,0,W,H);
  streaks(g,t,1.6,.15);drawSnow(g,t,1.4,3);
  if(t>t1-1.0){g.save();g.globalAlpha=clamp((t-(t1-1.0))/.3,0,1);tag(g,300,520,'ВИДИМОСТЬ: 2 М','#ff3b2f');g.restore()}
}
// diesel barrels + gauge
const SHED=mk();{const g=SHED.getContext('2d'),R=rng(23);g.fillStyle='#10181c';g.fillRect(0,0,W,H);
  for(let x=-20;x<W;x+=100)poly(g,jag([[x,0],[x+96,0],[x+96,1300],[x,1300]],R,3,8),R()<.5?'#131d22':'#0f171b');
  poly(g,[[0,1300],[W,1290],[W,H],[0,H]],'#1d1a17');
  poly(g,[[60,980],[420,980],[420,1310],[60,1310]],'#2c3a36');poly(g,[[60,980],[420,980],[410,1000],[70,1000]],'#4a5c56');g.fillStyle='#121918';g.beginPath();g.arc(170,1150,90,0,7);g.fill();g.fillStyle='#3d4a46';g.beginPath();g.arc(170,1150,30,0,7);g.fill();
  g.fillStyle='#0c1112';g.fillRect(360,700,22,280);g.fillStyle='#c9bfa5';g.font='700 26px '+MONO;g.fillText('ДГ-30',280,1060);
  for(let i=0;i<4;i++){const x=470+i*150,col=i%2?'#5e3b2a':'#2f4650';poly(g,[[x,1020],[x+130,1020],[x+130,1310],[x,1310]],col);poly(g,[[x,1020],[x+40,1020],[x+40,1310],[x,1310]],'rgba(255,255,255,.08)');
    g.fillStyle='rgba(0,0,0,.35)';for(const y of [1080,1170,1260])g.fillRect(x,y,130,8);poly(g,[[x,1012],[x+130,1012],[x+130,1024],[x,1024]],'#a9bcc1');g.fillStyle='#e7ddc4';g.font='700 30px '+MONO;g.fillText('ДТ',x+44,1150)}}
function fuelScene(g,t,t0,f0,f1,noGauge){
  g.drawImage(SHED,0,0);const fl=.85+.15*Math.sin(t*9);g.fillStyle='#ffd27a';g.fillRect(536,300,10,30);
  g.globalCompositeOperation='lighter';glow(g,540,330,800,'rgba(232,150,60,A)',.3*fl);g.globalCompositeOperation='source-over';g.strokeStyle='#0b0f10';g.lineWidth=3;g.beginPath();g.moveTo(540,0);g.lineTo(540,300);g.stroke();
  if(noGauge)return;const n=Math.round(30*easeOut((t-f0)/(f1-f0)));g.save();const x0=110,y0=470,w=860;
  g.fillStyle='rgba(6,14,20,.8)';g.fillRect(x0-20,y0-80,w+40,200);g.strokeStyle='#e8a24a';g.lineWidth=2;g.strokeRect(x0-20,y0-80,w+40,200);
  g.fillStyle='#e8a24a';g.font='700 30px '+MONO;g.fillText('СОЛЯРКА',x0,y0-30);g.font='800 54px '+MONO;g.textAlign='right';g.fillStyle='#f5b83d';g.fillText(n+' ДН.',x0+w,y0-24);g.textAlign='left';
  for(let i=0;i<30;i++){g.fillStyle=i<n?'#e8a24a':'rgba(232,162,74,.15)';g.fillRect(x0+i*(w/30),y0+10,w/30-6,70)}g.restore();
}
// Mi-8 at dawn
function heliScene(g,t,t0,t1){
  const sg=g.createLinearGradient(0,0,0,HZ+60);sg.addColorStop(0,'#0c1d29');sg.addColorStop(.5,'#2a4d58');sg.addColorStop(.85,'#b98352');sg.addColorStop(1,'#e2a76a');g.fillStyle=sg;g.fillRect(0,0,W,H);
  g.globalCompositeOperation='lighter';glow(g,760,HZ,500,'rgba(255,190,120,A)',.45);g.globalCompositeOperation='source-over';
  g.drawImage(L1,0,0);g.drawImage(L2,0,0);g.fillStyle='rgba(30,20,30,.25)';g.fillRect(0,0,W,HZ+120);
  poly(g,[[0,HZ+70],[W,HZ+64],[W,H],[0,H]],'#2b4049');poly(g,[[0,HZ+70],[W,HZ+64],[W,HZ+90],[0,HZ+96]],'#c9a27c');
  const p=(t-t0)/(t1-t0),hx=lerp(-260,1300,p),hy=640+Math.sin(t*2)*10;
  g.setLineDash([10,14]);g.strokeStyle='rgba(230,240,240,.5)';g.lineWidth=3;g.beginPath();g.moveTo(-100,700);g.quadraticCurveTo(540,560,1200,640);g.stroke();g.setLineDash([]);
  g.save();g.translate(hx,hy);g.rotate(-.06);const c='#0b1418';
  poly(g,[[-150,-20],[-40,-46],[60,-46],[110,-30],[130,0],[110,26],[-110,28],[-170,8]],c);poly(g,[[-160,-6],[-330,-14],[-336,6],[-160,10]],c);
  poly(g,[[-320,-14],[-350,-60],[-332,-60],[-308,-14]],c);poly(g,[[60,-40],[100,-28],[104,-6],[60,-10]],'#3b5560');
  poly(g,[[-60,-46],[30,-46],[20,-66],[-50,-66]],c);g.fillRect(-12,-80,8,16);
  const rot=(t*40)%2<1;g.fillRect(-260,rot?-84:-82,520,rot?4:3);g.globalAlpha=.25;g.fillRect(-270,-86,540,8);g.globalAlpha=1;
  g.beginPath();g.arc(-340,-14,26,0,7);g.globalAlpha=.3;g.fill();g.globalAlpha=1;g.fillRect(-60,26,8,22);g.fillRect(60,26,8,22);g.fillRect(-90,46,180,5);g.restore();
  if(p>.15){g.save();g.globalAlpha=clamp((p-.15)/.1,0,1);g.strokeStyle='#cfe3e8';g.lineWidth=2;g.beginPath();g.moveTo(hx+40,hy+40);g.lineTo(hx+90,hy+160);g.stroke();tag(g,hx+90,hy+180,'Ми-8 · ДЕНЬ 77','#cfe3e8');g.restore()}
  drawSnow(g,t,.7,1);
}
function noErrorScene(g,t,t0,hit){
  fuelScene(g,t,-99,-99,-98,true);dark(g,.6);
  const red=t>hit,sh=shakeAt(t,[hit],16,.35);g.save();g.translate(Math.sin(t*90)*sh,0);
  const bar=(y,lab,col,val)=>{g.fillStyle='rgba(6,14,20,.85)';g.fillRect(90,y-70,900,170);g.strokeStyle=red?'#ff3b2f':col;g.lineWidth=3;g.strokeRect(90,y-70,900,170);
    g.font='700 30px '+MONO;g.fillStyle=red?'#ff3b2f':col;g.fillText(lab,120,y-22);g.font='800 54px '+MONO;g.textAlign='right';g.fillText(val,960,y-16);g.textAlign='left';
    for(let i=0;i<30;i++){g.fillStyle=red?'#ff3b2f':col;g.globalAlpha=.9;g.fillRect(120+i*28.4,y+20,22,56)}g.globalAlpha=1};
  bar(560,'СОЛЯРКА','#e8a24a','30 ДН.');bar(900,'ВЕРТОЛЁТ ЧЕРЕЗ','#9fd4f5','30 ДН.');
  g.font='900 120px Mont';g.textAlign='center';g.fillStyle=red?'#ff3b2f':'#e7ddc4';g.fillText('=',540,760);
  if(red){g.globalAlpha=clamp((t-hit)/.2,0,1);tag(g,300,1120,'ЗАПАС: 0 ДН.','#ff3b2f')}g.restore();
  if(t>hit&&t<hit+.25){g.fillStyle=`rgba(255,40,30,${.35*(1-(t-hit)/.25)})`;g.fillRect(0,0,W,H)}
}
// empty-air / clean-signal scope over the dimmed radio
function scope(g,t,mode,y=360){
  g.save();g.fillStyle='rgba(6,14,20,.85)';g.fillRect(90,y-110,900,230);g.strokeStyle='#9fd4f5';g.lineWidth=2;g.strokeRect(90,y-110,900,230);
  g.strokeStyle='rgba(159,212,245,.15)';for(let x=130;x<990;x+=60){g.beginPath();g.moveTo(x,y-100);g.lineTo(x,y+110);g.stroke()}
  g.strokeStyle=mode==='beep'?'#f5b83d':'#9fd4f5';g.lineWidth=4;g.beginPath();
  for(let x=100;x<=980;x+=4){let v=0;if(mode==='noise')v=(Math.sin(x*.9+t*40)*Math.sin(x*.13+t*7))*3;
    if(mode==='beep'){const k=(x-100)/880;for(const c of [.25,.5,.75])if(Math.abs(k-c)<.06)v=Math.sin(x*1.1)*70}
    x===100?g.moveTo(x,y+v):g.lineTo(x,y+v)}g.stroke();g.restore();
}
function doorScene(g,t,t0){
  g.drawImage(PBG,0,0);const z=lerp(1,1.18,(t-t0)/3);g.save();g.translate(640,900);g.scale(z,z);g.translate(-640,-900);
  poly(g,[[380,420],[760,420],[760,1500],[380,1500]],'#0a0f12');poly(g,[[400,440],[740,440],[740,1500],[400,1500]],'#1f1813');
  for(let y=520;y<1480;y+=120)g.fillStyle='rgba(0,0,0,.3)',g.fillRect(410,y,320,6);
  poly(g,[[728,440],[742,440],[742,1500],[728,1500]],'#000');g.fillStyle='rgba(120,170,190,.35)';g.fillRect(736,440,3,1060);
  g.fillStyle='#8a7a5a';g.beginPath();g.arc(700,960,14,0,7);g.fill();g.restore();
  poly(g,[[0,1500],[W,1500],[W,H],[0,H]],'#1d1712');
  const fl=.7+.3*Math.sin(t*17)*Math.sin(t*5);g.globalCompositeOperation='lighter';glow(g,80,800,1000,'rgba(232,150,60,A)',.25*fl);g.globalCompositeOperation='source-over';
}
function timerScene(g,t,t0,c0,c1){
  radio(g,t,{K:[[0,540,820,1.15],[1,540,820,1.15]],on:true,t0:0,t1:0});dark(g,.55);
  const k=clamp((t-c0)/(c1-c0),0,1),sec=Math.round(2400*(1-easeInOut(k)));const mm=String(Math.floor(sec/60)).padStart(2,'0'),ss=String(sec%60).padStart(2,'0');
  g.save();g.textAlign='center';g.textBaseline='middle';g.lineWidth=14;g.strokeStyle='rgba(255,255,255,.12)';g.beginPath();g.arc(540,820,300,0,7);g.stroke();
  g.strokeStyle=sec<300?'#ff3b2f':'#f5b83d';g.beginPath();g.arc(540,820,300,-Math.PI/2,-Math.PI/2+Math.PI*2*(1-k));g.stroke();
  g.font='800 170px '+MONO;g.fillStyle=sec<300?'#ff3b2f':'#ffffff';g.fillText(mm+':'+ss,540,820);g.font='700 30px '+MONO;g.fillStyle='#e7ddc4';g.fillText('ДО ПОВТОРА',540,1000);g.restore();
}
function clockScene(g,t,t0){g.drawImage(TABLE,0,0);g.globalCompositeOperation='lighter';glow(g,150,500,1000,'rgba(232,150,60,A)',.32);g.globalCompositeOperation='source-over';
  const z=lerp(1,1.1,(t-t0)/3.8),min=3*60+lerp(28.6,30,clamp((t-t0)/(ps('06.1')-t0+.05),0,1))+Math.max(0,t-ps('06.1'))/60;
  g.save();g.translate(540,860);g.scale(z,z);clockObj(g,0,0,330,min);g.restore()}
function timesScene(g,t){g.fillStyle='#0a1014';g.fillRect(0,0,W,H);
  const T=[['02:10','07.0'],['02:50','07.1'],['03:30','07.2']];g.save();g.textAlign='center';g.textBaseline='middle';
  T.forEach(([s,id],i)=>{const a=t-ps(id);if(a<0)return;const sc=lerp(1.5,1,easeOut(a/.25));g.save();g.translate(540,520+i*300);g.scale(sc,sc);g.globalAlpha=clamp(a/.12,0,1);
    g.font='800 190px '+MONO;g.fillStyle='#f5b83d';g.shadowColor='rgba(245,184,61,.35)';g.shadowBlur=40;g.fillText(s,0,0);g.restore();
    if(i>0){g.globalAlpha=clamp(a/.3,0,1);g.setLineDash([8,10]);g.strokeStyle='#ff3b2f';g.lineWidth=3;g.beginPath();g.moveTo(820,520+(i-1)*300+60);g.lineTo(820,520+i*300-60);g.stroke();g.setLineDash([]);
      g.font='700 30px '+MONO;g.fillStyle='#ff3b2f';g.fillText('+40',900,520+i*300-150);g.globalAlpha=1}});g.restore()}
const SHELF=mk();{const g=SHELF.getContext('2d'),R=rng(29);g.drawImage(PBG,0,0);
  poly(g,[[0,1040],[W,1030],[W,1080],[0,1092]],'#2a1f17');poly(g,[[0,1030],[W,1020],[W,1040],[0,1050]],'#3b2c21');
  let x=40;const cols=['#3a2f28','#2c3a3a','#4a2a22','#26303a','#3d3528','#33282a'];
  while(x<W-40){const w=40+R()*50,h=260+R()*140;if(Math.abs(x-470)<60){x+=150;continue}poly(g,jag([[x,1032-h],[x+w,1032-h],[x+w,1032],[x,1032]],R,2,3),cols[Math.floor(R()*6)]);g.fillStyle='rgba(200,180,140,.25)';g.fillRect(x+6,1032-h+30,w-12,6);x+=w+4}
  g.fillStyle='rgba(225,236,240,.6)';for(let i=0;i<60;i++)g.fillRect(R()*W,1024+R()*8,4,3)}
function shelfScene(g,t,t0,hl){
  const z=lerp(1,1.9,easeInOut((t-t0)/3.8));g.save();g.translate(540,860);g.scale(z,z);g.translate(-540,-860);g.drawImage(SHELF,0,0);
  poly(g,[[470,700],[600,700],[600,1032],[470,1032]],'#4a3a2a');poly(g,[[470,700],[492,700],[492,1032],[470,1032]],'#5c4836');
  g.fillStyle='#b5452f';g.fillRect(470,740,130,10);g.fillRect(470,990,130,10);
  g.save();g.translate(548,866);g.rotate(-Math.PI/2);g.textAlign='center';g.fillStyle='#e7ddc4';g.font='700 40px Hand';g.fillText('Журнал наблюдений',0,-8);g.font='700 30px Hand';g.fillStyle='#d9c79f';g.fillText('прошлая зима',0,30);g.restore();
  g.restore();
  const fl=.85+.15*Math.sin(t*11);g.globalCompositeOperation='lighter';glow(g,140,700,900,'rgba(232,150,60,A)',.3*fl);if(t>hl)glow(g,540,860,380,'rgba(255,190,100,A)',.25*easeOut((t-hl)/.5));g.globalCompositeOperation='source-over';
}
// the old log page (taller than the screen, camera pans)
const JH=2700,JP=mk(W,JH);{const g=JP.getContext('2d'),R=rng(37);
  const pg=g.createLinearGradient(0,0,W,JH);pg.addColorStop(0,'#d6cab0');pg.addColorStop(1,'#a99d82');g.fillStyle=pg;g.fillRect(0,0,W,JH);
  for(let i=0;i<2500;i++){g.fillStyle=R()<.5?'rgba(255,255,255,.05)':'rgba(80,60,40,.05)';g.fillRect(R()*W,R()*JH,20+R()*60,2+R()*4)}
  g.strokeStyle='rgba(80,60,40,.35)';g.lineWidth=2;for(let y=380;y<JH-100;y+=90){g.beginPath();g.moveTo(60,y);g.lineTo(W-60,y);g.stroke()}
  g.beginPath();g.moveTo(250,250);g.lineTo(250,JH-120);g.moveTo(470,250);g.lineTo(470,JH-120);g.stroke();
  g.fillStyle='#3d332a';g.font='700 30px '+MONO;g.fillText('ДАТА',90,330);g.fillText('ВРЕМЯ',290,330);g.fillText('НАБЛЮДЕНИЕ',510,330);
  g.font='700 34px '+MONO;g.fillText('ЖУРНАЛ НАБЛЮДЕНИЙ · СТ. «СЕВЕРНАЯ»',90,170);
  const hand=(txt,x,y,sz=64,col='#2a2a3a')=>{g.save();g.translate(x,y);g.transform(1,0,-.28,1,0,0);g.font=`700 ${sz}px Hand`;g.fillStyle=col;g.fillText(txt,0,0);g.restore()};
  const rows=[['ночь 47','02:10','• • •  три коротких'],['','02:50','• • •  опять'],['','03:30','• • •  приёмник выкл.'],['','04:10','• • •'],['','04:50','• • •']];
  rows.forEach((r,i)=>{const y=455+i*90;hand(r[0],90,y,52);hand(r[1],290,y);hand(r[2],520,y)});
  hand('Не спал. Слушал.',520,455+6*90,56,'#3a3a48');hand('Они не прекратятся.',520,455+8*90,56,'#3a3a48');
  // the last line, pressed hard
  const ly=2330;g.save();g.translate(120,ly);g.transform(1,0,-.3,1,0,0);g.font='700 136px Hand';g.fillStyle='rgba(255,255,255,.35)';g.fillText('Не отвечай',4,4);g.fillStyle='#14141c';g.fillText('Не отвечай',0,0);g.restore();
  poly(g,jag([[860,ly-40],[905,ly-60],[925,ly-10],[880,ly+12]],R,6,3),'#1a120c');poly(g,jag([[300,ly+30],[330,ly+22],[336,ly+44],[305,ly+50]],R,4,2),'#1a120c');
}
function journalScene(g,t,o){
  const [cy,z]=keys(t,o.K);const s=z,ox=clamp(540-540*s,W-W*s,0),oy=clamp(860-cy*s,H-JH*s,0);
  g.fillStyle='#000';g.fillRect(0,0,W,H);g.save();g.setTransform(s,0,0,s,ox,oy);g.drawImage(JP,0,0);
  // red circles drawn by hand on the times
  [[0,o.c[0]],[1,o.c[1]],[2,o.c[2]]].forEach(([i,ct])=>{if(t<ct)return;const p=easeOut((t-ct)/.45);g.strokeStyle='#c0261b';g.lineWidth=6;g.beginPath();g.ellipse(360,435+i*90,105,48,-.05,-1.4,-1.4+Math.PI*2.1*p);g.stroke()});
  if(t>o.u){const p=easeOut((t-o.u)/.5);g.strokeStyle='#c0261b';g.lineWidth=9;g.beginPath();g.moveTo(130,2365);g.lineTo(130+760*p,2352);g.stroke()}
  g.restore();
  const fl=.85+.15*Math.sin(t*11);g.globalCompositeOperation='lighter';glow(g,100,300,1100,'rgba(232,150,60,A)',.18*fl);g.globalCompositeOperation='source-over';
  const v=g.createLinearGradient(0,0,0,H);v.addColorStop(0,'rgba(0,0,0,.35)');v.addColorStop(.5,'rgba(0,0,0,0)');v.addColorStop(.75,'rgba(0,0,0,.35)');v.addColorStop(1,'rgba(0,0,0,.85)');g.fillStyle=v;g.fillRect(0,0,W,H);
  if(o.tag&&t>o.tag[0]){g.globalAlpha=clamp((t-o.tag[0])/.3,0,1);tag(g,560,300,o.tag[1],'#ff3b2f');g.globalAlpha=1}
}
function endCard(g,t,t0){g.fillStyle='#000';g.fillRect(0,0,W,H);const a=t-t0;g.save();g.textAlign='center';g.textBaseline='middle';
  g.globalAlpha=clamp(a/.6,0,1);g.font='700 34px '+MONO;g.fillStyle='#8a9aa2';g.fillText('М Е Т Е О С Т А Н Ц И Я',540,700);
  g.globalAlpha=clamp((a-.5)/.5,0,1);g.font='700 120px Hand';g.fillStyle='#c0261b';g.fillText('часть 2',540,850);g.font='900 92px Mont';g.fillStyle='#e7ddc4';g.fillText('ЖУРНАЛ',540,980);
  g.globalAlpha=clamp((a-1.4)/.5,0,1);g.font='900 44px Mont';g.fillStyle='#ffffff';g.fillText('ПРОДОЛЖЕНИЕ СЛЕДУЕТ…',540,1240);
  for(let i=0;i<3;i++){const on=a>2.2+i*.27;g.fillStyle=on?'#ff3b2f':'rgba(255,255,255,.15)';g.beginPath();g.arc(480+i*60,1400,12,0,7);g.fill()}g.restore()}

// ---------------- sticker (changes text) & HUD ----------------
function sticker2(t,t0,title,sub){if(t<t0)return;const a=t-t0,y=lerp(-260,0,easeOutBack(a/.45)),rot=(-4+7*Math.exp(-a*5)*Math.sin(a*18))*Math.PI/180;
  const R=rng(5);ctx.save();ctx.translate(205,165+y);ctx.rotate(rot);ctx.shadowColor='rgba(0,0,0,.55)';ctx.shadowBlur=24;ctx.shadowOffsetY=10;
  poly(ctx,jag([[-150,-70],[150,-70],[150,70],[-150,70]],R,2,4),'#e7ddc4');ctx.shadowColor='transparent';
  ctx.save();ctx.rotate(.06);ctx.fillStyle='rgba(200,190,160,.85)';ctx.fillRect(-55,-86,110,30);ctx.restore();
  ctx.textAlign='center';ctx.fillStyle='#2a2420';ctx.font='700 70px Hand';ctx.fillText(title,0,8);ctx.fillStyle='#6a5d50';ctx.font='700 30px Hand';ctx.fillText(sub,0,50);ctx.restore()}
const STK=[[9.0,'День 47','ст. «Северная» · −38°'],[43.5,'Ночь 47','02:10'],[64.85,'Ночь 47','02:50'],[81.33,'Ночь 47','03:30'],[99.9,'Прошлая зима','ночь 47 · 02:10']];
function nameplate(t,t0){if(t<t0)return;const p=easeOut((t-t0)/.35);ctx.save();ctx.globalAlpha=p;const x=lerp(-500,90,p);
  ctx.fillStyle='rgba(6,14,20,.85)';ctx.fillRect(x,1340,620,120);ctx.fillStyle='#e8a24a';ctx.fillRect(x,1340,10,120);
  ctx.font='900 56px Mont';ctx.fillStyle='#fff';ctx.fillText('АНДРЕЙ',x+36,1400);ctx.font='700 24px '+MONO;ctx.fillStyle='#e8a24a';ctx.fillText('РАДИСТ-МЕТЕОРОЛОГ · 41 ГОД',x+36,1440);ctx.restore()}
function powerTag(T,t,t0,t1){if(t<t0||t>t1||!T)return;if(Math.floor(t*4)%2&&t>t0+.3)return;const q=T.transformPoint(new DOMPoint(370,1560));
  ctx.save();ctx.strokeStyle='#ff3b2f';ctx.lineWidth=3;ctx.beginPath();ctx.arc(q.x,q.y,70,0,7);ctx.stroke();ctx.beginPath();ctx.moveTo(q.x+50,q.y-50);ctx.lineTo(q.x+150,q.y-150);ctx.stroke();tag(ctx,q.x+150,q.y-150,'⏻ ПИТАНИЕ: ВЫКЛ','#ff3b2f');ctx.restore()}

// ---------------- captions from the voice timeline ----------------
const RED=new Set('ВЫКЛЮЧЕН ВЫДЕРНУТ СИГНАЛ ГУДКА ГУДКОВ ВЫКЛЮЧЕННОГО ДИНАМИКА ОШИБКУ НЕТ ОТВЕЧАЙ ОТВЕТИЛ СБОЙ ВЫДЕРНУЛ ЧУЖИМ ПОЧЕРКОМ НАЙТИ'.split(' '));
const YEL=new Set('АНДРЕЙ СЕВЕРНАЯ ТРИСТА КИЛОМЕТРОВ ДВАЖДЫ СОРОК СЕМЬ ДНЕЙ ШЕСТЬ ЧАСОВ МЕТРОВ ТРИДЦАТЬ ПЯТЬ ДВА ДЕСЯТЬ ПЯТЬДЕСЯТ ТРИ ВЕРТОЛЁТ СОЛЯРКИ ГОД ЖУРНАЛ ВЕРЁВКЕ'.split(' '));
const BLU=new Set('ТИШИНА ПУСТО ПОМЕХ ПОЗЫВНОГО'.split(' '));
const GROUPS=[];{const ids=Object.keys(PH);ids.forEach((id,pi)=>{const p=PH[id],nx=ids[pi+1]?PH[ids[pi+1]].s:p.e+2;let cur=[],len=0;
  const flush=end=>{if(cur.length)GROUPS.push({s:cur[0][1]-.04,e:end,w:cur});cur=[];len=0};
  p.w.forEach(([w,tt],k)=>{if(w==='—'&&cur.length){cur[cur.length-1]=[cur[cur.length-1][0]+' —',cur[cur.length-1][1]];return}if(cur.length&&(cur.length>=3||len+w.length>17)){flush(tt-.04)}cur.push([w,tt]);len+=w.length});
  flush(Math.min(nx-.04,p.e+.7))})}
function capColor(w){const k=w.toUpperCase().replace(/[«»—.,:?…!]/g,'');return RED.has(k)?'#ff3b2f':YEL.has(k)?'#f5b83d':BLU.has(k)?'#9fd4f5':'#ffffff'}
function captions3(t,cy){const c=GROUPS.find(c=>t>=c.s&&t<c.e);if(!c)return;
  ctx.save();ctx.font='900 76px Mont';ctx.textBaseline='middle';ctx.textAlign='center';ctx.lineJoin='round';
  const sp=28,lines=[[]],lw=[0];
  for(const [w0,tt] of c.w){const w=w0.toUpperCase(),m=ctx.measureText(w).width;let L=lines.length-1;if(lw[L]>0&&lw[L]+sp+m>940){lines.push([]);lw.push(0);L++}lines[L].push({s:w,t:tt,m,col:capColor(w0)});lw[L]+=(lw[L]>0?sp:0)+m}
  const lh=90,y0=cy-(lines.length-1)*lh/2;ctx.globalAlpha=clamp((t-c.s)/.08,0,1);
  lines.forEach((ln,i)=>{let x=540-lw[i]/2;for(const w of ln){const on=t>=w.t-.02,age=t-w.t,sc=on?1+.07*Math.max(0,1-age/.15):1;
    ctx.save();ctx.translate(x+w.m/2,y0+i*lh);ctx.scale(sc,sc);ctx.shadowColor='rgba(0,0,0,.9)';ctx.shadowBlur=22;ctx.shadowOffsetY=5;ctx.lineWidth=12;ctx.strokeStyle='rgba(0,0,0,.6)';ctx.strokeText(w.s,0,0);
    ctx.shadowColor='transparent';ctx.fillStyle=on?w.col:'rgba(150,162,170,.55)';ctx.fillText(w.s,0,0);ctx.restore();x+=w.m+sp}});ctx.restore()}

// ---------------- the shot list ----------------
const PP=(id)=>ps(id);
const SHOTS=[
 {s:0,e:1.0,cap:1520,f:(g,t)=>{g.fillStyle='#000';g.fillRect(0,0,W,H);let n=0;for(let i=0;i<3;i++)if(t>=BEEPS[i])n++;
   for(let i=0;i<n;i++){const on=t<BEEPS[i]+.13;g.globalCompositeOperation='lighter';if(on)glow(g,420+i*120,900,90,'rgba(255,220,160,A)',.5);g.globalCompositeOperation='source-over';g.fillStyle=on?'#fff6e0':'#8d8577';g.beginPath();g.arc(420+i*120,900,18,0,7);g.fill()}}},
 {s:1.0,e:7.45,cap:1520,f:(g,t)=>{const r=radio(g,t,{on:false,t0:1,t1:8,K:[[1.0,540,820,1.32],[2.9,540,830,1.40],[3.25,370,1360,1.55],[4.5,370,1380,1.62],[4.9,560,900,1.12],[7.45,560,880,1.2]]});SHOT_T=r.T},
   hud:t=>powerTag(SHOT_T,t,3.3,4.6)},
 {s:7.45,e:8.85,cap:1600,f:(g,t)=>portrait(g,t,{K:[[7.45,540,900,1.12],[8.85,540,860,1.2]],look:-.2}),hud:t=>nameplate(t,7.7)},
 {s:8.85,e:10.75,cap:1290,out:1,f:(g,t)=>scene2(g,t,lerp(1.0,1.08,(t-8.85)/2))},
 {s:10.75,e:11.15,cap:1290,out:1,f:(g,t)=>wipe2(g,(t-10.75)/.4,h=>scene2(h,t,1.08),h=>mapScene2(h,t,10.9,16.6,wt('02.2',3),ps('02.3')))},
 {s:11.15,e:16.55,cap:1290,out:1,f:(g,t)=>mapScene2(g,t,10.9,16.6,wt('02.2',3),ps('02.3'))},
 {s:16.55,e:16.95,cap:1290,out:1,f:(g,t)=>wipe2(g,(t-16.55)/.4,h=>mapScene2(h,t,10.9,16.6,wt('02.2',3),ps('02.3')),h=>scene2(h,t,1.25))},
 {s:16.95,e:20.25,cap:1290,out:1,f:(g,t)=>scene2(g,t,lerp(1.25,1.8,easeOut((t-16.95)/3.3)))},
 {s:20.25,e:22.9,cap:1600,f:(g,t)=>days(g,t,20.25,ps('02.6'),pe('02.6'))},
 {s:22.9,e:26.6,cap:1600,out:1,f:(g,t)=>exitScene(g,t,22.9)},
 {s:26.6,e:31.35,cap:1600,out:1,f:(g,t)=>ropeScene(g,t,26.6,ps('03.1')+.2)},
 {s:31.35,e:32.78,cap:1600,out:1,f:(g,t)=>mittenScene(g,t,31.35,wt('03.3',0)+.15)},
 {s:32.78,e:35.55,cap:1600,out:1,f:(g,t)=>whiteout(g,t,ps('03.4'),pe('03.4')+.3)},
 {s:35.55,e:38.45,cap:1600,f:(g,t)=>fuelScene(g,t,35.55,ps('03.6'),pe('03.6'))},
 {s:38.45,e:40.95,cap:1600,out:1,f:(g,t)=>heliScene(g,t,38.45,40.95)},
 {s:40.95,e:43.3,cap:1600,f:(g,t)=>noErrorScene(g,t,40.95,wt('03.8',3))},
 {s:43.3,e:47.6,cap:1640,f:(g,t)=>portrait(g,t,{K:[[43.3,540,900,1.0],[47.6,540,880,1.1]],lamp:.55,radioGlow:1,look:0}),hud:t=>{if(t>ps('04.1'))scope(ctx,t,'flat',330)}},
 {s:47.6,e:48.85,cap:1640,f:(g,t)=>portrait(g,t,{K:[[47.6,540,860,1.2],[48.85,540,830,1.9]],lamp:.55,radioGlow:1,look:0,bo:1})},
 {s:48.85,e:51.65,cap:1520,f:(g,t)=>radio(g,t,{on:true,t0:48,t1:52,K:[[48.85,500,800,1.3],[51.65,480,800,1.55]]})},
 {s:51.65,e:54.35,cap:1520,f:(g,t)=>radio(g,t,{on:true,t0:0,t1:0,dim:.5,K:[[51.65,480,800,1.55],[54.35,480,800,1.65]]}),
   hud:t=>{scope(ctx,t,'beep',520);ctx.save();tag(ctx,140,860,'ПОЗЫВНОЙ:  —','#9fd4f5');if(t>ps('04.5'))tag(ctx,140,940,'ПОМЕХИ:  0 %','#9fd4f5');ctx.restore()}},
 {s:54.35,e:55.95,cap:1640,f:(g,t)=>portrait(g,t,{K:[[54.35,540,880,1.15],[55.95,560,880,1.25]],lamp:.55,radioGlow:1,look:t=>lerp(0,1,ease((t-54.6)/1))})},
 {s:55.95,e:58.95,cap:1600,f:(g,t)=>doorScene(g,t,55.95)},
 {s:58.95,e:61.5,cap:1520,f:(g,t)=>radio(g,t,{on:true,t0:0,t1:0,hits:[59.5,60.2,60.85],K:[[58.95,540,840,1.2],[61.5,540,840,1.25]]})},
 {s:61.5,e:64.75,cap:1520,f:(g,t)=>timerScene(g,t,61.5,61.7,64.6)},
 {s:64.75,e:67.35,cap:1520,f:(g,t)=>radio(g,t,{on:true,t0:64,t1:66,K:[[64.75,540,820,1.35],[67.35,540,820,1.2]]})},
 {s:67.35,e:71.35,cap:1640,f:(g,t)=>portrait(g,t,{K:[[67.35,540,920,1.0],[71.35,540,920,1.1]],lamp:.6,radioGlow:1,mic:true,look:-.1}),
   hud:t=>{if(t>ps('05.4')){ctx.save();ctx.globalAlpha=clamp((t-ps('05.4'))/.2,0,1);tag(ctx,380,420,'«КТО НА СВЯЗИ? НАЗОВИТЕ СЕБЯ»','#e7ddc4');ctx.restore()}}},
 {s:71.35,e:73.15,cap:1290,out:1,f:(g,t)=>scene2(g,t,1.6)},
 {s:73.15,e:75.95,cap:1520,f:(g,t)=>radio(g,t,{on:t=>t<wt('05.7',2),t0:0,t1:0,hits:[wt('05.7',2)],plug:t=>easeOut((t-wt('05.7',2))/.22),K:[[73.15,250,1150,1.6],[75.95,280,1250,1.5]]})},
 {s:75.95,e:79.6,cap:1640,f:(g,t)=>portrait(g,t,{K:[[75.95,540,900,1.05],[79.6,540,880,1.15]],lamp:.5,look:-.6})},
 {s:79.6,e:83.4,cap:1640,f:(g,t)=>clockScene(g,t,79.6)},
 {s:83.4,e:86.15,cap:1520,f:(g,t)=>{const r=radio(g,t,{on:false,t0:83,t1:85,lamp:.6,K:[[83.4,560,860,1.15],[86.15,560,860,1.3]]});SHOT_T=r.T},hud:t=>{ctx.save();tag(ctx,300,250,'⏻ ПИТАНИЕ: ВЫКЛ','#ff3b2f');ctx.restore()}},
 {s:86.15,e:88.75,cap:1640,f:(g,t)=>portrait(g,t,{K:[[86.15,540,860,1.25],[88.75,540,840,1.45]],lamp:t=>.45+.25*Math.abs(Math.sin(t*23)),wide:true,hits:[86.2],look:0})},
 {s:88.75,e:93.75,cap:1600,f:(g,t)=>timesScene(g,t)},
 {s:93.75,e:95.8,cap:1640,f:(g,t)=>portrait(g,t,{K:[[93.75,540,830,1.6],[95.8,540,830,1.9]],lamp:.6,look:t=>lerp(0,-1,ease((t-94.2)/.8))})},
 {s:95.8,e:99.75,cap:1600,f:(g,t)=>shelfScene(g,t,95.8,ps('07.5'))},
 {s:99.75,e:115.25,cap:1640,f:(g,t)=>journalScene(g,t,{K:[[99.75,500,1.0],[101.7,460,1.05],[106.5,500,1.1],[108.0,470,1.6],[110.3,520,1.5],[112.2,2250,1.25],[115.25,2330,1.35]],c:[ps('08.1'),ps('08.2'),ps('08.3')],u:ps('08.8')+.1,tag:[ps('08.4'),'ПРОШЛАЯ ЗИМА · ПОЧЕРК: НЕИЗВЕСТЕН']})},
 {s:115.25,e:120.2,cap:1640,f:(g,t)=>portrait(g,t,{K:[[115.25,540,880,1.1],[120.2,540,860,1.35]],lamp:t=>lerp(.6,.05,ease((t-117.5)/2.3)),look:-.4})},
 {s:120.2,e:TOTAL,cap:-1,f:(g,t)=>endCard(g,t,120.2)},
];
let SHOT_T=null;
function wipe2(g,p,drawOld,drawNew){const cx=lerp(W+900,-900,easeInOut(p));drawOld(BA);drawNew(BB);g.drawImage(BUF_A,0,0);g.save();g.beginPath();g.rect(cx,0,W*4,H);g.clip();g.drawImage(BUF_B,0,0);g.restore();g.drawImage(WIPE,cx-900,-880)}

window.renderFrame=function(t){
  ctx.setTransform(1,0,0,1,0,0);ctx.globalAlpha=1;ctx.globalCompositeOperation='source-over';ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
  const sh=SHOTS.find(s=>t>=s.s&&t<s.e)||SHOTS[SHOTS.length-1];
  ctx.save();sh.f(ctx,t);ctx.restore();ctx.setTransform(1,0,0,1,0,0);
  if(sh.cap!==-1)finish(t);
  if(sh.hud)sh.hud(t);
  if(t>=8.85&&t<120.2){let cur=null;for(const k of STK)if(t>=k[0])cur=k;if(cur)sticker2(t,cur[0],cur[1],cur[2])}
  if(t>=9.4&&t<43.3)thermo(t,9.4);
  // flashes on hard cuts
  for(const c of [1.0,7.45,48.85,83.4]){if(t>=c&&t<c+.16){ctx.fillStyle=`rgba(235,245,248,${.6*(1-(t-c)/.16)})`;ctx.fillRect(0,0,W,H)}}
  if(sh.cap>0)captions3(t,sh.cap);
  if(t>TOTAL-.6){ctx.fillStyle=`rgba(0,0,0,${clamp((t-(TOTAL-.6))/.6,0,1)})`;ctx.fillRect(0,0,W,H)}
};
window.ready=document.fonts.load('900 78px Mont').then(()=>document.fonts.load('700 70px Hand')).then(()=>document.fonts.load('700 26px "JetBrains Mono"')).then(()=>true);
