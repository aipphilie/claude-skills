import React from 'react';
import {P} from '../palette';
import {Ashot, AshotEyes, AshotState} from '../characters/Ashot';
import {RiderFigure, Rider, Emotion, EMO, RIDERS} from '../characters/Rider';
import {City, Buildings, CabinBack} from '../scene/Cabin';

// Сцены-ракурсы сериала. Каждая рисует кадр 1080×1920 и принимает t (сек от начала плана).
// Используются и в раскадровке (Storyboard.tsx), и в ролике.

const F = 'Rubik';
export const A0: AshotState = {t: 0, turn: 1, browL: 0, browR: 0.15, blink: 0, wink: 0, mouth: 0, smirk: 1, look: [0.55, -0.1], arm: {from: 'rest', to: 'rest', k: 1}};
const TAXI = '#E9B23F', TAXI_D = '#C48F27';

export const Sub: React.FC<{text: string; keys?: string[]}> = ({text, keys = []}) => {
  const lines: string[][] = [[]];
  for (const w of text.split(' ')) {
    const cur = lines[lines.length - 1];
    if (cur.length && (cur.join(' ') + ' ' + w).length > 15) lines.push([w]); else cur.push(w);
  }
  return (
    <g>
      {lines.map((ws, j) => (
        <text key={j} x={540} y={1440 + j * 100 - (lines.length - 1) * 50} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={84}>
          {ws.map((w, i) => (
            <tspan key={i} dx={i ? 24 : 0} fill={keys.includes(w) ? P.mustard : P.cream} stroke={P.ink} strokeWidth={16} paintOrder="stroke" strokeLinejoin="round">{w.toUpperCase()}</tspan>
          ))}
        </text>
      ))}
    </g>
  );
};
const Lines: React.FC<{x: number; y: number; n?: number; len?: number; dir?: number}> = ({x, y, n = 5, len = 220, dir = -1}) => (
  <g stroke={P.cream} strokeWidth={10} strokeLinecap="round" opacity={0.7}>
    {Array.from({length: n}, (_, i) => <path key={i} d={`M${x},${y + i * 40} l${dir * (len - i * 30)},0`} />)}
  </g>
);

// ---------- Машина снаружи (вид сбоку, едет вправо)
export const TaxiSide: React.FC<{t?: number}> = ({t = 0}) => (
  <g>
    <ellipse cx={0} cy={10} rx={420} ry={26} fill="#000" opacity={0.35} />
    <path d="M-390,-10 L-392,-120 Q-384,-160 -310,-168 L-190,-178 L-120,-268 Q-96,-292 -40,-294 L150,-294 Q206,-292 236,-262 L306,-178 L370,-168 Q402,-156 402,-116 L402,-10Z" fill={TAXI} stroke={P.ink} strokeWidth={10} strokeLinejoin="round" />
    <path d="M-104,-180 L-50,-262 Q-40,-272 -10,-272 L40,-272 L40,-180Z" fill="#2C2840" stroke={P.ink} strokeWidth={8} />
    <path d="M62,-180 L62,-272 L140,-272 Q176,-270 196,-246 L250,-180Z" fill="#2C2840" stroke={P.ink} strokeWidth={8} />
    {/* силуэт Ашота в кепке */}
    <path d="M120,-180 L120,-236 Q130,-262 162,-258 Q188,-254 190,-232 L192,-180Z" fill="#1C1A26" />
    <path d="M110,-240 Q150,-276 196,-244Z" fill="#1C1A26" />
    {/* шашечки */}
    {Array.from({length: 14}, (_, i) => <rect key={i} x={-330 + i * 46} y={-132 + (i % 2) * 20} width={23} height={20} fill={P.ink} />)}
    <path d="M-392,-90 L402,-90" stroke={TAXI_D} strokeWidth={6} />
    <rect x={-10} y={-336} width={130} height={42} rx={10} fill={P.cream} stroke={P.ink} strokeWidth={7} />
    <text x={55} y={-305} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={30} fill={P.ink}>ТАКСИ</text>
    <rect x={378} y={-150} width={28} height={32} rx={8} fill="#FFF1C8" stroke={P.ink} strokeWidth={6} />
    <rect x={-398} y={-150} width={20} height={30} rx={6} fill="#E0523E" stroke={P.ink} strokeWidth={6} />
    {[-250, 255].map((x) => (
      <g key={x} transform={`translate(${x},-10) rotate(${t * 900})`}>
        <circle r={74} fill="#242024" stroke={P.ink} strokeWidth={10} />
        <circle r={36} fill="#9A938C" stroke={P.ink} strokeWidth={7} />
        <path d="M-30,0 L30,0 M0,-30 L0,30" stroke={P.ink} strokeWidth={6} />
      </g>
    ))}
    {/* свет фар */}
    <path d="M406,-134 L900,-230 L900,-30Z" fill="#FFE7A8" opacity={0.25} />
  </g>
);

