// ===== full episode 1 «Остановка»: shots synced to the voice timeline (TL) =====
const PH=id=>TL.phr.find(p=>p.id===id),ps=id=>PH(id).s,pe=id=>PH(id).e;
const END=TL.end;
const envAt=t=>ENV[clamp(Math.floor(t*30),0,ENV.length-1)]||0;
// story clock on the LED: 00:47 at the hook -> 07:12 when she stands over the gap
const storyClock=t=>{const s=Math.round(lerp(47,432,ease(seg(t,9,104))));return String(Math.floor(s/60)).padStart(2,'0')+':'+String(s%60).padStart(2,'0')};

// ---------- shared painted pieces ----------
let EMB=null,LITB=null;
function emBlur(){if(!WAGON)buildWagon();if(!EMB){EMB=mk();const g=EMB.getContext('2d');g.filter='blur(18px) brightness(.75)';g.drawImage(WAGON.em,-80,-140,W+160,H+280);g.filter='none'}return EMB}
function litBlur(){if(!WAGON)buildWagon();if(!LITB){LITB=mk();const g=LITB.getContext('2d');g.filter='blur(16px) brightness(.8)';g.drawImage(WAGON.lit,-80,-140,W+160,H+280);g.filter='none'}return LITB}
function amberLight(g,x,y,r,a,t){g.save();g.globalCompositeOperation='lighter';glow(g,x,y,r,'255,140,40',a*(.92+.08*Math.sin(t*9.3)*Math.sin(t*3.1)));g.restore()}
function capsule(g,x0,y0,x1,y1,w,col){g.lineCap='round';g.strokeStyle=col;g.lineWidth=w;g.beginPath();g.moveTo(x0,y0);g.lineTo(x1,y1);g.stroke()}
// finger with shading: base -> tip, width w
function finger(g,x0,y0,x1,y1,w,skin,{nail=1,light='255,170,90'}={}){
  capsule(g,x0,y0,x1,y1,w+2,'rgba(45,20,14,.35)');capsule(g,x0,y0,x1,y1,w,skin[0]);
  const nx=-(y1-y0),ny=x1-x0,L=Math.hypot(nx,ny)||1,ox=nx/L*w*.18,oy=ny/L*w*.18;
  capsule(g,lerp(x0,x1,.1)-ox,lerp(y0,y1,.1)-oy,lerp(x0,x1,.92)-ox,lerp(y0,y1,.92)-oy,w*.35,skin[1]);
  capsule(g,lerp(x0,x1,.15)-ox*1.8,lerp(y0,y1,.15)-oy*1.8,lerp(x0,x1,.85)-ox*1.8,lerp(y0,y1,.85)-oy*1.8,w*.1,`rgba(${light},.3)`);
  {const cx=lerp(x0,x1,.55),cy=lerp(y0,y1,.55);g.strokeStyle='rgba(70,35,25,.3)';g.lineWidth=1.5;g.beginPath();g.moveTo(cx-ox*2,cy-oy*2);g.lineTo(cx+ox,cy+oy);g.stroke()}
  if(nail){const dx=x1-x0,dy=y1-y0,l=Math.hypot(dx,dy),ux=dx/l,uy=dy/l;g.save();g.translate(x1-ux*w*.3,y1-uy*w*.3);g.rotate(Math.atan2(uy,ux));
    g.fillStyle='rgba(225,185,170,.75)';g.beginPath();g.ellipse(0,0,w*.28,w*.27,0,0,7);g.fill();g.fillStyle='rgba(255,255,255,.3)';g.beginPath();g.ellipse(-w*.04,-w*.09,w*.1,w*.06,0,0,7);g.fill();g.restore()}}
const SKIN=['#b9826a','#e2b49a'],SKIN_AMB=['#7a4a36','#b77a58'],SKIN_COLD=['#6f7f90','#a9bccd'],SKIN_OLD=['#8d6552','#c39a84'];
function sleeve(g,pts,w,col,hl='rgba(255,255,255,.05)'){g.lineCap='round';g.lineJoin='round';g.strokeStyle=col;g.lineWidth=w;g.beginPath();g.moveTo(...pts[0]);for(const p of pts.slice(1))g.lineTo(...p);g.stroke();
  g.strokeStyle=hl;g.lineWidth=w*.25;g.beginPath();g.moveTo(pts[0][0]-w*.2,pts[0][1]);for(const p of pts.slice(1))g.lineTo(p[0]-w*.2,p[1]);g.stroke();
  g.strokeStyle='rgba(0,0,0,.35)';g.lineWidth=3;for(let i=0;i<5;i++){const k=.2+i*.15,a=pts[0],b=pts[pts.length-1],x=lerp(a[0],b[0],k),y=lerp(a[1],b[1],k);g.beginPath();g.moveTo(x-w*.3,y-8);g.quadraticCurveTo(x,y+10,x+w*.3,y-6);g.stroke()}}
function hudPlate(txt,{x=56,y=1610,w=968,h=0,col='255,150,40',dot=4.2}={}){}
function nameTag(t,a,name,sub,{y=360,col='#f2c418'}={}){if(t<a)return;const k=easeOutBack(seg(t,a,a+.35));ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.globalAlpha=seg(t,a,a+.2);
  ctx.translate(70,y);ctx.scale(k,k);ctx.textAlign='left';ctx.font='84px MB';const bw=Math.max(ctx.measureText(name).width,sub?300:0)+80;ctx.fillStyle='rgba(8,8,8,.72)';ctx.fillRect(0,0,bw,sub?190:120);ctx.fillStyle=col;ctx.fillRect(0,0,10,sub?190:120);
  ctx.font='84px MB';ctx.textBaseline='top';ctx.fillStyle=col;ctx.fillText(name,40,6);if(sub){ctx.font='46px MB';ctx.fillStyle='#e8e2d6';ctx.fillText(sub,44,116)}ctx.restore()}
function bigCaption(txt,x,y,size,col,k=1,{font='MB',rot=0,stroke=16}={}){ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.translate(x,y);ctx.rotate(rot);ctx.scale(k,k);ctx.font=`${size}px ${font}`;ctx.textAlign='center';ctx.textBaseline='middle';
  ctx.lineJoin='round';ctx.lineWidth=stroke;ctx.strokeStyle='rgba(0,0,0,.85)';ctx.strokeText(txt,0,0);ctx.fillStyle=col;ctx.fillText(txt,0,0);ctx.restore()}
function vignetteTop(a=.6){ctx.setTransform(1,0,0,1,0,0);const gr=ctx.createLinearGradient(0,0,0,500);gr.addColorStop(0,`rgba(0,0,0,${a})`);gr.addColorStop(1,'rgba(0,0,0,0)');ctx.fillStyle=gr;ctx.fillRect(0,0,W,500)}

// =====================================================================
// 1. Sonya close-up in the dark car (02.1–02.2, 04.1, 07.1)
// =====================================================================
function sonyaClose(u,d,t,{look=[.2,.1],lookTo=null,lookAt=0,z0=1,z1=1.08,open=.9,openTo=null,lit=0,rim=.9,ay=640}={}){
  const z=lerp(z0,z1,ease(u/d));camTo(ctx,z,540,ay,Math.sin(t*.7)*5,0);
  ctx.drawImage(lit?litBlur():emBlur(),0,0);
  // background smoke stays behind her (never over the face)
  smoke(ctx,t,0,0,W,900,{alpha:.22,scale:1.6,vx:-18,vy:-10,sheet:1});
  amberLight(ctx,120,300,800,.35,t);
  const k=lookTo?ease(seg(u,lookAt,lookAt+.6)):0;const lk=lookTo?[lerp(look[0],lookTo[0],k),lerp(look[1],lookTo[1],k)]:look;
  const op=openTo!=null?lerp(open,openTo,k):open;
  const bl=((u*1.0)%3.7>3.5)?.15:op;
  drawSonya(ctx,540,820,560,{v:SV,t,rim,fill:.55,dark:lit?0:.12,look:lk,open:bl,breath:Math.sin(t*2.2),brow:lookTo?-.012*k:0});
  dust(ctx,t,'255,190,120',.35,g2=>{g2.beginPath();g2.rect(0,0,W,380)});
  finish(t,{vig:.82})}

// =====================================================================
// 2. lit car, last train (02.3)
// =====================================================================
function wagonLitShot(u,d,t){if(!WAGON)buildWagon();camTo(ctx,1.02+.06*ease(u/d),540,760,Math.sin(t*1.1)*3,0);
  ctx.drawImage(WAGON.lit,0,0);ctx.save();ctx.globalCompositeOperation='lighter';for(const X of[-.42,.42])for(const z of[2,4,7]){const [x,y]=pj(X,CEIL-.1,z);glow(ctx,x,y,500/z,'230,245,240',.08)}ctx.restore();
  // warm "memory" grade
  ctx.setTransform(1,0,0,1,0,0);ctx.globalCompositeOperation='soft-light';ctx.fillStyle='rgba(255,170,80,.35)';ctx.fillRect(0,0,W,H);ctx.globalCompositeOperation='source-over';
  sonyaBack(ctx,t,false);
  finish(t,{vig:.7})}

// =====================================================================
// 3. route map revealed by a flashlight (02.4)
// =====================================================================
const MAP=mk();{const g=MAP.getContext('2d');
  texFill(g,0,0,W,H,'#2a2d2b',41,{grime:.8,specks:.8});
  g.fillStyle='#e9e6dc';g.fillRect(110,250,860,1240);texFill(g,110,250,860,1240,'rgba(0,0,0,0)',42,{grime:.45,specks:.5,streaks:12});
  g.strokeStyle='#8c8f8a';g.lineWidth=10;g.strokeRect(105,245,870,1250);rivets(g,140,940,280,800);rivets(g,140,940,1460,800);
  g.font='40px MB';g.fillStyle='#c33a2c';g.fillText('СХЕМА ЛИНИИ',160,340);g.fillStyle='rgba(0,0,0,.6)';g.fillRect(160,360,420,5);
  // line
  g.strokeStyle='#c33a2c';g.lineWidth=34;g.lineCap='round';g.beginPath();g.moveTo(400,450);g.lineTo(400,1390);g.stroke();
  for(const [y,name,done] of [[470,'ОЗЁРНАЯ',1],[640,'ЗАРЕЧНАЯ',1],[1200,'ПАРКОВАЯ',0],[1370,'ЛЕСНАЯ',0]]){
    g.fillStyle='#fff';g.beginPath();g.arc(400,y,30,0,7);g.fill();g.strokeStyle='#c33a2c';g.lineWidth=12;g.stroke();
    g.font='54px MB';g.fillStyle=done?'#7a7a74':'#1a1a1a';g.fillText(name,470,y+20)}
  g.font='bold 30px '+MONO;g.fillStyle='rgba(0,0,0,.45)';g.fillText('Э-47 · ВАГОН 0473',160,1460)}
function mapShot(u,d,t){const z=1.06+.05*ease(u/d);camTo(ctx,z,540,900,0,0);
  ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
  // ambient amber + moving flashlight spot
  ctx.globalAlpha=.22;ctx.drawImage(MAP,0,0);ctx.globalAlpha=1;
  const sx=lerp(420,560,ease(u/d))+Math.sin(t*1.7)*25,sy=lerp(700,1000,ease(u/d))+Math.cos(t*1.3)*30;
  const L=layer();L.drawImage(MAP,0,0);
  // train marker + distance brackets drawn onto the map layer
  const ty=920,pulse=.5+.5*Math.sin(t*8);
  L.fillStyle='#f2c418';L.beginPath();L.roundRect(370,ty-60,60,120,14);L.fill();L.strokeStyle='#111';L.lineWidth=6;L.stroke();
  L.fillStyle=`rgba(242,196,24,${.35*pulse})`;L.beginPath();L.arc(400,ty,90+30*pulse,0,7);L.fill();
  L.font='44px MB';L.fillStyle='#1a1a1a';L.fillText('ВЫ ЗДЕСЬ',470,ty+16);
  const k1=easeOut(seg(u,.5,1.6)),k2=easeOut(seg(u,1.0,2.1));
  L.strokeStyle='#1a1a1a';L.lineWidth=5;L.setLineDash([16,12]);
  L.beginPath();L.moveTo(320,ty-80);L.lineTo(320,lerp(ty-80,670,k1));L.stroke();L.beginPath();L.moveTo(320,ty+80);L.lineTo(320,lerp(ty+80,1170,k2));L.stroke();L.setLineDash([]);
  L.font='46px MB';L.fillStyle='#c33a2c';L.textAlign='right';
  L.fillText(Math.round(850*k1)+' м',304,800);L.fillText(Math.round(900*k2)+' м',304,1060);L.textAlign='left';
  // hatch = darkness
  L.globalAlpha=.18*k2;L.fillStyle='#000';for(let y=680;y<1180;y+=26){if(Math.abs(y-ty)<70)continue;L.fillRect(442,y,500,10)}L.globalAlpha=1;
  L.globalCompositeOperation='destination-in';const gr=L.createRadialGradient(sx,sy,40,sx,sy,620);gr.addColorStop(0,'#000');gr.addColorStop(.6,'rgba(0,0,0,.75)');gr.addColorStop(1,'rgba(0,0,0,0)');L.fillStyle=gr;L.fillRect(0,0,W,H);
  ctx.drawImage(TMP,0,0);
  ctx.save();ctx.globalCompositeOperation='soft-light';glow(ctx,sx,sy,500,'200,220,255',.4);ctx.restore();
  smoke(ctx,t,0,0,W,H,{alpha:.10,scale:1.8,vx:-20,vy:-14,sheet:0});
  finish(t,{vig:.85})}

