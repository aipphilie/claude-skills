import React from 'react';
import {P} from '../palette';
import {RiderFigure, RIDERS, Rider} from '../characters/Rider';
import {clamp, easeInOut, easeOut, lerp, pop} from '../lib';
import {Cam, Coin, Note, Tag, TIM, emo, fmt, sky} from './World';
import {NightStreet, TaxiSide} from './Shots';

// Сцены серии 2 «Налоговый вычет». Те же правила, что в World.tsx: 1080×1920, lt — сек от начала врезки,
// dur — длина врезки, важное в зоне x 56..922, y 250..1300 (ниже — субтитры).

const F = 'Rubik';
const after = (lt: number, a: number, d = 0.3) => clamp((lt - a) / d);
const LUDA = RIDERS[1];
const TIM35: Rider = {...RIDERS[0], name: '35', hair: 'sidepart', hairColor: '#6A5446', clothes: 'shirtTie', c1: '#C9C2B4', c2: '#6B5A4A', glasses: true, wrinkles: true, bodyScale: 1.12};

// конверт «СДАЧА» / «ВЫЧЕТ»
const Envelope: React.FC<{x: number; y: number; s?: number; rot?: number; text?: string; fill?: string; o?: number}> = ({x, y, s = 1, rot = 0, text = 'СДАЧА', fill = P.sage, o = 1}) => (
  <g transform={`translate(${x},${y}) rotate(${rot}) scale(${s})`} opacity={o}>
    <rect x={-150} y={-95} width={300} height={190} rx={14} fill={P.cream} stroke={P.ink} strokeWidth={7} />
    <path d="M-150,-95 L0,15 L150,-95" fill="none" stroke={P.ink} strokeWidth={7} strokeLinejoin="round" />
    <rect x={-110} y={30} width={220} height={52} rx={26} fill={fill} stroke={P.ink} strokeWidth={5} />
    <text y={68} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={34} fill={P.cream}>{text}</text>
  </g>
);

// здание налоговой: колонны, вывеска, окно выдачи
const TaxOffice: React.FC<{x: number; y: number; s?: number; shut?: number}> = ({x, y, s = 1, shut = 0}) => (
  <g transform={`translate(${x},${y}) scale(${s})`}>
    <path d="M-260,-420 L0,-560 L260,-420Z" fill="#D9CFC0" stroke={P.ink} strokeWidth={9} strokeLinejoin="round" />
    <rect x={-250} y={-420} width={500} height={420} fill="#E7DED0" stroke={P.ink} strokeWidth={9} />
    {[-190, -95, 95, 190].map((cx) => <rect key={cx} x={cx - 22} y={-400} width={44} height={380} fill="#F3ECE0" stroke={P.ink} strokeWidth={5} />)}
    <rect x={-210} y={-395} width={420} height={70} rx={10} fill={P.capDark} stroke={P.ink} strokeWidth={6} />
    <text y={-347} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={44} fill={P.cream}>НАЛОГОВАЯ</text>
    <rect x={-70} y={-260} width={140} height={150} rx={10} fill="#3A2E2A" stroke={P.ink} strokeWidth={7} />
    <rect x={-70} y={-260} width={140} height={150 * shut} rx={10} fill="#8A8F96" stroke={P.ink} strokeWidth={6} />
    {shut > 0.9 && <text y={-170} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={26} fill={P.cream}>ЗАКРЫТО</text>}
  </g>
);

// 0. Хук: такси ночью влетает в «лежачего полицейского», подлетает (bump — момент удара, сек)
export const SceneBump: React.FC<{lt: number; bump?: number}> = ({lt, bump = 0.55}) => {
  const tt = Math.min(lt, bump + 0.4);
  const hop = lt < bump ? 0 : Math.max(0, Math.sin(clamp((lt - bump) / 0.45) * Math.PI)) * 120;
  const rot = lt < bump ? 0 : lt < bump + 0.15 ? -6 * after(lt, bump, 0.15) : -6 + 9 * after(lt, bump + 0.15, 0.3);
  const carX = 540 + (lt < bump ? (lt - bump) * 500 : Math.min(0.4, lt - bump) * 200);
  const bx = 540 + 330 - (lt - bump) * 700;   // «лежачий» уезжает назад
  return (
    <svg viewBox="0 0 1080 1920">
      <NightStreet t={tt * 1.2} />
      <path d={`M${bx - 120},1445 Q${bx},1370 ${bx + 120},1445Z`} fill={P.mustard} stroke={P.ink} strokeWidth={8} />
      {[0, 1, 2].map((i) => <rect key={i} x={bx - 70 + i * 50} y={1400} width={26} height={36} fill={P.ink} transform={`skewX(-20)`} style={{transformOrigin: `${bx}px 1420px`}} />)}
      <g transform={`translate(${carX},${1440 - hop}) scale(1.15) rotate(${rot})`}><TaxiSide t={tt} /></g>
      {lt > bump && lt < bump + 0.7 && <text x={540} y={760} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={170} fill={P.mustard} stroke={P.ink} strokeWidth={14} paintOrder="stroke" transform={`rotate(-6 540 760)`}>БУМ!</text>}
      {lt > bump && Array.from({length: 6}, (_, i) => <path key={i} d={`M${carX - 300 + i * 110},${1560 - hop * 0.3} l${-20 + i * 8},${40}`} stroke={P.cream} strokeWidth={10} strokeLinecap="round" opacity={1 - after(lt, bump, 0.5)} />)}
    </svg>
  );
};

