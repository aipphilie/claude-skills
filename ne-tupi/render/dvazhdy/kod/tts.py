import json,os,base64,requests
T=open('text.txt').read().strip()
key=os.environ['ELEVENLABS_API_KEY']; V='hU3rD0Yk7DoiYULTX1pD'
r=requests.post(f'https://api.elevenlabs.io/v1/text-to-speech/{V}/with-timestamps?output_format=mp3_44100_128',
    headers={'xi-api-key':key},json={'text':T,'model_id':'eleven_v4'},timeout=600)
print(r.status_code); j=r.json()
open('voice.mp3','wb').write(base64.b64decode(j['audio_base64']))
json.dump(j['alignment'],open('align.json','w'),ensure_ascii=False)
print(j['alignment']['character_end_times_seconds'][-1])
