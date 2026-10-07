import { choices, num, nearFill, poly, signed, surdTex, F, Frac, fac } from './helpers.js';

const fx = (c, x) => (c === 1 ? x : c === -1 ? `-${x}` : `${c}${x}`);

const transformPoint = {
  id: 'transform-point', topic: 'graphs', paper: 1, levels: [2, 4], skills: ['transformations'],
  name: 'Where does a point go under a transformation?',
  make(rng, level) {
    const p = rng.nonzero(-5, 5), q = rng.nonzero(-5, 5);
    const a = level === 2 ? 1 : rng.pick([-1, 2, 3, -2]);
    const b = rng.pick(level === 2 ? [1, 2] : [2, 3, -1, 1]);
    let c = rng.int(-4, 4), d = rng.int(-4, 4);
    if (level === 2 && b === 2) c = 0;
    const inner = b === 1 && c === 0 ? 'x' : `${fx(b, 'x')}${signed(c)}`;
    const outer = `${a === 1 ? '' : a === -1 ? '-' : a}f(${inner})${signed(d)}`;
    const X = F(p - c, b), Y = a * q + d;
    const pt = (x, y) => ({ key: `${Frac.of(x).key()}|${Frac.of(y).key()}`, text: `$\\left(${Frac.of(x).tex()},\\ ${Frac.of(y).tex()}\\right)$` });
    const w = [
      { ...pt(F(b * p + c), Y), why: 'Horizontal changes act in reverse: solve $bx + c = p$ rather than computing $bp + c$.' },
      { ...pt(F(p + c, b), Y), why: 'Sign slip: solve $bx + c = p$, so $x = (p - c)/b$.' },
      { ...pt(F(p, b).sub(c), Y), why: 'Order matters: $f(bx + c)$ means shift then stretch; solve $bx + c = p$ directly.' },
      { ...pt(X, a * (q + d)), why: 'Vertical: multiply by $a$ first, then add $d$.' },
      { ...pt(X, q + d), why: 'The vertical stretch factor was ignored.' },
    ];
    const opts = choices(rng, pt(X, Y), w, { n: 5, fill: r => pt(X.add(r.int(-3, 3)), Y + r.int(-3, 3)) });
    return {
      stem: `The graph of $y = f(x)$ passes through the point $(${p}, ${q})$. Which point must lie on the graph of $$y = ${outer}\\,?$$`,
      ...opts,
      solution: `We need the input to $f$ to be $${p}$: $${inner} = ${p} \\implies x = ${X.tex()}$.\n\nThen $y = ${a === 1 ? '' : a + '\\times '}f(${p})${signed(d)} = ${a === 1 ? '' : a + '\\times '}(${q})${signed(d)} = ${Y}$.\n\nSo the point is $(${X.tex()}, ${Y})$.`,
      insight: 'Ask "what x makes the inside equal the old x-coordinate?" — never apply horizontal changes forwards.',
      time: 100,
    };
  },
};

