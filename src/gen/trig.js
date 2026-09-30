import { choices, num, nearFill, poly, F, Frac } from './helpers.js';

// Exact special values, in degrees. For each value: base angles t in [0, 360) with f(t) = value.
const SIN = {
  '0': [0, 180], '\\tfrac12': [30, 150], '-\\tfrac12': [210, 330], '\\tfrac{\\sqrt3}{2}': [60, 120],
  '-\\tfrac{\\sqrt3}{2}': [240, 300], '1': [90], '-1': [270], '\\tfrac{1}{\\sqrt2}': [45, 135], '-\\tfrac{1}{\\sqrt2}': [225, 315],
};
const COS = {
  '0': [90, 270], '\\tfrac12': [60, 300], '-\\tfrac12': [120, 240], '\\tfrac{\\sqrt3}{2}': [30, 330],
  '-\\tfrac{\\sqrt3}{2}': [150, 210], '1': [0], '-1': [180], '\\tfrac{1}{\\sqrt2}': [45, 315], '-\\tfrac{1}{\\sqrt2}': [135, 225],
};

const countSolutions = {
  id: 'trig-count', topic: 'trig', paper: 1, levels: [2, 4], skills: ['trig equations', 'counting solutions'],
  name: 'Counting solutions of a trig equation',
  make(rng, level) {
    const fn = rng.pick(['sin', 'cos']);
    const table = fn === 'sin' ? SIN : COS;
    const val = rng.pick(Object.keys(table));
    const k = level === 2 ? rng.pick([1, 2]) : rng.pick([2, 3, 4, 5]);
    const range = level >= 4 ? rng.pick([180, 360, 540]) : 360;
    const radians = level >= 3 && rng.chance(0.6);
    // Solutions: x in [0, range] with k x ≡ base (mod 360)  <=> t = kx in [0, k*range]
    let count = 0;
    for (const b of table[val]) {
      for (let t = b; t <= k * range; t += 360) if (t >= 0) count++;
    }
    const fmtR = deg => (radians ? { 180: '\\pi', 360: '2\\pi', 540: '3\\pi' }[deg] : `${deg}^\\circ`);
    const w = [
      num(table[val].length * k, 'Check the endpoints of the interval: are any solutions exactly at the ends?'),
      num(table[val].length, `The graph of ${fn} ${k}x completes ${k} cycles per ${radians ? '$2\\pi$' : '$360^\\circ$'}, so there are more solutions than for ${fn} x.`),
      num(count + 1, 'Count carefully, including whether the interval endpoints count.'),
      num(count - 1),
      num(2 * count),
    ];
    const opts = choices(rng, num(count), w, { n: 5, sort: true, fill: nearFill(count, 3) });
    const eq = `\\${fn} ${k === 1 ? '' : k}x = ${val}`;
    const list = [];
    for (const b of table[val]) for (let t = b; t <= k * range; t += 360) list.push(t);
    list.sort((a, b) => a - b);
    return {
      stem: `How many solutions does the equation $$${eq}$$ have in the interval $0 \\le x \\le ${fmtR(range)}$?`,
      ...opts,
      solution: `Let $t = ${k === 1 ? '' : k}x$. As $x$ runs over $[0, ${fmtR(range)}]$, $t$ runs over $[0, ${k * range}^\\circ]$${radians ? ' (working in degrees for convenience)' : ''}.\n\nIn one turn, $\\${fn} t = ${val}$ at $t = ${table[val].map(b => b + '^\\circ').join(', ')}$. Adding multiples of $360^\\circ$ and keeping those in range: $t = ${list.map(t => t + '^\\circ').join(', ')}$.\n\nThat is **${count}** solutions.`,
      insight: 'Substitute t = kx, stretch the interval by k, then count solutions of the simple equation over the longer interval, minding endpoints.',
      time: 90 + level * 25,
    };
  },
};

