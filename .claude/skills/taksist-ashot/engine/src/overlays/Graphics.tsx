import React from 'react';
import {P} from '../palette';
import {after, clamp, cue, easeOut, lerp, pop} from '../lib';

// Инфографика в экранных координатах. Всё важное внутри безопасной зоны Reels:
// x 56..922, y 250..1600.
const F = 'Rubik';
const card = (w: number, h: number, fill = P.cream) => (
  <rect x={-w / 2} y={-h / 2} width={w} height={h} rx={h / 2.6} fill={fill} stroke={P.ink} strokeWidth={8} />
);
const vis = (t: number, a: string, b: string, fade = 0.12) => clamp(Math.min((t - cue(a)) / fade, (cue(b) - t) / fade));

export const MoneyCard: React.FC<{t: number}> = ({t}) => {
  const o = vis(t, 'n5', 'shock', 0.08);
  if (o <= 0) return null;
  const s5 = pop(after(t, cue('n5'), 0.45));
  const cr = easeOut(after(t, cue('cross'), 0.25));
  const s12 = pop(after(t, cue('n12'), 0.5));
  return (
    <g opacity={o}>
      <g transform={`translate(489,340) scale(${s5}) rotate(-3)`}>
        {card(600, 130)}
        <text y={26} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={78} fill={P.ink} opacity={1 - cr * 0.45}>5 000 000 ₽</text>
        <path d={`M-250,8 L${lerp(-250, 250, cr)},${lerp(8, -14, cr)}`} stroke={P.terracotta} strokeWidth={16} strokeLinecap="round" />
      </g>
      {s12 > 0.001 && (
        <g transform={`translate(489,510) scale(${s12}) rotate(2)`}>
          {card(720, 170, P.terracotta)}
          <text y={36} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={104} fill={P.cream}>12 000 000+ ₽</text>
        </g>
      )}
      {/* летящие монетки */}
      {Array.from({length: 7}, (_, i) => {
        const k = after(t, cue('n12') + i * 0.03, 0.7);
        if (k <= 0 || k >= 1) return null;
        const ang = -Math.PI / 2 + (i - 3) * 0.42;
        const x = 489 + Math.cos(ang) * 330 * easeOut(k), y = 510 + Math.sin(ang) * 220 * easeOut(k) + k * k * 240;
        return (
          <g key={i} transform={`translate(${x},${y}) rotate(${k * 300})`} opacity={1 - k}>
            <circle r={26} fill={P.gold} stroke={P.ink} strokeWidth={5} />
            <text y={11} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={30} fill={P.goldDark}>₽</text>
          </g>
        );
      })}
    </g>
  );
};

export const HouseRibbon: React.FC<{t: number}> = ({t}) => {
  const o = vis(t, 'explain', 'buttons', 0.1);
  if (o <= 0) return null;
  const sh = pop(after(t, cue('explain'), 0.45));
  const un = easeOut(after(t, cue('years'), 0.9));
  const lab = pop(after(t, cue('years') + 0.25, 0.45));
  const life = pop(after(t, cue('life'), 0.4));
  const x0 = 210, x1 = lerp(x0 + 40, 900, un), y = 430;
  const year = Math.round(lerp(2026, 2046, un));
  return (
    <g opacity={o}>
      {/* лента календаря */}
      {un > 0 && (
        <g>
          <path d={`M${x0},${y - 46} L${x1},${y - 46} L${x1 + 22},${y} L${x1},${y + 46} L${x0},${y + 46}Z`} fill={P.cream} stroke={P.ink} strokeWidth={7} strokeLinejoin="round" />
          {Array.from({length: 20}, (_, i) => {
            const x = x0 + 40 + i * 33;
            if (x > x1 - 10) return null;
            return <g key={i}><rect x={x - 10} y={y - 30} width={22} height={60} rx={5} fill={i % 5 === 4 ? P.mustard : P.beige} stroke={P.ink} strokeWidth={3} /></g>;
          })}
          <g transform={`translate(${x1 - 40},${y - 100})`}>
            <rect x={-80} y={-34} width={160} height={66} rx={14} fill={P.ink} />
            <text y={18} textAnchor="middle" fontFamily={F} fontWeight={800} fontSize={48} fill={P.mustard}>{year}</text>
          </g>
        </g>
      )}
      {/* домик */}
      <g transform={`translate(${x0},${y}) scale(${sh})`}>
        <rect x={-95} y={-40} width={190} height={150} rx={10} fill={P.cream} stroke={P.ink} strokeWidth={8} />
        <path d="M-125,-30 L0,-140 L125,-30Z" fill={P.terracotta} stroke={P.ink} strokeWidth={8} strokeLinejoin="round" />
        <rect x={-30} y={30} width={60} height={80} rx={6} fill={P.cabinLight} stroke={P.ink} strokeWidth={6} />
        <rect x={-78} y={-10} width={40} height={36} rx={5} fill={P.win} stroke={P.ink} strokeWidth={5} />
        <rect x={40} y={-10} width={40} height={36} rx={5} fill={P.win} stroke={P.ink} strokeWidth={5} />
      </g>
      {lab > 0.001 && (
        <g transform={`translate(660,${y + 150}) scale(${lab}) rotate(-4)`}>
          {card(330, 120, P.mustard)}
          <text y={30} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={84} fill={P.ink}>20 ЛЕТ</text>
        </g>
      )}
      {life > 0.001 && (
        <g transform={`translate(330,${y + 160}) scale(${life}) rotate(6)`}>
          <path d="M0,30 C-70,-20 -40,-70 0,-36 C40,-70 70,-20 0,30Z" fill={P.terracotta} stroke={P.ink} strokeWidth={6} />
        </g>
      )}
    </g>
  );
};

