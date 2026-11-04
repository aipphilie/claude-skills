import React from 'react';
import {P} from '../palette';
import {RiderFigure, RIDERS, EMO, Emotion} from '../characters/Rider';
import {clamp, easeInOut, easeOut, lerp, pop} from '../lib';

// Сцены ВНЕ такси (решение автора 2026-11-03: «чтобы не только такси, динамика до последнего кадра»).
// Каждая мысль Ашота уходит в свою сцену: банк, новостройка, деньги, пробка, платная дорога, свобода.
// Все сцены 1080×1920, принимают lt (сек от начала врезки) и dur (длина врезки). Важное в зоне x 56..922, y 250..1300
// (ниже — субтитры). Тимур — RIDERS[0], менеджер банка — RIDERS[5] (клерк).

const F = 'Rubik';
export const TIM = RIDERS[0], CLERK = RIDERS[5];
export const fmt = (n: number) => Math.round(n).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
export const emo = (e: Partial<Emotion>): Emotion => ({...EMO.calm, ...e});
const after = (lt: number, a: number, d = 0.3) => clamp((lt - a) / d);

// плашка-подпись места («ВЧЕРА · БАНК»)
export const Tag: React.FC<{text: string; lt: number; fill?: string; color?: string}> = ({text, lt, fill = P.ink, color = P.cream}) => {
  const w = text.length * 26 + 70;
  return (
    <g transform={`translate(${100 + w / 2},300) scale(${pop(after(lt, 0, 0.4))}) rotate(-3)`}>
      <rect x={-w / 2} y={-38} width={w} height={76} rx={38} fill={fill} stroke={P.cream} strokeWidth={5} />
      <text y={14} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={40} fill={color}>{text}</text>
    </g>
  );
};
export const Coin: React.FC<{x: number; y: number; r?: number; rot?: number; o?: number}> = ({x, y, r = 34, rot = 0, o = 1}) => (
  <g transform={`translate(${x},${y}) rotate(${rot})`} opacity={o}>
    <circle r={r} fill={P.gold} stroke={P.ink} strokeWidth={6} />
    <circle r={r * 0.72} fill="none" stroke={P.goldDark} strokeWidth={4} />
    <text y={r * 0.38} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={r * 1.05} fill={P.goldDark}>₽</text>
  </g>
);
export const Note: React.FC<{x: number; y: number; s?: number; rot?: number; v?: string; o?: number}> = ({x, y, s = 1, rot = 0, v = '5000', o = 1}) => (
  <g transform={`translate(${x},${y}) rotate(${rot}) scale(${s})`} opacity={o}>
    <rect x={-120} y={-58} width={240} height={116} rx={12} fill="#E9A06B" stroke={P.ink} strokeWidth={6} />
    <rect x={-104} y={-42} width={208} height={84} rx={8} fill="none" stroke="#B56E40" strokeWidth={4} />
    <circle cx={-50} cy={0} r={26} fill="#F2C49A" stroke="#B56E40" strokeWidth={4} />
    <text x={52} y={16} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={42} fill="#7A3E1E">{v}</text>
  </g>
);
export const sky = (top: string, bot: string, id: string) => (
  <>
    <defs><linearGradient id={id} x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor={top} /><stop offset="1" stopColor={bot} /></linearGradient></defs>
    <rect width={1080} height={1920} fill={`url(#${id})`} />
  </>
);
// «камера» сцены: медленный наезд + лёгкий сдвиг
export const Cam: React.FC<{k: number; z0?: number; z1?: number; cx?: number; cy?: number; children: React.ReactNode}> = ({k, z0 = 1, z1 = 1.12, cx = 540, cy = 900, children}) => {
  const z = lerp(z0, z1, easeInOut(k));
  return <g transform={`translate(${cx},${cy}) scale(${z}) translate(${-cx},${-cy})`}>{children}</g>;
};

