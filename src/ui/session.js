// Session runner: practice (instant feedback) and test (exam conditions) modes.
import { S, update, srsRecord } from '../lib/store.js';
import { getQuestion, srsKey, targetMs } from '../engine/bank.js';
import { genQuestion } from '../gen/index.js';
import { pickForTopic, seenMap } from '../engine/select.js';
import { buildModel } from '../engine/model.js';
import { TOPIC, EXAM } from '../data/topics.js';
import { randomSeed } from '../lib/rng.js';
import { esc, LETTERS, fmtClock, fmtSecs, uid, dateKey, pct, $ } from '../lib/util.js';
import { ICON } from './icons.js';
import { md, mdi, diffDots, topicChip, figureHTML, optionsHTML, solutionHTML, toast } from './common.js';
import { tutorHTML, hint as tutorHint, explain as tutorExplain, stop as tutorStop, keyOf } from './tutor.js';

export const REASONS = [
  ['concept', 'Didn\'t know the method'],
  ['careless', 'Careless slip'],
  ['misread', 'Misread the question'],
  ['trap', 'Fell for a trap'],
  ['time', 'Rushed / ran out of time'],
  ['guess', 'Guessed'],
];

let cur = null;
let tick = null;
let hooks = { done: () => {}, render: () => {} };

export const activeSession = () => cur;
export function setSessionHooks(h) { hooks = { ...hooks, ...h }; }

const blankResp = () => ({ choice: null, ms: 0, flag: false, guess: false, checked: false, ok: null, reason: null, struck: [] });

export function startSession({ kind, title, qs, test = false, limitMs = null, taskId = null, paper = null }) {
  qs = qs.filter(Boolean);
  if (!qs.length) { toast('Nothing to practise here yet.'); return false; }
  cur = {
    id: uid(), kind, title, test, limitMs, taskId, paper, qs, i: 0,
    resp: qs.map(blankResp), start: Date.now(), qStart: Date.now(), finished: false, view: null,
  };
  persistActive();
  return true;
}

export function resumeActive() {
  const a = S().active;
  if (!a) return false;
  const qs = a.ids.map(getQuestion).filter(Boolean);
  if (qs.length !== a.ids.length) { update(s => { s.active = null; }); return false; }
  cur = { ...a, qs, qStart: Date.now(), finished: false, view: null };
  // Time spent away does not count on a practice session; a test keeps running on the wall clock.
  return true;
}

export function discardActive() {
  cur = null;
  update(s => { s.active = null; });
}

function persistActive() {
  if (!cur || !cur.test) return;
  const { qs, view, ...rest } = cur;
  update(s => { s.active = { ...rest, ids: qs.map(q => q.id) }; });
}

function stampTime() {
  if (!cur) return;
  const now = Date.now();
  const r = cur.resp[cur.i];
  if (r && !(r.checked && !cur.test)) r.ms += Math.min(now - cur.qStart, 20 * 60 * 1000);
  cur.qStart = now;
}

const elapsed = () => Date.now() - cur.start;
const remaining = () => (cur.limitMs ? cur.limitMs - elapsed() : null);

function recordAttempt(q, r, mode) {
  update(s => {
    s.attempts.push({
      qid: q.id, topic: q.topic, d: q.difficulty, ok: r.ok, ms: Math.round(r.ms), at: Date.now(), mode,
      choice: r.choice, guess: r.guess || undefined, hint: r.hint || undefined, target: Math.round(targetMs(q) / 1000), sid: cur.id,
    });
    srsRecord(srsKey(q), q.topic, r.ok);
  });
}

function setReason(k, reason) {
  const r = cur.resp[k];
  r.reason = r.reason === reason ? null : reason;
  const q = cur.qs[k];
  update(s => {
    for (let j = s.attempts.length - 1; j >= 0; j--) {
      const a = s.attempts[j];
      if (a.sid === cur.id && a.qid === q.id) { a.reason = r.reason || undefined; break; }
    }
  });
}

// ---------------------------------------------------------------- rendering

export function renderSession() {
  if (!cur) return '';
  if (cur.finished) return renderResults();
  return cur.test ? renderTest() : renderPractice();
}

