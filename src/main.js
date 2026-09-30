import { S, update, subscribe, exportState, replaceState, resetState, dueReviews } from './lib/store.js';
import { buildModel } from './engine/model.js';
import { smartSession, topicDrill, reviewSession, mockPaper, timedSet, diagnostic, speedRound } from './engine/select.js';
import { buildPlan } from './engine/plan.js';
import { getQuestion } from './engine/bank.js';
import { TOPIC, EXAM } from './data/topics.js';
import { $, esc, dateKey, daysBetween, uid } from './lib/util.js';
import { ICON } from './ui/icons.js';
import { toast, initTips } from './ui/common.js';
import { todayView } from './ui/today.js';
import { practiceView, learnView, noteView, reviewView, questionView, progressView, papersView, settingsView, onboardingView } from './ui/pages.js';
import {
  startSession, renderSession, sessionAction, sessionKey, sessionContext, startTicker,
  setSessionHooks, activeSession, resumeActive, discardActive,
} from './ui/session.js';

const ui = {
  route: 'today', param: null, back: 'review',
  rvFilter: {}, exportText: '', importing: false, confirmReset: false, onbDate: null,
  paperDraft: null,
};

let modelCache = { n: -1, m: null };
function model() {
  const st = S();
  if (modelCache.n !== st.attempts.length) modelCache = { n: st.attempts.length, m: buildModel(st.attempts) };
  return modelCache.m;
}

const NAV = [
  ['today', 'Today', ICON.today],
  ['practice', 'Practice', ICON.practice],
  ['learn', 'Learn', ICON.learn],
  ['review', 'Mistakes', ICON.review],
  ['progress', 'Progress', ICON.progress],
  ['papers', 'Past papers', ICON.papers],
  ['settings', 'Settings', ICON.settings],
];

function applyTheme() {
  const t = S().settings.theme;
  if (t === 'light' || t === 'dark') document.documentElement.setAttribute('data-theme', t);
  else document.documentElement.removeAttribute('data-theme');
}

function newPaperDraft(year = '2017', paper = 1, taskId = null) {
  return { year, paper, mins: 75, wrong: [], topics: {}, notes: '', taskId };
}

function shell(content) {
  const st = S();
  const left = daysBetween(dateKey(), st.settings.examDate);
  const due = dueReviews().length;
  const navRoute = ui.route === 'note' ? 'learn' : ui.route === 'q' ? ui.back : ui.route === 'session' ? 'practice' : ui.route;
  const link = ([r, label, icon], cls = '') => `<a href="#${r}" data-act="go" data-to="${r}" ${navRoute === r ? 'aria-current="page"' : ''} class="${cls}">${icon}<span>${label}</span>${r === 'review' && due ? `<span class="badge">${due}</span>` : ''}</a>`;
  return `
    <nav class="rail" aria-label="Main">
      <a class="brand" href="#today" data-act="go" data-to="today"><span class="brand-mark">TMUA Fortnight</span></a>
      <div class="nav">${NAV.map(n => link(n)).join('')}</div>
      <div class="rail-foot">
        <span class="rail-count num">${Math.max(0, left)}</span>
        <span class="small muted">day${left === 1 ? '' : 's'} to ${new Date(st.settings.examDate).toLocaleDateString('en-GB', { day: 'numeric', month: 'short' })} · ${EXAM.questions} Qs in ${EXAM.minutes} min per paper</span>
      </div>
    </nav>
    <header class="topbar"><a class="brand" href="#today" data-act="go" data-to="today"><span class="brand-mark">TMUA Fortnight</span><span class="brand-sub">${Math.max(0, left)}d</span></a>
      <div class="row" style="gap:14px"><a href="#papers" data-act="go" data-to="papers" aria-label="Past papers">${ICON.papers}</a><a href="#settings" data-act="go" data-to="settings" aria-label="Settings">${ICON.settings}</a></div></header>
    <main class="main" id="main">${content}</main>
    <nav class="tabbar" aria-label="Main">${NAV.slice(0, 5).map(n => link(n)).join('')}</nav>`;
}