// 1. Зарплата → 13% по трубе в налоговую; на split из окна вылетает конверт «СДАЧА» обратно к Тимуру
export const SceneSalary: React.FC<{lt: number; dur: number; split?: number}> = ({lt, dur, split = 0.5}) => {
  const k = clamp(lt / dur), ts = split * dur;
  const back = easeInOut(after(lt, ts + 0.2, 1.1));
  return (
    <svg viewBox="0 0 1080 1920">
      {sky('#BFD9E8', '#F3E4CC', 'slsky')}
      <Cam k={k} z0={1.0} z1={1.08} cy={900}>
        <TaxOffice x={790} y={1180} s={0.95} />
        {/* труба от зарплаты к налоговой */}
        <path d="M270,700 Q540,520 720,820" fill="none" stroke="#8A8F96" strokeWidth={56} strokeLinecap="round" />
        <path d="M270,700 Q540,520 720,820" fill="none" stroke={P.ink} strokeWidth={56} strokeLinecap="round" strokeDasharray="2 2000" />
        {Array.from({length: 5}, (_, i) => {
          const p = ((lt * 0.8 + i / 5) % 1);
          const x = lerp(lerp(270, 540, p), lerp(540, 720, p), p), y = lerp(lerp(700, 520, p), lerp(520, 820, p), p);
          return <Coin key={i} x={x} y={y} r={30} rot={lt * 200 + i * 40} o={lt < ts + 0.4 ? 1 : 1 - after(lt, ts + 0.4, 0.3)} />;
        })}
        {/* пачка зарплаты, от неё отрезан кусок 13% */}
        <Note x={230} y={830} s={1.05} rot={-6} v="90 000" />
        <Note x={240} y={760} s={1.05} rot={4} v="90 000" />
        <g transform={`translate(330,600) scale(${pop(after(lt, 0.3, 0.4))}) rotate(-8)`}>
          <circle r={80} fill={P.terracotta} stroke={P.ink} strokeWidth={7} />
          <text y={22} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={60} fill={P.cream}>13%</text>
        </g>
        <g transform="translate(260,1450) scale(1.2)"><RiderFigure r={TIM} e={emo({smile: lt > ts + 1 ? 1 : 0.2, worry: lt < ts ? 0.6 : 0, look: [0.6, -0.3]})} /></g>
        {lt > ts && <Envelope x={lerp(700, 360, back)} y={lerp(900, 1030, back) - Math.sin(back * Math.PI) * 260} rot={lerp(20, -6, back)} s={lerp(0.5, 1, back)} />}
      </Cam>
      <Tag text={lt < ts ? 'КАЖДЫЙ МЕСЯЦ · НДФЛ' : 'КУПИЛ КВАРТИРУ → СДАЧА'} lt={lt < ts ? lt : lt - ts} fill={lt < ts ? P.ink : P.sageDark} />
    </svg>
  );
};