const NightStreet: React.FC<{t: number}> = ({t}) => (
  <g>
    <rect width={1080} height={1920} fill={P.sky1} />
    <g transform="translate(-100,-60) scale(1.2,1.6)"><City t={t} /></g>
    <rect x={0} y={1320} width={1080} height={600} fill="#2A2430" />
    <path d="M0,1320 L1080,1320" stroke="#4A4050" strokeWidth={14} />
    {Array.from({length: 6}, (_, i) => <rect key={i} x={((i * 260 - t * 900) % 1560 + 1560) % 1560 - 240} y={1560} width={140} height={18} rx={9} fill={P.mustard} opacity={0.7} />)}
  </g>
);

// 1. Холодный старт: такси влетает в кадр
export const ShotExterior: React.FC<{t?: number}> = ({t = 0}) => (
  <svg viewBox="0 0 1080 1920">
    <NightStreet t={t} />
    <Lines x={90} y={1060} n={5} len={260} />
    <g transform="translate(520,1440) scale(1.15) rotate(-1.5)"><TaxiSide t={t} /></g>
    <g transform="translate(860,980)"><circle r={42} fill={P.mustard} opacity={0.9} /><text y={14} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={40} fill={P.ink}>⇨</text></g>
  </svg>
);

// 2. Хук: телефон «ипотека одобрена»
export const ShotPhone: React.FC<{rider?: Rider}> = ({rider = RIDERS[0]}) => (
  <svg viewBox="0 0 1080 1920">
    <g transform="translate(-260,-420) scale(1.5)"><CabinBack t={0} /></g>
    <g transform="translate(540,1300) scale(1.9)"><RiderFigure r={rider} e={{...EMO.talk, smile: 0.8, look: [0, 0.4]}} /></g>
    <g transform="translate(560,860) rotate(-8)">
      <rect x={-210} y={-380} width={420} height={760} rx={56} fill="#1D1A1F" stroke={P.ink} strokeWidth={12} />
      <rect x={-184} y={-344} width={368} height={688} rx={38} fill={P.cream} />
      <circle cx={0} cy={-150} r={86} fill={P.sage} stroke={P.ink} strokeWidth={8} />
      <path d="M-40,-150 L-8,-116 L46,-186" fill="none" stroke={P.cream} strokeWidth={20} strokeLinecap="round" strokeLinejoin="round" />
      <text y={-10} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={50} fill={P.ink}>ИПОТЕКА</text>
      <text y={50} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={50} fill={P.sageDark}>ОДОБРЕНА</text>
      <rect x={-150} y={100} width={300} height={90} rx={20} fill={P.beige} stroke={P.ink} strokeWidth={5} />
      <text y={160} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={46} fill={P.ink}>5 000 000 ₽</text>
      <rect x={-150} y={230} width={300} height={70} rx={35} fill={P.mustard} stroke={P.ink} strokeWidth={5} />
      <text y={276} textAnchor="middle" fontFamily={F} fontWeight={800} fontSize={32} fill={P.ink}>ПОДПИСАТЬ</text>
      {/* пальцы пассажира */}
      {[0, 1, 2].map((i) => <rect key={i} x={196} y={-60 + i * 70} width={70} height={52} rx={26} fill={rider.skin} stroke={P.ink} strokeWidth={7} />)}
      <rect x={-262} y={40} width={80} height={56} rx={28} fill={rider.skin} stroke={P.ink} strokeWidth={7} />
    </g>
    {Array.from({length: 22}, (_, i) => {
      const x = (i * 137) % 1000 + 40, y = 300 + ((i * 251) % 900);
      return <rect key={i} x={x} y={y} width={22} height={12} rx={3} fill={[P.mustard, P.terracotta, P.sage, P.cream][i % 4]} transform={`rotate(${i * 37} ${x} ${y})`} />;
    })}
    <Sub text="Брат, ипотеку взял" />
  </svg>
);

