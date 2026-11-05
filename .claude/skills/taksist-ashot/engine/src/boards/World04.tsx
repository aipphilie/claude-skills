import React from 'react';
import {P} from '../palette';
import {RiderFigure, KRISTINA, EMO, Emotion} from '../characters/Rider';
import {clamp, easeInOut, easeOut, lerp, pop} from '../lib';
import {Cam, Coin, Note, Tag, fmt} from './World';
import {CabinBack} from '../scene/Cabin';

// Сцены серии 4 «До зарплаты не хватает». Правила те же, что в World.tsx: 1080×1920, lt — сек от начала врезки,
// dur — длина врезки, важное в зоне x 56..922, y 250..1300 (ниже — субтитры).
// Кристина — KRISTINA[0] (вариант А, утверждён автором 2026-11-05).

const F = 'Rubik';
const after = (lt: number, a: number, d = 0.3) => clamp((lt - a) / d);
export const KRIS = KRISTINA[0];
const em = (e: Partial<Emotion>): Emotion => ({...EMO.calm, ...e});

const Plate: React.FC<{x: number; y: number; text: string; s?: number; rot?: number; fill?: string; color?: string; size?: number}> = ({x, y, text, s = 1, rot = 0, fill = P.terracotta, color = P.cream, size = 64}) => {
  const w = text.length * size * 0.62 + 90;
  return (
    <g transform={`translate(${x},${y}) rotate(${rot}) scale(${s})`}>
      <rect x={-w / 2} y={-size * 0.95} width={w} height={size * 1.9} rx={size * 0.5} fill={fill} stroke={P.ink} strokeWidth={8} />
      <text y={size * 0.36} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={size} fill={color}>{text}</text>
    </g>
  );
};

// Кристина на заднем сиденье крупно (эмоция, наклон вперёд)
export const ShotKristina: React.FC<{lt?: number; e?: Partial<Emotion>; lean?: number; phone?: boolean}> = ({lt = 1, e = {}, lean = 0, phone}) => (
  <svg viewBox="0 0 1080 1920">
    <g transform="translate(-260,-420) scale(1.5)"><CabinBack t={lt} /></g>
    <g transform={`translate(540,${1300 - lean * 110}) scale(${1.9 + lean * 0.4}) rotate(${lean * -4})`}><RiderFigure r={KRIS} e={em(e)} /></g>
    {phone && (
      <g transform={`translate(560,1080) rotate(-6) scale(${0.6 * pop(after(lt, 0, 0.35))})`}>
        <rect x={-210} y={-380} width={420} height={760} rx={56} fill="#1D1A1F" stroke={P.ink} strokeWidth={12} />
        <rect x={-184} y={-344} width={368} height={688} rx={38} fill={P.cream} />
        <text y={-200} textAnchor="middle" fontFamily={F} fontWeight={800} fontSize={44} fill="#8A7A70">БАЛАНС</text>
        <text y={-80} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={120} fill={P.terracotta}>312 ₽</text>
        <rect x={-160} y={20} width={320} height={130} rx={24} fill={P.beige} stroke={P.ink} strokeWidth={5} />
        <text y={74} textAnchor="middle" fontFamily={F} fontWeight={800} fontSize={36} fill={P.ink}>до зарплаты</text>
        <text y={128} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={50} fill={P.ink}>9 дней</text>
      </g>
    )}
  </svg>
);

