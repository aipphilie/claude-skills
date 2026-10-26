// ===== scenes of the 14 s test (cold open + hook) =====
const SV=1;// Sonya variant used in the video
function renderFaceCard(v){
  ctx.setTransform(1,0,0,1,0,0);
  let gr=ctx.createLinearGradient(0,0,0,H);gr.addColorStop(0,'#0d1512');gr.addColorStop(1,'#050707');ctx.fillStyle=gr;ctx.fillRect(0,0,W,H);
  glow(ctx,260,620,900,'255,150,50',.45);glow(ctx,900,900,700,'120,170,220',.12);
  smoke(ctx,3+v,0,0,W,H,{alpha:.18,scale:2.2,sheet:v});
  drawSonya(ctx,540,760,640,{v,t:1,rim:1,fill:.8,look:[.15,-.1]});
  finish(1,{vig:.7});
  ctx.font='60px MB';ctx.textAlign='center';ctx.fillStyle='#fff';ctx.fillText('ВАРИАНТ '+(v+1),540,1560);
  ctx.font='44px MB';ctx.fillStyle='#f2c418';ctx.fillText(HAIRS[v].name.toUpperCase(),540,1630);
}

// ---------- helpers for painted metal / concrete ----------
function texFill(g,x,y,w,h,base,seed,{grime=.8,specks=.6,streaks=0}={}){
  g.save();g.beginPath();g.rect(x,y,w,h);g.clip();g.fillStyle=base;g.fillRect(x,y,w,h);
  g.globalAlpha=grime;g.drawImage(GRIME,x-(seed%7)*40,y-(seed%5)*60,Math.max(w,540)*1.4,Math.max(h,960)*1.2);
  g.globalAlpha=specks;g.drawImage(SPECK,x,y,W,H);g.globalAlpha=1;
  if(streaks){const R=rng(seed);for(let i=0;i<streaks;i++){const sx=x+R()*w,sy=y+R()*h*.6,l=60+R()*260;
    const gr=g.createLinearGradient(0,sy,0,sy+l);gr.addColorStop(0,`rgba(${R()<.5?'110,55,25':'40,30,20'},${.25+R()*.3})`);gr.addColorStop(1,'rgba(60,30,15,0)');
    g.fillStyle=gr;g.fillRect(sx,sy,2+R()*6,l)}}
  g.restore()}
function rivets(g,x0,x1,y,step,col='rgba(255,220,180,.25)'){for(let x=x0;x<=x1;x+=step){g.fillStyle='rgba(0,0,0,.5)';g.beginPath();g.arc(x+1.5,y+1.5,4,0,7);g.fill();g.fillStyle='#55605a';g.beginPath();g.arc(x,y,4,0,7);g.fill();g.fillStyle=col;g.beginPath();g.arc(x-1.2,y-1.2,1.6,0,7);g.fill()}}
function scratches(g,x,y,w,h,n,seed,a=.18){const R=rng(seed);g.lineWidth=1;for(let i=0;i<n;i++){const sx=x+R()*w,sy=y+R()*h,l=10+R()*80,an=R()*Math.PI;
  g.strokeStyle=`rgba(230,230,220,${R()*a})`;g.beginPath();g.moveTo(sx,sy);g.lineTo(sx+Math.cos(an)*l,sy+Math.sin(an)*l*.3);g.stroke()}}
function cable(g,pts,w,col,hl){g.lineCap='round';g.lineJoin='round';g.strokeStyle=col;g.lineWidth=w;g.beginPath();g.moveTo(pts[0][0],pts[0][1]);for(let i=1;i<pts.length;i++)g.lineTo(pts[i][0],pts[i][1]);g.stroke();
  g.strokeStyle=hl;g.lineWidth=w*.25;g.beginPath();g.moveTo(pts[0][0],pts[0][1]-w*.25);for(let i=1;i<pts.length;i++)g.lineTo(pts[i][0],pts[i][1]-w*.25);g.stroke()}
let CAM=null;// optional camera override for reused shots
function camTo(g,z,ax,ay,dx=0,dy=0){if(CAM){z*=CAM.z||1;ax=CAM.ax??ax;ay=CAM.ay??ay;dx+=CAM.dx||0;dy+=CAM.dy||0}g.setTransform(z,0,0,z,ax-ax*z+dx,ay-ay*z+dy)}
function flash(t,at,col='255,230,190',dur=.14,a=.7){const k=seg(t,at,at+dur);if(t>=at&&k<1){ctx.setTransform(1,0,0,1,0,0);ctx.fillStyle=`rgba(${col},${a*(1-k)})`;ctx.fillRect(0,0,W,H)}}
function glitch(t,a,b,amt=1){if(t<a||t>b)return;const R=rng(Math.floor(t*60));ctx.setTransform(1,0,0,1,0,0);
  const snap=mk(W,H),sg=snap.getContext('2d');sg.drawImage(cv,0,0);
  for(let i=0;i<14*amt;i++){const y=R()*H,h=10+R()*120,dx=(R()-.5)*160*amt;ctx.drawImage(snap,0,y,W,h,dx,y,W,h)}
  ctx.globalCompositeOperation='lighter';ctx.globalAlpha=.35*amt;ctx.drawImage(snap,10*amt,0);ctx.globalCompositeOperation='source-over';ctx.globalAlpha=1;
  ctx.fillStyle='rgba(0,0,0,.25)';for(let y=0;y<H;y+=6)ctx.fillRect(0,y,W,2)}
function ledHud(txt,dot=7){// top-right LED plate in safe zone
  ctx.setTransform(1,0,0,1,0,0);const x=560,y=278,w=350,h=74;ctx.fillStyle='rgba(8,8,8,.82)';ctx.fillRect(x,y,w,h);ctx.strokeStyle='rgba(255,150,40,.35)';ctx.lineWidth=2;ctx.strokeRect(x,y,w,h);
  ledText(ctx,txt,x+w/2,y+12,3.0,{align:'center',font:'bold 13px '+MONO})}

