export const $ = (sel, el = document) => el.querySelector(sel);
export const $$ = (sel, el = document) => Array.from(el.querySelectorAll(sel));

export function esc(s) {
  return String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}

export const LETTERS = 'ABCDEFGH';
export const clamp = (x, lo, hi) => Math.max(lo, Math.min(hi, x));
export const sigmoid = x => 1 / (1 + Math.exp(-x));
export const logit = p => Math.log(p / (1 - p));
export const sum = arr => arr.reduce((a, b) => a + b, 0);
export const mean = arr => (arr.length ? sum(arr) / arr.length : 0);

export const DAY = 86400000;

// Local calendar date as YYYY-MM-DD.
export function dateKey(t = Date.now()) {
  const d = new Date(t);
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
}
export function parseDateKey(k) {
  const [y, m, d] = k.split('-').map(Number);
  return new Date(y, m - 1, d).getTime();
}
export function daysBetween(aKey, bKey) {
  return Math.round((parseDateKey(bKey) - parseDateKey(aKey)) / DAY);
}
export function addDays(key, n) {
  const d = new Date(parseDateKey(key));
  d.setDate(d.getDate() + n);
  return dateKey(d.getTime());
}
export function fmtDate(key, opts = { weekday: 'short', day: 'numeric', month: 'short' }) {
  return new Date(parseDateKey(key)).toLocaleDateString('en-GB', opts);
}

export function fmtClock(ms) {
  const s = Math.max(0, Math.round(ms / 1000));
  const m = Math.floor(s / 60);
  return `${m}:${String(s % 60).padStart(2, '0')}`;
}
export function fmtSecs(ms) {
  const s = Math.round(ms / 1000);
  return s < 60 ? `${s}s` : `${Math.floor(s / 60)}m ${String(s % 60).padStart(2, '0')}s`;
}
export const pct = (x, digits = 0) => `${(x * 100).toFixed(digits)}%`;

export function uid() {
  return Date.now().toString(36) + Math.random().toString(36).slice(2, 7);
}

// Simple hash for deterministic per-day choices.
export function hashStr(s) {
  let h = 2166136261;
  for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); }
  return h >>> 0;
}