// 1. Вывеска «ЗАЙМЫ · 0,8%» мигает неоном, трескается, вываливается «292% ГОДОВЫХ»
export const SceneLoanSign: React.FC<{lt: number; dur: number}> = ({lt, dur}) => {
  const crack = after(lt, dur * 0.45, 0.25), drop = easeOut(after(lt, dur * 0.55, 0.4));
  const flick = lt < dur * 0.45 ? (Math.sin(lt * 40) > -0.6 ? 1 : 0.35) : 1;
  return (
    <svg viewBox="0 0 1080 1920">
      <rect width={1080} height={1920} fill="#1E1A26" />
      <rect x={0} y={1250} width={1080} height={670} fill="#2B2530" />
      <Cam k={clamp(lt / dur)}>
        <rect x={140} y={500} width={800} height={760} fill="#3A3340" stroke={P.ink} strokeWidth={10} />
        <rect x={330} y={880} width={420} height={380} rx={10} fill="#5A4E5E" stroke={P.ink} strokeWidth={8} />
        <g opacity={flick}>
          <rect x={110} y={330} width={860} height={240} rx={30} fill="#2A1F2E" stroke="#FF5FA2" strokeWidth={10} />
          <text x={540} y={420} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={70} fill="#FF8FC0">ЗАЙМЫ</text>
          <text x={540 - crack * 40} y={530} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={110} fill="#FFE27A" transform={`rotate(${crack * -8} 540 500)`}>ВСЕГО 0,8%</text>
        </g>
        {crack > 0 && <path d="M520,360 L560,430 L520,480 L580,560" fill="none" stroke={P.cream} strokeWidth={8} strokeLinejoin="round" opacity={crack} />}
      </Cam>
      {drop > 0 && <Plate x={540} y={lerp(500, 820, drop)} text="292% ГОДОВЫХ" s={pop(drop)} rot={-4} size={86} />}
    </svg>
  );
};

// 2. Календарь 12 листов, с каждого в трубу МФО падает монета «2 400»
export const SceneLoanCalendar: React.FC<{lt: number; dur: number}> = ({lt, dur}) => {
  const n = Math.min(12, Math.floor(clamp(lt / (dur * 0.8)) * 12) + 1);
  const M = ['ЯНВ', 'ФЕВ', 'МАР', 'АПР', 'МАЙ', 'ИЮН', 'ИЮЛ', 'АВГ', 'СЕН', 'ОКТ', 'НОЯ', 'ДЕК'];
  return (
    <svg viewBox="0 0 1080 1920">
      <rect width={1080} height={1920} fill={P.cream} />
      {M.map((m, i) => {
        const x = 150 + (i % 4) * 195, y = 380 + Math.floor(i / 4) * 230, on = i < n;
        return (
          <g key={m} transform={`translate(${x},${y})`}>
            <rect x={-80} y={-90} width={160} height={180} rx={16} fill={on ? '#F3D9C7' : '#FFFBF2'} stroke={P.ink} strokeWidth={6} />
            <rect x={-80} y={-90} width={160} height={50} rx={14} fill={P.terracotta} stroke={P.ink} strokeWidth={6} />
            <text y={-52} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={34} fill={P.cream}>{m}</text>
            {on && <text y={44} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={40} fill={P.terracotta}>−2 400</text>}
          </g>
        );
      })}
      {/* труба МФО */}
      <rect x={880} y={1060} width={150} height={280} rx={20} fill="#7C6F86" stroke={P.ink} strokeWidth={8} />
      <text x={955} y={1215} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={42} fill={P.cream}>МФО</text>
      {Array.from({length: 3}, (_, i) => { const k = ((lt * 1.6 + i / 3) % 1); return <Coin key={i} x={lerp(700, 955, k)} y={lerp(1000, 1100, k * k)} r={34} rot={k * 300} o={1 - k * 0.3} />; })}
      <Plate x={400} y={1180} text="12 РАЗ В ГОД" s={pop(after(lt, dur * 0.5, 0.4))} rot={-3} size={70} />
    </svg>
  );
};

