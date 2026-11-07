import React from 'react';
import {AbsoluteFill, Audio, staticFile, useCurrentFrame, continueRender, delayRender} from 'remotion';
import {P} from './palette';
import {FPS, after, ampAt, blink, clamp, cue, easeInOut, easeOut, lerp, mouthShape, noise, story, freezeT, timeline} from './lib';
import {Ashot, AshotState, ArmPose} from './characters/Ashot';
import {RiderFigure, RIDERS, KRISTINA, SVETA, ZINA, Emotion} from './characters/Rider';
import {CabinBack, CabinFront, DriverSeat} from './scene/Cabin';
import {Stamp400} from './overlays/Graphics';
import {Cards, Score, ShotCheat} from './overlays/Episode';
import {Subtitles} from './overlays/Subtitles';
import * as SH from './boards/Shots';
import * as W from './boards/World';
import * as W2 from './boards/World02';
import * as W4 from './boards/World04';
import * as W5 from './boards/World05';
import * as W6 from './boards/World06';

// пассажир серии (story.rider): 'kristina' → вариант А, иначе Тимур
const RIDER = story.rider === 'kristina' ? KRISTINA[0] : story.rider === 'sveta' ? SVETA[2] : story.rider === 'zina' ? ZINA[0] : RIDERS[0];
const FARE0 = story.fareStart ?? 287, FARE1 = story.fareEnd ?? 400;

