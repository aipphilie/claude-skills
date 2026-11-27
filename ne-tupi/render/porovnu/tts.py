"""Озвучивает сценарий голосом канала и сохраняет посимвольные тайминги."""
import argparse
import base64
import json
import os
import urllib.request
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    script = json.loads(Path(__file__).with_name('scenariy.json').read_text())
    text = '\n'.join(f'[{tag}] {line}' if tag else line for _, tag, line in script)
    endpoint = ('https://api.elevenlabs.io/v1/text-to-speech/hU3rD0Yk7DoiYULTX1pD'
                '/with-timestamps?output_format=mp3_44100_128')
    request = urllib.request.Request(
        endpoint, data=json.dumps({'text': text, 'model_id': 'eleven_v4'}, ensure_ascii=False).encode(),
        headers={'xi-api-key': os.environ['ELEVENLABS_API_KEY'], 'Content-Type': 'application/json'})
    with urllib.request.urlopen(request, timeout=90) as response:
        result = json.load(response)
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / 'voice.mp3').write_bytes(base64.b64decode(result['audio_base64'], validate=True))
    (args.output / 'alignment.json').write_text(json.dumps(result['alignment'], ensure_ascii=False))


if __name__ == '__main__':
    main()