// 3. «НЕ КОФЕ» → «НЕ ДОСТАВКА»: стаканчик 300 ₽ перечёркнут, курьер с пакетом перечёркнут
export const SceneNotCoffee: React.FC<{lt: number; dur: number}> = ({lt, dur}) => {
  const half = dur * 0.55, second = lt > half;
  const x1 = after(lt, 0.4, 0.25), x2 = after(lt, half + 0.3, 0.25);
  return (
    <svg viewBox="0 0 1080 1920">
      <rect width={1080} height={1920} fill={second ? '#E3EBDD' : '#EFE0CC'} />
      {!second ? (
        <g transform={`translate(540,800) scale(${pop(after(lt, 0, 0.35))})`}>
          <path d="M-150,-260 L150,-260 L115,250 L-115,250Z" fill="#FFFBF2" stroke={P.ink} strokeWidth={10} strokeLinejoin="round" />
          <rect x={-170} y={-320} width={340} height={70} rx={20} fill="#6B4A3A" stroke={P.ink} strokeWidth={10} />
          <rect x={-140} y={-60} width={280} height={140} rx={16} fill={P.mustard} stroke={P.ink} strokeWidth={6} />
          <text y={34} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={70} fill={P.ink}>300 ₽</text>
          {[0, 1, 2].map((i) => <path key={i} d={`M${-60 + i * 60},-350 q-20,-50 0,-100`} fill="none" stroke="#C9BFB4" strokeWidth={10} strokeLinecap="round" opacity={0.7} />)}
        </g>
      ) : (
        <g transform={`translate(540,820) scale(${pop(after(lt, half, 0.35))})`}>
          <rect x={-200} y={-160} width={400} height={360} rx={30} fill={P.sage} stroke={P.ink} strokeWidth={10} />
          <path d="M-90,-160 Q-90,-280 0,-280 Q90,-280 90,-160" fill="none" stroke={P.ink} strokeWidth={14} />
          <text y={60} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={70} fill={P.cream}>ЗАКАЗ</text>
        </g>
      )}
      {(second ? x2 : x1) > 0 && <path d={`M260,${second ? 560 : 520} L${260 + 560 * (second ? x2 : x1)},${(second ? 560 : 520) + 560 * (second ? x2 : x1)}`} stroke={P.terracotta} strokeWidth={34} strokeLinecap="round" />}
      <Plate x={540} y={1240} text={second ? 'НЕ ДОСТАВКА' : 'НЕ КОФЕ'} s={pop(second ? x2 : x1)} rot={-3} size={80} />
    </svg>
  );
};

// 4. Таксометр «СЮРПРИЗЫ ГОДА»: три ступеньки 55 → 95 → 120, список трат сбоку, стоп-кадр на 120 000
export const SUR = [['🎄', 'праздники', 30000], ['🎒', 'школа', 25000], ['🦷', 'врачи', 20000], ['🧥', 'одежда', 20000], ['📱', 'телефон', 15000], ['🚆', 'к маме', 10000]] as const;
export const SceneSurprises: React.FC<{lt: number; dur: number; steps?: [number, number, number]}> = ({lt, dur, steps}) => {
  const st = steps || [dur * 0.08, dur * 0.42, dur * 0.76];
  const shown = st.filter((s) => lt >= s).length * 2;
  const val = SUR.slice(0, shown).reduce((a, x) => a + x[2], 0);
  const freeze = shown === 6 ? easeOut(after(lt, st[2] + 0.4, 0.5)) : 0;
  return (
    <svg viewBox="0 0 1080 1920">
      <rect width={1080} height={1920} fill="#231B18" />
      <g transform={`translate(540,580) scale(${1 + freeze * 0.12})`}>
        <rect x={-470} y={-260} width={940} height={520} rx={60} fill="#1E1816" stroke={P.ink} strokeWidth={14} />
        <text x={-400} y={-170} fontFamily={F} fontWeight={800} fontSize={44} fill="#8A7A70">ТАКСОМЕТР</text>
        <rect x={-420} y={-120} width={840} height={260} rx={30} fill="#3A1F14" />
        <text y={70} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={150} fill="#FF9A4A">{fmt(val)} ₽</text>
        <text y={215} textAnchor="middle" fontFamily={F} fontWeight={800} fontSize={46} fill={P.mustard}>СЮРПРИЗЫ ГОДА</text>
      </g>
      {SUR.map(([ic, name, v], i) => {
        const s = i < shown ? pop(after(lt, st[Math.floor(i / 2)] + (i % 2) * 0.25, 0.35)) : 0;
        return s > 0 && (
          <g key={name} transform={`translate(540,${960 + i * 66}) scale(${s})`} opacity={1 - freeze * 0.5}>
            <rect x={-360} y={-28} width={720} height={56} rx={28} fill={P.cream} stroke={P.ink} strokeWidth={5} />
            <circle cx={-325} cy={0} r={15} fill={[P.terracotta, P.mustard, P.sage][i % 3]} stroke={P.ink} strokeWidth={4} />
            <text x={-295} y={11} fontFamily={F} fontWeight={800} fontSize={32} fill={P.ink}>{name}</text>
            <text x={335} y={11} textAnchor="end" fontFamily={F} fontWeight={900} fontSize={32} fill={P.terracotta}>{fmt(v)} ₽</text>
          </g>
        );
      })}
      {freeze > 0 && <rect width={1080} height={1920} fill="none" stroke="#000" strokeWidth={240 * freeze} opacity={0.5} />}
    </svg>
  );
};

