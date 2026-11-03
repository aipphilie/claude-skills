import React from 'react';
import {P} from '../palette';
import {clamp, lerp} from '../lib';

// Конструктор пассажира: каждый ролик — новый типаж, эмоции общие для всех.
// Начало координат — основание шеи. Голова ~190×220 (у ребёнка крупнее относительно тела).
export type Emotion = {blink: number; mouth: number; shock: number; worry: number; smile: number; look: [number, number]; sweat: number};
export const EMO: Record<string, Emotion> = {
  calm: {blink: 0, mouth: 0, shock: 0, worry: 0, smile: 0.6, look: [-0.4, 0], sweat: 0},
  talk: {blink: 0, mouth: 2, shock: 0, worry: 0, smile: 0.3, look: [-0.4, 0], sweat: 0},
  worry: {blink: 0, mouth: 0, shock: 0, worry: 1, smile: 0, look: [-0.5, 0.2], sweat: 1},
  shock: {blink: 0, mouth: 3, shock: 1, worry: 0, smile: 0, look: [0, 0], sweat: 0},
};
export type Rider = {
  name: string;
  skin: string; shade: string;
  headScale: number; bodyScale: number;
  jaw: 'soft' | 'round' | 'narrow';
  hair: 'messy' | 'perm' | 'cowlick' | 'ponytail' | 'bald' | 'sidepart' | 'bob';
  hairColor: string;
  clothes: 'hoodie' | 'cardigan' | 'schoolkid' | 'sweater' | 'jacket' | 'shirtTie';
  c1: string; c2: string;
  glasses?: boolean; earrings?: boolean; beads?: boolean; lips?: boolean; freckles?: boolean;
  headphones?: boolean; beard?: boolean; wrinkles?: boolean; lashes?: boolean;
};
const O = 7;

const Hair: React.FC<{r: Rider; back?: boolean}> = ({r, back}) => {
  const c = r.hairColor; const st = {fill: c, stroke: P.ink, strokeWidth: O, strokeLinejoin: 'round' as const};
  if (back) {
    if (r.hair === 'ponytail') return <path d="M70,-200 Q170,-190 150,-60 Q140,0 110,30 Q120,-60 70,-120Z" {...st} />;
    if (r.hair === 'bob') return <path d="M-112,-160 Q-120,-50 -100,-30 L100,-30 Q120,-50 112,-160Z" {...st} />;
    if (r.hair === 'perm') return <g>{[-1, 1].map((s) => [0, 1, 2].map((i) => <circle key={s + '' + i} cx={s * (100 - i * 4)} cy={-170 + i * 40} r={30} {...st} />))}</g>;
    return null;
  }
  switch (r.hair) {
    case 'messy': return <path d="M-98,-150 Q-112,-250 -10,-252 Q100,-262 104,-160 Q90,-196 60,-200 Q50,-176 20,-188 Q0,-170 -28,-190 Q-52,-170 -70,-196 Q-90,-180 -98,-150Z" {...st} />;
    case 'perm': return <g>{[-80, -40, 0, 40, 80, -60, -20, 20, 60].map((x, i) => <circle key={i} cx={x} cy={i < 5 ? -222 : -248} r={34} {...st} />)}</g>;
    case 'cowlick': return <g><path d="M-96,-150 Q-104,-246 0,-250 Q104,-246 96,-150 Q70,-200 0,-196 Q-70,-200 -96,-150Z" {...st} /><path d="M6,-248 Q-6,-292 30,-300 Q14,-280 22,-252" {...st} /></g>;
    case 'ponytail': return <path d="M-100,-140 Q-110,-252 0,-254 Q110,-252 100,-140 Q90,-200 30,-210 Q-20,-180 -100,-140Z" {...st} />;
    case 'bob': return <path d="M-112,-110 Q-124,-256 0,-258 Q124,-256 112,-110 Q100,-190 40,-206 Q-30,-200 -60,-180 Q-96,-160 -112,-110Z" {...st} />;
    case 'bald': return <g>{[-1, 1].map((s) => <path key={s} d={`M${s * 92},-170 Q${s * 110},-130 ${s * 90},-96 L${s * 78},-130Z`} {...st} />)}<path d="M-40,-226 q20,-10 40,0" fill="none" stroke={P.ink} strokeWidth={4} opacity={0.3} /></g>;
    case 'sidepart': return <path d="M-98,-140 Q-106,-252 -10,-254 Q104,-254 100,-150 Q96,-196 30,-206 L-30,-212 Q-80,-200 -98,-140Z" {...st} />;
  }
};

