import sys,json
from faster_whisper import WhisperModel
m=WhisperModel(sys.argv[3] if len(sys.argv)>3 else 'small',device='cpu',compute_type='int8',cpu_threads=4)
import numpy as np
audio=np.fromfile(sys.argv[1],dtype=np.float32)
segs,_=m.transcribe(audio,language='ru',word_timestamps=True,vad_filter=False,beam_size=5)
ws=[[w.word.strip(),round(w.start,3),round(w.end,3)] for s in segs for w in s.words]
json.dump(ws,open(sys.argv[2],'w'),ensure_ascii=False)
print(len(ws));print(' '.join(w[0] for w in ws))
