"""Verification for content/questions/graphs.json. Run: python3 content/checks/graphs_check.py"""
import json, os, subprocess, itertools, math, random
import sympy as sp

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
QL = json.load(open(os.path.join(ROOT, 'content/questions/graphs.json'), encoding='utf-8'))
Q = {q['id']: q for q in QL}
x, t, k = sp.symbols('x t k', real=True)
ROMAN = ["none of them", "I only", "II only", "III only", "I and II only", "I and III only",
         "II and III only", "I, II and III"]
ROM = {(False, False, False): 0, (True, False, False): 1, (False, True, False): 2, (False, False, True): 3,
       (True, True, False): 4, (True, False, True): 5, (False, True, True): 6, (True, True, True): 7}


def key(qid):
    return Q[qid]['answer']


# ---------------------------------------------------------------- structure
base = [f'graphs-{i:02d}' for i in range(1, 19)]
assert sorted(Q) == sorted(base + [b + 'b' for b in base]) and len(QL) == 36
diffs = sorted(Q[i]['difficulty'] for i in base)
assert diffs == [2] * 2 + [3] * 6 + [4] * 7 + [5] * 3, diffs
for i in base:
    a, b = Q[i], Q[i + 'b']
    assert a['family'] == i and b['family'] == i
    assert a['difficulty'] == b['difficulty'] and a['paper'] == b['paper']
    assert a['answer'] != b['answer'], i
for q in QL:
    n = len(q['options'])
    assert q['difficulty'] >= 2
    assert n == 5 or (n == 8 and q['options'] == ROMAN), q['id']
    assert 0 <= q['answer'] < n
    ops = [json.dumps(o, sort_keys=True) for o in q['options']]
    assert len(set(ops)) == n, q['id']
    assert len(q['distractors']) >= 3, q['id']
    for kk in q['distractors']:
        assert int(kk) != q['answer'] and int(kk) < n, (q['id'], kk)
    # numeric options ascending
    vals = []
    for o in q['options']:
        if isinstance(o, str) and o.startswith('$') and o.endswith('$') and o.count('$') == 2:
            try:
                vals.append(float(sp.sympify(o.strip('$'))))
            except Exception:
                vals = None
                break
        else:
            vals = None
            break
    if vals:
        assert vals == sorted(vals), q['id']
    # no control characters from unescaped backslashes (e.g. "\tfrac" read as TAB + "frac")
    def strings(o):
        if isinstance(o, str):
            yield o
        elif isinstance(o, dict):
            for v in o.values():
                yield from strings(v)
        elif isinstance(o, list):
            for v in o:
                yield from strings(v)
    assert not any(ch in st for st in strings(q) for ch in '\t\b\f\r\v'), q['id']

