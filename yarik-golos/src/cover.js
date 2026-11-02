// Обложка ролика №15 «Пьяный мозг Ярика». 1080×1920, главное в зоне y 285..1635.
function strokeTxt(g,s,x,y,size,fill,stroke=P.choc,lw=16,w=900){g.font=`${w} ${size}px ${F}`;g.textAlign='center';g.textBaseline='middle';g.lineJoin='round';g.lineWidth=lw;g.strokeStyle=stroke;g.strokeText(s,x,y);g.fillStyle=fill;g.fillText(s,x,y)}
function plateTxt(g,s,y,size,bg,col,rot=-.04){g.save();g.translate(540,y);g.rotate(rot);g.font=`900 ${size}px ${F}`;const w=g.measureText(s).width+80;rr(g,-w/2,-size*.7,w,size*1.4,40);fs(g,bg,P.choc,10);txt(g,s,0,8,size,col);g.restore()}
const COVERS={
 A(g){g.fillStyle=P.terra;g.fillRect(0,0,W,H);
   rays(g,540,1150,'rgba(246,238,221,.16)',0,18);
   g.save();g.globalCompositeOperation='lighter';glow(g,540,1100,560,'217,164,65',.3);g.restore();
   plateTxt(g,'ПОЧЕМУ СВОЙ ГОЛОС',400,70,P.mustard,P.choc,-.04);
   strokeTxt(g,'НА ЗАПИСИ',540,560,118,P.cream);
   strokeTxt(g,'БЕСИТ?',540,700,150,P.cream);
   at(g,830,1110,.78,()=>phoneBig(g,.3,(g)=>{g.fillStyle='#FBF5EA';g.fillRect(-150,-270,300,540);txt(g,'Пацаны 🔥',0,-220,30,P.choc,800);at(g,0,0,.55,()=>voiceMsg(g,.3,.6))}),.12);
   yk(g,450,1220,1.15,'shock',1,{look:.4,flush:.5});
   at(g,540,1560,1,()=>plaque(g,'ЭТО Я?!',P.cream,62,P.choc),.04);}
};