// =====================================================================
// A — cold open: Sonya above the black tunnel, doors forced (0.0–3.0)
// =====================================================================
const DX0=230,DX1=850,DY0=330,DY1=1290;// door opening
const A_BG=mk();{const g=A_BG.getContext('2d'),R=rng(1);
  g.fillStyle='#060807';g.fillRect(0,0,W,H);
  // tunnel vault + cables
  let gr=g.createLinearGradient(0,0,0,220);gr.addColorStop(0,'#0b0f0d');gr.addColorStop(1,'#151b18');g.fillStyle=gr;g.fillRect(0,0,W,230);
  texFill(g,0,0,W,230,'#141a17',3,{grime:.9});
  for(let k=0;k<5;k++)cable(g,[[-20,60+k*22],[300,70+k*22+R()*6],[700,64+k*22],[1100,75+k*22]],10+k%2*4,['#0c0c0c','#151515','#1b1a17'][k%3],'rgba(255,200,140,.10)');
  for(let x=60;x<W;x+=240){g.fillStyle='#262b28';g.fillRect(x,40,14,130);g.fillStyle='rgba(255,200,150,.12)';g.fillRect(x,40,3,130)}
  // car body
  gr=g.createLinearGradient(0,170,0,1300);gr.addColorStop(0,'#2b3832');gr.addColorStop(.5,'#34443c');gr.addColorStop(1,'#1f2924');
  g.fillStyle=gr;g.fillRect(-20,170,W+40,1140);texFill(g,-20,170,W+40,1140,'rgba(0,0,0,0)',11,{grime:.9,specks:.7,streaks:60});
  for(let y=200;y<1300;y+=46){g.fillStyle='rgba(0,0,0,.28)';g.fillRect(0,y,W,3);g.fillStyle='rgba(255,230,190,.05)';g.fillRect(0,y+3,W,2)}
  g.fillStyle='rgba(220,40,30,.55)';g.fillRect(0,1150,DX0-40,26);g.fillRect(DX1+40,1150,W,26);// red band
  rivets(g,20,DX0-60,300,46);rivets(g,DX1+60,W,300,46);rivets(g,20,DX0-60,1110,46);rivets(g,DX1+60,W,1110,46);
  scratches(g,0,170,W,1100,500,4,.2);
  // side windows with amber interior
  for(const [x0,x1] of [[-30,DX0-70],[DX1+70,W+30]]){g.fillStyle='#0d0f0e';g.fillRect(x0-10,370,x1-x0+20,380);
    gr=g.createLinearGradient(0,380,0,740);gr.addColorStop(0,'#6a3d14');gr.addColorStop(1,'#1d120a');g.fillStyle=gr;g.fillRect(x0,380,x1-x0,360);
    g.fillStyle='rgba(255,170,70,.35)';g.fillRect(x0,384,x1-x0,10);
    g.strokeStyle='rgba(255,255,255,.12)';g.lineWidth=3;g.beginPath();g.moveTo(x0+30,740);g.lineTo(x0+150,380);g.stroke();
    g.fillStyle='rgba(10,10,10,.8)';g.fillRect((x0+x1)/2-30,560,60,180)}// silhouette in window
  // number stencil
  g.font='bold 54px '+MONO;g.fillStyle='rgba(235,230,215,.75)';g.fillText('0473',DX1+110,1080);
  // door frame + leaves pushed aside
  g.fillStyle='#0b0d0c';g.fillRect(DX0-90,DY0-30,90,DY1-DY0+30);g.fillRect(DX1,DY0-30,90,DY1-DY0+30);
  for(const [x,w] of [[DX0-80,70],[DX1+10,70]]){texFill(g,x,DY0-20,w,DY1-DY0+10,'#3a4842',x,{grime:.7});g.fillStyle='#090a0a';g.fillRect(x+12,DY0+60,w-24,300);g.fillStyle='rgba(255,160,60,.18)';g.fillRect(x+12,DY0+60,w-24,300)}
  g.fillStyle='#050505';g.fillRect(DX0-12,DY0,12,DY1-DY0);g.fillRect(DX1,DY0,12,DY1-DY0);// rubber seals
  g.fillStyle='#5b6660';g.fillRect(DX0-6,DY0-36,DX1-DX0+12,22);g.fillStyle='rgba(255,220,170,.4)';g.fillRect(DX0-6,DY0-36,DX1-DX0+12,3);
  // interior through the door
  gr=g.createRadialGradient(540,DY0+60,40,540,DY0+300,900);gr.addColorStop(0,'#ffb24a');gr.addColorStop(.3,'#a05a1c');gr.addColorStop(.75,'#2a170b');gr.addColorStop(1,'#120a05');
  g.fillStyle=gr;g.fillRect(DX0,DY0,DX1-DX0,DY1-DY0);
  g.fillStyle='rgba(30,18,10,.85)';g.fillRect(DX0,DY0+420,120,260);g.fillRect(DX1-140,DY0+430,140,250);// seats
  gr=g.createLinearGradient(DX1-110,0,DX1-80,0);gr.addColorStop(0,'#3a3a36');gr.addColorStop(.4,'#e8d2b0');gr.addColorStop(1,'#2a2a28');g.fillStyle=gr;g.fillRect(DX1-110,DY0,26,DY1-DY0);// pole
  g.fillStyle='#ffd27a';g.fillRect(DX0+60,DY0+8,DX1-DX0-120,14);// lamp strip
  // floor/sill
  g.fillStyle='#4a4f4a';g.fillRect(DX0-20,DY1-8,DX1-DX0+40,22);g.fillStyle='rgba(255,190,110,.6)';g.fillRect(DX0-20,DY1-8,DX1-DX0+40,4);
  // undercarriage
  g.fillStyle='#070808';g.fillRect(0,1300,W,150);for(let i=0;i<7;i++){g.fillStyle=['#121413','#0e100f','#161816'][i%3];g.fillRect(40+i*150+R()*30,1320,90+R()*40,60+R()*50)}
  cable(g,[[0,1330],[400,1350],[1080,1325]],8,'#0a0a0a','rgba(255,170,90,.08)');
  // track bed: concrete + rails + ballast
  gr=g.createLinearGradient(0,1440,0,H);gr.addColorStop(0,'#0e100e');gr.addColorStop(1,'#1a1c19');g.fillStyle=gr;g.fillRect(0,1440,W,480);
  texFill(g,0,1440,W,480,'rgba(0,0,0,0)',21,{grime:.9,specks:1});
  for(let i=0;i<600;i++){const x=R()*W,y=1460+R()*460,s=4+R()*12;{const v=50+R()*70;g.fillStyle=`rgba(${v},${v*.97},${v*.9},${.25+R()*.4})`};g.beginPath();g.ellipse(x,y,s,s*.6,R()*3,0,7);g.fill()}
  for(const [y0,y1] of [[1560,1500],[1840,1760]]){g.fillStyle='#232523';g.beginPath();g.moveTo(0,y0);g.lineTo(W,y1);g.lineTo(W,y1+26);g.lineTo(0,y0+30);g.fill();
    g.strokeStyle='rgba(255,180,90,.55)';g.lineWidth=4;g.beginPath();g.moveTo(0,y0+2);g.lineTo(W,y1+2);g.stroke()}
  // puddle
  g.save();g.beginPath();g.ellipse(380,1700,330,60,-.05,0,7);g.clip();g.fillStyle='#0a0b0a';g.fillRect(0,1600,W,200);
  gr=g.createLinearGradient(0,1640,0,1760);gr.addColorStop(0,'rgba(255,160,60,.45)');gr.addColorStop(1,'rgba(255,160,60,0)');g.fillStyle=gr;g.fillRect(DX0,1640,DX1-DX0,120);g.restore()}

