"""Склейка глав в один voice.wav с паузами по tl.O"""
import subprocess, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tl import O, NCH, DUR
inp = []; fl = []
for i in range(NCH):
    inp += ['-i', f'zvuk/ch{i:02d}.mp3']; ms = int(O[i] * 1000); fl.append(f'[{i}:a]adelay={ms}|{ms}[a{i}]')
fl.append(''.join(f'[a{i}]' for i in range(NCH)) + f'amix=inputs={NCH}:normalize=0,apad,atrim=0:{DUR}[o]')
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error'] + inp + ['-filter_complex', ';'.join(fl), '-map', '[o]', '-ar', '44100', '-ac', '1', 'zvuk/voice.wav'], check=True)
