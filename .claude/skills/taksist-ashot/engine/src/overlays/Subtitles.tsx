import React from 'react';
import {P} from '../palette';
import {lines, story, after, pop} from '../lib';

// Субтитры. Стили (story.sub.style или inputProps.sub):
//  A — по 2–3 слова, капс, кремовые с обводкой, цифры горчичным (было);
//  B — по одному слову крупно, с поп-анимацией и наклоном;
//  C — фраза на плашке цвета героя (Ашот горчичный, пассажир шалфейный), обычный регистр;
//  D — караоке: фраза белым, сказанные слова жёлтые, тёмная подложка;
//  E — подпись как в кино: обычный регистр, белый, тонкая тень, по фразе;
//  F — плашка героя (C) + караоке, выбор автора 2026-11-03.
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


// фразы целиком (для C/D/E): до ~26 символов
const phrases = (() => {
  const out: {words: W[]; s: number; e: number; who: string}[] = [];
  for (const L of lines) {
    let cur: W[] = [];
    const flush = () => {
      // короткий предлог/союз в конце фразы («с», «в», «и») переносим в следующую
      let carry: W[] = [];
      if (cur.length > 1 && cur[cur.length - 1].w.length <= 2 && !/[.?!,:]$/.test(cur[cur.length - 1].w)) carry = [cur.pop()!];
      if (cur.length) out.push({words: cur, s: cur[0].s, e: 0, who: L.who}); cur = carry;
    };
    L.words.forEach((w) => {
      if (cur.length && (cur.map((x) => x.w).join(' ') + ' ' + w.w).length > 22) flush();
      cur.push(w);
      if (/[.?!:]$/.test(w.w)) flush();
    });
    flush(); flush();
  }
  out.forEach((c, i) => { const n = out[i + 1]; c.e = n ? Math.min(n.s, c.words[c.words.length - 1].e + 0.6) : 99; });
  return out;
})();
const clean = (w: string) => w.replace(/[,.:]$/, '');
const isKey = (w: string) => KEYS.includes(norm(w));