function sceneA(t){const lt=t;const z=1+.07*easeOut(lt/3),dx=Math.sin(lt*.9)*6;
  camTo(ctx,z,540,820,dx,0);ctx.drawImage(A_BG,0,0);
  // interior smoke behind her
  smoke(ctx,t,DX0,DY0,DX1-DX0,260,{alpha:.4,scale:1.3,vx:-25,vy:-35,sheet:0});
  const g=ctx;g.save();g.globalCompositeOperation='lighter';glow(g,540,DY0+40,520,'255,150,50',.35+.05*Math.sin(t*7));g.restore();
  // legs
  g.save();g.beginPath();g.rect(DX0,DY0,DX1-DX0,DY1-DY0);g.clip();
  for(const s of[-1,1]){g.beginPath();g.moveTo(540+s*10,1080);g.lineTo(540+s*110,1080);g.lineTo(540+s*92,DY1);g.lineTo(540+s*24,DY1);g.closePath();
    const gr=g.createLinearGradient(540+s*95,0,540,0);gr.addColorStop(0,'#2a3540');gr.addColorStop(1,'#0c1014');g.fillStyle=gr;g.fill()}
  g.fillStyle='#d8d4c8';for(const s of[-1,1])g.fillRect(540+s*22-(s<0?72:0),DY1-28,72,26);// sneakers
  drawSonya(g,540,560,250,{v:SV,t,dark:.45,rim:.55,fill:.3,look:[.1,.9],open:lt>1.9&&lt<2.05?.1:.85,breath:Math.sin(t*2.4)});
  {const hx=DX1-6,hy=860;g.fillStyle='#6a4536';g.beginPath();g.ellipse(hx-14,hy,26,40,.2,0,7);g.fill();g.fillStyle='rgba(255,160,70,.5)';for(let i=0;i<4;i++){g.beginPath();g.ellipse(hx+2,hy-24+i*16,10,7,0,0,7);g.fill()}}
  g.restore();
  // smoke pouring out of the door into the tunnel
  smokeMasked(ctx,t*1.2,0,0,W,1300,{alpha:.7,scale:1.8,vx:-60,vy:-40,sheet:1},lg=>{const gr=lg.createLinearGradient(0,0,0,DY0+60);gr.addColorStop(0,'rgba(0,0,0,.9)');gr.addColorStop(1,'rgba(0,0,0,0)');lg.fillStyle=gr;lg.fillRect(0,0,W,DY0+60);const g2=lg.createLinearGradient(0,0,DX0,0);g2.addColorStop(0,'rgba(0,0,0,.6)');g2.addColorStop(1,'rgba(0,0,0,0)');lg.fillStyle=g2;lg.fillRect(0,0,DX0,1300)});
  g.save();g.globalCompositeOperation='lighter';glow(g,540,DY0+20,300,'255,170,80',.18);g.restore();
  dust(ctx,t,'255,190,120',.6,g2=>{g2.beginPath();g2.rect(0,0,W,DY0);g2.rect(0,DY0,DX0,1000);g2.rect(DX1,DY0,W-DX1,1000)});
  finish(t,{vig:.8});ledHud('СТОИМ 07:12');
}

// =====================================================================
// B — LED display: rewind to 00:47 (3.0–4.6)
// =====================================================================
const B_BG=mk();{const g=B_BG.getContext('2d'),R=rng(2);
  texFill(g,0,0,W,H,'#151715',8,{grime:.7,specks:.8});
  g.fillStyle='#050505';g.fillRect(70,560,940,560);g.strokeStyle='#2b2e2c';g.lineWidth=18;g.strokeRect(61,551,958,578);
  for(const [x,y] of [[95,585],[985,585],[95,1095],[985,1095]]){g.fillStyle='#3a3d3a';g.beginPath();g.arc(x,y,12,0,7);g.fill();g.strokeStyle='#111';g.lineWidth=3;g.beginPath();g.moveTo(x-8,y);g.lineTo(x+8,y);g.stroke()}
  scratches(g,70,560,940,560,140,9,.12);
  g.font='bold 34px '+MONO;g.fillStyle='rgba(220,215,200,.55)';g.fillText('ВАГОН № 0473',90,1200);
  g.fillStyle='rgba(220,40,30,.7)';g.fillRect(90,1230,300,10)}
