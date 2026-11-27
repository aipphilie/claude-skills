"""Готовит ключи штатных анимаций для рендера 3D-героя."""
import json
import os
import sys
from pathlib import Path

project = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project))
import anim3d

work = Path(os.environ['NETUPI_WORK'])
work.mkdir(parents=True, exist_ok=True)
names = ('cheshet-golovu', 'dyhanie', 'pozhimaet-plechami')
jobs = {}
for name in names:
    poses, mouths = anim3d.ANIMS[name][1]()
    jobs[name] = [anim3d.to3d(pose, mouth, name) for pose, mouth in zip(poses, mouths)]
(work/'poses.json').write_text(json.dumps(jobs))