# ---------------------------------------------------------------- plot expressions
def collect_fns(obj):
    if isinstance(obj, dict):
        if 'fn' in obj:
            yield obj['fn']
        for v in obj.values():
            yield from collect_fns(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from collect_fns(v)


def sym(fn):
    return sp.sympify(fn.replace('^', '**'), locals={'x': x, 'e': sp.E, 'ln': sp.log, 'abs': sp.Abs})


def num(fn):
    f = sp.lambdify(x, sym(fn), modules=[{'sqrt': lambda v: math.sqrt(v) if v >= 0 else float('nan')}, 'math'])

    def g(v):
        try:
            r = f(v)
            return float(r) if isinstance(r, (int, float)) and math.isfinite(r) else float('nan')
        except (ValueError, ZeroDivisionError, OverflowError, TypeError):
            return float('nan')
    return g


fns = sorted(set(itertools.chain.from_iterable(collect_fns(q) for q in QL)))
samples = [-2.7, -1.3, -0.4, 0.35, 0.8, 1.6, 2.9, 4.2]
js = ("import {compileExpr} from '%s/src/render/plot.js';"
      "const fns=%s, xs=%s; const out={};"
      "for (const f of fns) out[f]=xs.map(v=>{const r=compileExpr(f)(v); return Number.isFinite(r)?r:null;});"
      "console.log(JSON.stringify(out));") % (ROOT, json.dumps(fns), json.dumps(samples))
res = json.loads(subprocess.run(['node', '--input-type=module', '-e', js], capture_output=True,
                                text=True, check=True).stdout)
for f in fns:
    g = num(f)
    for xv, jv in zip(samples, res[f]):
        pv = g(xv)
        if math.isnan(pv):
            assert jv is None, (f, xv, jv)
        else:
            assert jv is not None and abs(pv - jv) < 1e-9 * max(1, abs(pv)), (f, xv, pv, jv)


def visible(plot, fn, N=600):
    (x0, x1), (y0, y1) = plot['x'], plot['y']
    g = num(fn)
    out = []
    for i in range(N + 1):
        xv = x0 + (x1 - x0) * (i + 0.5) / (N + 1)
        yv = g(xv)
        out.append(None if math.isnan(yv) or yv < y0 or yv > y1 else yv)
    return out


def distinct(plot, f1, f2):
    """clearly distinguishable: >=4% of the x-range where one shows and the other doesn't, or the
    two visible curves are > 8% of the y-range apart."""
    a, b = visible(plot, f1), visible(plot, f2)
    yr = plot['y'][1] - plot['y'][0]
    one = sum((u is None) != (v is None) for u, v in zip(a, b))
    gap = max([abs(u - v) for u, v in zip(a, b) if u is not None and v is not None] or [0])
    return one > 0.04 * len(a) or gap > 0.08 * yr


def plot_options(qid):
    q = Q[qid]
    fs = []
    for o in q['options']:
        assert len(o['plot']['curves']) == 1
        fs.append(o['plot']['curves'][0]['fn'])
    for i, j in itertools.combinations(range(len(fs)), 2):
        assert distinct(q['options'][i]['plot'], fs[i], fs[j]), (qid, fs[i], fs[j])
    return fs


def check_plot_q(qid, target, domain=None):
    """exactly the keyed option equals target (numerically on the window, including where undefined)."""
    q = Q[qid]
    fs = plot_options(qid)
    (x0, x1) = domain or q['options'][0]['plot']['x']
    tg = sp.lambdify(x, target, modules=[{'sqrt': lambda v: math.sqrt(v) if v >= 0 else float('nan')}, 'math'])
    xs = [x0 + (x1 - x0) * (i + 0.37) / 300 for i in range(300)]
    def tv(v):
        try:
            r = float(tg(v))
            return r if math.isfinite(r) else float('nan')
        except (ValueError, OverflowError, ZeroDivisionError):
            return float('nan')
    match = []
    for i, f in enumerate(fs):
        g = num(f)
        ok = all((math.isnan(g(v)) and math.isnan(tv(v))) or abs(g(v) - tv(v)) < 1e-9 for v in xs)
        match.append(ok)
    assert match.count(True) == 1 and match.index(True) == q['answer'], (qid, match)


def real_roots_distinct(poly):
    return sorted(set(sp.Poly(sp.expand(poly), x).real_roots()))


# ---------------------------------------------------------------- 01, 01b
check_plot_q('graphs-01', 2 - sp.sqrt(4 - x))
check_plot_q('graphs-01b', 3 - 2 * sp.sqrt(x + 1))
# ---------------------------------------------------------------- 02, 02b
check_plot_q('graphs-02', 5 - 4 * 2**(-x), domain=(0, 6))
assert (5 - 4 * 2**(-x)).subs(x, 0) == 1 and sp.limit(5 - 4 * 2**(-x), x, sp.oo) == 5
check_plot_q('graphs-02b', 9 - 3**x, domain=(0, 2))
assert (9 - 3**x).subs(x, 0) == 8 and (9 - 3**x).subs(x, 2) == 0 and (9 - 3**x).subs(x, 1) == 6
# ---------------------------------------------------------------- 03, 03b
r = real_roots_distinct(x**3 - 4 * x - 3)
assert len(r) == 3 and 0 not in r and Q['graphs-03']['options'][key('graphs-03')] == '$3$'
r = real_roots_distinct(x**3 - 3 * x + 2)
assert r == [-2, 1] and Q['graphs-03b']['options'][key('graphs-03b')] == '$2$'
assert all(sp.simplify((3 - x**2) - 2 / x).subs(x, v) == 0 for v in r)

# ---------------------------------------------------------------- 04, 04b transformations
F = sp.Function('f')
def T(a, b=0):  # translate by (a,b)
    return lambda e: e.subs(x, x - a) + b
def SX(s):  # stretch parallel to x-axis, sf s
    return lambda e: e.subs(x, x / s)
def SY(s):
    return lambda e: s * e
RY = lambda e: e.subs(x, -x)   # reflect in y-axis
RX = lambda e: -e              # reflect in x-axis
def run(seq, e):
    for s in seq:
        e = s(e)
    return sp.expand(e)
h = sp.Rational(1, 2)
seqs4 = [[SX(h), RY, T(-3)], [SX(h), RY, T(3)], [SX(h), T(-6), RY], [SX(2), RY, T(3)], [T(6), RY, SX(h)]]
ok = [sp.simplify(run(s, F(x)) - F(6 - 2 * x)) == 0 for s in seqs4]
assert ok.count(True) == 1 and ok.index(True) == key('graphs-04'), ok
seqs4b = [[SX(2), T(0, 3), RX], [SX(h), RX, T(0, 3)], [T(0, 3), RY, SX(2)], [T(0, -3), RX, SX(2)], [RX, T(0, -3), SX(2)]]
ok = [sp.simplify(run(s, F(x)) - (3 - F(x / 2))) == 0 for s in seqs4b]
assert ok.count(True) == 1 and ok.index(True) == key('graphs-04b'), ok

# ---------------------------------------------------------------- 05, 05b  y=a(x+b)^2+c
a_, b_, c_ = sp.symbols('a b c')
fig = Q['graphs-05']['figure']['plot']['curves'][0]['fn']
assert sp.expand(sym(fig) - (-(x - 2)**2 + 3)) == 0
preds5 = [lambda a, b, c: b < 0 and a * b * b + c < 0, lambda a, b, c: a > 0 and c > 0,
          lambda a, b, c: a < 0 and b > 0, lambda a, b, c: b < 0 and c < 0,
          lambda a, b, c: c > 0 and a * b * b + c > 0]
random.seed(1)
cnt = 0
while cnt < 2000:   # every parabola with the pictured features: opens down, vertex in Q1, y-intercept < 0
    a, b, c = -random.uniform(0.05, 5), -random.uniform(0.05, 5), random.uniform(0.05, 5)
    if a * b * b + c >= 0:
        continue
    cnt += 1
    tv = [p(a, b, c) for p in preds5]
    assert tv.count(True) == 1 and tv.index(True) == key('graphs-05')
fs = plot_options('graphs-05b')
good = []
for f in fs:
    e = sp.expand(sym(f))
    A = e.coeff(x, 2); B = e.coeff(x, 1) / (2 * A); C = e.subs(x, 0) - A * B**2
    assert sp.expand(A * (x + B)**2 + C - e) == 0
    good.append(bool(A > 0 and B > 0 and C < 0 and A * B**2 + C > 0))
assert good.count(True) == 1 and good.index(True) == key('graphs-05b'), good

# ---------------------------------------------------------------- 06, 06b composites
f6 = lambda u: sp.Abs(u - 1); g6 = lambda u: u**2 - 2 * u
check_plot_q('graphs-06', f6(g6(x)))
f6b = lambda u: u**2 - 4; g6b = lambda u: sp.Abs(u - 1)
check_plot_q('graphs-06b', f6b(g6b(x)))

# ---------------------------------------------------------------- 07, 07b f' from f
F7 = x**3 / 3 - sp.Rational(5, 2) * x**2 + 4 * x + 3
assert sp.expand(sym(Q['graphs-07']['figure']['plot']['curves'][0]['fn']) - F7) == 0
assert sp.solve(sp.diff(F7, x), x) == [1, 4]
for px, py in Q['graphs-07']['figure']['plot']['points']:
    assert abs(float(F7.subs(x, px)) - py) < 1e-3
check_plot_q('graphs-07', sp.diff(F7, x))
F7b = x**4 / 4 - x**3 / 3 - x**2
assert sp.expand(sym(Q['graphs-07b']['figure']['plot']['curves'][0]['fn']) - F7b) == 0
assert sorted(sp.solve(sp.diff(F7b, x), x)) == [-1, 0, 2]
for px, py in Q['graphs-07b']['figure']['plot']['points']:
    assert abs(float(F7b.subs(x, px)) - py) < 1e-3
check_plot_q('graphs-07b', sp.diff(F7b, x))

# ---------------------------------------------------------------- 08, 08b  f(|x|)
def sols_even(fexpr, kv, outer_abs=False):
    """distinct real x with fexpr(|x|) = kv (or |fexpr(|x|)| = kv)."""
    rhs = [kv, -kv] if outer_abs else [kv]
    ts = set()
    for r in set(rhs):
        for rt in sp.Poly(sp.expand(fexpr - r), t).real_roots():
            if rt >= 0:
                ts.add(rt)
    xs = set()
    for tt in ts:
        xs.add(tt); xs.add(-tt)
    return xs
f8 = t**2 - 4 * t + 3
I8 = len(sols_even(f8, 3, True)) == 3
II8 = len(sols_even(f8, 1, True)) == 4
assert len(sols_even(f8, 1, True)) == 6
III8 = len(sols_even(f8, sp.Rational(1, 2), True)) == 8
assert ROM[(I8, II8, III8)] == key('graphs-08')
f8b = t**3 - 3 * t
I = len(sols_even(f8b, -1)) == 4
II = len(sols_even(f8b, 2)) == 3
III = len(sols_even(f8b, 0)) == 2
assert ROM[(I, II, III)] == key('graphs-08b')

# ---------------------------------------------------------------- 09, 09b
s9 = sp.solveset(sp.Eq(sp.Abs(x**2 - 2 * x - 3), x + 1), x, sp.S.Reals)
assert set(s9) == {-1, 2, 4} and Q['graphs-09']['options'][key('graphs-09')] == '$3$'
s9b = sp.solveset(sp.Eq(sp.Abs(x**2 - 4), 3 * x), x, sp.S.Reals)
assert set(s9b) == {1, 4} and Q['graphs-09b']['options'][key('graphs-09b')] == '$2$'

# ---------------------------------------------------------------- 10, 10b possible numbers of roots
def count_profile(hpoly):
    """{c: number of distinct real roots of hpoly = c} at every critical value and in every gap."""
    crit = sorted(set(hpoly.subs(x, r) for r in sp.Poly(sp.diff(hpoly, x), x).real_roots()))
    pts = list(crit)
    pts += [crit[0] - 1, crit[-1] + 1] + [(a + b) / 2 for a, b in zip(crit, crit[1:])]
    return {c: len(real_roots_distinct(hpoly - c)) for c in pts}, crit
prof, crit = count_profile((x**2 - 2 * x)**2)          # p(x)=0  <=>  h(x) = -k
assert crit == [0, 1]
counts = set(prof.values())
assert counts == {0, 2, 3, 4}
I = 1 in counts
II = 3 in counts
III = all(v >= 2 for c, v in prof.items() if c > 0)    # k<0  <=>  c=-k>0
assert ROM[(I, II, III)] == key('graphs-10')
prof, crit = count_profile(x**4 - 4 * x**3)
assert crit == [-27, 0]
counts = set(prof.values())
assert counts == {0, 1, 2}
I = 1 in counts
II = 3 in counts
III = all(v == 2 for c, v in prof.items() if c > 0)
assert ROM[(I, II, III)] == key('graphs-10b')

# ---------------------------------------------------------------- 11, 11b
def sign_changes(fun, a, b, N=200000):
    cnt, prev = 0, None
    for i in range(N + 1):
        v = fun(a + (b - a) * (i + 0.123) / (N + 1))
        s = v > 0
        if prev is not None and s != prev:
            cnt += 1
        prev = s
    return cnt
h11 = lambda v: abs(math.log(v)) - abs(v - 2)
assert sign_changes(h11, 1e-12, 60) == 3
assert h11(1e-12) > 0 and all(v - 2 - math.log(v) > 0 for v in [60, 100, 1e4, 1e8])  # stays apart for x>60
assert Q['graphs-11']['options'][key('graphs-11')] == '$3$'
# proof of exactly 3 for |ln x| = |x-2|: one strictly monotone difference on each of (0,1), [1,2], (2,oo)
def strictly(expr, lo, hi, sign):   # derivative of expr has fixed strict sign on the open interval
    d = sp.diff(expr, x)
    bad = sp.solveset(d <= 0 if sign > 0 else d >= 0, x, sp.Interval.open(lo, hi))
    return bad == sp.S.EmptySet
m = x - sp.log(x) - 2                # (0,1): -ln x = 2 - x
assert strictly(m, 0, 1, -1) and sp.limit(m, x, 0, '+') == sp.oo and m.subs(x, 1) < 0
kk = sp.log(x) + x - 2               # [1,2]: ln x = 2 - x
assert strictly(kk, 1, 2, 1) and kk.subs(x, 1) < 0 and kk.subs(x, 2) > 0
hh = x - 2 - sp.log(x)               # (2,oo): ln x = x - 2
assert strictly(hh, 2, sp.oo, 1) and hh.subs(x, 2) < 0 and hh.subs(x, 4) > 0
h11b = lambda v: abs(2**v - 4) - (v + 1)
assert sign_changes(h11b, -1, 40) == 2 and h11b(1) == 0 and h11b(3) == 0
assert Q['graphs-11b']['options'][key('graphs-11b')] == '$2$'
assert strictly(4 - 2**x - (x + 1), -1, 2, -1) and strictly(2**x - 4 - (x + 1), 2, sp.oo, 1)

# ---------------------------------------------------------------- 12, 12b
fin = run([T(2, -1), RY, SX(h)], x**2)
opts = [4*x**2 + 8*x + 3, 4*x**2 - 8*x + 3, 4*x**2 + 16*x + 15, x**2/4 + 2*x + 3, -4*x**2 + 8*x - 3]
ok = [sp.expand(o - fin) == 0 for o in opts]
assert ok.count(True) == 1 and ok.index(True) == key('graphs-12')
assert sp.expand(run([T(2, -1), RX, SX(h)], x**2) - opts[4]) == 0          # distractor E is the x-axis slip
assert sp.expand(run([RY, T(2, -1), SX(h)], x**2) - opts[1]) == 0          # distractor B: reflection first
fin = run([SY(3), RY, T(1, -2)], sp.sqrt(x))
opts = [3*sp.sqrt(-x-1) - 2, 3*sp.sqrt(x-1) - 2, 3*sp.sqrt(1-x) - 6, -3*sp.sqrt(x-1) - 2, 3*sp.sqrt(1-x) - 2]
ok = [sp.simplify(o - fin) == 0 for o in opts]
assert ok.count(True) == 1 and ok.index(True) == key('graphs-12b')
assert sp.simplify(run([SY(3), T(1, -2), RY], sp.sqrt(x)) - opts[0]) == 0

# ---------------------------------------------------------------- 13, 13b
def count_abs_line(quad, kv):
    s = set()
    for sgn in (1, -1):
        for r in sp.Poly(sp.expand(sgn * quad - (x + kv)), x).real_roots():
            if sgn * quad.subs(x, r) >= 0 and r + kv >= 0:
                s.add(r)
    return len(s)
grid = [sp.Rational(i, 16) for i in range(-112, 129)]
def check_k(qid, quad, want, preds):
    truth = {kv: count_abs_line(quad, kv) == want for kv in grid}
    agree = [all(p(kv) == truth[kv] for kv in grid) for p in preds]
    assert agree.count(True) == 1 and agree.index(True) == key(qid), (qid, agree)
check_k('graphs-13', x**2 - 4, 3,
        [lambda v: v == sp.Rational(17, 4), lambda v: v in (2, sp.Rational(17, 4)), lambda v: v in (-2, 2),
         lambda v: 2 <= v <= sp.Rational(17, 4), lambda v: 2 < v < sp.Rational(17, 4)])
check_k('graphs-13b', x**2 - 2 * x - 3, 4,
        [lambda v: -3 < v < 1, lambda v: v in (1, sp.Rational(13, 4)), lambda v: 1 <= v <= sp.Rational(13, 4),
         lambda v: 1 < v < sp.Rational(13, 4), lambda v: v < sp.Rational(13, 4)])

# ---------------------------------------------------------------- 14, 14b
def gradient_statements(fp, fig_fn):
    assert sp.expand(sym(fig_fn) - fp) == 0
    return sp.integrate(fp, x)
fp = (x + 2) * (x - 1)**2
f14 = gradient_statements(fp, Q['graphs-14']['figure']['plot']['curves'][0]['fn'])
eps = sp.Rational(1, 100)
I = (fp.subs(x, 1 - eps) > 0) != (fp.subs(x, 1 + eps) > 0)          # sign change at 1?
II = fp.subs(x, -2 - eps) < 0 < fp.subs(x, -2 + eps)
III = f14.subs(x, -1) < f14.subs(x, 1)
assert sp.Poly(fp, x).real_roots() == [-2, 1, 1]
assert ROM[(bool(I), bool(II), bool(III))] == key('graphs-14')
fp = -(x + 1) * (x - 3)
f14b = gradient_statements(fp, Q['graphs-14b']['figure']['plot']['curves'][0]['fn'])
I = fp.subs(x, 3 - eps) > 0 > fp.subs(x, 3 + eps)
II = f14b.subs(x, -1) < f14b.subs(x, 3)
III = f14b.subs(x, 0) > f14b.subs(x, 2)
assert ROM[(bool(I), bool(II), bool(III))] == key('graphs-14b')

# ---------------------------------------------------------------- 15, 15b  (build actual cubics)
def stationary(g):
    out = []
    for r in sp.solve(sp.diff(g, x), x):
        s2 = sp.diff(g, x, 2).subs(x, r)
        out.append((r, sp.simplify(g.subs(x, r)), 'max' if s2 < 0 else 'min'))
    return out
c = sp.Rational(9, 16)
f15 = c * (x**3 / 3 - 3 * x**2 + 5 * x) + sp.Rational(43, 16)
assert f15.subs(x, 1) == 4 and f15.subs(x, 5) == -2
st = stationary(1 - 2 * f15.subs(x, 3 - x / 2))
mx = [(a, b) for a, b, n in st if n == 'max']
assert mx == [(-4, 5)]
o = Q['graphs-15']['options'][key('graphs-15')]
assert o == '$(-4, 5)$'
c = -sp.Rational(1, 9)
f15b = sp.integrate(c * (x + 2) * (x - 4), x)
f15b = f15b + 3 - f15b.subs(x, -2)
assert f15b.subs(x, -2) == 3 and f15b.subs(x, 4) == 7
st = stationary(2 * f15b.subs(x, 2 - 2 * x) - 5)
mn = [(a, b) for a, b, n in st if n == 'min']
assert mn == [(2, 1)] and Q['graphs-15b']['options'][key('graphs-15b')] == '$(2, 1)$'
assert [(a, b) for a, b, n in st if n == 'max'] == [(-1, 9)]

# ---------------------------------------------------------------- 16, 16b
g16 = lambda v: 2**v - v * v - 1
assert g16(0) == 0 and g16(1) == 0
assert sign_changes(g16, 0, 60) == 2            # one at t=1, one in (4,5); plus the root at t=0
assert g16(4) < 0 < g16(5) and all(g16(v) > 0 for v in [6, 10, 30, 60])
assert Q['graphs-16']['options'][key('graphs-16')] == '$3$'
# proof: g''' = (ln 2)^3 2^t > 0, so by Rolle g has at most 3 real roots; 0, 1 and one in (4,5) are 3
G = 2**x - x**2 - 1
assert sp.simplify(sp.diff(G, x, 3) - sp.log(2)**3 * 2**x) == 0
assert G.subs(x, 0) == 0 and G.subs(x, 1) == 0 and G.subs(x, 4) < 0 < G.subs(x, 5)
g16b = lambda v: 3**v - 9 * v
assert sign_changes(g16b, -50, 50) == 2 and g16b(3) == 0
assert Q['graphs-16b']['options'][key('graphs-16b')] == '$2$'
# proof: (3^x - 9x)'' = (ln 3)^2 3^x > 0 (convex) so at most 2 roots; x = 3 and one in (0,1)
G = 3**x - 9 * x
assert sp.simplify(sp.diff(G, x, 2) - sp.log(3)**2 * 3**x) == 0
assert G.subs(x, 3) == 0 and G.subs(x, 0) > 0 > G.subs(x, 1)
assert '\\tfrac12' in Q['graphs-04']['options'][4]

# ---------------------------------------------------------------- 17, 17b
pts = [i / 7 for i in range(-30, 31)]
same = lambda f: all(abs(f(abs(v)) - abs(f(v))) < 1e-12 for v in pts)
assert not same(math.exp) and all(math.exp(v) >= 0 for v in pts)           # I not sufficient
assert not same(lambda v: v * v - 1)                                         # II not sufficient (even)
for f in [lambda v: v**3, lambda v: v * abs(v), lambda v: math.sin(v) * 0 + v**5 + v, lambda v: math.atan(v)]:
    assert same(f)                                                           # III examples hold
assert ROM[(False, False, True)] == key('graphs-17')
# 17b: |f| symmetric for even, odd, and any f with f(|x|)=|f(x)|
sym_abs = lambda f: all(abs(abs(f(-v)) - abs(f(v))) < 1e-12 for v in pts)
for f in [lambda v: v * v - 3, math.cos, lambda v: v**4 - 5 * v * v]:
    assert sym_abs(f)
for f in [lambda v: v**3 - 4 * v, math.sin, lambda v: v * abs(v) - v]:
    assert sym_abs(f)
for f in [lambda v: v**3, lambda v: v * v, lambda v: v + 1 if v >= 0 else (v - 1 if v < 0 else 0)]:
    if same(f):
        assert sym_abs(f)
u = sp.Function('u')
assert sp.simplify(sp.Abs(u(sp.Abs(-x))) - sp.Abs(u(sp.Abs(x)))) == 0
assert ROM[(True, True, True)] == key('graphs-17b')

# ---------------------------------------------------------------- 18, 18b
f18 = lambda e: e**3 - 3 * e
assert len(real_roots_distinct(f18(f18(x)) - 2)) == 5
assert Q['graphs-18']['options'][key('graphs-18')] == '$5$'
assert sp.expand(sym(Q['graphs-18']['figure']['plot']['curves'][0]['fn']) - f18(x)) == 0
f18b = lambda e: e**2 - 2 * e
assert len(real_roots_distinct(f18b(f18b(x)) - 3)) == 3
assert Q['graphs-18b']['options'][key('graphs-18b')] == '$3$'

print('ALL OK')