// =====================================================================
// 4. phone in hand, 23 %, cracked screen (02.5)
// =====================================================================
function phoneBody(g,x,y,w,h,rot,drawScreen){g.save();g.translate(x,y);g.rotate(rot);
  g.fillStyle='rgba(0,0,0,.5)';g.filter='blur(20px)';g.beginPath();g.roundRect(-w/2+20,-h/2+30,w,h,70);g.fill();g.filter='none';
  let gr=g.createLinearGradient(-w/2,0,w/2,0);gr.addColorStop(0,'#3a3d40');gr.addColorStop(.1,'#16181a');gr.addColorStop(.9,'#0e1012');gr.addColorStop(1,'#4a4d50');
  g.fillStyle=gr;g.beginPath();g.roundRect(-w/2,-h/2,w,h,70);g.fill();
  g.fillStyle='#000';g.beginPath();g.roundRect(-w/2+14,-h/2+14,w-28,h-28,58);g.fill();
  g.save();g.beginPath();g.roundRect(-w/2+22,-h/2+22,w-44,h-44,52);g.clip();drawScreen(g,-w/2+22,-h/2+22,w-44,h-44);g.restore();
  g.fillStyle='#000';g.beginPath();g.roundRect(-60,-h/2+38,120,34,17);g.fill();// camera pill
  g.fillStyle='rgba(255,255,255,.07)';g.beginPath();g.moveTo(-w/2+22,-h/2+120);g.lineTo(w/2-160,-h/2+22);g.lineTo(w/2-60,-h/2+22);g.lineTo(-w/2+22,-h/2+300);g.fill();
  g.restore()}
function crack(g,x,y,seed,n=9,len=420){const R=rng(seed);g.save();g.lineCap='round';
  for(let i=0;i<n;i++){let a=R()*7,px=x,py=y;g.beginPath();g.moveTo(px,py);const L=len*(.4+R()*.8);for(let s=0;s<6;s++){a+=(R()-.5)*.6;px+=Math.cos(a)*L/6;py+=Math.sin(a)*L/6;g.lineTo(px,py)}
    g.strokeStyle='rgba(255,255,255,.55)';g.lineWidth=2.2;g.stroke();g.strokeStyle='rgba(0,0,0,.6)';g.lineWidth=1;g.stroke()}
  g.fillStyle='rgba(255,255,255,.25)';g.beginPath();g.arc(x,y,16,0,7);g.fill();g.restore()}
function phoneShot(u,d,t){camTo(ctx,1.0+.05*ease(u/d),540,900,Math.sin(t*1.9)*4,Math.cos(t*1.3)*4);
  ctx.drawImage(emBlur(),0,0);ctx.fillStyle='rgba(0,0,0,.45)';ctx.fillRect(0,0,W,H);
  const pct=u<.9?24:23,low=u>.9;
  const scr=(g,x,y,w,h)=>{let gr=g.createLinearGradient(0,y,0,y+h);gr.addColorStop(0,'#1a2a44');gr.addColorStop(1,'#07080d');g.fillStyle=gr;g.fillRect(x,y,w,h);
    glow(g,x+w*.3,y+h*.3,500,'90,120,200',.35);
    g.textAlign='center';g.fillStyle='#e8eef8';g.font='bold 150px '+MONO;g.fillText('00:'+(u<1.5?'51':'52'),x+w/2,y+330);
    g.font='bold 36px '+MONO;g.fillStyle='rgba(232,238,248,.7)';g.fillText('Нет сети',x+w/2,y+400);
    // big battery
    const bx=x+w/2-140,by=y+520,bw=260,bh=120;g.strokeStyle='#e8eef8';g.lineWidth=8;g.beginPath();g.roundRect(bx,by,bw,bh,18);g.stroke();g.fillStyle='#e8eef8';g.fillRect(bx+bw+4,by+38,16,44);
    const blink=low&&Math.floor(t*3)%2===0;g.fillStyle=blink?'#ff3b30':'#d8342c';g.fillRect(bx+14,by+14,(bw-28)*pct/100,bh-28);
    g.font='92px MB';g.fillStyle=low?'#ff3b30':'#e8eef8';g.fillText(pct+' %',x+w/2,by+260);
    g.font='bold 30px '+MONO;g.fillStyle='rgba(232,238,248,.55)';g.fillText('Энергосбережение',x+w/2,by+320);
    g.textAlign='left';crack(g,x+w-90,y+h-160,7,11,520)};
  const g=ctx,sk=SKIN_AMB;
  // hand behind the phone: palm low, fingertips peek out on the right edge
  g.save();g.translate(560,860);g.rotate(-.06);
  sleeve(g,[[150,1250],[110,640]],360,'#14181b');
  g.fillStyle=sk[0];g.beginPath();g.ellipse(40,420,330,250,-.1,0,7);g.fill();blob(g,-120,420,200,160,'230,170,130',.25);
  for(let i=0;i<4;i++){const y=-170+i*125;finger(g,180,y+60,300,y-10+i*6,70,sk,{light:'170,200,255'})}
  g.restore();
  phoneBody(ctx,560,860,520,1060,-.06,scr);
  ctx.save();ctx.globalCompositeOperation='lighter';glow(ctx,560,860,760,'110,140,220',.16);ctx.restore();
  g.save();g.translate(560,860);g.rotate(-.06);
  g.fillStyle=sk[0];g.beginPath();g.ellipse(-250,470,120,170,.25,0,7);g.fill();blob(g,-250,430,80,100,'240,190,150',.25);
  finger(g,-290,400,-238,120,74,sk,{light:'170,200,255'});// thumb over the left edge
  g.restore();
  ctx.save();ctx.globalCompositeOperation='source-atop';ctx.restore();
  finish(t,{vig:.85})}

// =====================================================================
// 5. phone flashlight beam in the smoky dark car (02.6)
// =====================================================================
function flashlightShot(u,d,t){if(!WAGON)buildWagon();const on=easeOut(seg(u,.25,.4));
  camTo(ctx,1.04,540,760,Math.sin(t*1.4)*6,Math.cos(t*.9)*4);
  ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);ctx.globalAlpha=.32;ctx.drawImage(WAGON.em,0,0);ctx.globalAlpha=1;
  const ax=lerp(470,610,ease(u/d)),ay=760;// beam target
  if(on>0){const L=layer();L.drawImage(WAGON.lit,0,0);L.globalCompositeOperation='destination-in';
    const gr=L.createRadialGradient(ax,ay,30,ax,ay,560);gr.addColorStop(0,'rgba(0,0,0,1)');gr.addColorStop(.55,'rgba(0,0,0,.55)');gr.addColorStop(1,'rgba(0,0,0,0)');L.fillStyle=gr;L.fillRect(0,0,W,H);
    ctx.globalAlpha=on*.85;ctx.drawImage(TMP,0,0);ctx.globalAlpha=1;
    // volumetric cone from the phone (bottom) to the target
    const S=layer();smoke(S,t*1.3,0,0,W,H,{alpha:1,scale:1.2,vx:-30,vy:-25,sheet:2});S.globalCompositeOperation='destination-in';
    S.beginPath();S.moveTo(500,1920);S.lineTo(ax-330,ay-260);S.lineTo(ax+330,ay-200);S.lineTo(600,1920);S.closePath();const cg=S.createLinearGradient(0,1920,0,ay);cg.addColorStop(0,'rgba(0,0,0,.9)');cg.addColorStop(1,'rgba(0,0,0,.25)');S.fillStyle=cg;S.fill();
    ctx.save();ctx.globalCompositeOperation='screen';ctx.globalAlpha=.7*on;ctx.drawImage(TMP,0,0);ctx.restore();
    ctx.save();ctx.globalCompositeOperation='lighter';glow(ctx,550,1900,420,'210,225,255',.5*on);glow(ctx,ax,ay,380,'200,220,255',.12*on);ctx.restore();
    dust(ctx,t,'230,235,255',.8*on,g2=>{g2.moveTo(500,1920);g2.lineTo(ax-330,ay-260);g2.lineTo(ax+330,ay-200);g2.lineTo(600,1920);g2.closePath()})}
  smoke(ctx,t,0,0,W,800,{alpha:.18,scale:1.5,vx:-12,vy:6,sheet:1});
  flash(u,.25,'220,230,255',.12,.35);
  finish(t,{vig:.88})}

// =====================================================================
// 6. Mikhalych's cane taps the floor (03.1–03.2)
// =====================================================================
const FLOORC=mk();{const g=FLOORC.getContext('2d'),R=rng(61);
  g.fillStyle='#050505';g.fillRect(0,0,W,H);
  // rubber floor in perspective (horizon at 860)
  const hy=860;let gr=g.createLinearGradient(0,hy,0,H);gr.addColorStop(0,'#2a2724');gr.addColorStop(1,'#4a453e');g.fillStyle=gr;g.fillRect(0,hy,W,H-hy);
  for(let i=0;i<70;i++){const k=i/70,y=hy+Math.pow(k,1.8)*(H-hy);g.fillStyle=`rgba(0,0,0,${.15+k*.15})`;g.fillRect(0,y,W,1+k*5);g.fillStyle=`rgba(255,220,180,${.03+k*.05})`;g.fillRect(0,y+1+k*5,W,1+k*2)}
  texFill(g,0,hy,W,H-hy,'rgba(0,0,0,0)',62,{grime:.9,specks:1});
  // bench front + legs in the back
  g.fillStyle='#1e2a3a';g.fillRect(0,560,W,240);g.fillStyle='#283a52';g.fillRect(0,560,W,40);texFill(g,0,560,W,240,'rgba(0,0,0,0)',63,{grime:.6});
  g.fillStyle='#14181d';g.fillRect(0,800,W,70);
  for(let i=0;i<300;i++){g.fillStyle=`rgba(255,240,220,${R()*.05})`;g.fillRect(R()*W,hy+R()*(H-hy),2+R()*6,1)}}
