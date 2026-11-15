/* ============ Финдир — личный финансовый директор (Telegram Mini App) ============ */
'use strict';

const tg = window.Telegram && window.Telegram.WebApp;
const inTelegram = !!(tg && tg.platform && tg.platform !== 'unknown');
const can = v => { try { return !!(tg && tg.isVersionAtLeast && tg.isVersionAtLeast(v)); } catch (e) { return false; } };
const haptic = {
  tap() { try { can('6.1') && tg.HapticFeedback.impactOccurred('light'); } catch (e) {} },
  soft() { try { can('6.1') && tg.HapticFeedback.impactOccurred('soft'); } catch (e) {} },
  sel() { try { can('6.1') && tg.HapticFeedback.selectionChanged(); } catch (e) {} },
  ok() { try { can('6.1') && tg.HapticFeedback.notificationOccurred('success'); } catch (e) {} },
  warn() { try { can('6.1') && tg.HapticFeedback.notificationOccurred('warning'); } catch (e) {} },
};

/* ---------- иконки ---------- */
const ICONS = {
  home: 'M3 10.5 12 3l9 7.5V20a1 1 0 0 1-1 1h-5v-6h-6v6H4a1 1 0 0 1-1-1z',
  bolt: 'M13 2 4 14h7l-1 8 9-12h-7z',
  cart: 'M3 4h2l2.4 11.2a1 1 0 0 0 1 .8h9.2a1 1 0 0 0 1-.8L20 8H6.2M9 20.5h.01M17 20.5h.01',
  car: 'M5 17V12l2-5h10l2 5v5zM5 12h14M7.5 17v2.5M16.5 17v2.5M8 14.5h.01M16 14.5h.01',
  heart: 'M12 20s-7-4.5-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.5-7 10-7 10z',
  cup: 'M4 8h13v5a5 5 0 0 1-5 5H9a5 5 0 0 1-5-5zM17 10h1.5a2.5 2.5 0 0 1 0 5H17M8 2.5V5M12 2.5V5',
  spark: 'M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8zM19 16l.7 2 2 .7-2 .7-.7 2-.7-2-2-.7 2-.7z',
  bag: 'M5 8h14l-1 12H6zM9 8V6a3 3 0 0 1 6 0v2',
  repeat: 'M17 2l3 3-3 3M4 11V9a4 4 0 0 1 4-4h12M7 22l-3-3 3-3M20 13v2a4 4 0 0 1-4 4H4',
  dots: 'M5 12h.01M12 12h.01M19 12h.01',
  shield: 'M12 3l8 3v6c0 4.5-3.4 8.3-8 9-4.6-.7-8-4.5-8-9V6zM9 12l2 2 4-4',
  umbrella: 'M12 3a9 9 0 0 1 9 9H3a9 9 0 0 1 9-9zM12 12v7a2 2 0 0 0 4 0',
  trend: 'M3 17l6-6 4 4 8-8M15 7h6v6',
  plus: 'M12 5v14M5 12h14',
  pulse: 'M3 12h4l3-7 4 14 3-7h4',
  pie: 'M21 12A9 9 0 1 1 12 3v9zM15 3.5A9 9 0 0 1 20.5 9H15z',
  hourglass: 'M6 3h12M6 21h12M7 3c0 5 5 6 5 9s-5 4-5 9M17 3c0 5-5 6-5 9s5 4 5 9',
  gem: 'M6 3h12l3 6-9 12L3 9zM3 9h18M9 3l3 18M15 3l-3 18',
  sliders: 'M4 7h9M17 7h3M4 17h3M11 17h9M17 7a2 2 0 1 1-4 0 2 2 0 0 1 4 0M11 17a2 2 0 1 1-4 0 2 2 0 0 1 4 0',
  x: 'M6 6l12 12M18 6 6 18',
  check: 'M5 12.5l4.5 4.5L19 7',
  trash: 'M4 7h16M9 7V4h6v3M6 7l1 13h10l1-13',
  wallet: 'M3 7a2 2 0 0 1 2-2h13v4M3 7v11a2 2 0 0 0 2 2h15V9H5a2 2 0 0 1-2-2zM16 14.5h.01',
  calendar: 'M4 6h16v14H4zM4 10h16M8 3v4M16 3v4',
  up: 'M12 19V5M6 11l6-6 6 6',
  star: 'M12 3l2.6 5.3 5.9.9-4.3 4.1 1 5.8L12 16.4 6.8 19.1l1-5.8L3.5 9.2l5.9-.9z',
  stop: 'M8 3h8l5 5v8l-5 5H8l-5-5V8zM12 8v5M12 16h.01',
  alert: 'M12 3 2 20h20zM12 10v4M12 17h.01',
  info: 'M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18zM12 11v5M12 8h.01',
  coins: 'M9 9a6 3 0 1 0 0 .01M3 9v4c0 1.7 2.7 3 6 3s6-1.3 6-3V9M9 16v3c0 1.7 2.7 3 6 3s6-1.3 6-3v-4c0-1.7-2.7-3-6-3',
  flag: 'M5 21V4M5 4h12l-2 4 2 4H5',
  gift: 'M4 11h16v10H4zM3 7h18v4H3zM12 7v14M12 7S10.5 3 8 3.5 7.5 7 12 7zM12 7s1.5-4 4-3.5S16.5 7 12 7z',
};
const ic = (n, cls = 'i') => `<svg class="${cls}" viewBox="0 0 24 24" aria-hidden="true"><path d="${ICONS[n] || ICONS.dots}"/></svg>`;

/* ---------- справочники ---------- */
const CATS = {
  rent:       { n: 'Жильё',          g: 'needs',  i: 'home' },
  utilities:  { n: 'ЖКУ и связь',    g: 'needs',  i: 'bolt' },
  food:       { n: 'Продукты',       g: 'needs',  i: 'cart' },
  transport:  { n: 'Транспорт',      g: 'needs',  i: 'car' },
  health:     { n: 'Здоровье',       g: 'needs',  i: 'heart' },
  cafe:       { n: 'Кафе и доставка', g: 'wants', i: 'cup' },
  fun:        { n: 'Развлечения',    g: 'wants',  i: 'spark' },
  shopping:   { n: 'Покупки',        g: 'wants',  i: 'bag' },
  subs:       { n: 'Подписки',       g: 'wants',  i: 'repeat' },
  other:      { n: 'Другое',         g: 'wants',  i: 'dots' },
  unexpected: { n: 'Непредвиденное', g: 'buffer', i: 'shield' },
  safety:     { n: 'Подушка',        g: 'save',   i: 'umbrella' },
  invest:     { n: 'Инвестиции',     g: 'save',   i: 'trend' },
  salary:     { n: 'Зарплата',       g: 'income', i: 'wallet' },
  side:       { n: 'Подработка',     g: 'income', i: 'coins' },
  gift_in:    { n: 'Подарок',        g: 'income', i: 'gift' },
};
const GROUPS = {
  needs:  { n: 'Необходимое', c: 'var(--c-needs)',  hint: 'Жильё, еда, транспорт — то, без чего нельзя' },
  wants:  { n: 'Желания',     c: 'var(--c-wants)',  hint: 'Кафе, покупки, развлечения — жизнь в радость' },
  buffer: { n: 'Резерв',      c: 'var(--c-buffer)', hint: 'Непредвиденное: штраф, лекарства, сломанный телефон' },
  save:   { n: 'Будущее',     c: 'var(--c-save)',   hint: 'Подушка безопасности и инвестиции — платишь сначала себе' },
  income: { n: 'Доход',       c: 'var(--good)' },
};
const GROUP_RGB = { needs: '92,200,255', wants: '255,115,176', buffer: '255,195,92', save: '124,242,166', income: '124,242,166' };
const catColor = k => GROUPS[(CATS[k] || CATS.other).g].c;
const catBg = k => `rgba(${GROUP_RGB[(CATS[k] || CATS.other).g]},.16)`;

const PRESETS = {
  '50-30-20': { n: '50/30/20', needs: .5, wants: .3, save: .2, d: 'Классика сенатора Элизабет Уоррен: 50% — необходимое, 30% — желания, 20% — будущее. Подходит большинству.' },
  '60-20-20': { n: '60/20/20', needs: .6, wants: .2, save: .2, d: 'Для большого города и дорогой аренды: больше на быт, накопления не трогаем.' },
  '70-20-10': { n: '70/20/10', needs: .7, wants: .2, save: .1, d: 'Мягкий старт, если доход пока небольшой. Цель — со временем перейти на 50/30/20.' },
  '50-20-30': { n: '50/20/30', needs: .5, wants: .2, save: .3, d: 'Ускоренный: треть дохода в капитал. Для тех, кто строит финансовую независимость.' },
};
const RISK = {
  cons: { n: 'Спокойный',     rate: .10, shift: -20 },
  mod:  { n: 'Баланс',        rate: .13, shift: 0 },
  aggr: { n: 'Смелый',        rate: .16, shift: 10 },
};
const SWR = 0.04; // правило 4% безопасного изъятия

/* ---------- состояние ---------- */
const KEY = 'findir.v1';
const defaultState = () => ({
  v: 1, updatedAt: 0, onboarded: false, tab: 'home',
  profile: {
    name: (tg && tg.initDataUnsafe && tg.initDataUnsafe.user && tg.initDataUnsafe.user.first_name) || '',
    salary: 120000, extra: 0, advPct: 40, advDay: 20, salDay: 5,
    rent: 35000, age: 28, fundMonths: 6, emergency: 0, invested: 0,
    preset: '50-30-20', risk: 'mod', hours: 168, impulsePct: 3, theme: 'auto', inflation: 7,
  },
  tx: [], wishes: [], willpower: 0, proj: { years: 10, monthly: null, real: false },
});
let S = load() || defaultState();

function load() {
  try { const s = JSON.parse(localStorage.getItem(KEY)); return s ? merge(s) : null; } catch (e) { return null; }
}
function merge(s) {
  const d = defaultState();
  return { ...d, ...s, profile: { ...d.profile, ...(s.profile || {}) }, proj: { ...d.proj, ...(s.proj || {}) } };
}
function persist() {
  S.updatedAt = Date.now();
  try { localStorage.setItem(KEY, JSON.stringify(S)); } catch (e) {}
  cloudSave();
}

