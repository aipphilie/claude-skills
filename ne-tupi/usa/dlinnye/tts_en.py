import json,os,base64,sys,requests
v=sys.argv[1]; T=open(f'/mnt/project-files/ne-tupi-usa/{v}/ozvuchka-en.txt').read().strip()
blocks=[b.strip().split('\n',1) for b in T.split('\n\n')]
key=os.environ['ELEVENLABS_API_KEY']; V='QvlD90AkjGTCqc9685Rq'
for i,(hdr,txt) in enumerate(blocks):
    out=f'{v}/zvuk/ch{i:02d}'
    if os.path.exists(out+'.json'): continue
    for attempt in range(3):
        r=requests.post(f'https://api.elevenlabs.io/v1/text-to-speech/{V}/with-timestamps?output_format=mp3_44100_128',
            headers={'xi-api-key':key},json={'text':txt.strip(),'model_id':'eleven_v3'},timeout=600)
        if r.status_code==200: break
        print(i,r.status_code,r.text[:200],flush=True)
    j=r.json(); open(out+'.mp3','wb').write(base64.b64decode(j['audio_base64']))
    json.dump(j['alignment'],open(out+'.json','w'),ensure_ascii=False)
    print(v,i,hdr,round(j['alignment']['character_end_times_seconds'][-1],1),flush=True)
