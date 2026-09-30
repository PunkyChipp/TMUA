// Command palette: ⌘K / Ctrl+K / "/" — jump anywhere or start anything.
import { TOPICS } from '../data/topics.js';
import { esc } from '../lib/util.js';

let dlg = null, items = [], shown = [], sel = 0, runner = () => {};

function commands() {
  const c = [
    { g: 'Go to', t: 'Today', act: { go: 'today' } },
    { g: 'Go to', t: 'Practice', act: { go: 'practice' } },
    { g: 'Go to', t: 'Learn', act: { go: 'learn' } },
    { g: 'Go to', t: 'Mistakes', act: { go: 'review' } },
    { g: 'Go to', t: 'Progress', act: { go: 'progress' } },
    { g: 'Go to', t: 'Past papers', act: { go: 'papers' } },
    { g: 'Go to', t: 'Settings', act: { go: 'settings' } },
    { g: 'Start', t: 'Smart practice', k: 'mixed adaptive', act: { start: 'smart' } },
    { g: 'Start', t: 'Speed round', k: 'quick fluency', act: { start: 'speed' } },
    { g: 'Start', t: 'Mistake review', k: 'spaced repetition due', act: { start: 'review' } },
    { g: 'Start', t: 'Timed set', k: '10 questions 37 minutes', act: { start: 'timed' } },
    { g: 'Start', t: 'Mock Paper 1', k: 'full exam 75 minutes thinking', act: { start: 'mock', paper: 1 } },
    { g: 'Start', t: 'Mock Paper 2', k: 'full exam 75 minutes reasoning logic', act: { start: 'mock', paper: 2 } },
    { g: 'Start', t: 'Diagnostic', k: 'test', act: { start: 'diagnostic' } },
    { g: 'Read', t: 'Exam strategy', k: 'timing guessing', act: { note: 'strategy' } },
    { g: 'Read', t: 'Facts to know cold', k: 'formulas formula sheet', act: { note: 'facts' } },
  ];
  for (const t of TOPICS) {
    c.push({ g: 'Drill', t: t.name, k: t.short, act: { start: 'drill', topic: t.key } });
    c.push({ g: 'Read', t: `${t.name} notes`, k: t.short, act: { note: t.key } });
  }
  c.push({ g: 'Theme', t: 'Light', act: { theme: 'light' } }, { g: 'Theme', t: 'Dark', act: { theme: 'dark' } }, { g: 'Theme', t: 'Match system', act: { theme: 'system' } });
  return c;
}

function filter(q) {
  const toks = q.toLowerCase().split(/\s+/).filter(Boolean);
  const scored = [];
  for (const it of items) {
    const hay = `${it.g} ${it.t} ${it.k || ''}`.toLowerCase();
    if (!toks.every(tk => hay.includes(tk))) continue;
    const title = it.t.toLowerCase();
    const score = toks.reduce((s, tk) => s + (title.startsWith(tk) ? 3 : title.includes(tk) ? 2 : 1), 0);
    scored.push([score, it]);
  }
  return toks.length ? scored.sort((a, b) => b[0] - a[0]).map(x => x[1]) : items;
}

function paint() {
  const list = dlg.querySelector('.cmd-list');
  if (!shown.length) { list.innerHTML = '<li class="cmd-empty">No matches</li>'; return; }
  let lastG = null;
  list.innerHTML = shown.slice(0, 60).map((it, i) => {
    const head = !dlg.querySelector('input').value && it.g !== lastG ? `<li class="cmd-group" role="presentation">${esc(it.g)}</li>` : '';
    lastG = it.g;
    return `${head}<li role="option" id="cmd-${i}" class="cmd-item" aria-selected="${i === sel}" data-i="${i}"><span class="cmd-g">${esc(it.g)}</span><span>${esc(it.t)}</span></li>`;
  }).join('');
  list.querySelector('[aria-selected="true"]')?.scrollIntoView({ block: 'nearest' });
  dlg.querySelector('input').setAttribute('aria-activedescendant', `cmd-${sel}`);
}

function ensure() {
  if (dlg) return;
  dlg = document.createElement('dialog');
  dlg.className = 'cmdk';
  dlg.setAttribute('aria-label', 'Command palette');
  dlg.innerHTML = `<div class="cmd-box"><input class="cmd-input" id="cmd-input" type="text" placeholder="Type a command, topic or page…" autocomplete="off" role="combobox" aria-expanded="true" aria-controls="cmd-list"><ul class="cmd-list" id="cmd-list" role="listbox"></ul><div class="cmd-foot"><span><kbd>↑</kbd><kbd>↓</kbd> move</span><span><kbd>Enter</kbd> run</span><span><kbd>Esc</kbd> close</span></div></div>`;
  document.body.appendChild(dlg);
  const input = dlg.querySelector('input');
  input.addEventListener('input', () => { sel = 0; shown = filter(input.value); paint(); });
  input.addEventListener('keydown', e => {
    if (e.key === 'ArrowDown') { sel = Math.min(sel + 1, Math.min(shown.length, 60) - 1); paint(); e.preventDefault(); }
    else if (e.key === 'ArrowUp') { sel = Math.max(sel - 1, 0); paint(); e.preventDefault(); }
    else if (e.key === 'Enter') { const it = shown[sel]; if (it) { close(); runner(it.act); } e.preventDefault(); }
  });
  dlg.addEventListener('click', e => {
    if (e.target === dlg) { close(); return; }
    const li = e.target.closest('.cmd-item');
    if (li) { const it = shown[+li.dataset.i]; close(); runner(it.act); }
  });
}

export function openPalette() {
  ensure();
  items = commands();
  shown = items; sel = 0;
  const input = dlg.querySelector('input');
  input.value = '';
  paint();
  if (!dlg.open) dlg.showModal();
  input.focus();
}
export function close() { if (dlg?.open) dlg.close(); }
export const paletteOpen = () => !!dlg?.open;
export function setPaletteRunner(fn) { runner = fn; }