function header() {
  const n = cur.qs.length;
  const done = cur.resp.filter(r => (cur.test ? r.choice != null : r.checked)).length;
  return `<div class="stack">
    <div class="spread">
      <div class="stack" style="gap:2px"><span class="eyebrow">${esc(cur.test ? 'Exam conditions' : 'Practice')}</span><h2>${esc(cur.title)}</h2></div>
      <div class="row">
        <span class="clock" id="sess-clock">${ICON.clock}<span>${cur.limitMs ? fmtClock(remaining()) : fmtClock(elapsed())}</span></span>
        <button class="btn sm ghost" data-act="sess-quit">${cur.test ? 'Save & exit' : 'End'}</button>
      </div>
    </div>
    <div class="progress-line" aria-hidden="true"><i style="width:${(100 * done) / n}%"></i></div>
  </div>`;
}

function qTop(q, k) {
  return `<div class="qhead">
    <div class="qmeta"><span class="qnum">Q${k + 1}<span class="muted"> / ${cur.qs.length}</span></span>${topicChip(q.topic)}${diffDots(q.difficulty)}
      ${q._review ? '<span class="chip tone-warn">Review</span>' : ''}${q.paper === 2 && TOPIC[q.topic].paper === 1 ? '<span class="chip">Paper 2 style</span>' : ''}</div>
    ${cur.test ? '' : `<span class="clock" id="q-clock" data-target="${targetMs(q)}" aria-label="Time on this question">${ringSVG(0)}<span>0:00</span></span>`}
  </div>`;
}

