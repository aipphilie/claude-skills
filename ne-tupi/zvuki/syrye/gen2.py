import json, os, urllib.request, concurrent.futures as cf
K=os.environ['ELEVENLABS_API_KEY']; OUT='/mnt/project-files/ne-tupi-zvuki/probnye-v2'
S=[
("23-vzhuh-bas-a","fast short whoosh immediately followed by a deep heavy sub bass boom hit, punchy, short-form video edit transition",1.5,0.7),
("24-vzhuh-bas-b","quick air swoosh into a massive low 808 bass drop impact, cinematic trailer hit, tight",1.8,0.7),
("25-vzhuh-bas-c","whoosh swipe then deep distorted bass thump, modern TikTok edit transition sound",1.3,0.7),
("26-bum","single deep cinematic boom, huge low bass hit with short rumble tail, dramatic emphasis",1.5,0.7),
("27-bas-drop","808 sub bass drop, pitch falling deep sub, bass drop sound effect",1.5,0.7),
("28-tsik-bystro-a","fast clock ticking, rapid tick tick tick tick, stopwatch ticking quickly, crisp and dry, close mic",3.0,0.8),
("29-tsik-bystro-b","very fast metallic stopwatch ticks accelerating, tense countdown ticking, clicky and sharp",3.0,0.8),
("30-tsik-medlenno","loud mechanical clock tick tock with slight room echo, suspense, slow steady ticks",3.0,0.8),
("31-taymer","digital countdown timer beeps, three short beeps then one long beep",2.0,0.7),
("32-foto-shchelchok","camera shutter click with flash, freeze frame sound, crisp",0.7,0.7),
("33-zum-vhod","fast zoom in whoosh, rising swoosh punch in, video zoom transition",0.8,0.7),
("34-riser-bum","short rising riser building tension then hard impact boom at the end",2.5,0.7),
("35-blesk","magical sparkle shimmer, twinkle glitter sound, bright and short",1.2,0.7),
("36-dun-dun-dun","dramatic orchestral sting dun dun duuun, suspense reveal, brass and timpani",2.0,0.7),
("37-tsenzura","censor beep, single TV bleep tone 1 kHz",0.6,0.8),
("38-revers","reverse cymbal swell sucking in, reverse whoosh build up",1.5,0.7),
("39-tv-vykl","old CRT TV turning off, electric zap and power down",1.0,0.7),
("40-zamedlenie","tape stop effect, audio slowing down and pitching down to stop",1.2,0.7),
("41-serdtse","heartbeat thump thump, tense, deep and clear, two beats",1.5,0.7),
("42-boing","cartoon spring boing, comedic bounce",0.8,0.7),
]
def g(s):
    n,t,d,p=s
    b=json.dumps({"text":t,"duration_seconds":d,"prompt_influence":p,"model_id":"eleven_text_to_sound_v2"}).encode()
    r=urllib.request.Request("https://api.elevenlabs.io/v1/sound-generation?output_format=mp3_44100_128",b,{"xi-api-key":K,"Content-Type":"application/json"})
    open(f"{OUT}/{n}.mp3","wb").write(urllib.request.urlopen(r,timeout=120).read()); return n
with cf.ThreadPoolExecutor(3) as ex:
    for n in ex.map(g,S): print(n,end=' ')
json.dump([{"file":f"{n}.mp3","prompt":t,"sec":d} for n,t,d,p in S],open(f"{OUT}/prompts.json","w"),ensure_ascii=False,indent=1)
