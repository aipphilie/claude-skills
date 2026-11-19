# «Почему в казино нет часов и окон» v1 (2026-11-19)
- kazino-v1.mp4: 1080x1920, 30 fps, ~60 сек, 33 сцены. Голос hU3rD0Yk7DoiYULTX1pD, Eleven v4 с тегами. Звуки из ne-tupi-zvuki/gotovye ×0.5. Музыки нет.
- Сценарий и текст: ne-tupi-idei/kazino/ (scenariy-v1.md, ozvuchka-v1.txt, opisanie.md).
- Движок «Чаевых» (весь экран, белый фон, переходы через действие, depth()). Новые позы человечка в clips.py: slot (жмёт автомат), hammer (вешает часы), wrist (смотрит на запястье), phone_scr (листает).
- Новые предметы (kod/scenes_kz.py): зал казино casino() с гирляндой и ковром, настенные часы wallclock(), след от часов emptyclock(), окно в кирпичах brickwin() (кирпичи вываливаются, выходит солнце), игровой автомат без логотипов slotm(), ниточки кукловода strings(), чертёж-лабиринт blueprint(), носилки с часами stretcher(), пузырь-«побег» bubble_escape(), большой телефон bigphone() (время / лента / видео / таймер), пустая кнопка «ХВАТИТ» nobutton(), ноутбук с бесконечным свитком laptop(). Серый человечек grey_man() для Фридмана и изобретателя ленты.
- Порядок: из kod/ pip install cairosvg; python3 -m http.server 8777 → tts.py → clips.py → node 3d/frames.js clips.json kadry flat (проверить альфу кадров) → compose_kz.py sheet 0.6 → ./run_kz.sh → cover_kz.py.
- Обложки: oblozhka/ (A «ИГРОКИ САМИ ПОПРОСИЛИ» рекомендую, B «ГДЕ ЧАСЫ?»).