function caneShot(u,d,t,taps){camTo(ctx,1.04+.04*ease(u/d),540,1200,Math.sin(t*.8)*4,0);
  ctx.drawImage(FLOORC,0,0);amberLight(ctx,900,300,900,.35,t);
  // cane height: lifts and drops on each tap
  let lift=0,hit=-9;for(const a of taps){const k=u-a;if(k>-.22&&k<0)lift=Math.max(lift,Math.sin((k+.22)/.22*Math.PI/2)*90);if(k>=0&&k<.6)hit=k}
  const g=ctx;const tipX=520,tipY=1560-lift,topX=640,topY=420-lift;
  // trouser leg + old shoe on the right
  g.fillStyle='#2e2a26';g.beginPath();g.moveTo(700,560);g.lineTo(930,560);g.lineTo(960,1500);g.lineTo(720,1500);g.closePath();g.fill();
  g.fillStyle='rgba(0,0,0,.35)';g.fillRect(860,560,100,940);g.strokeStyle='rgba(255,255,255,.06)';g.lineWidth=6;g.beginPath();g.moveTo(790,600);g.lineTo(810,1480);g.stroke();
  let gr=g.createLinearGradient(0,1460,0,1640);gr.addColorStop(0,'#2a1d14');gr.addColorStop(1,'#120c08');g.fillStyle=gr;g.beginPath();g.moveTo(690,1480);g.quadraticCurveTo(640,1600,600,1640);g.lineTo(990,1650);g.quadraticCurveTo(1000,1520,970,1480);g.closePath();g.fill();
  g.fillStyle='rgba(255,200,150,.15)';g.beginPath();g.ellipse(700,1590,70,18,-.2,0,7);g.fill();
  g.fillStyle='rgba(0,0,0,.6)';g.filter='blur(10px)';g.beginPath();g.ellipse(800,1660,240,30,0,0,7);g.fill();g.filter='none';
  // cane shadow, cane, rubber tip
  g.strokeStyle='rgba(0,0,0,.55)';g.lineWidth=30;g.filter='blur(8px)';g.beginPath();g.moveTo(tipX+10,1575);g.lineTo(tipX+260,1630);g.stroke();g.filter='none';
  gr=g.createLinearGradient(tipX-14,0,tipX+14,0);gr.addColorStop(0,'#1e140d');gr.addColorStop(.4,'#6a4a30');gr.addColorStop(1,'#140d08');g.strokeStyle=gr;g.lineWidth=30;g.lineCap='butt';g.beginPath();g.moveTo(tipX,tipY-30);g.lineTo(topX,topY+40);g.stroke();
  g.strokeStyle='rgba(255,210,160,.25)';g.lineWidth=4;g.beginPath();g.moveTo(tipX-6,tipY-40);g.lineTo(topX-6,topY+40);g.stroke();
  g.fillStyle='#0b0b0b';g.beginPath();g.roundRect(tipX-20,tipY-46,40,50,8);g.fill();
  // crook handle + old hand
  g.strokeStyle='#4a3020';g.lineWidth=34;g.lineCap='round';g.beginPath();g.moveTo(topX,topY+60);g.lineTo(topX,topY);g.quadraticCurveTo(topX+20,topY-110,topX+130,topY-90);g.quadraticCurveTo(topX+190,topY-70,topX+180,topY);g.stroke();
  sleeve(g,[[1120,170],[topX+90,topY-150]],190,'#3b3128');
  const sk=SKIN_OLD;g.fillStyle=sk[0];g.beginPath();g.ellipse(topX+70,topY-95,110,72,-.25,0,7);g.fill();blob(g,topX+50,topY-120,70,30,'230,190,160',.35);
  for(let i=0;i<4;i++)finger(g,topX+120-i*42,topY-118,topX+110-i*44,topY-30,36,sk,{light:'255,170,90'});
  g.strokeStyle='rgba(60,35,25,.5)';g.lineWidth=3;for(let i=0;i<6;i++){g.beginPath();g.moveTo(topX+20+i*18,topY-150);g.quadraticCurveTo(topX+40+i*18,topY-120,topX+30+i*16,topY-100);g.stroke()}// veins/wrinkles
  // impact
  if(hit>=0){const k=hit/.6;g.save();g.globalCompositeOperation='lighter';g.strokeStyle=`rgba(255,200,140,${.6*(1-k)})`;g.lineWidth=6*(1-k)+1;g.beginPath();g.ellipse(tipX,1565,40+260*k,10+60*k,0,0,7);g.stroke();g.restore();
    const R=rng(Math.floor(taps.indexOf(taps.find(a=>u-a>=0&&u-a<.6))*7+3));for(let i=0;i<26;i++){const a=Math.PI+R()*Math.PI,v=80+R()*220;g.fillStyle=`rgba(200,180,150,${.5*(1-k)})`;g.beginPath();g.arc(tipX+Math.cos(a)*v*k,1560+Math.sin(a)*v*k*.4+200*k*k,2+R()*3,0,7);g.fill()}
    bigCaption('ТУК',lerp(330,300,k),1330-60*k,110+40*easeOut(k*3),`rgba(242,196,24,${1-k})`,1,{font:'CV',rot:-.12,stroke:10})}
  smoke(ctx,t,0,0,W,700,{alpha:.14,scale:1.5,vx:-14,vy:-8,sheet:0});
  finish(t,{vig:.82})}

// =====================================================================
// 7. hooded guy and his stream (03.3–03.4, 05.4–05.6)
// =====================================================================
function guyFace(g,x,y,s,{mouth=0,look=[0,0],t=0,lit=1}={}){g.save();g.translate(x,y);g.scale(s,s);const R=rng(71);
  // hood back
  let gr=g.createRadialGradient(0,-.1,.2,0,0,.9);gr.addColorStop(0,'#1a1e22');gr.addColorStop(1,'#08090a');g.fillStyle=gr;g.beginPath();g.ellipse(0,-.02,.62,.74,0,0,7);g.fill();
  // shoulders
  g.fillStyle='#111417';g.beginPath();g.moveTo(-1.3,1.6);g.bezierCurveTo(-1.2,.85,-.6,.62,0,.62);g.bezierCurveTo(.6,.62,1.2,.85,1.3,1.6);g.fill();
  // neck
  g.fillStyle='#38424d';g.fillRect(-.16,.3,.32,.4);
  // face (wider jaw), cold under-light from the phone
  g.save();g.scale(1.07,1.02);faceShape(g);g.restore();g.save();g.scale(1.07,1.02);faceShape(g);g.clip();g.scale(1/1.07,1/1.02);
  gr=g.createLinearGradient(0,.55,0,-.55);gr.addColorStop(0,'#b8cadb');gr.addColorStop(.45,'#7d8ea0');gr.addColorStop(1,'#2a323c');g.fillStyle=gr;g.fillRect(-.6,-.7,1.2,1.4);
  blob(g,-.25,.05,.2,.25,'20,26,34',.4*lit);blob(g,.28,.05,.2,.25,'20,26,34',.4);
  blob(g,0,.33,.3,.2,'40,50,60',.3);g.globalAlpha=.55;g.drawImage(SPECK,-.4,.15,.8,.4);g.drawImage(SPECK,-.4,.15,.8,.4);g.globalAlpha=1;// stubble
  for(let i=0;i<500;i++){const a=R()*Math.PI,r=.3+R()*.17;g.fillStyle=`rgba(15,18,22,${.35*R()})`;g.fillRect(Math.cos(a)*r*.9,.15+Math.sin(a)*r*.8,.006,.01)}
  // nose: under-light flips the shading (bright under the tip, dark bridge)
  blob(g,0,-.02,.05,.13,'20,26,34',.45);blob(g,0,.17,.07,.035,'220,235,250',.45);blob(g,0,.215,.06,.02,'15,20,25',.5);
  // eyes
  for(const sd of[-1,1]){const ex=sd*.15;blob(g,ex,-.01,.12,.07,'10,12,16',.6);
    g.save();g.beginPath();g.ellipse(ex,0,.065,.026,0,0,7);g.clip();g.fillStyle='#8c96a2';g.fillRect(ex-.08,-.04,.16,.08);
    const ix=ex+look[0]*.02,iy=look[1]*.01;g.fillStyle='#2a2420';g.beginPath();g.arc(ix,iy,.024,0,7);g.fill();g.fillStyle='#050505';g.beginPath();g.arc(ix,iy,.01,0,7);g.fill();
    g.fillStyle='rgba(200,225,255,.9)';g.fillRect(ix-.01,iy+.004,.012,.008);g.restore();
    g.strokeStyle='#0c0d0f';g.lineWidth=.012;g.beginPath();g.ellipse(ex,0,.068,.028,0,Math.PI*1.05,Math.PI*1.95);g.stroke();
    g.strokeStyle='#14110f';g.lineWidth=.03;g.beginPath();g.moveTo(ex-sd*.08,-.08);g.quadraticCurveTo(ex,-.11,ex+sd*.09,-.085);g.stroke()}// heavy brows
  // mouth
  g.fillStyle='#2a1c1c';g.beginPath();g.ellipse(0,.32,.08,.012+mouth*.05,0,0,7);g.fill();
  g.strokeStyle='rgba(200,215,230,.35)';g.lineWidth=.008;g.beginPath();g.moveTo(-.06,.355+mouth*.05);g.quadraticCurveTo(0,.37+mouth*.05,.06,.355+mouth*.05);g.stroke();
  g.restore();
  // hood front edge
  g.fillStyle='#16191c';g.beginPath();g.moveTo(-.55,.6);g.bezierCurveTo(-.6,0,-.45,-.6,0,-.64);g.bezierCurveTo(.45,-.6,.6,0,.55,.6);g.lineTo(.42,.6);g.bezierCurveTo(.46,0,.36,-.5,0,-.52);g.bezierCurveTo(-.36,-.5,-.46,0,-.42,.6);g.closePath();g.fill();
  g.strokeStyle='rgba(160,190,220,.18)';g.lineWidth=.012;g.beginPath();g.moveTo(-.43,.55);g.bezierCurveTo(-.47,0,-.36,-.5,0,-.53);g.stroke();
  // drawstrings
  g.strokeStyle='#9aa4ad';g.lineWidth=.014;for(const sd of[-1,1]){g.beginPath();g.moveTo(sd*.3,.6);g.quadraticCurveTo(sd*.32,.85,sd*.28,1.05+Math.sin(t*2+sd)*.01);g.stroke()}
  g.restore()}
const CHAT=['ты где??','это какая ветка','снимай дальше','держись бро','жесть','вызывай 112','сколько стоите?','там дым???','кто-нибудь знает что случилось','у меня тоже встал'];
const NICKS=['kot_leha','m1ra','dmitr.v','sasha_k','gleb88','nastya.pro','vovan','zhenya_x','lis','pash4'];
function streamUI(g,t,u,{viewers=312,chatMode=0,chatT=0}={}){
  g.setTransform(1,0,0,1,0,0);
  // top bar
  g.fillStyle='#e0302a';g.beginPath();g.roundRect(64,268,150,62,12);g.fill();g.font='40px MB';g.fillStyle='#fff';g.fillText('LIVE',86,316);
  g.fillStyle='rgba(0,0,0,.55)';g.beginPath();g.roundRect(230,268,210,62,12);g.fill();g.font='bold 36px '+MONO;g.fillStyle='#fff';g.fillText('● '+viewers,248,312);
  g.fillStyle='rgba(0,0,0,.55)';g.beginPath();g.roundRect(64,350,520,56,12);g.fill();g.font='bold 30px '+MONO;g.fillStyle='rgba(255,255,255,.85)';g.fillText('@hood_live · метро, встали',82,388);
  // chat feed (bottom-left, above subtitles zone)
  const step=.55,n=Math.floor(u/step);g.save();g.beginPath();g.rect(56,980,860,400);g.clip();
  for(let i=0;i<6;i++){const idx=n-i;if(idx<0)continue;const y=1330-i*70-(1-easeOut((u-idx*step)/.25))*-0;const a=i===0?easeOut((u-idx*step)/.25):1;
    g.globalAlpha=a*(1-i*.14);g.fillStyle='rgba(0,0,0,.45)';g.beginPath();g.roundRect(64,y-46,820,60,14);g.fill();
    g.font='bold 30px '+MONO;g.fillStyle='#8fd0ff';g.fillText(NICKS[idx%10],84,y-6);g.fillStyle='#fff';g.fillText(CHAT[idx%10],84+NICKS[idx%10].length*19+20,y-6)}
  g.restore();g.globalAlpha=1}
function streamShot(u,d,t,mode){
  // "we look at his phone screen": selfie view of the guy
  const z=mode==='read'?1+.1*ease(u/d):1.02;camTo(ctx,z,540,860,Math.sin(t*3.1)*7,Math.cos(t*2.3)*6);
  ctx.fillStyle='#07090c';ctx.fillRect(0,0,W,H);ctx.globalAlpha=.6;ctx.drawImage(emBlur(),0,0);ctx.globalAlpha=1;ctx.fillStyle='rgba(0,0,0,.35)';ctx.fillRect(0,0,W,H);
  const talk=mode==='talk'?envAt(t)*1.2:0;const look=mode==='read'?[Math.sin(u*2.2)*.6,.9]:[0,0];
  guyFace(ctx,540,900,640,{mouth:mode==='talk'?clamp(talk,0,1)*(.5+.5*Math.sin(t*23)):0,look,t});
  ctx.save();ctx.globalCompositeOperation='lighter';glow(ctx,540,1500,900,'120,160,220',.18);ctx.restore();
  ctx.setTransform(1,0,0,1,0,0);ctx.fillStyle='rgba(0,0,0,.18)';for(let y=0;y<H;y+=4)ctx.fillRect(0,y,W,1);
  streamUI(ctx,t,u,{viewers:mode==='talk'?312+Math.floor(u*9):(mode==='read'?1847+Math.floor(u*41):2318)});
  finish(t,{vig:.75,grain:.12})}
function chatShot(u,d,t){camTo(ctx,1.0+.12*easeIn(u/d),540,1100,0,0);
  ctx.fillStyle='#0a0d12';ctx.fillRect(0,0,W,H);ctx.globalAlpha=.35;guyFace(ctx,540,700,700,{t,look:[0,1]});ctx.globalAlpha=1;ctx.fillStyle='rgba(5,8,12,.55)';ctx.fillRect(0,0,W,H);
  const g=ctx;const msgs=[['nastya.pro','вас видно на карте?'],['gleb88','держись'],['lis','сколько уже стоите'],['m1ra','там ктото есть в кабине?'],['dmitr.v','СНИМАЙ ВПЕРЁД']];
  const appear=ps('05.6')-.25-(ps('05.4')-.15)-(ps('05.5')-.15-(ps('05.4')-.15));// local time of the key message
  const ka=ps('05.6')-.2-(ps('05.5')-.15);const k=easeOutBack(seg(u,ka,ka+.35));
  g.font='bold 44px '+MONO;
  msgs.forEach(([n,m],i)=>{const y=520+i*130-140*k;g.globalAlpha=.75;g.fillStyle='rgba(255,255,255,.08)';g.beginPath();g.roundRect(70,y-70,920,104,20);g.fill();g.fillStyle='#8fd0ff';g.fillText(n,100,y-6);g.fillStyle='#e8eef4';g.fillText(m,100+n.length*26+26,y-6)});
  g.globalAlpha=1;
  if(u>ka){const y=1210-140*k+140;g.save();g.translate(540,y);g.scale(.9+.1*k,.9+.1*k);
    g.fillStyle='rgba(224,48,42,.22)';g.beginPath();g.roundRect(-470,-90,940,150,24);g.fill();g.strokeStyle='#e0302a';g.lineWidth=5;g.stroke();
    g.font='bold 48px '+MONO;g.fillStyle='#ff8a80';g.fillText('вы…',-440,0);g.fillStyle='#fff';g.font='bold 60px '+MONO;g.fillText('кабина пустая',-300,2);g.restore();
    glitch(t,ps('05.6')-.05,ps('05.6')+.08,.5)}
  ctx.setTransform(1,0,0,1,0,0);ctx.fillStyle='rgba(0,0,0,.18)';for(let y=0;y<H;y+=4)ctx.fillRect(0,y,W,1);
  finish(t,{vig:.8,grain:.12})}