function view() {
  const st = S();
  if (!st.settings.onboarded) return onboardingView(ui);
  const m = model();
  switch (ui.route) {
    case 'session': return activeSession() ? renderSession() : todayView(m);
    case 'practice': return practiceView(m);
    case 'learn': return learnView(m);
    case 'note': return noteView(ui.param, m);
    case 'review': return reviewView(m, ui.rvFilter);
    case 'q': return questionView(ui.param, ui.back);
    case 'progress': return progressView(m);
    case 'papers': return papersView(ui.paperDraft || (ui.paperDraft = newPaperDraft()));
    case 'settings': return settingsView(ui);
    default: return todayView(m);
  }
}

let lastRoute = null;
function render(scrollTop = false) {
  const app = $('#app');
  const y = window.scrollY;
  app.innerHTML = S().settings.onboarded ? shell(view()) : `<main class="main solo">${view()}</main>`;
  if (scrollTop || lastRoute !== ui.route + ui.param) window.scrollTo(0, 0);
  else window.scrollTo(0, y);
  lastRoute = ui.route + ui.param;
  if (ui.route === 'q' || (ui.route === 'session' && activeSession()?.view?.startsWith('rv:'))) {
    const rv = $('#rv'); if (rv && scrollTop) rv.scrollIntoView({ block: 'start' });
  }
}

function go(route, param = null) {
  ui.route = route; ui.param = param;
  ui.exportText = ''; ui.importing = false; ui.confirmReset = false;
  const token = route === 'note' ? `learn.${param}` : route === 'q' || route === 'session' ? '' : route;
  try { if (token && location.hash !== `#${token}`) history.replaceState(null, '', `#${token}`); } catch (e) { /* sandboxed */ }
  render(true);
}

function markTask(id) {
  const d = dateKey();
  update(s => { s.plan[d] = Array.from(new Set([...(s.plan[d] || []), id])); });
}

function start(kind, { topic, paper, taskId, n } = {}) {
  const st = S(), m = model();
  let ok = false;
  if (activeSession() && !activeSession().finished && activeSession().test) {
    toast('Finish or discard the paper in progress first.');
    return;
  }
  switch (kind) {
    case 'smart': ok = startSession({ kind, title: n && n < 6 ? 'Warm-up' : 'Smart practice', qs: smartSession(st, m, n || 12), taskId }); break;
    case 'drill': ok = startSession({ kind, title: `${TOPIC[topic].name}`, qs: topicDrill(st, m, topic, 10), taskId }); break;
    case 'review': {
      const qs = reviewSession(st);
      if (!qs.length) { toast('Nothing due for review. Nice.'); if (taskId) markTask(taskId); render(); return; }
      ok = startSession({ kind, title: 'Mistake review', qs, taskId }); break;
    }
    case 'saved': ok = startSession({ kind, title: 'Saved questions', qs: Object.keys(st.flags).map(getQuestion).filter(Boolean).map(q => ({ ...q })), taskId }); break;
    case 'speed': ok = startSession({ kind, title: 'Speed round', qs: speedRound(m, 10), taskId }); break;
    case 'timed': ok = startSession({ kind, title: 'Timed set', qs: timedSet(st, m, 10), test: true, limitMs: 10 * EXAM.perQ * 1000, taskId }); break;
    case 'mock': ok = startSession({ kind, title: `Mock Paper ${paper}`, qs: mockPaper(st, m, +paper), test: true, limitMs: EXAM.minutes * 60000, taskId, paper: +paper }); break;
    case 'diagnostic': ok = startSession({ kind, title: 'Diagnostic', qs: diagnostic(st, m), test: true, limitMs: null, taskId: taskId || 'diag' }); break;
    default: break;
  }
  if (ok) go('session');
}

function runTask(id) {
  const st = S();
  const plan = buildPlan(st, model());
  const t = plan.days[0]?.tasks.find(x => x.id === id);
  if (!t) return;
  switch (t.kind) {
    case 'diagnostic': start('diagnostic', { taskId: id }); break;
    case 'learn': markTask(id); update(s => { s.learned[t.topic] ||= Date.now(); }); go('note', t.topic); break;
    case 'read': markTask(id); go('note', t.note); break;
    case 'drill': start('drill', { topic: t.topic, taskId: id }); break;
    case 'smart': start('smart', { taskId: id, n: t.n || 15 }); break;
    case 'review': start('review', { taskId: id }); break;
    case 'timed': start('timed', { taskId: id }); break;
    case 'mock': start('mock', { paper: t.paper, taskId: id }); break;
    case 'past': ui.paperDraft = newPaperDraft(t.year, t.paper, id); go('papers'); break;
    default: break;
  }
}

