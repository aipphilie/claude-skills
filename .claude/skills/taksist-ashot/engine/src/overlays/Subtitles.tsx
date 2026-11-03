import React from 'react';
import {P} from '../palette';
import {lines, story, after, pop} from '../lib';

// Субтитры: по 2–3 слова, ключевые цифры горчичным, текущее слово крупнее.
type W = {w: string; s: number; e: number};
const chunks = (() => {
  const out: {words: W[]; s: number; e: number; who: string}[] = [];
  for (const L of lines) {
    let cur: W[] = [];
    const flush = () => { if (cur.length) out.push({words: cur, s: cur[0].s, e: 0, who: L.who}); cur = []; };
    L.words.forEach((w, i) => {
      cur.push(w);
      const len = cur.map((x) => x.w).join(' ').length;
      const punct = /[,.?!]$/.test(w.w);
      if (cur.length >= 3 || len > 15 || (punct && cur.length >= 1 && i < L.words.length - 1 && (cur.length >= 2 || /[.?!]$/.test(w.w)))) flush();
    });
    flush();
  }
  out.forEach((c, i) => { const n = out[i + 1]; c.e = n ? Math.min(n.s, c.words[c.words.length - 1].e + 0.6) : 99; });
  return out;
})();
const KEYS: string[] = story.keys;
const norm = (w: string) => w.toLowerCase().replace(/[^а-яёa-z0-9]/g, '');

export const Subtitles: React.FC<{t: number}> = ({t}) => {
  const c = chunks.find((x) => t >= x.s - 0.03 && t < x.e);
  if (!c) return null;
  const k = pop(after(t, c.s - 0.03, 0.22));
  return (
    <div style={{position: 'absolute', left: 140, right: 140, top: 1330, height: 260, display: 'flex', justifyContent: 'center', alignItems: 'center'}}>
      <div style={{display: 'flex', flexWrap: 'wrap', justifyContent: 'center', gap: '0 34px', maxWidth: 800, transform: `scale(${0.85 + 0.15 * k})`}}>
        {c.words.map((w, i) => {
          const active = t >= w.s - 0.02 && t < (c.words[i + 1]?.s ?? w.e + 0.4);
          const key = KEYS.includes(norm(w.w));
          return (
            <span key={i} style={{
              fontFamily: 'Rubik', fontWeight: 900, fontSize: 92, lineHeight: 1.12, textTransform: 'uppercase',
              color: key ? P.mustard : c.who === 'passenger' ? '#FFFFFF' : P.cream,
              WebkitTextStroke: `13px ${P.ink}`, paintOrder: 'stroke fill',
              transform: `scale(${active ? 1.1 : 1}) translateY(${active ? -4 : 0}px)`, display: 'inline-block',
              textShadow: `0 8px 0 ${P.ink}`,
            }}>{w.w.replace(/[,.]$/, '')}</span>
          );
        })}
      </div>
    </div>
  );
};