// =====================================================================
// 8. woman in metro uniform hides the radio (03.5–03.6)
// =====================================================================
function radioShot(u,d,t,hideAt){camTo(ctx,1.02+.05*ease(u/d),540,900,Math.sin(t*.6)*4,0);
  ctx.drawImage(emBlur(),0,0);ctx.fillStyle='rgba(0,0,0,.35)';ctx.fillRect(0,0,W,H);
  const g=ctx;
  // navy uniform jacket torso
  let gr=g.createLinearGradient(0,0,W,0);gr.addColorStop(0,'#1c2840');gr.addColorStop(.5,'#26355a');gr.addColorStop(1,'#111a2c');g.fillStyle=gr;
  g.beginPath();g.moveTo(-60,1920);g.lineTo(-40,500);g.quadraticCurveTo(200,330,540,320);g.quadraticCurveTo(880,330,1120,500);g.lineTo(1140,1920);g.fill();
  texFill(g,0,320,W,1600,'rgba(0,0,0,0)',81,{grime:.35,specks:.5});
  // collar + white shirt + tie
  g.fillStyle='#e9e6e0';g.beginPath();g.moveTo(420,320);g.lineTo(540,560);g.lineTo(660,320);g.fill();g.fillStyle='#7a1a1a';g.beginPath();g.moveTo(520,380);g.lineTo(560,380);g.lineTo(575,640);g.lineTo(540,690);g.lineTo(505,640);g.fill();
  g.fillStyle='#1a2338';for(const sd of[-1,1]){g.beginPath();g.moveTo(540+sd*120,320);g.lineTo(540+sd*20,700);g.lineTo(540+sd*260,560);g.closePath();g.fill()}
  g.strokeStyle='rgba(0,0,0,.45)';g.lineWidth=5;g.beginPath();g.moveTo(540,700);g.lineTo(540,1920);g.stroke();
  for(const y of[820,1060,1300,1540]){g.fillStyle='#b9963e';g.beginPath();g.arc(575,y,22,0,7);g.fill();g.fillStyle='rgba(255,240,180,.6)';g.beginPath();g.arc(569,y-6,7,0,7);g.fill()}
  // shoulder board + badge
  g.fillStyle='#c8a64a';g.fillRect(830,420,200,22);g.fillRect(70,420,190,22);
  g.save();g.translate(330,820);g.fillStyle='#1d2a40';g.beginPath();g.roundRect(-110,-60,220,120,14);g.fill();g.strokeStyle='#c8a64a';g.lineWidth=5;g.stroke();
  g.fillStyle='#d8342c';g.font='70px MB';g.textAlign='center';g.fillText('М',0,26);g.textAlign='left';g.restore();
  g.font='bold 22px '+MONO;g.fillStyle='rgba(220,210,180,.8)';g.fillText('МЕТРОПОЛИТЕН',245,920);
  // breast pocket on the right
  const px=700,py=1080;g.fillStyle='#1a2338';g.fillRect(px-150,py,300,300);g.strokeStyle='rgba(0,0,0,.5)';g.lineWidth=4;g.strokeRect(px-150,py,300,300);
  // radio: from hand height into the pocket
  const k=ease(seg(u,hideAt,hideAt+1.4));const rx=lerp(760,700,k),ry=lerp(760,1180,k),rr=lerp(-.25,0,k);
  const ledOn=1-ease(seg(u,hideAt+1.2,hideAt+1.8));
  g.save();g.beginPath();g.rect(0,0,W,py+40+ (1-k)*2000);g.clip();
  g.save();g.translate(rx,ry);g.rotate(rr);
  g.fillStyle='#0d0e0f';g.fillRect(-14,-330,28,200);g.fillStyle='#202224';g.fillRect(-10,-330,6,200);// antenna
  gr=g.createLinearGradient(-90,0,90,0);gr.addColorStop(0,'#2a2c2e');gr.addColorStop(.3,'#141516');gr.addColorStop(1,'#0a0a0b');g.fillStyle=gr;g.beginPath();g.roundRect(-90,-150,180,420,22);g.fill();
  g.fillStyle='#1d2a2a';g.fillRect(-60,-110,120,70);g.fillStyle=`rgba(120,255,160,${.25+.5*ledOn})`;g.font='bold 30px '+MONO;g.fillText('CH 2',-48,-62);
  for(let yy=0;yy<6;yy++)for(let xx=0;xx<5;xx++){g.fillStyle='#050505';g.beginPath();g.arc(-48+xx*24,10+yy*24,7,0,7);g.fill()}
  const bl=ledOn*(Math.floor(t*4)%2?1:.35);g.fillStyle=`rgba(80,255,120,${bl})`;g.beginPath();g.arc(50,-130,9,0,7);g.fill();
  g.save();g.globalCompositeOperation='lighter';glow(g,50,-130,80,'80,255,120',.6*bl);g.restore();
  g.restore();g.restore();
  // pocket flap over the radio once inside
  g.fillStyle='#1d2740';g.beginPath();g.moveTo(px-160,py-10);g.lineTo(px+160,py-10);g.lineTo(px+150,py+70);g.lineTo(px,py+90);g.lineTo(px-150,py+70);g.closePath();g.fill();
  g.fillStyle='#b9963e';g.beginPath();g.arc(px,py+56,16,0,7);g.fill();
  // hand holding the radio until it is inside
  if(k<.98){const sk=SKIN_AMB;g.save();g.translate(rx+40,ry+120);g.rotate(rr);
    sleeve(g,[[300,500],[80,120]],170,'#1c2840');
    g.fillStyle=sk[0];g.beginPath();g.ellipse(70,60,90,110,.4,0,7);g.fill();
    for(let i=0;i<4;i++)finger(g,80,-60+i*55,-120,-80+i*58,40,sk);
    finger(g,20,140,-70,60,46,sk);
    g.restore()}
  amberLight(ctx,200,250,900,.4,t);
  smoke(ctx,t,0,0,W,600,{alpha:.12,scale:1.5,vx:-10,vy:-8,sheet:0});
  finish(t,{vig:.82})}

// =====================================================================
// 9. ceiling speaker: dead / alive / speaking (03.7–03.9, 05.10–06)
// =====================================================================
const SPK=mk();{const g=SPK.getContext('2d');
  texFill(g,0,0,W,H,'#b8beb9',91,{grime:.9,specks:.8,streaks:20});
  for(let y=120;y<H;y+=180){g.fillStyle='rgba(0,0,0,.12)';g.fillRect(0,y,W,3)}
  // speaker housing
  g.fillStyle='rgba(0,0,0,.4)';g.filter='blur(16px)';g.beginPath();g.arc(560,700,380,0,7);g.fill();g.filter='none';
  let gr=g.createRadialGradient(480,600,40,540,680,380);gr.addColorStop(0,'#e4e8e4');gr.addColorStop(1,'#8a918c');g.fillStyle=gr;g.beginPath();g.arc(540,680,360,0,7);g.fill();
  g.fillStyle='#2a2e2c';g.beginPath();g.arc(540,680,300,0,7);g.fill();
  for(let r=20;r<290;r+=26)for(let a=0;a<Math.PI*2;a+=26/r){g.fillStyle='#050606';g.beginPath();g.arc(540+Math.cos(a)*r,680+Math.sin(a)*r,8,0,7);g.fill();g.fillStyle='rgba(255,255,255,.12)';g.beginPath();g.arc(540+Math.cos(a)*r-2,680+Math.sin(a)*r-3,3,0,7);g.fill()}
  for(let i=0;i<4;i++){const a=i/4*Math.PI*2+.8;g.fillStyle='#5f6662';g.beginPath();g.arc(540+Math.cos(a)*332,680+Math.sin(a)*332,12,0,7);g.fill()}
  texFill(g,180,320,720,720,'rgba(0,0,0,0)',92,{grime:.5,specks:.4});
  // lamp housing (red indicator)
  g.fillStyle='#202322';g.beginPath();g.roundRect(820,1080,140,90,14);g.fill();g.fillStyle='#3a0d0b';g.beginPath();g.arc(890,1125,30,0,7);g.fill();
  // display strip
  g.fillStyle='#060606';g.fillRect(90,1150,700,190);g.strokeStyle='#4a504c';g.lineWidth=10;g.strokeRect(85,1145,710,200);
  g.font='bold 30px '+MONO;g.fillStyle='rgba(30,30,30,.85)';g.fillText('ДИНАМИК · ВАГОН 0473',100,1395)}
function speakerShot(u,d,t,mode,{typeFrom=0}={}){const alive=mode!=='dead';
  const z=1.02+.08*ease(u/d);const sh=alive&&mode==='alive'?envAt(t)*6:0;camTo(ctx,z,540,800,Math.sin(t*40)*sh,Math.cos(t*37)*sh);
  ctx.drawImage(SPK,0,0);
  ctx.setTransform(1,0,0,1,0,0);ctx.globalCompositeOperation='multiply';ctx.fillStyle='#5a3a1c';ctx.fillRect(0,0,W,H);ctx.globalCompositeOperation='source-over';
  camTo(ctx,z,540,800,0,0);amberLight(ctx,200,200,900,.35,t);
  const lamp=alive?seg(u,0,.25)*(mode==='alive'?.75+.25*Math.sin(t*12):1):0;
  if(lamp>0){ctx.fillStyle=`rgba(255,40,30,${lamp})`;ctx.beginPath();ctx.arc(890,1125,30,0,7);ctx.fill();ctx.save();ctx.globalCompositeOperation='lighter';glow(ctx,890,1125,260,'255,40,30',.55*lamp);glow(ctx,540,680,600,'255,40,30',.12*lamp);ctx.restore()}
  // waveform on the display strip
  const L=layer();camTo(L,1,0,0);L.beginPath();for(let i=0;i<=120;i++){const x=110+i*5.6,a=alive?envAt(t-(120-i)/240)*70:0;const y=1245+Math.sin(i*.9+t*40)*a*Math.sin(i/120*Math.PI)+(alive?0:Math.sin(i*3.1+t*30)*1.5);i?L.lineTo(x,y):L.moveTo(x,y)}
  L.strokeStyle=alive?'rgba(255,90,70,1)':'rgba(120,255,160,.9)';L.lineWidth=4;L.stroke();
  camTo(ctx,z,540,800,0,0);ctx.drawImage(TMP,0,0);ctx.save();ctx.globalCompositeOperation='lighter';ctx.filter='blur(8px)';ctx.drawImage(TMP,0,0);ctx.restore();
  if(!alive){ctx.font='bold 34px '+MONO;ctx.fillStyle=`rgba(120,255,160,${.5+.3*Math.sin(t*3)})`;ctx.fillText('НЕТ СИГНАЛА',560,1200)}
  smoke(ctx,t,0,0,W,1100,{alpha:alive?.12:.2,scale:1.6,vx:-18,vy:-10,sheet:1});
  finish(t,{vig:.84});
  // typed voice lines (06) – big LED text in the safe zone
  if(mode==='voice'){ctx.setTransform(1,0,0,1,0,0);const lines=[['06.1','СОНЯ.'],['06.2','НЕ ВЫХОДИ.'],['06.3','ПУСТЬ РЕШАТ ОНИ.']];
    ctx.fillStyle='rgba(0,0,0,.55)';ctx.fillRect(56,1430,968,290);
    lines.forEach(([id,s],i)=>{const p=PH(id),k=seg(t,p.s,p.s+Math.min(.8,(p.e-p.s)*.8));const n=Math.ceil(s.length*k);if(t<p.s-.02)return;
      ledText(ctx,s.slice(0,n)+(k<1&&Math.floor(t*8)%2?'▌':''),82,1450+i*88,4.2,{col:i===1?'255,60,45':'255,150,40'})})}}

