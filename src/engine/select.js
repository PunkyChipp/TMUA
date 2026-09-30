// Adaptive question selection.
import { BANK, BY_TOPIC, getQuestion, srsKey } from './bank.js';
import { GENERATORS, genQuestion } from '../gen/index.js';
import { TOPICS, TOPIC } from '../data/topics.js';
import { pCorrect, priorities } from './model.js';
import { dueReviews } from '../lib/store.js';
import { randomSeed } from '../lib/rng.js';

const rand = () => Math.random();
const pickW = items => { // items: [item, weight]
  const tot = items.reduce((s, [, w]) => s + w, 0);
  let r = rand() * tot;
  for (const [it, w] of items) { if ((r -= w) <= 0) return it; }
  return items[items.length - 1]?.[0];
};

export function seenMap(attempts) {
  const m = {};
  for (const a of attempts) {
    const e = (m[a.qid] ||= { n: 0, ok: 0, last: 0 });
    e.n++; if (a.ok) e.ok++; e.last = a.at;
  }
  return m;
}

// Level where predicted success is closest to the sweet spot (~65%).
export function targetLevel(model, topic, sweet = 0.65) {
  let best = 3, bd = 9;
  for (let lv = 1; lv <= 5; lv++) {
    const d = Math.abs(pCorrect(model, topic, lv) - sweet);
    if (d < bd) { bd = d; best = lv; }
  }
  // Gentle jitter so sessions are not monotonous.
  const j = rand();
  if (j < 0.18 && best > 1) best--;
  else if (j > 0.82 && best < 5) best++;
  return best;
}

function genFor(topic, level) {
  const gens = GENERATORS.filter(g => g.topic === topic);
  if (!gens.length) return null;
  const fits = gens.filter(g => level >= g.levels[0] && level <= g.levels[1]);
  const g = (fits.length ? fits : gens)[Math.floor(rand() * (fits.length ? fits.length : gens.length))];
  return genQuestion(g.id, level, randomSeed());
}

export function pickForTopic(topic, model, ctx) {
  const { exclude, seen, reported, paper, level: forced, preferBank = 0.7 } = ctx;
  const level = forced ?? targetLevel(model, topic);
  const pool = (BY_TOPIC[topic] || []).filter(q => !exclude.has(q.id) && !reported[q.id] && (!paper || q.paper === paper || rand() < 0.35));
  const unseen = pool.filter(q => !seen[q.id]);
  const useBank = unseen.length && (rand() < preferBank || !GENERATORS.some(g => g.topic === topic));
  if (useBank) {
    const scored = unseen.map(q => [q, 1 / (1 + 2.2 * Math.abs(q.difficulty - level))]);
    return pickW(scored);
  }
  const gq = genFor(topic, level);
  if (gq) return gq;
  // No generators (e.g. errors in proofs): reuse the least recently seen bank question.
  const old = pool.filter(q => seen[q.id]).sort((a, b) => seen[a.id].last - seen[b.id].last);
  return old[0] || null;
}

function reviewItem(r, seen, exclude) {
  if (r.key.startsWith('g:')) {
    const [, genId, lv] = r.key.split(':');
    return genQuestion(genId, +lv, randomSeed()) || null;
  }
  const q = getQuestion(r.key);
  if (!q || exclude.has(q.id)) return null;
  return { ...q };
}

// Spread topics so the same topic never appears twice in a row where avoidable.
function interleave(qs) {
  const out = [];
  const rest = qs.slice();
  while (rest.length) {
    const prev = out[out.length - 1];
    let i = rest.findIndex(q => !prev || q.topic !== prev.topic);
    if (i < 0) i = 0;
    out.push(rest.splice(i, 1)[0]);
  }
  return out;
}

export function smartSession(state, model, n = 12) {
  const seen = seenMap(state.attempts);
  const exclude = new Set();
  const out = [];
  const reviews = dueReviews().slice(0, Math.ceil(n * 0.3));
  for (const r of reviews) {
    const q = reviewItem(r, seen, exclude);
    if (q) { q._review = true; out.push(q); exclude.add(q.id); }
  }
  const pri = priorities(model);
  const perTopic = {};
  let guard = 0;
  while (out.length < n && guard++ < 100) {
    const k = pickW(pri.map(p => [p.key, Math.pow(p.score, 1.4)]));
    if ((perTopic[k] || 0) >= 3) continue;
    const q = pickForTopic(k, model, { exclude, seen, reported: state.reported });
    if (!q) continue;
    perTopic[k] = (perTopic[k] || 0) + 1;
    exclude.add(q.id); out.push(q);
  }
  return interleave(out);
}

