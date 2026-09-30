"""Verification for content/questions/alg.json.

For every question the keyed answer is recomputed independently (sympy / brute force)
and compared against the option at the keyed index; distractors are checked to be wrong.
Run: python3 content/checks/alg_check.py
"""
import json
import os
import random
from fractions import Fraction as Fr

import sympy as sp
from sympy import Rational as R, sqrt, symbols, Poly, real_roots, S

HERE = os.path.dirname(os.path.abspath(__file__))
Q = {q["id"]: q for q in json.load(open(os.path.join(HERE, "..", "questions", "alg.json"), encoding="utf-8"))}
x, y, k, u = symbols("x y k u", real=True)
ROMAN = ["none of them", "I only", "II only", "III only", "I and II only",
         "I and III only", "II and III only", "I, II and III"]


def roman_index(I, II, III):
    sel = [n for n, t in zip(["I", "II", "III"], [I, II, III]) if t]
    table = {(): 0, ("I",): 1, ("II",): 2, ("III",): 3, ("I", "II"): 4, ("I", "III"): 5,
             ("II", "III"): 6, ("I", "II", "III"): 7}
    return table[tuple(sel)]


def check_numeric(qid, value, option_values):
    """option_values: sympy values in option order; exactly one equals value and it is keyed."""
    q = Q[qid]
    matches = [i for i, v in enumerate(option_values) if v is not None and sp.simplify(v - value) == 0]
    assert matches == [q["answer"]], (qid, matches, q["answer"])
    # ascending order check for numeric options
    nums = [float(v) for v in option_values if v is not None]
    assert nums == sorted(nums), (qid, "options not ascending")


# alg-01
v = sp.radsimp((sqrt(3) + 1) / (sqrt(3) - 1))
check_numeric("alg-01", v, [2 - sqrt(3), (2 + sqrt(3)) / 2, 1 + sqrt(3), 2 + sqrt(3), 4 + 2 * sqrt(3)])

# alg-02
v = S(8) ** R(2, 3) * S(4) ** R(-1, 2) / S(2) ** -3
check_numeric("alg-02", v, [-64, R(1, 4), 1, 4, 16, 64])

# alg-03
den = 2 * x**2 - 12 * x + 23
assert sp.discriminant(den, x) < 0
mn = sp.minimum(den, x, sp.S.Reals)
v = 20 / mn
check_numeric("alg-03", v, [R(20, 23), R(10, 7), 4, 20, None])

# alg-04
a, b = sp.solve(x**2 - 5 * x + 3, x)
v = sp.simplify(a**3 + b**3)
check_numeric("alg-04", v, [80, 95, 116, 125, 170])

# alg-05
A, B = symbols("A B")
p = x**3 + A * x**2 + B * x - 6
sol = sp.solve([p.subs(x, 2), p.subs(x, -1) + 12], [A, B], dict=True)[0]
v = p.subs(sol).subs(x, 1)
check_numeric("alg-05", v, [-12, -6, -4, 0, 4, 6])
# distractor: sign slip p(-1)=12
sol2 = sp.solve([p.subs(x, 2), p.subs(x, -1) - 12], [A, B], dict=True)[0]
assert p.subs(sol2).subs(x, 1) == -12

# alg-06
f = lambda t: 2 * t + 3
g = lambda t: t**2 - 1
roots = sp.solve(sp.Eq(f(g(x)), g(f(x))), x)
assert len(roots) == 2 and all(r.is_real for r in roots)
check_numeric("alg-06", sp.simplify(sum(roots)), [-12, -6, R(-7, 2), R(7, 2), 6])


# alg-07: brute force over rational k
def n_real_roots(expr):
    P = Poly(expr, x)
    if P.degree() <= 0:
        return 0
    return len(set(real_roots(P)))


def in_opt7(kv, i):
    return [kv < -1 or kv > 4, -1 < kv < 4, -1 < kv < 4 and kv != 0, -4 < kv < 1,
            -4 < kv < 1 and kv != 0, 0 < kv < 4][i]


ks = [Fr(n, 4) for n in range(-40, 41)]
truth = {kv: n_real_roots(R(kv.numerator, kv.denominator) * x**2 + 4 * x + R(kv.numerator, kv.denominator) - 3) == 2 for kv in ks}
good = [i for i in range(6) if all(in_opt7(kv, i) == truth[kv] for kv in ks)]
assert good == [Q["alg-07"]["answer"]], good

# alg-08
m = symbols("m", real=True)
disc = sp.discriminant(x**2 - (1 + m) * x + 4, x)
two = sp.solve_univariate_inequality(disc > 0, m, relational=False)
I = sp.Interval.open(3, sp.oo).is_subset(two)
II = two.is_subset(sp.Interval.open(3, sp.oo))
III = len(sp.solve(sp.Eq(disc, 0), m)) == 1
assert (I, II, III) == (True, False, False)
assert roman_index(I, II, III) == Q["alg-08"]["answer"]

# alg-09: brute force on a fine grid
def opt9(t, i):
    return [0 < t < 3, -2 < t < 3, t < -2 or t > 3, -2 < t < 0 or t > 3, t < -2 or 0 < t < 3, t < -3 or 0 < t < 2][i]


pts = [Fr(n, 8) for n in range(-80, 81) if n != 0]
good = [i for i in range(6) if all((Fr(6) / t > t - 1) == opt9(t, i) for t in pts)]
assert good == [Q["alg-09"]["answer"]], good