// врезки-ракурсы поверх салона (story.json → inserts)
const inserts = (story.inserts || []).map((x: any) => ({...x, a: cue(x.from), b: cue(x.to)}));
const renderInsert = (x: any, t: number, lt: number, dur: number) => {
  const k = clamp(lt / dur);
  switch (x.shot) {
    case 'exterior': return <SH.ShotExterior t={t} />;
    case 'brake': return <SH.ShotBrake lt={lt} tb={x.tb ?? 0.3} ts={x.ts ?? 0.9} />;
    case 'jolt': return <SH.ShotJolt lt={lt} phone={x.phone} bad={x.bad} />;
    // серия 2 «Налоговый вычет» (boards/World02.tsx)
    case 'bump': return <W2.SceneBump lt={lt} bump={cue('bumpAt') - x.a} />;
    case 'salary': return <W2.SceneSalary lt={lt} dur={dur} split={clamp((cue(x.splitAt) - x.a) / dur)} />;
    case 'calc': return <W2.SceneCalc lt={lt} dur={dur} split={clamp((cue(x.splitAt) - x.a) / dur)} />;
    case 'yearPaid': return <W2.SceneYearPaid lt={lt} dur={dur} />;
    case 'ndfl': return <W2.SceneNdfl lt={lt} dur={dur} split={clamp((cue(x.splitAt) - x.a) / dur)} />;
    case 'envelopeShut': return <W2.SceneEnvelopeShut lt={lt} dur={dur} />;
    case 'triple': return <W2.SceneTriple lt={lt} dur={dur} />;
    case 'teeth': return <W2.SceneTeeth lt={lt} dur={dur} />;
    case 'queue': return <W2.SceneQueue lt={lt} dur={dur} />;
    case 'phoneLK': return <W2.ScenePhoneLK lt={lt} dur={dur} />;
    case 'yearsBack': return <W2.SceneYearsBack lt={lt} dur={dur} />;
    case 'callMom': return <W2.SceneCallMom lt={lt} dur={dur} />;
    case 'teaser': return <W2.SceneTeaser lt={lt} dur={dur} />;
    case 'meterRefund': { const [a, b] = x.value || [0, 650000]; return <SH.ShotMeter mode="refund" value={lerp(a, b, easeInOut(clamp(lt / Math.max(0.3, dur - 0.4))))} label={x.label} />; }
    // серия 4 «До зарплаты не хватает» (boards/World04.tsx)
    case 'kris': return <W4.ShotKristina lt={lt} e={x.e || {worry: 1, sweat: 1}} phone={x.phone} lean={x.lean || 0} />;
    case 'loanSign': return <W4.SceneLoanSign lt={lt} dur={dur} crack={x.crack !== undefined ? cue(x.crack) - x.a : undefined} />;
    case 'loanCalendar': return <W4.SceneLoanCalendar lt={lt} dur={dur} />;
    case 'notCoffee': return <W4.SceneNotCoffee lt={lt} dur={dur} s1={cue(x.s1) - x.a} half={cue(x.half) - x.a} />;
    case 'surprises': return <W4.SceneSurprises lt={lt} dur={dur} steps={x.steps.map((c: any) => cue(c) - x.a)} />;
    case 'meteor': return <W4.SceneMeteor lt={lt} dur={dur} boom={x.boom !== undefined ? cue(x.boom) - x.a : undefined} />;
    case 'divide': return <W4.SceneDivide lt={lt} dur={dur} eqAt={cue(x.eqAt) - x.a} flipAt={cue(x.flipAt) - x.a} />;
    case 'envelope': return <W4.SceneEnvelope lt={lt} dur={dur} />;
    case 'navHome': return <W4.SceneNavHome lt={lt} dur={dur} />;
    // серия 5 «Кредитка 100 дней» (boards/World05.tsx)
    case 'sveta': return <W5.ShotSveta lt={lt} e={{...(x.e || {}), mouth: mouthShape(ampAt('passenger', t))}} phone={x.phone} scissors={x.scissors} lean={x.lean || 0} />;
    case 'cutBill': return <W5.SceneCutBill lt={lt} dur={dur} cutAt={cue(x.cutAt) - x.a} coinAt={cue(x.coinAt) - x.a} labels={x.labels} badge={x.badge} />;
    case 'chapter': return <W5.SceneChapter lt={lt} dur={dur} n={x.n} title={x.title} phoneAt={x.phoneAt !== undefined ? cue(x.phoneAt) - x.a : undefined} />;
    case 'atm': return <W5.SceneAtm lt={lt} dur={dur} biteAt={cue(x.biteAt) - x.a} debtAt={cue(x.debtAt) - x.a} />;
    case 'calFly': return <W5.SceneCalFly lt={lt} dur={dur} grabAt={x.grabAt !== undefined ? cue(x.grabAt) - x.a : undefined} />;
    case 'beachAge': return <W5.SceneBeachAge lt={lt} dur={dur} endAt={cue(x.endAt) - x.a} angryAt={x.angryAt !== undefined ? cue(x.angryAt) - x.a : undefined} />;
    case 'hourglass': return <W5.SceneHourglass lt={lt} dur={dur} flipAt={cue(x.flipAt) - x.a} stampAt={cue(x.stampAt) - x.a} />;
    case 'rules': return <W5.SceneRules lt={lt} dur={dur} steps={x.steps.map((c: any) => cue(c) - x.a)} flipAt={cue(x.flipAt) - x.a} />;
    // серия 6 «Звонок из службы безопасности» (boards/World06.tsx)
    case 'zina': return <W6.ShotZina lt={lt} e={{...(x.e || {}), mouth: x.e?.mouth ?? mouthShape(ampAt('passenger', t))}} lean={x.lean || 0} phone={x.phone || 'none'} door={x.door} />;
    case 'call6': return <W6.SceneCall lt={lt} dur={dur} />;
    case 'btn': return <W6.SceneBtnChapter lt={lt} dur={dur} n={x.n} />;
    case 'fear': return <W6.SceneFear lt={lt} dur={dur} lampAt={cue(x.lampAt) - x.a} />;
    case 'shashki': return <W6.SceneShashki lt={lt} dur={dur} capAt={cue(x.capAt) - x.a} swapAt={cue(x.swapAt) - x.a} talk={ampAt('passenger', t)} />;
    case 'timer': return <W6.SceneTimer lt={lt} dur={dur} sonAt={cue(x.sonAt) - x.a} />;
    case 'secret': return <W6.SceneSecret lt={lt} dur={dur} crackAt={cue(x.crackAt) - x.a} />;
    case 'buttons': return <W6.SceneButtons lt={lt} dur={dur} />;
    case 'puzzle': return <W6.ScenePuzzle lt={lt} dur={dur} />;
    case 'pipes': return <W6.ScenePipes lt={lt} dur={dur} />;
    case 'leak': return <W6.SceneLeak lt={lt} dur={dur} />;
    case 'robot': return <W6.SceneRobot lt={lt} dur={dur} stampAt={cue(x.stampAt) - x.a} />;
    case 'safe': return <W6.SceneSafe lt={lt} dur={dur} openAt={cue(x.openAt) - x.a} />;
    case 'stats': return <W6.SceneStats lt={lt} dur={dur} splitAt={cue(x.splitAt) - x.a} />;
    case 'hangup': return <W6.SceneHangup lt={lt} dur={dur} />;
    case 'card': return <W6.SceneCard lt={lt} dur={dur} flipAt={cue(x.flipAt) - x.a} bubbleAt={cue(x.bubbleAt) - x.a} />;
    // сцены вне такси (boards/World.tsx)
    case 'bankStamp': return <W.SceneBankStamp lt={lt} dur={dur} />;
    case 'newBuilding': return <W.SceneNewBuilding lt={lt} dur={dur} split={x.splitAt !== undefined ? clamp((cue(x.splitAt) - x.a) / dur) : 0.5} />;
    case 'bankRent': return <W.SceneBankRent lt={lt} dur={dur} />;
    case 'hundred': return <W.SceneHundred lt={lt} dur={dur} />;
    case 'pizza': return <W.ScenePizza lt={lt} dur={dur} />;
    case 'stacks': return <W.SceneStacks lt={lt} dur={dur} />;
    case 'jam': return <W.SceneJam lt={lt} dur={dur} />;
    case 'toll': return <W.SceneToll lt={lt} dur={dur} />;
    case 'piggy': return <W.ScenePiggy lt={lt} dur={dur} />;
    case 'bars': return <W.SceneBars lt={lt} dur={dur} />;
    case 'calendar': return <W.SceneCalendar lt={lt} dur={dur} />;
    case 'rate': return <W.SceneRate lt={lt} dur={dur} />;
    case 'freedom': return <W.SceneFreedom lt={lt} dur={dur} />;
    case 'mirror': return <SH.ShotMirror brow={0.9} wink={0} />;
    case 'phone': return <SH.ShotPhone />;
    case 'meterCrazy': { const [a, b] = x.value || [287, 12000000]; return <SH.ShotMeter mode="crazy" value={lerp(a, b, easeInOut(clamp(lt / Math.max(0.3, dur - 0.35))))} label={x.label} />; }
    case 'meterRewind': { const [a, b] = x.value || [12000000, 9000000]; return <SH.ShotMeter mode="rewind" value={lerp(a, b, easeOut(k))} label={x.label} />; }
    case 'cheat': return <ShotCheat lt={lt} />;
    case 'meterFare': return <SH.ShotMeter mode="fare" value={FARE1} />;
    case 'aging': { const st = Math.min(2, Math.floor(k * 3)); return <SH.ShotAging stage={st} year={Math.round(lerp(2026, 2046, easeOut(k)))} />; }
    case 'nav': return <SH.ShotNav pick={t >= cue('poke')} hand={easeOut(clamp((t - cue('navIn')) / (cue('poke') - cue('navIn'))))} />;
    case 'topdown': return <SH.ShotTopDown k={easeInOut(k)} />;
  }
  return null;
};

