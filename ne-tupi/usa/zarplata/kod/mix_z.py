import subprocess
from compose_z import T, B, DUR
from words import END
ev=[('notif',T['zp']-0.1,0.35),('whoosh',T['gde']-0.4,0.25),('snap',T['stop']-0.05,0.4),('pop',T['kuda'],0.2),('popper',T['d1'],0.3),
('bags',T['d2']+0.2,0.35),('deflate',T['d3']+0.4,0.3),('pop',T['dumaesh']+0.6,0.25),('snap',T['net'],0.35),('pop',T['dva'],0.25),('bags',T['budet']+0.3,0.3),
('whoosh',T['kopish'],0.2),('thud',T['nol1']+0.3,0.3),('whoosh',T['naob'],0.25),('pop',T['desyat'],0.25),('whoosh',T['avto']-0.3,0.25),('pop',T['avto']+0.2,0.25)]
ev+=[('coin',T['shest']-0.2+j*0.25+0.45,0.3) for j in range(3)]
ev+=[('ding',T['sem']+1.0,0.25),('bags',B[11],0.25),('pop',T['bez'],0.25),('pop',T['snach'],0.3),('thud',T['nol2'],0.3),('snap',T['netupi']-0.15,0.4),('whoosh',END+0.75,0.25)]
inp=['-i','voice.mp3']; fl=[]; lab=['[0:a]']
for k,(n,t,v) in enumerate(ev):
    inp+=['-i',f'sfx/{n}.mp3']; ms=int(max(0,t)*1000)
    fl.append(f'[{k+1}:a]volume={v},adelay={ms}|{ms}[s{k}]'); lab.append(f'[s{k}]')
fl.append(''.join(lab)+f'amix=inputs={len(lab)}:normalize=0,apad,atrim=0:{DUR},loudnorm=I=-14:TP=-1.5[out]')
subprocess.run(['ffmpeg','-y','-loglevel','error']+inp+['-filter_complex',';'.join(fl),'-map','[out]','-ar','44100','-c:a','aac','-b:a','192k','mix.m4a'],check=True)
