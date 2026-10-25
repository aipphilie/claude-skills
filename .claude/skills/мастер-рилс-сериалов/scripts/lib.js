const W=1080,H=1920,FPS=30;
const cv=document.getElementById('c');cv.width=W;cv.height=H;
const ctx=cv.getContext('2d');
const MONO='"JetBrains Mono", monospace';

// ---------- utils ----------
function rng(seed){return function(){seed|=0;seed=seed+0x6D2B79F5|0;let t=Math.imul(seed^seed>>>15,1|seed);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
const clamp=(x,a,b)=>Math.max(a,Math.min(b,x));
const lerp=(a,b,t)=>a+(b-a)*t;
const ease=t=>{t=clamp(t,0,1);return t*t*(3-2*t)};
const easeOut=t=>{t=clamp(t,0,1);return 1-Math.pow(1-t,3)};
const easeInOut=t=>{t=clamp(t,0,1);return t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2};
const easeOutBack=t=>{t=clamp(t,0,1);const c1=1.70158,c3=c1+1;return 1+c3*Math.pow(t-1,3)+c1*Math.pow(t-1,2)};
function mk(w=W,h=H){const c=document.createElement('canvas');c.width=w;c.height=h;return c}
function path(g,pts){g.beginPath();g.moveTo(pts[0][0],pts[0][1]);for(let i=1;i<pts.length;i++)g.lineTo(pts[i][0],pts[i][1]);g.closePath()}
function poly(g,pts,fill){path(g,pts);g.fillStyle=fill;g.fill()}
// "hand-cut" edges: subdivide every edge and shake the points
function jag(pts,R,amp=4,seg=3){const out=[];const n=pts.length;for(let i=0;i<n;i++){const a=pts[i],b=pts[(i+1)%n];for(let s=0;s<seg;s++){const k=s/seg;out.push([lerp(a[0],b[0],k)+(s?(R()-.5)*2*amp:0),lerp(a[1],b[1],k)+(s?(R()-.5)*2*amp:0)])}}return out}
function glow(g,x,y,r,col,a){const gr=g.createRadialGradient(x,y,0,x,y,r);gr.addColorStop(0,col.replace('A',a));gr.addColorStop(1,col.replace('A',0));g.fillStyle=gr;g.fillRect(x-r,y-r,r*2,r*2)}

function pine(g,R,x,by,h,col,snow){
  g.fillStyle=col;g.fillRect(x-h*.025,by-h*.14,h*.05,h*.16);
  for(let i=0;i<4;i++){
    const ty=by-h*.1-i*h*.21,tw=h*.5*(1-i*.2),th=h*.36;
    poly(g,jag([[x+(R()-.5)*h*.02,ty-th],[x+tw/2,ty],[x-tw/2,ty]],R,h*.018,3),col);
    if(snow)poly(g,jag([[x,ty-th],[x-tw*.32,ty-th*.36],[x-tw*.08,ty-th*.42],[x+tw*.06,ty-th*.7]],R,h*.01,2),snow);
  }
}
function mountain(g,R,x,base,w,h,dark,light,snow,snowDark){
  const peak=[x+(R()-.5)*w*.15,base-h],L=[x-w/2,base],Rt=[x+w/2,base],mid=[peak[0]+(R()-.2)*w*.18,base];
  poly(g,jag([L,peak,mid],R,7,4),light);
  poly(g,jag([peak,Rt,mid],R,7,4),dark);
  const k1=.26+R()*.1,k2=.22+R()*.1;
  const a=[lerp(peak[0],L[0],k1),lerp(peak[1],L[1],k1)],b=[lerp(peak[0],Rt[0],k2),lerp(peak[1],Rt[1],k2)];
  const m=[lerp(peak[0],mid[0],k1*1.2),lerp(peak[1],mid[1],k1*1.2)];
  poly(g,jag([peak,m,[lerp(a[0],m[0],.5),a[1]-6],a],R,5,2),snow);
  poly(g,jag([peak,b,[lerp(b[0],m[0],.5),b[1]+8],m],R,5,2),snowDark);
}

// ---------- shared overlays ----------
const PAINT=mk();{const g=PAINT.getContext('2d'),R=rng(7);
  for(let i=0;i<5200;i++){const x=R()*W,y=R()*H,l=20+R()*70,w=3+R()*9,a=-.35+R()*.15;
    g.save();g.translate(x,y);g.rotate(a);g.fillStyle=R()<.5?`rgba(255,255,255,${.03+R()*.05})`:`rgba(0,0,0,${.04+R()*.07})`;g.fillRect(-l/2,-w/2,l,w);g.restore();}}
const GRAIN=[];for(let k=0;k<6;k++){const c=mk(540,960),g=c.getContext('2d'),d=g.createImageData(540,960),R=rng(100+k);
  for(let i=0;i<d.data.length;i+=4){const v=R()*255;d.data[i]=d.data[i+1]=d.data[i+2]=v;d.data[i+3]=255}g.putImageData(d,0,0);GRAIN.push(c)}
const SNOW=[];{const R=rng(3);for(let i=0;i<260;i++)SNOW.push({x:R()*W*1.4,y:R()*H,z:.3+R()*R()*1.7,s:R()})}
function drawSnow(g,t,amt=1,wind=1){
  g.fillStyle='#dfe8ea';
  for(const p of SNOW){const sp=60+p.z*110;let x=(p.x+t*sp*.55*wind+Math.sin(t*1.3+p.s*9)*14)%(W*1.4)-W*.2,y=(p.y+t*sp)%H;
    g.globalAlpha=Math.min(1,(.25+p.z*.35))*amt;const s=1.6+p.z*3.2;g.fillRect(x,y,s,s)}
  g.globalAlpha=1}
function finish(t,dark=0){
  ctx.globalCompositeOperation='overlay';ctx.globalAlpha=.55;ctx.drawImage(PAINT,0,0);
  ctx.globalAlpha=.10;ctx.drawImage(GRAIN[Math.floor(t*FPS)%6],0,0,W,H);
  ctx.globalCompositeOperation='source-over';ctx.globalAlpha=1;
  const v=ctx.createRadialGradient(W/2,H*.46,H*.22,W/2,H*.5,H*.72);
  v.addColorStop(0,'rgba(0,0,0,0)');v.addColorStop(1,`rgba(0,0,0,${.78+dark})`);ctx.fillStyle=v;ctx.fillRect(0,0,W,H);
}

// ---------- camera ----------
function cam(g,cx,cy,z,ax=540,ay=860,depth=1,base=1){
  const s=base*(1+(z-1)*depth);let ox=ax-cx*s,oy=ay-cy*s;
  ox=clamp(ox,W-W*s,0);oy=clamp(oy,H-H*s,0);g.setTransform(s,0,0,s,ox,oy);
}

// =====================================================================
// SCENE 1 — radio close-up (interior)
// =====================================================================
const S1=mk();{const g=S1.getContext('2d'),R=rng(11);
  g.fillStyle='#10181c';g.fillRect(0,0,W,H);
  for(let x=-20;x<W;x+=96)poly(g,jag([[x,0],[x+92,0],[x+92,1150],[x,1150]],R,3,6),R()<.5?'#131d22':'#0f171b');
  // frosted window on the wall
  poly(g,[[110,230],[400,230],[400,560],[110,560]],'#0a1216');
  poly(g,[[126,246],[384,246],[384,544],[126,544]],'#1b3a47');
  glow(g,250,400,220,'rgba(80,140,150,A)',.25);
  for(let i=0;i<40;i++){const side=i%4;let x,y;if(side==0){x=126+R()*258;y=246}else if(side==1){x=384;y=246+R()*298}else if(side==2){x=126+R()*258;y=544}else{x=126;y=246+R()*298}
    const l=18+R()*46,a=R()*Math.PI*2;poly(g,[[x,y],[x+Math.cos(a)*l,y+Math.sin(a)*l],[x+Math.cos(a+.25)*l*.6,y+Math.sin(a+.25)*l*.6]],`rgba(200,225,235,${.25+R()*.3})`)}
  g.fillStyle='#0a1216';g.fillRect(250,246,10,298);g.fillRect(126,390,258,10);
  // wall socket
  poly(g,[[86,1010],[146,1010],[146,1080],[86,1080]],'#2a3436');g.fillStyle='#0b1012';g.fillRect(104,1036,7,18);g.fillRect(121,1036,7,18);
  // table
  poly(g,jag([[0,1140],[W,1120],[W,H],[0,H]],R,3,8),'#2a1f19');
  poly(g,jag([[0,1140],[W,1120],[W,1160],[0,1182]],R,2,8),'#3b2b21');
  for(let i=0;i<14;i++){const y=1220+R()*700;g.strokeStyle='rgba(0,0,0,.25)';g.lineWidth=2;g.beginPath();g.moveTo(0,y);g.lineTo(W,y-30+R()*20);g.stroke()}
  // radio body
  poly(g,[[210,640],[870,640],[880,1100],[200,1100]],'#2d3b38');
  poly(g,[[210,640],[870,640],[860,664],[220,664]],'#4b5f59');
  poly(g,[[870,640],[900,660],[905,1095],[880,1100]],'#1b2523');
  poly(g,[[245,690],[835,690],[835,1060],[245,1060]],'#222e2c');
  // dial window
  poly(g,[[280,725],[565,725],[565,870],[280,870]],'#0f1413');
  const dg=g.createLinearGradient(0,735,0,860);dg.addColorStop(0,'#f2b55a');dg.addColorStop(1,'#a8641f');
  g.fillStyle=dg;g.fillRect(292,737,261,121);
  g.fillStyle='rgba(40,20,5,.85)';for(let i=0;i<=26;i++){const x=300+i*9.6;g.fillRect(x,742,2,i%5?14:26)}
  g.font='700 16px '+MONO;g.fillText('150   300   600   1200  кГц',300,845);
  // speaker
  g.fillStyle='#161e1d';g.beginPath();g.arc(705,805,112,0,7);g.fill();
  g.save();g.beginPath();g.arc(705,805,98,0,7);g.clip();g.fillStyle='#0b100f';for(let y=700;y<915;y+=16)g.fillRect(590,y,240,8);g.restore();
  // knobs
  for(const [x,y,r] of [[320,965,40],[440,965,40],[700,975,52]]){g.fillStyle='#121918';g.beginPath();g.arc(x,y,r,0,7);g.fill();g.fillStyle='#2b3735';g.beginPath();g.arc(x-4,y-5,r*.78,0,7);g.fill();g.fillStyle='#c9bfa5';g.fillRect(x-2,y-r*.75,4,r*.4)}
  // power toggle in OFF
  g.fillStyle='#121918';g.fillRect(540,935,46,70);g.fillStyle='#8a948f';g.fillRect(554,972,18,40);
  g.fillStyle='#c9bfa5';g.font='700 18px '+MONO;g.fillText('ВКЛ',538,926);g.fillText('ВЫКЛ',534,1036);
  // frost on radio corners
  for(let i=0;i<26;i++){const x=i<13?210+R()*130:740+R()*130,y=640+R()*10,l=14+R()*34,a=Math.PI*.3+R()*Math.PI*.4;
    poly(g,[[x,y],[x+Math.cos(a)*l,y+Math.sin(a)*l],[x+Math.cos(a+.3)*l*.5,y+Math.sin(a+.3)*l*.5]],`rgba(200,225,235,${.3+R()*.3})`)}
  // log book + pencil
  poly(g,jag([[700,1210],[900,1190],[1060,1240],[860,1270]],R,2,3),'#14100d');
  poly(g,jag([[705,1196],[880,1178],[882,1258],[862,1262]],R,2,3),'#b7ab90');
  poly(g,jag([[880,1178],[1050,1222],[1048,1262],[882,1258]],R,2,3),'#9d927a');
  g.strokeStyle='rgba(60,50,40,.55)';g.lineWidth=2;for(let i=0;i<6;i++){g.beginPath();g.moveTo(725,1200+i*10);g.lineTo(865,1186+i*10);g.stroke();g.beginPath();g.moveTo(895,1192+i*10);g.lineTo(1035,1230+i*6);g.stroke()}
  poly(g,[[760,1300],[960,1282],[962,1290],[762,1308]],'#b5793a');
  // kerosene lamp
  poly(g,[[905,1135],[1015,1135],[1000,1095],[920,1095]],'#3a2a1a');
  poly(g,jag([[925,1095],[995,1095],[1010,1000],[985,930],[935,930],[910,1000]],R,2,2),'rgba(255,214,150,.35)');
  poly(g,[[930,930],[990,930],[982,905],[938,905]],'#2a2018');
}
let S1T=null;let MOTES=[];{const R=rng(21);for(let i=0;i<46;i++)MOTES.push({x:600+R()*480,y:600+R()*900,s:R()})}
function scene1(g,t){
  // camera keys: [time, cx, cy, zoom]
  const K=[[1.0,540,820,1.32],[2.5,540,830,1.40],[2.85,370,1360,1.55],[3.4,370,1380,1.62],[3.75,560,900,1.12],[5.9,560,880,1.20]];
  let k=0;while(k<K.length-2&&t>K[k+1][0])k++;const a=K[k],b=K[k+1],p=easeInOut((t-a[0])/(b[0]-a[0]));
  let cx=lerp(a[1],b[1],p),cy=lerp(a[2],b[2],p),z=lerp(a[3],b[3],p);
  let shake=0;for(const bt of BEEPS)if(bt>4&&t>=bt&&t<bt+.18)shake=6*(1-(t-bt)/.18);
  g.save();cam(g,cx+Math.sin(t*90)*shake,cy+Math.cos(t*77)*shake,z);
  g.drawImage(S1,0,0);S1T=g.getTransform();
  // lamp flame + warm light
  const fl=.85+.15*Math.sin(t*13)*Math.sin(t*7.3);
  g.globalCompositeOperation='lighter';
  glow(g,960,1010,520*fl,'rgba(232,150,60,A)',.30);
  glow(g,960,1010,110,'rgba(255,190,100,A)',.55*fl);
  g.globalCompositeOperation='source-over';
  poly(g,[[960,1060],[972,1030],[960,995],[948,1030]],'#ffd27a');
  // dial needle (jumps on beeps)
  let nx=402+Math.sin(t*2.1)*2;for(const bt of BEEPS)if(t>=bt&&t<bt+.13)nx+=46;
  g.fillStyle='#c0261b';g.fillRect(nx,738,4,118);
  // speaker emits rings on beeps
  for(const bt of BEEPS){const d=t-bt;if(d>0&&d<.6){g.strokeStyle=`rgba(255,226,160,${(1-d/.6)*.75})`;g.lineWidth=5;g.beginPath();g.arc(705,805,112+d*420,0,7);g.stroke()}}
  // dust motes in lamp light
  g.fillStyle='#ffd9a0';for(const m of MOTES){g.globalAlpha=.25+.25*Math.sin(t*2+m.s*20);g.fillRect(m.x+Math.sin(t*.4+m.s*9)*30,m.y-((t*14+m.s*400)%400),3,3)}g.globalAlpha=1;
  g.restore();
  return {cx,cy,z};
}

// =====================================================================
// SCENE 2 — wide: sky, mountains, station
// =====================================================================
const HZ=1030;
const AUR=mk(W*2,900);{const g=AUR.getContext('2d'),R=rng(5);
  for(let band=0;band<3;band++){const base=180+band*120,amp=60+band*25,f=.004+band*.0015,ph=R()*6;
    for(let x=0;x<W*2;x+=4){const y=base+Math.sin(x*f+ph)*amp+Math.sin(x*f*2.7)*amp*.3,len=140+Math.sin(x*.01+ph)*80+band*30;
      const gr=g.createLinearGradient(0,y,0,y+len);gr.addColorStop(0,'rgba(95,191,143,0)');gr.addColorStop(.25,`rgba(95,191,143,${.10+.06*Math.sin(x*.02+band)})`);gr.addColorStop(1,'rgba(95,191,143,0)');
      g.fillStyle=gr;g.fillRect(x,y,4,len)}}}
const STARS=[];{const R=rng(9);for(let i=0;i<190;i++)STARS.push({x:R()*W,y:R()*HZ*.85,s:R()<.12?3:2,p:R()*9})}
const L1=mk(),L2=mk(),L3=mk(),L4=mk();
{const g=L1.getContext('2d'),R=rng(31);
  for(const [x,w,h] of [[60,520,250],[330,620,360],[660,560,300],[980,600,330],[1180,400,200],[-120,420,190]])mountain(g,R,x,HZ+30,w,h,'#172d35','#26434c','#8ea7ad','#5d7880');
  for(const [x,w,h] of [[170,360,150],[520,420,170],[860,380,140]])mountain(g,R,x,HZ+40,w,h,'#142730','#1e3841','#6f8a92','#4b6670');}
{const g=L2.getContext('2d'),R=rng(41);
  const ridge=[[0,HZ+28]];for(let x=0;x<=W;x+=60)ridge.push([x,HZ+20+Math.sin(x*.012)*14+R()*10]);ridge.push([W,HZ+120],[0,HZ+120]);
  poly(g,ridge,'#1a323b');
  for(let i=0;i<140;i++){const x=R()*W,h=26+R()*R()*80;if(Math.abs(x-560)<150&&h>40)continue;pine(g,R,x,HZ+50+R()*30,h,'#0d1b21','#4c6a74')}}
{const g=L3.getContext('2d'),R=rng(51);
  const sg=g.createLinearGradient(0,HZ+60,0,H);sg.addColorStop(0,'#3d5e68');sg.addColorStop(.35,'#2c4a54');sg.addColorStop(1,'#172d36');
  path(g,jag([[0,HZ+70],[W,HZ+64],[W,H],[0,H]],R,4,10));g.fillStyle=sg;g.fill();
  for(let i=0;i<9;i++){const y=HZ+120+i*80+R()*40,x=R()*W*.8-100,w=300+R()*500;
    poly(g,jag([[x,y],[x+w*.5,y-14-R()*12],[x+w,y+2],[x+w*.5,y+8]],R,4,3),'rgba(120,150,158,.35)');
    poly(g,jag([[x,y],[x+w,y+2],[x+w*.6,y+26],[x+w*.2,y+18]],R,4,3),'rgba(15,30,38,.35)')}
  // long blue shadow of the station
  poly(g,[[470,1195],[655,1195],[900,1260],[640,1270]],'rgba(12,26,34,.55)');
  // instrument booth + rope line with 3 poles (the knot is at the third)
  g.strokeStyle='#0e1a1f';g.lineWidth=3;
  for(const x of [440,405,370]){g.beginPath();g.moveTo(x,1190);g.lineTo(x,1166);g.stroke()}
  g.strokeStyle='#22343a';g.lineWidth=2;g.beginPath();g.moveTo(470,1168);g.quadraticCurveTo(455,1174,440,1167);g.quadraticCurveTo(422,1174,405,1167);g.quadraticCurveTo(388,1174,370,1167);g.quadraticCurveTo(355,1172,340,1166);g.stroke();
  g.fillStyle='#0e1a1f';g.fillRect(318,1160,3,34);g.fillRect(346,1160,3,34);
  poly(g,[[310,1134],[352,1134],[352,1162],[310,1162]],'#a9bcc1');poly(g,[[306,1130],[356,1130],[350,1124],[312,1124]],'#d2dde0');
  g.fillStyle='rgba(30,50,60,.6)';for(let i=0;i<4;i++)g.fillRect(314,1138+i*6,34,2);
  // station building
  poly(g,[[470,1128],[612,1128],[612,1196],[470,1196]],'#1b2c33');
  poly(g,[[612,1128],[650,1112],[650,1186],[612,1196]],'#101c21');
  poly(g,jag([[458,1132],[540,1092],[624,1132]],R,3,3),'#9ab1b7');
  poly(g,jag([[540,1092],[624,1132],[660,1114],[580,1078]],R,3,3),'#5f7a82');
  poly(g,[[572,1152],[592,1152],[592,1196],[572,1196]],'#0b151a');
  g.fillStyle='#0d181c';g.fillRect(584,1066,12,28);
  // snow drift against walls
  poly(g,jag([[440,1200],[480,1178],[560,1186],[640,1176],[690,1204]],R,3,3),'#4a6b75');
  // antenna mast with guy wires
  g.strokeStyle='#0c171b';g.lineWidth=4;g.beginPath();g.moveTo(690,1196);g.lineTo(694,900);g.stroke();
  g.lineWidth=2;for(let y=930;y<1190;y+=34){g.beginPath();g.moveTo(684,y);g.lineTo(702,y+17);g.stroke()}
  g.lineWidth=1.5;g.strokeStyle='rgba(10,20,25,.8)';for(const gx of [640,760,720]){g.beginPath();g.moveTo(694,920);g.lineTo(gx,1200);g.stroke()}
  g.fillStyle='#0c171b';g.fillRect(676,902,36,4);}
{const g=L4.getContext('2d'),R=rng(61);
  pine(g,R,40,H+60,1250,'#060e11','#24404a');pine(g,R,-140,H+40,900,'#05090b',null);
  pine(g,R,1060,H+80,1150,'#060e11','#24404a');pine(g,R,1240,H+20,950,'#05090b',null);
  const d=[[0,1700],[180,1640],[420,1680],[700,1620],[900,1660],[W,1610],[W,H],[0,H]];
  poly(g,jag(d,R,6,4),'#223a43');
  poly(g,jag([[0,1700],[180,1640],[420,1680],[700,1620],[900,1660],[W,1610],[W,1630],[900,1680],[700,1642],[420,1700],[180,1662],[0,1722]],R,3,2),'#6a8a93');}

function sky(g,t){
  const sg=g.createLinearGradient(0,0,0,HZ+40);
  sg.addColorStop(0,'#060d13');sg.addColorStop(.45,'#0f222b');sg.addColorStop(.8,'#1d3a44');sg.addColorStop(1,'#335a63');
  g.fillStyle=sg;g.fillRect(0,0,W,HZ+60);
  for(const s of STARS){g.globalAlpha=.35+.45*Math.abs(Math.sin(t*.9+s.p));g.fillStyle='#e6eef0';g.fillRect(s.x,s.y,s.s,s.s)}
  g.globalAlpha=.75+.25*Math.sin(t*.5);g.drawImage(AUR,-((t*10)%W),0);g.globalAlpha=1;
  g.fillStyle='#d9e2e0';g.beginPath();g.arc(800,330,26,0,7);g.fill();glow(g,800,330,110,'rgba(200,220,220,A)',.18);
}
function scene2(g,t,z){
  const px=520,py=1150,ax=540,ay=1150;
  g.save();cam(g,px,py,z,ax,ay,.08);sky(g,t);g.restore();
  for(const [L,d] of [[L1,.35],[L2,.6]]){g.save();cam(g,px,py,z,ax,ay,d);g.drawImage(L,0,0);g.restore()}
  g.save();cam(g,px,py,z,ax,ay,.9);g.drawImage(L3,0,0);
  // window glow, smoke, mast light
  const fl=.85+.15*Math.sin(t*11)*Math.sin(t*4.7);
  g.fillStyle='#ffb447';g.fillRect(498,1148,24,18);
  g.globalCompositeOperation='lighter';glow(g,510,1157,170,'rgba(232,150,60,A)',.28*fl);glow(g,510,1157,40,'rgba(255,200,120,A)',.6*fl);g.globalCompositeOperation='source-over';
  for(let k=0;k<14;k++){const p=(t*.22+k/14)%1;g.fillStyle=`rgba(160,182,188,${(1-p)*.32})`;g.beginPath();g.arc(590+p*150+Math.sin(p*6+k)*8,1062-p*230,7+p*30,0,7);g.fill()}
  if((t%1.4)<.18){g.globalCompositeOperation='lighter';glow(g,694,898,40,'rgba(255,60,40,A)',.9);g.globalCompositeOperation='source-over';g.fillStyle='#ff4a3a';g.fillRect(690,894,8,8)}
  g.restore();
  g.save();cam(g,px,py,z,ax,ay,1.0);g.drawImage(L4,0,0);g.restore();
  drawSnow(g,t,1,1.2);
}

// =====================================================================
// MAP — top-down, radar rings
// =====================================================================
const MW=2400,MH=3000,MCX=1200,MCY=1500;
const MAP=mk(MW,MH);{const g=MAP.getContext('2d'),R=rng(71);
  g.fillStyle='#13252d';g.fillRect(0,0,MW,MH);
  const S=120,nx=MW/S+2,ny=MH/S+2,P=[];
  for(let i=0;i<nx;i++){P.push([]);for(let j=0;j<ny;j++)P[i].push([i*S+(R()-.5)*S*.7,j*S+(R()-.5)*S*.7])}
  const pal=['#0e1d24','#12242c','#162a33','#1a3039','#1f3640','#263f49','#2e4952'];
  for(let i=0;i<nx-1;i++)for(let j=0;j<ny-1;j++){
    const n=Math.sin(i*.33)+Math.cos(j*.27)+Math.sin((i+j)*.11)*1.2+R()*1.1;
    const c1=pal[clamp(Math.floor(n+3.2),0,6)],c2=pal[clamp(Math.floor(n+2.6+R()),0,6)];
    poly(g,[P[i][j],P[i+1][j],P[i][j+1]],c1);poly(g,[P[i+1][j],P[i+1][j+1],P[i][j+1]],c2)}
  // frozen river
  const rv=[];for(let y=-50;y<=MH+50;y+=60)rv.push([500+y*.55+Math.sin(y*.004)*260+(R()-.5)*30,y]);
  g.lineJoin='miter';g.strokeStyle='#33545d';g.lineWidth=34;g.beginPath();rv.forEach((p,i)=>i?g.lineTo(p[0],p[1]):g.moveTo(p[0],p[1]));g.stroke();
  g.strokeStyle='#4f727a';g.lineWidth=9;g.stroke();
  for(const [x,y,r] of [[1750,700,120],[700,2350,160],[1900,2300,90]])poly(g,jag([[x-r,y],[x-r*.3,y-r*.7],[x+r*.6,y-r*.5],[x+r,y+r*.1],[x+r*.2,y+r*.6],[x-r*.6,y+r*.5]],R,10,3),'#2d4c55');
  for(let c=0;c<80;c++){const cx=R()*MW,cy=R()*MH;if(Math.hypot(cx-MCX,cy-MCY)<160)continue;const n=10+R()*40;
    for(let k=0;k<n;k++){const x=cx+(R()-.5)*160,y=cy+(R()-.5)*160,s=7+R()*9;poly(g,[[x,y-s*1.4],[x+s*.6,y],[x-s*.6,y]],'#09151a')}}
}
const RINGS=[[9.45,217,'100 КМ'],[9.95,433,'200 КМ'],[10.5,650,'300 КМ — НИ ДУШИ']];
function tag(g,x,y,txt,col,fill){g.font='700 26px '+MONO;const w=g.measureText(txt).width+26;
  g.fillStyle=fill||'rgba(8,16,20,.82)';g.fillRect(x,y-22,w,44);g.strokeStyle=col;g.lineWidth=2;g.strokeRect(x,y-22,w,44);
  g.fillStyle=fill?'#0b1418':col;g.fillText(txt,x+13,y+9);return w}
function mapScene(g,t){
  const s=lerp(1.5,.8,easeOut((t-9.0)/4.2)),sx=540,sy=820;
  g.save();g.setTransform(s,0,0,s,sx-MCX*s,sy-MCY*s);g.drawImage(MAP,0,0);g.restore();
  const fog=g.createRadialGradient(sx,sy,200,sx,sy,1100);fog.addColorStop(0,'rgba(5,10,13,0)');fog.addColorStop(1,'rgba(5,10,13,.75)');g.fillStyle=fog;g.fillRect(0,0,W,H);
  // signal pulses
  for(let k=0;k<4;k++){const p=(((t-9)*.7+k/4)%1+1)%1;g.strokeStyle=`rgba(232,162,74,${(1-p)*.35})`;g.lineWidth=2;g.beginPath();g.arc(sx,sy,p*720*s,0,7);g.stroke()}
  // range rings
  for(const [t0,r,lab] of RINGS){if(t<t0)continue;const p=easeOut((t-t0)/.7),rr=r*s*p;
    g.setLineDash([16,12]);g.lineDashOffset=-t*20;g.strokeStyle='rgba(232,162,74,.9)';g.lineWidth=3;g.beginPath();g.arc(sx,sy,rr,0,7);g.stroke();g.setLineDash([]);
    g.fillStyle='rgba(232,162,74,.05)';g.beginPath();g.arc(sx,sy,rr,0,7);g.fill();
    if(p>.6){const a=-0.75,lx=sx+Math.cos(a)*rr,ly=sy+Math.sin(a)*rr;g.globalAlpha=ease((p-.6)/.4);
      const last=r===650;const w=tag(g,Math.min(lx+8,W-30-(last?470:190)),ly,lab,'#e8a24a',last?'#e8a24a':null);g.globalAlpha=1}}
  // mainland link
  if(t>11.35){const p=easeOut((t-11.35)/.7),ex=sx+760*p,ey=sy-900*p;
    g.setLineDash([6,10]);g.strokeStyle='#cfe3e8';g.lineWidth=3;g.beginPath();g.moveTo(sx,sy);g.lineTo(ex,ey);g.stroke();g.setLineDash([]);
    if(p>.8){g.globalAlpha=ease((p-.8)/.2);tag(g,520,330,'МАТЕРИК ↗  СВЯЗЬ 08:00 / 20:00','#cfe3e8');g.globalAlpha=1}}
  // the station
  const fl=.85+.15*Math.sin(t*9);
  g.globalCompositeOperation='lighter';glow(g,sx,sy,140,'rgba(232,150,60,A)',.55*fl);g.globalCompositeOperation='source-over';
  g.fillStyle='#ffb447';g.fillRect(sx-9,sy-9,18,18);g.strokeStyle='#0b1418';g.lineWidth=3;g.strokeRect(sx-9,sy-9,18,18);
  g.globalAlpha=clamp((t-9.2)/.3,0,1);tag(g,sx+28,sy+44,'СТ. «СЕВЕРНАЯ»','#e8a24a');g.globalAlpha=1;
  drawSnow(g,t,.6,.5);
}

// =====================================================================
// transitions, HUD, captions
// =====================================================================
const BUF_A=mk(),BUF_B=mk(),BA=BUF_A.getContext('2d'),BB=BUF_B.getContext('2d');
const WIPE=mk(1800,H+900);{const g=WIPE.getContext('2d'),R=rng(81);pine(g,R,900,H+880,2600,'#04090b','#1c333b')}
function wipe(p,drawOld,drawNew){
  const cx=lerp(W+900,-900,easeInOut(p));
  drawOld(BA);drawNew(BB);
  ctx.drawImage(BUF_A,0,0);
  ctx.save();ctx.beginPath();ctx.rect(cx,0,W*4,H);ctx.clip();ctx.drawImage(BUF_B,0,0);ctx.restore();
  ctx.drawImage(WIPE,cx-900,-880);
}
function sticker(t,t0){if(t<t0)return;const a=t-t0,y=lerp(-260,0,easeOutBack(a/.45)),rot=(-4+7*Math.exp(-a*5)*Math.sin(a*18))*Math.PI/180;
  const R=rng(5);ctx.save();ctx.translate(205,165+y);ctx.rotate(rot);ctx.shadowColor='rgba(0,0,0,.55)';ctx.shadowBlur=24;ctx.shadowOffsetY=10;
  poly(ctx,jag([[-150,-70],[150,-70],[150,70],[-150,70]],R,2,4),'#e7ddc4');ctx.shadowColor='transparent';
  ctx.save();ctx.rotate(.06);ctx.fillStyle='rgba(200,190,160,.85)';ctx.fillRect(-55,-86,110,30);ctx.restore();
  ctx.textAlign='center';ctx.fillStyle='#2a2420';ctx.font='700 70px Hand';ctx.fillText('День 47',0,8);
  ctx.fillStyle='#6a5d50';ctx.font='700 30px Hand';ctx.fillText('02:10 · ст. «Северная»',0,50);ctx.restore()}
function thermo(t,t0){if(t<t0)return;const p=easeOut((t-t0)/.4),x=lerp(W+40,786,p);
  ctx.save();ctx.fillStyle='rgba(6,14,20,.78)';ctx.fillRect(x,96,250,108);ctx.strokeStyle='#6fc3ff';ctx.lineWidth=2;ctx.strokeRect(x,96,250,108);
  ctx.fillStyle='#6fc3ff';ctx.font='700 20px '+MONO;ctx.fillText('✱ СНАРУЖИ',x+16,128);
  ctx.fillStyle='#d6efff';ctx.font='800 52px '+MONO;ctx.fillText('−38°C',x+16,184);
  ctx.fillStyle='rgba(6,14,20,.78)';ctx.fillRect(x,214,250,44);ctx.strokeStyle='rgba(111,195,255,.5)';ctx.strokeRect(x,214,250,44);
  ctx.fillStyle='#9fd4f5';ctx.font='700 22px '+MONO;ctx.fillText('ВЕТЕР 14 М/С ↘',x+16,244);ctx.restore()}
