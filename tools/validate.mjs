// Validates content/: schema, KaTeX parsing, plot expressions, answer balance.
//   node tools/validate.mjs            (all topics)
//   node tools/validate.mjs alg logic  (selected topics)
import fs from 'node:fs';
import path from 'node:path';
import katex from 'katex';
import { compileExpr } from '../src/render/plot.js';
import { TOPIC } from '../src/data/topics.js';

const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const only = process.argv.slice(2);
const errors = [], warnings = [];
const err = (id, m) => errors.push(`${id}: ${m}`);
const warn = (id, m) => warnings.push(`${id}: ${m}`);

function checkMath(id, where, s) {
  if (typeof s !== 'string') return;
  const stripped = s.replace(/\\\$/g, '');
  const dd = stripped.match(/\$\$([\s\S]+?)\$\$/g) || [];
  for (const m of dd) tryTex(id, where, m.slice(2, -2), true);
  const rest = stripped.replace(/\$\$[\s\S]+?\$\$/g, '');
  const singles = (rest.match(/\$/g) || []).length;
  if (singles % 2) err(id, `${where}: unbalanced $`);
  for (const m of rest.match(/\$([^$\n]+?)\$/g) || []) tryTex(id, where, m.slice(1, -1), false);
}
function tryTex(id, where, tex, display) {
  try { katex.renderToString(tex, { displayMode: display, throwOnError: true, strict: 'ignore' }); }
  catch (e) { err(id, `${where}: KaTeX: ${e.message.split('\n')[0]} in "${tex.slice(0, 60)}"`); }
}
function checkPlot(id, where, p) {
  if (!p || !p.curves) return err(id, `${where}: plot without curves`);
  for (const c of p.curves) { try { compileExpr(c.fn)(0.5); } catch (e) { err(id, `${where}: ${e.message}`); } }
}

const qdir = path.join(root, 'content/questions');
const ids = new Set();
const pos = {};
const families = {};
let count = 0;
for (const f of fs.readdirSync(qdir).filter(f => f.endsWith('.json')).sort()) {
  const topic = f.replace('.json', '');
  if (only.length && !only.includes(topic)) continue;
  let arr;
  try { arr = JSON.parse(fs.readFileSync(path.join(qdir, f), 'utf8')); } catch (e) { err(f, `invalid JSON: ${e.message}`); continue; }
  for (const q of arr) {
    count++;
    const id = q.id || `${f}#?`;
    if (ids.has(id)) err(id, 'duplicate id');
    ids.add(id);
    if (!TOPIC[q.topic]) err(id, `unknown topic ${q.topic}`);
    if (q.topic !== topic) err(id, `topic ${q.topic} in ${f}`);
    if (![1, 2].includes(q.paper)) err(id, 'paper must be 1 or 2');
    if (!(q.difficulty >= 1 && q.difficulty <= 5)) err(id, 'difficulty 1–5');
    if (!Array.isArray(q.options) || q.options.length < 4 || q.options.length > 8) err(id, 'needs 4–8 options');
    if (!Number.isInteger(q.answer) || q.answer < 0 || q.answer >= (q.options?.length || 0)) err(id, 'answer index out of range');
    if (!q.solution || q.solution.length < 40) err(id, 'solution missing or very short');
    if (!q.insight) warn(id, 'no insight');
    const texts = (q.options || []).map(o => (typeof o === 'string' ? o.trim() : JSON.stringify(o)));
    if (new Set(texts).size !== texts.length) err(id, 'duplicate options');
    for (const k of Object.keys(q.distractors || {})) {
      if (+k === q.answer) err(id, 'distractor note on the correct option');
      if (+k >= texts.length) err(id, `distractor key ${k} out of range`);
    }
    checkMath(id, 'stem', q.stem);
    checkMath(id, 'solution', q.solution);
    checkMath(id, 'insight', q.insight);
    for (const v of Object.values(q.distractors || {})) checkMath(id, 'distractor', v);
    (q.options || []).forEach((o, i) => (typeof o === 'string' ? checkMath(id, `option ${i}`, o) : checkPlot(id, `option ${i}`, o.plot)));
    if (q.figure?.plot) checkPlot(id, 'figure', q.figure.plot);
    if (q.figure?.svg && !/viewBox/.test(q.figure.svg)) warn(id, 'svg figure without viewBox');
    (pos[topic] ||= []).push(q.answer);
    // 2026 readiness rules.
    if (q.difficulty < 2) err(id, 'difficulty 1 is below TMUA level');
    if (!q.family) warn(id, 'no twin family');
    else (families[q.family] ||= []).push(q);
    const visible = [q.stem, ...(q.options || []).filter(o => typeof o === 'string')].join(' ');
    if (['logic', 'proof', 'errors'].includes(q.topic)) {
      if (/[∧∨¬∀∃]|\\(land|lor|neg|lnot|forall|exists|wedge|vee)\b/.test(visible)) err(id, 'symbolic logic notation in stem/options (spec: words only)');
      if (q.topic === 'logic' && /⇒|⟹|⇔|\\(Rightarrow|implies|iff|Leftrightarrow)\b/.test(visible)) warn(id, 'implication symbol in a logic stem/options');
      if (/truth table/i.test(visible)) err(id, 'formal truth tables are not examined');
    }
    if (/change of base/i.test(q.stem + q.solution)) err(id, 'uses the change of base formula (not examined)');
    const roman = /\b(I{1,3}|IV)\b|\((i{1,3}|iv)\)/.test(q.stem);
    if ((q.options || []).length > 5 && !roman && !q.options.some(o => typeof o === 'object')) warn(id, `${q.options.length} options without a statement list (house rule: 5)`);
  }
}
for (const [fam, qs] of Object.entries(families)) {
  if (qs.length < 2) warn(fam, 'family has no twin');
  if (qs.length >= 2 && new Set(qs.map(q => q.answer)).size === 1) warn(fam, 'twins share the same answer letter');
  if (new Set(qs.map(q => q.topic)).size > 1) err(fam, 'twins in different topics');
}
const ndir = path.join(root, 'content/notes');
for (const f of fs.readdirSync(ndir).filter(f => f.endsWith('.md'))) {
  if (only.length && !only.includes(f.replace('.md', ''))) continue;
  checkMath(f, 'note', fs.readFileSync(path.join(ndir, f), 'utf8'));
}
for (const [t, arr] of Object.entries(pos)) {
  const c = {};
  for (const a of arr) c[a] = (c[a] || 0) + 1;
  const top = Math.max(...Object.values(c));
  if (top / arr.length > 0.4) warn(t, `answer position skew: ${JSON.stringify(c)}`);
}
for (const w of warnings) console.log('warn ', w);
for (const e of errors) console.log('ERROR', e);
console.log(`${count} questions checked, ${errors.length} errors, ${warnings.length} warnings`);
process.exit(errors.length ? 1 : 0);
