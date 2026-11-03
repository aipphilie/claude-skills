import React, {useMemo} from 'react';
import {P} from '../palette';
import {AshotEyes, AshotState} from '../characters/Ashot';

// Салон такси в мировых координатах 1080×1920. Вид с переднего пассажирского сиденья назад-влево.
const rnd = (seed: number) => () => { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; };

const REAR = 'M200,480 Q210,455 260,452 L930,452 Q975,455 985,480 L1010,850 L180,850Z';
const SIDE = 'M1040,420 L1080,420 L1080,980 L1050,980Z';

const Buildings: React.FC<{t: number; speed: number; seed: number; color: string; base: number; hMin: number; hMax: number; winOp: number}> = ({t, speed, seed, color, base, hMin, hMax, winOp}) => {
  const W = 1400;
  const blds = useMemo(() => {
    const r = rnd(seed); const out: {x: number; w: number; h: number; wins: [number, number][]}[] = [];
    let x = 0;
    while (x < W) {
      const w = 70 + r() * 110, h = hMin + r() * (hMax - hMin); const wins: [number, number][] = [];
      for (let yy = 18; yy < h - 20; yy += 30) for (let xx = 12; xx < w - 18; xx += 24) if (r() < 0.42) wins.push([xx, yy]);
      out.push({x, w, h, wins}); x += w + 6 + r() * 14;
    }
    return out;
  }, [seed, hMin, hMax]);
  const off = (t * speed) % W;
  return (
    <g>
      {[0, 1].map((rep) => (
        <g key={rep} transform={`translate(${off - W + rep * W + 100},0)`}>
          {blds.map((b, i) => (
            <g key={i}>
              <rect x={b.x} y={base - b.h} width={b.w} height={b.h + 400} fill={color} />
              {b.wins.map(([wx, wy], j) => (
                <rect key={j} x={b.x + wx} y={base - b.h + wy} width={11} height={14} rx={2} fill={P.win} opacity={winOp * (0.55 + ((i * 7 + j * 3) % 5) * 0.1)} />
              ))}
            </g>
          ))}
        </g>
      ))}
    </g>
  );
};

const City: React.FC<{t: number}> = ({t}) => {
  const lamps = Array.from({length: 9}, (_, i) => i);
  const lampOff = (t * 420) % 1400;
  return (
    <g>
      <defs>
        <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor={P.sky1} />
          <stop offset="0.55" stopColor={P.sky2} />
          <stop offset="1" stopColor={P.sky3} />
        </linearGradient>
        <filter id="blur8"><feGaussianBlur stdDeviation="8" /></filter>
        <filter id="blur3"><feGaussianBlur stdDeviation="3" /></filter>
      </defs>
      <rect x={100} y={380} width={1000} height={620} fill="url(#sky)" />
      <circle cx={760} cy={600} r={60} fill="#F2B880" opacity={0.35} filter="url(#blur8)" />
      <g filter="url(#blur3)">
        <Buildings t={t} speed={45} seed={11} color={P.bld1} base={790} hMin={110} hMax={260} winOp={0.6} />
      </g>
      <Buildings t={t} speed={140} seed={29} color={P.bld2} base={840} hMin={70} hMax={190} winOp={0.9} />
      {/* фонари и огни: ближний слой, быстрый, размытый */}
      <g filter="url(#blur8)">
        {lamps.map((i) => {
          const x = ((i * 160 + lampOff) % 1400) - 150;
          return (
            <g key={i}>
              <circle cx={x} cy={560 + (i % 3) * 18} r={22 + (i % 2) * 8} fill={i % 3 === 0 ? '#FFD9A0' : P.lamp} opacity={0.85} />
              <circle cx={x + 60} cy={800 + (i % 2) * 20} r={14} fill={i % 2 ? '#FF8A6A' : '#FFE1A8'} opacity={0.8} />
            </g>
          );
        })}
      </g>
    </g>
  );
};

