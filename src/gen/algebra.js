import { choices, num, nearFill, poly, signed, F, Frac, gcd, fac } from './helpers.js';

const lastDigit = {
  id: 'last-digit', speedOnly: true, topic: 'number', paper: 1, levels: [1, 2], skills: ['powers', 'cycles'],
  name: 'Last digit of a power',
  make(rng, level) {
    const a = rng.pick(level === 1 ? [2, 3, 7] : [3, 7, 8, 13, 17, 27]);
    const n = rng.int(level === 1 ? 20 : 101, level === 1 ? 60 : 999);
    const unit = a % 10;
    const cyc = [];
    let x = unit;
    do { cyc.push(x); x = (x * unit) % 10; } while (x !== unit);
    const ans = cyc[(n - 1) % cyc.length];
    const wrongs = cyc.filter(d => d !== ans).map(d => num(d, 'Right cycle, but check which position in the cycle $n$ lands on: use the remainder of $n$ divided by the cycle length.'));
    const opts = choices(rng, num(ans), [...wrongs, num((ans + 5) % 10)], { n: 5, sort: true, fill: r => num(r.int(0, 9)) });
    return {
      stem: `What is the last digit of $${a}^{${n}}$?`,
      ...opts,
      solution: `Only the last digit of the base matters. Powers of ${unit} end in the repeating cycle ${cyc.join(', ')} (length ${cyc.length}).\n\n$${n} = ${cyc.length}\\times ${Math.floor(n / cyc.length)} + ${n % cyc.length}$, so $${a}^{${n}}$ sits at position ${((n - 1) % cyc.length) + 1} of the cycle, giving last digit **${ans}**.`,
      insight: 'Last digits of powers repeat with period dividing 4: reduce the exponent modulo the cycle length.',
      time: 60 + level * 20,
    };
  },
};

const countMultiples = {
  id: 'count-multiples', topic: 'number', paper: 1, levels: [2, 3], skills: ['inclusion-exclusion', 'counting'],
  name: 'Counting multiples',
  make(rng, level) {
    let a, b;
    do { a = rng.int(2, 9); b = rng.int(3, 12); } while (a === b || b % a === 0 || a % b === 0 || (level === 3 && gcd(a, b) === 1));
    const N = rng.int(100, level === 2 ? 300 : 999);
    const l = (a * b) / gcd(a, b);
    const fa = Math.floor(N / a), fb = Math.floor(N / b), fl = Math.floor(N / l), fab = Math.floor(N / (a * b));
    const neither = rng.chance(0.5);
    const ans = neither ? N - (fa + fb - fl) : fa + fb - fl;
    const w = neither
      ? [num(N - (fa + fb - fab), `You removed multiples of $${a * b}$, but the overlap is multiples of lcm$(${a},${b}) = ${l}$.`),
         num(N - fa - fb, 'Numbers divisible by both were subtracted twice: add the overlap back.'),
         num(fa + fb - fl, 'That counts the numbers divisible by at least one. The question asks for neither.')]
      : [num(fa + fb - fab, `The overlap is multiples of lcm$(${a},${b}) = ${l}$, not of $${a}\\times${b}$.`),
         num(fa + fb, 'Numbers divisible by both have been counted twice.'),
         num(N - (fa + fb - fl), 'That is the count of numbers divisible by neither.')];
    const opts = choices(rng, num(ans), w, { n: 5, sort: true, fill: nearFill(ans, 6) });
    return {
      stem: `How many integers from $1$ to $${N}$ inclusive are divisible by ${neither ? '**neither**' : 'at least one of'} $${a}$ ${neither ? 'nor' : 'and'} $${b}$?`,
      ...opts,
      solution: `Multiples of ${a}: $\\lfloor ${N}/${a}\\rfloor = ${fa}$. Multiples of ${b}: $\\lfloor ${N}/${b}\\rfloor = ${fb}$.\n\nMultiples of both are multiples of $\\operatorname{lcm}(${a},${b}) = ${l}$: $\\lfloor ${N}/${l}\\rfloor = ${fl}$.\n\nAt least one: $${fa} + ${fb} - ${fl} = ${fa + fb - fl}$.${neither ? `\n\nNeither: $${N} - ${fa + fb - fl} = ${ans}$.` : ''}`,
      insight: 'Inclusion–exclusion: |A ∪ B| = |A| + |B| − |A ∩ B|, and "divisible by both" means divisible by the lcm.',
      time: 120,
    };
  },
};

