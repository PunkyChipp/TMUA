import { choices, num, nearFill, poly, signed, F, Frac, fac } from './helpers.js';

// Polynomial helpers: p = array of [coef, power] with integer powers (can be negative).
const evalP = (p, x) => p.reduce((s, [c, k]) => s.add(Frac.of(c).mul(pow(x, k))), F(0));
const pow = (x, k) => { let r = F(1); const b = Frac.of(x); for (let i = 0; i < Math.abs(k); i++) r = r.mul(b); return k < 0 ? F(1).div(r) : r; };
const deriv = p => p.filter(([c, k]) => k !== 0).map(([c, k]) => [Frac.of(c).mul(k), k - 1]);
const antider = p => p.map(([c, k]) => [Frac.of(c).div(k + 1), k + 1]);

const ptex = p => {
  // Show negative powers as fractions: c/x^k.
  let s = '';
  for (const [c0, k] of p) {
    const c = Frac.of(c0);
    if (c.n === 0) continue;
    const neg = c.n < 0, a = neg ? c.neg() : c;
    let body;
    if (k >= 0) body = poly([[a, k]]);
    else body = `\\dfrac{${a.tex()}}{x${k === -1 ? '' : `^{${-k}}`}}`;
    s += s ? (neg ? ' - ' : ' + ') + body : (neg ? '-' : '') + body;
  }
  return s;
};

const gradientAt = {
  id: 'gradient-at', topic: 'diff', paper: 1, levels: [1, 3], skills: ['differentiation', 'negative powers'],
  name: 'Gradient at a point',
  make(rng, level) {
    const p = [[rng.nonzero(-3, 4), rng.int(2, 3)], [rng.int(-6, 6), 1]];
    if (level >= 2) p.push([rng.nonzero(-8, 8), rng.pick([-1, -2])]);
    else p.push([rng.int(-9, 9), 0]);
    const x = rng.pick(level >= 2 ? [1, 2, -1, -2] : [1, 2, 3, -1, -2]);
    const d = deriv(p);
    const ans = evalP(d, F(x));
    const neg = p.find(([, k]) => k < 0);
    const wrongD = d.map(([c, k]) => (k < -1 ? [Frac.of(c).neg(), k] : [c, k]));
    const w = [
      neg ? num(evalP(wrongD, F(x)), 'Differentiating $x^{-n}$ gives $-nx^{-n-1}$: watch the sign.') : null,
      num(evalP(p, F(x)), 'That is the $y$-value, not the gradient.'),
      neg ? num(evalP(d.filter(([, k]) => k >= 0), F(x)), 'Rewrite $\\frac{a}{x^n}$ as $ax^{-n}$ and differentiate it too.') : null,
      num(evalP(d, F(-x)), 'Substitute the given value of $x$.'),
    ];
    const opts = choices(rng, num(ans), w, { n: 5, sort: true, fill: nearFill(ans, 6) });
    return {
      stem: `The curve $C$ has equation $y = ${ptex(p)}$. What is the gradient of $C$ at the point where $x = ${x}$?`,
      ...opts,
      solution: `$$\\frac{dy}{dx} = ${ptex(d)}.$$ At $x = ${x}$: $\\dfrac{dy}{dx} = ${ans.tex()}$.`,
      insight: 'Write every term as a power of x before differentiating.',
      time: 60 + level * 20,
    };
  },
};

const tangentIntercept = {
  id: 'tangent-intercept', topic: 'diff', paper: 1, levels: [2, 3], skills: ['tangents', 'normals'],
  name: 'Tangent or normal meets the axis',
  make(rng, level) {
    const p = [[rng.nonzero(-2, 2), 3], [rng.int(-4, 4), 2], [rng.int(-5, 5), 1], [rng.int(-6, 6), 0]];
    const t = rng.nonzero(-2, 2);
    const y0 = evalP(p, F(t)), m = evalP(deriv(p), F(t));
    const normal = level >= 3 && m.n !== 0 && rng.chance(0.5);
    const g = normal ? F(-1).div(m) : m;
    const ans = y0.sub(g.mul(t));
    const w = [
      num(y0.add(g.mul(t)), 'Sign slip: $c = y_1 - m x_1$.'),
      normal ? num(y0.sub(m.mul(t)), 'That is the tangent. The normal has gradient $-1/m$.') : (m.n !== 0 ? num(y0.sub(F(-1).div(m).mul(t)), 'That is the normal, not the tangent.') : null),
      num(g, 'That is the gradient.'),
      num(y0, 'That is the $y$-coordinate of the point of contact.'),
    ];
    const opts = choices(rng, num(ans), w, { n: 5, sort: true, fill: nearFill(ans, 5) });
    return {
      stem: `The ${normal ? 'normal' : 'tangent'} to the curve $y = ${ptex(p)}$ at the point where $x = ${t}$ meets the $y$-axis at $(0, c)$. What is $c$?`,
      ...opts,
      solution: `At $x = ${t}$: $y = ${y0.tex()}$ and $\\dfrac{dy}{dx} = ${ptex(deriv(p))} = ${m.tex()}$.${normal ? `\n\nThe normal has gradient $-1/(${m.tex()}) = ${g.tex()}$.` : ''}\n\nLine: $y - (${y0.tex()}) = ${g.tex()}(x - (${t}))$. At $x = 0$: $c = ${y0.tex()} - (${g.tex()})(${t}) = ${ans.tex()}$.`,
      insight: 'Tangent: gradient f′(a). Normal: −1/f′(a). y-intercept: f(a) − m·a.',
      time: 120,
    };
  },
};