export const CabinBack: React.FC<{t: number}> = ({t}) => (
  <g>
    {/* потолок и стенки */}
    <rect x={-200} y={-200} width={1500} height={2400} fill={P.cabin} />
    <path d="M-200,-200 L1300,-200 L1300,430 Q540,380 -200,430Z" fill={P.cabinMid} />
    <ellipse cx={640} cy={250} rx={110} ry={34} fill="#F8D9A6" opacity={0.25} />
    <rect x={590} y={232} width={100} height={34} rx={14} fill="#E9C48C" stroke={P.ink} strokeWidth={6} />
    {/* окна с городом */}
    <clipPath id="win"><path d={REAR} /><path d={SIDE} /></clipPath>
    <g clipPath="url(#win)"><City t={t} /></g>
    <path d={REAR} fill="none" stroke={P.ink} strokeWidth={14} />
    <path d={REAR} fill="none" stroke="#7A5E4E" strokeWidth={5} />
    <path d={SIDE} fill="none" stroke={P.ink} strokeWidth={12} />
    {/* блик на стекле */}
    <path d="M300,470 L380,470 L250,840 L200,840Z" fill="#fff" opacity={0.06} />
    {/* стойка */}
    <path d="M985,440 L1050,410 L1060,1000 L1010,1000Z" fill={P.cabinLight} stroke={P.ink} strokeWidth={8} />
    {/* заднее сиденье */}
    <path d="M150,840 Q160,800 230,800 L1000,800 Q1080,805 1090,860 L1100,1500 L140,1500Z" fill={P.seat} stroke={P.ink} strokeWidth={10} strokeLinejoin="round" />
    {[380, 560, 740, 920].map((x) => <path key={x} d={`M${x},830 L${x + 6},1400`} stroke={P.seatDark} strokeWidth={6} />)}
    <path d="M150,1160 L1100,1160" stroke={P.seatDark} strokeWidth={8} />
    {/* подголовник справа */}
    <rect x={850} y={700} width={150} height={120} rx={40} fill={P.seat} stroke={P.ink} strokeWidth={9} />
  </g>
);

export const DriverSeat: React.FC = () => (
  <g>
    <rect x={385} y={700} width={170} height={170} rx={52} fill={P.seatDark} stroke={P.ink} strokeWidth={10} />
    <rect x={430} y={860} width={26} height={60} fill="#2a2a2a" />
    <rect x={480} y={860} width={26} height={60} fill="#2a2a2a" />
    <path d="M330,920 Q340,880 420,880 L600,880 Q650,885 655,940 L680,1920 L320,1920Z" fill={P.seatDark} stroke={P.ink} strokeWidth={10} />
  </g>
);

export const CabinFront: React.FC<{t: number; ashot: AshotState; mirrorOn: number; fare: number; shake: number}> = ({t, ashot, mirrorOn, fare, shake}) => {
  const sway = Math.sin(t * 2.4) * 9 + shake * 6;
  return (
    <g>
      {/* руль */}
      <g transform="translate(120,1470) rotate(-14)">
        <ellipse rx={230} ry={96} fill="none" stroke={P.ink} strokeWidth={56} />
        <ellipse rx={230} ry={96} fill="none" stroke="#3E3532" strokeWidth={38} />
        <ellipse rx={230} ry={96} fill="none" stroke="#5A4E49" strokeWidth={8} strokeDasharray="30 40" />
      </g>
      {/* приборка снизу */}
      <path d="M-100,1700 Q540,1620 1200,1700 L1200,2100 L-100,2100Z" fill="#2E2420" stroke={P.ink} strokeWidth={10} />
      {/* таксометр */}
      <g transform="translate(760,1700)">
        <rect width={250} height={110} rx={18} fill="#1E1816" stroke={P.ink} strokeWidth={8} />
        <rect x={18} y={18} width={214} height={74} rx={10} fill="#3A1F14" />
        <text x={125} y={74} textAnchor="middle" fontFamily="Rubik" fontWeight={800} fontSize={54} fill="#FF9A4A">{Math.round(fare)} ₽</text>
      </g>
      {/* зеркало заднего вида */}
      <g transform="translate(470,420)">
        <rect x={-14} y={-260} width={28} height={200} fill="#2A2220" stroke={P.ink} strokeWidth={6} />
        <g transform={`rotate(${sway}, 0, -40)`}>
          <path d="M0,-40 L0,90" stroke="#E9D9B9" strokeWidth={3} />
          <path d="M0,90 l-34,52 h20 l-26,40 h28 l-20,34 h64 l-20,-34 h28 l-26,-40 h20Z" fill={P.terracotta} stroke={P.ink} strokeWidth={5} strokeLinejoin="round" />
        </g>
        <rect x={-180} y={-70} width={360} height={130} rx={44} fill="#241C1A" stroke={P.ink} strokeWidth={10} />
        <clipPath id="mirror"><rect x={-164} y={-56} width={328} height={102} rx={34} /></clipPath>
        <g clipPath="url(#mirror)">
          <rect x={-170} y={-60} width={340} height={110} fill="#8C7A72" />
          <rect x={-170} y={-60} width={340} height={110} fill="#B9A59A" opacity={0.5} />
          {/* в зеркале — глаза Ашота (отражение), исчезают после поворота */}
          <g opacity={mirrorOn} transform="translate(0,252) scale(0.95)">
            <rect x={-150} y={-320} width={300} height={140} fill={P.skin} />
            <AshotEyes s={{...ashot, look: [-0.2, -0.5]}} dx={0} />
          </g>
          <path d="M-150,-60 L-90,-60 L-150,50Z" fill="#fff" opacity={0.18} />
        </g>
      </g>
    </g>
  );
};
