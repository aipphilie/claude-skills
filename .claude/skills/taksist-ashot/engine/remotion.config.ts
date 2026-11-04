import {Config} from '@remotion/cli/config';
Config.setBrowserExecutable(process.env.REMOTION_CHROME || '/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell');
// swangle на 4 ядрах без GPU иногда дублирует полосы кадра (тайлы по 512 px) — рендерим через swiftshader
Config.setChromiumOpenGlRenderer('swiftshader');
