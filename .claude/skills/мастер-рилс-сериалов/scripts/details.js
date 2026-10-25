// Detailed props on top of the The Long Dark base style (needs lib.js: rng, glow, poly, MONO).
// Born from the author's note on «112» ep.1: "no boxes and circles — draw cars and rooms properly".
// rr/lg — rounded rect + linear gradient helpers; hand() — hand with fingers, nails, knuckles, thumb
// (curl 0 open … 1 fist, cuff=false for a bare forearm); car() — sedan in profile with damage 0..1;
// truck() — heavy truck from the front with headlights/roof markers; ambulance() — side view, flashing.
// The crash recipe is in the comment at the bottom.
function rr(g,x,y,w,h,r,fill){g.beginPath();g.moveTo(x+r,y);g.arcTo(x+w,y,x+w,y+h,r);g.arcTo(x+w,y+h,x,y+h,r);g.arcTo(x,y+h,x,y,r);g.arcTo(x,y,x+w,y,r);g.closePath();if(fill){g.fillStyle=fill;g.fill()}}
function lg(g,x0,y0,x1,y1,stops){const gr=g.createLinearGradient(x0,y0,x1,y1);stops.forEach(([k,c])=>gr.addColorStop(k,c));return gr}
function hand(g,x,y,s,curl,flip=1,col='#b07c64',colD='#7a5444',cuff=true){g.save();g.translate(x,y);g.scale(s*flip,s);
  const sh=lg(g,-80,0,90,0,[[0,col],[.65,col],[1,colD]]);
  if(cuff){g.fillStyle=lg(g,0,120,0,230,[[0,'#1d2530'],[1,'#121820']]);rr(g,-84,118,176,110,18,null);g.fill();g.fillStyle='rgba(255,255,255,.06)';g.fillRect(-84,118,176,8)}
  else{g.fillStyle=col;g.fillRect(-58,120,122,60)}
  // palm / back of hand
  g.fillStyle=sh;g.beginPath();g.moveTo(-66,-6);g.bezierCurveTo(-74,40,-70,96,-56,132);g.lineTo(62,132);g.bezierCurveTo(78,96,86,44,74,-4);g.bezierCurveTo(40,-18,-30,-18,-66,-6);g.fill();
  // fingers (index..little), rounded, with knuckles and nails
  const F=[[-50,128],[-16,140],[18,132],[50,106]];
  F.forEach(([fx,len],i)=>{const L=lerp(len,len*.32,curl),w=30-i*1.5,cx=fx+i*2;
    g.fillStyle=i%2?col:lg(g,cx-w/2,0,cx+w/2,0,[[0,col],[1,colD]]);rr(g,cx-w/2,-L-4,w,L+14,w/2,null);g.fill();
    g.strokeStyle='rgba(60,30,20,.35)';g.lineWidth=2;if(L>50){g.beginPath();g.moveTo(cx-w/2+5,-L*.42);g.lineTo(cx+w/2-5,-L*.42);g.stroke()}
    if(curl<.4){g.fillStyle='rgba(255,225,205,.55)';rr(g,cx-w/2+6,-L+2,w-12,18,7,null);g.fill()}
    else{g.fillStyle='rgba(60,30,20,.30)';rr(g,cx-w/2+3,-L-2,w-6,12,6,null);g.fill()}});
  g.strokeStyle='rgba(60,30,20,.25)';g.lineWidth=3;for(const [fx] of F){g.beginPath();g.moveTo(fx+2,8);g.lineTo(fx+4,40);g.stroke()} // tendons
  // thumb
  g.save();g.translate(70,40);g.rotate(lerp(-.9,-.4,curl));g.fillStyle=lg(g,0,0,30,0,[[0,col],[1,colD]]);rr(g,-15,-86,32,100,16,null);g.fill();g.fillStyle='rgba(255,225,205,.45)';rr(g,-9,-80,20,16,7,null);g.fill();g.restore();
  g.restore()}
