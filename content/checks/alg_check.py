"""Verification for content/questions/alg.json (originals alg-NN and twins alg-NNb).

For every question the keyed answer is recomputed independently (sympy / brute force)
and compared against the option at the keyed index; every other option is checked to be wrong.
Run: python3 content/checks/alg_check.py
"""
import json
import os
import random
from collections import Counter
from fractions import Fraction as Fr

import sympy as sp
from sympy import Rational as R, sqrt, symbols, Poly, real_roots, S

HERE = os.path.dirname(os.path.abspath(__file__))
Q = {q["id"]: q for q in json.load(open(os.path.join(HERE, "..", "questions", "alg.json"), encoding="utf-8"))}
x, y, k, u = symbols("x y k u", real=True)
ROMAN = ["none of them", "I only", "II only", "III only", "I and II only",
         "I and III only", "II and III only", "I, II and III"]


def roman_index(I, II, III):
    sel = tuple(n for n, t in zip(["I", "II", "III"], [I, II, III]) if t)
    table = {(): 0, ("I",): 1, ("II",): 2, ("III",): 3, ("I", "II"): 4, ("I", "III"): 5,
             ("II", "III"): 6, ("I", "II", "III"): 7}
    return table[sel]


def check_roman(qid, I, II, III):
    q = Q[qid]
    assert q["options"] == ROMAN, qid
    assert roman_index(I, II, III) == q["answer"], (qid, (I, II, III), q["answer"])


def check_numeric(qid, value, option_values, ascending=True):
    """option_values: sympy values in option order (None = non-numeric option, must be wrong)."""
    q = Q[qid]
    assert len(option_values) == len(q["options"]), qid
    matches = [i for i, v in enumerate(option_values) if v is not None and sp.simplify(v - value) == 0]
    assert matches == [q["answer"]], (qid, matches, q["answer"])
    if ascending:
        nums = [float(v) for v in option_values if v is not None]
        assert nums == sorted(nums), (qid, "options not ascending")


def check_pred(qid, truth, preds, samples):
    """truth(t) -> bool; preds: list of option predicates. Exactly the keyed one agrees everywhere."""
    q = Q[qid]
    assert len(preds) == len(q["options"]), qid
    tv = {t: truth(t) for t in samples}
    good = [i for i, p in enumerate(preds) if all(p(t) == tv[t] for t in samples)]
    assert good == [q["answer"]], (qid, good, q["answer"])


def nroots(expr, var=x):
    P = Poly(expr, var)
    if P.degree() <= 0:
        return None if P.is_zero else 0
    return len(set(real_roots(P)))


# ---------------------------------------------------------------- alg-01
A, B = symbols("A B")
sol = sp.solve([A + B - 3, -2 * A + B + 3], [A, B])
rem = sol[A] * x + sol[B]
# concrete instance: p(x) = (x^2+x-2)(x^3+5) + 2x + 1 has the stated remainders
pex = sp.expand((x**2 + x - 2) * (x**3 + 5) + rem)
assert pex.subs(x, 1) == 3 and pex.subs(x, -2) == -3
assert sp.rem(pex, x**2 + x - 2, x) == rem
opts = [S(-9), S(0), S(3), -6 * x + 9, 2 * x + 1]
assert [i for i, o in enumerate(opts) if sp.expand(o - rem) == 0] == [Q["alg-01"]["answer"]]

# alg-01b
p, q = symbols("p q")
r = sp.rem(x**4 + p * x**2 + q, x**2 + x + 1, x)
sol = sp.solve(Poly(r, x).all_coeffs(), [p, q], dict=True)
assert sol == [{p: 1, q: 1}]
pairs = [(-1, 1), (1, -1), (1, 1), (3, 1), (1, 0)]
ok = [i for i, (pv, qv) in enumerate(pairs) if sp.rem(x**4 + pv * x**2 + qv, x**2 + x + 1, x) == 0]
assert ok == [Q["alg-01b"]["answer"]]

# ---------------------------------------------------------------- alg-02
def sols_sqrt_eq(lhs, rhs):
    cands = sp.solve(sp.Eq(lhs**2, rhs**2), x)
    return sorted(c for c in cands if c.is_real and sp.simplify(lhs.subs(x, c) - rhs.subs(x, c)) == 0)