// =====================================================================
// 10. intercom button "СВЯЗЬ С МАШИНИСТОМ" (04.2–04.3, 05.1)
// =====================================================================
const BTN=mk();{const g=BTN.getContext('2d');
  texFill(g,0,0,W,H,'#9ea6a1',101,{grime:.9,specks:.8,streaks:30});
  // door edge on the left
  texFill(g,0,0,170,H,'#7f8984',102,{grime:.7});g.fillStyle='#0b0c0c';g.fillRect(160,0,22,H);
  // panel
  const x=250,y=420,w=700,h=980;g.fillStyle='rgba(0,0,0,.45)';g.filter='blur(14px)';g.fillRect(x+16,y+24,w,h);g.filter='none';
  let gr=g.createLinearGradient(x,y,x+w,y+h);gr.addColorStop(0,'#d2d6d3');gr.addColorStop(1,'#8b928e');g.fillStyle=gr;g.fillRect(x,y,w,h);
  texFill(g,x,y,w,h,'rgba(0,0,0,0)',103,{grime:.5,specks:.5});
  for(let i=-20;i<40;i++){g.save();g.beginPath();g.rect(x,y,w,48);g.rect(x,y+h-48,w,48);g.clip();g.fillStyle=i%2?'#151515':'#e8c21a';g.beginPath();g.moveTo(x+i*40,y-10);g.lineTo(x+i*40+40,y-10);g.lineTo(x+i*40-60,y+h+10);g.lineTo(x+i*40-100,y+h+10);g.fill();g.restore()}
  rivets(g,x+30,x+w-30,y+75,w-60);rivets(g,x+30,x+w-30,y+h-75,w-60);
  g.font='58px MB';g.fillStyle='#1a1a1a';g.textAlign='center';g.fillText('СВЯЗЬ',x+w/2,y+190);g.fillText('С МАШИНИСТОМ',x+w/2,y+260);
  // grille
  for(let r=0;r<5;r++)for(let c=0;c<9;c++){g.fillStyle='#0a0a0a';g.beginPath();g.arc(x+190+c*40,y+340+r*36,10,0,7);g.fill()}
  // button bezel
  g.fillStyle='#3a3e3c';g.beginPath();g.arc(x+w/2,y+690,170,0,7);g.fill();g.fillStyle='#1b1d1c';g.beginPath();g.arc(x+w/2,y+690,140,0,7);g.fill();
  g.font='bold 30px '+MONO;g.fillStyle='rgba(20,20,20,.85)';g.fillText('НАЖМИТЕ И ГОВОРИТЕ',x+w/2,y+900);g.textAlign='left'}
function buttonShot(u,d,t,pressAt,{after=0}={}){const z=1.0+.1*ease(u/d);camTo(ctx,z,600,1100,0,0);
  ctx.drawImage(BTN,0,0);ctx.setTransform(1,0,0,1,0,0);ctx.globalCompositeOperation='multiply';ctx.fillStyle='#6a4520';ctx.fillRect(0,0,W,H);ctx.globalCompositeOperation='source-over';
  camTo(ctx,z,600,1100,0,0);amberLight(ctx,300,250,1000,.4,t);
  const g=ctx,bx=600,by=1110,pk=after?1:clamp((u-pressAt)/.08,0,1)*(u<pressAt+.5?1:1);const depth=after?0:(u>pressAt&&u<pressAt+.35?1:0);
  let gr=g.createRadialGradient(bx-40,by-40,20,bx,by,130);gr.addColorStop(0,depth?'#d9b012':'#ffe25a');gr.addColorStop(1,depth?'#7a5a06':'#a87a08');g.fillStyle=gr;g.beginPath();g.arc(bx,by+depth*8,128-depth*6,0,7);g.fill();
  g.fillStyle='rgba(255,255,230,.45)';g.beginPath();g.ellipse(bx-40,by-50+depth*8,40,22,-.5,0,7);g.fill();
  // call LED
  const on=after||u>pressAt;const bl=on?(Math.floor(t*3)%2?1:.25):0;g.fillStyle=`rgba(255,50,40,${.15+.85*bl})`;g.beginPath();g.arc(bx+250,by-190,20,0,7);g.fill();
  if(bl>.5){g.save();g.globalCompositeOperation='lighter';glow(g,bx+250,by-190,140,'255,50,40',.6);g.restore()}
  g.font='bold 28px '+MONO;g.fillStyle=on?'rgba(255,90,70,.95)':'rgba(30,30,30,.6)';g.fillText(after?'ВЫЗОВ… НЕТ ОТВЕТА':'ВЫЗОВ',bx+200-(after?260:0),by-232);
  // hand with pointing finger, coming from bottom right
  if(!after){const k=ease(seg(u,pressAt-1.6,pressAt));const hx=lerp(1250,bx+70,k),hy=lerp(2100,by+110,k)+(depth?8:0);const sk=SKIN_AMB;
    g.save();g.translate(hx,hy);g.rotate(-.75);
    sleeve(g,[[0,900],[0,240]],250,'#1a1e21');
    g.fillStyle=sk[0];g.beginPath();g.roundRect(-110,40,220,230,80);g.fill();blob(g,-30,120,90,70,'230,170,130',.25);
    for(let i=0;i<3;i++){g.fillStyle=sk[0];g.beginPath();g.ellipse(-55+i*55,50,32,44,0,0,7);g.fill();g.strokeStyle='rgba(60,30,20,.5)';g.lineWidth=3;g.beginPath();g.arc(-55+i*55,40,26,Math.PI*1.1,Math.PI*1.9);g.stroke()}
    finger(g,-80,80,-40,-150,52,sk);// index
    finger(g,110,150,150,40,54,sk,{nail:0});// thumb
    g.restore()}
  if(u>pressAt&&u<pressAt+.12&&!after){ctx.setTransform(1,0,0,1,0,0);ctx.fillStyle='rgba(255,230,180,.15)';ctx.fillRect(0,0,W,H);bigCaption('КЛИК',300,820,90,'#f2c418',1,{font:'CV',rot:-.1,stroke:10})}
  if(after){// flat line: the speaker stays silent
    ctx.setTransform(1,0,0,1,0,0);ctx.fillStyle='rgba(0,0,0,.6)';ctx.fillRect(140,300,800,130);ctx.strokeStyle='rgba(120,255,160,.9)';ctx.lineWidth=4;ctx.beginPath();for(let i=0;i<=100;i++){const x=160+i*7.6,y=365+Math.sin(i*2.7+t*25)*1.2;i?ctx.lineTo(x,y):ctx.moveTo(x,y)}ctx.stroke();
    ctx.font='bold 26px '+MONO;ctx.fillStyle='rgba(120,255,160,.8)';ctx.fillText('ДИНАМИК: ТИШИНА',160,330)}
  smoke(ctx,t,0,0,W,800,{alpha:.12,scale:1.5,vx:-10,vy:-8,sheet:2});
  finish(t,{vig:.82})}

// =====================================================================
// 11. car number plate circled (04.4)
// =====================================================================
const PLATE=mk();{const g=PLATE.getContext('2d');
  texFill(g,0,0,W,H,'#4a5650',111,{grime:1,specks:.8,streaks:40});scratches(g,0,0,W,H,600,112,.2);
  for(let y=100;y<H;y+=140){g.fillStyle='rgba(0,0,0,.22)';g.fillRect(0,y,W,3)}
  g.fillStyle='rgba(0,0,0,.5)';g.filter='blur(12px)';g.fillRect(150,700,820,330);g.filter='none';
  g.fillStyle='#16263d';g.fillRect(130,680,820,320);g.strokeStyle='#cfd3d6';g.lineWidth=10;g.strokeRect(152,702,776,276);
  texFill(g,130,680,820,320,'rgba(0,0,0,0)',113,{grime:.5,specks:.6});
  g.font='bold 190px '+MONO;g.fillStyle='#e9ecef';g.textAlign='center';g.fillText('№0473',540,910);g.textAlign='left';
  rivets(g,170,910,720,740);rivets(g,170,910,960,740);
  g.font='bold 34px '+MONO;g.fillStyle='rgba(230,225,210,.6)';g.fillText('Э-47 · ГОД ВЫПУСКА 1987',170,1100)}
function plateShot(u,d,t){const z=1.0+.08*ease(u/d);camTo(ctx,z,540,840,0,0);ctx.drawImage(PLATE,0,0);
  ctx.setTransform(1,0,0,1,0,0);ctx.globalCompositeOperation='multiply';ctx.fillStyle='#5a3a1c';ctx.fillRect(0,0,W,H);ctx.globalCompositeOperation='source-over';
  camTo(ctx,z,540,840,0,0);
  // flashlight spot on the plate
  ctx.save();ctx.globalCompositeOperation='lighter';glow(ctx,540+Math.sin(t*1.3)*40,840,700,'200,215,240',.22);ctx.restore();
  // hand-drawn red circle
  const k=easeOut(seg(u,.35,1.0));if(k>0){ctx.strokeStyle='#e0302a';ctx.lineWidth=14;ctx.lineCap='round';ctx.beginPath();const R=rng(5);
    for(let i=0;i<=80*k;i++){const a=-1.9+i/80*Math.PI*2.15,rx=470+Math.sin(i*.3)*6,ry=210+Math.cos(i*.25)*6;const x=540+Math.cos(a)*rx,y=840+Math.sin(a)*ry;i?ctx.lineTo(x,y):ctx.moveTo(x,y)}ctx.stroke()}
  finish(t,{vig:.8})}

// =====================================================================
// 12. instruction sheet with steps + stamp (04.5–04.6)
// =====================================================================
const SHEET=mk();{const g=SHEET.getContext('2d');
  texFill(g,0,0,W,H,'#3a423e',121,{grime:1,specks:.8});
  g.fillStyle='rgba(0,0,0,.5)';g.filter='blur(14px)';g.fillRect(100,300,900,1300);g.filter='none';
  g.fillStyle='#ece8dc';g.fillRect(80,280,920,1300);texFill(g,80,280,920,1300,'rgba(0,0,0,0)',122,{grime:.4,specks:.5,streaks:10});
  g.fillStyle='#c33a2c';g.fillRect(80,280,920,190);g.font='54px MB';g.fillStyle='#fff';g.fillText('ПРИ ОСТАНОВКЕ',120,365);g.fillText('В ТОННЕЛЕ',120,435);
  g.font='bold 26px '+MONO;g.fillStyle='rgba(40,40,40,.6)';g.fillText('ПАМЯТКА ПАССАЖИРУ',120,1540)}
const STEPS=[['1','НАЖМИТЕ КНОПКУ','«СВЯЗЬ С МАШИНИСТОМ»'],['2','НАЗОВИТЕ НОМЕР','ВАГОНА: 0473'],['3','СКАЖИТЕ,','ЧТО СЛУЧИЛОСЬ']];
function stepsShot(u,d,t,checkAt,stampAt){const shake=u>stampAt&&u<stampAt+.3?Math.sin(u*90)*14*(1-(u-stampAt)/.3):0;
  camTo(ctx,1.02+.05*ease(u/d),540,900,shake,shake*.5);ctx.drawImage(SHEET,0,0);
  const g=ctx;
  STEPS.forEach(([n,a,b],i)=>{const y=600+i*250;g.fillStyle='#1a1a1a';g.beginPath();g.arc(170,y,52,0,7);g.fill();g.font='60px MB';g.fillStyle='#ece8dc';g.textAlign='center';g.fillText(n,170,y+22);g.textAlign='left';
    g.font='50px MB';g.fillStyle='#1a1a1a';g.fillText(a,260,y-6);g.font='40px MB';g.fillStyle='#4a4a46';g.fillText(b,260,y+50);
    const ck=i<2?1:easeOut(seg(u,checkAt,checkAt+.3));if(ck>0){g.strokeStyle='#2f8f5a';g.lineWidth=18;g.lineCap='round';g.beginPath();g.moveTo(880,y);g.lineTo(880+30*Math.min(1,ck*2),y+30*Math.min(1,ck*2));if(ck>.5)g.lineTo(910+70*(ck-.5)*2,y+30-80*(ck-.5)*2);g.stroke()}});
  // warning line
  g.fillStyle='#c33a2c';g.fillRect(120,1240,840,6);
  // amber + phone light
  ctx.setTransform(1,0,0,1,0,0);ctx.globalCompositeOperation='multiply';ctx.fillStyle='#8a6a40';ctx.fillRect(0,0,W,H);ctx.globalCompositeOperation='source-over';
  camTo(ctx,1.02+.05*ease(u/d),540,900,shake,shake*.5);ctx.save();ctx.globalCompositeOperation='lighter';glow(ctx,520+Math.sin(t)*60,900,800,'220,225,240',.16);ctx.restore();
  // stamp
  if(u>stampAt){const k=seg(u,stampAt,stampAt+.12),s=lerp(2.2,1,easeOut(k));ctx.save();ctx.translate(540,1290);ctx.rotate(-.1);ctx.scale(.72,.72);ctx.scale(s,s);ctx.globalAlpha=k*.92;
    ctx.strokeStyle='#d8261e';ctx.lineWidth=14;ctx.strokeRect(-430,-120,860,240);ctx.lineWidth=5;ctx.strokeRect(-410,-100,820,200);
    ctx.font='76px MB';ctx.fillStyle='#d8261e';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText('НЕ ОТКРЫВАЙ',0,-30);ctx.fillText('ДВЕРИ',0,50);
    ctx.globalCompositeOperation='destination-out';ctx.globalAlpha=.4;ctx.drawImage(SPECK,-540,-200,1080,400);ctx.drawImage(SPECK,-540,-200,1080,400);ctx.restore()}
  finish(t,{vig:.8})}