const discriminant = {
  id: 'disc-param', topic: 'alg', paper: 1, levels: [2, 4], skills: ['discriminant', 'parameters', 'inequalities'],
  name: 'Discriminant with a parameter',
  make(rng, level) {
    // x^2 + 2kx + (a k + b) = 0 has disc/4 = k^2 - a k - b = (k - r1)(k - r2)
    let r1, r2;
    do { r1 = rng.int(-6, 4); r2 = rng.int(r1 + 1, 7); } while (r1 === 0 && r2 === 0);
    const a = r1 + r2, b = -r1 * r2;
    const kind = level <= 2 ? 'two' : rng.pick(['two', 'none', 'real']);
    const cterm = poly([[a, 1], [b, 0]], 'k');
    const eq = a === 0 ? `x^2 + 2kx ${signed(b)} = 0` : `x^2 + 2kx + (${cterm}) = 0`;
    const out = `$k < ${r1}$ or $k > ${r2}$`;
    const outE = `$k \\le ${r1}$ or $k \\ge ${r2}$`;
    const inn = `$${r1} < k < ${r2}$`;
    const innE = `$${r1} \\le k \\le ${r2}$`;
    const map = { two: out, none: inn, real: outE };
    const phrase = { two: 'two distinct real roots', none: 'no real roots', real: 'at least one real root' }[kind];
    const correct = { key: kind, text: map[kind] };
    const pool = [
      { key: 'two', text: out, why: 'That is the condition for two distinct roots: strict inequality, outside the roots.' },
      { key: 'none', text: inn, why: 'Between the roots the discriminant is negative, so that gives no real roots.' },
      { key: 'real', text: outE, why: 'Including equality allows a repeated root; check whether the question wants distinct roots.' },
      { key: 'innE', text: innE, why: 'Check the direction: which side of the roots makes the discriminant positive?' },
      { key: 'neg', text: `$k < ${-r2}$ or $k > ${-r1}$`, why: 'Sign slip when factorising the discriminant.' },
      { key: 'half', text: `$k > ${r2}$`, why: 'A quadratic inequality $(k-p)(k-q) > 0$ has two pieces of solution; this misses one.' },
    ].filter(o => o.key !== kind);
    const opts = choices(rng, correct, pool, { n: 5 });
    return {
      stem: `Find the complete set of values of $k$ for which the equation $$${eq}$$ has ${phrase}.`,
      ...opts,
      solution: `The discriminant is $(2k)^2 - 4(${cterm}) = 4\\left(${poly([[1, 2], [-a, 1], [-b, 0]], 'k')}\\right) = 4${fac(r1, 'k')}${fac(r2, 'k')}$.\n\n- two distinct real roots: $\\Delta > 0 \\iff k < ${r1}$ or $k > ${r2}$\n- equal roots: $k = ${r1}$ or $k = ${r2}$\n- no real roots: $${r1} < k < ${r2}$\n\nSo the answer is ${map[kind]}.`,
      insight: 'Turn the root condition into an inequality in the discriminant, factorise, then sketch the parabola in k.',
      time: 150,
    };
  },
};

