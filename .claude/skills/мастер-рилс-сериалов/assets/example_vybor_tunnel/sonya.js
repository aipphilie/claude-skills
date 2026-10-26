// ===== Sonya: painted-by-code portrait (3 variants) =====
// local units: head height = 1, head centre (0,0); eyes y=0, chin y=.52
const FIG=mk();
const HAIRS=[
  {name:'каре с чёлкой',base:'#17100d',mid:'#2a1b15',sheen:'200,130,70',iris:'#5a3b22'},
  {name:'собранные волосы',base:'#2c160d',mid:'#4a2716',sheen:'230,140,70',iris:'#4d5a3a'},
  {name:'капюшон, длинные',base:'#120d0b',mid:'#241914',sheen:'190,130,80',iris:'#3f4c55'}];

function faceShape(g){g.beginPath();g.moveTo(0,-.52);
  g.bezierCurveTo(.22,-.53,.36,-.40,.37,-.18);g.bezierCurveTo(.385,-.02,.37,.10,.33,.22);
  g.bezierCurveTo(.28,.36,.15,.49,0,.52);g.bezierCurveTo(-.15,.49,-.28,.36,-.33,.22);
  g.bezierCurveTo(-.37,.10,-.385,-.02,-.37,-.18);g.bezierCurveTo(-.36,-.40,-.22,-.53,0,-.52);g.closePath()}
function blob(g,x,y,rx,ry,rgb,a){g.save();g.translate(x,y);g.scale(rx,ry);const gr=g.createRadialGradient(0,0,0,0,0,1);
  gr.addColorStop(0,`rgba(${rgb},${a})`);gr.addColorStop(1,`rgba(${rgb},0)`);g.fillStyle=gr;g.beginPath();g.arc(0,0,1,0,7);g.fill();g.restore()}
function strands(g,R,n,f,col,w,a){g.strokeStyle=col;g.lineCap='round';for(let i=0;i<n;i++){const p=f(R,i/n);g.globalAlpha=a*(.4+R()*.6);g.lineWidth=w*(.5+R());
  g.beginPath();g.moveTo(p[0],p[1]);g.bezierCurveTo(p[2],p[3],p[4],p[5],p[6],p[7]);g.stroke()}g.globalAlpha=1}

