# python3 asr_timing.py audio.mp3 scenes.js asr/words.json timing.json — тайминги слов по распознаванию (faster-whisper)
import json,re,sys,difflib,subprocess
mp3,sj,wj,out=sys.argv[1:5]
dur=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',mp3]))
paras=[re.sub(r'\[[a-z -]+\]\s*','',t).replace('́','').strip() for t in re.findall(r"\{txt:'(.*?)',bg",open(sj).read())]
asr=json.load(open(wj))
norm=lambda w:re.sub(r'[^a-zа-я0-9]','',w.lower().replace('ё','е').replace('nzt','нзт'))
S=[(p,w) for p,t in enumerate(paras) for w in t.split()]
a=[norm(w) for _,w in S];b=[norm(w[0]) for w in asr]
tm=[None]*len(S)
for blk in difflib.SequenceMatcher(None,a,b,autojunk=False).get_opcodes():
  tag,i1,i2,j1,j2=blk
  if tag=='equal':
    for k in range(i2-i1):tm[i1+k]=[asr[j1+k][1],asr[j1+k][2]]
  elif tag=='replace' and j2>j1:  # равномерно делим отрезок распознанных слов
    st,en=asr[j1][1],asr[j2-1][2]
    for k in range(i2-i1):tm[i1+k]=[st+(en-st)*k/(i2-i1),st+(en-st)*(k+1)/(i2-i1)]
miss=sum(x is None for x in tm)
for i in range(len(tm)):  # дыры: между соседями
  if tm[i] is None:
    p=next((tm[j][1] for j in range(i-1,-1,-1) if tm[j]),0);n=next((tm[j][0] for j in range(i+1,len(tm)) if tm[j]),dur)
    tm[i]=[p,min(n,p+.3)]
res=[];k=0
for p,t in enumerate(paras):
  ws=t.split();words=[[w,round(tm[k+i][0],3),round(tm[k+i][1],3)] for i,w in enumerate(ws)];k+=len(ws)
  res.append({'speech':[words[0][1],words[-1][2]],'words':words,'text':t})
for p in range(len(res)):res[p]['t0']=0 if p==0 else round((res[p-1]['speech'][1]+res[p]['speech'][0])/2,3)
for p in range(len(res)):res[p]['d']=round((res[p+1]['t0'] if p<len(res)-1 else dur+.7)-res[p]['t0'],3)
json.dump({'dur':dur,'total':round(dur+.7,3),'scenes':res},open(out,'w'),ensure_ascii=False,indent=1)
print('unmatched',miss,'of',len(S))
for p,x in enumerate(res):print(p+1,x['t0'],x['d'],x['text'][:40])
