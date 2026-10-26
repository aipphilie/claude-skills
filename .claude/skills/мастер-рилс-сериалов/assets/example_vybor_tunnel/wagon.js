// ===== D — Moscow metro car interior in real perspective =====
// camera in the aisle, eye height 1.6 m. X right, Y down (floor +1.6), Z forward
const WF=1050,WCX0=540,WCY0=760;
const pj=(X,Y,Z)=>[WCX0+WF*X/Z,WCY0+WF*Y/Z];
const FLOOR=1.6,CEIL=-.52,HW=1.36,SEATY=1.6-.46,SEATD=.5;
function q(g,pts,fill){g.beginPath();pts.forEach((p,i)=>{const [x,y]=pj(...p);i?g.lineTo(x,y):g.moveTo(x,y)});g.closePath();g.fillStyle=fill;g.fill()}
function ln(g,a,b,col,w){const [x0,y0]=pj(...a),[x1,y1]=pj(...b);g.strokeStyle=col;g.lineWidth=w;g.beginPath();g.moveTo(x0,y0);g.lineTo(x1,y1);g.stroke()}
const fogc=(Z,a=1)=>`rgba(18,20,20,${clamp((Z-3)/22,0,.75)*a})`;
// car layout along Z: doors and seat blocks
const DOORS=[[2.3,3.6],[8.4,9.7],[14.5,15.8]],SEATS=[[3.8,8.2],[9.9,14.3],[16,19.4]],ZEND=20;
function wagonLit(){const c=mk(),g=c.getContext('2d'),R=rng(41);
  g.fillStyle='#cfd4d0';g.fillRect(0,0,W,H);
  // end wall
  const zE=ZEND;q(g,[[-HW,CEIL,zE],[HW,CEIL,zE],[HW,FLOOR,zE],[-HW,FLOOR,zE]],'#b9bfbb');
  q(g,[[-.45,-.2,zE],[.45,-.2,zE],[.45,FLOOR,zE],[-.45,FLOOR,zE]],'#7d8783');q(g,[[-.35,-.1,zE],[.35,-.1,zE],[.35,.6,zE],[-.35,.6,zE]],'#151a19');
  // floor
  let [a,b]=[pj(0,FLOOR,1.2),pj(0,FLOOR,zE)];let gr=g.createLinearGradient(0,a[1],0,b[1]);gr.addColorStop(0,'#55534d');gr.addColorStop(1,'#7c7a72');
  q(g,[[-HW,FLOOR,1],[HW,FLOOR,1],[HW,FLOOR,zE],[-HW,FLOOR,zE]],gr);
  for(let i=0;i<1400;i++){const X=(R()*2-1)*HW,Z=1.2+R()*18;const [x,y]=pj(X,FLOOR,Z);g.fillStyle=R()<.5?'rgba(255,255,255,.18)':'rgba(0,0,0,.2)';const s=Math.max(1,6/Z);g.fillRect(x,y,s*1.6,s*.6)}
  for(const X of[-.6,0,.6])ln(g,[X,FLOOR,1],[X,FLOOR,zE],'rgba(0,0,0,.12)',2);
  g.save();g.filter='blur(18px)';for(const X of[-.42,.42])q(g,[[X-.12,FLOOR,1.5],[X+.12,FLOOR,1.5],[X+.04,FLOOR,zE],[X-.04,FLOOR,zE]],'rgba(255,255,255,.16)');g.restore();
  // ceiling
  gr=g.createLinearGradient(0,0,0,WCY0);gr.addColorStop(0,'#eef1ee');gr.addColorStop(1,'#c3c9c5');
  q(g,[[-HW*.78,CEIL-.12,1],[HW*.78,CEIL-.12,1],[HW*.78,CEIL-.12,zE],[-HW*.78,CEIL-.12,zE]],gr);
  for(const s of[-1,1])q(g,[[s*HW*.78,CEIL-.12,1],[s*HW,CEIL+.12,1],[s*HW,CEIL+.12,zE],[s*HW*.78,CEIL-.12,zE]],'#d9ddda');
  for(let z=1.5;z<zE;z+=1.2)ln(g,[-HW*.78,CEIL-.12,z],[HW*.78,CEIL-.12,z],'rgba(0,0,0,.07)',2);
  // walls (both sides)
  for(const s of[-1,1]){const X=s*HW;
    gr=g.createLinearGradient(...pj(X,0,1.2),...pj(X,0,zE));gr.addColorStop(0,'#e3e6e2');gr.addColorStop(1,'#aeb4b0');
    q(g,[[X,CEIL+.12,1],[X,CEIL+.12,zE],[X,FLOOR,zE],[X,FLOOR,1]],gr);
    // ad/map strip above windows
    q(g,[[X,-.38,1],[X,-.38,zE],[X,-.12,zE],[X,-.12,1]],'#f4f2ea');
    for(let z=1.3;z<zE-.5;z+=1.6){q(g,[[X,-.36,z],[X,-.36,z+1.3],[X,-.14,z+1.3],[X,-.14,z]],['#c33a2c','#2f6fb5','#2f8f5a','#e0a51c'][Math.floor(z)%4]);
      q(g,[[X,-.33,z+.08],[X,-.33,z+1.2],[X,-.17,z+1.2],[X,-.17,z+.08]],'rgba(255,255,255,.55)')}
    // windows along the whole length (behind seats)
    for(const [z0,z1] of SEATS){q(g,[[X,-.1,z0+.15],[X,-.1,z1-.15],[X,.62,z1-.15],[X,.62,z0+.15]],'#0c1110');
      for(let k=0;k<3;k++)ln(g,[X,-.04+k*.06,z0+.2],[X,-.07+k*.06,z1-.2],'rgba(40,45,42,.9)',Math.max(1,10/z0));// tunnel cables outside
      ln(g,[X,.55,z0+.4],[X,0,z0+1.4],'rgba(255,255,255,.10)',Math.max(1,14/z0));
      ln(g,[X,-.1,z0+.15],[X,-.1,z1-.15],'#8c938f',Math.max(1,10/z0));ln(g,[X,.62,z0+.15],[X,.62,z1-.15],'#8c938f',Math.max(1,10/z0))}
    // doors
    for(const [z0,z1] of DOORS){const zm=(z0+z1)/2;
      q(g,[[X,CEIL+.16,z0],[X,CEIL+.16,z1],[X,FLOOR,z1],[X,FLOOR,z0]],'#8f9792');
      for(const [za,zb] of [[z0+.05,zm-.01],[zm+.01,z1-.05]]){q(g,[[X,-.3,za],[X,-.3,zb],[X,FLOOR,zb],[X,FLOOR,za]],'#a9b0ac');
        q(g,[[X,-.2,za+.12],[X,-.2,zb-.12],[X,.55,zb-.12],[X,.55,za+.12]],'#101514');
        q(g,[[X,.85,za+.15],[X,.85,za+.45],[X,1.0,za+.45],[X,1.0,za+.15]],'#e8c21a')}
      ln(g,[X,-.3,zm],[X,FLOOR,zm],'#1a1d1c',Math.max(2,18/zm));
      q(g,[[X,-.5,z0+.3],[X,-.5,z1-.3],[X,-.34,z1-.3],[X,-.34,z0+.3]],'#121615');// info screen
      q(g,[[X,-.48,z0+.34],[X,-.48,z1-.34],[X,-.36,z1-.34],[X,-.36,z0+.34]],'#1f4f86')}
    // seats: cushions + backs + dividers
    for(const [z0,z1] of SEATS){const n=Math.round((z1-z0)/.52);
      q(g,[[X,SEATY-.02,z0],[X,SEATY-.02,z1],[X,FLOOR,z1],[X,FLOOR,z0]],'#3b4148');
      q(g,[[X-s*SEATD,SEATY,z0],[X-s*SEATD,SEATY,z1],[X-s*SEATD,FLOOR-.06,z1],[X-s*SEATD,FLOOR-.06,z0]],'#2c3238');
      for(let i=0;i<n;i++){const za=z0+i*(z1-z0)/n+.02,zb=z0+(i+1)*(z1-z0)/n-.02;
        q(g,[[X,SEATY-.04,za],[X,SEATY-.04,zb],[X-s*SEATD,SEATY,zb],[X-s*SEATD,SEATY,za]],i%2?'#2d5d95':'#2a578c');
        q(g,[[X-s*.02,.68,za],[X-s*.02,.68,zb],[X-s*.08,SEATY-.04,zb],[X-s*.08,SEATY-.04,za]],i%2?'#30639e':'#2c5c93');
        ln(g,[X-s*SEATD,SEATY,za],[X-s*SEATD,SEATY,zb],'rgba(255,255,255,.18)',Math.max(1,8/za))}
      // seat-end partitions (glass + chrome)
      for(const z of[z0,z1]){q(g,[[X,.05,z],[X-s*.62,.05,z],[X-s*.62,SEATY,z],[X,SEATY,z]],'rgba(200,215,215,.35)');ln(g,[X-s*.62,.05,z],[X-s*.62,SEATY,z],'#d8dcda',Math.max(2,14/z))}}
  }
  // poles + overhead rails (chrome)
  const chrome=(X,z)=>{const [x0,y0]=pj(X,CEIL-.05,z),[,y1]=pj(X,FLOOR,z),w=Math.max(3,32/z);const gr=g.createLinearGradient(x0-w/2,0,x0+w/2,0);
    gr.addColorStop(0,'#6d716f');gr.addColorStop(.35,'#ffffff');gr.addColorStop(.6,'#b9bdbb');gr.addColorStop(1,'#4d514f');g.fillStyle=gr;g.fillRect(x0-w/2,y0,w,y1-y0)};
  for(const s of[-1,1]){ln(g,[s*.72,-.28,1],[s*.72,-.28,zE],'#d6dad8',6);ln(g,[s*.72,-.29,1],[s*.72,-.29,zE],'#ffffff',2)}
  const poleList=[];for(const [z0,z1] of SEATS)for(const s of[-1,1])for(const z of[z0,z1])poleList.push([s*.72,z]);for(const [z0,z1] of DOORS)poleList.push([0,(z0+z1)/2]);
  poleList.sort((a,b)=>b[1]-a[1]);
  // light strips
  for(const X of[-.42,.42]){q(g,[[X-.07,CEIL-.115,1],[X+.07,CEIL-.115,1],[X+.07,CEIL-.115,zE],[X-.07,CEIL-.115,zE]],'#ffffff')}
  return {c,poles:poleList,chrome}}