const Clothes: React.FC<{r: Rider}> = ({r}) => {
  const st = {stroke: P.ink, strokeWidth: O, strokeLinejoin: 'round' as const};
  const torso = 'M-190,60 Q-180,0 -70,-4 L70,-4 Q180,0 190,60 L215,420 L-215,420Z';
  switch (r.clothes) {
    case 'hoodie': return <g>
      <path d={torso} fill={r.c1} {...st} />
      <path d="M-60,-2 Q0,40 60,-2" fill="none" {...st} />
      <path d="M-26,24 l-6,90 M26,24 l6,90" stroke={P.cream} strokeWidth={6} strokeLinecap="round" />
      <path d="M-120,250 L120,250 L110,330 L-110,330Z" fill={r.c2} {...st} strokeWidth={5} />
    </g>;
    case 'cardigan': return <g>
      <path d={torso} fill={r.c1} {...st} />
      <path d="M-50,-4 L0,90 L50,-4" fill={P.cream} {...st} />
      <path d="M-50,-4 L-20,420 M50,-4 L20,420" stroke={P.ink} strokeWidth={5} />
      {[140, 220, 300].map((y) => <circle key={y} cx={-28} cy={y} r={8} fill={r.c2} stroke={P.ink} strokeWidth={4} />)}
      {[-1, 1].map((s) => [100, 180, 260, 340].map((y) => <path key={s + '' + y} d={`M${s * 70},${y} l${s * 30},14 l${s * 30},-14 l${s * 30},14`} fill="none" stroke={r.c2} strokeWidth={4} opacity={0.6} />))}
    </g>;
    case 'schoolkid': return <g>
      <path d={torso} fill={r.c1} {...st} />
      <path d="M-46,-4 L0,50 L46,-4" fill={P.cream} {...st} />
      <path d="M-140,10 L-150,420 M140,10 L150,420" stroke={P.ink} strokeWidth={46} />
      <path d="M-140,10 L-150,420 M140,10 L150,420" stroke={r.c2} strokeWidth={32} />
      <rect x={-40} y={180} width={80} height={60} rx={12} fill={P.mustard} stroke={P.ink} strokeWidth={5} />
    </g>;
    case 'sweater': return <g>
      <path d="M-210,70 Q-200,-4 -70,-8 L70,-8 Q200,-4 210,70 L230,420 L-230,420Z" fill={r.c1} {...st} />
      <path d="M-62,-6 Q0,34 62,-6" fill="none" stroke={r.c2} strokeWidth={18} />
      <path d="M-210,200 L210,200" stroke={r.c2} strokeWidth={14} opacity={0.7} />
    </g>;
    case 'jacket': return <g>
      <path d={torso} fill={r.c1} {...st} />
      <path d="M-40,-4 L0,120 L40,-4" fill={P.cream} {...st} />
      <path d="M-70,-4 L-10,200 L-90,120Z M70,-4 L10,200 L90,120Z" fill={r.c2} {...st} />
      <path d="M0,120 L0,420" stroke={P.ink} strokeWidth={5} />
    </g>;
    case 'shirtTie': return <g>
      <path d={torso} fill={r.c1} {...st} />
      <path d="M-50,-6 L-10,50 L-60,40Z M50,-6 L10,50 L60,40Z" fill={r.c1} {...st} />
      <path d="M-14,14 L14,14 L22,40 L10,200 L0,220 L-10,200 L-22,40Z" fill={r.c2} {...st} />
    </g>;
  }
};

