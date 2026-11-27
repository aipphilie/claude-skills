"""Добавляет звуки к действиям и соединяет готовые части."""
import argparse
import subprocess
from pathlib import Path
import numpy as np
import wave
from film import WORK, load_shots, END, FPS

FILES={
    'hit': ('19-udar-final.mp3',.11), 'boom': ('26-bum.mp3',.11),
    'fall': ('14-plyuh.mp3',.12), 'key': ('10-monetki.mp3',.10),
    'swipe': ('03-perehod-swipe.mp3',.087), 'snapshot': ('32-foto-shchelchok.mp3',.15),
    'pop': ('04-pop.mp3',.105), 'swish': ('43-vzhuh-bas-skleyka.mp3',.105),
    'wave': ('02-vzhuh-dlinniy.mp3',.055), 'reverse': ('38-revers.mp3',.095),
    'message': ('12-soobshchenie.mp3',.14), 'click': ('05-klik.mp3',.10),
    'final': ('19-udar-final.mp3',.085),
}


def pcm(p):
    raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-f','f32le','-ar','44100','-ac','1','-'])
    return np.frombuffer(raw,dtype='<f4')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('library',type=Path)
    parser.add_argument('target',type=Path)
    parser.add_argument('parts',nargs='+',type=Path)
    a=parser.parse_args()
    shots=load_shots()
    length=round(round((END+.7)*FPS)/FPS*44100)
    mix=np.zeros(length,dtype=np.float32)
    voice=pcm(WORK/'voice.mp3')
    mix[:min(len(voice),length)]=voice[:length]*.96
    events=[(shot['t'],shot['sfx']) for shot in shots if shot['sfx']]
    t={shot['name']:shot['t'] for shot in shots}
    events.extend((t['suitcase']+j*.1+.25,'key' if j==0 else 'pop') for j in range(3))
    events.extend([(t['keys']+.25,'click'),(t['cloth']+.36,'swipe'),(t['beach']+.42,'wave'),
                   (t['turn']+.38,'snapshot'),(t['need']+.39,'click'),(t['leave']+.53,'fall')])
    effects={}
    for time,name in events:
        file,gain=FILES[name]
        if file not in effects:
            effects[file]=pcm(a.library/file)
        sound=effects[file]
        at=round(time*44100)
        n=min(length-at,len(sound))
        mix[at:at+n]+=sound[:n]*gain
    with wave.open(str(WORK/'mix.wav'),'wb') as f:
        f.setparams((1,2,44100,0,'NONE','not compressed'))
        f.writeframes((np.clip(mix,-1,1)*32767).astype('<i2').tobytes())
    manifests=WORK/'concat.txt'
    manifests.write_text(''.join("file '"+str(path.resolve()).replace("'","'\\''")+"'\n" for path in a.parts))
    subprocess.run(['ffmpeg','-y','-v','error','-f','concat','-safe','0','-i',str(manifests),
                    '-i',str(WORK/'mix.wav'),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac',
                    '-b:a','160k','-movflags','+faststart',str(a.target)],check=True)


if __name__=='__main__':
    main()
