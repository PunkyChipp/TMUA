// Fuzz every generator: many seeds at every level, checking structural invariants.
import test from 'node:test';
import assert from 'node:assert/strict';
import { GENERATORS, genQuestion } from '../src/gen/index.js';
import { compileExpr } from '../src/render/plot.js';
import katex from 'katex';

// Every maths fragment must parse in KaTeX.
function texOk(s, ctx) {
  const d = s.match(/\$\$([\s\S]+?)\$\$/g) || [];
  for (const m of d) katex.renderToString(m.slice(2, -2), { throwOnError: true, displayMode: true, strict: 'ignore' });
  const rest = s.replace(/\$\$[\s\S]+?\$\$/g, '');
  for (const m of rest.match(/\$([^$\n]+?)\$/g) || []) {
    try { katex.renderToString(m.slice(1, -1), { throwOnError: true, strict: 'ignore' }); }
    catch (e) { throw new Error(`${ctx}: KaTeX ${e.message.split('\n')[0]} in ${m}`); }
  }
}

for (const g of GENERATORS) {
  test(`generator ${g.id}`, () => {
    for (let level = g.levels[0]; level <= g.levels[1]; level++) {
      for (let seed = 1; seed <= 400; seed++) {
        const q = genQuestion(g.id, level, seed * 7919 + level);
        const ctx = `${g.id} L${level} seed ${seed}`;
        assert.ok(q.stem && typeof q.stem === 'string', `${ctx}: stem`);
        assert.ok(Array.isArray(q.options) && q.options.length >= 4 && q.options.length <= 8, `${ctx}: ${q.options?.length} options`);
        assert.ok(Number.isInteger(q.answer) && q.answer >= 0 && q.answer < q.options.length, `${ctx}: answer index ${q.answer}`);
        const texts = q.options.map(o => (typeof o === 'string' ? o : JSON.stringify(o)));
        assert.equal(new Set(texts).size, texts.length, `${ctx}: duplicate options ${texts.join(' | ')}`);
        for (const t of texts) {
          assert.ok(!/undefined|NaN|Infinity|\[object/.test(t), `${ctx}: bad option text ${t}`);
          assert.ok(((t.match(/\$/g) || []).length % 2) === 0, `${ctx}: unbalanced $ in ${t}`);
        }
        for (const t of [q.stem, q.solution, q.insight, ...texts.filter(x => x.startsWith('$') || !x.startsWith('{')), ...Object.values(q.distractors || {})]) texOk(t, ctx);
        for (const field of ['stem', 'solution']) {
          assert.ok(!/undefined|NaN|\[object/.test(q[field]), `${ctx}: bad ${field}: ${q[field]}`);
        }
        for (const o of q.options) if (typeof o === 'object') for (const c of o.plot.curves) compileExpr(c.fn);
        assert.ok(q.solution && q.insight, `${ctx}: solution/insight`);
        for (const k of Object.keys(q.distractors || {})) assert.notEqual(+k, q.answer, `${ctx}: distractor note on the answer`);
      }
    }
  });
}