function savePaper() {
  const d = ui.paperDraft;
  const year = $('#pp-year').value, paper = +$('#pp-paper').value, mins = Math.max(1, +$('#pp-mins').value || 75);
  const notes = $('#pp-notes').value.trim();
  const id = uid();
  const now = Date.now();
  update(s => {
    s.papers.push({ id, year, paper, score: 20 - d.wrong.length, mins, wrong: d.wrong.slice().sort((a, b) => a - b), topics: d.topics, notes, date: dateKey() });
    for (let q = 1; q <= 20; q++) {
      const wrong = d.wrong.includes(q);
      // Official papers get harder through the paper: rough level by position.
      const lv = q <= 5 ? 2 : q <= 12 ? 3 : q <= 17 ? 4 : 5;
      s.attempts.push({ qid: `past:${year}:${paper}:${q}`, pid: id, topic: wrong ? d.topics[q] || null : null, d: lv, ok: !wrong, ms: Math.round((mins * 60000) / 20), at: now, mode: 'past', weight: 0.8 });
    }
    const tid = d.taskId || `past:${year}:${paper}`;
    const k = dateKey();
    s.plan[k] = Array.from(new Set([...(s.plan[k] || []), tid]));
  });
  ui.paperDraft = newPaperDraft();
  toast(`Saved ${year} Paper ${paper}: ${20 - d.wrong.length}/20.`);
  render(true);
}

// ------------------------------------------------------------ events
const actions = {
  go: el => go(el.dataset.to),
  start: el => start(el.dataset.kind, { topic: el.dataset.topic, paper: el.dataset.paper }),
  task: el => runTask(el.dataset.id),
  'toggle-task': el => {
    const id = el.dataset.id, d = dateKey();
    update(s => { const cur = new Set(s.plan[d] || []); cur.has(id) ? cur.delete(id) : cur.add(id); s.plan[d] = Array.from(cur); });
    render();
  },
  'open-note': el => go('note', el.dataset.topic),
  'mark-read': el => { update(s => { if (s.learned[el.dataset.topic]) delete s.learned[el.dataset.topic]; else s.learned[el.dataset.topic] = Date.now(); }); render(); },
  'open-q': el => { ui.back = ui.route === 'q' ? ui.back : ui.route; go('q', el.dataset.id); },
  resume: () => { if (resumeActive()) go('session'); else toast('That session could not be restored.'); },
  discard: () => { discardActive(); render(); },
  'pp-toggle': el => {
    const q = +el.dataset.q, d = ui.paperDraft;
    syncPaperFields();
    d.wrong = d.wrong.includes(q) ? d.wrong.filter(x => x !== q) : [...d.wrong, q];
    render();
  },
  'pp-del': el => {
    const id = el.dataset.id;
    update(s => { s.papers = s.papers.filter(p => p.id !== id); s.attempts = s.attempts.filter(a => a.pid !== id); });
    render();
  },
  export: () => {
    ui.exportText = exportState();
    const txt = ui.exportText;
    try { navigator.clipboard.writeText(txt).then(() => toast('Backup code copied.'), () => toast('Select the code below and copy it.')); } catch (e) { toast('Select the code below and copy it.'); }
    render();
    const box = $('#export-box'); if (box) box.select();
  },
  'show-import': () => { ui.importing = true; render(); },
  import: () => {
    const raw = $('#import-box').value.trim();
    try {
      const obj = JSON.parse(raw);
      if (!obj || !Array.isArray(obj.attempts)) throw new Error('shape');
      replaceState(obj); ui.importing = false; applyTheme(); toast('Progress restored.'); render(true);
    } catch (e) { toast('That backup code is not valid. Copy the whole code and try again.'); }
  },
  unreport: el => { update(s => { delete s.reported[el.dataset.id]; }); render(); },
  'reset-ask': () => { ui.confirmReset = true; render(); },
  'reset-cancel': () => { ui.confirmReset = false; render(); },
  reset: () => { resetState(); ui.confirmReset = false; applyTheme(); ui.route = 'today'; render(true); },
  'onb-date': el => { ui.onbDate = el.dataset.d; render(); },
  'onb-go': () => {
    update(s => { s.settings.examDate = ui.onbDate || s.settings.examDate; s.settings.onboarded = true; });
    start('diagnostic', { taskId: 'diag' });
    if (!activeSession()) go('today');
  },
  'onb-skip': () => { update(s => { s.settings.examDate = ui.onbDate || s.settings.examDate; s.settings.onboarded = true; }); go('today'); },
};