// 1. ФЛЕШБЭК: банк, менеджер с размаху ставит штамп «ОДОБРЕНО», Тимур счастлив
export const SceneBankStamp: React.FC<{lt: number; dur: number}> = ({lt, dur}) => {
  const k = clamp(lt / dur);
  const st = after(lt, 0.35, 0.18);                       // удар штампа
  const up = lt < 0.35 ? -160 * easeOut(lt / 0.35) : -160 * (1 - st) + (lt > 0.6 ? -60 * after(lt, 0.6, 0.3) : 0);
  const shake = lt > 0.53 && lt < 0.8 ? Math.sin(lt * 90) * 10 * (0.8 - lt) * 4 : 0;
  return (
    <svg viewBox="0 0 1080 1920">
      <Cam k={k} z0={1.02} z1={1.14} cy={950}>
        <g transform={`translate(${shake},0)`}>
          <rect width={1080} height={1920} fill="#DCD3C4" />
          {/* стена банка: панели, логотип-абстракция, окно с городом */}
          {[0, 1, 2, 3].map((i) => <rect key={i} x={i * 280 - 20} y={0} width={260} height={1100} fill={i % 2 ? '#D2C8B8' : '#DCD3C4'} />)}
          <g transform="translate(780,330)"><circle r={90} fill={P.sage} stroke={P.ink} strokeWidth={8} /><text y={30} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={84} fill={P.cream}>Б</text></g>
          <text x={780} y={480} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={44} fill={P.ink}>ИПОТЕКА 11%</text>
          {/* менеджер слева, Тимур справа */}
          <g transform="translate(300,1010) scale(1.05)"><RiderFigure r={CLERK} e={emo({smile: 0.9, mouth: lt > 0.55 ? 2 : 0, look: [0.6, 0.2]})} /></g>
          <g transform="translate(800,1040) scale(1.05)"><RiderFigure r={TIM} e={emo({smile: lt > 0.55 ? 1 : 0.5, shock: lt > 0.55 ? 0.35 : 0, look: [-0.6, 0.4]})} /></g>
          {/* стол */}
          <path d="M-40,1180 L1120,1180 L1120,1920 L-40,1920Z" fill="#7A5A44" stroke={P.ink} strokeWidth={10} />
          <path d="M-40,1180 L1120,1180 L1120,1220 L-40,1220Z" fill="#94704F" stroke={P.ink} strokeWidth={8} />
          {/* договор */}
          <g transform="translate(560,1130) rotate(-4)">
            <rect x={-220} y={-170} width={440} height={300} rx={12} fill="#FFFDF6" stroke={P.ink} strokeWidth={7} />
            <text y={-110} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={40} fill={P.ink}>ДОГОВОР</text>
            {[0, 1, 2, 3].map((i) => <rect key={i} x={-170} y={-80 + i * 34} width={340 - (i % 2) * 90} height={12} rx={6} fill="#CFC6B8" />)}
            <text y={90} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={34} fill={P.ink}>5 000 000 ₽ · 20 лет</text>
            {st > 0 && <g transform={`rotate(-10) scale(${lerp(1.5, 1, easeOut(st))})`} opacity={clamp(st * 3)}>
              <rect x={-190} y={-70} width={380} height={110} rx={14} fill="none" stroke={P.sageDark} strokeWidth={10} />
              <text y={10} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={66} fill={P.sageDark}>ОДОБРЕНО</text>
            </g>}
          </g>
          {/* рука со штампом */}
          <g transform={`translate(520,${1010 + up})`}>
            <rect x={-60} y={-180} width={120} height={150} rx={30} fill="#5A4136" stroke={P.ink} strokeWidth={8} />
            <rect x={-90} y={-40} width={180} height={50} rx={10} fill="#3E3A40" stroke={P.ink} strokeWidth={8} />
            <path d="M-40,-180 Q-60,-260 0,-300 Q60,-260 40,-180Z" fill={CLERK.skin} stroke={P.ink} strokeWidth={8} />
            <path d="M-46,-300 L-56,-560 L56,-560 L46,-300Z" fill={CLERK.c1} stroke={P.ink} strokeWidth={8} />
            <rect x={-54} y={-330} width={108} height={40} rx={8} fill={CLERK.c2} stroke={P.ink} strokeWidth={6} />
          </g>
          {/* искры удара */}
          {lt > 0.52 && lt < 1.1 && Array.from({length: 8}, (_, i) => {
            const a = (i / 8) * Math.PI * 2, r = 230 + after(lt, 0.52, 0.4) * 120;
            return <path key={i} d={`M${560 + Math.cos(a) * r},${1100 + Math.sin(a) * r * 0.6} l${Math.cos(a) * 50},${Math.sin(a) * 30}`} stroke={P.mustard} strokeWidth={14} strokeLinecap="round" opacity={1 - after(lt, 0.52, 0.6)} />;
          })}
        </g>
      </Cam>
      <rect width={1080} height={1920} fill="#C9A56A" opacity={0.12} />
      <Tag text="ВЧЕРА · БАНК" lt={lt} />
    </svg>
  );
};