const stationary = {
  id: 'cubic-stationary', topic: 'diff', paper: 1, levels: [2, 4], skills: ['stationary points', 'increasing/decreasing'],
  name: 'Stationary points of a cubic',
  make(rng, level) {
    // f'(x) = 3a(x - p)(x - q) with p + q even so coefficients are integers.
    let p, q;
    do { p = rng.int(-4, 3); q = rng.int(p + 1, 5); } while ((p + q) % 2 !== 0);
    const a = level >= 3 ? rng.pick([1, -1]) : 1;
    const f = [[a, 3], [F(-3 * a * (p + q), 2), 2], [3 * a * p * q, 1], [rng.int(-5, 5), 0]];
    const kind = level >= 4 ? 'dec' : rng.pick(['max', 'min']);
    let correct, w;
    if (kind === 'dec') {
      // decreasing where f' < 0
      const between = a > 0;
      const inn = `$${p} < x < ${q}$`, out = `$x < ${p}$ or $x > ${q}$`;
      correct = { key: between ? 'in' : 'out', text: between ? inn : out };
      w = [
        { key: between ? 'out' : 'in', text: between ? out : inn, why: 'That is where the function is increasing.' },
        { key: 'n', text: `$${-q} < x < ${-p}$`, why: 'The stationary points are the roots of $f\'(x)$; check the signs.' },
        { key: 'm', text: `$x < ${(p + q) / 2}$`, why: 'A cubic is not monotonic either side of its point of inflection.' },
        { key: 'z', text: `$${Math.min(p, 0)} < x < ${Math.max(q, 0)}$` },
        { key: 'lq', text: `$x < ${q}$` },
        { key: 'gp', text: `$x > ${p}$` },
      ];
    } else {
      // Local max at smaller root if a > 0.
      const xmax = a > 0 ? p : q, xmin = a > 0 ? q : p;
      const ans = kind === 'max' ? xmax : xmin;
      correct = num(ans);
      w = [num(kind === 'max' ? xmin : xmax, 'That is the other stationary point. Check the nature with $f\'\'(x)$ or the shape of the cubic.'), num(-ans, 'Sign slip in the factorisation of $f\'(x)$.'), num((p + q) / 2, 'That is the point of inflection.'), num(-(kind === 'max' ? xmin : xmax))];
    }
    const opts = choices(rng, correct, w, { n: 5, sort: kind !== 'dec', fill: kind === 'dec' ? null : nearFill(correct.v, 4) });
    const ask = { max: 'What is the $x$-coordinate of the local maximum of', min: 'What is the $x$-coordinate of the local minimum of', dec: 'For which values of $x$ is the following function decreasing?' }[kind];
    return {
      stem: `${ask} $$f(x) = ${poly(f)}${kind === 'dec' ? '' : '\\,?'}$$`,
      ...opts,
      solution: `$f'(x) = ${poly(deriv(f))} = ${a > 0 ? '' : '-'}3${fac(p)}${fac(q)}$, so the stationary points are at $x = ${p}$ and $x = ${q}$.\n\nThe cubic has ${a > 0 ? 'positive' : 'negative'} leading coefficient, so ${a > 0 ? `it rises, turns at a local maximum at $x = ${p}$, falls, then turns at a local minimum at $x = ${q}$` : `it falls, turns at a local minimum at $x = ${p}$, rises, then turns at a local maximum at $x = ${q}$`}.${kind === 'dec' ? ` It is decreasing where $f'(x) < 0$: ${correct.text}.` : ''}`,
      insight: 'For a cubic you rarely need f″: the sign of the leading coefficient tells you which stationary point is the max.',
      time: 120,
    };
  },
};

