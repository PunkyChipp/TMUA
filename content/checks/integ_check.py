"""Independent verification of content/questions/integ.json. Run: python3 content/checks/integ_check.py"""
import json, os
from fractions import Fraction as F
import sympy as sp

x, k, u, a = sp.symbols("x k u a", real=True)
HERE = os.path.dirname(os.path.abspath(__file__))
QS = {q["id"]: q for q in json.load(open(os.path.join(HERE, "..", "questions", "integ.json"), encoding="utf-8"))}
assert len(QS) == 18 and sorted(QS) == [f"integ-{i:02d}" for i in range(1, 19)]
assert sorted(q["difficulty"] for q in QS.values()) == [1]*2 + [2]*4 + [3]*6 + [4]*4 + [5]*2
for q in QS.values():
    assert len(set(q["options"])) == len(q["options"]) and 4 <= len(q["options"]) <= 8
    assert 0 <= q["answer"] < len(q["options"])
    for key in q["distractors"]:
        assert int(key) != q["answer"] and int(key) < len(q["options"]), q["id"]
I_ = sp.integrate


def numeric(qid, values, truth):
    q = QS[qid]
    assert len(values) == len(q["options"]), qid
    vals = [sp.nsimplify(v) if not isinstance(v, sp.Basic) else v for v in values]
    assert all(float(vals[i]) < float(vals[i + 1]) for i in range(len(vals) - 1)), qid + " not ascending"
    hits = [i for i, v in enumerate(vals) if sp.simplify(v - truth) == 0]
    assert hits == [q["answer"]], (qid, hits, truth)


def keyed(qid, idx):
    assert QS[qid]["answer"] == idx, (qid, QS[qid]["answer"], idx)


ROMAN = [(), (1,), (2,), (3,), (1, 2), (1, 3), (2, 3), (1, 2, 3)]


def roman(qid, truths):
    keyed(qid, ROMAN.index(tuple(i + 1 for i, v in enumerate(truths) if v)))


def area(f, lo, hi):
    """Total (unsigned) area between f and x-axis."""
    pts = sorted({lo, hi} | {r for r in sp.solve(f, x) if r.is_real and lo < r < hi})
    return sum(abs(I_(f, (x, p, q))) for p, q in zip(pts, pts[1:]))


# integ-01
numeric("integ-01", [6, 8, 10, 12, 14], I_(3*sp.sqrt(x) - 2, (x, 1, 4)))

# integ-02: antiderivative check by differentiation
integrand = (x**2 - 4)/x**2
cands = [x - 4/x, x + 4/x, x + 8/x**3, (x**3 - 12*x)/x**3, x - 4*sp.log(x)]
ok = [i for i, G in enumerate(cands) if sp.simplify(sp.diff(G, x) - integrand) == 0]
assert ok == [1]; keyed("integ-02", 1)

# integ-03
numeric("integ-03", [F(3, 2), 3, F(9, 2), F(27, 2), 18], area(x - (x**2 - 2*x), 0, 3))

# integ-04
f = x**2 - 4*x + 3
numeric("integ-04", [0, F(4, 3), 2, F(8, 3), 4], area(f, 0, 3))
assert I_(f, (x, 0, 3)) == 0

# integ-05
sols = [s for s in sp.solve(sp.Eq(I_(2*x + 3, (x, 1, k)), 14), k) if s > 1]
assert len(sols) == 1
numeric("integ-05", [-6, 2, 3, 4, 6], sols[0])

# integ-06
numeric("integ-06", [-48, -16, -8, 0, 16], I_(x**5 - 3*x**2 + 4*x, (x, -2, 2)))

# integ-07: test with several f having integral 5 over [0,3]
for f in [sp.Rational(5, 3) + 0*x, sp.Rational(10, 9)*x, x**2 - sp.Rational(4, 3), 5*x**3/sp.Rational(81, 4)*1]:
    f = f * 5 / I_(f, (x, 0, 3))
    assert I_(f, (x, 0, 3)) == 5
    val = I_(2*f.subs(x, x - 1) + 3, (x, 1, 4))
    assert val == 19
numeric("integ-07", [10, 13, 16, 19, 22], 19)

# integ-08
f = x**3 - x/2
assert sp.simplify(f.subs(x, -x) + f) == 0 and I_(f, (x, 0, 2)) == 3
assert I_(f, (x, -2, 2)) == 0 and I_(f, (x, -2, 0)) == -3
abs_int = area(f, -2, 2)
assert abs_int > 6
roman("integ-08", [True, True, False])


