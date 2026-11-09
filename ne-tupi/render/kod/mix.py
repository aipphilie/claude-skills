import subprocess
from compose import T, B, DUR
from words import END
ev=[('siren',0.0,0.35),('snap',T['stop']-0.05,0.8),('whoosh',B[2]+0.1,0.5),('ding',T['eto']+0.9,0.5),('pop',T['tak']+0.2,0.5),('whoosh',T['podozhdi'],0.5),
('thud',T['taksi']+0.28,0.7),('thud',T['dost']+0.38,0.8),('thud',T['tel']+0.28,0.9),('pop',T['kop'],0.6),('whoosh',T['kak'],0.5),('pop',T['perv'],0.5),
('scissors',T['rezh']+0.15,0.7),('scissors',T['rezh']+0.79,0.7),('pop',T['melk'],0.4),('pop',T['otn'],0.5),('pop',T['kup'],0.5),('sip',T['kofe_pei']-0.5,0.6),('snap',T['netupi']-0.15,0.8),('whoosh',END+0.75,0.5)]
inp=['-i','voice.mp3']; fl=[]; lab=['[0:a]']
for k,(n,t,v) in enumerate(ev):
    inp+=['-i',f'sfx/{n}.mp3']; ms=int(t*1000)
    fl.append(f'[{k+1}:a]volume={v},adelay={ms}|{ms}[s{k}]'); lab.append(f'[s{k}]')
fl.append(''.join(lab)+f'amix=inputs={len(lab)}:normalize=0,apad,atrim=0:{DUR},loudnorm=I=-14:TP=-1.5[out]')
subprocess.run(['ffmpeg','-y','-loglevel','error']+inp+['-filter_complex',';'.join(fl),'-map','[out]','-ar','44100','-c:a','aac','-b:a','192k','mix.m4a'],check=True)