const noStationary = {
  id: 'cubic-no-stationary', topic: 'diff', paper: 1, levels: [3, 4], skills: ['stationary points', 'discriminant', 'parameters'],
  name: 'When does a cubic have no stationary points?',
  make(rng, level) {
    // f = x^3 + k x^2 + m x ; f' = 3x^2 + 2kx + m ; no roots iff 4k^2 < 12m iff k^2 < 3m. Take m = 3s^2.
    const s = rng.int(1, 4), m = 3 * s * s;
    const R = 3 * s;
    const kind = level >= 4 ? rng.pick(['none', 'two']) : 'none';
    const inn = `$-${R} < k < ${R}$`, out = `$k < -${R}$ or $k > ${R}$`;
    const correct = kind === 'none' ? { key: 'in', text: inn } : { key: 'out', text: out };
    const w = [
      { key: kind === 'none' ? 'out' : 'in', text: kind === 'none' ? out : inn, why: 'Two distinct stationary points need $\\Delta > 0$; none need $\\Delta < 0$.' },
      { key: 'e', text: `$-${R} \\le k \\le ${R}$`, why: 'At $k = \\pm' + R + '$ there is one stationary point (a point of inflection), so the boundary is excluded.' },
      { key: 'h', text: `$-${s} < k < ${s}$`, why: 'The discriminant of $3x^2 + 2kx + ' + m + '$ is $4k^2 - 12\\times' + m + '$.' },
      { key: 's', text: `$-${3 * s * s} < k < ${3 * s * s}$`, why: 'Take the square root at the end: $k^2 < ' + R * R + '$.' },
    ];
    const opts = choices(rng, correct, w, { n: 5 });
    return {
      stem: `Find the complete set of values of $k$ for which the curve $$y = x^3 + kx^2 + ${m}x$$ has ${kind === 'none' ? 'no stationary points' : 'two distinct stationary points'}.`,
      ...opts,
      solution: `$\\dfrac{dy}{dx} = 3x^2 + 2kx + ${m}$. Stationary points are its real roots.\n\nDiscriminant: $4k^2 - 4(3)(${m}) = 4(k^2 - ${R * R})$.\n\n- no roots: $k^2 < ${R * R} \\iff -${R} < k < ${R}$\n- two distinct roots: $k^2 > ${R * R} \\iff k < -${R}$ or $k > ${R}$`,
      insight: 'Count stationary points by applying the discriminant to f′(x).',
      time: 150,
    };
  },
};

const defInt = {
  id: 'definite-integral', topic: 'integ', paper: 1, levels: [1, 2], skills: ['definite integrals'],
  name: 'Definite integral of a polynomial',
  make(rng, level) {
    const p = [[rng.nonzero(-3, 3) * 3, 2], [rng.int(-4, 4) * 2, 1], [rng.int(-5, 5), 0]];
    if (level >= 2) p.push([rng.nonzero(-2, 2) * 4, 3]);
    const a = rng.int(-2, 1), b = rng.int(a + 1, 3);
    const A = antider(p);
    const ans = evalP(A, F(b)).sub(evalP(A, F(a)));
    const w = [
      num(evalP(A, F(a)).sub(evalP(A, F(b))), 'Upper limit minus lower limit, not the other way round.'),
      num(evalP(A, F(b)), a !== 0 ? 'Subtract the value at the lower limit too.' : null),
      num(evalP(p, F(b)).sub(evalP(p, F(a))), 'You need to integrate first, then substitute.'),
      num(evalP(deriv(p), F(b)).sub(evalP(deriv(p), F(a))), 'That differentiates instead of integrating.'),
    ];
    const opts = choices(rng, num(ans), w, { n: 5, sort: true, fill: nearFill(ans, 6) });
    return {
      stem: `Evaluate $$\\int_{${a}}^{${b}} \\left(${poly(p.slice().sort((u, v) => v[1] - u[1]))}\\right)\\,dx.$$`,
      ...opts,
      solution: `An antiderivative is $${poly(A.slice().sort((u, v) => v[1] - u[1]))}$.\n\n$$\\Bigl[${poly(A.slice().sort((u, v) => v[1] - u[1]))}\\Bigr]_{${a}}^{${b}} = (${evalP(A, F(b)).tex()}) - (${evalP(A, F(a)).tex()}) = ${ans.tex()}.$$`,
      insight: 'Integrate term by term, then F(upper) − F(lower).',
      time: 80 + level * 15,
    };
  },
};