const trigQuadMax = {
  id: 'trig-quad-range', topic: 'trig', paper: 1, levels: [4, 5], skills: ['trig identities', 'maximum and minimum'],
  name: 'Max/min of a quadratic in sin x',
  make(rng, level) {
    // f = A + B sin x - C cos^2 x = (A - C) + B s + C s^2, s in [-1, 1]
    const C = rng.pick([1, 2, 3]) * rng.sign();
    const B = rng.nonzero(-4, 4);
    const A = rng.int(-3, 5);
    const g = s => F(A - C).add(s.mul(B)).add(s.mul(s).mul(C));
    const sv = F(-B, 2 * C);
    const cands = [F(-1), F(1)];
    if (Math.abs(sv.value) < 1) cands.push(sv);
    const vals = cands.map(g);
    const askMax = rng.chance(0.5);
    const best = vals.reduce((m, v) => (askMax ? (v.value > m.value ? v : m) : (v.value < m.value ? v : m)));
    const endsOnly = [g(F(-1)), g(F(1))].reduce((m, v) => (askMax ? (v.value > m.value ? v : m) : (v.value < m.value ? v : m)));
    const w = [
      num(g(sv), 'The vertex of the quadratic in $s$ is only relevant if it lies in $-1 \\le s \\le 1$, and only if it is the right kind of extremum.'),
      num(endsOnly, 'Check the vertex of the quadratic too, not just $s = \\pm1$.'),
      num(askMax ? vals.reduce((m, v) => (v.value < m.value ? v : m)) : vals.reduce((m, v) => (v.value > m.value ? v : m)), askMax ? 'That is the minimum.' : 'That is the maximum.'),
      num(F(A + Math.abs(B) + Math.abs(C)), 'Maximising each term separately does not work: they are not independent.'),
    ];
    const opts = choices(rng, num(best), w, { n: 5, sort: true, fill: nearFill(best, 3) });
    const texF = `${A !== 0 ? A + ' ' : ''}${B > 0 ? (A !== 0 ? '+ ' : '') : '- '}${Math.abs(B) === 1 ? '' : Math.abs(B)}\\sin x ${C > 0 ? '-' : '+'} ${Math.abs(C) === 1 ? '' : Math.abs(C)}\\cos^2 x`;
    return {
      stem: `What is the ${askMax ? 'maximum' : 'minimum'} value of $$${texF}$$ as $x$ varies over all real numbers?`,
      ...opts,
      solution: `Use $\\cos^2 x = 1 - \\sin^2 x$ and let $s = \\sin x$, where $-1 \\le s \\le 1$:\n$$f = ${poly([[C, 2], [B, 1], [A - C, 0]], 's')}.$$\nCheck the endpoints and the vertex $s = ${sv.tex()}$${Math.abs(sv.value) < 1 ? '' : ' (outside the interval, so ignore it)'}: ${cands.map((c, i) => `$f(${c.tex()}) = ${vals[i].tex()}$`).join(', ')}.\n\nThe ${askMax ? 'maximum' : 'minimum'} is $${best.tex()}$.`,
      insight: 'Turn it into a quadratic in s = sin x on the closed interval [−1, 1]; compare the endpoints and the vertex.',
      time: 200,
    };
  },
};