// =====================================================================
// 13. contact rail, 825 V (04.6 end – 04.7)
// =====================================================================
const RAIL=mk();{const g=RAIL.getContext('2d'),R=rng(131);const vx=600,vy=640;
  g.fillStyle='#040505';g.fillRect(0,0,W,H);
  // tunnel tubbing rings
  for(let i=0;i<14;i++){const k=Math.pow(.8,i),r=1300*k;g.strokeStyle=`rgba(60,64,60,${.8*k+.1})`;g.lineWidth=40*k+2;g.beginPath();g.ellipse(vx,vy+40*k,r,r*1.05,0,Math.PI*.95,Math.PI*2.05);g.stroke();
    g.strokeStyle=`rgba(255,200,150,${.05*k})`;g.lineWidth=4*k+1;g.beginPath();g.ellipse(vx,vy+40*k-20*k,r,r*1.05,0,Math.PI*1.1,Math.PI*1.5);g.stroke()}
  // ballast/track bed
  let gr=g.createLinearGradient(0,vy,0,H);gr.addColorStop(0,'#050605');gr.addColorStop(1,'#232521');g.fillStyle=gr;g.beginPath();g.moveTo(vx-30,vy);g.lineTo(vx+30,vy);g.lineTo(W+400,H);g.lineTo(-400,H);g.fill();
  texFill(g,0,vy,W,H-vy,'rgba(0,0,0,0)',132,{grime:.9,specks:1});
  // sleepers
  for(let i=1;i<40;i++){const z=i*.6,k=1/z;const y=vy+700*k;if(y>H)continue;const hw=900*k;g.fillStyle=`rgba(40,36,30,${clamp(k*1.6,0,1)})`;g.fillRect(vx-hw,y,hw*2,Math.max(2,90*k))}
  // running rails
  for(const sd of[-1,1]){g.strokeStyle='#5a5650';g.lineWidth=1;g.fillStyle='#4a4640';g.beginPath();g.moveTo(vx+sd*8,vy);g.lineTo(vx+sd*12,vy);g.lineTo(vx+sd*520,H);g.lineTo(vx+sd*430,H);g.fill();
    g.fillStyle='rgba(255,220,180,.55)';g.beginPath();g.moveTo(vx+sd*10,vy);g.lineTo(vx+sd*11,vy);g.lineTo(vx+sd*470,H);g.lineTo(vx+sd*440,H);g.fill()}
  // contact rail on the right, raised on insulators, with cover board
  g.fillStyle='#2b2e2c';g.beginPath();g.moveTo(vx+40,vy-6);g.lineTo(vx+56,vy-6);g.lineTo(W+260,H-260);g.lineTo(W+80,H-180);g.fill();// cover
  g.fillStyle='#6f6a62';g.beginPath();g.moveTo(vx+40,vy+2);g.lineTo(vx+52,vy+2);g.lineTo(W+180,H-120);g.lineTo(W+60,H-90);g.fill();// rail head
  for(let i=1;i<20;i++){const k=1/(i*.9);const x=vx+40+(W+120-vx)*k,y=vy+(H-60-vy)*k;g.fillStyle=`rgba(200,190,170,${clamp(k*1.3,0,.9)})`;g.fillRect(x-20*k,y,40*k,120*k)}// insulators
  for(let i=0;i<700;i++){const x=R()*W,y=vy+80+R()*(H-vy),s=3+R()*10;const v=40+R()*60;g.fillStyle=`rgba(${v},${v*.95},${v*.88},${.3+R()*.4})`;g.beginPath();g.ellipse(x,y,s,s*.6,R()*3,0,7);g.fill()}}
function railShot(u,d,t,tagAt,voltAt){const z=1.0+.12*ease(u/d);camTo(ctx,z,860,1500,Math.sin(t*.9)*4,0);ctx.drawImage(RAIL,0,0);
  // flashlight sweeping the track
  const sx=lerp(300,860,ease(seg(u,0,tagAt+.3))),sy=lerp(1300,1480,ease(u/d));const L=layer();L.drawImage(RAIL,0,0);L.globalCompositeOperation='source-atop';L.fillStyle='rgba(255,255,255,.25)';L.fillRect(0,0,W,H);L.globalCompositeOperation='destination-in';
  const gr=L.createRadialGradient(sx,sy,30,sx,sy,520);gr.addColorStop(0,'#000');gr.addColorStop(1,'rgba(0,0,0,0)');L.fillStyle=gr;L.fillRect(0,0,W,H);
  ctx.save();ctx.globalCompositeOperation='lighter';ctx.drawImage(TMP,0,0);glow(ctx,sx,sy,420,'200,215,240',.1);ctx.restore();
  // live rail: arcs + hum after voltAt
  const v=seg(u,voltAt-.1,voltAt+.2);if(v>0){const R=rng(Math.floor(t*24));ctx.save();ctx.globalCompositeOperation='lighter';
    for(let i=0;i<3;i++){const k=.25+R()*.6;const x=lerp(640,W+140,k),y=lerp(640,H-110,k);let px=x,py=y;ctx.strokeStyle=`rgba(170,200,255,${.9*v})`;ctx.lineWidth=3+R()*3;ctx.beginPath();ctx.moveTo(px,py);for(let s=0;s<7;s++){px+=(R()-.5)*60;py-=10+R()*30;ctx.lineTo(px,py)}ctx.stroke();glow(ctx,x,y,180*k+60,'150,190,255',.5*v)}
    ctx.strokeStyle=`rgba(150,190,255,${.35*v*(.7+.3*Math.sin(t*60))})`;ctx.lineWidth=18;ctx.filter='blur(10px)';ctx.beginPath();ctx.moveTo(650,646);ctx.lineTo(W+180,H-120);ctx.stroke();ctx.restore()}
  smoke(ctx,t,0,0,W,1100,{alpha:.2,scale:1.6,vx:-20,vy:-6,sheet:0});
  finish(t,{vig:.85});
  if(u>tagAt){const k=easeOutBack(seg(u,tagAt,tagAt+.35));ctx.setTransform(1,0,0,1,0,0);ctx.save();ctx.globalAlpha=seg(u,tagAt,tagAt+.15);
    ctx.strokeStyle='#f2c418';ctx.lineWidth=6;ctx.beginPath();ctx.moveTo(420,980);ctx.lineTo(lerp(420,880,k),lerp(980,1060,k));ctx.stroke();ctx.fillStyle='#f2c418';ctx.beginPath();ctx.arc(lerp(420,880,k),lerp(980,1060,k),12,0,7);ctx.fill();
    ctx.fillStyle='rgba(0,0,0,.75)';ctx.fillRect(70,860,560,120);ctx.font='50px MB';ctx.fillStyle='#f2c418';ctx.fillText('КОНТАКТНЫЙ',100,915);ctx.fillText('РЕЛЬС',100,965);ctx.restore()}
  if(u>voltAt){const k=easeOutBack(seg(u,voltAt,voltAt+.3)),j=(rng(Math.floor(t*20))()-.5)*8;bigCaption('825 В',540+j,620,230,'#e0302a',k,{stroke:22});
    ctx.save();ctx.translate(540,380);ctx.scale(k,k);ctx.fillStyle='#f2c418';ctx.beginPath();ctx.moveTo(0,-90);ctx.lineTo(100,80);ctx.lineTo(-100,80);ctx.closePath();ctx.fill();ctx.strokeStyle='#111';ctx.lineWidth=8;ctx.stroke();
    ctx.fillStyle='#111';ctx.beginPath();ctx.moveTo(10,-40);ctx.lineTo(-25,15);ctx.lineTo(5,15);ctx.lineTo(-10,60);ctx.lineTo(30,0);ctx.lineTo(0,0);ctx.closePath();ctx.fill();ctx.restore()}}

// =====================================================================
// 14. visibility drops in the smoke (05.2–05.3)
// =====================================================================
function visibilityShot(u,d,t,a20){if(!WAGON)buildWagon();camTo(ctx,1.02+.06*ease(u/d),540,760,Math.sin(t*.8)*3,0);
  ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);ctx.drawImage(WAGON.em,0,0);
  const thick=.35+.5*ease(u/d);
  // depth fog: far end vanishes first
  const fg=ctx.createRadialGradient(WCX0,WCY0,10,WCX0,WCY0,lerp(380,820,thick));fg.addColorStop(0,`rgba(62,48,34,${.95})`);fg.addColorStop(1,'rgba(62,48,34,0)');ctx.fillStyle=fg;ctx.fillRect(0,0,W,H);
  smoke(ctx,t,0,0,W,H,{alpha:.25+.3*thick,scale:1.7,vx:-25,vy:-6,sheet:1,tint:'rgba(120,90,60,.35)'});
  smoke(ctx,t*.7,0,0,W,1100,{alpha:.2+.25*thick,scale:1.1,vx:20,vy:-12,sheet:2});
  ctx.save();ctx.globalCompositeOperation='lighter';for(const z of[3,6])for(const X of[-.42,.42]){const [x,y]=pj(X,CEIL-.1,z);glow(ctx,x,y,700/z,'255,150,60',.25)}ctx.restore();
  sonyaBack(ctx,t,true);
  finish(t,{vig:.85});
  // HUD: visibility meter
  ctx.setTransform(1,0,0,1,0,0);const m=u<a20?30:20,fl=u>a20&&u<a20+.25;ctx.fillStyle='rgba(8,8,8,.8)';ctx.fillRect(80,300,520,170);ctx.strokeStyle=m===20?'rgba(255,60,45,.6)':'rgba(255,150,40,.4)';ctx.lineWidth=3;ctx.strokeRect(80,300,520,170);
  ledText(ctx,'ВИДИМОСТЬ',100,318,3.4,{});ledText(ctx,m+' М',100,378,4.6,{col:m===20?'255,60,45':'255,150,40'});
  if(fl)glitch(t,t-.01,t+.01,.35)}

// =====================================================================
// 15. he pries the doors open (05.7–05.9)
// =====================================================================
function pryShot(u,d,t,jerks){if(!WAGON)buildWagon();
  // gap grows in jerks
  let gap=20;for(const [a,amt] of jerks)gap+=amt*easeOutBack(seg(u,a,a+.35));
  let sh=0;for(const [a] of jerks)if(u>a&&u<a+.3)sh=Math.sin(u*80)*10*(1-(u-a)/.3);
  camTo(ctx,1.0+.06*ease(u/d),540,900,sh,0);
  // tunnel beyond the gap
  ctx.fillStyle='#030404';ctx.fillRect(0,0,W,H);
  ctx.save();ctx.beginPath();ctx.rect(540-gap/2,0,gap,H);ctx.clip();ctx.drawImage(RAIL,-200,-300,W*1.4,H*1.4);ctx.fillStyle='rgba(0,0,0,.55)';ctx.fillRect(0,0,W,H);
  smoke(ctx,t,0,0,W,H,{alpha:.3,scale:1.4,vx:-30,vy:-12,sheet:0});ctx.restore();
  // two door leaves
  for(const sd of[-1,1]){const x0=sd<0?-60:540+gap/2,x1=sd<0?540-gap/2:W+60;
    ctx.save();ctx.beginPath();ctx.rect(x0,0,x1-x0,H);ctx.clip();texFill(ctx,x0,0,x1-x0,H,'#a9b0ac',150+sd,{grime:.8,specks:.7,streaks:16});
    const wx0=sd<0?x1-400:x0+80,wx1=sd<0?x1-80:x0+400;ctx.fillStyle='#0b0f0e';ctx.fillRect(wx0,260,wx1-wx0,620);ctx.fillStyle='rgba(255,255,255,.07)';ctx.beginPath();ctx.moveTo(wx0,800);ctx.lineTo(wx0+160,260);ctx.lineTo(wx0+230,260);ctx.lineTo(wx0+40,880);ctx.lineTo(wx0,880);ctx.fill();
    ctx.strokeStyle='#2a2e2c';ctx.lineWidth=16;ctx.strokeRect(wx0,260,wx1-wx0,620);
    ctx.fillStyle='#e8c21a';ctx.fillRect(sd<0?x1-330:x0+90,1180,240,110);ctx.fillStyle='#111';ctx.font='bold 26px '+MONO;ctx.fillText('НЕ ПРИСЛОНЯТЬСЯ',sd<0?x1-322:x0+98,1245);
    ctx.fillStyle='#050505';ctx.fillRect(sd<0?x1-26:x0,0,26,H);ctx.restore()}
  ctx.setTransform(1,0,0,1,0,0);ctx.globalCompositeOperation='multiply';ctx.fillStyle='#6a4520';ctx.fillRect(0,0,W,H);ctx.globalCompositeOperation='source-over';
  camTo(ctx,1.0+.06*ease(u/d),540,900,sh,0);amberLight(ctx,540,200,900,.3,t);
  // hands: fingers hooked into the rubber edges
  const g=ctx;for(const sd of[-1,1]){const ex=540+sd*gap/2,sk=SKIN_AMB;
    sleeve(g,[[540+sd*700,1500],[ex+sd*160,1000]],210,'#15181b');
    g.fillStyle=sk[0];g.beginPath();g.ellipse(ex+sd*110,950,100,130,sd*.3,0,7);g.fill();blob(g,ex+sd*90,920,70,70,'230,170,130',.2);
    for(let i=0;i<4;i++){const y=820+i*62;finger(g,ex+sd*120,y,ex-sd*14,y+10,46,sk)}
    finger(g,ex+sd*150,1050,ex+sd*40,1090,50,sk);
    g.strokeStyle='rgba(30,15,10,.5)';g.lineWidth=3;for(let i=0;i<4;i++){g.beginPath();g.moveTo(ex+sd*40,826+i*62);g.lineTo(ex+sd*60,840+i*62);g.stroke()}}
  smoke(ctx,t,0,0,W,700,{alpha:.12,scale:1.5,vx:-12,vy:-8,sheet:1});
  finish(t,{vig:.82});
  for(const [a] of jerks)if(u>a&&u<a+.7){const k=(u-a)/.7;bigCaption('СКР-Р-РИП',540+Math.sin(a*7)*120,560-40*k,110,`rgba(242,196,24,${1-k*k})`,1,{font:'CV',rot:-.1+Math.sin(a)*.08,stroke:10})}}