# integ-09
def trap(g, lo, hi, n):
    h = sp.Rational(hi - lo, n)
    ys = [g.subs(x, lo + i*h) for i in range(n + 1)]
    return h/2*(ys[0] + ys[-1] + 2*sum(ys[1:-1]))
res = []
for g in [x**2, sp.sqrt(x), x**3 - 3*x**2]:
    T, E = trap(g, 0, 2, 4), I_(g, (x, 0, 2))
    res.append(sp.N(T - E) > 1e-12)
assert trap(x**3 - 3*x**2, 0, 2, 4) == I_(x**3 - 3*x**2, (x, 0, 2)) == -4
roman("integ-09", res)

# integ-10
numeric("integ-10", [0, 2, 4, 8, 16], area(4*x - x**3, -2, 2))

# integ-11: area between x=1 and x=k is |1 - 1/k|
ks = sorted(s for s in sp.solve(sp.Eq(1 - 1/k, sp.Rational(3, 4)), k) + sp.solve(sp.Eq(1/k - 1, sp.Rational(3, 4)), k) if s > 0)
assert ks == [sp.Rational(4, 7), 4]
for kv in ks:
    lo, hi = sorted([1, kv])
    assert I_(1/x**2, (x, lo, hi)) == sp.Rational(3, 4)
keyed("integ-11", 3)

# integ-12
kk = [s for s in sp.solve(sp.Eq(I_(k*x - x**2, (x, 0, k)), 36), k) if s.is_real and s > 0]
numeric("integ-12", [3, sp.cbrt(36), sp.cbrt(72), sp.cbrt(108), 6], kk[0])

# integ-13: II counterexample; I and III are theorems for continuous f
f = x - 1
assert I_(f, (x, 0, 4)) >= 0 and f.subs(x, 0) < 0
roman("integ-13", [True, False, True])

# integ-14: concrete example symmetric about x=2 satisfying the data
A_, B_ = sp.symbols("A B")
f = A_ + B_*(x - 2)**2
sol = sp.solve([I_(f, (x, 0, 4)) - 10, I_(f, (x, 0, 1)) - 2], [A_, B_])
f = f.subs(sol)
assert sp.simplify(f.subs(x, 4 - x) - f) == 0
numeric("integ-14", [1, 2, 3, 5, 8], I_(f, (x, 1, 2)))

# integ-15: example f=3x^2/2 (even), g=3x/2 (odd)
f, g = sp.Rational(3, 2)*x**2, sp.Rational(3, 2)*x
assert I_(f, (x, 0, 2)) == 4 and I_(g, (x, 0, 2)) == 3
numeric("integ-15", [4, 8, 12, 14, 18], I_(f + g + f*g + 1, (x, -2, 2)))

# integ-16
Fa = I_(x**2 - 4*x + 3, (x, 0, a))
assert sp.factor(Fa - a*(a - 3)**2/3) == 0
grid = [sp.Rational(n, 10) for n in range(1, 100)]
S1 = all(Fa.subs(a, v) >= 0 for v in grid)
dF = sp.diff(Fa, a)
S2 = dF.subs(a, 0.9) > 0 and dF.subs(a, 1.1) < 0
S3 = area(x**2 - 4*x + 3, 0, 3) == Fa.subs(a, 3)
roman("integ-16", [S1, S2, S3])

# integ-17
kv = sp.symbols("kv", positive=True)
whole = I_(2*x - x**2, (x, 0, 2))
upper = I_((2*x - x**2) - kv*x, (x, 0, 2 - kv))
sols = [s for s in sp.solve(sp.Eq(upper, whole/2), kv) if s.is_real and 0 < s < 2]
assert len(sols) == 1
numeric("integ-17", [2 - sp.cbrt(4), 2 - sp.sqrt(2), F(2, 3), 2 - sp.cbrt(2), 1], sols[0])

# integ-18: general argument via shift; check on a family of solutions f = x^2 - x + c + p(x), p period 1
c = sp.symbols("c")
for p in [0, sp.sin(2*sp.pi*x), sp.cos(2*sp.pi*x)**2 - sp.Rational(1, 2)]:
    f = x**2 - x + c + p
    assert sp.simplify(f.subs(x, x + 1) - f - 2*x) == 0
    cval = sp.solve(sp.Eq(I_(f, (x, 0, 1)), 2), c)[0]
    tot = sp.simplify(I_(f.subs(c, cval), (x, 0, 3)))
    assert tot == 11, tot
numeric("integ-18", [9, 11, 12, 15, 17], 11)

print("ALL OK")
