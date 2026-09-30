// Signature visuals: the fortnight dial and the mastery wheel (inline SVG).
import { TOPICS } from '../data/topics.js';
import { masteryLabel } from '../engine/model.js';
import { esc, dateKey, addDays, fmtDate, pct } from '../lib/util.js';

const TAU = Math.PI * 2;
const pt = (cx, cy, r, a) => [cx + r * Math.cos(a), cy + r * Math.sin(a)];
function arc(cx, cy, r0, r1, a0, a1) {
  const large = a1 - a0 > Math.PI ? 1 : 0;
  const [x0, y0] = pt(cx, cy, r1, a0), [x1, y1] = pt(cx, cy, r1, a1);
  const [x2, y2] = pt(cx, cy, r0, a1), [x3, y3] = pt(cx, cy, r0, a0);
  return `M${x0.toFixed(2)},${y0.toFixed(2)}A${r1},${r1} 0 ${large} 1 ${x1.toFixed(2)},${y1.toFixed(2)}L${x2.toFixed(2)},${y2.toFixed(2)}A${r0},${r0} 0 ${large} 0 ${x3.toFixed(2)},${y3.toFixed(2)}Z`;
}

// 15 segments: the fortnight before the test plus test day. Segment shade = questions
// answered that day; an outer tick marks days whose plan was completed.
export function fortnightDial(st, exam, today = dateKey()) {
  const days = 15;
  const start = addDays(exam, -(days - 1));
  const counts = {};
  for (const a of st.attempts) { const k = dateKey(a.at); counts[k] = (counts[k] || 0) + 1; }
  const cx = 120, cy = 120, r0 = 84, r1 = 108;
  const seg = TAU / days, gap = 0.035;
  let left = 0;
  const parts = [];
  for (let i = 0; i < days; i++) {
    const k = addDays(start, i);
    const n = counts[k] || 0;
    const a0 = -Math.PI / 2 + i * seg + gap, a1 = -Math.PI / 2 + (i + 1) * seg - gap;
    const isToday = k === today, isExam = k === exam, past = k < today;
    if (k >= today && !isExam) left++;
    const heat = Math.min(1, n / 30);
    const cls = isExam ? 'd-exam' : isToday ? 'd-today' : past ? (n ? 'd-done' : 'd-miss') : 'd-future';
    const tasksDone = (st.plan[k] || []).length;
    const tip = `${fmtDate(k)}${isExam ? ' · test day' : isToday ? ' · today' : ''}: ${n} answered${tasksDone ? ` · ${tasksDone} plan task${tasksDone === 1 ? '' : 's'} done` : ''}`;
    parts.push(`<path class="dseg ${cls}" style="--heat:${heat.toFixed(2)};--i:${i}" d="${arc(cx, cy, r0, r1, a0, a1)}" data-tip="${esc(tip)}"/>`);
    if (tasksDone >= 2 && !isExam) {
      const [x, y] = pt(cx, cy, r1 + 7, (a0 + a1) / 2);
      parts.push(`<circle class="dtick" cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="2.6"/>`);
    }
  }
  const daysLeft = Math.max(0, Math.round((new Date(exam) - new Date(today)) / 86400000));
  return `<svg class="dial" viewBox="0 0 240 240" role="img" aria-label="${daysLeft} days to go. Each segment is a day of the fortnight, shaded by questions answered.">
    <circle class="dial-face" cx="${cx}" cy="${cy}" r="${r0 - 8}"/>
    ${parts.join('')}
    <text class="dial-num" x="${cx}" y="${cy + 14}" text-anchor="middle">${daysLeft}</text>
    <text class="dial-lab" x="${cx}" y="${cy + 38}" text-anchor="middle">${daysLeft === 1 ? 'DAY TO GO' : 'DAYS TO GO'}</text>
  </svg>`;
}

const WHEEL_LABEL = { number: 'Number', alg: 'Algebra', graphs: 'Graphs', coord: 'Coords', seq: 'Sequences', trig: 'Trig', explog: 'Logs', diff: 'Diff', integ: 'Integration', geom: 'Geometry', prob: 'Probability', logic: 'Logic', proof: 'Proof', errors: 'Errors' };

const TONE = { good: 'w-good', ok: 'w-ok', warn: 'w-warn', bad: 'w-bad', none: 'w-none' };

// Polar bars: one wedge per topic, radius = mastery. Paper 2 topics sit together at the end.
export function masteryWheel(model, { size = 320, interactive = true } = {}) {
  const cx = size / 2, cy = size / 2;
  const inner = size * 0.12, outer = size * 0.36;
  const n = TOPICS.length, seg = TAU / n, gap = 0.03;
  const rings = [0.45, 0.62, 0.8].map(m => `<circle class="w-ring" cx="${cx}" cy="${cy}" r="${(inner + (outer - inner) * m).toFixed(1)}"/>`).join('');
  const wedges = TOPICS.map((t, i) => {
    const m = model.topics[t.key];
    const ml = masteryLabel(m.mastery, m.n);
    const a0 = -Math.PI / 2 + (i - 0.5) * seg + gap, a1 = -Math.PI / 2 + (i + 0.5) * seg - gap;
    const val = m.n ? Math.max(0.06, m.mastery) : 0.22;
    const r = inner + (outer - inner) * val;
    const mid = (a0 + a1) / 2;
    const [lx, ly] = pt(cx, cy, outer + size * 0.06, mid);
    const anchor = Math.abs(Math.cos(mid)) < 0.3 ? 'middle' : Math.cos(mid) > 0 ? 'start' : 'end';
    const tip = `${t.name}: ${m.n ? `${pct(m.mastery)} mastery · ${m.ok}/${m.n} right` : 'not practised yet'}`;
    return `<g class="wg${interactive ? ' click' : ''}" ${interactive ? `data-act="start" data-kind="drill" data-topic="${t.key}"` : ''} data-tip="${esc(tip)}" style="--i:${i}">
      <path class="w-bg" d="${arc(cx, cy, inner, outer, a0, a1)}"/>
      <path class="w-val ${TONE[ml.tone]}" d="${arc(cx, cy, inner, r, a0, a1)}"/>
      <text class="w-lab${t.paper === 2 ? ' p2' : ''}" x="${lx.toFixed(1)}" y="${(ly + 4).toFixed(1)}" text-anchor="${anchor}">${esc(WHEEL_LABEL[t.key] || t.short)}</text>
    </g>`;
  }).join('');
  // Bracket marking the Paper 2 topics.
  const p2i = TOPICS.findIndex(t => t.paper === 2);
  const b0 = -Math.PI / 2 + (p2i - 0.5) * seg, b1 = -Math.PI / 2 + (n - 0.5) * seg;
  const br = outer + 4;
  const [bx0, by0] = pt(cx, cy, br, b0 + 0.02), [bx1, by1] = pt(cx, cy, br, b1 - 0.02);
  return `<svg class="wheel" viewBox="${-size * 0.2} 0 ${size * 1.4} ${size}" role="img" aria-label="Mastery by topic">
    <defs><pattern id="hatch" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="5" height="5" class="hatch-bg"/><line x1="0" y1="0" x2="0" y2="5" class="hatch-ln"/></pattern></defs>
    ${rings}${wedges}
    <path class="w-p2" d="M${bx0.toFixed(1)},${by0.toFixed(1)}A${br},${br} 0 0 1 ${bx1.toFixed(1)},${by1.toFixed(1)}"/>
    <circle class="w-hub" cx="${cx}" cy="${cy}" r="${inner - 4}"/>
  </svg>`;
}