// 2. Калькулятор Тимура: 6 млн × 13% = 780 000 → на split перечёркнуто, «ЛИМИТ 2 МЛН → 260 000 ₽»
export const SceneCalc: React.FC<{lt: number; dur: number; split?: number}> = ({lt, dur, split = 0.5}) => {
  const ts = split * dur;
  const big = pop(after(lt, Math.min(1.6, ts * 0.6), 0.45));
  const cr = easeOut(after(lt, ts, 0.25));
  const lim = pop(after(lt, ts + 0.5, 0.45));
  return (
    <svg viewBox="0 0 1080 1920">
      <rect width={1080} height={1920} fill="#2B2440" />
      {Array.from({length: 14}, (_, i) => <circle key={i} cx={(i * 233) % 1080} cy={(i * 389) % 1920} r={50 + (i % 4) * 30} fill={P.sage} opacity={0.06} />)}
      <g transform={`translate(540,${820 - lt * 10}) rotate(-3)`}>
        <rect x={-330} y={-520} width={660} height={1040} rx={70} fill="#1D1A1F" stroke={P.ink} strokeWidth={14} />
        <rect x={-296} y={-480} width={592} height={960} rx={48} fill={P.cream} />
        <text x={250} y={-370} textAnchor="end" fontFamily={F} fontWeight={800} fontSize={54} fill="#7A6E66">6 000 000 × 13% =</text>
        <g transform={`translate(0,-210) scale(${big})`}>
          <text x={0} y={0} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={124} fill={P.ink}>780 000</text>
          <path d={`M-300,-40 L${-300 + 600 * cr},${-40 - 30 * cr}`} stroke={P.terracotta} strokeWidth={22} strokeLinecap="round" />
        </g>
        {/* кнопки калькулятора */}
        {Array.from({length: 12}, (_, i) => {
          const x = -195 + (i % 3) * 195, y = -10 + Math.floor(i / 3) * 120;
          return <g key={i}><rect x={x - 80} y={y} width={160} height={100} rx={26} fill={i % 3 === 2 ? P.mustard : P.beige} stroke={P.ink} strokeWidth={5} />
            <text x={x} y={y + 68} textAnchor="middle" fontFamily={F} fontWeight={800} fontSize={52} fill={P.ink}>{'789456123%0='[i]}</text></g>;
        })}
      </g>
      {lim > 0 && <g transform={`translate(540,520) scale(${lim}) rotate(-5)`}>
        <rect x={-420} y={-90} width={840} height={180} rx={90} fill={P.sage} stroke={P.ink} strokeWidth={9} />
        <text y={-14} textAnchor="middle" fontFamily={F} fontWeight={800} fontSize={42} fill={P.cream}>ЛИМИТ 2 МЛН ×13%</text>
        <text y={58} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={70} fill={P.cream}>= 260 000 ₽</text>
      </g>}
    </svg>
  );
};

// 3. Год ипотеки оплачен: 12 месяцев, на каждый падает штамп «ОПЛАЧЕНО»
export const SceneYearPaid: React.FC<{lt: number; dur: number}> = ({lt, dur}) => {
  const M = ['ЯНВ', 'ФЕВ', 'МАР', 'АПР', 'МАЙ', 'ИЮН', 'ИЮЛ', 'АВГ', 'СЕН', 'ОКТ', 'НОЯ', 'ДЕК'];
  const step = Math.max(0.08, (dur - 1.0) / 12);
  return (
    <svg viewBox="0 0 1080 1920">
      <rect width={1080} height={1920} fill="#F0E2C8" />
      <text x={540} y={330} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={66} fill={P.ink}>ИПОТЕКА · 51 609 ₽/мес</text>
      {M.map((m, i) => {
        const x = 230 + (i % 3) * 310, y = 470 + Math.floor(i / 3) * 210;
        const s = after(lt, 0.25 + i * step, 0.16);
        return (
          <g key={i} transform={`translate(${x},${y})`}>
            <rect x={-135} y={-80} width={270} height={170} rx={20} fill={P.cream} stroke={P.ink} strokeWidth={7} />
            <rect x={-135} y={-80} width={270} height={50} rx={20} fill={P.terracotta} stroke={P.ink} strokeWidth={7} />
            <text y={-42} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={34} fill={P.cream}>{m}</text>
            <text y={40} textAnchor="middle" fontFamily={F} fontWeight={800} fontSize={34} fill="#9A8E84">51 609</text>
            {s > 0 && <g transform={`rotate(-12) scale(${lerp(1.8, 1, easeOut(s))})`} opacity={clamp(s * 2)}>
              <rect x={-120} y={-12} width={240} height={68} rx={10} fill="none" stroke={P.sageDark} strokeWidth={8} />
              <text y={38} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={38} fill={P.sageDark}>ОПЛАЧЕНО</text>
            </g>}
          </g>
        );
      })}
      <g transform={`translate(540,1340) scale(${pop(after(lt, 0.25 + 12 * step, 0.45))}) rotate(-3)`}>
        <rect x={-420} y={-75} width={840} height={150} rx={75} fill={P.sage} stroke={P.ink} strokeWidth={8} />
        <text y={26} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={64} fill={P.cream}>ПЛАТИТ ГОСУДАРСТВО</text>
      </g>
    </svg>
  );
};