// затылок Ашота (вид сзади)
const AshotBack: React.FC = () => (
  <g>
    <path d="M-170,140 Q-200,0 -120,-30 L120,-30 Q200,0 170,140 L240,700 L-240,700Z" fill={P.shirt} stroke={P.ink} strokeWidth={10} />
    <rect x={-80} y={-90} width={160} height={90} fill={P.skinShade} stroke={P.ink} strokeWidth={9} />
    <ellipse cx={0} cy={-200} rx={150} ry={150} fill={P.hairGray} stroke={P.ink} strokeWidth={10} />
    <path d="M-120,-140 q40,30 0,60 M110,-140 q-40,30 0,60" fill="none" stroke={P.hairDark} strokeWidth={5} />
    {[-1, 1].map((s) => <ellipse key={s} cx={s * 150} cy={-200} rx={28} ry={42} fill={P.skin} stroke={P.ink} strokeWidth={9} />)}
    <path d="M-176,-230 Q-190,-380 0,-392 Q190,-380 176,-230 Q100,-210 0,-212 Q-100,-210 -176,-230Z" fill={P.cap} stroke={P.ink} strokeWidth={10} />
    {[-100, -40, 30, 90].map((x) => <path key={x} d={`M${x},-216 Q${x * 0.5},-320 0,-384`} fill="none" stroke={P.capDark} strokeWidth={6} />)}
  </g>
);

const RoadAhead: React.FC<{t?: number}> = ({t = 0}) => (
  <g>
    <rect width={1080} height={1100} fill={P.sky1} />
    <g transform="translate(0,-120) scale(1,1.2)"><Buildings t={t} speed={0} seed={44} color={P.bld1} base={900} hMin={150} hMax={380} winOp={0.7} /></g>
    <path d="M0,980 L1080,980 L1080,1100 L0,1100Z" fill="#2A2430" />
    <g filter="url(#blur8)">
      {[[300, 940, '#E0523E'], [380, 940, '#E0523E'], [700, 930, '#FFD9A0'], [820, 950, '#FFB760'], [160, 900, P.lamp]].map(([x, y, c], i) => <circle key={i} cx={x as number} cy={y as number} r={20} fill={c as string} />)}
    </g>
  </g>
);

// 3 / 13. Зеркало глазами пассажира: в нём глаза Ашота
export const ShotMirror: React.FC<{wink?: number; brow?: number}> = ({wink = 0, brow = 0.9}) => (
  <svg viewBox="0 0 1080 1920">
    <defs><filter id="blur8"><feGaussianBlur stdDeviation="8" /></filter></defs>
    <RoadAhead />
    <rect y={1100} width={1080} height={820} fill={P.cabin} />
    <path d="M0,0 L1080,0 L1080,240 Q540,190 0,240Z" fill={P.cabinMid} />
    <rect x={526} y={160} width={28} height={380} fill="#2A2220" stroke={P.ink} strokeWidth={6} />
    <g transform="translate(540,720)">
      <rect x={-420} y={-180} width={840} height={360} rx={110} fill="#241C1A" stroke={P.ink} strokeWidth={14} />
      <clipPath id="mclip"><rect x={-394} y={-154} width={788} height={308} rx={90} /></clipPath>
      <g clipPath="url(#mclip)">
        <rect x={-400} y={-160} width={800} height={320} fill={P.skin} />
        <path d="M-400,-160 L400,-160 L400,-110 Q0,-80 -400,-110Z" fill={P.capDark} />
        <g transform="translate(0,600) scale(2.4)">
          <AshotEyes s={{...A0, browL: brow, browR: 0.2 + wink * 0.3, wink, look: [0.2, 0.5]}} dx={0} />
        </g>
        <path d="M-30,60 Q-40,130 -60,160 L60,160 Q40,130 30,60Z" fill={P.skinShade} stroke={P.ink} strokeWidth={8} />
        <path d="M-380,-150 L-260,-150 L-380,150Z" fill="#fff" opacity={0.15} />
      </g>
    </g>
    <g transform="translate(290,1560) scale(1.1)"><AshotBack /></g>
    <Sub text={wink ? 'Запомнил?' : 'пять лямов. Норм же?'} keys={['пять', 'лямов.']} />
  </svg>
);

