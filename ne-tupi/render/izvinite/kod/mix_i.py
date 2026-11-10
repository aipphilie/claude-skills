import subprocess
from compose_i import T, B, DUR, IZ
from words import END
ev=[('pop',IZ[0],0.5),('pop',IZ[1],0.55),('pop',IZ[2],0.6),('snap',T['stop']-0.05,0.8),('pop',T['prost'],0.5),('pop',T['slomal']-0.3,0.4),('notif',T['slomal'],0.5),
('pop',T['vopros'],0.5),('thud',T['podvoh']-0.05,0.7),('pop',T['lishnee'],0.5),('scissors',T['zvuchit'],0.4),('thud',T['meshayu']-0.6,0.6)]
ev+=[('pop',B[4]+k*(T['desyat']+0.5-B[4])/7,0.3) for k in range(7)]
ev+=[('thud',T['poveryat'],0.6),('whoosh',T['nas']-0.1,0.4),('pop',T['izvin'],0.4),('pop',T['uvazh'],0.5),('ding',T['viny'],0.5),
('whoosh',T['delat']-0.5,0.5),('pop',T['tri'],0.4),('pop',B[7],0.5),('pop',T['nakos']-0.3,0.5),('pop',T['opozd']-0.15,0.5),('pop',T['perep']-0.15,0.5),('pop',T['nogu']-0.15,0.5),
('pop',B[8],0.5),('pop',T['menyay'],0.5),('pop',T['ne2'],0.4),('scissors',T['zader']+0.3,0.4),('ding',T['spas2'],0.5),('whoosh',T['mozhno']-0.4,0.4),('ding',T['mozhno2'],0.6),
('pop',B[9],0.5),('notif',T['soob']-0.4,0.5)]
step=(T['prich']-T['vych'])/3
ev+=[('scissors',T['vych']+k*step,0.4) for k in range(3)]
ev+=[('ding',T['prich']+0.3,0.5),('whoosh',B[10],0.4),('scissors',T['vezhliv'],0.4),('thud',T['zaranee'],0.6),('snap',T['netupi']-0.15,0.8),('whoosh',END+0.75,0.5)]
inp=['-i','voice.mp3']; fl=[]; lab=['[0:a]']
for k,(n,t,v) in enumerate(ev):
    inp+=['-i',f'sfx/{n}.mp3']; ms=int(max(0,t)*1000)
    fl.append(f'[{k+1}:a]volume={v},adelay={ms}|{ms}[s{k}]'); lab.append(f'[s{k}]')
fl.append(''.join(lab)+f'amix=inputs={len(lab)}:normalize=0,apad,atrim=0:{DUR},loudnorm=I=-14:TP=-1.5[out]')
subprocess.run(['ffmpeg','-y','-loglevel','error']+inp+['-filter_complex',';'.join(fl),'-map','[out]','-ar','44100','-c:a','aac','-b:a','192k','mix.m4a'],check=True)