// 4. Копилка НДФЛ: «за год заплатил 140 400» → ровно столько пересыпается в конверт
export const SceneNdfl: React.FC<{lt: number; dur: number; split?: number}> = ({lt, dur, split = 0.5}) => {
  const ts = split * dur, k = clamp(lt / dur);
  const pour = after(lt, ts, Math.max(0.6, dur - ts - 0.3));
  return (
    <svg viewBox="0 0 1080 1920">
      {sky('#3C3456', '#7C5A78', 'ndsky')}
      <Cam k={k} z0={1.0} z1={1.1} cy={850}>
        <g transform={`translate(330,${760}) rotate(${lerp(0, 28, easeOut(pour))})`}>
          <ellipse rx={230} ry={180} fill="#E79AA8" stroke={P.ink} strokeWidth={10} />
          <circle cx={190} cy={-30} r={60} fill="#E79AA8" stroke={P.ink} strokeWidth={9} />
          <ellipse cx={230} cy={-30} rx={22} ry={30} fill="#D27D8E" stroke={P.ink} strokeWidth={6} />
          {[-120, -40, 60, 140].map((x) => <rect key={x} x={x - 22} y={150} width={44} height={70} rx={14} fill="#E79AA8" stroke={P.ink} strokeWidth={8} />)}
          <rect x={-70} y={-195} width={140} height={22} rx={11} fill={P.ink} />
          <text y={10} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={42} fill={P.ink}>НДФЛ ЗА ГОД</text>
          <text y={70} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={54} fill={P.ink}>140 400 ₽</text>
        </g>
        {pour > 0 && Array.from({length: 8}, (_, i) => {
          const p = ((lt - ts) * 1.6 + i / 8) % 1;
          return <Coin key={i} x={lerp(520, 720, p)} y={lerp(640, 1060, p * p)} r={28} rot={i * 50 + lt * 300} o={pour < 1 ? 1 : 0} />;
        })}
        <Envelope x={760} y={1110} s={1.1} text={fmt(140400 * easeOut(pour)) + ' ₽'} />
      </Cam>
      <Tag text="БОЛЬШЕ ЗА ГОД НЕ ВЕРНУТ" lt={lt} fill={P.terracotta} />
    </svg>
  );
};

// 5. Зарплата в конверте: окно налоговой захлопывается «ЗАКРЫТО»
export const SceneEnvelopeShut: React.FC<{lt: number; dur: number}> = ({lt, dur}) => {
  const shut = easeOut(after(lt, dur * 0.35, 0.25));
  return (
    <svg viewBox="0 0 1080 1920">
      {sky('#BFD9E8', '#F3E4CC', 'essky')}
      <g transform={`translate(${Math.sin(lt * 80) * 8 * (shut > 0.95 && lt < dur * 0.35 + 0.5 ? 1 : 0)},0)`}><TaxOffice x={540} y={1080} s={1.3} shut={shut} /></g>
      <g transform="translate(250,1450) scale(1.2)"><RiderFigure r={TIM} e={emo({smile: shut < 0.5 ? 0.8 : 0, worry: shut, shock: shut * 0.5, look: [0.6, -0.4]})} /></g>
      <Envelope x={520} y={1230} s={0.95} rot={-10} text="ЗАРПЛАТА" fill={P.mustard} />
      <Tag text="НАЛОГ НЕ ПЛАТИЛ — СДАЧИ НЕТ" lt={after(lt, dur * 0.35, 1) * 1} fill={P.terracotta} />
    </svg>
  );
};