# alg-10
sols = sp.solve(9**x - 4 * 3**(x + 1) + 27, x)
sols = [s for s in sols if s.is_real]
check_numeric("alg-10", sp.nsimplify(sum(sols)), [0, 1, 2, 3, 12, 27])
assert sorted(sols) == [1, 2]

# alg-11
fx = x**2 - 6 * x + 11
finv = 3 + sqrt(x - 2)
assert sp.simplify(fx.subs(x, finv) - x) == 0
cands = [(7 - sqrt(5)) / 2, (7 + sqrt(5)) / 2, 2, 3]
works = [c for c in cands if c >= 3 and sp.simplify(fx.subs(x, c) - finv.subs(x, c)) == 0]
assert works == [(7 + sqrt(5)) / 2]
# numerical scan for any other solutions on x >= 3
fl = sp.lambdify(x, fx - finv)
signs = [fl(3 + i / 1000) for i in range(0, 20000)]
changes = sum(1 for s1, s2 in zip(signs, signs[1:]) if s1 * s2 < 0)
assert changes == 1
assert Q["alg-11"]["answer"] == 2

# alg-12
F = lambda t: (2 * t + 1) / (t - 2)
I = sp.solve(sp.Eq(F(x), 2), x) == [] and sp.limit(F(x), x, sp.oo) == 2  # 2 not attained
# every other value is attained: solve F(x)=c for symbolic c != 2
c = symbols("c")
assert sp.simplify(F(sp.solve(sp.Eq(F(x), c), x)[0]) - c) == 0
II = sp.simplify(F(F(x)) - x) == 0
III = len(sp.solve(sp.Eq(F(x), x), x)) == 1
assert roman_index(I, II, III) == Q["alg-12"]["answer"]


# alg-13: brute force over b, c in a grid
def count_real_x(bv, cv):
    P = Poly(x**4 + bv * x**2 + cv, x)
    return len(set(real_roots(P)))


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
assert (I, II, III) == (True, False, True)
assert roman_index(I, II, III) == Q["alg-13"]["answer"]

# alg-14
kk = sp.solve((x**3 - 6 * x**2 + k * x - 6).subs(x, 2), k)[0]
rts = sorted(sp.solve(x**3 - 6 * x**2 + kk * x - 6, x))
assert len(set(rts)) == 3 and rts[1] - rts[0] == rts[2] - rts[1]
check_numeric("alg-14", kk, [-19, 6, 9, 11, 12])
# no other k gives an AP (AP forces middle root 2, which forces k = 11): distractors fail
for bad in [-19, 6, 9, 12]:
    r = sp.Poly(x**3 - 6 * x**2 + bad * x - 6, x).nroots()
    rr = sorted(r, key=lambda z: (sp.re(z), sp.im(z)))
    ok = all(abs(sp.im(z)) < 1e-9 for z in rr) and abs((rr[1] - rr[0]) - (rr[2] - rr[1])) < 1e-9
    assert not ok

# alg-15
sols = sp.solve([y - x**2 + 2, x - y**2 + 2], [x, y], dict=True)
real = {(sp.nsimplify(s[x]), sp.nsimplify(s[y])) for s in sols if s[x].is_real and s[y].is_real}
check_numeric("alg-15", len(real), [0, 1, 2, 3, 4])

# alg-16
pp = sp.interpolate([(1, 1), (2, 2), (3, 3), (4, 5)], x)
assert Poly(pp, x).degree() == 3
check_numeric("alg-16", pp.subs(x, 5), [5, 6, 7, 8, 9, 10])


# alg-17: count real solutions for a range of k (including boundaries)
def count17(kv):
    rs = [r for r in set(real_roots(Poly(u**2 - 2 * u + kv, u))) if r > 0]
    return len(rs)  # each positive u = 2^x gives exactly one x


def opt17(kv, i):
    return [kv == 1, kv < 0, kv <= 0, kv < 0 or kv == 1, kv <= 0 or kv == 1, kv < 1, kv <= 1][i]


kvals = [R(n, 8) for n in range(-24, 25)]
good = [i for i in range(7) if all((count17(kv) == 1) == opt17(kv, i) for kv in kvals)]
assert good == [Q["alg-17"]["answer"]], good


# alg-18: random search for counterexamples to sufficiency + proof of III
def two_distinct(bv, cv):
    return bv * bv - 4 * cv > 0


random.seed(1)
I_ok = II_ok = III_ok = True
for _ in range(200000):
    bv = Fr(random.randint(-60, 60), random.randint(1, 10))
    cv = Fr(random.randint(-60, 60), random.randint(1, 10))
    if bv * bv > 3 * cv and not two_distinct(bv, cv):
        I_ok = False
    if cv < 0 and not two_distinct(bv, cv):
        II_ok = False
    if bv > cv + 1 and not two_distinct(bv, cv):
        III_ok = False
assert not two_distinct(Fr(2), Fr(6, 5)) and Fr(4) > 3 * Fr(6, 5)  # stated counterexample
assert (I_ok, II_ok, III_ok) == (False, True, True)
# III proof: b > c+1 means f(-1) = 1 - b + c < 0
assert sp.expand((x**2 + symbols("b") * x + c).subs(x, -1)) == 1 - symbols("b") + c
assert roman_index(I_ok, II_ok, III_ok) == Q["alg-18"]["answer"]

# structural checks
assert sorted(Q) == [f"alg-{i:02d}" for i in range(1, 19)]
for q in Q.values():
    assert len(set(q["options"])) == len(q["options"])
    assert str(q["answer"]) not in q["distractors"]
print("ALL OK")