// салон сбоку: камера на переднем пассажирском сиденье, Ашот лицом к дороге (вправо)
const SideCabin: React.FC<{t?: number}> = ({t = 0}) => (
  <g>
    <rect width={1080} height={1920} fill={P.cabin} />
    <clipPath id="sidewin"><path d="M-20,420 L640,380 Q700,380 720,440 L760,1000 L-20,1040Z" /></clipPath>
    <g clipPath="url(#sidewin)"><g transform="translate(-140,-20) scale(1.1)"><City t={t} /></g></g>
    <path d="M-20,420 L640,380 Q700,380 720,440 L760,1000 L-20,1040" fill="none" stroke={P.ink} strokeWidth={14} />
    <path d="M760,300 L1100,240 L1100,1120 L800,1060Z" fill="#2B2440" stroke={P.ink} strokeWidth={14} />
    <g filter="url(#blur8)">{[[900, 820, '#E0523E'], [980, 780, P.lamp], [870, 700, '#FFD9A0']].map(([x, y, c], i) => <circle key={i} cx={x as number} cy={y as number} r={24} fill={c as string} />)}</g>
    <path d="M720,300 L800,1080 L760,1100 L680,320Z" fill={P.cabinLight} stroke={P.ink} strokeWidth={8} />
    <path d="M-20,1040 L1100,1100 L1100,1920 L-20,1920Z" fill={P.cabinMid} />
    <rect x={40} y={760} width={250} height={900} rx={60} fill={P.seatDark} stroke={P.ink} strokeWidth={10} />
    <rect x={70} y={600} width={200} height={190} rx={60} fill={P.seatDark} stroke={P.ink} strokeWidth={10} />
  </g>
);
const SideWheel = () => (
  <g transform="translate(860,1380)">
    <ellipse rx={70} ry={250} fill="none" stroke={P.ink} strokeWidth={54} />
    <ellipse rx={70} ry={250} fill="none" stroke="#3E3532" strokeWidth={36} />
    <path d="M60,0 L240,80" stroke={P.ink} strokeWidth={50} />
  </g>
);

// 4 / 7. Ашот за рулём, вид с пассажирского сиденья
export const ShotSide: React.FC<{turn?: number; arm?: 'rest' | 'up'; mouth?: number; text: string; keys?: string[]; whoosh?: boolean}> = ({turn = 0.3, arm = 'rest', mouth = 2, text, keys, whoosh}) => (
  <svg viewBox="0 0 1080 1920">
    <defs><filter id="blur8"><feGaussianBlur stdDeviation="8" /></filter></defs>
    <SideCabin />
    <g transform="translate(470,1180) scale(-1.15,1.15)">
      <Ashot s={{...A0, turn, mouth, smirk: 1, look: turn > 0.5 ? [0.7, 0] : [-0.8, -0.2], arm: {from: arm, to: arm, k: 1}}} />
    </g>
    <SideWheel />
    {whoosh && <g opacity={0.8}>{[0, 1, 2].map((i) => <path key={i} d={`M${200 + i * 30},${520 + i * 60} q-120,80 -60,200`} fill="none" stroke={P.cream} strokeWidth={12} strokeLinecap="round" />)}</g>}
    <Sub text={text} keys={keys} />
  </svg>
);

// 5 / 12. Таксометр крупно
export const ShotMeter: React.FC<{mode: 'crazy' | 'rewind' | 'fare'}> = ({mode}) => {
  const val = mode === 'crazy' ? '12 000 000' : mode === 'rewind' ? '− − − − −' : '400';
  return (
    <svg viewBox="0 0 1080 1920">
      <rect width={1080} height={1920} fill="#231B18" />
      <path d="M-50,1300 Q540,1200 1130,1300 L1130,1920 L-50,1920Z" fill="#2E2420" stroke={P.ink} strokeWidth={10} />
      <g transform={`translate(540,880) rotate(${mode === 'crazy' ? -4 : 0})`}>
        <rect x={-470} y={-300} width={940} height={600} rx={60} fill="#1E1816" stroke={P.ink} strokeWidth={14} />
        <text x={-400} y={-200} fontFamily={F} fontWeight={800} fontSize={46} fill="#8A7A70">ТАКСОМЕТР</text>
        <circle cx={380} cy={-214} r={22} fill={mode === 'crazy' ? '#E0523E' : P.sage} />
        <rect x={-420} y={-140} width={840} height={300} rx={30} fill="#3A1F14" />
        <text x={0} y={70} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={mode === 'fare' ? 220 : 140} fill={mode === 'rewind' ? '#9FD18A' : '#FF9A4A'}>{val} ₽</text>
        <text x={0} y={240} textAnchor="middle" fontFamily={F} fontWeight={800} fontSize={44} fill={P.cream}>{mode === 'fare' ? 'ПОЕЗДКА' : mode === 'crazy' ? 'ПЕРЕПЛАТА БАНКУ' : 'ПЕРЕПЛАТА ↓'}</text>
      </g>
      {mode === 'crazy' && <>
        {[[-300, -380], [120, -420], [380, -360]].map(([x, y], i) => <circle key={i} cx={540 + x} cy={880 + y} r={70 + i * 20} fill="#8C8079" opacity={0.6} />)}
        {Array.from({length: 8}, (_, i) => <path key={i} d={`M${540 + Math.cos(i) * 500},${880 + Math.sin(i) * 340} l${Math.cos(i) * 60},${Math.sin(i) * 60}`} stroke={P.mustard} strokeWidth={12} strokeLinecap="round" />)}
        <Sub text="Отдашь больше двенадцати" keys={['двенадцати']} />
      </>}
      {mode === 'rewind' && <>
        {Array.from({length: 6}, (_, i) => (
          <g key={i} transform={`translate(${200 + i * 140},${1230 - (i % 3) * 60})`}>
            <circle r={40} fill={P.gold} stroke={P.ink} strokeWidth={6} />
            <text y={14} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={40} fill={P.goldDark}>₽</text>
            <path d="M0,60 l0,90" stroke={P.cream} strokeWidth={8} strokeLinecap="round" opacity={0.6} />
          </g>
        ))}
        <path d="M800,520 a120,120 0 1 1 -60,-100" fill="none" stroke={P.sage} strokeWidth={22} strokeLinecap="round" />
        <path d="M740,380 l0,60 l60,-10" fill="none" stroke={P.sage} strokeWidth={22} strokeLinecap="round" strokeLinejoin="round" />
        <Sub text="Так переплатишь меньше" keys={['меньше']} />
      </>}
    </svg>
  );
};