function hairBack(g,v,R,t){const h=HAIRS[v];
  if(v===0){g.beginPath();g.moveTo(-.47,.44);g.bezierCurveTo(-.56,.05,-.52,-.52,-.2,-.63);g.bezierCurveTo(.05,-.7,.45,-.6,.5,-.25);
    g.bezierCurveTo(.56,.05,.52,.3,.48,.44);g.lineTo(.3,.46);g.lineTo(-.3,.46);g.closePath();
    const gr=g.createLinearGradient(-.5,0,.5,0);gr.addColorStop(0,h.mid);gr.addColorStop(.6,h.base);gr.addColorStop(1,'#0b0807');g.fillStyle=gr;g.fill();
    strands(g,R,160,(R,k)=>{const x=-.48+k*.96+(R()-.5)*.03,top=-.55+Math.abs(x)*.2;return[x*.6,top,x*1.02,top+.3,x*1.06,.2,x*.98+(R()-.5)*.02,.43+R()*.03]},'#3a2a22',.006,.5)}
  if(v===1){// bun at back + tight cap
    blob(g,.05,-.62,.2,.14,'40,22,14',1);g.fillStyle=h.base;g.beginPath();g.ellipse(.04,-.6,.17,.12,.2,0,7);g.fill();
    g.beginPath();g.moveTo(-.4,.05);g.bezierCurveTo(-.45,-.4,-.25,-.6,0,-.6);g.bezierCurveTo(.25,-.6,.45,-.4,.41,.05);g.lineTo(.37,-.1);g.lineTo(-.37,-.1);g.closePath();
    const gr=g.createLinearGradient(-.4,-.6,.4,0);gr.addColorStop(0,h.mid);gr.addColorStop(1,h.base);g.fillStyle=gr;g.fill()}
  if(v===2){// hood + long hair
    g.beginPath();g.moveTo(-.95,1.2);g.bezierCurveTo(-.85,.3,-.72,-.62,-.05,-.74);g.bezierCurveTo(.6,-.76,.8,-.2,.86,.4);g.bezierCurveTo(.9,.8,.95,1.0,.98,1.2);g.closePath();
    const gr=g.createLinearGradient(-.8,0,.8,0);gr.addColorStop(0,'#262c2c');gr.addColorStop(.5,'#161a1b');gr.addColorStop(1,'#0a0c0d');g.fillStyle=gr;g.fill();
    // hood inner shadow
    g.beginPath();g.moveTo(-.66,1.2);g.bezierCurveTo(-.6,.2,-.55,-.58,0,-.64);g.bezierCurveTo(.55,-.62,.62,.0,.68,1.2);g.closePath();g.fillStyle='#070808';g.fill();
    g.beginPath();g.moveTo(-.5,.9);g.bezierCurveTo(-.55,.2,-.5,-.55,0,-.58);g.bezierCurveTo(.5,-.56,.56,.1,.5,.9);{const Rb=rng(8);for(let i=0;i<=16;i++)g.lineTo(.5-i/16,.9+Rb()*.12)}g.closePath();g.fillStyle=h.base;g.fill();
    strands(g,R,180,(R,k)=>{const x=-.5+k,s=Math.sign(x)||1;return[x*.5,-.52,x*.9,-.2,x*1.0+s*.03,.3,x*.95+(R()-.5)*.05,.85+R()*.12]},'#33261e',.006,.5)}
}
function hairFront(g,v,R,t){const h=HAIRS[v],sw=Math.sin(t*1.3)*.006;
  if(v===0){// blunt bangs
    g.beginPath();g.moveTo(-.4,-.12);g.bezierCurveTo(-.42,-.45,-.22,-.6,.02,-.6);g.bezierCurveTo(.28,-.6,.44,-.42,.4,-.12);
    {const Rb=rng(4);for(let i=0;i<=26;i++){const x=.4-i*(.8/26),y=-.19+Math.pow(Math.abs(x),1.5)*.25+(Rb()-.3)*.03+sw;g.lineTo(x,y)}}g.closePath();
    const gr=g.createLinearGradient(0,-.6,0,-.15);gr.addColorStop(0,h.mid);gr.addColorStop(1,h.base);g.fillStyle=gr;g.fill();
    strands(g,R,120,(R,k)=>{const x=-.38+k*.76;return[x*.5,-.58,x*.85,-.45,x,-.3,x+(R()-.5)*.03,-.19+Math.abs(x)*.12]},'#3c2b22',.005,.6);
    // side locks over cheeks
    for(const s of[-1,1]){g.beginPath();g.moveTo(s*.36,-.2);g.bezierCurveTo(s*.4,.0,s*.38,.25,s*.34,.43);g.lineTo(s*.47,.45);g.bezierCurveTo(s*.5,.1,s*.48,-.2,s*.42,-.3);g.closePath();g.fillStyle=h.base;g.fill()}}
  if(v===1){// swept back hairline + loose strands
    g.beginPath();g.moveTo(-.39,0);g.bezierCurveTo(-.42,-.45,-.22,-.6,0,-.6);g.bezierCurveTo(.22,-.6,.42,-.45,.39,0);
    g.bezierCurveTo(.36,-.2,.3,-.33,.14,-.36);g.quadraticCurveTo(.04,-.37,0,-.34);g.quadraticCurveTo(-.04,-.37,-.14,-.36);g.bezierCurveTo(-.3,-.33,-.36,-.2,-.39,0);g.closePath();
    const gr=g.createLinearGradient(-.4,-.6,.4,-.2);gr.addColorStop(0,h.mid);gr.addColorStop(1,h.base);g.fillStyle=gr;g.fill();
    strands(g,R,110,(R,k)=>{const x=-.36+k*.72,y=-.34-.03*Math.cos(x*4)+Math.abs(x)*.5*Math.abs(x);return[x,y,x*.9,y-.12,x*.6,-.55,x*.3,-.62]},'#6a3c22',.005,.45);
    strands(g,R,8,(R,k)=>{const s=k<.5?-1:1;return[s*.2,-.36,s*(.33+R()*.05),-.2,s*(.33+R()*.06),.05+sw*4,s*(.35+R()*.05),.28+R()*.12]},'#3a1e12',.006,.9)}
  if(v===2){// middle-part long hair framing face
    g.beginPath();g.moveTo(-.4,.0);g.bezierCurveTo(-.42,-.45,-.22,-.62,0,-.62);g.bezierCurveTo(.22,-.62,.42,-.45,.4,0);g.bezierCurveTo(.34,-.28,.15,-.4,.01,-.43);g.bezierCurveTo(-.15,-.4,-.34,-.28,-.4,0);g.closePath();g.fillStyle=h.base;g.fill();
    for(const s of[-1,1]){g.beginPath();g.moveTo(s*.02,-.55);g.bezierCurveTo(s*.3,-.55,s*.4,-.3,s*.38,0);g.bezierCurveTo(s*.36,.3,s*.36,.6,s*.42,.95);
      g.lineTo(s*.56,.95);g.bezierCurveTo(s*.52,.5,s*.52,-.2,s*.42,-.42);g.bezierCurveTo(s*.3,-.6,s*.1,-.6,s*.02,-.55);g.closePath();g.fillStyle=h.base;g.fill()}
    strands(g,R,140,(R,k)=>{const s=k<.5?-1:1,o=R()*.12;return[s*.03,-.55,s*(.3+o),-.45,s*(.38+o),-.0,s*(.4+o)+sw,.9+R()*.06]},'#3b2b22',.005,.55)}
}

