"""Verification for content/questions/errors.json. Run: python3 content/checks/errors_check.py

Each question presents an argument; we machine-check the mathematical facts that decide
which line (if any) is wrong, whether the claim is true, and that distractors' claims fail.
"""
import json
import os
from collections import Counter
from fractions import Fraction as F

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
QS = {q["id"]: q for q in json.load(open(os.path.join(HERE, "..", "questions", "errors.json")))}
x, y, a, b, n, k, p, q, r = sp.symbols("x y a b n k p q r")


def key(qid, idx):
    qq = QS[qid]
    assert qq["answer"] == idx, (qid, qq["answer"], idx)
    assert len(set(qq["options"])) == len(qq["options"]), qid
    assert 4 <= len(qq["options"]) <= 8, qid


def eq(e1, e2):
    return sp.expand(e1 - e2) == 0


# 01: lines I-III valid identities when a=b; IV divides by a-b = 0
assert eq((a + b) * (a - b), a ** 2 - b ** 2)
assert eq(b * (a - b), a * b - b ** 2)
# with a=b=1, line III holds (0=0) but line IV (a+b=b) fails
assert ((1 + 1) * 0 == 1 * 0) and (1 + 1 != 1)
key("errors-01", 3)

# 02: sqrt(x+2)=x -> candidates 2,-1; only 2 genuine
assert set(sp.solve(x + 2 - x ** 2, x)) == {2, -1}
assert set(sp.solve(sp.sqrt(x + 2) - x, x)) == {2}
key("errors-02", 4)

# 03: 1/x < 2  <=>  x<0 or x>1/2
xr = sp.Symbol("xr", real=True)
sol = sp.solve_univariate_inequality(1 / xr < 2, xr, relational=False)
assert sol == sp.Union(sp.Interval.open(-sp.oo, 0), sp.Interval.open(F(1, 2), sp.oo))
key("errors-03", 1)

# 04: correct proof; check identity and claim
assert eq(n ** 3 - n, (n - 1) * n * (n + 1))
assert all((m ** 3 - m) % 6 == 0 for m in range(-300, 300))
key("errors-04", 0)

# 05: claim false (x=1,y=-1); sqrt(x^2)=|x|
assert 1 ** 2 == (-1) ** 2 and 1 != -1
assert sp.sqrt(xr ** 2) == sp.Abs(xr)
key("errors-05", 2)

# 06: correct solution x=4, student's x=5 wrong; line I misapplies law
xp = sp.Symbol("xp", positive=True)
sols = [s for s in sp.solve(sp.log(xp, 2) + sp.log(xp - 2, 2) - 3, xp)]
assert sols == [4]
assert sp.simplify(sp.log(5, 2) + sp.log(3, 2) - 3) != 0
# line II follows from line I: log2(2x-2)=3 -> 2x-2=8
assert sp.solve(sp.Eq(2 * x - 2, 8), x) == [5]
key("errors-06", 0)

# 07: proof proves converse; claim true; algebra in II correct
assert eq((2 * k + 1) ** 2 + 2 * (2 * k + 1), 4 * k ** 2 + 8 * k + 3)
assert eq(4 * k ** 2 + 8 * k + 3, 2 * (2 * k ** 2 + 4 * k + 1) + 1)
assert all(((m * m + 2 * m) % 2 == 1) == (m % 2 == 1) for m in range(-200, 200))
key("errors-07", 2)

# 08: claim false for x<0, true for x>0
assert (-1) + F(1, -1) < 2
assert all(F(t, 7) + F(7, t) >= 2 for t in range(1, 200))
assert eq(x ** 2 - 2 * x + 1, (x - 1) ** 2)
key("errors-08", 3)

# 09: (-8)^(1/3) real cube root = -2 ; ((-8)^2)^(1/6) = 2 ; line III first false equality
assert (-2) ** 3 == -8
assert sp.Integer(64) ** sp.Rational(1, 6) == 2
assert sp.Rational(2, 6) == sp.Rational(1, 3)
key("errors-09", 1)  # line (II): sixth root of (-8)^2 is 2, not -2

# 10: correct proof; option E not a counterexample
assert sp.simplify((p / q + r / sp.Symbol("s")) - (p * sp.Symbol("s") + q * r) / (q * sp.Symbol("s"))) == 0
assert (sp.sqrt(2) + (-sp.sqrt(2))).is_rational
key("errors-10", 0)

# 11: correct proof
assert eq((x - 1) * (x ** 3 + x ** 2 + x - 3), x ** 4 - 4 * x + 3)
assert eq((x - 1) ** 2 * (x ** 2 + 2 * x + 3), x ** 4 - 4 * x + 3)
assert eq((x + 1) ** 2 + 2, x ** 2 + 2 * x + 3)
assert sp.minimum(x ** 4 - 4 * x + 3, x, sp.S.Reals) == 0
key("errors-11", 0)

# 12: factorisation right; residues 2,3 missing; claim true
assert eq((n - 1) * n * (n + 1) * (n ** 2 + 1), n ** 5 - n)
assert all((m ** 5 - m) % 5 == 0 for m in range(-500, 500))
covered = {0, 1, 4}
assert covered != set(range(5)) and all((m * m + 1) % 5 == 0 for m in (2, 3))
key("errors-12", 3)

# 13: solutions are x=-1 and x=3
sols = sp.solve(sp.sqrt(2 * x + 3) - sp.sqrt(x + 1) - 1, x)
assert set(sols) == {-1, 3}
assert sp.sqrt(3) - 1 != 1  # x=0 not a solution
key("errors-13", 2)

# 14: 12 | p^2 does not imply 12 | p ; sqrt(12) irrational
assert 36 % 12 == 0 and 6 % 12 != 0
assert not sp.sqrt(12).is_rational
assert all(pp * pp != 12 * qq * qq for pp in range(1, 400) for qq in range(1, 120))
key("errors-14", 2)

# 15: factorisation right; claim false (a=0,b=-1)
assert eq(a ** 3 + b ** 3 - a ** 2 * b - a * b ** 2, (a + b) * (a - b) ** 2)
assert not (0 + (-1) ** 3 >= 0 + 0)
key("errors-15", 3)

# 16: series diverges: partial sums 2^n - 1
assert all(sum(2 ** i for i in range(m)) == 2 ** m - 1 for m in range(1, 40))
assert sp.summation(sp.Rational(1, 2) ** n, (n, 0, sp.oo)) == 2
key("errors-16", 1)

# 17: correct proof (logic); facts quoted in distractors
assert 2 * 3 * 5 * 7 * 11 * 13 + 1 == 30031 == 59 * 509
key("errors-17", 0)

# 18: |x-1| > 2x  <=>  x < 1/3
sol = sp.solve_univariate_inequality(sp.Abs(xr - 1) > 2 * xr, xr, relational=False)
assert sol == sp.Interval.open(-sp.oo, F(1, 3))
assert not ((-2 - 1) ** 2 > 4 * 4)  # x=-2 satisfies original but not squared version
assert abs(-2 - 1) > 2 * (-2)
key("errors-18", 1)

assert Counter(qq["difficulty"] for qq in QS.values()) == Counter({1: 2, 2: 4, 3: 6, 4: 4, 5: 2})
assert sorted(QS) == [f"errors-{i:02d}" for i in range(1, 19)]
correct = [qid for qid, qq in QS.items() if qq["answer"] == 0 and "correct" in qq["options"][0].lower()]
assert len(correct) >= 3, correct
print("ALL OK")
