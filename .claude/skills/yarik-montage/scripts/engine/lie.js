// Варианты сцены «Ярик лежит пластом в одном носке» (сцена 3; потом и сцена 18 на кровати).
// Координаты карточки 840×990, как в scenes.js.
let LIE_VAR='C2'; // утверждено автором 28.10.2026
const JEANS='#5B6B7A',JEANS_D='#4A5866';
function sock(g,col=P.cream){rr(g,-44,-60,88,120,40);fs(g,col);g.fillStyle=P.mustard;g.fillRect(-44,-34,88,16);rr(g,-44,-60,88,120,40);fs(g,null)}
function bareFoot(g){rr(g,-40,-56,80,112,38);fs(g,P.peach);for(let i=0;i<5;i++){g.beginPath();g.arc(-26+i*13,-50+Math.abs(i-1.5)*3,7-i*.6,0,7);fs(g,P.peach,P.choc,3)}}
function sunBeam(g,x0,x1,y0,x2,x3,y1,a=.28){g.save();g.globalAlpha=a;g.fillStyle=P.mustard;g.beginPath();g.moveTo(x0,y0);g.lineTo(x1,y0);g.lineTo(x3,y1);g.lineTo(x2,y1);g.closePath();g.fill();g.restore()}
function floorMess(g,t,y=880){at(g,90,y,.5*pop(t,.6),()=>bottle(g,P.sageD),1.45);at(g,760,y-10,.5*pop(t,.8),()=>bottle(g,P.terra),-1.4);}
// Ярик лёжа на спине, вид сверху: руки раскинуты, ноги вниз, один носок.
function yarikFlat(g,emo,t,o={}){
  for(const s of [-1,1]){ // руки
    g.save();g.translate(s*400,450);g.rotate(s*-.95);rr(g,-70,-40,140,330,60);fs(g,YC.shirt,P.choc,7);g.beginPath();g.arc(0,330,52,0,7);fs(g,P.peach,P.choc,6);g.restore()}
  for(const s of [-1,1]){ // ноги
    g.save();g.translate(s*130,700);g.rotate(s*.06);rr(g,-95,0,190,560,60);fs(g,s<0?JEANS:JEANS_D,P.choc,7);
    g.translate(0,600);g.scale(1.9,1.9);s<0?sock(g):bareFoot(g);g.restore()}
  drawYarik(g,{emo,cap:true,blink:o.blink||0})}