function eye(g,ex,side,o){const open=o.open,lx=o.look[0],ly=o.look[1],h=HAIRS[o.v];
  blob(g,ex,-.005,.13,.085,'70,35,30',.35);blob(g,ex+side*.01,.06,.09,.04,'60,30,30',.25);// socket / eyebag
  g.strokeStyle='rgba(80,40,35,.5)';g.lineWidth=.006;g.beginPath();g.moveTo(ex-.075,-.02);g.quadraticCurveTo(ex,-.075,ex+.08,-.03);g.stroke();// crease
  const ip=side>0?.07:-.07;// outer corner direction
  const pth=()=>{g.beginPath();g.moveTo(ex-ip*.95,.006);g.quadraticCurveTo(ex-ip*.1,-.06*open,ex+ip,-.008);g.quadraticCurveTo(ex,.04*open,ex-ip*.95,.006);g.closePath()};
  if(open>.08){g.save();pth();g.clip();
    let gr=g.createLinearGradient(0,-.05,0,.04);gr.addColorStop(0,'#b9a99e');gr.addColorStop(.5,'#ece3da');gr.addColorStop(1,'#d2c4bb');g.fillStyle=gr;g.fillRect(ex-.1,-.08,.2,.14);
    const ix=ex+lx*.022,iy=-.006+ly*.014;
    gr=g.createRadialGradient(ix,iy,0,ix,iy,.034);gr.addColorStop(0,'#1a1410');gr.addColorStop(.33,h.iris);gr.addColorStop(.8,h.iris);gr.addColorStop(1,'#140e0b');
    g.fillStyle=gr;g.beginPath();g.arc(ix,iy,.034,0,7);g.fill();
    const R=rng(3);g.strokeStyle='rgba(220,180,120,.25)';g.lineWidth=.0015;for(let i=0;i<40;i++){const a=R()*7;g.beginPath();g.moveTo(ix+Math.cos(a)*.013,iy+Math.sin(a)*.013);g.lineTo(ix+Math.cos(a)*.03,iy+Math.sin(a)*.03);g.stroke()}
    g.fillStyle='#050404';g.beginPath();g.arc(ix,iy,.013,0,7);g.fill();
    g.fillStyle=`rgba(${o.catch||'255,210,150'},.95)`;g.beginPath();g.arc(ix-.012,iy-.012,.0065,0,7);g.fill();
    g.fillStyle='rgba(255,255,255,.35)';g.beginPath();g.arc(ix+.01,iy+.012,.003,0,7);g.fill();
    gr=g.createLinearGradient(0,-.06,0,-.01);gr.addColorStop(0,'rgba(30,15,10,.75)');gr.addColorStop(1,'rgba(30,15,10,0)');g.fillStyle=gr;g.fillRect(ex-.1,-.08,.2,.08);
    g.restore()}
  // upper lid line + lashes
  g.strokeStyle='#160c09';g.lineCap='round';g.lineWidth=.011;g.beginPath();g.moveTo(ex-ip*.95,.006);g.quadraticCurveTo(ex-ip*.1,-.06*open,ex+ip,-.008);g.stroke();
  g.lineWidth=.004;for(let i=0;i<7;i++){const k=.45+i*.08,x=lerp(ex-ip*.95,ex+ip,k),y=lerp(.006,-.008,k)-.055*open*4*k*(1-k)*.9;
    g.beginPath();g.moveTo(x,y);g.quadraticCurveTo(x+ip*.15,y-.015,x+ip*.3,y-.022);g.stroke()}
  g.strokeStyle='rgba(120,60,55,.55)';g.lineWidth=.004;g.beginPath();g.moveTo(ex-ip*.9,.01);g.quadraticCurveTo(ex,.044*Math.max(open,.2),ex+ip,-.004);g.stroke();
  // brow
  const R2=rng(side>0?21:22);g.strokeStyle=HAIRS[o.v].base;for(let i=0;i<46;i++){const k=i/46,x=lerp(ex-ip*1.1,ex+ip*1.25,k),y=-.1-.03*Math.sin(k*3)+(R2()-.5)*.008+(o.brow||0);
    g.globalAlpha=.55+R2()*.4;g.lineWidth=.005+(1-k)*.004;g.beginPath();g.moveTo(x,y+.008);g.lineTo(x+ip*.12,y-.01);g.stroke()}g.globalAlpha=1}

