import json,os,re,base64,sys,requests
T=open('/mnt/project-files/ne-tupi-youtube/gde-dengi/ozvuchka-v1.txt').read().strip()
blocks=[b.strip().split('\n',1) for b in T.split('\n\n')]
key=os.environ['ELEVENLABS_API_KEY']; V='hU3rD0Yk7DoiYULTX1pD'
only=[int(x) for x in sys.argv[1:]]
for i,(hdr,txt) in enumerate(blocks):
    if only and i not in only: continue
    out=f'zvuk/ch{i:02d}'
    if os.path.exists(out+'.json') and not only: continue
    r=requests.post(f'https://api.elevenlabs.io/v1/text-to-speech/{V}/with-timestamps?output_format=mp3_44100_128',
        headers={'xi-api-key':key},json={'text':txt.strip(),'model_id':'eleven_v3'},timeout=600)
    if r.status_code!=200: print(i,r.status_code,r.text[:300]); continue
    j=r.json(); open(out+'.mp3','wb').write(base64.b64decode(j['audio_base64']))
    json.dump(j['alignment'],open(out+'.json','w'),ensure_ascii=False)
    print(i,hdr,j['alignment']['character_end_times_seconds'][-1],flush=True)