const LIE={
 // А. Вид сверху: лежит пластом на диване, руки раскинуты, носок на одной ноге.
 A(g,t){g.fillStyle='#D9C4A6';g.fillRect(0,0,840,990);
   rr(g,130,30,580,930,50);fs(g,P.sageD);rr(g,170,70,500,850,36);fs(g,P.sage,'rgba(74,47,36,.35)',4);g.strokeStyle='rgba(74,47,36,.25)';g.lineWidth=5;g.beginPath();g.moveTo(170,500);g.lineTo(670,500);g.stroke();
   rr(g,250,60,340,150,50);fs(g,P.cream);
   sunBeam(g,520,840,0,300,520,420,.22);
   at(g,420,215,.47,()=>yarikFlat(g,'bad',t));
   at(g,95,640,.55*pop(t,1.2),()=>phone(g,'3%'),-.3);floorMess(g,t,880);badFx(g,420,215,.47,t);},
 // Б. Крупный план: лицо на подушке, луч солнца по глазам, из-под пледа торчит нога в носке.
 B(g,t){g.fillStyle=P.sageD;g.fillRect(0,0,840,990);
   rr(g,-40,250,700,520,120);fs(g,P.cream);g.strokeStyle='rgba(74,47,36,.2)';g.lineWidth=6;g.beginPath();g.moveTo(80,330);g.quadraticCurveTo(200,380,140,520);g.stroke();
   at(g,330,520,1.05,()=>{g.rotate(-Math.PI/2+.08);drawYarik(g,{emo:'bad',cap:true})});
   // плед поверх тела
   g.beginPath();g.moveTo(560,240);g.quadraticCurveTo(700,200,900,230);g.lineTo(900,990);g.lineTo(520,990);g.quadraticCurveTo(470,700,560,240);g.closePath();fs(g,P.mustard);
   g.strokeStyle='rgba(74,47,36,.3)';g.lineWidth=7;for(const x of [620,700,780]){g.beginPath();g.moveTo(x,240);g.quadraticCurveTo(x-40,600,x-20,990);g.stroke()}
   sunBeam(g,0,840,40,0,840,300,.3);
   at(g,720,880,1.1*pop(t,.9),()=>sock(g),-1.3);
   at(g,140,850,.7*pop(t,1.3),()=>phone(g,'3%'),.25);badFx(g,330,520,.8,t);},
 // В. Растёкся по дивану сидя, плед до подбородка, ноги на полу: одна в носке, другая босая.
 C(g,t){g.fillStyle=P.beige;g.fillRect(0,0,840,990);
   rr(g,520,50,240,200,16);fs(g,'#F7E3B5');g.fillStyle=P.choc;g.fillRect(636,50,8,200);g.fillRect(520,146,240,8);sunBeam(g,520,760,250,260,520,640,.22);
   g.fillStyle='#D9C4A6';g.fillRect(0,800,840,190);
   rr(g,70,300,700,380,50);fs(g,P.sageD);rr(g,40,420,110,330,40);fs(g,P.sage);rr(g,690,420,110,330,40);fs(g,P.sage);rr(g,130,560,580,170,30);fs(g,P.sage);
   for(const s of [-1,1]){g.save();g.translate(420+s*90,640);g.rotate(s*-.12);rr(g,-55,0,110,230,40);fs(g,s<0?JEANS:JEANS_D,P.choc,6);g.translate(0,250);s<0?sock(g):bareFoot(g);g.restore()}
   at(g,420,360,.56,()=>{g.rotate(-.18);drawYarik(g,{emo:'bad',cap:true})});
   g.beginPath();g.moveTo(230,500);g.quadraticCurveTo(420,440,610,500);g.quadraticCurveTo(650,620,600,700);g.lineTo(240,700);g.quadraticCurveTo(190,620,230,500);g.closePath();fs(g,P.mustard);
   at(g,120,900,.5*pop(t,.6),()=>bottle(g,P.sageD),1.45);at(g,700,905,.5*pop(t,.9),()=>phone(g,'3%'),1.2);badFx(g,420,330,.56,t);},
 // Г. Лицом в подушку, рука свисает до пола к телефону, нога в носке на подлокотнике.
 D(g,t){g.fillStyle=P.beige;g.fillRect(0,0,840,990);sunBeam(g,420,760,0,120,380,560,.2);
   g.fillStyle='#D9C4A6';g.fillRect(0,760,840,230);
   rr(g,40,420,760,230,40);fs(g,P.sageD);rr(g,20,380,110,330,40);fs(g,P.sage);rr(g,710,380,110,330,40);fs(g,P.sage);
   rr(g,120,390,190,90,40);fs(g,P.cream); // подушка
   // тело под пледом горбом
   g.beginPath();g.moveTo(250,470);g.quadraticCurveTo(470,300,720,430);g.lineTo(720,500);g.lineTo(250,500);g.closePath();fs(g,P.mustard);
   // рука свисает
   g.save();g.translate(330,470);g.rotate(.08);rr(g,-36,0,72,300,34);fs(g,YC.shirt,P.choc,6);g.beginPath();g.arc(0,310,38,0,7);fs(g,P.peach,P.choc,5);g.restore();
   // голова сзади: кепка козырьком к нам, ухо
   g.beginPath();g.ellipse(215,400,95,82,0,0,7);fs(g,YC.cap,P.choc,7);rr(g,150,440,130,40,16);fs(g,YC.capD,P.choc,6);
   g.beginPath();g.ellipse(305,410,22,32,.3,0,7);fs(g,P.peach,P.choc,5);
   // нога в носке на подлокотнике
   at(g,770,340,1.2,()=>sock(g),.9);
   at(g,360,860,.6*pop(t,.8),()=>phone(g,'3%'),.15);floorMess(g,t,880);
   at(g,215,300,.9,()=>{g.rotate(t*3);swirl(g)});},
};
// Голова Ярика лёжа на боку (тело обрезано по ворот — его закрывает одеяло).
function yarikHeadLying(g,x,y,s,emo,t,cut=650,bl=null){g.save();g.translate(x,y+Math.sin(t*2)*2);g.scale(s,s);g.rotate(-Math.PI/2);g.beginPath();g.rect(-330,-330,660,cut);g.clip();drawYarik(g,{emo,cap:true,blink:bl===null?o_blink(t):bl});g.restore()}
const o_blink=t=>((t*1.3)%3.2)<.12?1:0;
// Б2: крупный план на подушке и одеяле, без носка.
LIE.B2=function(g,t){g.fillStyle=P.sageD;g.fillRect(0,0,840,990);
  rr(g,-40,250,700,520,120);fs(g,P.cream);g.strokeStyle='rgba(74,47,36,.2)';g.lineWidth=6;g.beginPath();g.moveTo(80,330);g.quadraticCurveTo(200,380,140,520);g.stroke();
  yarikHeadLying(g,330,520,1.05,'bad',t);
  g.beginPath();g.moveTo(540,200);g.quadraticCurveTo(700,170,900,200);g.lineTo(900,990);g.lineTo(500,990);g.quadraticCurveTo(450,700,540,200);g.closePath();fs(g,P.mustard);
  g.strokeStyle='rgba(74,47,36,.3)';g.lineWidth=7;for(const x of [610,690,770]){g.beginPath();g.moveTo(x,210);g.quadraticCurveTo(x-40,600,x-20,990);g.stroke()}
  // клетка на одеяле
  g.strokeStyle='rgba(194,106,78,.35)';g.lineWidth=10;for(const y of [380,560,740]){g.beginPath();g.moveTo(490,y);g.quadraticCurveTo(700,y-30,900,y);g.stroke()}
  sunBeam(g,0,840,40,0,840,300,.3);
  at(g,140,850,.7*pop(t,1.0),()=>phone(g,'3%'),.25);badFx(g,330,520,.8,t);};