// sedan, side profile facing right; local origin = ground under the middle; d = damage 0..1
function car(g,x,y,s,rot,col,lights,d=0,t=0){g.save();g.translate(x,y);g.rotate(rot);g.scale(s,s);
  g.fillStyle='rgba(0,0,0,.45)';g.beginPath();g.ellipse(0,4,175,16,0,0,7);g.fill();
  const rf=d*26,rb=d*12;
  const body=[[-160,-24],[-162,-58],[-138,-66],[-70,-70],[-42,-108+rb],[-10,-112+rf],[44,-112+rf],[78,-108+rb],[108,-72],[150,-64],[166,-50],[166,-24]];
  poly(g,body,col);poly(g,[[-160,-24],[166,-24],[166,-36],[-160,-36]],'#2c3a40');                       // sill
  poly(g,[[-162,-58],[166,-50],[166,-44],[-162,-50]],'rgba(255,255,255,.18)');                          // shoulder line highlight
  poly(g,[[-38,-104+rb],[-8,-106+rf],[-8,-74],[-62,-72]],'#0b1418');poly(g,[[0,-106+rf],[42,-106+rf],[74,-102+rb],[98,-74],[0,-74]],'#0b1418'); // windows
  poly(g,[[-30,-100+rb],[-18,-102+rf],[-48,-74],[-56,-74]],'rgba(170,210,225,.25)');poly(g,[[20,-104+rf],[34,-104+rf],[4,-76],[-4,-76]],'rgba(170,210,225,.25)');
  g.strokeStyle='rgba(10,16,20,.7)';g.lineWidth=3;g.beginPath();g.moveTo(-6,-72);g.lineTo(-6,-26);g.moveTo(-74,-70);g.lineTo(-78,-28);g.moveTo(96,-70);g.lineTo(100,-28);g.stroke(); // door gaps
  g.fillStyle='#0d1418';g.fillRect(-34,-56,16,4);g.fillRect(40,-56,16,4);                                // handles
  for(const wx of [-104,108]){g.fillStyle='#05080a';g.beginPath();g.arc(wx,-16,30,Math.PI,0);g.fill();g.beginPath();g.arc(wx,-6,26,0,7);g.fill();g.fillStyle='#6c7a80';g.beginPath();g.arc(wx,-6,13,0,7);g.fill();g.fillStyle='#2a3438';g.beginPath();g.arc(wx,-6,5,0,7);g.fill()}
  g.fillStyle='#9a1a14';g.fillRect(-164,-58,8,14);                                                      // tail light
  g.fillStyle=lights?'#fff6dc':'#8a8f88';g.fillRect(158,-56,10,12);                                     // headlight
  if(lights){g.globalCompositeOperation='lighter';poly(g,[[166,-50],[420,-100],[420,30],[166,-40]],'rgba(255,240,200,.12)');glow(g,166,-50,90,'rgba(255,240,200,A)',.55);glow(g,-164,-52,50,'rgba(255,40,30,A)',.4);g.globalCompositeOperation='source-over'}
  if(d>0){ // crushed far side: caved doors, crazed glass, crumpled roof
    g.globalAlpha=d;poly(g,[[-70,-70],[-10,-112+rf],[44,-112+rf],[96,-72],[60,-40],[-30,-38]],'rgba(0,0,0,.35)');
    poly(g,[[-40,-66],[20,-52],[70,-66],[30,-34],[-20,-36]],'rgba(255,255,255,.12)');
    g.strokeStyle='rgba(230,245,250,.85)';g.lineWidth=2;const R=rng(17);for(let i=0;i<14;i++){const cx=-40+R()*120,cy=-100+R()*24;g.beginPath();g.moveTo(cx,cy);g.lineTo(cx+(R()-.5)*50,cy+(R()-.5)*30);g.stroke()}
    g.globalAlpha=1}
  g.restore()}
