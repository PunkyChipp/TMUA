import { choices, num, nearFill, poly, signed, binom, F, Frac, fac } from './helpers.js';

const apSum = {
  id: 'ap-sum', speedOnly: true, topic: 'seq', paper: 1, levels: [1, 3], skills: ['arithmetic series'],
  name: 'Arithmetic series from two terms',
  make(rng, level) {
    const a = rng.int(-10, 15), d = rng.nonzero(-4, 6);
    const p = rng.int(2, 6), q = rng.int(p + 2, 12);
    const n = rng.int(10, level === 1 ? 20 : 40);
    const up = a + (p - 1) * d, uq = a + (q - 1) * d;
    const S = (n * (2 * a + (n - 1) * d)) / 2;
    const w = [
      num((n * (2 * a + n * d)) / 2, 'Off by one: the $n$th term is $a + (n-1)d$.'),
      num(n * (2 * a + (n - 1) * d), 'Missing the factor of $\\tfrac12$.'),
      num((n * (2 * (a + d) + (n - 1) * d)) / 2, 'Check the first term: work back from the given terms.'),
    ];
    const opts = choices(rng, num(S), w, { n: 5, sort: true, fill: nearFill(S, 20) });
    return {
      stem: `In an arithmetic sequence the ${ord(p)} term is $${up}$ and the ${ord(q)} term is $${uq}$. What is the sum of the first $${n}$ terms?`,
      ...opts,
      solution: `$u_{${q}} - u_{${p}} = ${q - p}d = ${uq - up}$, so $d = ${d}$ and $a = u_{${p}} - ${p - 1}d = ${a}$.\n\n$$S_{${n}} = \\frac{${n}}{2}\\bigl(2(${a}) + ${n - 1}(${d})\\bigr) = ${S}.$$`,
      insight: 'Two terms give d by subtraction; S_n = n/2 (2a + (n − 1)d).',
      time: 100,
    };
  },
};

function ord(n) {
  const s = ['th', 'st', 'nd', 'rd'], v = n % 100;
  return n + (s[(v - 20) % 10] || s[v] || s[0]);
}

const gpInfinity = {
  id: 'gp-infinity', speedOnly: true, topic: 'seq', paper: 1, levels: [2, 3], skills: ['geometric series', 'sum to infinity'],
  name: 'Sum to infinity',
  make(rng, level) {
    let r;
    do { r = F(rng.nonzero(-4, 4), rng.int(2, 5)); } while (Math.abs(r.value) >= 1);
    const a = F(rng.nonzero(-6, 12) * r.d);
    const S = a.div(F(1).sub(r));
    const t2 = a.mul(r);
    const w = [
      num(a.div(F(1).add(r)), 'The formula is $a/(1 - r)$; check the sign of $r$.'),
      num(a.div(r.sub(1)), 'That is $a/(r - 1)$: the sign is wrong.'),
      num(t2.div(F(1).sub(r)), 'Start from the first term, not the second.'),
    ];
    const opts = choices(rng, num(S), w, { n: 5, sort: true, fill: nearFill(S, 5) });
    return {
      stem: `A geometric series has first term $${a.tex()}$ and second term $${t2.tex()}$. What is its sum to infinity?`,
      ...opts,
      solution: `$r = \\dfrac{${t2.tex()}}{${a.tex()}} = ${r.tex()}$, and $|r| < 1$ so the series converges.\n\n$$S_\\infty = \\frac{a}{1 - r} = \\frac{${a.tex()}}{1 - (${r.tex()})} = ${S.tex()}.$$`,
      insight: 'Find r = u₂/u₁, check |r| < 1, then S∞ = a / (1 − r).',
      time: 80,
    };
  },
};

