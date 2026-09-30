"""Verification for content/questions/explog.json. Run: python3 content/checks/explog_check.py"""
import json
import math
import os
from fractions import Fraction as F

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
QS = {q["id"]: q for q in json.load(open(os.path.join(HERE, "..", "questions", "explog.json"), encoding="utf-8"))}
x, t = sp.symbols("x t", real=True)
L = lambda base, v: sp.log(v) / sp.log(base)


def key(qid, values, truth):
    q = QS[qid]
    assert len(values) == len(q["options"]), qid
    hits = [i for i, v in enumerate(values) if sp.simplify(sp.nsimplify(v) - sp.nsimplify(truth)) == 0]
    assert hits == [q["answer"]], (qid, hits, q["answer"])
    assert len(set(map(str, values))) == len(values), (qid, "options not distinct")


def key_roman(qid, I, II, III):
    table = {(0, 0, 0): 0, (1, 0, 0): 1, (0, 1, 0): 2, (0, 0, 1): 3, (1, 1, 0): 4,
             (1, 0, 1): 5, (0, 1, 1): 6, (1, 1, 1): 7}
    assert QS[qid]["answer"] == table[(int(I), int(II), int(III))], qid


def key_set(qid, preds, truth, grid):
    """Option i is a predicate; exactly the keyed one must agree with truth on every grid point."""
    hits = [i for i, p in enumerate(preds) if all(p(v) == truth(v) for v in grid)]
    assert hits == [QS[qid]["answer"]], (qid, hits)


# explog-01
v = sp.simplify(sp.expand_log(L(3, 12) + 2 * L(3, 6) - L(3, 16), force=True))
key("explog-01", [1, 2, 3, L(3, 32), 4], v)
assert 3 < math.log(32, 3) < 4  # option ordering

# explog-02
sol = sp.solve(sp.Eq(3 ** (2 * x + 1), 27 ** (x - 1)), x)
assert sol == [4]
key("explog-02", [-4, 1, 2, 4, 5], sol[0])

# explog-03
v = sp.nsimplify(sp.simplify(L(2, 3) * L(3, 5) * L(5, 32)))
key("explog-03", [2, F(5, 2), 5, L(2, 480), 10], v)
assert 5 < math.log2(480) < 10

# explog-04
sols = sp.solve(4**x - 6 * 2**x + 8, x)
assert sorted(sols) == [1, 2]
key("explog-04", [1, 2, 3, 6, 8], sum(sols))

# explog-05
p, qq = math.log(2, 7), math.log(3, 7)  # arbitrary base a = 7
vals = [2 * p + 3 * qq, 3 * p + 2 * qq, 6 * p * qq, p**3 + qq**2, p**3 * qq**2]
hits = [i for i, w in enumerate(vals) if abs(w - math.log(72, 7)) < 1e-12]
assert hits == [QS["explog-05"]["answer"]]

# explog-06
xs = [0.3, 1, 2.5, 7, 40]
I = all(abs((math.log(x_, 3) + 2) - math.log(9 * x_, 3)) < 1e-12 for x_ in xs)
II = all(abs(math.log(9 * x_, 3) - math.log(9 * x_, 3)) < 1e-12 for x_ in xs)  # x -> 9x is stretch sf 1/9
III = all(abs(math.log(x_ + 9, 3) - math.log(9 * x_, 3)) < 1e-12 for x_ in xs)
key_roman("explog-06", I, II, III)

# explog-07
cands = sp.solve(sp.sqrt(x) - (x - 2), x)
valid = [c for c in cands if c > 2 and abs(math.log(c, 4) - math.log(c - 2, 2)) < 1e-12]
assert valid == [4]
# option sets
opts = [{1}, {4}, {1, 4}, {16}, set()]
assert [i for i, s_ in enumerate(opts) if s_ == set(valid)] == [QS["explog-07"]["answer"]]

# explog-08
def truth8(v):
    return v > 1 and math.log(v - 1, 0.5) > -2
grid = [k / 64 + 1 / 128 for k in range(-200, 800)]
key_set("explog-08",
        [lambda v: v > 5, lambda v: v < 5, lambda v: 1 < v < 5, lambda v: 1 < v < 1.25, lambda v: v > 1.25],
        truth8, grid)

# explog-09
key_roman("explog-09", 2**30 > 10**9, 3**20 > 2**30, 5**13 < 10**9)

# explog-10
A, b = sp.symbols("A b", positive=True)
s10 = sp.solve([A * b**2 - 16000, A * b**6 - 4000], [A, b], dict=True)[0]
T = sp.solve(sp.Eq(s10[A] * s10[b] ** t, 1000), t)
key("explog-10", [7, 8, 10, 12, 14], sp.simplify(T[0]))

# explog-11
ts = sp.solve(t + 1 / t - F(5, 2), t)
xs11 = [2**tt for tt in ts]
for xv in xs11:
    assert xv > 0 and xv != 1 and sp.simplify(L(2, xv) + L(xv, 2) - F(5, 2)) == 0
key("explog-11", [1, F(5, 2), 4, 4 * sp.sqrt(2), 8], sp.prod(xs11))