// passengers: [X (m), Z (m), kind, colour, extras]
const PEOPLE=[
 {X:-1.06,Z:16.8,sit:1,coat:'#3a3f46',hair:'#2a211b'},{X:1.06,Z:17.5,sit:1,coat:'#5a4636',hair:'#17110e'},{X:-1.06,Z:18.4,sit:1,coat:'#2a2f38',hair:'#3a2a20'},
 {X:-1.06,Z:12.6,sit:1,coat:'#25303a',hair:'#3b2a1e',phone:1},{X:1.06,Z:11.2,sit:1,coat:'#6b2f2a',hair:'#1a1410',hat:'#2f2f2f'},{X:-1.06,Z:10.8,sit:1,coat:'#4b5560',hair:'#d8d2c8'},
 {X:1.06,Z:13.4,sit:1,coat:'#2f3a2f',hair:'#5b4636'},{X:.35,Z:9.0,stand:1,coat:'#2c3a5a',uniform:1,hair:'#2b1d14'},{X:-.4,Z:15.1,stand:1,coat:'#3f3a4a',hair:'#211915'},
 {X:-1.06,Z:7.4,sit:1,coat:'#4a3c30',hair:'#c9c4bb',cane:1},{X:-1.06,Z:5.6,sit:1,coat:'#3c3a38',hair:'#211a15',phone:1},{X:-1.06,Z:4.6,sit:1,coat:'#5d6b52',hair:'#6b4a30'},
 {X:1.06,Z:6.4,sit:1,coat:'#7a6a55',hair:'#3a2a20'},{X:1.06,Z:4.9,sit:1,coat:'#1f2a36',hair:'#141010',phone:1},
 {X:.5,Z:3.3,stand:1,coat:'#1d2125',hood:1,phone:1}];
