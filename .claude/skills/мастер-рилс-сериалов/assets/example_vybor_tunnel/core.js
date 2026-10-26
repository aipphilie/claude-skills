// ===== core: utils, noise, textures, overlays =====
const W=1080,H=1920,FPS=30;
const cv=document.getElementById('c');cv.width=W;cv.height=H;
const ctx=cv.getContext('2d');
const MONO='"DejaVu Sans Mono", monospace';

function rng(seed){return function(){seed|=0;seed=seed+0x6D2B79F5|0;let t=Math.imul(seed^seed>>>15,1|seed);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
const clamp=(x,a,b)=>Math.max(a,Math.min(b,x));
const lerp=(a,b,t)=>a+(b-a)*t;
const ease=t=>{t=clamp(t,0,1);return t*t*(3-2*t)};
const easeOut=t=>{t=clamp(t,0,1);return 1-Math.pow(1-t,3)};
const easeIn=t=>{t=clamp(t,0,1);return t*t*t};
const easeOutBack=t=>{t=clamp(t,0,1);const c1=1.70158,c3=c1+1;return 1+c3*Math.pow(t-1,3)+c1*Math.pow(t-1,2)};
const seg=(t,a,b)=>clamp((t-a)/(b-a),0,1);
function mk(w=W,h=H){const c=document.createElement('canvas');c.width=w;c.height=h;return c}
function glow(g,x,y,r,rgb,a){if(r<=0)return;const gr=g.createRadialGradient(x,y,0,x,y,r);gr.addColorStop(0,`rgba(${rgb},${a})`);gr.addColorStop(.35,`rgba(${rgb},${a*.45})`);gr.addColorStop(1,`rgba(${rgb},0)`);g.fillStyle=gr;g.fillRect(x-r,y-r,r*2,r*2)}

// periodic value noise -> Float32Array in [0,1]
function noiseField(w,h,seed,cell,oct=4,pers=.5){
  const out=new Float32Array(w*h);const R=rng(seed);let amp=1,tot=0;
  for(let o=0;o<oct;o++){
    const cw=Math.max(1,Math.round(w/cell)),ch=Math.max(1,Math.round(h/cell));
    const lat=new Float32Array(cw*ch);for(let i=0;i<lat.length;i++)lat[i]=R();
    const sx=cw/w,sy=ch/h;
    for(let y=0;y<h;y++){const fy=y*sy,y0=Math.floor(fy),ty=fy-y0,uy=ty*ty*(3-2*ty),r0=(y0%ch)*cw,r1=((y0+1)%ch)*cw;
      for(let x=0;x<w;x++){const fx=x*sx,x0=Math.floor(fx),tx=fx-x0,ux=tx*tx*(3-2*tx),a0=x0%cw,a1=(x0+1)%cw;
        const v=lerp(lerp(lat[r0+a0],lat[r0+a1],ux),lerp(lat[r1+a0],lat[r1+a1],ux),uy);out[y*w+x]+=v*amp}}
    tot+=amp;amp*=pers;cell/=2;}
  for(let i=0;i<out.length;i++)out[i]/=tot;return out}
function fieldCanvas(w,h,f,map){const c=mk(w,h),g=c.getContext('2d'),d=g.createImageData(w,h);
  for(let i=0,p=0;i<f.length;i++,p+=4){const [r,gg,b,a]=map(f[i],i%w,(i/w)|0);d.data[p]=r;d.data[p+1]=gg;d.data[p+2]=b;d.data[p+3]=a}
  g.putImageData(d,0,0);return c}

// ---- shared textures ----
const SMOKE=[];// tileable smoke sheets
for(let k=0;k<3;k++){const f=noiseField(512,512,40+k,128,5,.55);
  SMOKE.push(fieldCanvas(512,512,f,v=>{const a=clamp((v-.38)*2.4,0,1);return[200,186,160,Math.pow(a,1.4)*255]}))}
const GRAIN=[];for(let k=0;k<6;k++){const c=mk(540,960),g=c.getContext('2d'),d=g.createImageData(540,960),R=rng(100+k);
  for(let i=0;i<d.data.length;i+=4){const v=R()*255;d.data[i]=d.data[i+1]=d.data[i+2]=v;d.data[i+3]=255}g.putImageData(d,0,0);GRAIN.push(c)}
const GRIME=(()=>{const f=noiseField(540,960,7,140,6,.6);return fieldCanvas(540,960,f,(v,x,y)=>{const a=clamp((v-.45)*3,0,1);return[20,22,16,a*170]})})();
const SPECK=(()=>{const c=mk(1080,1920),g=c.getContext('2d'),R=rng(77);for(let i=0;i<9000;i++){g.fillStyle=R()<.5?`rgba(255,255,240,${R()*.10})`:`rgba(0,0,0,${R()*.25})`;const s=1+R()*2.5;g.fillRect(R()*W,R()*H,s,s)}return c})();

// draws smoke sheet tiled across rect, scrolling
function smoke(g,t,x,y,w,h,{alpha=.6,scale=1.6,vx=-30,vy=-18,sheet=0,tint=null,comp='source-over'}={}){
  const S=SMOKE[sheet],tw=512*scale,th=512*scale;
  g.save();g.beginPath();g.rect(x,y,w,h);g.clip();g.globalAlpha=alpha;g.globalCompositeOperation=comp;
  let ox=((t*vx)%tw+tw)%tw,oy=((t*vy)%th+th)%th;
  for(let yy=y-th+oy;yy<y+h;yy+=th)for(let xx=x-tw+ox;xx<x+w;xx+=tw)g.drawImage(S,xx,yy,tw,th);
  if(tint){g.globalCompositeOperation='source-atop';g.globalAlpha=1;g.fillStyle=tint;g.fillRect(x,y,w,h)}
  g.restore()}
// soft smoke blob layer with mask gradient (falls off at edges)
function smokeMasked(g,t,x,y,w,h,opts,maskFn){
  const L=mk(W,H),lg=L.getContext('2d');smoke(lg,t,x,y,w,h,{...opts,alpha:1});
  lg.globalCompositeOperation='destination-in';maskFn(lg);g.save();g.globalAlpha=opts.alpha??.6;g.drawImage(L,0,0);g.restore()}
const TMP=mk();
function layer(){const g=TMP.getContext('2d');g.setTransform(1,0,0,1,0,0);g.globalAlpha=1;g.globalCompositeOperation='source-over';g.clearRect(0,0,W,H);return g}

// particles (dust in beams / sparks)
const DUST=[];{const R=rng(5);for(let i=0;i<420;i++)DUST.push({x:R()*W,y:R()*H,z:.3+R()*1.2,p:R()*9,s:R()})}
function dust(g,t,rgb,amt=1,clipFn){g.save();if(clipFn){clipFn(g);g.clip()}
  for(const d of DUST){const x=(d.x+Math.sin(t*.5+d.p)*30+t*8*d.z)%W,y=(d.y-t*14*d.z+H*10)%H;const a=(.25+.6*Math.abs(Math.sin(t*1.7+d.p)))*amt;
    g.fillStyle=`rgba(${rgb},${a})`;const s=1.2+d.z*2;g.beginPath();g.arc(x,y,s,0,7);g.fill()}g.restore()}

function finish(t,{vig=.75,grain=.09}={}){
  ctx.setTransform(1,0,0,1,0,0);
  ctx.globalCompositeOperation='overlay';ctx.globalAlpha=grain;ctx.drawImage(GRAIN[Math.floor(t*FPS)%6],0,0,W,H);
  ctx.globalCompositeOperation='source-over';ctx.globalAlpha=1;
  const v=ctx.createRadialGradient(W/2,H*.46,H*.25,W/2,H*.5,H*.75);
  v.addColorStop(0,'rgba(0,0,0,0)');v.addColorStop(1,`rgba(0,0,0,${vig})`);ctx.fillStyle=v;ctx.fillRect(0,0,W,H)}

// ---- dot-matrix LED text ----
const DOTC=mk(400,40);
function ledText(g,txt,x,y,dot,{col='255,150,40',font='bold 15px '+MONO,on=1,align='left',cols=null}={}){
  const dg=DOTC.getContext('2d');dg.clearRect(0,0,400,40);dg.fillStyle='#fff';dg.font=font;dg.textBaseline='top';dg.fillText(txt,1,2);
  const tw=Math.min(400,Math.ceil(dg.measureText(txt).width)+2),th=20,d=dg.getImageData(0,0,tw,th).data;
  const ox=align==='center'?x-tw*dot/2:x;
  for(let j=0;j<th;j++)for(let i=0;i<tw;i++){const v=d[(j*tw+i)*4+3]/255;const cx=ox+i*dot+dot/2,cy=y+j*dot+dot/2;
    g.fillStyle=`rgba(${col},${v>.45?on:.07})`;g.beginPath();g.arc(cx,cy,dot*.36,0,7);g.fill()}
  return tw*dot}

// ---- subtitles ----
function subtitle(t,items){
  for(const it of items){if(t<it.s||t>it.e)continue;const k=easeOut(seg(t,it.s,it.s+.12));
    ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.font='76px MB';ctx.textAlign='center';ctx.textBaseline='middle';
    const y=it.y||1480;ctx.translate(540,y);ctx.scale(.85+.15*k,.85+.15*k);ctx.globalAlpha=k;
    ctx.lineWidth=14;ctx.strokeStyle='rgba(0,0,0,.85)';ctx.lineJoin='round';ctx.strokeText(it.txt,0,0);
    ctx.fillStyle=it.col||'#fff';ctx.fillText(it.txt,0,0);ctx.restore()}}