s2 = sols_sqrt_eq(sqrt(2 * x + 7), x + 2)
assert s2 == [1]
opt2 = [[], [1], [-3, 1], [-1, 3], [3]]
assert [i for i, o in enumerate(opt2) if o == s2] == [Q["alg-02"]["answer"]]

# alg-02b: x - sqrt(x) = 6
cands = sp.solve(sp.Eq(x - sqrt(x), 6), x)
s2b = sorted(c for c in cands if c >= 0 and c - sqrt(c) == 6)
assert s2b == [9]
assert 4 - sqrt(4) != 6
opt2b = [[3], [4, 9], [9], [-2, 3], []]
assert [i for i, o in enumerate(opt2b) if o == s2b] == [Q["alg-02b"]["answer"]]

# ---------------------------------------------------------------- alg-03
den = 2 * x**2 - 12 * x + 23
assert sp.discriminant(den, x) < 0
v = 20 / sp.minimum(den, x, S.Reals)
check_numeric("alg-03", v, [R(20, 23), R(10, 7), 4, 20, None])

# alg-03b
mn = sp.minimum(x**2 - 4 * x + 1, x, S.Reals)
check_numeric("alg-03b", S(2)**mn, [R(1, 8), R(1, 2), 1, 2, None])

# ---------------------------------------------------------------- alg-04: |x-2| = kx
def count4(kv):
    sols = set()
    for c in sp.solve(sp.Eq(x - 2, kv * x), x):
        if c >= 2:
            sols.add(c)
    for c in sp.solve(sp.Eq(2 - x, kv * x), x):
        if c < 2:
            sols.add(c)
    # k=-1 or k=1 lines parallel to an arm: solve() returns [] (no solution) - handled
    return len(sols)


kvals = [R(n, 8) for n in range(-40, 41)]
check_pred("alg-04", lambda kv: count4(kv) == 2,
           [lambda kv: kv < -1 or 0 < kv < 1, lambda kv: -1 < kv < 1, lambda kv: 0 <= kv < 1,
            lambda kv: 0 < kv < 1, lambda kv: kv > 0], kvals)


# alg-04b: |x^2-4x| = k
def count4b(kv):
    if kv < 0:
        return 0
    s = set()
    for sgn in (1, -1):
        for c in sp.solve(sp.Eq(x**2 - 4 * x, sgn * kv), x):
            if c.is_real:
                s.add(sp.nsimplify(c))
    return len(s)


kvals = [R(n, 4) for n in range(-8, 41)]
check_pred("alg-04b", lambda kv: count4b(kv) == 4,
           [lambda kv: kv > 0, lambda kv: 0 < kv < 4, lambda kv: 0 < kv <= 4, lambda kv: kv > 4,
            lambda kv: 0 < kv < 2], kvals)

# ---------------------------------------------------------------- alg-05
a = symbols("a", real=True)
e5 = sp.expand((x - a)**2 - (x**2 - a**2))
I = sp.expand(e5.subs(a, 0)) == 0
II = all(sp.solve(e5.subs(a, av), x) == [av] for av in [R(n, 3) for n in range(-9, 10) if n != 0])
III = any(nroots(e5.subs(a, av)) == 0 for av in [R(n, 3) for n in range(-9, 10)])
check_roman("alg-05", I, II, III)

# alg-05b
b = symbols("b", real=True)
e5b = sp.expand((x + b)**3 - (x**3 + b**3))
bvals = [R(n, 3) for n in range(-9, 10) if n != 0]
I = all(len(sp.solve(e5b.subs(b, bv), x)) == 1 for bv in bvals)
idents = [bv for bv in [R(n, 3) for n in range(-9, 10)] if sp.expand(e5b.subs(b, bv)) == 0]
coeff_sol = sp.solve(Poly(e5b, x).all_coeffs(), b)
II = idents == [0] and coeff_sol in ([0], [(0,)], {b: 0})
III = all(sum(sp.solve(e5b.subs(b, bv), x)) == -bv for bv in bvals)
check_roman("alg-05b", I, II, III)


# ---------------------------------------------------------------- alg-06 one-to-one
def one_to_one(f, lo, hi, n=4001):
    """Strictly monotone on a fine grid of [lo, hi] (exact rationals) <=> one-to-one there."""
    pts = [lo + (hi - lo) * Fr(i, n - 1) for i in range(n)]
    vals = [f(t) for t in pts]
    d = [b_ - a_ for a_, b_ in zip(vals, vals[1:])]
    # a continuous function on an interval is one-to-one iff strictly monotone
    return all(t > 0 for t in d) or all(t < 0 for t in d)


