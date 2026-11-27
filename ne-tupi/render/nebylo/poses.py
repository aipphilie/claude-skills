"""Позы для рилса. Базовые ключи берутся из исходного рига проекта."""
import json
import math
import os
import sys
from pathlib import Path

here=Path(__file__).resolve().parent
root=Path(os.environ.get('NETUPI_ROOT','/workspace/claude-skills/ne-tupi'))
out=Path(os.environ.get('NETUPI_WORK',str(here)))
sys.path.insert(0,str(root))
import anim3d

def standard(name, count, **kwargs):
    p,m=anim3d.ANIMS[name][1]()
    frames=[dict(anim3d.to3d(pose,mouth,name),**kwargs) for pose,mouth in zip(p,m)]
    return frames[::2][:count]

base=standard('dyhanie',1)[0]
def action(n,fn,**kwargs):
    return [dict(base,**kwargs)|fn(j/(n-1)) for j in range(n)]

def swing(u):
    return math.sin(u*math.pi*2)

girl=dict(girl=1,bw=.90,th=.94,lh=.95)
jobs={
    'idle':standard('dyhanie',24),
    'shrug':standard('pozhimaet-plechami',24),
    'shock':standard('pryzhok',24),
    'point':standard('ukazyvaet-vbok',24),
    'push':standard('tashit-v-goru',20),
    'walkR':[dict(f,yaw=90) for f in standard('shag-profil',16)],
    'reach':action(25,lambda u:dict(head=-15,lean=-12*min(1,u*2),ra=[72+45*u,18],raF=1.1,la=[66,32],laF=.8,mouth='O')),
    'flip':action(24,lambda u:dict(yaw=-10+25*swing(u),head=-15,ra=[92,32+52*u],raF=1.2,la=[70,38],laF=.8)),
    'hold':action(24,lambda u:dict(ra=[72,48],la=[64,52],raF=1.1,laF=.9,head=-11+4*swing(u),mouth='sad')),
    'sit':action(24,lambda u:dict(lsw=73,rsw=76,sink=.6,ra=[80,32],la=[60,52],raF=.7,laF=.6,head=4+5*swing(u),mouth='smile')),
    'g_sit':action(24,lambda u:dict(lsw=73,rsw=76,sink=.6,yaw=-30,ra=[57,52],la=[92,28],laF=.83,head=-7+6*swing(u),mouth='smile'),**girl),
    'g_walk':standard('shag-profil',16,**girl),
    'stop':action(18,lambda u:dict(ra=[90+7*swing(u),6],la=[88,6],raF=1.4,laF=1.4,mouth='A')),
    'call':action(24,lambda u:dict(head=8+5*swing(u),ra=[139,79],raF=1.0,la=[12,15],mouth='smile'))
}
(out/'clips.json').write_text(json.dumps(jobs))
