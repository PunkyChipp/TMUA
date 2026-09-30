"""Verification for content/questions/graphs.json. Run: python3 content/checks/graphs_check.py"""
import json, os, subprocess, itertools
import sympy as sp

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
Q = {q['id']: q for q in json.load(open(os.path.join(ROOT, 'content/questions/graphs.json'), encoding='utf-8'))}
x, t, k = sp.symbols('x t k', real=True)

# ---------- structural checks ----------
assert len(Q) == 18 and sorted(Q) == [f'graphs-{i:02d}' for i in range(1, 19)]
diffs = sorted(q['difficulty'] for q in Q.values())
assert diffs == [1]*2 + [2]*4 + [3]*6 + [4]*4 + [5]*2, diffs
for q in Q.values():
    assert 4 <= len(q['options']) <= 8
    assert 0 <= q['answer'] < len(q['options'])
    ops = [json.dumps(o, sort_keys=True) for o in q['options']]
    assert len(set(ops)) == len(ops), q['id']
    assert len(q['distractors']) >= 2
    for key in q['distractors']:
        assert int(key) != q['answer'] and int(key) < len(q['options']), (q['id'], key)

# ---------- plot expressions: compile with the app's own compiler ----------
def collect_fns(obj):
    if isinstance(obj, dict):
        if 'fn' in obj:
            yield obj['fn']
        for v in obj.values():
            yield from collect_fns(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from collect_fns(v)

fns = sorted(set(itertools.chain.from_iterable(collect_fns(q) for q in Q.values())))
samples = [-2.7, -1.3, -0.4, 0.35, 0.8, 1.6, 2.9]
js = ("import {compileExpr} from '%s/src/render/plot.js';"
      "const fns=%s, xs=%s; const out={};"
      "for (const f of fns) out[f]=xs.map(v=>compileExpr(f)(v));"
      "console.log(JSON.stringify(out));") % (ROOT, json.dumps(fns), json.dumps(samples))
res = json.loads(subprocess.run(['node', '--input-type=module', '-e', js], capture_output=True,
                                text=True, check=True).stdout)
for f in fns:
    e = sp.sympify(f.replace('^', '**'), locals={'x': x})
    for xv, jv in zip(samples, res[f]):
        pv = float(e.subs(x, xv))
        assert abs(pv - jv) < 1e-9 * max(1, abs(pv)), (f, xv, pv, jv)

def plot_fn(opt):
    fs = {c['fn'] for c in opt['plot']['curves']}
    assert len(fs) == 1
    return sp.sympify(fs.pop().replace('^', '**'), locals={'x': x})

def check_plot_q(qid, target):
    q = Q[qid]
    exprs = [plot_fn(o) for o in q['options']]
    # exactly one option equals the target; all options pairwise different
    matches = [i for i, e in enumerate(exprs) if sp.simplify(e - target) == 0]
    assert matches == [q['answer']], (qid, matches)
    for a, b in itertools.combinations(exprs, 2):
        assert sp.simplify(a - b) != 0
        # clearly distinguishable: differ by > 0.5 somewhere visible
        assert max(abs(float((a - b).subs(x, v))) for v in [-2.5, -1.5, -0.5, 0, 0.5, 2.5]) > 0.5

def nroots(expr, var=x):
    """distinct real roots of polynomial/rational equation expr=0"""
    sols = sp.solveset(sp.Eq(expr, 0), var, sp.S.Reals)
    if sols == sp.S.EmptySet:
        return sols
    assert isinstance(sols, sp.FiniteSet), sols
    return sols

def count_abs_eq(lhs, rhs):
    """count distinct real solutions of lhs = rhs where lhs, rhs may contain Abs (piecewise via cases)"""
    sols = sp.solveset(sp.Eq(lhs, rhs), x, sp.S.Reals)
    if sols == sp.S.EmptySet:
        return 0
    assert isinstance(sols, sp.FiniteSet), sols
    return len(sols)

# 01: f(2)=3; which point on y=f(x-1)+2
q = Q['graphs-01']
pts = [(1, 1), (1, 5), (2, 5), (3, 1), (3, 5)]
fs = [lambda u: u + 1, lambda u: 3 * u - 3, lambda u: u**2 - 1]  # all with f(2)=3
must = [all(f(px - 1) + 2 == py for f in fs) for px, py in pts]
assert must.index(True) == q['answer'] and sum(must) == 1

# 02
check_plot_q('graphs-02', (x - 1)**2 * (x + 2))
# 03
assert len(nroots(x**3 - 4*x - 3)) == 3 and 0 not in nroots(x**3 - 4*x - 3)
assert Q['graphs-03']['options'][Q['graphs-03']['answer']] == '$3$'

# 04: transformations: compose substitutions
fX = sp.Function('f')
def translate(expr, a):  # by (a,0)
    return expr.subs(x, x - a)
def stretch(expr, s):  # parallel to x-axis sf s
    return expr.subs(x, x / s)
base = fX(x)
seqs = [stretch(translate(base, -3), sp.Rational(1, 2)),
        stretch(translate(base, -6), sp.Rational(1, 2)),
        translate(stretch(base, sp.Rational(1, 2)), -6),
        translate(stretch(base, 2), -3),
        stretch(translate(base, 3), sp.Rational(1, 2))]
ok = [sp.simplify(s - fX(2*x + 6)) == 0 for s in seqs]
assert ok.index(True) == Q['graphs-04']['answer'] and sum(ok) == 1

# 05: (4,-2) on f -> y=3f(2x-2)+1
pts = [(1, -5), (3, -7), (3, -5), (3, -3), (10, -5)]
fs = [lambda u: u - 6, lambda u: -u**2 / 8, lambda u: 2 - u]  # f(4)=-2
must = [all(3 * f(2*px - 2) + 1 == py for f in fs) for px, py in pts]
assert must.index(True) == Q['graphs-05']['answer'] and sum(must) == 1

# 06
check_plot_q('graphs-06', 1/(x - 1) + 2)

# 07: f' of given f
F7 = x**3/3 - x**2/2 - 2*x
assert sp.factor(sp.diff(F7, x)) == (x + 1)*(x - 2)
fig = Q['graphs-07']['figure']['plot']
assert all(c['fn'] == 'x^3/3-x^2/2-2*x' for c in fig['curves'])
assert sp.solve(sp.diff(F7, x), x) == [-1, 2]
check_plot_q('graphs-07', sp.diff(F7, x))

# 08: f(|x|)=k
f8 = lambda u: u**2 - 4*u + 3
def c8(kv):
    return count_abs_eq(f8(sp.Abs(x)), kv)
assert c8(3) == 3 and c8(-1) == 2 and c8(0) == 4
truth = (True, True, False)
ROM = {(False, False, False): 0, (True, False, False): 1, (False, True, False): 2, (False, False, True): 3,
       (True, True, False): 4, (True, False, True): 5, (False, True, True): 6, (True, True, True): 7}
assert ROM[truth] == Q['graphs-08']['answer']

# 09
assert count_abs_eq(sp.Abs(x**2 - 2*x - 3), x + 1) == 3
assert set(sp.solveset(sp.Eq(sp.Abs(x**2 - 2*x - 3), x + 1), x, sp.S.Reals)) == {-1, 2, 4}
assert Q['graphs-09']['options'][Q['graphs-09']['answer']] == '$3$'

# 10: f=(x-a)^2(x-b), 0<a<b ; test many (a,b)
import random
random.seed(1)
for _ in range(30):
    a = sp.Rational(random.randint(1, 20), random.randint(1, 5))
    b = a + sp.Rational(random.randint(1, 20), random.randint(1, 5))
    f = (x - a)**2 * (x - b)
    # I: local max at a (f'' < 0)
    assert sp.diff(f, x).subs(x, a) == 0 and sp.diff(f, x, 2).subs(x, a) < 0
    # II false: negative at midpoint
    assert f.subs(x, (a + b) / 2) < 0
    # III: sign changes only at b
    eps = sp.Rational(1, 1000)
    assert sp.sign(f.subs(x, a - eps)) == sp.sign(f.subs(x, a + eps))
    assert sp.sign(f.subs(x, b - eps)) != sp.sign(f.subs(x, b + eps))
assert ROM[(True, False, True)] == Q['graphs-10']['answer']

# 11
check_plot_q('graphs-11', 1/(x**2 - 1))

# 12: y=x^2 translate (2,-1) then stretch x sf 1/2
y12 = sp.expand(((x - 2)**2 - 1).subs(x, 2*x))
cands = [x**2/4 - 2*x + 3, 4*x**2 - 16*x + 15, 4*x**2 - 8*x + 3, 4*x**2 - 8*x + 5, 4*x**2 + 8*x + 3]
ok = [sp.expand(c - y12) == 0 for c in cands]
assert ok.index(True) == Q['graphs-12']['answer'] and sum(ok) == 1
assert sp.expand(((2*(x - 2))**2 - 1)) == cands[1]  # stretch-first slip

# 13: |x^2-4| = x+k has exactly 3 solutions
def c13(kv):
    return count_abs_eq(sp.Abs(x**2 - 4), x + kv)
assert c13(2) == 3 and c13(sp.Rational(17, 4)) == 3 and c13(-2) == 1
for kv in [sp.Rational(n, 8) for n in range(-40, 60)]:
    n = c13(kv)
    assert (n == 3) == (kv in (2, sp.Rational(17, 4))), (kv, n)
assert c13(3) == 4
assert Q['graphs-13']['answer'] == 2

# 14: f'(x) = (x+2)(x-1)^2
fp = (x + 2)*(x - 1)**2
assert all(c['fn'] == '(x+2)*(x-1)^2' for c in Q['graphs-14']['figure']['plot']['curves'])
ff = sp.integrate(fp, x)
assert ff.subs(x, 0) < ff.subs(x, 1)  # III false
assert fp.subs(x, -2.1) < 0 < fp.subs(x, -1.9)  # II min
assert fp.subs(x, 0.9) > 0 and fp.subs(x, 1.1) > 0  # I inflection
assert ROM[(True, True, False)] == Q['graphs-14']['answer']

# 15: f with max (1,4), min (5,-2); y = 1 - 2 f(3 - x/2)
a15 = sp.Rational(9, 16)
f15 = a15*(x**3/3 - 3*x**2 + 5*x)
f15 = f15 - f15.subs(x, 1) + 4
assert f15.subs(x, 5) == -2 and sp.solve(sp.diff(f15, x), x) == [1, 5]
g15 = 1 - 2*f15.subs(x, 3 - x/2)
st = sp.solve(sp.diff(g15, x), x)
maxima = [(s, g15.subs(x, s)) for s in st if sp.diff(g15, x, 2).subs(x, s) < 0]
assert maxima == [(-4, 5)], maxima
opts15 = [(-4, -7), (-4, 5), (1, 5), (4, -7), (4, 5)]
assert opts15.index((-4, 5)) == Q['graphs-15']['answer']

# 16: y=k meets 1/(x^2-2x-3) at exactly two points
def c16(kv):
    if kv == 0:
        return 0
    return len(nroots(x**2 - 2*x - 3 - 1/kv))
for kv in [sp.Rational(n, 16) for n in range(-80, 80)]:
    expected = 2 if (kv < -sp.Rational(1, 4) or kv > 0) else None
    n = c16(kv)
    assert (n == 2) == (expected == 2), (kv, n)
assert c16(-sp.Rational(1, 4)) == 1
assert Q['graphs-16']['answer'] == 2

# 17: sufficiency; counterexamples for I, II; III checked on sample odd, nonneg-on-right functions
def same(f):
    return all(abs(float(f(sp.Abs(v)) - sp.Abs(f(v)))) < 1e-12 for v in [sp.Rational(n, 3) for n in range(-9, 10)])
assert not same(lambda u: sp.exp(u))           # I fails
assert not same(lambda u: u**2 - 1)            # II fails
for f in [lambda u: u, lambda u: u**3, lambda u: u*sp.Abs(u), lambda u: sp.sin(u) + u, lambda u: u**3 + 2*u]:
    assert same(f)
# III general proof in solution; also check odd functions nonneg on x>=0 above satisfy condition
assert ROM[(False, False, True)] == Q['graphs-17']['answer']

# 18: f(f(x)) = 2 with f = x^3-3x
f18 = lambda u: u**3 - 3*u
sols = set(sp.Poly(f18(f18(x)) - 2, x).real_roots())
assert len(sols) == 5
assert Q['graphs-18']['options'][Q['graphs-18']['answer']] == '$5$'

print('ALL OK')