// 5. Метеорит падает у ёлки, на ёлке табличка «31 декабря · каждый год»
export const SceneMeteor: React.FC<{lt: number; dur: number}> = ({lt, dur}) => {
  const k = easeInOut(clamp(lt / (dur * 0.45))), boom = after(lt, dur * 0.45, 0.3);
  const mx = lerp(1000, 760, k), my = lerp(150, 1000, k);
  return (
    <svg viewBox="0 0 1080 1920">
      <rect width={1080} height={1920} fill="#1C2238" />
      {Array.from({length: 30}, (_, i) => <circle key={i} cx={(i * 197) % 1080} cy={(i * 131) % 900} r={3 + (i % 3)} fill={P.cream} opacity={0.6} />)}
      <rect x={0} y={1150} width={1080} height={770} fill="#E8EEF2" />
      <g transform="translate(400,1150)">
        {[0, 1, 2].map((i) => <path key={i} d={`M${-220 + i * 50},${-i * 220} L0,${-260 - i * 220} L${220 - i * 50},${-i * 220}Z`} fill="#4E7F52" stroke={P.ink} strokeWidth={8} strokeLinejoin="round" />)}
        <rect x={-30} y={0} width={60} height={70} fill="#6B4A3A" stroke={P.ink} strokeWidth={6} />
        <path d="M0,-740 l14,30 32,4 -24,22 6,32 -28,-16 -28,16 6,-32 -24,-22 32,-4Z" fill={P.mustard} stroke={P.ink} strokeWidth={5} />
        {[[-120, -60], [90, -120], [-60, -300], [70, -380], [-30, -520]].map(([x, y], i) => <circle key={i} cx={x} cy={y} r={20} fill={i % 2 ? P.terracotta : P.mustard} stroke={P.ink} strokeWidth={4} opacity={Math.sin(lt * 8 + i) > 0 ? 1 : 0.5} />)}
        <g transform={`translate(0,-200) rotate(-4) scale(${pop(after(lt, 0.1, 0.4))})`}>
          <rect x={-200} y={-60} width={400} height={120} rx={18} fill={P.cream} stroke={P.ink} strokeWidth={6} />
          <text y={-6} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={44} fill={P.terracotta}>31 ДЕКАБРЯ</text>
          <text y={40} textAnchor="middle" fontFamily={F} fontWeight={800} fontSize={34} fill={P.ink}>каждый год</text>
        </g>
      </g>
      {boom === 0 ? (
        <g>
          <path d={`M${mx},${my} L${mx + 180},${my - 260}`} stroke="#FF9A4A" strokeWidth={50} strokeLinecap="round" opacity={0.5} />
          <circle cx={mx} cy={my} r={60} fill="#8C6A55" stroke={P.ink} strokeWidth={8} />
        </g>
      ) : (
        <g transform={`translate(780,1130) scale(${pop(boom)})`}>
          <path d="M-200,0 L-120,-90 L-60,-30 L0,-160 L60,-30 L130,-100 L200,0Z" fill="#FF9A4A" stroke={P.ink} strokeWidth={8} strokeLinejoin="round" />
          <text y={-190} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={70} fill={P.mustard} stroke={P.ink} strokeWidth={8} paintOrder="stroke">БУМ</text>
        </g>
      )}
      <Plate x={540} y={300} text="ВНЕЗАПНО = МЕТЕОРИТ" s={pop(after(lt, dur * 0.5, 0.4))} rot={-3} size={54} fill={P.ink} />
    </svg>
  );
};

