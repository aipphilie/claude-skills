# «Он выбрал тебя» v1 (2026-11-12)
- vybral-v1.mp4 — 1080x1920, 24 fps, 42 сек. Голос hU3rD0Yk7DoiYULTX1pD, eleven_v4. Звуки из ne-tupi-zvuki/gotovye, ×0.5.
- По присланному Ярославом рилсу («муж — единственный, кто выбрал тебя сам»): тот же ход мысли и порядок сцен, текст свой, плюс наш каркас («Стоп. Тут ты тупишь», «А вот и подвох», «Всё. Не тупи.») и призыв переслать мужу.
- Новое: ДЕВУШКА — третий персонаж (каре до плеч, розовый бант #FF4F8B, bw 0.9 / th 0.9 / lh 0.9; в 3d/index.html параметр girl=1). Первые 3D-ПРЕДМЕТЫ: 3d/props.html (сердце, кольца, дом, часы, цветок с параметрами wilt/bloom), рендер props.js.
- Порядок: python3 -m http.server 8790 (из kod/) → tts.py → track_v.py → node 3d/frames.js track.json kadry flat 1080 1920 8790 → props_plan.py → node props.js props.json kadry_props 8790 → compose_v.py → mix_v.py → склейка (run_all.sh).
- Обложки: oblozhka/ (A «ОН ВЫБРАЛ ТЕБЯ» — рекомендую, B «ЛЮБОВЬ ВЯНЕТ»), cover_v.py. Описание: ne-tupi-idei/vybral/opisanie.md.
