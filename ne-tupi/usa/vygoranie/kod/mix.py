import subprocess
from compose_v import T, B, DUR
from words import END
ev=[('ding',0.05,0.25),('ding',0.45,0.25),('deflate',2.9,0.25),('snap',T['stop']-0.05,0.4),('pop',T['p71'],0.25),('thud',T['nepr'],0.25),
('whoosh',T['otp']-0.2,0.25),('pop',T['dve'],0.2),('ding',T['bat']+1.3,0.3),('thud',T['podvoh'],0.35),('notif',T['cherez']+0.1,0.3),('deflate',T['cherez']+0.3,0.3),
('pop',T['uchili'],0.25),('thud',T['nikto'],0.25),('pop',T['vykl']+0.2,0.25),('notif',T['chat'],0.3),('pop',T['dodel'],0.25),('pop',T['son'],0.25),('thud',T['nu'],0.35),
('pop',T['trat'],0.2),('pop',T['zar'],0.2),('whoosh',T['delat']-0.4,0.25),('pop',T['tri'],0.2),('pop',B[9],0.25),('pop',T['bezzv'],0.25),
('pop',B[10],0.25),('pop',T['ned2'],0.25),('scissors',T['pochtu']+0.2,0.2),('whoosh',T['mozhno']-0.3,0.2),('ding',T['mozhno2'],0.3),
('pop',B[11],0.25),('coin',T['r3']+1.5,0.2),('ding',T['r3']+3.4,0.25),('pop',T['radu']-0.2,0.25),('thud',T['len_']-0.1,0.25),('pop',T['otp2'],0.25),
('pop',T['pb'],0.3),('snap',T['netupi']-0.15,0.4),('whoosh',END+0.75,0.25)]
inp=['-i','voice.mp3']; fl=[]; lab=['[0:a]']
for k,(n,t,v) in enumerate(ev):
    inp+=['-i',f'sfx/{n}.mp3']; ms=int(max(0,t)*1000)
    fl.append(f'[{k+1}:a]volume={v},adelay={ms}|{ms}[s{k}]'); lab.append(f'[s{k}]')
fl.append(''.join(lab)+f'amix=inputs={len(lab)}:normalize=0,apad,atrim=0:{DUR},loudnorm=I=-14:TP=-1.5[out]')
subprocess.run(['ffmpeg','-y','-loglevel','error']+inp+['-filter_complex',';'.join(fl),'-map','[out]','-ar','44100','-c:a','aac','-b:a','192k','mix.m4a'],check=True)
