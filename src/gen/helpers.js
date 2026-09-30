import { Frac, F, gcd } from '../lib/frac.js';

// Build a multiple-choice set. `correct` and each of `wrongs` are
// { key, text, v?, why? }. Duplicate keys are dropped; `fill()` tops up the list.
export function choices(rng, correct, wrongs, { n = 5, sort = false, fill = null } = {}) {
  const seen = new Set([correct.key]);
  const seenText = new Set([correct.text]);
  const picked = [];
  for (const w of wrongs) {
    if (!w || seen.has(w.key) || seenText.has(w.text)) continue;
    seen.add(w.key); seenText.add(w.text); picked.push(w);
    if (picked.length >= n - 1) break;
  }
  let guard = 0;
  while (picked.length < n - 1 && fill && guard++ < 200) {
    const w = fill(rng);
    if (!w || seen.has(w.key) || seenText.has(w.text)) continue;
    seen.add(w.key); seenText.add(w.text); picked.push(w);
  }
  let all = [{ ...correct, ok: true }, ...picked];
  all = sort ? all.sort((a, b) => a.v - b.v) : rng.shuffle(all);
  const distractors = {};
  all.forEach((o, i) => { if (o.why) distractors[i] = o.why; });
  return { options: all.map(o => o.text), answer: all.findIndex(o => o.ok), distractors };
}

// Numeric option from a Frac or number.
export function num(x, why) {
  const f = Frac.of(x);
  return { key: f.key(), text: `$${f.tex()}$`, v: f.value, why };
}

// Nearby-number filler for numeric options.
export const nearFill = (base, spread = 5) => rng => {
  const b = Frac.of(base);
  const delta = rng.nonzero(-spread, spread);
  return num(b.d === 1 ? b.add(delta) : b.add(F(delta, b.d)));
};

// ax^n style polynomial term formatting: terms = [[coef(Frac|number), power], ...]
export function poly(terms, v = 'x') {
  let s = '';
  for (const [c0, p] of terms) {
    const c = Frac.of(c0);
    if (c.n === 0) continue;
    const neg = c.n < 0;
    const abs = neg ? c.neg() : c;
    let body;
    const vp = p === 0 ? '' : p === 1 ? v : `${v}^{${p}}`;
    if (p === 0) body = abs.tex();
    else if (abs.n === 1 && abs.d === 1) body = vp;
    else body = abs.tex() + vp;
    if (!s) s = (neg ? '-' : '') + body;
    else s += (neg ? ' - ' : ' + ') + body;
  }
  return s || '0';
}

// "+ 3" / "- 3" suffix for a constant term.
export const signed = (c, lead = false) => {
  const f = Frac.of(c);
  if (f.n === 0) return '';
  if (lead) return f.tex();
  return f.n < 0 ? ` - ${f.neg().tex()}` : ` + ${f.tex()}`;
};

// Simplify sqrt(n) as a*sqrt(b).
export function surd(n) {
  let a = 1, b = n;
  for (let k = 2; k * k <= b; k++) while (b % (k * k) === 0) { b /= k * k; a *= k; }
  return { a, b };
}
export function surdTex(coef, n) {
  // coef * sqrt(n)
  const { a, b } = surd(n);
  const c = coef * a;
  if (b === 1) return String(c);
  return `${c === 1 ? '' : c === -1 ? '-' : c}\\sqrt{${b}}`;
}

export const binom = (n, k) => {
  if (k < 0 || k > n) return 0;
  let r = 1;
  for (let i = 1; i <= k; i++) r = (r * (n - k + i)) / i;
  return Math.round(r);
};

export { F, Frac, gcd };

// (x - r) factor, printed as just x when r = 0.
export const fac = (r, v = 'x') => (r === 0 ? v : `(${v} ${r > 0 ? '-' : '+'} ${Math.abs(r)})`);
