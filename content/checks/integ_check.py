"""Independent verification of content/questions/integ.json. Run: python3 content/checks/integ_check.py"""
import json, os
from fractions import Fraction as F
import sympy as sp

x, t, k, a, u = sp.symbols("x t k a u", real=True)
HERE = os.path.dirname(os.path.abspath(__file__))
QS = {q["id"]: q for q in json.load(open(os.path.join(HERE, "..", "questions", "integ.json"), encoding="utf-8"))}
BASE = [f"integ-{i:02d}" for i in range(1, 19)]
assert sorted(QS) == sorted(BASE + [b + "b" for b in BASE]), sorted(QS)
assert sorted(QS[b]["difficulty"] for b in BASE) == [2]*2 + [3]*7 + [4]*6 + [5]*3
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

I_ = sp.integrate


def numeric(qid, values, truth):
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


def area(f, lo, hi):
    """Geometric area between y=f and the x-axis on [lo, hi], splitting at real roots."""
    pts = sorted({sp.nsimplify(lo), sp.nsimplify(hi)} | {r for r in sp.solve(f, x) if r.is_real and lo < r < hi})
    return sum(abs(I_(f, (x, pts[i], pts[i + 1]))) for i in range(len(pts) - 1))


def sets_match(qid, preds, truth, grid):
    agree = [all(pr(v) == truth(v) for v in grid) for pr in preds]
    assert agree.count(True) == 1 and agree.index(True) == QS[qid]["answer"], (qid, agree)


# integ-01 / 01b
numeric("integ-01", [F(13, 3), F(29, 3), F(35, 3), F(59, 3), 21], I_((2*x - 1)**2/(x*sp.sqrt(x)), (x, 1, 4)))
numeric("integ-01b", [18, F(138, 5), F(156, 5), F(163, 5), F(167, 3)], sp.simplify(I_((x + 2)/sp.cbrt(x), (x, 1, 8))))

# integ-02 / 02b: solve dy/dx = f with a condition
c = sp.symbols("c")
h = I_((t + 1)/(2*sp.sqrt(t)), t) + c
h = h.subs(c, sp.solve(sp.Eq(h.subs(t, 1), 2), c)[0])
assert sp.simplify(sp.diff(h, t) - (t + 1)/(2*sp.sqrt(t))) == 0
numeric("integ-02", [F(10, 3), F(14, 3), F(16, 3), F(20, 3), F(15, 2)], sp.simplify(h.subs(t, 4)))
y = I_((x**2 - 1)/x**2, x) + c
y = y.subs(c, sp.solve(sp.Eq(y.subs(x, 1), 5), c)[0])
numeric("integ-02b", [F(5, 2), F(11, 2), F(13, 2), F(15, 2), F(17, 2)], y.subs(x, 2))

# integ-03 / 03b: area between curve and line (computed as |integral| between consecutive crossings)
numeric("integ-03", [0, F(9, 2), F(27, 2), 18, F(45, 2)], area(x - (x**2 - 2*x), 0, 3))
numeric("integ-03b", [F(95, 6), F(55, 3), F(125, 6), F(233, 6), F(125, 3)], area(6 - x**2 - x, -3, 2))

# integ-04: distance = integral of |v|; integ-04b: A - I
v = x**2 - 6*x + 8
numeric("integ-04", [F(4, 3), F(16, 3), F(20, 3), 8, F(28, 3)], area(v, 0, 5))
assert I_(v, (x, 0, 5)) == F(20, 3)
f = x**3 - 4*x
numeric("integ-04b", [0, 4, 8, 12, 16], area(f, -1, 3) - I_(f, (x, -1, 3)))

# integ-05: int_a^x f = x^3 - 3x^2 + 4 for all x -> f = derivative, and RHS vanishes at x = a
rhs = x**3 - 3*x**2 + 4
fx = sp.diff(rhs, x)
valid = sorted(av for av in range(-10, 11) if sp.expand(I_(fx.subs(x, t), (t, av, x)) - rhs) == 0)
assert valid == [-1, 2]
keyed("integ-05", ["0,2", "-1", "2", "-1,2", "-2,1"].index(",".join(map(str, valid))))
# integ-05b
rhs = 2*x*sp.sqrt(x) + k*x
kv = sp.solve(rhs.subs(x, 4), k)[0]
fx = sp.diff(rhs.subs(k, kv), x)
assert sp.simplify(I_(fx.subs(x, t), (t, 4, x)) - rhs.subs(k, kv)) == 0
numeric("integ-05b", [F(1, 2), 5, 9, 13, 18], fx.subs(x, 9))

