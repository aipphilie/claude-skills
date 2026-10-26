// ===== episode covers (1080x1920, all text inside the 3:4 grid zone y 240..1680) =====
function coverTitle(y=330,{sub='ТОННЕЛЬ · СЕРИЯ 1',tag=null}={}){ctx.setTransform(1,0,0,1,0,0);
  const gr=ctx.createLinearGradient(0,y-200,0,y+260);gr.addColorStop(0,'rgba(0,0,0,.75)');gr.addColorStop(1,'rgba(0,0,0,0)');ctx.fillStyle=gr;ctx.fillRect(0,y-200,W,460);
  ctx.textAlign='center';ctx.textBaseline='middle';ctx.font='178px MB';ctx.lineJoin='round';ctx.lineWidth=18;ctx.strokeStyle='rgba(0,0,0,.8)';ctx.strokeText('ВЫБОР',505,y);ctx.fillStyle='#fff';ctx.fillText('ВЫБОР',505,y);
  const w=ctx.measureText('ВЫБОР').width;ctx.font='178px MB';ctx.strokeText('?',505+w/2+60,y);ctx.fillStyle='#e0302a';ctx.fillText('?',505+w/2+60,y);
  ctx.font='50px MB';ctx.lineWidth=12;ctx.strokeText(sub,540,y+128);ctx.fillStyle='#d9d2c4';ctx.fillText(sub,540,y+128);
  if(tag){ctx.font='44px MB';ctx.fillStyle='#f2c418';ctx.strokeText(tag,540,y+192);ctx.fillText(tag,540,y+192)}
  ctx.textAlign='left';ctx.textBaseline='alphabetic'}
function abBadges(y=1520,{q=true}={}){ctx.setTransform(1,0,0,1,0,0);
  const gr=ctx.createLinearGradient(0,y-260,0,y+200);gr.addColorStop(0,'rgba(0,0,0,0)');gr.addColorStop(1,'rgba(0,0,0,.8)');ctx.fillStyle=gr;ctx.fillRect(0,y-260,W,460);
  for(const [x,l,bg,fg] of [[300,'А','#ffffff','#111'],[780,'Б','#e0302a','#fff']]){ctx.save();ctx.translate(x,y);ctx.rotate(x<540?-.06:.06);
    ctx.fillStyle='rgba(0,0,0,.5)';ctx.beginPath();ctx.roundRect(-112,-102,236,236,30);ctx.fill();ctx.fillStyle=bg;ctx.beginPath();ctx.roundRect(-120,-120,240,240,30);ctx.fill();
    ctx.font='190px MB';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillStyle=fg;ctx.fillText(l,0,12);ctx.restore()}
  if(q){ctx.font='64px MB';ctx.textAlign='center';ctx.textBaseline='middle';ctx.lineWidth=12;ctx.strokeStyle='#000';ctx.strokeText('или',540,y+10);ctx.fillStyle='#f2c418';ctx.fillText('или',540,y+10)}
  ctx.textAlign='left';ctx.textBaseline='alphabetic'}
function resetCtx(){ctx.setTransform(1,0,0,1,0,0);ctx.globalAlpha=1;ctx.globalCompositeOperation='source-over';ctx.filter='none';ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);CAM=null;ctx.textAlign='left';ctx.textBaseline='alphabetic'}
function coverFrame(n){resetCtx();const t=2.2;
  if(n===0){// doorway over the black tunnel
    CAM={z:.98,ay:900,dy:230};sceneA(1.5);CAM=null;ctx.setTransform(1,0,0,1,0,0);ctx.fillStyle='rgba(0,0,0,.2)';ctx.fillRect(0,0,W,H);
    coverTitle(330,{tag:'ПОЕЗД ВСТАЛ В ТОННЕЛЕ'});abBadges(1530)}
  else if(n===1){// the eye with the red lamp
    sceneF(10+2.2);ctx.setTransform(1,0,0,1,0,0);coverTitle(330,{tag:'ЧТО ОНА СДЕЛАЕТ?'});abBadges(1530)}
  else if(n===2){// fork: car above, tunnel below, Sonya between
    if(!WAGON)buildWagon();ctx.save();ctx.beginPath();ctx.rect(0,0,W,H/2);ctx.clip();ctx.setTransform(1,0,0,1,0,-260);ctx.drawImage(WAGON.em,0,0);ctx.restore();
    ctx.save();ctx.beginPath();ctx.rect(0,H/2,W,H/2);ctx.clip();ctx.setTransform(1.3,0,0,1.3,-160,-280);ctx.drawImage(RAIL,0,0);ctx.restore();ctx.setTransform(1,0,0,1,0,0);
    ctx.fillStyle='rgba(0,0,0,.35)';ctx.fillRect(0,0,W,H);ctx.fillStyle='#e0302a';ctx.fillRect(0,H/2-5,W,10);
    drawSonya(ctx,540,1000,430,{v:SV,t,rim:1,fill:.6,dark:.05,look:[-.5,-.2],open:.95});
    finish(t,{vig:.75});
    for(const [x,y,l,bg,fg,txt] of [[150,700,'А','#fff','#111','ОСТАТЬСЯ'],[930,1240,'Б','#e0302a','#fff','ВЫЙТИ']]){ctx.fillStyle=bg;ctx.beginPath();ctx.roundRect(x-95,y-95,190,190,26);ctx.fill();ctx.font='150px MB';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillStyle=fg;ctx.fillText(l,x,y+10);
      ctx.font='40px MB';ctx.lineWidth=10;ctx.strokeStyle='#000';ctx.strokeText(txt,x,y+140);ctx.fillStyle='#fff';ctx.fillText(txt,x,y+140)}
    ctx.textAlign='left';ctx.textBaseline='alphabetic';coverTitle(330)}
  else{// the voice: Sonya + red line "НЕ ВЫХОДИ"
    sonyaClose(1,3,t,{look:[.05,-.6],z0:1.12,z1:1.12,ay:600,open:1});ctx.setTransform(1,0,0,1,0,0);
    ctx.globalCompositeOperation='multiply';ctx.fillStyle='rgba(170,40,30,.35)';ctx.fillRect(0,0,W,H);ctx.globalCompositeOperation='source-over';
    ctx.fillStyle='rgba(0,0,0,.7)';ctx.fillRect(110,1250,860,130);ledText(ctx,'«СОНЯ. НЕ ВЫХОДИ.»',540,1272,5,{align:'center',col:'255,60,45'});
    coverTitle(330,{tag:'ОТКУДА ОН ЗНАЕТ ЕЁ ИМЯ?'});abBadges(1560,{q:true})}}
