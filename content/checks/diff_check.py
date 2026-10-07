"""Independent verification of content/questions/diff.json. Run: python3 content/checks/diff_check.py"""
import json, os
from fractions import Fraction as F
import sympy as sp

x, t, k, a, p, s, c = sp.symbols("x t k a p s c", real=True)
HERE = os.path.dirname(os.path.abspath(__file__))
QS = {q["id"]: q for q in json.load(open(os.path.join(HERE, "..", "questions", "diff.json"), encoding="utf-8"))}
BASE = [f"diff-{i:02d}" for i in range(1, 19)]
assert sorted(QS) == sorted(BASE + [b + "b" for b in BASE]), sorted(QS)
# difficulty spread for the 18 originals; twins match their original
assert sorted(QS[b]["difficulty"] for b in BASE) == [2]*2 + [3]*6 + [4]*6 + [5]*4
for b in BASE:
    X, Y = QS[b], QS[b + "b"]
    assert X["family"] == b and Y["family"] == b, b
    assert X["difficulty"] == Y["difficulty"], b
    assert X["answer"] != Y["answer"], b + " twin answer at same letter"
for q in QS.values():
    n = len(q["options"])
    assert len(set(q["options"])) == n and (n == 5 or (n == 8 and q["options"][0] == "none of them")), q["id"]
    assert 0 <= q["answer"] < n and q["difficulty"] >= 2
    assert len(q["distractors"]) >= 3, q["id"]
    for key in q["distractors"]:
        assert int(key) != q["answer"] and int(key) < n, q["id"]


def numeric(qid, values, truth):
    """Options in order equal `values`, ascending; exactly one equals truth and it is keyed."""
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
    keyed(qid, ROMAN.index(tuple(i + 1 for i, v in enumerate(truths) if v)))


def sets_match(qid, preds, truth, grid):
    """preds: one predicate per option (describing its set); truth: the exact condition.
    Exactly the keyed option agrees with truth on every grid point; every other one differs somewhere."""
    agree = [all(pr(v) == truth(v) for v in grid) for pr in preds]
    assert agree.count(True) == 1 and agree.index(True) == QS[qid]["answer"], (qid, agree)


def global_min(expr, var, lo_open=0):
    crit = [r for r in sp.solve(sp.diff(expr, var), var) if r.is_real and r > lo_open]
    vals = [sp.simplify(expr.subs(var, r)) for r in crit]
    m = min(vals, key=lambda v: float(v))
    for probe in [sp.Rational(1, 100), sp.Rational(1, 3), 1, 2, 5, 13, 50]:  # sanity: it is a global min
        assert float(expr.subs(var, probe)) >= float(m) - 1e-12
    return m


def distinct_real_roots(poly_expr, var=x):
    return set(sp.real_roots(sp.Poly(poly_expr, var)))


RAT = [sp.Rational(n, 8) for n in range(-200, 201)]  # grid for parameter sets

# diff-01 / 01b
numeric("diff-01", [F(16, 9), F(16, 3), 4*sp.sqrt(3), 9, 16], global_min((x + 3)**2/(x*sp.sqrt(x)), x))
numeric("diff-01b", [6, 4*sp.sqrt(6), F(32, 3), 8*sp.sqrt(3), 64], global_min((x**2 + 12)**2/x**3, x))


# diff-02 / 02b: total distance = sum of |changes| between sign changes of the rate
def total_variation(f, lo, hi):
    pts = sorted({lo, hi} | {r for r in sp.solve(sp.diff(f, t), t) if lo < r < hi})
    return sum(abs(f.subs(t, pts[i + 1]) - f.subs(t, pts[i])) for i in range(len(pts) - 1))
numeric("diff-02", [20, 24, 28, 36, 40], total_variation(t**3 - 9*t**2 + 24*t, 0, 5))
numeric("diff-02b", [36, 63, 79, 90, 113], total_variation(2*t**3 - 21*t**2 + 60*t, 0, 6))