export const Buttons: React.FC<{t: number}> = ({t}) => {
  const o = vis(t, 'buttons', 'remember', 0.1);
  if (o <= 0) return null;
  const a = pop(after(t, cue('buttons'), 0.4)), b = pop(after(t, cue('buttons') + 0.12, 0.4));
  const pk = after(t, cue('poke'), 0.12);
  const press = pk > 0 && pk < 1 ? 1 - Math.sin(pk * Math.PI) * 0.08 : 1;
  const on = pk >= 0.5 ? 1 : 0;
  const dim = Math.max(easeOut(after(t, cue('poke'), 0.3)) * 0.5, easeOut(after(t, cue('dim'), 0.3)));
  const less = pop(after(t, cue('less'), 0.45));
  // рука Ашота заходит слева и тычет в «срок»
  const hin = easeOut(after(t, cue('poke') - 0.4, 0.35));
  const hk = pk > 0 ? Math.sin(Math.min(1, pk) * Math.PI) : 0;
  const hx = lerp(-260, 470, hin) + hk * 24, hy = lerp(930, 650, hin) - hk * 20;
  const hout = easeOut(after(t, cue('dim') + 0.15, 0.35));
  return (
    <g opacity={o}>
      <g transform={`translate(489,380) scale(${a})`} opacity={1 - dim * 0.6}>
        {card(700, 140, lerp(1, 0, dim) > 0.5 ? P.cream : '#CFC4B4')}
        <text y={22} textAnchor="middle" fontFamily={F} fontWeight={800} fontSize={60} fill={P.ink}>УМЕНЬШИТЬ ПЛАТЁЖ</text>
        {dim > 0.6 && <path d="M-300,0 L300,0" stroke={P.terracotta} strokeWidth={10} strokeLinecap="round" opacity={(dim - 0.6) * 2.5} />}
      </g>
      <g transform={`translate(489,560) scale(${b * press})`}>
        {card(700, 140, on ? P.sage : P.cream)}
        {on ? <circle cx={-290} cy={0} r={44} fill={P.cream} stroke={P.ink} strokeWidth={6} /> : null}
        {on ? <path d="M-312,0 L-296,18 L-266,-18" fill="none" stroke={P.sageDark} strokeWidth={11} strokeLinecap="round" strokeLinejoin="round" /> : null}
        <text x={on ? 30 : 0} y={22} textAnchor="middle" fontFamily={F} fontWeight={800} fontSize={60} fill={on ? P.cream : P.ink}>УМЕНЬШИТЬ СРОК</text>
      </g>
      {on ? (
        <g transform={`translate(489,560)`} opacity={1 - after(t, cue('poke'), 0.5)}>
          <rect x={-350 - after(t, cue('poke'), 0.5) * 30} y={-70 - after(t, cue('poke'), 0.5) * 30} width={700 + after(t, cue('poke'), 0.5) * 60} height={140 + after(t, cue('poke'), 0.5) * 60} rx={60} fill="none" stroke={P.sage} strokeWidth={10} />
        </g>
      ) : null}
      {hin > 0 && hout < 1 && (
        <g transform={`translate(${hx - hout * 600},${hy + hout * 300}) rotate(-38)`}>
          <path d="M-30,60 L-34,420" stroke={P.ink} strokeWidth={112} strokeLinecap="round" />
          <path d="M-30,60 L-34,420" stroke={P.skin} strokeWidth={96} strokeLinecap="round" />
          <path d="M-34,330 L-36,520" stroke={P.ink} strokeWidth={150} />
          <path d="M-34,330 L-36,520" stroke={P.shirt} strokeWidth={134} />
          <rect x={-74} y={-10} width={96} height={110} rx={40} fill={P.skin} stroke={P.ink} strokeWidth={9} />
          <rect x={-16} y={-110} width={38} height={130} rx={19} fill={P.skin} stroke={P.ink} strokeWidth={9} />
          <path d="M-74,40 Q-104,10 -86,-14 Q-66,-20 -56,6" fill={P.skin} stroke={P.ink} strokeWidth={8} />
          <path d="M-60,40 Q-30,54 10,40" fill="none" stroke={P.skinShade} strokeWidth={6} />
        </g>
      )}
      {less > 0.001 && (
        <g transform={`translate(489,720) scale(${less})`}>
          {card(560, 110, P.cream)}
          <text x={-30} y={20} textAnchor="middle" fontFamily={F} fontWeight={800} fontSize={54} fill={P.sageDark}>ПЕРЕПЛАТА</text>
          <g transform={`translate(200,${Math.sin(t * 9) * 8})`}>
            <path d="M0,-34 L0,26 M-24,4 L0,30 L24,4" fill="none" stroke={P.sageDark} strokeWidth={12} strokeLinecap="round" strokeLinejoin="round" />
          </g>
        </g>
      )}
    </g>
  );
};

export const Stamp400: React.FC<{t: number}> = ({t}) => {
  const k = after(t, cue('n400'), 0.35);
  if (k <= 0) return null;
  const s = lerp(2.4, 1, easeOut(k));
  return (
    <g transform={`translate(489,470) scale(${s}) rotate(-7)`} opacity={clamp(k * 3)}>
      <rect x={-260} y={-95} width={520} height={190} rx={30} fill={P.cream} stroke={P.terracotta} strokeWidth={14} />
      <rect x={-240} y={-75} width={480} height={150} rx={20} fill="none" stroke={P.terracotta} strokeWidth={5} />
      <text y={46} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={140} fill={P.terracotta}>400 ₽</text>
    </g>
  );
};