// шрифт
const fontHandle = typeof window !== 'undefined' ? delayRender('fonts') : 0;
if (typeof window !== 'undefined') {
  const faces = [600, 800, 900].flatMap((w) => ['cyrillic', 'latin'].map((sub) => new FontFace('Rubik', `url(${staticFile(`fonts/rubik-${sub}-${w}-normal.woff2`)})`, {weight: String(w)})));
  Promise.all(faces.map((f) => f.load().then((ff) => (document as any).fonts.add(ff)))).then(() => continueRender(fontHandle));
}

// анимация по времени: [[cue, значение], …] → плавный переход за dur сек
const AN = (() => {
  const a = story.anim || {};
  const num = (xs: any[] = [[0, 0]]) => xs.map(([c, v]) => [cue(c), v]);
  return {turn: num(a.turn), arm: (a.arm || [[0, 'rest']]).map(([c, v]: any) => [cue(c), v]), wink: (a.wink || []).map((c: any) => cue(c)),
    sweat: num(a.sweat), pass: (a.pass || [[0, {}]]).map(([c, v]: any) => [cue(c), v])};
})();
const seqNum = (xs: any[], t: number, dur: number) => {
  let i = 0; while (i + 1 < xs.length && t >= xs[i + 1][0]) i++;
  const prev = i > 0 ? xs[i - 1][1] : xs[0][1];
  return lerp(prev, xs[i][1], easeOut(after(t, xs[i][0], dur)));
};
const EMO_KEYS = ['shock', 'worry', 'smile'] as const;
const seqEmo = (t: number) => {
  const out: Record<string, number> = {};
  for (const k of EMO_KEYS) {
    let v = 0; const pts: any[] = [];
    for (const [c, e] of AN.pass) if (e[k] !== undefined) pts.push([c, e[k]]);
    v = pts.length ? seqNum(pts, t, k === 'shock' ? 0.12 : 0.3) : 0;
    out[k] = clamp(v);
  }
  return out as {shock: number; worry: number; smile: number};
};