const DROPS=[];{const R=rng(12);for(let i=0;i<70;i++)DROPS.push({x:80+R()*920,y:570+R()*540,r:3+R()*R()*16})}
function sceneB(t){const lt=t-3;const z=1.12-.06*easeOut(lt/1.6);camTo(ctx,z,540,840,Math.sin(lt*2)*4,0);
  ctx.drawImage(B_BG,0,0);const L=layer();
  if(lt<.8){const sec=Math.round(432*(1-easeIn(lt/.8)));const mm=String(Math.floor(sec/60)).padStart(2,'0'),ss=String(sec%60).padStart(2,'0');
    ledText(L,'СТОИМ',540,640,11,{align:'center'});ledText(L,mm+':'+ss,540,840,18,{align:'center',font:'bold 14px '+MONO})}
  else{ledText(L,'00:47',540,700,20,{align:'center',font:'bold 14px '+MONO});
    const sc=((lt-.8)*120)%700;L.save();L.beginPath();L.rect(90,960,900,130);L.clip();ledText(L,'ЗАРЕЧНАЯ — ПАРКОВАЯ',1000-sc*1.6,975,7);L.restore()}
  ctx.drawImage(TMP,0,0);ctx.save();ctx.globalCompositeOperation='lighter';ctx.filter='blur(14px)';ctx.globalAlpha=.8;ctx.drawImage(TMP,0,0);ctx.restore();
  for(const d of DROPS){ctx.fillStyle='rgba(255,200,140,.10)';ctx.beginPath();ctx.arc(d.x,d.y,d.r,0,7);ctx.fill();ctx.fillStyle='rgba(255,230,200,.5)';ctx.beginPath();ctx.arc(d.x-d.r*.35,d.y-d.r*.35,d.r*.25,0,7);ctx.fill()}
  ctx.save();ctx.globalCompositeOperation='lighter';glow(ctx,540,840,700,'255,140,40',.12);ctx.restore();
  finish(t,{vig:.8});
}

// =====================================================================
// C — wheel macro: sparks die, train stops (4.6–6.0)
// =====================================================================
const WCX=700,WCY=740,WR=700;
const C_BG=mk(),WHEEL=mk(1400,1400);
{const g=C_BG.getContext('2d'),R=rng(3);g.fillStyle='#070807';g.fillRect(0,0,W,H);
  glow(g,200,500,900,'255,140,50',.12);texFill(g,0,0,W,1100,'rgba(0,0,0,0)',5,{grime:.8});
  for(let k=0;k<4;k++)cable(g,[[-10,200+k*30],[1100,170+k*30]],12,'#0c0c0c','rgba(255,170,90,.08)');
  // sleepers + ballast + rail
  for(let i=0;i<900;i++){const x=R()*W,y=1460+R()*460,s=6+R()*16;{const v=45+R()*70;g.fillStyle=`rgba(${v},${v*.96},${v*.9},${.35+R()*.4})`};g.beginPath();g.ellipse(x,y,s,s*.6,R()*3,0,7);g.fill()}
  g.fillStyle='#1b1a18';g.fillRect(0,1500,W,70);texFill(g,0,1500,W,70,'rgba(0,0,0,0)',6,{grime:1});
  let gr=g.createLinearGradient(0,1430,0,1500);gr.addColorStop(0,'#b9a48a');gr.addColorStop(.15,'#6b5e50');gr.addColorStop(1,'#2a2622');g.fillStyle=gr;g.fillRect(0,1440,W,62);
  texFill(g,0,1455,W,45,'rgba(0,0,0,0)',7,{grime:.6,streaks:30});
  for(let x=60;x<W;x+=300){g.fillStyle='#2e2a26';g.fillRect(x,1500,60,40);g.fillStyle='rgba(255,200,150,.25)';g.fillRect(x+8,1504,10,10)}
  // puddle
  g.save();g.beginPath();g.ellipse(260,1760,300,70,0,0,7);g.clip();g.fillStyle='#050505';g.fillRect(0,1650,W,240);g.restore()}
{const g=WHEEL.getContext('2d'),c=700,R=rng(4);
  let gr=g.createRadialGradient(c-120,c-160,60,c,c,WR);gr.addColorStop(0,'#4a4f4c');gr.addColorStop(.7,'#262927');gr.addColorStop(1,'#151716');
  g.fillStyle='#0c0d0d';g.beginPath();g.arc(c,c,WR,0,7);g.fill();// flange
  g.fillStyle=gr;g.beginPath();g.arc(c,c,WR-34,0,7);g.fill();
  g.save();g.beginPath();g.arc(c,c,WR-34,0,7);g.clip();texFill(g,0,0,1400,1400,'rgba(0,0,0,0)',13,{grime:.9,streaks:80});g.restore();
  g.strokeStyle='#8f8a82';g.lineWidth=26;g.beginPath();g.arc(c,c,WR-52,0,7);g.stroke();// tread
  g.strokeStyle='rgba(255,240,220,.35)';g.lineWidth=4;g.beginPath();g.arc(c,c,WR-44,0,7);g.stroke();
  for(let a=0;a<7;a+=.02){g.strokeStyle=`rgba(255,255,255,${R()*.1})`;g.lineWidth=1;g.beginPath();g.arc(c,c,WR-64+R()*24,a,a+.05);g.stroke()}
  g.fillStyle='#1d201e';g.beginPath();g.arc(c,c,240,0,7);g.fill();g.strokeStyle='#3c403d';g.lineWidth=10;g.stroke();
  for(let i=0;i<8;i++){const a=i/8*Math.PI*2,x=c+Math.cos(a)*180,y=c+Math.sin(a)*180;g.fillStyle='#4b4f4c';g.beginPath();g.arc(x,y,22,0,7);g.fill();g.fillStyle='rgba(255,230,200,.3)';g.beginPath();g.arc(x-6,y-6,7,0,7);g.fill()}
  for(let i=0;i<5;i++){const a=i/5*Math.PI*2+.3;g.fillStyle='#0a0b0a';g.beginPath();g.ellipse(c+Math.cos(a)*420,c+Math.sin(a)*420,70,48,a,0,7);g.fill()}
  g.save();g.translate(c+300,c+80);g.rotate(.4);g.font='bold 60px '+MONO;g.fillStyle='rgba(240,235,220,.7)';g.fillText('Э-47',0,0);g.restore();
  g.fillStyle='rgba(255,255,240,.85)';g.fillRect(c-6,c-WR+40,12,90)}// chalk mark (shows rotation)
