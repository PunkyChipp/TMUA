// Tiny SVG function plotter for graph questions. Expressions are compiled from a
// whitelisted grammar (numbers, x, operators, a few functions) — nothing else runs.
const FUNCS = {
  sin: Math.sin, cos: Math.cos, tan: Math.tan, exp: Math.exp, ln: Math.log, log: Math.log,
  log10: Math.log10, sqrt: Math.sqrt, abs: Math.abs, floor: Math.floor,
};
const TOKEN = /\s*(\d+\.?\d*|\.\d+|[a-z]+[0-9]*|\*\*|[-+*/^(),])/y;

// Recursive-descent parser → closure. Grammar:
//   expr := term (('+'|'-') term)*      term := unary (('*'|'/') unary)*
//   unary := ('-'|'+') unary | power    power := atom ('^' unary)?
//   atom := number | x | pi | e | fn '(' expr ')' | '(' expr ')'
function compile(expr) {
  const src = String(expr).trim();
  const toks = [];
  let pos = 0;
  while (pos < src.length) {
    TOKEN.lastIndex = pos;
    const m = TOKEN.exec(src);
    if (!m) throw new Error(`Bad plot expression: ${expr}`);
    toks.push(m[1] === '**' ? '^' : m[1]);
    pos = TOKEN.lastIndex;
    while (pos < src.length && src[pos] === ' ') pos++;
  }
  let i = 0;
  const peek = () => toks[i];
  const eat = t => { if (toks[i] !== t) throw new Error(`Expected ${t} in ${expr}`); i++; };
  const parseExpr = () => {
    let f = parseTerm();
    while (peek() === '+' || peek() === '-') {
      const op = toks[i++], a = f, b = parseTerm();
      f = op === '+' ? x => a(x) + b(x) : x => a(x) - b(x);
    }
    return f;
  };
  const parseTerm = () => {
    let f = parseUnary();
    while (peek() === '*' || peek() === '/') {
      const op = toks[i++], a = f, b = parseUnary();
      f = op === '*' ? x => a(x) * b(x) : x => a(x) / b(x);
    }
    return f;
  };
  const parseUnary = () => {
    if (peek() === '-') { i++; const a = parseUnary(); return x => -a(x); }
    if (peek() === '+') { i++; return parseUnary(); }
    return parsePower();
  };
  const parsePower = () => {
    const a = parseAtom();
    if (peek() === '^') { i++; const b = parseUnary(); return x => Math.pow(a(x), b(x)); }
    return a;
  };
  const parseAtom = () => {
    const t = toks[i++];
    if (t === undefined) throw new Error(`Unexpected end of ${expr}`);
    if (/^[\d.]/.test(t)) { const v = parseFloat(t); return () => v; }
    if (t === '(') { const f = parseExpr(); eat(')'); return f; }
    if (t === 'x') return x => x;
    if (t === 'pi') return () => Math.PI;
    if (t === 'e') return () => Math.E;
    if (FUNCS[t]) { const fn = FUNCS[t]; eat('('); const a = parseExpr(); eat(')'); return x => fn(a(x)); }
    throw new Error(`Unknown name "${t}" in plot expression ${expr}`);
  };
  const f = parseExpr();
  if (i !== toks.length) throw new Error(`Unexpected "${toks[i]}" in ${expr}`);
  return f;
}

let uidc = 0;

export function plotSVG(spec, { width = 280, height = 210, compact = false } = {}) {
  const [x0, x1] = spec.x || [-4, 4];
  const [y0, y1] = spec.y || [-4, 4];
  const pad = 6;
  const W = width, H = height;
  const sx = x => pad + ((x - x0) / (x1 - x0)) * (W - 2 * pad);
  const sy = y => H - pad - ((y - y0) / (y1 - y0)) * (H - 2 * pad);
  const id = `pc${++uidc}`;
  const parts = [];
  parts.push(`<defs><clipPath id="${id}"><rect x="${pad}" y="${pad}" width="${W - 2 * pad}" height="${H - 2 * pad}"/></clipPath></defs>`);
  // Axes.
  if (y0 <= 0 && y1 >= 0) parts.push(`<line class="pl-axis" x1="${pad}" x2="${W - pad}" y1="${sy(0)}" y2="${sy(0)}"/>`);
  if (x0 <= 0 && x1 >= 0) parts.push(`<line class="pl-axis" y1="${pad}" y2="${H - pad}" x1="${sx(0)}" x2="${sx(0)}"/>`);
  if (spec.ticks) {
    for (let i = Math.ceil(x0); i <= Math.floor(x1); i++) if (i) parts.push(`<line class="pl-axis" x1="${sx(i)}" x2="${sx(i)}" y1="${sy(0) - 3}" y2="${sy(0) + 3}"/>`);
    for (let j = Math.ceil(y0); j <= Math.floor(y1); j++) if (j) parts.push(`<line class="pl-axis" y1="${sy(j)}" y2="${sy(j)}" x1="${sx(0) - 3}" x2="${sx(0) + 3}"/>`);
  }
  for (const v of spec.vlines || []) parts.push(`<line class="pl-asym" x1="${sx(v)}" x2="${sx(v)}" y1="${pad}" y2="${H - pad}"/>`);
  for (const h of spec.hlines || []) parts.push(`<line class="pl-asym" y1="${sy(h)}" y2="${sy(h)}" x1="${pad}" x2="${W - pad}"/>`);
  if (!compact) {
    parts.push(`<text class="pl-lab" x="${W - pad - 2}" y="${Math.min(H - pad - 3, Math.max(12, sy(0) - 4))}" text-anchor="end">x</text>`);
    parts.push(`<text class="pl-lab" x="${Math.min(W - 12, Math.max(pad + 4, sx(0) + 5))}" y="${pad + 10}">y</text>`);
  }
  for (const c of spec.curves || []) {
    let f;
    try { f = compile(c.fn); } catch (e) { continue; }
    const [a, b] = c.domain || [x0, x1];
    const N = 400;
    let d = '', pen = false, prevY = null;
    for (let i = 0; i <= N; i++) {
      const x = a + ((b - a) * i) / N;
      let y;
      try { y = f(x); } catch (e) { y = NaN; }
      const ok = Number.isFinite(y) && Math.abs(y) < 1e6;
      // Break the path across asymptotes (big jumps).
      if (ok && prevY !== null && Math.abs(y - prevY) > (y1 - y0) * 2) pen = false;
      if (ok) {
        const Y = Math.max(-H, Math.min(2 * H, sy(y)));
        d += `${pen ? 'L' : 'M'}${sx(x).toFixed(1)},${Y.toFixed(1)}`;
        pen = true; prevY = y;
      } else { pen = false; prevY = null; }
    }
    parts.push(`<path class="pl-curve${c.dash ? ' pl-dash' : ''}" clip-path="url(#${id})" d="${d}"/>`);
  }
  for (const [px, py] of spec.points || []) parts.push(`<circle class="pl-pt" cx="${sx(px)}" cy="${sy(py)}" r="3"/>`);
  for (const l of spec.labels || []) {
    const [lx, ly] = l.at;
    parts.push(`<text class="pl-lab" x="${sx(lx) + 5}" y="${sy(ly) - 5}">${String(l.text).replace(/[<&>]/g, '')}</text>`);
  }
  return `<svg class="plot" viewBox="0 0 ${W} ${H}" role="img" aria-label="graph">${parts.join('')}</svg>`;
}

export { compile as compileExpr };
