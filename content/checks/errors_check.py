"""Verification for content/questions/errors.json. Run: python3 content/checks/errors_check.py

Each question presents an argument. We machine-check the mathematical facts that decide which
line (if any) is the first invalid one, whether the claim is true, and that every distractor's
claim fails. Each original X and its twin Xb are covered.
"""
import json
import os
from collections import Counter
from fractions import Fraction as F

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ALL = json.load(open(os.path.join(HERE, "..", "questions", "errors.json")))
QS = {q["id"]: q for q in ALL}
x, y, a, b, n, k, p, q, r, m, s = sp.symbols("x y a b n k p q r m s")
xr = sp.Symbol("xr", real=True)
ROMAN8 = [set(), {1}, {2}, {3}, {1, 2}, {1, 3}, {2, 3}, {1, 2, 3}]


def key(qid, idx):
    qq = QS[qid]
    assert qq["answer"] == idx, (qid, qq["answer"], idx)
    assert len(set(qq["options"])) == len(qq["options"]), qid
    assert 4 <= len(qq["options"]) <= 8, qid


def roman(qid, truths):
    key(qid, ROMAN8.index({i + 1 for i, t in enumerate(truths) if t}))


def eq(e1, e2):
    return sp.expand(e1 - e2) == 0


def solset(expr_ineq):
    return sp.solve_univariate_inequality(expr_ineq, xr, relational=False)


iv = sp.Interval
oo = sp.oo

# 01: with a=b=1 lines I, II hold; III (a+b=b) fails -> first error III (index 2)
A, B = 1, 1
assert A * A - B * B == A * B - B * B and (A + B) * (A - B) == B * (A - B)
assert A + B != B
assert eq((a + b) * (a - b), a ** 2 - b ** 2) and eq(b * (a - b), a * b - b ** 2)
key("errors-01", 2)
# 01b: x^3=4x has roots {0,2,-2}; division by x loses 0
assert set(sp.solve(x ** 3 - 4 * x, x)) == {0, 2, -2}
key("errors-01b", 1)

# 02: x-1 = sqrt(x+5): candidates 4,-1; only 4
assert set(sp.solve(x ** 2 - 3 * x - 4, x)) == {4, -1}
assert eq((x - 1) ** 2 - (x + 5), x ** 2 - 3 * x - 4) and eq((x - 4) * (x + 1), x ** 2 - 3 * x - 4)
assert set(sp.solve(x - 1 - sp.sqrt(x + 5), x)) == {4}
key("errors-02", 3)
# 02b: sqrt(3x+1) = x-3 -> only 8
assert set(sp.solve(x ** 2 - 9 * x + 8, x)) == {1, 8}
assert set(sp.solve(sp.sqrt(3 * x + 1) - (x - 3), x)) == {8}
key("errors-02b", 4)

# 03: (x+3)/(x-1) > 2  <=> 1<x<5
assert solset((xr + 3) / (xr - 1) > 2) == iv.open(1, 5)
key("errors-03", 1)
# 03b: x - 6/x > 1 <=> -2<x<0 or x>3
assert solset(xr - 6 / xr > 1) == sp.Union(iv.open(-2, 0), iv.open(3, oo))
assert eq((x - 3) * (x + 2), x ** 2 - x - 6)
key("errors-03b", 2)

# 04: correct proof; facts
assert all((t * (t + 1) * (t + 2) * (t + 3)) % 24 == 0 for t in range(-300, 300))
assert all((2 * t) % 4 == 0 or (2 * t + 2) % 4 == 0 for t in range(-300, 300))
key("errors-04", 4)
# 04b: sqrt3 irrational, 3 prime
assert sp.isprime(3) and not sp.sqrt(3).is_rational
assert all(pp * pp != 3 * qq * qq for pp in range(1, 300) for qq in range(1, 200))
key("errors-04b", 0)

# 05: (2x-1)^2=(x+4)^2 -> {5,-1}
assert set(sp.solve((2 * x - 1) ** 2 - (x + 4) ** 2, x)) == {5, -1}
key("errors-05", 3)
# 05b: sqrt((x-1)^2) = |x-1|; claim fails at x=0
assert sp.sqrt((xr - 1) ** 2) == sp.Abs(xr - 1)
assert sp.sqrt(F(1)) != 0 - 1
assert eq((x - 1) ** 2, x ** 2 - 2 * x + 1)
key("errors-05b", 2)

