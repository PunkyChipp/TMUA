"""Independent verification of content/questions/diff.json. Run: python3 content/checks/diff_check.py"""
import json, os, random
from fractions import Fraction as F
import sympy as sp

x, t, k, a, b, c, d, u = sp.symbols("x t k a b c d u", real=True)
HERE = os.path.dirname(os.path.abspath(__file__))
QS = {q["id"]: q for q in json.load(open(os.path.join(HERE, "..", "questions", "diff.json"), encoding="utf-8"))}
assert len(QS) == 18 and sorted(QS) == [f"diff-{i:02d}" for i in range(1, 19)]
diffs = sorted(q["difficulty"] for q in QS.values())
assert diffs == [1]*2 + [2]*4 + [3]*6 + [4]*4 + [5]*2, diffs
for q in QS.values():
    assert len(set(q["options"])) == len(q["options"]) and 4 <= len(q["options"]) <= 8
    assert 0 <= q["answer"] < len(q["options"])
    for key in q["distractors"]:
        assert int(key) != q["answer"] and int(key) < len(q["options"]), q["id"]


def numeric(qid, values, truth):
    """values: sympy values of options in order; exactly one equals truth and it is keyed."""
    q = QS[qid]
    assert len(values) == len(q["options"]), qid
    vals = [sp.nsimplify(v) for v in values]
    assert all(float(vals[i]) < float(vals[i + 1]) for i in range(len(vals) - 1)), qid + " not ascending"
    hits = [i for i, v in enumerate(vals) if sp.simplify(v - truth) == 0]
    assert hits == [q["answer"]], (qid, hits, truth)


def keyed(qid, idx):
    assert QS[qid]["answer"] == idx, (qid, QS[qid]["answer"], idx)


ROMAN = [(), (1,), (2,), (3,), (1, 2), (1, 3), (2, 3), (1, 2, 3)]


def roman(qid, truths):
    true_set = tuple(i + 1 for i, v in enumerate(truths) if v)
    keyed(qid, ROMAN.index(true_set))


# diff-01
y = 4*sp.sqrt(x) - 8/x
numeric("diff-01", [F(1, 2), 1, F(3, 2), 2, F(5, 2)], sp.diff(y, x).subs(x, 4))

# diff-02
f = x**3 - 6*x**2 + 9*x + 1
st = sp.solve(sp.diff(f, x), x)
mins = [s for s in st if sp.diff(f, x, 2).subs(x, s) > 0]
numeric("diff-02", [-15, 0, 1, 3, 5], f.subs(x, mins[0]))

# diff-03
f = x**3; P = (1, 1); m = sp.diff(f, x).subs(x, 1)
A = sp.solve(1 + m*(x - 1), x)[0]; B = sp.solve(1 - (x - 1)/m, x)[0]
numeric("diff-03", [F(1, 3), F(4, 3), F(5, 3), 2, F(10, 3)], sp.Rational(1, 2)*abs(B - A)*1)

# diff-04: decreasing set
f = x**sp.Rational(3, 2) - 3*x
dec = sp.solve_univariate_inequality(sp.diff(f, x) < 0, x, relational=False).intersect(sp.Interval.open(0, sp.oo))
assert dec == sp.Interval.open(0, 4)
keyed("diff-04", 1)

# diff-05
f = x**4 - 4*x**3
f1, f2 = sp.diff(f, x), sp.diff(f, x, 2)
I = f1.subs(x, 0) == 0 and f2.subs(x, 0) == 0
II = f1.subs(x, -0.1) > 0 and f1.subs(x, 0.1) < 0
III = sp.minimum(f, x) == -27
roman("diff-05", [I, II, III])


# diff-06: no local max/min  <=> f' never changes sign
def has_turning(kv):
    fp = sp.Poly(3*x**2 + 2*kv*x + 3, x)
    roots = [r for r in sp.real_roots(fp)]
    return len(set(roots)) == 2  # distinct real roots => sign changes
set_true = [kv for kv in [sp.Rational(n, 4) for n in range(-60, 61)] if not has_turning(kv)]
assert min(set_true) == -3 and max(set_true) == 3 and len(set_true) == 25
keyed("diff-06", 4)

# diff-07
A_ = 2*a*(12 - a**2)
crit = [s for s in sp.solve(sp.diff(A_, a), a) if s > 0]
numeric("diff-07", [16, 24, 32, 36, 48], max(A_.subs(a, s) for s in crit))

# diff-08
ts = sp.solve(sp.Eq(-3, 2*t*1 - t**2), t)
(xa, ya), (xb, yb) = [(s, s**2) for s in ts]
area = sp.Rational(1, 2)*abs((xa - 1)*(yb + 3) - (xb - 1)*(ya + 3))
numeric("diff-08", [8, 12, 16, 24, 32], area)

