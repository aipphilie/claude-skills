# Мои скиллы для Claude Code

Открывайте облачную сессию Claude Code с этим репозиторием, и скиллы подключатся автоматически.

- `.claude/skills/` — скиллы: HyperFrames, ui-ux-pro-max, taste-skill, impeccable, emilkowalski/skills
- `.claude/skills/идеи-сериалов`, `.claude/skills/мастер-рилс-сериалов` — мои скиллы: идеи мистических сериалов и производство рилсов (сценарий, озвучка, анимация, монтаж, звук)
- `.claude/skills/yarik-ideas`, `.claude/skills/yarik-montage` — скиллы канала «Как работает Ярик»: идеи роликов и монтаж Reels. В каждой папке лежит полная концепция `КОНЦЕПЦИЯ.md`
- `.claude/skills/sud-prisyazhnyh` — суд присяжных для рилсов Ярика: гений по хукам, 20 агентов-зрителей, тролль, друг с репостом, алгоритм Инсты, адвокат Ярика и судья. Дай сценарий и напиши «запусти суд». Zip для claude.ai — `zip/yarik/sud-prisyazhnyh.zip`
- `.claude/skills/petlya-vovlechennosti` — петля вовлечённости: прокачивает сценарий рилса по 6 шагам (шок, интрига, пружина, катарсис с поворотом, перенос симпатии, условный рефлекс), ставит оценки и выдаёт исправленный сценарий. Zip для claude.ai — `zip/yarik/petlya-vovlechennosti.zip`
- `taksist-ashot/` — папка проекта «Таксист Ашот»: сценарии серий, суды, раскадровки, персонажи, черновые видео
- `.claude/skills/taksist-ashot` — сериал Reels «Таксист Ашот»: персонажи кодом (Ашот + конструктор пассажиров), салон, инфографика, субтитры, озвучка, звук, рендер на Remotion. правила, голоса, движок
- `.claude/skills/ushi` — уши для Claude: **Openverse** (где взять звук, CC0), **Real SFX** ([opus-sound-layer](https://github.com/Bodila51/opus-sound-layer), MIT — библиотека живых записей, микс, QA), **PANNs** (нейросеть слушает ролик и говорит, что и где звучит). Подключён к скиллам Ашота, Ярика и мистических сериалов. В новой сессии: «поставь уши» → `bash .claude/skills/ushi/scripts/setup.sh`
- `.claude/skills/ig-*` — 13 скиллов для Instagram из [Jakeschincariol/instagram-agent-skill](https://github.com/Jakeschincariol/instagram-agent-skill) (MIT): `/ig-reel` (хуки, сценарий, раскадровка по времени), `/ig-caption`, `/ig-human` и др. Шаблон голоса — `.claude/skills/ig-reel/voice-template.md`, заполненный кладите в `~/.claude/instagram/voice.md`
- `zip/instagram/` — те же 13 скиллов Instagram в zip, по одному на скилл, для загрузки в claude.ai (Настройки → скиллы)
- `.claude/skills/higgsfield-*` — скиллы Higgsfield (генерация картинок и видео)
- `.mcp.json` — MCP-сервер [codebase-memory-mcp](https://github.com/DeusData/codebase-memory-mcp) 0.12.1 (граф кода: поиск функций, связей, архитектуры). Включается сам в каждой сессии, при старте индексирует репо в фоне, а к каждому сообщению хук добавляет напоминание пользоваться его инструментами
- `.claude/settings.json` — плагин Remotion (подтягивается из маркетплейса remotion-dev/claude-code-plugin) и автоустановка программы Higgsfield при старте сессии

## Higgsfield в новой сессии

Программа ставится сама. Войти нужно вручную: попросите Claude «войди в Higgsfield» — он даст ссылку для входа, а после входа нужно прислать ему адрес страницы с ошибкой (`http://localhost:8765/callback?code=...`).

Обновить скиллы до свежих версий: `npx skills add <источник> -g -y -a claude-code`, затем заново скопировать нужные папки из `~/.claude/skills` сюда.