function person(g,p){const k=WF/p.Z,[fx,fy]=pj(p.X,FLOOR,p.Z),side=p.X<0?1:-1;
  g.save();g.translate(fx,fy);g.scale(k,k);const R=rng(Math.floor(p.Z*10));
  const skin=p.hair==='#c9c4bb'?'#c79a84':['#d2a289','#b98a6f','#e0b8a0'][Math.floor(R()*3)];
  if(p.sit){// seated on the bench: hips at seat height, knees toward the aisle
    g.fillStyle='#1c1f24';g.beginPath();g.moveTo(-.1*side,-.46);g.lineTo(side*.38,-.48);g.lineTo(side*.42,-.02);g.lineTo(side*.32,0);g.lineTo(side*.28,-.38);g.lineTo(-.12*side,-.36);g.closePath();g.fill();// legs
    g.fillStyle='#0d0e10';g.fillRect(side>0?.3:-.46,-.04,.16,.05);
    const tx=-.02*side,ty=-.46;g.fillStyle=p.coat;g.beginPath();g.moveTo(tx-.22,ty+.04);g.lineTo(tx-.2,ty-.5);g.quadraticCurveTo(tx,ty-.6,tx+.2,ty-.5);g.lineTo(tx+.22,ty+.04);g.closePath();g.fill();
    g.fillStyle='rgba(0,0,0,.25)';g.fillRect(tx+(side>0?-.22:.12),ty-.48,.1,.5);
    g.fillStyle=p.coat;g.beginPath();g.ellipse(tx+side*.14,ty-.2,.06,.22,-side*.35,0,7);g.fill();// arm
    if(p.phone){g.fillStyle=skin;g.beginPath();g.arc(tx+side*.22,ty-.2,.035,0,7);g.fill();g.fillStyle='#d9ecff';g.fillRect(tx+side*.2-.025,ty-.27,.05,.08)}
    if(p.cane){g.strokeStyle='#2a1d14';g.lineWidth=.03;g.beginPath();g.moveTo(tx+side*.3,ty-.25);g.lineTo(tx+side*.42,0);g.stroke();g.beginPath();g.arc(tx+side*.27,ty-.27,.04,Math.PI,0);g.stroke()}
    head(g,tx,ty-.72,skin,p,side,p.phone?.4:0)}
  else{// standing, holding the overhead rail
    const jeans='#1b2129';
    for(const sd of[-1,1]){g.fillStyle=jeans;g.beginPath();g.moveTo(sd*.02,-.86);g.lineTo(sd*.15,-.86);g.quadraticCurveTo(sd*.16,-.45,sd*.12,-.06);g.lineTo(sd*.04,-.06);g.quadraticCurveTo(sd*.05,-.45,sd*.02,-.86);g.fill();
      g.fillStyle='#0b0c0d';g.beginPath();g.moveTo(sd*.03,-.07);g.lineTo(sd*.14,-.07);g.quadraticCurveTo(sd*.2,-.03,sd*.19,0);g.lineTo(sd*.03,0);g.fill();g.fillStyle='rgba(255,255,255,.5)';g.fillRect(Math.min(sd*.03,sd*.19),-.012,.16,.012)}
    g.fillStyle='rgba(255,255,255,.06)';g.fillRect(-.13,-.8,.04,.7);
    g.fillStyle=p.coat;g.beginPath();g.moveTo(-.2,-.78);g.quadraticCurveTo(-.23,-1.1,-.21,-1.36);g.quadraticCurveTo(-.17,-1.46,0,-1.47);g.quadraticCurveTo(.17,-1.46,.21,-1.36);g.quadraticCurveTo(.23,-1.1,.2,-.78);g.closePath();g.fill();
    g.fillStyle='rgba(0,0,0,.25)';g.beginPath();g.moveTo(.06,-1.44);g.quadraticCurveTo(.2,-1.4,.2,-.78);g.lineTo(.08,-.78);g.fill();
    g.strokeStyle='rgba(0,0,0,.4)';g.lineWidth=.008;g.beginPath();g.moveTo(0,-1.44);g.lineTo(0,-.8);g.stroke();
    g.fillStyle='rgba(255,255,255,.08)';g.beginPath();g.moveTo(-.2,-1.36);g.quadraticCurveTo(-.17,-1.46,-.05,-1.47);g.lineTo(-.12,-1.3);g.fill();
    // raised arm with sleeve, hand on the overhead rail
    g.strokeStyle=p.coat;g.lineWidth=.095;g.lineCap='round';g.beginPath();g.moveTo(.17,-1.38);g.quadraticCurveTo(.28,-1.6,.25,-1.86);g.stroke();
    g.strokeStyle='rgba(0,0,0,.25)';g.lineWidth=.03;g.beginPath();g.moveTo(.21,-1.4);g.quadraticCurveTo(.31,-1.6,.28,-1.84);g.stroke();
    g.fillStyle=skin;g.beginPath();g.ellipse(.25,-1.9,.04,.05,0,0,7);g.fill();
    // other arm down / with phone
    g.strokeStyle=p.coat;g.lineWidth=.085;g.beginPath();g.moveTo(-.18,-1.36);if(p.phone){g.quadraticCurveTo(-.24,-1.15,-.06,-1.16)}else{g.quadraticCurveTo(-.25,-1.1,-.22,-.86)}g.stroke();
    g.fillStyle=skin;if(p.phone){g.beginPath();g.arc(-.04,-1.17,.035,0,7);g.fill();g.fillStyle='#cfe6ff';g.fillRect(-.06,-1.27,.05,.09)}else{g.beginPath();g.arc(-.22,-.84,.035,0,7);g.fill()}
    if(p.uniform){g.fillStyle='#c8a64a';g.fillRect(-.2,-1.36,.07,.02);g.fillRect(.13,-1.36,.07,.02);g.fillStyle='#e8e8e8';g.beginPath();g.moveTo(-.05,-1.46);g.lineTo(0,-1.36);g.lineTo(.05,-1.46);g.fill();g.fillStyle='#8a1c1c';g.fillRect(-.012,-1.42,.024,.1)}
    head(g,0,-1.6,skin,p,0,p.phone?.5:0)}
  g.restore()}
