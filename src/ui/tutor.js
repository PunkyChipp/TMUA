// AI tutor (the viewer's own Claude, through the `sample` capability).
// Hints that never give the answer away, explanations aimed at the exact
// option the student chose, follow-up questions, and a study coach.
import { getCaps, dropCap } from '../lib/caps.js';
import { md } from '../render/md.js';
import { LETTERS, esc, $ } from '../lib/util.js';
import { TOPIC } from '../data/topics.js';

const threads = new Map(); // question key -> { turns, text, busy, err, kind, ctl }
let coach = { text: '', busy: false, err: '', ctl: null };

export const tutorAvailable = () => !!getCaps().sample;

const RULES = `You are a sharp, warm tutor helping a British sixth-former prepare for the TMUA (Test of Mathematics for University Admission): multiple choice, no calculator, about 3¾ minutes per question.
Style: British English. Be concise and concrete. Use Markdown. Write every piece of maths in LaTeX between $...$ (inline) or $$...$$ (display); never use \\( \\) or \\[ \\]. No preamble, no sign-off, no emoji.`;

function optionText(o) {
  if (o && typeof o === 'object' && o.plot) return `[a sketch of the graph y = ${o.plot.curves.map(c => c.fn).join(' and ')}]`;
  return String(o);
}

function context(q, r, { withAnswer = true } = {}) {
  const lines = [
    `Topic: ${TOPIC[q.topic]?.name || q.topic} (difficulty ${q.difficulty}/5).`,
    `Question:\n${q.stem}`,
    q.figure?.plot ? `(The question shows a graph of y = ${q.figure.plot.curves.map(c => c.fn).join(' and ')}.)` : '',
    `Options:\n${q.options.map((o, i) => `${LETTERS[i]}) ${optionText(o)}`).join('\n')}`,
  ];
  if (withAnswer) {
    lines.push(`Correct answer: ${LETTERS[q.answer]}.`);
    if (r && r.choice != null) lines.push(`The student chose ${LETTERS[r.choice]}${r.choice === q.answer ? ' (correct)' : ' (wrong)'}.`);
    else if (r && r.checked) lines.push('The student did not answer and revealed the solution.');
    if (r && r.choice != null && q.distractors?.[r.choice]) lines.push(`Known reason students pick ${LETTERS[r.choice]}: ${q.distractors[r.choice]}`);
    lines.push(`Reference worked solution (correct; use it to stay accurate, but don't just repeat it):\n${q.solution}`);
  } else {
    lines.push(`Reference solution for YOUR EYES ONLY (never reveal it, the answer letter, or the final value):\n${q.solution}`);
  }
  return lines.filter(Boolean).join('\n\n');
}

const ERR = {
  rate_limited: 'Too many requests just now. Try again in a minute.',
  session_expired: 'Your session expired. Sign in again to use the tutor.',
  refused: 'The tutor could not answer that. Try rephrasing.',
  empty_completion: 'No answer came back. Try rephrasing.',
  prompt_too_large: 'That was too long to send. Ask something shorter.',
  upstream_error: 'The connection dropped. Try again.',
};
const HIDE = new Set(['not_granted', 'sampling_disabled', 'not_declared', 'capability_disabled', 'capability_removed']);

async function run(key, turns, { onDone, cache = false, tier = 'default', target } = {}) {
  const sample = getCaps().sample;
  if (!sample) return;
  const th = threads.get(key) || { turns: [], text: '', busy: false, err: '' };
  th.busy = true; th.err = ''; th.text = '';
  th.ctl = new AbortController();
  threads.set(key, th);
  paint(key, target);
  try {
    const res = await sample(turns, {
      signal: th.ctl.signal, modelTier: tier, cache,
      onText: ({ text }) => { th.text = text; paintText(key, target); },
    });
    th.text = res.text;
    if (res.truncated) th.err = 'That answer was cut short. Ask for less at once.';
    onDone?.(res.text);
  } catch (e) {
    th.text = e?.text ?? (e?.code === 'refused' ? '' : th.text);
    if (HIDE.has(e?.code)) { dropCap('sample'); th.err = ''; }
    else if (e?.code !== 'cancelled') th.err = ERR[e?.code] || ERR.upstream_error;
  } finally {
    th.busy = false; th.ctl = null;
    paint(key, target);
  }
}