# integ-06 / 06b: concrete functions realising the data (answer must not depend on the choice)
for extra in [0, (x - 1)*(x - 3)*(x - 4), (x - 1)*(x - 3)]:
    # f: piecewise-free polynomial fitted to the two f-conditions; g fitted to the (f+g) condition
    p0, p1, q0 = sp.symbols("p0 p1 q0")
    f = p0 + p1*x + extra
    sol = sp.solve([I_(f, (x, 1, 4)) - 5, I_(f, (x, 3, 4)) - 2], [p0, p1])
    f = f.subs(sol)
    g = q0 + x**2
    g = g.subs(q0, sp.solve(I_(f + g, (x, 1, 3)) - 1, q0)[0])
    val = I_(2*g - 1, (x, 3, 1))
    assert val == 6, val
numeric("integ-06", [-6, 4, 5, 6, 14], 6)
for extra in [0, (x - 3)*(x - 5), x**3]:
    p0, p1, q0 = sp.symbols("p0 p1 q0")
    f = p0 + p1*x + extra
    f = f.subs(sp.solve([I_(f, (x, 1, 3)) - 4, I_(f, (x, 1, 5)) - 9], [p0, p1]))
    g = q0 + extra
    g = g.subs(q0, sp.solve(I_(g, (x, 5, 3)) - 3, q0)[0])
    val = I_(f + 2*g + x, (x, 3, 5))
    assert val == 7, val
numeric("integ-06b", [-1, 1, 7, 15, 19], 7)

# integ-07: several f with integral 5 over [0,3]
for f in [1 + 0*x, x, x**2 - 1, x**3]:
    f = f*5/I_(f, (x, 0, 3))
    assert I_(2*f.subs(x, x - 1) + 3, (x, 1, 4)) == 19
numeric("integ-07", [10, 13, 16, 19, 22], 19)
# integ-07b: several g with integral 9 over [-2,4]
for g in [1 + 0*x, x + 3, x**2, x**3 + 10]:
    g = g*9/I_(g, (x, -2, 4))
    assert I_(g.subs(x, 2*x) + x, (x, -1, 2)) == 6
numeric("integ-07b", [F(9, 2), 6, F(15, 2), F(21, 2), F(39, 2)], 6)

# integ-08: odd f; III fails for f = x^3 - x/2
f = x**3 - x/2
assert sp.simplify(f.subs(x, -x) + f) == 0 and I_(f, (x, 0, 2)) == 3
assert I_(f, (x, -2, 2)) == 0 and I_(f, (x, -2, 0)) == -3 and area(f, -2, 2) > 6
roman("integ-08", [True, True, False])
# integ-08b: even g; check with two examples
for g in [sp.Rational(4, 3) + 0*x, sp.Rational(4, 9)*x**2 + sp.Rational(0, 1), x**2 - sp.Rational(5, 3)]:
    g = g*4/I_(g, (x, 0, 3)) if I_(g, (x, 0, 3)) != 0 else g
    assert sp.simplify(g.subs(x, -x) - g) == 0 and I_(g, (x, 0, 3)) == 4
    S1 = I_(g, (x, -3, 3)) == 8
    S2 = I_(g, (x, -3, 0)) == -4
    S3 = I_(x*g, (x, -3, 3)) == 0
    roman("integ-08b", [S1, S2, S3])


# integ-09 / 09b: trapezium rule comparisons
def trap(g, lo, hi, n):
    h_ = sp.Rational(hi - lo, n)
    ys = [g.subs(x, lo + i*h_) for i in range(n + 1)]
    return h_/2*(ys[0] + ys[-1] + 2*sum(ys[1:-1]))
res = [sp.N(trap(g, 0, 2, 4) - I_(g, (x, 0, 2))) > 1e-12 for g in [x**2, sp.sqrt(x), x**3 - 3*x**2]]
assert trap(x**3 - 3*x**2, 0, 2, 4) == I_(x**3 - 3*x**2, (x, 0, 2)) == -4
roman("integ-09", res)
res = [sp.N(trap(g, -1, 1, 2) - I_(g, (x, -1, 1))) < -1e-12 for g in [1 - x**2, x**3, sp.sqrt(x + 1)]]
assert trap(x**3, -1, 1, 2) == 0 == I_(x**3, (x, -1, 1))
roman("integ-09b", res)

# integ-10 / 10b
numeric("integ-10", [0, 2, 4, 8, 16], area(4*x - x**3, -2, 2))
numeric("integ-10b", [F(9, 4), F(8, 3), F(37, 12), F(15, 4), F(37, 6)], area(x**3 - x**2 - 2*x, -1, 2))
assert abs(I_(x**3 - x**2 - 2*x, (x, -1, 2))) == F(9, 4)