const areaParabola = {
  id: 'area-parabola', topic: 'integ', paper: 1, levels: [2, 3], skills: ['area under a curve'],
  name: 'Area enclosed by a parabola and the x-axis',
  make(rng, level) {
    const p = rng.int(-3, 2), q = rng.int(p + 1, p + 4);
    const a = level >= 3 ? rng.pick([1, 2, 3, -1, -2]) : 1;
    const f = [[a, 2], [-a * (p + q), 1], [a * p * q, 0]];
    const w3 = (q - p) ** 3;
    const ans = F(Math.abs(a) * w3, 6);
    const w = [
      num(ans.neg(), 'The integral is negative because the region is below the axis; the area is its absolute value.'),
      num(F(Math.abs(a) * w3, 3), 'Check the arithmetic of the antiderivative at both limits.'),
      num(F(Math.abs(a) * w3, 2)),
      num(F(Math.abs(a) * (q - p) ** 2, 2)),
    ];
    const opts = choices(rng, num(ans), w, { n: 5, sort: true, fill: nearFill(ans, 3) });
    const A = antider(f);
    return {
      stem: `What is the area of the finite region enclosed by the curve $y = ${poly(f)}$ and the $x$-axis?`,
      ...opts,
      solution: `$y = ${a === 1 ? '' : a === -1 ? '-' : a}${fac(p)}${fac(q)}$ meets the axis at $x = ${p}$ and $x = ${q}$.\n\n$$\\int_{${p}}^{${q}} y\\,dx = ${evalP(A, F(q)).sub(evalP(A, F(p))).tex()},$$ so the area is $${ans.tex()}$ (the region is ${a > 0 ? 'below' : 'above'} the axis).\n\nShortcut: the area between $y = a(x-p)(x-q)$ and the axis is $\\dfrac{|a|(q-p)^3}{6}$.`,
      insight: 'Area between a parabola and its chord on the axis is |a|(q − p)³/6 — worth memorising for TMUA.',
      time: 120,
    };
  },
};

const signedArea = {
  id: 'signed-area', topic: 'integ', paper: 1, levels: [3, 4], skills: ['area', 'signed area'],
  name: 'Integral vs area when the curve crosses the axis',
  make(rng, level) {
    // y = x(x - p) on [0, b] with b > p > 0
    const p = rng.int(1, 3), b = rng.int(p + 1, p + 3);
    const f = [[1, 2], [-p, 1]];
    const A = antider(f);
    const I = x => evalP(A, F(x));
    const below = I(p).sub(I(0)).neg(); // positive area below axis
    const above = I(b).sub(I(p));
    const area = below.add(above);
    const integral = I(b).sub(I(0));
    const w = [
      num(integral, 'That is the integral, which counts the region below the axis as negative.'),
      num(above.sub(below).neg()),
      num(above, 'You also need the region below the axis between $x = 0$ and $x = ' + p + '$.'),
      num(below),
    ];
    const opts = choices(rng, num(area), w, { n: 5, sort: true, fill: nearFill(area, 3) });
    return {
      stem: `What is the total area of the regions between the curve $y = ${poly(f)}$, the $x$-axis and the lines $x = 0$ and $x = ${b}$?`,
      ...opts,
      solution: `The curve crosses the axis at $x = 0$ and $x = ${p}$, and is negative in between.\n\n$\\int_0^{${p}} y\\,dx = ${below.neg().tex()}$, so that region has area $${below.tex()}$.\n\n$\\int_{${p}}^{${b}} y\\,dx = ${above.tex()}$.\n\nTotal area $= ${below.tex()} + ${above.tex()} = ${area.tex()}$, whereas $\\int_0^{${b}} y\\,dx = ${integral.tex()}$.`,
      insight: 'Before integrating for an area, sketch: split at every root and add absolute values.',
      time: 180,
    };
  },
};

const findLimit = {
  id: 'integral-find-k', topic: 'integ', paper: 1, levels: [2, 3], skills: ['definite integrals', 'solving for a limit'],
  name: 'Find the limit of integration',
  make(rng, level) {
    const a = rng.int(1, 5), k = rng.int(a + 1, a + 6);
    const V = k * k - a * k;
    const w = [num(a - k, 'This root is not positive.'), num(k + a), num(V), num(Math.max(1, k - 1))];
    const opts = choices(rng, num(k), w, { n: 5, sort: true, fill: nearFill(k, 4) });
    return {
      stem: `Given that $k > 0$ and $$\\int_0^k (2x - ${a})\\,dx = ${V},$$ find $k$.`,
      ...opts,
      solution: `$\\int_0^k (2x - ${a})\\,dx = k^2 - ${a}k$. Set equal to $${V}$: $k^2 - ${a}k - ${V} = 0 \\implies (k - ${k})(k + ${k - a}) = 0$.\n\nSince $k > 0$, $k = ${k}$.`,
      insight: 'Integrate with the unknown as a limit, then solve the resulting equation — and apply the stated condition.',
      time: 90,
    };
  },
};

export default [gradientAt, tangentIntercept, stationary, noStationary, defInt, areaParabola, signedArea, findLimit];