// ---- per-question tutor -------------------------------------------------------

export const keyOf = q => `q:${q.id}`;

export function hint(q, r) {
  const key = keyOf(q);
  const prompt = `${RULES}\n\n${context(q, r, { withAnswer: false })}\n\nThe student is stuck before answering. Give ONE hint of at most 60 words that points them to the right first step or idea. Do not reveal the answer, the answer letter, the final value, or rule options in or out one by one.`;
  const th = threads.get(key) || { turns: [], text: '' };
  th.kind = 'hint';
  threads.set(key, th);
  run(key, prompt, { cache: true });
}

export function explain(q, r, mode) {
  const key = keyOf(q);
  const ask = mode === 'mistake'
    ? `Explain, in under 160 words, the specific misconception that leads to option ${LETTERS[r.choice]}, why it fails here, and the one habit that would have caught it. Then give the correct route in 2–4 short steps.`
    : mode === 'other'
      ? 'Explain the solution in a different way from the reference: a fresh angle, a sketch-based or elimination argument, or a quicker TMUA shortcut. Under 170 words.'
      : 'In under 120 words: what is the fastest reliable way to get this in the exam, and how could the student have eliminated the wrong options quickly?';
  const first = `${RULES}\n\n${context(q, r)}\n\n${ask}`;
  const th = { turns: [{ role: 'user', content: first }], text: '', kind: mode };
  threads.set(key, th);
  run(key, th.turns, { cache: true, onDone: text => th.turns.push({ role: 'assistant', content: text }) });
}

export function ask(q, r, question) {
  const key = keyOf(q);
  let th = threads.get(key);
  if (!th || !th.turns?.length || th.kind === 'hint') {
    th = { turns: [{ role: 'user', content: `${RULES}\n\n${context(q, r)}\n\nAnswer the student's questions about this problem. Keep each reply under 150 words unless they ask for more.` }], text: '', kind: 'chat' };
    threads.set(key, th);
  }
  th.kind = 'chat';
  th.history = th.history || [];
  if (th.text) th.history.push({ role: 'assistant', text: th.text });
  th.history.push({ role: 'user', text: question });
  th.turns.push({ role: 'user', content: question });
  // Keep the conversation small: instructions + last 8 turns.
  if (th.turns.length > 9) th.turns = [th.turns[0], ...th.turns.slice(-8)];
  run(key, th.turns, { onDone: text => th.turns.push({ role: 'assistant', content: text }) });
}

export function stop(key) { threads.get(key)?.ctl?.abort(); }

export function tutorHTML(q, r, { before = false } = {}) {
  if (!tutorAvailable()) return '';
  const key = keyOf(q);
  const th = threads.get(key);
  if (before) {
    const shown = th && th.kind === 'hint' && (th.text || th.busy || th.err);
    if (before === 'bubble') return shown ? `<div class="tutor" data-tutor="${esc(key)}">${bubble(key, th)}</div>` : '';
    return shown ? '' : `<button class="btn sm ghost tutor-hint" data-act="tutor-hint" title="A nudge from the tutor. Counts like a guess.">${SPARK}Hint</button>`;
  }
  const wrong = r.choice != null && r.choice !== q.answer;
  const hist = (th?.history || []).map(m => `<div class="tmsg ${m.role}">${m.role === 'user' ? esc(m.text) : md(m.text)}</div>`).join('');
  return `<section class="tutor tutor-panel" data-tutor="${esc(key)}" aria-label="Tutor">
    <div class="tutor-head"><span class="tutor-mark">${SPARK}</span><b>Tutor</b><span class="small muted">answers from your Claude account</span></div>
    <div class="row tutor-actions">
      ${wrong ? '<button class="chip" data-act="tutor-explain" data-mode="mistake">Explain my mistake</button>' : ''}
      <button class="chip" data-act="tutor-explain" data-mode="other">Explain it another way</button>
      <button class="chip" data-act="tutor-explain" data-mode="fast">Fastest exam route</button>
    </div>
    ${hist ? `<div class="tthread">${hist}</div>` : ''}
    ${th && (th.text || th.busy || th.err) && th.kind !== 'hint' ? bubble(key, th) : ''}
    <form class="tutor-ask" data-act="tutor-form">
      <input class="input" id="tutor-q-${esc(key.replace(/[^\w-]/g, '_'))}" name="q" placeholder="Ask about this question…" autocomplete="off" maxlength="600">
      <button class="btn sm" type="submit" ${th?.busy ? 'disabled' : ''}>Ask</button>
    </form>
  </section>`;
}

