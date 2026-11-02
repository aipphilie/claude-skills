// Обложка ролика №15 «Пьяный мозг Ярика». 1080×1920, главное в зоне y 285..1635.
function strokeTxt(g,s,x,y,size,fill,stroke=P.choc,lw=16,w=900){g.font=`${w} ${size}px ${F}`;g.textAlign='center';g.textBaseline='middle';g.lineJoin='round';g.lineWidth=lw;g.strokeStyle=stroke;g.strokeText(s,x,y);g.fillStyle=fill;g.fillText(s,x,y)}
function plateTxt(g,s,y,size,bg,col,rot=-.04){g.save();g.translate(540,y);g.rotate(rot);g.font=`900 ${size}px ${F}`;const w=g.measureText(s).width+80;rr(g,-w/2,-size*.7,w,size*1.4,40);fs(g,bg,P.choc,10);txt(g,s,0,8,size,col);g.restore()}
const COVERS={
 A(g){g.save();g.scale(W/840,H/990);brainIn(g,0,1);g.restore();
   rays(g,540,1150,'rgba(217,164,65,.18)',0,18);
   g.save();g.globalCompositeOperation='lighter';glow(g,540,1000,520,'217,164,65',.35);g.restore();
   plateTxt(g,'ПЬЯНЫЙ МОЗГ',420,118,P.mustard,P.choc,-.05);
   strokeTxt(g,'ЯРИКА',540,590,130,P.cream);
   at(g,540,880,1.25,()=>brainMap(g,.05,'front'));
   for(const [x,y,r] of [[250,800,40],[820,760,32],[300,1000,26],[850,980,44]])at(g,x,y,1,()=>abub(g,r,0));
   yk(g,470,1250,1.0,'shock',1,{look:.3,flush:.7});
   at(g,860,1330,1.25,()=>cone(g),.25);
   at(g,200,1470,1.1,()=>mugBeer(g,1,0,1),-.12);
   at(g,560,1560,1,()=>plaque(g,'ЧТО ВЧЕРА БЫЛО?',P.terra,46,P.cream),.04);}
};