const cubicLevel = {
  id: 'cubic-level', topic: 'graphs', paper: 1, levels: [3, 4], skills: ['intersections', 'turning points'],
  name: 'Number of solutions of cubic = k',
  make(rng, level) {
    const m = rng.pick([1, 2, 3]);
    const T = 2 * m ** 3; // turning values ±T
    const f = `x^3 - ${3 * m * m}x`;
    if (level >= 4) {
      const ans = 2 * T - 1;
      const w = [num(2 * T + 1, 'At $k = \\pm' + T + '$ the line is tangent: only two distinct solutions.'), num(2 * T, 'Count the integers in the open interval carefully (including 0).'), num(T - 1, 'You only counted positive $k$.'), num(T, 'Half the interval.')];
      const opts = choices(rng, num(ans), w, { n: 5, sort: true });
      return {
        stem: `For how many **integer** values of $k$ does the equation $${f} = k$ have three distinct real solutions?`,
        ...opts,
        solution: `Let $g(x) = ${f}$. Then $g'(x) = 3x^2 - ${3 * m * m} = 0$ at $x = \\pm ${m}$, with $g(-${m}) = ${T}$ (local max) and $g(${m}) = -${T}$ (local min).\n\nThe horizontal line $y = k$ meets the curve three times exactly when $-${T} < k < ${T}$. The integers in that open interval number $2\\times${T} - 1 = ${ans}$.`,
        insight: 'Count intersections of the curve with a horizontal line: everything depends on where k sits relative to the turning values.',
        time: 180,
      };
    }
    const kind = rng.pick(['in', 'edge', 'out', 'zero']);
    const k = kind === 'in' ? rng.int(1, T - 1) * rng.sign() : kind === 'edge' ? T * rng.sign() : kind === 'zero' ? 0 : (T + rng.int(1, 6)) * rng.sign();
    const ans = Math.abs(k) < T ? 3 : Math.abs(k) === T ? 2 : 1;
    const opts = choices(rng, num(ans), [0, 1, 2, 3].map(v => num(v, v === 3 && ans === 2 ? 'At a turning value the line is tangent, so two roots coincide.' : undefined)), { n: 4, sort: true });
    return {
      stem: `How many distinct real solutions does the equation $${f} = ${k}$ have?`,
      ...opts,
      solution: `Sketch $y = ${f}$. Its derivative $3x^2 - ${3 * m * m}$ vanishes at $x = \\pm${m}$; the turning values are $y = ${T}$ (at $x=-${m}$) and $y = -${T}$ (at $x = ${m}$).\n\nThe line $y = ${k}$ is ${Math.abs(k) < T ? 'strictly between the turning values, so it crosses three times' : Math.abs(k) === T ? 'level with a turning point, so it touches there and crosses once elsewhere: two distinct solutions' : 'beyond both turning values, so it crosses once'}. Answer: **${ans}**.`,
      insight: 'Solutions of f(x) = k are intersections of y = f(x) with a horizontal line; compare k with the turning values.',
      time: 120,
    };
  },
};

const whichGraph = {
  id: 'which-graph', speedOnly: true, topic: 'graphs', paper: 1, levels: [2, 3], skills: ['sketching', 'roots and multiplicity'],
  name: 'Which graph is it?',
  make(rng, level) {
    let a, b;
    do { a = rng.int(-2, 2); b = rng.int(-2, 2); } while (a === b);
    const s = rng.sign();
    const tex = `y = ${s < 0 ? '-' : ''}${fac(a)}${fac(b)}^2`;
    const mk = (sg, r1, r2, why) => ({
      key: `${sg},${r1},${r2}`, why,
      plot: { x: [-3.5, 3.5], y: [-5, 5], ticks: true, curves: [{ fn: `${sg * 0.45}*(x-(${r1}))*(x-(${r2}))^2` }] },
    });
    const correct = mk(s, a, b);
    const pool = [
      mk(-s, a, b, 'Look at the sign of the leading coefficient: it fixes how the graph behaves for large $x$.'),
      mk(s, b, a, 'The squared factor gives the repeated root, where the graph touches the axis rather than crossing.'),
      mk(s, -a, -b, 'The factor $(x - r)$ gives a root at $x = r$, not $x = -r$.'),
      mk(-s, b, a),
      mk(-s, -a, -b),
    ];
    const seenKeys = new Set([correct.key]);
    const picked = [correct];
    for (const o of pool) { if (!seenKeys.has(o.key) && picked.length < 4) { seenKeys.add(o.key); picked.push(o); } }
    const shuffled = rng.shuffle(picked);
    const distractors = {};
    shuffled.forEach((o, i) => { if (o.why) distractors[i] = o.why; });
    return {
      stem: `Which of the following is a sketch of $$${tex}\\,?$$`,
      options: shuffled.map(o => ({ plot: o.plot })),
      answer: shuffled.indexOf(correct),
      distractors,
      solution: `Roots: $x = ${a}$ (single, so the graph **crosses** the axis) and $x = ${b}$ (double, so the graph **touches** the axis and turns).\n\nThe cubic has leading coefficient ${s > 0 ? 'positive: $y \\to +\\infty$ as $x \\to +\\infty$' : 'negative: $y \\to -\\infty$ as $x \\to +\\infty$'}.\n\nOnly one sketch has all three features.`,
      insight: 'Read a factorised polynomial as: where are the roots, which are repeated (touch) and which are single (cross), and which way do the ends go?',
      time: 90 + level * 20,
    };
  },
};