# explog-12
import random
random.seed(1)
pairs = [(random.choice([0.1, 0.5, 2, 3, 10]) * random.random() + 0.01, random.random() * 5 + 0.01) for _ in range(300)]
pairs = [(a_, b_) for a_, b_ in pairs if abs(a_ - 1) > 1e-3 and abs(b_ - 1) > 1e-3]
I = all(abs(math.log(b_, a_) * math.log(a_, b_) - 1) < 1e-9 for a_, b_ in pairs)
II = all(math.log(b_, a_) + math.log(a_, b_) >= 2 - 1e-12 for a_, b_ in pairs + [(2, 0.5)])
III = all(abs(math.log(b_**2, a_**2) - math.log(b_, a_)) < 1e-9 for a_, b_ in pairs)
key_roman("explog-12", I, II, III)

# explog-13
a13, b13, c13 = math.log(3, 2), math.log(4, 3), math.log(5, 4)
assert c13 < b13 < a13
orders = [(a13, b13, c13), (a13, c13, b13), (b13, a13, c13), (c13, a13, b13), (c13, b13, a13)]
assert [i for i, o in enumerate(orders) if o[0] < o[1] < o[2]] == [QS["explog-13"]["answer"]]
assert 3 < F(256, 81) and 3 ** 1.25 < 4 < 3 ** 1.5 and 4 ** 1.25 > 5 and 2 ** 1.5 < 3

# explog-14
grid14 = [k / 50 + 1 / 97 for k in range(0, 400)]
grid14 = [v for v in grid14 if v > 0 and abs(v - 1) > 1e-9]
key_set("explog-14",
        [lambda v: v > 2, lambda v: 1 < v < 2, lambda v: 0 < v < 1 or v > 2, lambda v: 0 < v < 2 and v != 1,
         lambda v: 0 < v < 1 or 1 < v < 2],
        lambda v: math.log(2, v) < 1, grid14)

# explog-15: count solutions via positive roots in y
def nsol15(k):
    return len({r for r in sp.solve(t**2 - k * t + 4, t) if r.is_real and r > 0})
ks = [F(k, 4) for k in range(-40, 41)]
key_set("explog-15",
        [lambda k: k > 0, lambda k: k > 4, lambda k: k >= 4, lambda k: k < -4 or k > 4, lambda k: -4 < k < 4],
        lambda k: nsol15(k) == 2, ks)

# explog-17: count x-solutions; also brute-force sign changes numerically for a few k
def nsol17(k):
    n = 0
    for u in sp.solve(t**2 - 3 * t + k - 2, t):
        if u.is_real:
            if u > 2:
                n += 2
            elif u == 2:
                n += 1
    return n
ks = [F(k, 8) for k in range(-80, 81)] + [F(17, 4), F(33, 8), F(65, 16)]
key_set("explog-17",
        [lambda k: k < 4, lambda k: k <= 4, lambda k: k < F(17, 4), lambda k: 4 < k < F(17, 4), lambda k: k > 4],
        lambda k: nsol17(k) == 2, ks)
for k in [-3, 0, 3.9, 4.1, 4.2, 5]:
    f = lambda z: 4**z + 4**-z + k - 3 * (2**z + 2**-z)
    zs = [i / 1000 for i in range(-8000, 8001)]
    changes = sum(1 for i in range(len(zs) - 1) if f(zs[i]) * f(zs[i + 1]) < 0)
    assert changes == nsol17(F(k).limit_denominator(100)), (k, changes)

# explog-18
def truth18(v):
    if v <= 0 or abs(v - 1) < 1e-12 or 2 * v - 1 <= 0:
        return False
    return math.log(2 * v - 1, v) > 2
grid18 = [k / 64 + 1 / 131 for k in range(-100, 500)]
key_set("explog-18",
        [lambda v: False, lambda v: 0.5 < v < 1, lambda v: v > 1, lambda v: 0.5 < v < 1 or v > 1, lambda v: 0 < v < 1],
        truth18, grid18)

# explog-16
pairs16 = [(a_, b_) for a_ in [0.2, 0.5, 0.9, 1.5, 2, 5] for b_ in [0.1, 0.3, 0.7, 1.2, 1.8, 3] if a_ > b_]
I = all(math.log(a_, 0.5) < math.log(b_, 0.5) for a_, b_ in pairs16)
II = all(0.5**a_ > 0.5**b_ for a_, b_ in pairs16)
III = all(math.log(2, a_) < math.log(2, b_) for a_, b_ in pairs16)
assert not (math.log(2, 2) < math.log(2, 0.5))
key_roman("explog-16", I, II, III)

# metadata checks
diffs = sorted(q["difficulty"] for q in QS.values())
assert diffs == [1] * 2 + [2] * 4 + [3] * 6 + [4] * 4 + [5] * 2, diffs
assert sorted(QS) == [f"explog-{i:02d}" for i in range(1, 19)]
for q in QS.values():
    assert 4 <= len(q["options"]) <= 8 and len(set(q["options"])) == len(q["options"])
    assert 0 <= q["answer"] < len(q["options"])
    assert len(q["distractors"]) >= 2 and all(int(k) != q["answer"] for k in q["distractors"])
print("ALL OK")