/* Telegram CloudStorage: данные живут в аккаунте и синхронизируются между устройствами */
let cloudTimer;
function cloudSave() {
  if (!inTelegram || !can('6.9')) return;
  clearTimeout(cloudTimer);
  cloudTimer = setTimeout(() => {
    try {
      const str = JSON.stringify(S);
      const parts = str.match(/[\s\S]{1,3800}/g) || [];
      tg.CloudStorage.setItem('fd_n', String(parts.length), () => {});
      parts.forEach((p, i) => tg.CloudStorage.setItem('fd_p' + i, p, () => {}));
    } catch (e) {}
  }, 1200);
}
function cloudLoad(cb) {
  if (!inTelegram || !can('6.9')) return cb(null);
  try {
    tg.CloudStorage.getItem('fd_n', (err, n) => {
      n = parseInt(n, 10);
      if (err || !n) return cb(null);
      const keys = Array.from({ length: n }, (_, i) => 'fd_p' + i);
      tg.CloudStorage.getItems(keys, (e2, vals) => {
        if (e2 || !vals) return cb(null);
        try { cb(merge(JSON.parse(keys.map(k => vals[k] || '').join('')))); } catch (e) { cb(null); }
      });
    });
  } catch (e) { cb(null); }
}

/* ---------- утилиты ---------- */
const $ = s => document.querySelector(s);
const esc = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const nf = new Intl.NumberFormat('ru-RU', { maximumFractionDigits: 0 });
const fmtN = n => nf.format(Math.round(n || 0));
const money = n => fmtN(n) + ' ₽';
const short = n => {
  const a = Math.abs(n);
  if (a >= 1e6) return (n / 1e6).toLocaleString('ru-RU', { maximumFractionDigits: a >= 1e8 ? 0 : 1 }) + ' млн ₽';
  if (a >= 1e4) return Math.round(n / 1e3).toLocaleString('ru-RU') + ' тыс ₽';
  return money(n);
};
const pad = n => String(n).padStart(2, '0');
const iso = d => `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
const todayIso = () => iso(new Date());
const dim = (y, m) => new Date(y, m + 1, 0).getDate();
const parseIso = s => { const [y, m, d] = s.split('-').map(Number); return new Date(y, m - 1, d); };
const uid = () => Date.now().toString(36) + Math.random().toString(36).slice(2, 7);
const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
const plural = (n, f) => { n = Math.abs(n) % 100; const n1 = n % 10; if (n > 10 && n < 20) return f[2]; if (n1 > 1 && n1 < 5) return f[1]; if (n1 === 1) return f[0]; return f[2]; };
const days = n => `${n} ${plural(n, ['день', 'дня', 'дней'])}`;
const months = n => `${n} ${plural(n, ['месяц', 'месяца', 'месяцев'])}`;
const years = n => `${n} ${plural(n, ['год', 'года', 'лет'])}`;
const MONTHS_GEN = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря'];
const WD = ['воскресенье', 'понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота'];
const dateLong = d => `${d.getDate()} ${MONTHS_GEN[d.getMonth()]}`;
const relDay = s => {
  const t = todayIso(); if (s === t) return 'Сегодня';
  const y = new Date(); y.setDate(y.getDate() - 1); if (s === iso(y)) return 'Вчера';
  const d = parseIso(s); return `${dateLong(d)}, ${WD[d.getDay()]}`;
};
const num = v => { const n = parseFloat(String(v).replace(/\s/g, '').replace(',', '.')); return isFinite(n) ? n : 0; };

/* ---------- финансовая модель ---------- */
function balances() {
  const p = S.profile; let safety = +p.emergency || 0, invest = +p.invested || 0;
  S.tx.forEach(t => { if (t.type === 'save') { if (t.cat === 'safety') safety += t.amount; else invest += t.amount; } });
  return { safety, invest, total: safety + invest };
}

/** Главная формула: делим доход по выбранному правилу, учитываем аренду, подушку и резерв. */
function buildPlan() {
  const p = S.profile;
  const income = Math.max(0, num(p.salary) + num(p.extra));
  const pr = PRESETS[p.preset] || PRESETS['50-30-20'];
  let needs = income * pr.needs, wants = income * pr.wants, save = income * pr.save;
  const buffer = income * 0.05;            // 5% — непредвиденные расходы (из «желаний»)
  wants -= buffer;
  const rent = Math.max(0, num(p.rent));
  const minOther = income * 0.2;           // на еду, транспорт и ЖКУ нужно минимум ~20% дохода
  let shifted = 0;
  if (needs - rent < minOther) {
    let gap = minOther - (needs - rent);
    const fromW = Math.min(gap, Math.max(0, wants - income * 0.08)); wants -= fromW; gap -= fromW; needs += fromW; shifted += fromW;
    const fromS = Math.min(gap, Math.max(0, save - income * 0.05)); save -= fromS; gap -= fromS; needs += fromS; shifted += fromS;
  }
  const other = Math.max(0, needs - rent);
  const cats = { rent };
  const NW = { food: .46, utilities: .22, transport: .19, health: .13 };
  const WW = { cafe: .3, shopping: .3, fun: .24, subs: .08, other: .08 };
  Object.keys(NW).forEach(k => cats[k] = other * NW[k]);
  Object.keys(WW).forEach(k => cats[k] = Math.max(0, wants) * WW[k]);
  cats.unexpected = buffer;
  const essentials = rent + other;
  const fundTarget = essentials * (num(p.fundMonths) || 6);
  const bal = balances();
  const safeShare = bal.safety >= fundTarget ? 0 : bal.safety < essentials ? 0.7 : 0.5;
  cats.safety = save * safeShare;
  cats.invest = save - cats.safety;
  const groups = { needs: rent + other, wants: Math.max(0, wants), buffer, save };
  const spendPlan = groups.needs + groups.wants + groups.buffer;
  const flexKeys = ['food', 'transport', 'health', 'cafe', 'fun', 'shopping', 'other', 'unexpected'];
  const flexPlan = flexKeys.reduce((s, k) => s + cats[k], 0);
  return {
    income, preset: pr, cats, groups, spendPlan, flexKeys, flexPlan, essentials, fundTarget,
    rentShare: income ? rent / income : 0, shifted, bal,
    monthlyLife: spendPlan,
  };
}

function monthTx(offset = 0) {
  const d = new Date(); d.setDate(1); d.setMonth(d.getMonth() + offset);
  const key = `${d.getFullYear()}-${pad(d.getMonth() + 1)}`;
  return S.tx.filter(t => t.date.slice(0, 7) === key);
}
function monthStats(offset = 0) {
  const list = monthTx(offset);
  const byCat = {}; let spent = 0, income = 0, saved = 0;
  list.forEach(t => {
    if (t.type === 'expense') { spent += t.amount; byCat[t.cat] = (byCat[t.cat] || 0) + t.amount; }
    else if (t.type === 'income') income += t.amount;
    else if (t.type === 'save') { saved += t.amount; byCat[t.cat] = (byCat[t.cat] || 0) + t.amount; }
  });
  const byGroup = { needs: 0, wants: 0, buffer: 0, save: 0 };
  Object.entries(byCat).forEach(([k, v]) => { const g = (CATS[k] || CATS.other).g; if (byGroup[g] != null) byGroup[g] += v; });
  return { list, byCat, byGroup, spent, income, saved };
}

function payments() {
  const p = S.profile, sal = num(p.salary), adv = clamp(num(p.advPct), 0, 90) / 100;
  const list = [];
  if (adv > 0) list.push({ label: 'Аванс', day: clamp(Math.round(num(p.advDay)) || 20, 1, 31), amount: sal * adv });
  list.push({ label: 'Зарплата', day: clamp(Math.round(num(p.salDay)) || 5, 1, 31), amount: sal * (1 - adv) });
  return list;
}
function nextPayment() {
  const now = new Date(), t0 = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  const out = [];
  for (let k = 0; k < 2; k++) {
    const base = new Date(now.getFullYear(), now.getMonth() + k, 1);
    payments().forEach(pp => out.push({ ...pp, date: new Date(base.getFullYear(), base.getMonth(), Math.min(pp.day, dim(base.getFullYear(), base.getMonth()))) }));
  }
  const n = out.filter(x => x.date >= t0).sort((a, b) => a.date - b.date)[0];
  n.inDays = Math.round((n.date - t0) / 864e5);
  return n;
}
function payAllocation(amount, P) {
  const share = P.income ? amount / P.income : 0;
  return {
    invest: P.cats.invest * share,
    safety: P.cats.safety * share,
    rent: P.cats.rent * share,
    fixed: (P.cats.utilities + P.cats.subs) * share,
    life: amount - (P.cats.invest + P.cats.safety + P.cats.rent + P.cats.utilities + P.cats.subs) * share,
  };
}

function hourly() { const p = S.profile; return num(p.salary) / (num(p.hours) || 168); }
function impulseThreshold(P) { return Math.max(500, P.income * (num(S.profile.impulsePct) || 3) / 100); }
function wishCooldownHours(price, P) {
  if (!P.income) return 72;
  const r = price / P.income;
  return r < 0.03 ? 24 : r < 0.1 ? 72 : 24 * 30;
}

function today() {
  const P = buildPlan(), m = monthStats(), now = new Date();
  const dIn = dim(now.getFullYear(), now.getMonth()), day = now.getDate();
  const daysLeft = dIn - day + 1;
  const t = todayIso();
  let flexSpentBefore = 0, flexSpentToday = 0;
  m.list.forEach(x => {
    if (x.type !== 'expense' || !P.flexKeys.includes(x.cat)) return;
    if (x.date === t) flexSpentToday += x.amount; else if (x.date < t) flexSpentBefore += x.amount;
  });
  const flexLeftStart = P.flexPlan - flexSpentBefore;
  const perDayToday = flexLeftStart / daysLeft;
  const safe = Math.max(0, perDayToday - flexSpentToday);
  return { P, m, daysLeft, dIn, day, safe, flexLeft: Math.max(0, flexLeftStart - flexSpentToday), perDayPlan: P.flexPlan / dIn, flexSpentToday };
}

/* ---------- советы финдиректора ---------- */
function insights(T) {
  const { P, m, day, dIn } = T, out = [];
  const add = (tone, icon, html) => out.push({ tone, icon, html });
  const pay = nextPayment();
  if (pay.inDays === 0) add('good', 'wallet', `<b>Сегодня ${pay.label.toLowerCase()}!</b> Сначала заплати себе: переведи <b>${money(payAllocation(pay.amount, P).invest + payAllocation(pay.amount, P).safety)}</b> на накопления, пока деньги не растворились.`);
  else if (pay.inDays <= 3) add('info', 'calendar', `Через ${days(pay.inDays)} ${pay.label.toLowerCase()} — <b>${money(pay.amount)}</b>. Сразу отложи <b>${money(payAllocation(pay.amount, P).invest)}</b> на инвестиции.`);

  if (P.rentShare > 0.4) add('bad', 'home', `Жильё съедает <b>${Math.round(P.rentShare * 100)}%</b> дохода. Норма — до 30%. Это главный рычаг: соседи, другой район или переговоры с арендодателем.`);
  else if (P.rentShare > 0.3) add('warn', 'home', `Аренда — <b>${Math.round(P.rentShare * 100)}%</b> дохода, чуть выше нормы в 30%. Я урезал «желания», чтобы хватило на еду.`);

  const dayShare = day / dIn;
  const spentShare = P.spendPlan ? m.spent / P.spendPlan : 0;
  if (m.spent > 0 && spentShare > dayShare + 0.12) add('warn', 'pulse', `Ты тратишь быстрее плана: прошло <b>${Math.round(dayShare * 100)}%</b> месяца, а ушло <b>${Math.round(spentShare * 100)}%</b> бюджета. Пару дней без кафе выровняют курс.`);
  else if (m.spent > 0 && day > 7 && spentShare < dayShare - 0.1) add('good', 'check', `Отличный темп: потрачено <b>${Math.round(spentShare * 100)}%</b> бюджета за <b>${Math.round(dayShare * 100)}%</b> месяца. Излишек в конце — на инвестиции.`);

  const overs = Object.keys(P.cats).filter(k => CATS[k].g !== 'save' && P.cats[k] > 0 && (m.byCat[k] || 0) > P.cats[k])
    .map(k => ({ k, d: m.byCat[k] - P.cats[k] })).sort((a, b) => b.d - a.d);
  if (overs[0]) add('bad', CATS[overs[0].k].i, `Перерасход в «${CATS[overs[0].k].n}»: <b>+${money(overs[0].d)}</b>. Возьми из резерва или урежь «желания» до конца месяца.`);

  const wantsUsed = P.groups.wants ? m.byGroup.wants / P.groups.wants : 0;
  if (wantsUsed > 0.8 && wantsUsed <= 1 && !overs.length) add('warn', 'bag', `На желания осталось <b>${money(P.groups.wants - m.byGroup.wants)}</b>. Всё новое — сначала в «Хотелки».`);

  const fundPct = P.fundTarget ? P.bal.safety / P.fundTarget : 0;
  if (fundPct < 1) {
    const left = P.fundTarget - P.bal.safety;
    const mo = P.cats.safety ? Math.ceil(left / P.cats.safety) : 0;
    add('info', 'umbrella', `Подушка: <b>${Math.round(fundPct * 100)}%</b> от цели ${short(P.fundTarget)}${mo ? `. При плане ${money(P.cats.safety)}/мес соберёшь за <b>${months(mo)}</b>` : ''}. Держи её на накопительном счёте.`);
  } else add('good', 'shield', `Подушка собрана — ${S.profile.fundMonths} мес. расходов. Теперь все 100% накоплений идут в инвестиции.`);

  const savePlan = P.groups.save;
  if (day >= 10 && m.saved < savePlan * dayShare * 0.5) add('warn', 'trend', `В этом месяце отложено <b>${money(m.saved)}</b> из ${money(savePlan)}. Отметь перевод через «+» → «Отложил».`);

  if (S.willpower > 0) add('good', 'star', `Сила воли уже сэкономила <b>${money(S.willpower)}</b> на передуманных покупках.`);
  if (!S.tx.length) add('info', 'plus', `Начни с малого: записывай каждую трату через кнопку <b>+</b>. Через неделю я покажу, куда утекают деньги.`);
  return out.slice(0, 5);
}

/* ---------- графические элементы ---------- */
function ring(pct, color, size = 44, sw = 5) {
  const r = (size - sw) / 2, c = 2 * Math.PI * r, p = clamp(pct, 0, 1);
  return `<svg class="ring" viewBox="0 0 ${size} ${size}" style="width:${size}px;height:${size}px"><circle class="track" cx="${size / 2}" cy="${size / 2}" r="${r}" style="stroke-width:${sw}"/><circle class="val" cx="${size / 2}" cy="${size / 2}" r="${r}" style="stroke:${pct > 1 ? 'var(--bad)' : color};stroke-width:${sw};stroke-dasharray:${c};stroke-dashoffset:${c * (1 - p)}"/></svg>`;
}
function donut(parts, center) {
  const r = 60, c = 2 * Math.PI * r, total = parts.reduce((s, x) => s + x.v, 0) || 1;
  let off = 0;
  const segs = parts.map(x => {
    const len = (x.v / total) * c, gap = parts.length > 1 ? 3 : 0;
    const s = `<circle cx="75" cy="75" r="${r}" style="stroke:${x.c};stroke-dasharray:${Math.max(0, len - gap)} ${c};stroke-dashoffset:${-off};stroke-linecap:butt"/>`;
    off += len; return s;
  }).join('');
  return `<div class="donut"><svg viewBox="0 0 150 150"><circle cx="75" cy="75" r="${r}" style="stroke:rgba(127,127,160,.14)"/>${segs}</svg><div class="c">${center}</div></div>`;
}
const catIcon = k => `<span class="cat-ic" style="background:${catBg(k)};color:${catColor(k)}">${ic((CATS[k] || CATS.other).i)}</span>`;

/* ---------- экраны ---------- */
function topBar(title, sub) {
  return `<header class="top"><div><div class="sub">${sub}</div><h1>${title}</h1></div><button class="icon-btn glass" data-action="settings" aria-label="Настройки">${ic('sliders')}</button></header>`;
}
function greeting() {
  const h = new Date().getHours(), n = S.profile.name ? ', ' + esc(S.profile.name) : '';
  return (h < 5 ? 'Доброй ночи' : h < 12 ? 'Доброе утро' : h < 18 ? 'Добрый день' : 'Добрый вечер') + n;
}

function vHome() {
  const T = today(), { P, m } = T, now = new Date();
  const pay = nextPayment(), al = payAllocation(pay.amount, P);
  const spentPct = P.spendPlan ? m.spent / P.spendPlan : 0;
  const tips = insights(T);
  const toneBg = { good: 'rgba(124,242,166,.16)', warn: 'rgba(255,195,92,.16)', bad: 'rgba(255,107,125,.16)', info: 'rgba(143,124,255,.18)' };
  const toneFg = { good: 'var(--good)', warn: 'var(--warn)', bad: 'var(--bad)', info: 'var(--accent)' };
  const recent = S.tx.slice().sort((a, b) => b.date.localeCompare(a.date) || b.ts - a.ts).slice(0, 5);
  return `<section class="screen stack">
    ${topBar(greeting(), `${WD[now.getDay()]}, ${dateLong(now)}`)}
    <div class="glass hero">
      <div class="label">Можно потратить сегодня</div>
      <div class="big grad-text">${fmtN(T.safe)}<small>₽</small></div>
      <div class="muted small">Гибкий бюджет: осталось ${money(T.flexLeft)} на ${days(T.daysLeft)} · норма ${money(T.perDayPlan)}/день</div>
      <div class="meter"><b class="${spentPct > 1 ? 'over' : ''}" style="width:${clamp(spentPct, 0, 1) * 100}%"></b><i style="left:${(T.day / T.dIn) * 100}%"></i></div>
      <div class="meter-legend"><span>Потрачено ${money(m.spent)}</span><span>План ${money(P.spendPlan)}</span></div>
    </div>

    <div class="glass card">
      <div class="card-h"><h3>${pay.inDays === 0 ? `Сегодня ${pay.label.toLowerCase()}` : `${pay.label} · ${dateLong(pay.date)}`}</h3><span class="chip">${pay.inDays === 0 ? 'сегодня' : 'через ' + days(pay.inDays)}</span></div>
      <div class="pay-h"><span class="muted small">Придёт</span><b>${money(pay.amount)}</b></div>
      <div class="stackbar">
        <i style="flex:${al.invest};background:var(--c-save)"></i><i style="flex:${al.safety};background:var(--c-save);opacity:.55"></i>
        <i style="flex:${al.rent + al.fixed};background:var(--c-needs)"></i><i style="flex:${Math.max(0, al.life)};background:var(--c-wants)"></i>
      </div>
      <div class="alloc">
        ${al.invest > 0 ? `<div class="a"><span class="dot" style="background:var(--c-save)"></span><span>Сразу на инвестиции</span><b>${money(al.invest)}</b></div>` : ''}
        ${al.safety > 0 ? `<div class="a"><span class="dot" style="background:var(--c-save);opacity:.55"></span><span>На подушку (накопительный счёт)</span><b>${money(al.safety)}</b></div>` : ''}
        <div class="a"><span class="dot" style="background:var(--c-needs)"></span><span>Отложить на жильё и счета</span><b>${money(al.rent + al.fixed)}</b></div>
        <div class="a"><span class="dot" style="background:var(--c-wants)"></span><span>На жизнь до следующей выплаты</span><b>${money(al.life)}</b></div>
      </div>
    </div>

    <div class="glass card">
      <div class="card-h"><h3>Финдиректор говорит</h3>${ic('star')}</div>
      <div class="tips">${tips.map(t => `<div class="tip"><span class="ic" style="background:${toneBg[t.tone]};color:${toneFg[t.tone]}">${ic(t.icon)}</span><p>${t.html}</p></div>`).join('')}</div>
    </div>

    <div class="grid2">
      ${['needs', 'wants', 'buffer', 'save'].map(g => {
        const plan = P.groups[g], fact = m.byGroup[g];
        return `<button class="glass mini" data-action="tab" data-tab="budget">${ring(plan ? fact / plan : 0, GROUPS[g].c)}<div><div class="t">${GROUPS[g].n}</div><div class="v">${short(fact)}</div><div class="tiny faint">из ${short(plan)}</div></div></button>`;
      }).join('')}
    </div>

    <div class="glass card">
      <div class="card-h"><h3>Последние операции</h3>${S.tx.length ? `<button class="link" data-action="all-tx">Все</button>` : ''}</div>
      ${recent.length ? `<div class="list">${recent.map(txRow).join('')}</div>` : `<div class="empty"><div class="em">🧾</div>Пока пусто. Нажми <b>+</b>, чтобы записать первую трату.</div>`}
    </div>
  </section>`;
}

function txRow(t) {
  const c = CATS[t.cat] || CATS.other;
  const sign = t.type === 'expense' ? '−' : t.type === 'income' ? '+' : '→';
  const cls = t.type === 'income' ? 'plus' : t.type === 'save' ? 'save' : '';
  return `<button class="row" data-action="tx" data-id="${t.id}">${catIcon(t.cat)}<div class="mid"><div class="name">${esc(t.note || c.n)}</div><div class="meta">${t.note ? c.n + ' · ' : ''}${relDay(t.date)}</div></div><div class="amt ${cls}">${sign}${money(t.amount)}</div></button>`;
}

function vBudget() {
  const P = buildPlan(), m = monthStats(), p = S.profile;
  const groupCats = g => Object.keys(P.cats).filter(k => CATS[k].g === g);
  const pays = payments();
  const pct = v => P.income ? Math.round((v / P.income) * 100) : 0;
  return `<section class="screen stack">
    ${topBar('Бюджет', 'Формула на месяц')}
    <div class="glass seg">${Object.entries(PRESETS).map(([k, v]) => `<button class="${p.preset === k ? 'on' : ''}" data-action="preset" data-k="${k}">${v.n}</button>`).join('')}</div>

    <div class="glass card">
      <p class="muted small" style="margin:0 0 16px">${P.preset.d}</p>
      <div class="donut-wrap">
        ${donut(['needs', 'wants', 'buffer', 'save'].map(g => ({ v: P.groups[g], c: GROUPS[g].c })), `<span class="tiny muted">Доход</span><b>${short(P.income)}</b>`)}
        <div class="legend">${['needs', 'wants', 'buffer', 'save'].map(g => `<div class="li"><span class="dot" style="background:${GROUPS[g].c}"></span><span>${GROUPS[g].n}</span><b>${pct(P.groups[g])}%</b></div>`).join('')}</div>
      </div>
      ${P.shifted > 0 ? `<div class="tip" style="margin-top:16px"><span class="ic" style="background:rgba(255,195,92,.16);color:var(--warn)">${ic('alert')}</span><p>Аренда ${pct(P.cats.rent)}% дохода не влезает в формулу, поэтому я перенёс <b>${money(P.shifted)}</b> из желаний${P.groups.save < P.income * PRESETS[p.preset].save ? ' и накоплений' : ''} на необходимое.</p></div>` : ''}
    </div>

    ${['needs', 'wants', 'buffer', 'save'].map(g => `
      <div class="glass card">
        <div class="group-h"><span class="dot" style="background:${GROUPS[g].c}"></span><h3>${GROUPS[g].n}</h3><span class="pct" style="background:rgba(${GROUP_RGB[g]},.16);color:${GROUPS[g].c}">${pct(P.groups[g])}% · ${short(P.groups[g])}</span></div>
        <div class="tiny faint" style="margin-bottom:6px">${GROUPS[g].hint}</div>
        ${groupCats(g).map(k => {
          const plan = P.cats[k], fact = m.byCat[k] || 0, r = plan ? fact / plan : 0;
          const over = g !== 'save' && fact > plan;
          return `<div class="cat-line">${catIcon(k)}<div><div class="top-l"><span>${CATS[k].n}</span><b>${g === 'save' ? 'отложено ' : ''}${fmtN(fact)} <span class="faint">/ ${money(plan)}</span></b></div><div class="bar"><b style="width:${clamp(r, 0, 1) * 100}%;background:${over ? 'var(--bad)' : GROUPS[g].c}"></b></div></div></div>`;
        }).join('')}
      </div>`).join('')}

    <div class="card-h" style="margin:22px 4px 0"><h3>План на каждую выплату</h3></div>
    ${pays.map(pp => {
      const al = payAllocation(pp.amount, P);
      return `<div class="glass pay">
        <div class="pay-h"><span><span class="label">${pp.label}</span><br><span class="muted small">${pp.day}-го числа</span></span><b>${money(pp.amount)}</b></div>
        <div class="alloc">
          <div class="a"><span class="dot" style="background:var(--c-save)"></span><span>Инвестиции — в тот же день</span><b>${money(al.invest)}</b></div>
          ${al.safety > 0 ? `<div class="a"><span class="dot" style="background:var(--c-save);opacity:.55"></span><span>Подушка безопасности</span><b>${money(al.safety)}</b></div>` : ''}
          <div class="a"><span class="dot" style="background:var(--c-needs)"></span><span>Аренда</span><b>${money(al.rent)}</b></div>
          <div class="a"><span class="dot" style="background:var(--c-needs);opacity:.55"></span><span>ЖКУ, связь, подписки</span><b>${money(al.fixed)}</b></div>
          <div class="a"><span class="dot" style="background:var(--c-wants)"></span><span>На жизнь</span><b>${money(al.life)}</b></div>
        </div>
      </div>`;
    }).join('')}

    <div class="glass card">
      <div class="card-h"><h3>По каким правилам я считаю</h3></div>
      <details class="rule"><summary>Правило 50/30/20</summary><p>Половина дохода — на обязательное, 30% — на то, что делает жизнь приятной, 20% — на будущее. Популяризировала Элизабет Уоррен в книге «All Your Worth». Пресет можно сменить сверху.</p></details>
      <details class="rule"><summary>Сначала заплати себе</summary><p>Деньги на инвестиции и подушку переводятся в день зарплаты, до любых трат. Что осталось — то и бюджет на жизнь. Так накопления не зависят от силы воли.</p></details>
      <details class="rule"><summary>Жильё — не больше 30%</summary><p>Если аренда выше, формула автоматически урезает «желания» (до 8% дохода), а потом накопления (до 5%), чтобы на еду и транспорт оставалось хотя бы 20%.</p></details>
      <details class="rule"><summary>Подушка безопасности — 3–6 месяцев</summary><p>Запас на обязательные расходы на случай потери работы. Пока её нет, 50–70% накоплений идут в неё, остальное — в инвестиции. Когда собрана — 100% в инвестиции.</p></details>
      <details class="rule"><summary>5% на непредвиденное</summary><p>Отдельный резерв на сюрпризы: штраф, врач, сломанный телефон. Так один форс-мажор не ломает весь месяц.</p></details>
      <details class="rule"><summary>«Можно потратить сегодня»</summary><p>Остаток гибкого бюджета (еда, транспорт, кафе, покупки, развлечения, резерв), делённый на оставшиеся дни месяца. Потратил меньше — завтрашний лимит вырастет.</p></details>
    </div>
  </section>`;
}

function vWishes() {
  const P = buildPlan(), now = Date.now();
  const waiting = S.wishes.filter(w => w.status === 'waiting').sort((a, b) => a.unlockAt - b.unlockAt);
  const done = S.wishes.filter(w => w.status !== 'waiting').sort((a, b) => (b.doneAt || 0) - (a.doneAt || 0)).slice(0, 8);
  const hr = hourly();
  const skipped = S.wishes.filter(w => w.status === 'skipped').length;
  return `<section class="screen stack">
    ${topBar('Хотелки', 'Защита от импульсивных покупок')}
    <div class="glass hero">
      <div class="label">Сэкономлено силой воли</div>
      <div class="big grad-text">${fmtN(S.willpower)}<small>₽</small></div>
      <div class="muted small">${skipped ? `Передумал ${skipped} ${plural(skipped, ['раз', 'раза', 'раз'])}. ` : ''}Это ${(hr ? Math.round(S.willpower / hr) : 0)} ч твоей работы, которые остались с тобой.</div>
      <button class="btn primary full" style="margin-top:16px" data-action="add-wish">${ic('plus')} Хочу купить…</button>
    </div>

    <div class="glass card">
      <div class="card-h"><h3>Правило остывания</h3>${ic('hourglass')}</div>
      <div class="tips">
        <div class="tip"><span class="ic" style="background:rgba(124,242,166,.16);color:var(--good)">24ч</span><p>До <b>${money(P.income * 0.03)}</b> (3% дохода) — подожди сутки.</p></div>
        <div class="tip"><span class="ic" style="background:rgba(255,195,92,.16);color:var(--warn)">72ч</span><p>До <b>${money(P.income * 0.1)}</b> (10% дохода) — три дня.</p></div>
        <div class="tip"><span class="ic" style="background:rgba(255,107,125,.16);color:var(--bad)">30д</span><p>Дороже — правило 30 дней. Если через месяц всё ещё хочется, покупка осознанная.</p></div>
      </div>
    </div>

    ${waiting.length ? waiting.map(w => {
      const total = w.unlockAt - w.created, left = w.unlockAt - now, ready = left <= 0;
      const pr = ready ? 1 : clamp(1 - left / total, 0, 1);
      return `<div class="glass wish">
        <div class="wish-top">${catIcon(w.cat)}<div class="mid"><div class="name">${esc(w.title)}</div><div class="tiny faint">${hr ? `${Math.round(w.price / hr)} ч работы · ` : ''}${CATS[w.cat].n}</div></div><div class="price">${money(w.price)}</div></div>
        <div class="bar"><b style="width:${pr * 100}%;background:${ready ? 'var(--good)' : 'var(--accent-grad)'}"></b></div>
        <div class="timer"><span>${ready ? 'Время вышло. Всё ещё хочешь?' : 'Остывает: ' + leftStr(left)}</span><span>${ready ? '✓' : Math.round(pr * 100) + '%'}</span></div>
        <div class="wish-actions">
          <button class="btn sm good" data-action="wish-skip" data-id="${w.id}">${ic('check')} Передумал</button>
          <button class="btn sm ghost" data-action="wish-buy" data-id="${w.id}" ${ready ? '' : 'disabled'}>Купить</button>
        </div>
      </div>`;
    }).join('') : `<div class="glass card"><div class="empty"><div class="em">🧊</div>Нет хотелок на остывании.<br>Захотелось что-то купить? Сначала сюда.</div></div>`}

    ${done.length ? `<div class="glass card"><div class="card-h"><h3>История</h3></div><div class="list">${done.map(w => `<div class="row">${catIcon(w.cat)}<div class="mid"><div class="name">${esc(w.title)}</div><div class="meta">${w.status === 'skipped' ? 'Передумал — сэкономлено' : 'Куплено осознанно'}</div></div><div class="amt ${w.status === 'skipped' ? 'plus' : ''}">${w.status === 'skipped' ? '+' : '−'}${money(w.price)}</div></div>`).join('')}</div></div>` : ''}
  </section>`;
}
function leftStr(ms) {
  const h = Math.ceil(ms / 36e5);
  if (h >= 48) return days(Math.ceil(h / 24));
  return `${h} ч`;
}

function allocation() {
  const p = S.profile, r = RISK[p.risk] || RISK.mod;
  const stocks = clamp(100 - num(p.age) + r.shift, 15, 85);
  const gold = 10, cash = p.risk === 'cons' ? 10 : 5;
  const bonds = Math.max(0, 100 - stocks - gold - cash);
  return [
    { n: 'Акции', v: stocks, c: '#a18bff', d: 'Фонды (БПИФ) на индекс Мосбиржи — сразу десятки крупнейших компаний, низкая комиссия.' },
    { n: 'Облигации', v: bonds, c: '#5cc8ff', d: 'ОФЗ и надёжные корпоративные облигации (рейтинг от AA). Стабильный купон.' },
    { n: 'Золото', v: gold, c: '#ffc35c', d: 'Фонд на золото — страховка от девальвации рубля и кризисов.' },
    { n: 'Деньги', v: cash, c: '#7cf2a6', d: 'Фонд денежного рынка: доходность около ключевой ставки, «сухой порох» для докупок.' },
  ];
}
function project(start, monthly, rate, yrs) {
  const pts = [{ y: 0, v: start, c: start }]; let b = start, c = start;
  for (let mth = 1; mth <= yrs * 12; mth++) { b = b * (1 + rate / 12) + monthly; c += monthly; if (mth % 12 === 0) pts.push({ y: mth / 12, v: b, c }); }
  return pts;
}
function yearsTo(target, start, monthly, rate) {
  if (start >= target) return 0;
  let b = start;
  for (let mth = 1; mth <= 720; mth++) { b = b * (1 + rate / 12) + monthly; if (b >= target) return Math.ceil(mth / 12 * 10) / 10; }
  return null;
}

function vCapital() {
  const P = buildPlan(), m = monthStats(), p = S.profile, r = RISK[p.risk] || RISK.mod;
  const bal = P.bal;
  const fundPct = P.fundTarget ? bal.safety / P.fundTarget : 0;
  const covered = P.essentials ? bal.safety / P.essentials : 0;
  const monthly = S.proj.monthly != null ? S.proj.monthly : Math.round(P.cats.invest + (fundPct >= 1 ? 0 : 0));
  const fire = (P.monthlyLife * 12) / SWR;
  const fireYears = yearsTo(fire, bal.invest, Math.max(monthly, 1), r.rate);
  const millionYears = yearsTo(1e6, bal.invest, Math.max(monthly, 1), r.rate);
  const al = allocation();
  return `<section class="screen stack">
    ${topBar('Капитал', 'Подушка и инвестиции')}
    <div class="glass hero">
      <div class="label">Мой капитал</div>
      <div class="big grad-text">${fmtN(bal.total)}<small>₽</small></div>
      <div class="kpis">
        <div class="kpi"><div class="t">Подушка</div><div class="v">${short(bal.safety)}</div></div>
        <div class="kpi"><div class="t">Инвестиции</div><div class="v">${short(bal.invest)}</div></div>
        <div class="kpi"><div class="t">В этом мес.</div><div class="v" style="color:var(--c-save)">+${short(m.saved)}</div></div>
      </div>
    </div>

    <div class="glass card">
      <div class="card-h"><h3>Подушка безопасности</h3>${ic('umbrella')}</div>
      <div style="display:flex;gap:16px;align-items:center">
        ${ring(fundPct, 'var(--c-save)', 76, 8)}
        <div><div style="font-size:22px;font-weight:700;letter-spacing:-.02em">${Math.round(fundPct * 100)}%</div>
        <div class="muted small">Покрывает ${covered.toFixed(1).replace('.', ',')} из ${p.fundMonths} мес. обязательных расходов. Цель — ${money(P.fundTarget)}.</div></div>
      </div>
      ${fundPct < 1 && P.cats.safety > 0 ? `<div class="tip" style="margin-top:14px"><span class="ic" style="background:rgba(124,242,166,.16);color:var(--good)">${ic('flag')}</span><p>Откладывая <b>${money(P.cats.safety)}</b> в месяц, соберёшь подушку за <b>${months(Math.ceil((P.fundTarget - bal.safety) / P.cats.safety))}</b>. Храни её на накопительном счёте или в фонде денежного рынка, не в акциях.</p></div>` : ''}
    </div>

    <div class="glass card" id="proj">
      <div class="card-h"><h3>Прогноз роста</h3>${ic('trend')}</div>
      <div class="seg" style="background:rgba(127,127,160,.1)">${Object.entries(RISK).map(([k, v]) => `<button class="${p.risk === k ? 'on' : ''}" data-action="risk" data-k="${k}">${v.n}</button>`).join('')}</div>
      <div class="seg" style="background:rgba(127,127,160,.1);margin-top:8px"><button class="${S.proj.real ? '' : 'on'}" data-action="proj-real" data-v="0">В будущих рублях</button><button class="${S.proj.real ? 'on' : ''}" data-action="proj-real" data-v="1">С учётом инфляции</button></div>
      <div id="proj-body">${projBody(monthly)}</div>
      <div class="slider-h"><span>Срок</span><b id="yrs-l">${years(S.proj.years)}</b></div>
      <input class="range" type="range" min="1" max="30" step="1" value="${S.proj.years}" data-input="years" style="--p:${(S.proj.years - 1) / 29 * 100}%">
      <div class="slider-h"><span>Инвестирую в месяц</span><b id="mon-l">${money(monthly)}</b></div>
      <input class="range" type="range" min="0" max="${Math.max(10000, Math.ceil(P.income * 0.5 / 1000) * 1000)}" step="500" value="${monthly}" data-input="monthly" style="--p:${monthly / Math.max(10000, Math.ceil(P.income * 0.5 / 1000) * 1000) * 100}%">
      <div class="slider-h"><span>Инфляция в год</span><b id="inf-l">${pctStr(infl() * 100)}%</b></div>
      <input class="range" type="range" min="0" max="30" step="0.5" value="${Math.round(infl() * 1000) / 10}" data-input="inflation" style="--p:${infl() * 100 / 30 * 100}%">
      <div class="tiny faint">Официальная инфляция часто ниже личной. Поставь свою: цены на то, что покупаешь именно ты.</div>
    </div>

    <div class="glass card">
      <div class="card-h"><h3>Куда вкладывать</h3><span class="chip">${p.age} лет · ${r.n.toLowerCase()}</span></div>
      <div class="alloc-bar">${al.map(a => `<i style="flex:${a.v};background:${a.c}"></i>`).join('')}</div>
      <div class="tips">${al.map(a => `<div class="tip"><span class="ic" style="background:${a.c}22;color:${a.c};font-weight:700;font-size:12px">${a.v}%</span><p><b>${a.n}.</b> ${a.d}</p></div>`).join('')}</div>
      <p class="disclaimer" style="margin-top:12px">Доля акций по правилу «100 минус возраст» с поправкой на твой риск-профиль. Ребалансируй раз в год: продай то, что выросло сверх доли, докупи отстающее.</p>
    </div>

    <div class="glass card">
      <div class="card-h"><h3>Цели</h3>${ic('flag')}</div>
      <div class="list">
        <div class="row"><span class="cat-ic" style="background:rgba(161,139,255,.18);color:#a18bff">${ic('gem')}</span><div class="mid"><div class="name">Первый миллион</div><div class="meta">в инвестициях</div></div><div class="amt">${millionYears === 0 ? 'есть ✓' : millionYears ? '≈ ' + years(Math.ceil(millionYears)) : '—'}</div></div>
        <div class="row"><span class="cat-ic" style="background:rgba(124,242,166,.16);color:var(--good)">${ic('flag')}</span><div class="mid"><div class="name">Финансовая независимость</div><div class="meta">${short(fire)} — жить на 4% в год</div></div><div class="amt">${fireYears === 0 ? 'есть ✓' : fireYears ? '≈ ' + years(Math.ceil(fireYears)) : '> 60 лет'}</div></div>
      </div>
    </div>

    <div class="glass card">
      <div class="card-h"><h3>Лайфхаки</h3>${ic('star')}</div>
      <div class="tips">
        <div class="tip"><span class="ic" style="background:rgba(143,124,255,.18);color:var(--accent)">${ic('coins')}</span><p><b>ИИС третьего типа</b> — налоговый вычет 13% со взносов до 400&nbsp;000&nbsp;₽ в год, то есть до 52&nbsp;000&nbsp;₽ возврата. Плюс освобождение от налога на доход при долгом сроке.</p></div>
        <div class="tip"><span class="ic" style="background:rgba(143,124,255,.18);color:var(--accent)">${ic('calendar')}</span><p><b>Автопополнение в день зарплаты.</b> Настрой автоперевод в банке — тогда инвестиции происходят без участия воли.</p></div>
        <div class="tip"><span class="ic" style="background:rgba(143,124,255,.18);color:var(--accent)">${ic('up')}</span><p><b>Повысили зарплату — повысь взнос.</b> Отправляй половину прибавки в инвестиции, и уровень жизни всё равно вырастет.</p></div>
      </div>
      <p class="disclaimer" style="margin-top:12px">Не является индивидуальной инвестиционной рекомендацией. Доходность в прогнозе условная (${Math.round(r.rate * 100)}% годовых), инфляция — ${pctStr(infl() * 100)}%. Прошлая доходность не гарантирует будущую.</p>
    </div>
  </section>`;
}

function pctStr(v) { return String(Math.round(v * 10) / 10).replace('.', ','); }
function infl() { const v = num(S.profile.inflation); return clamp(isFinite(v) ? v : 7, 0, 30) / 100; }

function projBody(monthly) {
  const r = (RISK[S.profile.risk] || RISK.mod).rate, yrs = S.proj.years, bal = balances(), i = infl(), isReal = !!S.proj.real;
  const nom = project(bal.invest, monthly, r, yrs);
  const defl = y => isReal ? Math.pow(1 + i, y) : 1;
  const pts = nom.map(p => ({ y: p.y, v: p.v / defl(p.y), c: p.c / defl(p.y) }));
  const last = pts[pts.length - 1], nomLast = nom[nom.length - 1], realLast = nomLast.v / Math.pow(1 + i, yrs);
  const realRate = (1 + r) / (1 + i) - 1;
  const W = 320, Hh = 150, max = Math.max(...pts.map(p => p.v), 1);
  const x = i => (i / (pts.length - 1 || 1)) * W, y = v => Hh - (v / max) * (Hh - 12);
  const line = pts.map((p, i) => `${i ? 'L' : 'M'}${x(i).toFixed(1)},${y(p.v).toFixed(1)}`).join('');
  const cl = pts.map((p, i) => `${i ? 'L' : 'M'}${x(i).toFixed(1)},${y(p.c).toFixed(1)}`).join('');
  const ticks = [0, Math.round(yrs / 2), yrs].filter((v, i, a) => a.indexOf(v) === i);
  return `
    <svg class="chart" viewBox="0 0 ${W} ${Hh + 16}" preserveAspectRatio="none">
      <defs><linearGradient id="pg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8f7cff" stop-opacity=".45"/><stop offset="1" stop-color="#8f7cff" stop-opacity="0"/></linearGradient>
      <linearGradient id="pl" x1="0" x2="1"><stop offset="0" stop-color="#a18bff"/><stop offset="1" stop-color="#4fe3d6"/></linearGradient></defs>
      <path d="${line}L${W},${Hh}L0,${Hh}Z" fill="url(#pg)"/>
      <path d="${cl}" fill="none" stroke="currentColor" stroke-opacity=".35" stroke-width="1.5" stroke-dasharray="4 4"/>
      <path d="${line}" fill="none" stroke="url(#pl)" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" vector-effect="non-scaling-stroke"/>
      ${ticks.map(t => `<text x="${clamp(x(t), 8, W - 8)}" y="${Hh + 14}" text-anchor="${t === 0 ? 'start' : t === yrs ? 'end' : 'middle'}">${t ? t + ' ' + plural(t, ['год', 'года', 'лет']) : 'сейчас'}</text>`).join('')}
    </svg>
    <div class="kpis">
      <div class="kpi"><div class="t">${isReal ? 'Будет, по ценам сегодня' : 'Будет'}</div><div class="v grad-text">${short(last.v)}</div></div>
      <div class="kpi"><div class="t">Вложишь</div><div class="v">${short(last.c)}</div></div>
      <div class="kpi"><div class="t">${isReal ? 'Реальный доход' : 'Доход'}</div><div class="v" style="color:${last.v - last.c >= 0 ? 'var(--c-save)' : 'var(--bad)'}">${last.v - last.c >= 0 ? '+' : '−'}${short(Math.abs(last.v - last.c))}</div></div>
    </div>
    <p class="disclaimer" style="margin-top:10px">${isReal
      ? `Все суммы пересчитаны в сегодняшние цены. В будущих рублях на счёте будет ${short(nomLast.v)}, но купить на них можно столько же, сколько сейчас на ${short(last.v)}. Реальная доходность ≈ ${(realRate * 100).toFixed(1).replace('.', ',')}% в год.`
      : `С учётом инфляции ${pctStr(i * 100)}% это как ${short(realLast)} сегодня. Переключи «С учётом инфляции», чтобы видеть реальные суммы.`} Пунктир — сколько вложено своих.</p>`;
}

const VIEWS = { home: vHome, budget: vBudget, wishes: vWishes, capital: vCapital };

/* ---------- онбординг ---------- */
let onbStep = 0;
function vOnboarding() {
  const p = S.profile;
  const steps = `<div class="steps">${[0, 1, 2, 3].map(i => `<i class="${i <= onbStep ? 'on' : ''}"></i>`).join('')}</div>`;
  if (onbStep === 0) return `<section class="screen onb">
    <div class="logo">${ic('trend')}</div>
    <h1>Твой личный<br><span class="grad-text">финансовый директор</span></h1>
    <p class="lead">Разложу зарплату по формуле, остановлю импульсивные покупки и покажу, как деньги превращаются в капитал.</p>
    <div class="feat">${catIcon('rent')}<div><b>Бюджет по формуле 50/30/20</b><div class="muted small">с учётом аренды, аванса и зарплаты</div></div></div>
    <div class="feat">${catIcon('shopping')}<div><b>Стоп-кран для импульсов</b><div class="muted small">цена в часах работы и правило остывания</div></div></div>
    <div class="feat">${catIcon('invest')}<div><b>План инвестиций</b><div class="muted small">подушка, портфель и прогноз капитала</div></div></div>
    <button class="btn primary full" style="margin-top:26px" data-action="onb-next">Начать — 1 минута</button>
  </section>`;
  if (onbStep === 1) return `<section class="screen onb">${steps}
    <h1>Сколько ты получаешь?</h1><p class="lead">Сумма на руки после налогов. Аванс и зарплату посчитаю отдельно.</p>
    <div class="field"><label>Как тебя зовут</label><input data-f="name" value="${esc(p.name)}" placeholder="Имя"></div>
    <div class="field"><label>Зарплата в месяц, ₽</label><input data-f="salary" inputmode="numeric" value="${p.salary || ''}" placeholder="120 000"></div>
    <div class="row2">
      <div class="field"><label>Аванс, % от з/п</label><input data-f="advPct" inputmode="numeric" value="${p.advPct}"><span class="hint">0 — если одна выплата</span></div>
      <div class="field"><label>Подработка, ₽/мес</label><input data-f="extra" inputmode="numeric" value="${p.extra || ''}" placeholder="0"></div>
    </div>
    <div class="row2">
      <div class="field"><label>Дата аванса</label><input data-f="advDay" inputmode="numeric" value="${p.advDay}"></div>
      <div class="field"><label>Дата зарплаты</label><input data-f="salDay" inputmode="numeric" value="${p.salDay}"></div>
    </div>
    <div class="actions"><button class="btn ghost" data-action="onb-back">Назад</button><button class="btn primary full" data-action="onb-next">Дальше</button></div>
  </section>`;
  if (onbStep === 2) return `<section class="screen onb">${steps}
    <h1>Жильё и возраст</h1><p class="lead">Аренда — главный обязательный расход. Возраст нужен, чтобы подобрать портфель.</p>
    <div class="field"><label>Аренда / ипотека в месяц, ₽</label><input data-f="rent" inputmode="numeric" value="${p.rent || ''}" placeholder="0 — если своё жильё"></div>
    <div class="field"><label>Возраст</label><input data-f="age" inputmode="numeric" value="${p.age}"></div>
    <div class="field"><label>Отношение к риску</label><select data-f="risk">${Object.entries(RISK).map(([k, v]) => `<option value="${k}" ${p.risk === k ? 'selected' : ''}>${v.n}</option>`).join('')}</select></div>
    <div class="actions"><button class="btn ghost" data-action="onb-back">Назад</button><button class="btn primary full" data-action="onb-next">Дальше</button></div>
  </section>`;
  return `<section class="screen onb">${steps}
    <h1>Что уже накоплено?</h1><p class="lead">Можно 0 — начнём с нуля. Это нормально.</p>
    <div class="field"><label>Подушка безопасности (вклады, накопительный счёт), ₽</label><input data-f="emergency" inputmode="numeric" value="${p.emergency || ''}" placeholder="0"></div>
    <div class="field"><label>Инвестиции (брокерский счёт, ИИС), ₽</label><input data-f="invested" inputmode="numeric" value="${p.invested || ''}" placeholder="0"></div>
    <div class="field"><label>Размер подушки</label><select data-f="fundMonths"><option value="3" ${p.fundMonths == 3 ? 'selected' : ''}>3 месяца — стабильная работа</option><option value="6" ${p.fundMonths == 6 ? 'selected' : ''}>6 месяцев — рекомендую</option><option value="12" ${p.fundMonths == 12 ? 'selected' : ''}>12 месяцев — фриланс, ИП</option></select></div>
    <div class="actions"><button class="btn ghost" data-action="onb-back">Назад</button><button class="btn primary full" data-action="onb-finish">Посчитать мой план</button></div>
  </section>`;
}
function readFields(scope) {
  scope.querySelectorAll('[data-f]').forEach(el => {
    const k = el.dataset.f, v = el.value;
    S.profile[k] = (k === 'name' || k === 'risk' || k === 'theme' || k === 'preset') ? v.trim() : num(v);
  });
}

/* ---------- таббар ---------- */
const TABS = [
  { k: 'home', n: 'Обзор', i: 'pulse' },
  { k: 'budget', n: 'Бюджет', i: 'pie' },
  { k: 'add' },
  { k: 'wishes', n: 'Хотелки', i: 'hourglass' },
  { k: 'capital', n: 'Капитал', i: 'gem' },
];
function renderTabbar() {
  const bar = $('#tabbar');
  bar.hidden = !S.onboarded;
  if (!S.onboarded) return;
  if (!bar.dataset.ready) {
    bar.innerHTML = `<span class="tab-pill" id="pill"></span>` + TABS.map(t => t.k === 'add'
      ? `<div class="fab-slot"><button class="fab" data-action="add" aria-label="Добавить">${ic('plus')}</button></div>`
      : `<button class="tab" data-action="tab" data-tab="${t.k}">${ic(t.i)}<span>${t.n}</span></button>`).join('');
    bar.dataset.ready = '1';
  }
  bar.querySelectorAll('.tab').forEach(b => b.classList.toggle('on', b.dataset.tab === S.tab));
  movePill(false);
}
function movePill(squish) {
  const bar = $('#tabbar'), pill = $('#pill'), act = bar && bar.querySelector('.tab.on');
  if (!pill || !act) return;
  const w = Math.min(act.offsetWidth, 78);
  pill.style.width = w + 'px';
  pill.style.transform = `translateX(${act.offsetLeft + (act.offsetWidth - w) / 2}px)`;
  if (squish) { pill.classList.remove('squish'); void pill.offsetWidth; pill.classList.add('squish'); }
}

/* ---------- рендер ---------- */
function render() {
  applyTheme();
  const app = $('#app');
  app.innerHTML = S.onboarded ? (VIEWS[S.tab] || vHome)() : vOnboarding();
  renderTabbar();
}

/* ---------- шторки ---------- */
let sheetOnClose = null;
function openSheet(html, onClose) {
  const root = $('#sheet-root');
  root.innerHTML = `<div class="scrim" data-action="close-sheet"></div><div class="sheet" role="dialog"><div class="grabber"></div>${html}</div>`;
  sheetOnClose = onClose || null;
  requestAnimationFrame(() => requestAnimationFrame(() => root.classList.add('open')));
  try { can('6.1') && tg.BackButton.show(); } catch (e) {}
}
function setSheet(html) { const s = $('#sheet-root .sheet'); if (s) { s.innerHTML = `<div class="grabber"></div>${html}`; s.scrollTop = 0; } }
function closeSheet() {
  const root = $('#sheet-root');
  if (!root.classList.contains('open')) return;
  root.classList.remove('open');
  setTimeout(() => { if (!root.classList.contains('open')) root.innerHTML = ''; }, 450);
  try { can('6.1') && tg.BackButton.hide(); } catch (e) {}
  const cb = sheetOnClose; sheetOnClose = null; cb && cb();
}

let toastT;
function toast(msg) { const t = $('#toast'); t.textContent = msg; t.classList.add('show'); clearTimeout(toastT); toastT = setTimeout(() => t.classList.remove('show'), 2200); }

/* ---------- добавление операции ---------- */
let draft = null;
function sizeAmt(el) { el.style.width = Math.max(1, (el.value || el.placeholder).length) + 0.3 + 'ch'; }
function refreshProj() { const b = $('#proj-body'); if (b) b.innerHTML = projBody(S.proj.monthly != null ? S.proj.monthly : Math.round(buildPlan().cats.invest)); }
function openAdd(type = 'expense') {
  draft = { type, amount: '', cat: type === 'expense' ? 'food' : type === 'income' ? 'salary' : 'invest', note: '', date: todayIso() };
  openSheet(addHtml());
  setTimeout(() => { const a = $('#amt'); if (a) { sizeAmt(a); a.focus(); } }, 380);
}
function addHtml() {
  const cats = Object.keys(CATS).filter(k => {
    const g = CATS[k].g;
    return draft.type === 'expense' ? ['needs', 'wants', 'buffer'].includes(g) : draft.type === 'income' ? g === 'income' : g === 'save';
  });
  return `<h2>${draft.type === 'expense' ? 'Новая трата' : draft.type === 'income' ? 'Доход' : 'Отложил на будущее'}</h2>
    <div class="seg" style="background:rgba(127,127,160,.1);margin-top:12px">
      ${[['expense', 'Расход'], ['income', 'Доход'], ['save', 'Отложил']].map(([k, n]) => `<button class="${draft.type === k ? 'on' : ''}" data-action="draft-type" data-k="${k}">${n}</button>`).join('')}
    </div>
    <div class="amount-in"><input id="amt" inputmode="decimal" placeholder="0" value="${esc(draft.amount)}" data-draft="amount" autocomplete="off"><span>₽</span></div>
    <div class="cat-grid">${cats.map(k => `<button class="cat-btn ${draft.cat === k ? 'on' : ''}" style="--cc:${catColor(k)}" data-action="draft-cat" data-k="${k}">${catIcon(k)}${CATS[k].n}</button>`).join('')}</div>
    <div class="row2">
      <div class="field"><label>Комментарий</label><input data-draft="note" value="${esc(draft.note)}" placeholder="${draft.type === 'expense' ? 'Например, «Пятёрочка»' : 'Необязательно'}" maxlength="60"></div>
      <div class="field"><label>Дата</label><input type="date" data-draft="date" value="${draft.date}" max="${todayIso()}"></div>
    </div>
    <div class="actions"><button class="btn primary full" data-action="draft-save">${ic('check')} Сохранить</button></div>`;
}
function saveDraft(force) {
  const amount = Math.round(num(draft.amount) * 100) / 100;
  if (!(amount > 0)) { haptic.warn(); toast('Введи сумму'); const a = $('#amt'); a && a.focus(); return; }
  const P = buildPlan();
  if (!force && draft.type === 'expense' && CATS[draft.cat].g === 'wants') {
    const m = monthStats(), wantsLeft = P.groups.wants - m.byGroup.wants;
    if (amount >= impulseThreshold(P) || amount > wantsLeft) return showStop(amount, P, wantsLeft);
  }
  S.tx.push({ id: uid(), ts: Date.now(), type: draft.type, amount, cat: draft.cat, note: draft.note.trim(), date: draft.date || todayIso() });
  persist(); haptic.ok(); closeSheet(); render();
  toast(draft.type === 'save' ? 'Будущий ты говорит спасибо 💚' : draft.type === 'income' ? 'Доход записан' : 'Записал');
}
function showStop(amount, P, wantsLeft) {
  haptic.warn();
  const hrs = hourly() ? amount / hourly() : 0;
  const cd = wishCooldownHours(amount, P);
  const pctW = P.groups.wants ? Math.round((amount / P.groups.wants) * 100) : 0;
  const yearsGrow = amount * Math.pow(1 + RISK.mod.rate, 10);
  setSheet(`<div style="text-align:center"><div class="stop-badge">${ic('stop')}</div>
      <h2>Стоп-кран</h2><p class="lead">${money(amount)} на «${CATS[draft.cat].n}». Это точно нужно прямо сейчас?</p></div>
    <div class="facts">
      <div class="fact"><b>${hrs >= 1 ? Math.round(hrs) + ' ч' : Math.round(hrs * 60) + ' мин'}</b><span>твоей работы</span></div>
      <div class="fact"><b style="color:${wantsLeft < amount ? 'var(--bad)' : 'inherit'}">${pctW}%</b><span>бюджета на желания</span></div>
      <div class="fact"><b>${short(Math.max(0, wantsLeft))}</b><span>осталось на желания</span></div>
      <div class="fact"><b class="grad-text">${short(yearsGrow)}</b><span>если вложить на 10 лет</span></div>
    </div>
    <div class="actions" style="flex-direction:column">
      <button class="btn primary full" data-action="stop-wish">${ic('hourglass')} Остыть ${cd >= 48 ? days(Math.round(cd / 24)) : cd + ' ч'} в «Хотелках»</button>
      <button class="btn ghost full" data-action="stop-force">Это не импульс — записать</button>
    </div>`);
}

/* ---------- хотелки ---------- */
function openWish() {
  openSheet(`<h2>Хочу купить</h2><p class="lead">Запиши желание — я заморожу его на время. Если желание пройдёт, деньги останутся у тебя.</p>
    <div class="field"><label>Что</label><input id="w-title" placeholder="Например, наушники" maxlength="50"></div>
    <div class="field"><label>Сколько стоит, ₽</label><input id="w-price" inputmode="numeric" placeholder="0"></div>
    <div class="field"><label>Категория</label><select id="w-cat">${['shopping', 'fun', 'cafe', 'other'].map(k => `<option value="${k}">${CATS[k].n}</option>`).join('')}</select></div>
    <div class="actions"><button class="btn primary full" data-action="wish-save">${ic('hourglass')} Заморозить</button></div>`);
  setTimeout(() => { const a = $('#w-title'); a && a.focus(); }, 380);
}
function addWish(title, price, cat) {
  const P = buildPlan(), h = wishCooldownHours(price, P), now = Date.now();
  S.wishes.push({ id: uid(), title: title || 'Покупка', price, cat, created: now, unlockAt: now + h * 36e5, status: 'waiting' });
  persist();
  return h;
}

/* ---------- настройки ---------- */
function openSettings() {
  const p = S.profile;
  const f = (k, label, hint = '', mode = 'numeric') => `<div class="field"><label>${label}</label><input data-f="${k}" inputmode="${mode}" value="${esc(p[k])}">${hint ? `<span class="hint">${hint}</span>` : ''}</div>`;
  openSheet(`<h2>Профиль и формула</h2><p class="lead">Всё хранится на твоём устройстве${inTelegram ? ' и в облаке Telegram' : ''}.</p>
    <div class="field"><label>Имя</label><input data-f="name" value="${esc(p.name)}"></div>
    <div class="row2">${f('salary', 'Зарплата, ₽/мес')}${f('extra', 'Подработка, ₽/мес')}</div>
    <div class="row2">${f('advPct', 'Аванс, %', '0 — одна выплата')}${f('rent', 'Аренда, ₽/мес')}</div>
    <div class="row2">${f('advDay', 'День аванса')}${f('salDay', 'День зарплаты')}</div>
    <div class="row2">${f('emergency', 'Подушка сейчас, ₽', 'без учёта записанных')}${f('invested', 'Инвестиции сейчас, ₽', 'без учёта записанных')}</div>
    <div class="row2">${f('age', 'Возраст')}${f('hours', 'Рабочих часов в месяц', 'для «цены в часах»')}</div>
    <div class="row2">${f('impulsePct', 'Стоп-кран от, % дохода', 'порог импульсной траты')}
      <div class="field"><label>Подушка</label><select data-f="fundMonths">${[3, 6, 12].map(n => `<option value="${n}" ${p.fundMonths == n ? 'selected' : ''}>${months(n)}</option>`).join('')}</select></div></div>
    <div class="row2">
      <div class="field"><label>Риск-профиль</label><select data-f="risk">${Object.entries(RISK).map(([k, v]) => `<option value="${k}" ${p.risk === k ? 'selected' : ''}>${v.n}</option>`).join('')}</select></div>
      <div class="field"><label>Тема</label><select data-f="theme">${[['auto', 'Как в Telegram'], ['dark', 'Тёмная'], ['light', 'Светлая']].map(([k, n]) => `<option value="${k}" ${p.theme === k ? 'selected' : ''}>${n}</option>`).join('')}</select></div>
    </div>
    <div class="actions"><button class="btn primary full" data-action="settings-save">Сохранить</button></div>
    <div class="actions"><button class="btn ghost full" data-action="export">Экспорт данных</button><button class="btn danger full" data-action="reset">Сбросить всё</button></div>`);
}

function openAllTx() {
  const list = S.tx.slice().sort((a, b) => b.date.localeCompare(a.date) || b.ts - a.ts).slice(0, 300);
  let last = '', html = '';
  list.forEach(t => { if (t.date !== last) { html += `<div class="day-h">${relDay(t.date)}</div>`; last = t.date; } html += txRow(t); });
  const m = monthStats();
  openSheet(`<h2>Операции</h2><p class="lead">В этом месяце: расходы ${money(m.spent)} · доходы ${money(m.income)} · отложено ${money(m.saved)}</p><div class="list">${html}</div>`);
}
function openTx(id) {
  const t = S.tx.find(x => x.id === id); if (!t) return;
  const c = CATS[t.cat] || CATS.other;
  openSheet(`<div style="display:flex;gap:14px;align-items:center;margin-bottom:8px">${catIcon(t.cat)}<div><h2>${money(t.amount)}</h2><div class="muted small">${c.n} · ${relDay(t.date)}</div></div></div>
    ${t.note ? `<p class="lead" style="margin-top:10px">${esc(t.note)}</p>` : ''}
    ${t.type === 'expense' && hourly() ? `<div class="tip" style="margin-top:10px"><span class="ic" style="background:rgba(143,124,255,.18);color:var(--accent)">${ic('hourglass')}</span><p>Это <b>${(t.amount / hourly()).toFixed(1).replace('.', ',')} ч</b> твоей работы.</p></div>` : ''}
    <div class="actions"><button class="btn danger full" data-action="tx-del" data-id="${t.id}">${ic('trash')} Удалить</button></div>`);
}

/* ---------- тема ---------- */
function applyTheme() {
  const pref = S.profile.theme;
  const theme = pref === 'auto' ? (inTelegram ? (tg.colorScheme || 'dark') : 'dark') : pref;
  document.documentElement.dataset.theme = theme;
  const bg = theme === 'light' ? '#eef0f8' : '#06060b';
  document.querySelector('meta[name="theme-color"]').content = bg;
  try { if (can('6.1')) { tg.setHeaderColor(bg); tg.setBackgroundColor(bg); } if (can('7.10')) tg.setBottomBarColor(bg); } catch (e) {}
}

/* ---------- события ---------- */
document.addEventListener('click', e => {
  const el = e.target.closest('[data-action]'); if (!el) return;
  const a = el.dataset.action, P = () => buildPlan();
  switch (a) {
    case 'tab':
      if (S.tab === el.dataset.tab) { window.scrollTo({ top: 0, behavior: 'smooth' }); return; }
      haptic.sel(); S.tab = el.dataset.tab; persist(); render(); movePill(true); window.scrollTo(0, 0); break;
    case 'add': haptic.tap(); openAdd(); break;
    case 'close-sheet': closeSheet(); break;
    case 'settings': haptic.tap(); openSettings(); break;
    case 'settings-save': readFields($('#sheet-root')); persist(); haptic.ok(); closeSheet(); render(); toast('План пересчитан'); break;
    case 'export': {
      const blob = new Blob([JSON.stringify(S, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob), link = document.createElement('a');
      link.href = url; link.download = `findir-${todayIso()}.json`; link.click(); setTimeout(() => URL.revokeObjectURL(url), 2000);
      break;
    }
    case 'reset': {
      const doReset = ok => { if (!ok) return; S = defaultState(); onbStep = 0; persist(); closeSheet(); $('#tabbar').dataset.ready = ''; render(); };
      if (inTelegram && can('6.2')) tg.showConfirm('Удалить все данные и начать заново?', doReset); else doReset(confirm('Удалить все данные и начать заново?'));
      break;
    }
    case 'preset': haptic.sel(); S.profile.preset = el.dataset.k; persist(); render(); break;
    case 'risk': haptic.sel(); S.profile.risk = el.dataset.k; persist(); render(); break;
    case 'proj-real': haptic.sel(); S.proj.real = el.dataset.v === '1'; persist(); el.parentNode.querySelectorAll('button').forEach(b => b.classList.toggle('on', b === el)); refreshProj(); break;
    case 'all-tx': openAllTx(); break;
    case 'tx': openTx(el.dataset.id); break;
    case 'tx-del': S.tx = S.tx.filter(t => t.id !== el.dataset.id); persist(); haptic.tap(); closeSheet(); render(); toast('Удалено'); break;
    case 'draft-type': haptic.sel(); draft.type = el.dataset.k; draft.cat = draft.type === 'expense' ? 'food' : draft.type === 'income' ? 'salary' : 'invest'; setSheet(addHtml()); { const a = $('#amt'); a && sizeAmt(a); } break;
    case 'draft-cat': haptic.sel(); draft.cat = el.dataset.k; document.querySelectorAll('.cat-btn').forEach(b => b.classList.toggle('on', b.dataset.k === draft.cat)); break;
    case 'draft-save': saveDraft(false); break;
    case 'stop-force': saveDraft(true); break;
    case 'stop-wish': {
      const h = addWish(draft.note || CATS[draft.cat].n, Math.round(num(draft.amount)), draft.cat);
      haptic.ok(); closeSheet(); S.tab = 'wishes'; persist(); render();
      toast(`Заморожено на ${h >= 48 ? days(Math.round(h / 24)) : h + ' ч'} 🧊`); break;
    }
    case 'add-wish': haptic.tap(); openWish(); break;
    case 'wish-save': {
      const title = $('#w-title').value.trim(), price = Math.round(num($('#w-price').value)), cat = $('#w-cat').value;
      if (!(price > 0)) { haptic.warn(); toast('Укажи цену'); return; }
      const h = addWish(title, price, cat); haptic.ok(); closeSheet(); render();
      toast(`Заморожено на ${h >= 48 ? days(Math.round(h / 24)) : h + ' ч'} 🧊`); break;
    }
    case 'wish-skip': {
      const w = S.wishes.find(x => x.id === el.dataset.id); if (!w) return;
      w.status = 'skipped'; w.doneAt = Date.now(); S.willpower += w.price; persist(); haptic.ok(); render();
      toast(`+${money(w.price)} к силе воли 💪`); break;
    }
    case 'wish-buy': {
      const w = S.wishes.find(x => x.id === el.dataset.id); if (!w) return;
      w.status = 'bought'; w.doneAt = Date.now();
      S.tx.push({ id: uid(), ts: Date.now(), type: 'expense', amount: w.price, cat: w.cat, note: w.title, date: todayIso() });
      persist(); haptic.ok(); render(); toast('Осознанная покупка записана'); break;
    }
    case 'onb-next': {
      readFields($('#app'));
      if (onbStep === 1 && !(num(S.profile.salary) > 0)) { haptic.warn(); toast('Укажи зарплату'); return; }
      haptic.tap(); onbStep++; persist(); render(); window.scrollTo(0, 0); break;
    }
    case 'onb-back': readFields($('#app')); onbStep = Math.max(0, onbStep - 1); render(); break;
    case 'onb-finish': readFields($('#app')); S.onboarded = true; S.tab = 'budget'; persist(); haptic.ok(); render(); toast('Твой план готов ✨'); break;
  }
  void P;
});

document.addEventListener('input', e => {
  const el = e.target;
  if (el.dataset.draft && draft) { draft[el.dataset.draft] = el.value; if (el.id === 'amt') sizeAmt(el); return; }
  if (el.dataset.input) {
    const v = num(el.value);
    el.style.setProperty('--p', ((v - el.min) / (el.max - el.min)) * 100 + '%');
    if (el.dataset.input === 'years') { S.proj.years = v; $('#yrs-l').textContent = years(v); }
    else if (el.dataset.input === 'inflation') { S.profile.inflation = v; $('#inf-l').textContent = String(v).replace('.', ',') + '%'; }
    else { S.proj.monthly = v; $('#mon-l').textContent = money(v); }
    refreshProj();
    clearTimeout(el._t); el._t = setTimeout(persist, 400);
  }
});
document.addEventListener('keydown', e => {
  if (e.key === 'Enter' && e.target.dataset && e.target.dataset.draft) { e.preventDefault(); saveDraft(false); }
  if (e.key === 'Escape') closeSheet();
});
window.addEventListener('resize', () => movePill(false));

/* таймеры хотелок обновляются раз в минуту */
setInterval(() => { if (S.onboarded && S.tab === 'wishes' && !$('#sheet-root').classList.contains('open')) render(); }, 60000);

/* ---------- старт ---------- */
(function init() {
  if (tg) {
    try { tg.ready(); tg.expand(); } catch (e) {}
    try { can('7.7') && tg.disableVerticalSwipes(); } catch (e) {}
    try { can('6.1') && tg.BackButton.onClick(closeSheet); } catch (e) {}
    try { tg.onEvent('themeChanged', applyTheme); } catch (e) {}
  }
  render();
  cloudLoad(remote => { if (remote && remote.updatedAt > (S.updatedAt || 0)) { S = remote; $('#tabbar').dataset.ready = ''; render(); } });
})();