f6 = lambda t: t * t - 4 * t
g6 = lambda t: t * abs(t)
h6 = lambda t: t**3 - 3 * t
I = one_to_one(f6, Fr(1), Fr(10))
II = one_to_one(g6, Fr(-10), Fr(10))
III = one_to_one(h6, Fr(1), Fr(10))
assert f6(1) == f6(3)
# analytic confirmation for II and III
assert sp.diff(x**3 - 3 * x, x).subs(x, 1) == 0 and sp.solve(sp.diff(x**3 - 3 * x, x) < 0, x) != S.EmptySet
check_roman("alg-06", I, II, III)

f6b = lambda t: t + abs(t)
g6b = lambda t: abs(t)  # sqrt(t^2) = |t|
h6b = lambda t: (t - 1) * (t - 3)
assert all(sp.sqrt(sp.Integer(n)**2) == abs(n) for n in range(-10, 1))
I = one_to_one(f6b, Fr(-10), Fr(10))
II = one_to_one(g6b, Fr(-10), Fr(0))
III = one_to_one(h6b, Fr(1), Fr(10))
check_roman("alg-06b", I, II, III)


# ---------------------------------------------------------------- alg-07
def two_distinct(expr):
    return nroots(expr) == 2


kvals = [R(n, 4) for n in range(-40, 41)]
check_pred("alg-07", lambda kv: two_distinct(kv * x**2 + 4 * x + kv - 3),
           [lambda kv: kv < -1 or kv > 4, lambda kv: -1 < kv < 4, lambda kv: -1 < kv < 4 and kv != 0,
            lambda kv: -4 < kv < 1, lambda kv: -4 < kv < 1 and kv != 0], kvals)

check_pred("alg-07b", lambda kv: two_distinct((kv - 1) * x**2 - 2 * kv * x + kv + 2),
           [lambda kv: kv < 2, lambda kv: kv < 2 and kv != 1, lambda kv: kv > 2,
            lambda kv: 1 < kv < 2, lambda kv: kv <= 2 and kv != 1], kvals)

# ---------------------------------------------------------------- alg-08
m = symbols("m", real=True)
disc = sp.discriminant(x**2 - (1 + m) * x + 4, x)
two = sp.solve_univariate_inequality(disc > 0, m, relational=False)
I = sp.Interval.open(3, sp.oo).is_subset(two)
II = two.is_subset(sp.Interval.open(3, sp.oo))
III = len(sp.solve(sp.Eq(disc, 0), m)) == 1
check_roman("alg-08", I, II, III)

# alg-08b
c = symbols("c", real=True)
quad = lambda cv: x**2 + 4 * x + 5 - (2 * x + cv)
cvals = [R(n, 4) for n in range(-20, 61)]
I = all(nroots(quad(cv)) == 0 for cv in cvals if cv < 4)
II = all(cv > 4 for cv in cvals if nroots(quad(cv)) == 2)
III = all(all(r < 0 for r in sp.solve(quad(cv), x)) for cv in cvals if cv > 4)
assert sorted(sp.solve(quad(8), x)) == [-3, 1]
check_roman("alg-08b", I, II, III)

# ---------------------------------------------------------------- alg-09
pts = [Fr(n, 8) for n in range(-80, 81) if n != 0]
check_pred("alg-09", lambda t: Fr(6) / t > abs(t - 1),
           [lambda t: t > 0, lambda t: 1 <= t < 3, lambda t: 0 < t < 3, lambda t: -2 < t < 3,
            lambda t: t < -2 or 0 < t < 3], pts)

pts = [Fr(n, 8) for n in range(-80, 81)]
check_pred("alg-09b", lambda t: abs(t - 3) > 2 * abs(t),
           [lambda t: -3 < t < 1, lambda t: -1 < t < 3, lambda t: t < -3 or t > 1, lambda t: t < 1,
            lambda t: -3 < t < 3], pts)

