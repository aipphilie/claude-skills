// node layout.js <engineDir> <out.png> <t>
const {chromium}=require('playwright');const fs=require('fs');const [dir,out,T]=process.argv.slice(2);
(async()=>{const b=await chromium.launch();const p=await b.newPage();p.on('pageerror',e=>console.log('ERR',e.message));
await p.setContent(`<html><body style="margin:0"><canvas id=c width=1080 height=1920></canvas><script>${fs.readFileSync(dir+'/yarik.js','utf8')}\n${fs.readFileSync(dir+'/scenes.js','utf8')}\n${fs.readFileSync(dir+'/lie.js','utf8')}</script></body></html>`);
await p.evaluate(()=>Promise.all([document.fonts.load('900 50px Inter'),document.fonts.load('800 50px Inter')]));
const d=await p.evaluate(T=>{const c=document.getElementById('c'),g=c.getContext('2d');render(g,+T);
 const R='#D9503F';g.save();g.setLineDash([14,10]);g.lineWidth=4;
 g.strokeStyle='rgba(46,125,190,.9)';g.strokeRect(56,250,866,1350); // безопасная зона
 g.strokeStyle=R;g.strokeRect(158,515,764,900); // карточка
 g.beginPath();g.moveTo(540,0);g.lineTo(540,1920);g.strokeStyle='rgba(217,80,63,.45)';g.lineWidth=2;g.stroke();g.setLineDash([]);
 const lab=(s,x,y,col=R,al='left')=>{g.font='800 26px Inter';const w=g.measureText(s).width;const X=al==='left'?x:x-w;g.fillStyle='rgba(255,255,255,.92)';g.fillRect(X-8,y-26,w+16,36);g.fillStyle=col;g.textAlign='left';g.fillText(s,X,y)};
 lab('строка 1 заголовка: y=288, 56px choc',60,240);
 lab('плашка: y 334–438, текст 60–64px',60,470);
 lab('карточка 764×900: x 158–922, y 515–1415',166,560);
 lab('фаза (meter) 742,128 в карточке',910,640,R,'right');
 lab('субтитры: центр y=1490, 50px, обводка 12',60,1560);
 lab('безопасная зона 866×1350 (56..922, 250..1600)',60,1650,'rgb(46,125,190)');
 lab('низ 320px — интерфейс Reels, пусто',60,1700,'rgb(46,125,190)');
 lab('центр x=540',548,1880);
 g.restore();return c.toDataURL('image/jpeg',.9)},T);
fs.writeFileSync(out,Buffer.from(d.split(',')[1],'base64'));await b.close()})();