# integ-11 / 11b: all k > 0 with the stated area (search both sides of the fixed line)
def ks_with_area(fn, fixed, target):
    kk = sp.Symbol("kk", positive=True)
    out = set()
    for s in sp.solve(sp.Eq(I_(fn, (x, fixed, kk)), target), kk):
        if s > fixed: out.add(s)
    for s in sp.solve(sp.Eq(I_(fn, (x, kk, fixed)), target), kk):
        if s < fixed: out.add(s)
    return sorted(out)
assert ks_with_area(1/x**2, 1, F(3, 4)) == [F(4, 7), 4]
keyed("integ-11", 3)
assert ks_with_area(1/sp.sqrt(x), 4, 2) == [1, 9]
keyed("integ-11b", 1)

# integ-12 / 12b: trapezium error as function of k, checked over a grid
K = [sp.Rational(n, 4) for n in range(-40, 20)]
over = lambda kv: trap(x**3 + kv*x**2, 0, 2, 2) - I_(x**3 + kv*x**2, (x, 0, 2)) > 0
sets_match("integ-12", [lambda v: v >= 0, lambda v: v > -3, lambda v: v > -6, lambda v: v < -3, lambda v: v > 0], over, K)
K = [sp.Rational(n, 5) for n in range(-40, 20)]
under = lambda kv: trap(x**4 + kv*x**2, -1, 1, 2) - I_(x**4 + kv*x**2, (x, -1, 1)) < 0
sets_match("integ-12b", [lambda v: v <= -6, lambda v: v < -sp.Rational(6, 5), lambda v: v < -sp.Rational(9, 5),
                         lambda v: v < 0, lambda v: v > -sp.Rational(9, 5)], under, K)


# integ-13 / 13b: piecewise-linear rate from the stated vertices
def pw(verts):
    return sp.Piecewise(*[((verts[i][1] + (verts[i + 1][1] - verts[i][1])*(t - verts[i][0])/(verts[i + 1][0] - verts[i][0])),
                           t <= verts[i + 1][0]) for i in range(len(verts) - 1)])
r = pw([(0, 0), (1, 3), (2, 0), (3, -2), (4, -2), (5, 0), (6, 2)])
for tv in [sp.Rational(n, 10) for n in range(0, 61)]:  # the plot formula matches the vertices
    assert r.subs(t, tv) == (-5 + sp.Rational(5, 2)*tv - 3*abs(tv - 1) + abs(tv - 2)/2 + abs(tv - 3) + abs(tv - 4))
V = lambda X: I_(r, (t, 0, X))
I1 = r.subs(t, sp.Rational(19, 10)) > 0 and r.subs(t, sp.Rational(21, 10)) < 0
# zeros of V on (0, 6]: V is piecewise polynomial; count sign changes on a fine grid plus exact zeros
grid = [sp.Rational(n, 100) for n in range(1, 601)]
vals = [V(g_) for g_ in grid]
zeros = sum(1 for v_ in vals if v_ == 0) + sum(1 for i in range(len(vals) - 1) if vals[i]*vals[i + 1] < 0)
assert V(6) == 0 and V(2) == 3 and V(5) == -1
I2 = zeros == 2
inflow = I_(sp.Max(r, 0), (t, 0, 6))
assert inflow == 4
roman("integ-13", [I1, I2, inflow == 3])
f = pw([(0, -2), (1, 0), (2, 2), (3, 2), (4, 0), (6, -2)])
for tv in [sp.Rational(n, 10) for n in range(0, 61)]:
    assert f.subs(t, tv) == 1 + tv/2 - abs(tv - 2) - abs(tv - 3) + abs(tv - 4)/2
G = lambda X: I_(f, (t, 2, X))
J1 = f.subs(t, sp.Rational(9, 10)) < 0 and f.subs(t, sp.Rational(11, 10)) > 0
roman("integ-13b", [J1, G(0) < 0, G(6) > 0])
assert G(0) == 0 and G(6) == 1

