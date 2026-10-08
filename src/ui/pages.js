import { S, dueReviews, storageWorks } from '../lib/store.js';
import { TOPICS, TOPIC, PAST_PAPERS, PREP_URL } from '../data/topics.js';
import { masteryLabel, predict, priorities } from '../engine/model.js';
import { BANK, BY_TOPIC, NOTES, getQuestion, bankStats } from '../engine/bank.js';
import { GENERATORS } from '../gen/index.js';
import { esc, dateKey, addDays, fmtDate, fmtSecs, pct, LETTERS, mean } from '../lib/util.js';
import { ICON } from './icons.js';
import { md, mdi, diffDots, topicChip, figureHTML, optionsHTML, solutionHTML } from './common.js';
import { REASONS } from './session.js';
import { masteryWheel } from './viz.js';
import { tutorHTML, coachHTML } from './tutor.js';
import { getCaps } from '../lib/caps.js';
import { syncStatus } from '../lib/sync.js';
import { dueReviews as dueList } from '../lib/store.js';

const toneOf = ml => (ml.tone === 'good' ? 'good' : ml.tone === 'bad' ? 'bad' : ml.tone === 'warn' ? 'warn' : '');

// ------------------------------------------------------------ practice
export function practiceView(model) {
  const st = S();
  const due = dueReviews().length;
  const flags = Object.keys(st.flags).length;
  const topicBtns = paper => TOPICS.filter(t => t.paper === paper).map((t, i) => {
    const m = model.topics[t.key];
    const ml = masteryLabel(m.mastery, m.n);
    return `<button class="topic-card rise" style="--i:${i}" data-act="start" data-kind="drill" data-topic="${t.key}">
      <div class="spread"><h3>${esc(t.name)}</h3></div>
      <div class="meter ${toneOf(ml)}"><i style="width:${m.n ? Math.round(m.mastery * 100) : 0}%"></i></div>
      <div class="spread small muted"><span>${m.n ? `${m.ok}/${m.n} right` : 'Not started'}</span><span>${(BY_TOPIC[t.key] || []).length} questions${GENERATORS.some(g => g.topic === t.key) ? ' + generated' : ''}</span></div>
    </button>`;
  }).join('');
  return `<div class="col wide">
    <div class="stack" style="gap:6px"><span class="eyebrow">Practice</span><h1>Choose how to practise</h1>
      <p class="muted">Every answer updates your topic estimates. Mistakes come back on a spaced schedule until you get them right.</p></div>
    <section class="quick">
      <button class="qa" data-act="start" data-kind="smart"><strong>Smart practice</strong><span>12 mixed questions, weighted towards your weak spots, pitched so you get about two in three right.</span></button>
      <button class="qa" data-act="start" data-kind="review"><strong>Mistake review ${due ? `<span class="badge">${due}</span>` : ''}</strong><span>${due ? `${due} due. Each comes back as a different question on the same idea.` : 'Nothing due right now.'}</span></button>
      <button class="qa" data-act="start" data-kind="speed"><strong>Speed round</strong><span>10 quick-fire fluency questions, about a minute each. Builds the speed that frees time for hard questions.</span></button>
      <button class="qa" data-act="start" data-kind="timed"><strong>Timed set</strong><span>10 questions in 37½ minutes. No feedback until the end.</span></button>
      <button class="qa" data-act="start" data-kind="mock" data-paper="1"><strong>Mock Paper 1</strong><span>20 questions, 75 minutes, Mathematical Thinking.</span></button>
      <button class="qa" data-act="start" data-kind="mock" data-paper="2"><strong>Mock Paper 2</strong><span>20 questions, 75 minutes, Mathematical Reasoning.</span></button>
      <button class="qa" data-act="start" data-kind="diagnostic"><strong>Diagnostic</strong><span>16 questions, one per topic. ${st.diag ? 'Retake to recalibrate.' : 'Start here.'}</span></button>
      ${flags ? `<button class="qa" data-act="start" data-kind="saved"><strong>Saved questions</strong><span>${flags} bookmarked.</span></button>` : ''}
    </section>
    <section class="stack"><div class="section-head"><div><span class="eyebrow">Paper 1 content · also on Paper 2</span><h2>Drill a topic</h2></div></div>
      <div class="topic-grid">${topicBtns(1)}</div></section>
    <section class="stack"><div class="section-head"><div><span class="eyebrow">Paper 2 only</span><h2>Logic and proof</h2></div></div>
      <div class="topic-grid">${topicBtns(2)}</div></section>
  </div>`;
}

// ------------------------------------------------------------ learn
const EXTRA_NOTES = [
  ['strategy', 'Exam strategy', 'Timing, guessing, and what to do when stuck.'],
  ['facts', 'Facts to know cold', 'The formulas and results TMUA assumes.'],
];

