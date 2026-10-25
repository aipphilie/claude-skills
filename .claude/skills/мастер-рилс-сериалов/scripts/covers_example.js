// Reels covers: 1080x1920; the profile grid crops to 3:4 (y 240–1680), so title + part live in y 420–1500
function coverText(g,o){
  g.save();g.textAlign='center';g.textBaseline='middle';
  const shade=g.createLinearGradient(0,o.y-260,0,o.y+330);shade.addColorStop(0,'rgba(0,0,0,0)');shade.addColorStop(.35,'rgba(0,0,0,.55)');shade.addColorStop(.75,'rgba(0,0,0,.55)');shade.addColorStop(1,'rgba(0,0,0,0)');
  g.fillStyle=shade;g.fillRect(0,o.y-260,W,590);
  g.font='900 98px Mont';g.lineJoin='round';g.lineWidth=14;g.strokeStyle='rgba(0,0,0,.65)';g.strokeText('МЕТЕОСТАНЦИЯ',540,o.y);g.fillStyle='#f2ead8';g.fillText('МЕТЕОСТАНЦИЯ',540,o.y);
  g.save();g.translate(540,o.y+120);g.rotate(-.04);g.font='700 128px Hand';g.shadowColor='rgba(0,0,0,.8)';g.shadowBlur=20;g.fillStyle='#ff4a3a';g.fillText(o.part,0,0);g.restore();
  if(o.name){g.font='900 46px Mont';g.fillStyle='#f5b83d';g.shadowColor='rgba(0,0,0,.8)';g.shadowBlur=16;g.fillText('«'+o.name+'»',540,o.y+235)}
  g.restore();
}
const COVERS=[
 g=>{scene2(g,6.3,1.12);g.globalAlpha=.8;g.drawImage(AUR,-200,0);g.globalAlpha=1;finish(0);coverText(g,{y:560,part:'серия 1',name:'СИГНАЛ'})},
 g=>{scene2(g,9.7,1.12);g.globalAlpha=.8;g.drawImage(AUR,-520,40);g.globalAlpha=1;finish(0);coverText(g,{y:560,part:'серия 2',name:'ЖУРНАЛ'})},
 g=>{scene2(g,6.3,1.12);g.globalAlpha=.8;g.drawImage(AUR,-200,0);g.globalAlpha=1;finish(0);coverText(g,{y:560,part:'часть 1',name:'СИГНАЛ'})},
 g=>{portrait(g,10,{K:[[0,540,880,1.15],[1,540,880,1.15]],lamp:.85,look:-.25});finish(0);coverText(g,{y:1290,part:'часть 1',name:'СИГНАЛ'})},
 g=>{pageShot(g,1,PNO,{K:[[0,410,900,1.0],[2,410,900,1.0]]});
   g.globalCompositeOperation='lighter';glow(g,540,1200,500,'rgba(255,60,40,A)',.12);g.globalCompositeOperation='source-over';finish(0);coverText(g,{y:520,part:'часть 1',name:'СИГНАЛ'})},
 g=>{radio(g,5.0,{on:false,t0:0,t1:0,K:[[0,540,900,1.05],[9,540,900,1.05]]});dark(g,.25);
   for(let i=0;i<3;i++){g.globalCompositeOperation='lighter';glow(g,420+i*120,1290,90,'rgba(255,60,40,A)',.6);g.globalCompositeOperation='source-over';g.fillStyle='#ff3b2f';g.beginPath();g.arc(420+i*120,1290,22,0,7);g.fill()}
   finish(0);coverText(g,{y:470,part:'часть 1',name:'СИГНАЛ'})},
 g=>{avWin(g);finish(0);coverText(g,{y:1270,part:'часть 1',name:'СИГНАЛ'})},
];
window.renderFrame=function(i){ctx.setTransform(1,0,0,1,0,0);ctx.globalAlpha=1;ctx.globalCompositeOperation='source-over';ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);ctx.save();COVERS[i](ctx);ctx.restore()};