# diff-09: f' = (x+1)(x-2)^2
fp = (x + 1)*(x - 2)**2
f = sp.integrate(fp, x)
I = fp.subs(x, -1.1) < 0 and fp.subs(x, -0.9) > 0
II = fp.subs(x, 1.9) > 0 and fp.subs(x, 2.1) < 0
III = f.subs(x, 0) > f.subs(x, 2)
roman("diff-09", [I, II, III])

# diff-10
curve = x**2 - 4*x
mn = -1/sp.diff(curve, x).subs(x, 1)
sols = sp.solve(sp.Eq(curve, -3 + mn*(x - 1)), x)
other = [s for s in sols if s != 1]
numeric("diff-10", [2, F(5, 2), 3, F(7, 2), 5], other[0])


# diff-11: x^3-3x+k three distinct real roots
def nroots(poly):
    return len(set(sp.real_roots(sp.Poly(poly, x))))
good = [kv for kv in [sp.Rational(n, 4) for n in range(-16, 17)] if nroots(x**3 - 3*x + kv) == 3]
assert min(good) == sp.Rational(-7, 4) and max(good) == sp.Rational(7, 4) and nroots(x**3 - 3*x + 2) == 2
keyed("diff-11", 1)

# diff-12: I false by x^3; II, III true (standard theorems)
g = x**3
assert sp.diff(g, x).subs(x, 0) == 0 and all(sp.diff(g, x).subs(x, v) > 0 for v in (-0.1, 0.1))
roman("diff-12", [False, True, True])

# diff-13: exact condition p^2>3q. Check option classifications by sampling
random.seed(1)
samples = [(F(random.randint(-40, 40), 4), F(random.randint(-40, 40), 4)) for _ in range(5000)]
samples += [(F(1), F(1, 2)), (F(3), F(1)), (F(0), F(1)), (F(1), F(1)), (F(0), F(-1))]
exact = lambda p, q: p*p > 3*q
conds = [lambda p, q: p*p > 3*q, lambda p, q: p*p > q, lambda p, q: q < 0,
         lambda p, q: q > 0, lambda p, q: p > 0, lambda p, q: p*p < 3*q]
def classify(cond):
    suff = all(exact(p, q) for p, q in samples if cond(p, q))
    nec = all(cond(p, q) for p, q in samples if exact(p, q))
    return suff, nec
cls = [classify(cd) for cd in conds]
hits = [i for i, (s, n) in enumerate(cls) if s and not n]
assert hits == [2], cls
keyed("diff-13", 2)


# diff-14: number of distinct tangents to y=x^3-x through (a,0)
def ntangents(av):
    return len(set(sp.real_roots(sp.Poly(2*t**3 - 3*av*t**2 + av, t))))
# confirm derived equation
tan_eq = sp.expand((3*t**2 - 1)*(a - t) + t**3 - t)
assert sp.expand(tan_eq + (2*t**3 - 3*a*t**2 + a)) == 0
grid = [sp.Rational(n, 8) for n in range(-24, 25)]
three = [av for av in grid if ntangents(av) == 3]
assert all(abs(av) > 1 for av in three) and all(ntangents(av) != 3 for av in grid if abs(av) <= 1)
assert set(three) == {av for av in grid if abs(av) > 1}
assert ntangents(1) == 2 and ntangents(-1) == 2
keyed("diff-14", 5)

# diff-15
f = x**3 + b*x**2 + c*x + d
m = -b/3
al_be_sum = -sp.Rational(2, 3)*b  # sum of roots of 3x^2+2bx+c
assert sp.simplify(al_be_sum/2 - m) == 0
I = sp.simplify(sp.diff(f, x, 2).subs(x, m)) == 0
s = sp.symbols("s")
II = sp.simplify(f.subs(x, m - s) + f.subs(x, m + s) - 2*f.subs(x, m)) == 0  # holds for every s
g = x**3 - 3*x + 5
III = not (g.subs(x, -1) > 0 and g.subs(x, 1) > 0)
roman("diff-15", [I, II, III])

# diff-16
y = (x**2 + 4)/sp.sqrt(x)
numeric("diff-16", [2, F(11, 4), 3, F(13, 4), 32], sp.diff(y, x).subs(x, 4))

# diff-17
f = x**3 - 6*x**2 + 9*x
cands = [0, 5] + [s for s in sp.solve(sp.diff(f, x), x) if 0 <= s <= 5]
numeric("diff-17", [0, 4, 9, 20, 45], max(f.subs(x, v) for v in cands))

# diff-18
f = 3*x**4 - 8*x**3 - 6*x**2 + 24*x
count = sum(1 for cv in range(-40, 41) if nroots(f - cv) == 4)
numeric("diff-18", [2, 3, 4, 5, 6], count)

print("ALL OK")