const remainder = {
  id: 'remainder-thm', speedOnly: true, topic: 'alg', paper: 1, levels: [1, 3], skills: ['remainder theorem', 'polynomials'],
  name: 'Remainder theorem',
  make(rng, level) {
    const a = rng.int(-4, 4), b = rng.int(-6, 6), c = rng.int(-9, 9);
    const r = rng.nonzero(-3, 3);
    const lead = level >= 3 ? rng.pick([2, 3]) : 1;
    const p = x => lead * x ** 3 + a * x * x + b * x + c;
    const ans = p(r);
    const div = r > 0 ? `x - ${r}` : `x + ${-r}`;
    const w = [
      num(p(-r), `That is $p(${-r})$. Dividing by $(${div})$ means substituting $x = ${r}$.`),
      num(p(r) - 2 * c, 'Sign slip on the constant term.'),
      num(lead * r ** 3 + a * r * r + b * r, 'You dropped the constant term.'),
    ];
    const opts = choices(rng, num(ans), w, { n: 5, sort: true, fill: nearFill(ans, 8) });
    const P = poly([[lead, 3], [a, 2], [b, 1], [c, 0]]);
    return {
      stem: `What is the remainder when $p(x) = ${P}$ is divided by $(${div})$?`,
      ...opts,
      solution: `By the remainder theorem the remainder is $p(${r})$:\n\n$$p(${r}) = ${[[lead, 3], [a, 2], [b, 1], [c, 0]].filter(([co]) => co).map(([co, k], j) => `${j ? (co < 0 ? ' - ' : ' + ') : co < 0 ? '-' : ''}${Math.abs(co) === 1 && k ? '' : Math.abs(co)}${k ? `(${r})${k > 1 ? `^${k}` : ''}` : ''}`).join('')} = ${ans}.$$`,
      insight: 'Remainder on division by (x − r) is p(r); no long division needed.',
      time: 60 + level * 15,
    };
  },
};

const factorK = {
  id: 'factor-k', speedOnly: true, topic: 'alg', paper: 1, levels: [2, 3], skills: ['factor theorem', 'polynomials'],
  name: 'Factor theorem with an unknown',
  make(rng, level) {
    const r = rng.nonzero(-3, 3);
    const k = rng.nonzero(-6, 6);
    const b = rng.int(-8, 8);
    const c = -(r ** 3 + k * r * r + b * r);
    const div = r > 0 ? `x - ${r}` : `x + ${-r}`;
    const w = [
      num(F(-(((-r) ** 3) + b * (-r) + c), r * r), `You substituted $x = ${-r}$. A factor $(${div})$ means $p(${r}) = 0$.`),
      num(-k, 'Sign slip when rearranging for $k$.'),
      num(F(-(r ** 3 + b * r + c), r), `$k$ multiplies $x^2$, so divide by $${r}^2 = ${r * r}$, not by $${r}$.`),
    ];
    const opts = choices(rng, num(k), w, { n: 5, sort: true, fill: nearFill(k, 5) });
    return {
      stem: `Given that $(${div})$ is a factor of $x^3 + kx^2 ${b ? (b > 0 ? '+ ' + b : '- ' + -b) + 'x' : ''} ${signed(c)}$, find $k$.`,
      ...opts,
      solution: `Factor theorem: $p(${r}) = 0$.\n\n$$(${r})^3 + k(${r})^2 ${signed(b)}(${r}) ${signed(c)} = 0 \\implies ${poly([[r * r, 1], [r ** 3 + b * r + c, 0]], 'k')} = 0 \\implies k = ${k}.$$`,
      insight: '(x − r) is a factor exactly when p(r) = 0.',
      time: 90,
    };
  },
};

