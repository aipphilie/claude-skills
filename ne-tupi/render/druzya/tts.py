import base64,json,os,urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
p=Path(os.environ['NETUPI_WORK'])
p.mkdir(parents=True,exist_ok=True)
script=json.loads(Path(__file__).with_name('replicas.json').read_text())
def voice(section):
    text='\n'.join((f'[{tag}] ' if tag else '')+line for _,tag,line in script[section])
    url='https://api.elevenlabs.io/v1/text-to-speech/hU3rD0Yk7DoiYULTX1pD/with-timestamps?output_format=mp3_44100_128'
    req=urllib.request.Request(url,data=json.dumps({'text':text,'model_id':'eleven_v4'},ensure_ascii=False).encode(),headers={'xi-api-key':os.environ['ELEVENLABS_API_KEY'],'Content-Type':'application/json'})
    with urllib.request.urlopen(req,timeout=60) as r: data=json.load(r)
    (p/f'{section}.mp3').write_bytes(base64.b64decode(data['audio_base64']))
    (p/f'{section}.json').write_text(json.dumps(data['alignment'],ensure_ascii=False))
    print(section,data['alignment']['character_end_times_seconds'][-1])
with ThreadPoolExecutor(max_workers=2) as pool:
    list(pool.map(voice,script))