export function topicDrill(state, model, topic, n = 10) {
  const seen = seenMap(state.attempts);
  const exclude = new Set();
  const out = [];
  let guard = 0;
  while (out.length < n && guard++ < 60) {
    const q = pickForTopic(topic, model, { exclude, seen, reported: state.reported, preferBank: 0.6 });
    if (!q) break;
    if (exclude.has(q.id)) continue;
    exclude.add(q.id); out.push(q);
  }
  return out;
}

export function reviewSession(state, n = 15) {
  const seen = seenMap(state.attempts);
  const exclude = new Set();
  const out = [];
  for (const r of dueReviews()) {
    if (out.length >= n) break;
    const q = reviewItem(r, seen, exclude);
    if (q) { q._review = true; out.push(q); exclude.add(q.id); }
  }
  return interleave(out);
}

// Mock paper: 20 questions spread by the paper's topic weights, easier first.
export function mockPaper(state, model, paper, n = 20) {
  const seen = seenMap(state.attempts);
  const exclude = new Set();
  const w = TOPICS.map(t => [t.key, paper === 1 ? t.w1 : t.w2]).filter(([, x]) => x > 0);
  const tot = w.reduce((s, [, x]) => s + x, 0);
  // Largest-remainder allocation of n questions.
  const alloc = w.map(([k, x]) => ({ k, exact: (n * x) / tot }));
  alloc.forEach(a => { a.c = Math.floor(a.exact); a.r = a.exact - a.c; });
  let left = n - alloc.reduce((s, a) => s + a.c, 0);
  alloc.sort((a, b) => b.r - a.r).forEach(a => { if (left > 0) { a.c++; left--; } });
  const levels = [2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 5, 5, 5];
  const shuffledLv = levels.sort(() => rand() - 0.5);
  let li = 0;
  const out = [];
  for (const a of alloc) {
    for (let i = 0; i < a.c; i++) {
      const lv = shuffledLv[li++ % shuffledLv.length];
      const q = pickForTopic(a.k, model, { exclude, seen, reported: state.reported, paper, level: lv, preferBank: 0.85 });
      if (q) { exclude.add(q.id); out.push(q); }
    }
  }
  return out.sort((a, b) => a.difficulty - b.difficulty + (rand() - 0.5) * 1.2);
}

export function timedSet(state, model, n = 10) {
  return smartSession(state, model, n).sort((a, b) => a.difficulty - b.difficulty);
}

// Diagnostic: one mid-level question per topic plus extra logic, bank first.
export function diagnostic(state, model) {
  const seen = seenMap(state.attempts);
  const exclude = new Set();
  const out = [];
  const plan = TOPICS.map(t => [t.key, 3]).concat([['logic', 2], ['alg', 4]]);
  for (const [k, lv] of plan) {
    const q = pickForTopic(k, model, { exclude, seen, reported: state.reported, level: lv, preferBank: 1 });
    if (q) { exclude.add(q.id); out.push(q); }
  }
  return out.sort((a, b) => (TOPIC[a.topic].paper - TOPIC[b.topic].paper) || (a.difficulty - b.difficulty));
}

export { srsKey, BANK };

// Speed round: quick generated questions (levels 1–2) weighted to weaker topics, tight targets.
export function speedRound(model, n = 10) {
  const gens = GENERATORS.filter(g => g.levels[0] <= 2);
  const pri = Object.fromEntries(priorities(model).map(p => [p.key, p.score]));
  const out = [];
  let guard = 0;
  while (out.length < n && guard++ < 100) {
    const g = pickW(gens.map(x => [x, pri[x.topic] || 0.01]));
    if (out.filter(q => q.gen === g.id).length >= 2) continue;
    const q = genQuestion(g.id, Math.min(2, g.levels[1]), randomSeed());
    if (q) { q.time = Math.min(q.time || 90, 75); out.push(q); }
  }
  return interleave(out);
}