// 2. Новостройка: Тимур с ключами; камера отъезжает — за одной квартирой «две с половиной» (k2: 0..1)
export const SceneNewBuilding: React.FC<{lt: number; dur: number; split?: number}> = ({lt, dur, split = 0.5}) => {
  const k = clamp(lt / dur);
  const kk = easeInOut(clamp((k - split) / (1 - split)));   // вторая половина: появляются «ещё полторы»
  const z = lerp(1.15, 0.86, kk);
  const jiggle = Math.sin(lt * 14) * 6;
  const Tower: React.FC<{x: number; w: number; h: number; c: string; lit?: number; o?: number; ghost?: boolean}> = ({x, w, h, c, lit = -1, o = 1, ghost}) => (
    <g opacity={o}>
      <rect x={x - w / 2} y={1250 - h} width={w} height={h} fill={ghost ? 'none' : c} stroke={ghost ? P.terracotta : P.ink} strokeWidth={ghost ? 10 : 9} strokeDasharray={ghost ? '30 20' : undefined} />
      {!ghost && Array.from({length: Math.floor(h / 90) * 4}, (_, i) => {
        const cx = x - w / 2 + 30 + (i % 4) * ((w - 60) / 3.3), cy = 1250 - h + 40 + Math.floor(i / 4) * 90;
        return <rect key={i} x={cx} y={cy} width={44} height={50} rx={6} fill={i === lit ? P.win : '#8FA9C0'} stroke={P.ink} strokeWidth={4} />;
      })}
    </g>
  );
  return (
    <svg viewBox="0 0 1080 1920">
      {sky('#9CC8E8', '#F6E2C4', 'nbsky')}
      <circle cx={860} cy={360} r={80} fill="#FFE8A8" opacity={0.9} />
      <g transform={`translate(540,1100) scale(${z}) translate(-540,-1100)`}>
        {/* краны стройки */}
        <path d="M150,1250 L150,420 M150,440 L520,440 M150,440 L60,440" stroke="#E0A030" strokeWidth={16} />
        <path d="M480,440 L480,560" stroke={P.ink} strokeWidth={5} />
        <Tower x={lerp(540, 300, kk)} w={300} h={760} c="#EFE6D8" lit={9} />
        {/* ещё полторы башни, которые «отдашь» */}
        <Tower x={640} w={300} h={760} c="#EFE6D8" o={kk} ghost />
        <Tower x={890} w={150} h={760} c="#EFE6D8" o={kk} ghost />
        {kk > 0.3 && <g opacity={clamp((kk - 0.3) * 3)}>
          <text x={300} y={440} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={60} fill={P.sageDark}>ТВОЯ</text>
          <text x={720} y={440} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={60} fill={P.terracotta}>+1,5 БАНКУ</text>
        </g>}
        <rect x={-600} y={1250} width={2280} height={700} fill="#B9B0A2" />
        <path d="M-600,1250 L1680,1250" stroke={P.ink} strokeWidth={8} />
      </g>
      {/* Тимур на переднем плане с ключами */}
      <g transform={`translate(300,${1430 + kk * 60}) scale(1.25)`}><RiderFigure r={TIM} e={emo({smile: 1 - kk, worry: kk * 0.8, shock: kk * 0.5, look: [0.5, -0.5]})} /></g>
      <g transform={`translate(560,${1060 + jiggle}) rotate(${jiggle * 2})`} opacity={1 - kk * 0.5}>
        <path d="M0,-80 L0,0" stroke="#9A938C" strokeWidth={6} />
        <circle cx={0} cy={-100} r={26} fill="none" stroke="#C9C2B4" strokeWidth={10} />
        <path d="M-10,0 L-10,90 L10,90 L10,60 L26,60 L26,40 L10,40 L10,0Z" fill={P.gold} stroke={P.ink} strokeWidth={5} />
        <rect x={-40} y={-40} width={50} height={40} rx={8} fill={P.terracotta} stroke={P.ink} strokeWidth={4} />
      </g>
      <Tag text={kk > 0.3 ? 'ОДНУ ПОЛУЧИШЬ · 2,5 ОТДАШЬ' : 'НОВОСТРОЙКА'} lt={lt} fill={kk > 0.3 ? P.terracotta : P.ink} />
    </svg>
  );
};

// 3. Банк снаружи: «сдаёт деньги в аренду» — мешки с деньгами на ценниках «В АРЕНДУ»
export const SceneBankRent: React.FC<{lt: number; dur: number}> = ({lt, dur}) => {
  const k = clamp(lt / dur);
  return (
    <svg viewBox="0 0 1080 1920">
      {sky('#3E3460', '#C9876A', 'brsky')}
      <Cam k={k} z0={1.18} z1={1.0} cy={800}>
        {/* фасад с колоннами */}
        <path d="M120,560 L540,330 L960,560Z" fill={P.cream} stroke={P.ink} strokeWidth={10} strokeLinejoin="round" />
        <text x={540} y={520} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={70} fill={P.ink}>БАНК</text>
        <rect x={140} y={560} width={800} height={60} fill={P.beige} stroke={P.ink} strokeWidth={8} />
        {[0, 1, 2, 3, 4].map((i) => <rect key={i} x={180 + i * 160} y={620} width={70} height={480} fill={P.cream} stroke={P.ink} strokeWidth={8} />)}
        <rect x={100} y={1100} width={880} height={70} fill={P.beige} stroke={P.ink} strokeWidth={8} />
        {/* вывеска «АРЕНДА ДЕНЕГ» */}
        <g transform={`translate(540,700) rotate(${Math.sin(lt * 4) * 3})`}>
          <path d="M-200,-90 L-200,-140 M200,-90 L200,-140" stroke={P.ink} strokeWidth={6} />
          <rect x={-300} y={-90} width={600} height={130} rx={20} fill={P.mustard} stroke={P.ink} strokeWidth={8} />
          <text y={0} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={66} fill={P.ink}>АРЕНДА ДЕНЕГ</text>
        </g>
      </Cam>
      {/* мешки с деньгами выезжают с ценниками */}
      {[0, 1, 2].map((i) => {
        const a = after(lt, 0.2 + i * 0.25, 0.5);
        const x = lerp(1250, 250 + i * 290, easeOut(a));
        return (
          <g key={i} transform={`translate(${x},1060) rotate(${(1 - a) * 20})`}>
            <path d="M-90,60 Q-110,-60 -40,-90 L40,-90 Q110,-60 90,60 Q0,90 -90,60Z" fill="#CDB07A" stroke={P.ink} strokeWidth={8} />
            <path d="M-40,-90 Q0,-130 40,-90" fill="none" stroke={P.ink} strokeWidth={8} />
            <text y={30} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={70} fill="#7A5A2A">₽</text>
            <g transform="translate(60,-80) rotate(18)"><rect x={-10} y={-24} width={150} height={48} rx={10} fill={P.cream} stroke={P.ink} strokeWidth={5} /><text x={65} y={11} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={26} fill={P.terracotta}>11%/год</text></g>
          </g>
        );
      })}
    </svg>
  );
};