// 6. Не только квартира: стоматолог → учёба → спортзал, из каждой сцены вылетает конверт «ВЫЧЕТ»
export const SceneTriple: React.FC<{lt: number; dur: number}> = ({lt, dur}) => {
  const part = dur / 3, i = Math.min(2, Math.floor(lt / part)), pl = lt - i * part;
  const bg = ['#D7ECEA', '#E9DCC4', '#2F3442'][i];
  const tag = ['ЛЕЧЕНИЕ', 'УЧЁБА', 'СПОРТ'][i];
  return (
    <svg viewBox="0 0 1080 1920">
      <rect width={1080} height={1920} fill={bg} />
      <Cam k={pl / part} z0={1.0} z1={1.12} cy={900}>
        {i === 0 && <g>
          {/* кресло стоматолога + огромный зуб */}
          <g transform="translate(700,980) rotate(-30)"><rect x={-10} y={0} width={20} height={260} rx={10} fill="#BFC4CC" stroke={P.ink} strokeWidth={6} /><circle r={46} fill="#DDE6EA" stroke={P.ink} strokeWidth={7} /></g>
          <circle cx={830} cy={560} r={110} fill="#FFF8D8" stroke={P.ink} strokeWidth={8} />
          <g transform="translate(470,650)">
            <path d="M-130,-150 Q-150,-230 -60,-230 Q0,-200 60,-230 Q150,-230 130,-150 Q120,0 90,140 Q70,200 40,120 Q0,40 -40,120 Q-70,200 -90,140 Q-120,0 -130,-150Z" fill="#FFFFFF" stroke={P.ink} strokeWidth={10} />
            <path d="M-60,-150 Q-40,-170 -10,-160" stroke="#C9D6DA" strokeWidth={10} fill="none" strokeLinecap="round" />
          </g>
        </g>}
        {i === 1 && <g>
          {/* стопка книг и шапочка выпускника */}
          {[0, 1, 2, 3].map((j) => <rect key={j} x={290 + (j % 2) * 30} y={1120 - j * 90} width={460} height={80} rx={10} fill={[P.terracotta, P.sage, P.capLight, P.mustard][j]} stroke={P.ink} strokeWidth={8} />)}
          <g transform="translate(560,700) rotate(-6)">
            <path d="M-260,0 L0,-110 L260,0 L0,110Z" fill="#2B2A33" stroke={P.ink} strokeWidth={9} />
            <path d="M-150,50 L-150,150 Q0,210 150,150 L150,50" fill="#2B2A33" stroke={P.ink} strokeWidth={9} />
            <path d="M200,20 L200,190" stroke={P.mustard} strokeWidth={10} /><circle cx={200} cy={200} r={20} fill={P.mustard} />
          </g>
        </g>}
        {i === 2 && <g>
          {/* штанга, поднимается вверх */}
          <g transform={`translate(540,${900 - Math.abs(Math.sin(pl * 5)) * 120})`}>
            <rect x={-380} y={-12} width={760} height={24} rx={12} fill="#BFC4CC" stroke={P.ink} strokeWidth={6} />
            {[-1, 1].map((sd) => <g key={sd}>
              <rect x={sd * 300 - 30} y={-130} width={60} height={260} rx={12} fill={P.terracotta} stroke={P.ink} strokeWidth={8} />
              <rect x={sd * 360 - 22} y={-95} width={44} height={190} rx={10} fill={P.terracotta} stroke={P.ink} strokeWidth={8} />
            </g>)}
          </g>
          <rect x={0} y={1250} width={1080} height={700} fill="#4A4F5E" />
        </g>}
        <Envelope x={lerp(700, 760, easeOut(after(pl, 0.2, 0.4)))} y={lerp(1100, 470, easeOut(after(pl, 0.2, 0.5)))} s={0.8 * pop(after(pl, 0.2, 0.4))} rot={10} text="ВЫЧЕТ" />
      </Cam>
      <g transform={`translate(${130 + tag.length * 18},300) scale(${pop(after(pl, 0, 0.35))}) rotate(-3)`}>
        <rect x={-tag.length * 18 - 40} y={-42} width={tag.length * 36 + 80} height={84} rx={42} fill={P.ink} stroke={P.cream} strokeWidth={5} />
        <text y={16} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={46} fill={P.cream}>{tag}</text>
      </g>
      <text x={540} y={1360} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={50} fill={i === 2 ? P.cream : P.ink} opacity={0.85}>до 19 500 ₽ в год</text>
    </svg>
  );
};