export const Subtitles: React.FC<{t: number; style?: string}> = ({t, style}) => {
  const st = style || story.sub?.style || 'A';
  if (st === 'B') {
    let cur: W | null = null; let who = 'ashot';
    for (const L of lines) for (let i = 0; i < L.words.length; i++) {
      const w = L.words[i]; const nx = L.words[i + 1]?.s ?? w.e + 0.35;
      if (t >= w.s - 0.03 && t < nx) { cur = w; who = L.who; }
    }
    if (!cur) return null;
    const k = pop(after(t, cur.s - 0.03, 0.25));
    const key = isKey(cur.w);
    const rot = ((cur.s * 7.3) % 1 > 0.5 ? 1 : -1) * 3;
    return (
      <div style={{position: 'absolute', left: 60, right: 60, top: 1290, height: 260, display: 'flex', justifyContent: 'center', alignItems: 'center'}}>
        <span style={{fontFamily: 'Rubik', fontWeight: 900, fontSize: 104, textTransform: 'uppercase', color: key ? P.mustard : who === 'passenger' ? '#FFFFFF' : P.cream,
          WebkitTextStroke: `12px ${P.ink}`, paintOrder: 'stroke fill', textShadow: `0 8px 0 ${P.ink}`, display: 'inline-block',
          transform: `scale(${0.6 + 0.4 * k}) rotate(${rot}deg)`}}>{clean(cur.w)}</span>
      </div>
    );
  }
  if (st === 'C' || st === 'D' || st === 'E' || st === 'F') {
    const c = phrases.find((x) => t >= x.s - 0.03 && t < x.e);
    if (!c) return null;
    const k = pop(after(t, c.s - 0.03, 0.22));
    if (st === 'F') {
      // плашка героя + караоке: текущее слово на цветном чипе, сказанные яркие, ещё не сказанные приглушены
      const pas = c.who === 'passenger';
      const base = pas ? '#FFFFFF' : P.ink, chip = pas ? P.ink : P.terracotta;
      return (
        <div style={{position: 'absolute', left: 70, right: 70, top: 1330, height: 260, display: 'flex', justifyContent: 'center', alignItems: 'center'}}>
          <div style={{background: pas ? P.sage : P.mustard, border: `7px solid ${P.ink}`, borderRadius: 40, padding: '16px 26px', maxWidth: 860,
            boxShadow: `0 9px 0 ${P.ink}`, transform: `scale(${0.85 + 0.15 * k}) rotate(${pas ? 1.5 : -1.5}deg)`, textAlign: 'center',
            fontFamily: 'Rubik', fontWeight: 800, fontSize: 58, lineHeight: 1.3, color: base}}>
            {c.words.map((w, i) => {
              const said = t >= w.s - 0.02;
              const cur = said && t < (c.words[i + 1]?.s ?? w.e + 0.3);
              const kk = cur ? pop(after(t, w.s - 0.02, 0.2)) : 1;
              return (
                <React.Fragment key={i}>{i ? ' ' : ''}
                  <span style={{display: 'inline-block', padding: '0 8px', borderRadius: 16, background: cur ? chip : 'transparent',
                    color: cur ? P.cream : isKey(w.w) && said ? (pas ? P.ink : P.terracotta) : base, opacity: said ? 1 : 0.45,
                    fontWeight: isKey(w.w) || cur ? 900 : 800, transform: `scale(${cur ? 1 + 0.08 * kk : 1})`}}>{w.w}</span>
                </React.Fragment>
              );
            })}
          </div>
        </div>
      );
    }
    if (st === 'C') {
      const pas = c.who === 'passenger';
      return (
        <div style={{position: 'absolute', left: 80, right: 80, top: 1330, height: 260, display: 'flex', justifyContent: 'center', alignItems: 'center'}}>
          <div style={{background: pas ? P.sage : P.mustard, border: `7px solid ${P.ink}`, borderRadius: 40, padding: '18px 34px', maxWidth: 820,
            boxShadow: `0 9px 0 ${P.ink}`, transform: `scale(${0.85 + 0.15 * k}) rotate(${pas ? 1.5 : -1.5}deg)`, textAlign: 'center',
            fontFamily: 'Rubik', fontWeight: 800, fontSize: 54, lineHeight: 1.15, color: pas ? '#FFFFFF' : P.ink}}>
            {c.words.map((w, i) => <span key={i} style={{color: isKey(w.w) ? (pas ? P.ink : P.terracotta) : undefined, fontWeight: isKey(w.w) ? 900 : 800}}>{(i ? ' ' : '') + w.w}</span>)}
          </div>
        </div>
      );
    }
    if (st === 'D') return (
      <div style={{position: 'absolute', left: 70, right: 70, top: 1330, height: 260, display: 'flex', justifyContent: 'center', alignItems: 'center'}}>
        <div style={{background: 'rgba(20,14,12,0.78)', borderRadius: 26, padding: '16px 30px', maxWidth: 860, textAlign: 'center',
          fontFamily: 'Rubik', fontWeight: 900, fontSize: 60, lineHeight: 1.15, textTransform: 'uppercase', transform: `scale(${0.92 + 0.08 * k})`}}>
          {c.words.map((w, i) => {
            const said = t >= w.s - 0.02;
            return <span key={i} style={{color: said ? (isKey(w.w) ? '#7FE07A' : '#FFD84A') : '#FFFFFF', opacity: said ? 1 : 0.85}}>{(i ? ' ' : '') + clean(w.w)}</span>;
          })}
        </div>
      </div>
    );
    return (
      <div style={{position: 'absolute', left: 90, right: 90, top: 1380, height: 200, display: 'flex', justifyContent: 'center', alignItems: 'center'}}>
        <div style={{maxWidth: 840, textAlign: 'center', fontFamily: 'Rubik', fontWeight: 700, fontSize: 52, lineHeight: 1.2, color: '#FFFFFF',
          textShadow: '0 3px 6px rgba(0,0,0,0.9), 0 0 2px #000', opacity: Math.min(1, k * 2)}}>
          {c.words.map((w, i) => <span key={i} style={{color: isKey(w.w) ? '#FFD84A' : undefined}}>{(i ? ' ' : '') + w.w}</span>)}
        </div>
      </div>
    );
  }
  // A — как было
  const c = chunks.find((x) => t >= x.s - 0.03 && t < x.e);
  if (!c) return null;
  const k = pop(after(t, c.s - 0.03, 0.22));
  return (
    <div style={{position: 'absolute', left: 140, right: 140, top: 1330, height: 260, display: 'flex', justifyContent: 'center', alignItems: 'center'}}>
      <div style={{display: 'flex', flexWrap: 'wrap', justifyContent: 'center', gap: '0 30px', maxWidth: 800, transform: `scale(${0.85 + 0.15 * k})`}}>
        {c.words.map((w, i) => {
          const active = t >= w.s - 0.02 && t < (c.words[i + 1]?.s ?? w.e + 0.4);
          const key = KEYS.includes(norm(w.w));
          return (
            <span key={i} style={{
              fontFamily: 'Rubik', fontWeight: 900, fontSize: 55, lineHeight: 1.12, textTransform: 'uppercase',
              color: key ? P.mustard : c.who === 'passenger' ? '#FFFFFF' : P.cream,
              WebkitTextStroke: `8px ${P.ink}`, paintOrder: 'stroke fill',
              transform: `scale(${active ? 1.1 : 1}) translateY(${active ? -4 : 0}px)`, display: 'inline-block',
              textShadow: `0 5px 0 ${P.ink}`,
            }}>{w.w.replace(/[,.]$/, '')}</span>
          );
        })}
      </div>
    </div>
  );
};
