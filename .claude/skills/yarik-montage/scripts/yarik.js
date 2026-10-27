// Ярик — плоский 2D-бюст. Локальные координаты: центр лица (0,0), глаза y≈-25, подбородок y≈224, макушка y≈-265.
// opts: {emo:'norm'|'bad'|'shock', cap:true (по умолчанию, фирменная кепка назад; false — без кепки), blink:0..1, look:-1..1}
const YARIK_PAL={
  beige:'#E9D8BF',cream:'#F6EEDD',peach:'#F3C7A6',terra:'#C26A4E',sage:'#9DB38F',mustard:'#D9A441',choc:'#4A2F24'};
const YC={
  skin:'#F3C7A6',skinSh:'#E3AB89',skinDeep:'#CF9373',blush:'rgba(226,128,104,.16)',
  hair:'#3A261C',hairL:'#56392B',hairFade:'rgba(58,38,28,.38)',
  brow:'#33211A',line:'#4A2F24',lip:'#CC8C79',lipL:'#DDA290',lipD:'#A9685A',
  iris:'#6E4329',white:'#FBF5EA',
  shirt:'#B8B0A6',shirtSh:'#A1988E',shirtL:'#C9C2B9',rib:'#ABA399',
  cap:'#4A3A33',capL:'#5D4A41',capD:'#382A24'};

function yPath(g,cmds){g.beginPath();for(const c of cmds){const [k,...a]=c;
  if(k==='M')g.moveTo(...a);else if(k==='L')g.lineTo(...a);else if(k==='C')g.bezierCurveTo(...a);else if(k==='Q')g.quadraticCurveTo(...a);else if(k==='Z')g.closePath()}}
function yFill(g,cmds,fill,stroke,lw=6){yPath(g,cmds);if(fill){g.fillStyle=fill;g.fill()}if(stroke){g.strokeStyle=stroke;g.lineWidth=lw;g.lineJoin='round';g.lineCap='round';g.stroke()}}
function yLine(g,cmds,col,lw){yPath(g,cmds);g.strokeStyle=col;g.lineWidth=lw;g.lineCap='round';g.lineJoin='round';g.stroke()}

const FACE=[['M',-148,-130],['C',-160,-50,-158,20,-150,70],['C',-145,130,-132,172,-100,200],
  ['C',-70,222,-36,230,0,230],['C',36,230,70,222,100,200],['C',132,172,145,130,150,70],
  ['C',158,20,160,-50,148,-130],['C',138,-225,70,-262,0,-264],['C',-70,-262,-138,-225,-148,-130],['Z']];