// 7. Зубы за 80 000 → 10 400 ₽ = 26 поездок с Ашотом
export const SceneTeeth: React.FC<{lt: number; dur: number}> = ({lt, dur}) => {
  const a = pop(after(lt, 0.1, 0.4)), arrow = easeOut(after(lt, 0.4, 0.3)), b = pop(after(lt, 0.6, 0.45));
  const n = Math.floor(clamp((lt - 1.2) / Math.max(0.6, dur - 1.6)) * 26);
  return (
    <svg viewBox="0 0 1080 1920">
      <rect width={1080} height={1920} fill="#231B18" />
      <g transform={`translate(300,420) scale(${a})`}>
        <rect x={-210} y={-75} width={420} height={150} rx={30} fill={P.cream} stroke={P.ink} strokeWidth={8} />
        <text y={24} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={70} fill="#9A8E84">80 000 ₽</text>
      </g>
      <path d={`M520,420 L${520 + 80 * arrow},420`} stroke={P.cream} strokeWidth={16} strokeLinecap="round" />
      <g transform={`translate(800,420) scale(${b})`}>
        <rect x={-230} y={-80} width={460} height={160} rx={30} fill={P.sage} stroke={P.ink} strokeWidth={8} />
        <text y={26} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={76} fill={P.cream}>10 400 ₽</text>
      </g>
      {Array.from({length: 26}, (_, i) => {
        const x = 140 + (i % 6) * 160, y = 650 + Math.floor(i / 6) * 140;
        const s = i < n ? pop(after(lt, 1.2 + i * (Math.max(0.6, dur - 1.6) / 26), 0.3)) : 0;
        return s > 0 && <g key={i} transform={`translate(${x},${y}) scale(${s * 0.55})`}>
          <rect x={-110} y={-60} width={220} height={120} rx={22} fill={P.mustard} stroke={P.ink} strokeWidth={9} />
          <rect x={-70} y={-95} width={140} height={40} rx={10} fill="#1D1A1F" stroke={P.ink} strokeWidth={7} />
          {[-1, 1].map((sd) => <rect key={sd} x={sd > 0 ? 0 : -70} y={-95} width={35} height={20} fill={P.cream} transform={`translate(${sd > 0 ? 35 : 0},0)`} />)}
          <circle cx={-60} cy={62} r={30} fill="#2E2B33" stroke={P.ink} strokeWidth={7} />
          <circle cx={60} cy={62} r={30} fill="#2E2B33" stroke={P.ink} strokeWidth={7} />
        </g>;
      })}
      <text x={540} y={1300} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={60} fill={P.mustard} opacity={clamp((lt - 1.4) * 3)}>{n} ПОЕЗДОК С АШОТОМ</text>
    </svg>
  );
};

// 8. Очередь в налоговую: Тимур в хвосте и стареет, пока стоит
export const SceneQueue: React.FC<{lt: number; dur: number}> = ({lt, dur}) => {
  const k = clamp(lt / dur), old = k > 0.55;
  const crowd = [RIDERS[4], RIDERS[1], RIDERS[5], RIDERS[3], RIDERS[4]];
  return (
    <svg viewBox="0 0 1080 1920">
      {sky('#A8B4C0', '#E2D6C6', 'qsky')}
      <Cam k={k} z0={1.0} z1={1.15} cx={300} cy={1000}>
        <TaxOffice x={900} y={1150} s={0.9} />
        <rect x={-200} y={1150} width={1500} height={800} fill="#B9B0A2" />
        {crowd.map((r, i) => <g key={i} transform={`translate(${760 - i * 120},${1290 + (i % 2) * 10}) scale(0.62)`}><RiderFigure r={r} e={emo({smile: 0, worry: 0.6, look: [0.6, 0]})} /></g>)}
        <g transform={`translate(150,1330) scale(0.75)`}><RiderFigure r={old ? TIM35 : TIM} e={emo({smile: 0, worry: 1, sweat: 1, look: [0.6, 0]})} /></g>
        {/* часы над очередью: стрелки бегут */}
        <g transform="translate(420,600)">
          <circle r={110} fill={P.cream} stroke={P.ink} strokeWidth={10} />
          <path d={`M0,0 L${Math.sin(lt * 9) * 80},${-Math.cos(lt * 9) * 80}`} stroke={P.ink} strokeWidth={10} strokeLinecap="round" />
          <path d={`M0,0 L${Math.sin(lt * 0.8) * 55},${-Math.cos(lt * 0.8) * 55}`} stroke={P.terracotta} strokeWidth={14} strokeLinecap="round" />
        </g>
      </Cam>
      <Tag text={old ? 'ВСЁ ЕЩЁ В ОЧЕРЕДИ…' : 'ОЧЕРЕДЬ В НАЛОГОВУЮ'} lt={old ? lt - dur * 0.55 : lt} />
    </svg>
  );
};

