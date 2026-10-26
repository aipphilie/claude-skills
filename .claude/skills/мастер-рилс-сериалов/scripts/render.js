// usage: PAGE=episode.html node render.js stills t1,t2,...   |   PAGE=episode.html node render.js video out.mp4 <duration_sec>
// Renders a canvas page frame by frame. Pages must define window.ready (Promise) and window.renderFrame(t).
let chromium;
try { ({ chromium } = require('playwright')); } catch (e) { ({ chromium } = require('/opt/node-tools/node_modules/playwright')); }
const { spawn } = require('child_process');
const path = require('path');
(async () => {
  const [mode, a, b] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  page.on('pageerror', e => console.error('PAGE ERROR', e));
  await page.goto('file://' + path.join(__dirname, process.env.PAGE || 'index.html'));
  await page.evaluate(() => window.ready); if (process.env.SAFE) await page.evaluate(() => window.SAFE = true);
  if (mode === 'stills') {
    for (const t of a.split(',').map(Number)) {
      await page.evaluate(t => renderFrame(t), t);
      await page.screenshot({ path: path.join(__dirname, `still_${t}.png`) });
    }
  } else {
    const dur = Number(b), fps = 30, n = Math.round(dur * fps);
    const ff = spawn('ffmpeg', ['-y', '-v', 'error', '-f', 'image2pipe', '-framerate', '30', '-i', '-',
      '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', a], { stdio: ['pipe', 'inherit', 'inherit'] });
    const i0 = Math.round((+process.env.START || 0) * fps);   // START=<sec>: render a slice (parallel renders, then concat)
    for (let i = i0; i < i0 + n; i++) {
      await page.evaluate(t => renderFrame(t), i / fps);
      const buf = await page.screenshot({ type: 'jpeg', quality: 94 });
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
      if (i % 60 === 0) console.log('frame', i, '/', n);
    }
    ff.stdin.end();
    await new Promise(r => ff.on('close', r));
  }
  await browser.close();
})();
