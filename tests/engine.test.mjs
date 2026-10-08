// Engine tests: ability model, selection, mocks and the study plan.
// (Run `npm run build` first so src/generated/content.js exists.)
import test from 'node:test';
import assert from 'node:assert/strict';
import { buildModel, predict, priorities } from '../src/engine/model.js';
import { smartSession, topicDrill, mockPaper, diagnostic } from '../src/engine/select.js';
import { buildPlan } from '../src/engine/plan.js';
import { defaultState } from '../src/lib/store.js';
import { TOPICS } from '../src/data/topics.js';

const att = (topic, ok, d = 3, n = 1) => Array.from({ length: n }, (_, i) => ({ qid: `x${topic}${i}${ok}`, topic, d, ok, ms: 60000, at: Date.now() - (n - i) * 1000, target: 200 }));

test('model: correct answers raise mastery, wrong answers lower it', () => {
  const up = buildModel(att('trig', true, 3, 10));
  const down = buildModel(att('trig', false, 3, 10));
  assert.ok(up.topics.trig.mastery > 0.6, `up ${up.topics.trig.mastery}`);
  assert.ok(down.topics.trig.mastery < 0.3, `down ${down.topics.trig.mastery}`);
  // Global ability carries some signal to untouched topics.
  assert.ok(up.topics.alg.mastery > down.topics.alg.mastery);
});

test('model: weak topics come first in priorities', () => {
  const m = buildModel([...att('alg', true, 3, 12), ...att('logic', false, 3, 12)]);
  const pri = priorities(m).map(p => p.key);
  assert.ok(pri.indexOf('logic') < pri.indexOf('alg'));
});

test('prediction stays within 0–20', () => {
  for (const a of [[], att('alg', true, 5, 40), att('alg', false, 1, 40)]) {
    const p = predict(buildModel(a));
    for (const k of [1, 2]) assert.ok(p[k].exp >= 0 && p[k].exp <= 20 && p[k].lo <= p[k].exp && p[k].exp <= p[k].hi);
  }
});

test('smart session: right length, no duplicates', () => {
  const st = defaultState();
  const m = buildModel([]);
  for (let r = 0; r < 20; r++) {
    const qs = smartSession(st, m, 12);
    assert.equal(qs.length, 12);
    assert.equal(new Set(qs.map(q => q.id)).size, 12);
  }
});

test('topic drill stays on topic', () => {
  const st = defaultState();
  const m = buildModel([]);
  for (const t of TOPICS) {
    const qs = topicDrill(st, m, t.key, 10);
    assert.ok(qs.length >= 8, `${t.key}: ${qs.length}`);
    assert.ok(qs.every(q => q.topic === t.key));
  }
});

test('mock papers: 20 distinct questions, Paper 2 heavy on logic and proof', () => {
  const st = defaultState();
  const m = buildModel([]);
  const p1 = mockPaper(st, m, 1);
  const p2 = mockPaper(st, m, 2);
  assert.equal(p1.length, 20); assert.equal(p2.length, 20);
  assert.equal(new Set(p1.map(q => q.id)).size, 20);
  assert.ok(p1.every(q => !['logic', 'proof', 'errors'].includes(q.topic)));
  assert.ok(p2.filter(q => ['logic', 'proof', 'errors'].includes(q.topic)).length >= 10);
});

test('diagnostic covers every topic', () => {
  const qs = diagnostic(defaultState(), buildModel([]));
  for (const t of TOPICS) assert.ok(qs.some(q => q.topic === t.key), t.key);
});

test('plan: one entry per day up to the exam, phases in order', () => {
  const st = defaultState();
  st.settings.examDate = '2026-10-14';
  const plan = buildPlan(st, buildModel([]), '2026-09-30');
  assert.equal(plan.days.length, 15);
  assert.equal(plan.days[0].tasks[0].id, 'diag');
  assert.equal(plan.days[14].phase.key, 'exam');
  assert.equal(plan.days[13].phase.key, 'taper');
  const papers = plan.days.flatMap(d => d.tasks).filter(t => t.kind === 'past');
  assert.ok(papers.length >= 5, `official papers scheduled: ${papers.length}`);
  assert.equal(new Set(papers.map(t => t.id)).size, papers.length);
});

import { alternativeTo, excludeFamily, FLOOR } from '../src/engine/select.js';
import { BANK, familyOf } from '../src/engine/bank.js';

test('a review alternative is never the question itself', () => {
  for (const q of BANK) {
    for (let k = 0; k < 3; k++) {
      const alt = alternativeTo(q, { seen: { [q.id]: { n: 1, ok: 0, last: 1 } } });
      assert.ok(alt, `${q.id}: no alternative`);
      assert.notEqual(alt.id, q.id, `${q.id}: alternative repeated the question`);
    }
  }
});

test('an unseen twin is preferred for reviews', () => {
  const withTwin = BANK.filter(q => familyOf(q).length > 1);
  for (const q of withTwin) {
    const alt = alternativeTo(q, { seen: { [q.id]: { n: 1, ok: 0, last: 1 } } });
    assert.ok(familyOf(q).includes(alt.id), `${q.id}: expected a twin, got ${alt.id}`);
  }
});

test('sessions never contain both twins of a family', () => {
  const st = defaultState();
  const m = buildModel([]);
  for (let r = 0; r < 10; r++) {
    for (const qs of [smartSession(st, m, 12), mockPaper(st, m, 1), mockPaper(st, m, 2)]) {
      const fams = qs.filter(q => q.family).map(q => q.family);
      assert.equal(new Set(fams).size, fams.length, 'twins in one session');
    }
  }
});

test('practice never serves below TMUA level', () => {
  const st = defaultState();
  const m = buildModel(att('alg', false, 3, 40)); // a weak student
  for (let r = 0; r < 10; r++) for (const q of smartSession(st, m, 12)) assert.ok(q.difficulty >= FLOOR - 1, `${q.id} level ${q.difficulty}`);
});

test('excludeFamily blocks every member', () => {
  const q = BANK.find(x => familyOf(x).length > 1) || BANK[0];
  const ex = new Set();
  excludeFamily(ex, q);
  for (const id of familyOf(q)) assert.ok(ex.has(id));
});