const binomCoef = {
  id: 'binom-coef', topic: 'seq', paper: 1, levels: [2, 4], skills: ['binomial expansion'],
  name: 'Coefficient in a binomial expansion',
  make(rng, level) {
    const n = rng.int(4, level >= 4 ? 9 : 7);
    const a = rng.pick([1, 2, 3]), b = rng.pick([1, 2, 3, -1, -2]);
    if (level >= 4) {
      // Constant term of (x + c/x^2)^n style: (x^p + b/x^q)^n with p=1..2, q=1..2
      const p = rng.pick([1, 2]), q = rng.pick([1, 2]);
      // term: C(n,r) (x^p)^(n-r) (b x^-q)^r ; power p(n-r) - q r = 0 -> r = pn/(p+q)
      let nn = n;
      while ((p * nn) % (p + q) !== 0) nn++;
      const r = (p * nn) / (p + q);
      const ans = binom(nn, r) * b ** r;
      const w = [num(binom(nn, r), 'The constant $' + b + '$ is raised to the power too.'), num(binom(nn, r + 1) * b ** (r + 1), 'Solve for the power of $x$ being zero carefully.'), num(-ans, 'Sign: $(' + b + ')^{' + r + '}$.')];
      const opts = choices(rng, num(ans), w, { n: 5, sort: true, fill: nearFill(ans, 10) });
      const X = p === 1 ? 'x' : 'x^2';
      const Y = q === 1 ? 'x' : 'x^2';
      return {
        stem: `What is the term independent of $x$ in the expansion of $$\\left(${X} ${b < 0 ? '-' : '+'} \\frac{${Math.abs(b)}}{${Y}}\\right)^{${nn}}\\,?$$`,
        ...opts,
        solution: `General term: $\\binom{${nn}}{r}(${X})^{${nn}-r}\\left(\\dfrac{${b}}{${Y}}\\right)^r$, with power of $x$ equal to $${p}(${nn} - r) - ${q}r$.\n\nSet this to zero: $r = ${r}$. The term is $\\binom{${nn}}{${r}}(${b})^{${r}} = ${binom(nn, r)}\\times ${b ** r} = ${ans}$.`,
        insight: 'Write the general term, collect the power of x, and solve for the r that makes it what you want.',
        time: 180,
      };
    }
    const k = rng.int(2, n - 1);
    const ans = binom(n, k) * a ** (n - k) * b ** k;
    const w = [
      num(a ** (n - k) * b ** k, 'Include the binomial coefficient $\\binom{n}{k}$.'),
      num(binom(n, k) * a ** k * b ** (n - k), 'The powers are the wrong way round: $x^k$ comes with $b^k$.'),
      num(binom(n, k) * b ** k, 'The constant term $a$ is also raised to a power.'),
      num(-ans, 'Check the sign.'),
    ];
    const opts = choices(rng, num(ans), w, { n: 5, sort: true, fill: nearFill(ans, 12) });
    return {
      stem: `What is the coefficient of $x^{${k}}$ in the expansion of $(${a} ${b < 0 ? '-' : '+'} ${Math.abs(b) === 1 ? '' : Math.abs(b)}x)^{${n}}$?`,
      ...opts,
      solution: `The term in $x^{${k}}$ is $\\binom{${n}}{${k}}(${a})^{${n - k}}(${b}x)^{${k}}$, with coefficient $${binom(n, k)} \\times ${a ** (n - k)} \\times ${b ** k} = ${ans}$.`,
      insight: 'Term in xᵏ of (a + bx)ⁿ is C(n,k) aⁿ⁻ᵏ bᵏ xᵏ.',
      time: 100,
    };
  },
};

const periodic = {
  id: 'periodic-seq', topic: 'seq', paper: 1, levels: [3, 4], skills: ['recurrence relations', 'periodic sequences'],
  name: 'Periodic recurrence',
  make(rng, level) {
    // u_{n+1} = 1/(1 - u_n) has period 3.
    let t;
    do { t = F(rng.nonzero(-5, 5), rng.int(1, 3)); } while (t.eq(1) || t.eq(0));
    const u = [t, F(1).div(F(1).sub(t))];
    u.push(F(1).div(F(1).sub(u[1])));
    const N = rng.int(20, 100);
    const askSum = level >= 4;
    let ans, sol;
    const cyc = u[0].add(u[1]).add(u[2]);
    if (askSum) {
      const full = Math.floor(N / 3), rem = N % 3;
      ans = cyc.mul(full);
      for (let i = 0; i < rem; i++) ans = ans.add(u[i]);
      sol = `One period sums to $${u.map(x => x.tex()).join(' + ')} = ${cyc.tex()}$. $${N} = 3\\times${full} + ${rem}$, so the sum is $${full}\\times ${cyc.tex()}${rem ? ' + ' + u.slice(0, rem).map(x => `(${x.tex()})`).join(' + ') : ''} = ${ans.tex()}$.`;
    } else {
      ans = u[(N - 1) % 3];
      sol = `The sequence repeats every 3 terms. $${N} = 3\\times ${Math.floor((N - 1) / 3)} + ${((N - 1) % 3) + 1}$, so $u_{${N}} = u_{${((N - 1) % 3) + 1}} = ${ans.tex()}$.`;
    }
    const w = askSum
      ? [num(cyc.mul(Math.floor(N / 3))), num(cyc.mul(Math.ceil(N / 3))), num(ans.add(u[0]))]
      : u.filter(x => !x.eq(ans)).map(x => num(x, 'Right cycle; check which position ' + N + ' lands on.'));
    const opts = choices(rng, num(ans), w, { n: 5, sort: true, fill: nearFill(ans, 3) });
    return {
      stem: `A sequence is defined by $u_1 = ${t.tex()}$ and $$u_{n+1} = \\frac{1}{1 - u_n}.$$ What is ${askSum ? `$\\displaystyle\\sum_{n=1}^{${N}} u_n$` : `$u_{${N}}$`}?`,
      ...opts,
      solution: `Compute a few terms: $u_1 = ${u[0].tex()}$, $u_2 = ${u[1].tex()}$, $u_3 = ${u[2].tex()}$, $u_4 = \\frac{1}{1 - (${u[2].tex()})} = ${u[0].tex()} = u_1$.\n\n${sol}`,
      insight: 'When a recurrence looks awkward, write out the first few terms: TMUA sequences are often periodic.',
      time: 150,
    };
  },
};

