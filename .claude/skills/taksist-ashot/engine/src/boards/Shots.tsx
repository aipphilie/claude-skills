import React from 'react';
import {P} from '../palette';
import {Ashot, AshotEyes, AshotState} from '../characters/Ashot';
import {RiderFigure, Rider, Emotion, EMO, RIDERS} from '../characters/Rider';
import {City, Buildings, CabinBack, CabinFront, DriverSeat} from '../scene/Cabin';

// Сцены-ракурсы сериала. Каждая рисует кадр 1080×1920 и принимает t (сек от начала плана).
// Используются и в раскадровке (Storyboard.tsx), и в ролике.

const F = 'Rubik';
export const A0: AshotState = {t: 0, turn: 1, browL: 0, browR: 0.15, blink: 0, wink: 0, mouth: 0, smirk: 1, look: [0.55, -0.1], arm: {from: 'rest', to: 'rest', k: 1}};
const TAXI = '#E9B23F', TAXI_D = '#C48F27';

export const SubCtx = React.createContext(true); // в ролике субтитры рисует общий слой, во врезках их выключаем
export const Sub: React.FC<{text: string; keys?: string[]}> = ({text, keys = []}) => {
  if (!React.useContext(SubCtx)) return null;
  const lines: string[][] = [[]];
  for (const w of text.split(' ')) {
    const cur = lines[lines.length - 1];
    if (cur.length && (cur.join(' ') + ' ' + w).length > 22) lines.push([w]); else cur.push(w);
  }
  return (
    <g>
      {lines.map((ws, j) => (
        <text key={j} x={540} y={1440 + j * 62 - (lines.length - 1) * 31} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={50}>
          {ws.map((w, i) => (
            <tspan key={i} dx={i ? 14 : 0} fill={keys.includes(w) ? P.mustard : P.cream} stroke={P.ink} strokeWidth={10} paintOrder="stroke" strokeLinejoin="round">{w.toUpperCase()}</tspan>
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
    <g transform="translate(55,-296)"><Checker w={150} h={46} /></g>
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

export const NightStreet: React.FC<{t: number}> = ({t}) => (
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

// Ашот с заднего сиденья: видно спинку водительского кресла, плечи по бокам от неё, шею и затылок.
// Ремня НЕ видно — он спереди, на груди.
const AshotBack: React.FC = () => (
  <g>
    <path d="M-250,120 Q-250,20 -120,0 L120,0 Q250,20 250,120 L250,400 L-250,400Z" fill={P.shirt} stroke={P.ink} strokeWidth={10} />
    <path d="M-250,120 Q-250,20 -120,0 M120,0 Q250,20 250,120" fill="none" stroke="#6A7890" strokeWidth={8} opacity={0.8} />
    <rect x={-80} y={-90} width={160} height={110} fill={P.skinShade} stroke={P.ink} strokeWidth={9} />
    <path d="M-50,-20 q50,14 100,0" fill="none" stroke="#9C6B4C" strokeWidth={5} />
    <ellipse cx={0} cy={-200} rx={150} ry={150} fill={P.hairGray} stroke={P.ink} strokeWidth={10} />
    <path d="M-120,-140 q40,30 0,60 M110,-140 q-40,30 0,60" fill="none" stroke={P.hairDark} strokeWidth={5} />
    {[-1, 1].map((s) => <ellipse key={s} cx={s * 150} cy={-200} rx={28} ry={42} fill={P.skin} stroke={P.ink} strokeWidth={9} />)}
    <path d="M-176,-230 Q-190,-380 0,-392 Q190,-380 176,-230 Q100,-210 0,-212 Q-100,-210 -176,-230Z" fill={P.cap} stroke={P.ink} strokeWidth={10} />
    {[-100, -40, 30, 90].map((x) => <path key={x} d={`M${x},-216 Q${x * 0.5},-320 0,-384`} fill="none" stroke={P.capDark} strokeWidth={6} />)}
    {/* спинка водительского кресла закрывает спину */}
    <path d="M-200,70 Q-205,20 -150,16 L150,16 Q205,20 200,70 L225,1400 L-225,1400Z" fill={P.seatDark} stroke={P.ink} strokeWidth={10} strokeLinejoin="round" />
    {[-120, -40, 40, 120].map((x) => <path key={x} d={`M${x},60 L${x * 1.08},1380`} stroke="#3A2820" strokeWidth={8} />)}
    <path d="M-200,300 L205,300" stroke="#3A2820" strokeWidth={8} />
    <rect x={150} y={420} width={50} height={80} rx={10} fill="#2A1E19" stroke={P.ink} strokeWidth={6} />
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
const fmt = (n: number) => Math.round(n).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
export const ShotMeter: React.FC<{mode: 'crazy' | 'rewind' | 'fare' | 'refund'; value?: number; label?: string}> = ({mode, value, label}) => {
  const val = value !== undefined ? fmt(value) : mode === 'crazy' ? '12 000 000' : mode === 'rewind' ? '− − − − −' : '400';
  return (
    <svg viewBox="0 0 1080 1920">
      <rect width={1080} height={1920} fill="#231B18" />
      <path d="M-50,1300 Q540,1200 1130,1300 L1130,1920 L-50,1920Z" fill="#2E2420" stroke={P.ink} strokeWidth={10} />
      <g transform={`translate(540,880) rotate(${mode === 'crazy' ? -4 : 0})`}>
        <rect x={-470} y={-300} width={940} height={600} rx={60} fill="#1E1816" stroke={P.ink} strokeWidth={14} />
        <text x={-400} y={-200} fontFamily={F} fontWeight={800} fontSize={46} fill="#8A7A70">ТАКСОМЕТР</text>
        <circle cx={380} cy={-214} r={22} fill={mode === 'crazy' ? '#E0523E' : P.sage} />
        <rect x={-420} y={-140} width={840} height={300} rx={30} fill="#3A1F14" />
        <text x={0} y={70} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={mode === 'fare' ? 220 : val.length > 9 ? 112 : 140} fill={mode === 'rewind' || mode === 'refund' ? '#9FD18A' : '#FF9A4A'}>{mode === 'refund' ? '+' : ''}{val} ₽</text>
        <text x={0} y={240} textAnchor="middle" fontFamily={F} fontWeight={800} fontSize={44} fill={P.cream}>{label || (mode === 'fare' ? 'ПОЕЗДКА' : mode === 'crazy' ? 'ПЕРЕПЛАТА БАНКУ' : 'ПЕРЕПЛАТА ↓')}</text>
      </g>
      {mode === 'crazy' && <>
        {[[-300, -380], [120, -420], [380, -360]].map(([x, y], i) => <circle key={i} cx={540 + x} cy={880 + y} r={70 + i * 20} fill="#8C8079" opacity={0.6} />)}
        {Array.from({length: 8}, (_, i) => <path key={i} d={`M${540 + Math.cos(i) * 500},${880 + Math.sin(i) * 340} l${Math.cos(i) * 60},${Math.sin(i) * 60}`} stroke={P.mustard} strokeWidth={12} strokeLinecap="round" />)}
        <Sub text="Отдашь больше двенадцати" keys={['двенадцати']} />
      </>}
      {mode === 'refund' && <>
        {Array.from({length: 8}, (_, i) => <path key={i} d={`M${540 + Math.cos(i) * 500},${880 + Math.sin(i) * 340} l${Math.cos(i) * 60},${Math.sin(i) * 60}`} stroke={P.sage} strokeWidth={12} strokeLinecap="round" />)}
        {Array.from({length: 7}, (_, i) => (
          <g key={i} transform={`translate(${170 + i * 125},${1420 - (i % 3) * 60})`}>
            <path d="M0,150 l0,-90" stroke={P.sage} strokeWidth={8} strokeLinecap="round" opacity={0.7} />
            <circle r={40} fill={P.gold} stroke={P.ink} strokeWidth={6} />
            <text y={14} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={40} fill={P.goldDark}>₽</text>
          </g>
        ))}
      </>}
      {mode === 'rewind' && <>
        {Array.from({length: 6}, (_, i) => (
          <g key={i} transform={`translate(${200 + i * 140},${1420 - (i % 3) * 50})`}>
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

const AGES: Rider[] = [
  RIDERS[0],
  {...RIDERS[0], name: '35', hair: 'sidepart', hairColor: '#6A5446', clothes: 'shirtTie', c1: '#C9C2B4', c2: '#6B5A4A', glasses: true, wrinkles: true, bodyScale: 1.12},
  {...RIDERS[4], name: '60'},
];
export const ShotAging: React.FC<{stage?: number; year?: number}> = ({stage = 2, year = 2046}) => (
  <svg viewBox="0 0 1080 1920">
    <g transform="translate(-200,-300) scale(1.4)"><CabinBack t={0} /></g>
    {/* снег за окном — прошли годы */}
    {Array.from({length: 40}, (_, i) => <circle key={i} cx={(i * 173) % 1080} cy={360 + (i * 89) % 560} r={6 + (i % 3) * 3} fill="#fff" opacity={0.8} />)}
    <g transform="translate(540,1270) scale(1.8)"><RiderFigure r={AGES[stage]} e={EMO.worry} /></g>
    <g transform="translate(540,330)">
      <rect x={-170} y={-110} width={340} height={210} rx={20} fill={P.cream} stroke={P.ink} strokeWidth={9} />
      <rect x={-170} y={-110} width={340} height={60} rx={20} fill={P.terracotta} stroke={P.ink} strokeWidth={9} />
      {[-110, -40, 40, 110].map((x) => <rect key={x} x={x - 8} y={-130} width={16} height={46} rx={8} fill={P.ink} />)}
      <text y={70} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={110} fill={P.ink}>{year}</text>
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

// ---------- шашки на крыше (начало координат — низ по центру)
export const Checker: React.FC<{w: number; h: number}> = ({w, h}) => {
  const n = 7, cw = w / n, ch = h / 2;
  return (
    <g>
      <ellipse cx={0} cy={-h / 2} rx={w * 0.75} ry={h * 1.1} fill="#FFE7A8" opacity={0.18} />
      <rect x={-w / 2} y={-h} width={w} height={h} rx={8} fill={P.mustard} />
      {Array.from({length: n * 2}, (_, i) => { const c = i % n, r = Math.floor(i / n); return (c + r) % 2 === 0 ? <rect key={i} x={-w / 2 + c * cw} y={-h + r * ch} width={cw} height={ch} fill={P.ink} /> : null; })}
      <rect x={-w / 2} y={-h} width={w} height={h} rx={8} fill="none" stroke={P.ink} strokeWidth={6} />
      <rect x={-w / 2 + 10} y={-4} width={w - 20} height={10} rx={4} fill="#2A2422" />
    </g>
  );
};

// ---------- торпеда «как у классики» (вид с заднего сиденья, водитель слева)
const Dash2107: React.FC<{fare?: string; wheel?: boolean}> = ({fare = '312', wheel = true}) => (
  <g>
    <path d="M-50,1000 Q540,950 1130,1000 L1130,1920 L-50,1920Z" fill="#1F1B1A" stroke={P.ink} strokeWidth={10} />
    <path d="M-50,1000 Q540,950 1130,1000 L1130,1030 Q540,980 -50,1030Z" fill="#2E2826" />
    {/* щиток приборов под козырьком */}
    <path d="M200,1010 Q390,950 590,1010 L580,1080 L210,1080Z" fill="#141110" stroke={P.ink} strokeWidth={8} />
    {[320, 470].map((x, i) => (
      <g key={x} transform={`translate(${x},1060)`}>
        <circle r={56} fill="#0E0C0B" stroke="#6E6660" strokeWidth={6} />
        {Array.from({length: 9}, (_, k) => { const a = Math.PI * (0.8 + k * 0.175); return <path key={k} d={`M${Math.cos(a) * 40},${Math.sin(a) * 40} L${Math.cos(a) * 50},${Math.sin(a) * 50}`} stroke="#E9E1D2" strokeWidth={4} />; })}
        <path d={`M0,0 L${Math.cos(Math.PI * (1.2 + i * 0.5)) * 42},${Math.sin(Math.PI * (1.2 + i * 0.5)) * 42}`} stroke="#FF9A4A" strokeWidth={6} strokeLinecap="round" />
      </g>
    ))}
    {/* центральная консоль: часы, решётки, магнитола */}
    <rect x={660} y={1040} width={260} height={300} rx={14} fill="#191514" stroke={P.ink} strokeWidth={8} />
    {[0, 1, 2, 3].map((i) => <rect key={i} x={680 + i * 60} y={1060} width={44} height={60} rx={6} fill="#0E0C0B" />)}
    <rect x={690} y={1150} width={200} height={70} rx={8} fill="#0E0C0B" stroke="#6E6660" strokeWidth={4} />
    <text x={790} y={1198} textAnchor="middle" fontFamily={F} fontWeight={800} fontSize={36} fill="#9FD18A">FM 101.7</text>
    <circle cx={790} cy={1280} r={36} fill="#0E0C0B" stroke="#6E6660" strokeWidth={5} />
    <path d="M790,1280 l0,-24 M790,1280 l16,8" stroke="#E9E1D2" strokeWidth={4} strokeLinecap="round" />
    {/* таксометр на торпеде */}
    <g transform="translate(960,990)">
      <rect x={-100} y={-50} width={200} height={84} rx={14} fill="#1E1816" stroke={P.ink} strokeWidth={7} />
      <text y={14} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={46} fill="#FF9A4A">{fare} ₽</text>
    </g>
    {/* тонкий двухспицевый руль */}
    {wheel && <g transform="translate(395,1110)">
      <ellipse rx={270} ry={200} fill="none" stroke={P.ink} strokeWidth={30} />
      <ellipse rx={270} ry={200} fill="none" stroke="#2A2422" strokeWidth={18} />
      <path d="M-60,30 L-250,90 M60,30 L250,90" stroke={P.ink} strokeWidth={34} strokeLinecap="round" />
      <path d="M-60,30 L-250,90 M60,30 L250,90" stroke="#2A2422" strokeWidth={22} strokeLinecap="round" />
      <ellipse cx={0} cy={30} rx={80} ry={56} fill="#2A2422" stroke={P.ink} strokeWidth={8} />
      <circle cx={0} cy={30} r={20} fill="#B9A58C" stroke={P.ink} strokeWidth={5} />
    </g>}
  </g>
);

// 2. Хук: телефон «ипотека одобрена» — кисть с пятью пальцами
export const ShotPhone: React.FC<{rider?: Rider}> = ({rider = RIDERS[0]}) => (
  <svg viewBox="0 0 1080 1920">
    <g transform="translate(-260,-420) scale(1.5)"><CabinBack t={0} /></g>
    <g transform="translate(540,1300) scale(1.9)"><RiderFigure r={rider} e={{...EMO.talk, smile: 0.8, look: [0, 0.4]}} /></g>
    <g transform="translate(560,860) rotate(-8)">
      {/* ладонь за телефоном */}
      <path d="M-150,300 Q-170,420 -40,470 Q120,480 190,380 L200,250 L-140,250Z" fill={rider.skin} stroke={P.ink} strokeWidth={8} />
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
      {/* четыре пальца обхватывают правый край */}
      {[0, 1, 2, 3].map((i) => <rect key={i} x={180} y={-30 + i * 66} width={66 - i * 4} height={56} rx={28} fill={rider.skin} stroke={P.ink} strokeWidth={7} />)}
      {/* большой палец спереди слева */}
      <path d="M-226,200 Q-250,120 -200,90 Q-160,80 -150,130 L-150,240Z" fill={rider.skin} stroke={P.ink} strokeWidth={7} />
    </g>
    {Array.from({length: 22}, (_, i) => {
      const x = (i * 137) % 1000 + 40, y = 300 + ((i * 251) % 900);
      return <rect key={i} x={x} y={y} width={22} height={12} rx={3} fill={[P.mustard, P.terracotta, P.sage, P.cream][i % 4]} transform={`rotate(${i * 37} ${x} ${y})`} />;
    })}
    <Sub text="Брат, ипотеку взял" />
  </svg>
);

// 3 / 13. С заднего сиденья: голова Ашота наполовину перекрывает зеркало, во второй половине — его глаза
export const ShotMirror: React.FC<{wink?: number; brow?: number}> = ({wink = 0, brow = 0.9}) => (
  <svg viewBox="0 0 1080 1920">
    <defs><filter id="blur8"><feGaussianBlur stdDeviation="8" /></filter></defs>
    <RoadAhead />
    <path d="M0,0 L1080,0 L1080,200 Q540,160 0,200Z" fill={P.cabinMid} />
    <path d="M0,180 L90,180 L40,1000 L0,1000Z M1080,180 L990,180 L1040,1000 L1080,1000Z" fill={P.cabinLight} stroke={P.ink} strokeWidth={8} />
    <Dash2107 />
    {/* зеркало */}
    <rect x={608} y={150} width={24} height={150} fill="#2A2220" stroke={P.ink} strokeWidth={6} />
    <g transform="translate(620,420)">
      <rect x={-330} y={-125} width={660} height={250} rx={40} fill="#1E1A19" stroke={P.ink} strokeWidth={12} />
      <clipPath id="mclip2"><rect x={-310} y={-105} width={620} height={210} rx={28} /></clipPath>
      <g clipPath="url(#mclip2)">
        <rect x={-320} y={-110} width={640} height={220} fill="#4A3B36" />
        <g transform="translate(110,0)">
          <rect x={-200} y={-110} width={400} height={220} fill={P.skin} />
          <path d="M-200,-110 L200,-110 L200,-80 Q0,-60 -200,-80Z" fill={P.capDark} />
          <g transform="translate(0,436) scale(2)"><AshotEyes s={{...A0, browL: brow, browR: 0.2 + wink * 0.3, wink, look: [0.25, 0.4]}} dx={0} /></g>
          <path d="M-24,70 Q-34,100 -40,110 L40,110 Q34,100 24,70Z" fill={P.skinShade} stroke={P.ink} strokeWidth={7} />
          {[-1, 1].map((sd) => <path key={sd} d={`M${sd * 200},-110 Q${sd * 170},0 ${sd * 200},110`} fill={P.hairGray} stroke={P.ink} strokeWidth={6} />)}
        </g>
        <path d="M-300,-100 L-220,-100 L-300,100Z" fill="#fff" opacity={0.12} />
      </g>
    </g>
    {/* руки на руле по бокам */}
    {[[120, 1100, -20], [560, 1100, 20]].map(([x, y, r], i) => (
      <g key={i} transform={`translate(${x},${y}) rotate(${r})`}>
        <rect x={-40} y={-34} width={80} height={68} rx={30} fill={P.skin} stroke={P.ink} strokeWidth={8} />
      </g>
    ))}
    <g transform="translate(340,730) scale(0.9)"><AshotBack /></g>
    <Sub text={wink ? 'Запомнил?' : 'пять лямов. Норм же?'} keys={['пять', 'лямов.']} />
  </svg>
);

// 4 / 7. Сбоку с переднего пассажирского: руль в перспективе, рука на ободе, приборка
export const ShotSide: React.FC<{turn?: number; arm?: 'rest' | 'up'; mouth?: number; text: string; keys?: string[]; whoosh?: boolean}> = ({turn = 0.3, arm = 'rest', mouth = 2, text, keys, whoosh}) => (
  <svg viewBox="0 0 1080 1920">
    <defs><filter id="blur8"><feGaussianBlur stdDeviation="8" /></filter></defs>
    <SideCabin />
    {/* торпеда справа */}
    <path d="M690,1080 L1100,1000 L1100,1920 L760,1920Z" fill="#1F1B1A" stroke={P.ink} strokeWidth={10} />
    <path d="M700,1080 Q760,1020 860,1030 L880,1100 L720,1130Z" fill="#141110" stroke={P.ink} strokeWidth={8} />
    <ellipse cx={800} cy={1090} rx={36} ry={30} fill="#0E0C0B" stroke="#6E6660" strokeWidth={5} />
    <g transform="translate(450,1150) scale(-1.15,1.15)">
      <Ashot s={{...A0, turn, mouth, smirk: 1, look: turn > 0.5 ? [0.7, 0] : [-0.8, -0.2], arm: {from: arm, to: arm, k: 1}}} />
    </g>
    {/* рулевая колонка и руль — перед Ашотом */}
    <path d="M840,1450 L1100,1560" stroke={P.ink} strokeWidth={70} />
    <path d="M840,1450 L1100,1560" stroke="#2A2422" strokeWidth={54} />
    <g transform="translate(820,1420) rotate(-6)">
      <ellipse rx={95} ry={250} fill="none" stroke={P.ink} strokeWidth={34} />
      <ellipse rx={95} ry={250} fill="none" stroke="#5C504A" strokeWidth={20} />
      <path d="M-70,-200 Q-96,0 -70,200" fill="none" stroke="#8A7C72" strokeWidth={6} strokeLinecap="round" />
      <path d="M20,30 L-70,180 M20,30 L-74,-150" stroke={P.ink} strokeWidth={26} strokeLinecap="round" />
      <path d="M20,30 L-70,180 M20,30 L-74,-150" stroke="#5C504A" strokeWidth={14} strokeLinecap="round" />
      <ellipse cx={20} cy={30} rx={34} ry={64} fill="#5C504A" stroke={P.ink} strokeWidth={7} />
    </g>
    {/* кулак на ободе */}
    <g transform="translate(728,1470) rotate(-10)">
      <rect x={-46} y={-40} width={92} height={80} rx={34} fill={P.skin} stroke={P.ink} strokeWidth={9} />
      <path d="M-40,-6 Q-10,6 30,-8" fill="none" stroke={P.skinShade} strokeWidth={5} />
    </g>
    {whoosh && <g opacity={0.8}>{[0, 1, 2].map((i) => <path key={i} d={`M${200 + i * 30},${520 + i * 60} q-120,80 -60,200`} fill="none" stroke={P.cream} strokeWidth={12} strokeLinecap="round" />)}</g>}
    <Sub text={text} keys={keys} />
  </svg>
);

// 6. Машина спереди: фары, решётка, капот, шашки
export const ShotCarFront: React.FC<{text: string; keys?: string[]}> = ({text, keys}) => (
  <svg viewBox="0 0 1080 1920">
    <defs><filter id="blur8"><feGaussianBlur stdDeviation="8" /></filter></defs>
    <rect width={1080} height={1920} fill={P.sky1} />
    <g filter="url(#blur8)">{Array.from({length: 10}, (_, i) => <circle key={i} cx={(i * 211) % 1080} cy={150 + (i * 97) % 300} r={30} fill={[P.lamp, '#FFD9A0', '#E0523E'][i % 3]} opacity={0.6} />)}</g>
    <rect y={1780} width={1080} height={140} fill="#2A2430" />
    {/* кузов */}
    <path d="M150,530 Q540,480 930,530 L1000,1170 L1050,1200 L1050,1800 L30,1800 L30,1200 L80,1170Z" fill={TAXI} stroke={P.ink} strokeWidth={12} strokeLinejoin="round" />
    <g transform="translate(540,505)"><Checker w={240} h={66} /></g>
    {/* салон через лобовое */}
    <clipPath id="wsh2"><path d="M195,560 Q540,520 885,560 L950,1150 L130,1150Z" /></clipPath>
    <g clipPath="url(#wsh2)">
      <rect width={1080} height={1920} fill={P.cabin} />
      <clipPath id="rw2"><path d="M300,650 L780,650 L800,860 L280,860Z" /></clipPath>
      <g clipPath="url(#rw2)"><g transform="translate(40,200) scale(0.95,0.7)"><City t={0} /></g></g>
      <path d="M200,840 L880,840 L900,1300 L180,1300Z" fill={P.seat} stroke={P.ink} strokeWidth={10} />
      <g transform="translate(400,1040) scale(1.1)"><RiderFigure r={RIDERS[0]} e={{...EMO.shock, mouth: 3}} /></g>
      <g transform="translate(760,1120) scale(0.92)"><Ashot s={{...A0, turn: 0.75, smirk: 1, look: [-0.5, 0]}} /></g>
      <path d="M560,1150 Q560,1080 760,1070 Q960,1080 960,1150" fill="none" stroke={P.ink} strokeWidth={30} />
      <path d="M60,1140 L1020,1100 L1020,1160 L60,1160Z" fill="#1F1B1A" />
      <path d="M250,560 L360,560 L210,1150 L140,1150Z" fill="#fff" opacity={0.1} />
      <path d="M760,550 L810,550 L700,1150 L670,1150Z" fill="#fff" opacity={0.08} />
    </g>
    <path d="M195,560 Q540,520 885,560 L950,1150 L130,1150Z" fill="none" stroke={P.ink} strokeWidth={14} />
    {/* дворники */}
    <path d="M200,1150 L520,1100 M560,1150 L880,1100" stroke={P.ink} strokeWidth={14} strokeLinecap="round" />
    {/* капот с рёбрами */}
    <path d="M60,1190 L1020,1190 L1050,1560 L30,1560Z" fill={TAXI} stroke={P.ink} strokeWidth={10} />
    <path d="M400,1195 L340,1555 M680,1195 L740,1555" stroke={TAXI_D} strokeWidth={8} />
    {/* решётка и прямоугольные фары */}
    <rect x={30} y={1560} width={1020} height={150} fill="#2A2422" stroke={P.ink} strokeWidth={10} />
    {[0, 1, 2, 3].map((i) => <path key={i} d={`M330,${1590 + i * 30} L750,${1590 + i * 30}`} stroke="#B9B2A8" strokeWidth={10} />)}
    {[[60, 300], [780, 1020]].map(([a, b], i) => (
      <g key={i}>
        <rect x={a} y={1575} width={b - a} height={120} rx={14} fill="#FFF3CF" stroke={P.ink} strokeWidth={8} />
        <circle cx={(a + b) / 2 + (i ? 40 : -40)} cy={1635} r={42} fill="#FFFBEB" stroke={P.ink} strokeWidth={5} />
        <rect x={(a + b) / 2 + (i ? -110 : 30)} y={1600} width={80} height={70} rx={8} fill="#FFE7A8" stroke={P.ink} strokeWidth={4} />
      </g>
    ))}
    <path d="M300,1640 L60,1500 L60,1780Z M780,1640 L1020,1500 L1020,1780Z" fill="#FFE7A8" opacity={0.0} />
    {/* бампер и номер */}
    <rect x={10} y={1715} width={1060} height={60} rx={28} fill="#B9B2A8" stroke={P.ink} strokeWidth={9} />
    <rect x={400} y={1690} width={280} height={74} rx={8} fill="#F5F2EA" stroke={P.ink} strokeWidth={7} />
    <text x={540} y={1745} textAnchor="middle" fontFamily={F} fontWeight={800} fontSize={48} fill={P.ink}>А 400 ВА</text>
    <Sub text={text} keys={keys} />
  </svg>
);

// ---------- телефон-навигатор в держателе (интерфейс «как у навигатора», без логотипов)
export const NavPhone: React.FC<{pick?: boolean}> = ({pick = true}) => (
  <g>
    <rect x={-270} y={-520} width={540} height={1040} rx={60} fill="#111014" stroke={P.ink} strokeWidth={12} />
    <clipPath id="navp"><rect x={-246} y={-494} width={492} height={988} rx={44} /></clipPath>
    <g clipPath="url(#navp)">
      <rect x={-250} y={-500} width={500} height={1000} fill="#2F333B" />
      {Array.from({length: 8}, (_, i) => <path key={i} d={`M-260,${-480 + i * 120} L260,${-440 + i * 120}`} stroke="#444A55" strokeWidth={22} />)}
      {Array.from({length: 6}, (_, i) => <path key={'v' + i} d={`M${-230 + i * 100},-500 L${-200 + i * 100},520`} stroke="#444A55" strokeWidth={22} />)}
      <path d="M-260,120 Q-60,60 260,160" stroke="#3E5A74" strokeWidth={50} fill="none" />
      {/* длинный маршрут с пробками */}
      <path d="M0,250 L-180,240 L-190,-60 L-140,-200 L0,-260" fill="none" stroke={pick ? '#5A5F68' : '#E0523E'} strokeWidth={22} strokeLinecap="round" strokeLinejoin="round" />
      {!pick && <path d="M-185,100 L-190,-60" stroke="#F2B84B" strokeWidth={22} strokeLinecap="round" />}
      {/* короткий маршрут */}
      <path d="M0,250 L20,0 L0,-260" fill="none" stroke={pick ? '#6FCF5A' : '#7FAF6B'} strokeWidth={pick ? 30 : 20} strokeLinecap="round" strokeLinejoin="round" />
      <g transform="translate(0,-290)"><circle r={22} fill="#fff" stroke={P.ink} strokeWidth={6} /><circle r={9} fill="#E0523E" /></g>
      <path d="M0,230 L-26,290 L0,276 L26,290Z" fill="#fff" stroke={P.ink} strokeWidth={5} />
      {/* плашка манёвра сверху */}
      <rect x={-226} y={-474} width={452} height={130} rx={24} fill="#1C1E23" />
      <path d="M-180,-380 L-180,-430 L-150,-430 M-162,-446 L-146,-430 L-162,-414" fill="none" stroke="#fff" strokeWidth={10} strokeLinecap="round" strokeLinejoin="round" />
      <text x={-110} y={-396} fontFamily={F} fontWeight={900} fontSize={58} fill="#fff">300 м</text>
      {/* нижняя карточка: выбор маршрута */}
      <rect x={-250} y={150} width={500} height={360} rx={36} fill="#F6F3EC" />
      <rect x={-40} y={166} width={80} height={10} rx={5} fill="#C9C2B4" />
      {[['УМЕНЬШИТЬ ПЛАТЁЖ', '20 лет', 'пробки', !pick], ['УМЕНЬШИТЬ СРОК', 'быстрее', 'свободно', pick]].map(([a, b, c, on], i) => (
        <g key={i} transform={`translate(${i ? 118 : -118},280)`}>
          <rect x={-108} y={-80} width={216} height={160} rx={22} fill={on ? '#FFF4C2' : '#fff'} stroke={on ? '#F2C230' : '#DDD6C8'} strokeWidth={6} />
          <text y={-46} textAnchor="middle" fontFamily={F} fontWeight={800} fontSize={20} fill={P.ink}>{(a as string).split(' ')[0]}</text>
          <text y={-20} textAnchor="middle" fontFamily={F} fontWeight={800} fontSize={20} fill={P.ink}>{(a as string).split(' ')[1]}</text>
          <text y={26} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={34} fill={i ? P.sageDark : '#C8553D'}>{b as string}</text>
          <text y={62} textAnchor="middle" fontFamily={F} fontWeight={600} fontSize={22} fill="#7A7268">{c as string}</text>
        </g>
      ))}
      <rect x={-226} y={390} width={452} height={90} rx={24} fill="#F2C230" />
      <text y={450} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={44} fill={P.ink}>Поехали</text>
    </g>
  </g>
);

// 9. Торпеда: телефон в держателе, рука Ашота тянется
export const ShotDash: React.FC = () => (
  <svg viewBox="0 0 1080 1920">
    <defs><filter id="blur8"><feGaussianBlur stdDeviation="8" /></filter></defs>
    <RoadAhead />
    <path d="M-50,1000 Q540,920 1130,1000 L1130,1920 L-50,1920Z" fill="#1F1B1A" stroke={P.ink} strokeWidth={12} />
    <g transform="translate(-60,1450) rotate(-10)">
      <ellipse rx={260} ry={150} fill="none" stroke={P.ink} strokeWidth={34} />
      <ellipse rx={260} ry={150} fill="none" stroke="#2A2422" strokeWidth={20} />
    </g>
    {/* держатель */}
    <path d="M540,1300 L540,1420 M480,1440 L600,1440" stroke="#2A2422" strokeWidth={30} strokeLinecap="round" />
    <g transform="translate(560,900) scale(0.78)"><NavPhone pick={false} /></g>
    <PokeHand x={650} y={1150} rot={-24} s={1.05} />
    <Sub text="Гаси досрочно" keys={['досрочно']} />
  </svg>
);

// 10. Экран навигатора крупно: тык в «срок»
export const ShotNav: React.FC<{pick?: boolean; hand?: number}> = ({pick = true, hand = 1}) => (
  <svg viewBox="0 0 1080 1920">
    <rect width={1080} height={1920} fill="#1D1A1F" />
    <g transform="translate(540,800) scale(1.12)"><NavPhone pick={pick} /></g>
    <g transform="translate(700,1180)"><circle r={60} fill="#fff" opacity={0.25} /><circle r={36} fill="#fff" opacity={0.35} /></g>
    <PokeHand x={712 + (1 - hand) * 300} y={1278 + (1 - hand) * 700} rot={-14} s={0.9} />
    <Sub text="уменьшай срок, а не платёж" keys={['срок,']} />
  </svg>
);

// машинка сверху
const CarTop: React.FC<{x: number; y: number; r: number; c: string; brake?: boolean; taxi?: boolean}> = ({x, y, r, c, brake, taxi}) => (
  <g transform={`translate(${x},${y}) rotate(${r})`}>
    <rect x={-30} y={-52} width={60} height={104} rx={16} fill={c} stroke={P.ink} strokeWidth={6} />
    <rect x={-22} y={-30} width={44} height={24} rx={6} fill="#2C2840" />
    <rect x={-22} y={22} width={44} height={16} rx={5} fill="#2C2840" />
    {taxi && <rect x={-16} y={-4} width={32} height={16} rx={3} fill={P.mustard} stroke={P.ink} strokeWidth={3} />}
    {brake && <><rect x={-26} y={46} width={14} height={8} rx={3} fill="#FF4A3A" /><rect x={12} y={46} width={14} height={8} rx={3} fill="#FF4A3A" /></>}
  </g>
);

// 11. Сверху: развилка, слева пробка в полосах, такси идёт по короткой
export const ShotTopDown: React.FC<{k?: number}> = ({k = 0}) => {
  const W = 170;
  const road = (d: string) => <><path d={d} fill="none" stroke="#5E566A" strokeWidth={W} strokeLinejoin="round" /><path d={d} fill="none" stroke={P.cream} strokeWidth={6} strokeDasharray="34 30" opacity={0.7} strokeLinejoin="round" /></>;
  const cols = ['#C8553D', '#8FA57E', '#B9C6CF', '#E9E2D6', '#6B5A4A', '#B5677A'];
  const cars: [number, number, number][] = [];
  // нижняя горизонталь y=1250 (едут влево), две полосы
  for (let x = 470; x > 200; x -= 120) { cars.push([x, 1250 - 40, -90]); cars.push([x - 50, 1250 + 40, -90]); }
  // вертикаль x=150 (едут вверх)
  for (let y = 1130; y > 520; y -= 125) { cars.push([150 - 40, y, 0]); cars.push([150 + 40, y - 55, 0]); }
  // верхняя горизонталь y=420 (едут вправо)
  for (let x = 250; x < 470; x += 120) { cars.push([x, 420 - 40, 90]); }
  return (
    <svg viewBox="0 0 1080 1920">
      <rect width={1080} height={1920} fill="#3A3346" />
      {Array.from({length: 30}, (_, i) => <rect key={i} x={(i % 5) * 230 - 40} y={Math.floor(i / 5) * 330 - 60} width={170} height={250} rx={20} fill="#4A4258" />)}
      {road('M540,1960 L540,240')}
      {road('M540,1250 L150,1250 L150,420 L540,420')}
      {cars.map(([x, y, r], i) => <CarTop key={i} x={x} y={y} r={r} c={cols[i % cols.length]} brake />)}
      <path d="M580,1180 L580,330" stroke={P.sage} strokeWidth={16} strokeDasharray="40 24" />
      <g transform="translate(540,240)"><path d="M-60,30 L0,-30 L60,30Z" fill={P.terracotta} stroke={P.ink} strokeWidth={6} /><rect x={-44} y={30} width={88} height={60} fill={P.cream} stroke={P.ink} strokeWidth={6} /></g>
      <CarTop x={580} y={1130 - k * 600} r={0} c={TAXI} taxi />
      <Lines x={580} y={1220} n={3} len={120} dir={0} />
      {[0, 1, 2].map((i) => <path key={i} d={`M${555 + i * 25},1200 l0,${90 + i * 20}`} stroke={P.cream} strokeWidth={8} strokeLinecap="round" opacity={0.6} />)}
      <g transform="translate(300,1110)"><rect x={-180} y={-44} width={360} height={88} rx={44} fill={P.terracotta} stroke={P.ink} strokeWidth={7} /><text y={15} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={38} fill={P.cream}>ПЛАТЁЖ · 20 ЛЕТ</text></g>
      <g transform="translate(820,700)"><rect x={-150} y={-44} width={300} height={88} rx={44} fill={P.sage} stroke={P.ink} strokeWidth={7} /><text y={15} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={38} fill={P.cream}>СРОК · КОРОЧЕ</text></g>
      <Sub text="Так переплатишь меньше" keys={['меньше']} />
    </svg>
  );
};

// 14. Глазами пассажира: Ашот повернулся, тянет ОДНУ правую руку ладонью в камеру
export const ShotPOV: React.FC = () => (
  <svg viewBox="0 0 1080 1920">
    <defs><filter id="blur8"><feGaussianBlur stdDeviation="8" /></filter></defs>
    <RoadAhead />
    <path d="M0,0 L1080,0 L1080,200 Q540,160 0,200Z" fill={P.cabinMid} />
    <Dash2107 fare="400" />
    <g transform="translate(340,1330) scale(1.05)"><Ashot s={{...A0, turn: 1, mouth: 2, smirk: 1, look: [0.3, 0.1], noRightArm: true}} /></g>
    {/* спинка его кресла между ним и камерой */}
    <path d="M90,1500 Q90,1440 160,1436 L560,1436 Q630,1440 630,1500 L650,1920 L70,1920Z" fill={P.seatDark} stroke={P.ink} strokeWidth={10} />
    {[200, 300, 400, 500].map((x) => <path key={x} d={`M${x},1480 L${x},1900`} stroke="#3A2820" strokeWidth={8} />)}
    {/* рука от плеча к камере, с ракурсом: чем ближе, тем толще */}
    <path d="M560,1380 L640,1300 L700,1215" fill="none" stroke={P.ink} strokeWidth={128} strokeLinecap="round" strokeLinejoin="round" />
    <path d="M560,1380 L640,1300" fill="none" stroke={P.shirt} strokeWidth={110} strokeLinecap="round" />
    <ellipse cx={640} cy={1300} rx={66} ry={46} fill={P.shirtShade} stroke={P.ink} strokeWidth={8} transform="rotate(-40 640 1300)" />
    <path d="M640,1300 L700,1215" fill="none" stroke={P.skin} strokeWidth={100} strokeLinecap="round" />
    <g transform="translate(740,1150) scale(2.3) rotate(-14)">
      <path d="M-58,-6 Q-60,34 -10,40 Q48,42 62,6 L70,-14 Q74,-26 62,-26 L50,-12 Q30,-30 -10,-28 Q-50,-26 -58,-6Z" fill={P.skin} stroke={P.ink} strokeWidth={5} />
      {[-34, -12, 10, 32].map((fx, i) => <path key={i} d={`M${fx},-24 q-4,-26 8,-28 q12,2 8,28`} fill={P.skin} stroke={P.ink} strokeWidth={5} />)}
      <path d="M-30,10 Q0,22 34,8" fill="none" stroke={P.skinShade} strokeWidth={3} />
    </g>
    <Sub text="С тебя четыреста рублей" keys={['четыреста', 'рублей']} />
  </svg>
);

// 15. Стоп-кадр изнутри салона: Ашот с протянутой рукой, пассажир в шоке
export const ShotFreeze: React.FC = () => {
  const s = {...A0, turn: 1, mouth: 0, smirk: 1, look: [0.6, -0.1] as [number, number], arm: {from: 'palm' as const, to: 'palm' as const, k: 1}};
  return (
    <svg viewBox="0 0 1080 1920">
      <g transform="translate(540,960) scale(1.12) translate(-560,-1010)">
        <CabinBack t={0} />
        <g transform="translate(720,1000)"><RiderFigure r={RIDERS[0]} e={EMO.shock} /></g>
        <DriverSeat />
        <g transform="translate(330,1090) rotate(2)"><Ashot s={s} /></g>
        <CabinFront t={0} ashot={s} mirrorOn={0} fare={400} shake={0} />
      </g>
      <rect width={1080} height={1920} fill="#FFF6E6" opacity={0.15} />
      <rect x={18} y={18} width={1044} height={1884} fill="none" stroke={P.cream} strokeWidth={24} />
      <g transform="translate(489,470) rotate(-7)">
        <rect x={-230} y={-85} width={460} height={170} rx={28} fill={P.cream} stroke={P.terracotta} strokeWidth={12} />
        <text y={44} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={124} fill={P.terracotta}>400 ₽</text>
      </g>
      <Sub text="четыреста рублей" keys={['четыреста', 'рублей']} />
    </svg>
  );
};

// ---------- Хук «Ипотека» v2: визг тормозов. Такси летит, резко тормозит: клюёт носом, дым, следы шин.
// lt — сек от начала плана, tb — момент торможения, ts — полная остановка (сек от начала плана)
export const ShotBrake: React.FC<{lt: number; tb?: number; ts?: number}> = ({lt, tb = 0.3, ts = 0.9}) => {
  const v0 = 1;                                        // скорость «улицы» до тормоза
  const d = Math.max(0, Math.min(lt, ts) - tb), D = ts - tb;
  const tt = lt < tb ? lt : tb + (d - d * d / (2 * D)); // равнозамедленно до нуля
  const braking = lt >= tb && lt < ts + 0.05;
  const dip = lt < tb ? 0 : lt < ts ? 4 * Math.min(1, (lt - tb) / 0.12) : 4 * Math.max(0, Math.cos((lt - ts) * 9)) * Math.exp(-(lt - ts) * 5) - 1.2 * Math.sin(Math.min(1, (lt - ts) / 0.15) * Math.PI);
  const carX = 520 + (lt < tb ? (lt - tb) * 600 : 0);
  return (
    <svg viewBox="0 0 1080 1920">
      <NightStreet t={tt * v0} />
      {/* следы шин */}
      {lt > tb && [-250, 255].map((x) => <path key={x} d={`M${carX + x * 1.15 - 30},${1440 + 74} l${-Math.min(420, (lt - tb) * 900)},0`} stroke="#151217" strokeWidth={16} strokeLinecap="round" opacity={0.85} />)}
      {!braking && lt < tb && <Lines x={90} y={1060} n={5} len={260} />}
      <g transform={`translate(${carX},1440) scale(1.15) rotate(${-1.5 + dip})`}><TaxiSide t={tt} /></g>
      {/* дым из-под колёс */}
      {lt > tb && Array.from({length: 10}, (_, i) => {
        const k = (lt - tb) * 2.2 - i * 0.09; if (k <= 0 || k > 1.4) return null;
        const x = carX + (i % 2 ? -250 : 255) * 1.15 - 60 - k * 160, y = 1500 - k * 140;
        return <circle key={i} cx={x} cy={y} r={40 + k * 90} fill="#D9D2CC" opacity={Math.max(0, 0.55 - k * 0.4)} />;
      })}
      {/* «визг»: штрихи у колёс */}
      {braking && [0, 1, 2].map((i) => <path key={i} d={`M${carX + 420},${1330 + i * 60} l${70 + i * 20},${-20 + i * 20}`} stroke={P.cream} strokeWidth={12} strokeLinecap="round" opacity={0.8} />)}
      {braking && <text x={540} y={760} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={150} fill={P.mustard} stroke={P.ink} strokeWidth={14} paintOrder="stroke" transform={`rotate(-6 540 760) scale(${1 + 0.04 * Math.sin(lt * 60)})`} style={{transformOrigin: '540px 760px'}}>ВИИИЗГ!</text>}
    </svg>
  );
};

// ---------- Хук v2: в салоне Тимура бросает вперёд, телефон «ИПОТЕКА ОДОБРЕНА» вылетает на передний ряд
export const ShotJolt: React.FC<{lt: number; rider?: Rider; phone?: [string, string, string]; bad?: boolean}> = ({lt, rider = RIDERS[0], phone = ['ИПОТЕКА', 'ОДОБРЕНА ✓', '5 000 000 ₽'], bad}) => {
  const j = Math.min(1, lt / 0.18), back = Math.max(0, Math.min(1, (lt - 0.35) / 0.3));
  const lean = j * (1 - back * 0.7);                     // рывок вперёд и откат
  const pk = Math.min(1, lt / 0.6);                      // полёт телефона
  const px = 560 - pk * 360, py = 880 - Math.sin(pk * Math.PI) * 380 + pk * 220, pr = -8 - pk * 540;
  return (
    <svg viewBox="0 0 1080 1920">
      <g transform={`translate(${-260 + lean * 20},${-420 - lean * 30}) scale(1.5)`}><CabinBack t={0} /></g>
      <g transform={`translate(540,${1300 - lean * 120}) scale(${1.9 + lean * 0.45}) rotate(${lean * -6})`}><RiderFigure r={rider} e={{...EMO.shock, look: [-0.5, -0.6]}} /></g>
      {/* полосы движения — рывок */}
      {lt < 0.3 && Array.from({length: 6}, (_, i) => <path key={i} d={`M${120 + i * 170},${1700 - i * 30} l0,${-200 - i * 20}`} stroke={P.cream} strokeWidth={10} strokeLinecap="round" opacity={0.5 * (1 - lt / 0.3)} />)}
      <g transform={`translate(${px},${py}) rotate(${pr}) scale(${0.62 - pk * 0.12})`} opacity={pk < 1 ? 1 : 0.9}>
        <rect x={-210} y={-380} width={420} height={760} rx={56} fill="#1D1A1F" stroke={P.ink} strokeWidth={12} />
        <rect x={-184} y={-344} width={368} height={688} rx={38} fill={P.cream} />
        <circle cx={0} cy={-150} r={86} fill={bad ? P.terracotta : P.sage} stroke={P.ink} strokeWidth={8} />
        {bad ? <path d="M-40,-150 L40,-150" stroke={P.cream} strokeWidth={22} strokeLinecap="round" /> : <path d="M-40,-150 L-8,-116 L46,-186" fill="none" stroke={P.cream} strokeWidth={20} strokeLinecap="round" strokeLinejoin="round" />}
        <text y={-10} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={50} fill={P.ink}>{phone[0]}</text>
        <text y={50} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={46} fill={bad ? P.terracotta : P.sageDark}>{phone[1]}</text>
        <rect x={-160} y={100} width={320} height={90} rx={20} fill={P.beige} stroke={P.ink} strokeWidth={5} />
        <text y={160} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={phone[2].length > 10 ? 40 : 46} fill={bad ? P.terracotta : P.ink}>{phone[2]}</text>
      </g>
      {/* след полёта */}
      {pk > 0.05 && pk < 1 && <path d={`M560,880 Q${(560 + px) / 2},${py - 160} ${px},${py}`} fill="none" stroke={P.cream} strokeWidth={8} strokeDasharray="20 22" opacity={0.5} />}
    </svg>
  );
};