export function learnView(model) {
  const st = S();
  const card = t => {
    const m = model.topics[t.key];
    const ml = masteryLabel(m.mastery, m.n);
    const read = st.learned[t.key];
    return `<button class="topic-card" data-act="open-note" data-topic="${t.key}">
      <div class="spread"><h3>${esc(t.name)}</h3>${read ? '<span class="chip tone-good" style="padding:0 8px">Read</span>' : ''}</div>
      <div class="meter ${toneOf(ml)}"><i style="width:${m.n ? Math.round(m.mastery * 100) : 0}%"></i></div>
      <span class="small muted">${ml.label}</span>
    </button>`;
  };
  return `<div class="col wide">
    <div class="stack" style="gap:6px"><span class="eyebrow">Learn</span><h1>Notes, techniques and traps</h1>
      <p class="muted">Short, exam-focused notes. Read one, then drill it straight away while it is fresh.</p></div>
    <section class="grid-2">${EXTRA_NOTES.filter(([k]) => NOTES[k]).map(([k, t, d]) => `<button class="qa" data-act="open-note" data-topic="${k}"><strong>${t}</strong><span>${d}</span></button>`).join('')}</section>
    <section class="stack"><h2>Paper 1 topics</h2><div class="topic-grid">${TOPICS.filter(t => t.paper === 1).map(card).join('')}</div></section>
    <section class="stack"><h2>Paper 2: logic and proof</h2><div class="topic-grid">${TOPICS.filter(t => t.paper === 2).map(card).join('')}</div></section>
  </div>`;
}

export function noteView(key, model) {
  const src = NOTES[key];
  const t = TOPIC[key];
  const extra = EXTRA_NOTES.find(e => e[0] === key);
  if (!src) return `<div class="col"><p>Notes for this topic are not available.</p><button class="btn" data-act="go" data-to="learn">Back</button></div>`;
  const m = t ? model.topics[key] : null;
  const ml = m ? masteryLabel(m.mastery, m.n) : null;
  const skills = t ? Array.from(new Set((BY_TOPIC[key] || []).flatMap(q => q.skills || []))).slice(0, 14) : [];
  const heads = [];
  const html = md(src).replace(/<h2>([\s\S]*?)<\/h2>/g, (m, t) => {
    const id = `sec-${heads.length + 1}`;
    heads.push({ id, t: t.replace(/<[^>]+>/g, '') });
    return `<h2 id="${id}">${t}</h2>`;
  });
  return `<div class="col wide">
    <div class="readbar" aria-hidden="true"></div>
    <div class="row"><button class="btn sm ghost" data-act="go" data-to="learn">${ICON.arrowL}All notes</button></div>
    <div class="learn-layout">
      <article class="sheet pad note">${html}</article>
      <aside class="learn-side">
        ${heads.length ? `<nav class="toc" aria-label="On this page"><span class="eyebrow" style="margin-bottom:6px">On this page</span>${heads.map(h => `<a href="#${h.id}">${h.t}</a>`).join('')}</nav>` : ''}
        ${t ? `<div class="sheet pad stack">
          <span class="eyebrow">${esc(t.name)}</span>
          <div class="meter ${toneOf(ml)}"><i style="width:${m.n ? Math.round(m.mastery * 100) : 0}%"></i></div>
          <span class="small muted">${ml.label}${m.n ? ` · ${m.ok}/${m.n} right` : ''}</span>
          <button class="btn primary" data-act="start" data-kind="drill" data-topic="${key}">Drill this topic</button>
          <button class="btn" data-act="mark-read" data-topic="${key}">${S().learned[key] ? 'Marked as read' : 'Mark as read'}</button>
        </div>
        ${skills.length ? `<div class="stack"><span class="eyebrow">Skills in the question bank</span><div class="row" style="gap:6px">${skills.map(s => `<span class="chip">${esc(s)}</span>`).join('')}</div></div>` : ''}`
        : `<div class="sheet pad stack"><span class="eyebrow">${esc(extra?.[1] || '')}</span><button class="btn primary" data-act="mark-read" data-topic="${key}">${S().learned[key] ? 'Read' : 'Mark as read'}</button></div>`}
      </aside>
    </div>
  </div>`;
}