function wheelAngle(lt){const T=.75;const p=clamp(lt/T,0,1);return 2.2*(T*p-T*p*p/2)*Math.PI}// decelerating
function sceneC(t){const lt=t-4.6,stop=.75;const shake=lt>stop?Math.exp(-(lt-stop)*7)*18*Math.sin(lt*60):0;
  camTo(ctx,1.2+.04*lt/1.4,540,1300,shake,shake*.4-120);ctx.drawImage(C_BG,0,0);
  ctx.save();ctx.translate(WCX,WCY);ctx.rotate(-wheelAngle(lt));ctx.drawImage(WHEEL,-700,-700);ctx.restore();
  const pr=1-clamp(lt/stop,0,1);// spark intensity
  const g=ctx;g.save();g.globalCompositeOperation='lighter';
  glow(g,WCX-20,1440,260*pr+40,'255,170,60',.7*pr+.05);
  const R=rng(Math.floor(lt*30)+1);
  for(let i=0;i<220*pr;i++){const age=R()*.35,a=Math.PI+.15+R()*.55,v=900+R()*900,x=WCX-30+Math.cos(a)*v*age,y=1440-Math.sin(a)*v*age*.7+600*age*age;
    const l=20+R()*40;g.strokeStyle=`rgba(255,${180+R()*60},${80+R()*60},${(1-age/.35)})`;g.lineWidth=1.5+R()*2.5;g.beginPath();g.moveTo(x,y);g.lineTo(x-Math.cos(a)*l,y+Math.sin(a)*l*.7);g.stroke()}
  // reflection in puddle
  glow(g,260,1760,220*pr+30,'255,150,60',.4*pr);g.restore();
  if(lt>stop)smoke(ctx,lt,300,1250,800,400,{alpha:.25*Math.min(1,(lt-stop)*3),scale:1,vx:-20,vy:-40,sheet:2});
  finish(t,{vig:.85});
}

// =====================================================================
// D — car interior: light dies, amber emergency (6.0–8.0)
// =====================================================================
const VPX=540,VPY=860;
const D_IN=mk();{const g=D_IN.getContext('2d'),R=rng(6);
  const P=(x,y,k)=>[VPX+(x-VPX)*k,VPY+(y-VPY)*k];
  g.fillStyle='#9fa9a4';g.fillRect(0,0,W,H);
  // ceiling
  let gr=g.createLinearGradient(0,0,0,VPY);gr.addColorStop(0,'#d9dfda');gr.addColorStop(1,'#8c9690');g.fillStyle=gr;g.beginPath();g.moveTo(0,0);g.lineTo(W,0);g.lineTo(...P(W,0,.22));g.lineTo(...P(0,0,.22));g.fill();
  // floor
  gr=g.createLinearGradient(0,VPY,0,H);gr.addColorStop(0,'#5d5a52');gr.addColorStop(1,'#34322d');g.fillStyle=gr;g.beginPath();g.moveTo(0,H);g.lineTo(W,H);g.lineTo(...P(W,H,.22));g.lineTo(...P(0,H,.22));g.fill();
  texFill(g,0,1100,W,820,'rgba(0,0,0,0)',30,{grime:.8});
  // side walls
  for(const s of[0,1]){const x=s?W:0;gr=g.createLinearGradient(x,0,VPX,0);gr.addColorStop(0,'#b7c2bb');gr.addColorStop(1,'#7c8781');g.fillStyle=gr;
    g.beginPath();g.moveTo(x,0);g.lineTo(...P(x,0,.22));g.lineTo(...P(x,H,.22));g.lineTo(x,H);g.fill();
    // windows
    for(let i=0;i<4;i++){const k0=1-i*.2,k1=k0-.13;g.fillStyle='#0b0f0e';g.beginPath();g.moveTo(...P(x,330,k0));g.lineTo(...P(x,330,k1));g.lineTo(...P(x,760,k1));g.lineTo(...P(x,760,k0));g.fill();
      g.strokeStyle='rgba(255,255,255,.12)';g.lineWidth=3;g.beginPath();g.moveTo(...P(x,700,k0-.02));g.lineTo(...P(x,380,k1+.03));g.stroke()}
    // bench
    gr=g.createLinearGradient(0,1100,0,1300);gr.addColorStop(0,'#5a7186');gr.addColorStop(1,'#2a3846');g.fillStyle=gr;
    g.beginPath();g.moveTo(...P(x,1080,1));g.lineTo(...P(x,1080,.3));g.lineTo(...P(x,1330,.3));g.lineTo(...P(x,1330,1));g.fill();
    g.fillStyle='#2b3138';g.beginPath();g.moveTo(...P(x,1330,1));g.lineTo(...P(x,1330,.3));g.lineTo(...P(x,1500,.3));g.lineTo(...P(x,1500,1));g.fill()}
  // far end wall + door
  const [ax,ay]=P(0,0,.22),[bx,by]=P(W,H,.22);g.fillStyle='#8a948e';g.fillRect(ax,ay,bx-ax,by-ay);g.fillStyle='#101413';g.fillRect(ax+70,ay+80,bx-ax-140,(by-ay)*.45);
  g.fillStyle='#6d7772';g.fillRect(ax+40,ay+40,bx-ax-80,by-ay-40);g.fillStyle='#0d1110';g.fillRect(ax+80,ay+80,bx-ax-160,(by-ay)*.38);
  // poles
  for(const [x,k] of [[300,1],[780,1],[300,.6],[780,.6],[300,.4],[780,.4]]){const [px,py]=P(x,0,k),[qx,qy]=P(x,H,k);gr=g.createLinearGradient(px-10*k,0,px+10*k,0);gr.addColorStop(0,'#6b6e6c');gr.addColorStop(.4,'#f2efe6');gr.addColorStop(1,'#4d504e');g.fillStyle=gr;g.fillRect(px-11*k,py,22*k,qy-py)}
  // lamp strips
  for(const x of[330,750]){g.strokeStyle='#f6fbf7';g.lineWidth=18;g.beginPath();g.moveTo(...P(x,0,1.2));g.lineTo(...P(x,0,.24));g.stroke()}
  // passengers (muted colours)
  const man=(x,y,s,col)=>{g.fillStyle=col;g.beginPath();g.ellipse(x,y,26*s,32*s,0,0,7);g.fill();g.beginPath();g.moveTo(x-60*s,y+40*s);g.quadraticCurveTo(x,y+20*s,x+60*s,y+40*s);g.lineTo(x+70*s,y+260*s);g.lineTo(x-70*s,y+260*s);g.fill()};
  man(330,1000,1.0,'#4b3f36');g.strokeStyle='#2a221c';g.lineWidth=8;g.beginPath();g.moveTo(390,1100);g.lineTo(420,1330);g.stroke();// old man + cane
  man(700,900,1.25,'#24282c');g.fillStyle='#24282c';g.beginPath();g.ellipse(700,880,44,52,0,Math.PI,0);g.fill();// hooded guy
  man(560,880,.6,'#2e4058');g.fillStyle='#1d2a3a';g.fillRect(538,846,44,10);// woman in uniform (cap)
  texFill(g,0,0,W,H,'rgba(0,0,0,0)',31,{grime:.35,specks:.4});}
