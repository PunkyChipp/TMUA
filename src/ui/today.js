import { S } from '../lib/store.js';
import { dueReviews } from '../lib/store.js';
import { buildPlan, phaseOf } from '../engine/plan.js';
import { predict, priorities, masteryLabel } from '../engine/model.js';
import { TOPIC } from '../data/topics.js';
import { esc, dateKey, daysBetween, fmtDate, pct } from '../lib/util.js';
import { ICON } from './icons.js';

export function todayView(model) {
  const st = S();
  const today = dateKey();
  const exam = st.settings.examDate;
  const left = daysBetween(today, exam);
  const phase = phaseOf(left);
  const plan = buildPlan(st, model, today);
  const day = plan.days[0];
  const due = dueReviews().length;
  const pred = predict(model);
  const enough = st.attempts.length >= 10;
  const todayCount = st.attempts.filter(a => dateKey(a.at) === today).length;
  const todayOk = st.attempts.filter(a => dateKey(a.at) === today && a.ok).length;
  const streak = (() => {
    const days = new Set(st.attempts.map(a => dateKey(a.at)));
    let n = 0, d = new Date();
    if (!days.has(dateKey(d.getTime()))) d.setDate(d.getDate() - 1);
    while (days.has(dateKey(d.getTime()))) { n++; d.setDate(d.getDate() - 1); }
    return n;
  })();

  // Phase track: one segment per remaining day, fixed 14-day window.
  const span = Math.max(left + 1, 1);
  const track = Array.from({ length: Math.min(span, 21) }, (_, i) => `<span class="${i === 0 ? 'now' : ''}${i === span - 1 ? ' exam' : ''}" title="${fmtDate(plan.days[i]?.key || exam)}"></span>`).join('');

  const resume = st.active ? `<section class="sheet pad spread">
      <div class="stack" style="gap:2px"><b>${esc(st.active.title)} is in progress</b><span class="small muted">Question ${st.active.i + 1} of ${st.active.ids.length}${st.active.limitMs ? ' · the clock kept running' : ''}</span></div>
      <div class="row"><button class="btn primary" data-act="resume">Resume</button><button class="btn ghost" data-act="discard">Discard</button></div>
    </section>` : '';

  const focus = priorities(model).slice(0, 4).map(p => {
    const t = model.topics[p.key];
    const ml = masteryLabel(t.mastery, t.n);
    return `<div class="focus-item">
      <div class="stack" style="gap:2px"><b>${esc(TOPIC[p.key].name)}</b><span class="small muted">${t.n ? `${t.ok}/${t.n} correct` : 'Not practised yet'}${t.n >= 3 ? ` · <span class="chip ${'tone-' + ml.tone}" style="padding:0 8px">${ml.label}</span>` : ''}</span></div>
      <div class="meter ${ml.tone === 'good' ? 'good' : ml.tone === 'bad' ? 'bad' : ml.tone === 'warn' ? 'warn' : ''}" title="Estimated mastery ${pct(t.mastery)}"><i style="width:${t.n ? Math.round(t.mastery * 100) : 0}%"></i></div>
      <div class="row" style="gap:6px"><button class="btn sm ghost" data-act="open-note" data-topic="${p.key}">Notes</button><button class="btn sm" data-act="start" data-kind="drill" data-topic="${p.key}">Drill</button></div>
    </div>`;
  }).join('');

  const tasks = day ? day.tasks.map(t => `<div class="task ${t.done ? 'done' : ''}">
      <button class="tick" data-act="toggle-task" data-id="${esc(t.id)}" aria-pressed="${t.done}" aria-label="Mark ${esc(t.title)} ${t.done ? 'not done' : 'done'}">${ICON.check}</button>
      <div class="stack" style="gap:1px;min-width:0"><span class="task-title">${esc(t.title)}</span><span class="task-meta">${esc(t.detail)} · ~${t.mins} min</span></div>
      <button class="btn sm ${t.done ? 'ghost' : ''}" data-act="task" data-id="${esc(t.id)}">${t.kind === 'learn' || t.kind === 'read' ? 'Open' : t.kind === 'past' ? 'Log score' : 'Start'}</button>
    </div>`).join('') : '';

  const upcoming = plan.days.slice(1, 4).map(d => `<div class="stack" style="gap:4px"><span class="eyebrow">${fmtDate(d.key)} · ${esc(d.phase.name)}</span><span class="small">${d.tasks.filter(t => t.kind !== 'review').map(t => esc(t.title)).join(' · ') || 'Rest'}</span></div>`).join('');

  const heroCopy = left > 1 ? `${left} days until your TMUA` : left === 1 ? 'Your TMUA is tomorrow' : left === 0 ? 'Test day' : 'Test done';
  const lede = {
    build: 'Build phase: close the biggest gaps first. Learn, drill, then mix.',
    sharpen: 'Sharpen phase: mixed practice at exam pace, with official papers in between.',
    simulate: 'Simulation: full papers under exam conditions. Review every mistake.',
    taper: 'Taper: light practice, read the strategy notes, sleep properly.',
    exam: 'Arrive early, answer every question, keep moving. Good luck.',
    done: 'Set a new test date in Settings if you are sitting it again in January.',
  }[phase.key];

  return `<div class="col">
    ${resume}
    <header class="hero">
      <div class="countdown">${Math.max(0, left)}<small>${left === 1 ? 'day' : 'days'} to go</small></div>
      <div class="hero-copy">
        <span class="eyebrow">${fmtDate(exam, { weekday: 'long', day: 'numeric', month: 'long' })} · ${esc(phase.name)}</span>
        <h1>${esc(heroCopy)}</h1>
        <p class="muted">${esc(lede)}</p>
        <div class="phase-track" aria-hidden="true">${track}</div>
      </div>
    </header>

    <section class="sheet predict" aria-label="Predicted marks">
      ${[1, 2].map(p => `<div>
        <span class="eyebrow">Paper ${p} · ${p === 1 ? 'Mathematical thinking' : 'Mathematical reasoning'}</span>
        ${enough ? `<span class="big num">${pred[p].exp.toFixed(1)}<span> / 20</span></span>
          <div class="range" title="Likely range ${pred[p].lo.toFixed(0)}–${pred[p].hi.toFixed(0)}"><i style="left:${pred[p].lo * 5}%;width:${(pred[p].hi - pred[p].lo) * 5}%"></i><b style="left:calc(${pred[p].exp * 5}% - 1px)"></b></div>
          <span class="small muted">Likely ${pred[p].lo.toFixed(0)}–${pred[p].hi.toFixed(0)} · ${pred[p].confidence < 0.5 ? 'more data will narrow this' : 'based on ' + st.attempts.length + ' answers'}</span>`
          : `<span class="big num">–<span> / 20</span></span><span class="small muted">Answer ${10 - st.attempts.length} more question${10 - st.attempts.length === 1 ? '' : 's'} for an estimate.</span>`}
      </div>`).join('')}
    </section>

    <section class="stack">
      <div class="section-head"><div><span class="eyebrow">${fmtDate(today, { weekday: 'long', day: 'numeric', month: 'long' })}</span><h2>Today's plan</h2></div>
        <span class="small muted">${todayCount ? `${todayOk}/${todayCount} right today` : 'Nothing answered yet today'}${streak > 1 ? ` · ${streak}-day streak` : ''}</span></div>
      <div class="sheet pad"><div class="tasks">${tasks || '<p class="muted">No tasks: your test date has passed.</p>'}</div></div>
    </section>

    <section class="stack">
      <h3>Quick start</h3>
      <div class="quick four">
        <button class="qa" data-act="start" data-kind="smart"><strong>Smart practice</strong><span>12 questions, chosen for you</span></button>
        <button class="qa" data-act="start" data-kind="review"><strong>Mistakes${due ? ` <span class="badge">${due}</span>` : ''}</strong><span>${due ? 'Due for another go' : 'Nothing due yet'}</span></button>
        <button class="qa" data-act="start" data-kind="timed"><strong>Timed set</strong><span>10 questions, 37½ min</span></button>
        <button class="qa" data-act="start" data-kind="mock" data-paper="${left % 2 ? 1 : 2}"><strong>Mock Paper ${left % 2 ? 1 : 2}</strong><span>20 questions, 75 min</span></button>
      </div>
    </section>

    <section class="stack">
      <div class="section-head"><div><h3>Where the marks are</h3><span class="small muted">Your highest-value topics right now: weak, heavily examined, or not yet tested.</span></div><button class="btn sm ghost" data-act="go" data-to="progress">All topics</button></div>
      <div class="sheet pad focus-list">${focus}</div>
    </section>

    ${upcoming ? `<section class="stack"><h3>Coming up</h3><div class="grid-3">${upcoming}</div></section>` : ''}
  </div>`;
}