export const RiderFigure: React.FC<{r: Rider; e: Emotion}> = ({r, e}) => {
  const sh = e.shock;
  const jaw = r.jaw === 'round' ? 'M-98,-150 Q-102,-234 0,-236 Q102,-234 98,-150 L96,-100 Q84,-22 0,-18 Q-84,-22 -96,-100Z'
    : r.jaw === 'narrow' ? 'M-86,-150 Q-90,-232 0,-234 Q90,-232 86,-150 L82,-96 Q66,-28 0,-22 Q-66,-28 -82,-96Z'
    : 'M-92,-150 Q-96,-230 0,-232 Q96,-230 92,-150 L88,-96 Q74,-30 0,-26 Q-74,-30 -88,-96Z';
  const eye = (cx: number) => {
    const open = clamp(1 - e.blink * (1 - sh));
    if (e.smile > 0.5 && sh < 0.1 && e.mouth === 0 && r.hair === 'perm')
      return <path d={`M${cx - 16},-118 Q${cx},-134 ${cx + 16},-118`} fill="none" stroke={P.ink} strokeWidth={6} strokeLinecap="round" />;
    const rx = 17 + sh * 7, ry = (17 + sh * 9) * open + 1.5;
    return (
      <g>
        <ellipse cx={cx} cy={-122} rx={rx} ry={ry} fill="#FFFBF2" stroke={P.ink} strokeWidth={5} />
        <circle cx={cx + e.look[0] * 6} cy={-121 + e.look[1] * 5} r={lerp(8, 5, sh)} fill={P.ink} />
        <circle cx={cx + e.look[0] * 6 + 2.5} cy={-124 + e.look[1] * 5} r={2.2} fill="#fff" />
        {r.lashes && <path d={`M${cx - rx},${-122 - ry * 0.4} l-8,-6 M${cx - rx * 0.4},${-122 - ry} l-3,-9 M${cx + rx * 0.4},${-122 - ry} l3,-9`} stroke={P.ink} strokeWidth={4} strokeLinecap="round" />}
      </g>
    );
  };
  const by = -158 - sh * 22 - e.worry * 8;
  const browC = r.hair === 'bald' ? '#E8E2DA' : r.hairColor;
  const mouth = () => {
    const lip = r.lips ? '#B5473E' : P.ink;
    if (e.mouth === 0) return <path d={`M-18,-64 Q0,${-64 + e.smile * 12 - e.worry * 8} 18,-64`} fill="none" stroke={lip} strokeWidth={r.lips ? 8 : 6} strokeLinecap="round" />;
    const W = [0, 15, 20, 18][e.mouth] + sh * 4, H = [0, 7, 14, 20][e.mouth] + sh * 8;
    return <g>
      <ellipse cx={0} cy={-64 + H * 0.4} rx={W} ry={H} fill="#5A1F1A" stroke={lip} strokeWidth={r.lips ? 7 : 5} />
      <ellipse cx={1} cy={-64 + H * 0.85} rx={W * 0.5} ry={H * 0.35} fill="#C9665A" />
    </g>;
  };
  return (
    <g>
      <g transform={`scale(${r.bodyScale})`}>
        <rect x={-36} y={-60} width={72} height={70} fill={r.shade} stroke={P.ink} strokeWidth={O} />
        <Clothes r={r} />
        {r.beads && <g>{Array.from({length: 11}, (_, i) => { const a = Math.PI * (0.15 + 0.7 * i / 10); return <circle key={i} cx={Math.cos(a) * 70} cy={-6 + Math.sin(a) * 70} r={9} fill="#F3EDE4" stroke={P.ink} strokeWidth={3} />; })}</g>}
      </g>
      <g transform={`scale(${r.headScale})`}>
        <Hair r={r} back />
        {[-1, 1].map((s) => <ellipse key={s} cx={s * 94} cy={-112} rx={18} ry={26} fill={r.skin} stroke={P.ink} strokeWidth={O} />)}
        {r.earrings && [-1, 1].map((s) => <circle key={s} cx={s * 96} cy={-80} r={9} fill={P.gold} stroke={P.ink} strokeWidth={4} />)}
        <path d={jaw} fill={r.skin} stroke={P.ink} strokeWidth={O} strokeLinejoin="round" />
        {r.beard && <path d="M-88,-110 Q-80,-10 0,0 Q80,-10 88,-110 Q60,-60 30,-80 Q0,-70 -30,-80 Q-60,-60 -88,-110Z" fill="#E8E2DA" stroke={P.ink} strokeWidth={O} strokeLinejoin="round" />}
        {[-1, 1].map((s) => <ellipse key={s} cx={s * 52} cy={-82} rx={16} ry={9} fill={P.terracotta} opacity={0.25 + e.worry * 0.2} />)}
        {r.freckles && [-1, 1].map((s) => [0, 1, 2].map((i) => <circle key={s + '' + i} cx={s * (40 + i * 10)} cy={-92 + (i % 2) * 6} r={3} fill="#A8643F" />))}
        {r.wrinkles && <path d="M-60,-176 q20,-6 40,0 M20,-176 q20,-6 40,0 M-74,-110 l-12,6 M74,-110 l12,6" fill="none" stroke={r.shade} strokeWidth={4} strokeLinecap="round" />}
        <Hair r={r} />
        {eye(-36)}{eye(36)}
        {r.glasses && <g fill="none" stroke={P.ink} strokeWidth={6}><circle cx={-36} cy={-122} r={30} /><circle cx={36} cy={-122} r={30} /><path d="M-6,-124 Q0,-130 6,-124 M-66,-126 L-92,-134 M66,-126 L92,-134" /></g>}
        <path d={`M-58,${by + 8 + e.worry * 6} Q-36,${by - 6} -16,${by + 4 - e.worry * 6}`} fill="none" stroke={browC} strokeWidth={8} strokeLinecap="round" />
        <path d={`M16,${by + 4 - e.worry * 6} Q36,${by - 6} 58,${by + 8 + e.worry * 6}`} fill="none" stroke={browC} strokeWidth={8} strokeLinecap="round" />
        <path d="M-4,-112 Q-12,-90 -2,-84 Q6,-82 10,-88" fill="none" stroke={r.shade} strokeWidth={5} strokeLinecap="round" />
        {mouth()}
        {r.headphones && <g><path d="M-104,-120 Q-110,-280 0,-282 Q110,-280 104,-120" fill="none" stroke={P.ink} strokeWidth={20} /><path d="M-104,-120 Q-110,-280 0,-282 Q110,-280 104,-120" fill="none" stroke="#E9E4DA" strokeWidth={10} />{[-1, 1].map((s) => <rect key={s} x={s * 108 - 20} y={-150} width={40} height={64} rx={16} fill="#E9E4DA" stroke={P.ink} strokeWidth={6} />)}</g>}
        {e.sweat > 0.01 && <path transform={`translate(86,${-190 + e.sweat * 40}) scale(${e.sweat})`} d="M0,-18 Q12,0 8,8 Q0,16 -8,8 Q-12,0 0,-18Z" fill="#BFE0F2" stroke={P.ink} strokeWidth={4} />}
      </g>
    </g>
  );
};