// heavy truck, seen from the front; local origin = ground under the bumper centre
function truck(g,x,y,s,t=0,d=0){g.save();g.translate(x,y);g.scale(s,s);
  g.fillStyle='rgba(0,0,0,.5)';g.beginPath();g.ellipse(0,6,190,22,0,0,7);g.fill();
  for(const wx of [-128,128]){g.fillStyle='#05080a';g.fillRect(wx-28,-70,56,74)}
  poly(g,[[-150,-360],[150,-360],[158,-120],[-158,-120]],'#2b3c46');poly(g,[[-150,-360],[-20,-360],[-30,-120],[-158,-120]],'#344854'); // cab
  poly(g,[[-132,-340],[132,-340],[140,-226],[-140,-226]],'#0a1218');poly(g,[[-100,-336],[-40,-336],[-110,-230],[-136,-230]],'rgba(170,210,225,.18)'); // windscreen
  g.fillStyle='#0d1418';g.fillRect(-4,-340,8,114);
  for(const sx of [-1,1]){g.fillStyle='#0d1418';g.fillRect(sx*158-(sx<0?28:0),-330,28,6);g.fillRect(sx*176-10,-336,20,70)}                // mirrors
  for(let i=0;i<5;i++){g.fillStyle='#ffb447';g.fillRect(-60+i*30,-374,14,8)}                                                          // roof markers (warm)
  poly(g,[[-96,-210],[96,-210],[100,-80],[-100,-80]],'#121b20');g.fillStyle='#3a4a52';for(let yy=-198;yy<-84;yy+=16)g.fillRect(-90,yy,180,7); // grille
  poly(g,[[-170,-84],[170,-84],[166,-34],[-166,-34]],'#5c6a70');poly(g,[[-170,-84],[170,-84],[168,-74],[-168,-74]],'#8a989e');             // bumper
  g.fillStyle='#e8e2c8';g.fillRect(-36,-66,72,20);g.fillStyle='#14181a';g.font='700 14px '+MONO;g.textAlign='center';g.fillText('А 412 КС',0,-51);g.textAlign='left';
  g.fillStyle='#fff6dc';for(const sx of [-128,128])g.fillRect(sx-26,-120,52,26);
  g.globalCompositeOperation='lighter';for(const sx of [-128,128]){glow(g,sx,-106,240,'rgba(255,240,210,A)',.7);glow(g,sx,-106,46,'rgba(255,255,255,A)',.9)}for(let i=0;i<5;i++)glow(g,-53+i*30,-370,30,'rgba(255,170,60,A)',.5);g.globalCompositeOperation='source-over';
  if(d>0){g.globalAlpha=d;poly(g,[[-170,-84],[-60,-70],[20,-90],[120,-60],[170,-84],[166,-34],[-166,-34]],'rgba(0,0,0,.45)');g.globalAlpha=1}
  g.restore()}
function ambulance(g,x,y,s,t){g.save();g.translate(x,y);g.scale(s,s);g.fillStyle='rgba(0,0,0,.45)';g.beginPath();g.ellipse(0,4,190,16,0,0,7);g.fill();
  poly(g,[[-180,-24],[-180,-190],[90,-190],[130,-120],[180,-96],[180,-24]],'#d8dde0');poly(g,[[96,-180],[126,-122],[96,-122]],'#0b1418');
  g.fillStyle='#c0261b';g.fillRect(-180,-110,360,16);g.fillRect(-90,-170,24,60);g.fillRect(-108,-152,60,24);
  for(const wx of [-110,120]){g.fillStyle='#05080a';g.beginPath();g.arc(wx,-6,28,0,7);g.fill();g.fillStyle='#6c7a80';g.beginPath();g.arc(wx,-6,12,0,7);g.fill()}
  const on=Math.floor(t*6)%2;g.fillStyle=on?'#3a7bff':'#123';g.fillRect(-20,-206,40,16);g.fillStyle=on?'#123':'#ff3b2f';g.fillRect(24,-206,40,16);g.restore()}

/* crash snippet (camera on a pole, vanishing point ~ (540,640)):
  const pre=clamp((t-(tc-4.2))/4.2,0,1),after=t>=tc,ka=easeOut((t-tc)/.7),k=easeInOut(pre);
  const ty=after?lerp(1062,1086,ka):lerp(700,1062,k*k),ts=after?1:lerp(.12,1,k*k);           // truck grows as it comes
  const sx=after?lerp(520,650,ka):lerp(-260,520,pre),sy=after?lerp(1118,1200,ka):1118;        // sedan crosses, then is shoved
  truck(f,520,ty,ts,t,after?1:0);car(f,sx,sy,1.15,after?lerp(0,.32,ka):0,'#7a8c92',!after,after?1:0,t);
  + glass/sparks particles, a steam puff, debris, white flash + camera shake 0.5 s, then 1 s of stillness;
  zoom the camera to ~1.3 on the impact so the cars read at phone size. */