// 6 / 15. Через лобовое стекло снаружи
export const ShotWindshield: React.FC<{shock?: number; freeze?: boolean; text: string; keys?: string[]}> = ({shock = 1, freeze, text, keys}) => (
  <svg viewBox="0 0 1080 1920">
    <defs><filter id="blur8"><feGaussianBlur stdDeviation="8" /></filter></defs>
    <rect width={1080} height={1920} fill={P.sky1} />
    <g filter="url(#blur8)">{Array.from({length: 10}, (_, i) => <circle key={i} cx={(i * 211) % 1080} cy={200 + (i * 97) % 400} r={30} fill={[P.lamp, '#FFD9A0', '#E0523E'][i % 3]} opacity={0.6} />)}</g>
    <path d="M60,500 Q540,400 1020,500 L1080,1500 L0,1500Z" fill={TAXI} stroke={P.ink} strokeWidth={12} />
    <rect x={460} y={400} width={160} height={54} rx={12} fill={P.cream} stroke={P.ink} strokeWidth={8} />
    <text x={540} y={442} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={36} fill={P.ink}>ТАКСИ</text>
    <clipPath id="wsh"><path d="M140,560 Q540,490 940,560 L1010,1440 L70,1440Z" /></clipPath>
    <g clipPath="url(#wsh)">
      <rect width={1080} height={1920} fill={P.cabin} />
      <clipPath id="rw"><path d="M240,640 L840,640 L860,900 L220,900Z" /></clipPath>
      <g clipPath="url(#rw)"><g transform="translate(-40,180) scale(1.1,0.75)"><City t={0} /></g></g>
      <path d="M150,860 L930,860 L960,1500 L120,1500Z" fill={P.seat} stroke={P.ink} strokeWidth={10} />
      <g transform="translate(400,1150) scale(1.35)"><RiderFigure r={RIDERS[0]} e={{...EMO.shock, shock, mouth: freeze ? 0 : 3}} /></g>
      <g transform="translate(790,1380) scale(1.05)"><Ashot s={{...A0, turn: 0.75, smirk: 1, look: [-0.5, 0], arm: {from: freeze ? 'palm' : 'rest', to: freeze ? 'palm' : 'rest', k: 1}}} /></g>
      <g transform="translate(790,1500) rotate(4)">
        <ellipse rx={200} ry={70} fill="none" stroke={P.ink} strokeWidth={46} />
        <ellipse rx={200} ry={70} fill="none" stroke="#3E3532" strokeWidth={30} />
      </g>
      <path d="M200,560 L340,560 L160,1440 L60,1440Z" fill="#fff" opacity={0.1} />
      <path d="M760,540 L820,540 L700,1440 L660,1440Z" fill="#fff" opacity={0.08} />
    </g>
    <path d="M140,560 Q540,490 940,560 L1010,1440 L70,1440Z" fill="none" stroke={P.ink} strokeWidth={16} />
    <path d="M-20,1440 L1100,1440 L1100,1920 L-20,1920Z" fill={TAXI} stroke={P.ink} strokeWidth={12} />
    <path d="M140,1440 Q330,1460 520,1430 M560,1430 Q750,1460 940,1440" stroke={P.ink} strokeWidth={14} fill="none" strokeLinecap="round" />
    {freeze && <rect x={18} y={18} width={1044} height={1884} fill="none" stroke={P.cream} strokeWidth={24} />}
    <Sub text={text} keys={keys} />
  </svg>
);