function sceneD(t){const lt=t-6;const off=.55,fl=lt>=off-.12&&lt<off+.18?((Math.floor(lt*40)%3)?1:0):(lt<off?1:0);
  const L=lt<off-.12?1:(lt<off+.18?fl:0),E=easeOut(seg(lt,off+.2,off+.6));
  const shake=lt>off&&lt<off+.4?Math.sin(lt*70)*6*(1-(lt-off)/.4):0;
  camTo(ctx,1+.05*lt/2,540,860,shake,0);ctx.drawImage(D_IN,0,0);
  if(L<1){ctx.fillStyle=`rgba(4,5,6,${.9*(1-L)})`;ctx.fillRect(0,0,W,H)}
  if(L>0){ctx.save();ctx.globalCompositeOperation='lighter';for(const x of[330,750])glow(ctx,x,120,420,'210,240,230',.12*L);ctx.restore()}
  if(E>0){ctx.save();ctx.globalCompositeOperation='lighter';
    for(const [x,y,r] of [[260,250,520],[820,250,520],[540,700,260]]){glow(ctx,x,y,r,'255,140,40',.4*E*(.9+.1*Math.sin(t*9+x)));ctx.fillStyle=`rgba(255,190,90,${E})`;ctx.fillRect(x-24,y-8,48,16)}
    ctx.restore();smoke(ctx,t,0,0,W,900,{alpha:.18*E,scale:1.4,vx:-15,vy:8,sheet:1})}
  // phone glow on hooded guy
  ctx.save();ctx.globalCompositeOperation='lighter';glow(ctx,720,960,160,'150,200,255',.5);ctx.fillStyle='rgba(220,240,255,.9)';ctx.fillRect(730,950,22,36);ctx.restore();
  // Sonya foreground (back of head, yellow headphones)
  ctx.save();ctx.translate(0,0);ctx.fillStyle='#0b0c0d';ctx.beginPath();ctx.ellipse(880,1560,190,230,0,0,7);ctx.fill();ctx.beginPath();ctx.moveTo(620,1920);ctx.quadraticCurveTo(700,1700,880,1720);ctx.quadraticCurveTo(1060,1700,1120,1920);ctx.fill();
  const hg=ctx.createLinearGradient(0,1700,0,1820);hg.addColorStop(0,'#ffe25a');hg.addColorStop(1,'#a87a08');ctx.fillStyle=hg;ctx.beginPath();ctx.ellipse(720,1770,60,72,-.4,0,7);ctx.fill();
  ctx.fillStyle='rgba(255,255,230,.5)';ctx.beginPath();ctx.ellipse(700,1745,15,26,-.4,0,7);ctx.fill();ctx.restore();
  finish(t,{vig:.85});
}

// =====================================================================
// E — smoke seeping from the gap above the inter-car door (8.0–10.0)
// =====================================================================
const E_BG=mk();{const g=E_BG.getContext('2d'),R=rng(7);
  texFill(g,0,0,W,H,'#4a5650',14,{grime:1,specks:.8,streaks:40});
  for(let y=80;y<H;y+=120){g.fillStyle='rgba(0,0,0,.25)';g.fillRect(0,y,W,3)}
  scratches(g,0,0,W,H,700,15,.22);
  // gap / grille
  g.fillStyle='#050606';g.fillRect(250,560,580,70);for(let x=262;x<820;x+=22){g.fillStyle='#2a302d';g.fillRect(x,566,8,58)}
  // door
  texFill(g,250,660,580,1300,'#56625c',16,{grime:.8,specks:.8});g.strokeStyle='#1a1e1c';g.lineWidth=14;g.strokeRect(250,660,580,1300);
  g.fillStyle='#070908';g.fillRect(330,740,420,520);g.fillStyle='rgba(255,255,255,.07)';g.beginPath();g.moveTo(330,1100);g.lineTo(560,740);g.lineTo(620,740);g.lineTo(390,1260);g.lineTo(330,1260);g.fill();
  g.fillStyle='#8c8f8a';g.fillRect(760,1300,40,140);
  // warning sticker
  g.save();g.translate(410,1160);g.fillStyle='#e8c21a';g.fillRect(0,0,260,120);g.fillStyle='#111';g.font='bold 24px '+MONO;g.fillText('НЕ',18,50);g.fillText('ПРИСЛОНЯТЬСЯ',18,90);
  g.beginPath();g.moveTo(200,20);g.lineTo(240,90);g.lineTo(160,90);g.closePath();g.fill();g.fillStyle='#e8c21a';g.fillRect(197,45,6,26);g.fillRect(197,76,6,6);g.restore();
  // car number plate
  g.fillStyle='#16263d';g.fillRect(60,400,220,90);g.strokeStyle='#cfd3d6';g.lineWidth=3;g.strokeRect(66,406,208,78);g.font='bold 44px '+MONO;g.fillStyle='#e9ecef';g.fillText('№0473',80,462);
  // emergency lamp housing
  g.fillStyle='#202322';g.fillRect(120,250,140,60);rivets(g,60,1020,200,80)}