function head(g,x,y,skin,p,side,down){
  g.fillStyle=skin;g.fillRect(x-.04,y+.08,.08,.08);
  g.fillStyle=skin;g.beginPath();g.ellipse(x,y,.095,.12,0,0,7);g.fill();
  g.fillStyle='rgba(0,0,0,.18)';g.beginPath();g.ellipse(x+.03,y+.02,.07,.11,0,-1.2,1.6);g.fill();
  if(p.hood){g.fillStyle='rgba(0,0,0,.35)';g.beginPath();g.ellipse(x,y,.095,.12,0,0,7);g.fill();g.fillStyle=p.coat;g.beginPath();g.ellipse(x,y-.02,.13,.155,0,Math.PI*.95,Math.PI*2.05);g.lineTo(x+.13,y+.14);g.lineTo(x+.09,y+.14);g.lineTo(x+.09,y-.02);g.quadraticCurveTo(x,y-.12,x-.09,y-.02);g.lineTo(x-.09,y+.14);g.lineTo(x-.13,y+.14);g.closePath();g.fill()}
  else{g.fillStyle=p.hair;g.beginPath();g.ellipse(x,y-.05,.1,.085,0,Math.PI,0);g.fill();g.fillRect(x-.1,y-.06,.03,.1)}
  if(p.hat){g.fillStyle=p.hat;g.beginPath();g.ellipse(x,y-.07,.105,.07,0,Math.PI,0);g.fill()}
  if(p.uniform){g.fillStyle='#1d2a40';g.fillRect(x-.11,y-.12,.22,.05);g.fillRect(x-.08,y-.17,.16,.06);g.fillStyle='#c8a64a';g.fillRect(x-.02,y-.15,.04,.03)}
  g.fillStyle='rgba(20,12,10,.8)';const ey=y+.01+down*.02;g.fillRect(x-.05+side*.02,ey,.025,.012);g.fillRect(x+.025+side*.02,ey,.025,.012)}
