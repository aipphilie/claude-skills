import subprocess
from compose_i import T, B, DUR, IZ
from words import END
ev=[('pop',IZ[0],0.25),('pop',IZ[1],0.275),('pop',IZ[2],0.3),('snap',T['stop']-0.05,0.4),('pop',T['prost'],0.25),('pop',T['slomal']-0.3,0.2),('notif',T['slomal'],0.25),
('pop',T['vopros'],0.25),('thud',T['podvoh']-0.05,0.35),('pop',T['lishnee'],0.25),('scissors',T['zvuchit'],0.2),('thud',T['meshayu']-0.6,0.3)]
ev+=[('pop',B[4]+k*(T['desyat']+0.5-B[4])/7,0.15) for k in range(7)]
ev+=[('thud',T['poveryat'],0.3),('whoosh',T['nas']-0.1,0.2),('pop',T['izvin'],0.2),('pop',T['uvazh'],0.25),('ding',T['viny'],0.25),
('whoosh',T['delat']-0.5,0.25),('pop',T['tri'],0.2),('pop',B[7],0.25),('pop',T['nakos']-0.3,0.25),('pop',T['opozd']-0.15,0.25),('pop',T['perep']-0.15,0.25),('pop',T['nogu']-0.15,0.25),
('pop',B[8],0.25),('pop',T['menyay'],0.25),('pop',T['ne2'],0.2),('scissors',T['zader']+0.3,0.2),('ding',T['spas2'],0.25),('whoosh',T['mozhno']-0.4,0.2),('ding',T['mozhno2'],0.3),
('pop',B[9],0.25),('notif',T['soob']-0.4,0.25)]
step=(T['prich']-T['vych'])/3
ev+=[('scissors',T['vych']+k*step,0.2) for k in range(3)]
ev+=[('ding',T['prich']+0.3,0.25),('whoosh',B[10],0.2),('scissors',T['vezhliv'],0.2),('thud',T['zaranee'],0.3),('snap',T['netupi']-0.15,0.4),('whoosh',END+0.75,0.25)]
inp=['-i','voice.mp3']; fl=[]; lab=['[0:a]']
for k,(n,t,v) in enumerate(ev):
    inp+=['-i',f'sfx/{n}.mp3']; ms=int(max(0,t)*1000)
    fl.append(f'[{k+1}:a]volume={v},adelay={ms}|{ms}[s{k}]'); lab.append(f'[s{k}]')
fl.append(''.join(lab)+f'amix=inputs={len(lab)}:normalize=0,apad,atrim=0:{DUR},loudnorm=I=-14:TP=-1.5[out]')
subprocess.run(['ffmpeg','-y','-loglevel','error']+inp+['-filter_complex',';'.join(fl),'-map','[out]','-ar','44100','-c:a','aac','-b:a','192k','mix.m4a'],check=True)