// 8. Пассажир стареет на заднем сиденье
const AGES: Rider[] = [
  RIDERS[0],
  {...RIDERS[0], name: '35', hair: 'sidepart', hairColor: '#6A5446', clothes: 'shirtTie', c1: '#C9C2B4', c2: '#6B5A4A', glasses: true, wrinkles: true, bodyScale: 1.12},
  {...RIDERS[4], name: '60'},
];
export const ShotAging: React.FC = () => (
  <svg viewBox="0 0 1080 1920">
    <g transform="translate(-200,-300) scale(1.4)"><CabinBack t={0} /></g>
    {/* снег за окном — прошли годы */}
    {Array.from({length: 40}, (_, i) => <circle key={i} cx={(i * 173) % 1080} cy={360 + (i * 89) % 560} r={6 + (i % 3) * 3} fill="#fff" opacity={0.8} />)}
    <g transform="translate(540,1270) scale(1.8)"><RiderFigure r={AGES[2]} e={EMO.worry} /></g>
    <g transform="translate(540,330)">
      <rect x={-170} y={-110} width={340} height={210} rx={20} fill={P.cream} stroke={P.ink} strokeWidth={9} />
      <rect x={-170} y={-110} width={340} height={60} rx={20} fill={P.terracotta} stroke={P.ink} strokeWidth={9} />
      {[-110, -40, 40, 110].map((x) => <rect key={x} x={x - 8} y={-130} width={16} height={46} rx={8} fill={P.ink} />)}
      <text y={70} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={110} fill={P.ink}>2046</text>
      <path d="M-150,40 Q-40,-80 150,-30" fill="none" stroke={P.cream} strokeWidth={6} opacity={0.6} />
    </g>
    {/* полоска: 3 склейки */}
    <g transform="translate(540,600)">
      {AGES.map((r, i) => (
        <g key={i} transform={`translate(${(i - 1) * 260},0)`}>
          <circle r={105} fill={P.beige} stroke={P.ink} strokeWidth={7} opacity={0.95} />
          <clipPath id={`age${i}`}><circle r={100} /></clipPath>
          <g clipPath={`url(#age${i})`}><g transform="translate(0,120) scale(0.75)"><RiderFigure r={r} e={EMO.worry} /></g></g>
          <text y={150} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={42} fill={P.cream} stroke={P.ink} strokeWidth={10} paintOrder="stroke">{['2026', '2036', '2046'][i]}</text>
          {i < 2 && <path d="M120,0 l30,0 M140,-12 l12,12 l-12,12" stroke={P.cream} strokeWidth={8} fill="none" strokeLinecap="round" />}
        </g>
      ))}
    </g>
    <Sub text="а двадцать лет твоей жизни" keys={['двадцать', 'лет']} />
  </svg>
);

