import subprocess
from compose_z import T, B, DUR
from words import END
ev=[('notif',T['zp']-0.1,0.7),('whoosh',T['gde']-0.4,0.5),('snap',T['stop']-0.05,0.8),('pop',T['kuda'],0.4),('popper',T['d1'],0.6),
('bags',T['d2']+0.2,0.7),('deflate',T['d3']+0.4,0.6),('pop',T['dumaesh']+0.6,0.5),('snap',T['net'],0.7),('pop',T['dva'],0.5),('bags',T['budet']+0.3,0.6),
('whoosh',T['kopish'],0.4),('thud',T['nol1']+0.3,0.6),('whoosh',T['naob'],0.5),('pop',T['desyat'],0.5),('whoosh',T['avto']-0.3,0.5),('pop',T['avto']+0.2,0.5)]
ev+=[('coin',T['shest']-0.2+j*0.25+0.45,0.6) for j in range(3)]
ev+=[('ding',T['sem']+1.0,0.5),('bags',B[11],0.5),('pop',T['bez'],0.5),('pop',T['snach'],0.6),('thud',T['nol2'],0.6),('snap',T['netupi']-0.15,0.8),('whoosh',END+0.75,0.5)]
inp=['-i','voice.mp3']; fl=[]; lab=['[0:a]']
for k,(n,t,v) in enumerate(ev):
    inp+=['-i',f'sfx/{n}.mp3']; ms=int(max(0,t)*1000)
    fl.append(f'[{k+1}:a]volume={v},adelay={ms}|{ms}[s{k}]'); lab.append(f'[s{k}]')
fl.append(''.join(lab)+f'amix=inputs={len(lab)}:normalize=0,apad,atrim=0:{DUR},loudnorm=I=-14:TP=-1.5[out]')
subprocess.run(['ffmpeg','-y','-loglevel','error']+inp+['-filter_complex',';'.join(fl),'-map','[out]','-ar','44100','-c:a','aac','-b:a','192k','mix.m4a'],check=True)
