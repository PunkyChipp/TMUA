// Persistent state in localStorage, with a safe in-memory fallback.
import { dateKey, addDays } from './util.js';

const KEY = 'tmua-fortnight-v1';
const listeners = new Set();

export function defaultState() {
  return {
    v: 1,
    settings: { examDate: '2026-10-12', dailyMinutes: 120, theme: 'system', onboarded: false, sound: false },
    attempts: [],      // { qid, topic, d, ok, ms, at, mode, choice, guess, reason }
    srs: {},           // key -> { box, due, lapses, last, topic }
    plan: {},          // dateKey -> [taskId, …] completed
    papers: [],        // logged official past papers
    sessions: [],      // finished session summaries
    flags: {},         // qid -> true (bookmarked)
    reported: {},      // qid -> note (excluded from selection)
    diag: null,        // { done: ts }
    learned: {},       // topic -> ts note read
    active: null,      // resumable mock/session snapshot
    tomb: { papers: [] }, // deleted past-paper ids (so sync merges don't resurrect them)
    updatedAt: 0,
  };
}

let state = load();

function load() {
  try {
    const raw = localStorage.getItem(KEY);
    if (raw) return migrate({ ...defaultState(), ...JSON.parse(raw) });
  } catch (e) { /* storage unavailable */ }
  return defaultState();
}

function migrate(s) {
  s.settings = { ...defaultState().settings, ...s.settings };
  s.tomb = { papers: [], ...(s.tomb || {}) };
  return s;
}

let saveTimer = null;
export function save() {
  clearTimeout(saveTimer);
  saveTimer = setTimeout(() => {
    try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) { /* quota or blocked */ }
  }, 50);
}

export const S = () => state;
export function update(fn) {
  fn(state);
  state.updatedAt = Date.now();
  save();
  for (const l of listeners) l(state, 'local');
}

// Replace state with a merged copy that came from another device.
export function applyRemote(next) {
  state = migrate({ ...defaultState(), ...next });
  save();
  for (const l of listeners) l(state, 'remote');
}
export const subscribe = fn => (listeners.add(fn), () => listeners.delete(fn));

export function replaceState(next) {
  state = migrate({ ...defaultState(), ...next, updatedAt: Date.now() });
  save();
  for (const l of listeners) l(state, 'local');
}
export function resetState() { replaceState(defaultState()); }

export function exportState() { return JSON.stringify(state); }

export function storageWorks() {
  try { localStorage.setItem('__t', '1'); localStorage.removeItem('__t'); return true; } catch (e) { return false; }
}

// Spaced repetition (Leitner boxes). Intervals in days per box.
const INTERVALS = [0, 1, 3, 7, 14];

export function srsRecord(key, topic, ok, now = Date.now()) {
  const today = dateKey(now);
  const cur = state.srs[key];
  if (!ok) {
    state.srs[key] = { box: 1, due: addDays(today, 1), lapses: (cur?.lapses || 0) + 1, last: now, topic };
  } else if (cur) {
    const box = Math.min(cur.box + 1, INTERVALS.length - 1);
    if (box >= INTERVALS.length - 1 && cur.box >= 3) delete state.srs[key]; // graduated
    else state.srs[key] = { ...cur, box, due: addDays(today, INTERVALS[box]), last: now };
  }
}

export function dueReviews(today = dateKey()) {
  return Object.entries(state.srs)
    .filter(([, v]) => v.due <= today)
    .sort((a, b) => a[1].due.localeCompare(b[1].due))
    .map(([k, v]) => ({ key: k, ...v }));
}