// карта навигатора
const NavMap: React.FC<{pick?: boolean; big?: boolean}> = ({pick, big}) => (
  <g>
    <rect x={-480} y={-560} width={960} height={1120} fill="#EFE6D4" />
    {Array.from({length: 12}, (_, i) => <path key={i} d={`M${-480 + i * 90},-560 L${-480 + i * 90 + 40},560`} stroke="#DDD1BA" strokeWidth={18} />)}
    {Array.from({length: 12}, (_, i) => <path key={'h' + i} d={`M-480,${-560 + i * 100} L480,${-560 + i * 100 + 30}`} stroke="#DDD1BA" strokeWidth={18} />)}
    {/* длинный маршрут — по пробкам */}
    <path d="M0,420 C-420,380 -460,120 -300,40 C-80,-60 -460,-200 -340,-330 C-240,-440 -120,-420 0,-430" fill="none" stroke={pick ? '#BFB3A2' : P.terracotta} strokeWidth={30} strokeLinecap="round" strokeDasharray={pick ? '0' : '60 30'} />
    {/* короткий маршрут */}
    <path d="M0,420 C160,240 120,-160 0,-430" fill="none" stroke={pick ? P.sage : '#9DB98F'} strokeWidth={pick ? 44 : 30} strokeLinecap="round" />
    {[[-330, 60], [-380, -280], [-230, 190]].map(([x, y], i) => <rect key={i} x={x} y={y} width={40} height={24} rx={6} fill="#E0523E" stroke={P.ink} strokeWidth={4} />)}
    <g transform="translate(0,-470)"><path d="M-60,30 L0,-30 L60,30Z" fill={P.terracotta} stroke={P.ink} strokeWidth={6} /><rect x={-44} y={30} width={88} height={60} fill={P.cream} stroke={P.ink} strokeWidth={6} /></g>
    <g transform="translate(0,440)"><circle r={36} fill={TAXI} stroke={P.ink} strokeWidth={7} /></g>
    {big && <>
      <g transform="translate(-250,-120) rotate(-4)">
        <rect x={-190} y={-70} width={380} height={140} rx={30} fill={pick ? '#D8CFC2' : P.cream} stroke={P.ink} strokeWidth={7} />
        <text y={-12} textAnchor="middle" fontFamily={F} fontWeight={800} fontSize={36} fill={P.ink}>УМЕНЬШИТЬ ПЛАТЁЖ</text>
        <text y={44} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={44} fill={P.terracotta}>20 ЛЕТ</text>
      </g>
      <g transform="translate(250,80) rotate(3)">
        <rect x={-190} y={-70} width={380} height={140} rx={30} fill={pick ? P.sage : P.cream} stroke={P.ink} strokeWidth={7} />
        <text y={-12} textAnchor="middle" fontFamily={F} fontWeight={800} fontSize={36} fill={pick ? P.cream : P.ink}>УМЕНЬШИТЬ СРОК</text>
        <text y={44} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={44} fill={pick ? P.cream : P.sageDark}>БЫСТРЕЕ</text>
      </g>
    </>}
  </g>
);
const PokeHand: React.FC<{x: number; y: number; rot?: number; s?: number}> = ({x, y, rot = -30, s = 1}) => (
  <g transform={`translate(${x},${y}) rotate(${rot}) scale(${s})`}>
    <path d="M-30,60 L-34,500" stroke={P.ink} strokeWidth={112} strokeLinecap="round" />
    <path d="M-30,60 L-34,500" stroke={P.skin} strokeWidth={96} strokeLinecap="round" />
    <path d="M-34,380 L-36,700" stroke={P.ink} strokeWidth={150} />
    <path d="M-34,380 L-36,700" stroke={P.shirt} strokeWidth={134} />
    <rect x={-74} y={-10} width={96} height={110} rx={40} fill={P.skin} stroke={P.ink} strokeWidth={9} />
    <rect x={-16} y={-110} width={38} height={130} rx={19} fill={P.skin} stroke={P.ink} strokeWidth={9} />
    <path d="M-74,40 Q-104,10 -86,-14 Q-66,-20 -56,6" fill={P.skin} stroke={P.ink} strokeWidth={8} />
  </g>
);

// 9. Торпеда: рука Ашота тянется к навигатору
export const ShotDash: React.FC = () => (
  <svg viewBox="0 0 1080 1920">
    <defs><filter id="blur8"><feGaussianBlur stdDeviation="8" /></filter></defs>
    <RoadAhead />
    <path d="M-50,1000 Q540,880 1130,1000 L1130,1920 L-50,1920Z" fill="#2E2420" stroke={P.ink} strokeWidth={12} />
    <g transform="translate(-60,1350) rotate(-10)">
      <ellipse rx={240} ry={110} fill="none" stroke={P.ink} strokeWidth={60} />
      <ellipse rx={240} ry={110} fill="none" stroke="#3E3532" strokeWidth={40} />
    </g>
    <g transform="translate(560,1060)">
      <rect x={-300} y={-210} width={600} height={420} rx={40} fill="#1D1A1F" stroke={P.ink} strokeWidth={12} />
      <clipPath id="navs"><rect x={-270} y={-180} width={540} height={360} rx={24} /></clipPath>
      <g clipPath="url(#navs)"><g transform="scale(0.55) rotate(-90)"><NavMap /></g></g>
      <rect x={-30} y={210} width={60} height={110} fill="#1D1A1F" stroke={P.ink} strokeWidth={8} />
    </g>
    <PokeHand x={620} y={1120} rot={-20} s={1.1} />
    <Sub text="Гаси досрочно" keys={['досрочно']} />
  </svg>
);

// 10. Экран навигатора: два маршрута
export const ShotNav: React.FC<{pick?: boolean}> = ({pick = true}) => (
  <svg viewBox="0 0 1080 1920">
    <rect width={1080} height={1920} fill="#1D1A1F" />
    <g transform="translate(540,880)">
      <clipPath id="navb"><rect x={-480} y={-560} width={960} height={1120} rx={40} /></clipPath>
      <g clipPath="url(#navb)"><NavMap pick={pick} big /></g>
      <rect x={-480} y={-560} width={960} height={1120} rx={40} fill="none" stroke={P.ink} strokeWidth={14} />
    </g>
    <PokeHand x={680} y={990} rot={-25} />
    <Sub text="уменьшай срок, а не платёж" keys={['срок,']} />
  </svg>
);

