"""Черновые тайминги без озвучки: ~темп голоса канала. Заменяются настоящим align.json после tts.py."""
import json, subprocess
T = open('text.txt').read().strip(); OFF = 4.3
C, S, E = [], [], []; t = OFF; intag = False
for ch in T:
    if ch == '[': intag = True
    d = 0.0 if intag else (0.066 if ch.isalpha() or ch.isdigit() else 0.42 if ch in '.?!' else 0.2 if ch in ',:' else 0.3 if ch == '\n' else 0.045)
    if T[max(0, len(C) - 6):len(C)].endswith('pause]') and ch == ' ': d = 0.5
    C.append(ch); S.append(round(t, 3)); t += d; E.append(round(t, 3))
    if ch == ']': intag = False
json.dump({'characters': C, 'character_start_times_seconds': S, 'character_end_times_seconds': E}, open('align.json', 'w'), ensure_ascii=False)
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'lavfi', '-i', f'anoisesrc=d={t+4}:c=pink:a=0.02', '-ar', '44100', 'voice.mp3'], check=True)
json.dump({'off': OFF, 'draft': True}, open('meta.json', 'w'))
print(t)
