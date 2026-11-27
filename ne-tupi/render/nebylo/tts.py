import base64
import json
import os
import urllib.request
from pathlib import Path

here = Path(__file__).parent
work = Path(os.environ.get('NETUPI_WORK', str(here)))
work.mkdir(parents=True, exist_ok=True)
script = json.loads((here/'scenariy.json').read_text())
text = '\n'.join(f'[{tag}] {line}' if tag else line for _, tag, line in script)
url = ('https://api.elevenlabs.io/v1/text-to-speech/hU3rD0Yk7DoiYULTX1pD'
       '/with-timestamps?output_format=mp3_44100_128')
req = urllib.request.Request(url, data=json.dumps({'text':text,'model_id':'eleven_v4'},ensure_ascii=False).encode(),
    headers={'xi-api-key':os.environ['ELEVENLABS_API_KEY'],'Content-Type':'application/json'})
with urllib.request.urlopen(req,timeout=90) as response:
    data = json.load(response)
(work/'voice.mp3').write_bytes(base64.b64decode(data['audio_base64'], validate=True))
(work/'align2.json').write_text(json.dumps(data['alignment'],ensure_ascii=False))
print(data['alignment']['character_end_times_seconds'][-1])