# diff-03: tangent/normal to x^3 at (1,1) meet x-axis
m = sp.diff(x**3, x).subs(x, 1)
A = sp.solve(1 + m*(x - 1), x)[0]; B = sp.solve(1 - (x - 1)/m, x)[0]
numeric("diff-03", [F(1, 3), F(4, 3), F(5, 3), 2, F(10, 3)], sp.Rational(1, 2)*abs(B - A)*1)
# diff-03b: tangent/normal to 8/x at (2,4) meet y-axis
m = sp.diff(8/x, x).subs(x, 2)
yA = 4 + m*(0 - 2); yB = 4 - (0 - 2)/m
numeric("diff-03b", [3, 5, 8, 10, 16], sp.Rational(1, 2)*abs(yA - yB)*2)

# diff-04: P'(x) = k - 3 sqrt(x) > 0 on (0,4); test with fine x grid incl. points close to 4
xs = [sp.Rational(n, 1000) for n in range(1, 4000, 7)] + [4 - sp.Rational(1, 10**6)]
def holds04(kv): return all(kv - 3*sp.sqrt(v) > 0 for v in xs)
truth04 = lambda kv: kv >= 6
assert all(holds04(kv) == truth04(kv) for kv in [0, 3, 4, 5, sp.Rational(599, 100), 6, 7, 12, 13])
K = [sp.Rational(n, 4) for n in range(1, 80)]
sets_match("diff-04", [lambda v: 0 < v <= 6, lambda v: v >= 4, lambda v: v > 6, lambda v: v >= 6, lambda v: v >= 12], truth04, K)
# diff-04b: f'(x) = 4 x^(1/3) - k > 0 for x > 8
xs = [8 + sp.Rational(1, 10**6)] + [sp.Rational(n, 10) for n in range(81, 2000, 13)]
truth04b = lambda kv: kv <= 8
assert all(all(4*sp.cbrt(v) - kv > 0 for v in xs) == truth04b(kv) for kv in [-3, 0, 6, 8, sp.Rational(801, 100), 9, 32])
sets_match("diff-04b", [lambda v: v <= 6, lambda v: v < 8, lambda v: v <= 8, lambda v: v >= 8, lambda v: v <= 32], truth04b, K + [-2, 0])

# diff-05: monic cubic, max - min = 32 -> distance between stationary x's; check general identity
al, be = sp.symbols("alpha beta", real=True)
for lead in [1, 2]:
    f = sp.integrate(3*lead*(x - al)*(x - be), x)
    assert sp.factor(f.subs(x, al) - f.subs(x, be)) == sp.factor(lead*(be - al)**3/2)
dd = sp.Symbol("d", positive=True)
dist = sp.solve(sp.Eq(dd**3/2, 32), dd)[0]
numeric("diff-05", [2, 2*sp.cbrt(4), 4, 4*sp.cbrt(2), 8], dist)
f = 2*x**3 - sp.Rational(27, 2)*x  # concrete example with stationary points 3 apart
st = sorted(sp.solve(sp.diff(f, x), x)); assert st[1] - st[0] == 3
numeric("diff-05b", [9, F(27, 2), 18, 27, 54], f.subs(x, st[0]) - f.subs(x, st[1]))

# diff-06: f'(x) = 3(x^2 - 2kx + 1) < 0 on (1,2)
xs = [1 + sp.Rational(n, 200) for n in range(1, 200)]
def h06(kv): return all(x0**2 - 2*kv*x0 + 1 < 0 for x0 in xs)
truth06 = lambda kv: kv >= sp.Rational(5, 4)
K6 = [sp.Rational(n, 16) for n in range(-48, 64)]
assert all(h06(kv) == truth06(kv) for kv in K6)
sets_match("diff-06", [lambda v: v < -1 or v > 1, lambda v: v >= 1, lambda v: v > sp.Rational(5, 4),
                       lambda v: v >= sp.Rational(5, 4), lambda v: v >= sp.Rational(5, 2)], truth06, K6)