function sceneE(t){const lt=t-8;const z=1.05+.1*easeOut(lt/2);camTo(ctx,z,540,600,0,easeOut(lt/2)*60);
  ctx.drawImage(E_BG,0,0);const g=ctx;
  const fl=.85+.15*Math.sin(t*13)*Math.sin(t*5.3);
  g.save();g.globalCompositeOperation='lighter';glow(g,190,280,700,'255,140,40',.45*fl);g.fillStyle=`rgba(255,200,110,${fl})`;g.fillRect(130,262,120,36);g.restore();
  const grow=.35+.65*easeOut(lt/2);
  smokeMasked(ctx,t*1.4,0,0,W,800,{alpha:.85,scale:1.1,vx:-40,vy:-60,sheet:2},lg=>{const gr=lg.createRadialGradient(540,600,20,540,520,620*grow);gr.addColorStop(0,'#000');gr.addColorStop(.6,'rgba(0,0,0,.6)');gr.addColorStop(1,'rgba(0,0,0,0)');lg.fillStyle=gr;lg.fillRect(0,0,W,H)});
  // wisps from the slot
  g.save();g.lineCap='round';for(let i=0;i<9;i++){const x=290+i*60,ph=t*1.5+i;g.strokeStyle=`rgba(200,185,160,${.08})`;g.lineWidth=30+i%3*14;g.filter='blur(14px)';g.beginPath();g.moveTo(x,600);
    g.bezierCurveTo(x+Math.sin(ph)*40,520,x+Math.cos(ph)*60,430-lt*40,x+Math.sin(ph*.7)*90-40,330-lt*60);g.stroke()}g.restore();
  g.save();g.globalCompositeOperation='lighter';glow(g,190,280,380,'255,150,60',.15*fl);g.restore();
  finish(t,{vig:.85});
}

// =====================================================================
// F — the eye, red lamp in the pupil, logo (10.0–14.0)
// =====================================================================
const F_SKIN=mk();{const g=F_SKIN.getContext('2d');
  let gr=g.createLinearGradient(0,0,W,H);gr.addColorStop(0,'#b47a5f');gr.addColorStop(.6,'#7d4c3c');gr.addColorStop(1,'#3a2019');g.fillStyle=gr;g.fillRect(0,0,W,H);
  const f=noiseField(540,960,55,40,4,.6);g.globalAlpha=.35;g.drawImage(fieldCanvas(540,960,f,v=>[v*255,v*190,v*160,255]),0,0,W,H);g.globalAlpha=.5;g.drawImage(SPECK,0,0);g.globalAlpha=1;
  // soot smear
  g.save();g.filter='blur(18px)';g.fillStyle='rgba(25,22,20,.45)';g.beginPath();g.ellipse(820,1380,260,90,-.3,0,7);g.fill();g.restore();
  // brow
  const R=rng(5);for(let i=0;i<500;i++){const k=R(),x=120+k*860,y=380-Math.sin(k*3)*90+(R()-.5)*50;g.strokeStyle=`rgba(25,15,10,${.4+R()*.5})`;g.lineWidth=2+R()*3;g.beginPath();g.moveTo(x,y);g.lineTo(x+18+R()*20,y-12-R()*10);g.stroke()}}
function eyeMacro(g,t,open,pupil,redA){const cx=540,cy=830,ew=420;
  g.drawImage(F_SKIN,0,0);
  blob(g,cx,cy,520,300,'40,18,14',.55);// socket shadow
  g.strokeStyle='rgba(60,30,25,.6)';g.lineWidth=10;g.beginPath();g.moveTo(cx-ew,cy-40);g.quadraticCurveTo(cx,cy-360,cx+ew,cy-80);g.stroke();// crease
  const pth=()=>{g.beginPath();g.moveTo(cx-ew,cy+20);g.quadraticCurveTo(cx-40,cy-330*open,cx+ew,cy-30);g.quadraticCurveTo(cx,cy+240*open,cx-ew,cy+20);g.closePath()};
  if(open>.05){g.save();pth();g.clip();
    let gr=g.createLinearGradient(0,cy-260,0,cy+200);gr.addColorStop(0,'#8d7c72');gr.addColorStop(.45,'#ece2d8');gr.addColorStop(1,'#c4b0a6');g.fillStyle=gr;g.fillRect(0,0,W,H);
    const R=rng(8);g.strokeStyle='rgba(190,60,50,.35)';for(let i=0;i<14;i++){g.lineWidth=1+R()*2;g.beginPath();let x=R()<.5?cx-ew+20:cx+ew-20,y=cy+(R()-.5)*120;g.moveTo(x,y);for(let k=0;k<5;k++){x+=(x<cx?1:-1)*(20+R()*40);y+=(R()-.5)*30;g.lineTo(x,y)}g.stroke()}
    const ix=cx+10,iy=cy-10,ir=175;
    gr=g.createRadialGradient(ix,iy,0,ix,iy,ir);gr.addColorStop(0,'#2b2a12');gr.addColorStop(.3,'#8a7a3a');gr.addColorStop(.5,'#6a8a4a');gr.addColorStop(.8,'#4d6a3a');gr.addColorStop(.93,'#22301a');gr.addColorStop(1,'#0c100a');
    g.fillStyle=gr;g.beginPath();g.arc(ix,iy,ir,0,7);g.fill();
    for(let i=0;i<260;i++){const a=R()*7,r0=pupil+10+R()*20,r1=ir*(.6+R()*.38);g.strokeStyle=`rgba(${170+R()*60},${200+R()*50},${110+R()*50},${.12+R()*.2})`;g.lineWidth=1+R()*2;g.beginPath();g.moveTo(ix+Math.cos(a)*r0,iy+Math.sin(a)*r0);g.lineTo(ix+Math.cos(a+.05)*r1,iy+Math.sin(a+.05)*r1);g.stroke()}
    g.fillStyle='#030202';g.beginPath();g.arc(ix,iy,pupil,0,7);g.fill();
    // red lamp reflection + amber catchlight
    g.save();g.globalCompositeOperation='lighter';g.translate(ix-55,iy-60);g.rotate(-.2);g.fillStyle=`rgba(255,40,30,${redA})`;g.beginPath();g.roundRect(-34,-18,68,36,12);g.fill();
    glow(g,0,0,90,'255,40,30',.5*redA);g.restore();
    g.fillStyle='rgba(255,220,170,.9)';g.beginPath();g.ellipse(ix+70,iy-80,16,22,.4,0,7);g.fill();
    g.fillStyle='rgba(255,255,255,.18)';g.beginPath();g.ellipse(ix-20,iy+90,90,20,-.1,0,7);g.fill();
    gr=g.createLinearGradient(0,cy-300,0,cy-60);gr.addColorStop(0,'rgba(20,8,5,.85)');gr.addColorStop(1,'rgba(20,8,5,0)');g.fillStyle=gr;g.fillRect(0,0,W,cy-60);
    g.restore()}
  // lid line + lashes
  g.strokeStyle='#120806';g.lineWidth=16;g.lineCap='round';g.beginPath();g.moveTo(cx-ew,cy+20);g.quadraticCurveTo(cx-40,cy-330*open,cx+ew,cy-30);g.stroke();
  const R2=rng(9);for(let i=0;i<70;i++){const k=.15+i/70*.85,x=lerp(cx-ew,cx+ew,k),y=lerp(cy+20,cy-30,k)-330*open*2*k*(1-k)*1.0;
    g.lineWidth=3+R2()*3;g.beginPath();g.moveTo(x,y);g.quadraticCurveTo(x+30+k*40,y-60-R2()*30,x+60+k*90,y-90-R2()*40);g.stroke()}
  g.strokeStyle='rgba(110,50,45,.7)';g.lineWidth=6;g.beginPath();g.moveTo(cx-ew+10,cy+24);g.quadraticCurveTo(cx,cy+240*Math.max(open,.15),cx+ew,cy-26);g.stroke();
  for(let i=0;i<30;i++){const k=.3+i/30*.7,x=lerp(cx-ew,cx+ew,k),y=cy+(240*Math.max(open,.15))*2*k*(1-k)*.98;g.strokeStyle='rgba(30,15,10,.6)';g.lineWidth=2;g.beginPath();g.moveTo(x,y);g.lineTo(x+10,y+26);g.stroke()}
  // sweat drop
  g.fillStyle='rgba(255,230,210,.25)';g.beginPath();g.ellipse(170,1150,14,22,0,0,7);g.fill();g.fillStyle='rgba(255,255,255,.7)';g.beginPath();g.arc(165,1142,4,0,7);g.fill()}