# ---------------------------------------------------------------- alg-10
us = sp.solve(u**2 - 12 * u + 27, u)
assert all(9**sp.log(uu, 3) - 4 * 3**(sp.log(uu, 3) + 1) + 27 == 0 for uu in us)
xs = sorted(sp.log(uu, 3) for uu in us if uu > 0)
assert xs == [1, 2]
check_numeric("alg-10", sum(xs), [0, 1, 2, 3, 12])

# alg-10b
us = sp.solve(u**2 - 5 * u + 4, u)
xs = sorted(uu**3 for uu in us)
assert all(sp.real_root(xv, 3)**2 - 5 * sp.real_root(xv, 3) + 4 == 0 for xv in xs)
check_numeric("alg-10b", sum(xs), [4, 5, 17, 63, 65])

# ---------------------------------------------------------------- alg-11
fx = x**2 - 6 * x + 11
finv = 3 + sqrt(x - 2)
assert sp.simplify(fx.subs(x, finv) - x) == 0
cands = [(7 - sqrt(5)) / 2, (7 + sqrt(5)) / 2, 2, 3]
works = [cv for cv in cands if cv >= 3 and sp.simplify(fx.subs(x, cv) - finv.subs(x, cv)) == 0]
assert works == [(7 + sqrt(5)) / 2]
fl = sp.lambdify(x, fx - finv)
vals = [fl(3 + i / 1000) for i in range(0, 20000)]
assert sum(1 for s1, s2 in zip(vals, vals[1:]) if s1 * s2 < 0) == 1
assert Q["alg-11"]["answer"] == 2 and "7+\\sqrt5" in Q["alg-11"]["options"][2]

# alg-11b
fx = x**2 + 4 * x + 2
finv = -2 + sqrt(x + 2)
assert sp.simplify(fx.subs(x, finv) - x) == 0 and sp.simplify(finv.subs(x, fx) - x).subs(x, 5) == 0
sols = [cv for cv in sp.solve(fx - x, x) if cv >= -2 and sp.simplify(fx.subs(x, cv) - finv.subs(x, cv)) == 0]
assert sorted(sols) == [-2, -1]
fl = sp.lambdify(x, fx - finv)
vals = [fl(-2 + i / 1000 + 0.0005) for i in range(0, 20000)]
# exactly one root of f - f^{-1} in (-2, 18) besides the endpoint -2 (it is at -1)
assert sum(1 for s1, s2 in zip(vals, vals[1:]) if s1 * s2 < 0) == 1
opts = [[], [-2], [-1], [-2, -1], [1, 2]]
assert [i for i, o in enumerate(opts) if o == sorted(sols)] == [Q["alg-11b"]["answer"]]


# ---------------------------------------------------------------- alg-12 / 12b
def moebius_statements(F, excl, rng_excl):
    cc = symbols("cc")
    # range: every value except rng_excl is attained; rng_excl is not
    I = sp.solve(sp.Eq(F(x), rng_excl), x) == [] and all(
        len(sp.solve(sp.Eq(F(x), cv), x)) == 1 for cv in [R(n, 2) for n in range(-10, 11) if R(n, 2) != rng_excl])
    II = all(F(t) != excl and sp.simplify(F(F(t)) - t) == 0 for t in [R(n, 3) for n in range(-12, 13) if R(n, 3) != excl])
    III = len(sp.solve(sp.Eq(F(x), x), x)) == 1
    return I, II, III


check_roman("alg-12", *moebius_statements(lambda t: (2 * t + 1) / (t - 2), 2, 2))
check_roman("alg-12b", *moebius_statements(lambda t: (3 * t - 1) / (t + 1), -1, 3))


# ---------------------------------------------------------------- alg-13
def count_real_x(bv, cv):
    return len(set(real_roots(Poly(x**4 + bv * x**2 + cv, x))))


I = II = III = True
vals = [R(n, 2) for n in range(-12, 13)]
for bv in vals:
    for cv in vals:
        n = count_real_x(bv, cv)
        if cv < 0 and n != 2:
            I = False
        if bv < 0 and bv**2 > 4 * cv and n != 4:
            II = False
        if bv > 0 and cv > 0 and n != 0:
            III = False
check_roman("alg-13", I, II, III)


# alg-13b: 4^x + p 2^x + q = 0  <->  positive roots u of u^2 + p u + q
def count13b(pv, qv):
    return len([r for r in set(real_roots(Poly(u**2 + pv * u + qv, u))) if r > 0])