// 4. «11 ₽ с каждой сотни»: сотка, из неё каждый год отлетают 11 монет в окно банка
export const SceneHundred: React.FC<{lt: number; dur: number}> = ({lt, dur}) => {
  const k = clamp(lt / dur);
  return (
    <svg viewBox="0 0 1080 1920">
      <rect width={1080} height={1920} fill="#2A2238" />
      {Array.from({length: 14}, (_, i) => <circle key={i} cx={(i * 173) % 1080} cy={(i * 311) % 1300 + 200} r={90} fill={P.mustard} opacity={0.04} />)}
      <Cam k={k} z0={1} z1={1.1} cy={760}>
        <g transform={`translate(380,820) rotate(-6) scale(${pop(after(lt, 0, 0.4)) * 2.2})`}>
          <rect x={-120} y={-58} width={240} height={116} rx={12} fill="#B9C9A8" stroke={P.ink} strokeWidth={4} />
          <rect x={-104} y={-42} width={208} height={84} rx={8} fill="none" stroke="#6E8A5A" strokeWidth={3} />
          <text x={40} y={22} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={60} fill="#3E5A2E">100</text>
        </g>
        {/* окошко банка справа */}
        <g transform="translate(880,520)">
          <rect x={-120} y={-150} width={240} height={300} rx={20} fill="#3E3A50" stroke={P.cream} strokeWidth={8} />
          <rect x={-90} y={-60} width={180} height={180} rx={10} fill="#1C1828" />
          <text y={-90} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={44} fill={P.cream}>БАНК</text>
        </g>
        {Array.from({length: 11}, (_, i) => {
          const a = after(lt, 0.25 + i * 0.12, 0.6);
          if (a <= 0) return null;
          const x = lerp(470, 880, easeInOut(a)), y = lerp(820, 560, a) - Math.sin(a * Math.PI) * 260;
          return <Coin key={i} x={x} y={y} r={30} rot={a * 400} o={a < 1 ? 1 : 0} />;
        })}
        <text x={540} y={1180} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={84} fill={P.mustard}>
          {fmt(Math.min(11, Math.floor(after(lt, 0.25, 1.32) * 11.99)))} ₽ банку
        </text>
      </Cam>
    </svg>
  );
};

// 5. Пицца-платёж: огромный кусок «ПРОЦЕНТЫ» уезжает к банку, тонкий «ДОЛГ» остаётся
export const ScenePizza: React.FC<{lt: number; dur: number}> = ({lt, dur}) => {
  const k = clamp(lt / dur);
  const cut = easeOut(after(lt, dur * 0.45, 0.5));
  const R = 330, cx = 540, cy = 860, a0 = -Math.PI / 2, aD = (2 * Math.PI) * (5776 / 51609); // доля долга в первом платеже
  const arc = (from: number, to: number) => `M0,0 L${Math.cos(from) * R},${Math.sin(from) * R} A${R},${R} 0 ${to - from > Math.PI ? 1 : 0} 1 ${Math.cos(to) * R},${Math.sin(to) * R}Z`;
  return (
    <svg viewBox="0 0 1080 1920">
      <rect width={1080} height={1920} fill="#3A2A22" />
      <ellipse cx={540} cy={1000} rx={480} ry={140} fill="#2A1E19" />
      <text x={540} y={380} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={80} fill={P.cream}>ПЛАТЁЖ 51 609 ₽</text>
      <g transform={`translate(${cx},${cy}) rotate(${(1 - easeOut(after(lt, 0, 0.6))) * -90})`}>
        <circle r={R + 30} fill="#E8D8C0" stroke={P.ink} strokeWidth={8} />
        {/* кусок процентов уезжает вправо-вверх */}
        <g transform={`translate(${cut * 330},${-cut * 120}) rotate(${cut * 12})`}>
          <path d={arc(a0 + aD, a0 + 2 * Math.PI)} fill={P.terracotta} stroke={P.ink} strokeWidth={8} />
          {Array.from({length: 9}, (_, i) => { const a = a0 + aD + 0.4 + i * 0.6, r = 110 + (i % 3) * 70; return <circle key={i} cx={Math.cos(a) * r} cy={Math.sin(a) * r} r={30} fill="#E3B04B" stroke={P.ink} strokeWidth={5} />; })}
        </g>
        <path d={arc(a0, a0 + aD)} fill={P.sage} stroke={P.ink} strokeWidth={8} transform={`translate(${-cut * 60},${-cut * 30})`} />
      </g>
      <g opacity={cut}>
        <g transform="translate(760,1260)"><rect x={-260} y={-50} width={520} height={100} rx={50} fill={P.terracotta} stroke={P.ink} strokeWidth={7} /><text y={18} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={50} fill={P.cream}>46 000 → БАНКУ</text></g>
        <g transform="translate(300,1260)"><rect x={-200} y={-50} width={400} height={100} rx={50} fill={P.sage} stroke={P.ink} strokeWidth={7} /><text y={18} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={50} fill={P.cream}>6 000 → ДОЛГ</text></g>
      </g>
    </svg>
  );
};

