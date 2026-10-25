// Andrey — bust portrait in local coords: face centre (0,0), chin ~ +225, hat top ~ -386.
// opts: {blink, look, breath, seed,
//        hat:'ushanka'|'hood'|'beanie', beard:'full'|'stubble'|'grey'|'moustache',
//        coat:'parka'|'expedition'|'tulup'|'telogreika', scarf:true|false, glasses, headphones, old}
function drawAndrey(g,opts={}){
  const R=rng(opts.seed||404),blink=opts.blink||0,look=opts.look||0;
  const hat=opts.hat||'ushanka',beard=opts.beard||'full',coat=opts.coat||'parka';
  const C={fur:'#6e5a46',furL:'#8c7558',furD:'#463729',
    skin:'#9c7660',skinL:'#c09a80',skinD:'#5f463b',rim:'rgba(134,163,173,.55)',scarf:'#8a3b2a',scarfL:'#a8503a'};
  const COATS={parka:['#34423a','#475a4b'],expedition:['#a2452a','#c25a35'],tulup:['#4e3726','#684a33'],telogreika:['#2b323b','#3b4450']};
  const [cD,cL]=COATS[coat];
  // ---- body ----
  poly(g,jag([[-470,760],[-430,400],[-260,285],[260,285],[430,400],[470,760]],R,6,4),cD);
  poly(g,jag([[-470,760],[-430,400],[-260,285],[-20,300],[-40,760]],R,6,4),cL);
  if(coat==='telogreika'){g.strokeStyle='rgba(10,14,18,.55)';g.lineWidth=4;for(let y=360;y<760;y+=48){g.beginPath();g.moveTo(-450,y);g.lineTo(450,y+6);g.stroke()}
    g.fillStyle='#14181d';for(let y=380;y<760;y+=110){g.beginPath();g.arc(-30,y,9,0,7);g.fill()}}
  else if(coat==='expedition'){g.fillStyle='#1c1c1c';g.fillRect(-6,330,12,430);g.fillStyle='rgba(230,230,220,.85)';g.fillRect(-470,560,940,22);
    g.fillStyle='#e7e2d4';g.fillRect(-380,440,120,46);g.fillStyle='#a2452a';g.font='700 26px '+MONO;g.fillText('СЕВЕР',-372,472)}
  else if(coat==='parka'){g.fillStyle='#1d2622';g.fillRect(-6,330,12,430)}
  if(coat!=='tulup'){g.strokeStyle='rgba(15,22,18,.5)';g.lineWidth=4;g.beginPath();g.moveTo(-300,420);g.lineTo(-360,760);g.moveTo(300,420);g.lineTo(360,760);g.stroke()}
  if(opts.scarf!==false){poly(g,jag([[-175,200],[175,200],[200,290],[-200,290]],R,5,4),C.scarf);poly(g,jag([[-175,200],[0,205],[-10,290],[-200,290]],R,5,3),C.scarfL)}
  if(coat==='tulup'){ // wide shearling collar
    poly(g,jag([[-360,330],[-230,220],[-90,300],[-60,520],[-170,470]],R,10,6),'#d6c6a4');
    poly(g,jag([[360,330],[230,220],[90,300],[60,520],[170,470]],R,10,6),'#a8987a');
    g.fillStyle='rgba(120,100,70,.35)';for(let i=0;i<120;i++){const s=R()<.5?-1:1,x=s*(80+R()*260),y=240+R()*260;g.fillRect(x,y,5,5)}}
  else if(coat!=='expedition'&&coat!=='telogreika'){
    poly(g,jag([[-262,312],[-190,236],[-80,282],[0,300],[80,282],[190,236],[262,312],[200,362],[0,334],[-200,362]],R,9,8),C.fur);
    poly(g,jag([[-262,312],[-190,236],[-80,282],[0,300],[-10,334],[-200,362]],R,8,6),C.furL);
    g.strokeStyle='rgba(40,30,22,.55)';g.lineWidth=3;for(let i=0;i<50;i++){const x=-250+R()*500,y=250+R()*100;g.beginPath();g.moveTo(x,y);g.lineTo(x+(R()-.5)*16,y+10+R()*12);g.stroke()}}
  else if(coat==='telogreika'){poly(g,jag([[-230,300],[-170,230],[0,280],[170,230],[230,300],[0,330]],R,6,5),'#232a32')}
  if(opts.headphones){ // radio headphones hanging round the neck
    g.strokeStyle='#15191b';g.lineWidth=16;g.beginPath();g.moveTo(-150,330);g.quadraticCurveTo(0,420,150,330);g.stroke();
    for(const s of [-1,1]){g.fillStyle='#1d2326';g.beginPath();g.ellipse(s*170,320,48,62,s*.3,0,7);g.fill();g.fillStyle='#3a4448';g.beginPath();g.ellipse(s*166,314,32,44,s*.3,0,7);g.fill()}
    g.strokeStyle='#0d0f10';g.lineWidth=6;g.beginPath();g.moveTo(170,380);g.bezierCurveTo(220,500,120,600,200,760);g.stroke()}
  // ---- hood (behind head) ----
  if(hat==='hood'){
    poly(g,jag([[-250,-60],[-215,-250],[-110,-345],[0,-365],[110,-345],[215,-250],[250,-60],[245,150],[180,300],[-180,300],[-245,150]],R,8,4),cD);
    poly(g,jag([[-250,-60],[-215,-250],[-110,-345],[0,-365],[-20,300],[-180,300],[-245,150]],R,8,4),cL);
    poly(g,[[-190,-150],[190,-150],[200,120],[-200,120]],'#120e0c')}
  else if(hat==='ushanka'){
    poly(g,jag([[-190,-160],[-140,-160],[-128,90],[-170,130],[-205,50]],R,8,5),C.fur);
    poly(g,jag([[190,-160],[140,-160],[128,90],[170,130],[205,50]],R,8,5),C.furD)}
  // ---- face ----
  const face=[[-124,-160],[124,-160],[146,-70],[138,30],[104,130],[48,205],[0,224],[-48,205],[-104,130],[-138,30],[-146,-70]];
  poly(g,face,C.skin);
  poly(g,[[-124,-160],[-5,-160],[-14,40],[-58,135],[-104,130],[-138,30],[-146,-70]],C.skinL);
  poly(g,[[-140,-40],[-64,-28],[-74,22],[-136,30]],'#cfa98d');
  poly(g,[[55,-160],[124,-160],[146,-70],[138,30],[104,130],[62,118],[38,0]],C.skinD);
  poly(g,[[140,-70],[146,-70],[138,30],[131,30]],C.rim);
  if(opts.old){g.strokeStyle='rgba(70,45,35,.45)';g.lineWidth=3;for(const y of [-140,-124,-110]){g.beginPath();g.moveTo(-70,y);g.lineTo(70,y+2);g.stroke()}
    for(const s of [-1,1]){g.beginPath();g.moveTo(s*96,-50);g.lineTo(s*118,-40);g.moveTo(s*96,-44);g.lineTo(s*116,-28);g.stroke()}}
  poly(g,[[-120,-92],[120,-92],[112,-62],[-112,-62]],'rgba(70,45,35,.35)');
  for(const s of [-1,1])poly(g,[[s*28,-70],[s*100,-74],[s*96,-36],[s*30,-38]],s<0?'rgba(120,80,60,.45)':'rgba(60,40,30,.45)');
  for(const s of [-1,1]){const ex=s*63,ey=-54,open=1-blink;
    if(open>.15){g.save();path(g,[[ex-30,ey],[ex,ey-13*open],[ex+28,ey],[ex,ey+8*open]]);g.fillStyle=s<0?'#ddd0bd':'#9c8e7d';g.fill();g.clip();
      g.fillStyle='#3a4a52';g.beginPath();g.arc(ex+look*9,ey,10,0,7);g.fill();g.fillStyle='#0d0d0d';g.beginPath();g.arc(ex+look*9,ey,5,0,7);g.fill();
      g.fillStyle='#fff';g.fillRect(ex+look*9-6,ey-6,3,3);g.restore()}
    g.strokeStyle='#1c130f';g.lineWidth=4;g.beginPath();g.moveTo(ex-32,ey+1);g.lineTo(ex,ey-14*open-1);g.lineTo(ex+30,ey+1);g.stroke();
    g.strokeStyle='rgba(60,38,28,.6)';g.lineWidth=2;g.beginPath();g.moveTo(ex-22,ey+16);g.lineTo(ex+18,ey+18);g.stroke()}
  const browC=beard==='grey'?['#6d6862','#5a5650']:['#241a14','#1a120e'];
  poly(g,jag([[-122,-86],[-34,-100],[-26,-84],[-116,-72]],R,3,2),browC[0]);
  poly(g,jag([[122,-86],[34,-100],[26,-84],[116,-72]],R,3,2),browC[1]);
  g.strokeStyle='rgba(70,45,35,.6)';g.lineWidth=3;g.beginPath();g.moveTo(-8,-96);g.lineTo(-4,-74);g.moveTo(8,-96);g.lineTo(4,-74);g.stroke();
  poly(g,[[-13,-48],[5,-48],[12,40],[-20,40]],'#dcae8c');
  poly(g,[[5,-48],[32,30],[12,48]],'#78523f');
  poly(g,[[-32,42],[32,42],[24,58],[-24,58]],'#5a3c2f');
  poly(g,[[-120,10],[-70,0],[-62,40],[-110,52]],'rgba(180,95,80,.25)');
  poly(g,[[120,10],[70,0],[62,40],[110,52]],'rgba(140,70,60,.2)');
  // ---- facial hair ----
  const BOUT=[[-147,10],[-122,40],[-90,70],[-40,80],[0,72],[40,80],[90,70],[122,40],[147,10]];
  if(beard==='full'||beard==='grey'){
    const long=beard==='grey'?70:0,bc=beard==='grey'?['#87827b','#aaa49c','#6e6a64']:['#36291f','#58463a','#2a1f18'];
    poly(g,jag([...BOUT,[142,110],[102,192+long*.5],[52,244+long],[0,268+long],[-52,244+long],[-102,192+long*.5],[-142,110]],R,9,5),bc[0]);
    poly(g,jag([[-147,10],[-122,40],[-90,70],[-40,80],[-10,150],[-52,244+long],[-102,192+long*.5],[-142,110]],R,8,4),bc[1]);
    poly(g,jag([[-74,68],[-20,56],[0,64],[20,56],[74,68],[54,96],[0,82],[-54,96]],R,4,3),bc[2]);
    g.fillStyle='#160e0b';g.fillRect(-34,104,68,6);poly(g,[[-26,110],[26,110],[18,122],[-18,122]],'#6a4636')}
  else if(beard==='stubble'){
    g.save();path(g,jag([...BOUT,[138,60],[104,130],[48,205],[0,224],[-48,205],[-104,130],[-138,60]],R,3,3));g.clip();
    g.fillStyle='rgba(40,28,22,.32)';g.fillRect(-160,0,320,240);g.fillStyle='rgba(30,20,16,.5)';for(let i=0;i<500;i++)g.fillRect(-150+R()*300,10+R()*220,2,2);g.restore();
    poly(g,[[-60,70],[-14,62],[0,66],[14,62],[60,70],[46,80],[0,74],[-46,80]],'rgba(40,28,22,.6)');
    g.fillStyle='#3a2018';g.fillRect(-36,104,72,6);poly(g,[[-28,110],[28,110],[20,124],[-20,124]],'#8a5a48')}
  else if(beard==='moustache'){
    g.fillStyle='rgba(40,28,22,.18)';g.beginPath();g.ellipse(0,140,120,90,0,0,7);g.fill();
    poly(g,jag([[-90,70],[-30,54],[0,62],[30,54],[90,70],[100,130],[78,132],[60,92],[0,86],[-60,92],[-78,132],[-100,130]],R,4,3),'#2c2019');
    g.fillStyle='#1e120e';g.fillRect(-34,106,68,6);poly(g,[[-26,112],[26,112],[18,124],[-18,124]],'#7c5040')}
  // ---- glasses ----
  if(opts.glasses){g.strokeStyle='#121212';g.lineWidth=5;for(const s of [-1,1]){g.beginPath();g.arc(s*62,-52,40,0,7);g.stroke();g.fillStyle='rgba(180,210,220,.12)';g.fill();
      g.strokeStyle='rgba(255,255,255,.5)';g.lineWidth=3;g.beginPath();g.arc(s*62,-52,30,3.6,4.3);g.stroke();g.strokeStyle='#121212';g.lineWidth=5}
    g.beginPath();g.moveTo(-22,-56);g.quadraticCurveTo(0,-66,22,-56);g.moveTo(-102,-56);g.lineTo(-140,-62);g.moveTo(102,-56);g.lineTo(140,-62);g.stroke()}
  // ---- headwear ----
  if(hat==='ushanka'){
    poly(g,jag([[-180,-150],[-170,-300],[-96,-372],[0,-386],[96,-372],[170,-300],[180,-150]],R,7,5),'#4a3a2e');
    poly(g,jag([[-180,-150],[-170,-300],[-96,-372],[0,-386],[-10,-150]],R,7,4),'#5c4838');
    poly(g,jag([[-192,-138],[-182,-218],[0,-238],[182,-218],[192,-138],[0,-160]],R,10,8),C.fur);
    poly(g,jag([[-192,-138],[-182,-218],[0,-238],[0,-160]],R,9,5),C.furL);
    g.strokeStyle='rgba(40,30,22,.6)';g.lineWidth=3;for(let i=0;i<40;i++){const x=-180+R()*360,y=-225+R()*80;g.beginPath();g.moveTo(x,y);g.lineTo(x+(R()-.5)*14,y+12+R()*10);g.stroke()}
    poly(g,jag([[-150,-312],[-84,-372],[0,-388],[92,-372],[152,-314],[60,-340],[-40,-346]],R,6,4),'#d6dfe0')}
  else if(hat==='hood'){ // fur ruff framing the face
    const ring=[];for(let i=0;i<=40;i++){const a=Math.PI*2*i/40;ring.push([Math.cos(a)*215,-40+Math.sin(a)*250])}
    const inner=[];for(let i=40;i>=0;i--){const a=Math.PI*2*i/40;inner.push([Math.cos(a)*158,-30+Math.sin(a)*205])}
    g.save();path(g,ring);g.moveTo(inner[0][0],inner[0][1]);for(const p of inner)g.lineTo(p[0],p[1]);g.closePath();g.fillStyle='#7d6a55';g.fill('evenodd');g.restore();
    g.save();g.beginPath();g.rect(-400,-500,400,1000);g.clip();path(g,ring);g.moveTo(inner[0][0],inner[0][1]);for(const p of inner)g.lineTo(p[0],p[1]);g.closePath();g.fillStyle='#9a8670';g.fill('evenodd');g.restore();
    g.strokeStyle='rgba(45,35,25,.6)';g.lineWidth=4;for(let i=0;i<140;i++){const a=R()*Math.PI*2,r=160+R()*55,x=Math.cos(a)*r*1.0,y=-35+Math.sin(a)*r*1.18;g.beginPath();g.moveTo(x,y);g.lineTo(x+Math.cos(a)*22,y+Math.sin(a)*22);g.stroke()}
    g.fillStyle='rgba(225,236,240,.8)';for(let i=0;i<60;i++){const a=R()*Math.PI*2,r=170+R()*45;g.fillRect(Math.cos(a)*r,-35+Math.sin(a)*r*1.18,4,4)}
    // hide the chin area under ruff bottom
  }
  else if(hat==='beanie'){
    poly(g,jag([[-168,-120],[-160,-250],[-90,-320],[0,-336],[90,-320],[160,-250],[168,-120]],R,5,5),'#24304a');
    poly(g,jag([[-168,-120],[-160,-250],[-90,-320],[0,-336],[-6,-120]],R,5,4),'#30405e');
    g.strokeStyle='rgba(10,14,24,.45)';g.lineWidth=5;for(let x=-150;x<=150;x+=22){g.beginPath();g.moveTo(x,-130);g.lineTo(x*.8,-300);g.stroke()}
    poly(g,jag([[-176,-112],[-172,-196],[0,-206],[172,-196],[176,-112],[0,-128]],R,4,6),'#2a3854');
    g.strokeStyle='rgba(10,14,24,.5)';g.lineWidth=4;for(let x=-170;x<=170;x+=18){g.beginPath();g.moveTo(x,-118);g.lineTo(x,-196);g.stroke()}
    poly(g,[[-30,-140],[30,-140],[30,-178],[-30,-178]],'#8a3b2a');g.fillStyle='#e0d6c0';g.font='700 18px '+MONO;g.fillText('СЕВ',-20,-152)}
  // frost
  g.fillStyle='rgba(225,236,240,.8)';
  for(let i=0;i<70;i++){const t=R();let x,y;if(t<.25){x=-120+R()*240;y=-98+R()*20}else if(t<.75){if(beard==='stubble'||beard==='moustache')continue;x=-130+R()*260;y=90+R()*160}else{x=-280+R()*560;y=230+R()*120}
    const s=2+R()*3;g.fillRect(x,y,s,s)}
  if(opts.breath){const b=opts.breath;for(let k=0;k<6;k++){const p=(b+k/6)%1;g.fillStyle=`rgba(220,232,236,${(1-p)*.22})`;g.beginPath();g.arc(-30-p*170,120+p*30-p*p*60,14+p*60,0,7);g.fill()}}
}