const sigma = {
  id: 'sigma-linear', speedOnly: true, topic: 'seq', paper: 1, levels: [1, 2], skills: ['sigma notation'],
  name: 'Sigma notation',
  make(rng, level) {
    const a = rng.nonzero(-5, 6), b = rng.int(-9, 9);
    const lo = level === 1 ? 1 : rng.int(1, 11), hi = rng.int(lo + 8, lo + 30);
    const S = x => (a * x * (x + 1)) / 2 + b * x;
    const ans = S(hi) - S(lo - 1);
    const cnt = hi - lo + 1;
    const w = [
      num((a * hi * (hi + 1)) / 2 + b * hi - ((a * lo * (lo + 1)) / 2 + b * lo), 'Subtract the sum up to $' + (lo - 1) + '$, not up to $' + lo + '$.'),
      num((a * (hi + lo) * cnt) / 2, 'The constant term is added once for every term.'),
      num(ans + b, 'Count the terms: there are $' + cnt + '$.'),
    ];
    const opts = choices(rng, num(ans), w, { n: 5, sort: true, fill: nearFill(ans, 25) });
    const term = poly([[a, 1], [b, 0]], 'r');
    return {
      stem: `Evaluate $$\\sum_{r=${lo}}^{${hi}} (${term}).$$`,
      ...opts,
      solution: `This is an arithmetic series with $${cnt}$ terms, first term $${a * lo + b}$ and last term $${a * hi + b}$.\n\n$$\\text{Sum} = \\frac{${cnt}}{2}(${a * lo + b} + ${a * hi + b}) = ${ans}.$$`,
      insight: 'A linear sigma is an arithmetic series: number of terms × average of first and last.',
      time: 90,
    };
  },
};

const logSimplify = {
  id: 'log-simplify', speedOnly: true, topic: 'explog', paper: 1, levels: [1, 2], skills: ['laws of logarithms'],
  name: 'Simplifying logarithms',
  make(rng, level) {
    const base = rng.pick([2, 3, 5]);
    const E = rng.int(1, level === 1 ? 4 : 6);
    // p * log(x) + log(y) - log(z) = E with y, z chosen as integers.
    const p = rng.pick([1, 2, 3]);
    const x = rng.pick([2, 3, 5, 6, 7]);
    // want x^p * y / z = base^E => choose y = base^E * z / x^p with z multiple of x^p
    const z = x ** p * rng.pick([1, 2, 3]);
    const y = (base ** E * z) / x ** p;
    const w = [num(E + 1), num(E - 1), num(E + 2), num(F(E, 2)), num(2 * E)];
    const opts = choices(rng, num(E), w, { n: 5, sort: true });
    const pT = p === 1 ? '' : p;
    return {
      stem: `Evaluate $$${pT}\\log_{${base}} ${x} + \\log_{${base}} ${y} - \\log_{${base}} ${z}.$$`,
      ...opts,
      solution: `Combine into one logarithm: $\\log_{${base}}\\dfrac{${x}^{${p}}\\times ${y}}{${z}} = \\log_{${base}} \\dfrac{${x ** p * y}}{${z}} = \\log_{${base}} ${base ** E} = ${E}$.`,
      insight: 'k log a = log aᵏ; add logs to multiply, subtract to divide, then spot the power.',
      time: 70,
    };
  },
};