# diff-06b: f'(x) = 3x^2 - 12x + k > 0 on (0,1)
xs = [sp.Rational(n, 200) for n in range(1, 200)]
truth06b = lambda kv: kv >= 9
K6b = [sp.Rational(n, 4) for n in range(-8, 64)]
assert all(all(3*x0**2 - 12*x0 + kv > 0 for x0 in xs) == truth06b(kv) for kv in K6b)
sets_match("diff-06b", [lambda v: v >= 0, lambda v: v > 9, lambda v: v >= 9, lambda v: v > 12, lambda v: v >= 12], truth06b, K6b)

# diff-07 / 07b optimisation
Aw = 2*a*(12 - a**2)
crit = [r for r in sp.solve(sp.diff(Aw, a), a) if r > 0]; assert sp.diff(Aw, a, 2).subs(a, crit[0]) < 0
numeric("diff-07", [8, 16, 32, 48, 64], Aw.subs(a, crit[0]))
V = x*(12 - 2*x)**2
crit = [r for r in sp.solve(sp.diff(V, x), x) if 0 < r < 6]; assert len(crit) == 1
numeric("diff-07b", [2, 8, 64, 128, 256], V.subs(x, crit[0]))


# diff-08 / 08b: tangents from external point
def tri_area(curve, P):
    ts = sp.solve(sp.Eq(P[1], curve.subs(x, t) + sp.diff(curve, x).subs(x, t)*(P[0] - t)), t)
    A_, B_ = [(tt, curve.subs(x, tt)) for tt in ts]
    return sp.Rational(1, 2)*abs((A_[0] - P[0])*(B_[1] - P[1]) - (A_[1] - P[1])*(B_[0] - P[0]))
numeric("diff-08", [8, 12, 16, 24, 32], tri_area(x**2, (1, -3)))
numeric("diff-08b", [9, 27, 36, 54, 72], tri_area(x**2/2, (1, -4)))

# diff-09: f' = (x+1)(x-1)(x-3)/2
fp = (x + 1)*(x - 1)*(x - 3)/2
fpp = sp.diff(fp, x)
I = fp.subs(x, sp.Rational(1, 2)) > 0 and fp.subs(x, sp.Rational(3, 2)) < 0
II = all(fp.subs(x, sp.Rational(n, 10)) < 0 for n in range(1, 10))
III = fpp.subs(x, 3) > 0
roman("diff-09", [I, II, III])
# diff-09b: f' = -x(x-2)(x+2)/2
fp = -x*(x - 2)*(x + 2)/2
fpp = sp.diff(fp, x)
I = fp.subs(x, -sp.Rational(1, 2)) < 0 and fp.subs(x, sp.Rational(1, 2)) > 0
II = sp.integrate(fp, (x, 1, 2)) > 0 and all(fp.subs(x, 1 + sp.Rational(n, 10)) > 0 for n in range(0, 10))
III = fpp.subs(x, 2) > 0
roman("diff-09b", [I, II, III])

# diff-10: tangent to x^3-3x^2+2 at x=-1 meets again
f = x**3 - 3*x**2 + 2
T = f.subs(x, -1) + sp.diff(f, x).subs(x, -1)*(x + 1)
others = [r for r in sp.solve(f - T, x) if r != -1]; assert len(others) == 1
numeric("diff-10", [-5, 2, 3, 4, 5], others[0])
# diff-10b: normal to x^2-2x-3 at (3,0)
f = x**2 - 2*x - 3
N = -(x - 3)/sp.diff(f, x).subs(x, 3)
others = [r for r in sp.solve(f - N, x) if r != 3]; assert len(others) == 1
numeric("diff-10b", [-5, F(-5, 4), -1, F(-3, 4), F(5, 4)], others[0])

# diff-11 / 11b: count distinct real roots exactly over a parameter grid
K11 = [sp.Rational(n, 8) for n in range(-24, 48)]
truth11 = lambda kv: len(distinct_real_roots(x**3 - 3*kv*x + 2)) == 3
assert truth11(sp.Rational(9, 8)) and not truth11(1)
sets_match("diff-11", [lambda v: v > 0, lambda v: 0 < v < 1, lambda v: v >= 1, lambda v: v > 1, lambda v: v > 2], truth11, K11)
K11b = [sp.Rational(n, 4) for n in range(-12, 32)]
truth11b = lambda kv: kv != 0 and len(distinct_real_roots(kv*x**3 - 3*x + 1)) == 3
assert truth11b(sp.Rational(15, 4)) and not truth11b(4)
sets_match("diff-11b", [lambda v: v < 4, lambda v: 0 < v < 2, lambda v: 0 < v < 4, lambda v: 0 < v <= 4, lambda v: v > 4],
           truth11b, K11b)

