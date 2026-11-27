# «Друзья есть, а встреч нет»

Вертикальный ролик с голосом канала на Eleven v4. В чате все за встречу, но пустую дату никто не берёт на себя. Финал показывает приглашение с днём, временем и местом. Человечек рендерится из оригинальной 3D-модели «Не тупи». Видео 1080×1920, 30 кадров в секунду.

## Сборка

Нужны Python с Pillow, NumPy и CairoSVG, FFmpeg, Node с Playwright, Chromium, шрифт DejaVu Sans и ключ `ELEVENLABS_API_KEY` в окружении.

```sh
export NETUPI_WORK=/tmp/ne-tupi-druzya-work
export NETUPI_OUTPUT=/tmp/ne-tupi-druzya-out
python poses.py
curl -fL https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js -o "$NETUPI_WORK/three.module.js"
node poses.cjs
python tts.py
python film.py
```

При необходимости укажи путь к Chromium через `CHROMIUM_BIN`. Три части озвучки сохраняются в рабочей папке. Монтаж вступления и финала привязан к словам из ElevenLabs. Утверждённый фрагмент имеет собственный монтаж по фиксированным таймингам записи. При его повторной генерации нужно сверить `cut`, `end` и звуковые акценты в `fragment.py` с новой озвучкой.