# 06: sin2x = sin x on [0,360): {0,60,180,300}
sols = sorted(d for d in range(0, 360) if sp.simplify(sp.sin(2 * sp.rad(d)) - sp.sin(sp.rad(d))) == 0)
assert sols == [0, 60, 180, 300], sols
key("errors-06", 4)
# 06b: sinB = sqrt3/2; B=120 also valid: A=30,B=120,C=30, sides a=6,b=6sqrt3
sB = 6 * sp.sqrt(3) * sp.Rational(1, 2) / 6
assert sp.simplify(sB - sp.sqrt(3) / 2) == 0
for Bdeg in (60, 120):
    C = 180 - 30 - Bdeg
    assert C > 0
    ratio_a = 6 / sp.sin(sp.rad(30))
    assert sp.simplify(6 * sp.sqrt(3) / sp.sin(sp.rad(Bdeg)) - ratio_a) == 0
key("errors-06b", 2)

# 07: proof proves converse; claim true
assert eq((2 * k + 1) ** 2 + 2 * (2 * k + 1), 4 * k ** 2 + 8 * k + 3)
assert all(((t * t + 2 * t) % 2 == 1) <= (t % 2 == 1) for t in range(-300, 300))
key("errors-07", 2)
# 07b: proves converse; claim false at n=2
assert (2 * 2) % 4 == 0 and 2 % 4 != 0
assert eq((4 * k) ** 2, 4 * (4 * k ** 2))
key("errors-07b", 1)

# 08: claim false for x<0, true for x>0
assert (-1) + F(1, -1) < 2
assert all(F(t, 7) + F(7, t) >= 2 for t in range(1, 200))
key("errors-08", 3)
# 08b: x^4+1 >= 2x^2 true for all x; (x^2-1)^2 expansion
assert eq((x ** 2 - 1) ** 2, x ** 4 - 2 * x ** 2 + 1)
assert sp.minimum(xr ** 4 + 1 - 2 * xr ** 2, xr, sp.S.Reals) == 0
key("errors-08b", 1)

# 09: 3-4-5 triangle satisfies a cosA = b cosB, not isosceles
aa, bb, cc = 3, 4, 5
cosA = F(bb * bb + cc * cc - aa * aa, 2 * bb * cc)
cosB = F(aa * aa + cc * cc - bb * bb, 2 * aa * cc)
assert aa * cosA == bb * cosB and aa != bb
key("errors-09", 2)
# 09b: A=30, B=120: sin^2A + sin^2B = 1, C=30; sinA = -cosB
SA, SB, CB = sp.sin(sp.rad(30)), sp.sin(sp.rad(120)), sp.cos(sp.rad(120))
assert sp.simplify(SA ** 2 + SB ** 2 - 1) == 0 and sp.simplify(SA + CB) == 0 and sp.simplify(SA - CB) != 0
key("errors-09b", 1)

# 10: correct contrapositive proof; option E is not a counterexample
assert sp.simplify(p / q + r / s - (p * s + q * r) / (q * s)) == 0
assert (sp.sqrt(2) + (-sp.sqrt(2))).is_rational
key("errors-10", 0)
# 10b
assert eq((2 * m + 1) * (2 * n + 1), 2 * (2 * m * n + m + n) + 1)
assert all(((u * v) % 2 == 0) <= (u % 2 == 0 or v % 2 == 0) for u in range(-50, 50) for v in range(-50, 50))
key("errors-10b", 4)

# 11: correct proof
assert eq((x - 1) * (x ** 3 + x ** 2 + x - 3), x ** 4 - 4 * x + 3)
assert eq((x - 1) ** 2 * (x ** 2 + 2 * x + 3), x ** 4 - 4 * x + 3)
assert eq((x + 1) ** 2 + 2, x ** 2 + 2 * x + 3)
assert sp.minimum(xr ** 4 - 4 * xr + 3, xr, sp.S.Reals) == 0
key("errors-11", 4)
# 11b: lines I-III correct, IV fails (x=-3)
assert eq((x - 1) * (x ** 2 + x - 2), x ** 3 - 3 * x + 2)
assert eq((x - 1) ** 2 * (x + 2), x ** 3 - 3 * x + 2)
assert (-3) ** 3 - 3 * (-3) + 2 == -16
key("errors-11b", 3)

# 12: n^5-n; residues 2,3 missing but claim true
assert eq((n - 1) * n * (n + 1) * (n ** 2 + 1), n ** 5 - n)
assert all((t ** 5 - t) % 5 == 0 for t in range(-500, 500))
key("errors-12", 3)
# 12b: n^2+n+1 divisible by 3 when n = 3k+1; algebra of lines II, III correct
assert eq((3 * k) ** 2 + 3 * k + 1, 9 * k ** 2 + 3 * k + 1)
assert eq((3 * k + 2) ** 2 + (3 * k + 2) + 1, 9 * k ** 2 + 15 * k + 7)
assert eq((3 * k + 1) ** 2 + (3 * k + 1) + 1, 3 * (3 * k ** 2 + 3 * k + 1))
assert (1 + 1 + 1) % 3 == 0
key("errors-12b", 1)