// 6. Две стопки денег за первый год: «546 000 → банку» растёт, «73 000 → долг» еле видно
export const SceneStacks: React.FC<{lt: number; dur: number}> = ({lt, dur}) => {
  const k = easeOut(clamp(lt / (dur * 0.7)));
  const n1 = Math.round(18 * k), n2 = Math.round(3 * clamp((lt - 0.5) / (dur * 0.5)));
  const stack = (x: number, n: number, c: string) => Array.from({length: n}, (_, i) => (
    <g key={i} transform={`translate(${x + Math.sin(i * 2.1) * 8},${1180 - i * 46})`}>
      <rect x={-150} y={-24} width={300} height={48} rx={8} fill={c} stroke={P.ink} strokeWidth={6} />
      <rect x={-30} y={-24} width={60} height={48} fill={P.cream} opacity={0.6} />
    </g>
  ));
  return (
    <svg viewBox="0 0 1080 1920">
      <rect width={1080} height={1920} fill="#2E2630" />
      <rect x={0} y={1205} width={1080} height={715} fill="#4A3B36" />
      <text x={540} y={330} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={70} fill={P.cream}>ЗА 1-Й ГОД: {fmt(619000 * k)} ₽</text>
      {stack(330, n1, '#E9A06B')}
      {stack(780, n2, '#9FD18A')}
      <text x={330} y={1290} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={50} fill={P.terracotta}>546 000 БАНКУ</text>
      <text x={780} y={1290} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={50} fill={P.sage}>73 000 В ДОЛГ</text>
    </svg>
  );
};

// 7. Пробка: вид сзади на стоящие машины, стоп-сигналы, а таксометр бешено тикает
export const SceneJam: React.FC<{lt: number; dur: number}> = ({lt, dur}) => {
  const k = clamp(lt / dur);
  const v = 287 + lt * 900;
  const car = (x: number, y: number, s: number, c: string, i: number) => (
    <g key={i} transform={`translate(${x},${y}) scale(${s})`}>
      <rect x={-150} y={-120} width={300} height={170} rx={30} fill={c} stroke={P.ink} strokeWidth={8} />
      <rect x={-110} y={-180} width={220} height={80} rx={20} fill="#2C2840" stroke={P.ink} strokeWidth={8} />
      {[-1, 1].map((sd) => <rect key={sd} x={sd * 110 - 22} y={-90} width={44} height={30} rx={8} fill="#FF4A3A" opacity={0.7 + 0.3 * Math.sin(lt * 8 + i)} />)}
      <rect x={-50} y={-30} width={100} height={30} rx={4} fill={P.cream} stroke={P.ink} strokeWidth={4} />
    </g>
  );
  return (
    <svg viewBox="0 0 1080 1920">
      {sky('#2C2342', '#6B3F57', 'jamsky')}
      <rect x={0} y={760} width={1080} height={1160} fill="#3A3346" />
      <Cam k={k} z0={1} z1={1.08} cy={900}>
        {[[200, 820, 0.45], [520, 830, 0.45], [860, 820, 0.45], [120, 960, 0.7], [560, 980, 0.7], [980, 960, 0.7], [300, 1200, 1.05], [800, 1220, 1.05]].map(([x, y, s], i) => car(x, y, s, ['#C8553D', '#8FA57E', '#B9C6CF', '#E9E2D6', '#6B5A4A', '#B5677A', '#8F7FB0', '#D8C27A'][i], i))}
      </Cam>
      <g transform={`translate(540,470) rotate(${Math.sin(lt * 30) * 1.5})`}>
        <rect x={-330} y={-110} width={660} height={220} rx={30} fill="#1E1816" stroke={P.ink} strokeWidth={10} />
        <rect x={-300} y={-80} width={600} height={160} rx={20} fill="#3A1F14" />
        <text y={36} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={100} fill="#FF9A4A">{fmt(v)} ₽</text>
      </g>
      <text x={540} y={680} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={44} fill={P.cream}>СЧЁТЧИК ТИКАЕТ · МАШИНА СТОИТ</text>
    </svg>
  );
};

