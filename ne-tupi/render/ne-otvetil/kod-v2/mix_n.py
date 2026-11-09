import subprocess
from compose_n import T, B, DUR
from words import END
ev=[('notif',0.05,0.6),('pop',T['desyat'],0.4),('thud',T['tish'],0.5),('pop',T['tochno'],0.5),('snap',T['stop']-0.05,0.8),('thud',T['podvoh']-0.05,0.7),
('pop',T['nezn']-0.1,0.5),('pop',T['obid'],0.5),('pop',T['neto'],0.5),('thud',T['konec'],0.6),('thud',T['nu'],0.7),('whoosh',B[3],0.4),('pop',T['dramu']-0.2,0.5),
('pop',T['odinch'],0.4),('thud',T['ty']-0.05,0.7),('whoosh',T['zachem']-0.1,0.5),('pop',T['tri'],0.4),('ding',T['tretem'],0.5),('pop',B[5],0.5),
('ding',T['fakt']-0.1,0.5),('pop',T['ostal']-0.1,0.4),('scissors',T['neon'],0.4),('thud',T['neon'],0.5),('pop',B[6],0.5),('pop',T['pyt'],0.5),('thud',T['nevyd'],0.6),
('whoosh',T['prid'],0.4),('pop',T['rul']-0.15,0.5),('pop',T['sov']-0.15,0.5),('pop',T['usnul']-0.15,0.5),('deflate',T['rul'],0.35),('pop',B[7],0.5),('pop',T['spr'],0.5),
('whoosh',T['propal']-0.1,0.5),('whoosh',T['mozhno']-0.6,0.4),('ding',T['mozhno2'],0.6),('pop',B[8],0.5),('pop',T['mozg'],0.5),('whoosh',T['doris'],0.5),
('thud',T['doris']+0.7,0.6),('pop',T['strash']-0.3,0.5),('whoosh',B[9],0.4),('pop',T['kto'],0.5),('thud',T['pred']-0.5,0.6),('ding',T['vot'],0.6),
('notif',T['aon']+0.05,0.7),('popper',T['obedal'],0.6),('snap',T['netupi']-0.15,0.8),('whoosh',END+0.75,0.5)]
inp=['-i','voice.mp3']; fl=[]; lab=['[0:a]']
for k,(n,t,v) in enumerate(ev):
    inp+=['-i',f'sfx/{n}.mp3']; ms=int(max(0,t)*1000)
    fl.append(f'[{k+1}:a]volume={v},adelay={ms}|{ms}[s{k}]'); lab.append(f'[s{k}]')
fl.append(''.join(lab)+f'amix=inputs={len(lab)}:normalize=0,apad,atrim=0:{DUR},loudnorm=I=-14:TP=-1.5[out]')
subprocess.run(['ffmpeg','-y','-loglevel','error']+inp+['-filter_complex',';'.join(fl),'-map','[out]','-ar','44100','-c:a','aac','-b:a','192k','mix.m4a'],check=True)