# integ-14: example symmetric about t=2 meeting the data
A_, B_ = sp.symbols("A B")
f = A_ + B_*(x - 2)**2
f = f.subs(sp.solve([I_(f, (x, 0, 4)) - 10, I_(f, (x, 0, 1)) - 2], [A_, B_]))
assert sp.simplify(f.subs(x, 4 - x) - f) == 0
numeric("integ-14", [1, 2, 3, 5, 8], I_(f, (x, 1, 2)))
# integ-14b: f(4-x) = 6 - f(x): f = 3 + odd function about x=2, several examples
for odd in [(x - 2), (x - 2)**3, (x - 2) + (x - 2)**3]:
    f = 3 + A_*odd
    f = f.subs(A_, sp.solve(I_(f, (x, 0, 1)) - 1, A_)[0])
    assert sp.simplify(f.subs(x, 4 - x) - (6 - f)) == 0
    assert I_(f, (x, 3, 4)) == 5
numeric("integ-14b", [-1, 1, 3, 5, 6], 5)

# integ-15 / 15b: concrete examples
f, g = sp.Rational(3, 2)*x**2, sp.Rational(3, 2)*x
assert I_(f, (x, 0, 2)) == 4 and I_(g, (x, 0, 2)) == 3
numeric("integ-15", [4, 8, 12, 14, 18], I_(f + g + f*g + 1, (x, -2, 2)))
f, g = sp.Rational(4, 9)*x, sp.Rational(5, 3) + 0*x
assert I_(f, (x, 0, 3)) == 2 and I_(g, (x, 0, 3)) == 5
numeric("integ-15b", [8, 11, 14, 15, 21], I_(f + 2*g + 1, (x, -3, 0)))

# integ-16
r = x**2 - 4*x + 3
Va = I_(r, (x, 0, a))
S1 = all(Va.subs(a, sp.Rational(n, 10)) >= 0 for n in range(1, 100))
dV = sp.diff(Va, a)
S2 = dV.subs(a, sp.Rational(9, 10)) > 0 and dV.subs(a, sp.Rational(11, 10)) < 0
S3 = area(r, 0, 3) == Va.subs(a, 3)
roman("integ-16", [S1, S2, S3])
# integ-16b
r = x**2 - x - 2
Fa = I_(r, (x, -1, a))
T1 = sp.diff(Fa, a).subs(a, 0) == -2
dF = sp.diff(Fa, a)
T2 = dF.subs(a, sp.Rational(19, 10)) > 0 and dF.subs(a, sp.Rational(21, 10)) < 0
T3 = area(r, -1, 2) == -Fa.subs(a, 2)
roman("integ-16b", [T1, T2, T3])

# integ-17
kv = sp.symbols("kv", positive=True)
whole = I_(2*x - x**2, (x, 0, 2))
upper = I_((2*x - x**2) - kv*x, (x, 0, 2 - kv))
sols = [s_ for s_ in sp.solve(sp.Eq(upper, whole/2), kv) if s_.is_real and 0 < s_ < 2]
assert len(sols) == 1
numeric("integ-17", [2 - sp.cbrt(4), 2 - sp.sqrt(2), F(2, 3), 2 - sp.cbrt(2), 1], sols[0])
# integ-17b
cv = sp.symbols("cv", positive=True)
whole = I_(4 - x**2, (x, -2, 2))
cap = I_(4 - x**2 - cv, (x, -sp.sqrt(4 - cv), sp.sqrt(4 - cv)))
sols = [s_ for s_ in sp.solve(sp.Eq(cap, whole/2), cv) if s_.is_real and 0 < s_ < 4]
assert len(sols) == 1
numeric("integ-17b", [4 - 2*sp.cbrt(4), 4 - 2*sp.sqrt(2), 4 - 2*sp.cbrt(2), 2, 4 - sp.cbrt(4)], sols[0])

# integ-18 / 18b: families of solutions (particular solution + periodic part)
for p_ in [0, sp.sin(2*sp.pi*x), sp.cos(2*sp.pi*x)**2 - sp.Rational(1, 2)]:
    f = x**2 - x + c + p_
    assert sp.simplify(f.subs(x, x + 1) - f - 2*x) == 0
    f = f.subs(c, sp.solve(sp.Eq(I_(f, (x, 0, 1)), 2), c)[0])
    assert sp.simplify(I_(f, (x, 0, 3))) == 11
numeric("integ-18", [9, 11, 12, 15, 17], 11)
for p_ in [0, sp.sin(sp.pi*x), sp.cos(sp.pi*x)]:
    f = x**2/4 - x/2 + c + p_
    assert sp.simplify(f.subs(x, x + 2) - f - x) == 0
    f = f.subs(c, sp.solve(sp.Eq(I_(f, (x, 0, 2)), 5), c)[0])
    assert sp.simplify(I_(f, (x, 0, 6))) == 25
numeric("integ-18b", [20, 21, 25, 33, 37], 25)

print("ALL OK")