// 8. Платная дорога: обычная монета застревает у шлагбаума «ПРОЦЕНТЫ», досрочная летит по выделенке к «ДОЛГУ»
export const SceneToll: React.FC<{lt: number; dur: number}> = ({lt, dur}) => {
  const a = easeInOut(clamp(lt / (dur * 0.8)));
  const bar = lt > dur * 0.2 ? Math.min(1, (lt - dur * 0.2) / 0.3) : 0;
  return (
    <svg viewBox="0 0 1080 1920">
      {sky('#6FA8D8', '#F2DDB8', 'tlsky')}
      <path d="M0,1000 L1080,1000 L1080,1920 L0,1920Z" fill="#5E566A" />
      {/* полосы */}
      <path d="M540,1000 L540,1920" stroke={P.cream} strokeWidth={10} strokeDasharray="50 40" />
      <path d="M0,1000 L1080,1000" stroke={P.ink} strokeWidth={8} />
      {/* будка «ПРОЦЕНТЫ» и шлагбаум слева */}
      <g transform="translate(160,980)">
        <rect x={-90} y={-260} width={180} height={260} fill={P.terracotta} stroke={P.ink} strokeWidth={8} />
        <rect x={-110} y={-300} width={220} height={60} fill={P.cream} stroke={P.ink} strokeWidth={8} />
        <text y={-256} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={34} fill={P.terracotta}>ПРОЦЕНТЫ</text>
        <g transform={`translate(90,-120) rotate(${-bar * 0})`}><rect x={0} y={-14} width={360} height={28} rx={14} fill={P.cream} stroke={P.ink} strokeWidth={6} />{[0, 1, 2].map((i) => <rect key={i} x={40 + i * 110} y={-14} width={50} height={28} fill={P.terracotta} />)}</g>
      </g>
      {/* выделенка справа «ДОСРОЧКА» */}
      <g transform="translate(810,980)">
        <rect x={-150} y={-90} width={300} height={70} rx={20} fill={P.sage} stroke={P.ink} strokeWidth={7} />
        <text y={-42} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={38} fill={P.cream}>ДОСРОЧКА</text>
      </g>
      {/* цель — «ДОЛГ» вдали */}
      <g transform="translate(810,560)"><rect x={-130} y={-60} width={260} height={120} rx={24} fill={P.cream} stroke={P.ink} strokeWidth={8} /><text y={20} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={56} fill={P.ink}>ДОЛГ</text></g>
      {/* монеты */}
      <Coin x={lerp(300, 330, a)} y={lerp(1700, 1080, Math.min(a, 0.7) / 0.7)} r={60} rot={a * 200} />
      <Coin x={lerp(800, 810, a)} y={lerp(1700, 640, a)} r={lerp(70, 34, a)} rot={a * 720} />
      {a > 0.55 && <text x={300} y={1240} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={46} fill={P.cream} opacity={clamp((a - 0.55) * 4)}>застряла</text>}
      {[0, 1, 2].map((i) => <path key={i} d={`M${790 + i * 20},${lerp(1760, 700, a) + 60} l0,${80 + i * 20}`} stroke={P.cream} strokeWidth={8} strokeLinecap="round" opacity={0.6} />)}
    </svg>
  );
};

// 9. «Где взять десятку?» — Тимур и копилка, купюры прилетают по одной: +10 000 ₽/мес
export const ScenePiggy: React.FC<{lt: number; dur: number}> = ({lt, dur}) => {
  const k = clamp(lt / dur);
  return (
    <svg viewBox="0 0 1080 1920">
      {sky('#F3D9B0', '#E6B98A', 'pgsky')}
      <Cam k={k} z0={1} z1={1.1} cy={900}>
        <g transform="translate(760,1300) scale(1.1)"><RiderFigure r={TIM} e={emo({smile: 0.8, look: [-0.6, 0.3]})} /></g>
        <g transform={`translate(380,1010) scale(${1 + Math.sin(lt * 10) * 0.02})`}>
          <ellipse rx={230} ry={180} fill="#F0A8B0" stroke={P.ink} strokeWidth={10} />
          <circle cx={-200} cy={-10} r={60} fill="#F0A8B0" stroke={P.ink} strokeWidth={8} />
          <circle cx={-215} cy={-10} r={8} fill={P.ink} /><circle cx={-185} cy={-10} r={8} fill={P.ink} />
          <circle cx={-60} cy={-80} r={14} fill={P.ink} />
          <rect x={-40} y={-185} width={120} height={20} rx={10} fill={P.ink} />
          {[-140, -40, 60, 150].map((x) => <rect key={x} x={x - 25} y={150} width={50} height={70} rx={14} fill="#F0A8B0" stroke={P.ink} strokeWidth={8} />)}
        </g>
        {[0, 1, 2, 3].map((i) => {
          const a = after(lt, 0.15 + i * 0.4, 0.45);
          if (a <= 0 || a >= 1) return null;
          return <Note key={i} x={lerp(700 - i * 60, 400, a)} y={lerp(300, 830, easeInOut(a))} s={0.8} rot={(1 - a) * 40 - 10} v="10 000" />;
        })}
      </Cam>
      <text x={540} y={420} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={56} fill={P.ink}>+10 000 ₽ КАЖДЫЙ МЕСЯЦ</text>
    </svg>
  );
};