// В2: общий план, длинный диван, лежит целиком под одеялом, ноги торчат: одна в носке, другая босая.
LIE.C2=function(g,t){g.fillStyle=P.beige;g.fillRect(0,0,840,990);
  rr(g,80,60,230,190,16);fs(g,'#F7E3B5');g.fillStyle=P.choc;g.fillRect(191,60,8,190);g.fillRect(80,151,230,8);sunBeam(g,80,310,250,120,330,470,.24);
  g.fillStyle='#D9C4A6';g.fillRect(0,720,840,270);
  // диван во всю ширину
  rr(g,40,330,760,230,40);fs(g,P.sageD);
  rr(g,20,420,90,260,34);fs(g,P.sage);rr(g,730,420,90,260,34);fs(g,P.sage);
  rr(g,90,500,660,170,26);fs(g,P.sage);g.strokeStyle='rgba(74,47,36,.3)';g.lineWidth=5;g.beginPath();g.moveTo(310,505);g.lineTo(310,665);g.moveTo(530,505);g.lineTo(530,665);g.stroke();
  for(const x of [140,700]){rr(g,x-14,680,28,50,8);fs(g,P.choc,null)}
  rr(g,96,410,170,100,44);fs(g,P.cream); // подушка
  yarikHeadLying(g,195,440,.42,'bad',t,560);
  // одеяло: горб от плеч до щиколоток
  g.beginPath();g.moveTo(278,528);g.bezierCurveTo(268,420,280,375,330,372);g.bezierCurveTo(370,368,400,372,430,380);g.bezierCurveTo(530,405,610,380,715,410);g.bezierCurveTo(745,425,748,500,735,535);g.lineTo(240,540);g.closePath();fs(g,P.mustard);
  g.strokeStyle='rgba(194,106,78,.4)';g.lineWidth=9;for(const x of [330,450,570,670]){g.beginPath();g.moveTo(x,390);g.quadraticCurveTo(x-8,470,x,532);g.stroke()}
  // ноги торчат из-под одеяла на подлокотнике
  at(g,775,438,.85,()=>{g.rotate(-1.45);sock(g)});at(g,785,505,.82,()=>{g.rotate(-1.62);bareFoot(g)});
  at(g,130,880,.5*pop(t,.6),()=>bottle(g,P.sageD),1.45);at(g,330,900,.5*pop(t,.8),()=>bottle(g,P.terra),-1.5);at(g,620,880,.55*pop(t,1.1),()=>phone(g,'3%'),1.2);
  at(g,140,300,.8,()=>{g.rotate(t*3);swirl(g)});at(g,250,330+((t*40)%30),.9,()=>sweat(g));};

// Сцена 18 (кровать) в стиле В2: лежит целиком, одеяло до шеи. ph=0 — ночь, ph=1 — утро.
function bedScene(g,t,ph){
  g.fillStyle='rgba(74,47,36,.08)';g.fillRect(0,640,840,350);
  rr(g,30,300,40,360,14);fs(g,P.choc);rr(g,770,420,40,240,14);fs(g,P.choc); // спинки
  rr(g,60,470,720,150,26);fs(g,P.cream); // матрас
  for(const x of [90,750]){rr(g,x-12,620,24,50,8);fs(g,P.choc,null)}
  rr(g,80,395,180,100,44);fs(g,'#FFFFFF'); // подушка
  yarikHeadLying(g,180,425,.42,ph?'norm':'bad',t,560,ph?null:1);
  g.beginPath();g.moveTo(262,512);g.bezierCurveTo(252,410,266,362,318,358);g.bezierCurveTo(420,352,560,370,700,392);g.bezierCurveTo(750,402,770,450,770,520);g.lineTo(770,560);g.lineTo(250,560);g.closePath();fs(g,P.terraL);
  g.strokeStyle='rgba(246,238,221,.55)';g.lineWidth=9;for(const x of [380,520,660]){g.beginPath();g.moveTo(x,368);g.quadraticCurveTo(x-8,470,x,556);g.stroke()}
  // тумбочка с бутылкой воды
  rr(g,70,780,200,150,14);fs(g,'#D9C4A6');g.strokeStyle=P.choc;g.lineWidth=4;g.beginPath();g.moveTo(70,855);g.lineTo(270,855);g.stroke();
  at(g,170,690,.85*pop(t,.5),()=>waterBottle(g));
}