const indices = {
  id: 'indices-eval', speedOnly: true, topic: 'alg', paper: 1, levels: [1, 3], skills: ['indices', 'fractional powers'],
  name: 'Evaluating indices',
  make(rng, level) {
    // Base 2 or 3 powers with fractional exponents.
    const base = rng.pick([2, 3]);
    const pows = base === 2 ? [2, 3, 4, 5] : [2, 3, 4];
    let terms, E;
    let guard = 0;
    do {
      const count = level === 1 ? 2 : 3;
      terms = [];
      for (let i = 0; i < count; i++) {
        const p = rng.pick(pows);
        const den = rng.pick([1, 2, 3, p]);
        const numr = rng.nonzero(-3, 3);
        terms.push({ n: base ** p, p, e: F(numr, den), inv: level >= 3 && i === count - 1 && rng.chance(0.5) });
      }
      E = terms.reduce((acc, t) => acc.add(t.e.mul(t.p).mul(t.inv ? -1 : 1)), F(0));
    } while ((!E.isInt() || Math.abs(E.value) > 7 || terms.some(t => !t.e.mul(t.p).isInt())) && guard++ < 500);
    const texTerm = t => {
      const ex = t.e.isInt() ? String(t.e.n) : `${t.e.n < 0 ? '-' : ''}\\frac{${Math.abs(t.e.n)}}{${t.e.d}}`;
      return `${t.n}^{${ex}}`;
    };
    const top = terms.filter(t => !t.inv).map(texTerm).join(' \\times ');
    const bot = terms.filter(t => t.inv).map(texTerm);
    const expr = bot.length ? `\\dfrac{${top}}{${bot.join('\\times')}}` : top;
    const val = e => (e >= 0 ? F(base ** e) : F(1, base ** -e));
    const e = E.value;
    const w = [num(val(-e), 'Sign error on one of the exponents.'), num(val(e + 1)), num(val(e - 1)), num(val(e + 2))];
    const opts = choices(rng, num(val(e)), w, { n: 5, sort: true });
    const parts = terms.map(t => `$${t.n}^{${t.e.tex()}} = ${base}^{${t.e.mul(t.p).tex()}}$`).join(', ');
    return {
      stem: `Evaluate $$${expr}$$`,
      ...opts,
      solution: `Write everything as a power of ${base}: ${parts}.\n\nAdd exponents${bot.length ? ' (subtracting for the denominator)' : ''}: total exponent $= ${e}$, so the value is $${base}^{${e}} = ${val(e).tex()}$.`,
      insight: 'Rewrite every number as a power of the same prime, then just add and subtract exponents.',
      time: 60 + 25 * level,
    };
  },
};

const rootsSym = {
  id: 'roots-symmetric', topic: 'alg', paper: 1, levels: [3, 4], skills: ['sum and product of roots', 'quadratics'],
  name: 'Symmetric functions of roots',
  make(rng, level) {
    const a = rng.pick([1, 2, 3]);
    let b = rng.nonzero(-7, 7), c = rng.nonzero(-6, 6);
    const S = F(-b, a), P = F(c, a);
    const kind = rng.pick(level >= 4 ? ['sq', 'recip', 'recipsq', 'diffsq'] : ['sq', 'recip']);
    const calc = {
      sq: S.mul(S).sub(P.mul(2)),
      recip: S.div(P),
      recipsq: S.mul(S).sub(P.mul(2)).div(P.mul(P)),
      diffsq: S.mul(S).sub(P.mul(4)),
    };
    const label = {
      sq: '\\alpha^2 + \\beta^2', recip: '\\dfrac{1}{\\alpha} + \\dfrac{1}{\\beta}',
      recipsq: '\\dfrac{1}{\\alpha^2} + \\dfrac{1}{\\beta^2}', diffsq: '(\\alpha - \\beta)^2',
    };
    const ans = calc[kind];
    const w = [
      num(kind === 'sq' ? S.mul(S).add(P.mul(2)) : kind === 'recip' ? P.div(S) : kind === 'diffsq' ? S.mul(S).sub(P.mul(2)) : S.mul(S).add(P.mul(2)).div(P.mul(P)), 'Check the identity: e.g. α² + β² = (α + β)² − 2αβ.'),
      num(kind === 'sq' ? F(b * b, a * a).sub(P.mul(2)).neg() : ans.neg(), 'Sign slip: α + β = −b/a.'),
      num(kind === 'recip' ? F(b, c) : F(b * b - 2 * c)),
    ];
    const opts = choices(rng, num(ans), w, { n: 5, sort: true, fill: nearFill(ans, 4) });
    const Q = poly([[a, 2], [b, 1], [c, 0]]);
    const idText = {
      sq: `$\\alpha^2+\\beta^2 = (\\alpha+\\beta)^2 - 2\\alpha\\beta = (${S.tex()})^2 - 2(${P.tex()}) = ${ans.tex()}$`,
      recip: `$\\dfrac1\\alpha + \\dfrac1\\beta = \\dfrac{\\alpha+\\beta}{\\alpha\\beta} = \\dfrac{${S.tex()}}{${P.tex()}} = ${ans.tex()}$`,
      recipsq: `$\\dfrac1{\\alpha^2}+\\dfrac1{\\beta^2} = \\dfrac{\\alpha^2+\\beta^2}{(\\alpha\\beta)^2} = \\dfrac{${calc.sq.tex()}}{${P.mul(P).tex()}} = ${ans.tex()}$`,
      diffsq: `$(\\alpha-\\beta)^2 = (\\alpha+\\beta)^2 - 4\\alpha\\beta = (${S.tex()})^2 - 4(${P.tex()}) = ${ans.tex()}$`,
    }[kind];
    return {
      stem: `The roots of $${Q} = 0$ are $\\alpha$ and $\\beta$. What is the value of $${label[kind]}$?`,
      ...opts,
      solution: `From the coefficients: $\\alpha+\\beta = -\\dfrac{b}{a} = ${S.tex()}$ and $\\alpha\\beta = \\dfrac{c}{a} = ${P.tex()}$.\n\n${idText}.\n\n(The roots may not be real; the algebra still holds.)`,
      insight: 'Never find the roots: express the target in terms of α + β and αβ.',
      time: 150,
    };
  },
};