// 9. Личный кабинет в телефоне: справки ✓, заявление ✓, «Получить вычет» → «Зачислено +140 400 ₽»
export const ScenePhoneLK: React.FC<{lt: number; dur: number}> = ({lt, dur}) => {
  const c1 = after(lt, dur * 0.3, 0.2), c2 = after(lt, dur * 0.5, 0.2);
  const tap = dur * 0.72, pressed = lt > tap && lt < tap + 0.2;
  const note = pop(after(lt, tap + 0.35, 0.4));
  const hand = easeOut(after(lt, tap - 0.5, 0.45)) * (1 - easeOut(after(lt, tap + 0.3, 0.3)));
  const Row: React.FC<{y: number; text: string; on: number}> = ({y, text, on}) => (
    <g transform={`translate(0,${y})`}>
      <rect x={-250} y={-55} width={500} height={110} rx={24} fill={P.cream} stroke={P.ink} strokeWidth={5} />
      <text x={-215} y={14} fontFamily={F} fontWeight={800} fontSize={36} fill={P.ink}>{text}</text>
      <circle cx={190} cy={0} r={32} fill={on > 0 ? P.sage : '#DDD4C6'} stroke={P.ink} strokeWidth={5} />
      {on > 0 && <path d="M174,0 L186,14 L208,-12" fill="none" stroke={P.cream} strokeWidth={9} strokeLinecap="round" strokeLinejoin="round" opacity={on} />}
    </g>
  );
  return (
    <svg viewBox="0 0 1080 1920">
      <rect width={1080} height={1920} fill="#2A3A3A" />
      <g transform="translate(540,880)">
        <rect x={-320} y={-560} width={640} height={1120} rx={70} fill="#1D1A1F" stroke={P.ink} strokeWidth={14} />
        <rect x={-290} y={-520} width={580} height={1040} rx={46} fill="#EDE7DC" />
        <rect x={-290} y={-520} width={580} height={150} rx={46} fill={P.capDark} />
        <text y={-430} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={40} fill={P.cream}>ЛИЧНЫЙ КАБИНЕТ</text>
        <text y={-390} textAnchor="middle" fontFamily={F} fontWeight={700} fontSize={28} fill={P.cream} opacity={0.8}>налоговая</text>
        <Row y={-240} text="Справки из банка" on={c1} />
        <Row y={-100} text="Заявление" on={c2} />
        <g transform={`translate(0,80) scale(${pressed ? 0.94 : 1})`}>
          <rect x={-250} y={-65} width={500} height={130} rx={65} fill={pressed ? P.sageDark : P.sage} stroke={P.ink} strokeWidth={7} />
          <text y={16} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={46} fill={P.cream}>ПОЛУЧИТЬ ВЫЧЕТ</text>
        </g>
        {note > 0 && <g transform={`translate(0,300) scale(${note})`}>
          <rect x={-260} y={-90} width={520} height={180} rx={30} fill="#FFFDF6" stroke={P.sageDark} strokeWidth={8} />
          <text y={-24} textAnchor="middle" fontFamily={F} fontWeight={800} fontSize={36} fill={P.ink}>Зачислено на карту</text>
          <text y={50} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={64} fill={P.sageDark}>+140 400 ₽</text>
        </g>}
        {/* палец */}
        {hand > 0 && <g transform={`translate(${lerp(300, 60, hand)},${lerp(560, 140, hand)}) rotate(-20)`}>
          <rect x={-40} y={0} width={80} height={300} rx={40} fill={TIM.skin} stroke={P.ink} strokeWidth={8} />
          <path d="M-22,24 Q0,8 22,24" fill="none" stroke={P.ink} strokeWidth={5} opacity={0.5} />
        </g>}
      </g>
    </svg>
  );
};

// 10. Календарь назад: 2026 → 2016, ключи от квартиры — «вычет не сгорает»
export const SceneYearsBack: React.FC<{lt: number; dur: number}> = ({lt, dur}) => {
  const k = easeInOut(clamp((lt - 0.2) / Math.max(0.5, dur - 1.2)));
  const year = Math.round(lerp(2026, 2016, k));
  const done = k >= 1;
  return (
    <svg viewBox="0 0 1080 1920">
      <rect width={1080} height={1920} fill="#2A2238" />
      <g transform={`translate(540,760) rotate(${Math.sin(lt * 20) * (done ? 0 : 1.5)})`}>
        <rect x={-300} y={-330} width={600} height={660} rx={34} fill={P.cream} stroke={P.ink} strokeWidth={12} />
        <rect x={-300} y={-330} width={600} height={140} rx={34} fill={done ? P.sage : P.terracotta} stroke={P.ink} strokeWidth={12} />
        <text y={110} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={200} fill={P.ink}>{year}</text>
        {[-180, -60, 60, 180].map((x) => <rect key={x} x={x - 14} y={-360} width={28} height={70} rx={14} fill="#9A938C" stroke={P.ink} strokeWidth={5} />)}
      </g>
      {done && <g transform={`translate(820,1100) scale(${pop(after(lt, 0.2 + Math.max(0.5, dur - 1.2), 0.45))}) rotate(-20)`}>
        <circle cx={0} cy={-90} r={50} fill="none" stroke={P.gold} strokeWidth={22} />
        <path d="M-14,-40 L-14,120 L14,120 L14,90 L44,90 L44,62 L14,62 L14,-40Z" fill={P.gold} stroke={P.ink} strokeWidth={6} />
      </g>}
      <g transform={`translate(540,1240) scale(${done ? pop(after(lt, 0.3 + Math.max(0.5, dur - 1.2), 0.45)) : 0}) rotate(-3)`}>
        <rect x={-380} y={-70} width={760} height={140} rx={70} fill={P.sage} stroke={P.ink} strokeWidth={8} />
        <text y={24} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={60} fill={P.cream}>ВЫЧЕТ НЕ СГОРАЕТ</text>
      </g>
    </svg>
  );
};