// =====================================================================
// 16. view out of the open doors: his beam goes into the tunnel (08.1)
// =====================================================================
function doorwayOut(u,d,t,jumpAt){camTo(ctx,1.02+.04*ease(u/d),540,900,0,0);
  ctx.fillStyle='#020303';ctx.fillRect(0,0,W,H);
  const k=ease(seg(u,jumpAt+.5,d));// walking away
  // tunnel through the opening
  const ox0=200,ox1=880,oy0=300,oy1=1500;ctx.save();ctx.beginPath();ctx.rect(ox0,oy0,ox1-ox0,oy1-oy0);ctx.clip();
  ctx.globalAlpha=.4;ctx.drawImage(RAIL,-300,-200,W*1.5,H*1.4);ctx.globalAlpha=1;
  // beam
  const bx=lerp(560,600,k),by=lerp(1150,780,k),bs=lerp(1,.25,k);
  const L=layer();L.drawImage(RAIL,-300,-200,W*1.5,H*1.4);L.globalCompositeOperation='destination-in';const sweep=Math.sin(u*1.7)*200*bs;
  const gr=L.createRadialGradient(bx+sweep,by-200*bs,10,bx+sweep,by-200*bs,500*bs+60);gr.addColorStop(0,'#000');gr.addColorStop(1,'rgba(0,0,0,0)');L.fillStyle=gr;L.fillRect(0,0,W,H);
  ctx.globalAlpha=.9;ctx.drawImage(TMP,0,0);ctx.globalAlpha=1;
  smoke(ctx,t,ox0,oy0,ox1-ox0,oy1-oy0,{alpha:.35,scale:1.3,vx:-20,vy:-10,sheet:2,tint:'rgba(60,50,40,.3)'});
  // figure walking away
  if(u>jumpAt){const s=lerp(1.0,.22,k),fx=bx,fy=lerp(1520,820,k)+(u<jumpAt+.5?-Math.sin(seg(u,jumpAt,jumpAt+.5)*Math.PI)*60:0);const step=Math.sin(u*9)*.06;
    ctx.save();ctx.translate(fx,fy);ctx.scale(s*420,s*420);ctx.fillStyle='#050606';
    ctx.beginPath();ctx.ellipse(0,-1.62,.13,.15,0,0,7);ctx.fill();ctx.beginPath();ctx.moveTo(-.25,-1.45);ctx.quadraticCurveTo(0,-1.55,.25,-1.45);ctx.lineTo(.22,-.8);ctx.lineTo(-.22,-.8);ctx.fill();
    ctx.beginPath();ctx.moveTo(-.18,-.82);ctx.lineTo(-.1+step,0);ctx.lineTo(-.02+step,0);ctx.lineTo(0,-.7);ctx.lineTo(.02-step,0);ctx.lineTo(.1-step,0);ctx.lineTo(.18,-.82);ctx.fill();
    ctx.restore();ctx.save();ctx.globalCompositeOperation='lighter';glow(ctx,fx+sweep*.1,fy-s*560,260*s+40,'220,230,255',1);ctx.restore()}
  ctx.restore();
  // open door leaves + frame, amber interior foreground
  texFill(ctx,0,0,ox0,H,'#5a5e5a',161,{grime:.8});texFill(ctx,ox1,0,W-ox1,H,'#5a5e5a',162,{grime:.8});texFill(ctx,0,0,W,oy0,'#646a66',163,{grime:.8});
  ctx.fillStyle='#050505';ctx.fillRect(ox0-22,oy0,22,oy1-oy0);ctx.fillRect(ox1,oy0,22,oy1-oy0);
  ctx.fillStyle='#3e3c38';ctx.fillRect(0,oy1,W,H-oy1);texFill(ctx,0,oy1,W,H-oy1,'rgba(0,0,0,0)',164,{grime:.9,specks:1});ctx.fillStyle='#8a8478';ctx.fillRect(ox0-30,oy1,ox1-ox0+60,16);
  ctx.setTransform(1,0,0,1,0,0);ctx.globalCompositeOperation='multiply';ctx.fillStyle='#5a3a1c';ctx.fillRect(0,0,W,H);ctx.globalCompositeOperation='source-over';
  amberLight(ctx,540,120,900,.35,t);
  // Sonya's shoulder at the edge (back view), headphones
  ctx.save();ctx.translate(-120,280);sonyaBack(ctx,t,true);ctx.restore();
  finish(t,{vig:.85})}

// =====================================================================
// 17. choice plates, fork card, end card (08.3–end)
// =====================================================================
function choicePlate(g,letter,line1,line2,col,y,k){g.save();g.translate(540,y);g.scale(k,k);
  g.fillStyle='rgba(0,0,0,.72)';g.beginPath();g.roundRect(-470,-150,940,300,30);g.fill();g.strokeStyle=col;g.lineWidth=6;g.stroke();
  g.fillStyle=col;g.beginPath();g.roundRect(-440,-120,240,240,24);g.fill();g.font='200px MB';g.fillStyle=col==='#ffffff'?'#111':'#fff';g.textAlign='center';g.textBaseline='middle';g.fillText(letter,-320,10);
  g.textAlign='left';g.font='58px MB';g.fillStyle='#fff';g.fillText(line1,-170,-36);g.fillStyle=col==='#ffffff'?'#d9d2c4':'#ff8a80';g.fillText(line2,-170,40);g.restore()}
function plateA(u,d,t){if(!WAGON)buildWagon();camTo(ctx,1.04+.04*ease(u/d),540,760,0,0);ctx.drawImage(WAGON.em,0,0);smoke(ctx,t,0,0,W,H,{alpha:.25,scale:1.6,vx:-14,vy:-6,sheet:1});
  finish(t,{vig:.9});ctx.setTransform(1,0,0,1,0,0);ctx.fillStyle='rgba(0,0,0,.35)';ctx.fillRect(0,0,W,H);
  choicePlate(ctx,'А','ОСТАТЬСЯ','В ВАГОНЕ И ЖДАТЬ','#ffffff',900,easeOutBack(seg(u,.1,.45)))}
function plateB(u,d,t){camTo(ctx,1.4+.1*ease(u/d),540,1500,0,0);ctx.drawImage(RAIL,0,0);smoke(ctx,t,0,0,W,H,{alpha:.3,scale:1.6,vx:-20,vy:-6,sheet:0});
  ctx.setTransform(1,0,0,1,0,0);ctx.save();ctx.globalCompositeOperation='lighter';glow(ctx,600,700,500,'220,230,255',.18);ctx.restore();finish(t,{vig:.9});
  ctx.fillStyle='rgba(60,0,0,.3)';ctx.fillRect(0,0,W,H);
  choicePlate(ctx,'Б','ВЫЙТИ ЗА НИМ','В ТОННЕЛЬ','#e0302a',900,easeOutBack(seg(u,.1,.45)))}
function forkShot(u,d,t,nextAt){if(!WAGON)buildWagon();ctx.setTransform(1,0,0,1,0,0);
  ctx.save();ctx.beginPath();ctx.rect(0,0,W,H/2);ctx.clip();ctx.setTransform(1,0,0,1,0,-300);ctx.drawImage(WAGON.em,0,0);ctx.restore();
  ctx.save();ctx.beginPath();ctx.rect(0,H/2,W,H/2);ctx.clip();ctx.setTransform(1.3,0,0,1.3,-160,-280);ctx.drawImage(RAIL,0,0);ctx.restore();
  ctx.setTransform(1,0,0,1,0,0);smoke(ctx,t,0,0,W,H,{alpha:.2,scale:1.6,vx:-14,vy:-6,sheet:2});finish(t,{vig:.9});
  ctx.fillStyle='rgba(0,0,0,.4)';ctx.fillRect(0,0,W,H);ctx.fillStyle='#e0302a';ctx.fillRect(0,H/2-4,W,8);
  choicePlate(ctx,'А','ОСТАТЬСЯ','В ВАГОНЕ И ЖДАТЬ','#ffffff',560,1);choicePlate(ctx,'Б','ВЫЙТИ ЗА НИМ','В ТОННЕЛЬ','#e0302a',1260,1);
  const k=easeOutBack(seg(u,.1,.4));ctx.save();ctx.translate(540,H/2);ctx.scale(k,k);ctx.fillStyle='#111';ctx.beginPath();ctx.roundRect(-420,-70,840,140,70);ctx.fill();ctx.strokeStyle='#f2c418';ctx.lineWidth=6;ctx.stroke();
  ctx.font='52px MB';ctx.fillStyle='#f2c418';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(u<nextAt?'ПИШИТЕ А ИЛИ Б':'ВЫБИРАЕТЕ ВЫ',0,4);ctx.restore();
  if(u>nextAt){const k2=seg(u,nextAt,nextAt+.3);ctx.globalAlpha=k2;ctx.font='44px MB';ctx.textAlign='center';ctx.fillStyle='#fff';ctx.lineWidth=12;ctx.strokeStyle='#000';ctx.strokeText('СЛЕДУЮЩАЯ СЕРИЯ —',540,1500);ctx.fillText('СЛЕДУЮЩАЯ СЕРИЯ —',540,1500);
    ctx.strokeText('ПО ВАШЕМУ ВЫБОРУ',540,1560);ctx.fillText('ПО ВАШЕМУ ВЫБОРУ',540,1560);ctx.globalAlpha=1;ctx.textAlign='left'}
  else{ctx.font='44px MB';ctx.textAlign='center';ctx.fillStyle='#fff';ctx.lineWidth=12;ctx.strokeStyle='#000';ctx.strokeText('В КОММЕНТАРИЯХ',540,1500);ctx.fillText('В КОММЕНТАРИЯХ',540,1500);ctx.textAlign='left'}}
function endCard(u,d,t){ctx.setTransform(1,0,0,1,0,0);ctx.fillStyle='#050606';ctx.fillRect(0,0,W,H);smoke(ctx,t,0,0,W,H,{alpha:.22,scale:2,vx:-10,vy:-6,sheet:1});
  ctx.save();ctx.globalCompositeOperation='lighter';glow(ctx,540,900,800,'255,140,40',.16);ctx.restore();finish(t,{vig:.8});
  const k=easeOutBack(seg(u,.05,.4));ctx.save();ctx.translate(540,760);ctx.scale(k,k);ctx.font='190px MB';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillStyle='#fff';ctx.fillText('ВЫБОР',0,0);ctx.restore();
  const q=easeOutBack(seg(u,.35,.65));ctx.save();ctx.translate(540,1000);ctx.scale(q,q);ctx.font='260px MB';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillStyle='#e0302a';ctx.fillText('?',0,0);ctx.restore();
  ctx.globalAlpha=seg(u,.6,.9);ctx.font='48px MB';ctx.textAlign='center';ctx.fillStyle='#d9d2c4';ctx.fillText('ТОННЕЛЬ · СЕРИЯ 1',540,1220);
  ctx.font='64px MB';ctx.fillStyle='#f2c418';ctx.fillText('А или Б?',540,1340);ctx.globalAlpha=1;ctx.textAlign='left'}

