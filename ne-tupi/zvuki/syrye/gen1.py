import json, os, sys, urllib.request, concurrent.futures as cf
K=os.environ['ELEVENLABS_API_KEY']; OUT='/mnt/project-files/ne-tupi-zvuki/probnye'
S=[
("01-vzhuh-korotkiy","quick clean cartoon whoosh, single fast air swipe, crisp, no music",0.7),
("02-vzhuh-dlinniy","smooth airy whoosh transition passing left to right, clean modern motion graphics sound, no music",1.3),
("03-perehod-swipe","short soft swoosh up, UI swipe transition, minimal and clean",0.6),
("04-pop","single soft cartoon pop, bubble pop, clean UI sound",0.5),
("05-klik","single crisp UI tap click, soft plastic button press",0.5),
("06-dzyn-insayt","bright single bell ding, idea moment, clean and cheerful, short tail",1.2),
("07-pravilno","positive success chime, two rising notes, clean UI sound, short",1.0),
("08-oshibka","short wrong answer buzzer, low cartoon error buzz, game show, not harsh",0.8),
("09-kassa","cash register cha-ching, drawer opening with bell, clear",1.3),
("10-monetki","a few coins dropping onto a wooden table, clear jingle",1.2),
("11-uvedomlenie","generic smartphone notification sound, soft two-tone pling, clean",0.8),
("12-soobshchenie","chat message sent sound, soft bubble whoosh pop",0.6),
("13-klaviatura","fast typing on a laptop keyboard, short burst of clicks",1.2),
("14-plyuh","soft heavy cartoon thud, object dropped on floor, muffled",0.6),
("15-skretch","vinyl record scratch stop, comedic sudden stop",0.8),
("16-proval","sad trombone wah wah wah, comedic failure",2.0),
("17-tik-tak","clock ticking, steady tick tock, four ticks, dry",2.0),
("18-nagnetanie","short tension riser, rising whoosh building up then stops, cinematic but light",2.0),
("19-udar-final","punchy deep impact hit with short boom, logo sting accent, clean",1.2),
("20-pechat","rubber stamp slamming on paper, firm single stamp",0.6),
("21-glitch","short digital glitch stutter, electronic error glitch",0.7),
("22-pshik","can soda opening, short fizz, refreshing",0.9),
]
def g(s):
    n,t,d=s
    body=json.dumps({"text":t,"duration_seconds":d,"prompt_influence":0.6,"model_id":"eleven_text_to_sound_v2"}).encode()
    r=urllib.request.Request("https://api.elevenlabs.io/v1/sound-generation?output_format=mp3_44100_128",body,{"xi-api-key":K,"Content-Type":"application/json"})
    open(f"{OUT}/{n}.mp3","wb").write(urllib.request.urlopen(r,timeout=120).read()); return n
with cf.ThreadPoolExecutor(3) as ex:
    for n in ex.map(g,S): print(n)
json.dump([{"file":f"{n}.mp3","prompt":t,"sec":d} for n,t,d in S],open(f"{OUT}/prompts.json","w"),ensure_ascii=False,indent=1)