// Short preview of a stem that never cuts through a maths fragment.
function snippet(stem, max = 90) {
  const flat = stem.replace(/\$\$[\s\S]*?\$\$/g, ' … ').replace(/^>\s*/gm, '').replace(/[#*_`]/g, '').replace(/\s+/g, ' ').trim();
  let out = '', len = 0;
  for (const part of flat.split(/(\$[^$]*\$)/)) {
    const cost = part.startsWith('$') ? Math.ceil(part.length / 2) : part.length;
    if (len + cost > max) {
      if (!part.startsWith('$')) out += part.slice(0, Math.max(0, max - len)).replace(/\s+\S*$/, '');
      return mdi(out.trim()) + '…';
    }
    out += part; len += cost;
  }
  return mdi(out);
}

// ------------------------------------------------------------ mistakes
export function reviewView(model, filter = {}) {
  const st = S();
  const due = dueReviews();
  const wrong = st.attempts.filter(a => !a.ok && a.qid && !a.qid.startsWith('past:'));
  const byQ = new Map();
  for (const a of wrong) {
    const e = byQ.get(a.qid) || { qid: a.qid, topic: a.topic, n: 0, last: 0, reason: null, d: a.d };
    e.n++; e.last = Math.max(e.last, a.at); if (a.reason) e.reason = a.reason;
    byQ.set(a.qid, e);
  }
  let rows = Array.from(byQ.values()).sort((a, b) => b.last - a.last);
  if (filter.topic) rows = rows.filter(r => r.topic === filter.topic);
  if (filter.reason) rows = rows.filter(r => (filter.reason === 'untagged' ? !r.reason : r.reason === filter.reason));
  const counts = {};
  for (const a of wrong) counts[a.reason || 'untagged'] = (counts[a.reason || 'untagged'] || 0) + 1;
  const tagged = wrong.filter(a => a.reason);
  const top = Object.entries(counts).filter(([k]) => k !== 'untagged').sort((a, b) => b[1] - a[1])[0];
  const advice = {
    concept: 'Most misses are method gaps. Read the notes for those topics before drilling them.',
    careless: 'Most misses are slips. Build a 10-second check into every answer: signs, endpoints, and whether you answered the question asked.',
    misread: 'You often misread. Underline "not", "must", "complete set", and "which is false" before you start working.',
    trap: 'You are falling for designed traps. After choosing an answer, ask which slip each other option represents.',
    time: 'Time pressure is costing marks. Practise timed sets and skip anything that has not moved after 90 seconds.',
    guess: 'Many misses are guesses. That is fine under time pressure, but they mark topics to revisit.',
  };
  const topicsWithMisses = Array.from(new Set(wrong.map(a => a.topic))).filter(Boolean);
  return `<div class="col wide">
    <div class="stack" style="gap:6px"><span class="eyebrow">Mistakes</span><h1>Your error log</h1>
      <p class="muted">Missed ideas come back after 1, 3, 7 and 14 days, and every review is a different question on the same idea: a twin with new numbers and a new set-up, never the one you got wrong. You can't pass a review by remembering an answer.</p></div>
    <section class="sheet pad spread">
      <div class="stack" style="gap:2px"><b class="num" style="font-size:1.5rem">${due.length} due</b><span class="small muted">${Object.keys(st.srs).length} in rotation · ${byQ.size} different questions missed</span></div>
      <button class="btn primary" data-act="start" data-kind="review" ${due.length ? '' : 'disabled'}>Review ${due.length ? 'now' : '(none due)'}</button>
    </section>
    ${wrong.length ? `<section class="sheet pad stack">
      <h3>Why you lose marks</h3>
      <div class="hbars">${REASONS.map(([k, l]) => {
        const c = counts[k] || 0;
        return `<div class="hbar"><span class="small">${l}</span><div class="track"><div class="fill" style="width:${tagged.length ? (100 * c) / tagged.length : 0}%"></div></div><span class="mono small">${c}</span></div>`;
      }).join('')}</div>
      <p class="small muted">${counts.untagged ? `${counts.untagged} miss${counts.untagged === 1 ? ' is' : 'es are'} untagged. Tag them when you review so this gets sharper.` : ''}</p>
      ${top ? `<p><b>Pattern:</b> ${esc(advice[top[0]])}</p>` : ''}
    </section>` : ''}
    <section class="stack">
      <div class="section-head"><h3>Missed questions</h3>
        <div class="row" style="gap:8px">
          <select class="input" id="rv-topic" data-act="rv-filter" style="width:auto;min-height:34px;padding:4px 10px"><option value="">All topics</option>${topicsWithMisses.map(k => `<option value="${k}" ${filter.topic === k ? 'selected' : ''}>${esc(TOPIC[k].short)}</option>`).join('')}</select>
          <select class="input" id="rv-reason" data-act="rv-filter" style="width:auto;min-height:34px;padding:4px 10px"><option value="">Any reason</option>${REASONS.map(([k, l]) => `<option value="${k}" ${filter.reason === k ? 'selected' : ''}>${l}</option>`).join('')}<option value="untagged" ${filter.reason === 'untagged' ? 'selected' : ''}>Untagged</option></select>
        </div></div>
      ${rows.length ? `<div class="sheet table-wrap"><table class="data"><thead><tr><th>Question</th><th>Topic</th><th>Level</th><th class="num">Misses</th><th>Reason</th><th>Last</th></tr></thead><tbody>
        ${rows.slice(0, 80).map(r => {
          const q = getQuestion(r.qid);
          const title = q ? snippet(q.stem) : esc(r.qid);
          return `<tr class="click" data-act="open-q" data-id="${esc(r.qid)}"><td style="min-width:200px">${title}</td><td>${esc(TOPIC[r.topic]?.short || '')}</td><td>${diffDots(r.d || 3)}</td><td class="num mono">${r.n}</td><td class="small">${esc((REASONS.find(x => x[0] === r.reason) || [, '–'])[1])}</td><td class="small muted">${fmtDate(dateKey(r.last))}</td></tr>`;
        }).join('')}</tbody></table></div>`
        : `<div class="sheet empty"><b>No mistakes logged${filter.topic || filter.reason ? ' for this filter' : ' yet'}.</b><span>Every wrong answer lands here with its worked solution.</span></div>`}
    </section>
  </div>`;
}

// Single question viewer (from the error log).
export function questionView(id, back = 'review') {
  const q = getQuestion(id);
  if (!q) return `<div class="col"><p>Question not found.</p></div>`;
  const hist = S().attempts.filter(a => a.qid === id);
  const last = hist[hist.length - 1];
  return `<div class="col">
    <div class="row"><button class="btn sm ghost" data-act="go" data-to="${back}">${ICON.arrowL}Back</button></div>
    <article class="sheet qsheet">
      <div class="qhead"><div class="qmeta">${topicChip(q.topic)}${diffDots(q.difficulty)}</div>
        <span class="small muted">${hist.length} attempt${hist.length === 1 ? '' : 's'} · ${hist.filter(a => a.ok).length} right</span></div>
      <div class="stem">${md(q.stem)}</div>
      ${figureHTML(q.figure)}
      ${optionsHTML(q, { sel: last?.choice ?? null, reveal: true })}
      <div class="feedback">${solutionHTML(q, last?.choice)}${tutorHTML(q, { choice: last?.choice ?? null, checked: true })}</div>
      <div class="row"><button class="btn primary" data-act="twin" data-id="${esc(q.id)}">Try its twin</button><button class="btn" data-act="start" data-kind="drill" data-topic="${q.topic}">Drill ${esc(TOPIC[q.topic].short)}</button></div>
    </article>
  </div>`;
}

// ------------------------------------------------------------ progress
function activityChart(st) {
  const days = 14;
  const today = dateKey();
  const data = [];
  for (let i = days - 1; i >= 0; i--) {
    const k = addDays(today, -i);
    const at = st.attempts.filter(a => dateKey(a.at) === k);
    data.push({ k, n: at.length, ok: at.filter(a => a.ok).length });
  }
  const max = Math.max(10, ...data.map(d => d.n));
  const W = 420, H = 170, L = 26, B = 22, T = 8;
  const bw = (W - L) / days;
  const y = v => T + (H - T - B) * (1 - v / max);
  const step = max > 40 ? 20 : max > 20 ? 10 : 5;
  let grid = '';
  for (let v = 0; v <= max; v += step) grid += `<line class="gl" x1="${L}" x2="${W}" y1="${y(v)}" y2="${y(v)}"/><text class="tick" x="${L - 6}" y="${y(v) + 3.5}" text-anchor="end">${v}</text>`;
  const bars = data.map((d, i) => {
    const x = L + i * bw + 3, w = bw - 6;
    const h1 = (H - T - B) * (d.n / max), h2 = (H - T - B) * (d.ok / max);
    const tip = `${fmtDate(d.k)}: ${d.n} answered, ${d.ok} right${d.n ? ` (${pct(d.ok / d.n)})` : ''}`;
    return `<g class="bh" data-tip="${esc(tip)}">
      <rect class="hit" x="${L + i * bw}" y="${T}" width="${bw}" height="${H - T - B}"/>
      ${d.n ? `<rect class="bar dim" x="${x}" y="${y(d.n)}" width="${w}" height="${Math.max(0, h1)}" rx="3"/>` : ''}
      ${d.ok ? `<rect class="bar" x="${x}" y="${y(d.ok)}" width="${w}" height="${Math.max(0, h2)}" rx="3"/>` : ''}
      ${i % 2 === (days - 1) % 2 ? `<text class="tick" x="${x + w / 2}" y="${H - 8}" text-anchor="middle">${fmtDate(d.k, { day: 'numeric', month: 'numeric' })}</text>` : ''}
    </g>`;
  }).join('');
  return `<svg class="chart" viewBox="0 0 ${W} ${H}" role="img" aria-label="Questions answered per day, last 14 days">${grid}<line class="ax" x1="${L}" x2="${W}" y1="${y(0)}" y2="${y(0)}"/>${bars}</svg>
    <div class="legend"><span><i style="background:var(--accent)"></i>Right</span><span><i style="background:var(--rule-2)"></i>Answered</span></div>`;
}

export function progressView(model) {
  const st = S();
  const pred = predict(model);
  const rows = TOPICS.map(t => ({ t, m: model.topics[t.key] })).sort((a, b) => (a.m.n ? a.m.mastery : 2) - (b.m.n ? b.m.mastery : 2));
  const pace = [1, 2, 3, 4, 5].map(d => {
    const at = st.attempts.filter(a => a.d === d && a.ms && a.mode !== 'past');
    const tgt = mean(at.map(a => a.target || 0).filter(Boolean)) || [0, 90, 140, 200, 260, 320][d];
    return { d, n: at.length, avg: mean(at.map(a => a.ms / 1000)), tgt, acc: at.length ? at.filter(a => a.ok).length / at.length : null };
  });
  const pmax = Math.max(360, ...pace.map(p => p.avg * 1.05));
  const sessions = st.sessions.slice().reverse().filter(s => ['mock', 'timed', 'diagnostic'].includes(s.kind)).slice(0, 12);
  const papers = st.papers.slice().sort((a, b) => a.date.localeCompare(b.date));
  const enough = st.attempts.length >= 10;
  return `<div class="col wide">
    <div class="stack" style="gap:6px"><span class="eyebrow">Progress</span><h1>How you're doing</h1>
      <p class="muted">${st.attempts.length} answers logged. Estimates weight recent answers and harder questions more, and discount slow or guessed correct answers.</p></div>
    <section class="sheet predict">
      ${[1, 2].map(p => `<div><span class="eyebrow">Predicted Paper ${p}</span>${enough ? `<span class="big num">${pred[p].exp.toFixed(1)}<span> / 20</span></span><span class="small muted">Likely ${pred[p].lo.toFixed(0)}–${pred[p].hi.toFixed(0)}</span>` : '<span class="big">–</span><span class="small muted">Needs 10+ answers</span>'}</div>`).join('')}
    </section>
    <section class="sheet pad marks">
      <div class="stack" style="justify-items:center">${masteryWheel(model)}</div>
      <div class="stack">
        <h3>Shape of your strengths</h3>
        <p class="small muted">Wedge length is estimated mastery: the chance you get a typical TMUA question on that topic right. Dotted rings mark 45%, 62% and 80%. The blue labels are Paper 2 only. Tap a wedge to drill it.</p>
        ${strongWeak(model)}
      </div>
    </section>
    ${coachHTML()}
    <section class="stack">
      <div class="section-head"><h2>Topics, weakest first</h2><span class="small muted">Mastery = estimated chance of a typical TMUA question right</span></div>
      <div class="sheet table-wrap"><table class="data">
        <thead><tr><th>Topic</th><th style="width:30%">Mastery</th><th>Status</th><th class="num">Right</th><th class="num">Avg time</th><th>Last 8</th><th></th></tr></thead>
        <tbody>${rows.map(({ t, m }) => {
          const ml = masteryLabel(m.mastery, m.n);
          return `<tr><td><b>${esc(t.name)}</b>${t.paper === 2 ? ' <span class="small muted">P2</span>' : ''}</td>
            <td><div class="meter ${toneOf(ml)}" data-tip="${esc(t.short)}: ${m.n ? pct(m.mastery) : 'no data'}"><i style="width:${m.n ? Math.round(m.mastery * 100) : 0}%"></i></div></td>
            <td><span class="chip tone-${ml.tone}">${ml.label}</span></td>
            <td class="num mono">${m.n ? `${m.ok}/${m.n}` : '–'}</td>
            <td class="num mono">${m.avgMs ? fmtSecs(m.avgMs) : '–'}</td>
            <td><span class="spark">${m.recent.map(v => `<i class="${v ? 'y' : 'n'}"></i>`).join('') || '<span class="muted small">–</span>'}</span></td>
            <td><button class="btn sm" data-act="start" data-kind="drill" data-topic="${t.key}">Drill</button></td></tr>`;
        }).join('')}</tbody></table></div>
    </section>
    <section class="grid-2">
      <div class="sheet pad stack"><h3>Last 14 days</h3>${activityChart(st)}</div>
      <div class="sheet pad stack"><h3>Pace by difficulty</h3>
        <div class="hbars">${pace.map(p => `<div class="hbar"><span class="small">Level ${p.d}${p.acc != null ? ` <span class="muted">· ${pct(p.acc)}</span>` : ''}</span>
          <div class="track" data-tip="${p.n ? `Level ${p.d}: average ${fmtSecs(p.avg * 1000)} vs target ${fmtSecs(p.tgt * 1000)} (${p.n} answers)` : 'No answers yet'}"><div class="fill ${p.avg > p.tgt ? 'over' : ''}" style="width:${(100 * p.avg) / pmax}%"></div><div class="target" style="left:${(100 * p.tgt) / pmax}%"></div></div>
          <span class="mono small">${p.n ? fmtSecs(p.avg * 1000) : '–'}</span></div>`).join('')}</div>
        <div class="legend"><span><i style="background:var(--accent)"></i>Your average</span><span><i style="background:var(--warn)"></i>Over target</span><span><i style="background:var(--ink);width:2px"></i>Target</span></div>
      </div>
    </section>
    <section class="grid-2">
      <div class="sheet pad stack"><h3>Timed sessions</h3>
        ${sessions.length ? `<table class="data"><tbody>${sessions.map(s => `<tr><td>${esc(s.title)}</td><td class="small muted">${fmtDate(dateKey(s.at))}</td><td class="num mono">${s.ok}/${s.n}</td></tr>`).join('')}</tbody></table>` : '<p class="muted small">Mocks, timed sets and diagnostics appear here.</p>'}
      </div>
      <div class="sheet pad stack"><div class="spread"><h3>Official papers</h3><button class="btn sm ghost" data-act="go" data-to="papers">Log a paper</button></div>
        ${papers.length ? `<table class="data"><tbody>${papers.map(p => `<tr><td>${esc(p.year)} Paper ${p.paper}</td><td class="small muted">${fmtDate(p.date)}</td><td class="num mono">${p.score}/20</td></tr>`).join('')}</tbody></table>` : '<p class="muted small">Scores from official past papers appear here.</p>'}
      </div>
    </section>
  </div>`;
}

// ------------------------------------------------------------ papers
export function papersView(draft) {
  const st = S();
  const d = draft;
  const logged = st.papers.slice().sort((a, b) => b.date.localeCompare(a.date));
  return `<div class="col">
    <div class="stack" style="gap:6px"><span class="eyebrow">Official past papers</span><h1>Log a real paper</h1>
      <p class="muted">The official papers are the best practice there is. Download them from the <a href="${PREP_URL}" target="_blank" rel="noopener">UAT-UK TMUA preparation page ${ICON.ext.replace('<svg', '<svg style="width:13px;height:13px;vertical-align:-1px"')}</a>, sit one under timed conditions, mark it with the official answer key, then log it here. Tagging the topic of each miss feeds your plan.</p></div>
    <form class="sheet pad stack-lg" id="paper-form" autocomplete="off">
      <div class="grid-3">
        <div class="field"><label for="pp-year">Paper</label><select class="input" id="pp-year">${PAST_PAPERS.map(y => `<option ${d.year === y ? 'selected' : ''}>${y}</option>`).join('')}</select></div>
        <div class="field"><label for="pp-paper">Which paper</label><select class="input" id="pp-paper"><option value="1" ${d.paper === 1 ? 'selected' : ''}>Paper 1</option><option value="2" ${d.paper === 2 ? 'selected' : ''}>Paper 2</option></select></div>
        <div class="field"><label for="pp-mins">Minutes used</label><input class="input" id="pp-mins" type="number" min="1" max="200" value="${d.mins}"></div>
      </div>
      <div class="field"><label>Tap the questions you got wrong or left blank</label>
        <div class="paper-q">${Array.from({ length: 20 }, (_, i) => `<button type="button" data-act="pp-toggle" data-q="${i + 1}" aria-pressed="${d.wrong.includes(i + 1)}">${i + 1}</button>`).join('')}</div>
        <span class="small muted">Score: <b class="num">${20 - d.wrong.length}/20</b></span>
      </div>
      ${d.wrong.length ? `<div class="field"><label>Topic of each miss (optional, but it sharpens your plan)</label>
        <div class="grid-2">${d.wrong.slice().sort((a, b) => a - b).map(n => `<div class="row" style="gap:8px;flex-wrap:nowrap"><span class="mono" style="width:32px">Q${n}</span><select class="input" data-act="pp-topic" data-q="${n}" id="pp-t${n}"><option value="">Not sure</option>${TOPICS.filter(t => d.paper === 2 || t.paper === 1).map(t => `<option value="${t.key}" ${d.topics[n] === t.key ? 'selected' : ''}>${esc(t.name)}</option>`).join('')}</select></div>`).join('')}</div></div>` : ''}
      <div class="field"><label for="pp-notes">Notes to self</label><input class="input" id="pp-notes" value="${esc(d.notes)}" placeholder="e.g. ran out of time on 17–20; logic questions felt fine"></div>
      <div class="row"><button class="btn primary" type="submit">Save paper</button></div>
    </form>
    ${logged.length ? `<section class="stack"><h2>Logged</h2><div class="sheet table-wrap"><table class="data"><thead><tr><th>Paper</th><th>Date</th><th class="num">Score</th><th class="num">Time</th><th>Missed</th><th></th></tr></thead><tbody>
      ${logged.map(p => `<tr><td><b>${esc(p.year)} P${p.paper}</b>${p.notes ? `<div class="small muted">${esc(p.notes)}</div>` : ''}</td><td class="small muted">${fmtDate(p.date)}</td><td class="num mono">${p.score}/20</td><td class="num mono">${p.mins}m</td><td class="small">${p.wrong.join(', ') || '–'}</td><td><button class="btn sm ghost" data-act="pp-del" data-id="${p.id}">Delete</button></td></tr>`).join('')}
    </tbody></table></div></section>` : ''}
  </div>`;
}

// ------------------------------------------------------------ settings
export function settingsView(ui) {
  const st = S();
  const reported = Object.entries(st.reported);
  const stats = bankStats();
  return `<div class="col">
    <div class="stack" style="gap:6px"><span class="eyebrow">Settings</span><h1>Settings and data</h1></div>
    <section class="sheet pad stack-lg">
      <div class="grid-2">
        <div class="field"><label for="set-date">Test date</label><input class="input" type="date" id="set-date" value="${st.settings.examDate}"><span class="small muted">The October 2026 window is 12–16 October.</span></div>
        <div class="field"><label for="set-theme">Appearance</label><select class="input" id="set-theme">${[['system', 'Match system'], ['light', 'Light'], ['dark', 'Dark']].map(([v, l]) => `<option value="${v}" ${st.settings.theme === v ? 'selected' : ''}>${l}</option>`).join('')}</select></div>
      </div>
    </section>
    <section class="sheet pad stack">
      <h3>Back up or move your progress</h3>
      <p class="small muted">${syncStatus() !== 'local' ? 'Your progress syncs automatically to every device where you open this page while signed in. Backups are still useful before a reset.' : `Progress is stored in this browser only${storageWorks() ? '' : ' (and storage is blocked here, so it will be lost when you close the page)'}. Use a backup to move it to another device.`}</p>
      <div class="row">${getCaps().downloads ? '<button class="btn" data-act="download-backup">Download backup file</button>' : ''}<button class="btn ${getCaps().downloads ? 'ghost' : ''}" data-act="export">Copy backup code</button><button class="btn ghost" data-act="show-import">Paste a backup…</button><label class="btn ghost" for="import-file">Restore from file…</label><input type="file" id="import-file" accept=".json,application/json" hidden></div>
      ${ui.exportText ? `<textarea class="input" id="export-box" readonly>${esc(ui.exportText)}</textarea>` : ''}
      ${ui.importing ? `<textarea class="input" id="import-box" placeholder="Paste your backup code here"></textarea><div class="row"><button class="btn primary" data-act="import">Restore</button><span class="small muted">This replaces the progress on this device.</span></div>` : ''}
    </section>
    ${reported.length ? `<section class="sheet pad stack"><h3>Reported questions</h3><p class="small muted">These are hidden from practice.</p>
      ${reported.map(([id, r]) => `<div class="spread"><span class="small">${mdi(esc(r.title || id))}…</span><button class="btn sm ghost" data-act="unreport" data-id="${esc(id)}">Restore</button></div>`).join('')}</section>` : ''}
    <section class="sheet pad stack">
      <h3>Start again</h3>
      ${ui.confirmReset ? `<p><b>Delete all progress on this device?</b> This cannot be undone.</p><div class="row"><button class="btn danger" data-act="reset">Delete everything</button><button class="btn ghost" data-act="reset-cancel">Cancel</button></div>`
        : `<div><button class="btn danger" data-act="reset-ask">Reset progress</button></div>`}
    </section>
    <p class="small muted">${stats.questions} written questions with worked solutions, plus ${stats.generators} question generators that make unlimited checked variants. Keyboard: <kbd>A</kbd>–<kbd>H</kbd> answer, <kbd>Enter</kbd> check, <kbd>G</kbd> guess, <kbd>Shift</kbd>+letter cross out.</p>
  </div>`;
}

// ------------------------------------------------------------ onboarding
export function onboardingView(ui) {
  const st = S();
  const dates = ['2026-10-12', '2026-10-13', '2026-10-14', '2026-10-15', '2026-10-16'];
  const sel = ui.onbDate || st.settings.examDate;
  const stats = bankStats();
  return `<div class="onb">
    <div class="answer-sheet" aria-hidden="true">${LETTERS.split('').map((l, i) => `<span class="${i === 3 ? 'fill' : ''}">${l}</span>`).join('')}</div>
    <div class="stack" style="gap:14px">
      <h1>Two weeks to the TMUA. <em>Let's spend them well.</em></h1>
      <p class="lede">A diagnostic finds your weak spots. Each day's plan and practice then goes after them, with timed papers so you get used to 20 questions in 75 minutes.</p>
    </div>
    <div class="features">
      <div><b>Adapts to you</b><span>Every answer updates your topic estimates and tomorrow's plan.</span></div>
      <div><b>${getCaps().sample ? 'A tutor on call' : 'Worked solutions'}</b><span>${getCaps().sample ? 'Hints that don\'t spoil it, and explanations of your exact mistake.' : 'Every question explains the trap behind each tempting wrong answer.'}</span></div>
      <div><b>Exam pace</b><span>Timed sets and full mocks with a pace line, flags and a navigator.</span></div>
    </div>
    <section class="stack">
      <span class="eyebrow">When is your test?</span>
      <div class="datepick">${dates.map(d => `<button data-act="onb-date" data-d="${d}" aria-pressed="${sel === d}"><span>${fmtDate(d, { weekday: 'short' })}</span><b>${+d.slice(8)}</b><span>Oct</span></button>`).join('')}</div>
      <div class="row small muted"><label for="onb-other">Different date:</label><input class="input" type="date" id="onb-other" style="width:auto" value="${sel}"></div>
    </section>
    <div class="row">
      <button class="btn primary lg" data-act="onb-go">Start the diagnostic</button>
      <button class="btn ghost" data-act="onb-skip">Skip for now</button>
    </div>
    <p class="small muted">${stats.questions} worked questions across ${TOPICS.length} topics, plus generators that make unlimited checked variants. Progress stays on this device.</p>
  </div>`;
}

function strongWeak(model) {
  const tested = TOPICS.map(t => ({ t, m: model.topics[t.key] })).filter(x => x.m.n >= 3).sort((a, b) => b.m.mastery - a.m.mastery);
  if (tested.length < 2) return '<p class="small">Answer a few questions in each topic and this fills in.</p>';
  const top = tested.slice(0, 2), bottom = tested.slice(-2).reverse();
  const li = x => `<li><b>${esc(x.t.name)}</b> <span class="muted">${pct(x.m.mastery)}</span></li>`;
  return `<div class="grid-2" style="gap:12px"><div><span class="eyebrow">Strongest</span><ul class="small" style="margin:6px 0 0;padding-left:1.1em">${top.map(li).join('')}</ul></div><div><span class="eyebrow">Weakest</span><ul class="small" style="margin:6px 0 0;padding-left:1.1em">${bottom.map(li).join('')}</ul></div></div>`;
}

// Plain-text summary of the student's data for the study coach.
export function coachSummary(model) {
  const st = S();
  const pred = predict(model);
  const left = Math.round((new Date(st.settings.examDate) - new Date(dateKey())) / 86400000);
  const topics = TOPICS.map(t => {
    const m = model.topics[t.key];
    return `- ${t.name} (Paper ${t.paper === 2 ? '2 only' : '1 and 2'}): ${m.n ? `${m.ok}/${m.n} right, mastery ${pct(m.mastery)}, avg ${fmtSecs(m.avgMs || 0)} per question` : 'not practised'}`;
  }).join('\n');
  const wrong = st.attempts.filter(a => !a.ok);
  const reasons = {};
  for (const a of wrong) reasons[a.reason || 'untagged'] = (reasons[a.reason || 'untagged'] || 0) + 1;
  const slow = st.attempts.filter(a => a.ok && a.target && a.ms > a.target * 1500).length;
  const sessions = st.sessions.slice(-6).map(x => `${x.title}: ${x.ok}/${x.n}`).join('; ') || 'none';
  const papers = st.papers.map(p => `${p.year} P${p.paper}: ${p.score}/20 in ${p.mins} min`).join('; ') || 'none logged';
  return `Days until the test: ${left}. Answers logged: ${st.attempts.length}. Predicted marks: Paper 1 ${pred[1].exp.toFixed(1)}/20, Paper 2 ${pred[2].exp.toFixed(1)}/20.
Topics:
${topics}
Reasons tagged on wrong answers: ${Object.entries(reasons).map(([k, v]) => `${k} ${v}`).join(', ') || 'none'}.
Correct but slow (over 1.5x target time): ${slow}. Guessed answers: ${st.attempts.filter(a => a.guess).length}. Hints used: ${st.attempts.filter(a => a.hint).length}.
Mistakes due for review: ${dueList().length}.
Recent sessions: ${sessions}.
Official past papers: ${papers}.`;
}