// =====================================================================
// shot list (cuts sit ~0.15 s before the phrase starts)
// =====================================================================
const c=id=>ps(id)-.15;
const SHOTS=[
 {a:0,b:c('01.3'),f:(u,d,t)=>sceneA(u)},
 {a:c('01.3'),b:c('01.4'),f:(u,d,t)=>{const k=ease(seg(u,.1,d));CAM={z:lerp(1,1.45,k),ay:lerp(820,1780,k)};sceneA(u+4.7);CAM=null},tr:'none'},
 {a:c('01.4'),b:9.95,f:u=>sceneB(u+3),tr:'glitch'},
 {a:9.95,b:10.9,f:u=>sceneC(u+4.6),tr:'flash'},
 {a:10.9,b:12.0,f:u=>sceneD(u+6),tr:'flash'},
 {a:12.0,b:13.7,f:u=>sceneE(u+8),tr:'flash'},
 {a:13.7,b:c('02.1'),f:u=>sceneF(u+10),tr:'flash'},
 {a:c('02.1'),b:c('02.3'),f:(u,d,t)=>{sonyaClose(u,d,t,{look:[.25,.15]});nameTag(t,ps('02.1')+.1,'СОНЯ',t>ps('02.2')?'19 ЛЕТ':null)},tr:'black',hud:1},
 {a:c('02.3'),b:c('02.4'),f:wagonLitShot,tr:'flash'},
 {a:c('02.4'),b:c('02.5'),f:mapShot,tr:'glitch'},
 {a:c('02.5'),b:c('02.6'),f:phoneShot,tr:'flash'},
 {a:c('02.6'),b:c('03.1'),f:flashlightShot,tr:'black'},
 {a:c('03.1'),b:c('03.3'),f:(u,d,t)=>{caneShot(u,d,t,[1.05,1.55,2.05,ps('03.2')-c('03.1')+.55]);nameTag(t,ps('03.1')+.1,'МИХАЛЫЧ',null,{col:'#e8e2d6'})},tr:'flash',hud:1},
 {a:c('03.3'),b:c('03.5'),f:(u,d,t)=>streamShot(u,d,t,'talk'),tr:'glitch'},
 {a:c('03.5'),b:c('03.7'),f:(u,d,t)=>radioShot(u,d,t,ps('03.6')-c('03.5')),tr:'flash',hud:1},
 {a:c('03.7'),b:c('04.1'),f:(u,d,t)=>speakerShot(u,d,t,'dead'),tr:'black'},
 {a:c('04.1'),b:c('04.2'),f:(u,d,t)=>sonyaClose(u,d,t,{look:[-.4,0],z0:1.05,z1:1.15,rim:1}),tr:'flash',hud:1},
 {a:c('04.2'),b:c('04.4'),f:(u,d,t)=>buttonShot(u,d,t,ps('04.3')-c('04.2')+.05),tr:'flash'},
 {a:c('04.4'),b:c('04.5'),f:plateShot,tr:'flash'},
 {a:c('04.5'),b:c('04.6')+1.75,f:(u,d,t)=>stepsShot(u,d,t,ps('04.5')-c('04.5')+.6,ps('04.6')-c('04.5')+.25),tr:'flash'},
 {a:c('04.6')+1.75,b:c('05.1'),f:(u,d,t)=>railShot(u,d,t,ps('04.6')+2.05-(c('04.6')+1.75),ps('04.7')-(c('04.6')+1.75)),tr:'flash'},
 {a:c('05.1'),b:c('05.2'),f:(u,d,t)=>buttonShot(u,d,t,-9,{after:1}),tr:'black'},
 {a:c('05.2'),b:c('05.4'),f:(u,d,t)=>visibilityShot(u,d,t,ps('05.3')+1.6-c('05.2')),tr:'flash',hud:1},
 {a:c('05.4'),b:c('05.5'),f:(u,d,t)=>streamShot(u,d,t,'read'),tr:'glitch'},
 {a:c('05.5'),b:c('05.7'),f:chatShot,tr:'none'},
 {a:c('05.7'),b:c('05.10'),f:(u,d,t)=>pryShot(u,d,t,[[.9,60],[ps('05.8')-c('05.7')+.2,90],[ps('05.9')-c('05.7')+.15,240]]),tr:'flash',hud:1},
 {a:c('05.10'),b:c('06.1'),f:(u,d,t)=>speakerShot(u,d,t,'alive'),tr:'glitch'},
 {a:c('06.1'),b:c('07.1'),f:(u,d,t)=>speakerShot(u,d,t,'voice'),tr:'none'},
 {a:c('07.1'),b:c('08.1'),f:(u,d,t)=>sonyaClose(u,d,t,{look:[.1,.8],lookTo:[.05,-.7],lookAt:1.3,z0:1.05,z1:1.3,ay:560,open:.7,openTo:1}),tr:'black'},
 {a:c('08.1'),b:c('08.2'),f:(u,d,t)=>doorwayOut(u,d,t,.5),tr:'flash',hud:1},
 {a:c('08.2'),b:c('08.3'),f:(u,d,t)=>sceneA(u+.3),tr:'flash'},
 {a:c('08.3'),b:c('08.4'),f:plateA,tr:'glitch'},
 {a:c('08.4'),b:c('08.5'),f:plateB,tr:'glitch'},
 {a:c('08.5'),b:pe('08.6')+.2,f:(u,d,t)=>forkShot(u,d,t,ps('08.6')-c('08.5')),tr:'flash'},
 {a:pe('08.6')+.2,b:END+.1,f:endCard,tr:'flash'}];

// ---------- subtitles (manual groups, timed by character share) ----------
const SUBTXT={'01.1':'ЧЕРЕЗ 7 МИНУТ','01.2':'СОНЯ БУДЕТ СТОЯТЬ|ВОТ ЗДЕСЬ','01.3':'НАД ЧЁРНЫМ ТОННЕЛЕМ','01.4':'А ПОКА —|00:47','01.5':'ПОЕЗД ВСТАЛ|СВЕТ ПОГАС|ПАХНЕТ ДЫМОМ',
 '01.6':'ЧТО СОНЯ|СДЕЛАЕТ ДАЛЬШЕ…','01.7':'РЕШАЕТЕ ВЫ','02.1':'ЭТО СОНЯ','02.2':'19 ЛЕТ','02.3':'ПОСЛЕДНИЙ ПОЕЗД|ПОСЛЕ СМЕНЫ|В КОФЕЙНЕ',
 '02.4':'ДО ЛЮБОЙ СТАНЦИИ —|ПОД КИЛОМЕТР|ТЕМНОТЫ','02.5':'ЗАРЯД ТЕЛЕФОНА —|23 %','02.6':'ЭТО ЕЁ|ЕДИНСТВЕННЫЙ ФОНАРЬ','03.1':'МИХАЛЫЧ|СТУЧИТ ТРОСТЬЮ В ПОЛ',
 '03.2':'«СЕЙЧАС ПОЕДЕМ»','03.3':'ПАРЕНЬ В КАПЮШОНЕ|УЖЕ В ЭФИРЕ','03.4':'«НАС ТУТ|ЗАМУРОВАЛИ»','03.5':'А ЖЕНЩИНА|В ФОРМЕ|МЕТРОПОЛИТЕНА…',
 '03.6':'МОЛЧА ПРЯЧЕТ|РАЦИЮ В КАРМАН','03.7':'МАШИНИСТ МОЛЧИТ','03.8':'НИ ОБЪЯВЛЕНИЯ','03.9':'НИЧЕГО','04.1':'СОНЯ ДЕЛАЕТ|ПРАВИЛЬНО',
 '04.2':'КНОПКА|«СВЯЗЬ С МАШИНИСТОМ»|У ДВЕРЕЙ','04.3':'НАЖАТЬ','04.4':'НАЗВАТЬ|НОМЕР ВАГОНА','04.5':'СКАЗАТЬ,|ЧТО СЛУЧИЛОСЬ',
 '04.6':'И ДВЕРИ САМИМ|НЕ ОТКРЫВАТЬ:|ВНИЗУ|КОНТАКТНЫЙ РЕЛЬС','04.7':'825 ВОЛЬТ','05.1':'В ДИНАМИКЕ —|ТИШИНА','05.2':'А ДЫМ ВСЁ ГУЩЕ',
 '05.3':'ВИДИМОСТЬ —|30 МЕТРОВ…|20','05.4':'ПАРЕНЬ ЧИТАЕТ ЧАТ —|И ЗАМОЛКАЕТ','05.5':'КТО-ТО ПИШЕТ:','05.6':'«КАБИНА ПУСТАЯ»',
 '05.7':'ОН РАЗЖИМАЕТ|ДВЕРИ РУКАМИ','05.8':'«Я ТУТ СДЫХАТЬ|НЕ СОБИРАЮСЬ»','05.9':'СТВОРКИ ПОДДАЮТСЯ','05.10':'И ТОГДА|ДИНАМИК ОЖИВАЕТ',
 '05.11':'ГОЛОС','05.12':'СПОКОЙНЫЙ','07.1':'СВОЁ ИМЯ|ОНА НИКОМУ|НЕ НАЗЫВАЛА','08.1':'ПАРЕНЬ СПРЫГИВАЕТ|ВНИЗ|И УХОДИТ В ТЕМНОТУ','08.2':'СОНЯ СТОИТ|НАД ПРОЁМОМ'};
const YEL=/СОНЯ|19 ЛЕТ|00:47|23 %|7 МИНУТ|МИХАЛЫЧ|30 МЕТРОВ|^20$|ГОЛОС/,RED=/РЕШАЕТЕ ВЫ|825|КАБИНА ПУСТАЯ|КОНТАКТНЫЙ|ТЕМНОТ|ЗАМУРОВАЛИ|НЕ ОТКРЫВАТЬ|ТИШИНА|НЕ НАЗЫВАЛА|НИЧЕГО/;
const SUBS_EP=[];{const ph=TL.phr;ph.forEach((p,i)=>{const s=SUBTXT[p.id];if(!s)return;const parts=s.split('|'),tot=parts.reduce((a,x)=>a+x.length+3,0);
  let acc=0;const nextS=i+1<ph.length?ph[i+1].s:END;
  parts.forEach((x,j)=>{const s0=p.s-.05+(p.e-p.s)*acc/tot;acc+=x.length+3;const e0=j===parts.length-1?Math.min(p.e+.35,nextS-.08):p.s-.05+(p.e-p.s)*acc/tot;
    SUBS_EP.push({s:s0,e:e0,txt:x,col:RED.test(x)?'#e0302a':(YEL.test(x)?'#f2c418':'#fff')})})})}
function subtitleFit(t,items){for(const it of items){if(t<it.s||t>it.e)continue;const k=easeOut(seg(t,it.s,it.s+.12));
  ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.font='76px MB';const w=ctx.measureText(it.txt).width,fit=Math.min(1,900/w);
  ctx.textAlign='center';ctx.textBaseline='middle';ctx.translate(540,1480);ctx.scale((.85+.15*k)*fit,(.85+.15*k)*fit);ctx.globalAlpha=k;
  ctx.lineWidth=14;ctx.strokeStyle='rgba(0,0,0,.85)';ctx.lineJoin='round';ctx.strokeText(it.txt,0,0);ctx.fillStyle=it.col;ctx.fillText(it.txt,0,0);ctx.restore()}}

function renderFrame(t){ctx.setTransform(1,0,0,1,0,0);ctx.globalAlpha=1;ctx.globalCompositeOperation='source-over';ctx.filter='none';ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);CAM=null;ctx.textAlign='left';ctx.textBaseline='alphabetic';
  let i=SHOTS.findIndex(s=>t>=s.a&&t<s.b);if(i<0)i=SHOTS.length-1;const S=SHOTS[i],u=t-S.a,d=S.b-S.a;
  S.f(u,d,t);
  ctx.setTransform(1,0,0,1,0,0);ctx.globalAlpha=1;ctx.globalCompositeOperation='source-over';ctx.filter='none';
  if(S.hud)ledHud('СТОИМ '+storyClock(t));
  // transitions into this shot
  if(i>0){if(S.tr==='flash')flash(u,0,'255,225,185',.14,.55);else if(S.tr==='glitch')glitch(t,S.a,S.a+.12,.8);else if(S.tr==='black'&&u<.25){ctx.fillStyle=`rgba(0,0,0,${1-u/.25})`;ctx.fillRect(0,0,W,H)}}
  // and the cold-open specials from the test cut
  glitch(t,2.92,3.0,.6);glitch(t,c('01.4')-.08,c('01.4'),1);
  subtitleFit(t,SUBS_EP);
  // fade out at the very end
  if(t>END-.6){ctx.fillStyle=`rgba(0,0,0,${seg(t,END-.6,END)})`;ctx.fillRect(0,0,W,H)}}