const shots = story.shots.map((s: any) => ({...s, t: cue(s.at)}));
const camera = (t: number) => {
  let i = 0; while (i + 1 < shots.length && t >= shots[i + 1].t) i++;
  const s = shots[i], p = shots[i - 1];
  let [x, y, z] = s.cam;
  if (p && s.move) { const k = easeInOut((t - s.t) / (s.move / FPS)); x = lerp(p.cam[0], x, k); y = lerp(p.cam[1], y, k); z = lerp(p.cam[2], z, k); }
  const dur = (shots[i + 1]?.t ?? timeline.total) - s.t;
  z *= 1 + (s.drift || 0.015) * clamp((t - s.t) / dur);
  let sh = 0; for (const q of shots) if (q.shake && t >= q.t) sh = Math.max(sh, q.shake * Math.exp(-(t - q.t) * 6));
  return {x, y, z, sh, i};
};

export const Video: React.FC<{sub?: string}> = ({sub}) => {
  const frame = useCurrentFrame();
  const real = frame / FPS;
  const tf = freezeT();
  const t = Math.min(real, tf);          // после стоп-кадра время замирает
  const cam = camera(t);
  const vib = Math.sin(t * 31) * 1.6 + Math.sin(t * 13.3) * 1.2; // тряска салона
  const shx = noise(t, 1) * cam.sh, shy = noise(t + 9, 1.3) * cam.sh;

  // ---- Ашот (поза по времени из story.anim)
  const turn = seqNum(AN.turn, t, 0.3);
  const brow = clamp(ampAt('ashot', t) * 1.4) * 0.6 * (1 - turn * 0.5);
  let ai = 0; while (ai + 1 < AN.arm.length && t >= AN.arm[ai + 1][0]) ai++;
  const arm = {from: AN.arm[Math.max(0, ai - 1)][1] as ArmPose, to: AN.arm[ai][1] as ArmPose, k: ai === 0 ? 1 : easeOut(after(t, AN.arm[ai][0], 0.3))};
  const aAmp = ampAt('ashot', t);
  const winkK = Math.max(0, ...AN.wink.map((w: number) => Math.sin(clamp(after(t, w, 0.45)) * Math.PI)));
  const ashot: AshotState = {
    t, turn, browL: brow, browR: brow * 0.25 + turn * 0.15 + winkK * 0.3, blink: blink(t, 1), wink: winkK,
    mouth: mouthShape(aAmp), smirk: turn, look: turn < 0.5 ? [-0.6, -0.6] : [0.55, -0.1],
    arm, poke: 0,
  };
  // ---- пассажир
  const pAmp = ampAt('passenger', t);
  const pe = seqEmo(t);
  const pass: Emotion = {smile: pe.smile,
    blink: blink(t, 4), mouth: mouthShape(pAmp), shock: pe.shock, worry: pe.worry,
    look: turn < 0.5 ? [0.4, 0] : [-0.7, 0.1], sweat: seqNum(AN.sweat, t, 0.4),
  };
  const fare = t < cue('n400') ? FARE0 + t * 0.9 : FARE1;
  const fl = Math.max(...shots.filter((s: any) => s.whoosh).map((s: any) => 1 - clamp(Math.abs(t - s.t) * 8)), ...inserts.map((x: any) => 1 - clamp(Math.abs(t - x.a) * 10)), 0);
  const ins = inserts.find((x: any) => t >= x.a && t < x.b);
  const insShake = ins && ins.shot === 'meterCrazy' && story.cues.n12 && t > cue('n12') ? 14 * Math.exp(-(t - cue('n12')) * 5) : 0;
  const freezeFlash = real >= tf ? 1 - clamp((real - tf) * 3) : 0;

  return (
    <AbsoluteFill style={{background: P.cabin}}>
      <svg width={1080} height={1920} viewBox="0 0 1080 1920" style={{position: 'absolute'}}>
        <g transform={`translate(${540 + shx},${960 + shy}) scale(${cam.z}) translate(${-cam.x},${-cam.y + vib})`}>
          <CabinBack t={t} />
          <g transform={`translate(720,1000) rotate(${noise(t * 0.3, 0.2) * 1.2})`}><RiderFigure r={RIDER} e={pass} /></g>
          <DriverSeat />
          <g transform={`translate(330,1090) rotate(${lerp(-3, 2, turn)})`}><Ashot s={ashot} /></g>
          <CabinFront t={t} ashot={ashot} mirrorOn={1 - turn} fare={fare} shake={cam.sh / 20} />
        </g>
        {/* виньетка */}
        <defs>
          <radialGradient id="vig" cx="0.5" cy="0.5" r="0.75">
            <stop offset="0.6" stopColor="#000" stopOpacity={0} />
            <stop offset="1" stopColor="#1A0E08" stopOpacity={0.55} />
          </radialGradient>
        </defs>
        <rect width={1080} height={1920} fill="url(#vig)" />
        <Stamp400 t={t} />
      </svg>
      {ins && (
        <AbsoluteFill style={{background: '#1D1A1F', overflow: 'hidden'}}>
          <div style={{position: 'absolute', inset: 0, transform: `translate(${noise(t, 1) * insShake}px,${noise(t + 5, 1.2) * insShake}px) scale(${1.02 + 0.06 * clamp((t - ins.a) / (ins.b - ins.a))})`}}>
            <SH.SubCtx.Provider value={false}>
              <style>{'.ins > svg{width:1080px;height:1920px;display:block}'}</style>
              <div className="ins">{renderInsert(ins, t, t - ins.a, ins.b - ins.a)}</div>
            </SH.SubCtx.Provider>
          </div>
        </AbsoluteFill>
      )}
      <svg width={1080} height={1920} viewBox="0 0 1080 1920" style={{position: 'absolute'}}>
        {!(ins && ins.shot === 'cheat') && <Cards t={t} />}
        {!ins && <Score t={t} />}
      </svg>
      {!(ins && ins.shot === 'cheat') && <Subtitles t={t} style={sub} />}
      <AbsoluteFill style={{background: '#FFF6E6', opacity: fl * 0.35 + freezeFlash * 0.8}} />
      {real >= tf && <AbsoluteFill style={{boxShadow: `inset 0 0 0 ${18 * (1 - freezeFlash * 0.5)}px ${P.cream}`}} />}
      <Audio src={staticFile('mix.wav')} />
    </AbsoluteFill>
  );
};
