# «Сколько стоит твоя свобода» v1 (2026-11-20)
- svoboda-v1.mp4: 1080x1920, 30 fps, 64,2 сек, 20 сцен. Сценарий v4 «лестница вопросов» (ne-tupi-idei/svoboda/scenariy-v4.md), голос hU3rD0Yk7DoiYULTX1pD, Eleven v4. Звуки из ne-tupi-zvuki/gotovye ×0.5, музыки нет.
- Плашка «Не является индивидуальной инвестиционной рекомендацией» первые 5 сек, сноска про «правило 4%» (Trinity, 1998) на сцене ответа 2.
- Счётчик вопросов 1-2-3 вверху кадра (y≈292): активный чёрный, отвеченный жёлтый с галочкой (circles() + qcounter()).
- Движок «Дивана» (compose_dv.py). Новые предметы в kod/scenes_sv.py: витрина «СВОБОДА» с ценником, мешок на ножках bagleg(), шезлонг, растяжка BLACK FRIDAY, кроссовки, корзина «ТРАТЫ», листок-расчёт, шкала «до свободы». Новый клип carryR.
- Порядок: из kod/ pip install cairosvg → tts.py → clips.py → node 3d/frames.js clips.json kadry flat → compose_sv.py sheet 0.6 → ./run_sv.sh.
- Обложки: oblozhka/ (A «СВОБОДА СО СКИДКОЙ» oblozhka-svoboda-v2-a-skidka.png — рекомендую, B «РАСХОДЫ ×300»).