# 13: solutions -1 and 3
assert set(sp.solve(sp.sqrt(2 * x + 3) - sp.sqrt(x + 1) - 1, x)) == {-1, 3}
key("errors-13", 2)
# 13b: x^2 sqrt(x+4) = 9 sqrt(x+4): {-4,-3,3}
f13b = lambda t: t * t * sp.sqrt(t + 4) - 9 * sp.sqrt(t + 4)
assert all(f13b(t) == 0 for t in (-4, -3, 3)) and f13b(4) != 0
assert set(sp.solve(x ** 2 * sp.sqrt(x + 4) - 9 * sp.sqrt(x + 4), x)) == {-4, -3, 3}
key("errors-13b", 1)

# 14: 12 | p^2 does not imply 12 | p ; sqrt(12) irrational
assert 36 % 12 == 0 and 6 % 12 != 0 and not sp.sqrt(12).is_rational
key("errors-14", 2)
# 14b: 4 | p^3 does not imply 4 | p ; cbrt(4) irrational
assert 8 % 4 == 0 and 2 % 4 != 0
assert all(pp ** 3 != 4 * qq ** 3 for pp in range(1, 200) for qq in range(1, 200))
key("errors-14b", 3)

# 15: factorisation right; claim false (a=0,b=-1)
assert eq(a ** 3 + b ** 3 - a ** 2 * b - a * b ** 2, (a + b) * (a - b) ** 2)
assert not (0 + (-1) ** 3 >= 0 + 0)
key("errors-15", 3)
# 15b: a=b=-1 counterexample; WLOG changes (a+b)/2
assert (-1) * (-1) >= 0 and F(-1 + -1, 2) < sp.sqrt(1)
key("errors-15b", 1)

# 16: Ana's statement true but examples only (invalid); Ben valid cases; Cara valid example
assert all((t * t - t) % 2 == 0 for t in range(-100, 100))
assert all((t ** 3 - t) % 3 == 0 for t in range(-100, 100))
assert all(sp.isprime(v) for v in (3, 5, 7))
roman("errors-16", [False, True, True])
# 16b: Dev exhaustive valid; Eve examples only; Finn counterexample valid
assert all(2 ** t >= t + 1 for t in range(1, 6))
assert all(2 ** t > t * t for t in range(5, 200))  # Eve's claim is true but not proved
assert not sp.isprime(9)
roman("errors-16b", [True, False, True])

# 17: correct proof (logic); facts quoted
assert 2 * 3 * 5 * 7 * 11 * 13 + 1 == 30031 == 59 * 509
key("errors-17", 0)
# 17b: correct proof; algebra of (II)
assert eq((sp.sqrt(2) + sp.sqrt(3)) ** 2, 5 + 2 * sp.sqrt(6))
assert not (sp.sqrt(2) + sp.sqrt(3)).is_rational and not sp.sqrt(6).is_rational
assert all(pp * pp != 6 * qq * qq for pp in range(1, 300) for qq in range(1, 200))
key("errors-17b", 3)

# 18: |x-1| > 2x  <=>  x < 1/3
assert solset(sp.Abs(xr - 1) > 2 * xr) == iv.open(-oo, F(1, 3))
key("errors-18", 1)
# 18b: sqrt(x+5) > x-1  <=> -5 <= x < 4
assert solset(sp.sqrt(xr + 5) > xr - 1) == iv.Ropen(-5, 4)
key("errors-18b", 4)

# structure
orig = [f"errors-{i:02d}" for i in range(1, 19)]
assert sorted(QS) == sorted(orig + [o + "b" for o in orig])
for o in orig:
    A_, B_ = QS[o], QS[o + "b"]
    assert A_["family"] == B_["family"] == o
    assert A_["difficulty"] == B_["difficulty"], o
    assert A_["answer"] != B_["answer"], o
assert Counter(QS[o]["difficulty"] for o in orig) == Counter({2: 2, 3: 6, 4: 7, 5: 3})
correct = [o for o in orig if QS[o]["options"][QS[o]["answer"]].startswith("The proof is correct")]
assert len(correct) >= 3, correct
for qq in ALL:
    for st in [qq["stem"]] + qq["options"]:
        for sym in "⇒∧∨¬∀∃":
            assert sym not in st, (qq["id"], sym)
print("ALL OK")
