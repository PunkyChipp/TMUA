import test from 'node:test';
import assert from 'node:assert/strict';
import { mergeStates } from '../src/lib/sync.js';
import { defaultState } from '../src/lib/store.js';

const a = (qid, at, extra = {}) => ({ qid, at, topic: 'alg', d: 3, ok: true, ms: 1000, ...extra });

test('merge unions attempts from both devices, in time order', () => {
  const phone = { ...defaultState(), attempts: [a('q1', 1), a('q2', 3)], updatedAt: 10 };
  const laptop = { ...defaultState(), attempts: [a('q1', 1), a('q3', 2)], updatedAt: 20 };
  const m = mergeStates(phone, laptop);
  assert.deepEqual(m.attempts.map(x => x.qid), ['q1', 'q3', 'q2']);
  assert.equal(m.updatedAt, 20);
});

test('a reason tagged on one device survives the merge', () => {
  const local = { ...defaultState(), attempts: [a('q1', 1, { ok: false })], updatedAt: 30 };
  const remote = { ...defaultState(), attempts: [a('q1', 1, { ok: false, reason: 'careless' })], updatedAt: 10 };
  assert.equal(mergeStates(local, remote).attempts[0].reason, 'careless');
});

test('settings follow the newer copy', () => {
  const local = { ...defaultState(), settings: { ...defaultState().settings, examDate: '2026-10-12' }, updatedAt: 5 };
  const remote = { ...defaultState(), settings: { ...defaultState().settings, examDate: '2026-10-15' }, updatedAt: 9 };
  assert.equal(mergeStates(local, remote).settings.examDate, '2026-10-15');
  assert.equal(mergeStates({ ...local, updatedAt: 99 }, remote).settings.examDate, '2026-10-12');
});

test('deleted papers stay deleted, with their attempts', () => {
  const paper = { id: 'p1', year: '2019', paper: 1, score: 15 };
  const local = { ...defaultState(), papers: [], tomb: { papers: ['p1'] }, attempts: [], updatedAt: 50 };
  const remote = { ...defaultState(), papers: [paper], attempts: [a('past:2019:1:1', 5, { pid: 'p1' })], updatedAt: 40 };
  const m = mergeStates(local, remote);
  assert.equal(m.papers.length, 0);
  assert.equal(m.attempts.length, 0);
});
