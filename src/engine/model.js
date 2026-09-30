// Ability model: a global ability plus a per-topic offset on a logit scale
// (a light hierarchical Elo / Rasch model). Replayed from the attempt log so it
// is always consistent with the data.
import { TOPICS, TOPIC, LEVEL_B, DEFAULT_TIME } from '../data/topics.js';
import { sigmoid, DAY } from '../lib/util.js';

export function outcome(a) {
  // Credit: slow-but-right and guessed-right count for less; TMUA is a speed test.
  if (!a.ok) return 0;
  let y = 1;
  if (a.guess) y = 0.55;
  const target = a.target || DEFAULT_TIME[a.d] || 200;
  if (a.ms && a.ms > target * 1000 * 1.7) y = Math.min(y, 0.75);
  return y;
}

export function buildModel(attempts) {
  let g = 0;             // global ability
  const t = {};          // topic offsets
  const n = {};          // attempts per topic
  const ok = {};         // correct per topic
  const ms = {};         // total ms per topic
  const last = {};       // last attempt time per topic
  const recent = {};     // last 8 outcomes per topic
  let total = 0;
  for (const k of TOPICS) { t[k.key] = 0; n[k.key] = 0; ok[k.key] = 0; ms[k.key] = 0; recent[k.key] = []; }
  for (const a of attempts) {
    if (a.topic && !TOPIC[a.topic]) continue;
    const b = LEVEL_B[a.d] ?? 0;
    const y = outcome(a);
    const w = a.weight ?? 1;
    total++;
    if (!a.topic) { // past-paper question with unknown topic: global only
      const p = sigmoid(g - b);
      g += w * (0.9 / (1 + 0.04 * total)) * (y - p);
      continue;
    }
    const k = a.topic;
    const p = sigmoid(g + t[k] - b);
    const kg = w * Math.max(0.05, 0.9 / (1 + 0.04 * total));
    const kt = w * Math.max(0.12, 1.1 / (1 + 0.18 * n[k]));
    g += kg * (y - p) * 0.6;
    t[k] += kt * (y - p);
    n[k]++; if (a.ok) ok[k]++; ms[k] += a.ms || 0; last[k] = a.at;
    recent[k].push(a.ok ? 1 : 0); if (recent[k].length > 8) recent[k].shift();
  }
  const topics = {};
  for (const k of TOPICS) {
    const theta = g + t[k.key];
    topics[k.key] = {
      key: k.key, theta, n: n[k.key], ok: ok[k.key], acc: n[k.key] ? ok[k.key] / n[k.key] : null,
      avgMs: n[k.key] ? ms[k.key] / n[k.key] : null, last: last[k.key] || null,
      // Mastery: chance of getting a typical (level 3.5) TMUA question right.
      mastery: sigmoid(theta - 0.4),
      confidence: Math.min(1, n[k.key] / 8),
      recent: recent[k.key],
    };
  }
  return { g, topics, total };
}

export const pCorrect = (model, topic, level) => sigmoid((model.topics[topic]?.theta ?? model.g) - (LEVEL_B[level] ?? 0));

// Expected marks out of 20 on each paper, averaging over a realistic difficulty mix.
const MIX = [[2, 0.2], [3, 0.35], [4, 0.3], [5, 0.15]];
export function predict(model) {
  const out = {};
  for (const paper of [1, 2]) {
    let e = 0, conf = 0, wsum = 0;
    for (const k of TOPICS) {
      const w = paper === 1 ? k.w1 : k.w2;
      if (!w) continue;
      const p = MIX.reduce((s, [lv, m]) => s + m * pCorrect(model, k.key, lv), 0);
      e += w * p; wsum += w; conf += w * model.topics[k.key].confidence;
    }
    const exp = (20 * e) / wsum;
    const c = conf / wsum;
    const spread = 1.5 + 3.5 * (1 - c);
    out[paper] = { exp, lo: Math.max(0, exp - spread), hi: Math.min(20, exp + spread), confidence: c };
  }
  return out;
}

// Priority for practice: how much a topic is worth working on right now.
export function priorities(model, now = Date.now()) {
  return TOPICS.map(k => {
    const s = model.topics[k.key];
    const weight = (k.w1 + k.w2) / 2;
    const gap = 1 - s.mastery;
    const unknown = 1 - s.confidence;
    const days = s.last ? (now - s.last) / DAY : 7;
    const stale = Math.min(1, days / 5);
    const score = weight * (1.6 * gap + 0.9 * unknown + 0.35 * stale) + 0.01;
    return { key: k.key, score, gap, unknown, stale };
  }).sort((a, b) => b.score - a.score);
}

export function masteryLabel(m, n) {
  if (n < 3) return { label: 'Not enough data', tone: 'none' };
  if (m >= 0.8) return { label: 'Secure', tone: 'good' };
  if (m >= 0.62) return { label: 'Solid', tone: 'ok' };
  if (m >= 0.45) return { label: 'Shaky', tone: 'warn' };
  return { label: 'Weak', tone: 'bad' };
}