function drawYarik(g,o={}){
  const emo=o.emo||'norm',L=YC.line,blink=o.blink||0,look=o.look||0;
  const E={ // параметры эмоций
    norm:{bIn:0,bOut:3,bArch:3,lid:.42,low:1,mouth:'pout'},
    bad:{bIn:-14,bOut:10,bArch:0,lid:.32,low:1,mouth:'frown'},
    shock:{bIn:-30,bOut:-22,bArch:10,lid:1.25,low:1.25,mouth:'open'}}[emo];
  g.save();
  // ---- тело: свитшот ----
  yFill(g,[['M',-430,720],['C',-428,520,-400,410,-300,365],['C',-220,330,-150,300,-112,280],['L',112,280],
    ['C',150,300,220,330,300,365],['C',400,410,428,520,430,720],['Z']],YC.shirt,L,7);
  g.save();yPath(g,[['M',-430,720],['C',-428,520,-400,410,-300,365],['C',-220,330,-150,300,-112,280],['L',112,280],
    ['C',150,300,220,330,300,365],['C',400,410,428,520,430,720],['Z']]);g.clip();
  g.fillStyle=YC.shirtSh;g.beginPath();g.moveTo(140,300);g.bezierCurveTo(260,360,330,430,360,720);g.lineTo(440,720);g.lineTo(440,300);g.fill();
  g.fillStyle=YC.shirtL;g.beginPath();g.moveTo(-300,380);g.bezierCurveTo(-360,420,-390,500,-395,720);g.lineTo(-340,720);g.bezierCurveTo(-335,520,-310,440,-260,390);g.fill();g.restore();
  yLine(g,[['M',-300,420],['C',-290,520,-280,620,-282,720]],'rgba(74,47,36,.35)',4); // плечевые швы
  yLine(g,[['M',300,420],['C',290,520,280,620,282,720]],'rgba(74,47,36,.35)',4);
  // ---- шея ----
  yFill(g,[['M',-116,150],['C',-118,220,-122,262,-126,292],['C',-60,330,60,330,126,292],['C',122,262,118,220,116,150],['Z']],YC.skin,L,6);
  g.save();yPath(g,[['M',-116,150],['C',-118,220,-122,262,-126,292],['C',-60,330,60,330,126,292],['C',122,262,118,220,116,150],['Z']]);g.clip();
  g.fillStyle=YC.skinSh;yPath(g,[['M',-140,140],['L',140,140],['L',140,215],['C',60,262,-60,262,-140,215],['Z']]);g.fill();g.fillRect(84,140,60,200);
  if(emo==='bad'){g.fillStyle='rgba(157,179,143,.32)';g.fillRect(-140,140,280,200)}
  g.restore();yLine(g,[['M',-10,255],['Q',0,268,10,255]],'rgba(74,47,36,.35)',3); // ямка
  // ворот-резинка
  yFill(g,[['M',-128,284],['C',-70,336,70,336,128,284],['C',138,296,142,306,140,318],['C',70,372,-70,372,-140,318],['C',-142,306,-138,296,-128,284],['Z']],YC.rib,L,6);
  g.strokeStyle='rgba(74,47,36,.22)';g.lineWidth=2;for(let i=-9;i<=9;i++){const x=i*14;g.beginPath();g.moveTo(x,313+Math.abs(x)*.02-Math.abs(x)*Math.abs(x)*.0018);g.lineTo(x*1.02,346-Math.abs(x)*Math.abs(x)*.0016);g.stroke()}
  // ---- уши ----
  for(const s of [-1,1]){
    yFill(g,[['M',s*144,-36],['C',s*176,-58,s*198,-30,s*194,8],['C',s*192,44,s*178,72,s*150,80],['Z']],YC.skin,L,6);
    yLine(g,[['M',s*154,-22],['C',s*180,-34,s*184,0,s*176,22],['C',s*170,40,s*160,46,s*156,40]],YC.skinDeep,5);
    yFill(g,[['M',s*158,0],['C',s*172,6,s*170,26,s*158,30],['Z']],'rgba(207,147,115,.6)');
    if(emo==='bad')yFill(g,[['M',s*144,-36],['C',s*176,-58,s*198,-30,s*194,8],['C',s*192,44,s*178,72,s*150,80],['Z']],'rgba(157,179,143,.32)');
  }
  // ---- лицо ----
  yFill(g,FACE,YC.skin);
  g.save();yPath(g,FACE);g.clip();
  // тень справа (свет слева) + под скулой
  g.fillStyle=YC.skinSh;g.beginPath();g.moveTo(96,-180);g.bezierCurveTo(118,-60,128,40,108,120);g.bezierCurveTo(92,170,60,205,20,230);g.lineTo(200,240);g.lineTo(200,-200);g.fill();
  if(emo==='bad'){g.fillStyle='rgba(157,179,143,.32)';g.fillRect(-170,-140,340,380)} // зеленоватый с похмелья
  // румянец
  g.fillStyle=emo==='bad'?'rgba(226,128,104,.12)':YC.blush;
  for(const s of [-1,1]){g.beginPath();g.ellipse(s*100,52,38,24,0,0,7);g.fill()}
  g.restore();
  yFill(g,FACE,null,L,7);
  // ---- волосы: французский кроп ----
  if(o.cap===false){
    // фейд по вискам
    for(const s of [-1,1])yFill(g,[['M',s*152,-108],['C',s*157,-80,s*156,-52,s*152,-30],['L',s*141,-34],['C',s*141,-66,s*140,-92,s*136,-118],['Z']],YC.hairFade);
    // короткая неровная чёлка, углы чуть залысиной вверх
    const OFF=[0,5,1,7,2,6,0,6,2,5,1,4,0],fr=[];
    for(let i=0;i<OFF.length;i++){const x=-118+236*i/(OFF.length-1),ax=Math.abs(x);fr.push([x,-132+OFF[i]*(emo==='bad'?1.6:1)-(ax>80?(ax-80)*.45:0)])}
    const hair=[['M',-153,-104],['C',-168,-200,-112,-274,0,-276],['C',112,-274,168,-200,153,-104],['L',138,-146]];
    for(let i=fr.length-1;i>=0;i--)hair.push(['L',...fr[i]]);
    hair.push(['L',-138,-146],['Z']);
    yFill(g,hair,YC.hair,L,6);
    // текстура: короткие пряди вперёд
    g.save();yPath(g,hair);g.clip();g.strokeStyle=YC.hairL;g.lineWidth=5;g.lineCap='round';
    for(const [x,y,dx,dy] of [[-120,-190,14,30],[-92,-226,12,34],[-58,-246,8,36],[-20,-256,4,38],[22,-254,-2,36],[60,-244,-8,34],[96,-222,-12,32],[124,-186,-14,30],
      [-100,-170,8,26],[-60,-196,6,30],[-18,-206,2,30],[24,-204,-2,30],[66,-192,-6,28],[104,-166,-8,24]]){g.beginPath();g.moveTo(x,y);g.quadraticCurveTo(x+dx*.2,y+dy*.6,x+dx,y+dy);g.stroke()}
    g.strokeStyle='rgba(120,86,66,.5)';g.lineWidth=10;g.beginPath();g.moveTo(-110,-238);g.quadraticCurveTo(-40,-276,40,-266);g.stroke();
    g.restore();
    if(emo==='bad'){ // торчат пряди
      for(const [x,y,tx,ty] of [[-60,-262,-84,-300],[-10,-272,-6,-312],[40,-268,66,-300],[96,-240,128,-262]])yFill(g,[['M',x-16,y+6],['Q',(x+tx)/2-10,(y+ty)/2,tx,ty],['Q',(x+tx)/2+10,(y+ty)/2+6,x+16,y+8],['Z']],YC.hair,L,5);
    }
  }else{
    // кепка козырьком назад
    yFill(g,[['M',-160,-100],['C',-176,-230,-100,-300,0,-302],['C',100,-300,176,-230,160,-100],['C',100,-128,-100,-128,-160,-100],['Z']],YC.cap,L,6);
    g.save();yPath(g,[['M',-160,-100],['C',-176,-230,-100,-300,0,-302],['C',100,-300,176,-230,160,-100],['C',100,-128,-100,-128,-160,-100],['Z']]);g.clip();
    g.fillStyle=YC.capL;g.beginPath();g.ellipse(-70,-220,90,70,-.4,0,7);g.fill();
    g.fillStyle=YC.capD;g.beginPath();g.moveTo(80,-300);g.bezierCurveTo(150,-250,170,-180,170,-100);g.lineTo(200,-100);g.lineTo(200,-300);g.fill();g.restore();
    yLine(g,[['M',0,-300],['C',-6,-240,-6,-180,-4,-126]],'rgba(30,20,16,.35)',4);
    // застёжка спереди (кепка задом наперёд): окошко с ремешком и чёлка под ним
    yFill(g,[['M',-72,-118],['C',-74,-160,-60,-180,-40,-184],['L',40,-184],['C',60,-180,74,-160,72,-118],['Z']],YC.hair,L,5);
    yFill(g,[['M',-80,-150],['L',80,-150],['L',80,-128],['L',-80,-128],['Z']],YC.capD,L,5);
    g.fillStyle='#9C8A7E';g.fillRect(-14,-147,28,16);
    // короткие волосы из-под кепки на висках
    for(const s of [-1,1])yFill(g,[['M',s*156,-104],['C',s*158,-80,s*156,-56,s*152,-34],['L',s*140,-38],['C',s*140,-66,s*138,-88,s*134,-108],['Z']],YC.hairFade);
  }
  // ---- брови ----
  for(const s of [-1,1]){
    const iy=-60+E.bIn,oy=-56+E.bOut,ix=s*34,ox=s*138,mx=s*96,my=(iy+oy)/2-E.bArch-4;
    yFill(g,[['M',ix,iy+11],['C',ix+s*6,iy-10,mx-s*18,my-10,mx,my-10],['C',mx+s*20,my-10,ox-s*10,oy-8,ox,oy+2],
      ['C',ox-s*16,oy+2,mx+s*10,my+6,mx,my+7],['C',mx-s*24,my+8,ix+s*10,iy+12,ix,iy+9],['Z']],YC.brow);
  }
  if(emo==='bad')yLine(g,[['M',-12,-78],['L',-8,-60]],'rgba(74,47,36,.45)',3),yLine(g,[['M',12,-78],['L',8,-60]],'rgba(74,47,36,.45)',3);
  if(emo==='shock'){for(const y of [-128,-112])yLine(g,[['M',-40,y],['Q',0,y-8,40,y]],'rgba(74,47,36,.35)',3)}
  // ---- глаза ----
  for(const s of [-1,1]){
    const ex=s*78,ey=-24,w=34,lid=E.lid*(1-blink),top=ey-24*lid,bot=ey+10*E.low;
    // складка века (тяжёлое веко — фирменное)
    yLine(g,[['M',ex-w,ey-6],['Q',ex,ey-30-(emo==='shock'?14:0),ex+w,ey-8]],'rgba(74,47,36,.45)',3);
    if(lid>.05){
      const eye=[['M',ex-w,ey],['C',ex-w*.5,top,ex+w*.5,top,ex+w,ey-2],['C',ex+w*.5,bot,ex-w*.5,bot,ex-w,ey],['Z']];
      yFill(g,eye,YC.white);
      g.save();yPath(g,eye);g.clip();
      const ir=emo==='shock'?11:15,px=ex+look*10,py=ey+(emo==='bad'?3:-1);
      g.fillStyle=YC.iris;g.beginPath();g.arc(px,py,ir,0,7);g.fill();
      g.fillStyle='#21140E';g.beginPath();g.arc(px,py,ir*.45,0,7);g.fill();
      g.fillStyle='#fff';g.beginPath();g.arc(px-ir*.35,py-ir*.4,ir*.28,0,7);g.fill();
      g.fillStyle='rgba(74,47,36,.25)';g.fillRect(ex-w-2,top-2,w*2+4,6);g.restore();
      yLine(g,[['M',ex-w-2,ey+1],['C',ex-w*.5,top-1,ex+w*.5,top-1,ex+w+2,ey-3]],L,6);
      yLine(g,[['M',ex-w*.7,ey+(bot-ey)*.6],['C',ex-w*.2,bot+1,ex+w*.3,bot+1,ex+w*.8,ey+(bot-ey)*.5]],'rgba(74,47,36,.5)',3);
    }else yLine(g,[['M',ex-w,ey],['Q',ex,ey+8,ex+w,ey-2]],L,6);
    if(emo==='bad'){ // мешки
      yLine(g,[['M',ex-w*.8,ey+20],['Q',ex,ey+32,ex+w*.8,ey+18]],'rgba(150,90,110,.55)',5);
      yLine(g,[['M',ex-w*.5,ey+30],['Q',ex,ey+38,ex+w*.5,ey+28]],'rgba(150,90,110,.3)',3);
    }
  }
  // ---- нос: прямой, широковатый, кончик мягкий и крупный ----
  yLine(g,[['M',14,-46],['C',18,-14,22,14,28,30]],'rgba(207,147,115,.9)',6); // тень спинки справа
  yLine(g,[['M',-12,-40],['C',-14,-14,-16,8,-20,22]],'rgba(255,232,214,.55)',5); // блик спинки слева
  g.fillStyle='rgba(255,232,214,.45)';g.beginPath();g.ellipse(-4,40,9,6,0,0,7);g.fill(); // блик кончика
  for(const s of [-1,1])yLine(g,[['M',s*24,22],['C',s*42,24,s*48,42,s*38,54]],L,5); // крылья
  yLine(g,[['M',-12,62],['Q',0,67,12,62]],L,4); // низ кончика
  for(const s of [-1,1])yFill(g,[['M',s*12,58],['C',s*16,51,s*28,51,s*32,56],['C',s*26,61,s*18,62,s*12,58],['Z']],'#7E4A3B');
  yFill(g,[['M',-26,64],['C',-10,72,10,72,26,64],['C',14,70,-14,70,-26,64],['Z']],'rgba(207,147,115,.7)'); // тень под носом
  // носогубный желобок
  yLine(g,[['M',-7,72],['L',-9,90]],'rgba(207,147,115,.8)',3);yLine(g,[['M',7,72],['L',9,90]],'rgba(207,147,115,.8)',3);
  // ---- губы: полные, выраженная «галочка» верхней ----
  if(E.mouth==='pout'||E.mouth==='frown'){
    const d=E.mouth==='frown'?1:0,cy=114,hw=56;
    const up=[['M',-hw,cy+d*14],['C',-40,cy-10,-22,cy-26,-9,cy-21],['Q',0,cy-15,9,cy-21],['C',22,cy-26,40,cy-10,hw,cy+d*14],
      ['C',30,cy+2-d*4,10,cy+(d?-3:2),0,cy+(d?-4:2)],['C',-10,cy+(d?-3:2),-30,cy+2-d*4,-hw,cy+d*14],['Z']];
    const lo=[['M',-hw+6,cy+2+d*8],['C',-30,cy+4-d*4,30,cy+4-d*4,hw-6,cy+2+d*8],['C',36,cy+36-d*2,-36,cy+36-d*2,-hw+6,cy+2+d*8],['Z']];
    yFill(g,lo,YC.lipL,L,5);yFill(g,[['M',-20,cy+12],['C',-8,cy+8,8,cy+8,20,cy+12],['C',10,cy+16,-10,cy+16,-20,cy+12],['Z']],'rgba(255,240,230,.5)');
    yFill(g,up,YC.lip,L,5);
    yLine(g,[['M',-hw,cy+d*14],['C',-30,cy+2-d*4,-10,cy+(d?-3:2),0,cy+(d?-4:2)],['C',10,cy+(d?-3:2),30,cy+2-d*4,hw,cy+d*14]],YC.lipD,5);
    if(!d){yLine(g,[['M',hw-2,cy+1],['Q',hw+6,cy-2,hw+9,cy+3]],'rgba(74,47,36,.45)',3)} // лёгкая ухмылка с одной стороны
    yLine(g,[['M',-22,cy+48-d*2],['Q',0,cy+54-d*2,22,cy+48-d*2]],'rgba(207,147,115,.9)',4); // складка под губой
  }else{ // шок: рот открыт
    const cy=118;
    yFill(g,[['M',-40,cy-14],['C',-38,cy-34,38,cy-34,40,cy-14],['C',44,cy+30,22,cy+52,0,cy+52],['C',-22,cy+52,-44,cy+30,-40,cy-14],['Z']],'#5A2A22',L,6);
    g.save();yPath(g,[['M',-40,cy-14],['C',-38,cy-34,38,cy-34,40,cy-14],['C',44,cy+30,22,cy+52,0,cy+52],['C',-22,cy+52,-44,cy+30,-40,cy-14],['Z']]);g.clip();
    g.fillStyle=YC.white;g.fillRect(-36,cy-34,72,16);g.fillStyle='#C9706A';g.beginPath();g.ellipse(0,cy+50,26,16,0,0,7);g.fill();g.restore();
    yFill(g,[['M',-46,cy-16],['C',-30,cy-40,-12,cy-44,-6,cy-38],['Q',0,cy-34,6,cy-38],['C',12,cy-44,30,cy-40,46,cy-16],['C',30,cy-26,-30,cy-26,-46,cy-16],['Z']],YC.lip,L,5);
    yFill(g,[['M',-44,cy-6],['C',-46,cy+36,-24,cy+62,0,cy+62],['C',24,cy+62,46,cy+36,44,cy-6],['C',40,cy+30,22,cy+50,0,cy+50],['C',-22,cy+50,-40,cy+30,-44,cy-6],['Z']],YC.lipL,L,5);
  }
  // родинка на правой щеке (как на фото)
  g.fillStyle='#8A5A45';g.beginPath();g.arc(128,96,3.5,0,7);g.fill();
  // ---- эффекты эмоций ----
  if(emo==='bad'||emo==='shock'){
    const drops=emo==='bad'?[[150,-150,1]]:[[-170,-170,1],[175,-140,.8]];
    for(const [x,y,k] of drops){yFill(g,[['M',x,y-26*k],['C',x+16*k,y-4*k,x+16*k,y+12*k,x,y+14*k],['C',x-16*k,y+12*k,x-16*k,y-4*k,x,y-26*k],['Z']],'#BFD9DE',L,4);
      g.fillStyle='rgba(255,255,255,.8)';g.beginPath();g.ellipse(x-5*k,y,3*k,6*k,0,0,7);g.fill()}
  }
  if(emo==='shock'){g.strokeStyle=YARIK_PAL.choc;g.lineWidth=9;g.lineCap='round';
    for(const [a,r1,r2] of [[-2.5,300,350],[-2.0,320,375],[-1.15,320,375],[-.65,300,350]]){g.beginPath();g.moveTo(Math.cos(a)*r1,-40+Math.sin(a)*r1);g.lineTo(Math.cos(a)*r2,-40+Math.sin(a)*r2);g.stroke()}}
  if(emo==='bad'){ // спираль головокружения
    g.strokeStyle=YARIK_PAL.cream;g.lineWidth=6;g.lineCap='round';g.beginPath();
    for(let i=0;i<=60;i++){const a=i/60*Math.PI*5,r=4+i*.55;const x=-190+Math.cos(a)*r,y=-250+Math.sin(a)*r*.7;i?g.lineTo(x,y):g.moveTo(x,y)}g.stroke();
  }
  g.restore();
}
if(typeof module!=='undefined')module.exports={drawYarik,YARIK_PAL,YC};