const circleCentre = {
  id: 'circle-centre', speedOnly: true, topic: 'coord', paper: 1, levels: [1, 2], skills: ['circles', 'completing the square'],
  name: 'Centre and radius of a circle',
  make(rng, level) {
    const h = rng.nonzero(-6, 6), k = rng.nonzero(-6, 6), r = rng.int(2, 9);
    const D = -2 * h, E = -2 * k, Fc = h * h + k * k - r * r;
    const eq = `x^2 + y^2 ${signed(D)}x ${signed(E)}y ${signed(Fc)} = 0`.replace(/ {2,}/g, ' ');
    const cr = (x, y, rad) => ({ key: `${x},${y},${rad}`, text: `centre $(${x}, ${y})$, radius $${rad}$` });
    const wrongR2 = h * h + k * k + Fc; // sign slip on F
    const w = [
      { ...cr(-h, -k, r), why: 'Completing the square: $x^2 + Dx = (x + D/2)^2 - \\dots$, so the centre is at $x = -D/2$.' },
      { ...cr(h, k, r * r), why: 'The right-hand side is $r^2$; take the square root.' },
      wrongR2 > 0 ? { ...cr(h, k, surdTex(1, wrongR2)), why: 'Sign slip when moving the constant to the other side.' } : null,
      { ...cr(D, E, r), why: 'Halve the coefficients of $x$ and $y$ (and change sign) to get the centre.' },
      { ...cr(-h, -k, r * r) },
    ];
    const opts = choices(rng, cr(h, k, r), w, { n: 5 });
    return {
      stem: `The circle $C$ has equation $$${eq}.$$ Which of the following gives the centre and radius of $C$?`,
      ...opts,
      solution: `Complete the square:\n$$${fac(h)}^2 - ${h * h} + (y ${signed(-k)})^2 - ${k * k} ${signed(Fc)} = 0$$\n$$${fac(h)}^2 + (y ${signed(-k)})^2 = ${r * r}.$$\nCentre $(${h}, ${k})$, radius $\\sqrt{${r * r}} = ${r}$.`,
      insight: 'x² + y² + Dx + Ey + F = 0 has centre (−D/2, −E/2) and radius √(D²/4 + E²/4 − F).',
      time: 70 + level * 15,
    };
  },
};

const perpIntercept = {
  id: 'perp-line', speedOnly: true, topic: 'coord', paper: 1, levels: [1, 2], skills: ['straight lines', 'perpendicular gradients'],
  name: 'Perpendicular line',
  make(rng, level) {
    let a, b;
    do { a = rng.nonzero(-5, 5); b = rng.nonzero(-5, 5); } while (Math.abs(a) === Math.abs(b));
    const c = rng.int(-9, 9);
    const p1 = rng.int(-5, 5), p2 = rng.int(-5, 5);
    const m = F(b, a); // perpendicular gradient: original is -a/b
    const ans = F(p2).sub(m.mul(p1));
    const w = [
      num(F(p2).sub(F(-a, b).mul(p1)), 'That uses the parallel gradient $-a/b$, not the perpendicular one.'),
      num(F(p2).sub(m.neg().mul(p1)), 'The perpendicular gradient is the negative reciprocal: $b/a$ here.'),
      num(F(p2).add(m.mul(p1)), 'Sign slip substituting the point: $c = y_1 - m x_1$.'),
    ];
    const opts = choices(rng, num(ans), w, { n: 5, sort: true, fill: nearFill(ans, 4) });
    return {
      stem: `The line $L$ passes through $(${p1}, ${p2})$ and is perpendicular to the line $${poly([[a, 1]], 'x')} ${b > 0 ? '+' : '-'} ${Math.abs(b) === 1 ? '' : Math.abs(b)}y = ${c}$. Where does $L$ cross the $y$-axis? (Give the $y$-coordinate.)`,
      ...opts,
      solution: `Rearranging, the given line has gradient $-\\dfrac{${a}}{${b}} = ${F(-a, b).tex()}$, so a perpendicular line has gradient $${m.tex()}$ (the product of the gradients is $-1$).\n\n$y - ${p2 < 0 ? `(${p2})` : p2} = ${m.tex()}\\,(x - ${p1 < 0 ? `(${p1})` : p1})$. Put $x = 0$: $y = ${p2} - (${m.tex()})(${p1}) = ${ans.tex()}$.`,
      insight: 'Perpendicular gradients multiply to −1; then substitute x = 0 for the intercept.',
      time: 90,
    };
  },
};