# diff-12: I true (MVT for polynomials), II true, III false via x^4
f = x**4
assert sp.diff(f, x).subs(x, 0) == 0 and sp.diff(f, x, 2).subs(x, 0) == 0 and all(f.subs(x, v) > 0 for v in [-1, -sp.Rational(1, 10), sp.Rational(1, 10), 1])
roman("diff-12", [True, True, False])
# diff-12b: I true (2nd derivative test), II false via -x^4, III true (f'' > 0 => f' strictly increasing)
f = -x**4
assert sp.diff(f, x, 2).subs(x, 0) == 0 and all(f.subs(x, v) < 0 for v in [-1, sp.Rational(1, 10)])
roman("diff-12b", [True, False, True])

# diff-13 / 13b: brute force over (p, q) grid
PQ = [(sp.Rational(i, 2), sp.Rational(j, 2)) for i in range(-8, 9) for j in range(-8, 9)]
exact13 = lambda P, Q: P**2 > 3*Q
opts13 = [lambda P, Q: P**2 > 3*Q, lambda P, Q: P**2 > Q, lambda P, Q: Q < 0, lambda P, Q: Q > 0, lambda P, Q: P > 0]
assert all(exact13(P, Q) == (len(distinct_real_roots(3*x**2 + 2*P*x + Q)) == 2) for P, Q in PQ)
def suff_not_nec(o, ex): return all(ex(*pq) for pq in PQ if o(*pq)) and any(ex(*pq) and not o(*pq) for pq in PQ)
def nec_not_suff(o, ex): return all(o(*pq) for pq in PQ if ex(*pq)) and any(o(*pq) and not ex(*pq) for pq in PQ)
res = [suff_not_nec(o, exact13) for o in opts13]
assert res.count(True) == 1; keyed("diff-13", res.index(True))
exact13b = lambda P, Q: P**2 < 3*Q
assert all(exact13b(P, Q) == (len(distinct_real_roots(3*x**2 + 2*P*x + Q)) == 0) for P, Q in PQ)
opts13b = [lambda P, Q: P**2 < 3*Q, lambda P, Q: Q > 0, lambda P, Q: Q > P**2, lambda P, Q: P == 0, lambda P, Q: P > 0 and Q > 0]
res = [nec_not_suff(o, exact13b) for o in opts13b]
assert res.count(True) == 1; keyed("diff-13b", res.index(True))


# diff-14 / 14b: number of tangents through a point = distinct real roots of contact cubic
def n_tangents(curve, X0, Y0):
    return len(distinct_real_roots(sp.expand(curve.subs(x, t) + sp.diff(curve, x).subs(x, t)*(X0 - t) - Y0), t))
A14 = [sp.Rational(n, 4) for n in range(-12, 13)]
truth14 = lambda av: n_tangents(x**3 - x, av, 0) == 3
sets_match("diff-14", [lambda v: 0 < abs(v) < 1, lambda v: abs(v) > 1/sp.sqrt(3), lambda v: v > 1,
                       lambda v: abs(v) >= 1, lambda v: abs(v) > 1], truth14, A14)
K14 = [sp.Rational(n, 4) for n in range(-8, 9)]
truth14b = lambda kv: n_tangents(x**3, 1, kv) == 3
sets_match("diff-14b", [lambda v: 0 < v < 1, lambda v: 0 <= v <= 1, lambda v: -1 < v < 1, lambda v: v > 0,
                        lambda v: v < 0 or v > 1], truth14b, K14)