// 6. 120 000 ÷ 12 = 10 000, плашка-вопрос переворачивается в «ЭТО РАСПИСАНИЕ»
export const SceneDivide: React.FC<{lt: number; dur: number}> = ({lt, dur}) => {
  const eq = pop(after(lt, dur * 0.35, 0.4)), flip = after(lt, dur * 0.6, 0.35);
  const sy = Math.abs(Math.cos(flip * Math.PI));
  return (
    <svg viewBox="0 0 1080 1920">
      <rect width={1080} height={1920} fill={P.cream} />
      <text x={540} y={560} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={130} fill={P.ink}>120 000 ÷ 12</text>
      <g transform={`translate(540,820) scale(${eq})`}>
        <rect x={-380} y={-130} width={760} height={240} rx={40} fill={P.sage} stroke={P.ink} strokeWidth={10} />
        <text y={45} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={150} fill={P.cream}>= 10 000 ₽</text>
      </g>
      <g transform={`translate(540,1140) scale(1,${sy})`}>
        {flip < 0.5
          ? <Plate x={0} y={0} text="КУДА ИСЧЕЗАЮТ 10 000?" size={50} fill={P.ink} />
          : <Plate x={0} y={0} text="НЕ ИСЧЕЗАЮТ. ЭТО РАСПИСАНИЕ" size={46} fill={P.terracotta} />}
      </g>
    </svg>
  );
};

// 7. Монета «2 400», летевшая в МФО, разворачивается в конверт «СЮРПРИЗЫ»; конверт уезжает на счёт с замком
export const SceneEnvelope: React.FC<{lt: number; dur: number}> = ({lt, dur}) => {
  const turn = easeInOut(clamp(lt / (dur * 0.4)));
  const cx = lerp(300, 820, Math.min(turn, 0.45) / 0.45 * 0.5) * (turn < 0.45 ? 1 : 0) + (turn >= 0.45 ? lerp(560, 400, (turn - 0.45) / 0.55) : 0);
  const cy = turn < 0.45 ? lerp(700, 560, turn / 0.45) : lerp(560, 960, (turn - 0.45) / 0.55);
  const vault = pop(after(lt, dur * 0.55, 0.4));
  return (
    <svg viewBox="0 0 1080 1920">
      <rect width={1080} height={1920} fill="#E3EBDD" />
      <rect x={860} y={420} width={150} height={260} rx={20} fill="#7C6F86" stroke={P.ink} strokeWidth={8} opacity={0.6} />
      <text x={935} y={570} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={40} fill={P.cream} opacity={0.6}>МФО</text>
      {turn > 0.5 && <path d="M850,560 l-60,0" stroke={P.terracotta} strokeWidth={18} strokeLinecap="round" />}
      <g transform="translate(400,1060)">
        <rect x={-210} y={-130} width={420} height={260} rx={18} fill="#FFFBF2" stroke={P.ink} strokeWidth={9} />
        <path d="M-210,-130 L0,20 L210,-130" fill="none" stroke={P.ink} strokeWidth={9} strokeLinejoin="round" />
        <rect x={-160} y={40} width={320} height={64} rx={32} fill={P.mustard} stroke={P.ink} strokeWidth={6} />
        <text y={86} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={40} fill={P.ink}>СЮРПРИЗЫ</text>
      </g>
      <g transform={`translate(${cx},${cy}) scale(1.5)`}><Coin x={0} y={0} r={50} rot={turn * 360} /></g>
      <text x={cx} y={cy - 100} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={54} fill={P.ink}>2 400</text>
      <g transform={`translate(820,1120) scale(${vault})`}>
        <rect x={-150} y={-160} width={300} height={320} rx={30} fill="#9AA3AB" stroke={P.ink} strokeWidth={9} />
        <circle r={70} fill="#C9CFD4" stroke={P.ink} strokeWidth={8} />
        <path d="M-40,0 h80 M0,-40 v80" stroke={P.ink} strokeWidth={10} strokeLinecap="round" />
        {[0, 1, 2].map((i) => { const k = (lt * 0.9 + i / 3) % 1; return <Coin key={i} x={-90 + i * 90} y={-260 + k * 120} r={22} o={1 - k} />; })}
        <text y={230} textAnchor="middle" fontFamily={F} fontWeight={800} fontSize={34} fill={P.ink}>+ проценты</text>
      </g>
      <Plate x={540} y={360} text="2 400 СЕБЕ, А НЕ МФО" s={pop(after(lt, dur * 0.35, 0.4))} rot={-3} size={58} fill={P.sageDark} />
    </svg>
  );
};