function drawSonya(g,x,y,s,o){
  o={v:0,t:0,open:1,look:[0,0],rim:1,fill:.5,dark:0,soot:0,breath:0,...o};
  const f=FIG.getContext('2d');f.setTransform(1,0,0,1,0,0);f.clearRect(0,0,W,H);f.translate(x,y);f.scale(s,s);
  const R=rng(9+o.v),t=o.t,hv=o.v;
  // ---- torso: hoodie ----
  f.save();f.translate(0,o.breath*.01);
  f.beginPath();f.moveTo(-.95,2.6);f.bezierCurveTo(-1.15,1.5,-1.1,.86,-.55,.74);f.bezierCurveTo(-.3,.68,.3,.68,.55,.74);f.bezierCurveTo(1.1,.86,1.15,1.5,.95,2.6);f.closePath();
  let gr=f.createLinearGradient(-1.2,0,1.2,0);gr.addColorStop(0,'#2d3335');gr.addColorStop(.45,'#1d2224');gr.addColorStop(1,'#0c0e0f');f.fillStyle=gr;f.fill();
  f.strokeStyle='rgba(0,0,0,.45)';f.lineWidth=.02;for(const [a,b,c,d] of [[-.8,1.05,-.7,2.4],[.7,1.1,.65,2.4],[-.3,1.25,-.25,2.5],[.25,1.3,.3,2.5]]){f.beginPath();f.moveTo(a,b);f.quadraticCurveTo(a+.1,(b+d)/2,c,d);f.stroke()}
  for(const sd of[-1,1]){f.strokeStyle='rgba(0,0,0,.35)';f.lineWidth=.05;f.beginPath();f.moveTo(sd*.62,.95);f.quadraticCurveTo(sd*.8,1.5,sd*.72,2.1);f.stroke();f.strokeStyle='rgba(255,255,255,.04)';f.lineWidth=.03;f.beginPath();f.moveTo(sd*.75,.9);f.quadraticCurveTo(sd*.95,1.5,sd*.85,2.2);f.stroke()}
  f.strokeStyle='rgba(255,255,255,.05)';f.lineWidth=.03;f.beginPath();f.moveTo(-1.1,1.0);f.quadraticCurveTo(-.95,.82,-.6,.78);f.stroke();
  // hood roll behind neck (not for v2)
  if(hv!==2){f.beginPath();f.ellipse(0,.76,.56,.17,0,0,7);gr=f.createRadialGradient(0,.76,.1,0,.76,.56);gr.addColorStop(0,'#0b0d0e');gr.addColorStop(1,'#283032');f.fillStyle=gr;f.fill()}
  // drawstrings
  f.strokeStyle='#c9c4b8';f.lineWidth=.016;for(const sx of[-.12,.12]){f.beginPath();f.moveTo(sx,.84);f.quadraticCurveTo(sx*1.3,1.1+Math.sin(t+sx*9)*.01,sx*1.1,1.38);f.stroke();f.fillStyle='#8f8a80';f.fillRect(sx*1.1-.014,1.36,.028,.07)}
  f.restore();
  // headband goes BEHIND the neck: drawn before the neck, the neck hides its middle
  f.lineCap='round';f.strokeStyle='#121212';f.lineWidth=.055;f.beginPath();f.ellipse(0,.78,.27,.13,0,Math.PI*1.02,Math.PI*1.98);f.stroke();
  f.strokeStyle='#b8900c';f.lineWidth=.042;f.beginPath();f.ellipse(0,.78,.27,.13,0,Math.PI*1.02,Math.PI*1.98);f.stroke();
  f.strokeStyle='rgba(255,230,120,.35)';f.lineWidth=.01;f.beginPath();f.ellipse(0,.77,.27,.13,0,Math.PI*1.05,Math.PI*1.3);f.stroke();
  // ---- neck ----
  f.beginPath();f.moveTo(-.15,.3);f.lineTo(-.165,.8);f.quadraticCurveTo(0,.86,.165,.8);f.lineTo(.15,.3);f.closePath();
  gr=f.createLinearGradient(-.17,0,.17,0);gr.addColorStop(0,'#b88670');gr.addColorStop(1,'#5a3a30');f.fillStyle=gr;f.fill();
  blob(f,0,.47,.2,.12,'40,20,15',.75);blob(f,.08,.65,.08,.15,'40,20,15',.35);
  // ---- hair back, ears ----
  hairBack(f,hv,R,t);
  if(hv===1)for(const sd of[-1,1]){f.fillStyle='#9a6a55';f.beginPath();f.ellipse(sd*.375,.05,.045,.09,sd*.15,0,7);f.fill();blob(f,sd*.37,.06,.03,.06,'60,30,25',.6)}
  // ---- headphones (yellow) around neck ----
  for(const sd of[-1,1])blob(f,sd*.27,.93,.15,.07,'0,0,0',.55);
  for(const sd of[-1,1]){f.save();f.translate(sd*.27,.85);f.rotate(sd*-.65);f.scale(.8,.72);
    f.fillStyle='#141414';f.beginPath();f.ellipse(sd*-.02,-.03,.12,.15,0,0,7);f.fill();
    gr=f.createLinearGradient(-.13,-.15,.13,.15);gr.addColorStop(0,'#ffe25a');gr.addColorStop(.5,'#f1bd10');gr.addColorStop(1,'#8a6406');f.fillStyle=gr;f.beginPath();f.ellipse(0,0,.13,.16,0,0,7);f.fill();
    f.fillStyle='rgba(255,255,230,.55)';f.beginPath();f.ellipse(-.04,-.07,.035,.06,-.4,0,7);f.fill();
    f.strokeStyle='rgba(60,40,0,.5)';f.lineWidth=.008;f.beginPath();f.ellipse(0,0,.1,.13,0,0,7);f.stroke();f.restore()}
  // ---- face ----
  f.save();faceShape(f);f.clip();
  gr=f.createLinearGradient(-.4,-.2,.4,.2);gr.addColorStop(0,'#e0b39a');gr.addColorStop(.5,'#c08a72');gr.addColorStop(1,'#6e463a');f.fillStyle=gr;f.fillRect(-.5,-.6,1,1.2);
  blob(f,-.08,-.33,.25,.13,'240,205,180',.35);// forehead
  blob(f,-.2,.1,.12,.08,'240,200,175',.35);blob(f,.2,.1,.1,.07,'200,150,130',.18);// cheekbones
  blob(f,-.3,.25,.16,.2,'90,50,40',.25);blob(f,.3,.25,.16,.22,'80,45,35',.28);// under cheek
  blob(f,0,.47,.25,.07,'60,30,25',.25);blob(f,-.33,-.15,.08,.18,'90,50,40',.3);blob(f,.33,-.15,.08,.18,'80,45,35',.3);blob(f,-.09,.24,.03,.07,'90,45,38',.25);blob(f,.1,.24,.035,.08,'70,35,28',.35);blob(f,-.1,.08,.06,.05,'220,110,100',.12);blob(f,.12,.09,.06,.05,'220,110,100',.10);
  // nose
  f.strokeStyle='rgba(255,230,210,.16)';f.lineWidth=.016;f.beginPath();f.moveTo(-.015,-.05);f.quadraticCurveTo(-.02,.08,-.012,.14);f.stroke();
  blob(f,.035,.08,.03,.09,'70,35,28',.4);blob(f,0,.165,.045,.03,'250,215,195',.35);blob(f,0,.205,.06,.02,'60,25,20',.45);
  f.fillStyle='rgba(55,25,20,.75)';for(const sd of[-1,1]){f.beginPath();f.ellipse(sd*.03,.195,.016,.008,sd*.3,0,7);f.fill()}
  f.strokeStyle='rgba(80,40,32,.5)';f.lineWidth=.006;for(const sd of[-1,1]){f.beginPath();f.arc(sd*.045,.18,.022,sd>0?-.6:2.2,sd>0?1.6:3.9);f.stroke()}
  // mouth
  blob(f,0,.25,.025,.02,'90,45,38',.3);
  f.beginPath();f.moveTo(-.088,.312);f.bezierCurveTo(-.05,.29,-.03,.276,0,.288);f.bezierCurveTo(.03,.276,.05,.29,.088,.312);f.quadraticCurveTo(0,.322,-.088,.312);f.fillStyle='#9a5a50';f.fill();
  f.beginPath();f.moveTo(-.082,.314);f.bezierCurveTo(-.05,.365,.05,.365,.082,.314);f.quadraticCurveTo(0,.324,-.082,.314);gr=f.createLinearGradient(0,.31,0,.37);gr.addColorStop(0,'#a8645a');gr.addColorStop(1,'#7a4038');f.fillStyle=gr;f.fill();
  blob(f,-.015,.335,.03,.01,'255,220,210',.35);f.strokeStyle='#3e1d19';f.lineWidth=.007;f.beginPath();f.moveTo(-.085,.312);f.quadraticCurveTo(0,.322,.085,.312);f.stroke();
  blob(f,0,.4,.07,.03,'60,30,25',.25);
  // eyes
  eye(f,-.14,-1,o);eye(f,.14,1,o);
  // soot & sweat
  if(o.soot){const Rs=rng(31);f.save();f.filter='blur(6px)';f.lineCap='round';for(let i=0;i<9;i++){f.strokeStyle=`rgba(30,28,26,${(.08+Rs()*.1)*o.soot})`;f.lineWidth=.025+Rs()*.03;const x0=.14+Rs()*.12,y0=.1+Rs()*.16;f.beginPath();f.moveTo(x0,y0);f.quadraticCurveTo(x0+.04,y0+.01,x0+.08+Rs()*.04,y0+.03);f.stroke()}f.restore();
    f.fillStyle='rgba(255,240,220,.5)';for(const [px,py] of[[-.2,-.28],[.24,-.15],[-.05,-.38]]){f.beginPath();f.ellipse(px,py,.004,.006,0,0,7);f.fill()}}
  // skin pores/grain
  f.globalAlpha=.25;f.drawImage(SPECK,-.5,-.6,1,1.2);f.globalAlpha=1;
  f.restore();
  // jaw edge shadow
  f.save();faceShape(f);f.strokeStyle='rgba(40,20,15,.35)';f.lineWidth=.012;f.stroke();f.restore();
  hairFront(f,hv,R,t);
  // ---- lighting passes ----
  f.globalCompositeOperation='source-atop';
  if(o.dark){f.fillStyle=`rgba(4,6,8,${o.dark})`;f.fillRect(-3,-3,6,6)}
  gr=f.createLinearGradient(-.75,0,.1,0);gr.addColorStop(0,`rgba(255,160,60,${.55*o.rim})`);gr.addColorStop(1,'rgba(255,160,60,0)');
  f.globalCompositeOperation='source-atop';f.fillStyle=gr;f.fillRect(-3,-3,3.1,6);
  gr=f.createLinearGradient(.8,0,.0,0);gr.addColorStop(0,`rgba(150,200,255,${.28*o.fill})`);gr.addColorStop(1,'rgba(150,200,255,0)');f.fillStyle=gr;f.fillRect(0,-3,3,6);
  f.globalCompositeOperation='source-over';
  // headphones glow pass (always pops)
  for(const sd of[-1,1])blob(f,sd*.27,.85,.22,.22,'255,200,40',.12*(1-o.dark*.5));
  g.drawImage(FIG,0,0)}