const tangentCircle = {
  id: 'tangent-circle', topic: 'coord', paper: 1, levels: [3, 4], skills: ['circles', 'discriminant', 'tangents'],
  name: 'Line tangent to a circle',
  make(rng, level) {
    const m = rng.pick([1, 2, 3, -1, -2]), r = rng.int(1, 5);
    const n = 1 + m * m; // k^2 = r^2 n
    const kTex = surdTex(r, n);
    const w = [
      { key: 'a', text: `$k = \\pm ${r * n}$`, why: 'The discriminant condition gives $k^2 = r^2(1 + m^2)$: take the square root of the whole.' },
      { key: 'b', text: `$k = \\pm ${r}$`, why: 'That ignores the gradient: it only works for horizontal lines.' },
      { key: 'c', text: `$k = ${kTex}$ only`, why: 'There are two parallel tangents, one on each side of the circle.' },
      { key: 'd', text: `$k = \\pm ${surdTex(1, r * r + m * m)}$`, why: 'Expand $(mx + k)^2$ carefully.' },
    ];
    const opts = choices(rng, { key: 'ok', text: `$k = \\pm ${kTex}$` }, w, { n: 5 });
    return {
      stem: `The line $y = ${fx(m, 'x')} + k$ is a tangent to the circle $x^2 + y^2 = ${r * r}$. What are the possible values of $k$?`,
      ...opts,
      solution: `Substitute: $x^2 + (${fx(m, 'x')} + k)^2 = ${r * r}$, i.e. $${n}x^2 + ${2 * m}kx + k^2 - ${r * r} = 0$.\n\nTangent means a repeated root, so the discriminant is zero:\n$$(${2 * m}k)^2 - 4(${n})(k^2 - ${r * r}) = 0 \\implies ${4 * m * m}k^2 - ${4 * n}k^2 + ${4 * n * r * r} = 0 \\implies k^2 = ${r * r * n}.$$\nSo $k = \\pm${kTex}$.\n\nQuicker: the distance from the centre $(0,0)$ to the line $${fx(m, 'x')} - y + k = 0$ must equal the radius: $\\dfrac{|k|}{\\sqrt{${n}}} = ${r}$.`,
      insight: 'Tangency = repeated root = discriminant zero; or, for circles, distance from centre to line = radius.',
      time: 180,
    };
  },
};

const triangleArea = {
  id: 'triangle-area', speedOnly: true, topic: 'coord', paper: 1, levels: [2, 3], skills: ['area', 'coordinates'],
  name: 'Area of a triangle from coordinates',
  make(rng, level) {
    let A, B, C, twice;
    do {
      A = [rng.int(-5, 5), rng.int(-5, 5)]; B = [rng.int(-5, 5), rng.int(-5, 5)]; C = [rng.int(-5, 5), rng.int(-5, 5)];
      twice = A[0] * (B[1] - C[1]) + B[0] * (C[1] - A[1]) + C[0] * (A[1] - B[1]);
    } while (Math.abs(twice) < 6);
    const ans = F(Math.abs(twice), 2);
    const w = [num(Math.abs(twice), 'The shoelace sum gives twice the area: halve it.'), num(F(Math.abs(twice), 4)), num(ans.add(F(1, 2).mul(rng.pick([2, 4, 6]))))];
    const opts = choices(rng, num(ans), w, { n: 5, sort: true, fill: nearFill(ans, 4) });
    const P = p => `(${p[0]}, ${p[1]})`;
    return {
      stem: `What is the area of the triangle with vertices $${P(A)}$, $${P(B)}$ and $${P(C)}$?`,
      ...opts,
      solution: `Shoelace formula: $\\tfrac12\\left|x_1(y_2 - y_3) + x_2(y_3 - y_1) + x_3(y_1 - y_2)\\right|$\n$$= \\tfrac12\\left|${A[0]}(${B[1] - C[1]}) + ${B[0]}(${C[1] - A[1]}) + ${C[0]}(${A[1] - B[1]})\\right| = \\tfrac12\\left|${twice}\\right| = ${ans.tex()}.$$\n\nAlternative: draw the bounding rectangle and subtract the three right-angled triangles around the edge.`,
      insight: 'Shoelace formula, or bounding rectangle minus corner triangles; both avoid finding heights.',
      time: 120,
    };
  },
};

export default [transformPoint, cubicLevel, whichGraph, circleCentre, perpIntercept, tangentCircle, triangleArea];
