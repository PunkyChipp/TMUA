import { md, mdi } from '../render/md.js';
import { plotSVG } from '../render/plot.js';
import { TOPIC } from '../data/topics.js';
import { esc, LETTERS, $ } from '../lib/util.js';

export function toast(msg, ms = 2400) {
  const t = $('#toast');
  if (!t) return;
  t.textContent = msg;
  t.hidden = false;
  clearTimeout(toast._t);
  toast._t = setTimeout(() => { t.hidden = true; }, ms);
}

export const diffDots = d => `<span class="diff" title="Difficulty ${d} of 5" aria-label="Difficulty ${d} of 5">${[1, 2, 3, 4, 5].map(i => `<i class="${i <= d ? 'on' : ''}"></i>`).join('')}</span>`;

export const topicChip = key => `<span class="chip">${esc(TOPIC[key]?.short || key)}</span>`;

export function figureHTML(fig) {
  if (!fig) return '';
  if (fig.plot) return `<div class="figure">${plotSVG(fig.plot, { width: 320, height: 240 })}</div>`;
  if (fig.svg && /^\s*<svg[\s>]/i.test(fig.svg) && !/<script|on\w+=/i.test(fig.svg)) return `<div class="figure">${fig.svg}</div>`;
  return '';
}

export function optionBody(o) {
  if (o && typeof o === 'object' && o.plot) return plotSVG(o.plot, { width: 260, height: 190, compact: true });
  return mdi(String(o));
}

export const hasPlots = q => q.options.some(o => o && typeof o === 'object');

// Options list. state: { sel, reveal (bool), answer, struck:Set }
export function optionsHTML(q, st = {}) {
  const plots = hasPlots(q);
  return `<div class="options${plots ? ' plots' : ''}" role="radiogroup" aria-label="Answer options">${q.options.map((o, i) => {
    const cls = ['opt'];
    if (st.sel === i) cls.push('sel');
    if (st.reveal) {
      if (i === q.answer) cls.push('right');
      else if (st.sel === i) cls.push('wrong');
    }
    if (st.struck?.has(i) && !st.reveal) cls.push('struck');
    return `<button class="${cls.join(' ')}" style="--i:${i}" data-act="choose" data-i="${i}" role="radio" aria-checked="${st.sel === i}" ${st.reveal ? 'disabled' : ''}>
      <span class="lozenge">${LETTERS[i]}</span><span class="otext">${optionBody(o)}</span></button>`;
  }).join('')}</div>`;
}

export function solutionHTML(q, choice) {
  const trap = choice != null && choice !== q.answer && q.distractors?.[choice];
  return `${q.insight ? `<div class="insight"><b>Key idea</b><div>${mdi(q.insight)}</div></div>` : ''}
    ${trap ? `<div class="trapnote"><b>Why ${LETTERS[choice]} is tempting</b><div>${mdi(trap)}</div></div>` : ''}
    <div class="solution">${md(q.solution)}</div>`;
}

export { md, mdi, esc };

// Hover tooltips for chart marks with data-tip.
let tipEl = null;
export function initTips() {
  document.addEventListener('pointerover', e => {
    const t = e.target.closest?.('[data-tip]');
    if (!t) { if (tipEl) tipEl.hidden = true; return; }
    if (!tipEl) { tipEl = document.createElement('div'); tipEl.className = 'tip'; document.body.appendChild(tipEl); }
    tipEl.textContent = t.getAttribute('data-tip');
    tipEl.hidden = false;
  });
  document.addEventListener('pointermove', e => {
    if (!tipEl || tipEl.hidden) return;
    const x = Math.min(window.innerWidth - tipEl.offsetWidth - 8, e.clientX + 12);
    tipEl.style.left = `${Math.max(8, x)}px`;
    tipEl.style.top = `${e.clientY + 14}px`;
  });
}