const cosineRule = {
  id: 'cosine-rule', topic: 'trig', paper: 1, levels: [1, 3], skills: ['cosine rule', 'triangle area'],
  name: 'Cosine rule and area',
  make(rng, level) {
    const b = rng.int(2, 9), c = rng.int(2, 9);
    const A = rng.pick([60, 120]);
    const askArea = level >= 3 && rng.chance(0.5);
    if (askArea) {
      const coef = F(b * c, 4); // area = (1/2) b c sin A = (sqrt3/4) bc
      const t = x => ({ key: x.key(), text: `$${x.isInt() ? (x.n === 1 ? '' : x.n) : x.tex()}\\sqrt{3}$`, v: x.value });
      const w = [
        { ...t(F(b * c, 2)), why: 'Area $= \\tfrac12 bc\\sin A$ and $\\sin' + A + '^\\circ = \\tfrac{\\sqrt3}{2}$: you are missing a factor of $\\tfrac12$.' },
        { key: 'half', text: `$${F(b * c, 4).tex()}$`, v: b * c / 4, why: 'Use $\\sin A$, not $\\cos A$.' },
        { ...t(F(b * c)) },
        { key: 'ha', text: `$${F(b * c, 2).tex()}$`, v: b * c / 2 },
      ];
      const opts = choices(rng, t(coef), w, { n: 5, sort: true });
      return {
        stem: `In triangle $ABC$, $AB = ${c}$, $AC = ${b}$ and angle $BAC = ${A}^\\circ$. What is the area of the triangle?`,
        ...opts,
        solution: `Area $= \\tfrac12 \\times AB \\times AC \\times \\sin A = \\tfrac12 \\times ${c} \\times ${b} \\times \\tfrac{\\sqrt3}{2} = ${coef.isInt() ? coef.n : coef.tex()}\\sqrt3$.\n\n(Note $\\sin 120^\\circ = \\sin 60^\\circ$.)`,
        insight: 'Area = ½ab sin C with the included angle; sin(180° − θ) = sin θ.',
        time: 80,
      };
    }
    const a2 = A === 60 ? b * b + c * c - b * c : b * b + c * c + b * c;
    const w = [
      num(A === 60 ? b * b + c * c + b * c : b * b + c * c - b * c, 'Check the sign of $\\cos ' + A + '^\\circ$.'),
      num(b * b + c * c, 'The $-2bc\\cos A$ term is missing.'),
      num(A === 60 ? b * b + c * c - 2 * b * c : b * b + c * c + 2 * b * c, '$\\cos' + A + '^\\circ = ' + (A === 60 ? '' : '-') + '\\tfrac12$, so $2bc\\cos A = ' + (A === 60 ? '' : '-') + 'bc$.'),
    ];
    const opts = choices(rng, num(a2), w, { n: 5, sort: true, fill: nearFill(a2, 8) });
    return {
      stem: `In triangle $ABC$, $AB = ${c}$, $AC = ${b}$ and angle $BAC = ${A}^\\circ$. What is $BC^2$?`,
      ...opts,
      solution: `Cosine rule: $BC^2 = ${b}^2 + ${c}^2 - 2(${b})(${c})\\cos ${A}^\\circ = ${b * b + c * c} ${A === 60 ? '-' : '+'} ${b * c} = ${a2}$.`,
      insight: 'a² = b² + c² − 2bc cos A; cos 120° = −½ makes the last term add.',
      time: 70,
    };
  },
};

const sector = {
  id: 'sector', topic: 'trig', paper: 1, levels: [1, 2], skills: ['radians', 'arc length', 'sector area'],
  name: 'Arc length and sector area',
  make(rng, level) {
    const r = rng.int(2, 12);
    const th = F(rng.int(1, 5), rng.pick([2, 3, 4, 6]));
    if (th.value >= 2) th.n = 1;
    const askArea = rng.chance(0.5);
    const val = askArea ? th.mul(r * r).div(2) : th.mul(r);
    const pi = x => ({ key: x.key(), text: `$${x.isInt() ? (x.n === 1 ? '' : x.n) : `\\frac{${x.n}}{${x.d}}`}\\pi$`, v: x.value });
    const w = askArea
      ? [{ ...pi(th.mul(r * r)), why: 'Sector area is $\\tfrac12 r^2\\theta$.' }, { ...pi(th.mul(r)), why: 'That is the arc length.' }, pi(th.mul(r * r).div(4)), pi(th.mul(r).div(2))]
      : [{ ...pi(th.mul(r * r).div(2)), why: 'That is the sector area.' }, { ...pi(th.mul(2 * r)), why: 'Arc length is $r\\theta$ (no factor of 2).' }, pi(th.mul(r).div(2)), pi(th)];
    const opts = choices(rng, pi(val), w, { n: 5, sort: true, fill: r => pi(val.mul(F(r.int(1, 6), r.int(1, 4)))) });
    return {
      stem: `A sector of a circle has radius $${r}$ and angle $${th.n === 1 ? '' : th.n}\\pi${th.d === 1 ? '' : '/' + th.d}$ radians. What is its ${askArea ? 'area' : 'arc length'}?`,
      ...opts,
      solution: askArea ? `Area $= \\tfrac12 r^2\\theta = \\tfrac12\\times ${r * r}\\times ${pi(th).text.slice(1, -1)} = ${pi(val).text.slice(1, -1)}$.` : `Arc length $= r\\theta = ${r}\\times ${pi(th).text.slice(1, -1)} = ${pi(val).text.slice(1, -1)}$.`,
      insight: 'In radians: arc = rθ, area = ½r²θ.',
      time: 60,
    };
  },
};

export default [countSolutions, trigQuadMax, cosineRule, sector];