function renderPractice() {
  const q = cur.qs[cur.i], r = cur.resp[cur.i];
  const fresh = cur.fresh === cur.i;
  cur.fresh = null;
  const flagged = !!S().flags[q.id];
  let fb = '';
  if (r.checked) {
    const tgt = targetMs(q);
    fb = `<div class="feedback">
      <div class="verdict ${r.ok ? 'ok' : 'no'}">
        <span class="big">${r.ok ? 'Correct' : r.choice == null ? 'Revealed' : 'Not quite'}</span>
        <span class="muted">${r.ok ? '' : `Answer: <b>${LETTERS[q.answer]}</b> · `}${fmtSecs(r.ms)} <span class="small">(target ${fmtSecs(tgt)})</span></span>
        ${r.ok && r.ms > tgt * 1.5 ? '<span class="chip tone-warn">Right, but slow</span>' : ''}
      </div>
      ${!r.ok ? `<div class="stack" style="gap:8px"><span class="eyebrow">Why did you miss it?</span><div class="reasons">${REASONS.map(([k, l]) => `<button class="chip" data-act="reason" data-r="${k}" aria-pressed="${r.reason === k}">${l}</button>`).join('')}</div></div>` : ''}
      ${solutionHTML(q, r.choice)}
      ${tutorHTML(q, r)}
    </div>`;
  }
  return `<div class="col">
    ${header()}
    <article class="sheet qsheet${fresh ? ' fresh' : ''}" aria-live="polite">
      ${qTop(q, cur.i)}
      <div class="stem">${md(q.stem)}</div>
      ${figureHTML(q.figure)}
      ${optionsHTML(q, { sel: r.choice, reveal: r.checked, struck: new Set(r.struck) })}
      <div class="actions">
        <div class="left">
          ${r.checked ? `<button class="btn sm ghost" data-act="flag" aria-pressed="${flagged}">${ICON.bookmark}${flagged ? 'Saved' : 'Save'}</button>
            <button class="btn sm ghost" data-act="report">Report a problem</button>`
            : `<label class="toggle"><input type="checkbox" id="guess-toggle" data-act="guess" ${r.guess ? 'checked' : ''}> I'm guessing</label>${tutorHTML(q, r, { before: true })}`}
        </div>
        <div class="right">
          ${r.checked
            ? `${q.gen || TOPIC[q.topic] ? `<button class="btn" data-act="similar">Try a similar one</button>` : ''}
               <button class="btn primary" data-act="next">${cur.i + 1 < cur.qs.length ? 'Next' : 'Finish'} <kbd>Enter</kbd></button>`
            : `<button class="btn ghost" data-act="reveal">Show answer</button>
               <button class="btn primary" data-act="check" ${r.choice == null ? 'disabled' : ''}>Check <kbd>Enter</kbd></button>`}
        </div>
      </div>
      ${r.checked ? fb : tutorHTML(q, r, { before: 'bubble' })}
    </article>
    <div class="keys"><span><kbd>A</kbd>–<kbd>H</kbd> choose</span><span><kbd>Shift</kbd>+letter or right-click to cross out</span><span><kbd>G</kbd> guess</span><span><kbd>Enter</kbd> check / next</span></div>
  </div>`;
}

function paceLine() {
  const n = cur.qs.length;
  const perQ = cur.limitMs ? cur.limitMs / n : EXAM.perQ * 1000;
  const shouldBe = Math.min(n, Math.floor(elapsed() / perQ) + 1);
  const answered = cur.resp.filter(r => r.choice != null).length;
  const diff = answered - (shouldBe - 1);
  const frac = Math.min(1, elapsed() / (perQ * n));
  return `<div class="stack" id="pace" style="gap:6px;min-width:min(100%,320px)">
    <div class="pacebar" aria-hidden="true"><i style="width:${(100 * answered) / n}%"></i><b style="left:calc(${(frac * 100).toFixed(2)}% - 1px)"></b></div>
    <span class="pace">Ideal pace: <b>Q${shouldBe}</b> now · answered <b>${answered}</b>${diff >= 1 ? ' · on track' : diff < -1 ? ' · speed up: guess and flag' : ''}</span></div>`;
}

function renderTest() {
  const q = cur.qs[cur.i], r = cur.resp[cur.i];
  const confirm = cur.view === 'confirm';
  const blanks = cur.resp.filter(x => x.choice == null).length;
  return `<div class="col">
    ${header()}
    <article class="sheet qsheet">
      ${qTop(q, cur.i)}
      <div class="stem">${md(q.stem)}</div>
      ${figureHTML(q.figure)}
      ${optionsHTML(q, { sel: r.choice, struck: new Set(r.struck) })}
      <div class="actions">
        <div class="left">
          <button class="btn sm ${r.flag ? '' : 'ghost'}" data-act="tflag" aria-pressed="${r.flag}">${ICON.flag}${r.flag ? 'Flagged' : 'Flag'}</button>
          <label class="toggle"><input type="checkbox" id="guess-toggle" data-act="guess" ${r.guess ? 'checked' : ''}> Guess</label>
        </div>
        <div class="right">
          <button class="btn" data-act="prev" ${cur.i === 0 ? 'disabled' : ''}>${ICON.arrowL}Prev</button>
          ${cur.i + 1 < cur.qs.length ? `<button class="btn primary" data-act="tnext">Next${ICON.arrowR}</button>` : `<button class="btn primary" data-act="finish-ask">Finish</button>`}
        </div>
      </div>
    </article>
    <section class="sheet pad stack">
      <div class="spread"><span class="eyebrow">Question navigator</span>${paceLine()}</div>
      <div class="navgrid">${cur.qs.map((_, k) => {
        const x = cur.resp[k];
        return `<button class="${[x.choice != null ? 'ans' : '', x.flag ? 'flag' : '', k === cur.i ? 'cur' : ''].join(' ')}" data-act="goto" data-k="${k}" aria-label="Question ${k + 1}${x.choice != null ? ', answered' : ''}${x.flag ? ', flagged' : ''}">${k + 1}</button>`;
      }).join('')}</div>
      ${confirm
        ? `<div class="sheet pad stack" style="box-shadow:none;background:var(--ground)">
            <p><b>Submit now?</b> ${blanks ? `${blanks} question${blanks === 1 ? ' is' : 's are'} blank. There's no penalty for wrong answers, so fill every blank with your best guess first.` : 'Every question has an answer.'}</p>
            <div class="row"><button class="btn primary" data-act="finish">Submit paper</button><button class="btn ghost" data-act="finish-cancel">Keep going</button></div>
           </div>`
        : `<div class="row"><button class="btn sm" data-act="finish-ask">Finish paper</button><span class="small muted">Flag anything you want to revisit; unanswered questions score zero.</span></div>`}
    </section>
  </div>`;
}

function renderResults() {
  const n = cur.qs.length;
  const right = cur.resp.filter(r => r.ok).length;
  const totalMs = cur.resp.reduce((s, r) => s + r.ms, 0);
  const byTopic = {};
  cur.qs.forEach((q, k) => {
    const b = (byTopic[q.topic] ||= { n: 0, ok: 0, ms: 0 });
    b.n++; if (cur.resp[k].ok) b.ok++; b.ms += cur.resp[k].ms;
  });
  const rv = cur.view && cur.view.startsWith('rv:') ? +cur.view.slice(3) : null;
  let detail = '';
  if (rv != null) {
    const q = cur.qs[rv], r = cur.resp[rv];
    detail = `<article class="sheet qsheet" id="rv">
      <div class="spread">${qTop(q, rv)}<button class="btn sm ghost" data-act="rv-close">${ICON.x}Close</button></div>
      <div class="stem">${md(q.stem)}</div>
      ${figureHTML(q.figure)}
      ${optionsHTML(q, { sel: r.choice, reveal: true })}
      <div class="feedback">
        <div class="verdict ${r.ok ? 'ok' : 'no'}"><span class="big">${r.ok ? 'Correct' : r.choice == null ? 'Blank' : 'Wrong'}</span><span class="muted">${fmtSecs(r.ms)} spent</span></div>
        ${!r.ok ? `<div class="reasons">${REASONS.map(([k, l]) => `<button class="chip" data-act="rv-reason" data-k="${rv}" data-r="${k}" aria-pressed="${r.reason === k}">${l}</button>`).join('')}</div>` : ''}
        ${solutionHTML(q, r.choice)}
        ${tutorHTML(q, r)}
      </div>
    </article>`;
  }
  const verdict = right / n >= 0.8 ? 'Strong work.' : right / n >= 0.6 ? 'Solid. The misses below are where the marks are.' : 'Plenty to learn from here. Go through every miss below.';
  return `<div class="col">
    <div class="stack" style="gap:6px"><span class="eyebrow">${esc(cur.title)} · results</span>
      <div class="row" style="align-items:baseline;gap:18px"><span class="countdown" style="font-size:clamp(3.4rem,9vw,5rem)">${right}<span class="muted" style="font-size:0.45em">/${n}</span></span>
      <div class="stack" style="gap:2px"><b>${pct(right / n)} correct</b><span class="muted">${fmtClock(totalMs)} total · ${fmtSecs(totalMs / n)} per question (TMUA pace: 3m 45s)</span></div></div>
      <p class="muted">${verdict}</p>
    </div>
    ${detail}
    <section class="sheet pad stack">
      <div class="spread"><h3>Question by question</h3><span class="small muted">Tap a row to see the worked solution</span></div>
      <div class="navgrid">${cur.qs.map((_, k) => {
        const r = cur.resp[k];
        return `<button class="${r.ok ? 'right' : r.choice == null ? 'blank' : 'wrong'}${rv === k ? ' cur' : ''}" data-act="rv" data-k="${k}" aria-label="Question ${k + 1}: ${r.ok ? 'correct' : 'wrong'}">${k + 1}</button>`;
      }).join('')}</div>
      <div class="table-wrap"><table class="data">
        <thead><tr><th>#</th><th>Topic</th><th>You</th><th>Answer</th><th class="num">Time</th><th>Why missed</th></tr></thead>
        <tbody>${cur.qs.map((q, k) => {
          const r = cur.resp[k];
          return `<tr class="click" data-act="rv" data-k="${k}"><td class="mono">${k + 1}</td><td>${esc(TOPIC[q.topic].short)}</td>
            <td><span class="chip ${r.ok ? 'tone-good' : 'tone-bad'}">${r.choice == null ? '–' : LETTERS[r.choice]}</span></td><td class="mono">${LETTERS[q.answer]}</td>
            <td class="num mono ${r.ms > targetMs(q) * 1.5 ? 'muted' : ''}">${fmtSecs(r.ms)}</td><td class="small muted">${r.ok ? '' : esc((REASONS.find(x => x[0] === r.reason) || [, 'tag it'])[1])}</td></tr>`;
        }).join('')}</tbody></table></div>
    </section>
    <section class="sheet pad stack">
      <h3>By topic</h3>
      <div class="hbars">${Object.entries(byTopic).sort((a, b) => a[1].ok / a[1].n - b[1].ok / b[1].n).map(([k, b]) => `
        <div class="hbar"><span>${esc(TOPIC[k].short)}</span><div class="track"><div class="fill" style="width:max(4px, ${(100 * b.ok) / b.n}%);background:${b.ok / b.n >= 0.7 ? 'var(--good)' : b.ok / b.n >= 0.4 ? 'var(--warn)' : 'var(--bad)'}"></div></div><span class="mono small">${b.ok}/${b.n}</span></div>`).join('')}</div>
    </section>
    <div class="row">
      <button class="btn primary" data-act="go" data-to="today">Back to today</button>
      <button class="btn" data-act="go" data-to="review">Go to mistakes</button>
    </div>
  </div>`;
}

// ---------------------------------------------------------------- actions

function finish() {
  stampTime();
  cur.finished = true;
  cur.view = null;
  if (cur.test) {
    cur.qs.forEach((q, k) => {
      const r = cur.resp[k];
      r.ok = r.choice === q.answer;
      r.checked = true;
      recordAttempt(q, r, cur.kind);
    });
  }
  const answered = cur.resp.filter(r => r.checked);
  const right = answered.filter(r => r.ok).length;
  update(s => {
    s.active = null;
    s.sessions.push({ id: cur.id, kind: cur.kind, title: cur.title, at: Date.now(), n: answered.length, ok: right, ms: cur.resp.reduce((a, r) => a + r.ms, 0), paper: cur.paper || undefined });
    if (cur.kind === 'diagnostic') s.diag = { done: Date.now() };
    if (cur.taskId && answered.length) {
      const d = dateKey();
      s.plan[d] = Array.from(new Set([...(s.plan[d] || []), cur.taskId]));
    }
  });
  hooks.done(cur);
}

function similar() {
  const q = cur.qs[cur.i];
  let nq = null;
  if (q.gen) nq = genQuestion(q.gen, q.difficulty, randomSeed());
  else {
    const st = S();
    const exclude = new Set(cur.qs.map(x => x.id));
    nq = pickForTopic(q.topic, buildModel(st.attempts), { exclude, seen: seenMap(st.attempts), reported: st.reported, level: q.difficulty, preferBank: 0.3 });
  }
  if (!nq) { toast('No similar question available right now.'); return; }
  cur.qs.splice(cur.i + 1, 0, nq);
  cur.resp.splice(cur.i + 1, 0, blankResp());
  go(cur.i + 1);
}

function go(k) {
  if (k < 0 || k >= cur.qs.length) return;
  stampTime();
  const dir = k > cur.i ? 'next' : 'prev';
  cur.i = k;
  cur.view = null;
  persistActive();
  hooks.render(true, dir);
}

function choose(i) {
  const r = cur.resp[cur.i];
  if (r.checked && !cur.test) return;
  r.choice = i;
  r.struck = r.struck.filter(x => x !== i);
  persistActive();
  hooks.render();
}

function strike(i) {
  const r = cur.resp[cur.i];
  if (r.checked && !cur.test) return;
  r.struck = r.struck.includes(i) ? r.struck.filter(x => x !== i) : [...r.struck, i];
  if (r.choice === i) r.choice = null;
  hooks.render();
}

function check(reveal = false) {
  const q = cur.qs[cur.i], r = cur.resp[cur.i];
  if (r.checked) return;
  if (!reveal && r.choice == null) return;
  stampTime();
  if (reveal) r.choice = null;
  r.checked = true;
  r.ok = r.choice === q.answer;
  cur.fresh = cur.i;
  recordAttempt(q, r, cur.kind);
  if (reveal) setReason(cur.i, 'concept');
  hooks.render();
}

export function sessionAction(act, el, ev) {
  if (!cur) return false;
  switch (act) {
    case 'choose': {
      if (ev?.type === 'contextmenu') return false;
      choose(+el.dataset.i); return true;
    }
    case 'check': check(); return true;
    case 'reveal': check(true); return true;
    case 'next': cur.i + 1 < cur.qs.length ? go(cur.i + 1) : finish(); return true;
    case 'similar': similar(); return true;
    case 'reason': setReason(cur.i, el.dataset.r); hooks.render(); return true;
    case 'guess': cur.resp[cur.i].guess = el.checked; persistActive(); return true;
    case 'flag': {
      const q = cur.qs[cur.i];
      update(s => { if (s.flags[q.id]) delete s.flags[q.id]; else s.flags[q.id] = Date.now(); });
      hooks.render(); return true;
    }
    case 'report': {
      const q = cur.qs[cur.i];
      update(s => { s.reported[q.id] = { at: Date.now(), title: q.stem.slice(0, 80) }; });
      toast('Reported. This question will not be shown again. You can undo this in Settings.');
      return true;
    }
    case 'tflag': cur.resp[cur.i].flag = !cur.resp[cur.i].flag; persistActive(); hooks.render(); return true;
    case 'prev': go(cur.i - 1); return true;
    case 'tnext': go(cur.i + 1); return true;
    case 'goto': go(+el.dataset.k); return true;
    case 'finish-ask': stampTime(); cur.view = 'confirm'; hooks.render(); return true;
    case 'finish-cancel': cur.view = null; hooks.render(); return true;
    case 'finish': finish(); return true;
    case 'rv': cur.view = `rv:${el.dataset.k}`; hooks.render(true); return true;
    case 'rv-close': cur.view = null; hooks.render(); return true;
    case 'rv-reason': setReason(+el.dataset.k, el.dataset.r); hooks.render(); return true;
    case 'tutor-hint': {
      const t = tutorTarget(); if (!t) return false;
      t.r.hint = true; tutorHint(t.q, t.r); return true;
    }
    case 'tutor-explain': { const t = tutorTarget(); if (!t) return false; tutorExplain(t.q, t.r, el.dataset.mode); return true; }
    case 'tutor-stop': { const t = tutorTarget(); if (!t) return false; tutorStop(keyOf(t.q)); return true; }
    case 'sess-quit': {
      if (cur.finished || cur.test) { if (!cur.finished) { stampTime(); persistActive(); } cur = null; hooks.done(null); return true; }
      const any = cur.resp.some(r => r.checked);
      if (any) finish(); else { cur = null; hooks.done(null); }
      return true;
    }
    default: return false;
  }
}

export function sessionContext(i) { strike(i); }

export function sessionKey(e) {
  if (!cur || cur.finished) return false;
  const t = e.target;
  if (t && (t.tagName === 'INPUT' && t.type !== 'checkbox' || t.tagName === 'TEXTAREA' || t.tagName === 'SELECT')) return false;
  if (e.metaKey || e.ctrlKey || e.altKey) return false;
  const q = cur.qs[cur.i], r = cur.resp[cur.i];
  const k = e.key.toLowerCase();
  let idx = LETTERS.toLowerCase().indexOf(k);
  if (idx < 0 && /^[1-8]$/.test(k)) idx = +k - 1;
  if (idx >= 0 && idx < q.options.length && k.length === 1) {
    if (e.shiftKey) strike(idx); else choose(idx);
    return true;
  }
  if (k === 'enter') {
    if (cur.test) { cur.i + 1 < cur.qs.length ? go(cur.i + 1) : sessionAction('finish-ask'); return true; }
    if (r.checked) sessionAction('next'); else check();
    return true;
  }
  if (k === 'g') { r.guess = !r.guess; hooks.render(); return true; }
  if (cur.test && k === 'f') { sessionAction('tflag'); return true; }
  if (cur.test && k === 'arrowright') { go(cur.i + 1); return true; }
  if (cur.test && k === 'arrowleft') { go(cur.i - 1); return true; }
  return false;
}

// Clock updates without a full re-render.
export function startTicker() {
  clearInterval(tick);
  tick = setInterval(() => {
    if (!cur || cur.finished) return;
    const c = $('#sess-clock span');
    if (c) {
      const rem = remaining();
      c.textContent = cur.limitMs ? fmtClock(rem) : fmtClock(elapsed());
      const box = $('#sess-clock');
      if (cur.limitMs) { box.classList.toggle('urgent', rem < 5 * 60000); }
      if (cur.limitMs && rem <= 0) { toast('Time is up. Paper submitted.'); finish(); }
    }
    const qc = $('#q-clock');
    if (qc && !cur.test) {
      const r = cur.resp[cur.i];
      const ms = r.checked ? r.ms : r.ms + (Date.now() - cur.qStart);
      const tgt = +qc.dataset.target;
      qc.innerHTML = `${ringSVG(ms / tgt)}<span>${fmtClock(ms)}</span><span class="muted small">/ ${fmtClock(tgt)}</span>`;
      qc.classList.toggle('over', ms > tgt);
    }
    const p = $('#pace');
    if (p && cur.test) p.outerHTML = paceLine();
  }, 500);
}

// Countdown ring for the per-question target time.
function ringSVG(frac) {
  const c = 2 * Math.PI * 8;
  const f = Math.max(0, Math.min(1, frac));
  return `<svg class="qring" viewBox="0 0 22 22" aria-hidden="true"><circle class="bg" cx="11" cy="11" r="8"/><circle class="fg" cx="11" cy="11" r="8" stroke-dasharray="${c.toFixed(2)}" stroke-dashoffset="${(c * (1 - f)).toFixed(2)}"/></svg>`;
}

// The question the tutor should talk about right now (practice question or a reviewed result).
export function tutorTarget() {
  if (!cur) return null;
  if (cur.finished) {
    const rv = cur.view && cur.view.startsWith('rv:') ? +cur.view.slice(3) : null;
    return rv == null ? null : { q: cur.qs[rv], r: cur.resp[rv] };
  }
  return { q: cur.qs[cur.i], r: cur.resp[cur.i] };
}