// 10. Две полоски экономии: «на платёж −1,6 млн» и «на срок −3,2 млн» (вдвое длиннее)
export const SceneBars: React.FC<{lt: number; dur: number}> = ({lt, dur}) => {
  const a = easeOut(after(lt, 0.15, 0.7)), b = easeOut(after(lt, dur * 0.45, 0.8));
  return (
    <svg viewBox="0 0 1080 1920">
      <rect width={1080} height={1920} fill="#231B18" />
      <text x={540} y={380} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={66} fill={P.cream}>ТЕ ЖЕ +10 000 ₽ / МЕС</text>
      <g transform="translate(110,620)">
        <text y={-30} fontFamily={F} fontWeight={800} fontSize={48} fill={P.cream}>на ПЛАТЁЖ</text>
        <rect y={0} width={860} height={120} rx={30} fill="#3A2E2A" />
        <rect y={0} width={430 * a} height={120} rx={30} fill={P.mustard} stroke={P.ink} strokeWidth={6} />
        <text x={460} y={84} fontFamily={F} fontWeight={900} fontSize={64} fill={P.mustard} opacity={a}>−1,6 млн</text>
      </g>
      <g transform="translate(110,960)">
        <text y={-30} fontFamily={F} fontWeight={800} fontSize={48} fill={P.cream}>на СРОК</text>
        <rect y={0} width={860} height={160} rx={36} fill="#3A2E2A" />
        <rect y={0} width={860 * b} height={160} rx={36} fill={P.sage} stroke={P.ink} strokeWidth={6} />
        <text x={430} y={110} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={84} fill={P.cream} opacity={b}>−3,2 млн</text>
      </g>
      {b > 0.8 && <g transform={`translate(800,840) rotate(-10) scale(${pop(after(lt, dur * 0.45 + 0.6, 0.4))})`}><circle r={80} fill={P.terracotta} stroke={P.ink} strokeWidth={7} /><text y={26} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={70} fill={P.cream}>×2</text></g>}
    </svg>
  );
};

// 11. Календарь: листки 2046 → 2039 сгорают — «каждый вырезанный год — год без процентов»
export const SceneCalendar: React.FC<{lt: number; dur: number}> = ({lt, dur}) => {
  const n = 8;
  return (
    <svg viewBox="0 0 1080 1920">
      <rect width={1080} height={1920} fill="#2A2238" />
      {Array.from({length: n}, (_, i) => {
        const year = 2046 - i;
        const a = after(lt, 0.2 + i * (dur - 0.8) / n, 0.45);
        const x = 540 + (i - 3.5) * 14, y = 820 + i * 10;
        return (
          <g key={i} transform={`translate(${x + a * (i % 2 ? 300 : -300)},${y - a * 500}) rotate(${a * (i % 2 ? 40 : -40)})`} opacity={1 - a}>
            <rect x={-260} y={-300} width={520} height={600} rx={30} fill={P.cream} stroke={P.ink} strokeWidth={10} />
            <rect x={-260} y={-300} width={520} height={130} rx={30} fill={P.terracotta} stroke={P.ink} strokeWidth={10} />
            <text y={90} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={170} fill={P.ink}>{year}</text>
            {a > 0 && Array.from({length: 6}, (_, j) => <path key={j} d={`M${-220 + j * 90},300 q20,-${80 + j * 10} 0,-${150 + (j % 3) * 30} q-20,40 -30,10`} fill={P.mustard} stroke="#E0523E" strokeWidth={6} opacity={0.9} />)}
          </g>
        );
      }).reverse()}
      <g transform="translate(540,820)" opacity={after(lt, dur - 0.5, 0.3)}>
        <rect x={-260} y={-300} width={520} height={600} rx={30} fill={P.cream} stroke={P.ink} strokeWidth={10} />
        <rect x={-260} y={-300} width={520} height={130} rx={30} fill={P.sage} stroke={P.ink} strokeWidth={10} />
        <text y={90} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={170} fill={P.ink}>2038</text>
      </g>
      <text x={540} y={1260} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={60} fill={P.cream}>ГОДЫ БЕЗ ПРОЦЕНТОВ</text>
    </svg>
  );
};