I = II = III = True
for pv in vals:
    for qv in vals:
        n = count13b(pv, qv)
        if qv < 0 and n != 1:
            I = False
        if pv > 0 and n != 0:
            II = False
        if pv**2 == 4 * qv and n != 1:
            III = False
check_roman("alg-13b", I, II, III)

# ---------------------------------------------------------------- alg-14
kk = sp.solve((x**3 - 6 * x**2 + k * x - 6).subs(x, 2), k)[0]
rts = sorted(sp.solve(x**3 - 6 * x**2 + kk * x - 6, x))
assert len(set(rts)) == 3 and rts[1] - rts[0] == rts[2] - rts[1]
check_numeric("alg-14", kk, [-19, 5, 6, 11, 12])


def is_ap(coeffs_k, kv):
    rr = sorted(sp.Poly(coeffs_k(kv), x).nroots(), key=lambda z: (sp.re(z), sp.im(z)))
    return all(abs(sp.im(z)) < 1e-9 for z in rr) and abs((rr[1] - rr[0]) - (rr[2] - rr[1])) < 1e-9 and abs(rr[1] - rr[0]) > 1e-9


for bad in [-19, 5, 6, 12]:
    assert not is_ap(lambda kv: x**3 - 6 * x**2 + kv * x - 6, bad)

# alg-14b
kk = sp.solve((x**3 - 7 * x**2 + k * x - 8).subs(x, 2), k)[0]
rts = sorted(sp.solve(x**3 - 7 * x**2 + kk * x - 8, x))
assert len(set(rts)) == 3 and rts[1] / rts[0] == rts[2] / rts[1]
check_numeric("alg-14b", kk, [-22, -14, 6, 10, 14])


def is_gp(kv):
    rr = sorted(sp.Poly(x**3 - 7 * x**2 + kv * x - 8, x).nroots(), key=lambda z: (sp.re(z), sp.im(z)))
    if not all(abs(sp.im(z)) < 1e-9 for z in rr):
        return False
    rr = [sp.re(z) for z in rr]
    return len({round(float(t), 6) for t in rr}) == 3 and abs(rr[1]**2 - rr[0] * rr[2]) < 1e-6


assert is_gp(14) and not any(is_gp(bad) for bad in [-22, -14, 6, 10])


# ---------------------------------------------------------------- alg-15 / 15b: count intersections exactly
def count_meets(f_expr, g_expr):
    """Curves y = f(x) and x = g(y): count distinct real intersection points."""
    sols = sp.solve([y - f_expr, x - g_expr], [x, y], dict=True)
    pts = set()
    for s_ in sols:
        xv, yv = sp.nsimplify(s_[x]), sp.nsimplify(s_[y])
        if xv.is_real and yv.is_real:
            pts.add((sp.simplify(xv), sp.simplify(yv)))
    return len(pts)


avals = [R(n, 4) for n in range(-3, 13)] + [R(-1, 4), R(3, 4), R(1, 2), R(7, 8), R(5, 8)]
avals = sorted(set(avals))
cnt15 = {av: count_meets(x**2 - av, y**2 - av) for av in avals}
assert cnt15[R(3, 4)] == 2 and cnt15[2] == 4 and cnt15[R(-1, 4)] == 1
check_pred("alg-15", lambda av: cnt15[av] == 4,
           [lambda av: av > R(-1, 4), lambda av: R(-1, 4) < av < R(3, 4), lambda av: av >= R(3, 4),
            lambda av: av > R(3, 4), lambda av: av > 0], avals)

cnt15b = {kv: count_meets(kv - x**2, kv - y**2) for kv in avals}
assert cnt15b[R(3, 4)] == 2 and cnt15b[R(-1, 4)] == 1 and cnt15b[1] == 4
check_pred("alg-15b", lambda kv: cnt15b[kv] == 2,
           [lambda kv: kv > R(-1, 4), lambda kv: R(-1, 4) < kv < R(3, 4), lambda kv: R(-1, 4) < kv <= R(3, 4),
            lambda kv: R(-1, 4) <= kv <= R(3, 4), lambda kv: kv > R(3, 4)], avals)

