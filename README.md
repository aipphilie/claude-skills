# Мои скиллы для Claude Code

Открывайте облачную сессию Claude Code с этим репозиторием, и скиллы подключатся автоматически.

- `.claude/skills/` — скиллы: HyperFrames, ui-ux-pro-max, taste-skill, impeccable, emilkowalski/skills
- `.claude/skills/идеи-сериалов`, `.claude/skills/мастер-рилс-сериалов` — мои скиллы: идеи мистических сериалов и производство рилсов (сценарий, озвучка, анимация, монтаж, звук)
- `.claude/settings.json` — плагин Remotion (подтягивается из маркетплейса remotion-dev/claude-code-plugin)

Обновить скиллы до свежих версий: `npx skills add <источник> -g -y -a claude-code`, затем заново скопировать нужные папки из `~/.claude/skills` сюда.