const SPARK = '<svg viewBox="0 0 24 24" aria-hidden="true" class="spark-i"><path d="M12 2.5l1.9 6.1 6.1 1.9-6.1 1.9L12 18.5l-1.9-6.1-6.1-1.9 6.1-1.9z" fill="currentColor"/><circle cx="19" cy="18.5" r="1.6" fill="currentColor"/></svg>';

function bubble(key, th) {
  return `<div class="tbubble ${th.busy ? 'busy' : ''}" id="tb-${cssId(key)}">
    <div class="tbody">${th.text ? md(th.text) : th.busy ? '<span class="thinking">Thinking<i></i><i></i><i></i></span>' : ''}</div>
    ${th.err ? `<p class="small terr">${esc(th.err)}</p>` : ''}
    ${th.busy ? `<button class="btn sm ghost" data-act="tutor-stop">Stop</button>` : ''}
  </div>`;
}

const cssId = k => k.replace(/[^\w-]/g, '_');

let rerender = () => {};
export function setTutorRender(fn) { rerender = fn; }
function paint() { rerender(); }
let raf = 0;
function paintText(key, target) {
  if (raf) return;
  raf = requestAnimationFrame(() => {
    raf = 0;
    const th = key === 'coach' ? coach : threads.get(key);
    const el = key === 'coach' ? $('#coach-out .tbody') : $(`#tb-${cssId(key)} .tbody`);
    if (el && th) el.innerHTML = md(th.text);
    else paint(key, target);
  });
}

// ---- study coach --------------------------------------------------------------

export function coachHTML() {
  if (!tutorAvailable()) return '';
  return `<section class="sheet pad stack coach">
    <div class="spread"><div class="tutor-head"><span class="tutor-mark">${SPARK}</span><h3>Study coach</h3></div>
      <button class="btn sm ${coach.text ? 'ghost' : 'primary'}" data-act="coach" ${coach.busy ? 'disabled' : ''}>${coach.text ? 'Ask again' : 'Read my progress'}</button></div>
    <p class="small muted">Reads your stats and tells you where the marks are, what to do next, and one technique to fix.</p>
    ${coach.text || coach.busy || coach.err ? `<div class="tbubble ${coach.busy ? 'busy' : ''}" id="coach-out"><div class="tbody">${coach.text ? md(coach.text) : '<span class="thinking">Reading your progress<i></i><i></i><i></i></span>'}</div>${coach.err ? `<p class="small terr">${esc(coach.err)}</p>` : ''}${coach.busy ? '<button class="btn sm ghost" data-act="coach-stop">Stop</button>' : ''}</div>` : ''}
  </section>`;
}

export async function runCoach(summary) {
  const sample = getCaps().sample;
  if (!sample || coach.busy) return;
  coach = { text: '', busy: true, err: '', ctl: new AbortController() };
  paint();
  const prompt = `${RULES}\n\nHere is a student's TMUA revision data (their test is soon):\n\n${summary}\n\nWrite a short coaching note (under 220 words) with three headed parts: **Where your marks are going** (name the 2–3 biggest leaks, with numbers), **Next three sessions** (concrete: which mode, which topic, how many questions), and **One technique** (a specific exam habit tied to their error pattern). Be direct and specific to the data; no generic advice.`;
  try {
    const res = await sample(prompt, { signal: coach.ctl.signal, cache: false, onText: ({ text }) => { coach.text = text; paintText('coach'); } });
    coach.text = res.text;
  } catch (e) {
    coach.text = e?.text || '';
    if (HIDE.has(e?.code)) dropCap('sample');
    else if (e?.code !== 'cancelled') coach.err = ERR[e?.code] || ERR.upstream_error;
  } finally {
    coach.busy = false; coach.ctl = null;
    paint();
  }
}
export function stopCoach() { coach.ctl?.abort(); }