export const RIDERS: Rider[] = [
  {name: 'Молодой пацан', skin: '#E7B996', shade: '#CC9A78', headScale: 1, bodyScale: 1, jaw: 'soft', hair: 'messy', hairColor: '#5A3B28', clothes: 'hoodie', c1: '#8FA57E', c2: '#738A64'},
  {name: 'Тётя Люда, 60', skin: '#EBC3A4', shade: '#D2A486', headScale: 1, bodyScale: 1.08, jaw: 'round', hair: 'perm', hairColor: '#B7A7C4', clothes: 'cardigan', c1: '#B5677A', c2: '#8E4A5C', glasses: true, earrings: true, beads: true, lips: true, wrinkles: true},
  {name: 'Школьник, 10', skin: '#F0C6A2', shade: '#D8A783', headScale: 1.12, bodyScale: 0.72, jaw: 'round', hair: 'cowlick', hairColor: '#C07A3A', clothes: 'schoolkid', c1: '#5E7FA0', c2: '#C8553D', freckles: true},
  {name: 'Студентка', skin: '#E9BC9A', shade: '#CF9E7C', headScale: 0.97, bodyScale: 0.92, jaw: 'narrow', hair: 'ponytail', hairColor: '#3B2A22', clothes: 'sweater', c1: '#E3B04B', c2: '#C8553D', headphones: true, lashes: true, lips: true},
  {name: 'Дед Михалыч', skin: '#E2B394', shade: '#C69477', headScale: 1, bodyScale: 1.05, jaw: 'soft', hair: 'bald', hairColor: '#E8E2DA', clothes: 'jacket', c1: '#6B6A55', c2: '#55543F', beard: true, glasses: true, wrinkles: true},
  {name: 'Офисный клерк', skin: '#E4B592', shade: '#C99673', headScale: 0.98, bodyScale: 1, jaw: 'narrow', hair: 'sidepart', hairColor: '#2E2420', clothes: 'shirtTie', c1: '#DCE3E8', c2: '#3E5A78', glasses: true},
];
