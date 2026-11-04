import TL from './timeline.json';
import STORY from './story.json';
export const FPS = 30;
export const timeline = TL as any;
export const story = STORY as any;
type Line = {id: string; who: string; start: number; end: number; words: {w: string; s: number; e: number}[]};
export const lines: Line[] = timeline.lines;
export const lineById = (id: string) => lines.find((l) => l.id === id)!;
export const cue = (name: string | number | any[]): number => {
  if (typeof name === 'number') return name;
  const c = Array.isArray(name) ? name : story.cues[name];
  if (c === undefined) throw new Error('no cue ' + name);
  if (typeof c === 'number') return c;
  const [id, w, off] = c; const L = lineById(id);
  const base = w === 'end' ? L.end : w === 'start' ? L.start : L.words[w].s;
  return base + (off || 0);
};
export const clamp = (x: number, a = 0, b = 1) => Math.max(a, Math.min(b, x));
export const lerp = (a: number, b: number, k: number) => a + (b - a) * k;
export const easeOut = (k: number) => 1 - Math.pow(1 - clamp(k), 3);
export const easeInOut = (k: number) => { k = clamp(k); return k < 0.5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2; };
// пружинка 0→1 с перелётом
export const pop = (k: number) => { k = clamp(k); return 1 - Math.cos(k * Math.PI * 2.5) * Math.exp(-k * 6); };
// прогресс после события за dur секунд
export const after = (t: number, at: number, dur = 0.25) => clamp((t - at) / dur);
export const ampAt = (who: 'ashot' | 'passenger', t: number) => {
  const a: number[] = timeline.amp[who]; const f = t * FPS; const i = Math.floor(f);
  const v0 = a[i] || 0, v1 = a[i + 1] || 0; return lerp(v0, v1, f - i);
};
// форма рта по амплитуде: 0 закрыт, 1 узкий, 2 средний «а», 3 широкий «о»
export const mouthShape = (amp: number) => (amp < 0.07 ? 0 : amp < 0.3 ? 1 : amp < 0.62 ? 2 : 3);
// моргание: детерминированно, ~каждые 2.6–3.4 сек
export const blink = (t: number, seed = 0) => {
  const period = 2.9 + (seed % 3) * 0.35; const ph = (t + seed * 0.77) % period;
  return ph < 0.12 ? Math.sin((ph / 0.12) * Math.PI) : 0;
};
export const noise = (t: number, s = 1) => Math.sin(t * 37.1 * s + 1.3) * 0.5 + Math.sin(t * 23.7 * s + 4.1) * 0.3 + Math.sin(t * 61.3 * s) * 0.2;
export const freezeT = () => cue('freeze');