let WAGON=null;
function buildWagon(){const w=wagonLit(),g=w.c.getContext('2d');
  // people and poles sorted far -> near
  const items=[...PEOPLE.map(p=>({z:p.Z,f:()=>person(g,p)})),...w.poles.map(([X,z])=>({z,f:()=>w.chrome(X,z)}))].sort((a,b)=>b.z-a.z);
  for(const it of items){it.f();}
  // depth haze
  const hz=g.createRadialGradient(WCX0,WCY0,10,WCX0,WCY0,520);hz.addColorStop(0,'rgba(120,128,124,.45)');hz.addColorStop(1,'rgba(120,128,124,0)');g.fillStyle=hz;g.fillRect(0,0,W,H);
  g.globalAlpha=.35;g.drawImage(SPECK,0,0);g.globalAlpha=1;
  // emergency version: dark amber grade + lamp pools
  const e=mk(),eg=e.getContext('2d');eg.drawImage(w.c,0,0);eg.globalCompositeOperation='multiply';eg.fillStyle='#4a2e14';eg.fillRect(0,0,W,H);
  eg.globalCompositeOperation='screen';
  for(const z of[3,6,9])for(const X of[-.42,.42]){const [x,y]=pj(X,CEIL-.1,z);const r=900/z;const gr=eg.createRadialGradient(x,y+r*.6,0,x,y+r*.6,r*2.2);gr.addColorStop(0,`rgba(255,140,40,${.35*Math.min(1,4/z)})`);gr.addColorStop(1,'rgba(255,140,40,0)');eg.fillStyle=gr;eg.fillRect(x-r*2.2,y-r*1.6,r*4.4,r*4.4)}
  eg.globalCompositeOperation='source-over';
  for(const z of[3,6,9,12,15,18])for(const X of[-.42,.42]){const [x,y]=pj(X,CEIL-.115,z);eg.fillStyle='#ffc36a';eg.fillRect(x-60/z,y-6/z*3,120/z,24/z*2)}
  WAGON={lit:w.c,em:e}}