function syncPaperFields() {
  const d = ui.paperDraft;
  if (!d || !$('#pp-year')) return;
  d.year = $('#pp-year').value; d.paper = +$('#pp-paper').value; d.mins = +$('#pp-mins').value || 75; d.notes = $('#pp-notes').value;
}

function onClick(e) {
  const el = e.target.closest('[data-act]');
  if (!el || el.tagName === 'SELECT' || (el.tagName === 'INPUT' && el.type !== 'checkbox')) return;
  const act = el.dataset.act;
  if (el.tagName === 'A') e.preventDefault();
  if (el.tagName === 'INPUT') { if (!sessionAction(act, el, e)) return; return; }
  if (sessionAction(act, el, e)) return;
  const fn = actions[act];
  if (fn) { e.preventDefault(); fn(el, e); }
}

function onChange(e) {
  const el = e.target;
  if (el.id === 'set-date' && el.value) { update(s => { s.settings.examDate = el.value; }); toast('Test date updated. Your plan has been rebuilt.'); render(); }
  else if (el.id === 'set-theme') { update(s => { s.settings.theme = el.value; }); applyTheme(); }
  else if (el.id === 'onb-other' && el.value) { ui.onbDate = el.value; render(); }
  else if (el.dataset.act === 'rv-filter') { ui.rvFilter = { topic: $('#rv-topic').value || undefined, reason: $('#rv-reason').value || undefined }; render(); }
  else if (el.dataset.act === 'pp-topic') { ui.paperDraft.topics[+el.dataset.q] = el.value || undefined; }
  else if (el.id === 'pp-paper') { syncPaperFields(); render(); }
}

function onSubmit(e) {
  if (e.target.id === 'paper-form') { e.preventDefault(); syncPaperFields(); savePaper(); }
}

function onContext(e) {
  const el = e.target.closest('.opt[data-act="choose"]');
  if (!el || !activeSession()) return;
  e.preventDefault();
  sessionContext(+el.dataset.i);
}

function onKey(e) {
  if (ui.route === 'session' && sessionKey(e)) e.preventDefault();
}

setSessionHooks({
  render: (top = false) => render(top),
  done: sess => {
    if (!sess) { go('today'); return; }
    ui.route = 'session';
    render(true);
  },
});

function boot() {
  applyTheme();
  const token = (location.hash || '').slice(1);
  if (token.startsWith('learn.')) { ui.route = 'note'; ui.param = token.slice(6); }
  else if (['today', 'practice', 'learn', 'review', 'progress', 'papers', 'settings'].includes(token)) ui.route = token;
  document.addEventListener('click', onClick);
  document.addEventListener('change', onChange);
  document.addEventListener('submit', onSubmit);
  document.addEventListener('contextmenu', onContext);
  document.addEventListener('keydown', onKey);
  window.addEventListener('hashchange', () => {
    const t = location.hash.slice(1);
    if (t.startsWith('learn.')) { if (ui.route !== 'note' || ui.param !== t.slice(6)) go('note', t.slice(6)); }
    else if (t && t !== ui.route && actions.go) { if (['today', 'practice', 'learn', 'review', 'progress', 'papers', 'settings'].includes(t)) go(t); }
  });
  window.matchMedia?.('(prefers-color-scheme: dark)').addEventListener?.('change', () => render());
  subscribe(() => {});
  initTips();
  startTicker();
  render(true);
}

boot();