# ---------------------------------------------------------------- alg-16
pp = sp.interpolate([(1, 1), (2, 2), (3, 3), (4, 5)], x)
assert Poly(pp, x).degree() == 3
check_numeric("alg-16", pp.subs(x, 5), [6, 7, 8, 9, 11])

# alg-16b
qq = sp.interpolate([(1, 1), (2, R(1, 2)), (3, R(1, 3)), (4, R(1, 4))], x)
assert Poly(qq, x).degree() == 3
check_numeric("alg-16b", qq.subs(x, 0), [R(-25, 12), R(1, 24), R(25, 12), R(25, 6), None])


# ---------------------------------------------------------------- alg-17 / 17b
def pos_roots(kv):
    return [r for r in set(real_roots(Poly(u**2 - 2 * u + kv, u)))]


def count17(kv):  # 4^x - 2^{x+1} + k = 0 with u = 2^x > 0
    return len([r for r in pos_roots(kv) if r > 0])


def count17b(kv):  # x^2 - 2|x| + k = 0 directly, both branches
    s = set()
    for sgn in (1, -1):
        for r in real_roots(Poly(x**2 - 2 * sgn * x + kv, x)):
            if (sgn == 1 and r >= 0) or (sgn == -1 and r <= 0):
                s.add(r)
    return len(s)


P17 = [lambda kv: kv < 0, lambda kv: kv <= 0, lambda kv: kv < 0 or kv == 1, lambda kv: kv <= 0 or kv == 1,
       lambda kv: kv < 1]
kvals = [R(n, 8) for n in range(-24, 25)]
check_pred("alg-17", lambda kv: count17(kv) == 1, P17, kvals)
check_pred("alg-17b", lambda kv: count17b(kv) == 2, P17, kvals)
assert Q["alg-17"]["options"] == Q["alg-17b"]["options"]

# ---------------------------------------------------------------- alg-18 / 18b
random.seed(1)
I_ok = II_ok = III_ok = True
for _ in range(200000):
    bv = Fr(random.randint(-60, 60), random.randint(1, 10))
    cv = Fr(random.randint(-60, 60), random.randint(1, 10))
    td = bv * bv - 4 * cv > 0
    if bv * bv > 3 * cv and not td:
        I_ok = False
    if cv < 0 and not td:
        II_ok = False
    if bv > cv + 1 and not td:
        III_ok = False
assert Fr(2) ** 2 - 4 * Fr(6, 5) < 0 and Fr(4) > 3 * Fr(6, 5)
check_roman("alg-18", I_ok, II_ok, III_ok)


def two_pos(bv, cv):
    return bv * bv - 4 * cv > 0 and -bv > 0 and cv > 0


I_ok = II_ok = III_ok = True
for _ in range(200000):
    bv = Fr(random.randint(-60, 60), random.randint(1, 10))
    cv = Fr(random.randint(-60, 60), random.randint(1, 10))
    if bv < 0 and cv > 0 and not two_pos(bv, cv):
        I_ok = False
    if cv > 0 and bv < -cv - 1 and not two_pos(bv, cv):
        II_ok = False
    if bv < 0 and cv < 0 and not two_pos(bv, cv):
        III_ok = False
# II proof: b^2 - 4c > (c+1)^2 - 4c = (c-1)^2 >= 0
cs = symbols("cs")
assert sp.expand((cs + 1)**2 - 4 * cs - (cs - 1)**2) == 0
check_roman("alg-18b", I_ok, II_ok, III_ok)

# ---------------------------------------------------------------- structure
ids = [f"alg-{i:02d}" for i in range(1, 19)]
assert sorted(Q) == sorted(ids + [i + "b" for i in ids])
diff = Counter(Q[i]["difficulty"] for i in ids)
assert diff == Counter({2: 2, 3: 6, 4: 6, 5: 4}), diff
for i in ids:
    a_, b_ = Q[i], Q[i + "b"]
    assert a_["family"] == b_["family"] == i
    assert a_["difficulty"] == b_["difficulty"], i
    assert a_["answer"] != b_["answer"], i
for q_ in Q.values():
    assert len(set(q_["options"])) == len(q_["options"])
    assert str(q_["answer"]) not in q_["distractors"]
    assert len(q_["distractors"]) >= 3, q_["id"]
    assert len(q_["options"]) == 5 or q_["options"] == ROMAN, q_["id"]
    assert q_["difficulty"] >= 2
print("ALL OK")