// Sonya foreground: back of head, bun, headband behind the neck, yellow cup
function sonyaBack(g,t,amber){g.save();g.translate(900,1790);g.scale(1.1,1.1);
  const sk=amber?['#6a4434','#3a2219']:['#c8977d','#7a4f40'];
  g.fillStyle='#15181b';g.beginPath();g.moveTo(-330,320);g.bezierCurveTo(-300,90,-170,40,-60,40);g.lineTo(60,40);g.bezierCurveTo(170,40,300,90,330,320);g.fill();// hoodie shoulders
  g.fillStyle='#202529';g.beginPath();g.ellipse(0,60,190,55,0,0,7);g.fill();// hood roll
  let gr=g.createLinearGradient(-70,0,70,0);gr.addColorStop(0,sk[0]);gr.addColorStop(1,sk[1]);g.fillStyle=gr;
  g.beginPath();g.moveTo(-62,-90);g.quadraticCurveTo(-70,10,-80,55);g.quadraticCurveTo(0,75,80,55);g.quadraticCurveTo(70,10,62,-90);g.closePath();g.fill();// neck (tapered)
  // headband across the BACK of the neck, cups hanging forward at the sides
  g.lineCap='round';g.strokeStyle='#121212';g.lineWidth=30;g.beginPath();g.ellipse(0,18,112,34,0,.12,Math.PI-.12);g.stroke();
  g.strokeStyle='#d9a90f';g.lineWidth=22;g.beginPath();g.ellipse(0,18,112,34,0,.12,Math.PI-.12);g.stroke();
  g.strokeStyle='rgba(255,240,150,.5)';g.lineWidth=5;g.beginPath();g.ellipse(0,12,112,34,0,.5,1.4);g.stroke();
  for(const sd of[-1,1]){gr=g.createLinearGradient(sd*110,0,sd*170,60);gr.addColorStop(0,'#ffe25a');gr.addColorStop(1,'#9a7006');g.fillStyle=gr;g.beginPath();g.ellipse(sd*140,30,34,52,sd*.5,0,7);g.fill()}
  // head (back) with hair pulled to a bun
  gr=g.createRadialGradient(-40,-230,20,0,-190,170);gr.addColorStop(0,'#5a3220');gr.addColorStop(1,'#1e0f08');g.fillStyle=gr;g.beginPath();g.ellipse(0,-195,125,140,0,0,7);g.fill();
  const R=rng(17);g.lineWidth=2.2;for(let i=0;i<120;i++){const a=R()*Math.PI*2,x0=Math.cos(a)*120,y0=-195+Math.sin(a)*135;
    g.strokeStyle=`rgba(${120+R()*60},${60+R()*30},${30+R()*20},${.25+R()*.3})`;g.beginPath();g.moveTo(x0,y0);g.quadraticCurveTo(x0*.6,-190+(y0+195)*.2,(R()-.5)*30,-300);g.stroke()}
  for(const sd of[-1,1]){g.fillStyle=sk[1];g.beginPath();g.ellipse(sd*122,-170,16,30,sd*.2,0,7);g.fill()}// ears
  gr=g.createRadialGradient(-15,-330,5,0,-315,60);gr.addColorStop(0,'#6a3a22');gr.addColorStop(1,'#2a160c');g.fillStyle=gr;g.beginPath();g.ellipse(0,-318,62,50,0,0,7);g.fill();// bun
  g.strokeStyle='rgba(150,90,50,.35)';g.lineWidth=2;for(let i=0;i<14;i++){g.beginPath();g.arc(0,-318,20+i*3,-.5+i*.3,1.2+i*.3);g.stroke()}
  g.fillStyle='#111';g.fillRect(-60,-280,120,10);// hair tie
  g.restore()}