const quadIneq = {
  id: 'quad-ineq', speedOnly: true, topic: 'alg', paper: 1, levels: [1, 3], skills: ['quadratic inequalities'],
  name: 'Quadratic inequalities',
  make(rng, level) {
    let r1 = rng.int(-6, 5), r2 = rng.int(r1 + 1, 8);
    const neg = level >= 3 && rng.chance(0.5); // -(x-r1)(x-r2)
    const lt = rng.chance(0.5);
    const b = -(r1 + r2), c = r1 * r2;
    const Q = neg ? poly([[-1, 2], [-b, 1], [-c, 0]]) : poly([[1, 2], [b, 1], [c, 0]]);
    // Region where (x - r1)(x - r2) is negative = between.
    const between = neg ? !lt : lt;
    const inn = `$${r1} < x < ${r2}$`, out = `$x < ${r1}$ or $x > ${r2}$`;
    const correct = between ? { key: 'in', text: inn } : { key: 'out', text: out };
    const pool = [
      { key: 'in', text: inn, why: 'Between the roots the parabola is on the other side of the axis; recheck the sign.' },
      { key: 'out', text: out, why: 'Outside the roots: check the sign of the $x^2$ coefficient.' },
      { key: 'sw', text: `$${-r2} < x < ${-r1}$`, why: 'Roots have the wrong signs: $(x-a)(x-b)$ vanishes at $x = a$ and $x = b$.' },
      { key: 'sw2', text: `$x < ${-r2}$ or $x > ${-r1}$`, why: 'Roots have the wrong signs.' },
      { key: 'one', text: `$x > ${r2}$`, why: 'Only half of the solution set.' },
      { key: 'le', text: `$${r1} \\le x \\le ${r2}$`, why: 'The inequality is strict, so the roots themselves are excluded.' },
      { key: 'lo', text: `$x < ${r1}$`, why: 'Only half of the solution set.' },
      { key: 'ge', text: `$x \\le ${r1}$ or $x \\ge ${r2}$`, why: 'The inequality is strict, so the roots themselves are excluded.' },
    ];
    const opts = choices(rng, correct, pool, { n: 5 });
    return {
      stem: `Find the set of values of $x$ for which $${Q} ${lt ? '<' : '>'} 0$.`,
      ...opts,
      solution: `${neg ? `Multiply by $-1$ and flip the inequality: $x^2 ${signed(b)}x ${signed(c)} ${lt ? '>' : '<'} 0$.\n\n` : ''}Factorise: $${fac(r1)}${fac(r2)}$, roots $${r1}$ and $${r2}$.\n\nThe upward parabola is negative between its roots and positive outside, so the answer is ${correct.text}.`,
      insight: 'Find the roots, sketch the parabola, and read off where it is above or below the axis.',
      time: 60 + level * 20,
    };
  },
};

export default [lastDigit, countMultiples, discriminant, remainder, factorK, indices, rootsSym, quadIneq];
