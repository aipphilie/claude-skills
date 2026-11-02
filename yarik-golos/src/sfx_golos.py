# python3 sfx.py ev.json out.wav — звуки монтажа (синтез, без чужих сэмплов) + тихий бит под весь ролик
import json,sys,numpy as np
from scipy.signal import butter,lfilter
from scipy.io import wavfile
SR=48000;d=json.load(open(sys.argv[1]));N=int((d['total']+1)*SR);out=np.zeros(N);rng=np.random.default_rng(7)
def bp(x,lo,hi):b,a=butter(2,[lo/(SR/2),hi/(SR/2)],'band');return lfilter(b,a,x)
def env(n,a=.005,r=None):t=np.arange(n)/SR;e=np.minimum(1,t/a);return e*np.exp(-t/(r or n/SR/4))
def put(t,x,g=1.0):
  i=int(t*SR)
  if i<0 or i>=N:return
  j=min(N,i+len(x));out[i:j]+=x[:j-i]*g
def noise(s):return rng.standard_normal(int(s*SR))
def tone(f,s,r=.08):n=int(s*SR);t=np.arange(n)/SR;return np.sin(2*np.pi*f*t)*env(n,.002,r)
def kick(s=.25):n=int(s*SR);t=np.arange(n)/SR;f=50+90*np.exp(-t*30);return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*12)
def whoosh(s=.28):n=int(s*SR);x=bp(noise(s),600,5000);t=np.arange(n)/SR;return x*np.sin(np.pi*t/s)**2
def click():return bp(noise(.02),2000,8000)*env(int(.02*SR),.001,.004)
def knock():return bp(noise(.08),150,900)*env(int(.08*SR),.001,.015)*3+kick(.08)[:int(.08*SR)]*.5
def pssh():return bp(noise(.35),3000,10000)*env(int(.35*SR),.004,.1)
def thud():
  k=kick(.3)*1.2;k[:int(.1*SR)]+=bp(noise(.1),100,600)*env(int(.1*SR),.001,.03);return k
def ding():return tone(1320,.6,.25)+.5*tone(2640,.6,.15)
def jingle():return sum(tone(f,.25,.06) for f in (3100,4200,5300))*.5
EV={}
for e in d['ev']:
  t,sc,sh=e['t'],e['scene'],e['shot'];EV[(sc,sh)]=t
  if sh>0 or sc>0:put(t-.06,whoosh(),.10)
nxt=lambda k,dt:EV.get(k,0)+dt
g=lambda k:EV.get(k)
def honk(s=.32):
  n=int(s*SR);t=np.arange(n)/SR;x=np.sign(np.sin(2*np.pi*420*t))+np.sign(np.sin(2*np.pi*530*t));return bp(x,300,3000)*env(n,.01,.2)*.5
def boing(s=.5):
  n=int(s*SR);t=np.arange(n)/SR;f=120+260*np.exp(-t*6)*(1+.3*np.sin(t*40));return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*5)
def gulp():
  n=int(.12*SR);t=np.arange(n)/SR;f=300-200*t/.12;return np.sin(2*np.pi*np.cumsum(f)/SR)*np.sin(np.pi*t/.12)
def creak(s=1.0):
  n=int(s*SR);t=np.arange(n)/SR;f=180+60*np.sin(t*5);x=np.sign(np.sin(2*np.pi*np.cumsum(f)/SR));return bp(x,400,2500)*np.sin(np.pi*t/s)*.4
def clap():return bp(noise(.03),800,6000)*env(int(.03*SR),.001,.008)
# --- серия «Голос на записи» ---
# хук: «дзынь» отправки голосового + бум на «ЧТО ЭТО?!»
put(g((0,0))+.02,ding(),.25);put(g((0,1))-.04,thud(),.5)
# штампы ИМЯ / ГОРОД / ГОЛОС
for k in (3,4,5):put(g((1,k))+.04,thud(),.4)
# интрига: сердце в тишине
for i in range(3):put(g((2,0))+.3+i*.8,kick(.2),.35);put(g((2,0))+.5+i*.8,kick(.2),.25)
# АЙ! — дверь
put(g((3,4))+.05,thud(),.6);put(g((3,4))+.12,boing(),.3)
# фирменный переход внутрь: вжух-тоннель
x0=g((4,0))+.4;n=int(1.6*SR);x=bp(noise(1.6),300,4000)*np.linspace(0,1,n)**2;put(x0,x,.3)
# ПУТЬ 1 / ПУТЬ 2
put(g((5,0))+.03,thud(),.45);put(g((5,3))+.03,thud(),.45)
# кости гудят: низкий тон
n=int(1.8*SR);t=np.arange(n)/SR;put(g((5,4))+.1,np.sin(2*np.pi*70*t)*np.sin(np.pi*t/1.8),.35)
# без басов / без бархата / как есть
put(g((6,4))+.2,thud(),.4);put(g((6,5))+.05,thud(),.4);put(g((6,6))+.05,boing(),.35)
# ВСЕ — удар, корона падает
put(g((7,1))+.02,thud(),.6);put(g((7,7))+.5,boing(),.4)
# лайфхак: повторы щелчками
for i in range(5):put(g((8,2))+i*.33,click(),.35)
put(g((8,4))+.35,jingle(),.35)
# чат: входящие сообщения
for dt in (.1,.5,.9):put(g((9,1))+dt,ding(),.18)
# тихий бит 112 bpm (кроме интриги и перехода внутрь)
bt=60/112;t=0.0;k=0
while t<d['total']-1:
  if not (g((2,0))<=t<g((3,0)) or g((4,0))<=t<g((4,2))):
    put(t,kick(),.16 if k%2==0 else .0);put(t+bt/2,bp(noise(.05),6000,12000)*env(int(.05*SR),.001,.01),.06)
  t+=bt;k+=1
out/=max(1e-9,np.abs(out).max())/0.8
wavfile.write(sys.argv[2],SR,(np.stack([out,out],1)*32767).astype(np.int16))
print('ok',len(out)/SR)