// 11. Сверху: такси сворачивает на короткую дорогу
export const ShotTopDown: React.FC = () => (
  <svg viewBox="0 0 1080 1920">
    <rect width={1080} height={1920} fill="#3A3346" />
    {Array.from({length: 30}, (_, i) => <rect key={i} x={(i % 5) * 230 - 40} y={Math.floor(i / 5) * 330 - 60} width={170} height={250} rx={20} fill="#4A4258" />)}
    {Array.from({length: 30}, (_, i) => <rect key={'w' + i} x={(i % 5) * 230 + 10} y={Math.floor(i / 5) * 330 - 20} width={30} height={30} rx={6} fill={P.win} opacity={0.5} />)}
    <path d="M540,1950 L540,1250 C540,1100 120,1100 120,800 C120,450 520,600 470,300 L470,-40" fill="none" stroke="#5E566A" strokeWidth={150} />
    <path d="M540,1250 C700,1100 760,700 470,300" fill="none" stroke="#5E566A" strokeWidth={150} />
    <path d="M540,1950 L540,1250 C540,1100 120,1100 120,800 C120,450 520,600 470,300" fill="none" stroke={P.terracotta} strokeWidth={14} strokeDasharray="40 30" opacity={0.8} />
    <path d="M540,1250 C700,1100 760,700 470,300" fill="none" stroke={P.sage} strokeWidth={18} strokeDasharray="40 24" />
    {[[140, 900], [160, 760], [230, 1080], [300, 600]].map(([x, y], i) => <rect key={i} x={x - 30} y={y - 50} width={60} height={100} rx={14} fill="#E0523E" stroke={P.ink} strokeWidth={6} />)}
    <g transform="translate(640,1120) rotate(35)">
      <rect x={-45} y={-80} width={90} height={160} rx={22} fill={TAXI} stroke={P.ink} strokeWidth={8} />
      <rect x={-34} y={-50} width={68} height={40} rx={8} fill="#2C2840" />
      <rect x={-24} y={0} width={48} height={22} rx={5} fill={P.cream} stroke={P.ink} strokeWidth={4} />
      <path d="M-30,-82 L-60,-200 L60,-200 L30,-82Z" fill="#FFE7A8" opacity={0.35} />
    </g>
    <Lines x={560} y={1300} n={3} len={160} dir={-1} />
    <g transform="translate(250,470)"><rect x={-170} y={-46} width={340} height={92} rx={46} fill={P.terracotta} stroke={P.ink} strokeWidth={7} /><text y={16} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={42} fill={P.cream}>ПРОБКА 20 ЛЕТ</text></g>
    <g transform="translate(790,700)"><rect x={-150} y={-46} width={300} height={92} rx={46} fill={P.sage} stroke={P.ink} strokeWidth={7} /><text y={16} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={42} fill={P.cream}>КОРОЧЕ</text></g>
    <Sub text="Так переплатишь меньше" keys={['меньше']} />
  </svg>
);

// 14. Глазами пассажира: Ашот тянет руку за деньгами
export const ShotPOV: React.FC = () => (
  <svg viewBox="0 0 1080 1920">
    <defs><filter id="blur8"><feGaussianBlur stdDeviation="8" /></filter></defs>
    <RoadAhead />
    <path d="M-50,1050 Q540,980 1130,1050 L1130,1920 L-50,1920Z" fill="#2E2420" />
    <g transform="translate(830,1110)">
      <rect x={-120} y={-50} width={240} height={100} rx={16} fill="#1E1816" stroke={P.ink} strokeWidth={7} />
      <text y={22} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={60} fill="#FF9A4A">400 ₽</text>
    </g>
    <rect x={560} y={1000} width={500} height={920} rx={60} fill={P.seat} stroke={P.ink} strokeWidth={10} />
    <g transform="translate(360,1330) scale(1.05)"><Ashot s={{...A0, turn: 1, mouth: 2, smirk: 1, look: [0.3, 0.1], arm: {from: 'palm', to: 'palm', k: 1}}} /></g>
    {/* ладонь крупно на камеру */}
    <g transform="translate(720,1220) scale(1.9) rotate(-12)">
      <path d="M-58,-6 Q-60,34 -10,40 Q48,42 62,6 L70,-14 Q74,-26 62,-26 L50,-12 Q30,-30 -10,-28 Q-50,-26 -58,-6Z" fill={P.skin} stroke={P.ink} strokeWidth={5} />
      {[-34, -12, 10, 32].map((fx, i) => <path key={i} d={`M${fx},-24 q-4,-26 8,-28 q12,2 8,28`} fill={P.skin} stroke={P.ink} strokeWidth={5} />)}
    </g>
    <Sub text="С тебя четыреста рублей" keys={['четыреста', 'рублей']} />
  </svg>
);