function sceneD(t){if(!WAGON)buildWagon();const lt=t-6;const off=.55,fl=lt>=off-.12&&lt<off+.18?((Math.floor(lt*40)%3)?1:0):(lt<off?1:0);
  const L=lt<off-.12?1:(lt<off+.18?fl:0),E=easeOut(seg(lt,off+.2,off+.6));
  const shake=lt>off&&lt<off+.4?Math.sin(lt*70)*6*(1-(lt-off)/.4):0;
  camTo(ctx,1.02+.05*lt/2,540,760,shake,0);
  ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
  if(L>0){ctx.globalAlpha=L;ctx.drawImage(WAGON.lit,0,0);ctx.globalAlpha=1}
  if(E>0){ctx.globalAlpha=E*(1-L);ctx.drawImage(WAGON.em,0,0);ctx.globalAlpha=1;
    smoke(ctx,t,0,0,W,760,{alpha:.16*E,scale:1.4,vx:-15,vy:8,sheet:1})}
  // phone glows on faces (visible in the dark)
  ctx.save();ctx.globalCompositeOperation='lighter';for(const p of PEOPLE)if(p.phone){const [x,y]=pj(p.X,FLOOR-(p.sit?1.1:1.35),p.Z);glow(ctx,x,y,500/p.Z,'150,200,255',.22*(1-L*.6))}ctx.restore();
  sonyaBack(ctx,t,L<.5);
  finish(t,{vig:.8});
}