const logEquation = {
  id: 'log-mixed-base', topic: 'explog', paper: 1, levels: [2, 3], skills: ['change of base'],
  name: 'Logs with related bases',
  make(rng, level) {
    const b = rng.pick([2, 3]);
    // log_b x + log_{b^2} x (+ log_{b^3} x) = k
    const three = level >= 3;
    // coefficient: 1 + 1/2 (+1/3) = 3/2 or 11/6
    const coef = three ? F(11, 6) : F(3, 2);
    const L = three ? rng.pick([6, 12, -6]) : rng.pick([2, 4, 6, -2]);
    const k = coef.mul(L);
    const ans = L >= 0 ? F(b ** L) : F(1, b ** -L);
    const val = e => (e >= 0 ? F(b ** e) : F(1, b ** -e));
    const w = [num(val(L / 2 | 0), 'Change of base: $\\log_{b^2}x = \\tfrac12\\log_b x$.'), num(val(k.isInt() ? k.n : L + 1), 'Remember to combine the terms before exponentiating.'), num(val(L + 1)), num(val(-L), 'Sign slip.')];
    const opts = choices(rng, num(ans), w, { n: 5, sort: true });
    return {
      stem: `Solve $$\\log_{${b}} x + \\log_{${b * b}} x${three ? ` + \\log_{${b ** 3}} x` : ''} = ${k.tex()}.$$`,
      ...opts,
      solution: `Use $\\log_{${b}^m} x = \\dfrac{\\log_{${b}} x}{m}$. Writing $L = \\log_{${b}} x$:\n$$L + \\tfrac12 L${three ? ' + \\tfrac13 L' : ''} = ${coef.tex()}L = ${k.tex()} \\implies L = ${L}.$$\nSo $x = ${b}^{${L}} = ${ans.tex()}$.`,
      insight: 'Change everything to one base: log_{bᵐ} x = (log_b x) / m.',
      time: 100,
    };
  },
};

const hiddenQuad = {
  id: 'hidden-quadratic-exp', topic: 'explog', paper: 1, levels: [3, 4], skills: ['exponential equations', 'substitution'],
  name: 'Hidden quadratic in 2^x',
  make(rng, level) {
    const kind = level >= 4 ? 'count' : 'sum';
    let u1, u2;
    if (kind === 'sum') { u1 = 2 ** rng.int(0, 3); do { u2 = 2 ** rng.int(0, 4); } while (u2 === u1); }
    else { u1 = rng.pick([1, 2, 3, 4, 5, 6, 8]) * rng.pick([1, -1]); do { u2 = rng.pick([1, 2, 3, 4, 5, 6, 8]) * rng.pick([1, 1, -1]); } while (u2 === u1 || u2 === -u1); }
    const B = -(u1 + u2), C = u1 * u2;
    const eq = `4^x ${signed(B)}\\times 2^x ${signed(C)} = 0`.replace('+ 1\\times', '+').replace('- 1\\times', '-');
    if (kind === 'sum') {
      const ans = Math.log2(u1) + Math.log2(u2);
      const w = [num(u1 + u2, 'That is the sum of the values of $2^x$, not of $x$.'), num(Math.log2(u1 + u2) | 0), num(ans + 1), num(Math.max(Math.log2(u1), Math.log2(u2)), 'There are two solutions; add both.')];
      const opts = choices(rng, num(ans), w, { n: 5, sort: true, fill: nearFill(ans, 3) });
      return {
        stem: `Find the sum of the real solutions of $$${eq}.$$`,
        ...opts,
        solution: `Let $u = 2^x$, so $4^x = u^2$: $${poly([[1, 2], [B, 1], [C, 0]], 'u')} = 0$, i.e. $(u - ${u1})(u - ${u2}) = 0$.\n\n$2^x = ${u1}$ gives $x = ${Math.log2(u1)}$; $2^x = ${u2}$ gives $x = ${Math.log2(u2)}$. Sum $= ${ans}$.\n\nShortcut: $2^{x_1}\\cdot 2^{x_2} = u_1u_2 = ${C}$, so $x_1 + x_2 = \\log_2 ${C} = ${ans}$.`,
        insight: 'Spot 4ˣ = (2ˣ)²; the product of the u-roots gives the sum of the x-roots.',
        time: 130,
      };
    }
    const ans = [u1, u2].filter(u => u > 0).length;
    const opts = choices(rng, num(ans), [0, 1, 2, 3].map(v => num(v, v === 2 && ans < 2 ? '$2^x$ is always positive, so a negative value of $u$ gives no solution.' : undefined)), { n: 4, sort: true });
    return {
      stem: `How many real solutions does the equation $$${eq}$$ have?`,
      ...opts,
      solution: `Let $u = 2^x > 0$: $${poly([[1, 2], [B, 1], [C, 0]], 'u')} = ${fac(u1, 'u')}${fac(u2, 'u')} = 0$, so $u = ${u1}$ or $u = ${u2}$.\n\nOnly positive values of $u$ give a real $x$ (since $2^x > 0$). Number of solutions: **${ans}**.`,
      insight: 'After substituting u = 2ˣ, discard any root with u ≤ 0.',
      time: 120,
    };
  },
};

// logEquation needs the change of base formula, which the 2026 specification excludes.
void logEquation;
export default [apSum, gpInfinity, binomCoef, periodic, sigma, logSimplify, hiddenQuad];