function sceneF(t){const lt=t-10;const z=1+.4*easeIn(clamp(lt/2.4,0,1));camTo(ctx,z,550,820,0,0);
  const bl=lt>1.0&&lt<1.28?Math.sin((lt-1.0)/.28*Math.PI):0;
  const pupil=62+18*easeOut(seg(lt,1.9,2.3));const red=.55+.45*easeOut(seg(lt,1.9,2.2));
  eyeMacro(ctx,t,1-bl*.97,pupil,red);
  finish(t,{vig:.85});
  if(lt>2.3){const k=seg(lt,2.3,2.5);ctx.setTransform(1,0,0,1,0,0);ctx.fillStyle=`rgba(150,0,0,${.55*k})`;ctx.globalCompositeOperation='multiply';ctx.fillRect(0,0,W,H);ctx.globalCompositeOperation='source-over'}
  if(lt>2.45){const k=easeOutBack(seg(lt,2.45,2.75));ctx.setTransform(1,0,0,1,0,0);ctx.fillStyle=`rgba(0,0,0,${.75*seg(lt,2.45,2.6)})`;ctx.fillRect(0,0,W,H);
    ctx.save();ctx.translate(540,860);ctx.scale(k,k);ctx.font='190px MB';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillStyle='#fff';ctx.fillText('ВЫБОР',0,0);ctx.restore();
    const q=easeOutBack(seg(lt,2.8,3.05));ctx.save();ctx.translate(540,1110);ctx.rotate(-.12*(1-q));ctx.scale(q,q);ctx.font='260px MB';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillStyle='#e0302a';ctx.fillText('?',0,0);ctx.restore();
    ctx.globalAlpha=seg(lt,3.0,3.3);ctx.font='44px MB';ctx.textAlign='center';ctx.fillStyle='#d9d2c4';ctx.fillText('ТОННЕЛЬ · СЕРИЯ 1',540,1320);ctx.globalAlpha=1}
}

// =====================================================================
const SUBS=[
 {s:.15,e:1.35,txt:'ЧЕРЕЗ СЕМЬ МИНУТ'},{s:1.35,e:2.2,txt:'СОНЯ БУДЕТ СТОЯТЬ',col:'#f2c418'},{s:2.2,e:3.0,txt:'ВОТ ЗДЕСЬ'},
 {s:3.1,e:3.75,txt:'А ПОКА —'},{s:3.75,e:4.6,txt:'00:47',col:'#f2c418'},
 {s:4.7,e:5.9,txt:'ПОЕЗД ВСТАЛ'},{s:6.1,e:7.6,txt:'СВЕТ ПОГАС'},{s:8.2,e:9.8,txt:'ПАХНЕТ ДЫМОМ'},
 {s:10.1,e:11.2,txt:'ЧТО СОНЯ СДЕЛАЕТ',col:'#fff'},{s:11.2,e:11.85,txt:'ДАЛЬШЕ —'},{s:11.85,e:12.45,txt:'РЕШАЕТЕ ВЫ',col:'#e0302a'}];
function renderFrame(t){ctx.setTransform(1,0,0,1,0,0);ctx.globalAlpha=1;ctx.globalCompositeOperation='source-over';ctx.filter='none';ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
  if(t<3)sceneA(t);else if(t<4.6)sceneB(t);else if(t<6)sceneC(t);else if(t<8)sceneD(t);else if(t<10)sceneE(t);else sceneF(t);
  ctx.setTransform(1,0,0,1,0,0);
  glitch(t,2.92,3.12,1);glitch(t,3.76,3.84,.6);flash(t,4.6);flash(t,6.0,'255,255,255',.1,.5);flash(t,8.0);flash(t,10.0,'255,200,150',.12,.5);
  subtitle(t,SUBS)}
window.ready=Promise.all([document.fonts.load('60px MB'),document.fonts.load('30px CV')]);
