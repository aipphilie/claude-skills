import React from 'react';
import {P} from '../palette';
import {after, clamp, cue, easeOut, lerp, pop, story} from '../lib';

// Плашки полной серии из story.json: cards (цифры и цитаты), score («ОТЫГРАЛИ У БАНКА»), шпаргалка.
// Экранные координаты 1080×1920, всё внутри безопасной зоны x 56..922, y 250..1600.
const F = 'Rubik';
const FILL: Record<string, [string, string]> = {
  cream: [P.cream, P.ink], terracotta: [P.terracotta, P.cream], sage: [P.sage, P.cream], mustard: [P.mustard, P.ink],
};
const fmt = (n: number) => Math.round(n).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
// ширина текста Rubik 900 ≈ 0.64 em на символ (капс шире)
const textW = (s: string, size: number) => s.length * size * (s === s.toUpperCase() ? 0.66 : 0.58);

// пока видна шкала «ОТЫГРАЛИ» (сверху справа), плашки уходят ниже, чтобы не налезать
const scoreA = story.score ? cue(story.score.from) : 1e9, scoreB = story.score ? cue(story.score.to) : 0;
const cards = (story.cards || []).map((c: any) => { const a = cue(c.from); return {...c, a, b: cue(c.to), y: c.y + (a >= scoreA - 0.3 && a < scoreB ? 160 : 0)}; });

export const Cards: React.FC<{t: number}> = ({t}) => (
  <g>
    {cards.filter((c: any) => t >= c.a && t < c.b + 0.15).map((c: any, i: number) => {
      const o = clamp(Math.min((t - c.a) / 0.08, (c.b + 0.15 - t) / 0.15));
      const s = pop(after(t, c.a, 0.45));
      const [bg, fg] = FILL[c.fill] || FILL.cream;
      let size = c.size; let w = textW(c.text, size) + 90;
      if (w > 860) { size *= 860 / w; w = 860; }
      const h = size * 1.75;
      return (
        <g key={i} opacity={o} transform={`translate(489,${c.y}) scale(${s}) rotate(${c.rot || 0})`}>
          <rect x={-w / 2} y={-h / 2 + 10} width={w} height={h} rx={h / 2.6} fill={P.ink} opacity={0.35} />
          <rect x={-w / 2} y={-h / 2} width={w} height={h} rx={h / 2.6} fill={bg} stroke={P.ink} strokeWidth={8} />
          <text y={size * 0.36} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={size} fill={fg}>{c.text}</text>
        </g>
      );
    })}
  </g>
);

// шкала «ОТЫГРАЛИ У БАНКА»: появляется на «фокусе», цифра прыгает по шагам
export const Score: React.FC<{t: number}> = ({t}) => {
  const sc = story.score; if (!sc) return null;
  const a = cue(sc.from), b = cue(sc.to);
  if (t < a || t > b + 0.2) return null;
  const steps: [number, number][] = sc.steps.map((s: any) => [cue(s[0]), s[1]]);
  let i = 0; while (i + 1 < steps.length && t >= steps[i + 1][0]) i++;
  const prev = i > 0 ? steps[i - 1][1] : 0, k = easeOut(after(t, steps[i][0], 0.7));
  const val = lerp(prev, steps[i][1], k);
  const bump = i > 0 ? Math.sin(clamp(after(t, steps[i][0], 0.4)) * Math.PI) * 0.12 : 0;
  const o = clamp(Math.min((t - a) / 0.2, (b + 0.2 - t) / 0.2));
  return (
    <g opacity={o} transform={`translate(${922 - 190},300) scale(${pop(after(t, a, 0.5)) * (1 + bump)})`}>
      <rect x={-190} y={-70} width={380} height={140} rx={30} fill={P.ink} opacity={0.88} stroke={P.sage} strokeWidth={6} />
      <text y={-22} textAnchor="middle" fontFamily={F} fontWeight={800} fontSize={28} fill={P.cream}>ОТЫГРАЛИ У БАНКА</text>
      <text y={44} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={56} fill="#9FD18A">{fmt(val)} ₽</text>
    </g>
  );
};

// шпаргалка в конце: скриншотабельная, 4 пункта + призыв
const CHEAT = [
  ['1', 'Смотри в графике платежей', 'ОБЩУЮ СУММУ выплат'],
  ['2', 'Сначала подушка —', '3 месяца жизни'],
  ['3', 'Лишнее — в досрочку,', 'на СРОК'],
  ['4', 'Ставка −1%', '= −806 000 ₽'],
];
export const ShotCheat: React.FC<{lt: number}> = ({lt}) => (
  <svg viewBox="0 0 1080 1920">
    <rect width={1080} height={1920} fill="#231B18" />
    {Array.from({length: 18}, (_, i) => <circle key={i} cx={(i * 211) % 1080} cy={(i * 347) % 1920} r={60 + (i % 4) * 30} fill={P.mustard} opacity={0.05} />)}
    <g transform={`translate(0,${lerp(40, 0, easeOut(lt / 0.4))})`} opacity={clamp(lt / 0.2)}>
      <text x={540} y={330} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={86} fill={P.mustard}>ШПАРГАЛКА АШОТА</text>
      <text x={540} y={400} textAnchor="middle" fontFamily={F} fontWeight={700} fontSize={38} fill={P.cream} opacity={0.8}>ипотека · сохрани</text>
      {CHEAT.map(([n, a, b], i) => {
        const k = pop(after(lt, 0.15 + i * 0.18, 0.4));
        const y = 520 + i * 230;
        return (
          <g key={i} transform={`translate(540,${y}) scale(${k})`}>
            <rect x={-430} y={-90} width={860} height={190} rx={40} fill={P.cream} stroke={P.ink} strokeWidth={8} />
            <circle cx={-340} cy={5} r={56} fill={P.terracotta} stroke={P.ink} strokeWidth={6} />
            <text x={-340} y={30} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={70} fill={P.cream}>{n}</text>
            <text x={-250} y={-12} fontFamily={F} fontWeight={700} fontSize={44} fill={P.ink}>{a}</text>
            <text x={-250} y={56} fontFamily={F} fontWeight={900} fontSize={52} fill={P.terracotta}>{b}</text>
          </g>
        );
      })}
      <g transform={`translate(540,1480) scale(${pop(after(lt, 1.0, 0.45))})`}>
        <rect x={-430} y={-70} width={860} height={140} rx={70} fill={P.mustard} stroke={P.ink} strokeWidth={8} />
        <text y={20} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={44} fill={P.ink}>Скинь тому, кто берёт ипотеку</text>
      </g>
      <text x={540} y={1610} textAnchor="middle" fontFamily={F} fontWeight={800} fontSize={34} fill={P.cream} opacity={clamp((lt - 1.3) / 0.3)}>Ты на срок или на платёж? Пиши в комменты</text>
    </g>
  </svg>
);