// 11. Тимур звонит маме: телефон у уха, на экране «Мама», волны звонка
export const SceneCallMom: React.FC<{lt: number; dur: number}> = ({lt, dur}) => {
  const k = clamp(lt / dur);
  return (
    <svg viewBox="0 0 1080 1920">
      <rect width={1080} height={1920} fill="#E9C9A0" />
      {Array.from({length: 3}, (_, i) => {
        const r = ((lt * 300 + i * 160) % 480) + 60;
        return <circle key={i} cx={780} cy={700} r={r} fill="none" stroke={P.terracotta} strokeWidth={10} opacity={1 - r / 540} />;
      })}
      <Cam k={k} z0={1.05} z1={1.2} cx={540} cy={900}>
        <g transform="translate(470,1180) scale(1.7)"><RiderFigure r={TIM} e={emo({shock: 0.6, mouth: 3, smile: 0.4, look: [0.5, -0.2]})} /></g>
        <g transform="translate(760,760) rotate(14)">
          <rect x={-110} y={-200} width={220} height={400} rx={32} fill="#1D1A1F" stroke={P.ink} strokeWidth={9} />
          <rect x={-94} y={-180} width={188} height={360} rx={22} fill={P.cream} />
          <circle cy={-70} r={50} fill={P.terracotta} stroke={P.ink} strokeWidth={5} />
          <text y={-52} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={50} fill={P.cream}>М</text>
          <text y={40} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={44} fill={P.ink}>Мама</text>
          <circle cy={120} r={34} fill={P.sage} stroke={P.ink} strokeWidth={5} />
        </g>
      </Cam>
      <Tag text="СКИНЬ РОДИТЕЛЯМ" lt={lt} fill={P.terracotta} />
    </svg>
  );
};

// 12. Тизер серии 3: дверь такси открывается, тётя Люда: «Ашот, я кредит на шубу взяла!»
export const SceneTeaser: React.FC<{lt: number; dur: number}> = ({lt}) => {
  const door = easeOut(after(lt, 0.05, 0.35));
  const b = pop(after(lt, 0.45, 0.45));
  return (
    <svg viewBox="0 0 1080 1920">
      <NightStreet t={0} />
      <g transform="translate(560,1360) scale(1.7)"><RiderFigure r={LUDA} e={emo({smile: 1, mouth: 2, look: [-0.3, 0]})} /></g>
      {/* дверь такси открывается в сторону */}
      <g transform={`translate(${lerp(540, 1000, door)},0)`}>
        <rect x={-300} y={500} width={600} height={1100} rx={40} fill="#E9B23F" stroke={P.ink} strokeWidth={12} />
        <rect x={-250} y={560} width={500} height={380} rx={30} fill="#3B4A5A" stroke={P.ink} strokeWidth={9} />
      </g>
      {/* шуба: пушистый воротник */}
      {Array.from({length: 9}, (_, i) => <circle key={i} cx={420 + i * 32} cy={1440 + Math.sin(i) * 12} r={36} fill="#8A6A55" stroke={P.ink} strokeWidth={5} />)}
      <g transform={`translate(540,420) scale(${b}) rotate(-3)`}>
        <rect x={-430} y={-110} width={860} height={220} rx={50} fill={P.cream} stroke={P.ink} strokeWidth={9} />
        <path d="M-40,110 L0,180 L40,110Z" fill={P.cream} stroke={P.ink} strokeWidth={9} strokeLinejoin="round" />
        <rect x={-50} y={100} width={100} height={14} fill={P.cream} />
        <text y={-18} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={54} fill={P.ink}>Ашот, я кредит</text>
        <text y={54} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={54} fill={P.terracotta}>на шубу взяла!</text>
      </g>
      <g transform={`translate(540,1700) scale(${pop(after(lt, 0.9, 0.4))})`}>
        <rect x={-260} y={-55} width={520} height={110} rx={55} fill={P.mustard} stroke={P.ink} strokeWidth={8} />
        <text y={20} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={52} fill={P.ink}>СЕРИЯ 3 · СКОРО</text>
      </g>
    </svg>
  );
};