// 12. Ставка: огромная крутилка 11% → 10%, отлетает «−806 000 ₽»
export const SceneRate: React.FC<{lt: number; dur: number}> = ({lt, dur}) => {
  const a = easeInOut(after(lt, 0.2, 0.8));
  const val = lerp(11, 10, a);
  return (
    <svg viewBox="0 0 1080 1920">
      <rect width={1080} height={1920} fill="#1F2A2A" />
      <g transform="translate(540,780)">
        <circle r={360} fill="#2E3E3C" stroke={P.ink} strokeWidth={12} />
        {Array.from({length: 24}, (_, i) => <path key={i} d={`M${Math.cos(i / 24 * Math.PI * 2) * 320},${Math.sin(i / 24 * Math.PI * 2) * 320} L${Math.cos(i / 24 * Math.PI * 2) * 350},${Math.sin(i / 24 * Math.PI * 2) * 350}`} stroke={P.cream} strokeWidth={8} />)}
        <g transform={`rotate(${lerp(40, -40, a)})`}><path d="M-16,0 L0,-300 L16,0Z" fill={P.terracotta} stroke={P.ink} strokeWidth={5} /></g>
        <circle r={190} fill="#1E1816" stroke={P.ink} strokeWidth={10} />
        <text y={50} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={150} fill={a > 0.5 ? '#9FD18A' : '#FF9A4A'}>{val.toFixed(1).replace('.0', '').replace('.', ',')}%</text>
      </g>
      <text x={540} y={380} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={70} fill={P.cream}>СТАВКА — ЭТО ВСЁ</text>
      {a > 0.9 && <g transform={`translate(540,1215) scale(${pop(after(lt, 1.0, 0.45))}) rotate(-4)`}><rect x={-300} y={-70} width={600} height={140} rx={70} fill={P.sage} stroke={P.ink} strokeWidth={8} /><text y={30} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={84} fill={P.cream}>−806 000 ₽</text></g>}
    </svg>
  );
};

// 13. Свобода: Тимур в своей квартире, договор «ЗАКРЫТО», конфетти, «2036 — СВОБОДЕН»
export const SceneFreedom: React.FC<{lt: number; dur: number}> = ({lt, dur}) => {
  const k = clamp(lt / dur);
  const jump = Math.abs(Math.sin(lt * 7)) * 40;
  return (
    <svg viewBox="0 0 1080 1920">
      <rect width={1080} height={1920} fill="#EFD9B8" />
      {/* окно с городом-днём */}
      <rect x={120} y={360} width={840} height={620} rx={20} fill="#9CC8E8" stroke={P.ink} strokeWidth={12} />
      {Array.from({length: 7}, (_, i) => <rect key={i} x={150 + i * 120} y={700 - (i % 3) * 90} width={100} height={300} fill="#D2DCE6" stroke={P.ink} strokeWidth={4} />)}
      <path d="M540,360 L540,980 M120,670 L960,670" stroke={P.ink} strokeWidth={12} />
      <rect x={0} y={1180} width={1080} height={740} fill="#C49A6C" />
      <Cam k={k} z0={1.05} z1={1.15} cy={1100}>
        <g transform={`translate(540,${1420 - jump}) scale(1.25)`}><RiderFigure r={TIM} e={emo({smile: 1, mouth: 2, look: [0, -0.2]})} /></g>
        <g transform={`translate(850,${1000 - jump}) rotate(12)`}>
          <rect x={-130} y={-170} width={260} height={340} rx={12} fill="#FFFDF6" stroke={P.ink} strokeWidth={7} />
          <text y={-110} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={30} fill={P.ink}>ИПОТЕКА</text>
          <g transform="rotate(-14)"><rect x={-120} y={-30} width={240} height={80} rx={10} fill="none" stroke={P.terracotta} strokeWidth={8} /><text y={28} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={48} fill={P.terracotta}>ЗАКРЫТО</text></g>
        </g>
      </Cam>
      {Array.from({length: 40}, (_, i) => {
        const x = (i * 97) % 1080, y = ((i * 173) % 600) + lt * (300 + (i % 5) * 80) - 100;
        return <rect key={i} x={x} y={y % 1400 + 200} width={24} height={14} rx={3} fill={[P.mustard, P.terracotta, P.sage, P.cream][i % 4]} transform={`rotate(${i * 37 + lt * 200} ${x} ${y % 1400 + 200})`} />;
      })}
      <g transform={`translate(540,300) scale(${pop(after(lt, 0.1, 0.5))}) rotate(-3)`}>
        <rect x={-400} y={-70} width={800} height={140} rx={70} fill={P.sage} stroke={P.ink} strokeWidth={8} />
        <text y={24} textAnchor="middle" fontFamily={F} fontWeight={900} fontSize={66} fill={P.cream}>2036 — СВОБОДЕН</text>
      </g>
    </svg>
  );
};