// 8. Навигатор: маршрут уже развёрнут к «Дом», точка МФО позади и зачёркнута
export const SceneNavHome: React.FC<{lt: number; dur: number}> = ({lt, dur}) => {
  const k = easeOut(clamp(lt / (dur * 0.6)));
  return (
    <svg viewBox="0 0 1080 1920">
      <rect width={1080} height={1920} fill="#231B18" />
      <g transform="translate(540,880)">
        <rect x={-330} y={-560} width={660} height={1120} rx={70} fill="#1D1A1F" stroke={P.ink} strokeWidth={14} />
        <rect x={-300} y={-520} width={600} height={1040} rx={44} fill="#2C3440" />
        {[-200, -60, 80, 220].map((y) => <path key={y} d={`M-300,${y} L300,${y + 60}`} stroke="#3B4552" strokeWidth={26} />)}
        {[-150, 40, 190].map((x) => <path key={x} d={`M${x},-520 L${x + 40},520`} stroke="#3B4552" strokeWidth={26} />)}
        <path d="M0,380 Q-20,140 -140,0 Q-230,-120 -150,-300" fill="none" stroke="#5FB4FF" strokeWidth={22} strokeLinecap="round" strokeDasharray={`${1200 * k} 2000`} />
        <path d="M0,380 Q60,200 180,60" fill="none" stroke="#7C6F86" strokeWidth={16} strokeLinecap="round" strokeDasharray="20 24" opacity={0.7} />
        <g transform="translate(180,60)">
          <circle r={40} fill="#7C6F86" stroke={P.ink} strokeWidth={6} />
          <text y={-60} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={34} fill={P.cream}>МФО</text>
          <path d="M-50,-50 L50,50 M50,-50 L-50,50" stroke={P.terracotta} strokeWidth={14} strokeLinecap="round" />
        </g>
        <g transform="translate(-150,-300)">
          <path d="M0,-70 L-50,-20 L-34,-20 L-34,40 L34,40 L34,-20 L50,-20Z" fill={P.sage} stroke={P.ink} strokeWidth={6} strokeLinejoin="round" />
          <text y={100} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={44} fill={P.cream}>ДОМ</text>
        </g>
        <path d="M0,350 l-30,60 30,-14 30,14Z" fill={P.mustard} stroke={P.ink} strokeWidth={5} />
        <rect x={-260} y={-500} width={520} height={110} rx={24} fill={P.sageDark} />
        <text y={-428} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={46} fill={P.cream}>↰ Разворот · ДОМ</text>
      </g>
    </svg>
  );
};

// 9. Шпаргалка 5 сек
export const SceneCheat: React.FC<{lt: number; dur: number}> = ({lt}) => {
  const rows = ['Выпиши «внезапные» траты за год и раздели на 12', 'В день зарплаты — первым делом в конверт «сюрпризы» (начни с 2 400)', 'Займ 0,8% в день = 292% годовых'];
  return (
    <svg viewBox="0 0 1080 1920">
      <rect width={1080} height={1920} fill={P.mustard} />
      <text x={540} y={330} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={84} fill={P.ink}>ШПАРГАЛКА АШОТА</text>
      {rows.map((r, i) => (
        <g key={i} transform={`translate(80,${470 + i * 260}) scale(${pop(after(lt, 0.15 + i * 0.25, 0.35))})`}>
          <rect width={920} height={220} rx={36} fill={P.cream} stroke={P.ink} strokeWidth={8} />
          <circle cx={90} cy={110} r={54} fill={P.terracotta} stroke={P.ink} strokeWidth={6} />
          <text x={90} y={132} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={64} fill={P.cream}>{i + 1}</text>
          <foreignObject x={170} y={20} width={720} height={180}><div style={{fontFamily: F, fontWeight: 800, fontSize: 40, lineHeight: 1.2, color: P.ink, display: 'flex', alignItems: 'center', height: '100%'}}>{r}</div></foreignObject>
        </g>
      ))}
      <text x={540} y={1330} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={38} fill={P.ink}>Посчитай свои сюрпризы — пиши сумму в комменты</text>
    </svg>
  );
};