# diff-15: normal chord of y=x^2
pp = sp.Symbol("pp", positive=True)
q_other = [r for r in sp.solve(sp.Eq(x**2, pp**2 - (x - pp)/(2*pp)), x) if sp.simplify(r - pp) != 0][0]
PQ2 = sp.simplify((q_other - pp)**2 + (q_other**2 - pp**2)**2)
crit = [r for r in sp.solve(sp.diff(PQ2, pp), pp) if r.is_positive]
mn = min(sp.simplify(PQ2.subs(pp, r)) for r in crit)
assert all(PQ2.subs(pp, v) >= mn for v in [sp.Rational(1, 10), sp.Rational(1, 2), 1, 2, 5])
numeric("diff-15", [4, F(27, 4), F(125, 16), 8, F(27, 2)], mn)
assert PQ2.subs(pp, 1) == F(125, 16) and PQ2.subs(pp, sp.Rational(1, 2)) == 8
# diff-15b: tangent triangle to y = 3 - x^2
curve = 3 - x**2
tan = curve.subs(x, pp) + sp.diff(curve, x).subs(x, pp)*(x - pp)
area = sp.Rational(1, 2)*sp.solve(tan, x)[0]*tan.subs(x, 0)
crit = [r for r in sp.solve(sp.diff(area, pp), pp) if r.is_positive and r < sp.sqrt(3)]
assert len(crit) == 1
mn = sp.simplify(area.subs(pp, crit[0]))
assert all(area.subs(pp, v) >= mn for v in [sp.Rational(1, 10), sp.Rational(1, 2), sp.Rational(3, 2), sp.Rational(17, 10)])
numeric("diff-15b", [2, 3, 4, 3*sp.sqrt(3), 8], mn)

# diff-16 / 16b
numeric("diff-16", [2, F(11, 4), 3, F(13, 4), 32], sp.diff((x**2 + 4)/sp.sqrt(x), x).subs(x, 4))
numeric("diff-16b", [F(-15, 16), F(-9, 16), F(-3, 16), F(3, 16), F(15, 16)], sp.simplify(sp.diff((sp.sqrt(x) - 3)**2/x, x).subs(x, 4)))


# diff-17 / 17b: greatest value on [0, a] by dense sampling + stationary points
def greatest(f, hi):
    pts = [sp.Integer(0), hi] + [r for r in sp.solve(sp.diff(f, x), x) if 0 < r < hi]
    return max(f.subs(x, v) for v in pts)
h = x**3 - 6*x**2 + 9*x
A17 = [sp.Rational(n, 8) for n in range(1, 60)]
truth17 = lambda av: greatest(h, av) == 4
sets_match("diff-17", [lambda v: v == 1, lambda v: 1 <= v <= 3, lambda v: 1 <= v <= 4, lambda v: 1 < v < 4, lambda v: v >= 1], truth17, A17)
f = 2*x**3 - 9*x**2 + 12*x
truth17b = lambda cv: greatest(f, cv) == f.subs(x, cv)
H = sp.Rational(5, 2)
sets_match("diff-17b", [lambda v: 0 < v <= 1, lambda v: v >= H, lambda v: 0 < v <= 1 or v >= 2,
                        lambda v: 0 < v <= 1 or v >= H, lambda v: 0 < v < 1 or v > H], truth17b, A17)


# diff-18 / 18b: |f(x)| = c, exact distinct-root counts
def n_abs(f, cv):
    return len(distinct_real_roots(f - cv) | distinct_real_roots(f + cv))
f = 3*x**4 - 8*x**3 - 6*x**2 + 24*x
good = [cv for cv in range(0, 60) if n_abs(f, cv) == 4]
assert good == list(range(1, 8)) + list(range(14, 19)) and n_abs(f, 200) == 2
numeric("diff-18", [4, 5, 7, 12, 13], len(good))
g = x**3 - 3*x**2 - 9*x
good = [cv for cv in range(0, 80) if n_abs(g, cv) == 4]
assert good == list(range(6, 27)) and n_abs(g, 500) == 2
numeric("diff-18b", [21, 22, 23, 26, 31], len(good))

print("ALL OK")
